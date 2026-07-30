import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import { AuthProvider, useAuth } from "@/contexts/AuthContext";
import Landing from "@/pages/Landing";
import Auth from "@/pages/Auth";
import CharacterCreate from "@/pages/CharacterCreate";
import Game from "@/pages/Game";
import LeaderboardPage from "@/pages/LeaderboardPage";
import GuildHouse from "@/pages/GuildHouse";
import GuildDetail from "@/pages/GuildDetail";
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
    if (user === false) return <Navigate to="/auth" replace />;
    if (requireCharacter && !user.has_character) return <Navigate to="/create" replace />;
    if (!requireCharacter && user.has_character && window.location.pathname === "/create") {
        return <Navigate to="/game" replace />;
    }
    return children;
}

function AppRoutes() {
    return (
        <Routes>
            <Route path="/" element={<Landing />} />
            <Route path="/auth" element={<Auth />} />
            <Route path="/create" element={
                <ProtectedRoute><CharacterCreate /></ProtectedRoute>
            } />
            <Route path="/game" element={
                <ProtectedRoute requireCharacter><Game /></ProtectedRoute>
            } />
            <Route path="/leaderboard" element={
                <ProtectedRoute requireCharacter><LeaderboardPage /></ProtectedRoute>
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
