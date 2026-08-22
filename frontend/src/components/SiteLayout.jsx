import { Link, useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "@/contexts/AuthContext";
import { Menu, X } from "lucide-react";
import { useEffect, useState } from "react";
import Die from "@/components/site/Die";
import Button from "@/components/site/Button";

/**
 * Public site shell.
 *
 * Two changes from the previous version worth noting:
 *
 *  - The mark is the d6, not a generic scroll icon. The die is the game's central
 *    mechanic, so it is the one thing that can carry the brand without artwork.
 *  - Nav links are monospace at label size rather than VT323 at 14px. A pixel face
 *    needs to be large to be legible; at nav size it reads as noise, which is why
 *    everything on the old site felt shouty and hard to scan.
 */

const NAV_LINKS = [
    { to: "/world", label: "World" },
    { to: "/races", label: "Races" },
    { to: "/mechanics", label: "Mechanics" },
    { to: "/blog", label: "Blog" },
    { to: "/leaderboard", label: "Ladder" },
    { to: "/about", label: "About" },
];

const FOOTER_GROUPS = [
    {
        title: "Game",
        links: [
            { to: "/world", label: "World" },
            { to: "/races", label: "Races" },
            { to: "/mechanics", label: "Mechanics" },
            { to: "/leaderboard", label: "Leaderboard" },
        ],
    },
    {
        title: "Community",
        links: [
            { to: "/blog", label: "Blog" },
            { to: "/changelog", label: "Changelog" },
            { to: "/about", label: "About" },
        ],
    },
    {
        title: "Account",
        links: [
            { to: "/register", label: "Create account" },
            { to: "/login", label: "Sign in" },
        ],
    },
];

export default function SiteLayout({ children }) {
    const { user } = useAuth();
    const navigate = useNavigate();
    const { pathname } = useLocation();
    const [menuOpen, setMenuOpen] = useState(false);

    // Close the mobile menu on navigation, otherwise it stays open over the new page.
    useEffect(() => setMenuOpen(false), [pathname]);

    const cta = user?.has_character
        ? { label: "Enter game", go: () => navigate("/game") }
        : user
        ? { label: "Create hero", go: () => navigate("/create") }
        : null;

    return (
        <div className="site-page flex min-h-screen flex-col bg-background">
            <a
                href="#main"
                className="sr-only focus:not-sr-only focus:absolute focus:left-4 focus:top-4 focus:z-[60] focus:border-2 focus:border-primary focus:bg-background focus:px-4 focus:py-2 focus:font-mono focus:text-label focus:uppercase focus:text-primary"
            >
                Skip to content
            </a>

            <header className="sticky top-0 z-50 border-b border-border/70 bg-background/90 backdrop-blur-md">
                <div className="mx-auto flex h-20 w-full max-w-6xl items-center justify-between px-6">
                    <Link to="/" className="flex items-center gap-3" aria-label="Erchis, home">
                        <Die size={30} face={6} roll={false} />
                        <span className="font-display text-card uppercase tracking-widest text-foreground">
                            Erchis
                        </span>
                    </Link>

                    <nav aria-label="Main" className="hidden items-center gap-1 lg:flex">
                        {NAV_LINKS.map((l) => {
                            const active = pathname === l.to;
                            return (
                                <Link
                                    key={l.to}
                                    to={l.to}
                                    aria-current={active ? "page" : undefined}
                                    className={`px-3 py-2 font-mono text-label uppercase transition-colors ${
                                        active
                                            ? "text-primary"
                                            : "text-muted-foreground hover:text-foreground"
                                    }`}
                                >
                                    {l.label}
                                </Link>
                            );
                        })}
                    </nav>

                    <div className="hidden items-center gap-3 lg:flex">
                        {cta ? (
                            <Button size="md" onClick={cta.go}>
                                {cta.label}
                            </Button>
                        ) : (
                            <>
                                <Link
                                    to="/login"
                                    className="px-3 py-2 font-mono text-label uppercase text-muted-foreground transition-colors hover:text-foreground"
                                >
                                    Sign in
                                </Link>
                                <Button to="/register" size="md">
                                    Play free
                                </Button>
                            </>
                        )}
                    </div>

                    <button
                        type="button"
                        onClick={() => setMenuOpen((v) => !v)}
                        aria-expanded={menuOpen}
                        aria-label={menuOpen ? "Close menu" : "Open menu"}
                        className="p-2 text-primary lg:hidden"
                    >
                        {menuOpen ? <X size={26} /> : <Menu size={26} />}
                    </button>
                </div>

                {menuOpen && (
                    <nav
                        aria-label="Mobile"
                        className="border-t border-border/70 bg-background lg:hidden"
                    >
                        <div className="mx-auto max-w-6xl px-6 py-4">
                            {NAV_LINKS.map((l) => (
                                <Link
                                    key={l.to}
                                    to={l.to}
                                    className="block border-b border-border/40 py-3 font-mono text-label uppercase text-muted-foreground hover:text-primary"
                                >
                                    {l.label}
                                </Link>
                            ))}
                            <div className="mt-5 flex flex-col gap-3">
                                {cta ? (
                                    <Button size="md" onClick={cta.go}>
                                        {cta.label}
                                    </Button>
                                ) : (
                                    <>
                                        <Button to="/register" size="md">
                                            Play free
                                        </Button>
                                        <Button to="/login" size="md" variant="ghost">
                                            Sign in
                                        </Button>
                                    </>
                                )}
                            </div>
                        </div>
                    </nav>
                )}
            </header>

            <main id="main" className="flex-1">
                {children}
            </main>

            <footer className="border-t border-border/70 bg-card/30">
                <div className="mx-auto w-full max-w-6xl px-6 py-14">
                    <div className="grid gap-10 md:grid-cols-[1.5fr_1fr_1fr_1fr]">
                        <div>
                            <div className="mb-4 flex items-center gap-3">
                                <Die size={24} face={6} roll={false} />
                                <span className="font-display text-card uppercase tracking-widest text-foreground">
                                    Erchis
                                </span>
                            </div>
                            <p className="max-w-xs text-body-sm text-muted-foreground">
                                A fantasy dice RPG. Eight races, eleven continents, one die that
                                decides all.
                            </p>
                        </div>

                        {FOOTER_GROUPS.map((g) => (
                            <div key={g.title}>
                                {/* Not a heading: footer column labels as <h2> put
                                    "Game / Community / Account" into the document
                                    outline on every page, competing with the real
                                    section headings a crawler should see. */}
                                <p className="mb-3 font-mono text-label uppercase text-primary/70">
                                    {g.title}
                                </p>
                                <ul className="space-y-2">
                                    {g.links.map((l) => (
                                        <li key={l.to}>
                                            <Link
                                                to={l.to}
                                                className="text-body-sm text-muted-foreground transition-colors hover:text-primary"
                                            >
                                                {l.label}
                                            </Link>
                                        </li>
                                    ))}
                                </ul>
                            </div>
                        ))}
                    </div>

                    <div className="mt-12 flex flex-wrap items-center justify-between gap-4 border-t border-border/50 pt-6">
                        <p className="font-mono text-caption uppercase text-muted-foreground/50">
                            © {new Date().getFullYear()} Erchis · A fantasy dice RPG
                        </p>
                        <Link
                            to="/changelog"
                            className="font-mono text-caption uppercase text-muted-foreground/50 hover:text-primary"
                        >
                            Changelog
                        </Link>
                    </div>
                </div>
            </footer>
        </div>
    );
}
