import fs from "fs";

const BASE = "http://127.0.0.1:9333";

function newTarget(url) {
  return fetch(BASE + "/json/new?" + encodeURIComponent(url), { method: "PUT" }).then((r) => r.json());
}

async function withPage(url, fn) {
  const target = await newTarget(url);
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
  await send("Runtime.enable");
  await send("Page.navigate", { url });
  await new Promise((r) => setTimeout(r, 9000));
  const out = await fn(send);
  ws.close();
  return out;
}

const evalJs = (send, expr) =>
  send("Runtime.evaluate", { expression: expr, returnByValue: true, awaitPromise: true }).then((r) => (r && r.result ? r.result.value : null));

// 1) 取 V1 的 owner mid
const meta = await withPage("https://www.bilibili.com/video/BV1dTtv6aEDc", async (send) => {
  const st = await evalJs(send, "JSON.stringify(window.__INITIAL_STATE__ ? (window.__INITIAL_STATE__.owner||(window.__INITIAL_STATE__.videoData&&window.__INITIAL_STATE__.videoData.owner)||null) : null)");
  let owner = null;
  try { owner = st ? JSON.parse(st) : null; } catch (e) {}
  return owner;
});
console.log("V1 owner:", JSON.stringify(meta));
const mid = meta && meta.mid;
const name = meta && meta.name;
if (!mid) { console.log("NO_MID"); process.exit(1); }

// 2) 用 space arc API 取视频列表
const list = await withPage("https://space.bilibili.com/" + mid + "/video", async (send) => {
  const js = `(async () => {
    const mid = ${mid};
    const res = await fetch('https://api.bilibili.com/x/space/arc/search?mid='+mid+'&ps=50&pn=1&order=pubdate&jsonp=jsonp', {credentials:'include'});
    const j = await res.json();
    if (j.code !== 0) return {code:j.code, msg:j.message};
    return {code:0, list: (j.data.list.vlist||[]).map(v=>({bvid:v.bvid, title:v.title, pubdate:v.pubdate, play:v.play}))};
  })()`;
  return await evalJs(send, js);
});
console.log("space code:", list && list.code, "count:", list && list.list && list.list.length);
const out = { mid, name, videos: (list && list.list) || [] };
fs.writeFileSync("channel_videos.json", JSON.stringify(out, null, 2));
console.log("saved channel_videos.json, total videos:", out.videos.length);
