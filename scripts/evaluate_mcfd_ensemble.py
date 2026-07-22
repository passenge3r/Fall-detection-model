from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

import numpy as np
import torch
from torch.utils.data import DataLoader, TensorDataset


PROJECT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT))
from models import build_model  # noqa: E402


ROUTES = (
    ("rtmpose", "stgcnpp"),
    ("rtmpose", "ctrgcn"),
    ("rtmpose", "posec3d"),
    ("yolo", "stgcnpp"),
    ("yolo", "ctrgcn"),
    ("yolo", "posec3d"),
    ("yolo_bytetrack", "stgcnpp"),
    ("yolo_bytetrack", "ctrgcn"),
    ("yolo_bytetrack", "posec3d"),
)


def roc_auc(labels: np.ndarray, scores: np.ndarray) -> float:
    positives = scores[labels == 1]
    negatives = scores[labels == 0]
    if not len(positives) or not len(negatives):
        return float("nan")
    return float(
        np.mean(positives[:, None] > negatives[None, :])
        + 0.5 * np.mean(positives[:, None] == negatives[None, :])
    )


def metrics(
    labels: np.ndarray, probabilities: np.ndarray, threshold: float = 0.5
) -> dict[str, float | int]:
    predictions = (probabilities >= threshold).astype(np.int64)
    tp = int(np.sum((predictions == 1) & (labels == 1)))
    tn = int(np.sum((predictions == 0) & (labels == 0)))
    fp = int(np.sum((predictions == 1) & (labels == 0)))
    fn = int(np.sum((predictions == 0) & (labels == 1)))
    safe = lambda numerator, denominator: numerator / denominator if denominator else 0.0
    precision = safe(tp, tp + fp)
    recall = safe(tp, tp + fn)
    specificity = safe(tn, tn + fp)
    return {
        "samples": len(labels),
        "threshold": threshold,
        "accuracy": safe(tp + tn, len(labels)),
        "balanced_accuracy": (recall + specificity) / 2,
        "precision": precision,
        "recall": recall,
        "specificity": specificity,
        "f1": safe(2 * precision * recall, precision + recall),
        "false_positive_rate": safe(fp, fp + tn),
        "roc_auc": roc_auc(labels, probabilities),
        "tp": tp,
        "tn": tn,
        "fp": fp,
        "fn": fn,
    }


def select_threshold(labels: np.ndarray, probabilities: np.ndarray) -> tuple[float, dict[str, float | int]]:
    candidates = np.linspace(0.01, 0.99, 99)
    scored = [(float(threshold), metrics(labels, probabilities, float(threshold))) for threshold in candidates]
    return max(
        scored,
        key=lambda item: (
            float(item[1]["balanced_accuracy"]), float(item[1]["f1"]), -abs(item[0] - 0.5)
        ),
    )


@torch.inference_mode()
def predict(model: torch.nn.Module, loader: DataLoader, device: torch.device) -> np.ndarray:
    model.eval()
    output = []
    for (inputs,) in loader:
        logits = model(inputs.to(device, non_blocking=True))
        output.extend(torch.softmax(logits, dim=1)[:, 1].cpu().numpy())
    return np.asarray(output, dtype=np.float64)


def evaluate_route(
    pose: str,
    model_name: str,
    tensor_path: Path,
    checkpoints_root: Path,
    output_root: Path,
    batch_size: int,
    device: torch.device,
) -> dict[str, object]:
    cached = np.load(tensor_path)
    data = cached["data"].astype(np.float32)
    labels = cached["labels"].astype(np.int64)
    names = cached["names"].astype(str)
    cameras = cached["cameras"].astype(str)
    loader = DataLoader(
        TensorDataset(torch.from_numpy(data)), batch_size=batch_size, shuffle=False,
        num_workers=0, pin_memory=True,
    )

    fold_probabilities = []
    fold_metrics = []
    for fold in range(1, 5):
        checkpoint = checkpoints_root / f"{pose}_{model_name}" / f"fold_{fold}" / "best.pt"
        saved = torch.load(checkpoint, map_location=device, weights_only=True)
        state_dict = saved["model"] if isinstance(saved, dict) and "model" in saved else saved
        model = build_model(
            model_name, num_class=2, base_channels=64, dropout=0.5
        ).to(device)
        model.load_state_dict(state_dict)
        probabilities = predict(model, loader, device)
        fold_probabilities.append(probabilities)
        fold_metrics.append({"fold": fold, **metrics(labels, probabilities)})
        del model
        torch.cuda.empty_cache()

    fold_matrix = np.stack(fold_probabilities)
    ensemble = np.mean(fold_matrix, axis=0)
    groups: dict[str, np.ndarray] = {"all": np.ones(len(labels), dtype=bool)}
    for cam in range(1, 9):
        groups[f"cam{cam}"] = cameras == str(cam)
    groups["cross_view_test"] = np.isin(cameras, ["2", "4", "5", "6", "7", "8"])
    fixed_metrics = {group: metrics(labels[mask], ensemble[mask]) for group, mask in groups.items()}
    calibration_mask = groups["cam1"]
    selected_threshold, calibration_metrics = select_threshold(
        labels[calibration_mask], ensemble[calibration_mask]
    )
    calibrated_metrics = {
        group: metrics(labels[mask], ensemble[mask], selected_threshold)
        for group, mask in groups.items()
    }

    route_dir = output_root / f"{pose}_{model_name}"
    route_dir.mkdir(parents=True, exist_ok=True)
    with (route_dir / "predictions.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "sample", "camera", "label", "fold1", "fold2", "fold3", "fold4",
                "ensemble", "prediction_0p5", "prediction_calibrated",
            ]
        )
        for index in range(len(labels)):
            writer.writerow(
                [
                    names[index], cameras[index], int(labels[index]),
                    *[f"{fold_matrix[fold, index]:.8f}" for fold in range(4)],
                    f"{ensemble[index]:.8f}", int(ensemble[index] >= 0.5),
                    int(ensemble[index] >= selected_threshold),
                ]
            )
    result = {
        "pose": pose,
        "model": model_name,
        "tensor": str(tensor_path),
        "ensemble": "mean probability of four subject-independent fold checkpoints",
        "threshold_selection": {
            "source": "cam1 only",
            "objective": "maximum balanced accuracy, then F1",
            "selected": selected_threshold,
            "calibration_metrics": calibration_metrics,
        },
        "fold_metrics": fold_metrics,
        "groups_fixed_0p5": fixed_metrics,
        "groups_calibrated": calibrated_metrics,
    }
    (route_dir / "result.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoints-root", type=Path, default=PROJECT / "results/benchmark")
    parser.add_argument(
        "--output-root", type=Path, default=PROJECT / "results/mcfd_external_benchmark"
    )
    parser.add_argument("--batch-size", type=int, default=32)
    args = parser.parse_args()
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required")

    tensors = {
        "rtmpose": PROJECT / "data/gcn/mcfd_rtmpose_t64.npz",
        "yolo": PROJECT / "data/gcn/mcfd_yolo_t64_c010.npz",
        "yolo_bytetrack": PROJECT / "data/gcn/mcfd_yolo_bytetrack_t64_c010.npz",
    }
    results = []
    for pose, model_name in ROUTES:
        result = evaluate_route(
            pose, model_name, tensors[pose], args.checkpoints_root, args.output_root,
            args.batch_size, torch.device("cuda"),
        )
        results.append(result)
        print(
            f"{pose}+{model_name} threshold={result['threshold_selection']['selected']:.2f} "
            f"fixed_f1={result['groups_fixed_0p5']['cross_view_test']['f1']:.4f} "
            f"calibrated_f1={result['groups_calibrated']['cross_view_test']['f1']:.4f}",
            flush=True,
        )

    summary = []
    for result in results:
        row: dict[str, object] = {"pose": result["pose"], "model": result["model"]}
        row["selected_threshold"] = result["threshold_selection"]["selected"]
        for mode in ("groups_fixed_0p5", "groups_calibrated"):
            prefix = "fixed" if mode == "groups_fixed_0p5" else "calibrated"
            for group in ("all", "cam1", "cam3", "cross_view_test"):
                for metric_name, value in result[mode][group].items():
                    row[f"{prefix}_{group}_{metric_name}"] = value
        summary.append(row)
    args.output_root.mkdir(parents=True, exist_ok=True)
    (args.output_root / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    with (args.output_root / "summary.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(summary[0]))
        writer.writeheader()
        writer.writerows(summary)


if __name__ == "__main__":
    main()
