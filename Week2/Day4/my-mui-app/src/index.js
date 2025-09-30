import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";  // ⬅️ import router
import App from "./App";
import "./styles.css"; // if you have global styles

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <BrowserRouter>   {/* ⬅️ wrap App in Router */}
      <App />
    </BrowserRouter>
  </React.StrictMode>
);
