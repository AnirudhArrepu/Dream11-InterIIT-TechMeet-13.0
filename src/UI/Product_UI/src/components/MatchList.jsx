import React, { useState, useEffect, useCallback } from "react";
import axios from "axios";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faFilter } from "@fortawesome/free-solid-svg-icons";
import MatchCard from "./MatchCard";
import NewsSection from "./NewsSection";
import PopCard from "./PopCard";

const MatchList = () => {
  const [selectedTab, setSelectedTab] = useState("upcoming");
  const [matches, setMatches] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [selectedMatch, setSelectedMatch] = useState(null);
  const [teams, setTeams] = useState(null);
  const [filterOption, setFilterOption] = useState("All");
  const [showDropdown, setShowDropdown] = useState(false); // State for dropdown visibility

  const handleMatchClick = useCallback(async (match) => {
    setSelectedMatch(match);
    try {
      const response = await axios.get(
        `http://localhost:5000/api/cricket-matches/${match.matchid}/players`
      );
      setTeams(response.data);
      setShowModal(true);
    } catch (error) {
      console.error("Error fetching match players:", error);
      setError("Failed to fetch players. Please try again later.");
    }
  }, []);

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
  }, []);

  const checkAndFetchMatches = useCallback(
    (param) => {
      const cachedData = localStorage.getItem(`matches_${param}`);
      if (cachedData) {
        const { timestamp, matches } = JSON.parse(cachedData);
        const oneHour = 30 * 60 * 1000;
        if (Date.now() - timestamp < oneHour) {
          setMatches(matches);
          return;
        }
      }
      fetchMatches(param);
    },
    [fetchMatches]
  );

  useEffect(() => {
    const paramMap = {
      upcoming: "upcoming",
      ongoing: "live",
      recent: "recent",
    };
    checkAndFetchMatches(paramMap[selectedTab]);
  }, [checkAndFetchMatches, selectedTab]);

  const filteredMatches = matches.filter((match) => {
    return filterOption === "All" || match.matchFormat === filterOption;
  });

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
            <div className="flex flex-wrap justify-between mb-4 w-full">
              <div className="flex space-x-4">
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

              {/* Filter Dropdown */}
              <div className="relative">
                <button
                  className="p-2 rounded-full border-2 border-red-600 bg-white text-red-600 hover:bg-red-600 hover:text-white transition-all duration-300"
                  onClick={() => setShowDropdown((prev) => !prev)}
                >
                  <FontAwesomeIcon icon={faFilter} />
                </button>
                {showDropdown && (
                  <div className="absolute right-0 mt-2 w-36 bg-white border border-gray-300 rounded-md shadow-lg z-10">
                    {["All", "T20", "ODI", "TEST"].map((option) => (
                      <div
                        key={option}
                        onClick={() => {
                          setFilterOption(option);
                          setShowDropdown(false); // Close dropdown after selection
                        }}
                        className={`p-2 text-sm text-gray-800 cursor-pointer hover:bg-gray-100 ${
                          filterOption === option ? "bg-gray-200 font-semibold" : ""
                        }`}
                      >
                        {option}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Match Cards */}
          <div className="space-y-4">
            {loading && (
              <p className="text-center text-gray-600">Loading matches...</p>
            )}
            {error && <p className="text-center text-red-500">{error}</p>}
            {!loading && !error && filteredMatches.length > 0 ? (
              <div className="max-h-screen overflow-y-auto">
                {filteredMatches.map((match, index) => (
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

        {/* News Section */}
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
