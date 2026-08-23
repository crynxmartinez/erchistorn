import { useEffect, useState, useMemo } from "react";
import { api, extractError } from "@/lib/api";
import { useGameData, RARITY_TEXT, RARITY_CLASS } from "@/data/gameData";
import { toast } from "sonner";
import { BedDouble, ShoppingBag, ScrollText, Users, ArrowLeft, Coins, MessageCircle, Wrench, Swords, MapPin, TrendingUp, TrendingDown, Minus, Clock, Crown, CheckCircle2, Circle, Trophy, XCircle, Sparkles, HeartPulse, Shield, Gem, Dumbbell, GraduationCap } from "lucide-react";
import NpcPanel from "@/components/NpcPanel";
import QuestModal from "@/components/QuestModal";
import WaypointPanel from "@/components/WaypointPanel";
import Inventory from "@/components/Inventory";
import TradeNpcPanel from "@/components/TradeNpcPanel";
import RunesmithPanel from "@/components/RunesmithPanel";
import GemsmithPanel from "@/components/GemsmithPanel";
import TrainingPanel from "@/components/TrainingPanel";
import StudyPanel from "@/components/StudyPanel";
import PixelSprite from "@/components/PixelSprite";
import { Tooltip, TooltipTrigger, TooltipContent, TooltipProvider } from "@/components/ui/tooltip";

export default function TownView({ townId, character, onCharacterUpdate, onLeave, onTravel, onCombatStart, initialTab, onTabChange }) {
    const gd = useGameData();
    const [town, setTown] = useState(null);
    const [tab, setTab] = useState("sanctuary");
    const [buyQty, setBuyQty] = useState({});
    const [showSellInv, setShowSellInv] = useState(false);
    const [noticeQuests, setNoticeQuests] = useState([]);
    const [loungeQuests, setLoungeQuests] = useState([]);
    const [events, setEvents] = useState([]);
    const [heritageData, setHeritageData] = useState(null);
    const [heritageQuests, setHeritageQuests] = useState(null);
    const [heritageVendor, setHeritageVendor] = useState(null);
    const [heritageLadder, setHeritageLadder] = useState(null);
    const [now, setNow] = useState(Date.now());
    const [marketData, setMarketData] = useState(null);
    const [marketCat, setMarketCat] = useState("all");
    const [marketLoading, setMarketLoading] = useState(false);
    const [tools, setTools] = useState([]);
    const [toolBusy, setToolBusy] = useState(null);
    const [questModal, setQuestModal] = useState(null);
    const [toolStock, setToolStock] = useState({});
    const [sanctuaryRoster, setSanctuaryRoster] = useState(null);
    const [sanctuaryNarrative, setSanctuaryNarrative] = useState(null);
    const [townReady, setTownReady] = useState(false);
    const TOOL_MAX_STOCK = 500;

    const _toolStockSeed = (toolId) => {
        const today = new Date().toISOString().slice(0, 10);
        let h = 0;
        for (const ch of `${toolId}:${today}`) h = ((h << 5) - h + ch.charCodeAt(0)) & 0x7fffffff;
        return 1 + (h % TOOL_MAX_STOCK);
    };

    useEffect(() => {
        const id = setInterval(() => setNow(Date.now()), 1000);
        return () => clearInterval(id);
    }, []);

    useEffect(() => {
        setTab(initialTab || "sanctuary");
        setTownReady(false);
        (async () => {
            try {
                const { data } = await api.post("/game/town/visit", { town_id: townId });
                onCharacterUpdate?.(data.character);
                setTown(data.town);
                const [notice, lounge, ev] = await Promise.all([
                    api.get(`/game/quests/available?town_id=${townId}&board=notice`),
                    api.get(`/game/quests/available?town_id=${townId}&board=lounge`),
                    api.get("/game/events/active"),
                ]);
                setNoticeQuests(notice.data.available);
                setLoungeQuests(lounge.data.available);
                setEvents(ev.data.events);
                // Fetch heritage data if this town is on the heritage continent
                try {
                    const hCur = await api.get("/game/heritage/current");
                    if (hCur.data.active && hCur.data.continent === data.town?.continent) {
                        setHeritageData(hCur.data);
                        const [hBoss, hQuests] = await Promise.all([
                            api.get("/game/heritage/boss"),
                            api.get("/game/heritage/quests/daily"),
                        ]);
                        setHeritageData(prev => ({ ...prev, bossInfo: hBoss.data }));
                        setHeritageQuests(hQuests.data);
                        // Fetch heritage vendor for this continent
                        const hVendor = await api.get(`/game/heritage/vendor/${hCur.data.continent}`);
                        setHeritageVendor(hVendor.data);
                        // Fetch heritage ladder
                        const hLadder = await api.get("/game/heritage/ladder");
                        setHeritageLadder(hLadder.data);
                    } else {
                        setHeritageData(null);
                        setHeritageQuests(null);
                        setHeritageVendor(null);
                        setHeritageLadder(null);
                    }
                } catch (e) {
                    setHeritageData(null);
                    setHeritageQuests(null);
                    setHeritageVendor(null);
                    setHeritageLadder(null);
                }
            } catch (e) {
                toast.error(extractError(e));
                onLeave?.();
            }
            setTownReady(true);
        })();
    }, [townId]);

    // Fetch sanctuary roster when sanctuary tab is opened
    useEffect(() => {
        if (tab === "sanctuary" && !sanctuaryRoster) {
            (async () => {
                try {
                    const { data } = await api.get("/game/town/sanctuary/roster");
                    setSanctuaryRoster(data.roster);
                } catch (e) {}
            })();
        }
    }, [tab]);

    // Refresh heritage quests when character updates (e.g. after gathering resources)
    useEffect(() => {
        if (!heritageData?.active) return;
        let cancelled = false;
        (async () => {
            try {
                const hQuests = await api.get("/game/heritage/quests/daily");
                if (!cancelled) setHeritageQuests(hQuests.data);
            } catch (e) {}
        })();
        return () => { cancelled = true; };
    }, [character?.hp, character?.level, character?.inventory?.length, heritageData?.active]);

    useEffect(() => {
        if (tab === "market" && !marketData && !marketLoading) {
            fetchMarket();
        }
        if (tab === "market" && tools.length === 0) {
            fetchTools();
        }
    }, [tab]);

    const filteredMarketListings = useMemo(() => {
        const marketListings = (marketData?.listings || []).map(l => ({ ...l, _type: "market" }));
        const toolListings = tools.map(t => ({ ...t, _type: "tool", item_id: `tool_${t.profession_id}` }));
        const allListings = [...marketListings, ...toolListings];

        if (marketCat === "all") return allListings;
        if (marketCat === "tool") return toolListings;
        return marketListings.filter(l => {
            const def = l.instance || gd.itemsById?.[l.item_id];
            if (!def) return false;
            if (marketCat === "weapon") return def.kind === "weapon";
            if (marketCat === "armor") return def.kind === "armor";
            if (marketCat === "consumable") return def.kind === "consumable";
            if (marketCat === "material") return def.kind === "material";
            if (marketCat === "skillbook") return def.kind === "skillbook";
            if (marketCat === "relic") return def.kind === "relic" || def.kind === "trinket";
            return true;
        });
    }, [marketData, marketCat, gd.itemsById, tools]);

    if (!townReady || !town || !character || !gd.ready) {
        const townName = townId?.replace(/_/g, " ").replace(/\b\w/g, c => c.toUpperCase()) || "town";
        return (
            <div className="flex flex-col items-center justify-center py-20 gap-4" data-testid="town-loading">
                <div className="font-pixel text-2xl text-primary animate-pulse">Approaching {townName}…</div>
                <div className="flex gap-1.5">
                    <span className="w-2 h-2 bg-primary/40 rounded-full animate-bounce" style={{ animationDelay: "0ms" }} />
                    <span className="w-2 h-2 bg-primary/60 rounded-full animate-bounce" style={{ animationDelay: "150ms" }} />
                    <span className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{ animationDelay: "300ms" }} />
                </div>
            </div>
        );
    }

    const hasBlessing = (character.statuses || []).some(s => s.id === "sanctuary_blessing");

    const sanctuaryService = async (service) => {
        try {
            const { data } = await api.post("/game/town/sanctuary", { service });
            onCharacterUpdate?.(data.character);
            setSanctuaryNarrative({
                service,
                narrative: data.narrative,
                cost: data.cost,
                sanctuary_name: data.sanctuary_name,
                resolve_info: data.resolve_info,
            });
            if (data.resolve_info?.boosted) {
                toast.success(`Resolve restored: ${data.resolve_info.before} → ${data.resolve_info.after}`);
            } else if (data.resolve_info && !data.resolve_info.boosted && data.resolve_info.before < 65) {
                toast.info("Resolve cooldown active — heal only, no resolve boost");
            }
        } catch (e) {
            toast.error(extractError(e));
        }
    };

    const fetchMarket = async () => {
        setMarketLoading(true);
        try {
            const { data } = await api.get("/game/town/market");
            setMarketData(data);
        } catch (e) {
            toast.error(extractError(e));
        } finally {
            setMarketLoading(false);
        }
    };

    const fetchTools = async () => {
        try {
            const { data } = await api.get("/game/tools/all");
            const fetched = data.tools || [];
            setTools(fetched);
            const stock = {};
            for (const t of fetched) {
                stock[t.tool_id] = _toolStockSeed(t.tool_id);
            }
            setToolStock(stock);
        } catch (e) {
            toast.error(extractError(e));
        }
    };

    const repairTool = async (profession_id) => {
        setToolBusy(profession_id);
        try {
            const { data } = await api.post("/game/tools/repair", { profession_id });
            onCharacterUpdate?.(data.character);
            toast.success(`Repaired — ${data.paid}g`);
            await fetchTools();
        } catch (e) {
            toast.error(extractError(e));
        } finally {
            setToolBusy(null);
        }
    };

    const buyTool = async (profession_id) => {
        setToolBusy(profession_id);
        try {
            const { data } = await api.post("/game/tools/buy", { profession_id });
            onCharacterUpdate?.(data.character);
            toast.success(`Bought ${data.tool_name} — ${data.paid}g`);
            const tool = tools.find(t => t.profession_id === profession_id);
            if (tool) {
                setToolStock(prev => ({ ...prev, [tool.tool_id]: Math.max(0, (prev[tool.tool_id] || 0) - 1) }));
            }
            await fetchTools();
        } catch (e) {
            toast.error(extractError(e));
        } finally {
            setToolBusy(null);
        }
    };

    const buy = async (item_id) => {
        try {
            const qty = buyQty[item_id] || 1;
            const listing = marketData?.listings?.find(l => l.item_id === item_id);
            const inst = listing?.instance;
            const displayName = inst?.name || gd.itemsById[item_id]?.name || item_id;
            const { data } = await api.post("/game/town/market/buy", { item_id, quantity: qty });
            onCharacterUpdate?.(data.character);
            toast.success(`Bought ${qty} × ${displayName} — ${data.paid}g`);
            // Update local market stock
            if (marketData) {
                setMarketData(prev => prev ? {
                    ...prev,
                    listings: prev.listings.map(l =>
                        l.item_id === item_id ? { ...l, stock: data.stock_remaining } : l
                    )
                } : prev);
            }
        } catch (e) {
            toast.error(extractError(e));
        }
    };

    const sell = async (item_id, quantity = 1) => {
        try {
            const { data } = await api.post("/game/town/market/sell", { item_id, quantity });
            onCharacterUpdate?.(data.character);
            toast.success(`Sold ${quantity > 1 ? `${quantity}x ` : ""}— received ${data.received}g`);
        } catch (e) {
            toast.error(extractError(e));
        }
    };

    const claimHeritageQuest = async (questId) => {
        try {
            const { data } = await api.post("/game/heritage/quests/claim", { quest_id: questId });
            toast.success(`Earned ${data.tokens_earned} heritage tokens!${data.bonus ? " (All quests bonus!)" : ""}`);
            const hQuests = await api.get("/game/heritage/quests/daily");
            setHeritageQuests(hQuests.data);
            // Refresh vendor token balance
            if (heritageData?.continent) {
                const hv = await api.get(`/game/heritage/vendor/${heritageData.continent}`);
                setHeritageVendor(hv.data);
            }
        } catch (e) { toast.error(extractError(e)); }
    };

    const buyHeritageItem = async (continent, itemId) => {
        try {
            const { data } = await api.post(`/game/heritage/vendor/${continent}/buy`, { item_id: itemId });
            toast.success(data.message);
            onCharacterUpdate?.(data.character);
            const hv = await api.get(`/game/heritage/vendor/${continent}`);
            setHeritageVendor(hv.data);
        } catch (e) { toast.error(extractError(e)); }
    };

    const acceptQuest = async (qid) => {
        try {
            const { data } = await api.post(`/game/quests/${qid}/accept`);
            setNoticeQuests((prev) => prev.filter((q) => q.id !== qid));
            setLoungeQuests((prev) => prev.filter((q) => q.id !== qid));
            onCharacterUpdate?.(data.character);
            setQuestModal({ type: "accept", quest: data.quest, narrative: data.narrative });
        } catch (e) {
            toast.error(extractError(e));
        }
    };
    const abandonQuest = async (qid) => {
        try {
            const { data } = await api.post(`/game/quests/${qid}/abandon`);
            onCharacterUpdate?.(data.character);
            setQuestModal({ type: "abandon", quest: data.quest, narrative: data.narrative });
        } catch (e) {
            toast.error(extractError(e));
        }
    };

    const joinEvent = async (eid) => {
        try {
            const { data } = await api.post(`/game/events/${eid}/join`);
            onCharacterUpdate?.(data.character);
            toast.success("Joined event");
        } catch (e) {
            toast.error(extractError(e));
        }
    };

    const leaveTown = async () => {
        try {
            const { data } = await api.post("/game/town/leave");
            if (data?.character) onCharacterUpdate?.(data.character);
        } catch { /* ignore */ }
        onLeave?.();
    };

    const startLearn = async (skill_id, teacher_id) => {
        try {
            const { data } = await api.post("/game/skill/learn", { skill_id, teacher_id });
            onCharacterUpdate?.(data.character);
            toast.success(`Began learning ${gd.skillsById?.[data.started]?.name || data.started} (${data.seconds}s)`);
        } catch (e) {
            toast.error(extractError(e));
        }
    };

    const finishLearn = async () => {
        try {
            const { data } = await api.post("/game/skill/finish_learn");
            onCharacterUpdate?.(data.character);
            toast.success(`Learned ${gd.skillsById?.[data.learned]?.name || data.learned}!`);
        } catch (e) {
            toast.error(extractError(e));
        }
    };

    const formatTime = (sec) => {
        const m = Math.floor(sec / 60);
        const s = sec % 60;
        return `${m}:${s.toString().padStart(2, "0")}`;
    };

    const MARKET_CATEGORIES = [
        { id: "all", label: "All" },
        { id: "weapon", label: "Weapons" },
        { id: "armor", label: "Armor" },
        { id: "consumable", label: "Consumables" },
        { id: "material", label: "Materials" },
        { id: "skillbook", label: "Skillbooks" },
        { id: "relic", label: "Relics" },
        { id: "tool", label: "Tools" },
    ];

    const statLine = (def) => {
        const parts = [];
        if (def.atk) parts.push(`ATK ${def.atk}`);
        if (def.def) parts.push(`DEF ${def.def}`);
        if (def.mag) parts.push(`MAG ${def.mag}`);
        if (def.hp) parts.push(`HP ${def.hp}`);
        if (def.heal) parts.push(`Heal ${def.heal}`);
        return parts.join(" · ") || "—";
    };

    const TREND_ICONS = {
        up: { icon: TrendingUp, color: "text-red-400" },
        down: { icon: TrendingDown, color: "text-green-400" },
        flat: { icon: Minus, color: "text-muted-foreground" },
    };

    const TABS = [
        { id: "sanctuary", label: "Sanctuary", icon: HeartPulse, avail: town.services.includes("sanctuary") },
        { id: "voices", label: "Voices", icon: MessageCircle, avail: true },
        { id: "festival", label: "Festival", icon: Crown, avail: !!heritageData },
        { id: "trade", label: "Trade", icon: Wrench, avail: true },
        { id: "market", label: "Market", icon: ShoppingBag, avail: town.services.includes("market") },
        { id: "waypoint", label: "Waypoint", icon: MapPin, avail: !!town.hometown },
        { id: "lounge", label: "Adventurer's Lounge", icon: Swords, avail: true },
        { id: "notice", label: "Notice Board", icon: ScrollText, avail: town.services.includes("notice_board") },
        { id: "trainers", label: "Trainers", icon: Users, avail: town.services.includes("trainers") },
        { id: "runesmith", label: "Runesmith", icon: Sparkles, avail: town.services.includes("runesmith") },
        { id: "gemsmith", label: "Gemsmith", icon: Gem, avail: town.services.includes("gemsmith") },
        { id: "training_main", label: "Gym (Main Stats)", icon: Dumbbell, avail: town.services.includes("training_main") },
        { id: "training_life", label: "Gym (Life Stats)", icon: HeartPulse, avail: town.services.includes("training_life") },
        { id: "study", label: "Academy", icon: GraduationCap, avail: town.services.includes("study") },
    ].filter(t => t.avail);

    return (
        <div className="space-y-4" data-testid="town-page">
            <div className="flex items-center justify-between">
                <button onClick={leaveTown} data-testid="town-leave" className="stat-label text-primary/70 hover:text-primary flex items-center gap-1">
                    <ArrowLeft size={12} /> LEAVE TOWN
                </button>
            </div>

            <div className="panel p-6 mb-4">
                <div className="stat-label text-primary/70">{town.type.replace(/_/g, " ").toUpperCase()} · {town.continent.toUpperCase()}</div>
                <h1 className="font-pixel text-5xl uppercase text-primary tracking-wider">{town.name}</h1>
                <p className="narr text-lg text-muted-foreground mt-2 max-w-3xl">{town.desc}</p>
                <div className="stat-label mt-3 text-primary/80">SPECIALTY: {town.specialty}</div>
                <div className="mt-3 flex items-center gap-2 stat-label">
                    <Coins size={12} className="text-primary" /> <span className="text-primary" data-testid="town-gold">{character.gold}g</span>
                    <span className="ml-4">HP {character.hp}/{character.max_hp}</span>
                </div>
            </div>

            {/* Tabs */}
            <div className="flex flex-wrap gap-2 mb-4">
                {TABS.map((t) => {
                    const Ic = t.icon;
                    return (
                        <button
                            key={t.id}
                            data-testid={`town-tab-${t.id}`}
                            onClick={() => { setTab(t.id); onTabChange?.(); }}
                            className={`press-btn font-pixel text-sm uppercase px-3 py-1.5 border-2 flex items-center gap-1.5 ${
                                tab === t.id
                                    ? "border-primary bg-primary text-primary-foreground"
                                    : "border-border text-muted-foreground hover:border-primary hover:text-primary"
                            }`}
                        >
                            <Ic size={14} strokeWidth={1.5} /> {t.label}
                        </button>
                    );
                })}
            </div>

            {/* Panels */}
            {tab === "voices" && (
                <div className="panel p-6" data-testid="town-voices">
                    <NpcPanel character={character} onCharacterUpdate={onCharacterUpdate} />
                </div>
            )}

            {tab === "sanctuary" && (
                <div className="panel p-6" data-testid="sanctuary-panel">
                    <h2 className="font-pixel text-3xl uppercase text-primary mb-2">The {town.name} Sanctuary</h2>
                    <p className="narr text-muted-foreground mb-6">A sanctified hall where the wounded are mended and the fallen are restored. Rest here to heal, or wake here after defeat.</p>
                    <div className="grid grid-cols-3 gap-4 font-mono text-sm mb-6">
                        <div className="flex items-center gap-2"><BedDouble size={16} className="text-primary/60" /><div><div className="stat-label">REST</div><div className="text-primary text-xl">{town.sanctuary_cost}g</div></div></div>
                        <div className="flex items-center gap-2"><Sparkles size={16} className="text-primary/60" /><div><div className="stat-label">CLEANSE</div><div className="text-primary text-xl">{town.sanctuary_cost * 2}g</div></div></div>
                        <div className="flex items-center gap-2"><Shield size={16} className="text-primary/60" /><div><div className="stat-label">BLESSING</div><div className="text-primary text-xl">{town.sanctuary_cost * 3}g</div></div></div>
                    </div>
                    <div className="space-y-3">
                        <div className="flex items-center justify-between border border-border/40 rounded p-3">
                            <div>
                                <div className="font-pixel text-sm uppercase text-primary">Rest</div>
                                <div className="text-xs text-muted-foreground">Full HP restore · Clear debuffs · -20 exhaustion · Resolve → 65 (2hr CD)</div>
                            </div>
                            <button
                                data-testid="sanctuary-rest-btn"
                                onClick={() => sanctuaryService("rest")}
                                disabled={character.gold < town.sanctuary_cost}
                                className="press-btn font-pixel text-sm uppercase px-4 py-2 bg-primary text-primary-foreground border-2 border-primary hover:bg-transparent hover:text-primary transition-colors disabled:opacity-40"
                            >
                                REST — {town.sanctuary_cost}g
                            </button>
                        </div>
                        <div className="flex items-center justify-between border border-border/40 rounded p-3">
                            <div>
                                <div className="font-pixel text-sm uppercase text-primary">Sanctuary Cleansing</div>
                                <div className="text-xs text-muted-foreground">Remove "Recovering" death debuff immediately</div>
                            </div>
                            <button
                                data-testid="sanctuary-cleanse-btn"
                                onClick={() => sanctuaryService("cleanse")}
                                disabled={character.gold < town.sanctuary_cost * 2}
                                className="press-btn font-pixel text-sm uppercase px-4 py-2 bg-primary text-primary-foreground border-2 border-primary hover:bg-transparent hover:text-primary transition-colors disabled:opacity-40"
                            >
                                CLEANSE — {town.sanctuary_cost * 2}g
                            </button>
                        </div>
                        <div className="flex items-center justify-between border border-border/40 rounded p-3">
                            <div>
                                <div className="font-pixel text-sm uppercase text-primary">Sanctuary Blessing</div>
                                <div className="text-xs text-muted-foreground">
                                    {hasBlessing ? "✦ Blessing active — already in effect" : "+5% XP gain for 10 actions"}
                                </div>
                            </div>
                            <button
                                data-testid="sanctuary-blessing-btn"
                                onClick={() => sanctuaryService("blessing")}
                                disabled={hasBlessing || character.gold < town.sanctuary_cost * 3}
                                className="press-btn font-pixel text-sm uppercase px-4 py-2 bg-primary text-primary-foreground border-2 border-primary hover:bg-transparent hover:text-primary transition-colors disabled:opacity-40"
                            >
                                {hasBlessing ? "ACTIVE" : `BLESS — ${town.sanctuary_cost * 3}g`}
                            </button>
                        </div>
                    </div>
                    {/* Sanctuary Roster */}
                    <div className="mt-6 border-t border-border/40 pt-4">
                        <h3 className="font-pixel text-lg uppercase text-primary mb-3 flex items-center gap-2">
                            <HeartPulse size={16} /> Sanctuary Roster
                        </h3>
                        <p className="text-xs text-muted-foreground mb-3">Adventurers currently recovering or resting in sanctuaries across Erchis.</p>
                        {sanctuaryRoster === null ? (
                            <div className="text-sm text-muted-foreground">Loading roster…</div>
                        ) : sanctuaryRoster.length === 0 ? (
                            <div className="text-sm text-muted-foreground">The halls are quiet. No one is recovering right now.</div>
                        ) : (
                            <div className="space-y-1 max-h-64 overflow-y-auto">
                                {sanctuaryRoster.map((p, i) => (
                                    <div key={i} className={`flex items-center justify-between px-3 py-2 border border-border/30 rounded ${p.recovering ? "bg-destructive/5" : ""}`}>
                                        <div className="flex items-center gap-3">
                                            <div className={`w-2 h-2 rounded-full ${p.recovering ? "bg-destructive" : "bg-primary/60"}`} />
                                            <div>
                                                <div className="font-mono text-sm text-foreground">{p.name}</div>
                                                <div className="text-xs text-muted-foreground">
                                                    Lv {p.level} {p.race} · {p.town}
                                                    {p.cause && ` · slain by ${p.cause}`}
                                                </div>
                                            </div>
                                        </div>
                                        <div className="text-right">
                                            {p.recovering ? (
                                                <span className="font-pixel text-xs uppercase text-destructive">Recovering</span>
                                            ) : (
                                                <span className="font-pixel text-xs uppercase text-primary/60">Resting</span>
                                            )}
                                            <div className="text-xs text-muted-foreground font-mono">{p.hp}/{p.max_hp} HP</div>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                </div>
            )}

            {tab === "market" && (
                <div className="panel p-6" data-testid="market-panel">
                    <div className="flex justify-between items-center mb-4">
                        <h2 className="font-pixel text-3xl uppercase text-primary">Marketplace</h2>
                        {marketData?.refreshes_in && (
                            <div className="stat-label text-xs text-muted-foreground flex items-center gap-1">
                                <Clock size={12} /> Refreshes in {marketData.refreshes_in}
                            </div>
                        )}
                    </div>

                    {/* Category tabs */}
                    <div className="flex flex-wrap gap-1 mb-4">
                        {MARKET_CATEGORIES.map(c => {
                            let count;
                            if (c.id === "all") {
                                count = (marketData?.listings?.length || 0) + tools.length;
                            } else if (c.id === "tool") {
                                count = tools.length;
                            } else {
                                count = (marketData?.listings || []).filter(l => {
                                    const def = l.instance || gd.itemsById?.[l.item_id];
                                    if (!def) return false;
                                    if (c.id === "weapon") return def.kind === "weapon";
                                    if (c.id === "armor") return def.kind === "armor";
                                    if (c.id === "consumable") return def.kind === "consumable";
                                    if (c.id === "material") return def.kind === "material";
                                    if (c.id === "skillbook") return def.kind === "skillbook";
                                    if (c.id === "relic") return def.kind === "relic" || def.kind === "trinket";
                                    return true;
                                }).length;
                            }
                            return (
                                <button
                                    key={c.id}
                                    onClick={() => setMarketCat(c.id)}
                                    className={`px-3 py-1 text-xs font-pixel uppercase border transition-colors ${
                                        marketCat === c.id
                                            ? "border-primary bg-primary text-primary-foreground"
                                            : "border-border text-muted-foreground hover:border-primary hover:text-primary"
                                    }`}
                                >
                                    {c.label} ({count})
                                </button>
                            );
                        })}
                    </div>

                    {marketLoading ? (
                        <div className="stat-label text-muted-foreground py-8 text-center">Loading market…</div>
                    ) : filteredMarketListings.length === 0 ? (
                        <div className="stat-label text-muted-foreground py-8 text-center">No items in this category today.</div>
                    ) : (
                        <TooltipProvider delayDuration={120}>
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                                {filteredMarketListings.map((listing) => {
                                    if (listing._type === "tool") {
                                        const t = listing;
                                        const toolDef = { name: t.tool_name, tool_id: t.tool_id, rarity: "common", kind: "tool" };
                                        const tStock = toolStock[t.tool_id] ?? 0;
                                        const tStockPct = Math.round((tStock / TOOL_MAX_STOCK) * 100);
                                        const tOutOfStock = tStock <= 0;
                                        const needsRepair = t.owned && t.durability < t.max_durability;
                                        const canRepair = t.owned && needsRepair && character.gold >= t.repair_cost && toolBusy !== t.profession_id;
                                        const canBuy = !t.owned && character.gold >= t.purchase_cost && toolBusy !== t.profession_id && !tOutOfStock;
                                        return (
                                            <Tooltip key={t.item_id}>
                                                <TooltipTrigger asChild>
                                                    <div
                                                        data-testid={`market-item-${t.item_id}`}
                                                        className={`panel p-3 cursor-help border-border ${tOutOfStock && !t.owned ? "opacity-50" : ""}`}
                                                    >
                                                        <div className="flex justify-between items-start">
                                                            <div className="flex items-center gap-3">
                                                                <PixelSprite item={toolDef} size={36} />
                                                                <div>
                                                                    <div className="font-pixel text-lg uppercase text-primary">{t.tool_name}</div>
                                                                    <div className="stat-label flex items-center gap-2">
                                                                        {t.profession}
                                                                        {t.owned && <span className="text-green-400">OWNED</span>}
                                                                    </div>
                                                                </div>
                                                            </div>
                                                            <div className="text-right">
                                                                {t.owned ? (
                                                                    <div className={`font-mono text-sm ${needsRepair ? "text-amber-400" : "text-muted-foreground"}`}>
                                                                        {needsRepair ? `${t.repair_cost}g` : "FULL"}
                                                                    </div>
                                                                ) : (
                                                                    <div className={`font-mono text-sm ${canBuy ? "text-primary" : "text-destructive"}`}>
                                                                        {t.purchase_cost}g
                                                                    </div>
                                                                )}
                                                            </div>
                                                        </div>
                                                        {/* Stock bar */}
                                                        <div className="mt-2">
                                                            <div className="flex justify-between items-center mb-0.5">
                                                                <span className="stat-label text-[10px] text-muted-foreground">STOCK</span>
                                                                <span className={`stat-label text-[10px] ${tOutOfStock ? "text-destructive" : tStockPct < 25 ? "text-amber-400" : "text-muted-foreground"}`}>
                                                                    {tStock}/{TOOL_MAX_STOCK}
                                                                </span>
                                                            </div>
                                                            <div className="h-1.5 bg-background border border-border">
                                                                <div
                                                                    className={`h-full transition-all ${tOutOfStock ? "bg-destructive" : tStockPct < 25 ? "bg-amber-400" : "bg-primary"}`}
                                                                    style={{ width: `${tStockPct}%` }}
                                                                />
                                                            </div>
                                                        </div>
                                                        {/* Action button */}
                                                        <div className="flex gap-2 mt-2">
                                                            {t.owned ? (
                                                                <button
                                                                    data-testid={`repair-tool-${t.profession_id}`}
                                                                    disabled={!canRepair}
                                                                    onClick={() => repairTool(t.profession_id)}
                                                                    className="press-btn flex-1 stat-label border border-primary text-primary hover:bg-primary hover:text-primary-foreground disabled:opacity-40 flex items-center justify-center gap-1"
                                                                >
                                                                    <Coins size={12} />
                                                                    {needsRepair ? `REPAIR ${t.repair_cost}g` : "FULL"}
                                                                </button>
                                                            ) : (
                                                                <button
                                                                    data-testid={`buy-tool-${t.profession_id}`}
                                                                    disabled={!canBuy}
                                                                    onClick={() => buyTool(t.profession_id)}
                                                                    className="press-btn flex-1 stat-label border border-primary text-primary hover:bg-primary hover:text-primary-foreground disabled:opacity-40 flex items-center justify-center gap-1"
                                                                >
                                                                    <Coins size={12} />
                                                                    {tOutOfStock ? "SOLD OUT" : `BUY ${t.purchase_cost}g`}
                                                                </button>
                                                            )}
                                                        </div>
                                                    </div>
                                                </TooltipTrigger>
                                                <TooltipContent side="bottom" className="max-w-[260px] bg-popover border border-border text-popover-foreground">
                                                    <div className="font-pixel text-xs uppercase text-primary mb-1">{t.tool_name}</div>
                                                    <div className="text-[10px] space-y-1">
                                                        <div className="text-muted-foreground">Profession: {t.profession}</div>
                                                        <div className="text-muted-foreground">Type: Tool</div>
                                                        <div className="text-muted-foreground">Stock: {tStock}/{TOOL_MAX_STOCK}</div>
                                                        {t.owned ? (
                                                            <>
                                                                <div className="text-foreground">Durability: {t.durability}/{t.max_durability}</div>
                                                                {needsRepair && <div className="text-amber-400">Repair cost: {t.repair_cost}g</div>}
                                                            </>
                                                        ) : (
                                                            <>
                                                                <div className="text-muted-foreground">Max durability: {t.max_durability}</div>
                                                                <div className="text-primary">Purchase: {t.purchase_cost}g</div>
                                                            </>
                                                        )}
                                                    </div>
                                                </TooltipContent>
                                            </Tooltip>
                                        );
                                    }
                                    const it = listing.instance || gd.itemsById?.[listing.item_id];
                                    if (!it) return null;
                                    const iid = listing.item_id;
                                    const stockPct = Math.round((listing.stock / listing.max_stock) * 100);
                                    const outOfStock = listing.stock <= 0;
                                    const TrendIcon = TREND_ICONS[listing.trend || "flat"];
                                    const isDiscount = listing.discount_pct > 0;
                                    const isMarkup = listing.discount_pct < 0;
                                    const canAfford = character.gold >= listing.final_price * (buyQty[iid] || 1);
                                    return (
                                        <Tooltip key={iid}>
                                            <TooltipTrigger asChild>
                                                <div
                                                    data-testid={`market-item-${iid}`}
                                                    className={`panel p-3 cursor-help ${RARITY_CLASS[it.rarity]} ${outOfStock ? "opacity-50" : ""}`}
                                                >
                                                    <div className="flex justify-between items-start">
                                                        <div className="flex items-center gap-3">
                                                            <PixelSprite item={it} size={36} />
                                                            <div>
                                                                <div className={`font-pixel text-lg uppercase ${RARITY_TEXT[it.rarity]}`}>{it.name}</div>
                                                                <div className="stat-label flex items-center gap-2">
                                                                    {it.rarity} · {it.kind}
                                                                    {isDiscount && (
                                                                        <span className="text-green-400 font-bold">↓{listing.discount_pct}%</span>
                                                                    )}
                                                                    {isMarkup && (
                                                                        <span className="text-red-400 font-bold">↑{Math.abs(listing.discount_pct)}%</span>
                                                                    )}
                                                                </div>
                                                            </div>
                                                        </div>
                                                        <div className="text-right">
                                                            <div className={`font-mono text-sm ${canAfford ? "text-primary" : "text-destructive"}`}>
                                                                {listing.final_price}g
                                                            </div>
                                                            {listing.regional_price !== listing.final_price && (
                                                                <div className="text-[10px] text-muted-foreground line-through">
                                                                    {listing.regional_price}g
                                                                </div>
                                                            )}
                                                            <div className={`flex items-center justify-end gap-0.5 ${TrendIcon.color}`}>
                                                                <TrendIcon.icon size={10} />
                                                            </div>
                                                        </div>
                                                    </div>
                                                    {/* Stock bar */}
                                                    <div className="mt-2">
                                                        <div className="flex justify-between items-center mb-0.5">
                                                            <span className="stat-label text-[10px] text-muted-foreground">STOCK</span>
                                                            <span className={`stat-label text-[10px] ${outOfStock ? "text-destructive" : stockPct < 25 ? "text-amber-400" : "text-muted-foreground"}`}>
                                                                {listing.stock}/{listing.max_stock}
                                                            </span>
                                                        </div>
                                                        <div className="h-1.5 bg-background border border-border">
                                                            <div
                                                                className={`h-full transition-all ${outOfStock ? "bg-destructive" : stockPct < 25 ? "bg-amber-400" : "bg-primary"}`}
                                                                style={{ width: `${stockPct}%` }}
                                                            />
                                                        </div>
                                                    </div>
                                                    {/* Buy controls */}
                                                    {!outOfStock && (
                                                        <div className="flex gap-2 mt-2">
                                                            <input
                                                                type="number"
                                                                min={1}
                                                                max={listing.stock}
                                                                value={Math.min(buyQty[iid] || 1, listing.stock)}
                                                                onChange={(e) => setBuyQty({ ...buyQty, [iid]: Math.min(parseInt(e.target.value) || 1, listing.stock) })}
                                                                className="w-16 bg-background border border-border px-2 py-1 font-mono text-xs"
                                                                data-testid={`market-qty-${iid}`}
                                                            />
                                                            <button
                                                                data-testid={`market-buy-${iid}`}
                                                                disabled={!canAfford}
                                                                onClick={() => buy(iid)}
                                                                className="press-btn flex-1 stat-label border border-primary text-primary hover:bg-primary hover:text-primary-foreground disabled:opacity-40"
                                                            >
                                                                BUY
                                                            </button>
                                                        </div>
                                                    )}
                                                    {outOfStock && (
                                                        <div className="stat-label text-destructive text-center mt-2 text-xs">SOLD OUT</div>
                                                    )}
                                                </div>
                                            </TooltipTrigger>
                                            <TooltipContent side="bottom" className="max-w-[260px] bg-popover border border-border text-popover-foreground">
                                                <div className="font-pixel text-xs uppercase text-primary mb-1">{it.name}</div>
                                                <div className="text-[10px] space-y-1">
                                                    <div className="text-muted-foreground">Rarity: {it.rarity}</div>
                                                    <div className="text-muted-foreground">Type: {it.kind}{it.weapon_type ? ` · ${it.weapon_type}` : ""}{it.two_handed ? " · 2H" : ""}</div>
                                                    {it.base_stats && Object.keys(it.base_stats).length > 0 && (
                                                        <div className="text-foreground font-mono">
                                                            {Object.entries(it.base_stats).filter(([,v]) => v).map(([k,v]) => `${k.slice(0,3).toUpperCase()} +${v}`).join(" · ")}
                                                        </div>
                                                    )}
                                                    {it.prefixes?.length > 0 && it.prefixes.map((p, i) => (
                                                        <div key={`pfx-${i}`} className="text-cyan-400">
                                                            {Object.entries(p.stats || {}).filter(([,v]) => v).map(([k,v]) => `${k.slice(0,3).toUpperCase()} +${v}`).join(" · ")}
                                                        </div>
                                                    ))}
                                                    {it.suffixes?.length > 0 && it.suffixes.map((s, i) => (
                                                        <div key={`sfx-${i}`} className="text-orange-400">
                                                            {Object.entries(s.stats || {}).filter(([,v]) => v).map(([k,v]) => `${k.slice(0,3).toUpperCase()} +${v}`).join(" · ")}
                                                        </div>
                                                    ))}
                                                    {!it.base_stats && statLine(it) !== "—" && <div className="text-foreground">{statLine(it)}</div>}
                                                    {it.desc && <div className="text-muted-foreground italic">{it.desc}</div>}
                                                    <div className="border-t border-border pt-1 mt-1">
                                                        <div className="text-muted-foreground">Base: {listing.base_price}g</div>
                                                        {listing.regional_mult !== 1.0 && (
                                                            <div className="text-muted-foreground">
                                                                Regional: ×{listing.regional_mult} ({listing.regional_price}g)
                                                            </div>
                                                        )}
                                                        <div className="text-muted-foreground">
                                                            Daily mod: ×{listing.price_mod}
                                                        </div>
                                                        <div className="text-primary">Final: {listing.final_price}g</div>
                                                    </div>
                                                    {listing.price_history?.length > 1 && (
                                                        <div className="border-t border-border pt-1 mt-1">
                                                            <div className="stat-label text-muted-foreground mb-0.5">7-DAY HISTORY</div>
                                                            <div className="flex items-end gap-0.5 h-8">
                                                                {listing.price_history.map((ph, i) => {
                                                                    const maxP = Math.max(...listing.price_history.map(p => p.price));
                                                                    const minP = Math.min(...listing.price_history.map(p => p.price));
                                                                    const range = maxP - minP || 1;
                                                                    const h = 20 + ((ph.price - minP) / range) * 80;
                                                                    return (
                                                                        <div
                                                                            key={i}
                                                                            className="w-2 bg-primary/60"
                                                                            style={{ height: `${h}%` }}
                                                                            title={`${ph.day}: ${ph.price}g`}
                                                                        />
                                                                    );
                                                                })}
                                                            </div>
                                                        </div>
                                                    )}
                                                </div>
                                            </TooltipContent>
                                        </Tooltip>
                                    );
                                })}
                            </div>
                        </TooltipProvider>
                    )}

                    <div className="mt-6 border-t border-border pt-4">
                        <button
                            onClick={() => setShowSellInv((v) => !v)}
                            className="press-btn w-full font-pixel text-lg uppercase py-2 bg-primary/10 border border-primary text-primary hover:bg-primary hover:text-primary-foreground"
                        >
                            {showSellInv ? "CLOSE INVENTORY" : "SELL FROM INVENTORY"}
                        </button>
                        {showSellInv && (
                            <div className="mt-4">
                                <Inventory character={character} itemsById={gd.itemsById} onCharacterUpdate={onCharacterUpdate} onSell={sell} />
                            </div>
                        )}
                    </div>

                    {/* Heritage Vendor — only during festival */}
                    {heritageVendor && (
                        <TooltipProvider delayDuration={120}>
                        <div className="mt-6 border-t border-primary/30 pt-4" data-testid="heritage-vendor-section">
                            <div className="flex items-center justify-between mb-4">
                                <div className="flex items-center gap-2">
                                    <Crown size={24} className="text-primary" />
                                    <h3 className="font-pixel text-2xl uppercase text-primary">Heritage Vendor</h3>
                                </div>
                                <div className="stat-label text-primary flex items-center gap-1">
                                    <Coins size={14} /> {heritageVendor.token_balance} tokens
                                </div>
                            </div>
                            <p className="narr text-sm text-muted-foreground mb-4">
                                Exclusive festival items. Tokens carry over year to year — spend wisely or save for legendary gear.
                            </p>
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                                {heritageVendor.items?.map((item) => {
                                    const owned = heritageVendor.purchased?.includes(item.id);
                                    const canAfford = heritageVendor.token_balance >= item.cost;
                                    return (
                                        <Tooltip key={item.id}>
                                            <TooltipTrigger asChild>
                                                <div data-testid={`heritage-vendor-${item.id}`} className={`panel p-3 border cursor-help ${owned ? "border-primary/30 opacity-60" : "border-border"}`}>
                                                    <div className="flex justify-between items-start">
                                                        <div className="flex-1 min-w-0">
                                                            <div className={`font-pixel text-lg uppercase ${RARITY_TEXT[item.rarity] || "text-primary"}`}>{item.name}</div>
                                                            <div className="stat-label flex items-center gap-2 mt-0.5">
                                                                <span className="text-muted-foreground uppercase">{item.category}</span>
                                                                <span className={RARITY_TEXT[item.rarity] || "text-primary"}>{item.rarity}</span>
                                                            </div>
                                                        </div>
                                                        <div className="text-right flex-shrink-0 ml-2">
                                                            {owned ? (
                                                                <CheckCircle2 size={20} className="text-primary" />
                                                            ) : (
                                                                <div className={`font-mono text-sm ${canAfford ? "text-primary" : "text-destructive"} flex items-center gap-1`}>
                                                                    <Coins size={12} /> {item.cost}
                                                                </div>
                                                            )}
                                                        </div>
                                                    </div>
                                                    {!owned && (
                                                        <button
                                                            data-testid={`heritage-buy-${item.id}`}
                                                            onClick={() => buyHeritageItem(heritageVendor.continent, item.id)}
                                                            disabled={!canAfford}
                                                            className="press-btn w-full mt-2 stat-label py-1 border border-primary text-primary hover:bg-primary hover:text-primary-foreground disabled:opacity-40"
                                                        >
                                                            BUY
                                                        </button>
                                                    )}
                                                    {owned && (
                                                        <div className="stat-label text-center mt-2 text-primary/50">✓ OWNED</div>
                                                    )}
                                                </div>
                                            </TooltipTrigger>
                                            <TooltipContent side="bottom" className="max-w-[280px] bg-popover border border-border text-popover-foreground">
                                                <div className="font-pixel text-xs uppercase text-primary mb-1">{item.name}</div>
                                                <div className="text-[10px] space-y-1">
                                                    <div className="text-muted-foreground">Category: {item.category}</div>
                                                    <div className={RARITY_TEXT[item.rarity] || "text-primary"}>Rarity: {item.rarity}</div>
                                                    <div className="text-muted-foreground">Cost: {item.cost} tokens</div>
                                                    {item.desc && <div className="text-foreground italic pt-1 border-t border-border">{item.desc}</div>}
                                                </div>
                                            </TooltipContent>
                                        </Tooltip>
                                    );
                                })}
                            </div>
                        </div>
                        </TooltipProvider>
                    )}
                </div>
            )}

            {tab === "waypoint" && (
                <div className="panel p-6" data-testid="waypoint-panel">
                    <WaypointPanel character={character} onCharacterUpdate={onCharacterUpdate} onTravel={onTravel} />
                </div>
            )}

            {tab === "lounge" && (
                <div className="panel p-6" data-testid="lounge-panel">
                    <h2 className="font-pixel text-3xl uppercase text-primary mb-2">Adventurer&apos;s Lounge</h2>
                    <p className="narr text-muted-foreground mb-6">Combat bounties and weekly events for swords-for-hire.</p>
                    {(character.active_quests || []).filter((a) => {
                        const q = gd.questsById?.[a.quest_id];
                        return q && q.board === "lounge";
                    }).length > 0 && (
                        <div className="mb-6">
                            <h3 className="font-pixel text-xl uppercase text-primary/80 mb-3">Active Quests</h3>
                            <div className="space-y-3">
                                {(character.active_quests || []).filter((a) => {
                                    const q = gd.questsById?.[a.quest_id];
                                    return q && q.board === "lounge";
                                }).map((a) => {
                                    const q = gd.questsById?.[a.quest_id];
                                    return (
                                        <div key={a.quest_id} className="panel p-4 border border-primary/30">
                                            <div className="flex justify-between items-start">
                                                <div>
                                                    <div className="font-pixel text-lg uppercase text-primary">{q.title}</div>
                                                    <p className="narr text-sm text-foreground/80 mt-1">{q.brief}</p>
                                                </div>
                                                <button
                                                    data-testid={`abandon-quest-${a.quest_id}`}
                                                    onClick={() => abandonQuest(a.quest_id)}
                                                    className="press-btn stat-label px-3 py-1 border border-destructive/60 text-destructive/80 hover:bg-destructive hover:text-destructive-foreground"
                                                >
                                                    <XCircle size={12} className="inline mr-1" />DROP
                                                </button>
                                            </div>
                                        </div>
                                    );
                                })}
                            </div>
                        </div>
                    )}

                    {events.length === 0 && loungeQuests.length === 0 && (
                        <div className="stat-label text-muted-foreground">The lounge is quiet right now.</div>
                    )}

                    {events.length > 0 && (
                        <div className="mb-6">
                            <h3 className="font-pixel text-xl uppercase text-primary/80 mb-3">Active Events</h3>
                            <div className="space-y-3">
                                {events.map((e) => {
                                    const isJoined = (character.active_quests || []).some((a) => a.quest_id === e.id);
                                    return (
                                        <div key={e.id} data-testid={`lounge-event-${e.id}`} className="panel p-4">
                                            <div className="stat-label text-primary/70">{e.kind?.toUpperCase()} · LV {e.level_req}+</div>
                                            <div className="font-pixel text-xl uppercase text-primary mt-1">{e.name}</div>
                                            <p className="narr text-sm text-foreground/85 mt-2">{e.brief}</p>
                                            <div className="stat-label mt-2 text-primary">+{e.reward?.gold ?? 0}g · +{e.reward?.xp ?? 0}xp</div>
                                            <button
                                                data-testid={`join-event-${e.id}`}
                                                onClick={() => joinEvent(e.id)}
                                                disabled={isJoined}
                                                className="press-btn mt-3 stat-label px-3 py-1 border border-primary text-primary hover:bg-primary hover:text-primary-foreground disabled:opacity-40"
                                            >
                                                {isJoined ? "JOINED" : "JOIN EVENT"}
                                            </button>
                                        </div>
                                    );
                                })}
                            </div>
                        </div>
                    )}

                    {loungeQuests.length > 0 && (
                        <div>
                            <h3 className="font-pixel text-xl uppercase text-primary/80 mb-3">Bounties</h3>
                            <div className="space-y-3">
                                {loungeQuests.map((q) => (
                                    <div key={q.id} data-testid={`lounge-quest-${q.id}`} className="panel p-4">
                                        <div className="flex justify-between items-start">
                                            <div>
                                                <div className="stat-label text-primary/70">{q.category?.toUpperCase() || "QUEST"} · LV {q.level_req}+</div>
                                                <div className="font-pixel text-xl uppercase text-primary mt-1">{q.title}</div>
                                            </div>
                                            <div className="stat-label text-primary">+{q.reward?.gold ?? 0}g · +{q.reward?.xp ?? 0}xp</div>
                                        </div>
                                        <p className="narr text-sm text-foreground/85 mt-2">{q.brief}</p>
                                        <button
                                            data-testid={`accept-quest-${q.id}`}
                                            onClick={() => acceptQuest(q.id)}
                                            className="press-btn mt-3 stat-label px-3 py-1 border border-primary text-primary hover:bg-primary hover:text-primary-foreground"
                                        >
                                            ACCEPT
                                        </button>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}
                </div>
            )}

            {tab === "festival" && heritageData && (
                <div className="panel p-6 space-y-4" data-testid="festival-panel">
                    <div className="border-b border-primary/30 pb-4">
                        <div className="flex items-center gap-2 mb-2">
                            <Crown size={28} className="text-primary" />
                            <h2 className="font-pixel text-3xl uppercase text-primary">{heritageData.name}</h2>
                        </div>
                        <p className="narr text-muted-foreground">{heritageData.desc}</p>
                        {heritageData.bonuses && (
                            <div className="mt-3 stat-label text-primary/80 border border-primary/20 bg-primary/5 p-2">
                                ✦ {heritageData.bonuses.desc}
                            </div>
                        )}
                    </div>

                    {/* Heritage Boss */}
                    {heritageData.bossInfo?.active && (
                        <div className="border border-primary/30 bg-primary/5 p-4">
                            <div className="flex items-center gap-2 mb-2">
                                <Swords size={20} className="text-primary" />
                                <h3 className="font-pixel text-xl uppercase text-primary">{heritageData.bossInfo?.boss?.name || "Unknown Boss"}</h3>
                            </div>
                            <div className="grid grid-cols-3 gap-2 stat-label">
                                <div>Threat: <span className="text-primary">{heritageData.bossInfo?.boss?.threat ?? "?"}</span></div>
                                <div>HP: <span className="text-primary">{heritageData.bossInfo?.boss?.hp ?? "?"}</span></div>
                                <div>Tokens: <span className="text-primary">{heritageData.bossInfo?.boss?.token_reward ?? 0}</span></div>
                            </div>
                            <p className="text-xs text-foreground/70 italic mt-2">{heritageData.bossInfo?.boss?.mechanic || ""}</p>
                            <p className="stat-label text-muted-foreground mt-2">Kills: {heritageData.bossInfo?.kill_count ?? 0}</p>
                            <div className="mt-3 border-t border-primary/20 pt-3">
                                <div className="stat-label text-primary/80 flex items-center gap-1">
                                    <MapPin size={14} /> Found in: <span className="text-primary uppercase">{(heritageData.bossInfo?.boss?.biome || "unknown").replace(/_/g, " ")}</span>
                                </div>
                                <p className="text-xs text-muted-foreground mt-1">
                                    Leave town and travel to this biome to challenge the boss. The boss will appear as a special encounter there.
                                </p>
                            </div>
                        </div>
                    )}

                    {/* Daily Heritage Quests */}
                    {heritageQuests?.active && (
                        <div>
                            <h3 className="font-pixel text-xl uppercase text-primary mb-3">Daily Festival Quests</h3>
                            <div className="space-y-3">
                                {heritageQuests.quests?.map((q) => {
                                    const qPct = Math.min(100, Math.round(((q.current || 0) / (q.count || 1)) * 100));
                                    const qComplete = (q.current || 0) >= (q.count || 1);
                                    return (
                                    <div key={q.id} data-testid={`festival-quest-${q.id}`} className="panel p-4 border border-border">
                                        <div className="flex items-start gap-2">
                                            {q.claimed ? (
                                                <CheckCircle2 size={16} className="text-primary flex-shrink-0 mt-1" />
                                            ) : (
                                                <Circle size={16} className="text-muted-foreground flex-shrink-0 mt-1" />
                                            )}
                                            <div className="flex-1 min-w-0">
                                                <div className="font-pixel text-lg uppercase text-primary">{q.name}</div>
                                                <p className="narr text-sm text-foreground/85 mt-1">{q.brief}</p>
                                                {!q.claimed && (
                                                    <div className="mt-2">
                                                        <div className="h-1.5 bg-background border border-border">
                                                            <div className={`h-full transition-all ${qComplete ? "bg-primary" : "bg-primary/60"}`} style={{ width: `${qPct}%` }} />
                                                        </div>
                                                        <div className="flex justify-between stat-label mt-1">
                                                            <span className={qComplete ? "text-primary" : "text-muted-foreground"}>{q.current || 0}/{q.count}</span>
                                                            <span className="text-primary"><Coins size={12} className="inline" /> {q.token_reward} tokens</span>
                                                        </div>
                                                    </div>
                                                )}
                                                <div className="flex justify-end items-center mt-2">
                                                    {!q.claimed && (
                                                        <button
                                                            data-testid={`claim-festival-${q.id}`}
                                                            onClick={() => claimHeritageQuest(q.id)}
                                                            className={`press-btn stat-label px-3 py-1 border ${qComplete ? "border-primary text-primary hover:bg-primary hover:text-primary-foreground" : "border-border text-muted-foreground/50"}`}
                                                        >
                                                            CLAIM
                                                        </button>
                                                    )}
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                    );
                                })}
                            </div>
                            {heritageQuests.all_claimed && (
                                <div className="mt-3 text-center stat-label text-primary border border-primary/30 bg-primary/5 p-2">
                                    <Crown size={14} className="inline mr-1" /> All quests complete! +{heritageQuests.bonus_tokens} bonus tokens!
                                </div>
                            )}
                        </div>
                    )}

                    {/* Heritage Ladder */}
                    {heritageLadder?.active && (
                        <div>
                            <h3 className="font-pixel text-xl uppercase text-primary mb-3 flex items-center gap-1">
                                <Trophy size={18} /> Festival Ladder
                            </h3>
                            <div className="space-y-1 max-h-[200px] overflow-y-auto">
                                {heritageLadder.rankings?.length > 0 ? heritageLadder.rankings.map((r, i) => (
                                    <div key={r.character_id} className={`flex items-center gap-2 border border-border p-2 ${i < 3 ? "bg-primary/5" : ""}`}>
                                        <span className="stat-label text-primary w-6">#{i + 1}</span>
                                        <div className="flex-1 min-w-0">
                                            <div className="text-xs font-mono text-foreground truncate">{r.name}</div>
                                            <div className="stat-label text-muted-foreground text-[10px]">
                                                Score: {r.score} · Boss: {r.boss_kills} · Quests: {r.daily_quests_completed}
                                            </div>
                                        </div>
                                    </div>
                                )) : (
                                    <div className="stat-label text-muted-foreground text-center py-2">No entries yet. Be the first!</div>
                                )}
                            </div>
                        </div>
                    )}

                    <div className="stat-label text-muted-foreground text-center pt-2">
                        Visit the Market for the Heritage Vendor. Spend tokens earned from quests and boss kills.
                    </div>
                </div>
            )}

            {tab === "notice" && (
                <div className="panel p-6" data-testid="notice-panel">
                    <h2 className="font-pixel text-3xl uppercase text-primary mb-2">Notice Board</h2>
                    <p className="narr text-muted-foreground mb-6">Crafting, gathering, and profession contracts posted by locals.</p>
                    {(character.active_quests || []).filter((a) => {
                        const q = gd.questsById?.[a.quest_id];
                        return q && q.board === "notice";
                    }).length > 0 && (
                        <div className="mb-6">
                            <h3 className="font-pixel text-xl uppercase text-primary/80 mb-3">Active Quests</h3>
                            <div className="space-y-3">
                                {(character.active_quests || []).filter((a) => {
                                    const q = gd.questsById?.[a.quest_id];
                                    return q && q.board === "notice";
                                }).map((a) => {
                                    const q = gd.questsById?.[a.quest_id];
                                    return (
                                        <div key={a.quest_id} className="panel p-4 border border-primary/30">
                                            <div className="flex justify-between items-start">
                                                <div>
                                                    <div className="font-pixel text-lg uppercase text-primary">{q.title}</div>
                                                    <p className="narr text-sm text-foreground/80 mt-1">{q.brief}</p>
                                                </div>
                                                <button
                                                    data-testid={`abandon-quest-${a.quest_id}`}
                                                    onClick={() => abandonQuest(a.quest_id)}
                                                    className="press-btn stat-label px-3 py-1 border border-destructive/60 text-destructive/80 hover:bg-destructive hover:text-destructive-foreground"
                                                >
                                                    <XCircle size={12} className="inline mr-1" />DROP
                                                </button>
                                            </div>
                                        </div>
                                    );
                                })}
                            </div>
                        </div>
                    )}
                    {noticeQuests.length === 0 && (
                        <div className="stat-label text-muted-foreground">No new notices right now.</div>
                    )}
                    <div className="space-y-3">
                        {noticeQuests.map((q) => (
                            <div key={q.id} data-testid={`notice-quest-${q.id}`} className="panel p-4">
                                <div className="flex justify-between items-start">
                                    <div>
                                        <div className="stat-label text-primary/70">{q.category?.toUpperCase() || "QUEST"} · LV {q.level_req}+</div>
                                        <div className="font-pixel text-xl uppercase text-primary mt-1">{q.title}</div>
                                    </div>
                                    <div className="stat-label text-primary">+{q.reward?.gold ?? 0}g · +{q.reward?.xp ?? 0}xp</div>
                                </div>
                                <p className="narr text-sm text-foreground/85 mt-2">{q.brief}</p>
                                <button
                                    data-testid={`accept-quest-${q.id}`}
                                    onClick={() => acceptQuest(q.id)}
                                    className="press-btn mt-3 stat-label px-3 py-1 border border-primary text-primary hover:bg-primary hover:text-primary-foreground"
                                >
                                    ACCEPT
                                </button>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {tab === "trainers" && (
                <div className="panel p-6" data-testid="trainers-panel">
                    <h2 className="font-pixel text-3xl uppercase text-primary mb-2">Skill Trainers</h2>
                    <p className="narr text-muted-foreground mb-6">Local masters who will teach — for a price. Higher skills cost more and take longer.</p>
                    {character.training_skill_id && (
                        <div className="panel p-4 mb-4 border border-primary">
                            <div className="stat-label text-primary/70">Training</div>
                            <div className="font-pixel text-lg uppercase text-primary">
                                {gd.skillsById?.[character.training_skill_id]?.name || character.training_skill_id}
                            </div>
                            <div className="font-mono text-sm text-foreground mt-1">
                                {(() => {
                                    const remain = Math.max(0, Math.ceil((new Date(character.training_until).getTime() - now) / 1000));
                                    return remain > 0 ? formatTime(remain) : "READY";
                                })()}
                            </div>
                            <button
                                data-testid="finish-learn-btn"
                                onClick={finishLearn}
                                disabled={new Date(character.training_until).getTime() > now}
                                className="press-btn mt-2 stat-label px-3 py-1 border border-primary text-primary hover:bg-primary hover:text-primary-foreground disabled:opacity-40"
                            >
                                FINISH
                            </button>
                        </div>
                    )}
                    <div className="space-y-3">
                        {(gd.teachers || []).filter((t) => t.town_id === town.id).map((teacher) => {
                            const visibleSkills = teacher.teaches.filter((o) => {
                                const sid = typeof o === "string" ? o : o.skill_id;
                                const skill = gd.skillsById?.[sid];
                                if (!skill) return false;
                                const masteryOk = !(skill.mastery_req?.length) || (skill.mastery_req || []).some((m) => (character.masteries || []).includes(m));
                                return masteryOk;
                            });
                            if (visibleSkills.length === 0) return null;
                            return (
                                <div key={teacher.id} data-testid={`town-trainer-${teacher.id}`} className="panel p-4">
                                    <div className="font-pixel text-xl uppercase text-primary">{teacher.name}</div>
                                    <div className="narr text-sm text-muted-foreground mb-3">{teacher.desc}</div>
                                    <div className="stat-label text-primary/80 mb-2">TEACHES:</div>
                                    <div className="space-y-2">
                                        {visibleSkills.map((o) => {
                                            const sid = typeof o === "string" ? o : o.skill_id;
                                            const skill = gd.skillsById?.[sid];
                                            if (!skill) return null;
                                            const learned = (character.skills || []).some((s) => (s.skill_id || s) === sid);
                                            const levelOk = character.level >= (skill.level_req || 1);
                                            const goldOk = character.gold >= (skill.cost_gold || 0);
                                            const busy = !!character.training_skill_id;
                                            const disabled = learned || !levelOk || !goldOk || busy;
                                            const status = learned ? "KNOWN" : !levelOk ? "LOW LEVEL" : !goldOk ? "NO GOLD" : busy ? "BUSY" : "LEARN";
                                            const rarityColor = RARITY_TEXT[skill.rarity] || "text-muted-foreground";
                                            const powerLabel = { strike: "Strike", heal: "Heal", defend: "Defend", buff: "Buff", debuff: "Debuff", imbue: "Imbue", performance: "Performance" }[skill.power_type] || skill.power_type;
                                            const triggerLabel = { always: "Always", low_hp: "Low HP", opponent_wounded: "Enemy Wounded", opponent_status: "Enemy Status", opening_move: "Opening Move", self_debuff: "When Debuffed" }[skill.trigger] || skill.trigger;
                                            const learnMin = Math.floor((skill.learn_seconds || 0) / 60);
                                            const learnSec = (skill.learn_seconds || 0) % 60;
                                            const learnDisplay = learnMin > 0 ? `${learnMin}m ${learnSec}s` : `${learnSec}s`;
                                            return (
                                                <div key={sid} className="flex justify-between items-center border-t border-border pt-2">
                                                    <TooltipProvider>
                                                        <Tooltip>
                                                            <TooltipTrigger asChild>
                                                                <div className="cursor-help flex-1">
                                                                    <div className={`font-mono text-sm ${rarityColor}`}>{skill.name}</div>
                                                                    <div className="stat-label text-muted-foreground">
                                                                        {skill.rarity} · {skill.cost_gold}g · Learn: {learnDisplay} · Lv {skill.level_req || 1}
                                                                    </div>
                                                                </div>
                                                            </TooltipTrigger>
                                                            <TooltipContent side="top" sideOffset={2} className="max-w-sm p-0 bg-popover border border-border text-popover-foreground">
                                                                <div className="p-3 space-y-2">
                                                                    <div className="flex items-center gap-2">
                                                                        <span className={`font-pixel text-sm uppercase ${rarityColor}`}>{skill.name}</span>
                                                                        <span className="text-[10px] opacity-70 uppercase">{skill.rarity}</span>
                                                                    </div>
                                                                    {skill.execution_text ? (
                                                                        <div className="narr text-xs italic leading-relaxed border-l-2 border-primary/40 pl-2">
                                                                            {skill.execution_text}
                                                                        </div>
                                                                    ) : (
                                                                        <div className="text-xs">{skill.desc}</div>
                                                                    )}
                                                                    <div className="border-t border-primary/20 pt-2 space-y-0.5 text-[10px]">
                                                                        {skill.power_type && (
                                                                            <div><span className="opacity-60">Type:</span> {powerLabel}{skill.damage_type ? ` (${skill.damage_type})` : ""}</div>
                                                                        )}
                                                                        {skill.damage > 0 && (
                                                                            <div><span className="opacity-60">Power:</span> {skill.damage}</div>
                                                                        )}
                                                                        {skill.cooldown != null && (
                                                                            <div><span className="opacity-60">Cooldown:</span> {skill.cooldown} turn{skill.cooldown !== 1 ? "s" : ""}</div>
                                                                        )}
                                                                        {skill.heal_percent && (
                                                                            <div><span className="opacity-60">Heal:</span> {Math.round(skill.heal_percent * 100)}% HP</div>
                                                                        )}
                                                                        {skill.status_apply && (
                                                                            <div><span className="opacity-60">Inflicts:</span> {skill.status_apply}</div>
                                                                        )}
                                                                        {skill.self_status && (
                                                                            <div><span className="opacity-60">Grants:</span> {skill.self_status}</div>
                                                                        )}
                                                                        <div><span className="opacity-60">Trigger:</span> {triggerLabel}</div>
                                                                        {skill.weapon_req && skill.weapon_req !== "none" && (
                                                                            <div><span className="opacity-60">Weapon:</span> {skill.weapon_req}</div>
                                                                        )}
                                                                        {skill.mastery_req?.length > 0 && (
                                                                            <div><span className="opacity-60">Mastery:</span> {skill.mastery_req.join(", ")}</div>
                                                                        )}
                                                                    </div>
                                                                    <div className="border-t border-primary/20 pt-2 text-[10px]">
                                                                        <span className="opacity-60">Learn time:</span> {learnDisplay} · <span className="opacity-60">Cost:</span> {skill.cost_gold}g · <span className="opacity-60">Req:</span> Lv {skill.level_req || 1}
                                                                    </div>
                                                                </div>
                                                            </TooltipContent>
                                                        </Tooltip>
                                                    </TooltipProvider>
                                                    <button
                                                        data-testid={`teach-${teacher.id}-${sid}`}
                                                        disabled={disabled}
                                                        onClick={() => startLearn(sid, teacher.id)}
                                                        className="press-btn stat-label px-3 py-1 border border-primary text-primary hover:bg-primary hover:text-primary-foreground disabled:opacity-40"
                                                    >
                                                        {status}
                                                    </button>
                                                </div>
                                            );
                                        })}
                                    </div>
                                </div>
                            );
                        })}
                        {(gd.teachers || []).filter((t) => t.town_id === town.id).every((t) => {
                            return t.teaches.every((o) => {
                                const sid = typeof o === "string" ? o : o.skill_id;
                                const skill = gd.skillsById?.[sid];
                                if (!skill) return true;
                                return !(skill.mastery_req?.length) || !(skill.mastery_req || []).some((m) => (character.masteries || []).includes(m));
                            });
                        }) && (
                            <div className="stat-label text-muted-foreground">No trainers in this town have skills you can learn.</div>
                        )}
                    </div>
                </div>
            )}

            {tab === "trade" && (
                <div className="panel p-6" data-testid="trade-panel">
                    <TradeNpcPanel town={town} character={character} onCharacterUpdate={onCharacterUpdate} />
                </div>
            )}
            {tab === "runesmith" && (
                <RunesmithPanel character={character} onCharacterUpdate={onCharacterUpdate} />
            )}
            {tab === "gemsmith" && (
                <GemsmithPanel character={character} onCharacterUpdate={onCharacterUpdate} />
            )}
            {tab === "training_main" && (
                <TrainingPanel character={character} onCharacterUpdate={onCharacterUpdate} trainerType="main" />
            )}
            {tab === "training_life" && (
                <TrainingPanel character={character} onCharacterUpdate={onCharacterUpdate} trainerType="life" />
            )}
            {tab === "study" && (
                <StudyPanel character={character} onCharacterUpdate={onCharacterUpdate} />
            )}
            {questModal && (
                <QuestModal result={questModal} onClose={() => setQuestModal(null)} />
            )}
            {sanctuaryNarrative && (
                <div
                    className="fixed inset-0 z-40 bg-black/85 flex items-center justify-center p-4 animate-fade-in"
                    onClick={() => setSanctuaryNarrative(null)}
                >
                    <div
                        className="panel max-w-2xl w-full p-8 relative"
                        onClick={(e) => e.stopPropagation()}
                        style={{ boxShadow: "0 0 40px rgba(0,0,0,0.9)" }}
                    >
                        <div className="flex justify-between items-start mb-6">
                            <div className="flex items-center gap-3">
                                {sanctuaryNarrative.service === "rest" && <BedDouble size={48} className="text-primary/70" />}
                                {sanctuaryNarrative.service === "cleanse" && <Sparkles size={48} className="text-primary/70" />}
                                {sanctuaryNarrative.service === "blessing" && <Shield size={48} className="text-primary/70" />}
                                <div>
                                    <div className="font-pixel text-2xl uppercase text-primary">
                                        {sanctuaryNarrative.service === "rest" ? "Rest" : sanctuaryNarrative.service === "cleanse" ? "Cleansing" : "Blessing"}
                                    </div>
                                    <div className="stat-label text-muted-foreground">{sanctuaryNarrative.sanctuary_name} Sanctuary</div>
                                </div>
                            </div>
                            <div className="stat-label px-3 py-1 border-2 border-primary/40 font-pixel text-sm tracking-widest text-primary">
                                -{sanctuaryNarrative.cost}g
                            </div>
                        </div>
                        <div className="narr text-xl md:text-2xl text-foreground/95 leading-relaxed mb-6">
                            {sanctuaryNarrative.narrative}
                        </div>
                        <button
                            data-testid="sanctuary-narrative-close"
                            onClick={() => setSanctuaryNarrative(null)}
                            className="press-btn font-pixel text-lg uppercase px-6 py-2 bg-primary text-primary-foreground border-2 border-primary hover:bg-transparent hover:text-primary transition-colors"
                        >
                            Continue →
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
}
