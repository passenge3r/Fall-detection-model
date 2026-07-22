from __future__ import annotations

import argparse
import csv
from pathlib import Path

import cv2
import numpy as np


PROJECT = Path(__file__).resolve().parent.parent
EDGES = [
    (0, 1), (0, 2), (1, 3), (2, 4),
    (5, 6), (5, 7), (7, 9), (6, 8), (8, 10),
    (5, 11), (6, 12), (11, 12),
    (11, 13), (13, 15), (12, 14), (14, 16),
]


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def pose_index(path: Path) -> dict[tuple[str, str, str], dict[str, str]]:
    return {
        (row["path"], row["start_frame"], row["end_frame"]): row
        for row in read_rows(path)
    }


def resolve(path: str) -> Path:
    value = Path(path)
    if value.is_absolute():
        return value
    candidates = (PROJECT / value, PROJECT.parent / value)
    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise FileNotFoundError(f"Cannot resolve pose cache {path}; tried {candidates}")


def draw_pose(image: np.ndarray, pose: np.ndarray, title: str, threshold: float) -> np.ndarray:
    canvas = image.copy()
    valid = pose[:, 2] >= threshold
    for start, end in EDGES:
        if valid[start] and valid[end]:
            p1 = tuple(np.rint(pose[start, :2]).astype(int))
            p2 = tuple(np.rint(pose[end, :2]).astype(int))
            cv2.line(canvas, p1, p2, (50, 220, 70), 2, cv2.LINE_AA)
    for point in pose[valid]:
        cv2.circle(canvas, tuple(np.rint(point[:2]).astype(int)), 4, (40, 80, 255), -1, cv2.LINE_AA)
    state = "NO POSE" if not np.any(valid) else "POSE OK"
    state_color = (30, 30, 255) if not np.any(valid) else (70, 240, 90)
    cv2.rectangle(canvas, (0, 0), (canvas.shape[1], 38), (0, 0, 0), -1)
    cv2.putText(canvas, title, (8, 17), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(canvas, state, (8, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.42, state_color, 1, cv2.LINE_AA)
    return canvas


def add_original_title(image: np.ndarray, case: dict[str, str]) -> np.ndarray:
    canvas = image.copy()
    truth = "FALL" if case["label"] == "1" else "ADL"
    cv2.rectangle(canvas, (0, 0), (canvas.shape[1], 73), (0, 0, 0), -1)
    lines = [
        f"{case['case_id']} | GT={truth} | cam{case['camera']}",
        f"RTM+ST {float(case['RTMPose+ST-GCN++_probability']):.3f}",
        f"YOLO+ST {float(case['YOLO-Pose+ST-GCN++_probability']):.3f}",
        f"YOLO+CTR {float(case['YOLO-Pose+CTR-GCN_probability']):.3f}",
    ]
    for line_number, line in enumerate(lines):
        cv2.putText(
            canvas, line, (7, 16 + 17 * line_number), cv2.FONT_HERSHEY_SIMPLEX,
            0.43, (255, 255, 255), 1, cv2.LINE_AA,
        )
    return canvas


def render_case(
    case: dict[str, str], rtm_row: dict[str, str], yolo_row: dict[str, str],
    video_root: Path, output: Path, threshold: float, fps: float,
) -> tuple[np.ndarray, dict[str, int]]:
    with np.load(resolve(rtm_row["pose_path"])) as cache:
        rtm_pose = cache["keypoints"]
        rtm_indices = cache["frame_indices"]
    with np.load(resolve(yolo_row["pose_path"])) as cache:
        yolo_pose = cache["keypoints"]
        yolo_indices = cache["frame_indices"]
    if not np.array_equal(rtm_indices, yolo_indices):
        raise RuntimeError(f"Mismatched sampled frames: {case['sample']}")

    video_path = video_root / case["path"]
    capture = cv2.VideoCapture(str(video_path))
    if not capture.isOpened():
        raise RuntimeError(f"Cannot open {video_path}")
    capture.set(cv2.CAP_PROP_POS_FRAMES, int(rtm_indices[0]))
    ok, first = capture.read()
    if not ok:
        raise RuntimeError(f"Cannot decode {video_path}")
    height, width = first.shape[:2]
    output.parent.mkdir(parents=True, exist_ok=True)
    writer = cv2.VideoWriter(
        str(output), cv2.VideoWriter_fourcc(*"mp4v"), fps, (width * 3, height)
    )
    if not writer.isOpened():
        raise RuntimeError(f"Cannot create {output}")

    contact_frame = None
    for position, frame_index in enumerate(rtm_indices):
        capture.set(cv2.CAP_PROP_POS_FRAMES, int(frame_index))
        ok, frame = capture.read()
        if not ok:
            raise RuntimeError(f"Cannot decode frame {frame_index}: {video_path}")
        original = add_original_title(frame, case)
        rtm = draw_pose(frame, rtm_pose[position], "RTMPose", threshold)
        yolo = draw_pose(frame, yolo_pose[position], "YOLO-Pose", threshold)
        combined = np.concatenate([original, rtm, yolo], axis=1)
        writer.write(combined)
        if position == len(rtm_indices) // 2:
            contact_frame = combined.copy()
    capture.release()
    writer.release()
    assert contact_frame is not None
    zero_counts = {
        "rtmpose_zero_frames": int(np.sum(np.max(rtm_pose[..., 2], axis=1) == 0)),
        "yolo_zero_frames": int(np.sum(np.max(yolo_pose[..., 2], axis=1) == 0)),
    }
    return contact_frame, zero_counts


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", type=Path, default=PROJECT / "results/mcfd_error_analysis/selected_cases.csv")
    parser.add_argument("--video-root", type=Path, default=PROJECT / "data/raw/MCFD/kaggle")
    parser.add_argument("--rtmpose-manifest", type=Path, default=PROJECT / "data/metadata/mcfd_rtmpose_t64.csv")
    parser.add_argument("--yolo-manifest", type=Path, default=PROJECT / "data/metadata/mcfd_yolo_t64_c010.csv")
    parser.add_argument("--output-dir", type=Path, default=PROJECT / "outputs/mcfd_error_cases")
    parser.add_argument("--confidence-threshold", type=float, default=0.2)
    parser.add_argument("--fps", type=float, default=8.0)
    args = parser.parse_args()

    cases = read_rows(args.cases)
    rtm = pose_index(args.rtmpose_manifest)
    yolo = pose_index(args.yolo_manifest)
    frames = []
    updated_cases = []
    for case in cases:
        key = (case["path"], case["start_frame"], case["end_frame"])
        frame, zero_counts = render_case(
            case, rtm[key], yolo[key], args.video_root,
            args.output_dir / f"{case['case_id']}.mp4", args.confidence_threshold, args.fps,
        )
        frames.append(frame)
        updated_cases.append({**case, **zero_counts})
        print(f"rendered {case['case_id']}: {case['sample']} {zero_counts}", flush=True)

    target_width = max(frame.shape[1] for frame in frames)
    padded = [cv2.copyMakeBorder(frame, 0, 0, 0, target_width - frame.shape[1], cv2.BORDER_CONSTANT) for frame in frames]
    contact_sheet = np.concatenate(padded, axis=0)
    encoded, buffer = cv2.imencode(".jpg", contact_sheet, [cv2.IMWRITE_JPEG_QUALITY, 90])
    if not encoded:
        raise RuntimeError("Cannot encode contact sheet")
    buffer.tofile(args.output_dir / "contact_sheet.jpg")
    with (args.output_dir / "cases_with_pose_quality.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(updated_cases[0]))
        writer.writeheader()
        writer.writerows(updated_cases)


if __name__ == "__main__":
    main()
