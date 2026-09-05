// debug_space.mjs — root space page + try arc.search API from Chrome page context
const BASE = "http://127.0.0.1:9333";
const fs = await import("fs");
const mid = process.argv[2] || "285286947";
const URL_ = "https://space.bilibili.com/" + mid;
const target = await fetch(BASE + "/json/new?" + encodeURIComponent(URL_), { method: "PUT" }).then(r => r.json());
const ws = new WebSocket(target.webSocketDebuggerUrl);
let id = 0; const waiters = new Map();
const send = (m, p = {}) => new Promise(res => { const i = ++id; waiters.set(i, res); ws.send(JSON.stringify({ id: i, method: m, params: p })); });
ws.onmessage = (ev) => { const m = JSON.parse(ev.data); if (m.id && waiters.has(m.id)) { waiters.get(m.id)(m.result); waiters.delete(m.id); } };
await new Promise(res => (ws.onopen = res));
await send("Page.enable");
await send("Page.navigate", { url: URL_ });
await new Promise(r => setTimeout(r, 7000));
const evalJs = async (expr) => { const res = await send("Runtime.evaluate", { expression: expr, returnByValue: true, awaitPromise: true }); return res && res.result ? res.result.value : null; };
console.log("TITLE:", await evalJs("document.title"));
console.log("URL:", await evalJs("location.href"));
const dom = await evalJs(`(function(){
  var a = document.querySelectorAll('a'); var bv = [];
  a.forEach(function(x){ var h=(x.getAttribute('href')||'')+''; if(h.indexOf('BV')>-1) bv.push(h); });
  return JSON.stringify({anchorTotal:a.length, bvSample: bv.slice(0,12)});
})()`);
console.log("DOM:", dom);
// try arc.search API from page context
const api = await evalJs(`(async function(){
  try {
    var r = await fetch('https://api.bilibili.com/x/space/arc/search?mid=${mid}&ps=30&pn=1&order=pubdate&jsonp=jsonp', {credentials:'omit'});
    var t = await r.text();
    return 'STATUS='+r.status+' LEN='+t.length+' HEAD='+t.slice(0,200);
  } catch(e) { return 'ERR='+e.message; }
})()`);
console.log("ARC_API:", api);
ws.close();