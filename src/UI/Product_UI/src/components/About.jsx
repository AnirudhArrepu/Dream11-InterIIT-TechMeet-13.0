import React from "react";

const About = () => {
  return (
    <div className="bg-gray-100 text-gray-800 font-sans py-10 px-5 lg:px-20">
      <div className="max-w-5xl mx-auto">
        <h1 className="text-4xl font-bold text-center mb-8 text-gray-900">About Us</h1>
        <p className="text-lg leading-8 mb-6">
          Welcome to <b>Fantasy Cricket Predictor</b>, your ultimate platform to enhance your fantasy cricket experience! 
          Our mission is to provide cricket enthusiasts and fantasy sports players with accurate and reliable predictions 
          to maximize their performance in fantasy leagues.
        </p>
        <p className="text-lg leading-8 mb-6">
          With a deep understanding of the fantasy cricket point system, we utilize advanced algorithms, match analytics, 
          and player performance data to forecast player scores and suggest the best team combinations. Our solution caters 
          to both beginners and experienced players who wish to gain a competitive edge in their leagues.
        </p>
        <h2 className="text-2xl font-semibold mt-6 mb-4">Our Vision</h2>
        <p className="text-lg leading-8 mb-6">
          To revolutionize the fantasy sports industry by delivering innovative and data-driven solutions that empower users 
          to make informed decisions while enjoying the thrill of fantasy cricket.
        </p>
        <h2 className="text-2xl font-semibold mt-6 mb-4">Why Choose Us?</h2>
        <ul className="list-disc list-inside space-y-3">
          <li className="text-lg">Accurate player performance predictions based on real-time data.</li>
          <li className="text-lg">User-friendly interface tailored for fantasy cricket enthusiasts.</li>
          <li className="text-lg">Insights derived from in-depth analysis of match conditions and player statistics.</li>
          <li className="text-lg">Dedicated support and a growing community of fantasy sports lovers.</li>
        </ul>
        <div className="bg-blue-50 border border-blue-200 p-6 rounded-lg mt-10">
          <h2 className="text-xl font-semibold text-blue-700">Get Started Today!</h2>
          <p className="text-lg leading-8 mt-3">
            Enhance your prediction skills and take your fantasy cricket game to the next level. Dive deep into the world of expert analysis and insights, 
            empowering you to make smarter, more informed decisions for every match. With our platform, you can refine your strategies, improve your 
            understanding of the game, and consistently win fantasy predictions. Whether you're a seasoned player or just starting your fantasy journey, 
            we are here to provide you with a seamless and enriching experience. Embrace the thrill of competition, master the art of prediction, 
            and enjoy an unparalleled fantasy cricket adventure like never before!
          </p>
        </div>
        <p className="text-center text-sm text-gray-500 mt-10">
          &copy; 2024 Fantasy Cricket Predictor. All Rights Reserved.
        </p>
      </div>
    </div>
  );
};

export default About;
