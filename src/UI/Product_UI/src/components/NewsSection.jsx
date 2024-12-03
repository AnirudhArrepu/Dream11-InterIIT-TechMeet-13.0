import React, { useState, useEffect } from "react";
import axios from "axios";

const NewsSection = () => {
  const [news, setNews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const fetchNews = async () => {
    try {
      // Check if cached data exists and is not expired (1 hour = 3600000 ms)
      const cachedNews = localStorage.getItem("cricketNews");
      const cachedTimestamp = localStorage.getItem("cricketNewsTimestamp");

      // If cache exists and it's within 1 hour, use the cached data
      if (cachedNews && cachedTimestamp) {
        const currentTime = new Date().getTime();
        if (currentTime - cachedTimestamp < 3600000) {
          setNews(JSON.parse(cachedNews));
          setLoading(false);
          return;
        }
      }

      // Fetch new data if cache is expired or does not exist
      const response = await axios.post("http://localhost:5000/api/cricket-news");

      // Check if 'news' is present and is an array
      if (response.data && Array.isArray(response.data.news)) {
        setNews(response.data.news);

        // Cache the news data and timestamp
        localStorage.setItem("cricketNews", JSON.stringify(response.data.news));
        localStorage.setItem("cricketNewsTimestamp", new Date().getTime().toString());
      } else {
        setError("No news found.");
      }

      setLoading(false);
    } catch (err) {
      setError("Failed to fetch news");
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchNews();
  }, []);

  const handleArticleClick = async (id) => {
    // Check if the URL is cached in localStorage
    const cachedUrl = localStorage.getItem(`articleUrl-${id}`);
  
    if (cachedUrl) {
      // If URL is cached, use it
      window.open(cachedUrl, "_blank");
    } else {
      try {
        // Fetch the URL from the backend if it's not cached
        const response = await axios.get(`http://localhost:5000/api/cricket-news/${id}`);
        const url = response.data.url;
  
        if (url) {
          // Cache the URL in localStorage with the article ID as the key
          localStorage.setItem(`articleUrl-${id}`, url);
  
          // Redirect to the article URL
          window.open(url, "_blank");
        } else {
          alert("Article URL not found.");
        }
      } catch (error) {
        console.error("Error fetching article URL:", error);
        alert("Failed to fetch article URL.");
      }
    }
  };
  

  if (loading) {
    return (
      <div className="w-full p-4">
        <div className="bg-white shadow-lg rounded-lg p-6 border-4 border-red-600">
          <p className="text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="w-full p-4">
        <div className="bg-white shadow-lg rounded-lg p-6 border-4 border-red-600">
          <p className="text-gray-600">{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="w-full p-4">
      <div className="bg-white shadow-lg rounded-lg p-6 border-4 border-red-600">
        <div className="space-y-4">
          {news.length > 0 ? (
            news.map((article, index) => (
              <div
                key={index}
                className="border-b border-gray-300 pb-4 cursor-pointer"
                onClick={() => handleArticleClick(article.id)}
              >
                <h3 className="text-lg font-semibold text-gray-800">
                  {article.headline}
                </h3>
                <p className="text-sm text-gray-600">{article.intro}</p>
                <p className="text-xs text-gray-500">Published on: {article.published_on}</p>
                <p className="text-xs text-gray-500">Source: {article.source}</p>
              </div>
            ))
          ) : (
            <p className="text-gray-600">No news available.</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default NewsSection;
