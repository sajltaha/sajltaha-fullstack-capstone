import { Route, Routes } from "react-router-dom";
import "./App.css";
import Dealer from "./components/Dealers/Dealer";
import Dealers from "./components/Dealers/Dealers";
import PostReview from "./components/Dealers/PostReview";
import Home from "./components/Home/Home";
import Login from "./components/Login/Login";
import Register from "./components/Register/Register";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="/dealers" element={<Dealers />} />
      <Route path="/dealer/:id" element={<Dealer />} />
      <Route path="/postreview/:id" element={<PostReview />} />
    </Routes>
  );
}

export default App;
