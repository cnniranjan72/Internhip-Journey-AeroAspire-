import axios from "axios";

const API_BASE = "http://localhost:5000/api/v1";

export const api = axios.create({
  baseURL: API_BASE,
  headers: { "Content-Type": "application/json" },
});

// 🔹 Example: login
export async function login(username, password) {
  const res = await api.post("/auth/login", { username, password });
  return res.data.access_token;
}

// 🔹 Example: get all tasks
export async function getTasks(token) {
  const res = await api.get("/tasks", {
    headers: { Authorization: `Bearer ${token}` },
  });
  return res.data;
}

// 🔹 Example: add new task
export async function addTask(task, token) {
  const res = await api.post("/tasks", task, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return res.data;
}
