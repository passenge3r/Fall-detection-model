from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
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


@dataclass(frozen=True)
class Frontend:
    title: str
    manifest: str
    best_route: str
    best_ba: float


FRONTENDS = (
    Frontend("RTMPose", "gmdcsa24_rtmpose_t64.csv", "ST-GCN++", 86.83),
    Frontend(
        "RTMPose + ByteTrack",
        "gmdcsa24_rtmpose_bytetrack_t64.csv",
        "ST-GCN++",
        86.29,
    ),
    Frontend("YOLO-Pose", "gmdcsa24_yolo_t64_c010.csv", "CTR-GCN", 78.79),
    Frontend(
        "YOLO-Pose + ByteTrack",
        "gmdcsa24_yolo_bytetrack_t64_c010.csv",
        "ST-GCN++",
        89.41,
    ),
    Frontend("RTMO", "gmdcsa24_rtmo_t64.csv", "ST-GCN++", 78.15),
    Frontend("Hourglass52", "gmdcsa24_hourglass_t64.csv", "ST-GCN++", 76.89),
    Frontend("OpenPose", "gmdcsa24_openpose_t64.csv", "CTR-GCN", 76.32),
    Frontend("AlphaPose", "gmdcsa24_alphapose_t64.csv", "ST-GCN++", 79.43),
)


def find_row(manifest: Path, video_path: str) -> dict[str, str]:
    with manifest.open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            if row["path"] == video_path:
                return row
    raise RuntimeError(f"Video not found in {manifest}: {video_path}")


def resolve_cache(raw_path: str) -> Path:
    path = Path(raw_path)
    candidates = (path, PROJECT / path, PROJECT.parent / path)
    for candidate in candidates:
        if candidate.is_file():
            return candidate.resolve()
    raise FileNotFoundError(f"Pose cache not found: {raw_path}")


def label_bar(
    canvas: np.ndarray,
    first_line: str,
    second_line: str,
    detected: bool = True,
) -> None:
    cv2.rectangle(canvas, (0, 0), (canvas.shape[1], 58), (0, 0, 0), -1)
    color = (255, 255, 255) if detected else (40, 40, 255)
    cv2.putText(
        canvas,
        first_line,
        (10, 23),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.62,
        color,
        2,
        cv2.LINE_AA,
    )
    cv2.putText(
        canvas,
        second_line,
        (10, 48),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.50,
        (210, 210, 210),
        1,
        cv2.LINE_AA,
    )


def draw_pose(
    frame: np.ndarray,
    pose: np.ndarray,
    frontend: Frontend,
    threshold: float,
    tile_size: tuple[int, int],
) -> np.ndarray:
    canvas = frame.copy()
    valid = pose[:, 2] >= threshold
    for start, end in EDGES:
        if valid[start] and valid[end]:
            p1 = tuple(np.rint(pose[start, :2]).astype(int))
            p2 = tuple(np.rint(pose[end, :2]).astype(int))
            cv2.line(canvas, p1, p2, (60, 220, 60), 3, cv2.LINE_AA)
    for point in pose[valid]:
        cv2.circle(
            canvas,
            tuple(np.rint(point[:2]).astype(int)),
            5,
            (40, 80, 255),
            -1,
            cv2.LINE_AA,
        )
    detected = bool(np.any(valid))
    mean_confidence = float(np.mean(pose[valid, 2])) if detected else 0.0
    label_bar(
        canvas,
        f"{frontend.title} | {'POSE OK' if detected else 'NO POSE'} | conf={mean_confidence:.2f}",
        f"best downstream: {frontend.best_route} | pooled BA={frontend.best_ba:.2f}%",
        detected,
    )
    return cv2.resize(canvas, tile_size, interpolation=cv2.INTER_AREA)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--video-path",
        default="Subject 2/Fall/10.mp4",
        help="Path relative to the GMDCSA24 video root",
    )
    parser.add_argument(
        "--video-root",
        type=Path,
        default=PROJECT / "data/raw/GMDCSA24",
    )
    parser.add_argument(
        "--metadata-root",
        type=Path,
        default=PROJECT / "data/metadata",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=PROJECT / "outputs/previews/subject2_fall10_all_frontends.mp4",
    )
    parser.add_argument(
        "--preview",
        type=Path,
        default=PROJECT / "outputs/previews/subject2_fall10_all_frontends.jpg",
    )
    parser.add_argument("--confidence-threshold", type=float, default=0.2)
    parser.add_argument("--fps", type=float, default=8.0)
    parser.add_argument("--tile-width", type=int, default=640)
    parser.add_argument("--tile-height", type=int, default=360)
    args = parser.parse_args()

    pose_sequences: list[np.ndarray] = []
    reference_indices: np.ndarray | None = None
    for frontend in FRONTENDS:
        row = find_row(args.metadata_root / frontend.manifest, args.video_path)
        with np.load(resolve_cache(row["pose_path"])) as cache:
            poses = cache["keypoints"].astype(np.float32)
            indices = cache["frame_indices"].astype(np.int32)
        if reference_indices is None:
            reference_indices = indices
        elif not np.array_equal(reference_indices, indices):
            raise RuntimeError(
                f"{frontend.title} cache does not use the common sampled frame indices"
            )
        pose_sequences.append(poses)
    assert reference_indices is not None

    video_path = args.video_root / args.video_path
    capture = cv2.VideoCapture(str(video_path))
    if not capture.isOpened():
        raise RuntimeError(f"Cannot open video: {video_path}")
    tile_size = (args.tile_width, args.tile_height)
    output_size = (args.tile_width * 3, args.tile_height * 3)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.preview.parent.mkdir(parents=True, exist_ok=True)
    writer = cv2.VideoWriter(
        str(args.output),
        cv2.VideoWriter_fourcc(*"mp4v"),
        args.fps,
        output_size,
    )
    if not writer.isOpened():
        capture.release()
        raise RuntimeError(f"Cannot create output video: {args.output}")

    preview_frame: np.ndarray | None = None
    preview_score = (-1, -1)
    for sample_number, frame_index in enumerate(reference_indices):
        capture.set(cv2.CAP_PROP_POS_FRAMES, int(frame_index))
        ok, frame = capture.read()
        if not ok:
            writer.release()
            capture.release()
            raise RuntimeError(f"Cannot decode frame {frame_index}: {video_path}")

        original = frame.copy()
        label_bar(
            original,
            f"ORIGINAL | sampled frame {sample_number + 1}/64 | source frame {frame_index}",
            "Same video, same frame, same COCO-17 display threshold",
        )
        tiles = [cv2.resize(original, tile_size, interpolation=cv2.INTER_AREA)]
        tiles.extend(
            draw_pose(
                frame,
                poses[sample_number],
                frontend,
                args.confidence_threshold,
                tile_size,
            )
            for frontend, poses in zip(FRONTENDS, pose_sequences)
        )
        grid = np.concatenate(
            [
                np.concatenate(tiles[0:3], axis=1),
                np.concatenate(tiles[3:6], axis=1),
                np.concatenate(tiles[6:9], axis=1),
            ],
            axis=0,
        )
        writer.write(grid)
        detected_frontends = sum(
            bool(np.any(poses[sample_number, :, 2] >= args.confidence_threshold))
            for poses in pose_sequences
        )
        valid_keypoints = sum(
            int(np.sum(poses[sample_number, :, 2] >= args.confidence_threshold))
            for poses in pose_sequences
        )
        score = (detected_frontends, valid_keypoints)
        if 20 <= sample_number <= 55 and score > preview_score:
            preview_frame = grid
            preview_score = score

    capture.release()
    writer.release()
    if preview_frame is None:
        preview_frame = grid
    encoded, buffer = cv2.imencode(
        ".jpg",
        preview_frame,
        [cv2.IMWRITE_JPEG_QUALITY, 94],
    )
    if not encoded:
        raise RuntimeError(f"Cannot write preview: {args.preview}")
    buffer.tofile(str(args.preview))
    print(args.output.resolve())
    print(args.preview.resolve())


if __name__ == "__main__":
    main()
