import React, { useState, useEffect } from "react";
import axios from "axios";
import MatchCard from "./MatchCard";
import NewsSection from "./NewsSection";

const MatchList = () => {
  const [selectedTab, setSelectedTab] = useState("upcoming");
  const [matches, setMatches] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchMatches = async (param) => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.post(
        `http://localhost:5000/api/cricket-matches/${param}`
      );
      setMatches(response.data.matches || []);
    } catch (err) {
      setError("Failed to fetch matches. Please try again later.");
      console.error("Error fetching matches:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const paramMap = {
      upcoming: "upcoming",
      ongoing: "live",
      recent: "recent",
    };
    fetchMatches(paramMap[selectedTab]);
  }, [selectedTab]);

  const handleTabChange = (tab) => {
    setSelectedTab(tab);
  };

  return (
    <div className="bg-gray-100 min-h-screen p-6 flex justify-center">
      <div className="flex flex-col md:flex-row w-full max-w-full">
        {/* Match List Section */}
        <div className="inline-block p-4 border-r-2 border-gray-300 w-full md:w-3/4">
          <div className="flex flex-col items-start">
            {/* Navbar */}
            <div className="flex flex-wrap space-x-4 mb-4">
              {["upcoming", "ongoing", "recent"].map((tab) => (
                <button
                  key={tab}
                  className={`px-3 py-1 text-xs sm:text-sm font-medium transition-all duration-300 ease-in-out rounded-md border-2 border-red-600 ${
                    selectedTab === tab
                      ? "bg-red-600 text-white border-red-600 scale-105 shadow-md"
                      : "bg-white text-red-600 hover:bg-red-600 hover:text-white"
                  }`}
                  onClick={() => handleTabChange(tab)}
                >
                  {tab.charAt(0).toUpperCase() + tab.slice(1)}
                </button>
              ))}
            </div>
          </div>
          {/* Match Cards */}
          <div className="space-y-4">
            {loading && (
              <p className="text-center text-gray-600">Loading matches...</p>
            )}
            {error && <p className="text-center text-red-500">{error}</p>}
            {!loading && !error && matches.length > 0 ? (
              <div className="max-h-screen overflow-y-auto">
                {matches.map((match, index) => (
                  <MatchCard key={index} match={match} />
                ))}
              </div>
            ) : (
              !loading &&
              !error && (
                <p className="text-center text-gray-600">
                  No matches available.
                </p>
              )
            )}
          </div>
        </div>

        {/* News Section (scrollable) */}
        <div className="w-full md:w-3/5 p-4">
          <h2 className="text-xl font-bold mb-4 text-center text-gray-800">
            Cricket News
          </h2>
          <div className="max-h-screen overflow-y-auto">
            <NewsSection />
          </div>
        </div>
      </div>
    </div>
  );
};

export default MatchList;
