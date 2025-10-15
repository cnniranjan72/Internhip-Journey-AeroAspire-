import React, { useEffect, useMemo, useState } from "react";
import { Routes, Route, useNavigate } from "react-router-dom";
import { ThemeProvider, CssBaseline, Container, Button } from "@mui/material";
import HomePage from "./pages/HomePage";
import AddTaskPage from "./pages/AddTaskPage";
import AboutPage from "./pages/AboutPage";
import LoginPage from "./pages/LoginPage";
import NavBar from "./components/NavBar";
import themeBuilder from "./theme";

const API_BASE = "http://localhost:5000/api/v1";

export default function App() {
  const navigate = useNavigate();
  const [tasks, setTasks] = useState([]);
  const [mode, setMode] = useState("light");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [token, setToken] = useState(localStorage.getItem("token") || "");

  const theme = useMemo(() => themeBuilder(mode), [mode]);

  const handleLogin = (jwt) => {
    localStorage.setItem("token", jwt);
    setToken(jwt);
    navigate("/"); // redirect to home after login
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    setToken("");
    navigate("/login");
  };

  // Fetch tasks
  useEffect(() => {
    const fetchTasks = async () => {
      setLoading(true);
      setError("");
      try {
        const res = await fetch(`${API_BASE}/tasks`);
        if (!res.ok) throw new Error(`Failed to fetch tasks: ${res.status}`);
        const data = await res.json();
        const items = data.items || data || [];
        setTasks(Array.isArray(items) ? items : []);
      } catch (err) {
        console.error(err);
        setError("Could not load tasks. Please try again later.");
      } finally {
        setLoading(false);
      }
    };
    fetchTasks();
  }, []);

  // Add task
  const addTask = async (taskPayload) => {
    if (!token) return alert("Please login first");
    try {
      const res = await fetch(`${API_BASE}/tasks`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          title: taskPayload.title.trim(),
          description: taskPayload.description?.trim() || "",
        }),
      });

      if (!res.ok) throw new Error("Failed to add task");
      const newTask = await res.json();
      setTasks((prev) => [newTask, ...prev]);
      navigate("/");
    } catch (err) {
      console.error(err);
      alert("Failed to add task");
    }
  };

  // Delete task
  const deleteTask = async (id) => {
    if (!token) return alert("Please login first");
    try {
      const res = await fetch(`${API_BASE}/tasks/${id}`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${token}` },
      });
      if (res.ok) {
        setTasks((prev) => prev.filter((t) => t.id !== id));
      } else {
        alert("Delete failed!");
      }
    } catch (err) {
      console.error(err);
    }
  };

  const toggleTheme = () => setMode((m) => (m === "light" ? "dark" : "light"));

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <NavBar mode={mode} onToggleTheme={toggleTheme} token={token} onLogout={handleLogout} />
      <Container maxWidth="md" sx={{ py: 3 }}>
        {error && <p style={{ color: "red", textAlign: "center" }}>{error}</p>}
        <Routes>
          <Route
            path="/login"
            element={<LoginPage onLogin={handleLogin} />}
          />
          <Route
            path="/"
            element={
              <HomePage tasks={tasks} onDelete={deleteTask} loading={loading} />
            }
          />
          <Route path="/add" element={<AddTaskPage onAdd={addTask} />} />
          <Route path="/about" element={<AboutPage />} />
        </Routes>
      </Container>
    </ThemeProvider>
  );
}
