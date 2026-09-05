import json, subprocess, sys

playinfo_path = sys.argv[1] if len(sys.argv) > 1 else "playinfo.json"
out_path = sys.argv[2] if len(sys.argv) > 2 else "src.mp4"

d = json.load(open(playinfo_path, encoding="utf-8"))
dash = d.get("dash") or {}

videos = dash.get("video") or []
audios = dash.get("audio") or []

# 选 AVC(H.264) 最高画质
avc = [v for v in videos if (v.get("codecs") or "").startswith("avc1")]
avc.sort(key=lambda v: v.get("width", 0), reverse=True)
v = avc[0] if avc else videos[0]
a = (sorted(audios, key=lambda x: x.get("bandwidth", 0), reverse=True) or [None])[0]

def url(track):
    return track.get("baseUrl") or (track.get("backupUrl") or [None])[0]

print("video:", v["width"], "x", v["height"], v["codecs"])
print("audio:", a.get("id"), a.get("codecs"))

headers = (
    "Referer: https://www.bilibili.com/\r\n"
    "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36\r\n"
)

cmd = [
    "ffmpeg", "-y", "-v", "error",
    "-headers", headers, "-i", url(v),
    "-headers", headers, "-i", url(a),
    "-c", "copy", "-bsf:a", "aac_adtstoasc", out_path,
]
print("downloading...")
r = subprocess.run(cmd)
print("exit:", r.returncode)
