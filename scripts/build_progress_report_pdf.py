from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Flowable,
    Frame,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output/pdf/行为检测模块阶段进展_20260812.pdf"

NAVY = colors.HexColor("#17365D")
BLUE = colors.HexColor("#2F75B5")
CYAN = colors.HexColor("#DDEBF7")
PALE = colors.HexColor("#F5F8FC")
ORANGE = colors.HexColor("#ED7D31")
GREEN = colors.HexColor("#70AD47")
TEXT = colors.HexColor("#263238")
MUTED = colors.HexColor("#64748B")
LINE = colors.HexColor("#D8E2EC")


def register_fonts() -> None:
    pdfmetrics.registerFont(TTFont("CN", r"C:\Windows\Fonts\Deng.ttf"))
    pdfmetrics.registerFont(TTFont("CN-Bold", r"C:\Windows\Fonts\Dengb.ttf"))


class SectionBand(Flowable):
    def __init__(self, number: str, title: str, width: float):
        super().__init__()
        self.number = number
        self.title = title
        self.width = width
        self.height = 13 * mm

    def draw(self) -> None:
        c = self.canv
        c.setFillColor(NAVY)
        c.roundRect(0, 1 * mm, self.width, 10 * mm, 2 * mm, fill=1, stroke=0)
        c.setFillColor(ORANGE)
        c.roundRect(3 * mm, 2.5 * mm, 16 * mm, 7 * mm, 1.5 * mm, fill=1, stroke=0)
        c.setFont("CN-Bold", 10)
        c.drawCentredString(11 * mm, 4.7 * mm, self.number)
        c.setFillColor(colors.white)
        c.setFont("CN-Bold", 14)
        c.drawString(23 * mm, 4.1 * mm, self.title)


def draw_header_footer(canvas, doc) -> None:
    canvas.saveState()
    width, height = A4
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.5)
    canvas.line(18 * mm, height - 14 * mm, width - 18 * mm, height - 14 * mm)
    canvas.setFont("CN", 8.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(18 * mm, height - 10.5 * mm, "挑战杯揭榜挂帅项目｜行为检测模块")
    canvas.drawRightString(width - 18 * mm, height - 10.5 * mm, "阶段进展报告")
    canvas.line(18 * mm, 13 * mm, width - 18 * mm, 13 * mm)
    canvas.drawString(18 * mm, 8.5 * mm, "更新时间：2026年8月12日")
    canvas.drawRightString(width - 18 * mm, 8.5 * mm, f"第 {doc.page} 页")
    canvas.restoreState()


def p(text: str, style) -> Paragraph:
    return Paragraph(text, style)


def bullet(text: str, styles) -> Paragraph:
    return Paragraph(f"<font color='#2F75B5'>●</font>&nbsp;&nbsp;{text}", styles["bullet"])


def build() -> None:
    register_fonts()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="bodyCN", fontName="CN", fontSize=10.2, leading=16, textColor=TEXT, spaceAfter=4))
    styles.add(ParagraphStyle(name="bullet", parent=styles["bodyCN"], leftIndent=2 * mm, firstLineIndent=-2 * mm, spaceAfter=3))
    styles.add(ParagraphStyle(name="h2CN", fontName="CN-Bold", fontSize=13, leading=18, textColor=NAVY, spaceBefore=7, spaceAfter=5))
    styles.add(ParagraphStyle(name="h3CN", fontName="CN-Bold", fontSize=11.2, leading=16, textColor=BLUE, spaceBefore=5, spaceAfter=3))
    styles.add(ParagraphStyle(name="small", fontName="CN", fontSize=8.5, leading=12, textColor=MUTED))
    styles.add(ParagraphStyle(name="titleCN", fontName="CN-Bold", fontSize=22, leading=30, textColor=TEXT, alignment=TA_CENTER, spaceAfter=4))
    styles.add(ParagraphStyle(name="subtitleCN", fontName="CN", fontSize=10, leading=15, textColor=MUTED, alignment=TA_CENTER, spaceAfter=12))
    styles.add(ParagraphStyle(name="box", fontName="CN", fontSize=9.3, leading=14, textColor=TEXT, alignment=TA_CENTER))
    styles.add(ParagraphStyle(name="tablehead", fontName="CN-Bold", fontSize=8.4, leading=11, textColor=colors.white, alignment=TA_CENTER))
    styles.add(ParagraphStyle(name="table", fontName="CN", fontSize=8.2, leading=11, textColor=TEXT, alignment=TA_CENTER))

    frame = Frame(18 * mm, 17 * mm, A4[0] - 36 * mm, A4[1] - 34 * mm, leftPadding=0, rightPadding=0, topPadding=4 * mm, bottomPadding=0)
    doc = BaseDocTemplate(str(OUTPUT), pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=18 * mm, bottomMargin=17 * mm, title="行为检测模块阶段进展报告", author="挑战杯项目团队")
    doc.addPageTemplates([PageTemplate(id="content", frames=[frame], onPage=draw_header_footer)])

    story = [
        Spacer(1, 8 * mm),
        p("行为检测模块阶段进展报告", styles["titleCN"]),
        p("实时跌倒检测、风险预警与多模态事件复核｜2026年8月12日", styles["subtitleCN"]),
        p("本报告说明行为检测模块当前采用的技术架构、已完成实验、系统接入状态、存在问题及下一步工作。所有指标均区分内部测试、外部测试和流程冒烟测试；尚未完成的真机闭环不作为已完成成果。", styles["bodyCN"]),
        Spacer(1, 3 * mm),
    ]
    story.append(SectionBand("01", "当前结论与初版架构", frame._width))
    story.append(p("行为检测模块的初版原型已基本确定，采用<b>“实时骨架检测 + 疑似事件多模态复核”</b>的两阶段方案。骨架模型持续筛查，多模态模型只在疑似事件触发后读取短视频片段。", styles["bodyCN"]))

    flow_rows = [
        ["摄像头视频流"], ["↓"], ["统一视频接入与帧缓存"], ["↓"],
        ["人体检测/跟踪 + 姿态关键点提取"], ["↓"], ["ST-GCN++ 时序动作识别"], ["↓"],
        ["NORMAL / SUSPECTED / CONFIRMED / COOLDOWN"], ["↓ 疑似事件"],
        ["截取事件前后 2-4 秒 RGB 视频"], ["↓"], ["Qwen3-VL / V-JEPA 复核"], ["↓"],
        ["告警等级 · 动作类别 · 原因解释 · 事件摘要"], ["↓"], ["FastAPI 接口输出至业务系统"]
    ]
    flow = Table([[p(x[0], styles["box"])] for x in flow_rows], colWidths=[132 * mm])
    ts = [("ALIGN", (0,0), (-1,-1), "CENTER"), ("VALIGN", (0,0), (-1,-1), "MIDDLE")]
    for i in range(len(flow_rows)):
        if "↓" == flow_rows[i][0] or flow_rows[i][0].startswith("↓ "):
            ts += [("BACKGROUND", (0,i), (0,i), colors.white), ("TEXTCOLOR", (0,i), (0,i), BLUE), ("TOPPADDING", (0,i), (0,i), 0), ("BOTTOMPADDING", (0,i), (0,i), 0)]
        else:
            fill = CYAN if i not in (8, 12, 14, 16) else colors.HexColor("#E2F0D9")
            ts += [("BACKGROUND", (0,i), (0,i), fill), ("BOX", (0,i), (0,i), 0.7, BLUE), ("TOPPADDING", (0,i), (0,i), 4), ("BOTTOMPADDING", (0,i), (0,i), 4)]
    flow.setStyle(TableStyle(ts))
    story += [Spacer(1, 3 * mm), flow, Spacer(1, 4 * mm)]
    story.append(p("<b>设计原则：</b>实时主链路优先保证低延迟和可审计；Qwen等大模型不逐帧常驻运行，避免阻塞检测。", styles["bodyCN"]))

    story += [PageBreak(), SectionBand("02", "骨架检测与时序分类", frame._width)]
    story.append(p("已完成7类姿态/跟踪前端与3类时序分类器的组合比较，并加入跟踪消融，共实测23条路线。", styles["bodyCN"]))
    for text in [
        "数据集：GMDCSA24，4名受试者严格隔离四折，测试覆盖全部160段视频。",
        "训练协议：每条路线每折完整训练300轮，总训练量27,600 epochs，共92个最优折模型。",
        "统一输入：COCO-17骨架、64帧窗口；以Balanced Accuracy作为核心指标。",
    ]: story.append(bullet(text, styles))
    data = [
        [p("路线", styles["tablehead"]), p("BA", styles["tablehead"]), p("F1", styles["tablehead"]), p("Recall", styles["tablehead"]), p("Specificity", styles["tablehead"])],
        [p("YOLO-Pose + ByteTrack + ST-GCN++", styles["table"]), "89.41%", "89.57%", "92.41%", "86.42%"],
        [p("RTMPose + ST-GCN++", styles["table"]), "86.83%", "86.27%", "83.54%", "90.12%"],
        [p("RTMPose + ByteTrack + ST-GCN++", styles["table"]), "86.29%", "86.59%", "89.87%", "82.72%"],
        [p("RTMPose + PoseC3D-style", styles["table"]), "86.29%", "86.59%", "89.87%", "82.72%"],
    ]
    table = Table(data, colWidths=[76 * mm, 22 * mm, 22 * mm, 25 * mm, 27 * mm], repeatRows=1)
    table.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,0), NAVY), ("FONTNAME", (1,1), (-1,-1), "CN"), ("FONTSIZE", (1,1), (-1,-1), 8.5), ("ALIGN", (1,1), (-1,-1), "CENTER"), ("VALIGN", (0,0), (-1,-1), "MIDDLE"), ("GRID", (0,0), (-1,-1), 0.5, LINE), ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, PALE]), ("TOPPADDING", (0,0), (-1,-1), 6), ("BOTTOMPADDING", (0,0), (-1,-1), 6)]))
    story += [Spacer(1, 3 * mm), table]
    story.append(p("内部冠军为YOLO-Pose + ByteTrack + ST-GCN++；综合MCFD外部测试，RTMPose + ST-GCN++的内部与跨数据集表现更均衡，当前作为稳健单路线首选。ByteTrack保留为可选开关。", styles["bodyCN"]))

    story += [PageBreak(), SectionBand("03", "多模态模型实跑结果", frame._width)]
    story.append(p("<b>V-JEPA 2.1：</b>已完成160段视频的768维RGB语义特征提取与300轮分类/融合训练。整段采样单路BA为70.71%，骨架定位疑似窗口后提升至80.01%；与RTMPose + ST-GCN++后融合达到87.51%，但受试者间增益不稳定。", styles["bodyCN"]))
    story.append(p("<b>Qwen3-VL：</b>已完成视频零样本二分类、五分类和结构化输出实验。平衡50段五分类初筛准确率为76%；MCFD-192二分类外测BA为72.92%、特异度98.96%，但跌倒召回率仅46.88%，适合高置信复核，不适合单独承担安全主链路。", styles["bodyCN"]))
    story.append(p("<b>Qwen3-VL + QLoRA：</b>使用123段训练视频、约321万个LoRA参数完成3轮微调。验证最佳Macro-F1为86.45%、BA为87.50%；外测BA为69.27%。微调消除了结构化解析错误，但尚未提升跨数据集泛化。", styles["bodyCN"]))
    multimodal_data = [
        [p("多模态路线", styles["tablehead"]), p("评价集", styles["tablehead"]), p("关键指标", styles["tablehead"]), p("当前定位", styles["tablehead"])],
        [p("V-JEPA疑似窗口", styles["table"]), "GMDCSA24", "BA 80.01%", p("低成本视频语义分支", styles["table"])],
        [p("骨架 + V-JEPA后融合", styles["table"]), "GMDCSA24", "BA 87.51%", p("实验开关，尚不默认上线", styles["table"])],
        [p("Qwen零样本", styles["table"]), "MCFD-192", "BA 72.92%", p("高置信事件确认", styles["table"])],
        [p("Qwen + QLoRA", styles["table"]), "MCFD-192", "BA 69.27%", p("稳定结构化输出", styles["table"])],
    ]
    mt = Table(multimodal_data, colWidths=[49 * mm, 31 * mm, 34 * mm, 58 * mm], repeatRows=1)
    mt.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),NAVY),("FONTNAME",(1,1),(2,-1),"CN"),("FONTSIZE",(1,1),(2,-1),8.5),("ALIGN",(1,1),(2,-1),"CENTER"),("GRID",(0,0),(-1,-1),0.5,LINE),("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white,PALE]),("VALIGN",(0,0),(-1,-1),"MIDDLE"),("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6)]))
    story += [Spacer(1, 3 * mm), mt, Spacer(1, 4 * mm)]
    story.append(p("InternVideo3、LLM-AR已列为后续候选，但尚无与现有协议一致的完整实跑结果，暂不纳入性能排名。", styles["small"]))

    story += [PageBreak(), SectionBand("04", "系统原型与摄像头接入", frame._width)]
    story.append(p("<b>本地系统链路已经跑通：</b>视频解码 → YOLO-Pose → 64帧骨架窗口 → 四折ST-GCN++ → 告警状态机 → FastAPI。", styles["bodyCN"]))
    for text in [
        "FastAPI已提供启动/停止、运行状态、事件查询、最新标注帧和MJPEG预览接口。",
        "本地视频冒烟测试处理77帧，姿态有效率100%，最新单次推理延迟约12-16 ms。",
        "8段流程测试中，4段跌倒均确认告警，4段日常活动均未报警；仅用于流程验证，不代替无偏准确率。",
        "当前代码18项自动化测试全部通过。",
    ]: story.append(bullet(text, styles))
    story.append(p("摄像头接入采用<b>路线A：保持视频加密，通过EZOPEN + 官方Windows PC SDK + 设备验证码取流</b>。摄像头在线，应用、Token、设备识别和SDK连接均成功。", styles["bodyCN"]))
    status_data = [
        [p("环节", styles["tablehead"]), p("状态", styles["tablehead"]), p("说明", styles["tablehead"])],
        ["开放平台鉴权", "已完成", p("应用与AccessToken可用", styles["table"])],
        ["官方SDK连接", "已完成", p("Windows x64 SDK正常加载", styles["table"])],
        ["加密EZOPEN取流", "受阻", p("两次返回525546：VTDU两路并发已满", styles["table"])],
        ["实时帧进入检测", "待验证", p("尚未取得真机视频帧", styles["table"])],
    ]
    st = Table(status_data, colWidths=[43 * mm, 30 * mm, 99 * mm], repeatRows=1)
    st.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),NAVY),("FONTNAME",(0,1),(1,-1),"CN"),("FONTSIZE",(0,1),(1,-1),8.5),("ALIGN",(0,1),(1,-1),"CENTER"),("GRID",(0,0),(-1,-1),0.5,LINE),("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white,PALE]),("VALIGN",(0,0),(-1,-1),"MIDDLE"),("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6)]))
    story += [Spacer(1, 2 * mm), st, Spacer(1, 4 * mm)]
    story.append(p("测试未抢占、停止其他组员的视频流，也未修改摄像头设置。当前真机闭环尚未完成，原因是平台取流并发资源被占用，而不是检测模型或SDK代码无法运行。", styles["bodyCN"]))

    story += [PageBreak(), SectionBand("05", "问题、调整方向与下一步", frame._width)]
    story.append(p("<b>当前主要问题</b>", styles["h2CN"]))
    for text in [
        "萤石仅有两路VTDU并发；各模块分别直接拉流会重复占用并发。",
        "公开数据与真实老人居家场景存在视角、遮挡、光照和动作差异。",
        "当前路线对“正在跌倒/已经跌倒”的检测较充分，对跌倒发生前的风险预测仍需加强。",
        "Qwen/QLoRA的原因描述可能受训练模板影响，不能直接作为真实因果结论。",
    ]: story.append(bullet(text, styles))
    story.append(p("<b>根据指导意见补充风险预警分支</b>", styles["h2CN"]))
    story.append(p("在现有跌倒检测前增加预跌倒预测：识别步态不稳、连续晃动、踉跄、失去支撑等前兆，预测未来1-3秒跌倒风险，并以预警召回率、平均提前时间和每小时误报次数评价。", styles["bodyCN"]))
    risk = Table([[p("视频/骨架时序",styles["box"]),"→",p("失稳与前兆识别",styles["box"]),"→",p("未来1-3秒风险",styles["box"]),"→",p("分级预警",styles["box"])]], colWidths=[34*mm,8*mm,39*mm,8*mm,37*mm,8*mm,38*mm])
    risk.setStyle(TableStyle([("BACKGROUND",(0,0),(0,0),CYAN),("BACKGROUND",(2,0),(2,0),CYAN),("BACKGROUND",(4,0),(4,0),colors.HexColor("#FFF2CC")),("BACKGROUND",(6,0),(6,0),colors.HexColor("#FCE4D6")),("BOX",(0,0),(0,0),0.7,BLUE),("BOX",(2,0),(2,0),0.7,BLUE),("BOX",(4,0),(4,0),0.7,ORANGE),("BOX",(6,0),(6,0),0.7,ORANGE),("ALIGN",(0,0),(-1,-1),"CENTER"),("VALIGN",(0,0),(-1,-1),"MIDDLE"),("FONTNAME",(1,0),(5,0),"CN-Bold"),("TEXTCOLOR",(1,0),(5,0),BLUE),("TOPPADDING",(0,0),(-1,-1),8),("BOTTOMPADDING",(0,0),(-1,-1),8)]))
    story += [Spacer(1, 2*mm), risk, Spacer(1, 4*mm)]
    story.append(p("<b>近期执行顺序</b>", styles["h2CN"]))
    for text in [
        "协调释放一路预览会话，完成15-30秒真机取流、实时解码和告警闭环。",
        "建立一次拉流、多模块共享的视频服务；各模型使用独立有界队列。",
        "重新标注NORMAL、UNSTABLE、STUMBLE、PRE_FALL、FALLING、FALLEN等阶段，严格避免模型看到跌倒后的画面。",
        "采集现场数据，统计事件级召回率、误报次数/小时、提前预警时间和端到端延迟。",
        "完成与师兄业务系统的接口联调和部署说明。",
    ]: story.append(bullet(text, styles))

    story += [PageBreak(), SectionBand("06", "统一视频接入与当前交付状态", frame._width)]
    story.append(p("正式系统采用<b>“一次萤石拉流，多模块共享”</b>，从架构上避免各模块分别消耗云端并发。", styles["bodyCN"]))
    shared = [
        [p("萤石摄像头（仅占用一路）", styles["box"])], ["↓"], [p("统一拉流 / 解码 / 帧缓存服务", styles["box"])], ["↓"],
        [p("跌倒检测　｜　心理状态分析　｜　行为识别　｜　多模态复核　｜　Web预览", styles["box"])],
    ]
    sv = Table(shared, colWidths=[150*mm])
    sv.setStyle(TableStyle([("ALIGN",(0,0),(-1,-1),"CENTER"),("BACKGROUND",(0,0),(0,0),CYAN),("BOX",(0,0),(0,0),0.8,BLUE),("BACKGROUND",(0,2),(0,2),colors.HexColor("#E2F0D9")),("BOX",(0,2),(0,2),0.8,GREEN),("BACKGROUND",(0,4),(0,4),colors.HexColor("#FFF2CC")),("BOX",(0,4),(0,4),0.8,ORANGE),("FONTNAME",(0,1),(0,3),"CN-Bold"),("TEXTCOLOR",(0,1),(0,3),BLUE),("TOPPADDING",(0,0),(-1,-1),7),("BOTTOMPADDING",(0,0),(-1,-1),7)]))
    story += [Spacer(1, 3*mm), sv, Spacer(1, 7*mm)]
    deliver = [
        [p("当前可交付", styles["tablehead"]), p("仍待完成", styles["tablehead"])],
        [p("初版技术架构<br/>23条骨架路线实验<br/>V-JEPA / Qwen / QLoRA实跑结果<br/>本地视频检测程序<br/>告警状态机与FastAPI原型<br/>萤石官方SDK接入代码", styles["bodyCN"]), p("萤石真机实时视频帧闭环<br/>统一视频共享服务<br/>预跌倒风险预测分支<br/>现场数据采集与测试<br/>与业务系统最终联调", styles["bodyCN"])],
    ]
    dt = Table(deliver, colWidths=[86*mm,86*mm])
    dt.setStyle(TableStyle([("BACKGROUND",(0,0),(0,0),GREEN),("BACKGROUND",(1,0),(1,0),ORANGE),("GRID",(0,0),(-1,-1),0.7,LINE),("VALIGN",(0,0),(-1,-1),"TOP"),("BACKGROUND",(0,1),(-1,1),PALE),("TOPPADDING",(0,0),(-1,-1),8),("BOTTOMPADDING",(0,0),(-1,-1),8),("LEFTPADDING",(0,1),(-1,1),10)]))
    story += [dt, Spacer(1, 8*mm)]
    story.append(p("阶段判断：检测、复核和服务化技术底座已经形成；下一阶段重点由“继续增加模型”转向“真机闭环、统一视频接入、预跌倒标签与提前量评价”。", ParagraphStyle(name="conclusion", parent=styles["bodyCN"], fontName="CN-Bold", fontSize=11, leading=18, textColor=NAVY, backColor=CYAN, borderColor=BLUE, borderWidth=0.7, borderPadding=10, alignment=TA_LEFT)))

    doc.build(story)
    print(OUTPUT)


if __name__ == "__main__":
    build()
