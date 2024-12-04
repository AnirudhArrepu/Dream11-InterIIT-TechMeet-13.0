import React from "react";
import {
  FaRegStar,
  FaRegThumbsUp,
  FaChartLine,
} from "react-icons/fa";
import { Link } from "react-router-dom";

const Home = () => {
  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <div
        className="relative min-h-screen flex items-center justify-center text-center bg-cover bg-center"
        style={{
          backgroundImage: `url('/lords.jpg')`, // Replace with your Lord's image path
        }}
      >
        <div className="absolute inset-0 bg-black bg-opacity-40"></div>{" "}
        {/* Changed from bg-opacity-50 to bg-opacity-70 */}
        <div className="relative z-10 text-white px-6 lg:px-0 max-w-4xl">
          <h1 className="text-5xl font-extrabold mb-6">
            Elevate Your Fantasy Cricket Experience
          </h1>
          <p className="text-xl font-medium mb-8">
            Combining the love for cricket with the power of AI to provide
            real-time predictions and insights.
          </p>
          <Link to="/signup">
            <button className="bg-red-600 text-white py-3 px-8 rounded-lg text-lg hover:bg-red-700 transition duration-300">
              Get Started Now
            </button>
          </Link>
        </div>
      </div>

      {/* Features Section */}
      <div className="bg-gradient-to-b from-red-50 to-white py-16 px-8">
        <h2 className="text-4xl font-semibold text-center text-gray-800 mb-12">
          Why Choose Us?
        </h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8 max-w-6xl mx-auto">
          {/* Feature 1 */}
          <div className="bg-white p-6 rounded-xl shadow-lg hover:shadow-2xl transition duration-300">
            <div className="flex items-center mb-4">
              <FaChartLine className="text-red-600 text-3xl mr-4" />
              <h3 className="text-2xl font-semibold text-gray-800">
                Real-Time Predictions
              </h3>
            </div>
            <p className="text-gray-600 mb-4">
              Our AI models analyze player stats and match conditions to give
              you the most accurate fantasy predictions.
            </p>
            <button className="text-red-600 hover:underline">Learn More</button>
          </div>

          {/* Feature 2 */}
          <div className="bg-white p-6 rounded-xl shadow-lg hover:shadow-2xl transition duration-300">
            <div className="flex items-center mb-4">
              <FaRegThumbsUp className="text-red-600 text-3xl mr-4" />
              <h3 className="text-2xl font-semibold text-gray-800">
                AI-Powered Insights
              </h3>
            </div>
            <p className="text-gray-600 mb-4">
              Leverage advanced analytics to create winning teams and improve
              your chances of success.
            </p>
            <button className="text-red-600 hover:underline">
              Explore Now
            </button>
          </div>

          {/* Feature 3 */}
          <div className="bg-white p-6 rounded-xl shadow-lg hover:shadow-2xl transition duration-300">
            <div className="flex items-center mb-4">
              <FaRegStar className="text-red-600 text-3xl mr-4" />
              <h3 className="text-2xl font-semibold text-gray-800">
                User-Friendly Design
              </h3>
            </div>
            <p className="text-gray-600 mb-4">
              Our intuitive interface ensures a seamless experience for all
              users, from beginners to pros.
            </p>
            <button className="text-red-600 hover:underline">
              View Features
            </button>
          </div>
        </div>
      </div>

      {/* User Testimonials */}
      <div className="py-16 px-8 bg-gray-50">
        <h2 className="text-4xl font-semibold text-center text-gray-800 mb-12">
          What Our Users Say
        </h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8 max-w-6xl mx-auto">
          {/* Testimonial 1 */}
          <div className="bg-white p-6 rounded-xl shadow-lg">
            <p className="text-gray-600 mb-4">
              "The best fantasy cricket platform out there! The predictions are
              spot on and helped me win big last season."
            </p>
            <p className="text-red-600 font-semibold">- Rahul S.</p>
          </div>

          {/* Testimonial 2 */}
          <div className="bg-white p-6 rounded-xl shadow-lg">
            <p className="text-gray-600 mb-4">
              "I love the user-friendly design and insightful AI tools. Makes
              managing my fantasy team so much easier!"
            </p>
            <p className="text-red-600 font-semibold">- Priya K.</p>
          </div>

          {/* Testimonial 3 */}
          <div className="bg-white p-6 rounded-xl shadow-lg">
            <p className="text-gray-600 mb-4">
              "Highly recommend for cricket enthusiasts! The interactive UI and
              AI-driven features are a game changer."
            </p>
            <p className="text-red-600 font-semibold">- Arjun M.</p>
          </div>
        </div>
      </div>

      {/* Call to Action Section */}
      <div className="bg-red-600 py-16 px-8 text-white text-center">
        <h2 className="text-3xl font-semibold mb-4">
          Ready to Dominate Your Fantasy League?
        </h2>
        <p className="text-lg mb-8">
          Get started today and access cutting-edge AI tools to boost your
          cricket predictions.
        </p>
        <Link to="/signup">
          <button className="bg-white text-red-600 py-3 px-8 rounded-lg text-lg hover:bg-gray-100 transition-all duration-300">
            Sign up here
          </button>
        </Link>
      </div>
    </div>
  );
};

export default Home;
