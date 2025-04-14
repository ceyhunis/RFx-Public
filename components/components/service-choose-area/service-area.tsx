import React, { useState, useEffect } from "react";
import { Card, Col, Form, Input, Radio, Row, Skeleton } from "antd";
import { useGenerateContext } from "@/lib/providers/GenerateContextProvider";
import { ApiResponse } from "@/types/general_types";
import { DynamicRouter } from "@/utils/request_utils";
import { SearchOutlined } from "@ant-design/icons";
import useSWR from "swr";

const Service = () => {
  const { service_ids, setService_ids } = useGenerateContext();
  const [searchTerm, setSearchTerm] = useState("");
  const [displayedData, setDisplayedData] = useState([]);
  const url = DynamicRouter("project", "service");
  const { data, error, isLoading } = useSWR<ApiResponse<any>>(url);

  useEffect(() => {
    if (data?.data) {
      const filteredData: any = searchTerm
        ? data.data.filter((item: any) =>
            item.name.toLowerCase().includes(searchTerm.toLowerCase())
          )
        : data.data.slice(0, 8);
      setDisplayedData(filteredData);
    }
  }, [data, searchTerm]);

  if (!data) {
    return <Skeleton.Input active />;
  }

  return (
    <Row justify={"center"}>
      <Col xs={24}>
        <h2 style={{ 
          fontSize: '24px', 
          marginBottom: '20px',
          color: '#1a1a1a' 
        }}>Services Information</h2>
        
        <Input
          prefix={<SearchOutlined style={{ color: '#bfbfbf' }} />}
          style={{ 
            marginBottom: '24px',
            borderRadius: '8px',
            boxShadow: '0 2px 4px rgba(0,0,0,0.05)'
          }}
          size="large"
          placeholder="Search services..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
        
        <div
          style={{
            height: 'calc(100vh - 250px)',
            overflow: "auto",
            padding: '4px',
            borderRadius: '12px',
            backgroundColor: '#f5f5f5'
          }}
        >
          <Row gutter={[16, 16]}>
            {displayedData.map((item: any) => (
              <Col key={item.id} xs={24} md={8}>
                <Card
                  hoverable
                  size="small"
                  style={{
                    borderRadius: '8px',
                    transition: 'all 0.3s ease',
                    backgroundColor: service_ids.filter((i) => i.id === item.id).length > 0 
                      ? '#e6f7ff' 
                      : '#ffffff',
                    borderColor: service_ids.filter((i) => i.id === item.id).length > 0
                      ? '#1890ff'
                      : '#d9d9d9',
                    boxShadow: '0 2px 4px rgba(0,0,0,0.05)',
                  }}
                  onClick={() => {
                    if (service_ids.filter((i) => i.id === item.id).length > 0) {
                      setService_ids(service_ids.filter((b: any) => b.id !== item.id));
                    } else {
                      setService_ids([...service_ids, { id: item.id, name: item.name }]);
                    }
                  }}
                >
                  <Card.Meta
                    title={
                      <div style={{ 
                        display: 'flex', 
                        alignItems: 'center',
                        padding: '8px 0'
                      }}>
                        <Radio
                          checked={service_ids.filter((i) => i.id === item.id).length > 0}
                          style={{ marginRight: 12 }}
                        />
                        <span style={{ 
                          fontSize: '16px',
                          fontWeight: 500,
                          color: '#262626'
                        }}>{item.name}</span>
                      </div>
                    }
                  />
                </Card>
              </Col>
            ))}
          </Row>
        </div>
      </Col>
    </Row>
  );
};

export default Service;
