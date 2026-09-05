# -*- coding: utf-8 -*-
"""gen-paper-0905.py — 2026-09-05 AI 早报/晚报内容生成
产出 examples/morning-0905.json（浅皮 morning）/ examples/evening-0905.json（深皮 evening）。
数据均来自 2026-09-04/05 公开报道（新华社/人民日报/21经济报道/财经/The CODEW/AIToolsRecap/Smartotics 等）。
"""
import json, os

D = "2026-09-05"

def news(section, content, points=None, stats=None, narration="", subtitle="", source="",
         summary=None, facts=None, highlight=None, kind="text", data=None):
    b = {"type": kind, "content": content, "section": section, "narration": narration,
         "subtitle": subtitle, "source": source}
    if points: b["points"] = points
    if stats: b["stats"] = [{"label": l, "value": v} for l, v in stats]
    if summary: b["summary"] = summary
    if facts: b["facts"] = facts
    if highlight: b["highlight"] = highlight
    if data: b["data"] = data
    return b

blocks = [
    # ---- 封面 ----
    {"type": "title", "content": "AI 早报 · 9月5日 · 周六",
     "narration": "早上好，今天是9月5日星期六，一起来看今天的AI早报。",
     "subtitle": "GPT-6 Astra 面世，超级智能时代宣言"},

    # ---- 要闻 ai-news ----
    news("ai-news", "GPT-6 Astra 面世：OpenAI 宣布「超级智能时代」到来",
         summary="OpenAI 凌晨发布新一代旗舰 GPT-6 Astra，官方定义为「目前全球最智能且对齐程度最高的模型」。训练动用超 10 万块 GPU，API 定价涨至上一代 2.5 倍。总裁 Brockman 收尾一句话：欢迎来到 AGI 时代。",
         facts=[
             "首个触发 Preparedness Framework「Critical」网安阈值的 OpenAI 模型",
             "Computer Use：接收高层目标后自主规划步骤，操作浏览器、读写文件、编写运行代码，出错自动回溯调试",
             "最强网安能力仅走 Daybreak 受邀计划，首批伙伴为 MS-ISAC 州级网络防御者与水务系统",
             "分批灰度上线：机构用户优先，订阅用户与 API 开发者数日后完整开放",
         ],
         stats=[("训练 GPU", "10万+"), ("API 定价", "$10/$50 ≈ 2.5×")],
         narration="头条是OpenAI的GPT-6 Astra。十万块GPU训练出的新旗舰，能自主操作电脑完成整套工作流，网安能力首次触发最高风险阈值，受限开放。",
         subtitle="首个触发 Critical 网安阈值的模型", highlight="GPT-6 Astra",
         source="OpenAI · 21世纪经济报道"),

    news("ai-news", "英伟达 129 亿美元收购 Hugging Face 官宣",
         points=["从传闻到官宣：129 亿美元收购落锤",
                 "开源模型的默认「家」正式归入芯片巨头旗下",
                 "官方承诺保持开放，社区规矩能否延续仍待观察"],
         stats=[("交易金额", "$129亿")],
         narration="第二落锤：英伟达129亿美元收购Hugging Face官宣。开源模型的默认之家并入芯片巨头，官方承诺保持开放，但规矩能否延续要看后续。",
         subtitle="开源大本营易主", highlight="Hugging Face", source="大模型晨报"),

    news("ai-news", "Anthropic：Fable 5.1 / Mythos 5.1 发布，IPO 临近",
         points=["Claude Fable 5.1：Agent 工作负载成本最高降 45%",
                 "Mythos 5.1 走网安与生命科学验证计划开放",
                 "报道称 9 月 7 日递交 IPO 招股书",
                 "年化营收约 470 亿美元，Q2 运营利润 5.59 亿"],
         stats=[("年化营收", "$47B"), ("IPO 递交", "9月7日")],
         narration="Anthropic 一周内连发Fable 5.1和Mythos 5.1，前者主打Agent成本直降四成五。同时据报道IPO招股书9月7日递交，年化营收已达470亿美元。",
         subtitle="双模型发布 + IPO 冲刺", highlight="Fable 5.1", source="The CODEW"),

    news("ai-news", "Google 收官：Gemini 3.8 Flash + 音乐模型 Lyria 3.5",
         points=["Gemini 3.8 Flash 正式发布，主打低延迟推理",
                 "Lyria 3.5 音乐生成模型上线 Gemini App 与 API",
                 "OpenAI、谷歌、Meta、Anthropic 一周内全部出牌"],
         narration="谷歌本周收官：Gemini 3.8 Flash与音乐模型Lyria 3.5同日上线。至此四大实验室在一周内全部完成旗舰发布，秋季发布潮进入最高潮。",
         subtitle="四大实验室一周全部出牌", highlight="Gemini 3.8", source="The CODEW"),

    news("ai-news", "K2 Horizon：今年首个「真开源」模型家族",
         points=["六个模型，参数跨度 0.9B 到 375B",
                 "权重、训练代码、训练数据、checkpoint、日志全部公开",
                 "今年首个满足开源定义的发布：可复现、可审计",
                 "开源界今夏多次质疑的「只有权重」模式被打破"],
         stats=[("模型数量", "6 个"), ("参数跨度", "0.9B–375B")],
         narration="开源侧的重磅：K2 Horizon一次放出六个模型，从9亿到3750亿参数，连训练数据和日志都公开，成为今年首个经得起复现和审计的真开源发布。",
         subtitle="连训练数据都公开了", highlight="K2 Horizon", source="AIToolsRecap"),

    # ---- 国内 cn-news ----
    news("cn-news", "沙特 humain 推出 MiniMax 打造的阿语大模型 humain-m3",
         points=["沙特胡迈因公司委托中国稀宇科技开发",
                 "基于 MiniMax M3：4280 亿参数混合专家模型",
                 "超 1 万亿阿拉伯语原生 token 二次预训练",
                 "7 项公开阿语基准平均分居参与模型之首"],
         stats=[("参数量", "4280亿"), ("阿语 Token", "1万亿+")],
         narration="国产模型出海标杆：沙特AI公司推出基于MiniMax M3的阿语大模型humain-m3，4280亿参数，用超万亿阿语原生语料继续预训练，七项基准平均分第一。",
         subtitle="中国模型出海中东", highlight="humain-m3", source="新华社 · 人民日报"),

    news("cn-news", "DeepSeek：营收 10 倍增长，算力投入 110 亿",
         points=["前 7 个月营收约 4.75 亿元，为去年全年 10 倍",
                 "AI 基础设施支出约 110 亿元",
                 "估值约 5000 亿元，启动第二轮融资",
                 "V4-Flash 高峰价百万 token 3 元，不到 GPT-4 的 1%"],
         stats=[("营收增速", "10×"), ("估值", "≈5000亿")],
         narration="DeepSeek前七月营收4.75亿元，是去年全年的十倍，但算力支出高达110亿。估值约五千亿并启动二轮融资，V4-Flash价格战把门槛打到GPT-4的百分之一。",
         subtitle="收入翻十倍，烧钱更猛", highlight="DeepSeek", source="财经 · 凤凰网"),

    {"type": "chart", "content": "DeepSeek：收入与算力投入对比（前 7 月，亿元）",
     "section": "cn-news", "source": "财经 · 凤凰网",
     "data": [{"label": "营收", "value": 4.75}, {"label": "算力支出", "value": 110}],
     "narration": "一张图看懂DeepSeek的打法：营收4.75亿，算力投入110亿，二十三倍的差距，全押在基础设施上。",
     "subtitle": "23 倍投入差换增长", "highlight": "算力投入"},

    news("cn-news", "豆包多 Agent 并行 + 全球首款 AI 智能体手机入网",
         points=["豆包工作上线多 Agent 并行架构：写报告、整数据、出图表分工协作",
                 "原生 Mac GUI 操作：直接「看见」桌面，自主点击输入拖拽",
                 "努比亚 NaviX Ultra 获工信部入网：全球首款 AI 智能体手机",
                 "搭载豆包手机助手，可跨应用自主执行任务，9 月发售"],
         narration="Agent落地加速：豆包工作支持多智能体并行和Mac本地GUI操作。努比亚NaviX Ultra全球首款AI智能体手机入网，跨应用自主干活，下月开卖。",
         subtitle="AI 办公进入「真动手」时代", highlight="豆包", source="科技日报"),

    # ---- 环球 intl-news ----
    news("intl-news", "韩国半导体出口暴涨 209%，AI 芯片重塑贸易流",
         points=["8 月半导体出口 466.5 亿美元，同比增 209%",
                 "创历史单月纪录",
                 "AI 芯片热潮持续改写全球贸易格局"],
         stats=[("同比增速", "+209%"), ("8月出口", "$466.5亿")],
         narration="看环球：韩国8月半导体出口466.5亿美元，同比暴涨两倍多创历史纪录，AI芯片需求是唯一引擎。",
         subtitle="AI 芯片是唯一引擎", highlight="+209%", source="The CODEW"),

    news("intl-news", "Grok 4.7 定档 + 阿里预览 Qwen4 架构",
         points=["马斯克预告：Grok 4.7 定档 9 月 12 日前后",
                 "阿里预览 Qwen4 架构：新增利用系统内存的组件",
                 "Qwen3.8-27B Apache 2.0 下载量破 525 万",
                 "Qwen4 正式版窗口临近"],
         stats=[("Qwen3.8-27B 下载", "525万+")],
         narration="发布潮还没完：Grok 4.7定档9月12日。阿里预览Qwen4架构，亮点是能调用系统内存的组件，27B开源版下载量已破五百万。",
         subtitle="下一波发布已在路上", highlight="Qwen4", source="Fortune · HF社区"),

    # ---- 行业 other-news ----
    news("other-news", "Azure 宕机拖垮五大 AI 服务；Gimlet 融资 3 亿美元",
         points=["Azure 数据中心故障，五大主流 AI 服务同时中断",
                 "AI 创业公司 Gimlet 获 a16z 领投 3 亿美元，估值 30 亿",
                 "Nanya 宣布 2027 年 60 亿美元支出押注 AI 内存"],
         narration="行业面：Azure一次宕机放倒五大AI服务，云依赖的脆弱性暴露无遗。同期Gimlet拿下3亿美元融资，AI内存也在被疯抢。",
         subtitle="云依赖的脆弱一天", highlight="Azure", source="The CODEW"),

    news("other-news", "全美第二大学区全面禁止学生使用 AI",
         points=["洛杉矶联合学区颁布 sweeping 禁令",
                 "迄今针对课堂 AI 最大规模的制度性反弹",
                 "与本周的发布狂潮形成鲜明对照"],
         narration="冷一面：全美第二大的洛杉矶学区全面禁止学生使用AI，是迄今最大规模的制度性反弹。技术狂奔，共识还没跟上。",
         subtitle="技术狂奔，治理滞后", highlight="学区禁令", source="Smartotics"),

    news("other-news", "果蝇完整神经系统图谱绘出：16.6 万神经元",
         points=["Google Research 联合 HHMI Janelia 完成",
                 "覆盖超 16.6 万个神经元、1.25 亿个突触",
                 "迄今最完整的高等动物连接组之一"],
         stats=[("神经元", "16.6万"), ("突触", "1.25亿")],
         narration="最后一条轻松的：谷歌联合Janelia绘出雄性果蝇完整神经系统，16.6万个神经元、1.25亿突触。AI研究反过来也在推动神经科学。",
         subtitle="AI × 神经科学交叉", highlight="连接组", source="AIToolsRecap"),
]

def make(style, edition, title_content, run_id):
    import copy
    blks = copy.deepcopy(blocks)
    blks[0]["content"] = title_content  # 封面大字随场次：早报/晚报
    cfg = {
        "style": style, "template": "news-paper", "title": f"2026年9月5日 · 星期六 · {'早间档' if edition == 'morning' else '晚间档'}",
        "subtitle": "全网 AI 要闻一页看尽", "edition": edition, "runId": run_id,
        "footer": "AI 早报 · 内容基于公开报道",
        "blocks": blks,
    }
    # 无 timeline 时的默认帧数：title 75 帧 + 其余每块 90 帧（与 framesForBlock 一致）
    total = 75 + 90 * (len(blks) - 1)
    return {"config": cfg, "timeline": {"entries": [], "totalFrames": total, "fps": 30}}

here = os.path.dirname(os.path.abspath(__file__))
out = os.path.join(here, "..", "examples")
os.makedirs(out, exist_ok=True)

for name, (style, edition, tc, rid) in {
    "morning-0905.json": ("news-paper", "morning", "AI 早报", f"ai-news-morning-{D}"),
    "evening-0905.json": ("news-paper", "evening", "AI 晚报", f"ai-news-evening-{D}"),
}.items():
    path = os.path.join(out, name)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(make(style, edition, tc, rid), f, ensure_ascii=False, indent=2)
    n = len(json.load(open(path, encoding="utf-8"))["config"]["blocks"])
    print(f"{name}: {n} blocks")
