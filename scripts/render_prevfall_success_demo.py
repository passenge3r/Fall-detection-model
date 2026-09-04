"""Render an H.264 held-out PreVFall prediction case."""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
from pathlib import Path

import cv2
import imageio_ffmpeg
import numpy as np
import torch

PROJECT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT))
from models import build_model  # noqa: E402
from scripts.build_gcn_tensor import sequence_normalize  # noqa: E402
from scripts.extract_full_video_rtmpose import cache_name  # noqa: E402


EDGES = (
    (0, 1), (0, 2), (1, 3), (2, 4), (0, 5), (0, 6), (5, 6),
    (5, 7), (7, 9), (6, 8), (8, 10), (5, 11), (6, 12), (11, 12),
    (11, 13), (13, 15), (12, 14), (14, 16),
)
HORIZONS = ("1s", "2s", "3s")


def text(frame: np.ndarray, value: str, xy: tuple[int, int], scale: float = 0.62,
         color: tuple[int, int, int] = (245, 245, 245), thickness: int = 2) -> None:
    cv2.putText(frame, value, xy, cv2.FONT_HERSHEY_SIMPLEX, scale, color, thickness, cv2.LINE_AA)


def manifest_row(path: str) -> dict[str, str]:
    manifest = PROJECT / "data/metadata/prevfall_v4_videos.csv"
    with manifest.open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            if row["path"].replace("\\", "/") == path.replace("\\", "/"):
                return row
    raise KeyError(f"Video is missing from manifest: {path}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--video",
        default="data/raw/PreVFall/v4_video_csv/Pre-VFall/dizziness_fall_forward/FDFSM1.mp4",
    )
    parser.add_argument("--fold", type=int, default=1)
    parser.add_argument("--model-root", type=Path,
                        default=PROJECT / "outputs/prevfall_rtmpose_stgcnpp_300e_b128")
    parser.add_argument("--pose-dir", type=Path,
                        default=PROJECT / "data/poses/prevfall_rtmpose_full")
    parser.add_argument("--output", type=Path,
                        default=PROJECT / "reports/prevfall_prefall_success_subject1.mp4")
    parser.add_argument("--window-frames", type=int, default=64)
    parser.add_argument("--stride", type=int, default=16)
    parser.add_argument("--seconds-before", type=float, default=8.0)
    parser.add_argument("--seconds-after", type=float, default=3.0)
    args = parser.parse_args()

    row = manifest_row(args.video)
    if int(row["subject"]) != args.fold:
        raise ValueError("For an unbiased demo, --fold must equal the held-out subject number")
    onset = int(row["fall_onset_frame"]) if row["fall_onset_frame"] else None
    video_path = PROJECT / args.video
    cache_path = args.pose_dir / cache_name(args.video)
    with np.load(cache_path) as cache:
        poses = cache["keypoints"].astype(np.float32)
        image_size = cache["image_size"].astype(np.int32)
        cached_fps = float(cache["fps"])

    fold_dir = args.model_root / f"fold_{args.fold}"
    metrics = json.loads((fold_dir / "metrics.json").read_text(encoding="utf-8"))
    thresholds = np.asarray([
        metrics["decision_thresholds_calibrated_on_validation"][name] for name in HORIZONS
    ], dtype=np.float32)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = build_model("stgcnpp", num_class=3, base_channels=64, dropout=0.5).to(device)
    model.load_state_dict(torch.load(fold_dir / "best.pt", map_location=device, weights_only=True))
    model.eval()

    score_at: dict[int, np.ndarray] = {}
    with torch.inference_mode():
        prediction_end = min(onset, len(poses)) if onset is not None else len(poses)
        for end in range(args.window_frames - 1, prediction_end, args.stride):
            start = end - args.window_frames + 1
            sample = sequence_normalize(poses[start:end + 1], image_size, 0.2)
            raw = torch.sigmoid(model(torch.from_numpy(sample[None]).to(device)))[0].cpu().numpy()
            score_at[end] = np.maximum.accumulate(raw)

    capture = cv2.VideoCapture(str(video_path))
    fps = float(capture.get(cv2.CAP_PROP_FPS)) or cached_fps
    source_width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    source_height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width, height = 1280, 720
    scale_x, scale_y = width / source_width, height / source_height
    trigger_frames = [
        frame for frame, scores in score_at.items() if bool(np.any(scores >= thresholds))
    ]
    detected_by_horizon: dict[str, bool] = {}
    if onset is not None:
        for index, name in enumerate(HORIZONS):
            horizon_seconds = index + 1
            detected_by_horizon[name] = any(
                0 <= (onset - frame) / fps <= horizon_seconds and scores[index] >= thresholds[index]
                for frame, scores in score_at.items()
            )
        outcome = "Outcome: " + " | ".join(
            f"{name} {'HIT' if detected_by_horizon[name] else 'MISS'}" for name in HORIZONS
        )
    else:
        outcome = "Outcome: FALSE ALERT on no-fall video" if trigger_frames else "Outcome: correct no-fall"
    focus_frame = onset if onset is not None else (
        trigger_frames[0] if trigger_frames else len(poses) // 2
    )
    start_frame = max(0, int(focus_frame - args.seconds_before * fps))
    end_frame = min(len(poses) - 1, int(focus_frame + args.seconds_after * fps))
    capture.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    temporary = args.output.with_name(args.output.stem + "_mp4v.mp4")
    writer = cv2.VideoWriter(str(temporary), cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height))
    if not writer.isOpened():
        raise RuntimeError(f"Cannot open video writer: {temporary}")

    latest: np.ndarray | None = None
    first_alert_frame: dict[str, int] = {}
    for frame_index in range(start_frame, end_frame + 1):
        ok, source = capture.read()
        if not ok:
            break
        frame = cv2.resize(source, (width, height), interpolation=cv2.INTER_AREA)
        if frame_index in score_at:
            latest = score_at[frame_index]
        pose = poses[frame_index].copy()
        pose[:, 0] *= scale_x; pose[:, 1] *= scale_y
        visible = pose[:, 2] >= 0.2
        for left, right in EDGES:
            if visible[left] and visible[right]:
                cv2.line(frame, tuple(pose[left, :2].astype(int)), tuple(pose[right, :2].astype(int)),
                         (60, 225, 80), 2, cv2.LINE_AA)
        for joint in np.flatnonzero(visible):
            cv2.circle(frame, tuple(pose[joint, :2].astype(int)), 3, (20, 210, 255), -1, cv2.LINE_AA)

        panel = frame.copy(); cv2.rectangle(panel, (12, 12), (600, 255), (15, 15, 15), -1)
        cv2.addWeighted(panel, 0.76, frame, 0.24, 0, frame)
        text(frame, f"Held-out Subject {row['subject']}: pre-fall prediction", (28, 42), 0.68)
        text(frame, f"RTMPose + ST-GCN++ | 9-subject LOSO | fold {args.fold}", (28, 70), 0.48, (210, 210, 210), 1)

        if onset is not None and frame_index >= onset:
            state, color = "FALL STARTED / detection takes over", (30, 30, 255)
        elif latest is None:
            state, color = "WARMUP", (0, 215, 255)
        else:
            triggered = latest >= thresholds
            for index, name in enumerate(HORIZONS):
                if triggered[index] and name not in first_alert_frame:
                    first_alert_frame[name] = frame_index
            if triggered[0]:
                state, color = "HIGH: fall risk within 1 s", (30, 30, 255)
            elif triggered[1]:
                state, color = "MEDIUM: fall risk within 2 s", (0, 145, 255)
            elif triggered[2]:
                state, color = "LOW: fall risk within 3 s", (0, 220, 255)
            else:
                state, color = "NORMAL", (70, 220, 80)
        text(frame, f"Risk: {state}", (28, 108), 0.67, color)
        if latest is not None and (onset is None or frame_index < onset):
            for index, name in enumerate(HORIZONS):
                text(frame, f"P(fall <= {name}) {latest[index]:.3f}  /  threshold {thresholds[index]:.3f}",
                     (28, 142 + 27 * index), 0.50, (238, 238, 238), 1)
        text(frame, outcome, (28, 232), 0.47, (120, 220, 255), 1)

        countdown = (onset - frame_index) / fps if onset is not None else None
        if countdown is None:
            gt = "Official label: NO FALL"
        else:
            gt = f"Official fall onset in {countdown:.2f} s" if countdown > 0 else "Official label: FALL"
        tw = cv2.getTextSize(gt, cv2.FONT_HERSHEY_SIMPLEX, 0.62, 2)[0][0]
        text(frame, gt, (width - tw - 24, 38), 0.62, (255, 215, 90))
        text(frame, "Ground truth is display-only", (width - 310, 67), 0.47, (255, 215, 90), 1)
        writer.write(frame)

    capture.release(); writer.release()
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    subprocess.run([
        ffmpeg, "-y", "-i", str(temporary), "-an", "-c:v", "libx264",
        "-preset", "medium", "-crf", "21", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
        str(args.output),
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    temporary.unlink()

    lead_times = (
        {name: (onset - frame) / fps for name, frame in first_alert_frame.items()}
        if onset is not None else {}
    )
    result = {
        "output": str(args.output), "source_video": args.video, "held_out_subject": int(row["subject"]),
        "fold": args.fold, "official_label": "fall" if onset is not None else "no_fall",
        "official_fall_onset_frame": onset, "fps": fps,
        "first_alert_lead_seconds": lead_times, "thresholds": dict(zip(HORIZONS, thresholds.tolist(), strict=True)),
        "detected_within_horizon": detected_by_horizon,
        "false_alert": onset is None and bool(trigger_frames),
        "evaluation_stride_frames": args.stride, "codec": "H.264/yuv420p",
    }
    args.output.with_suffix(".json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
