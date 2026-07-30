import { useEffect, useRef, useState } from "react";
import { ArrowLeft, Scissors } from "lucide-react";
import { api, extractError } from "@/lib/api";
import { toast } from "sonner";
import Dice from "@/components/Dice";
import PixelSprite from "@/components/PixelSprite";
import ItemTooltip from "@/components/ItemTooltip";
import { Tooltip, TooltipTrigger, TooltipContent, TooltipProvider } from "@/components/ui/tooltip";
import { RARITY_CLASS } from "@/data/gameData";
import StatusTooltipContent from "@/components/StatusTooltipContent";
import MasteryCombatHUD from "@/components/MasteryCombatHUD";

const RARITY_BORDER = {
    common: "border-border text-foreground",
    uncommon: "border-rarity-uncommon text-rarity-uncommon",
    rare: "border-rarity-rare text-rarity-rare",
    epic: "border-rarity-epic text-rarity-epic",
    legendary: "border-rarity-legendary text-rarity-legendary",
    mythic: "border-rarity-mythic text-rarity-mythic",
};

const RARITY_BG = {
    common: "1c1a17",
    uncommon: "1a2a1a",
    rare: "1a1a2a",
    epic: "2a1a1a",
    legendary: "2a1a2a",
    mythic: "2a0a1a",
};

function monsterPortraitUrl(name, rarity) {
    const bg = RARITY_BG[rarity] || RARITY_BG.common;
    return `https://api.dicebear.com/7.x/pixel-art/svg?seed=${encodeURIComponent(name)}&backgroundColor=${bg}&clothingColor=8b0000,d4af37,4b0082,3a332a`;
}

function DamageNumber({ value, type, isCrit, onDone }) {
    useEffect(() => {
        const t = setTimeout(onDone, 1500);
        return () => clearTimeout(t);
    }, [onDone]);
    const color = type === "heal" ? "text-primary" : isCrit ? "text-amber-400" : "text-destructive";
    const size = isCrit ? "text-4xl" : "text-2xl";
    return (
        <div
            className={`absolute left-1/2 -translate-x-1/2 font-pixel ${size} ${color} pointer-events-none z-20`}
            style={{
                animation: "dmgFloat 1.5s ease-out forwards",
                textShadow: "0 0 6px rgba(0,0,0,0.8), 2px 2px 0 rgba(0,0,0,0.6)",
            }}
        >
            {type === "heal" ? "+" : "-"}{value}
            {isCrit && <span className="block text-xs text-center">CRIT!</span>}
        </div>
    );
}

function HpBar({ pct, color, shieldPct, flash }) {
    return (
        <div className={`h-4 bg-background border border-border relative overflow-hidden`}>
            <div
                className={`h-full ${color} transition-all duration-500 ease-out ${flash ? "animate-pulse brightness-150" : ""}`}
                style={{ width: `${pct}%` }}
            />
            {shieldPct > 0 && (
                <div
                    className="absolute top-0 h-full bg-cyan-400/60 transition-all duration-500"
                    style={{ width: `${shieldPct}%` }}
                />
            )}
        </div>
    );
}

export default function CombatScreen({ combatStart, character, itemsById, skillsById, onEnd, onCharacterUpdate, pendingSkillId, setPendingSkillId, pendingItemId, setPendingItemId }) {
    const [state, setState] = useState(combatStart.state);
    const [ch, setCh] = useState(character);
    const itemInstances = ch.item_instances || [];
    const resolveItem = (id) => {
        if (!id) return null;
        const inst = itemInstances.find((i) => i.instance_id === id);
        if (inst) return inst;
        return itemsById?.[id] || null;
    };
    const [rolling, setRolling] = useState(false);
    const [lastOutcome, setLastOutcome] = useState(null);
    const [victory, setVictory] = useState(null);
    const [rewards, setRewards] = useState(null);
    const [sanctuaryTeleport, setSanctuaryTeleport] = useState(null);
    const [skinResult, setSkinResult] = useState(null);
    const [skinning, setSkinning] = useState(false);
    const [monsterDmg, setMonsterDmg] = useState([]);
    const [playerDmg, setPlayerDmg] = useState([]);
    const [monsterFlash, setMonsterFlash] = useState(false);
    const [playerFlash, setPlayerFlash] = useState(false);
    const [actionType, setActionType] = useState("strike");
    const [telegraph, setTelegraph] = useState(null);
    const prevMonsterHp = useRef(state.monster_hp);
    const prevPlayerHp = useRef(ch.hp);

    const fetchTelegraph = async (combatId) => {
        try {
            const { data } = await api.post("/game/combat/telegraph", { combat_id: combatId });
            setTelegraph(data.telegraph);
        } catch {
            setTelegraph(null);
        }
    };

    useEffect(() => {
        setState(combatStart.state);
        setCh(character);
        setActionType("strike");
        if (combatStart.state?.combat_id) {
            fetchTelegraph(combatStart.state.combat_id);
        }
    }, [combatStart]);

    useEffect(() => {
        setCh(character);
    }, [character]);

    const takeTurn = async () => {
        setRolling(true);
        setLastOutcome(null);
        try {
            const { data } = await api.post("/game/combat/turn", {
                combat_id: state.combat_id,
                manual_skill_id: pendingSkillId,
                manual_item_id: pendingItemId,
                action_type: actionType,
            });
            const newState = { ...data.result.state, combat_id: state.combat_id };

            // Damage numbers from log
            const pStrike = data.result.log?.find((l) => l.kind === "player_strike");
            const eStrike = data.result.log?.find((l) => l.kind === "enemy_strike");
            const counterStrike = data.result.log?.find((l) => l.kind === "innate_action" && l.text?.includes("Counter-strike"));
            if (pStrike && pStrike.damage > 0) {
                const id = Date.now() + Math.random();
                setMonsterDmg(prev => [...prev, { id, value: pStrike.damage, isCrit: pStrike.outcome === 6, type: pStrike.damage_type }]);
                setMonsterFlash(true);
                setTimeout(() => setMonsterFlash(false), 300);
            }
            if (counterStrike) {
                const match = counterStrike.text?.match(/(\d+) damage/);
                if (match) {
                    const id = Date.now() + Math.random() + 2;
                    setMonsterDmg(prev => [...prev, { id, value: parseInt(match[1]), isCrit: false, type: "physical" }]);
                    setMonsterFlash(true);
                    setTimeout(() => setMonsterFlash(false), 300);
                }
            }
            if (eStrike && eStrike.damage > 0) {
                const id = Date.now() + Math.random() + 1;
                setPlayerDmg(prev => [...prev, { id, value: eStrike.damage, isCrit: false, type: eStrike.damage_type }]);
                setPlayerFlash(true);
                setTimeout(() => setPlayerFlash(false), 300);
            }

            setState(newState);
            setCh(data.character);
            onCharacterUpdate?.(data.character);
            if (pStrike) setLastOutcome(pStrike.outcome);
            if (data.result.victory === true) {
                setVictory(true);
                setRewards(data.result.rewards);
                if (data.result.profession_ranks?.length > 0) {
                    for (const [newRank, oldRank] of data.result.profession_ranks) {
                        toast.success(`Profession rank up: ${oldRank} → ${newRank}!`);
                    }
                }
            } else if (data.result.victory === false) {
                setVictory(false);
                if (data.result.sanctuary_teleport) {
                    setSanctuaryTeleport(data.result.sanctuary_teleport);
                }
            }
            // Fetch telegraph for next turn
            if (data.result.victory === null) {
                fetchTelegraph(state.combat_id);
            }
        } catch (e) {
            toast.error(extractError(e));
        } finally {
            setRolling(false);
        }
    };

    const handleSkin = async () => {
        setSkinning(true);
        try {
            const { data } = await api.post("/game/combat/skin", {
                combat_id: state.combat_id,
            });
            setSkinResult(data.result);
            setCh(data.character);
            onCharacterUpdate?.(data.character);
            if (data.result.rank_change) {
                toast.success(`Profession rank up: ${data.result.rank_change[0]}!`);
            }
        } catch (e) {
            toast.error(extractError(e));
        } finally {
            setSkinning(false);
        }
    };

    const monsterHpPct = Math.round((state.monster_hp / Math.max(1, state.monster_max_hp)) * 100);
    const monsterShield = state.monster_shield || 0;
    const monsterMaxShield = state.monster_max_shield || 0;
    const monsterShieldPct = monsterMaxShield > 0 ? Math.round((monsterShield / monsterMaxShield) * 100) : 0;
    const monsterMp = state.monster_mp || 0;
    const monsterMaxMp = state.monster_max_mp || 0;
    const monsterStats = state.monster_stats || {};
    const monsterAffinities = state.monster_affinities || {};
    const monsterEnraged = state.monster_enraged || false;
    const monsterRarity = state.monster_rarity || "common";
    const monsterName = state.monster_name || state.monster_id.replace(/_/g, " ");
    const portraitUrl = monsterPortraitUrl(monsterName, monsterRarity);
    const playerHpPct = Math.round((ch.hp / Math.max(1, ch.max_hp)) * 100);

    const STAT_LABELS = { might: "MIG", insight: "INS", grace: "GRA", vitality: "VIT", essence: "ESS", armor: "ARM" };
    const AFFINITY_LABELS = { physical: "PHY", magical: "MAG", fire: "FIR", water: "WTR", lightning: "LTG", holy: "HLY", abyss: "ABY", earth: "ERT" };

    const INNATE_ACTIONS = [
        { id: "strike", label: "Strike", desc: "Basic attack. Full d6 roll." },
        { id: "defend", label: "Defend", desc: "Halve incoming damage. Heal 5% HP." },
        { id: "evade", label: "Evade", desc: "Roll d6: 4+ dodges attack, 1-3 = full damage." },
        { id: "aim", label: "Aim", desc: "Roll 2d6 keep higher. Damage capped at 1.2x." },
        { id: "counter", label: "Counter", desc: "If monster attacks, free counter-strike." },
        { id: "focus", label: "Focus", desc: "Restore 2 skill capacity. Next skill +1 outcome." },
    ];

    const comboCount = state.combo_count || 0;
    const comboMult = comboCount >= 7 ? 2.0 : comboCount >= 5 ? 1.5 : comboCount >= 3 ? 1.2 : 1.0;
    const isFocused = state.focused || false;

    // equipped skill bar (with cooldown info)
    const learnedSkills = (ch.skill_bar || [])
        .filter(Boolean)
        .map((sid) => ({
            id: sid,
            def: skillsById?.[sid],
            cooldown: state.skill_cooldowns?.[sid] || 0,
        }));

    // equipped item hotbar (with quantity)
    const consumables = (ch.item_bar || [])
        .filter(Boolean)
        .map((iid) => ({
            id: iid,
            qty: (ch.inventory || []).find((i) => i.item_id === iid)?.quantity || 0,
            def: resolveItem(iid),
        }))
        .filter((c) => c.def && c.qty > 0);

    if (victory !== null) {
        return (
            <TooltipProvider delayDuration={120}>
            <div className="panel p-6" data-testid="combat-result">
                <h3 className="font-pixel text-4xl uppercase mb-4"
                    style={{ color: victory ? "hsl(var(--primary))" : "hsl(var(--destructive))" }}>
                    {victory ? "VICTORY" : "DEFEAT"}
                </h3>
                <div className="narr text-lg text-foreground/90 mb-4">
                    {victory
                        ? `The ${state.monster_id.replace(/_/g, " ")} lies still. Erchis notices.`
                        : `${ch.name} collapses in the dust. The world does not weep.`}
                </div>
                {!victory && sanctuaryTeleport && (
                    <div className="mb-4 p-4 border border-primary/30 bg-primary/5 rounded">
                        <div className="font-pixel text-sm uppercase text-primary mb-1">Sanctuary Recovery</div>
                        <div className="narr text-sm text-foreground/80">
                            You wake in the Sanctuary at {sanctuaryTeleport.town_name}, your wounds tended by the priests. Your HP is restored to half. A lingering weakness remains — the Recovering debuff will fade after 3 actions, or visit the Sanctuary to cleanse it.
                        </div>
                    </div>
                )}
                {victory && rewards && (
                    <div className="grid grid-cols-3 gap-4 font-mono text-sm mb-4">
                        <div>
                            <div className="stat-label">GOLD</div>
                            <div className="text-primary text-xl">+{rewards.gold}</div>
                        </div>
                        <div>
                            <div className="stat-label">XP</div>
                            <div className="text-primary text-xl">+{rewards.xp}</div>
                        </div>
                        <div>
                            <div className="stat-label">DROPS</div>
                            <div className="text-primary text-xl">{rewards.items?.length || 0}</div>
                        </div>
                    </div>
                )}
                {victory && rewards?.items?.length > 0 && (
                    <div className="flex flex-wrap gap-2 mb-4">
                        {rewards.items.map((it, i) => {
                            const [iid, q] = it;
                            const def = (typeof iid === 'object' && iid !== null) ? iid : (resolveItem(iid) || null);
                            const rar = def?.rarity || "common";
                            const displayId = def?.instance_id || (typeof iid === 'string' ? iid : `item-${i}`);
                            return (
                                <ItemTooltip key={i} item={def}>
                                <span data-testid={`combat-drop-${displayId}`}
                                      className={`stat-label px-2 py-1 border ${RARITY_BORDER[rar] || RARITY_BORDER.common} ${RARITY_CLASS[rar] || ""} flex items-center gap-1.5`}>
                                    {def && <PixelSprite item={def} size={20} />}
                                    {def?.name || (typeof iid === 'string' ? iid : "Unknown")} × {q}
                                </span>
                                </ItemTooltip>
                            );
                        })}
                    </div>
                )}
                {victory && skinResult && (
                    <div className="mb-4 p-3 border border-primary/30 bg-primary/5 rounded">
                        <div className="narr text-sm text-foreground/80 mb-2">{skinResult.log}</div>
                        {skinResult.items?.length > 0 ? (
                            <div className="flex flex-wrap gap-2">
                                {skinResult.items.map((it, i) => {
                                    const [iid, q] = it;
                                    const def = (typeof iid === 'object' && iid !== null) ? iid : (resolveItem(iid) || null);
                                    const rar = def?.rarity || "common";
                                    const displayId = def?.instance_id || (typeof iid === 'string' ? iid : `skin-item-${i}`);
                                    return (
                                        <ItemTooltip key={i} item={def}>
                                        <span data-testid={`skin-drop-${displayId}`}
                                              className={`stat-label px-2 py-1 border ${RARITY_BORDER[rar] || RARITY_BORDER.common} ${RARITY_CLASS[rar] || ""} flex items-center gap-1.5`}>
                                            {def && <PixelSprite item={def} size={20} />}
                                            {def?.name || (typeof iid === 'string' ? iid : "Unknown")} × {q}
                                        </span>
                                        </ItemTooltip>
                                    );
                                })}
                            </div>
                        ) : (
                            <div className="stat-label text-muted-foreground">No materials recovered.</div>
                        )}
                    </div>
                )}
                {victory && !skinResult && (
                    <button
                        data-testid="combat-skin"
                        onClick={handleSkin}
                        disabled={skinning}
                        className="press-btn font-pixel text-sm uppercase px-4 py-2 bg-secondary text-secondary-foreground border-2 border-secondary hover:bg-transparent hover:text-secondary transition-colors mb-4 mr-2"
                    >
                        <Scissors className="inline w-4 h-4 mr-1" />
                        {skinning ? "Skinning..." : "Skin Beast"}
                    </button>
                )}
                <button
                    data-testid="combat-end-continue"
                    onClick={() => onEnd?.(ch, { sanctuaryTeleport })}
                    className="press-btn font-pixel text-lg uppercase px-6 py-2 bg-primary text-primary-foreground border-2 border-primary hover:bg-transparent hover:text-primary transition-colors"
                >
                    Continue →
                </button>
            </div>
            </TooltipProvider>
        );
    }

    return (
        <TooltipProvider delayDuration={120}>
        <div className="panel p-6 space-y-4" data-testid="combat-screen">
            <div className="flex items-start justify-between mb-2">
                <div>
                    <div className="stat-label text-primary/70 uppercase tracking-wider">Combat</div>
                    <h2 className={`font-pixel text-2xl uppercase ${RARITY_CLASS[monsterRarity] || "text-primary"}`}>{monsterName}</h2>
                </div>
                <button
                    onClick={() => onEnd?.(ch)}
                    data-testid="combat-back-btn"
                    className="press-btn flex items-center gap-1 stat-label px-3 py-1.5 border border-border text-muted-foreground hover:border-primary hover:text-primary transition-colors"
                >
                    <ArrowLeft size={14} /> Back
                </button>
            </div>

            {/* Combatants — player status (compact) + monster (wide) */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {/* Player combat status */}
                <div className="p-3 border border-border relative">
                    <div className="stat-label mb-2">{ch.name}</div>
                    {/* Player HP bar */}
                    <div className="mb-2">
                        <HpBar pct={playerHpPct} color="bg-primary" flash={playerFlash} />
                        <div className="font-mono text-[10px] text-muted-foreground mt-0.5">
                            HP {ch.hp}/{ch.max_hp}
                        </div>
                    </div>
                    {/* Floating damage numbers on player */}
                    <div className="absolute top-0 left-1/2 -translate-x-1/2 pointer-events-none">
                        {playerDmg.map(d => (
                            <DamageNumber key={d.id} value={d.value} type={d.type} isCrit={d.isCrit}
                                onDone={() => setPlayerDmg(prev => prev.filter(x => x.id !== d.id))} />
                        ))}
                    </div>
                    {(ch.statuses || []).length > 0 ? (
                        <div className="flex flex-wrap gap-1">
                            {ch.statuses.map((s, i) => (
                                <Tooltip key={`${s.id}-${i}`}>
                                    <TooltipTrigger asChild>
                                        <span
                                            className={`stat-label px-1.5 py-0.5 border text-[10px] cursor-help ${
                                                s.kind === "buff" ? "border-primary text-primary" : "border-destructive text-destructive"
                                            }`}
                                        >
                                            {s.name}{s.duration ? ` (${s.duration})` : ""}
                                        </span>
                                    </TooltipTrigger>
                                    <TooltipContent side="top" className="max-w-[280px] bg-popover border border-border text-popover-foreground">
                                        <StatusTooltipContent status={s} />
                                    </TooltipContent>
                                </Tooltip>
                            ))}
                        </div>
                    ) : (
                        <div className="stat-label text-[10px] text-muted-foreground/50">No active effects</div>
                    )}
                </div>
                {/* Monster */}
                <div className={`md:col-span-2 p-3 border-2 relative ${RARITY_BORDER[monsterRarity] || RARITY_BORDER.common}`}>
                    <div className="flex items-start gap-3 mb-2">
                        {/* Monster portrait */}
                        <div className={`flex-shrink-0 w-20 h-20 border-2 ${RARITY_BORDER[monsterRarity] || RARITY_BORDER.common} bg-background overflow-hidden`}>
                            <img
                                src={portraitUrl}
                                alt={monsterName}
                                className="w-full h-full object-cover"
                                style={{ imageRendering: "pixelated" }}
                            />
                        </div>
                        <div className="flex-1">
                            <div className={`stat-label uppercase flex items-center gap-2 ${RARITY_CLASS[monsterRarity] || "text-destructive"}`}>
                                {monsterName}
                                <span className="text-[10px] uppercase opacity-70">{monsterRarity}</span>
                                {monsterEnraged && <span className="text-orange-400 animate-pulse">ENRAGED</span>}
                            </div>
                            {/* Monster HP bar */}
                            <div className="mt-1">
                                <HpBar pct={monsterHpPct} color="bg-destructive" shieldPct={monsterShieldPct} flash={monsterFlash} />
                            </div>
                            <div className="font-mono text-xs text-muted-foreground mt-1 flex items-center gap-3">
                                <span>HP {state.monster_hp}/{state.monster_max_hp}</span>
                                {monsterMaxMp > 0 && <span className="text-blue-400">MP {monsterMp}/{monsterMaxMp}</span>}
                                {monsterMaxShield > 0 && <span className="text-cyan-400">SH {monsterShield}/{monsterMaxShield}</span>}
                            </div>
                        </div>
                    </div>
                    {/* Floating damage numbers on monster */}
                    <div className="absolute top-0 left-1/3 pointer-events-none">
                        {monsterDmg.map(d => (
                            <DamageNumber key={d.id} value={d.value} type={d.type} isCrit={d.isCrit}
                                onDone={() => setMonsterDmg(prev => prev.filter(x => x.id !== d.id))} />
                        ))}
                    </div>
                    {/* Monster stats */}
                    {Object.keys(monsterStats).length > 0 && (
                        <div className="flex flex-wrap gap-2 mt-2 font-mono text-[10px] text-muted-foreground">
                            {Object.entries(STAT_LABELS).map(([key, label]) => (
                                <span key={key} className="px-1 border border-border/50">
                                    {label} {monsterStats[key] || 0}
                                </span>
                            ))}
                        </div>
                    )}
                    {/* Affinities */}
                    {(monsterAffinities.weak?.length > 0 || monsterAffinities.resist?.length > 0) && (
                        <div className="flex flex-wrap gap-2 mt-1 font-mono text-[10px]">
                            {monsterAffinities.weak?.map((w) => (
                                <span key={w} className="px-1 text-orange-400 border border-orange-400/30">
                                    Weak {AFFINITY_LABELS[w] || w}
                                </span>
                            ))}
                            {monsterAffinities.resist?.map((r) => (
                                <span key={r} className="px-1 text-blue-400 border border-blue-400/30">
                                    Resist {AFFINITY_LABELS[r] || r}
                                </span>
                            ))}
                        </div>
                    )}
                </div>
            </div>

            {/* Dice + last log */}
            <div className="flex items-center gap-6 border-t border-border pt-4">
                <Dice result={lastOutcome || "?"} rolling={rolling} size={90} testId="combat-dice" />
                <div className="flex-1 max-h-40 overflow-y-auto space-y-2" data-testid="combat-log">
                    {state.log?.slice().reverse().map((entry, i) => (
                        <div key={i} className={`narr text-sm leading-snug ${entry.kind === "enrage" ? "text-orange-400 font-bold" : entry.kind === "shield_absorb" ? "text-cyan-400" : entry.kind === "enemy_skill" ? "text-amber-400" : entry.kind === "innate_action" ? "text-primary/90" : entry.kind === "carve" ? "text-primary font-semibold" : entry.kind === "range_gap" ? "text-blue-400" : entry.kind === "hunter_range" ? "text-orange-400" : "text-foreground/85"}`}>
                            {entry.skill_text && <div className="stat-label text-primary/70 mb-0.5">{entry.skill_text}</div>}
                            {entry.text}
                            {entry.damage !== undefined && (
                                <span className="ml-2 font-mono text-xs text-destructive">
                                    [{entry.damage} {entry.damage_type || ""} dmg]
                                </span>
                            )}
                        </div>
                    ))}
                </div>
            </div>

            {/* Telegraph banner */}
            {telegraph?.available && (
                <div className={`border-t border-border pt-3`}>
                    <div className={`flex items-start gap-2 p-2 border ${telegraph.is_heavy ? "border-destructive/50 bg-destructive/10" : telegraph.color === "amber" ? "border-amber-500/50 bg-amber-500/10" : "border-primary/50 bg-primary/10"}`}>
                        <span className={`text-lg ${telegraph.is_heavy ? "text-destructive" : telegraph.color === "amber" ? "text-amber-400" : "text-primary"}`}>⚠</span>
                        <div className="flex-1">
                            <div className={`text-sm font-pixel ${telegraph.is_heavy ? "text-destructive" : telegraph.color === "amber" ? "text-amber-400" : "text-primary"}`}>
                                {telegraph.warning_text}
                            </div>
                            <div className="flex gap-2 mt-1 text-[10px] stat-label">
                                {telegraph.skill_name && (
                                    <span className="px-1 border border-border text-foreground">{telegraph.skill_name}</span>
                                )}
                                {telegraph.damage_type && (
                                    <span className="px-1 border border-border text-muted-foreground uppercase">{telegraph.damage_type}</span>
                                )}
                                {telegraph.estimated_damage && (
                                    <span className="px-1 border border-destructive/40 text-destructive">~{telegraph.estimated_damage} dmg</span>
                                )}
                                {telegraph.is_heavy && (
                                    <span className="px-1 border border-destructive text-destructive font-bold">HEAVY</span>
                                )}
                            </div>
                        </div>
                    </div>
                </div>
            )}

            {/* Innate actions */}
            <div className="border-t border-border pt-3">
                <div className="stat-label mb-2">INNATE ACTION</div>
                <div className="flex flex-wrap gap-1">
                    {INNATE_ACTIONS.map((act) => (
                        <Tooltip key={act.id}>
                            <TooltipTrigger asChild>
                                <button
                                    data-testid={`innate-${act.id}`}
                                    onClick={() => setActionType(act.id)}
                                    className={`stat-label px-2 py-1.5 border transition-colors ${
                                        actionType === act.id
                                            ? "border-primary text-primary bg-primary/10"
                                            : "border-border text-muted-foreground hover:border-primary/50"
                                    } ${isFocused && act.id !== "focus" ? "ring-1 ring-primary/30" : ""}`}
                                >
                                    {act.label}
                                </button>
                            </TooltipTrigger>
                            <TooltipContent side="top" className="max-w-[220px] text-center overflow-visible bg-popover text-popover-foreground border border-border px-3 py-2">
                                <p className="font-pixel text-xs mb-1">{act.label}</p>
                                <p className="narr text-xs text-popover-foreground/80">{act.desc}</p>
                            </TooltipContent>
                        </Tooltip>
                    ))}
                </div>
            </div>

            {/* Mastery-specific combat HUD */}
            <MasteryCombatHUD
                character={ch}
                state={state}
                combatId={state.combat_id}
                onStateUpdate={(newState) => setState({ ...newState, combat_id: state.combat_id })}
            />

            {/* Skill / item override + combo */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 border-t border-border pt-4">
                <div>
                    <div className="stat-label mb-2">SKILL (auto: slot order)</div>
                    <div className="flex flex-wrap gap-1">
                        <button
                            data-testid="skill-manual-none"
                            onClick={() => setPendingSkillId(null)}
                            className={`stat-label px-2 py-1 border ${!pendingSkillId ? "border-primary text-primary" : "border-border text-muted-foreground"}`}
                        >
                            AUTO
                        </button>
                        {learnedSkills.map((s) => (
                            <button
                                key={s.id}
                                data-testid={`skill-manual-${s.id}`}
                                disabled={s.cooldown > 0 || !s.def}
                                onClick={() => setPendingSkillId(s.id)}
                                className={`stat-label px-2 py-1 border ${
                                    pendingSkillId === s.id
                                        ? "border-primary text-primary"
                                        : "border-border text-muted-foreground hover:border-primary"
                                } disabled:opacity-40`}
                            >
                                {s.def?.name || s.id}
                                {s.cooldown > 0 && <span className="ml-1 text-destructive">({s.cooldown})</span>}
                            </button>
                        ))}
                    </div>
                </div>
                <div>
                    <div className="stat-label mb-2">ITEM (auto: pre-combat)</div>
                    <div className="flex flex-wrap gap-1">
                        <button
                            data-testid="item-manual-none"
                            onClick={() => setPendingItemId(null)}
                            className={`stat-label px-2 py-1 border ${!pendingItemId ? "border-primary text-primary" : "border-border text-muted-foreground"}`}
                        >
                            AUTO
                        </button>
                        {consumables.map((c) => (
                            <button
                                key={c.id}
                                data-testid={`item-manual-${c.id}`}
                                onClick={() => setPendingItemId(c.id)}
                                className={`stat-label px-2 py-1 border ${
                                    pendingItemId === c.id
                                        ? "border-primary text-primary"
                                        : "border-border text-muted-foreground hover:border-primary"
                                }`}
                            >
                                {c.def?.name || c.id} × {c.qty}
                            </button>
                        ))}
                    </div>
                </div>
            </div>

            {/* Combo meter + skill capacity */}
            <div className="flex items-center justify-between border-t border-border pt-2">
                <div className="flex items-center gap-3">
                    {comboMult > 1.0 && (
                        <span className="font-pixel text-sm text-orange-400 animate-pulse" data-testid="combo-meter">
                            Combo ×{comboCount} {comboMult >= 2.0 ? "🔥🔥" : comboMult >= 1.5 ? "🔥" : ""}
                        </span>
                    )}
                    {isFocused && (
                        <span className="font-pixel text-xs text-primary border border-primary/50 px-1.5 py-0.5">
                            FOCUSED (+1 outcome)
                        </span>
                    )}
                </div>
                <div className="stat-label text-[10px] text-muted-foreground">
                    Skill Capacity: {state.max_skill_capacity - (state.skill_capacity_used || 0)}/{state.max_skill_capacity || 8}
                </div>
            </div>

            <div className="border-t border-border pt-4">
                <button
                    data-testid="combat-attack-btn"
                    onClick={takeTurn}
                    disabled={rolling}
                    className="press-btn w-full font-pixel text-2xl uppercase py-3 bg-primary text-primary-foreground border-2 border-primary hover:bg-transparent hover:text-primary transition-colors disabled:opacity-40"
                    style={{ boxShadow: "3px 3px 0 0 hsl(var(--destructive))" }}
                >
                    {rolling ? "ROLLING…" : actionType.toUpperCase()}
                </button>
            </div>

            <style>{`
                @keyframes dmgFloat {
                    0% { opacity: 1; transform: translate(-50%, 0) scale(1); }
                    20% { transform: translate(-50%, -10px) scale(1.3); }
                    100% { opacity: 0; transform: translate(-50%, -60px) scale(1); }
                }
            `}</style>
        </div>
        </TooltipProvider>
    );
}
