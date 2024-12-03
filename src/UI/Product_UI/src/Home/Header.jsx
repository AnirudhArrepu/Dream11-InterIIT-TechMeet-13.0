import { useState } from "react";
import { Link } from "react-router-dom";

const Header = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  return (
    <header className="bg-red-800 text-white">
      <div className="max-w-7xl mx-auto flex justify-between items-center px-4 py-4">
        {/* Logo */}
        <a href="/" className="text-xl font-bold hover:text-gray-300">
          Dream11
        </a>

        {/* Menu for larger screens */}
        <nav className="hidden md:flex space-x-8">
          <a href="/" className="hover:text-gray-400">Home</a>
          <a href="/Matches" className="hover:text-gray-400">Matches</a>
          <Link to="/AboutUs" className="hover:text-gray-400">About Us</Link>
          <Link to="/ContactUs" className="hover:text-gray-400">Support</Link>
        </nav>

        {/* Hamburger Menu for mobile */}
        <button
          className="md:hidden focus:outline-none"
          onClick={() => setIsMenuOpen(!isMenuOpen)}
        >
          <span className="block w-6 h-0.5 bg-white mb-1"></span>
          <span className="block w-6 h-0.5 bg-white mb-1"></span>
          <span className="block w-6 h-0.5 bg-white"></span>
        </button>
      </div>

      {/* Dropdown Menu for mobile */}
      {isMenuOpen && (
        <div className="md:hidden bg-gray-700 text-white py-4 space-y-2">
          <a href="/" className="block px-4 hover:bg-gray-600">Home</a>
          <a href="/matches" className="block px-4 hover:bg-gray-600">Matches</a>
          <Link to="/AboutUs" className="hover:text-gray-400">About Us</Link>
          <Link to="/ContactUs" className="hover:text-gray-400">Support</Link>
        </div>
      )}
    </header>
  );
};

export default Header;
