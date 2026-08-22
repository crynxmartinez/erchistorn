import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import { AuthProvider, useAuth } from "@/contexts/AuthContext";
import Home from "@/pages/Home";
import Login from "@/pages/Login";
import Register from "@/pages/Register";
import ForgotPassword from "@/pages/ForgotPassword";
import ResetPassword from "@/pages/ResetPassword";
import Auth from "@/pages/Auth";
import CharacterCreate from "@/pages/CharacterCreate";
import Game from "@/pages/Game";
import LeaderboardPage from "@/pages/LeaderboardPage";
import GuildHouse from "@/pages/GuildHouse";
import GuildDetail from "@/pages/GuildDetail";
import World from "@/pages/World";
import Races from "@/pages/Races";
import Mechanics from "@/pages/Mechanics";
import Blog from "@/pages/Blog";
import BlogPost from "@/pages/BlogPost";
import About from "@/pages/About";
import Changelog from "@/pages/Changelog";
import { Toaster } from "@/components/ui/sonner";
import "@/App.css";

function ProtectedRoute({ children, requireCharacter = false }) {
    const { user } = useAuth();
    if (user === null) {
        return (
            <div className="min-h-screen flex items-center justify-center text-primary font-pixel text-2xl">
                LOADING ERCHIS…
            </div>
        );
    }
    if (user === false) return <Navigate to="/login" replace />;
    if (requireCharacter && !user.has_character) return <Navigate to="/create" replace />;
    if (!requireCharacter && user.has_character && window.location.pathname === "/create") {
        return <Navigate to="/game" replace />;
    }
    return children;
}

function AppRoutes() {
    return (
        <Routes>
            {/* Public pages */}
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/forgot-password" element={<ForgotPassword />} />
            <Route path="/reset-password" element={<ResetPassword />} />
            <Route path="/auth" element={<Auth />} />
            <Route path="/world" element={<World />} />
            <Route path="/races" element={<Races />} />
            <Route path="/mechanics" element={<Mechanics />} />
            <Route path="/blog" element={<Blog />} />
            <Route path="/blog/:slug" element={<BlogPost />} />
            <Route path="/leaderboard" element={<LeaderboardPage />} />
            <Route path="/about" element={<About />} />
            <Route path="/changelog" element={<Changelog />} />

            {/* Protected pages */}
            <Route path="/create" element={
                <ProtectedRoute><CharacterCreate /></ProtectedRoute>
            } />
            <Route path="/game" element={
                <ProtectedRoute requireCharacter><Game /></ProtectedRoute>
            } />
            <Route path="/guild-house" element={
                <ProtectedRoute requireCharacter><GuildHouse /></ProtectedRoute>
            } />
            <Route path="/guild/:guildId" element={
                <ProtectedRoute requireCharacter><GuildDetail /></ProtectedRoute>
            } />
            <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
    );
}

export default function App() {
    return (
        <div className="App">
            <BrowserRouter>
                <AuthProvider>
                    <AppRoutes />
                    <Toaster />
                </AuthProvider>
            </BrowserRouter>
        </div>
    );
}
