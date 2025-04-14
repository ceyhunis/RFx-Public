import { useLoader } from "@/lib/providers/LoaderContextProvider";
import { LoadingOutlined } from "@ant-design/icons";
import { Spin } from "antd";
import React from "react";

export default function Loader({
  children,
  isLoading,
}: {
  children: React.ReactNode;
  isLoading?: boolean;
}) {
  const { loaderState } = useLoader();
  return (
    <Spin
      style={{
        zIndex: 9999999,
        display: "flex",
        width: "100%",
        height: "100%",
        pointerEvents: "none",
        justifyContent: "center",
        alignItems: "center",
      }}
      spinning={isLoading ?? loaderState.isLoading}
      size="large"
      indicator={<LoadingOutlined style={{ color: "gray", fontSize: 80 }} />}
    >
      {children}
    </Spin>
  );
}
