import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import { Toaster } from "react-hot-toast";
import axios from "axios";

import App from "./App";
import "./index.css";

// Applies to legacy pages that use axios directly, preventing endless loaders
// whenever the local API is unavailable or a route fails to respond.
axios.defaults.timeout = 10000;

/*
=========================================================
 AI Automated Answer Script Evaluation System
 Frontend Entry Point
---------------------------------------------------------
 This file initializes:
 ✓ React
 ✓ Browser Router
 ✓ Global Toast Notifications
 ✓ Global CSS
=========================================================
*/

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <BrowserRouter>
      <Toaster
        position="top-right"
        reverseOrder={false}
        gutter={10}
        containerStyle={{
          top: 20,
          right: 20,
        }}
        toastOptions={{
          duration: 3500,

          success: {
            iconTheme: {
              primary: "#10B981",
              secondary: "#ffffff",
            },
          },

          error: {
            iconTheme: {
              primary: "#EF4444",
              secondary: "#ffffff",
            },
          },

          style: {
            background: "#ffffff",
            color: "#111827",
            borderRadius: "14px",
            padding: "14px 18px",
            boxShadow:
              "0 10px 30px rgba(15,23,42,0.10)",
            fontSize: "14px",
            fontWeight: 500,
            border: "1px solid #E5E7EB",
          },
        }}
      />

      <App />
    </BrowserRouter>
  </React.StrictMode>
);
