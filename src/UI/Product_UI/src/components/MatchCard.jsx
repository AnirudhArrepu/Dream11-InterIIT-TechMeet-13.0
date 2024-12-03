import React from "react";

const MatchCard = ({ match }) => {
  return (
    <div className="w-full mx-auto my-4 bg-white shadow-lg rounded-lg border border-gray-200 hover:shadow-2xl transition-shadow duration-300 ease-in-out">
      {/* Match Info */}
      <div className="px-4 py-2 bg-gradient-to-r from-red-500 to-red-700 text-white flex justify-between items-center rounded-t-lg">
        <span className="text-sm font-semibold">{match.matchFormat}</span>
        <span
          className={`text-xs font-semibold px-2 py-1 rounded ${
            match.status === "In Progress"
              ? "bg-green-500 text-white"
              : "bg-gray-700 text-white"
          }`}
        >
          {match.state}
        </span>
      </div>

      {/* Teams */}
      <div className="flex justify-between items-center px-4 py-6">
        {/* Team 1 */}
        <div className="flex flex-col items-center">
          <span className="text-lg font-bold text-gray-800">
            {match.team1}
          </span>
          {/* <span className="text-sm text-gray-500">({match.team1.score})</span> */}
        </div>
        <span className="text-xl font-extrabold text-red-600">vs</span>
        {/* Team 2 */}
        <div className="flex flex-col items-center">
          <span className="text-lg font-bold text-gray-800">
            {match.team2}
          </span>
          {/* <span className="text-sm text-gray-500">({match.team2.score})</span> */}
        </div>
      </div>

      {/* Match Details */}
      <div className="px-4 py-4 bg-gray-50 rounded-b-lg">
        <div className="flex justify-between items-center mb-3">
          <p className="text-sm text-gray-600">
            <span className="font-semibold">Status:</span>{" "}
            <span
              className={`font-bold ${
                match.state === "In Progress"
                  ? "text-green-500"
                  : "text-gray-500"
              }`}
            >
              {match.status}
            </span>
          </p>
        </div>
        <p className="text-sm text-gray-600">
          <span className="font-semibold">Date:</span> {match.date}
        </p>
        <p className="text-sm text-gray-600">
          <span className="font-semibold">Time:</span> {match.time}
        </p>
        <p className="text-sm text-gray-600">
          <span className="font-semibold">Venue:</span> {match.stadium}
        </p>
      </div>
    </div>
  );
};

export default MatchCard;
