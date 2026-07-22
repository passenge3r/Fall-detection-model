from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROUTES = [
    ("rtmpose", "stgcnpp", "gmdcsa24_rtmpose_t64.npz"),
    ("rtmpose", "ctrgcn", "gmdcsa24_rtmpose_t64.npz"),
    ("rtmpose", "posec3d", "gmdcsa24_rtmpose_t64.npz"),
    ("yolo", "stgcnpp", "gmdcsa24_yolo_t64_c010.npz"),
    ("yolo", "ctrgcn", "gmdcsa24_yolo_t64_c010.npz"),
    ("yolo", "posec3d", "gmdcsa24_yolo_t64_c010.npz"),
    ("yolo_bytetrack", "stgcnpp", "gmdcsa24_yolo_bytetrack_t64_c010.npz"),
    ("yolo_bytetrack", "ctrgcn", "gmdcsa24_yolo_bytetrack_t64_c010.npz"),
    ("yolo_bytetrack", "posec3d", "gmdcsa24_yolo_bytetrack_t64_c010.npz"),
    ("rtmo", "stgcnpp", "gmdcsa24_rtmo_t64.npz"),
    ("rtmo", "ctrgcn", "gmdcsa24_rtmo_t64.npz"),
    ("rtmo", "posec3d", "gmdcsa24_rtmo_t64.npz"),
]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--epochs", type=int, default=80)
    parser.add_argument("--patience", type=int, default=15)
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--no-early-stopping", action="store_true")
    parser.add_argument(
        "--output-root", type=Path,
        help="Experiment output directory (default: <project>/results/benchmark)",
    )
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    trainer = args.project / "scripts" / "train_gcn.py"
    splits = args.project / "data" / "splits" / "gmdcsa24_loso"
    results = args.output_root or args.project / "results" / "benchmark"

    for pose, model, tensor_name in ROUTES:
        for fold in range(1, 5):
            output = results / f"{pose}_{model}" / f"fold_{fold}"
            if (output / "metrics.json").is_file() and not args.overwrite:
                print(f"SKIP completed: {pose}+{model} fold {fold}", flush=True)
                continue
            command = [
                sys.executable, str(trainer),
                "--data", str(args.project / "data" / "gcn" / tensor_name),
                "--splits", str(splits),
                "--fold", str(fold),
                "--model", model,
                "--pose", pose,
                "--output", str(output),
                "--epochs", str(args.epochs),
                "--patience", str(args.patience),
                "--batch-size", str(args.batch_size),
                "--seed", str(2026 + fold),
                "--device", "cuda",
            ]
            if args.no_early_stopping:
                command.append("--no-early-stopping")
            print(f"RUN: {pose}+{model} fold {fold}", flush=True)
            subprocess.run(command, check=True)


if __name__ == "__main__":
    main()
