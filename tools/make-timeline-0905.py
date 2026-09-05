# -*- coding: utf-8 -*-
"""make-timeline-0905.py — 用合成音频的实际时长生成 timeline，写回 examples/*.json 的 timeline 字段
用法: python tools/make-timeline-0905.py <voiceover_dir> <examples_json> [<more_json>...]
帧数 = ceil(dur*30) + 15 帧尾静音；title 块同样按音频（narration 已合成）。
"""
import json, math, subprocess, sys, os

vo_dir = os.path.abspath(sys.argv[1])
FPS = 30
SILENCE_FRAMES = 15

def dur_of(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
        capture_output=True, text=True).stdout.strip()
    return float(out)

entries, total = [], 0
n = len([f for f in os.listdir(vo_dir) if f.endswith(".wav")])
for i in range(n):
    wav = os.path.join(vo_dir, f"{i}.wav")
    d = dur_of(wav)
    frames = max(30, math.ceil(d * FPS) + SILENCE_FRAMES)
    entries.append({
        "blockIndex": i,
        "audioPath": wav.replace("\\", "/"),
        "audioDurationSec": round(d, 3),
        "targetFrames": frames,
        "globalStartFrame": total,
        "globalStartSec": round(total / FPS, 3),
    })
    total += frames

for jp in sys.argv[2:]:
    jp = os.path.abspath(jp)
    doc = json.load(open(jp, encoding="utf-8"))
    doc["timeline"] = {"entries": entries, "totalFrames": total, "fps": FPS}
    json.dump(doc, open(jp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"{os.path.basename(jp)}: timeline {len(entries)} entries, {total} frames ({total/FPS:.1f}s)")
