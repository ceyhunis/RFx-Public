import { Input, Checkbox, Select, InputNumber, DatePicker, Upload } from "antd";
import Password from "antd/es/input/Password";
import TextArea from "antd/es/input/TextArea";
import ReactNode from "react";

export interface ApiResponse<T> {
  data: T;
  message: string;
  statusCode: number;
}

export type FormMetaType = {
  name: string;
  label: string;
  type:
    | typeof Input
    | typeof Checkbox
    | typeof Select
    | typeof InputNumber
    | typeof DatePicker
    | typeof Password
    | typeof TextArea
    | typeof ReactNode;
  placeholder?: string;
  rules?: Array<{
    required?: boolean;
    message?: string;
    [key: string]: any;
  }>;
  lookup?: string;
  lookupTextField?: string;
  lookupValueField?: string;
  options?: Array<any>;
  disabled?: boolean;
  mode?: "multiple" | "tags" | undefined;
};
