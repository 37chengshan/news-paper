// news-paper 独立类型定义（自包含，无外部依赖）
// 与 motion/producer src/data/types.ts 保持字段兼容，便于双向移植

/** 视频风格：本模板用 news-paper（浅皮，morning）/ news-paper-dark（深皮） */
export type VideoStyle = "news-paper" | "news-paper-dark" | (string & {});

/** 场次：morning=浅皮 / evening=深皮（style 为 news-paper 时自动切换） */
export type EditionId = "morning" | "evening";

/** 逐块时间轴条目（与 render-batch timeline.json 契约一致） */
export interface TimelineEntry {
  blockIndex: number;
  audioPath: string | null;
  audioDurationSec: number;
  targetFrames: number;
  globalStartSec: number;
}

export interface TimelineDto {
  entries: TimelineEntry[];
  totalFrames: number;
  fps: number;
}

export interface VideoBlock {
  type:
    | "title"
    | "text"
    | "code"
    | "image"
    | "video"
    | "terminal"
    | "chart"
    | "list"
    | "hand-drawing";
  content: string;
  /** 动画效果名（兼容字段，本模板未使用） */
  effect?: string;
  /** 图片/视频地址（image/video 块用；public 相对路径或 URL） */
  src?: string;
  /** 列表项（list 块用；与 points 等价参与网格路由） */
  items?: string[];
  /** 图表数据（chart 块用，真渲染） */
  data?: { label: string; value: number }[];
  /** 详细摘要（触发 T5 文章特写） */
  summary?: string;
  /** 要点列表（3→T6 1×3 / 4→T3 2×2 / 5→T4 3+2 / ≥6→2×3 自动路由） */
  points?: string[];
  /** 数据卡模块（首个会参与 number-pop，全片上限 3 次） */
  stats?: { label: string; value: string; sourceUrl?: string }[];
  /** 旁白文案（字幕条 fallback：narration 前 28 字） */
  narration?: string;
  /** 来源标识（TrustLine 可信条展示） */
  source?: string;
  /** 原文链接（TrustLine 显示域名） */
  url?: string;
  /** 事实列表（T5 文章特写逐条展示） */
  facts?: string[];
  /** 声明（T5 底部小字） */
  disclaimer?: string;
  /** 内嵌字幕条文本（10-28 字压缩） */
  subtitle?: string;
  /** 关键词（行内 chip + 底部词条 tab 高亮） */
  highlight?: string;
  /** 板块 key（顶部 tab 分区：ai-news=要闻 / cn-news=国内 / intl-news=环球 / other-news=行业动态 / ent-news=文娱） */
  section?: string;
  /** ===== news-paper 模板扩展（全可选，缺省走自动路由）===== */
  /** 模板覆盖（T1-T6） */
  template?: "T1" | "T2" | "T3" | "T4" | "T5" | "T6";
  /** 卡片 icon 语义覆盖（缺省按卡内序号四色轮换） */
  icon?: { color?: "red" | "orange" | "green" | "cyan"; glyph?: string };
  /** 证据插入屏规格（S1 全屏 / S2 大幅 / S3 居中卡）；image/video 缺省 card/full */
  evidence?: {
    scale?: "full" | "wide" | "card";
    caption?: string;
  };
  /** 素材图（兼容 producer media 字段） */
  media?: {
    kind?: "screenshot" | "leaderboard" | "figure" | "illustration" | "output-frame";
    src: string;
    caption?: string;
    credit?: string;
  };
}

export interface VideoConfig {
  /** 视觉风格：news-paper（浅，morning）/ news-paper-dark（深） */
  style: VideoStyle;
  /** 模板标识：必须为 "news-paper" 才会路由到本模板 */
  template?: "news-paper" | (string & {});
  /** 片名（标题屏顶部小字） */
  title: string;
  /** 一句话摘要（封面/简介，模板未直接使用） */
  subtitle?: string;
  /** 场次（morning/evening）——style="news-paper" 时驱动自动换肤 */
  edition?: EditionId;
  /** run id（贴纸日期从此提取，如 "ai-news-morning-2026-09-04"） */
  runId?: string;
  /** 版权/署名（贴纸 fallback） */
  footer?: string;
  /** 内容块（逐段渲染） */
  blocks: VideoBlock[];
  /** BGM 路径（兼容字段，音频由外层 Audio/BgmAudio 管） */
  bgm?: string;
}
