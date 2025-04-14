"use client";
import logo from "@/assets/img/logo.svg";
import { Col, Layout, Row } from "antd";
import Image from "next/image";
import Link from "next/link";
import { useState, useEffect } from "react";

const { Footer } = Layout;

const MainFooter = () => {
  const currentYear = new Date().getFullYear();
  const [width, setWidth] = useState<any>();

  useEffect(() => {
    // Ensure window is defined (i.e., we're running in the browser)
    if (typeof window !== 'undefined') {
      // Function to update the state with the new width
      const handleResize = () => setWidth(window.innerWidth);

      // Set initial width
      setWidth(window.innerWidth);

      // Add event listener for window resize
      window.addEventListener('resize', handleResize);

      // Cleanup function to remove the event listener
      return () => window.removeEventListener('resize', handleResize);
    }
  }, []); // Empty array ensures effect runs only on mount and unmount

  const mobildeDevice = width <= 500;
  return (
<Footer style={{ textAlign: "center", 
   backgroundColor: "#bcc0e3", 
   padding: "67px 40px", 
   width: "100%",
   height:'410px',
   marginBottom:'90px'
     
   }}>
      <Row justify="space-between" gutter={[20, 20]}>
        <Col xs={24} md={8} style={{ display: "flex", justifyContent: mobildeDevice ? "center" : "flex-start" }}>
        <Image
          src={logo}
          alt="Logo"
          layout="intrinsic" 
          style={{
            width: '400px',   
            height: '70px',  
          }}
        />
        </Col>
        <Col
          md={5}
          xs={12}
          style={{
            display: "flex",
            flexDirection: "column",
            alignItems: mobildeDevice ? "center" : "flex-end",
          }}
        >
          <Link className="footer-link" href={"/"}>
            <strong>Home</strong>
          </Link>
          <Link className="footer-link" href={"/"}>
            Generate RFP
          </Link>
        </Col>
        <Col
          md={5}
          xs={12}
          style={{
            display: "flex",
            flexDirection: "column",
            alignItems: mobildeDevice ? "center" : "flex-end",
          }}
        >
          <Link className="footer-link" href={"/"}>
            <strong>Company</strong>
          </Link>
          <Link className="footer-link" href={"/"}>
            About Us
          </Link>
        </Col>
        <Col
          md={5}
          xs={12}
          style={{
            display: "flex",
            flexDirection: "column",
            alignItems: mobildeDevice ? "center" : "flex-end",
          }}
        >
          <Link className="footer-link" href={"/"}>
            <strong>Support</strong>
          </Link>
          <Link className="footer-link" href={"/"}>
            Contact Us
          </Link>
        </Col>
      </Row>
      <div style={{ marginTop: "40px", color: "#ffffff" }}>
        © {currentYear} ALGOFACT. All Rights Reserved.
      </div>
    </Footer>
  );
};
export default MainFooter;
