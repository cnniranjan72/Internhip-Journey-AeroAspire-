import React, { useEffect, useMemo, useState } from 'react';
import { Routes, Route, useNavigate } from 'react-router-dom';
import { ThemeProvider, CssBaseline, Container } from '@mui/material';
import HomePage from './pages/HomePage';
import AddTaskPage from './pages/AddTaskPage';
import AboutPage from './pages/AboutPage';
import NavBar from './components/NavBar';
import themeBuilder from './theme';
import { loadFromStorage, saveToStorage } from './utils/storage';

const TASKS_KEY = 'my_task_manager_tasks_v1';
const THEME_KEY = 'my_task_manager_theme_v1';

export default function App() {
  const navigate = useNavigate();

  const [tasks, setTasks] = useState([]);
  const [mode, setMode] = useState(() => loadFromStorage(THEME_KEY) || 'light');

  // Build MUI theme (memoized)
  const theme = useMemo(() => themeBuilder(mode), [mode]);

  // load tasks from localStorage once on mount
  useEffect(() => {
    const saved = loadFromStorage(TASKS_KEY);
    if (saved && Array.isArray(saved)) setTasks(saved);
  }, []);

  // persist tasks whenever they change
  useEffect(() => {
    saveToStorage(TASKS_KEY, tasks);
  }, [tasks]);

  // persist theme
  useEffect(() => {
    saveToStorage(THEME_KEY, mode);
  }, [mode]);

  const addTask = (taskPayload) => {
    const newTask = {
      id: Date.now(),
      title: taskPayload.title.trim(),
      description: taskPayload.description.trim(),
      priority: Number(taskPayload.priority) || 1,
      createdAt: new Date().toISOString(),
    };
    setTasks((prev) => [newTask, ...prev]);
    // navigate to home to show the new task
    navigate('/');
  };

  const deleteTask = (id) => {
    setTasks((prev) => prev.filter((t) => t.id !== id));
  };

  const toggleTheme = () => setMode((m) => (m === 'light' ? 'dark' : 'light'));

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <NavBar mode={mode} onToggleTheme={toggleTheme} />
      <Container maxWidth="md" sx={{ py: 3 }}>
        <Routes>
          <Route path="/" element={<HomePage tasks={tasks} onDelete={deleteTask} />} />
          <Route path="/add" element={<AddTaskPage onAdd={addTask} />} />
          <Route path="/about" element={<AboutPage />} />
        </Routes>
      </Container>
    </ThemeProvider>
  );
}
