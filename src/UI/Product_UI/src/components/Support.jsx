import React from "react";
import FAQSection from "./FAQ";

const Support = () => {
  return (
    <div className="min-h-screen bg-gray-100 py-12 px-6">
      <div className="max-w-6xl mx-auto bg-white rounded-lg shadow-md p-8">
        <div className="flex flex-col lg:flex-row items-center lg:items-start">
          {/* Illustration Section */}
          <div className="flex-1 text-center lg:text-left">
            <img
              src="\supportus.jpg" // Replace with the actual path to your illustration
              alt="Support Illustration"
              className="w-48 mx-auto lg:mx-0"
            />
            <h2 className="text-2xl font-semibold text-gray-800 mt-6">How can we help?</h2>
            <ul className="mt-4 text-gray-600 space-y-2 list-disc list-inside">
              <li>Do you need help understanding Fantasy Cricket rules?</li>
              <li>Want advice on improving your prediction strategies?</li>
              <li>Need technical assistance with the platform?</li>
              <li>Have suggestions to make our tools better?</li>
              <li>Curious about how our prediction system works?</li>
            </ul>
          </div>

          {/* Form Section */}
          <div className="flex-1 mt-8 lg:mt-0 lg:ml-12">
            {/* Have Questions Section */}
            <div className="text-center mb-6">
              <h1 className="text-3xl font-bold text-gray-800">Have questions? Shoot us an email.</h1>
              <p className="text-gray-600 mt-2">
                We are here to help you enhance your Fantasy Cricket skills and ensure you get the best out of our prediction tools. 
                Whether it's an issue, feedback, or a query, feel free to reach out to us!
              </p>
            </div>

            <h2 className="text-2xl font-semibold text-gray-800 mb-4">Submit Your Query</h2>
            <form className="space-y-6">
              {/* Dropdown */}
              <div>
                <label
                  htmlFor="queryType"
                  className="block text-sm font-medium text-gray-700"
                >
                  Select Your Query Type
                </label>
                <select
                  id="queryType"
                  className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                >
                  <option>Fantasy Cricket Issues</option>
                  <option>Feedback or Suggestions</option>
                  <option>Technical Issues</option>
                  <option>Other</option>
                </select>
              </div>

              {/* Name Field */}
              <div>
                <label
                  htmlFor="name"
                  className="block text-sm font-medium text-gray-700"
                >
                  Your Name
                </label>
                <input
                  type="text"
                  id="name"
                  placeholder="Enter your name"
                  className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                />
              </div>

              {/* Email Field */}
              <div>
                <label
                  htmlFor="email"
                  className="block text-sm font-medium text-gray-700"
                >
                  Your Email
                </label>
                <input
                  type="email"
                  id="email"
                  placeholder="Enter your email"
                  className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                />
              </div>

              {/* Message Field */}
              <div>
                <label
                  htmlFor="message"
                  className="block text-sm font-medium text-gray-700"
                >
                  Your Message
                </label>
                <textarea
                  id="message"
                  rows="4"
                  placeholder="Write your message here..."
                  className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                />
              </div>

              {/* File Upload */}
              <div>
                <label
                  htmlFor="fileUpload"
                  className="block text-sm font-medium text-gray-700"
                >
                  Attach a Screenshot (Optional)
                </label>
                <input
                  type="file"
                  id="fileUpload"
                  className="mt-1 block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded file:border-0 file:text-sm file:bg-gray-50 file:text-gray-700 hover:file:bg-gray-100"
                />
              </div>

              {/* Submit Button */}
              <button
                type="submit"
                className="w-full bg-indigo-600 text-white py-2 px-4 rounded-md shadow hover:bg-indigo-700 focus:ring focus:ring-indigo-300"
              >
                Submit
              </button>
            </form>
          </div>
        </div>

        <FAQSection />
      </div>
    </div>
  );
};

export default Support;
