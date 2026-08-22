import { ScrollText } from "lucide-react";

const PATCHES = [
    {
        version: "v0.4.0",
        date: "Aug 2026",
        title: "Guild UI Redesign + Hall Buffs",
        changes: [
            "Redesigned guild UI: entrance → create/join → dashboard flow",
            "Three dashboard sub-tabs: Overview, Members, Hall",
            "Guild Hall buff system: 5 purchasable buffs (combat XP, crafting, gathering, trade, expedition)",
            "Buffs cost treasury gold, grandmaster only, 24h duration",
            "Hall unlocks at 3+ members",
        ],
    },
    {
        version: "v0.3.0",
        date: "Aug 2026",
        title: "Front Page Website + Blog System",
        changes: [
            "Dedicated Home, Login, Register pages with site layout",
            "World, Races, Mechanics info pages with live game data",
            "Blog system with categories, search, pagination",
            "Public leaderboard (no auth required)",
            "About page with roadmap",
        ],
    },
    {
        version: "v0.2.0",
        date: "Aug 2026",
        title: "Country Chat + Codebase Cleanup",
        changes: [
            "Country chat with polling, presence, and toast notifications",
            "Deep audit: removed 84 dead/unused files",
            "MongoDB TLS fix for Render deployment",
            "CORS configuration for Vercel frontend",
        ],
    },
    {
        version: "v0.1.0",
        date: "Jul 2026",
        title: "Initial Release",
        changes: [
            "8 playable races with unique perks and resources",
            "11 continents with biome-specific actions",
            "Turn-based dice combat with 6 outcomes",
            "Crafting system with 6 rarity tiers",
            "Guild system: create, join, leave, donate",
            "Character creation with race, mastery, origin, portrait",
        ],
    },
];

export const metadata = {
    title: "Patch notes",
    description:
        "Every change shipped to Erchis, newest first — balance passes, new systems and fixes.",
    alternates: { canonical: "/changelog" },
};

export default function ChangelogPage() {
    return (
        <>
            <div className="max-w-4xl mx-auto px-4 md:px-8 py-16">
                <div className="stat-label text-primary/70 mb-2 flex items-center gap-2"><ScrollText size={14} /> CHANGELOG</div>
                <h1 className="mb-12 font-display text-display uppercase text-foreground">Patch <span className="text-primary">notes</span></h1>

                <div className="space-y-8">
                    {PATCHES.map((p, i) => (
                        <div key={p.version} className="panel p-8">
                            <div className="flex items-center justify-between mb-4">
                                <div className="flex items-center gap-3">
                                    <span className="font-display text-card uppercase text-primary">{p.version}</span>
                                    {i === 0 && <span className="stat-label px-2 py-0.5 border border-primary text-primary">LATEST</span>}
                                </div>
                                <span className="stat-label text-muted-foreground">{p.date}</span>
                            </div>
                            <div className="font-pixel text-base uppercase text-primary/80 mb-4">{p.title}</div>
                            <ul className="space-y-2">
                                {p.changes.map((c, j) => (
                                    <li key={j} className="text-base text-muted-foreground flex items-start gap-2">
                                        <span className="text-primary mt-0.5">▸</span> {c}
                                    </li>
                                ))}
                            </ul>
                        </div>
                    ))}
                </div>
            </div>
        </>
    );
}
