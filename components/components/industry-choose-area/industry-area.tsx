import React, { useState, useEffect } from "react";
import { Card, Col, Form, Input, Radio, Row, Skeleton, Pagination } from "antd";
import StepHeader from "@/components/General/StepHeader";
import { useGenerateContext } from "@/lib/providers/GenerateContextProvider";
import { ApiResponse } from "@/types/general_types";
import { DynamicRouter } from "@/utils/request_utils";
import useSWR from "swr";

const Industry = () => {
  const { industry, setIndustry } = useGenerateContext();
  const [searchTerm, setSearchTerm] = useState("");
  const [displayedData, setDisplayedData] = useState([]);
  const url = DynamicRouter("project", "industry");
  const { data, error, isLoading } = useSWR<ApiResponse<any>>(url);
  const [currentPage, setCurrentPage] = useState(1);
  const pageSize = 9;

  useEffect(() => {
    if (data?.data) {
      const filteredData: any = searchTerm
        ? data.data.filter((item: any) =>
            item.name.toLowerCase().includes(searchTerm.toLowerCase())
          )
        : data.data;
      
      if (currentPage > Math.ceil(filteredData.length / pageSize)) {
        setCurrentPage(1);
      }

      const startIndex = (currentPage - 1) * pageSize;
      const paginatedData = filteredData.slice(startIndex, startIndex + pageSize);
      setDisplayedData(paginatedData);
    }
  }, [data, searchTerm, currentPage]);

  if (!data) {
    return <Skeleton.Input active />;
  }

  return (
    <Row justify={"center"} style={{ width: "100%", height: "auto", marginBottom: "40px", paddingLeft: "60px", paddingRight: "20px" }}>
      <Col span={24} style={{ maxWidth: "1800px", width: "100%" }}>
        <Row gutter={[16, 16]} justify="center">
          <Col span={24}>
            <p>Industry Information</p>
            <Input
              style={{ marginBottom: "20px", width: "100%" }}
              size="large"
              placeholder="Search"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
            <Row gutter={[16, 16]} justify="start">
              {displayedData.map((item: any) => (
                <Col key={item.id} xs={24} sm={12} md={8}>
                  <Card
                    size="small"
                    style={{
                      borderColor: industry?.name === item.name ? "#626dcf" : "",
                      cursor: "pointer",
                      height: "100%",
                      width: "100%",
                      transition: "all 0.3s ease"
                    }}
                    onClick={() => {
                      setIndustry({
                        name: item.name,
                        id: item.id,
                      });
                    }}
                    hoverable
                  >
                    <Card.Meta
                      title={
                        <>
                          <Radio
                            checked={industry?.name === item.name}
                            style={{ marginRight: 10 }}
                          />
                          {item.name}
                        </>
                      }
                    />
                  </Card>
                </Col>
              ))}
            </Row>
          </Col>
        </Row>
        
        <Row justify="center" style={{ 
          marginTop: "10px",
          position: "relative",
          zIndex: 1,
          backgroundColor: "white",
          padding: "10px 0"
        }}>
          <Pagination
            current={currentPage}
            pageSize={pageSize}
            total={data?.data?.filter((item: any) => 
              searchTerm ? item.name.toLowerCase().includes(searchTerm.toLowerCase()) : true
            ).length}
            onChange={(page) => setCurrentPage(page)}
            showSizeChanger={false}
          />
        </Row>
      </Col>
    </Row>
  );
};

export default Industry;
