import React, { useState } from "react";
import { Button, Typography } from "antd";
import { Filter } from "lucide-react";
import CardIcon from "../components/icons/CardIcon";


const { Title } = Typography;

interface PageHeaderProps {
  setViewType: (viewType: "card" | "table") => void;
  viewType?: "card" | "table";
  showActions?: boolean;
  title: string;
}

const iconStyle = {
  width: 16,
  height: 16,
  color: "#8c8c8c",
};

const PageHeader: React.FC<PageHeaderProps> = ({
  setViewType,
  viewType,
  showActions = true,
  title,
}) => {
  const [isModalOpen, setIsModalOpen] = useState(false);

  const handleSuccess = () => {
    window.location.reload();
  };

  return (
    <div style={{ padding: "12px" }}>
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: "12px",
          marginTop: "8px",
        }}
      >
        <Title level={4} style={{ margin: 0 }}>
          {title}
        </Title>

        {showActions && (
          <div style={{ display: "flex", gap: "8px" }}>
            <Button type="primary" onClick={() => setIsModalOpen(true)}>
              Create Organization
            </Button>
          </div>
        )}
       
      </div>

    
    </div>
  );
};

export default PageHeader;
