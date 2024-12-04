import React, { useState } from "react";

const FAQSection = () => {
  const [openIndex, setOpenIndex] = useState(null);
  const [searchTerm, setSearchTerm] = useState("");

  const faqs = [
    {
      question: "How accurate are the predictions?",
      answer:
        "Our predictions are based on advanced algorithms and historical data. While we aim for high accuracy, outcomes in cricket can vary due to unforeseen match conditions.",
    },
    {
      question: "Can beginners use this platform?",
      answer:
        "Absolutely! Our platform is designed to cater to both beginners and experienced fantasy cricket players. Our user-friendly interface ensures a smooth experience for everyone.",
    },
    {
      question: "Do you provide predictions for all cricket matches?",
      answer:
        "We focus on major international and domestic tournaments. Our platform ensures coverage of the most popular and relevant matches.",
    },
    {
      question: "How often is the data updated?",
      answer:
        "Player and match data are updated in real-time to ensure that predictions are as accurate and current as possible.",
    },
    {
      question: "Is this platform free to use?",
      answer:
        "Our platform offers both free and premium plans. The free plan provides access to basic features, while the premium plan unlocks advanced analytics and exclusive insights.",
    },
  ];

  const filteredFAQs = faqs.filter((faq) =>
    faq.question.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const toggleFAQ = (index) => {
    setOpenIndex(openIndex === index ? null : index);
  };

  return (
    <div className="max-w-4xl mx-auto bg-white shadow-md rounded-lg p-8 mt-12">
      <h2 className="text-2xl font-bold text-gray-800 mb-6 text-center">
        Frequently Asked Questions
      </h2>

      {/* Search Field */}
      <div className="relative mb-6">
        <input
          type="text"
          placeholder="Type your question here"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="w-full border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 px-4 py-2 text-gray-700"
        />
        <button className="absolute right-2 top-1/2 transform -translate-y-1/2 text-indigo-500 hover:text-indigo-700">
          🔍
        </button>
      </div>

      {/* FAQs */}
      <div className="divide-y divide-gray-200">
        {filteredFAQs.length > 0 ? (
          filteredFAQs.map((faq, index) => (
            <div key={index} className="py-4">
              <button
                onClick={() => toggleFAQ(index)}
                className="flex justify-between w-full text-left font-medium text-gray-700 focus:outline-none"
              >
                <span>{faq.question}</span>
                <span
                  className={`transform transition-transform ${
                    openIndex === index ? "rotate-0" : ""
                  }`}
                >
                  +
                </span>
              </button>
              <div
                className={`overflow-hidden transition-all duration-300 ease-in-out ${
                  openIndex === index ? "max-h-96" : "max-h-0"
                }`}
              >
                {openIndex === index && (
                  <p className="mt-2 text-gray-600">{faq.answer}</p>
                )}
              </div>
            </div>
          ))
        ) : (
          <p className="text-gray-600 mt-4 text-center">
            No matching FAQs found. Please refine your search.
          </p>
        )}
      </div>
    </div>
  );
};

export default FAQSection;
