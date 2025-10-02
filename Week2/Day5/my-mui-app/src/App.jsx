import React, { useEffect, useMemo, useState } from "react";
import { Routes, Route, useNavigate } from "react-router-dom";
import { ThemeProvider, CssBaseline, Container } from "@mui/material";
import HomePage from "./pages/HomePage";
import AddTaskPage from "./pages/AddTaskPage";
import AboutPage from "./pages/AboutPage";
import NavBar from "./components/NavBar";
import themeBuilder from "./theme";

const API_URL = "http://127.0.0.1:5000"; 

export default function App() {
  const navigate = useNavigate();

  const [tasks, setTasks] = useState([]);
  const [mode, setMode] = useState("light");
  const [loading, setLoading] = useState(false);

  const theme = useMemo(() => themeBuilder(mode), [mode]);


  useEffect(() => {
    const fetchTasks = async () => {
      setLoading(true);
      try {
        const res = await fetch(`${API_URL}/tasks`);
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

  const addTask = async (taskPayload) => {
    try {
      const res = await fetch(`${API_URL}/tasks`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          title: taskPayload.title.trim(),
          description: taskPayload.description.trim(),
        }),
      });

      if (!res.ok) throw new Error("Failed to add task");
      const newTask = await res.json();
      setTasks((prev) => [newTask, ...prev]);
      navigate("/");
    } catch (err) {
      console.error(err);
    }
  };

  const deleteTask = async (id) => {
    try {
      const res = await fetch(`${API_URL}/tasks/${id}`, {
        method: "DELETE",
      });
      if (res.ok) {
        setTasks((prev) => prev.filter((t) => t.id !== id));
      } else {
        console.error("Failed to delete task");
      }
    } catch (err) {
      console.error(err);
    }
  };

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
