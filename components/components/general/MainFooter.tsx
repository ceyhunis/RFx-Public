"use client";
import { Col, Layout, Row } from "antd";
import Image from "next/image";
import Link from "next/link";
import { useEffect, useState } from "react";

const { Footer } = Layout;

interface FooterColumnProps {
  title: string;
  links: { title: string; href: string }[];
  href: string;
  isMobile: boolean;
}

const FooterColumn: React.FC<FooterColumnProps> = ({
  title,
  links,
  href,
  isMobile,
}) => (
  <Col
    md={5}
    xs={12}
    style={{
      display: "flex",
      flexDirection: "column",
      alignItems: isMobile ? "center" : "flex-start",
    }}
  >
    <Link className="footer-link" href={href}>
      <strong>{title}</strong>
    </Link>
    {links.map((link, index) => (
      <Link key={index} className="footer-link" href={link.href}>
        {link.title}
      </Link>
    ))}
  </Col>
);

interface FooterColumn {
  title: string;
  href: string;
  links: { title: string; href: string }[];
}

const MainFooter: React.FC = () => {
  const currentYear = new Date().getFullYear();
  const [width, setWidth] = useState<number | undefined>(undefined);

  useEffect(() => {
    const handleResize = () => setWidth(window.innerWidth);

    if (typeof window !== "undefined") {
      setWidth(window.innerWidth);
      window.addEventListener("resize", handleResize);
      return () => window.removeEventListener("resize", handleResize);
    }
  }, []);

  const isMobile = width !== undefined && width <= 500;

  const footerColumns: FooterColumn[] = [
    {
      title: "Home",
      href: "https://www.rfxengine.com",
      links: [{ title: "Generate RFP", href: "/" }],
    },
  ];

  return (
    <Footer
      style={{
        textAlign: "center",
        backgroundColor: "#b3e5fc",
        padding: "40px 40px",
        width: "100%",
      }}
    >
      <Row justify="space-between" align="top" style={{ height: "100%" }}>
        <Col
          xs={24}
          md={8}
          style={{
            display: "flex",
            justifyContent: isMobile ? "center" : "flex-start",
            alignItems: "flex-start",
            flexDirection: "column",
          }}
        >
          <Image
            src={"/img/logo.png"}
            alt="Logo"
            layout="intrinsic"
            width={150}
            height={150}
          />
          <div style={{ color: "#ffffff", marginTop: "20px" }}>
            © {currentYear} RFXENGINE. All Rights Reserved.
          </div>
        </Col>

        <Col xs={24} md={10}>
          <Row justify="end" gutter={[20, 20]}>
            {footerColumns.map((column, index) => (
              <FooterColumn
                key={index}
                title={column.title}
                links={column.links}
                href={column.href}
                isMobile={isMobile}
              />
            ))}
          </Row>
        </Col>
      </Row>
    </Footer>
  );
};

export default MainFooter;
