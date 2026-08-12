import { useState, useEffect, useCallback } from "react";
import { api, extractError } from "@/lib/api";
import { toast } from "sonner";
import { Tent, Coins, Clock, Star, Compass, Sparkles, CheckCircle2, Timer } from "lucide-react";

const SPECIALTY_META = {
    hunting: { label: "Hunter", color: "text-red-400", desc: "Monster drops + XP" },
    gathering: { label: "Gatherer", color: "text-green-400", desc: "Materials, ore & herbs" },
    fishing: { label: "Fisher", color: "text-blue-400", desc: "Fish & aquatic treasures" },
};

const QUIRK_META = {
    lucky: { label: "Lucky", desc: "+10% rare drop chance" },
    greedy: { label: "Greedy", desc: "+50% cost, +20% yield" },
    night_owl: { label: "Night Owl", desc: "+30% yield on 4+ hr trips" },
    scout: { label: "Scout", desc: "+5% biome exploration per trip" },
};

const RANK_LABEL = {
    novice: "Novice",
    skilled: "Skilled",
    veteran: "Veteran",
    elite: "Elite",
};

function fmtCountdown(seconds) {
    if (seconds <= 0) return "Ready!";
    const h = Math.floor(seconds / 3600);
    const m = Math.floor((seconds % 3600) / 60);
    const s = Math.floor(seconds % 60);
    if (h > 0) return `${h}h ${m}m ${s}s`;
    if (m > 0) return `${m}m ${s}s`;
    return `${s}s`;
}

export default function ExpeditionPanel({ character, biomeId, onCharacterUpdate }) {
    const [data, setData] = useState(null);
    const [hours, setHours] = useState(1);
    const [busy, setBusy] = useState(false);
    const [now, setNow] = useState(Date.now());

    const fetchMerc = useCallback(async () => {
        if (!biomeId) return;
        try {
            const { data: d } = await api.get(`/game/expedition/merc/${biomeId}`);
            setData(d);
        } catch {
            setData(null);
        }
    }, [biomeId]);

    useEffect(() => {
        fetchMerc();
    }, [fetchMerc]);

    useEffect(() => {
        const t = setInterval(() => setNow(Date.now()), 1000);
        return () => clearInterval(t);
    }, []);

    if (!data?.merc) return null;

    const merc = data.merc;
    const specialty = SPECIALTY_META[merc.specialty] || SPECIALTY_META.gathering;
    const quirk = QUIRK_META[merc.quirk];
    const queue = data.queue;
    const queueRemaining = queue
        ? Math.max(0, Math.floor((new Date(queue.finishes_at) - now) / 1000))
        : 0;
    const queueReady = queue && queueRemaining <= 0;
    const queueIsHere = queue && queue.biome_id === biomeId;

    const cooldownRemaining = data.cooldown_until
        ? Math.max(0, Math.floor((new Date(data.cooldown_until) - now) / 1000))
        : 0;

    const cost = merc.hourly_rate * hours;
    const explorationLocked = data.exploration_pct < data.min_exploration;

    const yieldEstimate = (() => {
        let pts = hours * merc.efficiency * Math.max(0.1, data.exploration_pct / 100);
        pts *= merc.loyalty_mult || 1;
        if (merc.quirk === "greedy") pts *= 1.2;
        if (merc.quirk === "night_owl" && hours >= 4) pts *= 1.3;
        return pts;
    })();

    const handleStart = async () => {
        setBusy(true);
        try {
            const { data: d } = await api.post("/game/expedition/start", {
                biome_id: biomeId,
                hours,
            });
            onCharacterUpdate?.(d.character);
            toast.success(`${merc.name} sets out for ${hours}hr — come back later!`);
            fetchMerc();
        } catch (e) {
            toast.error(extractError(e));
        } finally {
            setBusy(false);
        }
    };

    const handleCollect = async () => {
        setBusy(true);
        try {
            const { data: d } = await api.post("/game/expedition/collect");
            onCharacterUpdate?.(d.character);
            const r = d.expedition_result;
            const lootStr = (r.loot || [])
                .map((l) => `${l.quantity}x ${l.item_id.replace(/_/g, " ")}`)
                .join(", ");
            toast.success(
                `${r.merc_name} returned! Loot: ${lootStr || "nothing"}` +
                (r.xp_gain ? ` · +${r.xp_gain} XP` : "") +
                (r.exploration_gain ? ` · +${r.exploration_gain}% exploration` : "")
            );
            if (r.rare_found) {
                toast.success(`RARE FIND: ${r.rare_found.replace(/_/g, " ")}!`, { duration: 6000 });
            }
            fetchMerc();
        } catch (e) {
            toast.error(extractError(e));
        } finally {
            setBusy(false);
        }
    };

    return (
        <div className="mt-6 border-2 border-border bg-card/50 p-4" data-testid="expedition-panel">
            <div className="flex items-center gap-2 mb-3">
                <Tent size={18} className="text-primary" />
                <span className="font-pixel text-sm uppercase text-primary">Mercenary Camp</span>
            </div>

            {/* Merc card */}
            <div className="flex items-start gap-3 mb-4">
                <div className="w-12 h-12 rounded-full bg-primary/20 flex items-center justify-center shrink-0">
                    <span className="font-pixel text-lg text-primary">{merc.name[0]}</span>
                </div>
                <div className="flex-1">
                    <div className="flex items-center gap-2 flex-wrap">
                        <span className="font-pixel text-xs uppercase">{merc.name}</span>
                        <span className="stat-label text-muted-foreground text-[10px]">
                            {RANK_LABEL[merc.rank]} <span className={specialty.color}>{specialty.label}</span>
                        </span>
                        {quirk && (
                            <span className="px-1.5 py-0.5 border border-amber-500/50 text-amber-500 text-[10px] font-pixel uppercase" title={quirk.desc}>
                                {quirk.label}
                            </span>
                        )}
                    </div>
                    <div className="text-xs text-muted-foreground italic mt-1">{merc.desc}</div>
                    <div className="flex gap-3 mt-1 text-xs text-muted-foreground">
                        <span className="flex items-center gap-1">
                            <Coins size={11} className="text-amber-500" /> {merc.hourly_rate}g/hr
                        </span>
                        <span>Efficiency: {Math.round(merc.efficiency * 100)}%</span>
                        {merc.loyalty_hires > 0 && (
                            <span className="flex items-center gap-1 text-green-500">
                                <Star size={11} /> {merc.loyalty_hires} hires
                                {merc.loyalty_mult > 1 && ` (+${Math.round((merc.loyalty_mult - 1) * 100)}% eff)`}
                            </span>
                        )}
                    </div>
                </div>
            </div>

            {/* Active expedition */}
            {queue && (
                <div className="border-2 border-primary/40 bg-primary/5 p-3 mb-3">
                    <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                            <Timer size={16} className={queueReady ? "text-green-500" : "text-primary"} />
                            <div>
                                <div className="font-pixel text-xs uppercase">
                                    {queue.merc_name} — {queue.hours}hr {queue.specialty}
                                    {!queueIsHere && <span className="text-muted-foreground"> (another biome)</span>}
                                </div>
                                <div className="stat-label text-muted-foreground text-xs">
                                    {queueReady ? (
                                        <span className="text-green-500 font-bold">Returned! Collect the haul.</span>
                                    ) : (
                                        <>Returns in {fmtCountdown(queueRemaining)}</>
                                    )}
                                </div>
                            </div>
                        </div>
                        {queueReady && (
                            <button
                                data-testid="expedition-collect"
                                disabled={busy}
                                onClick={handleCollect}
                                className="press-btn font-pixel text-xs uppercase px-3 py-1.5 border-2 border-green-500 text-green-500 hover:bg-green-500 hover:text-white disabled:opacity-40 flex items-center gap-1"
                            >
                                <CheckCircle2 size={13} /> Collect
                            </button>
                        )}
                    </div>
                </div>
            )}

            {/* Hire form */}
            {!queue && (
                <>
                    {explorationLocked ? (
                        <div className="stat-label text-muted-foreground text-xs">
                            <Compass size={12} className="inline mr-1" />
                            Explore this biome to at least {data.min_exploration}% to hire {merc.name} (currently {data.exploration_pct}%).
                        </div>
                    ) : cooldownRemaining > 0 ? (
                        <div className="stat-label text-muted-foreground text-xs">
                            <Clock size={12} className="inline mr-1" />
                            {merc.name} is resting. Available in {fmtCountdown(cooldownRemaining)}.
                        </div>
                    ) : (
                        <div className="space-y-3">
                            <div className="flex items-center gap-3">
                                <label className="stat-label text-muted-foreground text-xs">Hours:</label>
                                <input
                                    type="range"
                                    min={1}
                                    max={8}
                                    value={hours}
                                    onChange={(e) => setHours(parseInt(e.target.value))}
                                    className="flex-1 accent-primary"
                                    data-testid="expedition-hours"
                                />
                                <span className="font-pixel text-sm text-primary w-8 text-center">{hours}h</span>
                            </div>
                            <div className="flex gap-4 text-xs items-center flex-wrap">
                                <span className="flex items-center gap-1">
                                    <Coins size={12} className="text-amber-500" /> {cost.toLocaleString()}g
                                </span>
                                <span className="flex items-center gap-1 text-muted-foreground">
                                    <Sparkles size={12} /> ~{Math.max(1, Math.floor(yieldEstimate))}
                                    {yieldEstimate % 1 > 0.01 && "-" + (Math.floor(yieldEstimate) + 1)} items
                                </span>
                                {merc.quirk === "night_owl" && hours >= 4 && (
                                    <span className="text-amber-500">Night Owl bonus active!</span>
                                )}
                                {cost > (character?.gold ?? 0) && (
                                    <span className="text-red-500">Not enough gold</span>
                                )}
                            </div>
                            <button
                                data-testid="expedition-start"
                                disabled={busy || cost > (character?.gold ?? 0)}
                                onClick={handleStart}
                                className="press-btn font-pixel text-xs uppercase w-full px-4 py-2 border-2 border-primary text-primary hover:bg-primary hover:text-primary-foreground disabled:opacity-40 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                            >
                                <Tent size={13} /> {busy ? "Hiring..." : `Hire ${merc.name} (${cost.toLocaleString()}g)`}
                            </button>
                        </div>
                    )}
                </>
            )}

            {/* Loot preview */}
            {merc.loot_preview?.length > 0 && (
                <div className="mt-3 pt-3 border-t border-border/50">
                    <div className="stat-label text-muted-foreground text-[10px] mb-1">POSSIBLE LOOT ({specialty.desc}):</div>
                    <div className="flex flex-wrap gap-1.5">
                        {merc.loot_preview.map((id) => (
                            <span key={id} className="px-1.5 py-0.5 border border-border text-muted-foreground text-[10px] uppercase">
                                {id.replace(/_/g, " ")}
                            </span>
                        ))}
                        {merc.rare_preview?.map((id) => (
                            <span key={id} className="px-1.5 py-0.5 border border-amber-400/50 text-amber-400 text-[10px] uppercase">
                                {id.replace(/_/g, " ")} ★
                            </span>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
}
