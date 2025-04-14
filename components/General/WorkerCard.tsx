"use client";

import React, { useState } from "react";
import {
  Modal,
  Select,
  Button,
  message,
  Form,
  Typography,
  Divider,
} from "antd";
import useSWRMutation from "swr/mutation";
import { DynamicRouter, postRequest } from "@/utils/request_utils";
import useSWR from "swr";
import { useForm } from "antd/es/form/Form";
import styles from "./WorkerCard.module.css";

const { Title, Text } = Typography;

interface BusinessCycle {
  id: number;
  name: string;
}

interface WorkerCardProps {
  name: string;
  email: string;
  business_cycles: string[];
  user_id: number;
  mutate: () => void;
}

const WorkerCard: React.FC<WorkerCardProps> = ({
  name,
  email,
  business_cycles = [],
  user_id,
  mutate,
}) => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isConfirmModalOpen, setIsConfirmModalOpen] = useState(false);

  const { data: businessCycles } = useSWR(
    DynamicRouter("project", "business-cycle")
  );
  const [form] = useForm();

  const { trigger } = useSWRMutation(
    DynamicRouter("auth", "user-match-business-cycle"),
    postRequest
  );

  const handleCardClick = () => {
    if (businessCycles?.data) {
      // Mevcut business cycles'ların ID'lerini bul
      const currentCycleIds = businessCycles.data
        .filter((cycle: BusinessCycle) => business_cycles.includes(cycle.name))
        .map((cycle: BusinessCycle) => cycle.id);

      // Form'u ID'ler ile set et
      form.setFieldsValue({
        business_cycle_ids: currentCycleIds
      });
    }
    setIsModalOpen(true);
  };

  const handleModalClose = () => {
    setIsModalOpen(false);
  };

  const handleSubmit = async () => {
    const business_cycle_ids = form.getFieldValue("business_cycle_ids");
    try {
      const data = {
        user_id: user_id,
        business_cycle_ids: business_cycle_ids,
      };
      await trigger(data, {
        onSuccess: (response) => {
          if (response.statusCode === 200 || response.statusCode === 201) {
            message.success("Business Cycle matched successfully");
            setIsModalOpen(false);
          } else {
            message.error(`${response.message} `);
          }
        },
      });
      mutate();
    } catch (error) {
      console.error("Error submitting data:", error);
    }
  };

  const handleClearSelections = () => {
    setIsConfirmModalOpen(true);
  };

  const handleConfirmClear = () => {
    form.setFieldValue("business_cycle_ids", []);
    setIsConfirmModalOpen(false);
  };

  return (
    <>
      <div className={styles.container} onClick={handleCardClick}>
        <div className={styles.infoOverlay} data-info-overlay>
          <span>ℹ️</span>
          <span>Click to assign</span>
        </div>
        <div className={styles.content}>
          <h2 className={styles.header}>{name}</h2>
          <p className={styles.subHeader}>{email}</p>

          {(() => {
            const filteredCycles = business_cycles
              .map((cycleName: string) => {
                const cycle = businessCycles?.data?.find((c: BusinessCycle) => c.name === cycleName);
                return cycle?.name || cycleName;
              })
              .filter((cycle: string) => cycle && cycle.trim() !== "");

            return (
              <>
                <div className={styles.cycleInfo}>
                  <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                    <span style={{ color: '#666' }}>Business Cycles</span>
                    {filteredCycles.length > 0 && (
                      <span className={styles.cycleCount}>
                        ({filteredCycles.length})
                      </span>
                    )}
                  </span>
                </div>
                <div className={styles.cycleList}>
                  {filteredCycles.length > 0 ? (
                    filteredCycles.map((name) => (
                      <span key={name} className={styles.cycleItem}>
                        {name}
                      </span>
                    ))
                  ) : (
                    <span className={styles.noCycles}>
                      No cycles assigned
                    </span>
                  )}
                </div>
              </>
            );
          })()}
        </div>
      </div>

      <Modal
        title={
          <div
            style={{
              borderBottom: "1px solid rgb(230,235,255)",
              padding: "0 0 16px 0",
            }}
          >
            <Title level={4} style={{ margin: 0, color: "rgb(0,80,255)" }}>
              Assign Business Cycles
            </Title>
          </div>
        }
        open={isModalOpen}
        onCancel={handleModalClose}
        footer={null}
        centered
        width={480}
        bodyStyle={{
          padding: "24px",
          maxHeight: "80vh",
          overflow: "auto",
          backgroundColor: "#ffffff",
        }}
        style={{
          borderRadius: "12px",
          overflow: "hidden",
        }}
      >
        <div style={{ marginBottom: "24px" }}>
          <Text
            type="secondary"
            style={{ fontSize: "13px", display: "block", marginBottom: "8px" }}
          >
            Worker Information
          </Text>
          <div
            style={{
              backgroundColor: "rgb(242,245,255)",
              padding: "16px",
              borderRadius: "8px",
              border: "1px solid rgb(230,235,255)",
            }}
          >
            <Text
              strong
              style={{
                fontSize: "15px",
                display: "block",
                marginBottom: "4px",
                color: "rgb(0,80,255)",
              }}
            >
              {name}
            </Text>
            <Text type="secondary" style={{ fontSize: "13px" }}>
              {email}
            </Text>
          </div>
        </div>

        <Form
          form={form}
          layout="vertical"
          initialValues={{ business_cycle_ids: business_cycles }}
        >
          <Form.Item 
            label={
              <Text style={{ fontSize: "13px", fontWeight: 500, color: "rgb(0,80,255)" }}>
                Business Cycles
              </Text>
            }
            name="business_cycle_ids"
            style={{ marginBottom: "24px" }}
          >
            <Select
              mode="multiple"
              placeholder="Select business cycles to assign"
              style={{ width: "100%" }}
              options={businessCycles?.data?.map((cycle: BusinessCycle) => ({
                label: cycle.name,
                value: cycle.id,
              }))}
              defaultValue={businessCycles?.data
                ?.filter((cycle: BusinessCycle) => business_cycles.includes(cycle.name))
                .map((cycle: BusinessCycle) => cycle.id)}
              maxTagCount={7}
              listHeight={220}
              dropdownStyle={{
                minWidth: "200px",
                backgroundColor: "rgb(242,245,255)",
              }}
            />
          </Form.Item>

          <div
            style={{
              display: "flex",
              flexDirection: "column",
              gap: "8px",
              marginTop: "24px",
            }}
          >
            <Button
              type="primary"
              onClick={handleSubmit}
              size="large"
              style={{
                width: "100%",
                height: "40px",
                backgroundColor: "rgb(242,245,255)",
                borderColor: "rgb(0,80,255)",
                color: "rgb(0,80,255)",
                fontWeight: 500,
                fontSize: "14px",
                transition: "all 0.3s ease",
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.backgroundColor = "rgb(0,80,255)";
                e.currentTarget.style.color = "rgb(242,245,255)";
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.backgroundColor = "rgb(242,245,255)";
                e.currentTarget.style.color = "rgb(0,80,255)";
              }}
            >
              Assign Business Cycles
            </Button>
            <Button
              onClick={handleClearSelections}
              size="middle"
              type="text"
              style={{
                width: "auto",
                alignSelf: "center",
                height: "32px",
                fontSize: "13px",
                color: "rgb(0,80,255)",
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.opacity = "0.7";
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.opacity = "1";
              }}
            >
              Clear All Selections
            </Button>
          </div>
        </Form>
      </Modal>

      <Modal
        title={
          <div style={{ borderBottom: '1px solid rgb(230,235,255)', padding: '0 0 16px 0' }}>
            <Title level={4} style={{ margin: 0, color: 'rgb(0,80,255)' }}>Clear Selections</Title>
          </div>
        }
        open={isConfirmModalOpen}
        onCancel={() => setIsConfirmModalOpen(false)}
        footer={
          <div style={{ display: 'flex', gap: '8px', justifyContent: 'flex-end' }}>
            <Button
              onClick={() => setIsConfirmModalOpen(false)}
              size="middle"
              style={{
                fontSize: '13px'
              }}
            >
              Cancel
            </Button>
            <Button
              onClick={handleConfirmClear}
              size="middle"
              style={{
                backgroundColor: 'rgb(242,245,255)',
                borderColor: 'rgb(0,80,255)',
                color: 'rgb(0,80,255)',
                fontSize: '13px',
                transition: 'all 0.3s ease'
              }}
              onMouseEnter={e => {
                e.currentTarget.style.backgroundColor = 'rgb(0,80,255)';
                e.currentTarget.style.color = 'rgb(242,245,255)';
              }}
              onMouseLeave={e => {
                e.currentTarget.style.backgroundColor = 'rgb(242,245,255)';
                e.currentTarget.style.color = 'rgb(0,80,255)';
              }}
            >
              Yes, clear all
            </Button>
          </div>
        }
        centered
        width={400}
        bodyStyle={{ 
          padding: "24px",
          backgroundColor: "#ffffff"
        }}
        style={{
          borderRadius: '12px',
          overflow: 'hidden'
        }}
      >
        <div style={{ 
          backgroundColor: 'rgb(242,245,255)',
          padding: '16px',
          borderRadius: '8px',
          border: '1px solid rgb(230,235,255)',
          fontSize: '13px',
          color: '#666'
        }}>
          <Text>Are you sure you want to remove all selections?</Text>
        </div>
      </Modal>
    </>
  );
};

export default WorkerCard;
