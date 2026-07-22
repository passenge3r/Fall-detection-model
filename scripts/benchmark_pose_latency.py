from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import cv2
import numpy as np


PROJECT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT / "scripts"))
from extract_pose_cache import RTMPoseBackend, YoloPoseBackend  # noqa: E402


def load_frame(video: Path, frame_index: int) -> np.ndarray:
    capture = cv2.VideoCapture(str(video))
    capture.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
    ok, frame = capture.read()
    capture.release()
    if not ok or frame is None:
        raise RuntimeError(f"Cannot decode frame {frame_index}: {video}")
    return frame


def benchmark(name: str, backend: object, frame: np.ndarray, warmup: int, repeats: int) -> dict[str, object]:
    for _ in range(warmup):
        backend(frame)  # type: ignore[operator]
    values = []
    confidences = []
    for _ in range(repeats):
        start = time.perf_counter()
        pose = backend(frame)  # type: ignore[operator]
        values.append((time.perf_counter() - start) * 1000)
        confidences.append(float(np.mean(pose[:, 2])))
    return {
        "backend": name,
        "repeats": repeats,
        "latency_ms_mean": float(np.mean(values)),
        "latency_ms_median": float(np.median(values)),
        "latency_ms_p95": float(np.percentile(values, 95)),
        "fps_from_mean": float(1000 / np.mean(values)),
        "mean_keypoint_confidence": float(np.mean(confidences)),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", type=Path, required=True)
    parser.add_argument("--frame-index", type=int, default=0)
    parser.add_argument("--warmup", type=int, default=10)
    parser.add_argument("--repeats", type=int, default=100)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--backend", choices=("rtmpose", "yolo"), required=True)
    parser.add_argument("--yolo-model", default=str(PROJECT / "models/yolo26n-pose.pt"))
    args = parser.parse_args()

    frame = load_frame(args.video, args.frame_index)
    backends = (
        [("rtmpose_balanced", RTMPoseBackend("balanced", "cuda"))]
        if args.backend == "rtmpose"
        else [("yolo26n_pose_c010", YoloPoseBackend(args.yolo_model, "cuda", 0.1))]
    )
    results = [benchmark(name, backend, frame, args.warmup, args.repeats) for name, backend in backends]
    report = {
        "video": str(args.video),
        "frame_index": args.frame_index,
        "image_shape": list(frame.shape),
        "results": results,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
