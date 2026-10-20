import React from "react";
import Header from "../Header/Header";

export default function Home() {
  return (
    <div className="site-shell">
      <Header />
      <main className="page">
        <section className="hero">
          <div className="hero-copy">
            <div className="eyebrow">Trusted dealerships nationwide</div>
            <h1>Find a dealer you can trust.</h1>
            <p>Compare verified car dealerships, read customer reviews, and share your own buying experience through one simple portal.</p>
            <div className="actions">
              <a className="button" href="/dealers">Browse dealerships</a>
              <a className="button secondary" href="/about/">Meet our team</a>
            </div>
          </div>
          <div className="hero-image" role="img" aria-label="Cars in a modern showroom" />
        </section>
      </main>
    </div>
  );
}
