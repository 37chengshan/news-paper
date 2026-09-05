# -*- coding: utf-8 -*-
"""thick-voice.py — 旁白增厚（lowshelf 低频 + 轻压缩）+ timeline 生成 + 拷贝 public
用法: python tools/thick-voice.py <voiceover_dir> <examples.json> [<more.json>...]
"""
import json, math, os, shutil, subprocess, sys

vo_dir = os.path.abspath(sys.argv[1])
FPS = 30
SILENCE_FRAMES = 15
THICK = "lowshelf=f=160:g=3.5,lowshelf=f=320:g=1.5,acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120:makeup=2,highshelf=f=9000:g=-1.5"

thick_dir = os.path.join(os.path.dirname(vo_dir), "voiceover-thick")
os.makedirs(thick_dir, exist_ok=True)

def dur_of(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
        capture_output=True, text=True).stdout.strip()
    return float(out)

n = len([f for f in os.listdir(vo_dir) if f.endswith(".wav") and f[:-4].isdigit()])
entries, total = [], 0
for i in range(n):
    src = os.path.join(vo_dir, f"{i}.wav")
    dst = os.path.join(thick_dir, f"{i}.wav")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-af", THICK,
                    "-ar", "48000", dst], check=True)
    d = dur_of(dst)
    frames = max(30, math.ceil(d * FPS) + SILENCE_FRAMES)
    entries.append({
        "blockIndex": i,
        "audioPath": dst.replace("\\", "/"),
        "audioDurationSec": round(d, 3),
        "targetFrames": frames,
        "globalStartFrame": total,
        "globalStartSec": round(total / FPS, 3),
    })
    total += frames
    print(f"  {i}.wav -> thick {d:.2f}s / {frames}f")

for jp in sys.argv[2:]:
    jp = os.path.abspath(jp)
    doc = json.load(open(jp, encoding="utf-8"))
    doc["timeline"] = {"entries": entries, "totalFrames": total, "fps": FPS}
    json.dump(doc, open(jp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"{os.path.basename(jp)}: timeline {len(entries)} entries, {total} frames ({total/FPS:.1f}s)")

pub = os.path.join(os.path.dirname(vo_dir), "public", "voiceover")
os.makedirs(pub, exist_ok=True)
for i in range(n):
    shutil.copy2(os.path.join(thick_dir, f"{i}.wav"), os.path.join(pub, f"{i}.wav"))
print(f"copied {n} thickened wavs -> public/voiceover/")
