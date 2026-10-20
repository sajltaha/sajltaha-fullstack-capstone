import React, { useState } from "react";
import Header from "../Header/Header";

export default function Login() {
  const [userName, setUserName] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const submit = async (event) => {
    event.preventDefault();
    setError("");
    const response = await fetch("/djangoapp/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "same-origin",
      body: JSON.stringify({ userName, password }),
    });
    const result = await response.json();
    if (response.ok && result.status === "Authenticated") {
      sessionStorage.setItem("username", result.userName);
      sessionStorage.setItem("firstname", result.firstName || "");
      sessionStorage.setItem("lastname", result.lastName || "");
      window.location.href = "/dealers";
    } else {
      setError("The username or password is incorrect.");
    }
  };

  return (
    <div className="site-shell">
      <Header />
      <main className="page">
        <form className="panel form-card" onSubmit={submit}>
          <div className="eyebrow">Welcome back</div>
          <h1>Login</h1>
          {error && <div className="error">{error}</div>}
          <div className="field"><label htmlFor="username">Username</label><input id="username" value={userName} onChange={(e) => setUserName(e.target.value)} required /></div>
          <div className="field"><label htmlFor="password">Password</label><input id="password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} required /></div>
          <button className="button" type="submit">Login</button>
          <p className="lead">New here? <a href="/register">Create an account</a>.</p>
        </form>
      </main>
    </div>
  );
}
