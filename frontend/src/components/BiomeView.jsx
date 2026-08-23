import { useEffect, useState, useRef } from "react";
import { api, extractError } from "@/lib/api";
import { toast } from "sonner";
import { Compass, Swords, Sprout, Fish, Skull, Clock, Wrench, Crown } from "lucide-react";
import { Tooltip, TooltipTrigger, TooltipContent, TooltipProvider } from "@/components/ui/tooltip";
import ExpeditionPanel from "@/components/ExpeditionPanel";

const RANK_LABELS = ["Novice", "Apprentice", "Journeyman", "Expert", "Master", "Grandmaster"];
const POINTS_PER_TIER = 10;

const ACTION_META = {
    hunt: { icon: Swords, label: "Hunt", flavor: "Pursue and slay." },
    gather: { icon: Sprout, label: "Gather", flavor: "Take what the land offers." },
    explore: { icon: Compass, label: "Explore", flavor: "Wander and see." },
    fish: { icon: Fish, label: "Fish", flavor: "Cast the line." },
    loot_ruins: { icon: Skull, label: "Loot Ruins", flavor: "Steal from the dead." },
};

const RARITY_STYLE = {
    common: "text-muted-foreground border-border",
    uncommon: "text-primary border-primary/40",
    rare: "text-amber-400 border-amber-400/50",
    epic: "text-orange-400 border-orange-400/50",
    legendary: "text-purple-400 border-purple-400/50",
    exotic: "text-pink-400 border-pink-400/50",
};

const RARITY_LABEL = {
    common: "Common",
    uncommon: "Uncommon",
    rare: "Rare",
    epic: "Epic",
    legendary: "Legendary",
    exotic: "Exotic",
};

export default function BiomeView({ character, continent, onBiomeChange, onActionResult, onCombatStart, onCharacterUpdate }) {
    const [actions, setActions] = useState([]);
    const [tools, setTools] = useState([]);
    const [exploration, setExploration] = useState(null);
    const [biomeLocked, setBiomeLocked] = useState(false);
    const [rolling, setRolling] = useState(false);
    const [heritageBoss, setHeritageBoss] = useState(null);
    const [now, setNow] = useState(Date.now());
    const actionsFetchedAt = useRef(0);
    const biome = character.current_biome;
    const biomeMeta = continent?.biomes?.find((b) => b.id === biome);

    // Tick every second for cooldown countdowns
    useEffect(() => {
        const timer = setInterval(() => setNow(Date.now()), 1000);
        return () => clearInterval(timer);
    }, []);

    useEffect(() => {
        if (!biome) return;
        (async () => {
            try {
                const [acts, t, ex] = await Promise.all([
                    api.get(`/game/data/biome/${biome}/actions`),
                    api.get("/game/tools"),
                    api.get("/game/exploration"),
                ]);
                setActions(acts.data.actions);
                actionsFetchedAt.current = Date.now();
                setBiomeLocked(acts.data.biome_unlocked === false);
                setTools(t.data.tools);
                setExploration(ex.data);
                // Check if heritage boss is in this biome
                try {
                    const hBoss = await api.get("/game/heritage/boss");
                    if (hBoss.data.active && hBoss.data.boss?.biome === biome) {
                        setHeritageBoss(hBoss.data);
                    } else {
                        setHeritageBoss(null);
                    }
                } catch { setHeritageBoss(null); }
            } catch (e) {
                toast.error(extractError(e));
            }
        })();
    }, [biome]);

    const doAction = async (action, targetId = null) => {
        if (rolling) return;
        setRolling(true);
        try {
            if (action === "hunt" && targetId) {
                // Trigger combat for hunt
                const { data } = await api.post("/game/combat/start", {
                    biome_id: biome,
                    monster_id: targetId,
                });
                onCombatStart?.(data);
                return;
            }
            const { data } = await api.post("/game/action", {
                action_id: action,
                biome_id: biome,
                target_id: targetId,
            });
            onActionResult?.(data);
            if (data.profession_ranks && data.profession_ranks.length > 0) {
                for (const [newRank, oldRank] of data.profession_ranks) {
                    toast.success(`Profession rank up: ${oldRank} → ${newRank}!`);
                }
            }
            // Refresh tools, actions, and exploration to update unlocks/cooldowns
            const [acts, t, ex] = await Promise.all([
                api.get(`/game/data/biome/${biome}/actions`),
                api.get("/game/tools"),
                api.get("/game/exploration"),
            ]);
            setActions(acts.data.actions);
            actionsFetchedAt.current = Date.now();
            setBiomeLocked(acts.data.biome_unlocked === false);
            setTools(t.data.tools);
            setExploration(ex.data);
        } catch (e) {
            toast.error(extractError(e));
        } finally {
            setRolling(false);
        }
    };

    const startHeritageBossFight = async () => {
        if (rolling) return;
        setRolling(true);
        try {
            const { data } = await api.post("/game/heritage/boss/start");
            if (data.combat?.error) { toast.error(data.combat.error); return; }
            onCombatStart?.({ state: data.combat, character: data.character });
        } catch (e) {
            toast.error(extractError(e));
        } finally {
            setRolling(false);
        }
    };

    const toolFor = (professionId) => tools.find((t) => t.profession_id === professionId);
    const formatCd = (secs) => secs > 60 ? `${Math.ceil(secs / 60)}m` : `${secs}s`;
    const elapsedSecs = actionsFetchedAt.current ? Math.floor((now - actionsFetchedAt.current) / 1000) : 0;
    const liveCd = (secs) => Math.max(0, secs - elapsedSecs);
    const buildRequirementsHint = (n, actionEntry) => {
        const hints = [];
        if (!n.has_profession) {
            hints.push(`Requires ${n.profession?.replace(/_/g, " ")} profession — learn in town`);
        } else if (!n.rank_ok) {
            hints.push(`Requires ${n.min_rank} ${n.profession?.replace(/_/g, " ")} rank`);
        }
        if (n.tool_ok === false) {
            hints.push(`Requires ${n.required_tool?.name || "a tool"} — buy in town`);
        }
        const cd = liveCd(n.cooldown_secs);
        if (cd > 0) {
            hints.push(`On cooldown: ${formatCd(cd)}`);
        }
        if (n.stock_current <= 0) {
            hints.push("Depleted — restocks over time");
        }
        return hints.length > 0 ? hints.join(" · ") : null;
    };
    const buildHuntHint = (actionEntry) => {
        const hints = [];
        if (actionEntry.tool_ok === false) {
            hints.push(`Requires ${actionEntry.tool_required?.name || "Hunter's Kit"} — buy in town`);
        }
        return hints.length > 0 ? hints.join(" · ") : null;
    };
    const biomeUnlocked = (id) => exploration?.biomes?.find((b) => b.biome_id === id)?.unlocked !== false;
    const biomeProgress = (id) => exploration?.biomes?.find((b) => b.biome_id === id)?.progress_pct || 0;
    const biomeRequired = (id) => exploration?.biomes?.find((b) => b.biome_id === id)?.required_pct || 0;

    // Extract unique gathering professions from action nodes
    const biomeProfessions = [...new Set(
        actions.flatMap(a => (a.resource_nodes || []).map(n => n.profession))
    )];

    return (
        <TooltipProvider delayDuration={120}>
        <div className="panel p-6" data-testid="biome-view">
            <div className="flex items-start justify-between mb-4">
                <div>
                    <div className="stat-label text-primary/80">{continent?.name}</div>
                    <h3 className="font-pixel text-3xl uppercase text-primary">{biomeMeta?.name || biome}</h3>
                    <div className="narr text-sm text-muted-foreground mt-2 max-w-2xl">
                        {biomeMeta?.desc}
                    </div>
                    {biomeProfessions.length > 0 && (
                        <div className="mt-2 flex flex-wrap gap-1.5">
                            <span className="stat-label text-muted-foreground text-[10px]">GATHERING:</span>
                            {biomeProfessions.map(pid => (
                                <span key={pid} className="px-1.5 py-0.5 border border-primary/30 text-primary text-[10px] font-pixel uppercase">
                                    {pid.replace(/_/g, " ")}
                                </span>
                            ))}
                        </div>
                    )}
                </div>
                {/* Exploration progress bar */}
                {exploration && (() => {
                    const pct = biomeProgress(biome);
                    const thresholds = [10, 25, 50, 75, 100];
                    return (
                        <div className="w-48 flex-shrink-0" data-testid="biome-progress-bar">
                            <div className="flex justify-between items-baseline mb-1">
                                <span className="stat-label text-primary/70 text-[10px]">EXPLORATION</span>
                                <span className="font-pixel text-sm text-primary">{pct}%</span>
                            </div>
                            <div className="relative h-3 bg-background border border-border">
                                <div
                                    className="h-full bg-primary transition-all"
                                    style={{ width: `${pct}%` }}
                                />
                                {thresholds.map(t => (
                                    <div
                                        key={t}
                                        className="absolute top-0 bottom-0 w-px bg-border/80"
                                        style={{ left: `${t}%` }}
                                        title={`${t}%`}
                                    />
                                ))}
                            </div>
                        </div>
                    );
                })()}
            </div>

            {/* Gathering profession progress for this biome */}
            {tools.length > 0 && (
                <div className="mb-4 flex flex-wrap gap-3">
                    {tools.map((t) => {
                        const xp = t.durability !== undefined ? null : null;
                        const prof = character.professions?.find((p) => p.id === t.profession_id);
                        if (!prof) return null;
                        const points = prof.xp || 0;
                        const tier = Math.min(Math.floor(points / POINTS_PER_TIER), RANK_LABELS.length - 1);
                        const intoTier = points % POINTS_PER_TIER;
                        const pct = (intoTier / POINTS_PER_TIER) * 100;
                        return (
                            <div key={t.profession_id} className="flex items-center gap-2 panel px-3 py-1.5">
                                <span className="stat-label text-primary text-xs uppercase">{t.profession}</span>
                                <span className="stat-label text-muted-foreground text-[10px]">{RANK_LABELS[tier]}</span>
                                <div className="w-16 h-1.5 bg-background border border-border">
                                    <div className="h-full bg-primary" style={{ width: `${pct}%` }} />
                                </div>
                                <span className="text-[10px] text-muted-foreground font-mono">{intoTier}/{POINTS_PER_TIER}</span>
                            </div>
                        );
                    })}
                </div>
            )}

            {continent?.biomes?.length > 1 && (
                <div className="mb-6 flex flex-wrap gap-2">
                    {continent.biomes.map((b) => {
                        const unlocked = biomeUnlocked(b.id);
                        const current = b.id === biome;
                        return (
                            <button
                                key={b.id}
                                data-testid={`biome-tab-${b.id}`}
                                onClick={() => unlocked && onBiomeChange?.(b.id)}
                                disabled={!unlocked}
                                className={`press-btn font-pixel text-sm uppercase px-3 py-1 border-2 ${
                                    current
                                        ? "border-primary bg-primary text-primary-foreground"
                                        : unlocked
                                            ? "border-border text-muted-foreground hover:border-primary hover:text-primary"
                                            : "border-border/50 text-muted-foreground/50 opacity-60"
                                }`}
                                title={unlocked ? b.name : `Explore ${biomeRequired(b.id)}% of ${b.name} to unlock (${biomeProgress(b.id)}%)`}
                            >
                                {b.name} {!unlocked && `(${biomeProgress(b.id)}/${biomeRequired(b.id)}%)`}
                            </button>
                        );
                    })}
                </div>
            )}

            {/* Heritage Boss — appears when player is in the boss biome */}
            {heritageBoss?.active && (
                <div className="mb-6 border-2 border-primary/50 bg-primary/5 p-4" data-testid="heritage-boss-card">
                    <div className="flex items-center gap-2 mb-3">
                        <Crown size={24} className="text-primary" />
                        <h3 className="font-pixel text-2xl uppercase text-primary">{heritageBoss.boss.name}</h3>
                        <span className="ml-auto stat-label text-primary/60 text-[10px]">FESTIVAL BOSS</span>
                    </div>
                    <div className="grid grid-cols-4 gap-3 stat-label mb-3">
                        <div>Threat: <span className="text-primary">{heritageBoss.boss.threat}</span></div>
                        <div>HP: <span className="text-primary">{heritageBoss.boss.hp}</span></div>
                        <div>Tokens: <span className="text-primary">{heritageBoss.boss.token_reward}</span></div>
                        <div>Your kills: <span className="text-primary">{heritageBoss.kill_count}</span></div>
                    </div>
                    <p className="text-xs text-foreground/70 italic mb-3">{heritageBoss.boss.mechanic}</p>
                    <button
                        data-testid="heritage-boss-challenge"
                        onClick={startHeritageBossFight}
                        disabled={rolling}
                        className="press-btn font-pixel text-lg uppercase px-6 py-2 border-2 border-primary text-primary hover:bg-primary hover:text-primary-foreground disabled:opacity-40"
                    >
                        <Swords size={16} className="inline mr-2" /> CHALLENGE THE BOSS
                    </button>
                </div>
            )}

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                {biomeLocked && (
                    <div className="col-span-full p-4 border border-destructive/50 bg-destructive/5 text-destructive stat-label">
                        This region is still unknown. Explore the previous land to unlock it.
                    </div>
                )}
                {actions.map((a) => {
                    const meta = ACTION_META[a.id] || { icon: Compass, label: a.name, flavor: "" };
                    const Ic = meta.icon;
                    const isGatherFish = a.id === "gather" || a.id === "fish";
                    const locked = !a.unlocked;
                    return (
                        <div key={a.id} className={`panel p-4 ${locked ? "opacity-60" : "hover:border-primary transition-colors"}`}>
                            <div className="flex items-center gap-2 mb-2">
                                <Ic className={locked ? "text-muted-foreground" : "text-primary"} size={20} strokeWidth={1.5} />
                                <div className={`font-pixel text-xl uppercase ${locked ? "text-muted-foreground" : "text-primary"}`}>{meta.label}</div>
                                {locked && (
                                    <span className="text-[10px] uppercase text-destructive ml-auto">Locked ({a.required_pct}%)</span>
                                )}
                            </div>
                            <div className="text-xs text-muted-foreground mb-3 narr">{meta.flavor}</div>

                            {/* Resource nodes for gather/fish */}
                            {isGatherFish && (
                                <div className="space-y-1.5 mb-3">
                                    {a.resource_nodes && a.resource_nodes.length > 0 ? (
                                        a.resource_nodes.map((n) => {
                                            const tool = toolFor(n.profession);
                                            const toolLow = tool && tool.durability < tool.max_durability * 0.2;
                                            const noTool = n.tool_ok === false;
                                            const cd = liveCd(n.cooldown_secs);
                                            const disabled = rolling || locked || cd > 0 || !n.rank_ok || n.stock_current <= 0;
                                            const hint = buildRequirementsHint(n, a);
                                            return (
                                                <Tooltip key={n.id}>
                                                    <TooltipTrigger asChild>
                                                        <button
                                                            data-testid={`action-${a.id}-${n.id}`}
                                                            disabled={disabled}
                                                            onClick={() => doAction(a.id, n.id)}
                                                            className={`press-btn w-full text-left px-2 py-1.5 border ${RARITY_STYLE[n.rarity] || RARITY_STYLE.common} disabled:opacity-40 disabled:cursor-not-allowed ${noTool ? "opacity-60" : ""}`}
                                                        >
                                                            <div className="flex justify-between items-center">
                                                                <span className="font-mono text-xs uppercase">› {n.name}</span>
                                                                <span className="text-[10px] uppercase">{RARITY_LABEL[n.rarity]}</span>
                                                            </div>
                                                            <div className="flex justify-between items-center text-[10px] mt-0.5">
                                                                <span className={n.has_profession ? (n.rank_ok ? "text-green-500" : "text-amber-400") : "text-destructive"}>
                                                                    {n.required_tool?.name || n.profession} · {n.min_rank}
                                                                    {!n.has_profession && <span className="ml-1">(missing)</span>}
                                                                    {n.has_profession && !n.rank_ok && <span className="ml-1">(low rank)</span>}
                                                                </span>
                                                                <span className="text-muted-foreground">
                                                                    {n.stock_current}/{n.stock_max}
                                                                </span>
                                                            </div>
                                                            <div className="flex justify-between items-center text-[10px] mt-0.5">
                                                                {cd > 0 ? (
                                                                    <span className="flex items-center gap-0.5 text-destructive">
                                                                        <Clock size={9} /> {formatCd(cd)}
                                                                    </span>
                                                                ) : noTool ? (
                                                                    <span className="text-destructive">Need {n.required_tool?.name || "tool"} — buy in town</span>
                                                                ) : tool ? (
                                                                    <span className={`flex items-center gap-0.5 ${toolLow ? "text-destructive" : "text-muted-foreground"}`}>
                                                                        <Wrench size={9} /> {tool.durability}/{tool.max_durability}
                                                                    </span>
                                                                ) : null}
                                                                {n.stock_current <= 0 && <span className="text-destructive">Depleted</span>}
                                                            </div>
                                                        </button>
                                                    </TooltipTrigger>
                                                    {hint && (
                                                        <TooltipContent side="top" className="max-w-[280px] text-[11px]">
                                                            {hint}
                                                        </TooltipContent>
                                                    )}
                                                </Tooltip>
                                            );
                                        })
                                    ) : (
                                        <div className="text-xs text-muted-foreground p-2 border border-dashed border-border">
                                            {locked ? `Locked until explored` : `0 / ${a.total_count || 0} resources discovered`}
                                        </div>
                                    )}
                                    {/* Scavenge fallback removed — tools now required */}
                                    {a.resource_nodes && a.resource_nodes.length === 0 && !locked && (
                                        <div className="text-xs text-muted-foreground p-2 border border-dashed border-border text-center">
                                            Explore this region to discover resources
                                        </div>
                                    )}
                                </div>
                            )}

                            {/* Hunt targets */}
                            {a.id === "hunt" && (
                                <div className="space-y-1">
                                    {a.tool_ok === false && (
                                        <div className="text-xs text-destructive p-2 border border-destructive/40 mb-2">
                                            No Hunter's Kit — buy one in town to hunt
                                        </div>
                                    )}
                                    {a.targets && a.targets.length > 0 ? (
                                        a.targets.map((t) => {
                                            const huntHint = buildHuntHint(a);
                                            return (
                                                <Tooltip key={t.id}>
                                                    <TooltipTrigger asChild>
                                                        <button
                                                            data-testid={`action-${a.id}-${t.id}`}
                                                            disabled={rolling || locked || t.stock <= 0}
                                                            onClick={() => doAction(a.id, t.id)}
                                                            className={`press-btn w-full font-mono text-xs uppercase px-2 py-1.5 border border-border hover:border-primary hover:text-primary text-left disabled:opacity-40 ${a.tool_ok === false ? "opacity-60" : ""}`}
                                                        >
                                                            <div className="flex justify-between items-center">
                                                                <span>› {t.name}</span>
                                                                <span className="text-[10px] uppercase">{RARITY_LABEL[t.rarity] || t.rarity}</span>
                                                            </div>
                                                            <div className="flex justify-between items-center text-[10px] text-muted-foreground mt-0.5">
                                                                <span className="text-[10px] text-muted-foreground" title="Threat scales with your level">THREAT {t.threat}</span>
                                                                <span className={t.stock <= 0 ? "text-destructive" : ""}>{t.stock}/{t.max_stock} in the wild</span>
                                                            </div>
                                                            {t.stock <= 0 && <div className="text-[10px] text-destructive">None left in this area</div>}
                                                        </button>
                                                    </TooltipTrigger>
                                                    {huntHint && (
                                                        <TooltipContent side="top" className="max-w-[280px] text-[11px]">
                                                            {huntHint}
                                                        </TooltipContent>
                                                    )}
                                                </Tooltip>
                                            );
                                        })
                                    ) : (
                                        <div className="text-xs text-muted-foreground p-2 border border-dashed border-border">
                                            {locked ? `Locked until explored` : `0 / ${a.total_count || 0} monsters discovered`}
                                        </div>
                                    )}
                                </div>
                            )}

                            {/* Other non-node actions */}
                            {!isGatherFish && a.id !== "hunt" && (
                                <button
                                    data-testid={`action-${a.id}`}
                                    disabled={rolling || locked}
                                    onClick={() => doAction(a.id, null)}
                                    className="press-btn w-full font-pixel text-lg uppercase py-2 bg-primary/10 border border-primary text-primary hover:bg-primary hover:text-primary-foreground disabled:opacity-40"
                                >
                                    Roll →
                                </button>
                            )}
                        </div>
                    );
                })}
            </div>

            {/* Mercenary expedition camp */}
            <ExpeditionPanel
                character={character}
                biomeId={biome}
                onCharacterUpdate={onCharacterUpdate}
            />
        </div>
        </TooltipProvider>
    );
}
