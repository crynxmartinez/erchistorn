import { Heart, Zap, Coins, Star, Trash2, Activity } from "lucide-react";
import { useState } from "react";
import RacialPanel from "@/components/RacialPanel";
import PixelSprite from "@/components/PixelSprite";
import ItemTooltip from "@/components/ItemTooltip";
import { Tooltip, TooltipTrigger, TooltipContent, TooltipProvider } from "@/components/ui/tooltip";
import { STAT_HINTS } from "@/data/hints";
import StatusTooltipContent from "@/components/StatusTooltipContent";

const FAITH_TIER_NAMES = [
    "Unbroken", "Faith Stirring", "Faith Rising",
    "Faith Burning", "Faith Blazing", "Faith Unleashed", "Faith Ascendant",
];
const FAITH_TIER_COLORS = [
    "text-green-400", "text-lime-400", "text-yellow-400",
    "text-orange-400", "text-red-400", "text-red-500", "text-fuchsia-400",
];
const FAITH_TIER_DESCS = [
    "HP > 90%. No bonuses.",
    "HP ≤ 90%. +10% main stats, +5% healing.",
    "HP ≤ 70%. +15% main stats, +10% healing.",
    "HP ≤ 50%. +25% main stats, +20% healing.",
    "HP ≤ 25%. +35% main stats, +30% healing.",
    "HP ≤ 10%. +40% main stats, +40% healing.",
    "HP ≤ 5%. +50% main stats, +50% healing.",
];

function StatHint({ label }) {
    return <div className="font-pixel text-xs leading-snug max-w-[240px]">{label}</div>;
}

function StatValue({ statKey, character }) {
    const total = character.stats?.[statKey] ?? 0;
    const paladinBonus = character.paladin_faith_bonuses?.[statKey] ?? 0;
    const knightOathBonus = character.knight_current_oath_bonuses?.[statKey] ?? 0;
    const knightSkillBonus = character.knight_self_stat_mods?.[statKey] ?? 0;
    const bonus = paladinBonus + knightOathBonus + knightSkillBonus;
    const base = total - bonus;
    if (bonus > 0) {
        return (
            <span>
                <span className="text-primary">{base}</span>
                <span className="text-green-400 text-[10px]"> (+{bonus})</span>
            </span>
        );
    }
    return <span className="text-primary">{total}</span>;
}

export default function CharacterSheet({ character, portraits, race, role, mastery, itemsById, timeOfDay, onDeleteCharacter }) {
    const [confirmDelete, setConfirmDelete] = useState(false);
    if (!character) return null;
    const portrait = portraits?.find((p) => p.id === character.portrait_id);
    const hpPct = Math.round((character.hp / Math.max(1, character.max_hp)) * 100);
    const xpNext = 100 + (character.level - 1) * 40;
    const xpPct = Math.round((character.xp / xpNext) * 100);
    const equipped = character.equipped || {};
    const EQUIP_SLOTS = [
        ["head", "Head"], ["body", "Body"],
        ["left_hand", "L.Hand"], ["right_hand", "R.Hand"],
        ["legs", "Legs"], ["feet", "Feet"],
        ["earring_l", "Ear L"], ["earring_r", "Ear R"],
        ["ring_l", "Ring L"], ["ring_r", "Ring R"],
        ["neck", "Neck"], ["back", "Back"],
    ];

    return (
        <TooltipProvider delayDuration={120}>
        <div className="panel p-4 space-y-4" data-testid="character-sheet">
            <div className="flex gap-3">
                {portrait ? (
                    <img
                        src={portrait.url}
                        alt={character.name}
                        className="w-20 h-20 border border-primary bg-card"
                        data-testid="char-portrait"
                    />
                ) : (
                    <div className="sprite-slot w-20 h-20">?</div>
                )}
                <div className="min-w-0 flex-1">
                    <div className="font-pixel text-xl uppercase text-primary truncate" data-testid="char-name">
                        {character.name}
                    </div>
                    <div className="stat-label truncate">
                        {race?.name} · {role?.name}
                    </div>
                    <div className="stat-label truncate text-muted-foreground">{mastery?.name}</div>
                    <div className="flex items-center gap-1 mt-1 stat-label">
                        <Star size={10} className="text-primary" /> LVL {character.level}
                    </div>
                </div>
            </div>

            {/* HP bar */}
            <div>
                <Tooltip>
                    <TooltipTrigger asChild>
                        <div className="flex justify-between stat-label mb-1 cursor-help" data-testid="hp-row-tip">
                            <span className="flex items-center gap-1"><Heart size={10} className="text-destructive" /> HP</span>
                            <span className="text-foreground" data-testid="hp-numeric">
                                {character.hp}/{character.max_hp}
                            </span>
                        </div>
                    </TooltipTrigger>
                    <TooltipContent side="bottom"><StatHint label={STAT_HINTS.hp} /></TooltipContent>
                </Tooltip>
                <div className="h-3 bg-background border border-border relative">
                    <div className="h-full bg-destructive transition-all" style={{ width: `${hpPct}%` }} />
                </div>
                {character.hp_regen_per_min > 0 && character.hp < character.max_hp && (
                    <Tooltip>
                        <TooltipTrigger asChild>
                            <div className="flex items-center gap-1 stat-label text-green-400/80 mt-0.5 cursor-help" data-testid="hp-regen-timer">
                                <Activity size={9} />
                                <span>+{character.hp_regen_per_min} HP/min</span>
                                <span className="text-muted-foreground">·</span>
                                <span className="text-muted-foreground">full in {Math.ceil((character.max_hp - character.hp) / character.hp_regen_per_min)}m</span>
                            </div>
                        </TooltipTrigger>
                        <TooltipContent side="bottom">
                            <div className="font-pixel text-xs leading-snug max-w-[240px]">
                                Racial passive: +{character.hp_regen_per_min} HP per minute (real-time).
                                Recovers even while logged out.
                                Full in ~{Math.ceil((character.max_hp - character.hp) / character.hp_regen_per_min)} minutes.
                            </div>
                        </TooltipContent>
                    </Tooltip>
                )}
            </div>

            {/* XP bar */}
            <div>
                <Tooltip>
                    <TooltipTrigger asChild>
                        <div className="flex justify-between stat-label mb-1 cursor-help">
                            <span className="flex items-center gap-1"><Zap size={10} className="text-primary" /> XP</span>
                            <span className="text-foreground">{character.xp}/{xpNext}</span>
                        </div>
                    </TooltipTrigger>
                    <TooltipContent side="bottom"><StatHint label={STAT_HINTS.xp} /></TooltipContent>
                </Tooltip>
                <div className="h-2 bg-background border border-border relative">
                    <div className="h-full bg-primary transition-all" style={{ width: `${xpPct}%` }} />
                </div>
            </div>

            {/* Gold */}
            <Tooltip>
                <TooltipTrigger asChild>
                    <div className="flex justify-between items-center stat-label cursor-help">
                        <span className="flex items-center gap-1"><Coins size={12} className="text-primary" /> GOLD</span>
                        <span className="text-primary font-mono" data-testid="char-gold">{character.gold}</span>
                    </div>
                </TooltipTrigger>
                <TooltipContent side="bottom"><StatHint label={STAT_HINTS.gold} /></TooltipContent>
            </Tooltip>

            {/* Stats */}
            <div className="border-t border-border pt-3">
                {/* Paladin faith bar */}
                {character.paladin_faith_tier != null && (() => {
                    const tier = character.paladin_faith_tier;
                    return (
                        <Tooltip>
                            <TooltipTrigger asChild>
                                <div className="flex items-center gap-1.5 mb-3 cursor-help">
                                    <span className="stat-label text-[10px] text-muted-foreground">FAITH</span>
                                    <div className="flex gap-0.5">
                                        {[1, 2, 3, 4, 5, 6].map((i) => (
                                            <div
                                                key={i}
                                                className={`w-2 h-2.5 ${i <= tier ? "bg-primary" : "bg-border"}`}
                                            />
                                        ))}
                                    </div>
                                    <span className={`font-pixel text-[10px] ${FAITH_TIER_COLORS[tier]}`}>
                                        {FAITH_TIER_NAMES[tier]}
                                    </span>
                                </div>
                            </TooltipTrigger>
                            <TooltipContent side="bottom" className="max-w-[300px] bg-popover text-popover-foreground border border-border px-3 py-2">
                                <p className="font-pixel text-xs mb-1.5">Faith Scaling</p>
                                <p className="narr text-xs mb-2 text-popover-foreground/80">The Paladin grows stronger as HP falls. All main stats scale up automatically.</p>
                                <div className="space-y-1 text-xs">
                                    {FAITH_TIER_NAMES.map((name, i) => (
                                        <div key={i} className={`flex items-center gap-1.5 ${i === tier ? "font-bold" : "opacity-70"}`}>
                                            <span className={FAITH_TIER_COLORS[i]}>{name}</span>
                                            <span>— {FAITH_TIER_DESCS[i]}</span>
                                        </div>
                                    ))}
                                </div>
                            </TooltipContent>
                        </Tooltip>
                    );
                })()}
                <div className="stat-label mb-2">MAIN STATS</div>
                <div className="grid grid-cols-3 gap-1 font-mono text-xs">
                    {["might", "grace", "insight"].map((k) => (
                        <Tooltip key={k}>
                            <TooltipTrigger asChild>
                                <div className="text-center border-b border-border/40 pb-1 cursor-help" data-testid={`stat-tip-${k}`}>
                                    <div className="stat-label">{k.slice(0, 3).toUpperCase()}</div>
                                    <div className="text-lg"><StatValue statKey={k} character={character} /></div>
                                </div>
                            </TooltipTrigger>
                            <TooltipContent side="top"><StatHint label={STAT_HINTS[k]} /></TooltipContent>
                        </Tooltip>
                    ))}
                </div>
                <div className="stat-label mt-3 mb-2">LIFE STATS</div>
                <div className="grid grid-cols-2 gap-1 font-mono text-xs">
                    {["vitality", "cognition", "essence", "durability"].map((k) => (
                        <Tooltip key={k}>
                            <TooltipTrigger asChild>
                                <div className="flex justify-between border-b border-border/40 pb-0.5 cursor-help" data-testid={`stat-tip-${k}`}>
                                    <span className="text-muted-foreground uppercase">{k.slice(0, 3)}</span>
                                    <StatValue statKey={k} character={character} />
                                </div>
                            </TooltipTrigger>
                            <TooltipContent side="bottom"><StatHint label={STAT_HINTS[k]} /></TooltipContent>
                        </Tooltip>
                    ))}
                </div>
                {(character.stats?.armor_bonus || character.stats?.evasion_mod) ? (
                    <div className="grid grid-cols-2 gap-1 font-mono text-xs mt-2">
                        {character.stats?.armor_bonus ? (
                            <Tooltip>
                                <TooltipTrigger asChild>
                                    <div className="flex justify-between border-b border-border/40 pb-0.5 cursor-help">
                                        <span className="text-muted-foreground">ARMOR+</span>
                                        <StatValue statKey="armor_bonus" character={character} />
                                    </div>
                                </TooltipTrigger>
                                <TooltipContent side="bottom"><StatHint label={STAT_HINTS.armor_bonus} /></TooltipContent>
                            </Tooltip>
                        ) : null}
                        {character.stats?.evasion_mod ? (
                            <Tooltip>
                                <TooltipTrigger asChild>
                                    <div className="flex justify-between border-b border-border/40 pb-0.5 cursor-help">
                                        <span className="text-muted-foreground">EVA</span>
                                        <span className={character.stats.evasion_mod < 0 ? "text-destructive" : "text-primary"}>
                                            {character.stats.evasion_mod >= 0 ? "+" : ""}{character.stats.evasion_mod}
                                        </span>
                                    </div>
                                </TooltipTrigger>
                                <TooltipContent side="bottom"><StatHint label={STAT_HINTS.evasion_mod} /></TooltipContent>
                            </Tooltip>
                        ) : null}
                    </div>
                ) : null}
            </div>

            {/* Equipped */}
            <div className="border-t border-border pt-3">
                <div className="stat-label mb-2">EQUIPPED</div>
                <div className="grid grid-cols-2 gap-x-3 gap-y-1 text-xs font-mono">
                    {EQUIP_SLOTS.map(([slotKey, slotLabel]) => {
                        const itemId = equipped[slotKey];
                        const itemInstances = character.item_instances || [];
                        const inst = itemInstances.find((i) => i.instance_id === itemId);
                        const item = inst || (itemId ? itemsById?.[itemId] : null);
                        return (
                            <div key={slotKey} className="flex justify-between items-center">
                                <span className="text-muted-foreground">{slotLabel}</span>
                                <ItemTooltip item={item}>
                                    <span className="text-foreground flex items-center gap-1.5 min-w-0">
                                        {item && <PixelSprite item={item} size={16} />}
                                        <span className="truncate">{item?.name || "—"}</span>
                                    </span>
                                </ItemTooltip>
                            </div>
                        );
                    })}
                </div>
            </div>

            {/* Statuses */}
            {(character.statuses || []).length > 0 && (
                <div className="border-t border-border pt-3">
                    <div className="stat-label mb-2">STATUS</div>
                    <div className="flex flex-wrap gap-1">
                        {character.statuses.map((s, i) => (
                            <Tooltip key={`${s.id}-${i}`}>
                                <TooltipTrigger asChild>
                                    <span
                                        data-testid={`status-${s.id}`}
                                        className={`stat-label px-2 py-0.5 border cursor-help ${
                                            s.kind === "buff"
                                                ? "border-primary text-primary"
                                                : "border-destructive text-destructive"
                                        }`}
                                    >
                                        {s.name}{s.duration ? ` (${s.duration})` : ""}
                                    </span>
                                </TooltipTrigger>
                                <TooltipContent side="bottom" className="max-w-[280px] bg-popover border border-border text-popover-foreground">
                                    <StatusTooltipContent status={s} />
                                </TooltipContent>
                            </Tooltip>
                        ))}
                    </div>
                </div>
            )}

            {/* Legendary Powers */}
            {(character.legendary_powers_summary || []).length > 0 && (
                <div className="border-t border-border pt-3">
                    <div className="stat-label mb-2 flex items-center gap-1"><Star size={10} className="text-yellow-400" /> LEGENDARY POWERS</div>
                    <div className="space-y-1">
                        {character.legendary_powers_summary.map((lp) => (
                            <Tooltip key={lp.id}>
                                <TooltipTrigger asChild>
                                    <div className="narr text-xs text-yellow-400/90 cursor-help leading-snug">
                                        {lp.name}
                                    </div>
                                </TooltipTrigger>
                                <TooltipContent side="bottom" className="max-w-[280px] bg-popover border border-border text-popover-foreground">
                                    <p className="font-pixel text-xs mb-1 text-yellow-400">{lp.name}</p>
                                    <p className="narr text-xs text-popover-foreground/80">{lp.desc}</p>
                                </TooltipContent>
                            </Tooltip>
                        ))}
                    </div>
                </div>
            )}

            {/* Set Bonuses */}
            {(character.set_bonuses_summary || []).length > 0 && (
                <div className="border-t border-border pt-3">
                    <div className="stat-label mb-2">SET BONUSES</div>
                    <div className="space-y-1">
                        {character.set_bonuses_summary.map((sb) => (
                            <div key={sb.set_id} className="narr text-xs text-foreground/80">
                                {sb.set_name} ({sb.count} pcs)
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* Item Bonus Effects */}
            {(() => {
                const ibe = character.item_bonus_effects_summary || {};
                const entries = Object.entries(ibe).filter(([k]) => k !== "_extra_damage");
                const extraDmg = ibe._extra_damage || [];
                if (entries.length === 0 && extraDmg.length === 0) return null;
                return (
                    <div className="border-t border-border pt-3">
                        <div className="stat-label mb-2">ITEM EFFECTS</div>
                        <div className="space-y-0.5">
                            {entries.map(([key, val]) => {
                                const isPct = key.includes("_pct") || key.includes("amp") || key.includes("pen") ||
                                    key.includes("lifesteal") || key.includes("thorns") || key.includes("resist") ||
                                    key.includes("chance") || key.includes("speed") || key.includes("accuracy") ||
                                    key.startsWith("apply_");
                                return (
                                    <div key={key} className="flex justify-between text-xs font-mono">
                                        <span className="text-muted-foreground">{key.replace(/_/g, " ")}</span>
                                        <span className="text-primary">
                                            {isPct ? `+${(val * 100).toFixed(0)}%` : `+${val}`}
                                        </span>
                                    </div>
                                );
                            })}
                            {extraDmg.map((ed, i) => (
                                <div key={`ed-${i}`} className="flex justify-between text-xs font-mono">
                                    <span className="text-muted-foreground">{ed.element} dmg</span>
                                    <span className="text-primary">+{ed.value}</span>
                                </div>
                            ))}
                        </div>
                    </div>
                );
            })()}

            {character.oath && (
                <div className="border-t border-border pt-3">
                    <div className="stat-label mb-1">SACRED OATH</div>
                    <div className="narr text-xs text-foreground/85 break-words">&ldquo;{character.oath}&rdquo;</div>
                </div>
            )}

            <RacialPanel character={character} timeOfDay={timeOfDay} />

            {onDeleteCharacter && (
                <div className="border-t border-border pt-3">
                    {!confirmDelete ? (
                        <button
                            onClick={() => setConfirmDelete(true)}
                            className="w-full press-btn font-pixel text-xs uppercase px-3 py-2 border-2 border-border text-muted-foreground hover:border-destructive hover:text-destructive flex items-center justify-center gap-1.5"
                        >
                            <Trash2 size={12} strokeWidth={1.5} /> Delete Character
                        </button>
                    ) : (
                        <div className="space-y-2">
                            <div className="font-pixel text-xs text-destructive text-center leading-snug">
                                This will permanently delete your character and log you out. You will need to create a new character to play again.
                            </div>
                            <div className="flex gap-2">
                                <button
                                    onClick={() => setConfirmDelete(false)}
                                    className="flex-1 press-btn font-pixel text-xs uppercase px-3 py-2 border-2 border-border text-muted-foreground hover:border-primary hover:text-primary"
                                >
                                    Cancel
                                </button>
                                <button
                                    onClick={onDeleteCharacter}
                                    className="flex-1 press-btn font-pixel text-xs uppercase px-3 py-2 border-2 border-destructive text-destructive hover:bg-destructive hover:text-destructive-foreground"
                                >
                                    Confirm Delete
                                </button>
                            </div>
                        </div>
                    )}
                </div>
            )}
        </div>
        </TooltipProvider>
    );
}
