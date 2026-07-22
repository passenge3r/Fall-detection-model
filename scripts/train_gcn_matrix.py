from __future__ import annotations

import argparse
import csv
import json
import math
import random
import sys
import time
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset


PROJECT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT))
from fall_models import build_model  # noqa: E402


LEFT_RIGHT = [(1, 2), (3, 4), (5, 6), (7, 8), (9, 10), (11, 12), (13, 14), (15, 16)]


def seed_everything(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


class SkeletonDataset(Dataset):
    def __init__(self, data: np.ndarray, labels: np.ndarray, indices: list[int], augment: bool) -> None:
        self.data = data
        self.labels = labels
        self.indices = indices
        self.augment = augment

    def __len__(self) -> int:
        return len(self.indices)

    def __getitem__(self, item: int) -> tuple[torch.Tensor, torch.Tensor]:
        index = self.indices[item]
        sample = torch.from_numpy(self.data[index].copy())
        if self.augment:
            valid = sample[2:3] > 0
            if torch.rand(()) < 0.5:
                sample[0] = -sample[0]
                for left, right in LEFT_RIGHT:
                    original_left = sample[:, :, left].clone()
                    sample[:, :, left] = sample[:, :, right]
                    sample[:, :, right] = original_left
                valid = sample[2:3] > 0
            scale = torch.empty(()).uniform_(0.9, 1.1)
            translation = torch.empty(2, 1, 1, 1).uniform_(-0.08, 0.08)
            sample[:2] = torch.where(valid.expand_as(sample[:2]), sample[:2] * scale + translation, 0)
            noise = torch.randn_like(sample[:2]) * 0.012
            sample[:2] = torch.where(valid.expand_as(sample[:2]), sample[:2] + noise, 0)
            if torch.rand(()) < 0.25:
                drop = torch.rand(sample.shape[1], sample.shape[2], sample.shape[3]) < 0.025
                sample[:, drop] = 0
        return sample, torch.tensor(int(self.labels[index]), dtype=torch.long)


def read_paths(path: Path) -> list[str]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [row["path"] for row in csv.DictReader(handle)]


def split_indices(names: np.ndarray, fold_dir: Path) -> dict[str, list[int]]:
    lookup = {str(name): index for index, name in enumerate(names)}
    output = {}
    for split in ("train", "val", "test"):
        paths = read_paths(fold_dir / f"{split}.csv")
        missing = [path for path in paths if path not in lookup]
        if missing:
            raise RuntimeError(f"Missing {split} samples: {missing[:3]}")
        output[split] = [lookup[path] for path in paths]
    if set(output["train"]) & set(output["val"]) or set(output["train"]) & set(output["test"]):
        raise RuntimeError(f"Split overlap in {fold_dir}")
    return output


def roc_auc(labels: np.ndarray, scores: np.ndarray) -> float:
    positives = scores[labels == 1]
    negatives = scores[labels == 0]
    if not len(positives) or not len(negatives):
        return float("nan")
    return float(np.mean(positives[:, None] > negatives[None, :]) + 0.5 * np.mean(positives[:, None] == negatives[None, :]))


def metrics(labels: np.ndarray, probabilities: np.ndarray) -> dict[str, float | int]:
    predictions = (probabilities >= 0.5).astype(np.int64)
    tp = int(np.sum((predictions == 1) & (labels == 1)))
    tn = int(np.sum((predictions == 0) & (labels == 0)))
    fp = int(np.sum((predictions == 1) & (labels == 0)))
    fn = int(np.sum((predictions == 0) & (labels == 1)))
    safe = lambda numerator, denominator: numerator / denominator if denominator else 0.0
    precision = safe(tp, tp + fp)
    recall = safe(tp, tp + fn)
    specificity = safe(tn, tn + fp)
    return {
        "accuracy": safe(tp + tn, len(labels)),
        "balanced_accuracy": (recall + specificity) / 2,
        "precision": precision,
        "recall": recall,
        "specificity": specificity,
        "f1": safe(2 * precision * recall, precision + recall),
        "false_positive_rate": safe(fp, fp + tn),
        "roc_auc": roc_auc(labels, probabilities),
        "tp": tp, "tn": tn, "fp": fp, "fn": fn,
    }


@torch.inference_mode()
def evaluate(model: nn.Module, loader: DataLoader, device: torch.device) -> tuple[dict, np.ndarray, np.ndarray]:
    model.eval()
    labels, probabilities = [], []
    for inputs, targets in loader:
        logits = model(inputs.to(device, non_blocking=True))
        probabilities.extend(torch.softmax(logits, dim=1)[:, 1].cpu().numpy())
        labels.extend(targets.numpy())
    label_array = np.asarray(labels, dtype=np.int64)
    probability_array = np.asarray(probabilities, dtype=np.float64)
    return metrics(label_array, probability_array), label_array, probability_array


@torch.inference_mode()
def latency_ms(model: nn.Module, sample: torch.Tensor, device: torch.device) -> float:
    model.eval()
    sample = sample[:1].to(device)
    for _ in range(20):
        model(sample)
    torch.cuda.synchronize()
    start = time.perf_counter()
    for _ in range(100):
        model(sample)
    torch.cuda.synchronize()
    return (time.perf_counter() - start) * 10


@dataclass
class RunConfig:
    pose: str
    model: str
    fold: int
    tensor_path: Path
    output_root: Path
    epochs: int
    batch_size: int
    patience: int
    learning_rate: float
    seed: int


def train_run(config: RunConfig, device: torch.device) -> dict[str, object]:
    seed = config.seed + config.fold
    seed_everything(seed)
    cached = np.load(config.tensor_path)
    data = cached["data"].astype(np.float32)
    labels = cached["labels"].astype(np.int64)
    names = cached["names"]
    indices = split_indices(names, PROJECT / "data/splits/gmdcsa24_loso" / f"fold_{config.fold}")
    loaders = {
        split: DataLoader(
            SkeletonDataset(data, labels, split_indices_, augment=split == "train"),
            batch_size=config.batch_size,
            shuffle=split == "train",
            num_workers=0,
            pin_memory=True,
            drop_last=False,
        )
        for split, split_indices_ in indices.items()
    }

    model = build_model(config.model, dropout=0.25).to(device)
    parameters = sum(parameter.numel() for parameter in model.parameters())
    train_labels = labels[indices["train"]]
    counts = np.bincount(train_labels, minlength=2)
    class_weights = len(train_labels) / (2 * np.maximum(counts, 1))
    criterion = nn.CrossEntropyLoss(
        weight=torch.tensor(class_weights, dtype=torch.float32, device=device), label_smoothing=0.05
    )
    optimizer = torch.optim.AdamW(model.parameters(), lr=config.learning_rate, weight_decay=1e-4)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=config.epochs, eta_min=1e-5)
    scaler = torch.amp.GradScaler("cuda")

    run_dir = config.output_root / f"{config.pose}_{config.model}" / f"fold_{config.fold}"
    run_dir.mkdir(parents=True, exist_ok=True)
    checkpoint = run_dir / "best.pt"
    history = []
    best_key = (-1.0, -1.0, -1.0)
    best_epoch = 0
    stale = 0
    started = time.perf_counter()
    for epoch in range(1, config.epochs + 1):
        model.train()
        losses = []
        for inputs, targets in loaders["train"]:
            inputs = inputs.to(device, non_blocking=True)
            targets = targets.to(device, non_blocking=True)
            optimizer.zero_grad(set_to_none=True)
            with torch.amp.autocast("cuda"):
                logits = model(inputs)
                loss = criterion(logits, targets)
            scaler.scale(loss).backward()
            scaler.unscale_(optimizer)
            torch.nn.utils.clip_grad_norm_(model.parameters(), 5.0)
            scaler.step(optimizer)
            scaler.update()
            losses.append(float(loss.detach()))
        scheduler.step()
        val_metrics, _, _ = evaluate(model, loaders["val"], device)
        key = (float(val_metrics["f1"]), float(val_metrics["balanced_accuracy"]), float(val_metrics["accuracy"]))
        history.append({"epoch": epoch, "loss": float(np.mean(losses)), "lr": scheduler.get_last_lr()[0], **val_metrics})
        if key > best_key:
            best_key = key
            best_epoch = epoch
            stale = 0
            torch.save({"model": model.state_dict(), "epoch": epoch, "config": config.__dict__}, checkpoint)
        else:
            stale += 1
        if epoch == 1 or epoch % 10 == 0:
            print(
                f"{config.pose}/{config.model}/fold{config.fold} epoch={epoch} "
                f"loss={np.mean(losses):.4f} val_f1={val_metrics['f1']:.4f}", flush=True
            )
        if stale >= config.patience:
            break

    saved = torch.load(checkpoint, map_location=device, weights_only=False)
    model.load_state_dict(saved["model"])
    val_metrics, _, _ = evaluate(model, loaders["val"], device)
    test_metrics, test_labels, test_probabilities = evaluate(model, loaders["test"], device)
    test_names = [str(names[index]) for index in indices["test"]]
    with (run_dir / "test_predictions.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["path", "label", "fall_probability", "prediction"])
        for name, label, probability in zip(test_names, test_labels, test_probabilities):
            writer.writerow([name, int(label), f"{probability:.8f}", int(probability >= 0.5)])
    (run_dir / "history.json").write_text(json.dumps(history, indent=2) + "\n", encoding="utf-8")
    result = {
        "pose": config.pose,
        "model": config.model,
        "fold": config.fold,
        "seed": seed,
        "best_epoch": best_epoch,
        "epochs_ran": len(history),
        "parameters": parameters,
        "latency_ms_clip": latency_ms(model, torch.from_numpy(data[indices["test"][:1]]), device),
        "training_seconds": time.perf_counter() - started,
        "train_samples": len(indices["train"]),
        "val_samples": len(indices["val"]),
        "test_samples": len(indices["test"]),
        "val": val_metrics,
        "test": test_metrics,
    }
    (run_dir / "result.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result), flush=True)
    del model, optimizer, scaler
    torch.cuda.empty_cache()
    return result


def aggregate(results: list[dict[str, object]], output_root: Path) -> None:
    grouped: dict[tuple[str, str], list[dict[str, object]]] = {}
    for result in results:
        grouped.setdefault((str(result["pose"]), str(result["model"])), []).append(result)
    rows = []
    metric_names = [
        "accuracy", "balanced_accuracy", "precision", "recall", "specificity", "f1",
        "false_positive_rate", "roc_auc",
    ]
    for (pose, model), runs in grouped.items():
        row: dict[str, object] = {
            "pose": pose,
            "model": model,
            "folds": len(runs),
            "parameters": runs[0]["parameters"],
            "latency_ms_clip_mean": float(np.mean([r["latency_ms_clip"] for r in runs])),
            "training_seconds_total": float(np.sum([r["training_seconds"] for r in runs])),
        }
        for metric_name in metric_names:
            values = [float(r["test"][metric_name]) for r in runs]  # type: ignore[index]
            row[f"{metric_name}_mean"] = float(np.mean(values))
            row[f"{metric_name}_std"] = float(np.std(values, ddof=1)) if len(values) > 1 else 0.0
        pooled_labels = []
        pooled_probabilities = []
        for run in runs:
            prediction_path = (
                output_root / f"{pose}_{model}" / f"fold_{run['fold']}" / "test_predictions.csv"
            )
            with prediction_path.open("r", encoding="utf-8-sig", newline="") as handle:
                for prediction in csv.DictReader(handle):
                    pooled_labels.append(int(prediction["label"]))
                    pooled_probabilities.append(float(prediction["fall_probability"]))
        pooled = metrics(
            np.asarray(pooled_labels, dtype=np.int64),
            np.asarray(pooled_probabilities, dtype=np.float64),
        )
        row["test_samples_pooled"] = len(pooled_labels)
        for name, value in pooled.items():
            row[f"pooled_{name}"] = value
        rows.append(row)
    output_root.mkdir(parents=True, exist_ok=True)
    (output_root / "summary.json").write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")
    with (output_root / "summary.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--poses", nargs="+", choices=("rtmpose", "yolo"), default=("rtmpose", "yolo"))
    parser.add_argument("--models", nargs="+", choices=("stgcnpp", "ctrgcn"), default=("stgcnpp", "ctrgcn"))
    parser.add_argument("--folds", nargs="+", type=int, default=(1, 2, 3, 4))
    parser.add_argument("--epochs", type=int, default=100)
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--patience", type=int, default=25)
    parser.add_argument("--learning-rate", type=float, default=0.002)
    parser.add_argument("--seed", type=int, default=20260721)
    parser.add_argument("--output-root", type=Path, default=PROJECT / "results/gcn_matrix")
    parser.add_argument("--summarize-only", action="store_true")
    args = parser.parse_args()

    if args.summarize_only:
        existing = []
        for pose in args.poses:
            for model in args.models:
                for fold in args.folds:
                    result_path = args.output_root / f"{pose}_{model}" / f"fold_{fold}" / "result.json"
                    if not result_path.is_file():
                        raise FileNotFoundError(result_path)
                    existing.append(json.loads(result_path.read_text(encoding="utf-8")))
        aggregate(existing, args.output_root)
        return

    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required for the benchmark matrix")
    tensor_paths = {
        "rtmpose": PROJECT / "data/gcn/gmdcsa24_rtmpose_t64.npz",
        "yolo": PROJECT / "data/gcn/gmdcsa24_yolo_t64_c010.npz",
    }
    device = torch.device("cuda")
    results = []
    for pose in args.poses:
        for model in args.models:
            for fold in args.folds:
                results.append(
                    train_run(
                        RunConfig(
                            pose=pose, model=model, fold=fold, tensor_path=tensor_paths[pose],
                            output_root=args.output_root, epochs=args.epochs,
                            batch_size=args.batch_size, patience=args.patience,
                            learning_rate=args.learning_rate, seed=args.seed,
                        ),
                        device,
                    )
                )
                aggregate(results, args.output_root)
    aggregate(results, args.output_root)


if __name__ == "__main__":
    main()
