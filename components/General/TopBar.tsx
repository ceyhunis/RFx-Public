"use client";
import { Divider } from "antd";
import { Header } from "antd/es/layout/layout";
import Image from "next/image";

export default function DashboardTopBar({ home }: { home?: string }) {
  return (
    <Header>
      <div
        style={{
          display: "flex",
          flexDirection: "row",
          alignItems: "center",
          justifyContent: "flex-end",
          height: "100%",
          marginTop: "10px",
        }}
      >
        <Image src="/img/logo.png" alt="Home" width={90} height={30} />
      </div>
    </Header>
  );
}
