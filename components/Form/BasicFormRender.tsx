import { FormMetaType } from "@/types/general_types";
import {
  Button,
  Checkbox,
  DatePicker,
  Form,
  Input,
  InputNumber,
  Row,
  Select,
  Typography
} from "antd";
import { FormInstance, useWatch } from "antd/es/form/Form";
import React, { createElement, useCallback, useEffect, useState } from "react";
import useSWRMutation from "swr/mutation";
import Loader from "../components/general/Loader";

interface BasicFormRenderProps {
  metadata: FormMetaType[];
  form?: FormInstance<any>;
  onFinish?: (values: any) => void;
  onCancel?: () => void;
  buttonText?: string;
  operation?: any;
  mutationURL?: string;
  lookup?: any;
  extraButtons?: React.ReactNode;
  initialValues?: any;
}

export default function BasicFormRender({
  metadata,
  form,
  onFinish,
  onCancel,
  buttonText,
  operation,
  mutationURL,
  lookup,
  extraButtons,
  initialValues,
}: BasicFormRenderProps) {
  const watching = useWatch([], form);
  const [isLoading, setIsLoading] = useState(false);
  const [watchingValues, setWatchingValues] = useState<any>({});

  useEffect(() => {
    if (initialValues && form) {
      form.setFieldsValue(initialValues);
    }
  }, [initialValues, form]);

  const { trigger } = useSWRMutation(mutationURL, operation);

  const formFieldCallback = useCallback(
    (field: FormMetaType, key: any) => {
      const props: any = {
        placeholder: field.placeholder,
        disabled: initialValues ? field.disabled : false,
        options: field.type === Select ? field.options : [],
        mode: field.mode,
      };

      if (field.name === "organization" && field.type === Select) {
        props.options = lookup?.organization || [];
        props.showSearch = true;
        props.filterOption = (input: string, option: any) => {
          if (!option || !option.label) return false;
          return option.label.toString().toLowerCase().includes(
            input.toLowerCase()
          );
        };
      }

      if (field.name === "role" && field.type === Select) {
        props.options = lookup?.role || [];
        props.showSearch = true;
        props.filterOption = (input: string, option: any) => {
          if (!option || !option.label) return false;
          return option.label.toString().toLowerCase().includes(
            input.toLowerCase()
          );
        };
      }




      
      if (
        lookup &&
        (lookup[field.name.substring(0, field.name.length - 3)] ||
          lookup[field.name.substring(0, field.name.length - 4)]) &&
        field.type === Select &&
        field.name !== "role" &&
        field.name !== "organization"
      ) {
        let response: any = [];
        if (lookup[field.name.substring(0, field.name.length - 3)]) {
          response = lookup[field.name.substring(0, field.name.length - 3)];
        }
        if (lookup[field.name.substring(0, field.name.length - 4)]) {
          response = lookup[field.name.substring(0, field.name.length - 4)];
        }

        if (watchingValues && watchingValues[field.name] && watching) {
          props.options = response
            ?.filter(
              (item: any) =>
                item[watchingValues[field.name]] ===
                watching[watchingValues[field.name]]
            )
            .map((item: any) => ({
              value: item.id,
              label: item.name ?? `${item.first_name} ${item.last_name}`,
            }));
        } else {
          props.options = response?.map((item: any) => ({
            value: item.id,
            label: item.name ?? `${item.first_name} ${item.last_name}`,
          }));
        }

        props.showSearch = true;
        props.filterOption = (input: string, option: any) =>
          (option?.label?.toLowerCase() ?? "").includes(
            input.toLowerCase()
          );
      }






      if (field.type === Select || field.type === InputNumber || field.type === DatePicker) {
        props.style = { width: "100%" };
        if (field.type === Select) {
          props.allowClear = true;
        }
      }

      if (field.type === Input.TextArea) {
        props.style = {
          resize: "none",
          height: "100px",
          overflow: "scroll",
        };
      }

      if (field.type === Checkbox) {
        return (
          <Form.Item
            key={key}
            rules={field.rules}
            name={field.name}
            valuePropName="checked"
            getValueProps={(value) => ({ checked: value })}
            getValueFromEvent={(e) => e.target.checked}
          >
            <Row justify={"start"} align={"middle"}>
              <Checkbox
                defaultChecked={initialValues?.[field.name]}
                {...props}
                onChange={(e) => {
                  if (e.target.checked) {
                    form?.setFieldsValue({
                      [field.name]: true,
                    });
                  }
                }}
              />
              <Typography.Text style={{ fontWeight: 500, fontSize: 14, marginLeft: 10 }}>
                {field.label}
              </Typography.Text>
            </Row>
          </Form.Item>
        );
      }

      return (
        <Form.Item
          rules={field.rules}
          key={key}
          label={
            <Typography.Text style={{ fontWeight: 500, fontSize: 14 }}>
              {field.label}
            </Typography.Text>
          }
          name={field.name}
        >
          {/* @ts-ignore */}
          {createElement(field.type, props)}
        </Form.Item>
      );
    },
    [watching, form, initialValues, lookup]
  );

  const handleFinish = async (values: any) => {
    try {
      setIsLoading(true);
      onFinish?.(values);
    } catch (error) {
      console.error('Form submission error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Loader isLoading={isLoading}>
      <Form
        form={form}
        layout="vertical"
        initialValues={initialValues}
        onFinish={handleFinish}
      >
        {metadata.map(formFieldCallback)}
        <Form.Item>
          <Button 
            htmlType="submit" 
            type="primary" 
            block
            style={{ marginBottom: 10 }}
          >
            {buttonText || "Save"}
          </Button>
          
          <Button 
            onClick={() => onCancel?.()} 
            block
            style={{ marginBottom: 10 }}
          >
            Cancel
          </Button>

          {extraButtons && (
            <div>
              {extraButtons}
            </div>
          )}
        </Form.Item>
      </Form>
    </Loader>
  );
}
