import React, { useState, useEffect, useCallback } from "react";
import axios from "axios";
import MatchCard from "./MatchCard";
import NewsSection from "./NewsSection";
import PopCard from "./PopCard";

const MatchList = () => {
  const [selectedTab, setSelectedTab] = useState("upcoming");
  const [matches, setMatches] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showModal, setShowModal] = useState(false); // Modal visibility state
  const [selectedMatch, setSelectedMatch] = useState(null); // Selected match for the modal
  const [teams, setTeams] = useState(null);

  // Handle match card click
  const handleMatchClick = async (match) => {
    setSelectedMatch(match);
    const response = await axios.get(`http://localhost:5000/api/cricket-matches/${match.matchid}/players`);
    // console.log(response);
    setTeams(response.data);
    setShowModal(true);
  };

  // Close modal
  const closeModal = () => {
    setShowModal(false);
    setSelectedMatch(null);
  };

  const fetchMatches = useCallback(async (param) => {
    setLoading(true);
    setError(null);
  
    try {
      const response = await axios.post(
        `http://localhost:5000/api/cricket-matches/${param}`
      );
      const fetchedMatches = response.data.matches || [];
  
      // Store matches and timestamp in localStorage
      localStorage.setItem(
        `matches_${param}`,
        JSON.stringify({ timestamp: Date.now(), matches: fetchedMatches })
      );
  
      setMatches(fetchedMatches);
    } catch (err) {
      setError("Failed to fetch matches. Please try again later.");
      console.error("Error fetching matches:", err);
    } finally {
      setLoading(false);
    }
  }, []); // No dependencies for `fetchMatches`
  
  const checkAndFetchMatches = useCallback(
    (param) => {
      const cachedData = localStorage.getItem(`matches_${param}`);
  
      if (cachedData) {
        const { timestamp, matches } = JSON.parse(cachedData);
        const oneHour = 60 * 60 * 1000;
  
        // If less than an hour has passed, use cached data
        if (Date.now() - timestamp < oneHour) {
          setMatches(matches);
          return;
        }
      }
  
      // Fetch fresh data if no cache or cache expired
      fetchMatches(param);
    },
    [fetchMatches] // `fetchMatches` is now stable
  );
  
  useEffect(() => {
    const paramMap = {
      upcoming: "upcoming",
      ongoing: "live",
      recent: "recent",
    };
  
    checkAndFetchMatches(paramMap[selectedTab]);
  }, [checkAndFetchMatches, selectedTab]);
  
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
                  <div key={index} onClick={() => handleMatchClick(match)}>
                    <MatchCard match={match} />
                  </div>
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

        {/* Modal */}
      {showModal && (
        <PopCard match={selectedMatch} teams={teams} onClose={closeModal} />
      )}
      </div>
    </div>
  );
};

export default MatchList;
