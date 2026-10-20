import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import Header from "../Header/Header";

export default function PostReview() {
  const { id } = useParams();
  const [dealer, setDealer] = useState(null);
  const [cars, setCars] = useState([]);
  const [form, setForm] = useState({ review: "", purchase_date: "", car: "", car_year: "2024" });
  const update = (event) => setForm({ ...form, [event.target.name]: event.target.value });

  useEffect(() => {
    if (!sessionStorage.getItem("username")) { window.location.href = "/login"; return; }
    fetch(`/djangoapp/dealer/${id}`).then((r) => r.json()).then((r) => setDealer((r.dealer || [])[0]));
    fetch("/djangoapp/get_cars").then((r) => r.json()).then((r) => setCars(r.CarModels || []));
  }, [id]);

  const submit = async (event) => {
    event.preventDefault();
    const selected = cars.find((car) => `${car.CarMake}|${car.CarModel}` === form.car) || {};
    const response = await fetch("/djangoapp/add_review", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "same-origin",
      body: JSON.stringify({
        name: `${sessionStorage.getItem("firstname") || "Talgat"} ${sessionStorage.getItem("lastname") || "Yerkhanuly"}`,
        dealership: Number(id),
        review: form.review,
        purchase: true,
        purchase_date: form.purchase_date,
        car_make: selected.CarMake,
        car_model: selected.CarModel,
        car_year: Number(form.car_year),
      }),
    });
    if (response.ok) window.location.href = `/dealer/${id}`;
  };

  return (
    <div className="site-shell">
      <Header />
      <main className="page">
        <div className="post-layout">
          <aside className="panel dealer-summary">
            <div className="eyebrow">Share your experience</div>
            <h2>{dealer?.full_name || "Dealer"}</h2>
            <p className="lead">Your review helps other drivers choose a dealership with confidence.</p>
          </aside>
          <form className="panel review-form" onSubmit={submit}>
            <h1 style={{ fontSize: "2.6rem" }}>Post Review</h1>
            <div className="field"><label htmlFor="review">Review details</label><textarea id="review" name="review" value={form.review} onChange={update} placeholder="Describe the service, staff, and buying experience" required /></div>
            <div className="field"><label htmlFor="purchase_date">Purchase Date</label><input id="purchase_date" name="purchase_date" type="date" value={form.purchase_date} onChange={update} required /></div>
            <div className="field"><label htmlFor="car">Car Make and Model</label><select id="car" name="car" value={form.car} onChange={update} required><option value="">Choose a vehicle</option>{cars.map((car) => <option key={car.id} value={`${car.CarMake}|${car.CarModel}`}>{car.CarMake} {car.CarModel}</option>)}</select></div>
            <div className="field"><label htmlFor="car_year">Car Year</label><input id="car_year" name="car_year" type="number" min="2015" max="2026" value={form.car_year} onChange={update} required /></div>
            <button className="button" type="submit">Submit Review</button>
          </form>
        </div>
      </main>
    </div>
  );
}
