import React, { useState, useEffect } from 'react';
import AppBar from './AppBar';
import HomePage from './HomePage';
import TaskCard from './TaskCard';

const dummyTasks = [
  { id: 1, title: 'Read React Docs', description: 'Study the official documentation.' },
  { id: 2, title: 'Build TaskCard', description: 'Create a component to display tasks.' },
  { id: 3, title: 'Test Component', description: 'Render TaskCard with dummy tasks.' },
];

export default function App() {
  const [darkMode, setDarkMode] = useState(false);

  useEffect(() => {
    document.body.className = darkMode ? 'dark-theme' : 'light-theme';
  }, [darkMode]);

  return (
    <>
      <AppBar />
      <HomePage />
      <button onClick={() => setDarkMode(prev => !prev)} style={{ margin: '1rem' }}>
        Switch to {darkMode ? 'Light' : 'Dark'} Theme
      </button>
      <TaskCard tasks={dummyTasks} darkMode={darkMode} />
    </>
  );
}
