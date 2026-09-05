// debug_channel.mjs — dump what the space page actually rendered
const BASE = "http://127.0.0.1:9333";
const fs = await import("fs");
const mid = process.argv[2] || "285286947";
const URL_ = "https://space.bilibili.com/" + mid + "/video";
const target = await fetch(BASE + "/json/new?" + encodeURIComponent(URL_), { method: "PUT" }).then(r => r.json());
const ws = new WebSocket(target.webSocketDebuggerUrl);
let id = 0; const waiters = new Map();
const send = (m, p = {}) => new Promise(res => { const i = ++id; waiters.set(i, res); ws.send(JSON.stringify({ id: i, method: m, params: p })); });
ws.onmessage = (ev) => { const m = JSON.parse(ev.data); if (m.id && waiters.has(m.id)) { waiters.get(m.id)(m.result); waiters.delete(m.id); } };
await new Promise(res => (ws.onopen = res));
await send("Page.enable");
await send("Page.navigate", { url: URL_ });
await new Promise(r => setTimeout(r, 8000));
const evalJs = async (expr) => { const res = await send("Runtime.evaluate", { expression: expr, returnByValue: true, awaitPromise: true }); return res && res.result ? res.result.value : null; };
console.log("TITLE:", await evalJs("document.title"));
console.log("URL:", await evalJs("location.href"));
console.log("READYSTATE:", await evalJs("document.readyState"));
const dbg = await evalJs(`(function(){
  var a = document.querySelectorAll('a');
  var bv = [];
  a.forEach(function(x){ var h=(x.getAttribute('href')||'')+''; if(h.indexOf('BV')>-1) bv.push(h); });
  var grid = document.querySelector('.bili-grid, .bili-video-card, .video-list, .cube-list, [class*=grid]');
  return JSON.stringify({
    anchorTotal: a.length,
    bvAnchorHrefs: bv.slice(0,10),
    bodyTextLen: (document.body.innerText||'').length,
    bodyTextHead: (document.body.innerText||'').replace(/\\s+/g,' ').slice(0,300),
    hasGrid: !!grid,
    gridClass: grid? grid.className : null
  });
})()`);
console.log(dbg);
ws.close();