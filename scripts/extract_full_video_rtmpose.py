from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import cv2
import numpy as np

try:
    from .extract_pose_cache import RTMPoseBackend
except ImportError:
    from extract_pose_cache import RTMPoseBackend


PROJECT = Path(__file__).resolve().parent.parent


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def cache_name(path: str) -> str:
    return path.replace("/", "__").replace("\\", "__").rsplit(".", 1)[0] + ".npz"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--manifest",
        type=Path,
        default=PROJECT / "data/metadata/gmdcsa24.csv",
    )
    parser.add_argument(
        "--video-root",
        type=Path,
        default=PROJECT / "data/raw/GMDCSA24",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=PROJECT / "data/poses/gmdcsa24_rtmpose_full",
    )
    parser.add_argument("--subjects", type=int, nargs="+")
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--rtmpose-mode", default="balanced")
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    rows = read_rows(args.manifest)
    if args.subjects:
        selected = set(args.subjects)
        rows = [row for row in rows if int(row["subject"]) in selected]
    args.output_dir.mkdir(parents=True, exist_ok=True)
    backend = RTMPoseBackend(args.rtmpose_mode, args.device)
    totals = {"videos": 0, "frames": 0, "zero_pose_frames": 0}

    for number, row in enumerate(rows, 1):
        output = args.output_dir / cache_name(row["path"])
        if output.is_file() and not args.overwrite:
            with np.load(output) as cached:
                poses = cached["keypoints"]
            print(f"[{number}/{len(rows)}] SKIP {row['path']}", flush=True)
        else:
            video = args.video_root / row["path"]
            capture = cv2.VideoCapture(str(video))
            if not capture.isOpened():
                raise RuntimeError(f"Cannot open video: {video}")
            fps = float(capture.get(cv2.CAP_PROP_FPS))
            width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
            sequence: list[np.ndarray] = []
            while True:
                ok, frame = capture.read()
                if not ok:
                    break
                sequence.append(np.asarray(backend(frame), dtype=np.float32))
            capture.release()
            if not sequence:
                raise RuntimeError(f"No frames decoded: {video}")
            poses = np.stack(sequence)
            np.savez_compressed(
                output,
                keypoints=poses,
                frame_indices=np.arange(len(poses), dtype=np.int32),
                image_size=np.asarray([height, width], dtype=np.int32),
                fps=np.asarray(fps, dtype=np.float32),
            )
            print(
                f"[{number}/{len(rows)}] {row['path']} frames={len(poses)}",
                flush=True,
            )
        totals["videos"] += 1
        totals["frames"] += len(poses)
        totals["zero_pose_frames"] += int(
            np.sum(np.max(poses[:, :, 2], axis=1) < 0.2)
        )

    subject_tag = "all" if not args.subjects else "-".join(map(str, args.subjects))
    summary_path = args.output_dir / f"summary-subjects-{subject_tag}.json"
    summary_path.write_text(
        json.dumps(totals, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(totals, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
