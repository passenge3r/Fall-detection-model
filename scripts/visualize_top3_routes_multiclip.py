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
DEFAULT_CLIPS = (
    "Subject 1/Fall/01.mp4",  # all three routes detect correctly
    "Subject 2/Fall/12.mp4",  # rank 1 misses; ranks 2 and 3 detect
    "Subject 3/Fall/05.mp4",  # rank 3 misses
    "Subject 4/Fall/08.mp4",  # rank 2 misses
    "Subject 4/Fall/03.mp4",  # all three routes detect correctly
)


@dataclass(frozen=True)
class Route:
    rank: str
    title: str
    result_dir: str
    manifest: str
    balanced_accuracy: float


ROUTES = (
    Route(
        "1",
        "YOLO-Pose + ByteTrack + ST-GCN++",
        "yolo_bytetrack_stgcnpp",
        "gmdcsa24_yolo_bytetrack_t64_c010.csv",
        89.41,
    ),
    Route(
        "2",
        "RTMPose + ST-GCN++",
        "rtmpose_stgcnpp",
        "gmdcsa24_rtmpose_t64.csv",
        86.83,
    ),
    Route(
        "3 (tied)",
        "RTMPose + ByteTrack + ST-GCN++",
        "rtmpose_bytetrack_stgcnpp",
        "gmdcsa24_rtmpose_bytetrack_t64.csv",
        86.29,
    ),
)


def read_manifest(manifest: Path) -> dict[str, dict[str, str]]:
    with manifest.open("r", encoding="utf-8-sig", newline="") as handle:
        return {row["path"]: row for row in csv.DictReader(handle)}


def read_predictions(route: Route) -> dict[str, dict[str, str]]:
    predictions: dict[str, dict[str, str]] = {}
    result_root = PROJECT / "results/benchmark_e300_full" / route.result_dir
    for fold in range(1, 5):
        path = result_root / f"fold_{fold}" / "test_predictions.csv"
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            for row in csv.DictReader(handle):
                predictions[row["path"]] = {**row, "fold": str(fold)}
    return predictions


def resolve_cache(raw_path: str) -> Path:
    path = Path(raw_path)
    for candidate in (path, PROJECT / path, PROJECT.parent / path):
        if candidate.is_file():
            return candidate.resolve()
    raise FileNotFoundError(f"Pose cache not found: {raw_path}")


def put_line(
    image: np.ndarray,
    text: str,
    y: int,
    color: tuple[int, int, int],
    scale: float = 0.54,
) -> None:
    cv2.putText(
        image,
        text,
        (10, y),
        cv2.FONT_HERSHEY_SIMPLEX,
        scale,
        color,
        2 if scale >= 0.54 else 1,
        cv2.LINE_AA,
    )


def draw_original(
    frame: np.ndarray,
    clip_number: int,
    clip_count: int,
    clip_path: str,
    sample_number: int,
    sample_count: int,
    tile_size: tuple[int, int],
) -> np.ndarray:
    canvas = frame.copy()
    cv2.rectangle(canvas, (0, 0), (canvas.shape[1], 76), (0, 0, 0), -1)
    put_line(canvas, f"ORIGINAL | clip {clip_number}/{clip_count}", 23, (255, 255, 255), 0.62)
    put_line(canvas, clip_path, 48, (210, 210, 210), 0.50)
    put_line(
        canvas,
        f"synchronized sample {sample_number + 1}/{sample_count}",
        69,
        (180, 180, 180),
        0.45,
    )
    return cv2.resize(canvas, tile_size, interpolation=cv2.INTER_AREA)


def draw_route(
    frame: np.ndarray,
    pose: np.ndarray,
    route: Route,
    prediction: dict[str, str],
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

    probability = float(prediction["fall_probability"])
    predicted_fall = int(prediction["prediction"]) == 1
    correct = predicted_fall  # Every clip in this comparison is a fall.
    status = "FALL / CORRECT" if correct else "ADL / MISSED FALL"
    status_color = (60, 220, 60) if correct else (30, 30, 255)
    pose_status = "POSE OK" if np.any(valid) else "NO POSE"
    cv2.rectangle(canvas, (0, 0), (canvas.shape[1], 76), (0, 0, 0), -1)
    put_line(
        canvas,
        f"Rank {route.rank} | {route.title}",
        23,
        (255, 255, 255),
        0.57,
    )
    put_line(
        canvas,
        f"clip p(fall)={probability:.3f} | {status}",
        48,
        status_color,
        0.53,
    )
    put_line(
        canvas,
        f"{pose_status} | pooled BA={route.balanced_accuracy:.2f}% | test fold={prediction['fold']}",
        69,
        (210, 210, 210) if np.any(valid) else (30, 30, 255),
        0.43,
    )
    return cv2.resize(canvas, tile_size, interpolation=cv2.INTER_AREA)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--clips", nargs="+", default=list(DEFAULT_CLIPS))
    parser.add_argument(
        "--video-root",
        type=Path,
        default=PROJECT / "data/raw/GMDCSA24",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=PROJECT / "outputs/previews/top3_routes_five_falls.mp4",
    )
    parser.add_argument(
        "--preview",
        type=Path,
        default=PROJECT / "outputs/previews/top3_routes_five_falls.jpg",
    )
    parser.add_argument("--confidence-threshold", type=float, default=0.2)
    parser.add_argument("--fps", type=float, default=8.0)
    parser.add_argument("--tile-width", type=int, default=640)
    parser.add_argument("--tile-height", type=int, default=360)
    args = parser.parse_args()

    manifests = {
        route.result_dir: read_manifest(PROJECT / "data/metadata" / route.manifest)
        for route in ROUTES
    }
    predictions = {route.result_dir: read_predictions(route) for route in ROUTES}
    tile_size = (args.tile_width, args.tile_height)
    output_size = (args.tile_width * 2, args.tile_height * 2)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.preview.parent.mkdir(parents=True, exist_ok=True)
    writer = cv2.VideoWriter(
        str(args.output),
        cv2.VideoWriter_fourcc(*"mp4v"),
        args.fps,
        output_size,
    )
    if not writer.isOpened():
        raise RuntimeError(f"Cannot create output video: {args.output}")

    preview_frame: np.ndarray | None = None
    for clip_number, clip_path in enumerate(args.clips, 1):
        sequences: list[np.ndarray] = []
        reference_indices: np.ndarray | None = None
        route_predictions: list[dict[str, str]] = []
        for route in ROUTES:
            row = manifests[route.result_dir].get(clip_path)
            if row is None:
                raise RuntimeError(f"{clip_path} not found in {route.manifest}")
            with np.load(resolve_cache(row["pose_path"])) as cache:
                poses = cache["keypoints"].astype(np.float32)
                indices = cache["frame_indices"].astype(np.int32)
            if reference_indices is None:
                reference_indices = indices
            elif not np.array_equal(reference_indices, indices):
                raise RuntimeError(f"Frame index mismatch for {route.title}: {clip_path}")
            sequences.append(poses)
            route_predictions.append(predictions[route.result_dir][clip_path])
        assert reference_indices is not None

        capture = cv2.VideoCapture(str(args.video_root / clip_path))
        if not capture.isOpened():
            writer.release()
            raise RuntimeError(f"Cannot open video: {args.video_root / clip_path}")
        for sample_number, frame_index in enumerate(reference_indices):
            capture.set(cv2.CAP_PROP_POS_FRAMES, int(frame_index))
            ok, frame = capture.read()
            if not ok:
                capture.release()
                writer.release()
                raise RuntimeError(f"Cannot decode frame {frame_index}: {clip_path}")
            tiles = [
                draw_original(
                    frame,
                    clip_number,
                    len(args.clips),
                    clip_path,
                    sample_number,
                    len(reference_indices),
                    tile_size,
                )
            ]
            tiles.extend(
                draw_route(
                    frame,
                    poses[sample_number],
                    route,
                    prediction,
                    args.confidence_threshold,
                    tile_size,
                )
                for route, poses, prediction in zip(
                    ROUTES,
                    sequences,
                    route_predictions,
                )
            )
            grid = np.concatenate(
                [
                    np.concatenate(tiles[0:2], axis=1),
                    np.concatenate(tiles[2:4], axis=1),
                ],
                axis=0,
            )
            writer.write(grid)
            if clip_number == 2 and sample_number == 36:
                preview_frame = grid
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
        raise RuntimeError(f"Cannot encode preview: {args.preview}")
    buffer.tofile(str(args.preview))
    print(args.output.resolve())
    print(args.preview.resolve())


if __name__ == "__main__":
    main()
