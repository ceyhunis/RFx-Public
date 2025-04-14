import type { ThemeConfig } from "antd";
import { Poppins } from "next/font/google";

const poppin = Poppins({
  subsets: ["latin"],
  weight: ["400", "500", "600"],
});

const theme: ThemeConfig = {
  token: {
    fontSize: 16,
    fontFamily: poppin.style.fontFamily,
  },
  components: {
    Layout: {
      headerBg: "transparent",
    },
    Button: {
      colorPrimary: "#0050FF",
      colorText: "black",
      colorPrimaryText: "black",
      colorPrimaryHover: "#88D9A6",
      boxShadow: "rgba(0, 0, 0, 0.24) 0px 3px 8px;",
      colorPrimaryActive: "black",
      colorPrimaryBg: "black",
      colorPrimaryTextActive: "black",
      fontFamily: poppin.style.fontFamily,
      fontSize: 14,
      borderRadius: 8,
      colorPrimaryBorder: "#9630f5",
    },
    Radio: {
      colorPrimary: "#3030f5b4",
    },
    Menu: {
      itemBorderRadius: 80,
      itemColor: "white",
      itemHoverColor: "black",
      itemHoverBg: "white",
      colorPrimary: "black",
    },
    Input: {
      fontSize: 14,
    },
    Select: {
      fontSize: 14,
    },
    Table: {
      fontSize: 14,
    },
    Steps: {
      fontSize: 14,
    },
  },
};

export default theme;
