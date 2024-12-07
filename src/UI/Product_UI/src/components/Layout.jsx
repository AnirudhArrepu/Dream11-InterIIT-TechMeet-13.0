import React from 'react';
import { Outlet } from 'react-router-dom';
import Header from './Header'; 
import Footer from './Footer';

const Layout = () => {
    return (
        <div className="flex flex-col min-h-screen">
            {/* Header */}
            <header className="bg-gray-800 text-white">
                <Header />
            </header>

            {/* Main Content */}
            <main className="flex-grow container mx-auto p-4">
                <Outlet />
            </main>

            {/* Footer */}
            <footer className="bg-gray-800 text-white">
                <Footer />
            </footer>
        </div>
    );
};

export default Layout;
