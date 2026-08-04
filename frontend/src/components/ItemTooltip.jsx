import { Tooltip, TooltipTrigger, TooltipContent } from "@/components/ui/tooltip";
import { RARITY_TEXT } from "@/data/gameData";

const RARITY_LABEL = {
    common: "Common",
    uncommon: "Uncommon",
    rare: "Rare",
    epic: "Epic",
    legendary: "Legendary",
    mythic: "Mythic",
    exotic: "Exotic",
    normal: "Normal",
    magic: "Magic",
    unique: "Unique",
    set: "Set",
};

const KIND_LABEL = {
    material: "Material",
    weapon: "Weapon",
    armor: "Armor",
    consumable: "Consumable",
    skillbook: "Skillbook",
    relic: "Relic",
    boss_part: "Boss Part",
    tool: "Tool",
    gem: "Gem",
    rune: "Rune",
};

const SLOT_LABELS = {
    head: "Head", body: "Body", left_hand: "Left Hand", right_hand: "Right Hand",
    legs: "Legs", feet: "Feet", earring_l: "Earring (L)", earring_r: "Earring (R)",
    ring_l: "Ring (L)", ring_r: "Ring (R)", neck: "Necklace", back: "Back",
};

const WEAPON_TYPE_LABEL = {
    dagger: "Dagger", sword_1h: "Sword (1H)", sword_2h: "Sword (2H)",
    axe_1h: "Axe (1H)", great_axe: "Great Axe", hammer_1h: "Hammer (1H)",
    great_hammer: "Great Hammer", spear: "Spear", scythe: "Scythe",
    katar: "Katar", orb: "Orb", tome: "Tome", instrument: "Instrument",
    bow: "Bow", crossbow: "Crossbow", shield: "Shield",
};

const STAT_LABELS = {
    might: "Might", grace: "Grace", cognition: "Cognition",
    insight: "Insight", essence: "Essence", durability: "Durability",
    vitality: "Vitality", resilience: "Resilience",
    armor: "Armor", armor_bonus: "Armor",
    magic_resist: "Magic Resist", magic_resistance: "Magic Resistance",
    accuracy: "Accuracy", evasion: "Evasion",
};

function isInstance(item) {
    return !!(item && item.instance_id);
}

function instanceStatLine(item) {
    const parts = [];
    const bs = item.base_stats || {};
    for (const [k, v] of Object.entries(bs)) {
        if (v) parts.push(`${STAT_LABELS[k] || k} +${v}`);
    }
    return parts.join(" · ");
}

function instanceAffixLines(item) {
    const lines = [];
    for (const p of (item.prefixes || [])) {
        for (const [k, v] of Object.entries(p.stats || {})) {
            if (v) lines.push({ label: STAT_LABELS[k] || k, value: `+${v}`, type: "prefix" });
        }
        if (p.bonus_effects) {
            for (const be of p.bonus_effects) {
                lines.push({ label: be.name || be.type, value: be.description || "", type: "prefix" });
            }
        }
    }
    for (const s of (item.suffixes || [])) {
        for (const [k, v] of Object.entries(s.stats || {})) {
            if (v) lines.push({ label: STAT_LABELS[k] || k, value: `+${v}`, type: "suffix" });
        }
        if (s.bonus_effects) {
            for (const be of s.bonus_effects) {
                lines.push({ label: be.name || be.type, value: be.description || "", type: "suffix" });
            }
        }
    }
    return lines;
}

function instanceBonusEffectLines(item) {
    const lines = [];
    for (const be of (item.bonus_effects || [])) {
        if (be.name) lines.push(be.name);
        else if (be.type) lines.push(be.type);
    }
    return lines;
}

function instanceUpgradeLines(item) {
    const up = item.upgrades;
    if (!up) return [];
    const lines = [];
    if (up.gems && up.gems.length) {
        for (const g of up.gems) {
            lines.push(`◆ ${g.name || g.id} (Gem)`);
        }
    }
    if (up.runes && up.runes.length) {
        for (const r of up.runes) {
            lines.push(`⟡ ${r.name || r.id} (Rune)`);
        }
    }
    if (up.count > 0) {
        lines.push(`Upgrades: ${up.count}/${up.max || 10}`);
    }
    return lines;
}

function autoDesc(item) {
    const kind = item.kind || "material";
    const rarity = item.rarity || "common";
    const name = item.name || "Unknown";

    if (kind === "weapon") {
        const statParts = [];
        if (item.stats) {
            for (const [k, v] of Object.entries(item.stats)) {
                if (v) statParts.push(`${k.charAt(0).toUpperCase() + k.slice(1)} +${v}`);
            }
        }
        return `A ${rarity} ${name.toLowerCase()}. ${statParts.join(". ")}.`;
    }
    if (kind === "armor") {
        const statParts = [];
        if (item.stats) {
            for (const [k, v] of Object.entries(item.stats)) {
                if (v) statParts.push(`${k.charAt(0).toUpperCase() + k.slice(1)} +${v}`);
            }
        }
        return `A ${rarity} piece of armor. ${statParts.join(". ")}.`;
    }
    if (kind === "consumable") {
        // `effect` is always a dict of {kind: magnitude}. Crafted potions used to
        // ship a string effect plus a separate `power` scalar, which the backend
        // could not read at all — every crafted potion raised a TypeError on use.
        const eff = item.effect || {};
        if (eff.heal) return `Restores ${eff.heal} HP when consumed.`;
        if (eff.gold) return `Open to receive ${eff.gold} gold.`;
        if (eff.cure) return `Cures ${eff.cure}.`;
        if (eff.damage) return `Deals ${eff.damage} damage when thrown.`;
        if (eff.restore_mp) return `Restores ${eff.restore_mp} MP when consumed.`;
        if (eff.buff_stat) return `Grants +${eff.buff_stat} ${item.stat || ""} for a time.`;
        if (eff.resist) return `Grants +${eff.resist} resistance for a time.`;
        if (eff.hp_regen) return `Regenerates ${eff.hp_regen} HP per turn.`;
        if (eff.mp_regen) return `Regenerates ${eff.mp_regen} MP per turn.`;
        if (eff.stamina) return `Recovers ${eff.stamina} stamina.`;
        if (eff.xp_buff) return `Grants +${eff.xp_buff}% XP gain.`;
        return `A ${rarity} consumable.`;
    }
    if (kind === "skillbook") {
        return `A tome that teaches the ${item.teaches || "unknown"} skill. Read carefully — knowledge is heavier than it looks.`;
    }
    if (kind === "relic") {
        return `An ancient relic of ${rarity} quality. Its origins are lost to time.`;
    }
    if (kind === "boss_part") {
        return `A rare trophy from a defeated boss. Used in legendary crafting.`;
    }
    if (kind === "gem") {
        return item.desc || `A ${rarity} gem. Socket into equipment for bonuses.`;
    }
    if (kind === "rune") {
        return item.desc || `A ${rarity} rune. Socket into equipment for powerful effects.`;
    }
    if (kind === "material") {
        if (item.refined_tier) {
            return `Refined to tier ${item.refined_tier}. ${item.refined_category || ""} material of ${rarity} quality.`;
        }
        return `A ${rarity} crafting material.`;
    }
    return `A ${rarity} ${KIND_LABEL[kind]?.toLowerCase() || "item"}.`;
}

function statLine(item) {
    const parts = [];
    if (item.accuracy) parts.push(`ACC +${item.accuracy}`);
    if (item.evasion) parts.push(`EVA +${item.evasion}`);
    if (item.stats) {
        for (const [k, v] of Object.entries(item.stats)) {
            parts.push(`${k.toUpperCase().slice(0, 3)} +${v}`);
        }
    }
    return parts.join(" · ");
}

export default function ItemTooltip({ item, side = "bottom", sideOffset = 4, children, ...rest }) {
    if (!item) return children;

    const name = item.name || item.tool_name || "Unknown";
    const rarity = item.rarity || "common";
    const kind = item.kind || "material";
    const desc = item.desc || autoDesc(item);
    const stats = statLine(item);
    const inst = isInstance(item);
    const instStats = inst ? instanceStatLine(item) : (item.base_stats ? instanceStatLine(item) : "");
    const affixLines = inst ? instanceAffixLines(item) : [];
    const bonusLines = inst ? instanceBonusEffectLines(item) : [];
    const upgradeLines = inst ? instanceUpgradeLines(item) : [];
    const wtypeLabel = item.weapon_type ? (WEAPON_TYPE_LABEL[item.weapon_type] || item.weapon_type) : null;

    return (
        <Tooltip>
            <TooltipTrigger asChild>
                {children}
            </TooltipTrigger>
            <TooltipContent
                side={side}
                sideOffset={sideOffset}
                className="max-w-[280px] bg-popover border border-border text-popover-foreground"
                {...rest}
            >
                <div className={`font-pixel text-xs uppercase mb-1 ${RARITY_TEXT[rarity] || "text-primary"}`}>
                    {name}
                </div>
                <div className="text-[10px] space-y-1">
                    <div className="text-muted-foreground">
                        {RARITY_LABEL[rarity] || rarity} · {KIND_LABEL[kind] || kind}{item.slot && SLOT_LABELS[item.slot] ? ` · ${SLOT_LABELS[item.slot]}` : ""}{item.two_handed ? " · 2H" : ""}{wtypeLabel ? ` · ${wtypeLabel}` : ""}{item.range ? ` · Range ${item.range}` : ""}{inst && item.quality ? ` · Q${item.quality}` : ""}
                    </div>
                    {/* Base stats (instance or base template) */}
                    {instStats && (
                        <div className="text-foreground font-mono">{instStats}</div>
                    )}
                    {/* Procedural instance: affix lines */}
                    {affixLines.map((al, i) => (
                        <div key={`affix-${i}`} className={al.type === "prefix" ? "text-cyan-400" : "text-orange-400"}>
                            {al.label} {al.value}
                        </div>
                    ))}
                    {/* Procedural instance: bonus effects */}
                    {bonusLines.length > 0 && (
                        <div className="text-purple-400">
                            {bonusLines.map((bl, i) => <div key={`be-${i}`}>{bl}</div>)}
                        </div>
                    )}
                    {/* Procedural instance: upgrades (gems/runes) */}
                    {upgradeLines.length > 0 && (
                        <div className="text-amber-400 border-t border-border/50 pt-1">
                            {upgradeLines.map((ul, i) => <div key={`up-${i}`}>{ul}</div>)}
                        </div>
                    )}
                    {/* Legacy stats line */}
                    {!inst && stats && (
                        <div className="text-foreground font-mono">{stats}</div>
                    )}
                    {item.effect && item.effect.heal && (
                        <div className="text-green-400">Heals {item.effect.heal} HP</div>
                    )}
                    {item.effect && item.effect.gold && (
                        <div className="text-amber-400">Contains {item.effect.gold} gold</div>
                    )}
                    {item.effect && item.effect.cure && (
                        <div className="text-green-400">Cures {item.effect.cure}</div>
                    )}
                    {item.effect && item.effect.damage && (
                        <div className="text-destructive">Deals {item.effect.damage} damage</div>
                    )}
                    {item.effect?.restore_mp && (
                        <div className="text-blue-400">Restores {item.effect.restore_mp} MP</div>
                    )}
                    {item.effect?.buff_stat && (
                        <div className="text-purple-400">+{item.effect.buff_stat} {item.stat || ""} (temporary)</div>
                    )}
                    {item.effect?.resist && (
                        <div className="text-cyan-400">+{item.effect.resist} resistance (temporary)</div>
                    )}
                    {item.effect?.hp_regen && (
                        <div className="text-green-400">+{item.effect.hp_regen} HP per turn</div>
                    )}
                    {item.effect?.mp_regen && (
                        <div className="text-blue-400">+{item.effect.mp_regen} MP per turn</div>
                    )}
                    {item.effect?.stamina && (
                        <div className="text-amber-400">+{item.effect.stamina} stamina</div>
                    )}
                    {item.effect?.xp_buff && (
                        <div className="text-primary">+{item.effect.xp_buff}% XP gain</div>
                    )}
                    {item.teaches && (
                        <div className="text-purple-400">Teaches: {item.teaches.replace(/_/g, " ")}</div>
                    )}
                    {item.refined_tier && (
                        <div className="text-muted-foreground">Refinement Tier {item.refined_tier}</div>
                    )}
                    {item.profession && (
                        <div className="text-muted-foreground">{item.profession}</div>
                    )}
                    {item.durability != null && item.max_durability != null && (
                        <div className="text-muted-foreground">
                            Durability: {item.durability}/{item.max_durability}
                        </div>
                    )}
                    {inst && item.req_level && item.req_level > 1 && (
                        <div className="text-muted-foreground">Requires Level {item.req_level}</div>
                    )}
                    {inst && item.req_stats && Object.keys(item.req_stats).length > 0 && (
                        <div className="text-muted-foreground">
                            {Object.entries(item.req_stats).map(([k, v]) => `${STAT_LABELS[k] || k} ${v}`).join(" · ")}
                        </div>
                    )}
                    <div className="text-popover-foreground/80 italic pt-1 border-t border-border/50 mt-1">
                        {desc}
                    </div>
                </div>
            </TooltipContent>
        </Tooltip>
    );
}
