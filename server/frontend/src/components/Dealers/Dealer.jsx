import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import Header from "../Header/Header";

export default function Dealer() {
  const { id } = useParams();
  const [dealer, setDealer] = useState(null);
  const [reviews, setReviews] = useState([]);
  const loggedIn = Boolean(sessionStorage.getItem("username"));

  useEffect(() => {
    Promise.all([
      fetch(`/djangoapp/dealer/${id}`).then((response) => response.json()),
      fetch(`/djangoapp/reviews/dealer/${id}`).then((response) => response.json()),
    ]).then(([dealerResult, reviewResult]) => {
      setDealer((dealerResult.dealer || [])[0] || null);
      setReviews(reviewResult.reviews || []);
    });
  }, [id]);

  return (
    <div className="site-shell">
      <Header />
      <main className="page">
        <section className="panel dealer-heading">
          <div className="eyebrow">Dealer #{id}</div>
          <h1>{dealer ? dealer.full_name : "Loading dealer…"}</h1>
          {dealer && <p className="lead">{dealer.address}, {dealer.city}, {dealer.state} {dealer.zip}</p>}
          {loggedIn && <a className="button" href={`/postreview/${id}`}>Post Review</a>}
        </section>
        <div className="section-title" style={{ marginTop: 34 }}><h2>Customer reviews</h2><span className="lead">{reviews.length} reviews</span></div>
        <section className="review-grid">
          {reviews.length ? reviews.map((review) => (
            <article className="review-card" key={review.id}>
              <span className="sentiment">{review.sentiment}</span>
              <div>{review.review}</div>
              <div className="reviewer"><strong>{review.name}</strong><br />{review.car_year} {review.car_make} {review.car_model}</div>
            </article>
          )) : <article className="review-card">No reviews have been posted yet.</article>}
        </section>
      </main>
    </div>
  );
}
