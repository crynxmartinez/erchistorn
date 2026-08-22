import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "@/contexts/AuthContext";
import { Menu, X, BookOpen, Swords, Globe, Users, Zap, Newspaper, Trophy, Info, ScrollText } from "lucide-react";
import { useState } from "react";

const NAV_LINKS = [
    { to: "/",          label: "Home",       icon: BookOpen },
    { to: "/world",     label: "World",      icon: Globe },
    { to: "/races",     label: "Races",      icon: Users },
    { to: "/mechanics", label: "Mechanics",  icon: Swords },
    { to: "/blog",      label: "Blog",       icon: Newspaper },
    { to: "/leaderboard", label: "Ladder",   icon: Trophy },
    { to: "/about",     label: "About",      icon: Info },
];

export default function SiteLayout({ children }) {
    const { user } = useAuth();
    const navigate = useNavigate();
    const [menuOpen, setMenuOpen] = useState(false);

    return (
        <div className="min-h-screen flex flex-col bg-background">
            {/* Navbar */}
            <nav className="sticky top-0 z-50 border-b-2 border-primary/30 bg-background/95 backdrop-blur-sm">
                <div className="max-w-7xl mx-auto px-4 md:px-6 h-14 flex items-center justify-between">
                    <Link to="/" className="flex items-center gap-2" onClick={() => setMenuOpen(false)}>
                        <ScrollText size={20} className="text-primary" />
                        <span className="font-pixel text-lg uppercase text-primary tracking-wider hidden sm:inline">Erchis</span>
                    </Link>

                    {/* Desktop nav */}
                    <div className="hidden lg:flex items-center gap-1">
                        {NAV_LINKS.map((l) => (
                            <Link
                                key={l.to}
                                to={l.to}
                                className="stat-label px-3 py-1.5 text-muted-foreground hover:text-primary transition-colors rounded"
                            >
                                {l.label}
                            </Link>
                        ))}
                    </div>

                    {/* Auth buttons */}
                    <div className="hidden lg:flex items-center gap-2">
                        {user && user.has_character ? (
                            <button
                                onClick={() => navigate("/game")}
                                className="press-btn font-pixel text-sm uppercase px-4 py-1.5 bg-primary text-primary-foreground border-2 border-primary hover:bg-transparent hover:text-primary transition-colors"
                            >
                                Enter Game
                            </button>
                        ) : user ? (
                            <button
                                onClick={() => navigate("/create")}
                                className="press-btn font-pixel text-sm uppercase px-4 py-1.5 bg-primary text-primary-foreground border-2 border-primary hover:bg-transparent hover:text-primary transition-colors"
                            >
                                Create Hero
                            </button>
                        ) : (
                            <>
                                <Link
                                    to="/login"
                                    className="press-btn stat-label px-3 py-1.5 border border-border text-muted-foreground hover:text-primary hover:border-primary transition-colors"
                                >
                                    Sign In
                                </Link>
                                <Link
                                    to="/register"
                                    className="press-btn font-pixel text-sm uppercase px-4 py-1.5 bg-primary text-primary-foreground border-2 border-primary hover:bg-transparent hover:text-primary transition-colors"
                                >
                                    Play Free
                                </Link>
                            </>
                        )}
                    </div>

                    {/* Mobile menu button */}
                    <button
                        onClick={() => setMenuOpen(!menuOpen)}
                        className="lg:hidden press-btn p-2 border border-border text-primary"
                    >
                        {menuOpen ? <X size={18} /> : <Menu size={18} />}
                    </button>
                </div>

                {/* Mobile menu */}
                {menuOpen && (
                    <div className="lg:hidden border-t border-border bg-background">
                        <div className="px-4 py-3 space-y-1">
                            {NAV_LINKS.map((l) => (
                                <Link
                                    key={l.to}
                                    to={l.to}
                                    onClick={() => setMenuOpen(false)}
                                    className="flex items-center gap-2 px-3 py-2 stat-label text-muted-foreground hover:text-primary hover:bg-primary/5 rounded transition-colors"
                                >
                                    <l.icon size={14} /> {l.label}
                                </Link>
                            ))}
                            <div className="pt-2 border-t border-border flex gap-2">
                                {user ? (
                                    <button
                                        onClick={() => { setMenuOpen(false); navigate(user.has_character ? "/game" : "/create"); }}
                                        className="flex-1 press-btn font-pixel text-sm uppercase px-4 py-2 bg-primary text-primary-foreground border-2 border-primary"
                                    >
                                        {user.has_character ? "Enter Game" : "Create Hero"}
                                    </button>
                                ) : (
                                    <>
                                        <Link to="/login" onClick={() => setMenuOpen(false)} className="flex-1 text-center press-btn stat-label px-3 py-2 border border-border text-muted-foreground">
                                            Sign In
                                        </Link>
                                        <Link to="/register" onClick={() => setMenuOpen(false)} className="flex-1 text-center press-btn font-pixel text-sm uppercase px-4 py-2 bg-primary text-primary-foreground border-2 border-primary">
                                            Play Free
                                        </Link>
                                    </>
                                )}
                            </div>
                        </div>
                    </div>
                )}
            </nav>

            {/* Page content */}
            <main className="flex-1">{children}</main>

            {/* Footer */}
            <footer className="border-t-2 border-primary/20 bg-card mt-12">
                <div className="max-w-7xl mx-auto px-4 md:px-6 py-10">
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
                        <div className="col-span-2 md:col-span-1">
                            <div className="flex items-center gap-2 mb-3">
                                <ScrollText size={18} className="text-primary" />
                                <span className="font-pixel text-lg uppercase text-primary">Erchis</span>
                            </div>
                            <p className="narr text-sm text-muted-foreground">A fantasy dice RPG. Eight races, eleven continents, one die that decides all.</p>
                        </div>
                        <div>
                            <div className="stat-label text-primary/70 mb-2">GAME</div>
                            <div className="space-y-1">
                                <Link to="/world" className="block text-sm text-muted-foreground hover:text-primary">World</Link>
                                <Link to="/races" className="block text-sm text-muted-foreground hover:text-primary">Races</Link>
                                <Link to="/mechanics" className="block text-sm text-muted-foreground hover:text-primary">Mechanics</Link>
                                <Link to="/leaderboard" className="block text-sm text-muted-foreground hover:text-primary">Leaderboard</Link>
                            </div>
                        </div>
                        <div>
                            <div className="stat-label text-primary/70 mb-2">COMMUNITY</div>
                            <div className="space-y-1">
                                <Link to="/blog" className="block text-sm text-muted-foreground hover:text-primary">Blog</Link>
                                <Link to="/changelog" className="block text-sm text-muted-foreground hover:text-primary">Changelog</Link>
                                <Link to="/about" className="block text-sm text-muted-foreground hover:text-primary">About</Link>
                            </div>
                        </div>
                        <div>
                            <div className="stat-label text-primary/70 mb-2">ACCOUNT</div>
                            <div className="space-y-1">
                                <Link to="/register" className="block text-sm text-muted-foreground hover:text-primary">Create Account</Link>
                                <Link to="/login" className="block text-sm text-muted-foreground hover:text-primary">Sign In</Link>
                            </div>
                        </div>
                    </div>
                    <div className="mt-8 pt-6 border-t border-border flex items-center justify-between">
                        <div className="stat-label text-muted-foreground/40">&copy; Erchis Saga · A Fantasy Dice RPG</div>
                        <div className="stat-label text-muted-foreground/40">v.MVP</div>
                    </div>
                </div>
            </footer>
        </div>
    );
}
