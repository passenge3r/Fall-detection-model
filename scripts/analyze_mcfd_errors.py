from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np


PROJECT = Path(__file__).resolve().parent.parent
PREDICTIONS = {
    "RTMPose+ST-GCN++": PROJECT / "results/mcfd_external_benchmark/rtmpose_stgcnpp/predictions.csv",
    "YOLO-Pose+ST-GCN++": PROJECT / "results/mcfd_external_benchmark/yolo_stgcnpp/predictions.csv",
    "YOLO-Pose+CTR-GCN": PROJECT / "results/mcfd_external_benchmark/yolo_ctrgcn/predictions.csv",
}
OUTPUT = PROJECT / "results/mcfd_error_analysis"
TEST_CAMERAS = {"2", "4", "5", "6", "7", "8"}


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def roc_auc(labels: np.ndarray, scores: np.ndarray) -> float:
    positives = scores[labels == 1]
    negatives = scores[labels == 0]
    return float(
        np.mean(positives[:, None] > negatives[None, :])
        + 0.5 * np.mean(positives[:, None] == negatives[None, :])
    )


def metrics(labels: np.ndarray, scores: np.ndarray) -> dict[str, float | int]:
    predictions = scores >= 0.5
    tp = int(np.sum(predictions & (labels == 1)))
    tn = int(np.sum(~predictions & (labels == 0)))
    fp = int(np.sum(predictions & (labels == 0)))
    fn = int(np.sum(~predictions & (labels == 1)))
    safe = lambda a, b: a / b if b else 0.0
    precision = safe(tp, tp + fp)
    recall = safe(tp, tp + fn)
    specificity = safe(tn, tn + fp)
    return {
        "samples": len(labels),
        "accuracy": safe(tp + tn, len(labels)),
        "precision": precision,
        "recall": recall,
        "specificity": specificity,
        "f1": safe(2 * precision * recall, precision + recall),
        "balanced_accuracy": (recall + specificity) / 2,
        "roc_auc": roc_auc(labels, scores),
        "tp": tp,
        "tn": tn,
        "fp": fp,
        "fn": fn,
    }


def parse_sample(sample: str) -> tuple[str, int, int]:
    path, interval = sample.rsplit("#f", 1)
    start, end = interval.split("-", 1)
    return path, int(start), int(end)


def main() -> None:
    route_rows = {name: read_rows(path) for name, path in PREDICTIONS.items()}
    reference = next(iter(route_rows.values()))
    samples = np.asarray([row["sample"] for row in reference])
    labels = np.asarray([int(row["label"]) for row in reference], dtype=np.int64)
    cameras = np.asarray([row["camera"] for row in reference])
    scores = {
        name: np.asarray([float(row["ensemble"]) for row in rows], dtype=np.float64)
        for name, rows in route_rows.items()
    }
    for rows in route_rows.values():
        assert [row["sample"] for row in rows] == list(samples)
        assert [int(row["label"]) for row in rows] == list(labels)

    test = np.isin(cameras, list(TEST_CAMERAS))
    combinations = {
        **scores,
        "三路线概率平均": np.mean(np.stack(list(scores.values())), axis=0),
        "两条ST-GCN++概率平均": np.mean(
            np.stack([scores["RTMPose+ST-GCN++"], scores["YOLO-Pose+ST-GCN++"]]), axis=0
        ),
    }
    yolo_pose_rows = read_rows(PROJECT / "data/metadata/mcfd_yolo_t64_c010.csv")
    if len(yolo_pose_rows) != len(reference):
        raise RuntimeError("YOLO pose manifest and prediction rows differ")
    yolo_zero_frames = np.asarray([int(row["zero_pose_frames"]) for row in yolo_pose_rows])
    fully_missing = yolo_zero_frames == 64
    conditional_fallback = scores["YOLO-Pose+ST-GCN++"].copy()
    conditional_fallback[fully_missing] = scores["RTMPose+ST-GCN++"][fully_missing]
    combinations["YOLO-ST，整段无姿态时回退RTMPose-ST"] = conditional_fallback
    fusion_rows = []
    for name, probability in combinations.items():
        fusion_rows.append({"method": name, "scope": "cross_view", **metrics(labels[test], probability[test])})
    majority = np.mean(np.stack([value >= 0.5 for value in scores.values()]), axis=0) >= 0.5
    fusion_rows.append(
        {"method": "三路线多数投票", "scope": "cross_view", **metrics(labels[test], majority[test].astype(float))}
    )

    camera_rows = []
    for route, probability in scores.items():
        for camera in sorted(TEST_CAMERAS, key=int):
            mask = cameras == camera
            camera_rows.append({"route": route, "camera": camera, **metrics(labels[mask], probability[mask])})

    prediction_matrix = np.stack([value >= 0.5 for value in scores.values()])
    common_fn = test & (labels == 1) & np.all(~prediction_matrix, axis=0)
    common_fp = test & (labels == 0) & np.all(prediction_matrix, axis=0)
    yolo_st = scores["YOLO-Pose+ST-GCN++"]
    rtm_st = scores["RTMPose+ST-GCN++"]
    yolo_ctr = scores["YOLO-Pose+CTR-GCN"]
    yolo_unique_correct = test & ((yolo_st >= 0.5) == labels.astype(bool)) & (
        (rtm_st >= 0.5) != labels.astype(bool)
    ) & ((yolo_ctr >= 0.5) != labels.astype(bool))

    mean_score = np.mean(np.stack(list(scores.values())), axis=0)
    selected: list[tuple[str, int]] = []
    for category, mask, descending in (
        ("共同高置信度漏报", common_fn, False),
        ("共同高置信度误报", common_fp, True),
        ("仅YOLO-Pose+ST-GCN++判断正确", yolo_unique_correct, True),
    ):
        indices = np.flatnonzero(mask)
        indices = indices[np.argsort(mean_score[indices])]
        if descending:
            indices = indices[::-1]
        selected.extend((category, int(index)) for index in indices[:2])

    detail_rows = []
    for index in np.flatnonzero(test):
        path, start, end = parse_sample(samples[index])
        predictions = {name: int(value[index] >= 0.5) for name, value in scores.items()}
        if labels[index] == 1 and all(value == 0 for value in predictions.values()):
            category = "共同漏报"
        elif labels[index] == 0 and all(value == 1 for value in predictions.values()):
            category = "共同误报"
        elif len(set(predictions.values())) > 1:
            category = "路线分歧"
        else:
            category = "共同正确"
        detail_rows.append(
            {
                "sample": samples[index], "path": path, "start_frame": start, "end_frame": end,
                "camera": cameras[index], "label": int(labels[index]), "category": category,
                **{f"{name}_probability": f"{value[index]:.8f}" for name, value in scores.items()},
            }
        )

    case_rows = []
    for rank, (category, index) in enumerate(selected, start=1):
        path, start, end = parse_sample(samples[index])
        case_rows.append(
            {
                "case_id": f"case_{rank:02d}", "selection": category, "sample": samples[index],
                "path": path, "start_frame": start, "end_frame": end,
                "camera": cameras[index], "label": int(labels[index]),
                **{f"{name}_probability": f"{value[index]:.8f}" for name, value in scores.items()},
            }
        )

    OUTPUT.mkdir(parents=True, exist_ok=True)
    for filename, rows in (
        ("fusion_summary.csv", fusion_rows),
        ("by_camera.csv", camera_rows),
        ("all_cross_view_samples.csv", detail_rows),
        ("selected_cases.csv", case_rows),
    ):
        with (OUTPUT / filename).open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)

    summary = {
        "cross_view_samples": int(np.sum(test)),
        "common_false_negatives": int(np.sum(common_fn)),
        "common_false_positives": int(np.sum(common_fp)),
        "route_disagreements": int(np.sum(test & (np.min(prediction_matrix, axis=0) != np.max(prediction_matrix, axis=0)))),
        "yolo_stgcnpp_unique_correct": int(np.sum(yolo_unique_correct)),
        "selected_cases": len(case_rows),
        "fully_missing_yolo_cross_view": int(np.sum(test & fully_missing)),
        "fully_missing_yolo_cross_view_adl": int(np.sum(test & fully_missing & (labels == 0))),
        "fully_missing_yolo_cross_view_fall": int(np.sum(test & fully_missing & (labels == 1))),
    }
    (OUTPUT / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
