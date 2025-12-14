import { useState, useEffect, useCallback } from "react";
import {
  register,
  login,
  getTodos,
  addTodo,
  toggleTodo,
  deleteTodo
} from "./api";

function App() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [token, setToken] = useState(localStorage.getItem("token"));
  const [todos, setTodos] = useState([]);
  const [title, setTitle] = useState("");

  // ---------------- AUTH ----------------

  async function handleRegister() {
    if (!email || !password) {
      alert("Enter email and password");
      return;
    }
    await register(email, password);
    alert("Registered successfully. Now login.");
  }

  async function handleLogin() {
    const data = await login(email, password);
    if (!data.access_token) {
      alert("Invalid credentials");
      return;
    }
    localStorage.setItem("token", data.access_token);
    setToken(data.access_token);
  }

  function handleLogout() {
    localStorage.removeItem("token");
    setToken(null);
    setTodos([]);
  }

  // ---------------- TODOS ----------------

  const loadTodos = useCallback(async () => {
    if (!token) return;
    const data = await getTodos(token);
    setTodos(data);
  }, [token]);

  async function handleAddTodo() {
    if (!title.trim()) return;
    await addTodo(title, token);
    setTitle("");
    loadTodos();
  }

  async function handleToggle(todo) {
    await toggleTodo(todo.id, !todo.completed, token);
    loadTodos();
  }

  async function handleDelete(todoId) {
    await deleteTodo(todoId, token);
    loadTodos();
  }

  // ---------------- EFFECT ----------------

  useEffect(() => {
    loadTodos();
  }, [loadTodos]);

  // ---------------- UI ----------------

  if (!token) {
    return (
      <div style={{ padding: 40 }}>
        <h2>Login / Register</h2>

        <input
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        /><br /><br />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        /><br /><br />

        <button onClick={handleRegister}>Register</button>
        <button onClick={handleLogin} style={{ marginLeft: 10 }}>
          Login
        </button>
      </div>
    );
  }

  return (
    <div style={{ padding: 40 }}>
      <h2>Todo App</h2>

      <input
        placeholder="New todo"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
      />
      <button onClick={handleAddTodo} style={{ marginLeft: 10 }}>
        Add
      </button>

      <ul style={{ marginTop: 20 }}>
        {todos.map((todo) => (
          <li key={todo.id} style={{ marginBottom: 10 }}>
            <input
              type="checkbox"
              checked={todo.completed}
              onChange={() => handleToggle(todo)}
            />
            <span
              style={{
                marginLeft: 8,
                textDecoration: todo.completed ? "line-through" : "none"
              }}
            >
              {todo.title}
            </span>
            <button
              onClick={() => handleDelete(todo.id)}
              style={{ marginLeft: 10 }}
            >
              ❌
            </button>
          </li>
        ))}
      </ul>

      <button onClick={handleLogout}>Logout</button>
    </div>
  );
}

export default App;
