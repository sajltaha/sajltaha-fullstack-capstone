import React from "react";

export default function Header() {
  const username = sessionStorage.getItem("username") || "";

  const handleLogout = async (event) => {
    event.preventDefault();
    await fetch("/djangoapp/logout", { method: "GET", credentials: "same-origin" });
    sessionStorage.clear();
    window.location.href = "/";
  };

  return (
    <header className="site-header">
      <a className="brand" href="/">Best Cars</a>
      <nav className="nav-links" aria-label="Primary navigation">
        <a href="/">Home</a>
        <a href="/dealers">Dealers</a>
        <a href="/about/">About Us</a>
        <a href="/contact/">Contact Us</a>
      </nav>
      <div className="auth-links">
        {username ? (
          <>
            <span className="username-pill">Signed in as {username}</span>
            <button className="link-button" onClick={handleLogout}>Logout</button>
          </>
        ) : (
          <>
            <a href="/login">Login</a>
            <a href="/register">Register</a>
          </>
        )}
      </div>
    </header>
  );
}
