import { Config } from "@remotion/cli/config";

// 显式声明 public 目录，确保 headless render 时 staticFile / 原生 <img src="/x.jpg">
// 能从 public/ 正确提供（部分 CLI 场景不会自动探测 publicDir）。
Config.setPublicDir("public");
