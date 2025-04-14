import { Button, Col, Row, Typography } from "antd";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import background from "@/assets/img/background.png";

const MainHero = () => {
  const router = useRouter();
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

  return (
    <div
      style={{
        height: "70vh",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        backgroundImage: `url('${background.src}')`,
        backgroundSize: "contain",
        backgroundPosition: "right center",
        backgroundRepeat: "no-repeat",
      }}
    >
      <Row
        align="middle"
        style={{
          textAlign: "center",
          flexDirection: "column",
        }}
      >
        <Col span={24}>
          <Typography.Text
            style={{ fontSize: 15, color: "#626DCF", letterSpacing: "5px" }}
          >
            AI POWERED
          </Typography.Text>
          <Typography.Title level={1}>
            Your Business
            <br /> Your Vision
          </Typography.Title>
          <Typography.Text
            style={{ fontSize: 18, color: "#8C8C8C", marginBottom: 20 }}
          >
            Crafting Tailored RFPs to Realize Your Unique Goals
          </Typography.Text>
        </Col>
        <Col span={24}>
          <Button
            type="primary"
            size="large"
            onClick={() => router.push("/")}
            style={{
              backgroundColor: "#3B1DFF",
              borderColor: "#3B1DFF",
              marginTop: 100,
              height: "50px",
              width: "300px",
              padding: "0 20px",
              fontSize: 18,
            }}
          >
            Generate RFP
          </Button>
        </Col>
      </Row>
    </div>
  );
};

export default MainHero;
