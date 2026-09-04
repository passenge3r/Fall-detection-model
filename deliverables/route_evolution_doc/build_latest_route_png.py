from pathlib import Path
import math
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent / "当前最新技术路线_答辩PPT版.png"
FONT = Path("C:/Windows/Fonts/msyh.ttc")
BOLD = Path("C:/Windows/Fonts/msyhbd.ttc")


def font(size, bold=False):
    return ImageFont.truetype(str(BOLD if bold else FONT), size)


def rounded(draw, box, outline, fill="#FFFFFF", radius=26, width=4, shadow=True):
    x0, y0, x1, y1 = box
    if shadow:
        draw.rounded_rectangle((x0+9, y0+10, x1+9, y1+10), radius=radius, fill="#DDE6EC")
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def centered(draw, box, title, sub, color):
    x0, y0, x1, y1 = box
    cx = (x0+x1)//2
    draw.text((cx, y0+72), title, font=font(35, True), fill="#153852", anchor="mm")
    draw.multiline_text((cx, y0+148), sub, font=font(24), fill="#5B6B76",
                        anchor="mm", align="center", spacing=10)
    draw.ellipse((cx-21, y0-25, cx+21, y0+17), fill=color)


def arrow(draw, start, end, color="#8196A5", width=7):
    draw.line((start, end), fill=color, width=width)
    x1, y1 = end
    x0, y0 = start
    a = math.atan2(y1-y0, x1-x0)
    s = 20
    p1 = (x1-s*math.cos(a-.52), y1-s*math.sin(a-.52))
    p2 = (x1-s*math.cos(a+.52), y1-s*math.sin(a+.52))
    draw.polygon([end, p1, p2], fill=color)


img = Image.new("RGB", (1920, 1080), "white")
d = ImageDraw.Draw(img)

d.text((90, 65), "当前最新技术路线", font=font(57, True), fill="#153852")
d.text((92, 140), "骨架实时预警 + 多模态触发复核", font=font(29), fill="#637581")

# Real-time chain
main_boxes = [
    ((75, 300, 325, 525), "视频接入", "萤石 / 本地\n统一拉流与缓存", "#183B56"),
    ((400, 300, 650, 525), "骨架提取", "RTMPose\nCOCO-17", "#2878B5"),
    ((725, 300, 975, 525), "时序分析", "ST-GCN++\n64帧滑窗", "#39A7C7"),
    ((1050, 300, 1340, 525), "双任务输出", "跌倒检测\n1 / 2 / 3秒预测", "#E89A3D"),
    ((1415, 300, 1805, 525), "风险分级", "NORMAL · LOW · MEDIUM\nHIGH · FALL", "#D06B48"),
]

for box, title, sub, color in main_boxes:
    rounded(d, box, color)
    centered(d, box, title, sub, color)

for i in range(len(main_boxes)-1):
    b1 = main_boxes[i][0]
    b2 = main_boxes[i+1][0]
    arrow(d, (b1[2]+12, (b1[1]+b1[3])//2), (b2[0]-12, (b2[1]+b2[3])//2))

# Triggered review branch
qwen_box = (985, 700, 1325, 915)
api_box = (1460, 700, 1805, 915)
rounded(d, qwen_box, "#4D9F65", fill="#F5FBF7")
centered(d, qwen_box, "Qwen3-VL复核", "触发前后RGB片段\n确认 · 解释 · 摘要", "#4D9F65")
rounded(d, api_box, "#183B56", fill="#F5F8FA")
centered(d, api_box, "FastAPI输出", "告警 · 概率 · 事件\n接入业务系统", "#183B56")

risk = main_boxes[-1][0]
arrow(d, ((risk[0]+risk[2])//2, risk[3]+15), ((qwen_box[0]+qwen_box[2])//2, qwen_box[1]-15), color="#4D9F65")
d.text((1410, 635), "HIGH / FALL 触发", font=font(25, True), fill="#4D9F65", anchor="mm")
arrow(d, (qwen_box[2]+15, (qwen_box[1]+qwen_box[3])//2), (api_box[0]-15, (api_box[1]+api_box[3])//2), color="#4D9F65")

# Direct alert path: skeleton alert does not wait for Qwen
arrow(d, (risk[2]-30, risk[3]+15), (api_box[0]+150, api_box[1]-15), color="#2878B5")
d.text((1600, 610), "实时告警直达", font=font(24, True), fill="#2878B5", anchor="mm")

# Key design note
d.rounded_rectangle((90, 925, 900, 1010), radius=18, fill="#EAF3F8")
d.text((125, 968), "骨架立即预警｜Qwen异步复核｜复核失败不撤销告警",
       font=font(25, True), fill="#1E5E87", anchor="lm")

img.save(OUT, quality=95)
print(OUT)
