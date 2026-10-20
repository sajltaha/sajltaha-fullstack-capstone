import React, { useEffect, useState } from "react";
import Header from "../Header/Header";

export default function Dealers() {
  const [dealers, setDealers] = useState([]);
  const [states, setStates] = useState([]);
  const [selected, setSelected] = useState("All");
  const loggedIn = Boolean(sessionStorage.getItem("username"));

  const load = async (state = "All") => {
    const endpoint = state === "All" ? "/djangoapp/get_dealers" : `/djangoapp/get_dealers/${encodeURIComponent(state)}`;
    const result = await fetch(endpoint).then((response) => response.json());
    setDealers(result.dealers || []);
    if (state === "All") {
      setStates([...new Set((result.dealers || []).map((dealer) => dealer.state))].sort());
    }
  };

  useEffect(() => { load(); }, []);

  const chooseState = (event) => {
    setSelected(event.target.value);
    load(event.target.value);
  };

  return (
    <div className="site-shell">
      <Header />
      <main className="page">
        <div className="section-title">
          <div><div className="eyebrow">Best Cars network</div><h1>Dealerships</h1></div>
          <p className="lead">{dealers.length} locations shown</p>
        </div>
        {loggedIn && <div className="notice">You are logged in. Use “Review Dealer” to share your experience.</div>}
        <section className="panel">
          <div className="filter-row">
            <label htmlFor="state"><strong>Filter by state</strong></label>
            <select id="state" value={selected} onChange={chooseState} style={{ maxWidth: 280 }}>
              <option value="All">All States</option>
              {states.map((state) => <option key={state} value={state}>{state}</option>)}
            </select>
          </div>
          <table className="dealer-table">
            <thead><tr><th>ID</th><th>Dealer Name</th><th>City</th><th>Address</th><th>State</th>{loggedIn && <th>Review Dealer</th>}</tr></thead>
            <tbody>{dealers.map((dealer) => (
              <tr key={dealer.id}>
                <td>{dealer.id}</td>
                <td><a className="dealer-name" href={`/dealer/${dealer.id}`}>{dealer.full_name}</a></td>
                <td>{dealer.city}</td>
                <td>{dealer.address}, {dealer.zip}</td>
                <td>{dealer.state} ({dealer.st})</td>
                {loggedIn && <td><a className="review-link" href={`/postreview/${dealer.id}`}>Review Dealer →</a></td>}
              </tr>
            ))}</tbody>
          </table>
        </section>
      </main>
    </div>
  );
}
