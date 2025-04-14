"use client";
import { Button, Row, Space, Typography } from "antd";

const { Title, Paragraph } = Typography;

export default function AdminPanelScreen() {
  return (
    <div style={{ marginLeft: "70px" }}>
      <Row gutter={20}>
        <HeroSection />
      </Row>
    </div>
  );
}

const HeroSection = () => {
  return (
    <div
      style={{
        width: "100%",
        minHeight: "70vh",
        background: "linear-gradient(180deg, #f7f7f7 0%, #ffffff 100%)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
      }}
    >
      <div
        style={{
          maxWidth: "1000px",
          textAlign: "center",
        }}
      >
        <Space direction="vertical" size="large" style={{ display: "flex" }}>
          <Title level={1} style={{ marginBottom: 0 }}>
            Enhance Your RFP Process with RFx Engine
          </Title>

          <Paragraph style={{ fontSize: "18px", color: "#666" }}>
            Discover the power of RFx Engine to streamline your RFP processes,
            improve efficiency, and achieve better outcomes for your
            organization.
          </Paragraph>

          <Space size="middle" style={{ marginTop: "24px" }}>
            <Button
              type="primary"
              size="large"
              style={{ height: "48px", padding: "0 32px" }}
            >
              Welcome to RFx Engine
            </Button>
            <Button size="large" style={{ height: "48px", padding: "0 32px" }}>
              Get Started
            </Button>
          </Space>
        </Space>
      </div>
    </div>
  );
};
