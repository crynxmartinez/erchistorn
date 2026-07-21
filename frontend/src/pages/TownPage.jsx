import { useEffect, useState } from "react";
import { useNavigate, useParams, Link } from "react-router-dom";
import { api, extractError } from "@/lib/api";
import { useGameData, RARITY_TEXT, RARITY_CLASS } from "@/data/gameData";
import { toast } from "sonner";
import { BedDouble, ShoppingBag, ScrollText, Users, ArrowLeft, Coins, MessageCircle } from "lucide-react";
import NpcPanel from "@/components/NpcPanel";

export default function TownPage() {
    const { townId } = useParams();
    const navigate = useNavigate();
    const gd = useGameData();
    const [town, setTown] = useState(null);
    const [character, setCharacter] = useState(null);
    const [tab, setTab] = useState("voices");
    const [buyQty, setBuyQty] = useState({});
    const [availableQuests, setAvailableQuests] = useState([]);

    useEffect(() => {
        (async () => {
            try {
                const { data } = await api.post("/game/town/visit", { town_id: townId });
                setCharacter(data.character);
                setTown(data.town);
                const q = await api.get("/game/quests/available");
                setAvailableQuests(q.data.available);
            } catch (e) {
                toast.error(extractError(e));
                navigate("/game");
            }
        })();
    }, [townId, navigate]);

    if (!town || !character || !gd.ready) {
        return <div className="min-h-screen flex items-center justify-center text-primary font-pixel text-2xl">Approaching {townId}…</div>;
    }

    const rest = async () => {
        try {
            const { data } = await api.post("/game/town/inn");
            setCharacter(data.character);
            toast.success(`Rested at the inn — paid ${data.cost}g`);
        } catch (e) {
            toast.error(extractError(e));
        }
    };

    const buy = async (item_id) => {
        try {
            const qty = buyQty[item_id] || 1;
            const { data } = await api.post("/game/town/market/buy", { item_id, quantity: qty });
            setCharacter(data.character);
            toast.success(`Bought ${qty} × ${gd.itemsById[item_id]?.name} — ${data.paid}g`);
        } catch (e) {
            toast.error(extractError(e));
        }
    };

    const sell = async (item_id) => {
        try {
            const { data } = await api.post("/game/town/market/sell", { item_id, quantity: 1 });
            setCharacter(data.character);
            toast.success(`Sold — received ${data.received}g`);
        } catch (e) {
            toast.error(extractError(e));
        }
    };

    const acceptQuest = async (qid) => {
        try {
            await api.post(`/game/quests/${qid}/accept`);
            setAvailableQuests((prev) => prev.filter((q) => q.id !== qid));
            toast.success("Quest accepted");
        } catch (e) {
            toast.error(extractError(e));
        }
    };

    const leaveTown = async () => {
        try {
            await api.post("/game/town/leave");
        } catch { /* ignore */ }
        navigate("/game");
    };

    const TABS = [
        { id: "voices", label: "Voices", icon: MessageCircle, avail: true },
        { id: "inn", label: "Inn", icon: BedDouble, avail: town.services.includes("inn") },
        { id: "market", label: "Market", icon: ShoppingBag, avail: town.services.includes("market") },
        { id: "notice", label: "Notice Board", icon: ScrollText, avail: town.services.includes("notice_board") },
        { id: "trainers", label: "Trainers", icon: Users, avail: town.services.includes("trainers") },
    ].filter(t => t.avail);

    return (
        <div className="min-h-screen p-4 md:p-6" data-testid="town-page">
            <div className="max-w-6xl mx-auto">
                <div className="flex items-center justify-between mb-4">
                    <button onClick={leaveTown} data-testid="town-leave" className="stat-label text-primary/70 hover:text-primary flex items-center gap-1">
                        <ArrowLeft size={12} /> LEAVE TOWN
                    </button>
                    <Link to="/guild-house" data-testid="town-goto-guild" className="stat-label text-primary hover:text-primary/80">
                        GUILD HOUSE →
                    </Link>
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
                                onClick={() => setTab(t.id)}
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
                        <NpcPanel character={character} onCharacterUpdate={setCharacter} />
                    </div>
                )}

                {tab === "inn" && (
                    <div className="panel p-6" data-testid="inn-panel">
                        <h2 className="font-pixel text-3xl uppercase text-primary mb-2">The {town.name} Inn</h2>
                        <p className="narr text-muted-foreground mb-6">Warm hearth. Warm bread. A bed that does not bite. Rest here to restore health, clear debuffs, and reduce exhaustion.</p>
                        <div className="grid grid-cols-3 gap-4 font-mono text-sm mb-6">
                            <div><div className="stat-label">COST</div><div className="text-primary text-xl">{town.inn_cost}g</div></div>
                            <div><div className="stat-label">HP RESTORED</div><div className="text-primary text-xl">FULL</div></div>
                            <div><div className="stat-label">DEBUFFS</div><div className="text-primary text-xl">CLEARED</div></div>
                        </div>
                        <button
                            data-testid="inn-rest-btn"
                            onClick={rest}
                            disabled={character.gold < town.inn_cost}
                            className="press-btn font-pixel text-lg uppercase px-6 py-2 bg-primary text-primary-foreground border-2 border-primary hover:bg-transparent hover:text-primary transition-colors disabled:opacity-40"
                        >
                            REST — {town.inn_cost}g
                        </button>
                    </div>
                )}

                {tab === "market" && (
                    <div className="panel p-6" data-testid="market-panel">
                        <h2 className="font-pixel text-3xl uppercase text-primary mb-4">Marketplace</h2>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                            {(town.market_items || []).map((iid) => {
                                const it = gd.itemsById[iid];
                                if (!it) return null;
                                const price = { common: 10, uncommon: 40, rare: 120, epic: 350, legendary: 900, mythic: 2500 }[it.rarity] || 10;
                                return (
                                    <div key={iid} data-testid={`market-item-${iid}`} className={`panel p-3 ${RARITY_CLASS[it.rarity]}`}>
                                        <div className="flex justify-between items-start">
                                            <div>
                                                <div className={`font-pixel text-lg uppercase ${RARITY_TEXT[it.rarity]}`}>{it.name}</div>
                                                <div className="stat-label">{it.rarity} · {it.kind}</div>
                                            </div>
                                            <div className="text-primary font-mono text-sm">{price}g</div>
                                        </div>
                                        <div className="flex gap-2 mt-2">
                                            <input
                                                type="number"
                                                min={1}
                                                value={buyQty[iid] || 1}
                                                onChange={(e) => setBuyQty({ ...buyQty, [iid]: parseInt(e.target.value) || 1 })}
                                                className="w-16 bg-background border border-border px-2 py-1 font-mono text-xs"
                                                data-testid={`market-qty-${iid}`}
                                            />
                                            <button
                                                data-testid={`market-buy-${iid}`}
                                                onClick={() => buy(iid)}
                                                className="press-btn flex-1 stat-label border border-primary text-primary hover:bg-primary hover:text-primary-foreground"
                                            >
                                                BUY
                                            </button>
                                            <button
                                                data-testid={`market-sell-${iid}`}
                                                onClick={() => sell(iid)}
                                                className="press-btn stat-label px-2 border border-border text-muted-foreground hover:border-destructive hover:text-destructive"
                                            >
                                                SELL 1
                                            </button>
                                        </div>
                                    </div>
                                );
                            })}
                        </div>
                    </div>
                )}

                {tab === "notice" && (
                    <div className="panel p-6" data-testid="notice-panel">
                        <h2 className="font-pixel text-3xl uppercase text-primary mb-2">Notice Board</h2>
                        <p className="narr text-muted-foreground mb-6">Regional quests posted by locals and travelers.</p>
                        {availableQuests.length === 0 && (
                            <div className="stat-label text-muted-foreground">No new notices right now.</div>
                        )}
                        <div className="space-y-3">
                            {availableQuests.filter((q) => q.category !== "event").map((q) => (
                                <div key={q.id} data-testid={`notice-quest-${q.id}`} className="panel p-4">
                                    <div className="flex justify-between items-start">
                                        <div>
                                            <div className="stat-label text-primary/70">{q.category.toUpperCase()} · LV {q.level_req}+</div>
                                            <div className="font-pixel text-xl uppercase text-primary mt-1">{q.title}</div>
                                        </div>
                                        <div className="stat-label text-primary">+{q.reward.gold}g · +{q.reward.xp}xp</div>
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
                        <p className="narr text-muted-foreground mb-6">Local masters who will teach — for a price.</p>
                        <div className="space-y-3">
                            {(town.trainer_ids || []).map((tid) => {
                                const teacher = gd.teachers.find((t) => t.id === tid);
                                if (!teacher) return null;
                                return (
                                    <div key={tid} data-testid={`town-trainer-${tid}`} className="panel p-4">
                                        <div className="font-pixel text-xl uppercase text-primary">{teacher.name}</div>
                                        <div className="narr text-sm text-muted-foreground mb-3">{teacher.desc}</div>
                                        <div className="stat-label text-primary/80">TEACHES:</div>
                                        <ul className="text-xs font-mono mt-1 space-y-0.5">
                                            {teacher.teaches.map((o) => (
                                                <li key={o.skill_id}>
                                                    · {gd.skillsById[o.skill_id]?.name || o.skill_id} — {o.cost_gold}g, Lv {o.level_req}+
                                                </li>
                                            ))}
                                        </ul>
                                        <div className="stat-label mt-3 text-muted-foreground">Go to the Skills tab in the main HUD to learn.</div>
                                    </div>
                                );
                            })}
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}
