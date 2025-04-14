"use client";
import { ConfigProvider } from "antd";
import theme from "../theme";

export default function AntConfig({ children }: { children: React.ReactNode }) {
  return <ConfigProvider theme={theme}>{children}</ConfigProvider>;
}
