"""Train a five-class RTMPose + ST-GCN++ baseline for 300 epochs per LOSO fold."""

from __future__ import annotations

import argparse
import csv
import json
import math
import random
import sys
from pathlib import Path

import matplotlib
import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader, Dataset

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

PROJECT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT))
from models import build_model  # noqa: E402
from train_vjepa21_posture5_probe import CLASS_NAMES, multiclass_metrics  # noqa: E402


LEFT_RIGHT = [0, 2, 1, 4, 3, 6, 5, 8, 7, 10, 9, 12, 11, 14, 13, 16, 15]


class CompactSkeletonTGCN(nn.Module):
    """Compact graph-temporal classifier used for the rapid five-class control."""

    def __init__(self, num_class: int) -> None:
        super().__init__()
        edges = [
            (0, 1), (0, 2), (1, 3), (2, 4), (0, 5), (0, 6), (5, 6),
            (5, 7), (7, 9), (6, 8), (8, 10), (5, 11), (6, 12), (11, 12),
            (11, 13), (13, 15), (12, 14), (14, 16),
        ]
        adjacency = torch.eye(17)
        for left, right in edges:
            adjacency[left, right] = 1.0; adjacency[right, left] = 1.0
        adjacency /= adjacency.sum(1, keepdim=True)
        self.register_buffer("adjacency", adjacency)
        self.temporal = nn.Sequential(
            nn.Conv1d(6 * 17, 96, kernel_size=7, padding=3, bias=False),
            nn.BatchNorm1d(96), nn.ReLU(inplace=True),
            nn.Conv1d(96, 96, kernel_size=5, padding=2, groups=96, bias=False),
            nn.BatchNorm1d(96), nn.ReLU(inplace=True),
            nn.Conv1d(96, 128, kernel_size=1, bias=False),
            nn.BatchNorm1d(128), nn.ReLU(inplace=True),
        )
        self.classifier = nn.Sequential(nn.AdaptiveAvgPool1d(1), nn.Flatten(), nn.Dropout(0.4), nn.Linear(128, num_class))

    def forward(self, inputs: torch.Tensor) -> torch.Tensor:
        inputs = inputs[..., 0]
        graph = torch.einsum("bctv,vw->bctw", inputs, self.adjacency)
        features = torch.cat((inputs, graph), dim=1).permute(0, 1, 3, 2).flatten(1, 2)
        return self.classifier(self.temporal(features))


class SkeletonSet(Dataset):
    def __init__(self, data: np.ndarray, labels: np.ndarray, names: np.ndarray, mask: np.ndarray,
                 augment: bool) -> None:
        self.data = torch.from_numpy(data[mask].astype(np.float32))
        self.labels = torch.from_numpy(labels[mask].astype(np.int64))
        self.names = names[mask].astype(str).tolist()
        self.augment = augment

    def __len__(self) -> int:
        return len(self.labels)

    def __getitem__(self, index: int) -> tuple[torch.Tensor, torch.Tensor, str]:
        sample = self.data[index].clone()
        return sample, self.labels[index], self.names[index]


def augment_batch(samples: torch.Tensor) -> torch.Tensor:
    """Apply scale, rotation, noise and horizontal flip in one GPU batch."""
    batch = samples.shape[0]
    points = samples[:, :2, :, :, 0].permute(0, 2, 3, 1)
    confidence = samples[:, 2, :, :, 0]
    angles = (-10.0 + 20.0 * torch.rand(batch, device=samples.device)) * (math.pi / 180.0)
    cosine, sine = torch.cos(angles), torch.sin(angles)
    rotation = torch.stack((cosine, -sine, sine, cosine), dim=1).reshape(batch, 2, 2)
    scales = (0.9 + 0.2 * torch.rand(batch, device=samples.device)).reshape(batch, 1, 1, 1)
    points = torch.einsum("btvc,bcq->btvq", points, rotation) * scales
    points += torch.randn_like(points) * 0.01 * (confidence >= 0.2).unsqueeze(-1)
    samples[:, :2, :, :, 0] = points.permute(0, 3, 1, 2)
    flip = torch.rand(batch, device=samples.device) < 0.5
    if flip.any():
        samples[flip, 0] *= -1
        samples[flip] = samples[flip][:, :, :, LEFT_RIGHT, :]
    return samples


@torch.inference_mode()
def evaluate(model: nn.Module, loader: DataLoader, loss_fn: nn.Module, device: str) -> tuple[float, np.ndarray, np.ndarray, list[str]]:
    model.eval(); total_loss = 0.0; labels_all = []; predictions_all = []; names_all = []
    for samples, labels, names in loader:
        samples = samples.to(device); labels = labels.to(device)
        with torch.amp.autocast("cuda", dtype=torch.float16, enabled=device.startswith("cuda")):
            logits = model(samples); loss = loss_fn(logits, labels)
        total_loss += float(loss) * len(labels)
        labels_all.extend(labels.cpu().numpy()); predictions_all.extend(logits.argmax(1).cpu().numpy())
        names_all.extend(names)
    return (
        total_loss / len(loader.dataset), np.asarray(labels_all),
        np.asarray(predictions_all), names_all,
    )


def save_predictions(path: Path, names: list[str], labels: np.ndarray, predictions: np.ndarray) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["segment_id", "label", "class_name", "prediction", "predicted_class"])
        for name, label, prediction in zip(names, labels, predictions, strict=True):
            writer.writerow([name, int(label), CLASS_NAMES[int(label)], int(prediction), CLASS_NAMES[int(prediction)]])


def plot_curves(root: Path) -> None:
    figure, axes = plt.subplots(2, 2, figsize=(14, 9))
    for fold, axis in enumerate(axes.flat, 1):
        with (root / f"fold_{fold}" / "history.csv").open("r", encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
        metrics = json.loads((root / f"fold_{fold}" / "metrics.json").read_text(encoding="utf-8"))
        epoch = [int(row["epoch"]) for row in rows]
        axis.plot(epoch, [float(row["train_loss"]) for row in rows], label="Train loss")
        axis.plot(epoch, [float(row["val_loss"]) for row in rows], label="Validation loss")
        axis.axvline(metrics["best_epoch"], linestyle="--", color="#2a9d62",
                     label=f"Selected epoch: {metrics['best_epoch']}")
        axis.set(title=f"Fold {fold}", xlabel="Epoch", ylabel="Loss"); axis.grid(alpha=0.2)
        second = axis.twinx()
        second.plot(epoch, [float(row["val_macro_recall"]) for row in rows],
                    color="#7a49a5", alpha=0.7, label="Validation macro recall")
        second.set_ylim(-0.02, 1.02); second.set_ylabel("Macro recall")
        handles, labels = axis.get_legend_handles_labels(); handles2, labels2 = second.get_legend_handles_labels()
        axis.legend(handles + handles2, labels + labels2, fontsize=8, loc="best")
    figure.suptitle("RTMPose + compact graph-temporal baseline: 300 epochs", fontsize=15)
    figure.tight_layout(); figure.savefig(root / "learning_curves.png", dpi=180, bbox_inches="tight")
    plt.close(figure)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--epochs", type=int, default=300)
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--learning-rate", type=float, default=3e-4)
    parser.add_argument("--weight-decay", type=float, default=1e-3)
    parser.add_argument("--seed", type=int, default=2027)
    parser.add_argument("--device", default="cuda")
    args = parser.parse_args()
    torch.set_num_threads(min(4, torch.get_num_threads()))
    package = np.load(args.data)
    data = package["data"]; labels = package["labels"].astype(int)
    names = package["names"].astype(str); subjects = package["subjects"].astype(str)
    unique_subjects = sorted(np.unique(subjects), key=int)
    args.output_root.mkdir(parents=True, exist_ok=True)
    all_labels = []; all_predictions = []; fold_summaries = []
    for fold_index, test_subject in enumerate(unique_subjects):
        val_subject = unique_subjects[(fold_index + 1) % len(unique_subjects)]
        train_mask = (subjects != test_subject) & (subjects != val_subject)
        val_mask = subjects == val_subject; test_mask = subjects == test_subject
        random.seed(args.seed + fold_index); np.random.seed(args.seed + fold_index)
        torch.manual_seed(args.seed + fold_index); torch.cuda.manual_seed_all(args.seed + fold_index)
        train_set = SkeletonSet(data, labels, names, train_mask, True)
        val_set = SkeletonSet(data, labels, names, val_mask, False)
        test_set = SkeletonSet(data, labels, names, test_mask, False)
        generator = torch.Generator().manual_seed(args.seed + fold_index)
        train_loader = DataLoader(train_set, batch_size=args.batch_size, shuffle=True, generator=generator)
        val_loader = DataLoader(val_set, batch_size=args.batch_size, shuffle=False)
        test_loader = DataLoader(test_set, batch_size=args.batch_size, shuffle=False)
        model = CompactSkeletonTGCN(len(CLASS_NAMES)).to(args.device)
        counts = np.bincount(labels[train_mask], minlength=len(CLASS_NAMES))
        weights = len(train_set) / (len(CLASS_NAMES) * np.maximum(counts, 1))
        loss_fn = nn.CrossEntropyLoss(
            weight=torch.as_tensor(weights, dtype=torch.float32, device=args.device), label_smoothing=0.05
        )
        optimizer = torch.optim.AdamW(model.parameters(), lr=args.learning_rate, weight_decay=args.weight_decay)
        scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
            optimizer, T_max=args.epochs, eta_min=args.learning_rate / 20
        )
        scaler = torch.amp.GradScaler("cuda", enabled=args.device.startswith("cuda"))
        best_score, best_epoch, best_state = -1.0, 0, None; history = []
        for epoch in range(1, args.epochs + 1):
            model.train(); loss_total = 0.0
            for samples, target, _ in train_loader:
                samples = samples.to(args.device); target = target.to(args.device)
                samples = augment_batch(samples)
                optimizer.zero_grad(set_to_none=True)
                with torch.amp.autocast("cuda", dtype=torch.float16, enabled=args.device.startswith("cuda")):
                    logits = model(samples); loss = loss_fn(logits, target)
                scaler.scale(loss).backward(); scaler.unscale_(optimizer)
                torch.nn.utils.clip_grad_norm_(model.parameters(), 5.0)
                scaler.step(optimizer); scaler.update(); loss_total += float(loss) * len(target)
            scheduler.step()
            val_loss, val_labels, val_predictions, _ = evaluate(model, val_loader, loss_fn, args.device)
            val_metric = multiclass_metrics(val_labels, val_predictions)
            score = float(val_metric["macro_recall_balanced_accuracy"])
            history.append({
                "epoch": epoch, "train_loss": loss_total / len(train_set), "val_loss": val_loss,
                "val_accuracy": val_metric["accuracy"], "val_macro_recall": score,
                "val_macro_f1": val_metric["macro_f1"], "learning_rate": optimizer.param_groups[0]["lr"],
            })
            if score > best_score + 1e-9:
                best_score, best_epoch = score, epoch
                best_state = {key: value.detach().cpu().clone() for key, value in model.state_dict().items()}
            if epoch == 1 or epoch % 25 == 0:
                print(f"fold={fold_index+1} epoch={epoch} val_macro_recall={score:.4f}", flush=True)
        assert best_state is not None; model.load_state_dict(best_state)
        val_loss, val_labels, val_predictions, _ = evaluate(model, val_loader, loss_fn, args.device)
        test_loss, test_labels, test_predictions, test_names = evaluate(model, test_loader, loss_fn, args.device)
        fold_dir = args.output_root / f"fold_{test_subject}"; fold_dir.mkdir(parents=True, exist_ok=True)
        torch.save({"model": best_state, "classes": CLASS_NAMES}, fold_dir / "best.pt")
        with (fold_dir / "history.csv").open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(history[0])); writer.writeheader(); writer.writerows(history)
        save_predictions(fold_dir / "test_predictions.csv", test_names, test_labels, test_predictions)
        summary = {
            "fold": int(test_subject), "epochs_ran": args.epochs, "best_epoch": best_epoch,
            "validation": {"loss": val_loss, **multiclass_metrics(val_labels, val_predictions)},
            "test": {"loss": test_loss, **multiclass_metrics(test_labels, test_predictions)},
        }
        (fold_dir / "metrics.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
        fold_summaries.append(summary); all_labels.append(test_labels); all_predictions.append(test_predictions)
        print(f"fold={test_subject} best_epoch={best_epoch} test_acc={summary['test']['accuracy']:.4f}", flush=True)
    total_labels = np.concatenate(all_labels); total_predictions = np.concatenate(all_predictions)
    summary = {
        "route": "RTMPose + compact graph-temporal five-class control",
        "classes": CLASS_NAMES, "protocol": "four-fold LOSO; next subject validation",
        "epochs": args.epochs, "oof_test": multiclass_metrics(total_labels, total_predictions),
        "folds": fold_summaries,
    }
    (args.output_root / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    plot_curves(args.output_root); print(json.dumps(summary["oof_test"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
