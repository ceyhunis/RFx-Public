"use client";
import { Button } from "antd";
import { Header } from "antd/es/layout/layout";
import Image from "next/image";
import { useRouter } from "next/navigation";
import { useEffect, useState, useCallback } from "react";

const MOBILE_BREAKPOINT = 500;

export default function MainNavbar() {
  const [windowWidth, setWindowWidth] = useState<number | undefined>(undefined);
  const router = useRouter();

  const handleResize = useCallback(() => {
    setWindowWidth(window.innerWidth);
  }, []);

  useEffect(() => {
    if (typeof window !== "undefined") {
      setWindowWidth(window.innerWidth);
      window.addEventListener("resize", handleResize);
      return () => window.removeEventListener("resize", handleResize);
    }
  }, [handleResize]);

  const isMobile =
    windowWidth !== undefined && windowWidth <= MOBILE_BREAKPOINT;

  const Logo = () => (
    <div onClick={() => router.push("/")} style={logoStyle}>
      <Image
        alt="logo"
        src={"/img/logo.png"}
        layout="intrinsic"
        width={isMobile ? 180 : 200}
        height={60}
      />
    </div>
  );

  const GetStartedButton = () => (
    <Button
      type="primary"
      style={getButtonStyle(isMobile)}
      onClick={() => router.push("https://www.rfxengine.com")}
    >
      Home
    </Button>
  );

  return (
    <Header style={getHeaderStyle(isMobile)}>
      <div style={navContainerStyle}>
        <Logo />
        <GetStartedButton />
      </div>
    </Header>
  );
}

const logoStyle = {
  cursor: "pointer",
  width: 200,
  display: "flex",
  justifyContent: "center",
  alignItems: "center",
};

const navContainerStyle = {
  display: "flex",
  alignItems: "center",
  justifyContent: "space-between",
};

const getButtonStyle = (isMobile: boolean) => ({
  padding: isMobile ? "4px 12px" : "6px 50px",
  fontSize: isMobile ? 12 : 14,
  height: isMobile ? 32 : 40,
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
});

const getHeaderStyle = (isMobile: boolean) => ({
  backgroundColor: "transparent",
  marginTop: 20,
  padding: isMobile ? "0 20px" : "0 50px",
});
