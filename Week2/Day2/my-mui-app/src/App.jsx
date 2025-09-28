// src/App.js
import React from 'react';
import AppBar from './AppBar';
import HomePage from './HomePage';
import TaskCard from './TaskCard';

const dummyTasks = [
  { id: 1, title: 'Read React Docs', description: 'Study the official documentation.' },
  { id: 2, title: 'Build TaskCard', description: 'Create a component to display tasks.' },
  { id: 3, title: 'Attend Team Meeting', description: 'Catch up for the daily team meeting.' },
  { id: 4, title: 'Document Code', description: 'Prepare for the task documentation.' }
];

function App() {
  return (
    <>
      <AppBar />
      <HomePage />
      <TaskCard tasks={dummyTasks} />
    </>
  );
}

export default App;
