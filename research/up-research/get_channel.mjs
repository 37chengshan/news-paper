// get_channel.mjs — enumerate video BVs from a Bilibili space page via CDP Chrome (port 9333)
// Usage: node get_channel.mjs <mid>
const BASE = "http://127.0.0.1:9333";
const fs = await import("fs");

const mid = process.argv[2];
if (!mid) { console.log("usage: node get_channel.mjs <mid>"); process.exit(1); }

// Root space page (not /video — that redirects to creator upload console when logged out)
const URL_ = "https://space.bilibili.com/" + mid;
const target = await fetch(BASE + "/json/new?" + encodeURIComponent(URL_), { method: "PUT" }).then(r => r.json());
const ws = new WebSocket(target.webSocketDebuggerUrl);
let id = 0;
const waiters = new Map();
const send = (m, p = {}) => new Promise(res => { const i = ++id; waiters.set(i, res); ws.send(JSON.stringify({ id: i, method: m, params: p })); });
ws.onmessage = (ev) => { const m = JSON.parse(ev.data); if (m.id && waiters.has(m.id)) { waiters.get(m.id)(m.result); waiters.delete(m.id); } };
await new Promise(res => (ws.onopen = res));

await send("Page.enable");
await send("Page.navigate", { url: URL_ });
await new Promise(r => setTimeout(r, 6000));

const evalJs = async (expr) => {
  const res = await send("Runtime.evaluate", { expression: expr, returnByValue: true, awaitPromise: true });
  return res && res.result ? res.result.value : null;
};

const COLLECT_JS = `(function(){
  const out = [];
  document.querySelectorAll('a[href*="/video/BV"]').forEach(function(a){
    var m = (a.getAttribute('href') || '').match(/BV[A-Za-z0-9]+/);
    if (!m) return;
    var t = (a.getAttribute('title') || a.innerText || '').trim().replace(/\\s+/g, ' ').slice(0, 120);
    out.push({bv: m[0], href: a.href, title: t});
  });
  return JSON.stringify(out);
})()`;

let all = [];
const seen = new Set();
for (let i = 0; i < 6; i++) {
  const raw = await evalJs(COLLECT_JS);
  let arr = [];
  try { arr = JSON.parse(raw || "[]"); } catch (e) {}
  arr.forEach(x => { if (!seen.has(x.bv)) { seen.add(x.bv); all.push(x); } });
  await evalJs("window.scrollTo(0, document.body.scrollHeight)");
  await new Promise(r => setTimeout(r, 3500));
}

console.log("UNIQUE BVS=" + all.length);
const list = all.slice(0, 80);
list.forEach((x, i) => console.log((i + 1).toString().padStart(2, " ") + ". " + x.bv + "  " + x.title));
fs.writeFileSync("channel_" + mid + ".json", JSON.stringify({ mid, count: all.length, videos: list }, null, 2));
console.log("\nsaved channel_" + mid + ".json  (kept first " + list.length + " of " + all.length + ")");
ws.close();