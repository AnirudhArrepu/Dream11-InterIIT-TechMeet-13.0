import { useState } from "react";
import { Link } from "react-router-dom";

const Header = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  return (
    <header className="bg-gradient-to-r from-red-500 to-red-700 text-white">
      <div className="max-w-7xl mx-auto flex justify-between items-center px-4 py-4">
        <Link to="/" className="flex items-center space-x-2 text-xl font-bold hover:text-gray-300">
          <img
            src="\logo.png"
            alt="Wicket Wizard Logo"
            className="h-8 w-8 object-cover"
          />
          <span>Wicket Wizard</span>
        </Link>

        {/* Menu for larger screens */}
        <nav className="hidden md:flex space-x-8">
          <Link to="/" className="hover:text-gray-400">Home</Link>
          <Link to="/matches" className="hover:text-gray-400">Matches</Link>
          <Link to="/about" className="hover:text-gray-400">About Us</Link>
          <Link to="/support" className="hover:text-gray-400">Support</Link>
          <Link to="/login" className="hover:text-gray-400">Log In</Link>
        </nav>

        {/* Hamburger Menu for mobile */}
        <button
          className="md:hidden focus:outline-none"
          onClick={() => setIsMenuOpen(!isMenuOpen)}
          aria-label="Toggle Menu"
        >
          <span className="block w-6 h-0.5 bg-white mb-1"></span>
          <span className="block w-6 h-0.5 bg-white mb-1"></span>
          <span className="block w-6 h-0.5 bg-white"></span>
        </button>
      </div>

      {/* Dropdown Menu for mobile */}
      {isMenuOpen && (
        <div className="md:hidden bg-gray-700 text-white py-4 space-y-2">
          <Link
            to="/"
            className="block px-4 py-2 hover:bg-gray-600"
            onClick={() => setIsMenuOpen(false)}
          >
            Home
          </Link>
          <Link
            to="/matches"
            className="block px-4 py-2 hover:bg-gray-600"
            onClick={() => setIsMenuOpen(false)}
          >
            Matches
          </Link>
          <Link
            to="/about"
            className="block px-4 py-2 hover:bg-gray-600"
            onClick={() => setIsMenuOpen(false)}
          >
            About Us
          </Link>
          <Link
            to="/support"
            className="block px-4 py-2 hover:bg-gray-600"
            onClick={() => setIsMenuOpen(false)}
          >
            Support
          </Link>
        </div>
      )}
    </header>
  );
};

export default Header;
