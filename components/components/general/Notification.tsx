"use client";
import React from "react";
import { ToastContainer } from "react-toastify";

export default function Notification() {
  return (
    <ToastContainer
      position="top-right"
      autoClose={4000}
      newestOnTop={false}
      closeOnClick
      rtl={false}
      pauseOnFocusLoss
      draggable
      pauseOnHover
      theme="light"
      hideProgressBar
    />
  );
}
