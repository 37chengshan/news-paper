# -*- coding: utf-8 -*-
"""patch-cat-progress.py — NewsPaper.tsx 接线：CatProgress/字幕全文/音频层（适配独立仓与生产端两种解构形态）"""
import io, sys

p = sys.argv[1]
s = io.open(p, encoding="utf-8").read()
n0 = len(s)

def rep(old, new, tag):
    global s
    if old in s:
        s = s.replace(old, new, 1)
        print(f"OK  {tag}")
    else:
        print(f"SKIP {tag} (not found)")

# 1) durationInFrames 解构（两种形态）
rep("const { fps: videoFps } = useVideoConfig();",
    "const { fps: videoFps, durationInFrames } = useVideoConfig();", "destructure-a")
rep("const { fps: videoFps, width, height } = useVideoConfig();",
    "const { fps: videoFps, width, height, durationInFrames } = useVideoConfig();", "destructure-b")

# 2) 字幕全文
rep('''  const subtitleText =
    block.subtitle ?? (block.narration ? clip(block.narration.replace(/\\s+/g, ""), 28) : "");''',
    '''  // 字幕直接渲染旁白全文（不再压缩、不再胶囊底）
  const subtitleText = block.narration
    ? block.narration.replace(/\\s+/g, "")
    : block.subtitle ?? "";''', "subtitle-fulltext")

# 3) 删 kwOfBlock
import re
m = re.search(r"  const kwOfBlock = \(\(\) => \{.*?\}\)\(\);\n", s, re.S)
if m:
    s = s[:m.start()] + s[m.end():]
    print("OK  kwOfBlock removed")

# 4) earcon + BGM
rep('''    <AbsoluteFill style={{ fontFamily: tokens.fontFamily, backgroundColor: tokens.bg }}>
      <div style={{ position: "absolute", inset: 0, opacity: chromeOpacity }}>''',
    '''    <AbsoluteFill style={{ fontFamily: tokens.fontFamily, backgroundColor: tokens.bg }}>
      {/* 音频层：片头记忆点音效 + 极低音量 BGM 循环 */}
      <Audio src={staticFile("sfx/earcon.wav")} volume={0.5} />
      <Audio src={staticFile("bgm.mp3")} volume={0.06} loop />
      <div style={{ position: "absolute", inset: 0, opacity: chromeOpacity }}>''', "audio-layer")

# 5) whoosh
rep('''                {audio ? <Audio src={audio} /> : null}
              </Series.Sequence>''',
    '''                {audio ? <Audio src={audio} /> : null}
                {i > 0 ? <Audio src={staticFile("sfx/whoosh.wav")} volume={0.22} /> : null}
              </Series.Sequence>''', "whoosh")

# 6) BottomKeywordTabs -> CatProgress
rep('''          <BottomKeywordTabs
            keywords={keywords}
            activeIndex={kwOfBlock}
            progress={blockProgress}
            tokens={tokens}
            fontSize={kwFont}
          />''',
    '''          <CatProgress
            sections={sections}
            currentIdx={currentIdx}
            blockProgress={blockProgress}
            globalP={durationInFrames > 0 ? frame / durationInFrames : 0}
            tokens={tokens}
          />''', "cat-progress")

io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print(f"done, {n0} -> {len(s)} chars")
