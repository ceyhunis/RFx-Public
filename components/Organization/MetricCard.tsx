import React from "react";
import { Card } from "antd";

interface MetricCardProps {
  icon: React.ElementType;
  title: string;
  value: string;
}

const iconStyle = {
  width: 16,
  height: 16,
  color: "#8c8c8c",
};

const MetricCard: React.FC<MetricCardProps> = ({ icon: Icon, title, value }) => (
  <Card>
    <div style={{ display: "flex", alignItems: "center", gap: "8px", color: "#8c8c8c" }}>
      <Icon style={iconStyle} />
      <span>{title}</span>
    </div>
    <div style={{ fontSize: "24px", fontWeight: "600", marginTop: "8px" }}>
      {value}
    </div>
  </Card>
);

export default MetricCard;
