import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import SiteLayout from "@/components/SiteLayout";
import { Globe, Skull, Sparkles, Lock, MapPin, Home, Sword, Shield, FlaskConical, ScrollText, MessageSquare, Beer, ShoppingBag, TrainFront, ChevronLeft, ChevronRight } from "lucide-react";

const RACE_ICONS = {
    human: "🛡", elf: "🌙", dwarf: "⛏", half_elf: "⚖", orc: "⚔", wildblood: "🐺", hyliondrian: "🌊", sylvan: "🌿",
};

const SERVICE_ICONS = {
    sanctuary: Shield, market: ShoppingBag, trainers: Sword, notice_board: MessageSquare, tavern: Beer, alchemist: FlaskConical, training_main: TrainFront,
};

const TIER_COLORS = {
    normal: "text-muted-foreground", mini_boss: "text-blue-400", boss: "text-purple-400", legendary: "text-yellow-400", event: "text-red-400",
};

const RARITY_COLORS = {
    common: "text-muted-foreground", uncommon: "text-green-500", rare: "text-blue-500", epic: "text-purple-500", legendary: "text-yellow-500", mythic: "text-red-500",
};

const TABS = [
    { id: "continents", label: "Continents" },
    { id: "biomes", label: "Biomes" },
    { id: "towns", label: "Towns" },
    { id: "bestiary", label: "Bestiary" },
    { id: "materials", label: "Materials" },
    { id: "lore", label: "Lore" },
];

const LORE_SECTIONS = [
    { title: "The Founding of the Eight Peoples", body: "Before the dice were carved, before the continents were named, there were eight peoples — Human, Elf, Dwarf, Half-Elf, Orc, Wildblood, Hyliondrian, and Sylvan. Each emerged from a different cradle: the plains, the forests, the mountains, the trade roads, the battlefields, the wilds, the deep sea, and the mist. They did not choose their homes. Their homes chose them." },
    { title: "The Great Tree of Haya", body: "In the heart of the Elven continent stands the Great Tree of Haya — the last living root of the world's first forest. Its leaves catch both sun and moon, and its roots are said to reach every continent beneath the sea. The Elves built their cities around it, and the Tree has watched every war, every peace, and every fall." },
    { title: "The Demon Invasion & Azurea's Fall", body: "Azurea was once the ninth continent — green, proud, and full of life. Then came the demonic storms. Portals tore open across the land, and the heroes who went to seal them were corrupted. Azurea is now surrounded by unstable portals and demonic storms. No one who has entered has returned sane." },
    { title: "The Orc Liberation", body: "The Orcs of Mushkara were not always free. They were forged in chains, in the forges of a forgotten empire. One day, a smith named Zaheer broke his chains and led a rebellion that shattered the old order. Every forge in Mushkara still carries the memory of that broken chain. The Orcs turned their prison into a stronghold, and their stronghold into a nation." },
    { title: "The Three Sealed Continents", body: "Azurea, Vael'Turog, and Orinth — three continents locked behind storms, shrouds, and divine wards. Azurea fell to demonic corruption. Vael'Turog hides behind a permanent supernatural storm, its civilizations unknown. Orinth is the First Continent, believed to hold the resting places of gods and the source of the Mythicodes. None have been entered in living memory." },
    { title: "The Mythicodes", body: "Ancient tablets speak of the Mythicodes — artifacts of divine origin that predate the eight peoples. They are said to grant abilities beyond the dice, beyond the stats, beyond the world itself. No Mythicode has ever been found. But the myths say they sleep in Orinth, waiting for someone worthy enough to wake them." },
    { title: "The Grand Teleporter", body: "Built in the age of cooperation, the Grand Teleporter connects all eight accessible continents. A Lv-1 traveler can step from the Golden Plains of Valeria to the Tide Pools of Hylion in a heartbeat. The locked continents are not on the network. Their coordinates were erased when the seals were placed." },
];

export default function World() {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [tab, setTab] = useState("continents");
    const [selectedContinent, setSelectedContinent] = useState(0);
    const [selectedBiome, setSelectedBiome] = useState(0);
    const [selectedTown, setSelectedTown] = useState(0);
    const [bestiaryFilter, setBestiaryFilter] = useState("all");
    const [materialFilter, setMaterialFilter] = useState("all");

    useEffect(() => {
        api.get("/public/world").then(r => setData(r.data)).catch(() => {}).finally(() => setLoading(false));
    }, []);

    const continents = data?.continents || [];
    const allBiomes = data?.all_biomes || [];
    const allTowns = data?.all_towns || [];
    const allMonsters = data?.all_monsters || [];
    const allItems = data?.all_items || [];

    const unlockedContinents = continents.filter(c => !c.locked);
    const lockedContinents = continents.filter(c => c.locked);
    const activeContinent = continents[selectedContinent];

    const filteredMonsters = bestiaryFilter === "all" ? allMonsters : allMonsters.filter(m => m.biomes?.some(b => {
        const biome = allBiomes.find(ab => ab.id === b);
        return biome?.continent === bestiaryFilter;
    }));

    const filteredItems = materialFilter === "all" ? allItems : allItems.filter(it => it.biomes?.some(b => {
        const biome = allBiomes.find(ab => ab.id === b);
        return biome?.continent === materialFilter;
    }));

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
                    <h1 className="font-pixel text-4xl md:text-6xl uppercase text-primary tracking-wider mb-4">The World of Erchis</h1>
                    <p className="narr text-lg md:text-xl text-muted-foreground max-w-2xl">
                        Eleven continents. Thirty biomes. Sixteen towns. Hundreds of creatures and materials. Explore every corner of the world — from the imperial halls of Valeria to the sunken depths of Hylion.
                    </p>
                </div>
            </section>

            {/* Tabs */}
            <div className="sticky top-20 z-40 bg-background/95 backdrop-blur-sm border-b border-border">
                <div className="max-w-7xl mx-auto px-4 md:px-8 flex gap-1 overflow-x-auto no-scrollbar">
                    {TABS.map(t => (
                        <button
                            key={t.id}
                            onClick={() => setTab(t.id)}
                            className={`px-5 py-4 font-pixel text-sm uppercase whitespace-nowrap transition-colors border-b-2 ${
                                tab === t.id ? "text-primary border-primary" : "text-muted-foreground border-transparent hover:text-foreground"
                            }`}
                        >
                            {t.label}
                        </button>
                    ))}
                </div>
            </div>

            <div className="max-w-7xl mx-auto px-4 md:px-8 py-12">
                {loading && <div className="stat-label text-muted-foreground text-center py-20">Unfurling the map…</div>}

                {/* ===== CONTINENTS TAB ===== */}
                {!loading && tab === "continents" && activeContinent && (
                    <div className="grid grid-cols-1 lg:grid-cols-[280px_1fr] gap-6">
                        {/* Slider */}
                        <div className="space-y-1">
                            <div className="stat-label text-primary/60 mb-3 px-2">UNLOCKED ({unlockedContinents.length})</div>
                            {unlockedContinents.map((c, i) => {
                                const idx = continents.indexOf(c);
                                return (
                                    <button
                                        key={c.id}
                                        onClick={() => setSelectedContinent(idx)}
                                        className={`w-full text-left px-4 py-3 transition-colors border-l-4 ${
                                            selectedContinent === idx ? "border-primary bg-primary/5 text-primary" : "border-transparent text-muted-foreground hover:text-foreground hover:bg-muted/30"
                                        }`}
                                    >
                                        <div className="font-pixel text-lg uppercase">{c.name}</div>
                                        <div className="stat-label mt-1 flex items-center gap-1">
                                            <span>{RACE_ICONS[c.home_race] || "⚜"}</span>
                                            <span>Lv {c.level_req}+</span>
                                        </div>
                                    </button>
                                );
                            })}
                            {lockedContinents.length > 0 && (
                                <div className="stat-label text-primary/60 mb-2 mt-6 px-2">SEALED ({lockedContinents.length})</div>
                            )}
                            {lockedContinents.map((c) => {
                                const idx = continents.indexOf(c);
                                return (
                                    <button
                                        key={c.id}
                                        onClick={() => setSelectedContinent(idx)}
                                        className={`w-full text-left px-4 py-3 transition-colors border-l-4 ${
                                            selectedContinent === idx ? "border-primary bg-primary/5 text-primary" : "border-transparent text-muted-foreground/50 hover:text-muted-foreground hover:bg-muted/20"
                                        }`}
                                    >
                                        <div className="font-pixel text-lg uppercase flex items-center gap-2">
                                            <Lock size={14} /> {c.name}
                                        </div>
                                        <div className="stat-label mt-1">Sealed</div>
                                    </button>
                                );
                            })}
                        </div>

                        {/* Detail Panel */}
                        <div className="panel p-8 md:p-10" key={activeContinent.id}>
                            <div className="fade-in">
                                {/* Header */}
                                <div className="flex items-start justify-between mb-4">
                                    <div>
                                        <h2 className="font-pixel text-3xl md:text-4xl uppercase text-primary tracking-wider mb-2">
                                            {activeContinent.locked && <Lock size={24} className="inline mr-2" />}
                                            {activeContinent.name}
                                        </h2>
                                        {activeContinent.home_race && (
                                            <div className="stat-label flex items-center gap-2">
                                                <Home size={12} /> Home: {RACE_ICONS[activeContinent.home_race] || "⚜"} {activeContinent.home_race.replace("_", " ")}
                                            </div>
                                        )}
                                    </div>
                                    <div className="stat-label text-primary/70 text-right">
                                        {activeContinent.locked ? "SEALED" : `Lv ${activeContinent.level_req}+`}
                                    </div>
                                </div>

                                <p className="narr text-base text-foreground/85 mb-6">{activeContinent.desc}</p>

                                {activeContinent.specialty && (
                                    <div className="mb-4 border-l-2 border-primary/40 pl-5">
                                        <div className="stat-label text-primary/80">SPECIALTY</div>
                                        <div className="text-base text-foreground/85">{activeContinent.specialty}</div>
                                    </div>
                                )}

                                {activeContinent.bonus_desc && (
                                    <div className="mb-6 border-l-2 border-primary/40 pl-5">
                                        <div className="stat-label text-primary/80">CONTINENTAL BONUS</div>
                                        <div className="text-base text-foreground/85">{activeContinent.bonus_desc}</div>
                                    </div>
                                )}

                                {/* Biomes */}
                                {activeContinent.biomes?.length > 0 && (
                                    <div className="mb-8">
                                        <div className="stat-label text-primary/60 mb-3">BIOMES ({activeContinent.biomes.length})</div>
                                        <div className="space-y-2">
                                            {activeContinent.biomes.map(b => (
                                                <div key={b.id} className="flex items-start gap-4 py-2 border-b border-border/30">
                                                    <div className="font-pixel text-lg text-primary whitespace-nowrap min-w-[180px]">{b.name}</div>
                                                    <div className="flex-1">
                                                        <div className="text-base text-muted-foreground">{b.desc}</div>
                                                        <div className="stat-label text-primary/70 mt-1">Lv {b.level_req}+</div>
                                                    </div>
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                )}

                                {/* Regions */}
                                {activeContinent.regions?.length > 0 && (
                                    <div className="mb-8">
                                        <div className="stat-label text-primary/60 mb-3">REGIONS ({activeContinent.regions.length})</div>
                                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                            {activeContinent.regions.map(r => (
                                                <div key={r.id} className="border border-border/50 p-5">
                                                    <div className="font-pixel text-lg text-primary mb-1">{r.name}</div>
                                                    <div className="text-base text-muted-foreground mb-2">{r.desc}</div>
                                                    {r.town_ids?.length > 0 && (
                                                        <div className="stat-label flex items-center gap-1"><MapPin size={10} /> {r.town_ids.map(t => t.replace(/_/g, " ")).join(", ")}</div>
                                                    )}
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                )}

                                {/* Towns */}
                                {activeContinent.towns?.length > 0 && (
                                    <div className="mb-8">
                                        <div className="stat-label text-primary/60 mb-3">TOWNS ({activeContinent.towns.length})</div>
                                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                            {activeContinent.towns.map(t => (
                                                <div key={t.id} className="border border-border/50 p-5">
                                                    <div className="flex items-start justify-between mb-2">
                                                        <div className="font-pixel text-lg text-primary">{t.name}</div>
                                                        <div className="stat-label text-muted-foreground">{t.type?.replace(/_/g, " ")}</div>
                                                    </div>
                                                    <div className="text-base text-muted-foreground mb-3">{t.desc}</div>
                                                    {t.specialty && (
                                                        <div className="stat-label text-primary/70 mb-2">★ {t.specialty}</div>
                                                    )}
                                                    {t.services?.length > 0 && (
                                                        <div className="flex flex-wrap gap-2">
                                                            {t.services.map(s => {
                                                                const Ic = SERVICE_ICONS[s] || null;
                                                                return (
                                                                    <span key={s} className="stat-label px-2 py-1 border border-border/50 flex items-center gap-1">
                                                                        {Ic && <Ic size={10} />} {s.replace(/_/g, " ")}
                                                                    </span>
                                                                );
                                                            })}
                                                        </div>
                                                    )}
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                )}

                                {/* Monsters */}
                                {activeContinent.monsters?.length > 0 && (
                                    <div className="mb-8">
                                        <div className="stat-label text-primary/60 mb-3">BESTIARY ({activeContinent.monsters.length})</div>
                                        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                                            {activeContinent.monsters.slice(0, 24).map(m => (
                                                <div key={m.id} className="border border-border/50 p-4">
                                                    <div className="font-pixel text-base text-primary">{m.name}</div>
                                                    <div className={`stat-label mt-1 ${TIER_COLORS[m.tier] || "text-muted-foreground"}`}>{m.tier}</div>
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                )}

                                {/* Materials */}
                                {activeContinent.materials?.length > 0 && (
                                    <div>
                                        <div className="stat-label text-primary/60 mb-3">MATERIALS ({activeContinent.materials.length})</div>
                                        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                                            {activeContinent.materials.slice(0, 24).map(it => (
                                                <div key={it.id} className="border border-border/50 p-4">
                                                    <div className="font-pixel text-base text-primary">{it.name}</div>
                                                    <div className={`stat-label mt-1 ${RARITY_COLORS[it.rarity] || "text-muted-foreground"}`}>{it.rarity}</div>
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                )}

                                {/* Locked continent flavor */}
                                {activeContinent.locked && (
                                    <div className="mt-6 p-6 border-2 border-dashed border-primary/20 text-center">
                                        <Lock size={32} className="text-primary/40 mx-auto mb-3" />
                                        <div className="narr text-base text-muted-foreground">This continent is sealed. No traveler has entered in living memory. The storms have not subsided.</div>
                                    </div>
                                )}
                            </div>
                        </div>
                    </div>
                )}

                {/* ===== BIOMES TAB ===== */}
                {!loading && tab === "biomes" && (
                    <div className="grid grid-cols-1 lg:grid-cols-[280px_1fr] gap-6">
                        {/* Slider */}
                        <div className="space-y-1 max-h-[600px] overflow-y-auto">
                            {continents.filter(c => !c.locked).map(c => (
                                <div key={c.id}>
                                    <div className="stat-label text-primary/60 mb-2 mt-4 px-2 sticky top-0 bg-background/95">{c.name}</div>
                                    {c.biomes.map(b => {
                                        const idx = allBiomes.findIndex(ab => ab.id === b.id);
                                        return (
                                            <button
                                                key={b.id}
                                                onClick={() => setSelectedBiome(idx)}
                                                className={`w-full text-left px-4 py-2.5 transition-colors border-l-4 ${
                                                    selectedBiome === idx ? "border-primary bg-primary/5 text-primary" : "border-transparent text-muted-foreground hover:text-foreground hover:bg-muted/30"
                                                }`}
                                            >
                                                <div className="font-pixel text-base uppercase">{b.name}</div>
                                                <div className="stat-label mt-0.5">Lv {b.level_req}+</div>
                                            </button>
                                        );
                                    })}
                                </div>
                            ))}
                        </div>

                        {/* Detail */}
                        {allBiomes[selectedBiome] && (
                            <div className="panel p-8 md:p-10" key={allBiomes[selectedBiome].id}>
                                <div className="fade-in">
                                    <div className="flex items-start justify-between mb-4">
                                        <h2 className="font-pixel text-3xl uppercase text-primary tracking-wider mb-2">{allBiomes[selectedBiome].name}</h2>
                                        <div className="stat-label text-primary/70">Lv {allBiomes[selectedBiome].level_req}+</div>
                                    </div>
                                    <div className="stat-label text-primary/60 mb-4 flex items-center gap-1"><MapPin size={12} /> {allBiomes[selectedBiome].continent_name}</div>
                                    <p className="narr text-base text-foreground/85 mb-6">{allBiomes[selectedBiome].desc}</p>

                                    {allBiomes[selectedBiome].monsters?.length > 0 && (
                                        <div className="mb-6">
                                            <div className="stat-label text-primary/60 mb-3">CREATURES ({allBiomes[selectedBiome].monsters.length})</div>
                                            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                                                {allBiomes[selectedBiome].monsters.map(m => (
                                                    <div key={m.id} className="border border-border/50 p-4">
                                                        <div className="font-pixel text-base text-primary">{m.name}</div>
                                                        <div className={`stat-label mt-1 ${TIER_COLORS[m.tier] || "text-muted-foreground"}`}>{m.tier}</div>
                                                    </div>
                                                ))}
                                            </div>
                                        </div>
                                    )}

                                    {allBiomes[selectedBiome].materials?.length > 0 && (
                                        <div>
                                            <div className="stat-label text-primary/60 mb-3">GATHERABLES ({allBiomes[selectedBiome].materials.length})</div>
                                            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                                                {allBiomes[selectedBiome].materials.map(it => (
                                                    <div key={it.id} className="border border-border/50 p-4">
                                                        <div className="font-pixel text-base text-primary">{it.name}</div>
                                                        <div className={`stat-label mt-1 ${RARITY_COLORS[it.rarity] || "text-muted-foreground"}`}>{it.rarity}</div>
                                                    </div>
                                                ))}
                                            </div>
                                        </div>
                                    )}
                                </div>
                            </div>
                        )}
                    </div>
                )}

                {/* ===== TOWNS TAB ===== */}
                {!loading && tab === "towns" && (
                    <div className="grid grid-cols-1 lg:grid-cols-[280px_1fr] gap-6">
                        {/* Slider */}
                        <div className="space-y-1 max-h-[600px] overflow-y-auto">
                            {continents.filter(c => !c.locked).map(c => {
                                const contTowns = allTowns.filter(t => t.continent === c.id);
                                if (contTowns.length === 0) return null;
                                return (
                                    <div key={c.id}>
                                        <div className="stat-label text-primary/60 mb-2 mt-4 px-2 sticky top-0 bg-background/95">{c.name}</div>
                                        {contTowns.map(t => {
                                            const idx = allTowns.indexOf(t);
                                            return (
                                                <button
                                                    key={t.id}
                                                    onClick={() => setSelectedTown(idx)}
                                                    className={`w-full text-left px-4 py-2.5 transition-colors border-l-4 ${
                                                        selectedTown === idx ? "border-primary bg-primary/5 text-primary" : "border-transparent text-muted-foreground hover:text-foreground hover:bg-muted/30"
                                                    }`}
                                                >
                                                    <div className="font-pixel text-base uppercase">{t.name}</div>
                                                    <div className="stat-label mt-0.5">{t.type?.replace(/_/g, " ")}</div>
                                                </button>
                                            );
                                        })}
                                    </div>
                                );
                            })}
                        </div>

                        {/* Detail */}
                        {allTowns[selectedTown] && (
                            <div className="panel p-8 md:p-10" key={allTowns[selectedTown].id}>
                                <div className="fade-in">
                                    <div className="flex items-start justify-between mb-4">
                                        <div>
                                            <h2 className="font-pixel text-3xl uppercase text-primary tracking-wider mb-2">{allTowns[selectedTown].name}</h2>
                                            <div className="stat-label text-primary/60 flex items-center gap-1"><MapPin size={12} /> {allTowns[selectedTown].continent_name}</div>
                                        </div>
                                        <div className="stat-label text-muted-foreground">{allTowns[selectedTown].type?.replace(/_/g, " ")}</div>
                                    </div>

                                    <p className="narr text-base text-foreground/85 mb-6">{allTowns[selectedTown].desc}</p>

                                    {allTowns[selectedTown].specialty && (
                                        <div className="mb-6 border-l-2 border-primary/40 pl-5">
                                            <div className="stat-label text-primary/80">SPECIALTY</div>
                                            <div className="text-base text-foreground/85">{allTowns[selectedTown].specialty}</div>
                                        </div>
                                    )}

                                    <div className="mb-6">
                                        <div className="stat-label text-primary/60 mb-3">SERVICES</div>
                                        <div className="flex flex-wrap gap-3">
                                            {allTowns[selectedTown].services?.map(s => {
                                                const Ic = SERVICE_ICONS[s] || null;
                                                return (
                                                    <span key={s} className="px-3 py-2 border border-border/50 flex items-center gap-2 text-base">
                                                        {Ic && <Ic size={16} className="text-primary" />} {s.replace(/_/g, " ")}
                                                    </span>
                                                );
                                            })}
                                        </div>
                                    </div>

                                    <div className="grid grid-cols-2 gap-4">
                                        {allTowns[selectedTown].sanctuary_cost != null && (
                                            <div className="border border-border/50 p-4">
                                                <div className="stat-label text-primary/60">SANCTUARY COST</div>
                                                <div className="font-pixel text-lg text-primary mt-1">{allTowns[selectedTown].sanctuary_cost}g</div>
                                            </div>
                                        )}
                                        {allTowns[selectedTown].fast_travel_cost != null && (
                                            <div className="border border-border/50 p-4">
                                                <div className="stat-label text-primary/60">FAST TRAVEL</div>
                                                <div className="font-pixel text-lg text-primary mt-1">{allTowns[selectedTown].fast_travel_cost}g</div>
                                            </div>
                                        )}
                                    </div>

                                    {allTowns[selectedTown].trainer_ids?.length > 0 && (
                                        <div className="mt-6">
                                            <div className="stat-label text-primary/60 mb-2">TRAINERS</div>
                                            <div className="flex flex-wrap gap-2">
                                                {allTowns[selectedTown].trainer_ids.map(tid => (
                                                    <span key={tid} className="stat-label px-2 py-1 border border-border/50">{tid.replace(/_/g, " ")}</span>
                                                ))}
                                            </div>
                                        </div>
                                    )}
                                </div>
                            </div>
                        )}
                    </div>
                )}

                {/* ===== BESTIARY TAB ===== */}
                {!loading && tab === "bestiary" && (
                    <div>
                        <div className="flex flex-wrap gap-2 mb-8">
                            <button
                                onClick={() => setBestiaryFilter("all")}
                                className={`stat-label px-4 py-2 border ${bestiaryFilter === "all" ? "border-primary bg-primary text-primary-foreground" : "border-border text-muted-foreground hover:text-primary hover:border-primary"}`}
                            >All</button>
                            {unlockedContinents.map(c => (
                                <button
                                    key={c.id}
                                    onClick={() => setBestiaryFilter(c.id)}
                                    className={`stat-label px-4 py-2 border ${bestiaryFilter === c.id ? "border-primary bg-primary text-primary-foreground" : "border-border text-muted-foreground hover:text-primary hover:border-primary"}`}
                                >{c.name}</button>
                            ))}
                        </div>
                        <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-4">
                            {filteredMonsters.map(m => (
                                <div key={m.id} className="panel p-6 hover:border-primary transition-colors">
                                    <div className="font-pixel text-lg text-primary mb-2">{m.name}</div>
                                    <div className={`stat-label ${TIER_COLORS[m.tier] || "text-muted-foreground"}`}>{m.tier || "normal"}</div>
                                </div>
                            ))}
                        </div>
                        {filteredMonsters.length === 0 && (
                            <div className="stat-label text-muted-foreground text-center py-12">No creatures found.</div>
                        )}
                    </div>
                )}

                {/* ===== MATERIALS TAB ===== */}
                {!loading && tab === "materials" && (
                    <div>
                        <div className="flex flex-wrap gap-2 mb-8">
                            <button
                                onClick={() => setMaterialFilter("all")}
                                className={`stat-label px-4 py-2 border ${materialFilter === "all" ? "border-primary bg-primary text-primary-foreground" : "border-border text-muted-foreground hover:text-primary hover:border-primary"}`}
                            >All</button>
                            {unlockedContinents.map(c => (
                                <button
                                    key={c.id}
                                    onClick={() => setMaterialFilter(c.id)}
                                    className={`stat-label px-4 py-2 border ${materialFilter === c.id ? "border-primary bg-primary text-primary-foreground" : "border-border text-muted-foreground hover:text-primary hover:border-primary"}`}
                                >{c.name}</button>
                            ))}
                        </div>
                        <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-4">
                            {filteredItems.map(it => (
                                <div key={it.id} className="panel p-6 hover:border-primary transition-colors">
                                    <div className="font-pixel text-lg text-primary mb-2">{it.name}</div>
                                    <div className={`stat-label ${RARITY_COLORS[it.rarity] || "text-muted-foreground"}`}>{it.rarity || "common"}</div>
                                    <div className="stat-label text-muted-foreground/60 mt-1">{it.kind || "material"}</div>
                                </div>
                            ))}
                        </div>
                        {filteredItems.length === 0 && (
                            <div className="stat-label text-muted-foreground text-center py-12">No materials found.</div>
                        )}
                    </div>
                )}

                {/* ===== LORE TAB ===== */}
                {!loading && tab === "lore" && (
                    <div className="max-w-4xl mx-auto space-y-8">
                        {LORE_SECTIONS.map((s, i) => (
                            <div key={i} className="panel p-8">
                                <h2 className="font-pixel text-2xl uppercase text-primary mb-4 flex items-center gap-2">
                                    <ScrollText size={20} className="text-primary/70" /> {s.title}
                                </h2>
                                <p className="narr text-base text-foreground/85 leading-relaxed">{s.body}</p>
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </SiteLayout>
    );
}
