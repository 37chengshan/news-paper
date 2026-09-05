// verify-render.mjs — news-paper 独立仓库验证渲染驱动（GPU NVENC）
// 用法: node tools/verify-render.mjs <props.json> <out.mp4>
//       node tools/verify-render.mjs light              → examples/light.json → verify/light.mp4
import { spawnSync } from "node:child_process";
import path from "node:path";
import { fileURLToPath } from "node:url";
import process from "node:process";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, "..");
process.chdir(ROOT);

const arg1 = process.argv[2] ?? "light";
const arg2 = process.argv[3];
const isPropsFile = arg1.endsWith(".json");
const propsPath = isPropsFile ? arg1 : path.join("examples", `${arg1}.json`);
const outFile = arg2 ?? path.join("verify", `${isPropsFile ? path.basename(arg1, ".json") : arg1}.mp4`);

const CLI = path.join(ROOT, "node_modules", "@remotion", "cli", "remotion-cli.js");
const CHROME =
  "D:/motion/.remotion/chrome-headless-shell/win64/chrome-headless-shell-win64/chrome-headless-shell.exe";

const args = [
  CLI,
  "render",
  "src/index.ts",
  "NewsPaper",
  outFile,
  `--props=${propsPath}`,
  `--browser-executable=${CHROME}`,
  "--hardware-acceleration=if-possible",
  "--log=error",
];
console.log(">> remotion render", propsPath, "->", outFile, "(GPU: if-possible)");
const r = spawnSync(process.execPath, args, { stdio: "inherit" });
console.log("exit:", r.status);
process.exit(r.status ?? 1);
