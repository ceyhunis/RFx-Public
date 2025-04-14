"use client";

import { notify } from "@/utils/functions_utils";
import { DynamicRouter, postRequest } from "@/utils/request_utils";
import { MailOutlined } from "@ant-design/icons";
import { Button, Card, Flex, Form, Input, Typography } from "antd";
import { redirect, useRouter } from "next/navigation";
import { useEffect, useState, useCallback } from "react";
import useSWRMutation from "swr/mutation";

const { Title, Text } = Typography;

export default function ForgotPasswordHero() {
  const [loading, setLoading] = useState(false);
  const [width, setWidth] = useState<number | undefined>(undefined);
  const router = useRouter();
  const url = DynamicRouter("auth", "reset-password");
  const { trigger } = useSWRMutation(url, postRequest);

  const handleResize = useCallback(() => {
    setWidth(window.innerWidth);
  }, []);

  useEffect(() => {
    if (typeof window !== "undefined") {
      setWidth(window.innerWidth);
      window.addEventListener("resize", handleResize);
      return () => window.removeEventListener("resize", handleResize);
    }
  }, [handleResize]);

  const isMobile = width && width < 768;
  const isTablet = width && width >= 768 && width < 1024;

  const handleSubmit = async (values: { email: string }) => {
    setLoading(true);
    trigger(
      { email: values.email },
      {
        onSuccess(response) {
          if (response.statusCode === 200) {
            notify(response.message, "success");
            router.push("/");
          } else {
            notify(response.message, "error");
          }
        },
        onError() {
          setLoading(false);
          notify("An error occurred", "error");
        },
      }
    );
  };

  return (
    <Flex justify="center" align="center" vertical style={{ height: "100%" }}>
      <div className="fadeInDown">
        <Card
          style={{
            width: "90%",
            maxWidth: 1244,
            borderRadius: 15,
            background: "linear-gradient(120deg, #e0c3fc 0%, #8ec5fc 100%)",
            border: "none",
            margin: "0 auto",
          }}
        >
          <Flex vertical justify="center" align="center">
            <Title
              level={2}
              style={{
                color: "#101828",
                fontSize: isMobile ? "24px" : "32px",
                textAlign: "center",
                marginBottom: 10,
              }}
            >
              Forgot Password
            </Title>
            <Text
              style={{
                textAlign: "center",
                display: "block",
                color: "#475467",
                fontSize: 16,
              }}
            >
              Please enter the email address associated with your account
            </Text>
          </Flex>
        </Card>
      </div>

      <div className="fadeInUp">
        <Card
          style={{
            width: "90%",
            maxWidth: isMobile ? "100%" : isTablet ? "60%" : "600px",
            border: "none",
            padding: isMobile ? "12px" : "24px",
            margin: "0 auto",
          }}
        >
          <Form
            name="forgot-password"
            layout="vertical"
            requiredMark={false}
            onFinish={handleSubmit}
            style={{
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              width: "100%",
            }}
          >
            <Form.Item
              label="E-mail"
              name="email"
              rules={[
                { required: true, message: "Email is required" },
                {
                  type: "email",
                  message: "Please enter a valid email address",
                },
              ]}
              style={{
                width: "150%",
                maxWidth: "500px",
                margin: "0 auto",
                marginBottom: "1rem",
              }}
            >
              <Input
                prefix={<MailOutlined style={{ color: "#626DCF" }} />}
                size="large"
                placeholder="Enter your email"
                style={{ height: 40 }}
              />
            </Form.Item>

            <Flex
              justify="center"
              align="center"
              vertical
              style={{
                width: "100%",
                gap: "1rem",
              }}
            >
              <Button
                type="primary"
                htmlType="submit"
                loading={loading}
                className="auth-submit-button"
                size="large"
              >
                Reset Password
              </Button>

              <Button
                onClick={() => router.push("/")}
                className="back-to-login-button"
                style={{
                  height: isMobile ? 29 : 32,
                  width: isMobile ? "80%" : "280px",
                  fontSize: isMobile ? 14 : 16,
                  borderRadius: 12,
                  borderColor: "#626DCF",
                  color: "#626DCF",
                }}
              >
                Back to Login
              </Button>
            </Flex>
          </Form>
        </Card>
      </div>
    </Flex>
  );
}
