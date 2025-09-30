import React, { useState } from 'react';
import {
  Typography,
  Box,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Stack,
  Button,
} from '@mui/material';
import TaskCard from '../components/TaskCard';

export default function HomePage({ tasks = [], onDelete }) {
  const [search, setSearch] = useState('');
  const [priorityFilter, setPriorityFilter] = useState('');

  // Filter tasks
  const filteredTasks = tasks
    .filter(
      (t) =>
        t.title.toLowerCase().includes(search.toLowerCase()) ||
        t.description.toLowerCase().includes(search.toLowerCase())
    )
    .filter((t) => !priorityFilter || t.priority === Number(priorityFilter));

  return (
    <Box>
      {/* Header */}
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
          Keep track of your daily tasks. So that you don't forget them!
        </Typography>
      </Box>

      {/* 🔎 Search + Filter Controls */}
      <Stack
        direction={{ xs: 'column', sm: 'row' }}
        spacing={2}
        sx={{ mb: 3 }}
        alignItems="center"
      >
        {/* Search */}
        <TextField
          label="Search tasks"
          variant="outlined"
          size="small"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          fullWidth
        />

        {/* Priority Filter */}
        <FormControl size="small" sx={{ minWidth: 140 }}>
          <InputLabel>Priority</InputLabel>
          <Select
            value={priorityFilter}
            onChange={(e) => setPriorityFilter(e.target.value)}
            label="Priority"
          >
            <MenuItem value="">All</MenuItem>
            <MenuItem value={1}>P1</MenuItem>
            <MenuItem value={2}>P2</MenuItem>
            <MenuItem value={3}>P3</MenuItem>
            <MenuItem value={4}>P4</MenuItem>
            <MenuItem value={5}>P5</MenuItem>
          </Select>
        </FormControl>

        {/* Clear Button */}
        <Button
          variant="outlined"
          color="secondary"
          onClick={() => {
            setSearch('');
            setPriorityFilter('');
          }}
        >
          Clear
        </Button>
      </Stack>

      {/* Task List */}
      <TaskCard tasks={filteredTasks} onDelete={onDelete} />
    </Box>
  );
}
