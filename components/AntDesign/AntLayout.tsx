"use client";
import { Layout } from "antd";
import React from "react";

export default function AntLayout({
  children,
  hasSider,
}: {
  children: React.ReactNode;
  hasSider?: boolean;
}) {
  return (
    <Layout hasSider={hasSider} style={{ backgroundColor: "transparent" }}>
      {children}
    </Layout>
  );
}
