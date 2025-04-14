import {
  Checkbox,
  Input,
  InputNumber,
  Select
} from "antd";
import { FormMetaType } from "./general_types";

export const userFieldMetaData: FormMetaType[] = [

  {
    name: "first_name",
    label: "First Name",
    type: Input,
    placeholder: "",
    rules: [{ required: true, message: "Please input first name!" }],
  },
  {
    name: "last_name",
    label: "Last Name",
    type: Input,
    placeholder: "",
    rules: [{ required: true, message: "Please input last name!" }],
  },
  {
    name: "email",
    label: "Email",
    type: Input,
    placeholder: "",
    rules: [{ required: true, message: "Please input email!" }],
  },
  {
    name: "password",
    label: "Password",
    type: Input.Password,
    placeholder: "Enter password",
    rules: [
      {
        required: false,
        message: "Please input password!",
      },
      {
        min: 6,
        message: "Password must be at least 6 characters!",
      }
    ],
  },
  {
    name: "role",
    label: "Role",
    type: Select,
    placeholder: "Select Role",
    rules: [{ required: true, message: "Please select role!" }],
  },
  {
    name: "organization",
    label: "Organization",
    type: Select,
    rules: [{ required: false }],
    placeholder: "Select Organization",
  },
];

export const providerFieldMetaData: FormMetaType[] = [
  {
    name: "company_name",
    label: "Company Name",
    type: Input,
    placeholder: "Enter company name",
    rules: [
      { required: true, message: "Company name is required!" },
      { min: 2, message: "Company name must be at least 2 characters!" },
      { max: 100, message: "Company name cannot exceed 100 characters!" },
      {
        pattern: /^[a-zA-Z0-9\s&.-]+$/,
        message: "Company name can only contain letters, numbers, spaces, &, ., and -"
      }
    ]
  },
  {
    name: "contact_name",
    label: "Contact Name",
    type: Input,
    placeholder: "Enter contact name",
    rules: [
      { required: true, message: "Contact name is required!" },
      { min: 2, message: "Contact name must be at least 2 characters!" },
      { max: 100, message: "Contact name cannot exceed 100 characters!" },
      {
        pattern: /^[a-zA-Z\s.-]+$/,
        message: "Contact name can only contain letters, spaces, . and -"
      }
    ]
  },
  {
    name: "contact_phone",
    label: "Contact Phone",
    type: Input,
    placeholder: "Enter contact phone",
    rules: [
      { required: true, message: "Contact phone is required!" },
      {
        pattern: /^[+]?[(]?[0-9]{3}[)]?[-\s.]?[0-9]{3}[-\s.]?[0-9]{4,6}$/,
        message: "Please enter a valid phone number! (e.g., +1234567890 or 123-456-7890)"
      }
    ]
  },
  {
    name: "contact_email",
    label: "Contact Email",
    type: Input,
    placeholder: "Enter contact email",
    rules: [
      { required: true, message: "Contact email is required!" },
      { type: 'email', message: "Please enter a valid email address!" },
      { max: 100, message: "Email cannot exceed 100 characters!" },
      {
        pattern: /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/,
        message: "Please enter a valid email format!"
      }
    ]
  }
];

export const organizationFieldMetaData: FormMetaType[] = [
  {
    name: "name",
    label: "Name",
    type: Input,
    rules: [{ required: true, message: "Please input organization name!" }],
  },
];

export const roleFieldMetaData: FormMetaType[] = [
  {
    name: "name",
    label: "Name",
    type: Input,
    rules: [{ required: true, message: "Please input role name!" }],
  },
  {
    name: "is_super_role",
    label: "Super Role",
    type: Checkbox,
    placeholder: "",
  },
];

export const industryFieldMetaData: FormMetaType[] = [
  {
    name: "name",
    label: "Name",
    type: Input,
    rules: [{ required: true, message: "Please input industry name!" }],
  },
  {
    name: "description",
    label: "Description",
    type: Input.TextArea,
    rules: [{ required: true, message: "Please input industry description!" }],
  },
];

export const serviceFieldMetaData: FormMetaType[] = [
  {
    name: "name",
    label: "Name",
    type: Input,
    rules: [{ required: true, message: "Please input service name!" }],
  },
  {
    name: "description",
    label: "Description",
    type: Input.TextArea,
    rules: [{ required: true, message: "Please input service description!" }],
  },
];

export const questionnaireFieldMetaData: FormMetaType[] = [
  {
    name: "name",
    label: "Name",
    type: Input,
    rules: [{ required: true, message: "Please input questionnaire name!" }],
  },
  {
    name: "type",
    label: "Value Type",
    type: Select,
    options: [
      { value: "number", label: "Number" },
      { value: "text", label: "Text" },
      { value: "boolean", label: "Boolean" },
      { value: "select", label: "Select" },
    ],
    rules: [{ required: true, message: "Please select value type!" }],
  },
  {
    name: "description",
    label: "Description",
    type: Input.TextArea,
    rules: [
      { required: true, message: "Please input questionnaire description!" },
    ],
  },
];

export const businessCycleFieldMetaData: FormMetaType[] = [
  {
    name: "order",
    label: "Order",
    type: InputNumber,
  },
  {
    name: "name",
    label: "Name",
    type: Input,
  },
  {
    name: "description",
    label: "Description",
    type: Input.TextArea,
  },
];

export const functionalAreaFieldMetaData: FormMetaType[] = [
  {
    name: "business_cycle_id",
    label: "Business Cycle",
    type: Select,
  },
  {
    name: "order",
    label: "Order",
    type: InputNumber,
  },
  {
    name: "name",
    label: "Name",
    type: Input,
  },
  {
    name: "description",
    label: "Functionality Description",
    type: Input.TextArea,
  },
];

export const demoFieldMetaData: FormMetaType[] = [
  {
    name: "first_name",
    label: "First Name",
    type: Input,
  },
  {
    name: "last_name",
    label: "Last Name",
    type: Input,
  },
  {
    name: "email",
    label: "Email",
    type: Input,
  },
  {
    name: "phone",
    label: "Phone",
    type: Input,
  },
  {
    name: "message",
    label: "Message",
    type: Input.TextArea,
  },
];

export const submiteedMetaData = [
  {
    name: "recived_person",
    label: "Name",
    type: Input,
    disable: true,
    rules: [
      {
        required: true,
        message: "Please input the name of the received person!",
      },
    ],
  },
  {
    name: "recived_person_email",
    label: "Email",
    type: Input,
    disable: true,
    rules: [
      {
        required: true,
        message: "Please input the email of the received person!",
      },
    ],
  },
  {
    name: "status",
    label: "Status",
    type: Select,
    options: ["in-progress", "completed", "pending", "cancelled"],
    rules: [{ required: false, message: "Please select the status!" }],
  },
  {
    name: "last_login_to_rfp",
    label: "Last Login to RFP",
    type: Input,
    rules: [
      { required: false, message: "Please input the last login date to RFP!" },
    ],
  },
  {
    name: "last_login_ip_address",
    label: "Last Login IP Address",
    type: Input,
    rules: [
      { required: false, message: "Please input the last login IP address!" },
    ],
  },

  {
    name: "is_opened",
    label: "Is Opened",
    type: Checkbox,
    disable: true,
    rules: [{ required: false, message: "Please indicate if it is opened!" }],
  },
];
