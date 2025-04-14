"use client";
import StepHeader from "@/components/General/StepHeader";
import { ApiResponse } from "@/types/general_types";
import { notify } from "@/utils/functions_utils";
import { DynamicRouter, postRequest } from "@/utils/request_utils";
import {
  Button,
  Col,
  Descriptions,
  DescriptionsProps,
  Drawer,
  Form,
  List,
  Row,
  Skeleton,
  Space,
} from "antd";
import { useSearchParams } from "next/navigation";
import React, { useState } from "react";
import { usePDF } from "react-to-pdf";
import useSWR from "swr";
import useSWRMutation from "swr/mutation";

export default function ExternalAccessPage() {
  const params = useSearchParams();
  const id = params.get("id");
  const url = DynamicRouter("project", "data", {
    id: id,
  });
  const { data } = useSWR<ApiResponse<any>>(url);
  const { toPDF, targetRef } = usePDF({ filename: "page.pdf" });
  const [drawerOpen, setDrawerOpen] = useState(false);

  const urlReject = DynamicRouter("project", "reject-proposal");
  const { trigger } = useSWRMutation(urlReject, postRequest);

  const urlAccept = DynamicRouter("project", "accept-proposal");
  const { trigger: acceptTrigger } = useSWRMutation(urlAccept, postRequest);

  const dataSource = data?.data[0];

  const items: DescriptionsProps["items"] = [
    {
      key: "1",
      label: "Document Name",
      children: dataSource?.name,
    },
    {
      key: "2",
      label: "Document Description",
      children: dataSource?.description,
      span: 4,
    },
    {
      key: "3",
      label: "Company Website (URL)",
      children: dataSource?.company_url,
    },

    {
      key: "4",
      label: "Company Description",
      children: dataSource?.value_propositions,
      span: 4,
    },
    {
      key: "tgg",
      label: "Industry",
      children: dataSource?.industry.name,
      span: 24,
    },
    {
      key: "5",
      label: "Selected Services",
      children: (
        <List bordered>
          {dataSource?.services.map((item: any) => (
            <List.Item key={item.id + "k"}>{item.name}</List.Item>
          ))}
        </List>
      ),
    },
    {
      key: "6",
      label: "Business Cycles",
      children: (
        <List bordered>
          {dataSource?.business_cycle.map((item: any) => (
            <List.Item key={item.id + "s"}>{item.name}</List.Item>
          ))}
        </List>
      ),
    },
    {
      key: "8",
      label: "Functional Areas",
      children: (
        <List bordered>
          {dataSource?.functional_areas.map((item: any) => (
            <List.Item key={item.id + "m"}>{item.name}</List.Item>
          ))}
        </List>
      ),
    },
    {
      key: "mmmm",
      label: "Functional Areas Descriptions",
      span: 24,
      children: (
        <List bordered>
          {dataSource?.functional_areas_descriptions.map((item: any) => (
            <List.Item key={item.id + "l"}>{item.description}</List.Item>
          ))}
        </List>
      ),
    },
  ];

  if (!dataSource) {
    return <Skeleton.Input active />;
  }
  return (
    <Row justify={"center"}>
      <Col xs={24}>
        <Row align={"middle"} justify={"space-between"}>
          <StepHeader title="Proposal Page" />
          <Space>
            <Button
              danger
              type="primary"
              onClick={() => {
                trigger(
                  { id: id },
                  {
                    onSuccess(response) {
                      if (response.statusCode === 200) {
                        notify(response.message, "success");
                      } else {
                        notify(response.message, "error");
                      }
                    },
                  }
                );
              }}
              size="large"
            >
              Reject Proposal
            </Button>
            <Button
              type="primary"
              onClick={() => {
                acceptTrigger(
                  { id: id },
                  {
                    onSuccess(response) {
                      if (response.statusCode === 200) {
                        notify(response.message, "success");
                      } else {
                        notify(response.message, "error");
                      }
                    },
                  }
                );
              }}
              size="large"
            >
              Accept Proposal
            </Button>
            <Button
              type="primary"
              onClick={() => {
                toPDF();
              }}
              size="large"
            >
              Export PDF
            </Button>
          </Space>
        </Row>

        <div
          style={{
            maxHeight: 600,
            overflow: "auto",
          }}
        >
          <Row ref={targetRef} style={{ margin: 10 }}>
            <Descriptions bordered items={items} />
          </Row>
        </div>
      </Col>
      <Drawer open={drawerOpen}>
        <Form>
          <Form.Item></Form.Item>
        </Form>
      </Drawer>
    </Row>
  );
}
