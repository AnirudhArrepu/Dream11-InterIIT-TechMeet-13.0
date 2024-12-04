import { Link } from "react-router-dom";

const Footer = () => {
    return (
      <footer className="bg-gray-800 text-white font-sans text-sm">
        {/* Top Section */}
        <div className="max-w-7xl mx-auto px-4 py-8">
          <div className="flex flex-wrap justify-between gap-6">
            {/* Logo & Social Icons */}
            <div className="flex flex-col items-center text-center space-y-4">
              <img src="/path/to/logo.png" alt="Dream11 Logo" className="w-36" />
            </div>
  
            {/* Links Section */}
            <div className="flex flex-wrap flex-grow justify-around">
              <div className="space-y-2">
                <a href="https://www.dream11.com/fantasy-cricket/point-system" className="block hover:text-gray-400">Fantasy Cricket Point System</a>
                <a href="https://www.dream11.com/fantasy-cricket/how-to-play-fantasy" className="block hover:text-gray-400">How to play</a>
                <a href="https://www.dream11.com/download-app" className="block hover:text-gray-400">Fantasy Cricket App Download</a>
              </div>
              <div className="space-y-2">
              <Link to="/about" className="block hover:text-gray-400">About Us</Link>
              <Link to="/support" className="block hover:text-gray-400">Support</Link>
              <p>© 2024 Fantasy Cricket Predictor. All rights reserved.</p>
              <p>Designed for Inter IIT Tech Meet | Powered by AI and Passion for Cricket</p>
              </div>
            </div>
          </div>
        </div>
      </footer>
    );
  };
  
  export default Footer;
  