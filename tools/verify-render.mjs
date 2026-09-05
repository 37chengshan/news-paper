// verify-render.mjs — news-paper 独立仓库验证渲染驱动（GPU NVENC）
// 用法: node tools/verify-render.mjs <light|dark>
import { spawnSync } from "node:child_process";
import path from "node:path";
import { fileURLToPath } from "node:url";
import process from "node:process";

const skin = process.argv[2] === "dark" ? "dark" : "light";
const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, "..");
process.chdir(ROOT);

const CLI = path.join(ROOT, "node_modules", "@remotion", "cli", "remotion-cli.js");
const CHROME =
  "D:/motion/.remotion/chrome-headless-shell/win64/chrome-headless-shell-win64/chrome-headless-shell.exe";

const args = [
  CLI,
  "render",
  "src/index.ts",
  "NewsPaper",
  path.join("verify", `${skin}.mp4`),
  `--props=${path.join("examples", `${skin}.json`)}`,
  `--browser-executable=${CHROME}`,
  "--hardware-acceleration=if-possible",
  "--log=error",
];
console.log(">> remotion render", skin, "(GPU: if-possible)");
const r = spawnSync(process.execPath, args, { stdio: "inherit" });
console.log("exit:", r.status);
process.exit(r.status ?? 1);
