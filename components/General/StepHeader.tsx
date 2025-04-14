import { Col, Row, Typography } from "antd";
import React from "react";

export default function StepHeader({
  title,
  description,
}: {
  title: string;
  description?: string;
}) {
  return (
    <Row>
      <Col>
        <Typography.Title 
          style={{ 
            fontSize: '30px',
            marginTop: 20,
            fontWeight: '900',
            color: '#121BDA',
            margin: 0,
            textAlign: 'left'
          }} 
          level={1}
        >
          {title}
        </Typography.Title>
        {description && (
          <Typography.Text style={{ fontWeight: 400, fontSize: 14 }}>
            {description}
          </Typography.Text>
        )}
      </Col>
    </Row>
  );
}
