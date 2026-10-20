import React, { useState } from "react";
import Header from "../Header/Header";

export default function Register() {
  const [form, setForm] = useState({ username: "", firstName: "", lastName: "", email: "", password: "" });
  const [error, setError] = useState("");
  const update = (event) => setForm({ ...form, [event.target.name]: event.target.value });

  const submit = async (event) => {
    event.preventDefault();
    setError("");
    const response = await fetch("/djangoapp/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "same-origin",
      body: JSON.stringify({
        userName: form.username,
        firstName: form.firstName,
        lastName: form.lastName,
        email: form.email,
        password: form.password,
      }),
    });
    const result = await response.json();
    if (response.ok) {
      sessionStorage.setItem("username", result.userName);
      sessionStorage.setItem("firstname", form.firstName);
      sessionStorage.setItem("lastname", form.lastName);
      window.location.href = "/dealers";
    } else {
      setError(result.message || "Registration failed.");
    }
  };

  return (
    <div className="site-shell">
      <Header />
      <main className="page">
        <form className="panel form-card" onSubmit={submit}>
          <div className="eyebrow">Join Best Cars</div>
          <h1>Sign-up</h1>
          {error && <div className="error">{error}</div>}
          <div className="field"><label htmlFor="username">Username</label><input id="username" name="username" value={form.username} onChange={update} required /></div>
          <div className="two-col">
            <div className="field"><label htmlFor="firstName">First Name</label><input id="firstName" name="firstName" value={form.firstName} onChange={update} required /></div>
            <div className="field"><label htmlFor="lastName">Last Name</label><input id="lastName" name="lastName" value={form.lastName} onChange={update} required /></div>
          </div>
          <div className="field"><label htmlFor="email">Email</label><input id="email" name="email" type="email" value={form.email} onChange={update} required /></div>
          <div className="field"><label htmlFor="password">Password</label><input id="password" name="password" type="password" value={form.password} onChange={update} required /></div>
          <button className="button" type="submit">Register</button>
        </form>
      </main>
    </div>
  );
}
