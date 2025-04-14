import { Content } from "antd/es/layout/layout";
import React from "react";

export default function AntContent({
  children,
  style,
}: {
  children: React.ReactNode;
  style?: React.CSSProperties;
}) {
  return (
    <Content style={style ?? { backgroundColor: "transparent" }}>
      {children}
    </Content>
  );
}
