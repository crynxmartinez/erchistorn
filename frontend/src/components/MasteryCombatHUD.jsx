import { useState } from "react";
import { api, extractError } from "@/lib/api";
import { toast } from "sonner";
import { Music, Swords, Shield, Eye, Crosshair, FlaskConical, Crown, Zap } from "lucide-react";
import { Tooltip, TooltipTrigger, TooltipContent, TooltipProvider } from "@/components/ui/tooltip";
import { useGameData } from "@/data/gameData";

const MASTERY_ICON = {
    rogue: Shield,
    knight: Crown,
    assassin: Eye,
    hunter: Crosshair,
    alchemist: FlaskConical,
    paladin: Shield,
    lancer: Zap,
    bard: Music,
};

const KNIGHT_OATHS = {
    iron: { name: "Oath of Iron", desc: "+1 Armor per stack. Gain on defend.", per_stack: "+1 Armor", ms5: "Immune to Shaken", ms10: "Reflect 10% melee damage" },
    wrath: { name: "Oath of Wrath", desc: "+1 Might per stack. Gain on hit.", per_stack: "+1 Might", ms5: "+20% strike damage", ms10: "Strikes apply Bleeding" },
    bulwark: { name: "Oath of Bulwark", desc: "-1 Might & Grace to enemy per stack. Gain when hit.", per_stack: "-1 Might & Grace (enemy)", ms5: "Enemy can't buff", ms10: "-20% enemy accuracy" },
    endurance: { name: "Oath of Endurance", desc: "+1 Durability per stack. Gain per turn.", per_stack: "+1 Durability", ms5: "Immune to Stunned", ms10: "-15% incoming damage" },
    vanguard: { name: "Oath of Vanguard", desc: "+1 all stats per stack. Strike first.", per_stack: "+1 All Stats (−1 Armor)", ms5: "Armor penalty removed", ms10: "All stats per stack doubled" },
};

const CF_ACTIONS = [
    { id: "analysis", label: "Analysis", cost: 5, desc: "Next strike +20%" },
    { id: "adjustment", label: "Adjustment", cost: 10, desc: "Imbue rule x2" },
    { id: "optimization", label: "Optimization", cost: 15, desc: "CD -1, free re-imbue" },
    { id: "perfect_formula", label: "Perfect Formula", cost: 20, desc: "Next strike empowered" },
];

const ELEMENT_COLORS = {
    fire: "text-orange-400 border-orange-400/50",
    ice: "text-cyan-400 border-cyan-400/50",
    lightning: "text-yellow-400 border-yellow-400/50",
    earth: "text-amber-600 border-amber-600/50",
    wind: "text-green-400 border-green-400/50",
    thunder: "text-purple-400 border-purple-400/50",
};

export default function MasteryCombatHUD({ character, state, combatId, onStateUpdate }) {
    const gd = useGameData();
    const mastery = character?.mastery;
    const masteries = character?.masteries || [];
    const activeMastery = masteries.find((m) => m === mastery) || mastery;
    const [oathPicking, setOathPicking] = useState(false);
    const [modeSwitching, setModeSwitching] = useState(false);

    if (!activeMastery) return null;

    const MASTERY_LABELS = {
        rogue: "ROGUE", knight: "KNIGHT", assassin: "ASSASSIN",
        hunter: "HUNTER", alchemist: "ALCHEMIST", paladin: "PALADIN",
        lancer: "LANCER", bard: "BARD",
    };

    const Ic = MASTERY_ICON[activeMastery] || Swords;

    const handleCfSpend = async (action) => {
        try {
            const { data } = await api.post("/game/combat/alchemist/cf", { combat_id: combatId, action });
            onStateUpdate?.(data.state);
            if (data.log?.length) {
                toast.success(data.log[data.log.length - 1]?.text || `${action} used`);
            }
        } catch (e) {
            toast.error(extractError(e));
        }
    };

    const handleBardModeSwitch = async (mode) => {
        setModeSwitching(true);
        try {
            const { data } = await api.post("/game/bard/mode-switch", { combat_id: combatId, mode });
            onStateUpdate?.(data.state);
            if (data.log?.length) {
                toast.success(data.log[data.log.length - 1]?.text || `Mode switched to ${mode}`);
            }
        } catch (e) {
            toast.error(extractError(e));
        } finally {
            setModeSwitching(false);
        }
    };

    const handleKnightOathSelect = async (oathId) => {
        setOathPicking(false);
        try {
            const { data } = await api.post("/game/knight/oath", { combat_id: combatId, oath: oathId });
            onStateUpdate?.(data.state);
            toast.success(`Oath selected: ${KNIGHT_OATHS[oathId]?.name}`);
        } catch (e) {
            toast.error(extractError(e));
        }
    };

    return (
        <div className="border-t border-border pt-3 space-y-2" data-testid="mastery-hud">
            <div className="flex items-center gap-2">
                <Ic size={14} className="text-primary" />
                <span className="stat-label text-primary">{MASTERY_LABELS[activeMastery] || activeMastery.toUpperCase()}</span>
            </div>

            {/* ===== RANGE (all masteries) ===== */}
            <RangeHUD state={state} />

            {/* ===== ROGUE ===== */}
            {activeMastery === "rogue" && (
                <RogueHUD state={state} character={character} innateSkills={gd.rogueInnateSkills} />
            )}

            {/* ===== KNIGHT ===== */}
            {activeMastery === "knight" && (
                <KnightHUD
                    state={state}
                    oathPicking={oathPicking}
                    setOathPicking={setOathPicking}
                    onOathSelect={handleKnightOathSelect}
                />
            )}

            {/* ===== ASSASSIN ===== */}
            {activeMastery === "assassin" && (
                <AssassinHUD state={state} />
            )}

            {/* ===== HUNTER ===== */}
            {activeMastery === "hunter" && (
                <HunterHUD state={state} />
            )}

            {/* ===== ALCHEMIST ===== */}
            {activeMastery === "alchemist" && (
                <AlchemistHUD state={state} onCfSpend={handleCfSpend} />
            )}

            {/* ===== PALADIN ===== */}
            {activeMastery === "paladin" && (
                <PaladinHUD state={state} />
            )}

            {/* ===== LANCER ===== */}
            {activeMastery === "lancer" && (
                <LancerHUD state={state} />
            )}

            {/* ===== BARD ===== */}
            {activeMastery === "bard" && (
                <BardHUD
                    state={state}
                    onModeSwitch={handleBardModeSwitch}
                    switching={modeSwitching}
                />
            )}
        </div>
    );
}

// ============ ROGUE ============
function RogueHUD({ state, character, innateSkills = [] }) {
    const luckyStacks = state.rogue_lucky_dodger_stacks || 0;
    const quickHands = state.rogue_quick_hands;
    const trapCharges = state.rogue_trap_master_charges || 0;
    const equipped = character?.rogue_innate_equipped || [];
    const innateById = Object.fromEntries((innateSkills || []).map((s) => [s.id, s]));

    return (
        <TooltipProvider delayDuration={120}>
        <div className="space-y-1.5" data-testid="rogue-hud">
            {/* Innate skills equipped */}
            <div className="flex flex-wrap gap-1">
                <span className="stat-label text-muted-foreground text-[10px]">INNATE:</span>
                {equipped.filter(Boolean).map((id, i) => {
                    const skill = innateById[id];
                    return (
                        <Tooltip key={i}>
                            <TooltipTrigger asChild>
                                <span className="stat-label text-[10px] px-1 border border-primary/40 text-primary cursor-help">
                                    {id.replace(/_/g, " ").slice(0, 12)}
                                </span>
                            </TooltipTrigger>
                            {skill && (
                                <TooltipContent side="bottom" sideOffset={4} className="max-w-[220px] bg-popover border border-border text-popover-foreground">
                                    <div className="font-pixel text-xs uppercase text-primary mb-1">{skill.name}</div>
                                    <div className="text-[10px] text-muted-foreground mb-1">{skill.type}</div>
                                    <div className="text-[10px] text-popover-foreground/80 italic">{skill.desc}</div>
                                </TooltipContent>
                            )}
                        </Tooltip>
                    );
                })}
                {equipped.filter(Boolean).length === 0 && (
                    <span className="stat-label text-[10px] text-muted-foreground/50">none equipped</span>
                )}
            </div>
            {/* Lucky Dodger */}
            {luckyStacks > 0 && (
                <div className="flex items-center gap-2">
                    <span className="font-pixel text-xs text-green-400" data-testid="rogue-lucky">
                        LUCKY DODGER +{luckyStacks}%
                    </span>
                </div>
            )}
            {/* Quick Hands */}
            {quickHands && (
                <span className="font-pixel text-[10px] text-primary border border-primary/40 px-1.5 py-0.5">
                    QUICK HANDS — act first
                </span>
            )}
            {/* Trap Master charges */}
            {trapCharges > 0 && (
                <span className="font-pixel text-[10px] text-amber-400 border border-amber-400/40 px-1.5 py-0.5">
                    TRAP MASTER ×{trapCharges}
                </span>
            )}
        </div>
        </TooltipProvider>
    );
}

// ============ KNIGHT ============
function KnightHUD({ state, oathPicking, setOathPicking, onOathSelect }) {
    const oath = state.knight_oath;
    const stacks = state.knight_oath_stacks || 0;
    const oathMastery = state.knight_oath_mastery;
    const eternalOath = state.knight_eternal_oath;

    return (
        <TooltipProvider delayDuration={120}>
        <div className="space-y-1.5" data-testid="knight-hud">
            {/* Oath selection */}
            {!oath && !oathPicking && (
                <button
                    onClick={() => setOathPicking(true)}
                    className="press-btn stat-label px-2 py-1 border border-primary text-primary text-xs"
                    data-testid="knight-oath-select"
                >
                    SELECT OATH
                </button>
            )}
            {oathPicking && (
                <div className="space-y-1 p-2 border border-primary/30 bg-primary/5">
                    {Object.entries(KNIGHT_OATHS).map(([id, info]) => (
                        <button
                            key={id}
                            onClick={() => onOathSelect(id)}
                            className="block w-full text-left text-xs p-1 hover:bg-primary/10 border border-border"
                            data-testid={`knight-oath-${id}`}
                        >
                            <span className="font-pixel text-primary">{info.name}</span>
                            <span className="stat-label text-muted-foreground ml-2">{info.desc}</span>
                        </button>
                    ))}
                </div>
            )}
            {/* Oath stacks */}
            {oath && (
                <div className="flex items-center gap-2 flex-wrap">
                    <Tooltip>
                        <TooltipTrigger asChild>
                            <div className="flex items-center gap-1.5 cursor-help" data-testid="knight-oath-name">
                                <span className="font-pixel text-xs text-primary">
                                    {KNIGHT_OATHS[oath]?.name || oath}
                                </span>
                                <div className="flex items-center gap-1">
                                    <span className="stat-label text-[10px] text-muted-foreground">STACKS:</span>
                                    <div className="flex gap-0.5">
                                        {Array.from({ length: 10 }).map((_, i) => (
                                            <div
                                                key={i}
                                                className={`w-2 h-3 ${i < stacks ? "bg-primary" : "bg-border"}`}
                                            />
                                        ))}
                                    </div>
                                    <span className="font-pixel text-xs text-primary">{stacks}</span>
                                </div>
                            </div>
                        </TooltipTrigger>
                        <TooltipContent side="bottom" className="max-w-[300px] bg-popover text-popover-foreground border border-border px-3 py-2">
                            <p className="font-pixel text-xs mb-1.5 text-primary">{KNIGHT_OATHS[oath]?.name || oath}</p>
                            <p className="narr text-xs mb-2 text-popover-foreground/80">{KNIGHT_OATHS[oath]?.desc}</p>
                            <div className="space-y-1 text-xs">
                                <div className="flex justify-between gap-3"><span className="text-muted-foreground">Per stack</span><span className="text-primary">{KNIGHT_OATHS[oath]?.per_stack}</span></div>
                                <div className="flex justify-between gap-3"><span className="text-muted-foreground">5 stacks</span><span className={`text-amber-400 ${stacks >= 5 ? "" : "opacity-40"}`}>{KNIGHT_OATHS[oath]?.ms5}</span></div>
                                <div className="flex justify-between gap-3"><span className="text-muted-foreground">10 stacks</span><span className={`text-orange-400 ${stacks >= 10 ? "" : "opacity-40"}`}>{KNIGHT_OATHS[oath]?.ms10}</span></div>
                                {oathMastery && <div className="flex justify-between gap-3"><span className="text-muted-foreground">Lv 60</span><span className="text-purple-400">Mastery x2 (5+ stacks)</span></div>}
                                {eternalOath && <div className="flex justify-between gap-3"><span className="text-muted-foreground">Lv 100</span><span className="text-pink-400">Eternal x3</span></div>}
                            </div>
                        </TooltipContent>
                    </Tooltip>
                    {stacks >= 5 && (
                        <span className="font-pixel text-[10px] text-amber-400 border border-amber-400/40 px-1">
                            MILESTONE
                        </span>
                    )}
                    {stacks >= 10 && (
                        <span className="font-pixel text-[10px] text-orange-400 border border-orange-400/40 px-1">
                            ULTIMATE
                        </span>
                    )}
                    {oathMastery && (
                        <span className="font-pixel text-[10px] text-purple-400 border border-purple-400/40 px-1">
                            MASTERY x2
                        </span>
                    )}
                    {eternalOath && (
                        <span className="font-pixel text-[10px] text-pink-400 border border-pink-400/40 px-1">
                            ETERNAL x3
                        </span>
                    )}
                    {!oathPicking && (
                        <button
                            onClick={() => setOathPicking(true)}
                            className="stat-label text-[10px] text-muted-foreground hover:text-primary border border-border hover:border-primary/40 px-1.5 py-0.5"
                            data-testid="knight-oath-change"
                        >
                            CHANGE
                        </button>
                    )}
                    {/* Stat bonuses */}
                    {(() => {
                        const bonuses = state.knight_current_oath_bonuses || {};
                        const statLabels = { might: "MIG", grace: "GRA", armor_bonus: "ARM", durability: "DUR", all_stats: "ALL", enemy_might: "eMIG", enemy_grace: "eGRA" };
                        const hasAny = Object.keys(bonuses).some(k => (bonuses[k] || 0) !== 0);
                        if (!hasAny) return null;
                        return (
                            <div className="flex items-center gap-1 flex-wrap">
                                {Object.entries(bonuses).map(([k, val]) => {
                                    if (!val) return null;
                                    const isEnemy = k.startsWith("enemy_");
                                    return (
                                        <span key={k} className={`stat-label text-[10px] px-1 border ${isEnemy ? "text-red-400 border-red-400/30" : "text-primary border-primary/30"}`}>
                                            {statLabels[k] || k.slice(0, 3).toUpperCase()} {val > 0 ? "+" : ""}{val}
                                        </span>
                                    );
                                })}
                            </div>
                        );
                    })()}
                </div>
            )}
            {oathPicking && oath && (
                <div className="space-y-1 p-2 border border-primary/30 bg-primary/5">
                    {Object.entries(KNIGHT_OATHS).map(([id, info]) => (
                        <button
                            key={id}
                            onClick={() => onOathSelect(id)}
                            className="block w-full text-left text-xs p-1 hover:bg-primary/10 border border-border"
                            data-testid={`knight-oath-${id}`}
                        >
                            <span className="font-pixel text-primary">{info.name}</span>
                            <span className="stat-label text-muted-foreground ml-2">{info.desc}</span>
                        </button>
                    ))}
                </div>
            )}
        </div>
        </TooltipProvider>
    );
}

// ============ ASSASSIN ============
function AssassinHUD({ state }) {
    const shadows = state.assassin_shadows || 0;
    const burstReady = state.assassin_burst_ready;
    const deposited = state.assassin_deposited_shadows || 0;
    const shadowLinger = state.assassin_shadow_linger || 0;
    const eclipseBlade = state.assassin_eclipse_blade_active;

    return (
        <div className="space-y-1.5" data-testid="assassin-hud">
            <div className="flex items-center gap-3 flex-wrap">
                {/* Shadow counter */}
                <div className="flex items-center gap-1.5">
                    <span className="stat-label text-[10px] text-muted-foreground">SHADOWS:</span>
                    <div className="flex items-center gap-1">
                        <div className="w-24 h-3 bg-background border border-border relative overflow-hidden">
                            <div
                                className="h-full bg-purple-500 transition-all duration-300"
                                style={{ width: `${Math.min(100, shadows)}%` }}
                            />
                        </div>
                        <span className="font-pixel text-xs text-purple-400" data-testid="assassin-shadows">{shadows}</span>
                    </div>
                </div>
                {/* Burst ready */}
                {burstReady && (
                    <span className="font-pixel text-xs text-pink-400 animate-pulse border border-pink-400/50 px-1.5 py-0.5" data-testid="assassin-burst">
                        BURST READY
                    </span>
                )}
                {/* Fear deposited */}
                {deposited > 0 && (
                    <span className="stat-label text-[10px] text-red-400">
                        FEAR: -{deposited} stats
                    </span>
                )}
                {/* Shadow linger */}
                {shadowLinger > 0 && (
                    <span className="font-pixel text-[10px] text-purple-300 border border-purple-300/40 px-1">
                        LINGER {shadowLinger}T
                    </span>
                )}
                {/* Eclipse Blade */}
                {eclipseBlade && (
                    <span className="font-pixel text-[10px] text-amber-400 border border-amber-400/40 px-1">
                        ECLIPSE BLADE
                    </span>
                )}
            </div>
        </div>
    );
}

// ============ RANGE (all masteries) ============
function RangeHUD({ state }) {
    const rangeGap = state.range_gap ?? 0;
    const playerRange = state.player_range ?? 0;
    const monsterRange = state.monster_range ?? 0;

    if (rangeGap === 0 && playerRange === 0 && monsterRange === 0) return null;

    return (
        <div className="flex items-center gap-2 flex-wrap" data-testid="range-hud">
            <span className="stat-label text-[10px] text-muted-foreground">RANGE:</span>
            {rangeGap > 0 ? (
                <span className="font-pixel text-xs text-green-400" data-testid="range-advantage">
                    {rangeGap} {rangeGap === 1 ? "TURN" : "TURNS"} — enemy can't reach
                </span>
            ) : rangeGap < 0 ? (
                <span className="font-pixel text-xs text-red-400" data-testid="range-disadvantage">
                    {-rangeGap} {-rangeGap === 1 ? "TURN" : "TURNS"} — can't reach enemy
                </span>
            ) : (
                <span className="font-pixel text-xs text-yellow-400" data-testid="range-mutual">
                    MUTUAL
                </span>
            )}
            {monsterRange > 0 && (
                <span className="stat-label text-[10px] text-amber-400/70">
                    (enemy range: {monsterRange})
                </span>
            )}
        </div>
    );
}

// ============ HUNTER ============
function HunterHUD({ state }) {
    const spiritGuidance = state.hunter_spirit_guidance || 0;
    const spiritCommunion = state.hunter_spirit_communion;
    const guaranteedCrits = state.hunter_guaranteed_crits || 0;
    const ambushUsed = state.hunter_ambush_used;
    const worldHunt = state.hunter_world_hunt_active;
    const spiritBow = state.hunter_spirit_bow_charges || 0;
    const spiritCopy = state.hunter_spirit_copy_active;

    return (
        <TooltipProvider delayDuration={120}>
        <div className="space-y-1.5" data-testid="hunter-hud">
            {/* Spirit Guidance */}
            <div className="flex items-center gap-1.5">
                <Tooltip>
                    <TooltipTrigger asChild>
                        <span className="stat-label text-[10px] text-muted-foreground cursor-help">GUIDANCE:</span>
                    </TooltipTrigger>
                    <TooltipContent side="bottom" className="max-w-[300px] bg-popover text-popover-foreground border border-border px-3 py-2">
                        <p className="font-pixel text-xs mb-1.5 text-green-400">Spirit Guidance</p>
                        <p className="narr text-xs mb-2 text-popover-foreground/80">Gained per hit on the enemy. Each stack increases crit chance. At {spiritCommunion ? "communion" : "10 stacks"}, Spirit Communion triggers — ancestors join the fight, empowering skills with unique effects.</p>
                        <div className="space-y-1 text-xs">
                            <div className="flex justify-between gap-3"><span className="text-muted-foreground">Crit / stack</span><span className="text-green-400">+2%</span></div>
                            <div className="flex justify-between gap-3"><span className="text-muted-foreground">Communion at</span><span className="text-green-400">10 stacks</span></div>
                            <div className="flex justify-between gap-3"><span className="text-muted-foreground">Lv 70</span><span className="text-green-400">8 stacks</span></div>
                            <div className="flex justify-between gap-3"><span className="text-muted-foreground">Lv 100</span><span className="text-green-400">6 stacks</span></div>
                        </div>
                        <p className="narr text-[10px] mt-2 pt-1.5 border-t border-border opacity-60">Multi-hit skills grant guidance per hit. Basic attacks grant 1 stack.</p>
                    </TooltipContent>
                </Tooltip>
                <Tooltip>
                    <TooltipTrigger asChild>
                        <div className="flex items-center gap-1 cursor-help">
                            <div className="flex gap-0.5">
                                {Array.from({ length: 10 }).map((_, i) => (
                                    <div
                                        key={i}
                                        className={`w-2 h-3 ${i < spiritGuidance ? "bg-green-500" : "bg-border"}`}
                                    />
                                ))}
                            </div>
                            <span className="font-pixel text-xs text-green-400">{spiritGuidance}</span>
                        </div>
                    </TooltipTrigger>
                    <TooltipContent side="bottom" className="max-w-[280px] bg-popover text-popover-foreground border border-border px-3 py-2">
                        <p className="font-pixel text-xs mb-1.5 text-green-400">Spirit Guidance — Current</p>
                        <div className="space-y-1 text-xs">
                            <div className="flex justify-between gap-3"><span className="text-muted-foreground">Stacks</span><span className="text-green-400">{spiritGuidance}</span></div>
                            <div className="flex justify-between gap-3"><span className="text-muted-foreground">Crit chance</span><span className="text-green-400">{spiritCommunion ? "100%" : `${Math.round(spiritGuidance * (0.07) * 100)}%`}</span></div>
                            <div className="flex justify-between gap-3"><span className="text-muted-foreground">Per stack</span><span className="text-green-400">{spiritCommunion ? "+12%" : "+7%"}</span></div>
                            {spiritCommunion ? (
                                <div className="flex justify-between gap-3"><span className="text-muted-foreground">Status</span><span className="text-emerald-400">Communion active</span></div>
                            ) : (
                                <div className="flex justify-between gap-3"><span className="text-muted-foreground">Communion at</span><span className="text-green-400">10 stacks</span></div>
                            )}
                        </div>
                    </TooltipContent>
                </Tooltip>
                {/* Crit chance bonus */}
                {spiritGuidance > 0 && (() => {
                    const perStack = spiritCommunion ? 0.12 : 0.07;
                    const critPct = spiritCommunion ? 100 : Math.round(spiritGuidance * perStack * 100);
                    return (
                        <span className="stat-label text-[10px] text-green-400 border border-green-400/30 px-1">
                            CRIT +{critPct}%
                        </span>
                    );
                })()}
            </div>
            <div className="flex items-center gap-3 flex-wrap">
                {/* Spirit Communion */}
                {spiritCommunion && (
                    <span className="font-pixel text-xs text-emerald-400 animate-pulse border border-emerald-400/50 px-1.5 py-0.5">
                        COMMUNION
                    </span>
                )}
                {/* Guaranteed crits */}
                {guaranteedCrits > 0 && (
                    <span className="font-pixel text-[10px] text-amber-400 border border-amber-400/40 px-1">
                        CRIT ×{guaranteedCrits}
                    </span>
                )}
                {/* Ambush */}
                {ambushUsed && (
                    <span className="font-pixel text-[10px] text-primary border border-primary/40 px-1">
                        AMBUSH
                    </span>
                )}
                {/* World Hunt */}
                {worldHunt && (
                    <span className="font-pixel text-[10px] text-orange-400 border border-orange-400/40 px-1 animate-pulse">
                        WORLD HUNT
                    </span>
                )}
                {/* Spirit Bow */}
                {spiritBow > 0 && (
                    <span className="font-pixel text-[10px] text-cyan-400 border border-cyan-400/40 px-1">
                        TRUE ×{spiritBow}
                    </span>
                )}
                {/* Spirit Copy */}
                {spiritCopy && (
                    <span className="font-pixel text-[10px] text-blue-400 border border-blue-400/40 px-1">
                        DECOY
                    </span>
                )}
            </div>
        </div>
        </TooltipProvider>
    );
}

// ============ ALCHEMIST ============
function AlchemistHUD({ state, onCfSpend }) {
    const cf = state.alchemist_cf || 0;
    const cfMax = state.alchemist_cf_max || 20;
    const imbue = state.alchemist_imbue;
    const imbueCharges = state.alchemist_imbue_charges || 0;
    const infiniteCharges = state.alchemist_infinite_charges || 0;
    const perfectFormula = state.alchemist_perfect_formula;
    const analysisBonus = state.alchemist_analysis_bonus;
    const enemyLaunched = state.alchemist_enemy_launched;
    const enemyImmobilized = state.alchemist_enemy_immobilized || 0;

    return (
        <div className="space-y-1.5" data-testid="alchemist-hud">
            <div className="flex items-center gap-3 flex-wrap">
                {/* Combo Flow meter */}
                <div className="flex items-center gap-1.5">
                    <span className="stat-label text-[10px] text-muted-foreground">CF:</span>
                    <div className="w-32 h-3 bg-background border border-border relative overflow-hidden">
                        <div
                            className="h-full transition-all duration-300"
                            style={{
                                width: `${(cf / cfMax) * 100}%`,
                                background: cf >= 20 ? "hsl(280, 80%, 50%)" : cf >= 15 ? "hsl(260, 70%, 50%)" : cf >= 10 ? "hsl(240, 60%, 50%)" : cf >= 5 ? "hsl(200, 60%, 50%)" : "hsl(180, 40%, 40%)",
                            }}
                        />
                    </div>
                    <span className="font-pixel text-xs text-primary" data-testid="alchemist-cf">{cf}/{cfMax}</span>
                </div>
                {/* CF Actions */}
                <div className="flex gap-1">
                    {CF_ACTIONS.map((act) => (
                        <button
                            key={act.id}
                            disabled={cf < act.cost}
                            onClick={() => onCfSpend(act.id)}
                            title={act.desc}
                            className={`stat-label text-[10px] px-1.5 py-0.5 border transition-colors ${
                                cf >= act.cost
                                    ? "border-primary text-primary hover:bg-primary/10 cursor-pointer"
                                    : "border-border text-muted-foreground/40 cursor-not-allowed"
                            }`}
                            data-testid={`cf-${act.id}`}
                        >
                            {act.label} ({act.cost})
                        </button>
                    ))}
                </div>
            </div>
            {/* Active imbue */}
            {imbue && (
                <div className="flex items-center gap-2">
                    <span className="stat-label text-[10px] text-muted-foreground">IMBUE:</span>
                    <span className="font-pixel text-[10px] text-primary border border-primary/40 px-1">
                        {imbue.name || imbue.id}
                    </span>
                    {infiniteCharges > 0 ? (
                        <span className="font-pixel text-[10px] text-purple-400">∞ ({infiniteCharges}T)</span>
                    ) : (
                        <span className="stat-label text-[10px] text-muted-foreground">CHARGES: {imbueCharges}</span>
                    )}
                </div>
            )}
            {/* Status flags */}
            <div className="flex items-center gap-2 flex-wrap">
                {perfectFormula && (
                    <span className="font-pixel text-[10px] text-purple-400 border border-purple-400/40 px-1 animate-pulse">
                        PERFECT FORMULA
                    </span>
                )}
                {analysisBonus && (
                    <span className="font-pixel text-[10px] text-cyan-400 border border-cyan-400/40 px-1">
                        ANALYSIS +{(analysisBonus - 1) * 100}%
                    </span>
                )}
                {enemyLaunched && (
                    <span className="font-pixel text-[10px] text-orange-400 border border-orange-400/40 px-1">
                        ENEMY AIRBORNE
                    </span>
                )}
                {enemyImmobilized > 0 && (
                    <span className="font-pixel text-[10px] text-amber-400 border border-amber-400/40 px-1">
                        IMMOBILIZED {enemyImmobilized}T
                    </span>
                )}
            </div>
        </div>
    );
}

// ============ PALADIN ============
function PaladinHUD({ state }) {
    const tier = state.paladin_hp_tier || 0;
    const avatarOfFaith = state.paladin_avatar_of_faith;
    const resurrectionUsed = state.paladin_resurrection_used;

    const TIER_NAMES = [
        "Unbroken", "Faith Stirring", "Faith Rising",
        "Faith Burning", "Faith Blazing", "Faith Unleashed", "Faith Ascendant",
    ];
    const TIER_COLORS = [
        "text-green-400", "text-lime-400", "text-yellow-400",
        "text-orange-400", "text-red-400", "text-red-500", "text-fuchsia-400",
    ];
    const TIER_DESCS = [
        "HP > 90%. No bonuses.",
        "HP ≤ 90%. +10% main stats, +5% healing.",
        "HP ≤ 70%. +15% main stats, +10% healing.",
        "HP ≤ 50%. +25% main stats, +20% healing.",
        "HP ≤ 25%. +35% main stats, +30% healing.",
        "HP ≤ 10%. +40% main stats, +40% healing.",
        "HP ≤ 5%. +50% main stats, +50% healing.",
    ];

    return (
        <div className="space-y-1.5" data-testid="paladin-hud">
            <div className="flex items-center gap-3 flex-wrap">
                {/* Faith tier */}
                <div className="flex items-center gap-1.5">
                    <span className="stat-label text-[10px] text-muted-foreground">FAITH:</span>
                    <Tooltip>
                        <TooltipTrigger asChild>
                            <div className="flex items-center gap-1.5 cursor-help">
                                <div className="flex gap-0.5">
                                    {[1, 2, 3, 4, 5, 6].map((i) => (
                                        <div
                                            key={i}
                                            className={`w-2.5 h-3 ${i <= tier ? "bg-primary" : "bg-border"}`}
                                        />
                                    ))}
                                </div>
                                <span className={`font-pixel text-xs ${TIER_COLORS[tier]}`} data-testid="paladin-tier">
                                    {TIER_NAMES[tier]}
                                </span>
                            </div>
                        </TooltipTrigger>
                        <TooltipContent side="bottom" className="max-w-[340px] overflow-visible bg-popover text-popover-foreground border border-border px-3 py-2">
                            <p className="font-pixel text-xs mb-1.5">Faith Scaling</p>
                            <p className="narr text-xs mb-2 text-popover-foreground/80">The Paladin grows stronger as HP falls. All main stats scale up automatically — no level requirement.</p>
                            <div className="space-y-1 text-xs">
                                {TIER_NAMES.map((name, i) => (
                                    <div key={i} className={`flex items-center gap-1.5 ${i === tier ? "font-bold" : "opacity-70"}`}>
                                        <span className={TIER_COLORS[i]}>{name}</span>
                                        <span>— {TIER_DESCS[i]}</span>
                                    </div>
                                ))}
                            </div>
                            <p className="narr text-[10px] mt-2 pt-1.5 border-t border-border opacity-60">Passives add extra flat armor on top at higher tiers.</p>
                        </TooltipContent>
                    </Tooltip>
                </div>
                {/* Stat bonuses */}
                {(() => {
                    const bonuses = state.paladin_faith_bonuses || {};
                    const healAmp = bonuses.heal_amp || 1.0;
                    const statKeys = ["might", "insight", "grace", "vitality", "essence", "armor_bonus"];
                    const hasAnyBonus = statKeys.some(k => (bonuses[k] || 0) > 0) || healAmp > 1.0;
                    if (!hasAnyBonus) return null;
                    return (
                        <div className="flex items-center gap-1.5 flex-wrap">
                            {statKeys.map((k) => {
                                const val = bonuses[k] || 0;
                                if (val <= 0) return null;
                                return (
                                    <span key={k} className="stat-label text-[10px] text-primary border border-primary/30 px-1">
                                        {k.slice(0, 3).toUpperCase()} +{val}
                                    </span>
                                );
                            })}
                            {healAmp > 1.0 && (
                                <span className="stat-label text-[10px] text-green-400 border border-green-400/30 px-1">
                                    HEAL +{Math.round((healAmp - 1) * 100)}%
                                </span>
                            )}
                        </div>
                    );
                })()}
                {/* Passives */}
                {avatarOfFaith && (
                    <span className="font-pixel text-[10px] text-amber-400 border border-amber-400/40 px-1 animate-pulse">
                        AVATAR OF FAITH
                    </span>
                )}
                {resurrectionUsed && (
                    <span className="font-pixel text-[10px] text-red-400 border border-red-400/40 px-1">
                        RESURRECTION USED
                    </span>
                )}
            </div>
        </div>
    );
}

// ============ LANCER ============
function LancerHUD({ state }) {
    const imbues = state.lancer_active_imbues || {};
    const overloadTurns = state.lancer_overload_turns || 0;
    const elementCount = Object.keys(imbues).length;

    return (
        <div className="space-y-1.5" data-testid="lancer-hud">
            <div className="flex items-center gap-3 flex-wrap">
                {/* Active imbues */}
                <div className="flex items-center gap-1.5">
                    <span className="stat-label text-[10px] text-muted-foreground">IMBUES ({elementCount}):</span>
                    <div className="flex gap-1">
                        {Object.entries(imbues).map(([elem, data]) => (
                            <span
                                key={elem}
                                className={`stat-label text-[10px] px-1 border ${ELEMENT_COLORS[elem] || "border-border text-foreground"}`}
                                title={`${elem} — ${data.duration || 0}T`}
                            >
                                {elem.toUpperCase().slice(0, 3)} {data.duration || 0}T
                            </span>
                        ))}
                        {elementCount === 0 && (
                            <span className="stat-label text-[10px] text-muted-foreground/50">none</span>
                        )}
                    </div>
                </div>
                {/* Overload */}
                {overloadTurns > 0 && (
                    <span className="font-pixel text-xs text-purple-400 animate-pulse border border-purple-400/50 px-1.5 py-0.5" data-testid="lancer-overload">
                        OVERLOAD {overloadTurns}T
                    </span>
                )}
                {/* Element synergy indicators */}
                {elementCount >= 3 && (
                    <span className="font-pixel text-[10px] text-amber-400 border border-amber-400/40 px-1">
                        3+ SYNERGY
                    </span>
                )}
                {elementCount >= 5 && (
                    <span className="font-pixel text-[10px] text-orange-400 border border-orange-400/40 px-1">
                        5+ SYNERGY
                    </span>
                )}
            </div>
        </div>
    );
}

// ============ BARD ============
function BardHUD({ state, onModeSwitch, switching }) {
    const mode = state.bard_mode || "song";
    const crescendo = state.bard_crescendo || 0;
    const crescendoMax = 10;
    const activePerformances = state.bard_active_performances || [];
    const encoreTurns = state.bard_encore_turns || 0;
    const encorePerf = state.bard_encore_performance;
    const voiceOfWorld = state.bard_voice_of_world;
    const charismatic = state.bard_charismatic;
    const unbreakableVoice = state.bard_unbreakable_voice;
    const legendOfStage = state.bard_legend_of_stage;

    return (
        <div className="space-y-1.5" data-testid="bard-hud">
            <div className="flex items-center gap-3 flex-wrap">
                {/* Mode switch */}
                <div className="flex items-center gap-1">
                    <button
                        onClick={() => onModeSwitch("song")}
                        disabled={switching || mode === "song"}
                        className={`stat-label text-[10px] px-2 py-0.5 border transition-colors ${
                            mode === "song"
                                ? "border-primary text-primary bg-primary/10"
                                : "border-border text-muted-foreground hover:border-primary/50"
                        }`}
                        data-testid="bard-mode-song"
                    >
                        SONG
                    </button>
                    <button
                        onClick={() => onModeSwitch("dance")}
                        disabled={switching || mode === "dance"}
                        className={`stat-label text-[10px] px-2 py-0.5 border transition-colors ${
                            mode === "dance"
                                ? "border-primary text-primary bg-primary/10"
                                : "border-border text-muted-foreground hover:border-primary/50"
                        }`}
                        data-testid="bard-mode-dance"
                    >
                        DANCE
                    </button>
                </div>
                {/* Crescendo meter */}
                <div className="flex items-center gap-1.5">
                    <span className="stat-label text-[10px] text-muted-foreground">CRESCENDO:</span>
                    <div className="flex gap-0.5">
                        {Array.from({ length: crescendoMax }).map((_, i) => (
                            <div
                                key={i}
                                className={`w-2 h-3 ${i < crescendo ? "bg-primary" : "bg-border"}`}
                            />
                        ))}
                    </div>
                    <span className="font-pixel text-xs text-primary" data-testid="bard-crescendo">{crescendo}</span>
                </div>
                {/* Encore */}
                {encoreTurns > 0 && (
                    <span className="font-pixel text-[10px] text-amber-400 border border-amber-400/40 px-1 animate-pulse" data-testid="bard-encore">
                        ENCORE {encoreTurns}T
                    </span>
                )}
            </div>
            {/* Active performances */}
            {activePerformances.length > 0 && (
                <div className="flex items-center gap-1.5 flex-wrap">
                    <span className="stat-label text-[10px] text-muted-foreground">PERFORMING:</span>
                    {activePerformances.map((p, i) => (
                        <span key={i} className="stat-label text-[10px] text-primary border border-primary/30 px-1">
                            {typeof p === "string" ? p.replace(/_/g, " ").slice(0, 15) : p?.name || p?.id?.replace(/_/g, " ").slice(0, 15)}
                        </span>
                    ))}
                </div>
            )}
            {/* Passives */}
            <div className="flex items-center gap-1.5 flex-wrap">
                {voiceOfWorld && (
                    <span className="font-pixel text-[10px] text-purple-400 border border-purple-400/40 px-1">
                        VOICE OF THE WORLD
                    </span>
                )}
                {charismatic && (
                    <span className="font-pixel text-[10px] text-green-400 border border-green-400/40 px-1">
                        CHARISMATIC +10
                    </span>
                )}
                {unbreakableVoice && (
                    <span className="font-pixel text-[10px] text-blue-400 border border-blue-400/40 px-1">
                        UNBREAKABLE VOICE
                    </span>
                )}
                {legendOfStage && (
                    <span className="font-pixel text-[10px] text-amber-400 border border-amber-400/40 px-1 animate-pulse">
                        LEGEND OF THE STAGE
                    </span>
                )}
            </div>
        </div>
    );
}
