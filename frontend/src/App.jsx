/*
=========================================================
 AI Automated Answer Script Evaluation System
---------------------------------------------------------
 App.jsx
---------------------------------------------------------
 Root Component

 Responsibilities
 ✔ Load Application Routes
 ✔ Global Layout
 ✔ Future Providers
=========================================================
*/

import React from "react";
import AppRoutes from "./routes/AppRoutes";
import { AuthProvider } from './context/AuthContext';

function App() {
  return (
    <>
      <AuthProvider><AppRoutes /></AuthProvider>
    </>
  );
}

export default App;
