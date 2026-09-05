// Demo Root — 注册可渲染的 NewsPaper 组合（长屏 1920×1080）
// 用法: npx remotion render src/index.ts NewsPaper out/demo.mp4 --props=examples/light.json
import React from "react";
import { Composition } from "remotion";
import { NewsPaperTemplate } from "./NewsPaper";
import type { TimelineDto, VideoConfig } from "./types";
import lightExample from "../examples/light.json";

interface DemoProps {
  config?: VideoConfig;
  timeline?: TimelineDto;
}

type ExampleBundle = { config: VideoConfig; timeline?: TimelineDto };

const LIGHT = lightExample as unknown as ExampleBundle;

/** 默认用 examples/light.json 预览；--props 传入 {config, timeline} 即可渲染任意内容 */
const Demo: React.FC<DemoProps> = ({ config, timeline }) => {
  const c = config ?? LIGHT.config;
  const t = timeline ?? LIGHT.timeline;
  return (
    <NewsPaperTemplate config={c} timelineEntries={t?.entries} fps={30} />
  );
};

const calc = async ({ props }: { props: Record<string, unknown> }) => {
  const p = props as DemoProps;
  const total =
    p.timeline?.totalFrames ?? LIGHT.timeline?.totalFrames ?? 300;
  return { durationInFrames: total, fps: 30, props };
};

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="NewsPaper"
      component={Demo}
      durationInFrames={300}
      fps={30}
      width={1920}
      height={1080}
      defaultProps={{}}
      calculateMetadata={calc}
    />
  );
};
