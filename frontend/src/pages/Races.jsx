import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "@/lib/api";
import SiteLayout from "@/components/SiteLayout";
import { Users, Crown } from "lucide-react";

const RACE_ICONS = {
    human: "🛡", elf: "🌙", dwarf: "⛏", half_elf: "⚖", orc: "⚔", wildblood: "🐺", hyliondrian: "🌊", sylvan: "🌿",
};

export default function Races() {
    const [races, setRaces] = useState([]);
    const [beastAspects, setBeastAspects] = useState([]);
    const [marineAdaptations, setMarineAdaptations] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        Promise.all([
            api.get("/public/races"),
            api.get("/public/beast_aspects"),
            api.get("/public/marine_adaptations"),
        ]).then(([r, ba, ma]) => {
            setRaces(r.data.races);
            setBeastAspects(ba.data.beast_aspects);
            setMarineAdaptations(ma.data.marine_adaptations);
        }).catch(() => {}).finally(() => setLoading(false));
    }, []);

    return (
        <SiteLayout>
            {/* Hero */}
            <section className="relative px-6 md:px-16 py-20 border-b border-border overflow-hidden">
                <div className="absolute inset-0 opacity-15" style={{
                    backgroundImage: "url(https://images.unsplash.com/photo-1518709268805-4e9042af2176?q=80&w=2000&auto=format&fit=crop)",
                    backgroundSize: "cover", backgroundPosition: "center",
                }} />
                <div className="relative max-w-4xl">
                    <div className="stat-label text-primary/70 mb-2 flex items-center gap-2"><Users size={14} /> BLOODLINES</div>
                    <h1 className="font-pixel text-4xl md:text-6xl uppercase text-primary tracking-wider mb-4">Eight Playable Races</h1>
                    <p className="narr text-lg md:text-xl text-muted-foreground max-w-2xl">
                        Each bloodline carries its own gift and its own price. From the sworn Humans to the shrinking Sylvans, your race shapes every roll.
                    </p>
                </div>
            </section>

            <div className="max-w-5xl mx-auto px-4 md:px-6 py-12">
                {loading && <div className="stat-label text-muted-foreground text-center py-20">Reading the bloodlines…</div>}

                {!loading && races.length > 0 && (
                    <div className="space-y-8">
                        {races.map((r) => (
                            <div key={r.id} className="panel p-6 md:p-8" data-testid={`race-detail-${r.id}`}>
                                <div className="flex items-start gap-4">
                                    <div className="text-5xl">{RACE_ICONS[r.id] || "⚜"}</div>
                                    <div className="flex-1">
                                        <div className="font-pixel text-2xl uppercase text-primary">{r.name}</div>
                                        {r.title && <div className="stat-label text-muted-foreground mb-2">{r.title}</div>}
                                        {r.story && <p className="narr text-sm text-foreground/85 mb-4">{r.story}</p>}
                                        {r.perk && (
                                            <div className="border-l-2 border-primary/40 pl-4">
                                                <div className="stat-label text-primary/80">RACIAL PERK — {r.perk.name}</div>
                                                <div className="text-sm text-foreground/80">{r.perk.desc}</div>
                                            </div>
                                        )}
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                )}

                {/* Beast Aspects */}
                {!loading && beastAspects.length > 0 && (
                    <section className="mt-12">
                        <h2 className="font-pixel text-2xl uppercase text-primary mb-4">Beast Aspects — Wildblood</h2>
                        <p className="narr text-sm text-muted-foreground mb-4">Choose your inner animal at creation. It shapes your instincts and gifts.</p>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                            {beastAspects.map((a) => (
                                <div key={a.id} className="panel p-4">
                                    <div className="font-pixel text-sm uppercase text-primary">{a.name}</div>
                                    <div className="stat-label text-muted-foreground italic mb-1">Kin of {a.examples}</div>
                                    <div className="text-sm text-foreground/80">{a.bonus_desc}</div>
                                </div>
                            ))}
                        </div>
                    </section>
                )}

                {/* Marine Adaptations */}
                {!loading && marineAdaptations.length > 0 && (
                    <section className="mt-12">
                        <h2 className="font-pixel text-2xl uppercase text-primary mb-4">Marine Adaptations — Hyliondrian</h2>
                        <p className="narr text-sm text-muted-foreground mb-4">The lineage of the deep that shaped your gills and instincts.</p>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                            {marineAdaptations.map((a) => (
                                <div key={a.id} className="panel p-4">
                                    <div className="font-pixel text-sm uppercase text-primary">{a.name}</div>
                                    <div className="text-sm text-foreground/80">{a.bonus_desc}</div>
                                </div>
                            ))}
                        </div>
                    </section>
                )}

                {/* CTA */}
                <div className="mt-16 text-center border-t border-border pt-12">
                    <h2 className="font-pixel text-3xl uppercase text-primary mb-4">Choose your bloodline</h2>
                    <Link to="/register" className="press-btn font-pixel text-xl uppercase px-8 py-3 bg-primary text-primary-foreground border-2 border-primary hover:bg-transparent hover:text-primary transition-colors">
                        Begin Your Saga
                    </Link>
                </div>
            </div>
        </SiteLayout>
    );
}
