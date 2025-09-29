import React from 'react';
import { Typography, Box } from '@mui/material';
import TaskCard from '../components/TaskCard';

export default function HomePage({ tasks = [], onDelete }) {
  return (
    <Box>
      <Box
        sx={{
          p: 3,
          borderRadius: 2,
          bgcolor: 'background.paper',
          boxShadow: 2,
          mb: 3,
        }}
      >
        <Typography variant="h3" component="h1" gutterBottom>
          Niranjan's Task Manager
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Keep track of your day — add tasks, set priority, and manage them quickly. Tasks are saved locally in your browser.
        </Typography>
      </Box>

      <TaskCard tasks={tasks} onDelete={onDelete} />
    </Box>
  );
}
