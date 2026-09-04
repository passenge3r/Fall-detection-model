from pathlib import Path
import math
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent / "当前技术路线工作流_关键子模块.png"
FONT = Path("C:/Windows/Fonts/msyh.ttc")
BOLD = Path("C:/Windows/Fonts/msyhbd.ttc")


def ft(size, bold=False):
    return ImageFont.truetype(str(BOLD if bold else FONT), size)


def node(draw, box, text, color, fill="#FFFFFF"):
    x0, y0, x1, y1 = box
    draw.rounded_rectangle((x0+9, y0+10, x1+9, y1+10), radius=25, fill="#DEE7EC")
    draw.rounded_rectangle(box, radius=25, fill=fill, outline=color, width=4)
    draw.text(((x0+x1)//2, (y0+y1)//2), text, font=ft(34, True),
              fill="#153852", anchor="mm", align="center", spacing=8)


def arrow(draw, start, end, color="#8095A4", width=7):
    draw.line((start, end), fill=color, width=width)
    x1, y1 = end
    x0, y0 = start
    angle = math.atan2(y1-y0, x1-x0)
    size = 21
    p1 = (x1-size*math.cos(angle-.52), y1-size*math.sin(angle-.52))
    p2 = (x1-size*math.cos(angle+.52), y1-size*math.sin(angle+.52))
    draw.polygon([end, p1, p2], fill=color)


img = Image.new("RGB", (1920, 1080), "white")
d = ImageDraw.Draw(img)

d.text((95, 70), "当前技术路线工作流", font=ft(58, True), fill="#153852")
d.text((98, 150), "关键子模块", font=ft(29), fill="#6A7A85")

boxes = {
    "input": (85, 330, 345, 535),
    "pose": (420, 330, 680, 535),
    "gcn": (755, 330, 1015, 535),
    "risk": (1090, 330, 1350, 535),
    "qwen": (1090, 740, 1350, 945),
    "api": (1515, 535, 1790, 740),
}

node(d, boxes["input"], "视频接入\n与缓存", "#183B56")
node(d, boxes["pose"], "YOLO-Pose\n+ ByteTrack", "#2878B5")
node(d, boxes["gcn"], "ST-GCN++", "#39A7C7")
node(d, boxes["risk"], "风险状态机", "#E89A3D", "#FFFBF4")
node(d, boxes["qwen"], "Qwen3-VL\n事件复核", "#4D9F65", "#F5FBF7")
node(d, boxes["api"], "FastAPI\n系统输出", "#183B56", "#F5F8FA")

# Main real-time route
arrow(d, (345, 432), (410, 432))
arrow(d, (680, 432), (745, 432))
arrow(d, (1015, 432), (1080, 432))

# Direct system output
arrow(d, (1355, 430), (1508, 600), color="#2878B5")
d.text((1460, 430), "实时输出", font=ft(25, True), fill="#2878B5", anchor="mm")

# Triggered multimodal review
arrow(d, (1220, 545), (1220, 725), color="#4D9F65")
d.text((1360, 635), "HIGH / FALL触发", font=ft(25, True), fill="#4D9F65", anchor="mm")
arrow(d, (1360, 842), (1505, 680), color="#4D9F65")

# Minimal role labels, not nodes
d.rounded_rectangle((95, 890, 865, 990), radius=20, fill="#EAF3F8")
d.text((130, 940), "骨架分支持续运行｜多模态分支按事件触发", font=ft(27, True),
       fill="#1F628B", anchor="lm")

img.save(OUT, quality=95)
print(OUT)
