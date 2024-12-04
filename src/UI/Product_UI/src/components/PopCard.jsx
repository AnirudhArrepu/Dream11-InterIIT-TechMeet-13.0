import React, { useState } from "react";
import axios from "axios";
import BeatLoader from "react-spinners/BeatLoader";
import Best11Display from "./Best11";

const PopCard = ({ match, teams, onClose }) => {
  const [prediction, setPrediction] = useState(null); // State for prediction data
  const [loading, setLoading] = useState(false); // State to manage loader

  // Check if squads are available
  const squad_avail = teams.team1.length > 0 && teams.team2.length > 0;

  const handlePredict = async () => {
    try {
      setLoading(true); // Show loader
      setPrediction(null); // Reset predictions

      const response = await axios.post("http://localhost:5000/app/model/predict", {
        match,
        teams,
      });

      if (response.status === 200) {
        setPrediction(response.data.predictions); // Set prediction data to state
      } else {
        console.error("Failed to fetch predictions");
      }
    } catch (error) {
      console.error("Error:", error.message);
    } finally {
      setLoading(false); // Hide loader
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-70 z-50">
      <div className="bg-white w-full h-full p-6 overflow-auto rounded-lg shadow-xl">
        {/* Modal Header */}
        <div className="flex justify-between items-center border-b pb-4">
          <h2 className="text-3xl font-extrabold text-red-600">{`${match.team1} vs ${match.team2}`}</h2>
          <button
            onClick={onClose}
            className="text-black hover:text-red-600 text-3xl font-bold transition-all duration-200"
          >
            &times;
          </button>
        </div>

        {/* Modal Content */}
        {squad_avail ? (
          <>
            <div className="flex justify-center mt-6">
              <div className="grid grid-cols-2 gap-6 w-[70%] mx-auto">
                {/* Team 1 Players */}
                <div className="bg-gray-100 p-4 rounded-xl shadow-md">
                  <h3 className="text-xl font-semibold text-black mb-3">{match.team1}</h3>
                  <ul>
                    {teams.team1.map((player, index) => (
                      <li
                        key={index}
                        className="flex justify-between items-center text-black py-2"
                      >
                        <span>{player.name}</span>
                        <span className="font-semibold text-red-600">{player.role}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                {/* Team 2 Players */}
                <div className="bg-gray-100 p-4 rounded-xl shadow-md">
                  <h3 className="text-xl font-semibold text-black mb-3">{match.team2}</h3>
                  <ul>
                    {teams.team2.map((player, index) => (
                      <li
                        key={index}
                        className="flex justify-between items-center text-black py-2"
                      >
                        <span>{player.name}</span>
                        <span className="font-semibold text-red-600">{player.role}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>

            {/* Predict Button */}
            <div className="flex justify-center mt-8">
              <button
                className="bg-red-600 text-white px-8 py-3 rounded-full shadow-lg hover:bg-red-700 transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-red-300"
                onClick={handlePredict}
              >
                Predict Dream11 Team
              </button>
            </div>

            {/* Prediction Content */}
            <div className="mt-6">
              {loading ? (
                <div className="flex justify-center">
                  <BeatLoader color="#000000" size={15} />
                </div>
              ) : prediction ? (
                <Best11Display
                  best11={prediction.best11} // Pass best11 data
                  text={prediction.text} // Pass the text description
                />
              ) : (
                <div className="text-center text-gray-500">Click the button to predict</div>
              )}
            </div>
          </>
        ) : (
          <div className="flex justify-center mt-6">
            <p className="text-gray-700">
              The squads will be shown once they are announced.
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default PopCard;
