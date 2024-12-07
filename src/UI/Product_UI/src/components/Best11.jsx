import React, { useState, useEffect, useRef } from 'react';

const Best11Display = ({ best11, text }) => {
    const [isReading, setIsReading] = useState(false); // State to track if the text is being read
    const titleRef = useRef(null); // Reference to the "Best 11 Players" heading

    // Scroll to the "Best 11 Players" heading when the component mounts
    useEffect(() => {
        if (titleRef.current) {
            titleRef.current.scrollIntoView({
                behavior: 'smooth',
                block: 'start',
            });
        }
    }, []);

    const handleToggleRead = () => {
        if (isReading) {
            // If it's already reading, stop it
            window.speechSynthesis.cancel();
            setIsReading(false);
        } else {
            // If it's not reading, start reading the text
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = 'en-US';
            window.speechSynthesis.speak(utterance);
            setIsReading(true);

            // When the speech is finished, update the state
            utterance.onend = () => setIsReading(false);
        }
    };

    return (
        <div className="max-w-7xl mx-auto bg-white shadow-lg rounded-2xl p-8 mt-12">
            {/* Scroll to this heading */}
            <h2 ref={titleRef} className="text-3xl font-bold text-center text-red-600 mb-6">
                Best 11 Players
            </h2>

            {/* Display players */}
            <div className="space-y-6">
                {best11.map((player, index) => (
                    <div
                        key={index}
                        className="flex justify-between items-center p-4 bg-gray-50 hover:bg-gray-100 rounded-lg shadow-md transition duration-300 ease-in-out"
                    >
                        <div className="flex flex-col space-y-2">
                            <span className="text-xl font-semibold text-gray-800">{player.Player}</span>
                            <span className="text-md text-gray-600">Score: <span className="font-semibold text-red-600">{player.Score}</span></span>
                            <span className="text-md text-gray-600">Role: <span className="font-semibold text-black">{player.Role}</span></span>
                            <span className="text-md text-gray-600">Team: <span className="font-semibold text-black">{player.Team}</span></span>
                        </div>
                    </div>
                ))}
            </div>

            {/* Explanation Text */}
            {text && (
                <div className="mt-8 bg-gray-100 p-6 rounded-lg shadow-md">
                    <h3 className="text-xl font-semibold text-black mb-2">Explanation</h3>
                    <p className="text-gray-700">{text}</p>
                    <button
                        onClick={handleToggleRead}
                        className="mt-4 text-red-600 font-semibold focus:outline-none hover:text-red-800"
                    >
                        {isReading ? 'Stop Reading' : 'Read Aloud'}
                    </button>
                </div>
            )}
        </div>
    );
};

export default Best11Display;
