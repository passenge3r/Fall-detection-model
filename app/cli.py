from __future__ import annotations

import argparse
import json
from pathlib import Path

from .decision import DecisionConfig
from .pipeline import PROJECT, ROUTES, run_video


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the pre-recorded fall-detection prototype")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--route", choices=sorted(ROUTES), default="rtmpose_stgcnpp")
    parser.add_argument(
        "--checkpoints-root",
        type=Path,
        default=PROJECT / "results/benchmark_e300_full",
    )
    parser.add_argument("--yolo-model", type=Path, default=PROJECT / "models/yolo26n-pose.pt")
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--window-frames", type=int, default=64)
    parser.add_argument("--stride-frames", type=int, default=16)
    parser.add_argument("--threshold", type=float, default=0.5)
    parser.add_argument("--confirm-windows", type=int, default=3)
    parser.add_argument("--cooldown-windows", type=int, default=10)
    parser.add_argument("--min-pose-valid-ratio", type=float, default=0.5)
    parser.add_argument("--min-positive-folds", type=int, default=3)
    parser.add_argument("--pose-threshold", type=float, default=0.2)
    parser.add_argument("--yolo-confidence", type=float, default=0.1)
    parser.add_argument("--max-frames", type=int)
    parser.add_argument("--no-video", action="store_true")
    args = parser.parse_args()

    summary = run_video(
        input_path=args.input,
        output_dir=args.output_dir,
        route=args.route,
        checkpoints_root=args.checkpoints_root,
        yolo_model=args.yolo_model,
        device_name=args.device,
        window_frames=args.window_frames,
        stride_frames=args.stride_frames,
        pose_threshold=args.pose_threshold,
        yolo_confidence=args.yolo_confidence,
        decision_config=DecisionConfig(
            threshold=args.threshold,
            confirm_windows=args.confirm_windows,
            cooldown_windows=args.cooldown_windows,
            min_pose_valid_ratio=args.min_pose_valid_ratio,
            min_positive_folds=args.min_positive_folds,
        ),
        write_video=not args.no_video,
        max_frames=args.max_frames,
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
