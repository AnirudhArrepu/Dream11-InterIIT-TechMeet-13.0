const Home = () => {
  return (
    <div className="bg-gray-100 min-h-screen">
      <div className="max-w-4xl mx-auto px-4 py-8">
        {/* Image Section */}
        <div className="mb-6">
          <img
            src="\lords.jpg"
            alt="Lords Cricket Ground"
            className="rounded-lg shadow-lg w-full"
          />
        </div>

        {/* Description Section */}
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h1 className="text-2xl font-bold text-gray-800 mb-4">
            Welcome to the Gentleman's Game
          </h1>
          <p className="text-gray-600 leading-relaxed">
            Cricket, often called the "gentleman's game," is a sport that has
            captured the hearts of millions across the globe. Its rich history,
            thrilling matches, and iconic moments are celebrated worldwide.
            From the roaring crowds at the Lord's Cricket Ground to the fierce
            rivalries on the field, cricket embodies passion, strategy, and
            teamwork. Dive into the world of cricket and explore the legacy of
            this beautiful game!
          </p>
        </div>
      </div>
    </div>
  );
};

export default Home;
