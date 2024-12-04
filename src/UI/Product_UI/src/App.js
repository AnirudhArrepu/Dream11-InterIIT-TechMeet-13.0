import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Layout from "./components/Layout"; // Adjust the path
import Home from "./components/Home"; // Adjust the path
import MatchList from "./components/MatchList"; // Adjust the path
import Support from "./components/Support"; // Adjust the path
import About from "./components/About"; // Adjust the path
import Signup from "./components/SignUp";
import Login from "./components/Login";

const App = () => {
  return (
    <Router>
      <Routes>
        {/* Parent Route with Layout */}
        <Route path="/" element={<Layout />}>
          {/* Child Routes */}
          <Route index element={<Home />} /> {/* Default route */}
          <Route path="matches" element={<MatchList />} />
          <Route path="support" element={<Support />} />
          <Route path="about" element={<About />} />
          <Route path="signup" element={<Signup />} />
          <Route path="login" element={<Login />} />
        </Route>
      </Routes>
    </Router>
  );
};

export default App;
