import { useEffect, useMemo, useState } from "react";
import { Sheet, SheetContent, SheetTrigger, SheetTitle, SheetDescription } from "@/components/ui/sheet";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { ScrollArea } from "@/components/ui/scroll-area";
import { api } from "@/lib/api";
import PixelSprite from "@/components/PixelSprite";
import { BookOpen } from "lucide-react";
import { STAT_HINTS, STATUS_HINTS, EXHAUSTION_HINT, RESOLVE_HINT, RESOURCE_META, RACE_TO_RESOURCE, PROFESSION_HINT, EXPLORATION_HINT, NODE_HINT, CONTINENT_BONUS_HINT, REPUTATION_HINT } from "@/data/hints";

/**
 * JournalDrawer — a slide-in in-world manual (Codex).
 *
 * Pulls the exact same hint strings shown in tooltips into a scrollable manual
 * with tabs for Stats, Statuses, Races, World, Bestiary and Materials.
 * Data is loaded on-open only, then cached across re-opens for the session.
 */
export default function JournalDrawer({ triggerClassName, embedded }) {
    const [open, setOpen] = useState(false);
    const [tab, setTab] = useState("intro");
    const [data, setData] = useState(null); // {races, continents, monsters, items, beastAspects, marineAdaptations, heritage}
    const [discoveries, setDiscoveries] = useState(null);
    const [busy, setBusy] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        if (data || busy) return;
        if (!embedded && !open) return;
        setBusy(true);
        (async () => {
            try {
                const [r, c, m, i, ba, ma, h, d] = await Promise.all([
                    api.get("/game/data/races"),
                    api.get("/game/data/continents"),
                    api.get("/game/data/monsters"),
                    api.get("/game/data/items"),
                    api.get("/game/data/beast_aspects"),
                    api.get("/game/data/marine_adaptations"),
                    api.get("/game/data/heritage"),
                    api.get("/game/discoveries"),
                ]);
                setData({
                    races: r.data.races,
                    continents: c.data.continents,
                    monsters: m.data.monsters,
                    items: i.data.items,
                    beastAspects: ba.data.beast_aspects,
                    marineAdaptations: ma.data.marine_adaptations,
                    heritage: h.data.heritage_rank_1,
                });
                setDiscoveries(d.data.biomes);
            } catch (e) {
                setError(e?.response?.data?.detail || "Codex sealed. Try again.");
            } finally {
                setBusy(false);
            }
        })();
    }, [open, data, busy, embedded]);

    const codexTabs = (
        <Tabs value={tab} onValueChange={setTab} className="flex flex-col flex-1 overflow-hidden">
            <TabsList className="rounded-none border-b border-border bg-transparent p-0 h-auto flex-wrap justify-start">
                {[
                    { id: "intro",     label: "Preface" },
                    { id: "stats",     label: "Stats" },
                    { id: "statuses",  label: "Statuses" },
                    { id: "races",     label: "Races" },
                    { id: "world",     label: "World" },
                    { id: "discoveries", label: "Discoveries" },
                    { id: "bestiary",  label: "Bestiary" },
                    { id: "materials", label: "Materials" },
                ].map((t) => (
                    <TabsTrigger
                        key={t.id}
                        value={t.id}
                        data-testid={`journal-tab-${t.id}`}
                        className="rounded-none border-r border-border data-[state=active]:bg-primary data-[state=active]:text-primary-foreground font-pixel uppercase text-sm px-3 py-2"
                    >
                        {t.label}
                    </TabsTrigger>
                ))}
            </TabsList>

            <ScrollArea className="flex-1 overflow-hidden">
                <div className="p-6 min-h-full" data-testid="journal-body">
                    {busy && <BusyNote />}
                    {error && !busy && <ErrorNote message={error} />}
                    {data && !busy && (
                        <>
                            <TabsContent value="intro"><Preface /></TabsContent>
                            <TabsContent value="stats"><StatsPage /></TabsContent>
                            <TabsContent value="statuses"><StatusesPage /></TabsContent>
                            <TabsContent value="races">
                                <RacesPage races={data.races} heritage={data.heritage}
                                           beastAspects={data.beastAspects}
                                           marineAdaptations={data.marineAdaptations} />
                            </TabsContent>
                            <TabsContent value="world"><WorldPage continents={data.continents} /></TabsContent>
                            <TabsContent value="discoveries"><DiscoveriesPage biomes={discoveries} /></TabsContent>
                            <TabsContent value="bestiary"><BestiaryPage monsters={data.monsters} continents={data.continents} /></TabsContent>
                            <TabsContent value="materials"><MaterialsPage items={data.items} /></TabsContent>
                        </>
                    )}
                </div>
            </ScrollArea>
        </Tabs>
    );

    if (embedded) return (
        <div className="panel p-0 flex flex-col h-[70vh]" data-testid="journal-embedded">
            <div className="p-5 border-b-2 border-primary bg-card">
                <div className="stat-label text-primary/70 mb-1">CODEX &middot; A TRAVELER&apos;S JOURNAL</div>
                <h2 className="font-pixel text-3xl uppercase text-primary tracking-wider">The Book of Erchis</h2>
                <div className="narr text-sm text-muted-foreground mt-1">
                    Turn a page. The world remembers itself when you read.
                </div>
            </div>
            {codexTabs}
        </div>
    );

    return (
        <Sheet open={open} onOpenChange={setOpen}>
            <SheetTrigger asChild>
                <button
                    data-testid="btn-journal-open"
                    className={`press-btn font-pixel text-sm uppercase px-3 py-1.5 border-2 border-border text-muted-foreground hover:border-primary hover:text-primary flex items-center gap-1.5 ${triggerClassName || ""}`}
                    title="Open your Codex"
                >
                    <BookOpen size={14} strokeWidth={1.5} /> Journal
                </button>
            </SheetTrigger>
            <SheetContent
                side="right"
                className="w-full sm:max-w-3xl bg-background border-l-2 border-primary p-0"
                data-testid="journal-drawer"
            >
                <div className="flex flex-col h-full">
                    {/* Book header — parchment style */}
                    <div className="p-5 border-b-2 border-primary bg-card">
                        <div className="stat-label text-primary/70 mb-1">CODEX &middot; A TRAVELER&apos;S JOURNAL</div>
                        <SheetTitle asChild>
                            <h2 className="font-pixel text-3xl uppercase text-primary tracking-wider">The Book of Erchis</h2>
                        </SheetTitle>
                        <SheetDescription asChild>
                            <div className="narr text-sm text-muted-foreground mt-1">
                                Turn a page. The world remembers itself when you read.
                            </div>
                        </SheetDescription>
                    </div>

                    {codexTabs}
                </div>
            </SheetContent>
        </Sheet>
    );
}

// ==================== SUB-COMPONENTS ====================

function BusyNote() {
    return <div className="stat-label text-primary/70">Unfurling the pages…</div>;
}
function ErrorNote({ message }) {
    return <div className="stat-label text-destructive">{message}</div>;
}

function Section({ title, sub, children }) {
    return (
        <section className="mb-8">
            <h3 className="font-pixel text-2xl uppercase text-primary mb-1">{title}</h3>
            {sub && <div className="narr text-sm text-muted-foreground mb-4">{sub}</div>}
            {children}
        </section>
    );
}

function Row({ term, def }) {
    return (
        <div className="border-b border-border/40 py-2 grid grid-cols-[110px_1fr] gap-3">
            <div className="font-pixel text-sm uppercase text-primary">{term}</div>
            <div className="text-sm text-foreground/85 leading-relaxed">{def}</div>
        </div>
    );
}

function Preface() {
    return (
        <div>
            <div className="narr text-base text-foreground/90 leading-relaxed mb-4">
                Written in the plain hand of a wandering scribe, this codex answers the
                questions travelers most often shout at the sanctuary keeper after their third mug &mdash;
                what a stat does, why a status won&apos;t leave, which continent hides which beast,
                and what the strange stones in your pack are called.
            </div>
            <div className="narr text-sm text-muted-foreground italic mb-4">
                &ldquo;Read once for calm. Read twice for cunning. Read thrice and the world will
                begin to read you back.&rdquo;
            </div>
            <div className="stat-label text-primary/70">&mdash; The First Scribe of the Vale of Elder Kings</div>
        </div>
    );
}

function StatsPage() {
    return (
        <div>
            <Section title="Main Stats" sub="The trinity of combat. Every roll and every blow leans on one of these.">
                <Row term="Might"   def={STAT_HINTS.might} />
                <Row term="Grace"   def={STAT_HINTS.grace} />
                <Row term="Insight" def={STAT_HINTS.insight} />
            </Section>
            <Section title="Life Stats" sub="The four humours the old physicians measured before every campaign.">
                <Row term="Vitality"  def={STAT_HINTS.vitality} />
                <Row term="Cognition" def={STAT_HINTS.cognition} />
                <Row term="Essence"   def={STAT_HINTS.essence} />
                <Row term="Durability" def={STAT_HINTS.durability} />
            </Section>
            <Section title="Derived" sub="What your gear and origin add on top.">
                <Row term="Armor+"      def={STAT_HINTS.armor_bonus} />
                <Row term="Evasion Mod" def={STAT_HINTS.evasion_mod} />
            </Section>
            <Section title="Meters" sub="The little bars that decide big fights.">
                <Row term="HP"         def={STAT_HINTS.hp} />
                <Row term="XP"         def={STAT_HINTS.xp} />
                <Row term="Gold"       def={STAT_HINTS.gold} />
                <Row term="Exhaustion" def={EXHAUSTION_HINT} />
                <Row term="Resolve"    def={RESOLVE_HINT} />
            </Section>
        </div>
    );
}

function StatusesPage() {
    const renderStatus = (k) => {
        const s = STATUS_HINTS[k];
        if (!s) return null;
        return (
            <div key={k} className="border-b border-border/40 py-2 grid grid-cols-[110px_1fr] gap-3">
                <div className="font-pixel text-sm uppercase text-primary">{k.charAt(0).toUpperCase() + k.slice(1)}</div>
                <div className="text-sm text-foreground/85 leading-relaxed">
                    <div>{s.desc}</div>
                    <div className="stat-label text-primary/70 mt-1">{s.effect} · {s.type}</div>
                </div>
            </div>
        );
    };
    return (
        <div>
            <Section title="Debuffs" sub="Ill omens on the flesh. All fade with time — most in 2 to 5 actions.">
                {["bleeding", "poisoned", "weary", "sick", "cursed", "burning", "stunned", "shaken", "blinded", "ensnared"].map(renderStatus)}
            </Section>
            <Section title="Buffs" sub="Small graces. Do not squander them.">
                {["blessed", "focused", "warded", "hidden", "evasive"].map(renderStatus)}
            </Section>
        </div>
    );
}

function RacesPage({ races, heritage, beastAspects, marineAdaptations }) {
    return (
        <div>
            <Section title="The Eight Peoples of Erchis" sub="Each bloodline carries its own gift and its own price.">
                <div className="space-y-6">
                    {races.map((r) => {
                        const resourceKey = RACE_TO_RESOURCE[r.id];
                        const meta = RESOURCE_META[resourceKey];
                        const heritageRank = heritage?.[r.id];
                        return (
                            <div key={r.id} className="border-b border-border/40 pb-5" data-testid={`journal-race-${r.id}`}>
                                <div className="font-pixel text-xl uppercase text-primary">{r.name}</div>
                                <div className="stat-label text-muted-foreground mb-2">{r.title}</div>
                                <div className="narr text-sm text-foreground/85 mb-3">{r.story}</div>
                                <div className="stat-label text-primary/70 mb-1">RACIAL PERK — {r.perk.name}</div>
                                <div className="text-sm text-foreground/80 mb-3">{r.perk.desc}</div>
                                {heritageRank && (
                                    <div className="border-l-2 border-primary/40 pl-3 mb-3">
                                        <div className="stat-label text-primary/80">HERITAGE RANK I — {heritageRank.name}</div>
                                        <div className="text-sm text-foreground/80">{heritageRank.desc}</div>
                                    </div>
                                )}
                                {meta && (
                                    <div className="text-xs text-muted-foreground">
                                        Resource: <span className="text-primary">{meta.label}</span> (0/{meta.max}) — {meta.hint}
                                    </div>
                                )}
                            </div>
                        );
                    })}
                </div>
            </Section>
            <Section title="Beast Aspects — Wildblood" sub="Choose your inner animal at creation. It shapes your instincts and gifts.">
                {beastAspects?.map((a) => (
                    <div key={a.id} className="border-b border-border/40 py-2">
                        <div className="font-pixel text-sm uppercase text-primary">{a.name}</div>
                        <div className="text-xs text-muted-foreground italic mb-1">Kin of {a.examples}</div>
                        <div className="text-sm text-foreground/80">{a.bonus_desc}</div>
                    </div>
                ))}
            </Section>
            <Section title="Marine Adaptations — Hyliondrian" sub="The lineage of the deep that shaped your gills and instincts.">
                {marineAdaptations?.map((a) => (
                    <div key={a.id} className="border-b border-border/40 py-2">
                        <div className="font-pixel text-sm uppercase text-primary">{a.name}</div>
                        <div className="text-sm text-foreground/80">{a.bonus_desc}</div>
                    </div>
                ))}
            </Section>
        </div>
    );
}

function WorldPage({ continents }) {
    return (
        <Section title="The Eleven Continents" sub="Eight peopled, three sealed. Each land has its own voice.">
            <div className="narr text-sm text-muted-foreground mb-4">
                {CONTINENT_BONUS_HINT} {REPUTATION_HINT}
            </div>
            <div className="border border-border/60 p-3 mb-4 bg-background">
                <div className="stat-label text-primary/80 mb-2">FIELD NOTES</div>
                <div className="text-xs text-muted-foreground space-y-1.5">
                    <p><span className="text-primary">Professions:</span> {PROFESSION_HINT}</p>
                    <p><span className="text-primary">Exploration:</span> {EXPLORATION_HINT}</p>
                    <p><span className="text-primary">Resource Nodes:</span> {NODE_HINT}</p>
                </div>
            </div>
            <div className="space-y-4">
                {continents.map((c) => (
                    <div key={c.id} className="border border-border p-3" data-testid={`journal-continent-${c.id}`}>
                        <div className="flex items-baseline justify-between">
                            <div className="font-pixel text-lg uppercase text-primary">{c.name}</div>
                            <div className="stat-label text-primary/70">{c.locked ? "Sealed" : `Lv ${c.level_req}+`}</div>
                        </div>
                        <div className="narr text-sm text-muted-foreground mt-1">{c.desc}</div>
                        {c.bonus_desc && !c.locked && (
                            <div className="stat-label text-primary/60 mt-2 italic">
                                {c.bonus_desc}
                            </div>
                        )}
                        {c.biomes?.length > 0 && !c.locked && (
                            <div className="mt-3">
                                <div className="stat-label text-primary/80 mb-1">Biomes</div>
                                <ul className="text-sm text-foreground/80 space-y-0.5">
                                    {c.biomes.map((b) => (
                                        <li key={b.id}>
                                            <span className="font-pixel text-primary uppercase">{b.name}</span>
                                            <span className="text-muted-foreground"> — {b.desc}</span>
                                        </li>
                                    ))}
                                </ul>
                            </div>
                        )}
                    </div>
                ))}
            </div>
        </Section>
    );
}

const RARITY_COLORS = {
    common:    "text-foreground/80",
    uncommon:  "text-rarity-uncommon",
    rare:      "text-rarity-rare",
    epic:      "text-rarity-epic",
    legendary: "text-rarity-legendary",
    mythic:    "text-rarity-mythic",
    exotic:    "text-rarity-exotic",
};

function DiscoveriesPage({ biomes }) {
    const [filter, setFilter] = useState("all");

    const grouped = useMemo(() => {
        if (!biomes) return {};
        const g = {};
        for (const b of biomes) {
            const cont = b.continent_name || "Unknown";
            g[cont] = g[cont] || [];
            g[cont].push(b);
        }
        return g;
    }, [biomes]);

    if (!biomes) return <div className="stat-label text-primary/70">Loading discoveries…</div>;

    const totalMonsters = biomes.reduce((s, b) => s + b.discovered_monsters, 0);
    const totalMonstersAll = biomes.reduce((s, b) => s + b.total_monsters, 0);
    const totalNodes = biomes.reduce((s, b) => s + b.discovered_nodes, 0);
    const totalNodesAll = biomes.reduce((s, b) => s + b.total_nodes, 0);

    return (
        <Section title="Discoveries" sub="Every beast you've faced, every herb you've named. The world reveals itself to those who wander.">
            {/* Summary */}
            <div className="flex gap-4 mb-6 border border-border p-3 bg-background">
                <div className="text-center">
                    <div className="font-pixel text-2xl text-primary">{totalMonsters}/{totalMonstersAll}</div>
                    <div className="stat-label text-muted-foreground text-[10px]">MONSTERS</div>
                </div>
                <div className="text-center">
                    <div className="font-pixel text-2xl text-primary">{totalNodes}/{totalNodesAll}</div>
                    <div className="stat-label text-muted-foreground text-[10px]">RESOURCES</div>
                </div>
            </div>

            {/* Filter */}
            <div className="flex gap-2 mb-4">
                {["all", "monsters", "nodes"].map(f => (
                    <button
                        key={f}
                        onClick={() => setFilter(f)}
                        className={`press-btn font-pixel text-xs uppercase px-3 py-1 border-2 ${filter === f ? "border-primary bg-primary text-primary-foreground" : "border-border text-muted-foreground hover:border-primary"}`}
                    >
                        {f}
                    </button>
                ))}
            </div>

            {/* Per-continent, per-biome */}
            <div className="space-y-6">
                {Object.entries(grouped).map(([cont, biomeList]) => (
                    <div key={cont}>
                        <div className="font-pixel text-lg uppercase text-primary mb-2">{cont}</div>
                        {biomeList.map(b => {
                            const showMonsters = filter === "all" || filter === "monsters";
                            const showNodes = filter === "all" || filter === "nodes";
                            return (
                                <div key={b.biome_id} className="mb-4 border border-border/60 p-3" data-testid={`discovery-biome-${b.biome_id}`}>
                                    <div className="flex justify-between items-baseline mb-2">
                                        <div className="font-pixel text-sm uppercase text-primary">{b.biome_name}</div>
                                        <div className="text-xs text-muted-foreground">
                                            {b.exploration_pct}% explored
                                        </div>
                                    </div>
                                    {showMonsters && b.monsters.length > 0 && (
                                        <div className="mb-2">
                                            <div className="stat-label text-muted-foreground text-[10px] mb-1">
                                                MONSTERS ({b.discovered_monsters}/{b.total_monsters})
                                            </div>
                                            <div className="grid grid-cols-2 md:grid-cols-3 gap-1">
                                                {b.monsters.map((m, i) => (
                                                    <div
                                                        key={i}
                                                        className={`border px-2 py-1 text-xs ${m.discovered ? "border-border/60" : "border-dashed border-border/30 opacity-50"}`}
                                                        data-testid={`discovery-monster-${b.biome_id}-${i}`}
                                                    >
                                                        <div className={`font-pixel uppercase text-[10px] ${m.discovered ? (RARITY_COLORS[m.rarity] || "text-foreground") : "text-muted-foreground"}`}>
                                                            {m.discovered ? m.name : "???"}
                                                        </div>
                                                        {m.discovered && (
                                                            <div className="text-muted-foreground text-[10px]">
                                                                THREAT {m.threat}
                                                            </div>
                                                        )}
                                                    </div>
                                                ))}
                                            </div>
                                        </div>
                                    )}
                                    {showNodes && b.nodes.length > 0 && (
                                        <div>
                                            <div className="stat-label text-muted-foreground text-[10px] mb-1">
                                                RESOURCES ({b.discovered_nodes}/{b.total_nodes})
                                            </div>
                                            <div className="grid grid-cols-2 md:grid-cols-3 gap-1">
                                                {b.nodes.map((n, i) => (
                                                    <div
                                                        key={i}
                                                        className={`border px-2 py-1 text-xs ${n.discovered ? "border-border/60" : "border-dashed border-border/30 opacity-50"}`}
                                                        data-testid={`discovery-node-${b.biome_id}-${i}`}
                                                    >
                                                        <div className={`font-pixel uppercase text-[10px] ${n.discovered ? (RARITY_COLORS[n.rarity] || "text-foreground") : "text-muted-foreground"}`}>
                                                            {n.discovered ? n.name : "???"}
                                                        </div>
                                                        {n.discovered && n.profession && (
                                                            <div className="text-muted-foreground text-[10px]">
                                                                {n.profession}
                                                            </div>
                                                        )}
                                                    </div>
                                                ))}
                                            </div>
                                        </div>
                                    )}
                                </div>
                            );
                        })}
                    </div>
                ))}
            </div>
        </Section>
    );
}

function BestiaryPage({ monsters, continents }) {
    const continentByBiome = useMemo(() => {
        const out = {};
        for (const c of continents) {
            for (const b of (c.biomes || [])) out[b.id] = c.name;
        }
        return out;
    }, [continents]);

    // Group monsters by continent → biome
    const grouped = useMemo(() => {
        const g = {};
        for (const m of monsters) {
            const cont = continentByBiome[m.biome] || "Unknown";
            g[cont] = g[cont] || {};
            g[cont][m.biome] = g[cont][m.biome] || [];
            g[cont][m.biome].push(m);
        }
        return g;
    }, [monsters, continentByBiome]);

    return (
        <Section title="Bestiary" sub="Notes on every beast the scribe knows to name. Higher power = harder fight.">
            <div className="space-y-6">
                {Object.entries(grouped).map(([cont, biomes]) => (
                    <div key={cont}>
                        <div className="font-pixel text-lg uppercase text-primary mb-1">{cont}</div>
                        {Object.entries(biomes).map(([biome, ms]) => (
                            <div key={biome} className="mb-3">
                                <div className="stat-label text-primary/70 mb-1">{biome.replace(/_/g, " ")}</div>
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                                    {ms.map((m) => (
                                        <div key={m.id} className="border border-border/60 p-2" data-testid={`journal-monster-${m.id}`}>
                                            <div className="flex justify-between items-baseline">
                                                <div className="font-pixel text-sm uppercase text-primary">{m.name}</div>
                                                <div className="stat-label text-primary/60">THREAT {m.threat} · HP {m.hp}</div>
                                            </div>
                                            {m.drops?.length > 0 && (
                                                <div className="text-xs text-muted-foreground mt-1">
                                                    Drops: {m.drops.map(([id, chance]) => `${id.replace(/_/g, ' ')} (${Math.round(chance * 100)}%)`).join(", ")}
                                                </div>
                                            )}
                                        </div>
                                    ))}
                                </div>
                            </div>
                        ))}
                    </div>
                ))}
            </div>
        </Section>
    );
}

function MaterialsPage({ items }) {
    const RARITY_ORDER = ["common", "uncommon", "rare", "epic", "legendary", "mythic"];
    const RARITY_LABEL = {
        common: "Common", uncommon: "Uncommon", rare: "Rare",
        epic: "Epic",     legendary: "Legendary", mythic: "Mythic",
    };
    const RARITY_COLORS = {
        common:    "text-foreground/80",
        uncommon:  "text-rarity-uncommon",
        rare:      "text-rarity-rare",
        epic:      "text-rarity-epic",
        legendary: "text-rarity-legendary",
        mythic:    "text-rarity-mythic",
    };

    const byRarity = useMemo(() => {
        const out = {};
        for (const it of items) {
            (out[it.rarity] = out[it.rarity] || []).push(it);
        }
        return out;
    }, [items]);

    return (
        <Section title="Materials & Items" sub="Everything that fills a hero's pack. Sorted by how rare the finding.">
            <div className="space-y-4">
                {RARITY_ORDER.filter((r) => byRarity[r]).map((r) => (
                    <div key={r}>
                        <div className={`font-pixel text-lg uppercase mb-1 ${RARITY_COLORS[r] || ""}`}>{RARITY_LABEL[r]}</div>
                        <div className="grid grid-cols-2 md:grid-cols-3 gap-1 text-xs">
                            {byRarity[r].map((it) => (
                                <div key={it.id} className="border border-border/40 px-2 py-1 flex items-center gap-2" data-testid={`journal-item-${it.id}`}>
                                    <PixelSprite item={it} size={28} />
                                    <div className="min-w-0">
                                        <div className={`font-pixel uppercase text-sm truncate ${RARITY_COLORS[r] || ""}`}>{it.name}</div>
                                        <div className="text-muted-foreground text-xs">{it.kind}</div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                ))}
            </div>
        </Section>
    );
}
