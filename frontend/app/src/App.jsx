import React from 'react';
import { BrowserRouter as Router, Route, Routes} from 'react-router-dom';
import DashboardPage from './pages/dashboard';
import SettingsPage from './pages/Settings';
import LoginPage from "./pages/loginSignup";
import Historypage from "@/pages/Historypage";
import AuthMiddleware from "./middleware";

const basename = import.meta.env.BASE_URL

function App() {
    return (
        <Router basename={basename}>
            <Routes>
                <Route path="/" element={<AuthMiddleware><DashboardPage/></AuthMiddleware>}/>
                <Route path="/login" element={<LoginPage/>}/>
                <Route path="/dashboard" element={<AuthMiddleware><DashboardPage/></AuthMiddleware>}/>
                <Route path="/documents" element={<AuthMiddleware><Historypage/></AuthMiddleware>}/>
                <Route path="/settings" element={<AuthMiddleware><SettingsPage/></AuthMiddleware>}/>
            </Routes>
        </Router>
    );
}

export default App;
