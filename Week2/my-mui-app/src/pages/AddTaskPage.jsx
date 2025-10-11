import React, { useState } from 'react';
import {
  Card,
  CardContent,
  Typography,
  TextField,
  Button,
  Box,
  Alert,
} from '@mui/material';

export default function AddTaskPage({ onAdd }) {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [priority, setPriority] = useState('3');
  const [errors, setErrors] = useState({});
  const [success, setSuccess] = useState('');

  const validate = () => {
    const errs = {};
    if (!title.trim()) errs.title = 'Title is required';
    else if (title.trim().length < 3) errs.title = 'Title must be at least 3 characters';

    if (!description.trim()) errs.description = 'Description is required';
    else if (description.trim().length < 5) errs.description = 'Description must be at least 5 characters';

    if (priority === '' || isNaN(Number(priority))) errs.priority = 'Priority is required';
    else {
      const p = Number(priority);
      if (!Number.isInteger(p) || p < 1 || p > 5) errs.priority = 'Priority must be an integer 1–5';
    }

    setErrors(errs);
    return Object.keys(errs).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setSuccess('');
    if (!validate()) return;
    onAdd({ title, description, priority: Number(priority) });
    setTitle('');
    setDescription('');
    setPriority('3');
    setSuccess('Task added successfully!');
    setTimeout(() => setSuccess(''), 2500);
  };

  return (
    <Card>
      <CardContent>
        <Typography variant="h5" gutterBottom>
          Add New Task
        </Typography>

        {success && <Alert severity="success" sx={{ mb: 2 }}>{success}</Alert>}

        <Box component="form" onSubmit={handleSubmit} noValidate>
          <TextField
            label="Title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            error={!!errors.title}
            helperText={errors.title}
            fullWidth
            margin="normal"
          />

          <TextField
            label="Description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            error={!!errors.description}
            helperText={errors.description}
            fullWidth
            margin="normal"
            multiline
            rows={3}
          />

          <TextField
            label="Priority (1 - 5)"
            value={priority}
            onChange={(e) => setPriority(e.target.value)}
            error={!!errors.priority}
            helperText={errors.priority || '1 = lowest, 5 = highest'}
            type="number"
            inputProps={{ min: 1, max: 5 }}
            margin="normal"
            sx={{ width: 160 }}
          />

          <Button type="submit" variant="contained" sx={{ mt: 2 }}>
            Add Task
          </Button>
        </Box>
      </CardContent>
    </Card>
  );
}
