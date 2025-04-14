"use client";

import { notify } from "@/utils/functions_utils";
import { DynamicRouter, postRequest } from "@/utils/request_utils";
import { LockOutlined } from "@ant-design/icons";
import { Button, Card, Flex, Form, Input, Typography } from "antd";
import { useRouter, useSearchParams } from "next/navigation";
import { useEffect, useState, useCallback } from "react";
import useSWRMutation from "swr/mutation";

const { Title, Text } = Typography;

const NewPasswordHero = () => {
  const [loading, setLoading] = useState(false);
  const router = useRouter();
  const [width, setWidth] = useState<number | undefined>(undefined);
  const searchParams = useSearchParams();
  const token = searchParams.get("token");
  const email = searchParams.get("email");

  const url = DynamicRouter("auth", "new-password");
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

  const onFinish = async (values: {
    newPassword: string;
    confirmPassword: string;
  }) => {
    setLoading(true);
    trigger(
      {
        new_password: values.newPassword,
        confirm_password: values.confirmPassword,
        token,
        email,
      },
      {
        onSuccess(data, key, config) {
          if (data.status === 200) {
            setLoading(false);
            notify("Password updated successfully", "success");
            router.push("/");
          } else {
            setLoading(false);
            notify(data.message, "error");
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
              Set New Password
            </Title>
            <Text
              style={{
                textAlign: "center",
                display: "block",
                color: "#475467",
                fontSize: 16,
              }}
            >
              Please enter your new password
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
            name="new-password"
            layout="vertical"
            requiredMark={false}
            onFinish={onFinish}
            style={{
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              width: "100%",
            }}
          >
            <Form.Item
              label="New Password"
              name="newPassword"
              rules={[
                { required: true, message: "Please enter your new password" },
                {
                  min: 6,
                  message: "Password must be at least 6 characters long",
                },
              ]}
              style={{
                width: "150%",
                maxWidth: "500px",
                margin: "0 auto",
                marginBottom: "1rem",
              }}
            >
              <Input.Password
                prefix={<LockOutlined style={{ color: "#626DCF" }} />}
                size="large"
                placeholder="Enter your new password"
                style={{ height: 40 }}
              />
            </Form.Item>

            <Form.Item
              label="Confirm Password"
              name="confirmPassword"
              rules={[
                { required: true, message: "Please confirm your password" },
                {
                  min: 6,
                  message: "Password must be at least 6 characters long",
                },
              ]}
              style={{
                width: "150%",
                maxWidth: "500px",
                margin: "0 auto",
                marginBottom: "1rem",
              }}
            >
              <Input.Password
                prefix={<LockOutlined style={{ color: "#626DCF" }} />}
                size="large"
                placeholder="Confirm your password"
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
               
              >
                Update Password
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
};

export default NewPasswordHero;
