const BASE = "http://127.0.0.1:9333";
const BVID = process.argv[2] || "BV1dTtv6aEDc";
const URL_ = "https://www.bilibili.com/video/" + BVID;
const fs = await import("fs");
import { fileURLToPath } from "url";
import path from "path";
const HERE = path.dirname(fileURLToPath(import.meta.url));

// 新建标签
const target = await fetch(BASE + "/json/new?" + encodeURIComponent(URL_), { method: "PUT" }).then((r) => r.json());
const ws = new WebSocket(target.webSocketDebuggerUrl);
let id = 0;
const waiters = new Map();
const send = (method, params = {}) =>
  new Promise((res) => {
    const i = ++id;
    waiters.set(i, res);
    ws.send(JSON.stringify({ id: i, method, params }));
  });
ws.onmessage = (ev) => {
  const m = JSON.parse(ev.data);
  if (m.id && waiters.has(m.id)) {
    waiters.get(m.id)(m.result);
    waiters.delete(m.id);
  }
};
await new Promise((res) => (ws.onopen = res));

await send("Page.enable");
await send("Page.navigate", { url: URL_ });
await new Promise((r) => setTimeout(r, 14000));

const evalJs = async (expr) => {
  const res = await send("Runtime.evaluate", { expression: expr, returnByValue: true, awaitPromise: true });
  return res && res.result ? res.result.value : null;
};

console.log("title:", await evalJs("document.title"));
console.log("playinfo type:", await evalJs("typeof window.__playinfo__"));

const raw = await evalJs("JSON.stringify(window.__playinfo__ ? (window.__playinfo__.data || window.__playinfo__) : null)");
if (!raw) {
  console.log("未取到 playinfo");
  ws.close();
  process.exit(0);
}
const d = JSON.parse(raw);
const dash = d.dash || (d.data && d.data.dash);
if (!dash) {
  console.log("no dash —— 可能需要登录或播放器未就绪");
  ws.close();
  process.exit(0);
}
console.log("\n=== VIDEO 轨道 ===");
(dash.video || []).forEach((v) => console.log("id=" + v.id + " " + v.width + "x" + v.height + " codecs=" + v.codecs));
console.log("\n=== AUDIO 轨道 ===");
(dash.audio || []).forEach((a) => console.log("id=" + a.id + " codecs=" + a.codecs));
const OUT = path.join(HERE, "playinfo_" + BVID + ".json");
fs.writeFileSync(OUT, raw);
console.log("\nsaved " + OUT);
ws.close();
