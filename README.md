# news-paper — 聚合页纸媒视频模板

对标 B 站《AI早报/晚报》的"新闻聚合页"版式，用 Remotion 实现的**可编程视频模板**。
整片如同一份带 Tabs 的资讯概览界面，一条新闻 = 卡片屏 → 插入素材屏 → 下一条。

> 版式逆向自《AI早报》（橘鸦Juya）与《AI晚报》（黑鸦Heya）共 6 部样本的逐帧分析；
> 在其版式语法之上加入了自己的特色（见下）。

## 版式骨架（保持对标不变）

- **顶部板块 tab**：Intro / 要闻 / 开发生态 / 模型发布 / 产品应用 / 技术与洞察 / 行业动态 / 前瞻与传闻（随内容 section 联动高亮）
- **底部猫猫分块进度条（CatProgress）**：章节分栏（宽度按各栏新闻条数比例），栏内每条新闻一个小格——已播格填满黄纹、当前格随进度填充；小猫沿整条轨道跑动（移植自 EduEvidence engine kit 的 ProgressCat，确定性 sin(f) 动画）
- **大标题**：浅皮深红 `#C0392B` / 深皮暖白 `#F5F1E8`
- **内容模板 T1-T6**：
  | 模板 | 触发 | 结构 |
  |---|---|---|
  | T6 1×3 | 3 个要点 | 一行三卡 |
  | T3 2×2 | 4 个要点 | 两行两卡 |
  | T4 3+2 | 5 个要点 | 上三下二 |
  | 2×3 | ≥6 个要点 | 两行三卡 |
  | T5 文章特写 | summary/facts | 白卡 + 事实逐条 + 来源行 |
  | 插入素材 | image/video 块 | S1 全屏 / S2 大幅 / S3 居中证据卡 |
- **频道贴纸**：底部日期 chip（从 runId 提取"今天是M月D日 周X"）
- **字幕直接渲染**：旁白全文常驻显示（不压缩、无胶囊底），浅皮深字白描边 / 深皮白字黑描边，位于猫轨道上方
- **卡片聚光**：同屏多卡时，正在解说的卡亮色边框

## 我方的特色创新

1. **来源可信条 TrustLine**：每卡底部 `来源 · 已核验快照`（事实必须绑定来源快照的纪律上屏）
2. **自动模板路由**：内容侧零标记——按要点数自动选模板，image/video 自动进插入层
3. **场次自动换肤**：`style="news-paper"` 时 morning=浅皮 / evening=深皮，双档零配置
4. **数字弹跳 number-pop**：stats/highlight 值 spring 弹出，全片硬上限 3 次
5. **图表真渲染**：chart 块原生条形图 + 生长动画（对标是贴原图截图）
6. **全确定性动画**：仅 useCurrentFrame + spring/interpolate，可 seek、可复现、无随机
7. **音频层**：片头记忆点 earcon（ffmpeg 合成纯五度上行）+ 极低音量 BGM 循环（0.06）+ 每块开头 whoosh 切屏音（0.22）+ 逐段旁白
8. **配音管线工具**：`tools/gen-paper-0905.py`（内容生成）→ CosyVoice3 `synth.py --segments --speed 1.35` → `tools/thick-voice.py`（lowshelf 增厚 + ffprobe 实测时长生成 timeline + 拷 public）→ 渲染

## 快速开始

```bash
npm install
npm run studio          # 预览（默认加载 examples/light.json）
npm run render:light    # 渲染浅皮示例 → out/demo-light.mp4
npm run render:dark     # 渲染深皮示例 → out/demo-dark.mp4
```

GPU 加速（NVENC）：

```bash
npx remotion render src/index.ts NewsPaper out/demo.mp4 \
  --props=examples/light.json --hardware-acceleration=if-possible
```

## 接入你自己的内容

传入 `--props=my.json`，结构：

```jsonc
{
  "config": {
    "style": "news-paper",          // 或 "news-paper-dark" 强制深皮
    "template": "news-paper",
    "title": "AI 早报",
    "runId": "ai-news-morning-2026-09-04",  // 贴纸日期来源
    "edition": "morning",           // evening + news-paper = 自动深皮
    "blocks": [
      { "type": "title", "content": "2026-09-04 资讯概览", "subtitle": "字幕" },
      {
        "type": "text",
        "content": "新闻大标题",
        "points": ["小标题：要点正文", "…"],   // 3/4/5/6+ 条自动选网格
        "source": "OpenAI",
        "highlight": "GPT-6 Astra",           // 行内 chip + 底部词条
        "subtitle": "随口播的字幕句"
      },
      {
        "type": "image",                       // 一条新闻中间插截图/录屏
        "src": "/shot.png",
        "evidence": { "scale": "card", "caption": "证据说明" }
      }
    ]
  },
  "timeline": {                       // 可选：无则每块回退 75/90 帧
    "entries": [{ "blockIndex": 0, "audioPath": null, "audioDurationSec": 2.5, "targetFrames": 75, "globalStartSec": 0 }],
    "totalFrames": 525,
    "fps": 30
  }
}
```

带旁白时 `audioPath` 填 public 下相对路径，模板自动在对应段落挂 `<Audio>`。

## 在 motion/producer 中使用

该模板已集成进 motion monorepo（`code/producer/src/compositions/news-paper/`）：
`config.template = "news-paper"` + `config.style = "news-paper" | "news-paper-dark"` 即可路由，
块字段与 producer `src/data/types.ts` 的 `VideoBlock` 完全兼容。本仓库为该模块的自包含提取版，
类型独立于 producer（`src/types.ts`），便于单独复用与演示。
