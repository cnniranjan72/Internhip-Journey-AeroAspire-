import React, { useState } from 'react';
import { TextField, Button, Card, CardContent, Typography } from '@mui/material';

export default function TaskForm({ onAdd }) {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [errors, setErrors] = useState({});

  const validate = () => {
    const newErrors = {};
    if (!title.trim()) newErrors.title = 'Title is required';
    if (title.length < 3) newErrors.title = 'Title must be at least 3 characters';
    if (!description.trim()) newErrors.description = 'Description is required';
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!validate()) return;
    onAdd({ id: Date.now(), title, description });
    setTitle('');
    setDescription('');
  };

  return (
    <Card sx={{ maxWidth: 600, mx: 'auto', mt: 3, p: 2 }}>
      <CardContent>
        <Typography variant="h5" gutterBottom>
          Add Task
        </Typography>
        <form onSubmit={handleSubmit}>
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
          />
          <Button type="submit" variant="contained" fullWidth sx={{ mt: 2 }}>
            Add Task
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}
