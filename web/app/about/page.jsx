import Link from "next/link";
import { Info, ScrollText, Newspaper, Code, Zap } from "lucide-react";

export const metadata = {
    title: "About",
    description:
        "What Erchis is, who builds it, and the stack behind a browser fantasy RPG resolved entirely by one six-sided die.",
    alternates: { canonical: "/about" },
};

export default function AboutPage() {
    return (
        <>
            <div className="max-w-4xl mx-auto px-4 md:px-8 py-16">
                <div className="stat-label text-primary/70 mb-2 flex items-center gap-2"><Info size={14} /> ABOUT</div>
                <h1 className="mb-8 font-display text-display uppercase text-foreground">About <span className="text-primary">Erchis</span></h1>

                <div className="space-y-6">
                    <div className="panel p-8">
                        <h2 className="font-display text-card uppercase text-primary mb-3">What is Erchis?</h2>
                        <p className="text-body text-foreground/85 leading-relaxed">
                            Erchis is a browser-based fantasy dice RPG where every action is resolved by a single six-sided die.
                            Eight playable races, eleven continents, turn-based combat, crafting, guilds, and a shared world
                            with a global leaderboard. No downloads, no energy caps — just you, your stats, and the dice.
                        </p>
                    </div>

                    <div className="panel p-8">
                        <h2 className="font-display text-card uppercase text-primary mb-3">Tech Stack</h2>
                        <div className="grid grid-cols-2 gap-3 text-base">
                            <div className="flex items-center gap-2"><Code size={14} className="text-primary" /> FastAPI (Python)</div>
                            <div className="flex items-center gap-2"><Code size={14} className="text-primary" /> MongoDB Atlas</div>
                            <div className="flex items-center gap-2"><Code size={14} className="text-primary" /> React + CRACO</div>
                            <div className="flex items-center gap-2"><Code size={14} className="text-primary" /> Tailwind CSS</div>
                            <div className="flex items-center gap-2"><Code size={14} className="text-primary" /> shadcn/ui</div>
                            <div className="flex items-center gap-2"><Code size={14} className="text-primary" /> Render + Vercel</div>
                        </div>
                    </div>

                    <div className="panel p-8">
                        <h2 className="font-display text-card uppercase text-primary mb-3">Roadmap</h2>
                        <div className="space-y-3">
                            <div className="flex items-start gap-3">
                                <Zap size={14} className="text-primary mt-1" />
                                <div>
                                    <div className="font-pixel text-sm uppercase text-primary">Guild Hall Buffs</div>
                                    <div className="text-base text-muted-foreground">Treasury-funded server-wide buffs for guild members.</div>
                                </div>
                            </div>
                            <div className="flex items-start gap-3">
                                <Zap size={14} className="text-primary mt-1" />
                                <div>
                                    <div className="font-pixel text-sm uppercase text-primary">Blog & Community</div>
                                    <div className="text-base text-muted-foreground">Devlogs, lore entries, patch notes, and community guides.</div>
                                </div>
                            </div>
                            <div className="flex items-start gap-3">
                                <Zap size={14} className="text-primary mt-1" />
                                <div>
                                    <div className="font-pixel text-sm uppercase text-primary">PvP Arena</div>
                                    <div className="text-base text-muted-foreground">Challenge other players in ranked dice combat.</div>
                                </div>
                            </div>
                            <div className="flex items-start gap-3">
                                <Zap size={14} className="text-primary mt-1" />
                                <div>
                                    <div className="font-pixel text-sm uppercase text-primary">Expeditions</div>
                                    <div className="text-base text-muted-foreground">Send parties on timed missions for rare rewards.</div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div className="panel p-8">
                        <h2 className="font-display text-card uppercase text-primary mb-3">Community</h2>
                        <div className="flex gap-3 flex-wrap">
                            <Link href="/blog" className="press-btn stat-label px-4 py-2 border border-border text-muted-foreground hover:text-primary hover:border-primary flex items-center gap-2">
                                <Newspaper size={14} /> Blog
                            </Link>
                            <Link href="/changelog" className="press-btn stat-label px-4 py-2 border border-border text-muted-foreground hover:text-primary hover:border-primary flex items-center gap-2">
                                <ScrollText size={14} /> Changelog
                            </Link>
                            <a href="https://github.com/crynxmartinez/erchistorn" target="_blank" rel="noopener noreferrer" className="press-btn stat-label px-4 py-2 border border-border text-muted-foreground hover:text-primary hover:border-primary flex items-center gap-2">
                                <Code size={14} /> GitHub
                            </a>
                        </div>
                    </div>
                </div>

                <div className="mt-12 text-center border-t border-border pt-8">
                    <p className="text-body text-muted-foreground">
                        Erchis is built by a solo developer. The dice are loaded, the world is vast, and the saga continues.
                    </p>
                </div>
            </div>
        </>
    );
}
