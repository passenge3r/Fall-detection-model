"""Render a pre-fall prediction demo on a held-out GMDCSA24 video."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import cv2
import numpy as np
import torch

PROJECT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT))
from models import build_model  # noqa: E402
from scripts.build_gcn_tensor import sequence_normalize  # noqa: E402
from scripts.build_sliding_window_dataset import load_fall_annotations  # noqa: E402
from scripts.extract_full_video_rtmpose import cache_name  # noqa: E402


EDGES = (
    (0, 1), (0, 2), (1, 3), (2, 4), (0, 5), (0, 6), (5, 6),
    (5, 7), (7, 9), (6, 8), (8, 10), (5, 11), (6, 12), (11, 12),
    (11, 13), (13, 15), (12, 14), (14, 16),
)


def put_text(frame: np.ndarray, text: str, xy: tuple[int, int], scale: float = 0.65,
             color: tuple[int, int, int] = (255, 255, 255), thickness: int = 2) -> None:
    cv2.putText(frame, text, xy, cv2.FONT_HERSHEY_SIMPLEX, scale, (0, 0, 0), thickness + 3, cv2.LINE_AA)
    cv2.putText(frame, text, xy, cv2.FONT_HERSHEY_SIMPLEX, scale, color, thickness, cv2.LINE_AA)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--video", default="Subject 1/Fall/01.mp4")
    parser.add_argument("--fold", type=int, default=1)
    parser.add_argument("--checkpoint", type=Path, default=PROJECT / "outputs/prefall_stgcnpp_300e/fold_1/best.pt")
    parser.add_argument("--metrics", type=Path, default=PROJECT / "outputs/prefall_stgcnpp_300e/fold_1/metrics.json")
    parser.add_argument("--pose-dir", type=Path, default=PROJECT / "data/poses/gmdcsa24_rtmpose_full")
    parser.add_argument("--video-root", type=Path, default=PROJECT / "data/raw/GMDCSA24")
    parser.add_argument("--output", type=Path, default=PROJECT / "outputs/prefall_stgcnpp_300e/prefall_demo_subject1_fall01.mp4")
    parser.add_argument("--window-frames", type=int, default=64)
    parser.add_argument("--inference-stride", type=int, default=4)
    args = parser.parse_args()

    video_path = args.video_root / args.video
    cache_path = args.pose_dir / cache_name(args.video)
    annotations = load_fall_annotations(args.video_root)
    onset_seconds = annotations[args.video][0]
    with np.load(cache_path) as cache:
        poses = cache["keypoints"].astype(np.float32)
        image_size = cache["image_size"]
        cached_fps = float(cache["fps"])

    metrics = json.loads(args.metrics.read_text(encoding="utf-8"))
    thresholds = np.asarray(
        [metrics["decision_thresholds_calibrated_on_validation"][name] for name in ("1s", "2s", "3s")],
        dtype=np.float32,
    )
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = build_model("stgcnpp", num_class=3, base_channels=64, dropout=0.5).to(device)
    model.load_state_dict(torch.load(args.checkpoint, map_location=device, weights_only=True)); model.eval()

    capture = cv2.VideoCapture(str(video_path))
    fps = float(capture.get(cv2.CAP_PROP_FPS)) or cached_fps
    width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)); height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    writer = cv2.VideoWriter(str(args.output), cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height))
    if not writer.isOpened():
        raise RuntimeError(f"Cannot open video writer: {args.output}")

    scores: np.ndarray | None = None
    first_alert_seconds: dict[str, float] = {}
    frame_index = 0
    while True:
        ok, frame = capture.read()
        if not ok:
            break
        current_seconds = frame_index / fps
        if frame_index < len(poses):
            pose = poses[frame_index]
            visible = pose[:, 2] >= 0.2
            for left, right in EDGES:
                if visible[left] and visible[right]:
                    cv2.line(frame, tuple(pose[left, :2].astype(int)), tuple(pose[right, :2].astype(int)), (80, 220, 80), 3, cv2.LINE_AA)
            for joint in np.flatnonzero(visible):
                cv2.circle(frame, tuple(pose[joint, :2].astype(int)), 4, (20, 210, 255), -1, cv2.LINE_AA)

        is_pre_onset = current_seconds < onset_seconds
        enough_context = frame_index >= args.window_frames - 1
        if is_pre_onset and enough_context and (scores is None or frame_index % args.inference_stride == 0):
            start = frame_index - args.window_frames + 1
            sample = sequence_normalize(poses[start : frame_index + 1], image_size, 0.2)
            tensor = torch.from_numpy(sample[None]).to(device)
            with torch.inference_mode():
                raw_scores = torch.sigmoid(model(tensor))[0].cpu().numpy()
            scores = np.maximum.accumulate(raw_scores)

        overlay = frame.copy(); cv2.rectangle(overlay, (12, 12), (550, 226), (18, 18, 18), -1)
        cv2.addWeighted(overlay, 0.72, frame, 0.28, 0, frame)
        put_text(frame, "Pre-fall prediction demo (held-out Subject 1)", (28, 43), 0.68)
        put_text(frame, "RTMPose + ST-GCN++ | 64-frame causal window", (28, 72), 0.54, (210, 210, 210), 1)
        if not is_pre_onset:
            put_text(frame, "FALL DETECTED - event confirmation active", (28, 112), 0.68, (40, 40, 255))
            put_text(frame, "State switched: prediction -> detection / response", (28, 145), 0.50, (180, 180, 255), 1)
        elif not enough_context or scores is None:
            put_text(frame, f"Collecting context: {frame_index + 1}/{args.window_frames} frames", (28, 112), 0.65, (0, 215, 255))
        else:
            triggered = scores >= thresholds
            for index, label in enumerate(("1s", "2s", "3s")):
                if triggered[index] and label not in first_alert_seconds:
                    first_alert_seconds[label] = current_seconds
            if triggered[0]:
                alert, color = "HIGH: predicted within 1 s", (30, 30, 255)
            elif triggered[1]:
                alert, color = "MEDIUM: predicted within 2 s", (0, 140, 255)
            elif triggered[2]:
                alert, color = "LOW: predicted within 3 s", (0, 220, 255)
            else:
                alert, color = "NORMAL", (80, 220, 80)
            put_text(frame, f"Risk state: {alert}", (28, 108), 0.68, color)
            for index, label in enumerate(("1 s", "2 s", "3 s")):
                put_text(frame, f"P(fall <= {label}) = {scores[index]:.3f}   threshold={thresholds[index]:.3f}",
                         (28, 140 + index * 27), 0.52, (235, 235, 235), 1)

        countdown = onset_seconds - current_seconds
        gt_text = f"GT onset countdown: {max(countdown, 0):.2f} s" if countdown > 0 else "GT: fall has started"
        text_width = cv2.getTextSize(gt_text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0][0]
        put_text(frame, gt_text, (width - text_width - 24, 38), 0.6, (255, 210, 80))
        put_text(frame, "GT is display-only, NOT model input", (width - 365, 67), 0.48, (255, 210, 80), 1)
        put_text(frame, f"t={current_seconds:.2f}s", (width - 125, height - 24), 0.55)
        writer.write(frame); frame_index += 1

    capture.release(); writer.release()
    print(json.dumps({"output": str(args.output), "frames": frame_index, "fps": fps, "duration_seconds": frame_index / fps,
                      "video": args.video, "onset_seconds": onset_seconds, "fold": args.fold,
                      "first_alert_seconds": first_alert_seconds,
                      "lead_time_seconds": {key: onset_seconds - value for key, value in first_alert_seconds.items()}},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
