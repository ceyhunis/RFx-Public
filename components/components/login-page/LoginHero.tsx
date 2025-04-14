"use client";
import { useLoader } from "@/lib/providers/LoaderContextProvider";
import { DynamicRouter, postRequest } from "@/utils/request_utils";
import {
  Button,
  Card,
  Checkbox,
  Flex,
  Form,
  Input,
  Layout,
  message,
  Segmented,
  Steps,
  Typography,
} from "antd";
import { signIn } from "next-auth/react";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import useSWRMutation from "swr/mutation";
import Loader from "../general/Loader";
const { Title, Text } = Typography;
const { Content } = Layout;

interface SignUpData {
  username: string;
  firstName: string;
  lastName: string;
  email: string;
  password: string;
  confirmPassword: string;
  organization: string;
}

const formValidationMessages = {
  username: "Please input your username!",
  firstName: "Please input your first name!",
  lastName: "Please input your last name!",
  email: {
    required: "Please input your email!",
    valid: "Please enter a valid email!",
  },
  password: {
    required: "Please input your password!",
    confirm: "Please confirm your password!",
    match: "Passwords do not match!",
  },
  organization: "Please input your organization!",
};

const passwordValidationRules = [
  { required: true, message: "Please enter your password!" },
  { min: 8, message: "Password must be at least 8 characters!" },
  {
    pattern:
      /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*.])[A-Za-z\d!@#$%^&*.]{8,}$/,
    message:
      "Password must contain at least one uppercase letter, one lowercase letter, one number and one special character!",
  },
];

export default function LoginHero() {
  const [width, setWidth] = useState<number | undefined>(undefined);
  const userUrl = DynamicRouter("auth", "signup");
  const { trigger: signUpTrigger } = useSWRMutation(userUrl, postRequest);
  const [activeSegment, setActiveSegment] = useState<string | number>(
    "Sign In"
  );
  const router = useRouter();

  const [currentStep, setCurrentStep] = useState(0);
  const [formData, setFormData] = useState<Partial<SignUpData>>({});
  const [form] = Form.useForm();
  const [isLoading, setIsLoading] = useState(false);
  const onChange = async (value: number) => {
    if (value > currentStep) {
      try {
        await form.validateFields();
        setCurrentStep(value);
      } catch (error) {
        message.error("Please fill in all required fields correctly");
      }
    } else {
      setCurrentStep(value);
    }
  };

  const steps = [
    {
      title: "Basic Info",
    },
    {
      title: "Email Address",
    },
    {
      title: "Create Password",
    },
  ];

  useEffect(() => {
    const handleResize = () => setWidth(window.innerWidth);

    if (typeof window !== "undefined") {
      setWidth(window.innerWidth);
      window.addEventListener("resize", handleResize);
      return () => window.removeEventListener("resize", handleResize);
    }
  }, []);

  const handleLogin = async (data: { email: string; password: string }) => {
    setIsLoading(true);

    const sanitizedEmail = data.email.toLowerCase().trim();

    const nextAuthSettings = {
      email: sanitizedEmail,
      password: data.password,
      callbackUrl: "/panel",
      callbackUrlOnError: "/",
      redirect: true,
    };

    try {
      const response = await signIn("credentials", nextAuthSettings);
      if (response?.error) {
        message.error("Login failed: Invalid username or password");
      }
    } catch (error) {
      message.error("An error occurred during login");
    }
  };

  const handleNext = async (values: Partial<SignUpData>) => {
    try {
      await form.validateFields();
      setFormData((prev) => ({ ...prev, ...values }));
      setCurrentStep((prev) => prev + 1);
    } catch (error) {
      message.error("Please fill in all required fields correctly");
    }
  };

  const handlePrevious = () => {
    setCurrentStep((prev) => prev - 1);
  };

  const renderStepContent = () => {
    switch (currentStep) {
      case 0:
        return (
          <Form
            form={form}
            name="step1"
            onFinish={handleNext}
            layout="vertical"
            requiredMark={false}
            initialValues={formData}
          >
            <Form.Item
              label="First Name"
              name="firstName"
              rules={[
                { required: true, message: formValidationMessages.firstName },
              ]}
            >
              <Input style={{ height: 40 }} />
            </Form.Item>
            <Form.Item
              label="Last Name"
              name="lastName"
              rules={[
                { required: true, message: formValidationMessages.lastName },
              ]}
            >
              <Input style={{ height: 40 }} />
            </Form.Item>
            <Flex gap="small" justify="center">
              <Button
                type="primary"
                htmlType="submit"
                className="auth-submit-button"
                style={{
                  height: 48,

                  borderRadius: 8,
                  width: 160,
                  fontSize: 16,
                }}
              >
                Next
              </Button>
            </Flex>
          </Form>
        );

      case 1:
        return (
          <Form
            form={form}
            name="step2"
            onFinish={handleNext}
            layout="vertical"
            requiredMark={false}
            initialValues={formData}
          >
            <Form.Item
              label="E-mail"
              name="email"
              rules={[
                {
                  required: true,
                  message: formValidationMessages.email.required,
                },
                { type: "email", message: formValidationMessages.email.valid },
                {
                  pattern:
                    /^[A-Za-z0-9._%+-]+@(?!gmail\.com)(?!hotmail\.com)(?!yahoo\.com)(?!outlook\.com)[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/,
                  message: "Only corporate email addresses are allowed!",
                },
              ]}
            >
              <Input style={{ height: 40 }} />
            </Form.Item>
            <Flex gap="small" justify="center">
              <Button
                onClick={handlePrevious}
                style={{
                  height: 48,
                  borderRadius: 8,
                  width: 160,
                  borderColor: "#626DCF",
                  color: "#626DCF",
                  fontSize: 16,
                }}
              >
                Previous
              </Button>
              <Button
                type="primary"
                htmlType="submit"
                className="auth-submit-button"
                style={{
                  height: 48,
                  backgroundColor: "#626DCF",
                  borderRadius: 8,
                  width: 160,
                  fontSize: 16,
                }}
              >
                Next
              </Button>
            </Flex>
          </Form>
        );

      case 2:
        return (
          <Form
            form={form}
            name="step3"
            onFinish={(values) => {
              setIsLoading(true);
              const finalData = { ...formData, ...values };
              handleSignUp(finalData);
            }}
            layout="vertical"
            requiredMark={false}
            initialValues={formData}
          >
            <Form.Item
              label="Password"
              name="password"
              rules={passwordValidationRules}
            >
              <Input.Password style={{ height: 40 }} />
            </Form.Item>
            <Form.Item
              label="Confirm Password"
              name="confirmPassword"
              dependencies={["password"]}
              rules={[
                {
                  required: true,
                  message: formValidationMessages.password.confirm,
                },
                ({ getFieldValue }) => ({
                  validator(_, value) {
                    if (!value || getFieldValue("password") === value) {
                      return Promise.resolve();
                    }
                    return Promise.reject(
                      new Error(formValidationMessages.password.match)
                    );
                  },
                }),
              ]}
            >
              <Input.Password style={{ height: 40 }} />
            </Form.Item>
            <Flex gap="small" justify="center">
              <Button
                onClick={handlePrevious}
                style={{
                  height: 48,
                  borderRadius: 8,
                  width: 160,
                  borderColor: "#626DCF",
                  color: "#626DCF",
                  fontSize: 16,
                }}
              >
                Previous
              </Button>
              <Button
                type="primary"
                htmlType="submit"
                className="auth-submit-button"
                style={{
                  height: 48,
                  backgroundColor: "#626DCF",
                  borderRadius: 8,
                  width: 160,
                  fontSize: 16,
                }}
              >
                Sign Up
              </Button>
            </Flex>
          </Form>
        );
    }
  };

  const handleSignUp = async (values: SignUpData) => {
    setIsLoading(true);

    try {
      const email = values.email.toLowerCase().trim();

      const userData = {
        username: email,
        email: email,
        password: values.password,
        first_name: values.firstName.trim(),
        last_name: values.lastName.trim(),
        is_active: true,
        is_staff: false,
        is_superuser: false,
        value_propositions: "system",
      };
      signUpTrigger(userData, {
        onSuccess: (response) => {
          if (response.statusCode === 200 || response.statusCode === 201) {
            message.success("Registration successful");
            router.push("/");
            setActiveSegment("Sign In");
            setCurrentStep(0);
            form.resetFields();
            setIsLoading(false);
          } else {
            message.error(`${response.message} `);
            setIsLoading(false);
          }
        },
      });
    } catch (error) {
      message.error("An unexpected error occurred during registration");
      setIsLoading(false);
    }
  };

  const isMobile = width && width < 768;
  const isTablet = width && width >= 768 && width < 1024;

  return (
    <Loader isLoading={isLoading}>
      <Layout style={{ backgroundColor: "transparent" }}>
        <Content
          style={{ padding: isMobile ? "10px 0" : "20px 0", minHeight: "60vh" }}
        >
          <Flex
            justify="center"
            align="center"
            vertical
            style={{ height: "100%" }}
          >
            <Card
              style={{
                width: "90%",
                maxWidth: 1244,
                borderRadius: 15,
                background: "linear-gradient(120deg, #688EF5 0%, #8ec5fc 100%)",
                border: "none",
              }}
            >
              <Title
                level={2}
                style={{
                  color: "#101828",
                  fontSize: isMobile ? "24px" : "32px",
                  textAlign: "center",
                  marginBottom: 10,
                }}
              >
                Log in to your account
              </Title>
              <Flex justify="center" gap="small">
                <Segmented
                  options={["Sign In", "Sign Up"]}
                  value={activeSegment}
                  onChange={setActiveSegment}
                  className="auth-segment"
                />
              </Flex>
            </Card>

            <Card
              style={{
                width: "90%",
                maxWidth:
                  activeSegment === "Sign In"
                    ? isMobile
                      ? "80%"
                      : isTablet
                      ? "60%"
                      : "600px"
                    : isMobile
                    ? "80%"
                    : isTablet
                    ? "60%"
                    : "600px",
                border: "none",
                padding: isMobile ? "12px" : "20px",
              }}
            >
              {activeSegment === "Sign Up" && (
                <>
                  <div className="registration-steps-wrapper">
                    <Steps
                      size="small"
                      current={currentStep}
                      labelPlacement="horizontal"
                      items={steps}
                      onChange={onChange}
                      className="responsive-steps"
                    />
                  </div>
                  {renderStepContent()}

                  <Flex
                    justify="center"
                    align="center"
                    style={{
                      marginTop: 15,
                      flexDirection: isMobile ? "column" : "row",
                      gap: isMobile ? "8px" : "0",
                    }}
                  >
                    <Text style={{ color: "#475467" }}>
                      Already have an account?
                    </Text>
                    <Button
                      type="link"
                      style={{
                        color: "#626DCF",
                        paddingLeft: isMobile ? 0 : 8,
                        height: "auto",
                      }}
                      onClick={() => setActiveSegment("Sign In")}
                    >
                      Log in
                    </Button>
                  </Flex>
                </>
              )}
              <Form
                name={activeSegment === "Sign In" ? "login" : "register"}
                initialValues={{ remember: true }}
                onFinish={
                  activeSegment === "Sign In" ? handleLogin : handleSignUp
                }
                layout="vertical"
                requiredMark={false}
                style={{ width: "100%" }}
              >
                {activeSegment === "Sign In" && (
                  <>
                    <Form.Item
                      label="Email"
                      name="email"
                      rules={[
                        {
                          required: true,
                          message: "Please input your E-mail!",
                        },
                      ]}
                    >
                      <Input
                        style={{
                          height: 40,
                          width: "100%",
                          minWidth: isMobile ? "100%" : "400px",
                          maxWidth: "800px",
                        }}
                      />
                    </Form.Item>

                    <Form.Item
                      label="Password"
                      name="password"
                      rules={[
                        {
                          required: true,
                          message: "Please input your Password!",
                        },
                      ]}
                    >
                      <Input.Password
                        style={{
                          height: 40,
                          width: "100%",
                          minWidth: isMobile ? "100%" : "400px",
                          maxWidth: "800px",
                        }}
                      />
                    </Form.Item>

                    <Flex
                      justify="space-between"
                      align="center"
                      style={{
                        marginBottom: 24,
                        width: "100%",
                        maxWidth: isMobile ? "100%" : "800px",
                      }}
                    >
                      <Form.Item
                        name="remember"
                        valuePropName="checked"
                        noStyle
                      >
                        <Checkbox>Remember me</Checkbox>
                      </Form.Item>
                      <Button
                        type="link"
                        style={{ padding: 0, color: "#626DCF" }}
                        onClick={() => router.push("/forgot-password")}
                      >
                        Forgot password?
                      </Button>
                    </Flex>

                    <Flex justify="center" align="center" vertical>
                      <Form.Item>
                        <Button
                          block
                          type="primary"
                          htmlType="submit"
                          className="auth-submit-button"
                          style={{
                            height: isMobile ? 36 : 40,
                            width: isMobile ? "100%" : "400px",
                            fontSize: isMobile ? 16 : 20,
                            borderRadius: 12,
                          }}
                        >
                          {activeSegment}
                        </Button>
                      </Form.Item>
                    </Flex>
                  </>
                )}
              </Form>
              {activeSegment === "Sign In" && (
                <Flex
                  justify="center"
                  align="center"
                  style={{
                    marginTop: 15,
                    flexDirection: isMobile ? "column" : "row",
                    gap: isMobile ? "8px" : "0",
                  }}
                >
                  <Text style={{ color: "#475467" }}>
                    {`Don't have an account?`}
                  </Text>
                  <Button
                    type="link"
                    style={{
                      color: "#626DCF",
                      paddingLeft: isMobile ? 0 : 8,
                      height: "auto",
                    }}
                    onClick={() => setActiveSegment("Sign Up")}
                  >
                    Sign Up
                  </Button>
                </Flex>
              )}
            </Card>
          </Flex>
        </Content>
      </Layout>
    </Loader>
  );
}
