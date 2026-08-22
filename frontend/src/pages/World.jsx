import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import SiteLayout from "@/components/SiteLayout";
import { Globe, Skull, Sparkles } from "lucide-react";

export default function World() {
    const [continents, setContinents] = useState([]);
    const [monsters, setMonsters] = useState([]);
    const [items, setItems] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        Promise.all([
            api.get("/public/continents"),
            api.get("/public/monsters"),
            api.get("/public/items"),
        ]).then(([c, m, i]) => {
            setContinents(c.data.continents);
            setMonsters(m.data.monsters);
            setItems(i.data.items);
        }).catch(() => {}).finally(() => setLoading(false));
    }, []);

    const rarityColors = {
        common: "text-muted-foreground",
        uncommon: "text-green-500",
        rare: "text-blue-500",
        epic: "text-purple-500",
        legendary: "text-yellow-500",
        mythic: "text-red-500",
    };

    return (
        <SiteLayout>
            {/* Hero */}
            <section className="relative px-6 md:px-16 py-20 border-b border-border overflow-hidden">
                <div className="absolute inset-0 opacity-15" style={{
                    backgroundImage: "url(https://images.unsplash.com/photo-1532012197267-da84d127e864?q=80&w=2000&auto=format&fit=crop)",
                    backgroundSize: "cover", backgroundPosition: "center",
                }} />
                <div className="relative max-w-4xl">
                    <div className="stat-label text-primary/70 mb-2 flex items-center gap-2"><Globe size={14} /> THE WORLD</div>
                    <h1 className="font-pixel text-4xl md:text-6xl uppercase text-primary tracking-wider mb-4">Eleven Continents</h1>
                    <p className="narr text-lg md:text-xl text-muted-foreground max-w-2xl">
                        From the imperial halls of Valeria to the sunken depths of Hylion, each land holds its own biomes, monsters, and materials. Eight are peopled. Three are sealed — waiting.
                    </p>
                </div>
            </section>

            <div className="max-w-5xl mx-auto px-4 md:px-6 py-12">
                {loading && <div className="stat-label text-muted-foreground text-center py-20">Unfurling the map…</div>}

                {/* Continents */}
                {!loading && continents.length > 0 && (
                    <section className="mb-16">
                        <h2 className="font-pixel text-2xl uppercase text-primary mb-6">The Continents</h2>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            {continents.map((c) => (
                                <div key={c.id} className="panel p-6 hover:border-primary transition-colors">
                                    <div className="flex items-start justify-between mb-2">
                                        <div className="font-pixel text-xl uppercase text-primary">{c.name}</div>
                                        {c.biome && <span className="stat-label text-muted-foreground">{c.biome}</span>}
                                    </div>
                                    {c.description && <p className="narr text-sm text-muted-foreground">{c.description}</p>}
                                    {c.danger_level && <div className="stat-label mt-2 text-primary/70">Danger: {c.danger_level}</div>}
                                </div>
                            ))}
                        </div>
                    </section>
                )}

                {/* Bestiary Preview */}
                {!loading && monsters.length > 0 && (
                    <section className="mb-16">
                        <h2 className="font-pixel text-2xl uppercase text-primary mb-2 flex items-center gap-2"><Skull size={18} /> Bestiary Preview</h2>
                        <p className="narr text-sm text-muted-foreground mb-6">A glimpse of the creatures roaming the wilds.</p>
                        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                            {monsters.slice(0, 16).map((m) => (
                                <div key={m.id} className="panel p-4">
                                    <div className="font-pixel text-sm uppercase text-primary">{m.name}</div>
                                    {m.tier && <div className="stat-label text-muted-foreground mt-1">{m.tier}</div>}
                                    {m.continent && <div className="stat-label text-muted-foreground/60 mt-1">{m.continent}</div>}
                                </div>
                            ))}
                        </div>
                    </section>
                )}

                {/* Materials */}
                {!loading && items.length > 0 && (
                    <section>
                        <h2 className="font-pixel text-2xl uppercase text-primary mb-2 flex items-center gap-2"><Sparkles size={18} /> Materials & Rarity</h2>
                        <p className="narr text-sm text-muted-foreground mb-6">Six tiers from Common to Mythic. Every craft begins with the land.</p>
                        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                            {items.slice(0, 16).map((it) => (
                                <div key={it.id} className="panel p-4">
                                    <div className="font-pixel text-sm uppercase text-primary">{it.name}</div>
                                    <div className={`stat-label mt-1 ${rarityColors[it.rarity] || "text-muted-foreground"}`}>{it.rarity || "common"}</div>
                                </div>
                            ))}
                        </div>
                    </section>
                )}
            </div>
        </SiteLayout>
    );
}
