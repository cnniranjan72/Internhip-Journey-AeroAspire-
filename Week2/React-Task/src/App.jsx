import React, { useEffect, useMemo, useState } from "react";
import { Routes, Route, useNavigate } from "react-router-dom";
import { ThemeProvider, CssBaseline, Container } from "@mui/material";
import HomePage from "./pages/HomePage";
import AddTaskPage from "./pages/AddTaskPage";
import AboutPage from "./pages/AboutPage";
import NavBar from "./components/NavBar";
import themeBuilder from "./theme";

// ✅ Base URL should point to the version root, not directly to /tasks
const API_BASE = "http://localhost:5000/api/v1";

export default function App() {
  const navigate = useNavigate();

  const [tasks, setTasks] = useState([]);
  const [mode, setMode] = useState("light");
  const [loading, setLoading] = useState(false);

  const theme = useMemo(() => themeBuilder(mode), [mode]);

  // ✅ Fetch all tasks
  useEffect(() => {
    const fetchTasks = async () => {
      setLoading(true);
      try {
        const res = await fetch(`${API_BASE}/tasks`);
        if (!res.ok) throw new Error("Failed to fetch tasks");
        const data = await res.json();
        setTasks(data);
      } catch (err) {
        console.error("Error fetching tasks:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchTasks();
  }, []);

  // ✅ Add new task
  const addTask = async (taskPayload) => {
    try {
      const res = await fetch(`${API_BASE}/tasks`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
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
      console.error("Error adding task:", err);
    }
  };

  // ✅ Delete task
  const deleteTask = async (id) => {
    try {
      const res = await fetch(`${API_BASE}/tasks/${id}`, {
        method: "DELETE",
      });
      if (res.ok) {
        setTasks((prev) => prev.filter((t) => t.id !== id));
      } else {
        console.error("Failed to delete task");
      }
    } catch (err) {
      console.error("Error deleting task:", err);
    }
  };

  // ✅ Toggle theme
  const toggleTheme = () =>
    setMode((m) => (m === "light" ? "dark" : "light"));

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <NavBar mode={mode} onToggleTheme={toggleTheme} />
      <Container maxWidth="md" sx={{ py: 3 }}>
        <Routes>
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
