import React from "react";
import { Card, Typography } from "antd";
import { ChevronDown } from "lucide-react";

const { Title } = Typography;

interface ProjectCardProps {
  title: string;
  dueDate: string;
  company: string;
}

const iconStyle = {
  width: 16,
  height: 16,
  color: "#8c8c8c",
};

const ProjectCard: React.FC<ProjectCardProps> = ({ title, dueDate, company }) => (
  <Card style={{ marginBottom: "16px" }} extra={<ChevronDown style={iconStyle} />}>
    <Title level={5} style={{ margin: 0 }}>{title}</Title>
    <div style={{ color: "#8c8c8c", marginTop: "8px", fontSize: "14px" }}>
      Due: {dueDate} • {company}
    </div>
  </Card>
);

export default ProjectCard;
