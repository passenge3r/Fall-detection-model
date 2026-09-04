"""Create a single shareable side-by-side MP4 from the two system demos."""

from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent.parent
FALL = ROOT / "outputs/final_sliding_system/fall_subject1_01/annotated.mp4"
ADL = ROOT / "outputs/final_sliding_system/adl_subject1_01/annotated.mp4"
OUTPUT = ROOT / "reports" / "跌倒检测实际效果对比.mp4"
FONT_BOLD = ImageFont.truetype("C:/Windows/Fonts/msyhbd.ttc", 34)
FONT = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 24)


def fit(frame: np.ndarray, width: int, height: int) -> np.ndarray:
    scale = min(width / frame.shape[1], height / frame.shape[0])
    resized = cv2.resize(frame, (int(frame.shape[1] * scale), int(frame.shape[0] * scale)))
    canvas = np.full((height, width, 3), (17, 28, 48), dtype=np.uint8)
    y = (height - resized.shape[0]) // 2
    x = (width - resized.shape[1]) // 2
    canvas[y:y + resized.shape[0], x:x + resized.shape[1]] = resized
    return canvas


def main() -> None:
    fall_cap, adl_cap = cv2.VideoCapture(str(FALL)), cv2.VideoCapture(str(ADL))
    if not fall_cap.isOpened() or not adl_cap.isOpened():
        raise RuntimeError("Cannot open one of the source videos")
    fps = min(fall_cap.get(cv2.CAP_PROP_FPS), adl_cap.get(cv2.CAP_PROP_FPS))
    frames = max(int(fall_cap.get(cv2.CAP_PROP_FRAME_COUNT)), int(adl_cap.get(cv2.CAP_PROP_FRAME_COUNT)))
    panel_w, panel_h, header_h, footer_h = 900, 506, 78, 112
    size = (panel_w * 2, header_h + panel_h + footer_h)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    writer = cv2.VideoWriter(str(OUTPUT), cv2.VideoWriter_fourcc(*"mp4v"), fps, size)
    if not writer.isOpened():
        raise RuntimeError("Cannot create output MP4")

    last_fall = np.full((panel_h, panel_w, 3), (17, 28, 48), dtype=np.uint8)
    last_adl = last_fall.copy()
    for _ in range(frames):
        ok_fall, fall_frame = fall_cap.read()
        ok_adl, adl_frame = adl_cap.read()
        if ok_fall:
            last_fall = fit(fall_frame, panel_w, panel_h)
        if ok_adl:
            last_adl = fit(adl_frame, panel_w, panel_h)
        canvas = np.full((size[1], size[0], 3), (7, 16, 31), dtype=np.uint8)
        canvas[header_h:header_h + panel_h, :panel_w] = last_fall
        canvas[header_h:header_h + panel_h, panel_w:] = last_adl
        cv2.line(canvas, (panel_w, 0), (panel_w, size[1]), (51, 65, 85), 2)

        rgb = cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB)
        pil = Image.fromarray(rgb)
        draw = ImageDraw.Draw(pil)
        draw.text((34, 18), "跌倒样例：正确确认报警", font=FONT_BOLD, fill=(34, 197, 94))
        draw.text((panel_w + 34, 18), "正常样例：成功拦截误报", font=FONT_BOLD, fill=(56, 189, 248))
        draw.text((34, header_h + panel_h + 15),
                  "流程：RTMPose → 64帧滑窗 → 4×ST-GCN++ → ≥3/4折共识 → 连续3窗状态机",
                  font=FONT, fill=(226, 232, 240))
        draw.text((34, header_h + panel_h + 58),
                  "V-JEPA实验旁路：跌倒 100.00%（正确）｜正常 99.89%（错误）｜未通过F1门槛，当前不参与报警",
                  font=FONT, fill=(196, 181, 253))
        canvas = cv2.cvtColor(np.asarray(pil), cv2.COLOR_RGB2BGR)
        writer.write(canvas)

    fall_cap.release()
    adl_cap.release()
    writer.release()
    print(OUTPUT)


if __name__ == "__main__":
    main()
