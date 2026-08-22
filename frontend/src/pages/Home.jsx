import { Link } from "react-router-dom";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import SiteLayout from "@/components/SiteLayout";
import { Dices, Swords, Sparkles, Map, Skull, ScrollText, Users, Zap, Newspaper, Trophy, ArrowRight } from "lucide-react";

const FEATURES = [
    { icon: Dices,    title: "Weighted D6 Fate",  desc: "Every action is a dice throw. 6 outcomes. 20+ narratives each. Your strength shifts the odds — but never guarantees them." },
    { icon: Swords,   title: "Turn-Based Combat", desc: "Auto-selected skills, item triggers, manual override when it matters. Dice narrative meets tactical depth." },
    { icon: Map,      title: "Eleven Continents", desc: "Valeria, Mushkara, Concordia, Khardrum, Haya, Gennel, Hylion, Daw'ul Talalu, Azurea, Vael'Turog, Orinth. Each biome, its own monsters and materials." },
    { icon: Sparkles, title: "Erchis Lore",       desc: "8 playable races with unique perks — Sacred Oaths, Sun-and-Moon magic, Zone-triggers, aquatic sovereignty." },
    { icon: Skull,    title: "Crafting & Rarity", desc: "Six-tier rarity from Common to Mythic. Craft with materials from every corner of the world." },
    { icon: ScrollText, title: "Skillbooks & Teachers", desc: "Learn from wandering masters or hunt rare skillbooks dropped by monsters." },
];

const RACE_CARDS = [
    { name: "Human",       tag: "Sacred Oath" },
    { name: "Elf",         tag: "Sun & Moon" },
    { name: "Dwarf",       tag: "Mountain Resilience" },
    { name: "Half-Elf",    tag: "Dual Heritage" },
    { name: "Orc",         tag: "Blood of the Liberated" },
    { name: "Wildblood",   tag: "The Zone" },
    { name: "Hyliondrian", tag: "Children of the Sea" },
    { name: "Sylvan",      tag: "Shrink" },
];

function fmtDate(s) {
    if (!s) return "";
    return new Date(s).toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" });
}

export default function Landing() {
    const [posts, setPosts] = useState([]);
    const [leaders, setLeaders] = useState([]);

    useEffect(() => {
        api.get("/blog?limit=3").then(r => setPosts(r.data.posts)).catch(() => {});
        api.get("/public/leaderboard").then(r => setLeaders(r.data.leaderboard.slice(0, 5))).catch(() => {});
    }, []);

    return (
        <SiteLayout>
            {/* HERO */}
            <section className="relative min-h-[88vh] flex flex-col justify-center px-6 md:px-16 py-24 overflow-hidden">
                <div
                    className="absolute inset-0 opacity-30"
                    style={{
                        backgroundImage: "url(https://images.unsplash.com/photo-1605806616949-1e87b487cb2a?q=80&w=2000&auto=format&fit=crop)",
                        backgroundSize: "cover",
                        backgroundPosition: "center",
                        filter: "grayscale(0.6) contrast(1.1)",
                    }}
                />
                <div className="absolute inset-0 bg-gradient-to-b from-background/40 via-background/85 to-background pointer-events-none" />
                <div className="relative max-w-5xl">
                    <div className="stat-label mb-4 text-primary/80">A FANTASY DICE RPG · MULTIPLAYER · ERCHIS</div>
                    <h1 className="font-pixel text-5xl md:text-7xl lg:text-8xl leading-[0.9] tracking-wide">
                        <span className="text-foreground">ROLL THE</span>
                        <br />
                        <span className="text-primary">BONES OF</span>
                        <br />
                        <span className="text-foreground">ERCHIS</span>
                    </h1>
                    <p className="narr text-xl md:text-2xl max-w-2xl mt-8 text-foreground/85">
                        Eight races. Eleven continents. One six-sided die that will decide
                        whether you become legend — or footnote.
                    </p>
                    <div className="flex flex-wrap gap-4 mt-12">
                        <Link
                            to="/register"
                            data-testid="landing-cta-play"
                            className="press-btn font-pixel text-2xl uppercase px-8 py-3 bg-primary text-primary-foreground border-2 border-primary hover:bg-transparent hover:text-primary transition-colors"
                            style={{ boxShadow: "4px 4px 0 0 hsl(var(--destructive))" }}
                        >
                            Begin Your Saga
                        </Link>
                        <Link
                            to="/world"
                            className="press-btn font-pixel text-2xl uppercase px-8 py-3 bg-transparent text-primary border-2 border-primary hover:bg-primary hover:text-primary-foreground transition-colors"
                        >
                            Explore the World
                        </Link>
                    </div>
                    <div className="mt-16 flex items-center gap-6 stat-label flex-wrap">
                        <span>d6 · 20+ narratives</span><span className="opacity-40">|</span>
                        <span>Shared world · Global ladder</span><span className="opacity-40">|</span>
                        <span>No energy caps · Play at your pace</span>
                    </div>
                </div>
            </section>

            {/* FEATURES BENTO */}
            <section className="px-6 md:px-16 py-24">
                <div className="stat-label text-primary/70 mb-3">.SECTION_02 // MECHANICS</div>
                <h2 className="font-pixel text-3xl md:text-5xl uppercase mb-16 max-w-3xl">
                    The dice do not care <span className="text-primary">who you are.</span><br />
                    But your gear, race, and cunning tilt the throw.
                </h2>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {FEATURES.map((f, i) => {
                        const Ic = f.icon;
                        return (
                            <div key={f.title} data-testid={`feature-card-${i}`} className="panel p-8 md:p-10 relative group">
                                <Ic className="text-primary mb-5" size={40} strokeWidth={1.5} />
                                <div className="font-pixel text-xl md:text-2xl uppercase text-primary mb-3 tracking-wider">{f.title}</div>
                                <div className="text-base text-muted-foreground leading-relaxed">{f.desc}</div>
                                <div className="absolute top-3 right-3 font-mono text-xs text-muted-foreground/50">0{i + 1}</div>
                            </div>
                        );
                    })}
                </div>
                <div className="mt-8">
                    <Link to="/mechanics" className="stat-label text-primary hover:underline flex items-center gap-1">
                        Read full mechanics <ArrowRight size={12} />
                    </Link>
                </div>
            </section>

            {/* RACES */}
            <section className="px-6 md:px-16 py-24 border-t border-border">
                <div className="stat-label text-primary/70 mb-3">.SECTION_03 // BLOODLINES</div>
                <h2 className="font-pixel text-3xl md:text-5xl uppercase mb-4">Eight Playable Races</h2>
                <p className="narr text-lg max-w-2xl text-muted-foreground mb-12">
                    From the sworn Humans of the great Empire to the shrinking Sylvans of Daw&apos;ul Talalu, every bloodline shapes your destiny.
                </p>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    {RACE_CARDS.map((r, i) => (
                        <Link
                            key={r.name}
                            to="/races"
                            data-testid={`race-preview-${r.name.toLowerCase()}`}
                            className="panel p-8 hover:border-primary transition-colors block"
                        >
                            <div className="font-pixel text-xl md:text-2xl uppercase text-primary">{r.name}</div>
                            <div className="stat-label mt-2 text-sm">{r.tag}</div>
                            <div className="mt-5 font-mono text-xs text-muted-foreground/60">race_{String(i).padStart(2, "0")}</div>
                        </Link>
                    ))}
                </div>
            </section>

            {/* LEADERBOARD PREVIEW */}
            {leaders.length > 0 && (
                <section className="px-6 md:px-16 py-24 border-t border-border">
                    <div className="stat-label text-primary/70 mb-3">.SECTION_04 // LEGENDS</div>
                    <h2 className="font-pixel text-3xl md:text-5xl uppercase mb-12">Heroes of the Ladder</h2>
                    <div className="panel p-8 max-w-3xl">
                        {leaders.map((p, i) => (
                            <div key={p.id} className="flex items-center justify-between border-b border-border/40 py-4 last:border-0">
                                <div className="flex items-center gap-4">
                                    <div className={`font-pixel text-xl ${i === 0 ? "text-primary" : "text-muted-foreground"}`}>#{i + 1}</div>
                                    <div>
                                        <div className="font-mono text-base text-foreground">{p.name}</div>
                                        <div className="stat-label text-sm">{p.race} · {p.mastery}</div>
                                    </div>
                                </div>
                                <div className="font-pixel text-lg text-primary">Lv {p.level}</div>
                            </div>
                        ))}
                    </div>
                    <div className="mt-6">
                        <Link to="/leaderboard" className="stat-label text-primary hover:underline flex items-center gap-1">
                            View full leaderboard <ArrowRight size={12} />
                        </Link>
                    </div>
                </section>
            )}

            {/* LATEST BLOG POSTS */}
            {posts.length > 0 && (
                <section className="px-6 md:px-16 py-24 border-t border-border">
                    <div className="stat-label text-primary/70 mb-3">.SECTION_05 // CHRONICLES</div>
                    <h2 className="font-pixel text-3xl md:text-5xl uppercase mb-12">Latest from the Blog</h2>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                        {posts.map((p) => (
                            <Link key={p.slug} to={`/blog/${p.slug}`} className="panel p-8 hover:border-primary transition-colors block">
                                {p.hero_image && (
                                    <div className="mb-5 -mx-8 -mt-8 h-40 overflow-hidden border-b border-border">
                                        <img src={p.hero_image} alt={p.title} className="w-full h-full object-cover" />
                                    </div>
                                )}
                                <div className="stat-label text-primary/70 mb-2">{p.category}</div>
                                <div className="font-pixel text-lg uppercase text-primary mb-3">{p.title}</div>
                                <div className="text-base text-muted-foreground line-clamp-2">{p.excerpt}</div>
                                <div className="stat-label text-muted-foreground/60 mt-4">{fmtDate(p.published_at)}</div>
                            </Link>
                        ))}
                    </div>
                    <div className="mt-6">
                        <Link to="/blog" className="stat-label text-primary hover:underline flex items-center gap-1">
                            Read all posts <ArrowRight size={12} />
                        </Link>
                    </div>
                </section>
            )}

            {/* FINAL CTA */}
            <section className="px-6 md:px-16 py-32 border-t border-border">
                <div className="max-w-3xl">
                    <div className="stat-label text-primary/70 mb-3">.END_TRANSMISSION</div>
                    <h2 className="font-pixel text-4xl md:text-6xl uppercase leading-none mb-6">
                        The die is <span className="text-primary">cast.</span>
                    </h2>
                    <p className="narr text-xl md:text-2xl text-muted-foreground mb-10">
                        Six faces. One outcome. Everything else — the story between the rolls — is yours to write.
                    </p>
                    <Link
                        to="/register"
                        data-testid="landing-cta-bottom"
                        className="press-btn font-pixel text-2xl md:text-3xl uppercase px-10 py-4 bg-primary text-primary-foreground border-2 border-primary hover:bg-transparent hover:text-primary transition-colors"
                        style={{ boxShadow: "5px 5px 0 0 hsl(var(--destructive))" }}
                    >
                        Enter Erchis →
                    </Link>
                </div>
            </section>
        </SiteLayout>
    );
}
