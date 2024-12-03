import React from "react";

const MatchCard = ({ match }) => {
  return (
    <div className="w-1/5 mx-auto bg-white shadow-lg rounded-lg border border-gray-200">
      {/* Match Info */}
      <div className="px-4 py-2 bg-gray-100 flex justify-between items-center rounded-t-lg">
        <span className="text-sm font-semibold text-gray-600">{match.type}</span>
        <span
          className={`text-xs font-semibold px-2 py-1 rounded ${
            match.status === "Live"
              ? "bg-red-500 text-white"
              : "bg-green-500 text-white"
          }`}
        >
          {match.status}
        </span>
      </div>

      {/* Teams */}
      <div className="flex justify-between items-center px-4 py-4">
        {/* Team 1 */}
        <div className="flex flex-col items-center">
          {/* <img
            src={match.team1.logo}
            alt={match.team1.name}
            className="w-12 h-12"
          /> */}
          <span className="text-sm mt-2 font-medium text-gray-800">
            {match.team1.name}
          </span>
        </div>
        <span className="text-xl font-bold text-gray-600">vs</span>
        {/* Team 2 */}
        <div className="flex flex-col items-center">
          {/* <img
            src={match.team2.logo}
            alt={match.team2.name}
            className="w-12 h-12"
          /> */}
          <span className="text-sm mt-2 font-medium text-gray-800">
            {match.team2.name}
          </span>
        </div>
      </div>

      {/* Match Details */}
      <div className="px-4 py-3 bg-gray-50 rounded-b-lg">
        <p className="text-sm text-gray-600">
          <span className="font-semibold">Date:</span> {match.date}
        </p>
        <p className="text-sm text-gray-600">
          <span className="font-semibold">Time:</span> {match.time}
        </p>
        <p className="text-sm text-gray-600">
          <span className="font-semibold">Venue:</span> {match.venue}
        </p>
      </div>
    </div>
  );
};

export default MatchCard;
