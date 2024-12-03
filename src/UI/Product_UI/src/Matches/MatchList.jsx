import React, { useState } from "react";
import MatchCard from "./MatchCard";

// Example match data
const matchesData = {
  upcoming: [
    {
      type: "T20",
      status: "Upcoming",
      team1: { name: "Team A" },
      team2: { name: "Team B" },
      date: "2024-12-10",
      time: "19:00",
      venue: "Stadium 1",
    },
    {
      type: "T20",
      status: "Upcoming",
      team1: { name: "Team C" },
      team2: { name: "Team D" },
      date: "2024-12-12",
      time: "20:00",
      venue: "Stadium 2",
    },
  ],
  ongoing: [
    {
      type: "T20",
      status: "Live",
      team1: { name: "Team E" },
      team2: { name: "Team F" },
      date: "2024-12-02",
      time: "15:00",
      venue: "Stadium 3",
    },
  ],
  past: [
    {
      type: "T20",
      status: "Completed",
      team1: { name: "Team G" },
      team2: { name: "Team H" },
      date: "2024-11-29",
      time: "18:00",
      venue: "Stadium 4",
    },
  ],
};

const MatchList = () => {
  const [selectedTab, setSelectedTab] = useState("upcoming"); // Default is 'upcoming'

  const handleTabChange = (tab) => {
    setSelectedTab(tab);
  };

  return (
    <div className="bg-gray-100 min-h-screen p-6 flex flex-col items-center">
      {/* Navbar */}
      <div className="flex space-x-6 mb-6"> {/* space-x-6 adds horizontal spacing */}
        <button
          className={`px-6 py-3 text-lg font-semibold transition-all duration-300 ease-in-out transform rounded-lg border-2 border-red-600 ${
            selectedTab === "upcoming"
              ? "bg-red-600 text-white border-red-600 scale-105 shadow-lg"
              : "bg-white text-red-600 hover:bg-red-600 hover:text-white"
          }`}
          onClick={() => handleTabChange("upcoming")}
        >
          Upcoming Matches
        </button>
        <button
          className={`px-6 py-3 text-lg font-semibold transition-all duration-300 ease-in-out transform rounded-lg border-2 border-red-600 ${
            selectedTab === "ongoing"
              ? "bg-red-600 text-white border-red-600 scale-105 shadow-lg"
              : "bg-white text-red-600 hover:bg-red-600 hover:text-white"
          }`}
          onClick={() => handleTabChange("ongoing")}
        >
          Ongoing Matches
        </button>
        <button
          className={`px-6 py-3 text-lg font-semibold transition-all duration-300 ease-in-out transform rounded-lg border-2 border-red-600 ${
            selectedTab === "past"
              ? "bg-red-600 text-white border-red-600 scale-105 shadow-lg"
              : "bg-white text-red-600 hover:bg-red-600 hover:text-white"
          }`}
          onClick={() => handleTabChange("past")}
        >
          Past Matches
        </button>
      </div>

      {/* Match Cards */}
      <div className="w-full mt-6">
        {matchesData[selectedTab].map((match, index) => (
          <div className="mb-6" key={index}>
            <MatchCard match={match} />
          </div>
        ))}
      </div>
    </div>
  );
};

export default MatchList;
