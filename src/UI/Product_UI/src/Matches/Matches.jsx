import React from "react";
import Header from "../Home/Header";
import Footer from "../Home/Footer";
import MatchList from "./MatchList";

const Matches = () => {
  return (
      <div>
        <Header />
        <MatchList />
        <Footer />  
      </div>
  );
};

export default Matches;
