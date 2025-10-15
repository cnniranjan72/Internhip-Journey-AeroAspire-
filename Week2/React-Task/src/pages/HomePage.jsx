import React, { useState, useEffect } from "react";
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
  CircularProgress,
} from "@mui/material";
import TaskCard from "../components/TaskCard";

const API_BASE = "http://localhost:5000/api/v1";

export default function HomePage({ onDelete }) {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [search, setSearch] = useState("");
  const [statusFilter, setStatusFilter] = useState("");
  const [page, setPage] = useState(1);

  // ✅ Fetch tasks with filters & pagination
  useEffect(() => {
    const fetchTasks = async () => {
      setLoading(true);
      try {
        const params = new URLSearchParams();
        if (search) params.append("search", search);
        if (statusFilter) params.append("status", statusFilter);
        params.append("page", page);

        const res = await fetch(`${API_BASE}/tasks?${params.toString()}`);
        if (!res.ok) throw new Error("Failed to fetch tasks");
        const data = await res.json();
        setTasks(data.items || []); // ✅ backend returns { items: [] }
      } catch (err) {
        console.error("Error fetching tasks:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchTasks();
  }, [search, statusFilter, page]);

  return (
    <Box>
      {/* Header */}
      <Box
        sx={{
          p: 3,
          borderRadius: 2,
          bgcolor: "background.paper",
          boxShadow: 2,
          mb: 3,
        }}
      >
        <Typography variant="h3" component="h1" gutterBottom>
          Niranjan’s Task Manager
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Keep track of your daily tasks with smart filters and search!
        </Typography>
      </Box>

      {/* Filters */}
      <Stack
        direction={{ xs: "column", sm: "row" }}
        spacing={2}
        sx={{ mb: 3 }}
        alignItems="center"
      >
        <TextField
          label="Search tasks"
          variant="outlined"
          size="small"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          fullWidth
        />

        <FormControl size="small" sx={{ minWidth: 140 }}>
          <InputLabel>Status</InputLabel>
          <Select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            label="Status"
          >
            <MenuItem value="">All</MenuItem>
            <MenuItem value="pending">Pending</MenuItem>
            <MenuItem value="completed">Completed</MenuItem>
          </Select>
        </FormControl>

        <Button
          variant="outlined"
          color="secondary"
          onClick={() => {
            setSearch("");
            setStatusFilter("");
          }}
        >
          Clear
        </Button>
      </Stack>

      {/* Loading State */}
      {loading ? (
        <Box textAlign="center" sx={{ mt: 5 }}>
          <CircularProgress />
        </Box>
      ) : (
        <TaskCard tasks={tasks} onDelete={onDelete} />
      )}
    </Box>
  );
}
