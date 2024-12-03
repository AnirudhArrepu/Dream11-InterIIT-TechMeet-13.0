import { createBrowserRouter } from 'react-router-dom';
import HomePage from "../Home/HomePage";
import SupportUs from '../SupportUs/SupportUs';
import AboutUs from '../AboutUs/AboutUS';
import Matches from '../Matches/Matches';

export const router = createBrowserRouter([
            {
                path: "/",
                element: <HomePage />,
                exact: true,
            },
            {
                path: "/ContactUs",
                element: <SupportUs />,
            },
            {
                path: "/AboutUs",
                element: <AboutUs />,
            },
            {
                path: "/Matches",
                element: <Matches />,
            }
]);