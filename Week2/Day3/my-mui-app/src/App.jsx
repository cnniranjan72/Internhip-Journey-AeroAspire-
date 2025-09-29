import React, { useState, useEffect } from 'react';
import AppBar from './AppBar';
import HomePage from './HomePage';
import TaskCard from './TaskCard';
import TaskForm from './TaskForm';

export default function App() {
  const [darkMode, setDarkMode] = useState(false);
  const [tasks, setTasks] = useState([]);

  useEffect(() => {
    document.body.className = darkMode ? 'dark-theme' : 'light-theme';
  }, [darkMode]);

  const handleAddTask = (task) => {
    setTasks((prev) => [...prev, task]);
  };

  return (
    <>
      <AppBar />
      <HomePage />
      <button
        onClick={() => setDarkMode((prev) => !prev)}
        style={{ margin: '1rem' }}
      >
        Switch to {darkMode ? 'Light' : 'Dark'} Theme
      </button>

      <TaskForm onAdd={handleAddTask} />
      <TaskCard tasks={tasks} />
    </>
  );
}
