from __future__ import annotations

import argparse
import csv
import json
import math
import random
import sys
import time
from pathlib import Path

import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader, Dataset


PROJECT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT))
from models import build_model  # noqa: E402


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


def read_split(path: Path) -> list[str]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [row["path"] for row in csv.DictReader(handle)]


class SkeletonDataset(Dataset):
    def __init__(self, data: np.ndarray, labels: np.ndarray, names: np.ndarray,
                 selected: list[str], augment: bool = False) -> None:
        lookup = {str(name): index for index, name in enumerate(names)}
        missing = [name for name in selected if name not in lookup]
        if missing:
            raise RuntimeError(f"Split contains names absent from tensor: {missing[:3]}")
        self.indices = np.asarray([lookup[name] for name in selected], dtype=np.int64)
        self.data = data
        self.labels = labels
        self.names = names
        self.augment = augment

    def __len__(self) -> int:
        return len(self.indices)

    def __getitem__(self, item: int) -> tuple[torch.Tensor, torch.Tensor, str]:
        index = int(self.indices[item])
        sample = self.data[index].copy()
        if self.augment:
            confidence = sample[2] >= 0.2
            angle = np.random.uniform(-10, 10) * math.pi / 180
            scale = np.random.uniform(0.9, 1.1)
            rotation = np.asarray(
                [[math.cos(angle), -math.sin(angle)], [math.sin(angle), math.cos(angle)]],
                dtype=np.float32,
            ) * scale
            xy = sample[:2, :, :, 0].transpose(1, 2, 0)
            xy = xy @ rotation.T
            noise = np.random.normal(0, 0.01, xy.shape).astype(np.float32)
            xy += noise * confidence[:, :, 0, None]
            sample[:2, :, :, 0] = xy.transpose(2, 0, 1)
        return torch.from_numpy(sample), torch.tensor(int(self.labels[index])), str(self.names[index])


def metrics_from_arrays(labels: np.ndarray, predictions: np.ndarray) -> dict[str, float | int]:
    labels = labels.astype(np.int64)
    predictions = predictions.astype(np.int64)
    tp = int(np.sum((labels == 1) & (predictions == 1)))
    tn = int(np.sum((labels == 0) & (predictions == 0)))
    fp = int(np.sum((labels == 0) & (predictions == 1)))
    fn = int(np.sum((labels == 1) & (predictions == 0)))
    safe = lambda numerator, denominator: float(numerator / denominator) if denominator else 0.0
    recall = safe(tp, tp + fn)
    specificity = safe(tn, tn + fp)
    precision = safe(tp, tp + fp)
    return {
        "accuracy": safe(tp + tn, len(labels)),
        "precision": precision,
        "recall": recall,
        "specificity": specificity,
        "f1": safe(2 * precision * recall, precision + recall),
        "balanced_accuracy": (recall + specificity) / 2,
        "tp": tp,
        "tn": tn,
        "fp": fp,
        "fn": fn,
    }


@torch.inference_mode()
def evaluate(model: nn.Module, loader: DataLoader, criterion: nn.Module,
             device: torch.device) -> tuple[float, dict[str, float | int], list[dict[str, object]]]:
    model.eval()
    total_loss = 0.0
    labels_all: list[int] = []
    predictions_all: list[int] = []
    rows: list[dict[str, object]] = []
    for samples, labels, names in loader:
        samples = samples.to(device, non_blocking=True)
        labels = labels.to(device, non_blocking=True)
        logits = model(samples)
        loss = criterion(logits, labels)
        probabilities = torch.softmax(logits, dim=1)[:, 1]
        predictions = torch.argmax(logits, dim=1)
        total_loss += float(loss) * len(labels)
        cpu_labels = labels.cpu().numpy()
        cpu_predictions = predictions.cpu().numpy()
        cpu_probabilities = probabilities.cpu().numpy()
        labels_all.extend(cpu_labels.tolist())
        predictions_all.extend(cpu_predictions.tolist())
        for name, label, prediction, probability in zip(
            names, cpu_labels, cpu_predictions, cpu_probabilities
        ):
            rows.append({
                "path": name,
                "label": int(label),
                "prediction": int(prediction),
                "fall_probability": float(probability),
            })
    metrics = metrics_from_arrays(np.asarray(labels_all), np.asarray(predictions_all))
    return total_loss / max(len(labels_all), 1), metrics, rows


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


@torch.inference_mode()
def benchmark_latency(model: nn.Module, sample: torch.Tensor, device: torch.device,
                      warmup: int = 20, repeats: int = 100) -> float:
    model.eval()
    sample = sample[None].to(device)
    for _ in range(warmup):
        model(sample)
    if device.type == "cuda":
        torch.cuda.synchronize()
    start = time.perf_counter()
    for _ in range(repeats):
        model(sample)
    if device.type == "cuda":
        torch.cuda.synchronize()
    return (time.perf_counter() - start) * 1000 / repeats


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--splits", type=Path, required=True)
    parser.add_argument("--fold", type=int, choices=(1, 2, 3, 4), required=True)
    parser.add_argument("--model", choices=("stgcnpp", "ctrgcn"), required=True)
    parser.add_argument("--pose", choices=("rtmpose", "yolo"), required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--epochs", type=int, default=80)
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--learning-rate", type=float, default=3e-4)
    parser.add_argument("--weight-decay", type=float, default=1e-3)
    parser.add_argument("--patience", type=int, default=20)
    parser.add_argument(
        "--no-early-stopping", action="store_true",
        help="Run every requested epoch while still saving the best validation checkpoint",
    )
    parser.add_argument("--dropout", type=float, default=0.5)
    parser.add_argument("--base-channels", type=int, default=64)
    parser.add_argument("--seed", type=int, default=2026)
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--no-amp", action="store_true")
    args = parser.parse_args()

    set_seed(args.seed)
    torch.set_float32_matmul_precision("high")
    device = torch.device(args.device if torch.cuda.is_available() else "cpu")
    args.output.mkdir(parents=True, exist_ok=True)
    with np.load(args.data) as package:
        data = package["data"].astype(np.float32)
        labels = package["labels"].astype(np.int64)
        names = package["names"]
    fold_dir = args.splits / f"fold_{args.fold}"
    datasets = {
        split: SkeletonDataset(data, labels, names, read_split(fold_dir / f"{split}.csv"), split == "train")
        for split in ("train", "val", "test")
    }
    loaders = {
        "train": DataLoader(
            datasets["train"], batch_size=args.batch_size, shuffle=True,
            num_workers=0, pin_memory=device.type == "cuda"
        ),
        "val": DataLoader(datasets["val"], batch_size=args.batch_size, shuffle=False, num_workers=0),
        "test": DataLoader(datasets["test"], batch_size=args.batch_size, shuffle=False, num_workers=0),
    }
    model = build_model(
        args.model, num_class=2, base_channels=args.base_channels, dropout=args.dropout
    ).to(device)
    train_labels = labels[datasets["train"].indices]
    counts = np.bincount(train_labels, minlength=2)
    class_weights = len(train_labels) / (2 * np.maximum(counts, 1))
    criterion = nn.CrossEntropyLoss(
        weight=torch.tensor(class_weights, dtype=torch.float32, device=device), label_smoothing=0.05
    )
    optimizer = torch.optim.AdamW(
        model.parameters(), lr=args.learning_rate, weight_decay=args.weight_decay
    )
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=args.epochs)
    amp_enabled = device.type == "cuda" and not args.no_amp
    scaler = torch.amp.GradScaler("cuda", enabled=amp_enabled)

    history: list[dict[str, object]] = []
    best_score = -1.0
    best_epoch = 0
    epochs_without_improvement = 0
    checkpoint_path = args.output / "best.pt"
    for epoch in range(1, args.epochs + 1):
        model.train()
        total_train_loss = 0.0
        for samples, batch_labels, _ in loaders["train"]:
            samples = samples.to(device, non_blocking=True)
            batch_labels = batch_labels.to(device, non_blocking=True)
            optimizer.zero_grad(set_to_none=True)
            with torch.amp.autocast("cuda", enabled=amp_enabled):
                logits = model(samples)
                loss = criterion(logits, batch_labels)
            scaler.scale(loss).backward()
            scaler.unscale_(optimizer)
            torch.nn.utils.clip_grad_norm_(model.parameters(), 5.0)
            scaler.step(optimizer)
            scaler.update()
            total_train_loss += float(loss.detach()) * len(batch_labels)
        scheduler.step()
        val_loss, val_metrics, _ = evaluate(model, loaders["val"], criterion, device)
        train_loss = total_train_loss / len(datasets["train"])
        record = {
            "epoch": epoch,
            "train_loss": train_loss,
            "val_loss": val_loss,
            "lr": optimizer.param_groups[0]["lr"],
            **{f"val_{key}": value for key, value in val_metrics.items()},
        }
        history.append(record)
        score = float(val_metrics["balanced_accuracy"])
        improved = score > best_score + 1e-6
        if improved:
            best_score = score
            best_epoch = epoch
            epochs_without_improvement = 0
            torch.save(model.state_dict(), checkpoint_path)
        else:
            epochs_without_improvement += 1
        print(json.dumps({"epoch": epoch, "train_loss": train_loss, "val_loss": val_loss,
                          "val_bal_acc": score, "val_f1": val_metrics["f1"], "best": improved}), flush=True)
        if not args.no_early_stopping and epochs_without_improvement >= args.patience:
            break

    model.load_state_dict(torch.load(checkpoint_path, map_location=device, weights_only=True))
    val_loss, val_metrics, val_rows = evaluate(model, loaders["val"], criterion, device)
    test_loss, test_metrics, test_rows = evaluate(model, loaders["test"], criterion, device)
    latency = benchmark_latency(model, datasets["test"][0][0], device)
    parameters = sum(parameter.numel() for parameter in model.parameters())
    summary = {
        "route": f"{args.pose}+{args.model}",
        "pose": args.pose,
        "model": args.model,
        "fold": args.fold,
        "seed": args.seed,
        "device": str(device),
        "gpu": torch.cuda.get_device_name(0) if device.type == "cuda" else None,
        "best_epoch": best_epoch,
        "epochs_ran": len(history),
        "parameters": parameters,
        "latency_ms_batch1": latency,
        "samples": {key: len(value) for key, value in datasets.items()},
        "validation": {"loss": val_loss, **val_metrics},
        "test": {"loss": test_loss, **test_metrics},
        "config": {
            "epochs": args.epochs,
            "batch_size": args.batch_size,
            "learning_rate": args.learning_rate,
            "weight_decay": args.weight_decay,
            "patience": args.patience,
            "early_stopping": not args.no_early_stopping,
            "dropout": args.dropout,
            "base_channels": args.base_channels,
            "amp": amp_enabled,
        },
    }
    (args.output / "metrics.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    write_csv(args.output / "history.csv", history)
    write_csv(args.output / "val_predictions.csv", val_rows)
    write_csv(args.output / "test_predictions.csv", test_rows)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
