import React, { useState } from "react";

const PopCard = ({ match, teams, onClose }) => {
  const [audioPlaying, setAudioPlaying] = useState(false); // State to manage audio play
  const squad_avail =
    teams["team1"].length > 0 && teams["team2"].length ? true : false;

  // Function to handle audio playback of the description
  const handleAudioPlay = () => {
    const descriptionText =
      "This is a match summary where you can view the team lineup and roles of the players.";
    const speech = new SpeechSynthesisUtterance(descriptionText);

    // Toggle play/pause of the audio
    if (audioPlaying) {
      speech.pause();
    } else {
      window.speechSynthesis.speak(speech);
    }

    setAudioPlaying(!audioPlaying);
  };

  return (
    <div className="fixed inset-0 bg-gray-800 bg-opacity-75 z-50">
      <div className="bg-white w-full h-full p-6 overflow-auto">
        {/* Modal Header */}
        <div className="flex justify-between items-center border-b pb-4">
          <h2 className="text-2xl font-bold text-gray-800">{`${match.team1} vs ${match.team2}`}</h2>
          <button
            onClick={onClose}
            className="text-gray-600 hover:text-red-500 text-xl font-bold"
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
                <div className="bg-gray-50 p-4 rounded shadow-md">
                  <h3 className="text-lg font-semibold text-gray-700 mb-3">
                    {match.team1}
                  </h3>
                  <ul>
                    {teams["team1"].map((player, index) => (
                      <li
                        key={index}
                        className="flex justify-between items-center text-gray-600 py-1"
                      >
                        <span>{player.name}</span>
                        <span className="font-semibold">{player.role}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                {/* Team 2 Players */}
                <div className="bg-gray-50 p-4 rounded shadow-md">
                  <h3 className="text-lg font-semibold text-gray-700 mb-3">
                    {match.team2}
                  </h3>
                  <ul>
                    {teams["team2"].map((player, index) => (
                      <li
                        key={index}
                        className="flex justify-between items-center text-gray-600 py-1"
                      >
                        <span>{player.name}</span>
                        <span className="font-semibold">{player.role}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
            {/* Green Button */}
            <div className="flex justify-center mt-8">
              <button
                className="bg-green-600 text-white px-6 py-2 rounded-md shadow hover:bg-green-700 focus:ring-2 focus:ring-green-300 focus:outline-none"
                onClick={() => {}}
              >
                Confirm Selection
              </button>
            </div>

            {/* Audio Button */}
            <div className="mt-6 text-center">
              <button
                onClick={handleAudioPlay}
                className="bg-blue-600 text-white px-6 py-2 rounded-md shadow hover:bg-blue-700 focus:ring-2 focus:ring-blue-300 focus:outline-none"
              >
                {audioPlaying ? "Pause Audio" : "Listen to Description"}
              </button>
            </div>
          </>
        ) : (
          <div className="flex justify-center mt-6">The squads will be shown once it is announced</div>
        )}
      </div>
    </div>
  );
};

export default PopCard;
