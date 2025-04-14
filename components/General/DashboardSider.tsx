"use client";
import { LogoutOutlined } from "@ant-design/icons";
import { Avatar, Divider, Tooltip } from "antd";
import Sider from "antd/es/layout/Sider";
import { Home } from "lucide-react";
import { signOut } from "next-auth/react";
import Link from "next/link";
import { cloneElement } from "react";

export default function GeneralSider({
  items,
  title,
  home,
}: {
  items: any;
  title?: string;
  home?: string;
}) {
  return (
    <Sider
      collapsed
      collapsedWidth={40}
      style={{
        height: "100vh",
        position: "fixed",
        left: 0,
        top: 0,
        backgroundColor: "#fff",
        boxShadow: "5px 0 8px rgba(0, 0, 0, 0.1)",
        zIndex: 2000,
      }}
    >
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          height: "100%",
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
        <div style={{ flex: 1, width: "100%" }}>
          <Link
            href={home ?? "/admin"}
            style={{
              display: "flex",
              padding: "10px 10px",
              justifyContent: "center",
              alignItems: "center",
            }}
          >
            <Home
              style={{
                color: "black",
                fontSize: "18px",
                width: "18px",
                height: "18px",
              }}
            />
          </Link>

          {items.map((item: any) => (
            <Tooltip
              title={<span>{item.label}</span>}
              placement="right"
              zIndex={3000}
              key={item.key}
              overlayInnerStyle={{
                backgroundColor: "white",
                color: "black",
              }}
              color="white"
            >
              <Link
                href={item.href}
                style={{
                  display: "flex",
                  alignItems: "center",
                  padding: "10px",
                  justifyContent: "center",
                  textDecoration: "none",
                  color: "black",
                }}
              >
                {cloneElement(item.icon, {
                  style: {
                    fontSize: "14px",
                    width: "18px",
                    height: "18px",
                  },
                })}
              </Link>
            </Tooltip>
          ))}
        </div>

        <Divider style={{ margin: "0" }} />

        <LogoutOutlined
          style={{
            fontSize: "20px",
            marginTop: "10px",
            marginBottom: "10px",
          }}
          onClick={() => signOut()}
        />
      </div>
    </Sider>
  );
}
