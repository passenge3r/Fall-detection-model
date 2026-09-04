"""Build a shareable one-page PNG showing the real fall-detection workflow."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "reports" / "跌倒检测完整流程效果.png"
FONT = Path("C:/Windows/Fonts/msyh.ttc")
FONT_BOLD = Path("C:/Windows/Fonts/msyhbd.ttc")


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_BOLD if bold else FONT), size)


def rounded(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], fill: str, outline: str = "#334155") -> None:
    draw.rounded_rectangle(box, radius=20, fill=fill, outline=outline, width=2)


def centered(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], text: str,
             text_font: ImageFont.FreeTypeFont, fill: str = "#f8fafc") -> None:
    left, top, right, bottom = box
    bounds = draw.multiline_textbbox((0, 0), text, font=text_font, spacing=8, align="center")
    width, height = bounds[2] - bounds[0], bounds[3] - bounds[1]
    draw.multiline_text(((left + right - width) / 2, (top + bottom - height) / 2), text,
                        font=text_font, fill=fill, spacing=8, align="center")


def contain(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    copy = image.copy().convert("RGB")
    copy.thumbnail(size, Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", size, "#020617")
    canvas.paste(copy, ((size[0] - copy.width) // 2, (size[1] - copy.height) // 2))
    return canvas


def plot(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], probabilities: list[float],
         votes: list[int], confirmed_at: int | None) -> None:
    left, top, right, bottom = box
    chart_left, chart_top, chart_right, chart_bottom = left + 70, top + 38, right - 24, bottom - 58
    if confirmed_at is not None:
        x_confirm = chart_left + confirmed_at * (chart_right - chart_left) / (len(probabilities) - 1)
        draw.rectangle((x_confirm, chart_top, chart_right, chart_bottom), fill="#0f332f")
    for level in (0.0, 0.5, 1.0):
        y = chart_bottom - level * (chart_bottom - chart_top)
        draw.line((chart_left, y, chart_right, y), fill="#334155", width=2)
        draw.text((left + 4, y - 15), f"{int(level * 100)}%", font=font(22), fill="#94a3b8")
    threshold_y = chart_bottom - 0.5 * (chart_bottom - chart_top)
    for x in range(chart_left, chart_right, 22):
        draw.line((x, threshold_y, min(x + 12, chart_right), threshold_y), fill="#f59e0b", width=3)
    points = []
    for index, probability in enumerate(probabilities):
        x = chart_left + index * (chart_right - chart_left) / (len(probabilities) - 1)
        y = chart_bottom - probability * (chart_bottom - chart_top)
        points.append((x, y))
    draw.line(points, fill="#38bdf8", width=5, joint="curve")
    for index, (x, y) in enumerate(points):
        color = "#22c55e" if votes[index] >= 3 else "#38bdf8"
        draw.ellipse((x - 7, y - 7, x + 7, y + 7), fill=color, outline="#e2e8f0", width=2)
        if index in (0, len(points) - 1) or votes[index] >= 3:
            draw.text((x - 20, chart_bottom + 12), str(index + 1), font=font(19), fill="#94a3b8")
    draw.text((chart_left, bottom - 35), "窗口序号", font=font(21), fill="#94a3b8")
    draw.text((chart_right - 290, top + 4), "蓝线：四折平均概率   绿点：≥3/4 折同意", font=font(20), fill="#cbd5e1")


def main() -> None:
    width, height = 2000, 1650
    image = Image.new("RGB", (width, height), "#07101f")
    draw = ImageDraw.Draw(image)

    draw.text((70, 42), "基于视觉的跌倒检测：完整流程与实际效果", font=font(48, True), fill="#f8fafc")
    draw.text((72, 108), "默认部署路线：RTMPose + ST-GCN++ + 四折共识 + 连续窗口状态机",
              font=font(27), fill="#94a3b8")

    stages = [
        ("① 视频输入", "RGB 连续帧"),
        ("② 姿态提取", "RTMPose\nCOCO-17"),
        ("③ 滑动窗口", "64 帧/窗\n步长 16"),
        ("④ 动作分类", "4× ST-GCN++"),
        ("⑤ 质量与共识", "骨架门控\n≥3/4 折"),
        ("⑥ 状态决策", "连续 3 窗\n确认报警"),
    ]
    stage_y, stage_h, gap = 175, 160, 28
    stage_w = (width - 140 - gap * 5) // 6
    for index, (title, subtitle) in enumerate(stages):
        x = 70 + index * (stage_w + gap)
        rounded(draw, (x, stage_y, x + stage_w, stage_y + stage_h), "#111c30")
        centered(draw, (x + 8, stage_y + 12, x + stage_w - 8, stage_y + 72), title, font(26, True))
        centered(draw, (x + 8, stage_y + 68, x + stage_w - 8, stage_y + stage_h - 10), subtitle, font(23), "#cbd5e1")
        if index < len(stages) - 1:
            arrow_x = x + stage_w + 5
            arrow_y = stage_y + stage_h // 2
            draw.line((arrow_x, arrow_y, arrow_x + gap - 10, arrow_y), fill="#38bdf8", width=4)
            draw.polygon([(arrow_x + gap - 10, arrow_y), (arrow_x + gap - 22, arrow_y - 8),
                          (arrow_x + gap - 22, arrow_y + 8)], fill="#38bdf8")

    # Experimental RGB-semantic branch. It is shown separately because it was
    # actually evaluated but did not pass the deployment metric gate.
    branch_y = 350
    draw.line((210, 335, 210, branch_y + 60), fill="#a78bfa", width=4)
    draw.line((210, branch_y + 60, 460, branch_y + 60), fill="#a78bfa", width=4)
    draw.polygon([(460, branch_y + 60), (446, branch_y + 51), (446, branch_y + 69)], fill="#a78bfa")
    rounded(draw, (475, branch_y, 795, branch_y + 120), "#24163d", "#a78bfa")
    centered(draw, (485, branch_y + 8, 785, branch_y + 112), "实验旁路\nV-JEPA 2.1-B", font(25, True), "#ede9fe")
    draw.line((795, branch_y + 60, 870, branch_y + 60), fill="#a78bfa", width=4)
    draw.polygon([(870, branch_y + 60), (856, branch_y + 51), (856, branch_y + 69)], fill="#a78bfa")
    rounded(draw, (885, branch_y, 1205, branch_y + 120), "#24163d", "#a78bfa")
    centered(draw, (895, branch_y + 8, 1195, branch_y + 112), "768维视频语义\n整段均匀取16帧", font(24), "#ede9fe")
    draw.line((1205, branch_y + 60, 1280, branch_y + 60), fill="#a78bfa", width=4)
    draw.polygon([(1280, branch_y + 60), (1266, branch_y + 51), (1266, branch_y + 69)], fill="#a78bfa")
    rounded(draw, (1295, branch_y, 1620, branch_y + 120), "#24163d", "#a78bfa")
    centered(draw, (1305, branch_y + 8, 1610, branch_y + 112), "与ST-GCN++融合\n分数/特征两种实验", font(23), "#ede9fe")
    rounded(draw, (1650, branch_y + 15, 1930, branch_y + 105), "#312026", "#ef4444")
    centered(draw, (1660, branch_y + 20, 1920, branch_y + 100), "未通过F1门槛\n当前不启用", font(23, True), "#fecaca")

    panels = [
        {
            "title": "跌倒样例：Subject 1 / Fall / 01",
            "image": ROOT / "outputs/final_rtmpose_system/fall_subject1_01/confirmed_preview.jpg",
            "probabilities": [0.0601, 0.0619, 0.0722, 0.5350, 0.9589, 0.9901, 0.9910, 0.9901, 0.9392],
            "votes": [0, 0, 0, 2, 4, 4, 4, 4, 4],
            "confirmed_at": 6,
            "facts": ["骨架有效率：100%", "V-JEPA概率：100.00%（正确）", "第 5 窗起：4/4 折同意", "第 7 窗：CONFIRMED", "最终事件：1 次跌倒"],
            "result": "正确报警",
            "result_color": "#22c55e",
        },
        {
            "title": "正常样例：Subject 1 / ADL / 01",
            "image": ROOT / "outputs/final_rtmpose_system/adl_subject1_01/normal_preview.jpg",
            "probabilities": [0.1254, 0.2531, 0.4950, 0.5102, 0.5174, 0.5250, 0.5227, 0.5235, 0.5257, 0.5235, 0.5238, 0.5237],
            "votes": [0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            "confirmed_at": None,
            "facts": ["骨架有效率：100%", "V-JEPA概率：99.89%（错误）", "平均概率部分超过 0.5", "始终仅 2/4 折同意", "最终事件：0 次"],
            "result": "成功拦截误报",
            "result_color": "#38bdf8",
        },
    ]

    panel_top = 510
    for column, panel in enumerate(panels):
        left = 70 + column * 965
        right = left + 895
        rounded(draw, (left, panel_top, right, 1435), "#0d1729")
        draw.text((left + 28, panel_top + 22), panel["title"], font=font(29, True), fill="#f8fafc")
        preview = contain(Image.open(panel["image"]), (520, 295))
        image.paste(preview, (left + 28, panel_top + 78))
        draw.rounded_rectangle((left + 575, panel_top + 82, right - 28, panel_top + 370), radius=14,
                               fill="#111c30", outline="#334155", width=2)
        for index, fact in enumerate(panel["facts"]):
            draw.text((left + 600, panel_top + 103 + index * 47), f"• {fact}", font=font(21), fill="#dbeafe")
        draw.text((left + 600, panel_top + 332), panel["result"], font=font(27, True), fill=panel["result_color"])
        plot(draw, (left + 25, panel_top + 420, right - 25, panel_top + 850),
             panel["probabilities"], panel["votes"], panel["confirmed_at"])

    rounded(draw, (70, 1465, 1930, 1620), "#112238", "#a78bfa")
    draw.text((105, 1485), "四折OOF实测：", font=font(25, True), fill="#f8fafc")
    draw.text((315, 1485), "ST-GCN++ F1 86.27%", font=font(24), fill="#e2e8f0")
    draw.text((660, 1485), "V-JEPA单路 F1 72.19%", font=font(24), fill="#c4b5fd")
    draw.text((1045, 1485), "分数融合 F1 80.45%", font=font(24), fill="#c4b5fd")
    draw.text((1405, 1485), "特征融合 F1 86.27%", font=font(24), fill="#c4b5fd")
    centered(draw, (105, 1540, 1895, 1605),
             "结论：V-JEPA 已完成实际接入与融合测试，但未超过骨架基线；当前不参与报警，下一步仅复核疑似跌倒窗口。",
             font(24, True), "#ede9fe")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    image.save(OUTPUT, quality=95)
    print(OUTPUT)


if __name__ == "__main__":
    main()
