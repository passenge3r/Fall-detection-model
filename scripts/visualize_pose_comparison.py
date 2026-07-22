from __future__ import annotations

import argparse
import csv
from pathlib import Path

import cv2
import numpy as np


EDGES = [
    (0, 1), (0, 2), (1, 3), (2, 4),
    (5, 6), (5, 7), (7, 9), (6, 8), (8, 10),
    (5, 11), (6, 12), (11, 12),
    (11, 13), (13, 15), (12, 14), (14, 16),
]


def find_row(manifest: Path, video_path: str) -> dict[str, str]:
    with manifest.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    for row in rows:
        if row["path"] == video_path:
            return row
    raise RuntimeError(f"Video not found in {manifest}: {video_path}")


def resolve(path: str, root: Path) -> Path:
    value = Path(path)
    return value if value.is_absolute() else root / value


def draw_pose(image: np.ndarray, pose: np.ndarray, title: str, threshold: float) -> np.ndarray:
    canvas = image.copy()
    valid = pose[:, 2] >= threshold
    for start, end in EDGES:
        if valid[start] and valid[end]:
            p1 = tuple(np.rint(pose[start, :2]).astype(int))
            p2 = tuple(np.rint(pose[end, :2]).astype(int))
            cv2.line(canvas, p1, p2, (60, 220, 60), 3, cv2.LINE_AA)
    for index, point in enumerate(pose):
        if valid[index]:
            center = tuple(np.rint(point[:2]).astype(int))
            cv2.circle(canvas, center, 5, (40, 80, 255), -1, cv2.LINE_AA)
    missing = not bool(np.any(valid))
    color = (40, 40, 255) if missing else (255, 255, 255)
    text = f"{title} | {'NO POSE' if missing else 'pose detected'}"
    cv2.rectangle(canvas, (0, 0), (canvas.shape[1], 42), (0, 0, 0), -1)
    cv2.putText(canvas, text, (12, 29), cv2.FONT_HERSHEY_SIMPLEX, 0.75, color, 2, cv2.LINE_AA)
    return canvas


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--video-path", required=True, help="Manifest-relative video path")
    parser.add_argument("--video-root", type=Path, required=True)
    parser.add_argument("--rtmpose-manifest", type=Path, required=True)
    parser.add_argument("--yolo-manifest", type=Path, required=True)
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--confidence-threshold", type=float, default=0.2)
    parser.add_argument("--fps", type=float, default=8.0)
    args = parser.parse_args()

    rtm_row = find_row(args.rtmpose_manifest, args.video_path)
    yolo_row = find_row(args.yolo_manifest, args.video_path)
    with np.load(resolve(rtm_row["pose_path"], args.project_root)) as cache:
        rtm_pose = cache["keypoints"]
        rtm_indices = cache["frame_indices"]
    with np.load(resolve(yolo_row["pose_path"], args.project_root)) as cache:
        yolo_pose = cache["keypoints"]
        yolo_indices = cache["frame_indices"]
    if not np.array_equal(rtm_indices, yolo_indices):
        raise RuntimeError("The two pose caches do not use identical frame indices")

    capture = cv2.VideoCapture(str(args.video_root / args.video_path))
    if not capture.isOpened():
        raise RuntimeError(f"Cannot open video: {args.video_root / args.video_path}")
    capture.set(cv2.CAP_PROP_POS_FRAMES, int(rtm_indices[0]))
    ok, first = capture.read()
    if not ok:
        raise RuntimeError("Cannot decode first sampled frame")
    height, width = first.shape[:2]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    writer = cv2.VideoWriter(
        str(args.output), cv2.VideoWriter_fourcc(*"mp4v"), args.fps, (width * 2, height)
    )
    if not writer.isOpened():
        raise RuntimeError(f"Cannot create output video: {args.output}")

    for frame_number, index in enumerate(rtm_indices):
        capture.set(cv2.CAP_PROP_POS_FRAMES, int(index))
        ok, frame = capture.read()
        if not ok:
            raise RuntimeError(f"Cannot decode frame {index}")
        left = draw_pose(frame, rtm_pose[frame_number], "RTMPose", args.confidence_threshold)
        right = draw_pose(frame, yolo_pose[frame_number], "YOLO26n-Pose", args.confidence_threshold)
        writer.write(np.concatenate([left, right], axis=1))
    capture.release()
    writer.release()
    print(args.output.resolve())


if __name__ == "__main__":
    main()
