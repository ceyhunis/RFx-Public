"use client";

import React from "react";
import { Card, Typography } from "antd";
import styles from "./EmployerCard.module.css";

const { Title, Text } = Typography;

interface EmployerCardProps {
  first_name: string;
  last_name: string;
  email: string;
}

const EmployerCard: React.FC<EmployerCardProps> = ({
  first_name,
  last_name,
  email,
}) => {
  const fullName = `${first_name} ${last_name}`;

  return (
    <Card className={styles.container}>
      <div className={styles.infoOverlay} data-info-overlay>
        <span>ℹ️</span>
        <span>Employer</span>
      </div>
      <div className={styles.content}>
        <Title level={4} className={styles.header}>
          {fullName}
        </Title>
        <Text className={styles.subHeader}>{email}</Text>
      </div>
    </Card>
  );
};

export default EmployerCard;
