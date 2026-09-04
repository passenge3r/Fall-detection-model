from __future__ import annotations

import csv
from pathlib import Path

import cv2
import numpy as np


PROJECT = Path(__file__).resolve().parents[1]
CASE_DIR = PROJECT / "outputs" / "mcfd_error_cases"
OUTPUT = CASE_DIR / "mcfd_error_review_compilation.mp4"

DIAGNOSES = [
    (
        "case_01",
        "GT=FALL | all three routes miss",
        "POSES OK -> classifier / short-window false negative",
    ),
    (
        "case_02",
        "GT=FALL | all three routes miss",
        "POSES OK -> classifier / temporal-context false negative",
    ),
    (
        "case_03",
        "GT=ADL | all three routes false alarm",
        "POSE DEGRADED + lying ADL resembles post-fall state",
    ),
    (
        "case_04",
        "GT=ADL | all three routes false alarm",
        "POSE FAILURE: YOLO 64/64 missing; RTMPose wrong target",
    ),
    (
        "case_05",
        "GT=ADL | only YOLO-Pose+ST-GCN++ is correct",
        "RTMPose pose present -> RTM classifier confuses lying ADL",
    ),
    (
        "case_06",
        "GT=ADL | only YOLO-Pose+ST-GCN++ is correct",
        "POSE/TARGET INSTABILITY; classifiers respond differently",
    ),
]


def fit_text(text: str, max_width: int, start_scale: float = 1.0) -> float:
    scale = start_scale
    while scale > 0.45:
        width = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, scale, 2)[0][0]
        if width <= max_width:
            return scale
        scale -= 0.05
    return scale


def title_card(width: int, height: int, case_id: str, summary: str, diagnosis: str) -> np.ndarray:
    frame = np.full((height, width, 3), (28, 32, 38), dtype=np.uint8)
    cv2.putText(
        frame, case_id.upper(), (55, int(height * 0.28)),
        cv2.FONT_HERSHEY_SIMPLEX, 1.35, (70, 200, 255), 3, cv2.LINE_AA,
    )
    summary_scale = fit_text(summary, width - 110, 0.9)
    diagnosis_scale = fit_text(diagnosis, width - 110, 0.78)
    cv2.putText(
        frame, summary, (55, int(height * 0.49)),
        cv2.FONT_HERSHEY_SIMPLEX, summary_scale, (245, 245, 245), 2, cv2.LINE_AA,
    )
    cv2.putText(
        frame, diagnosis, (55, int(height * 0.67)),
        cv2.FONT_HERSHEY_SIMPLEX, diagnosis_scale, (120, 225, 150), 2, cv2.LINE_AA,
    )
    cv2.putText(
        frame, "Layout: original video | RTMPose skeleton | YOLO-Pose skeleton",
        (55, int(height * 0.86)), cv2.FONT_HERSHEY_SIMPLEX,
        fit_text("Layout: original video | RTMPose skeleton | YOLO-Pose skeleton", width - 110, 0.58),
        (175, 185, 198), 1, cv2.LINE_AA,
    )
    return frame


def main() -> None:
    first_capture = cv2.VideoCapture(str(CASE_DIR / "case_01.mp4"))
    if not first_capture.isOpened():
        raise RuntimeError("Missing rendered case videos; run render_mcfd_error_cases.py first")
    width = int(first_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(first_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = float(first_capture.get(cv2.CAP_PROP_FPS)) or 8.0
    first_capture.release()

    writer = cv2.VideoWriter(
        str(OUTPUT), cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height)
    )
    if not writer.isOpened():
        raise RuntimeError(f"Cannot create {OUTPUT}")

    diagnosis_rows = []
    for case_id, summary, diagnosis in DIAGNOSES:
        card = title_card(width, height, case_id, summary, diagnosis)
        for _ in range(round(fps * 2.0)):
            writer.write(card)

        capture = cv2.VideoCapture(str(CASE_DIR / f"{case_id}.mp4"))
        if not capture.isOpened():
            raise RuntimeError(f"Cannot open {case_id}.mp4")
        frame_count = 0
        while True:
            ok, frame = capture.read()
            if not ok:
                break
            if frame.shape[1] != width or frame.shape[0] != height:
                frame = cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA)
            cv2.rectangle(frame, (0, height - 35), (width, height), (0, 0, 0), -1)
            scale = fit_text(diagnosis, width - 30, 0.55)
            cv2.putText(
                frame, diagnosis, (14, height - 11),
                cv2.FONT_HERSHEY_SIMPLEX, scale, (120, 225, 150), 1, cv2.LINE_AA,
            )
            writer.write(frame)
            frame_count += 1
        capture.release()
        diagnosis_rows.append(
            {"case_id": case_id, "summary": summary, "diagnosis": diagnosis, "frames": frame_count}
        )

    writer.release()
    with (CASE_DIR / "diagnosis.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer_csv = csv.DictWriter(handle, fieldnames=diagnosis_rows[0].keys())
        writer_csv.writeheader()
        writer_csv.writerows(diagnosis_rows)
    print(OUTPUT)


if __name__ == "__main__":
    main()
