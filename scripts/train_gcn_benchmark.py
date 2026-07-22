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


PROJECT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_DIR))
from models import build_model  # noqa: E402


LEFT_RIGHT = [0, 2, 1, 4, 3, 6, 5, 8, 7, 10, 9, 12, 11, 14, 13, 16, 15]


def seed_everything(seed: int) -> None:
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
                 selected_names: list[str], augment: bool = False) -> None:
        index = {str(name): position for position, name in enumerate(names)}
        missing = [name for name in selected_names if name not in index]
        if missing:
            raise RuntimeError(f"Split contains samples absent from tensor: {missing[:3]}")
        selected = [index[name] for name in selected_names]
        self.data = torch.from_numpy(data[selected].astype(np.float32))
        self.labels = torch.from_numpy(labels[selected].astype(np.int64))
        self.names = selected_names
        self.augment = augment

    def __len__(self) -> int:
        return len(self.labels)

    def __getitem__(self, index: int) -> tuple[torch.Tensor, torch.Tensor, str]:
        sample = self.data[index].clone()
        if self.augment:
            xy = sample[:2]
            confidence = sample[2:3]
            scale = 0.9 + 0.2 * torch.rand(1)
            angle = math.radians(float(-10 + 20 * torch.rand(1)))
            rotation = torch.tensor(
                [[math.cos(angle), -math.sin(angle)], [math.sin(angle), math.cos(angle)]],
                dtype=sample.dtype,
            )
            points = xy[:, :, :, 0].permute(1, 2, 0)
            points = torch.matmul(points, rotation.T) * scale
            valid = confidence[0, :, :, 0] >= 0.2
            points += torch.randn_like(points) * 0.01 * valid[..., None]
            xy[:, :, :, 0] = points.permute(2, 0, 1)
            if torch.rand(1).item() < 0.5:
                sample[0] *= -1
                sample = sample[:, :, LEFT_RIGHT, :]
        return sample, self.labels[index], self.names[index]


def confusion_metrics(labels: list[int], predictions: list[int]) -> dict[str, float | int]:
    labels_array = np.asarray(labels)
    predictions_array = np.asarray(predictions)
    tp = int(np.sum((labels_array == 1) & (predictions_array == 1)))
    tn = int(np.sum((labels_array == 0) & (predictions_array == 0)))
    fp = int(np.sum((labels_array == 0) & (predictions_array == 1)))
    fn = int(np.sum((labels_array == 1) & (predictions_array == 0)))
    safe = lambda numerator, denominator: float(numerator / denominator) if denominator else 0.0
    precision = safe(tp, tp + fp)
    recall = safe(tp, tp + fn)
    specificity = safe(tn, tn + fp)
    return {
        "tp": tp, "tn": tn, "fp": fp, "fn": fn,
        "accuracy": safe(tp + tn, len(labels)),
        "precision": precision,
        "recall": recall,
        "specificity": specificity,
        "f1": safe(2 * precision * recall, precision + recall),
        "balanced_accuracy": (recall + specificity) / 2,
    }


@torch.inference_mode()
def evaluate(model: nn.Module, loader: DataLoader, loss_function: nn.Module,
             device: torch.device, amp: bool) -> tuple[float, dict[str, float | int], list[dict[str, object]]]:
    model.eval()
    loss_total = 0.0
    labels_all: list[int] = []
    predictions_all: list[int] = []
    rows: list[dict[str, object]] = []
    for samples, labels, names in loader:
        samples = samples.to(device, non_blocking=True)
        labels = labels.to(device, non_blocking=True)
        with torch.amp.autocast("cuda", dtype=torch.float16, enabled=amp):
            logits = model(samples)
            loss = loss_function(logits, labels)
        probabilities = torch.softmax(logits.float(), dim=1)[:, 1]
        predictions = torch.argmax(logits, dim=1)
        loss_total += float(loss) * len(labels)
        labels_cpu = labels.cpu().tolist()
        predictions_cpu = predictions.cpu().tolist()
        probabilities_cpu = probabilities.cpu().tolist()
        labels_all.extend(labels_cpu)
        predictions_all.extend(predictions_cpu)
        rows.extend(
            {
                "path": name,
                "label": int(label),
                "prediction": int(prediction),
                "fall_probability": float(probability),
            }
            for name, label, prediction, probability in zip(
                names, labels_cpu, predictions_cpu, probabilities_cpu
            )
        )
    return loss_total / len(loader.dataset), confusion_metrics(labels_all, predictions_all), rows


@torch.inference_mode()
def benchmark_latency(model: nn.Module, sample: torch.Tensor, device: torch.device,
                      iterations: int = 100) -> float:
    model.eval()
    sample = sample[None].to(device)
    for _ in range(20):
        model(sample)
    torch.cuda.synchronize()
    start = time.perf_counter()
    for _ in range(iterations):
        model(sample)
    torch.cuda.synchronize()
    return 1000 * (time.perf_counter() - start) / iterations


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--splits", type=Path, required=True)
    parser.add_argument("--fold", type=int, required=True, choices=(1, 2, 3, 4))
    parser.add_argument("--model", choices=("stgcnpp", "ctrgcn"), required=True)
    parser.add_argument("--pose", choices=("rtmpose", "yolo"), required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--epochs", type=int, default=80)
    parser.add_argument("--patience", type=int, default=20)
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--learning-rate", type=float, default=3e-4)
    parser.add_argument("--weight-decay", type=float, default=1e-3)
    parser.add_argument("--dropout", type=float, default=0.5)
    parser.add_argument("--base-channels", type=int, default=64)
    parser.add_argument("--seed", type=int, default=20260721)
    parser.add_argument("--no-amp", action="store_true")
    args = parser.parse_args()

    seed_everything(args.seed + args.fold)
    torch.set_float32_matmul_precision("high")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    amp = device.type == "cuda" and not args.no_amp
    args.output.mkdir(parents=True, exist_ok=True)

    with np.load(args.data) as archive:
        data = archive["data"]
        labels = archive["labels"]
        names = archive["names"].astype(str)
    fold_dir = args.splits / f"fold_{args.fold}"
    train_set = SkeletonDataset(data, labels, names, read_split(fold_dir / "train.csv"), True)
    val_set = SkeletonDataset(data, labels, names, read_split(fold_dir / "val.csv"), False)
    test_set = SkeletonDataset(data, labels, names, read_split(fold_dir / "test.csv"), False)
    generator = torch.Generator().manual_seed(args.seed + args.fold)
    train_loader = DataLoader(
        train_set, batch_size=args.batch_size, shuffle=True, num_workers=0,
        pin_memory=device.type == "cuda", generator=generator
    )
    val_loader = DataLoader(val_set, batch_size=args.batch_size, shuffle=False, num_workers=0)
    test_loader = DataLoader(test_set, batch_size=args.batch_size, shuffle=False, num_workers=0)

    model = build_model(
        args.model, num_class=2, in_channels=3, num_point=17, num_person=1,
        base_channels=args.base_channels, dropout=args.dropout
    ).to(device)
    train_labels = train_set.labels.numpy()
    counts = np.bincount(train_labels, minlength=2)
    class_weights = len(train_labels) / (2 * np.maximum(counts, 1))
    loss_function = nn.CrossEntropyLoss(
        weight=torch.tensor(class_weights, dtype=torch.float32, device=device),
        label_smoothing=0.05,
    )
    optimizer = torch.optim.AdamW(
        model.parameters(), lr=args.learning_rate, weight_decay=args.weight_decay
    )
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
        optimizer, T_max=max(args.epochs, 1), eta_min=args.learning_rate / 20
    )
    scaler = torch.amp.GradScaler("cuda", enabled=amp)

    best_score = -1.0
    best_epoch = 0
    stale_epochs = 0
    history: list[dict[str, object]] = []
    checkpoint_path = args.output / "best.pt"
    started = time.perf_counter()
    for epoch in range(1, args.epochs + 1):
        model.train()
        loss_total = 0.0
        correct = 0
        for samples, target, _ in train_loader:
            samples = samples.to(device, non_blocking=True)
            target = target.to(device, non_blocking=True)
            optimizer.zero_grad(set_to_none=True)
            with torch.amp.autocast("cuda", dtype=torch.float16, enabled=amp):
                logits = model(samples)
                loss = loss_function(logits, target)
            scaler.scale(loss).backward()
            scaler.unscale_(optimizer)
            torch.nn.utils.clip_grad_norm_(model.parameters(), 5.0)
            scaler.step(optimizer)
            scaler.update()
            loss_total += float(loss.detach()) * len(target)
            correct += int((logits.argmax(1) == target).sum())
        val_loss, val_metrics, _ = evaluate(model, val_loader, loss_function, device, amp)
        score = float(val_metrics["balanced_accuracy"])
        history.append({
            "epoch": epoch,
            "learning_rate": optimizer.param_groups[0]["lr"],
            "train_loss": loss_total / len(train_set),
            "train_accuracy": correct / len(train_set),
            "val_loss": val_loss,
            **{f"val_{key}": value for key, value in val_metrics.items()},
        })
        print(
            f"epoch={epoch:03d} train_loss={history[-1]['train_loss']:.4f} "
            f"val_bal_acc={score:.4f} val_f1={val_metrics['f1']:.4f}", flush=True
        )
        if score > best_score + 1e-6:
            best_score = score
            best_epoch = epoch
            stale_epochs = 0
            torch.save(model.state_dict(), checkpoint_path)
        else:
            stale_epochs += 1
        scheduler.step()
        if stale_epochs >= args.patience:
            print(f"early_stop epoch={epoch}", flush=True)
            break

    model.load_state_dict(torch.load(checkpoint_path, map_location=device, weights_only=True))
    val_loss, val_metrics, val_rows = evaluate(model, val_loader, loss_function, device, amp)
    test_loss, test_metrics, test_rows = evaluate(model, test_loader, loss_function, device, amp)
    latency_ms = benchmark_latency(model, test_set[0][0], device)
    parameters = sum(parameter.numel() for parameter in model.parameters())
    result = {
        "route": f"{args.pose}+{args.model}",
        "pose": args.pose,
        "model": args.model,
        "fold": args.fold,
        "test_subjects": sorted({name.split('/')[0] for name in test_set.names}),
        "best_epoch": best_epoch,
        "epochs_ran": len(history),
        "train_samples": len(train_set),
        "val_samples": len(val_set),
        "test_samples": len(test_set),
        "parameters": parameters,
        "latency_ms_batch1": latency_ms,
        "training_seconds": time.perf_counter() - started,
        "device": str(device),
        "amp": amp,
        "config": {
            "batch_size": args.batch_size,
            "learning_rate": args.learning_rate,
            "weight_decay": args.weight_decay,
            "dropout": args.dropout,
            "base_channels": args.base_channels,
            "seed": args.seed,
        },
        "validation": {"loss": val_loss, **val_metrics},
        "test": {"loss": test_loss, **test_metrics},
    }
    write_csv(args.output / "history.csv", history)
    write_csv(args.output / "validation_predictions.csv", val_rows)
    write_csv(args.output / "test_predictions.csv", test_rows)
    (args.output / "metrics.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
