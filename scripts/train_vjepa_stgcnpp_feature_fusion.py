"""Train a small head on frozen RTMPose/ST-GCN++ and V-JEPA 2.1 features."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

import numpy as np
import torch
from torch import nn

PROJECT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT))
from models import build_model  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skeleton-data", type=Path, required=True)
    parser.add_argument("--splits", type=Path, required=True)
    parser.add_argument("--skeleton-checkpoints", type=Path, required=True)
    parser.add_argument("--vjepa-features", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--epochs", type=int, default=300)
    parser.add_argument("--learning-rate", type=float, default=1e-4)
    parser.add_argument("--weight-decay", type=float, default=1e-2)
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--seed", type=int, default=2027)
    parser.add_argument(
        "--route-name",
        default="Skeleton-GCN frozen features + V-JEPA 2.1-B frozen features",
    )
    return parser.parse_args()


def read_names(path: Path) -> list[str]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [row["path"] for row in csv.DictReader(handle)]


def metric(labels: np.ndarray, predictions: np.ndarray) -> dict[str, float | int]:
    tp = int(np.sum((labels == 1) & (predictions == 1)))
    tn = int(np.sum((labels == 0) & (predictions == 0)))
    fp = int(np.sum((labels == 0) & (predictions == 1)))
    fn = int(np.sum((labels == 1) & (predictions == 0)))
    safe = lambda a, b: float(a / b) if b else 0.0
    precision, recall, specificity = safe(tp, tp + fp), safe(tp, tp + fn), safe(tn, tn + fp)
    return {
        "accuracy": safe(tp + tn, len(labels)), "precision": precision,
        "recall": recall, "specificity": specificity,
        "f1": safe(2 * precision * recall, precision + recall),
        "balanced_accuracy": (recall + specificity) / 2,
        "tp": tp, "tn": tn, "fp": fp, "fn": fn,
    }


@torch.inference_mode()
def skeleton_features(model: nn.Module, data: np.ndarray, device: str) -> np.ndarray:
    outputs = []
    for start in range(0, len(data), 32):
        batch = torch.from_numpy(data[start : start + 32].astype(np.float32)).to(device)
        outputs.append(model.forward_features(batch).float().cpu().numpy())
    return np.concatenate(outputs)


def evaluate(head: nn.Module, x: torch.Tensor, labels: np.ndarray) -> tuple[float, np.ndarray]:
    head.eval()
    with torch.inference_mode():
        logits = head(x)
        loss = nn.functional.cross_entropy(
            logits, torch.as_tensor(labels, dtype=torch.long, device=x.device)
        )
        probability = logits.softmax(1)[:, 1].cpu().numpy()
    return float(loss), probability


def save_predictions(path: Path, names: list[str], labels: np.ndarray, probability: np.ndarray) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["path", "label", "prediction", "fall_probability"])
        for name, label, score in zip(names, labels, probability, strict=True):
            writer.writerow([name, int(label), int(score >= 0.5), float(score)])


def main() -> None:
    args = parse_args()
    args.output_root.mkdir(parents=True, exist_ok=True)
    skeleton_pack = np.load(args.skeleton_data)
    data = skeleton_pack["data"]
    labels = skeleton_pack["labels"].astype(int)
    names = skeleton_pack["names"].astype(str)
    index = {name: position for position, name in enumerate(names)}
    vjepa_pack = np.load(args.vjepa_features)
    vjepa_index = {name: position for position, name in enumerate(vjepa_pack["paths"].astype(str))}
    vjepa_all = vjepa_pack["features"].astype(np.float32)
    if set(index) != set(vjepa_index):
        raise ValueError("Skeleton and V-JEPA packages contain different video paths")
    vjepa_ordered = np.stack([vjepa_all[vjepa_index[name]] for name in names])

    all_labels, all_scores, fold_rows = [], [], []
    for fold in range(1, 5):
        torch.manual_seed(args.seed + fold)
        skeleton = build_model(
            "stgcnpp", num_class=2, in_channels=3, num_point=17,
            num_person=1, base_channels=64, dropout=0.5,
        ).to(args.device)
        checkpoint = args.skeleton_checkpoints / f"fold_{fold}" / "best.pt"
        skeleton.load_state_dict(torch.load(checkpoint, map_location=args.device, weights_only=True))
        skeleton.eval()
        for parameter in skeleton.parameters():
            parameter.requires_grad_(False)
        skeleton_all = skeleton_features(skeleton, data, args.device)

        fold_dir = args.splits / f"fold_{fold}"
        split_names = {split: read_names(fold_dir / f"{split}.csv") for split in ("train", "val", "test")}
        split_indices = {
            split: np.asarray([index[name] for name in selected], dtype=int)
            for split, selected in split_names.items()
        }
        train_idx = split_indices["train"]
        sk_mean, sk_std = skeleton_all[train_idx].mean(0), skeleton_all[train_idx].std(0)
        vj_mean, vj_std = vjepa_ordered[train_idx].mean(0), vjepa_ordered[train_idx].std(0)
        sk_std[sk_std < 1e-6] = 1.0
        vj_std[vj_std < 1e-6] = 1.0
        combined = np.concatenate(
            [(skeleton_all - sk_mean) / sk_std, (vjepa_ordered - vj_mean) / vj_std], axis=1
        ).astype(np.float32)
        tensors = {
            split: torch.from_numpy(combined[selected]).to(args.device)
            for split, selected in split_indices.items()
        }
        split_labels = {split: labels[selected] for split, selected in split_indices.items()}

        head = nn.Linear(combined.shape[1], 2).to(args.device)
        # Start from the already validated skeleton classifier. Standardization
        # changes the equivalent weights and bias; V-JEPA begins as a zero residual.
        with torch.no_grad():
            head.weight.zero_()
            head.weight[:, : skeleton.fc.in_features] = skeleton.fc.weight * torch.from_numpy(sk_std).to(args.device)
            head.bias.copy_(skeleton.fc.bias + skeleton.fc.weight @ torch.from_numpy(sk_mean).to(args.device))
        optimizer = torch.optim.AdamW(head.parameters(), lr=args.learning_rate, weight_decay=args.weight_decay)
        scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=args.epochs)
        train_y = torch.as_tensor(split_labels["train"], dtype=torch.long, device=args.device)
        counts = np.bincount(split_labels["train"], minlength=2)
        weights = len(train_y) / (2 * np.maximum(counts, 1))
        weights_t = torch.as_tensor(weights, dtype=torch.float32, device=args.device)

        best_score = -1.0
        best_epoch = 0
        best_state = {key: value.detach().cpu().clone() for key, value in head.state_dict().items()}
        history = []
        # Epoch zero is the unmodified skeleton decision and remains eligible.
        for epoch in range(0, args.epochs + 1):
            val_loss, val_probability = evaluate(head, tensors["val"], split_labels["val"])
            val_metric = metric(split_labels["val"], val_probability >= 0.5)
            score = float(val_metric["balanced_accuracy"])
            history.append({"epoch": epoch, "val_loss": val_loss, **{f"val_{k}": v for k, v in val_metric.items()}})
            if score > best_score + 1e-9:
                best_score, best_epoch = score, epoch
                best_state = {key: value.detach().cpu().clone() for key, value in head.state_dict().items()}
            if epoch == args.epochs:
                break
            head.train()
            optimizer.zero_grad(set_to_none=True)
            logits = head(tensors["train"])
            loss = nn.functional.cross_entropy(logits, train_y, weight=weights_t, label_smoothing=0.05)
            loss.backward()
            optimizer.step()
            scheduler.step()

        head.load_state_dict(best_state)
        val_loss, val_probability = evaluate(head, tensors["val"], split_labels["val"])
        test_loss, test_probability = evaluate(head, tensors["test"], split_labels["test"])
        test_metric = metric(split_labels["test"], test_probability >= 0.5)
        output_fold = args.output_root / f"fold_{fold}"
        output_fold.mkdir(parents=True, exist_ok=True)
        torch.save({"head": best_state, "skeleton_mean": sk_mean, "skeleton_std": sk_std,
                    "vjepa_mean": vj_mean, "vjepa_std": vj_std}, output_fold / "best.pt")
        with (output_fold / "history.csv").open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(history[0]))
            writer.writeheader(); writer.writerows(history)
        save_predictions(output_fold / "val_predictions.csv", split_names["val"], split_labels["val"], val_probability)
        save_predictions(output_fold / "test_predictions.csv", split_names["test"], split_labels["test"], test_probability)
        row = {"fold": fold, "best_epoch": best_epoch, "validation": {"loss": val_loss, **metric(split_labels["val"], val_probability >= 0.5)}, "test": {"loss": test_loss, **test_metric}}
        (output_fold / "metrics.json").write_text(json.dumps(row, ensure_ascii=False, indent=2), encoding="utf-8")
        fold_rows.append(row); all_labels.append(split_labels["test"]); all_scores.append(test_probability)
        print(f"fold={fold} best_epoch={best_epoch} test_f1={test_metric['f1']:.4f}", flush=True)

    total_labels, total_scores = np.concatenate(all_labels), np.concatenate(all_scores)
    summary = {"route": args.route_name,
               "protocol": "LOSO, validation-selected epoch including epoch-0 skeleton baseline",
               "oof_test": metric(total_labels, total_scores >= 0.5), "folds": fold_rows}
    (args.output_root / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary["oof_test"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
