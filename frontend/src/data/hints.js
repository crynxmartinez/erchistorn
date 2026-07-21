// Shared explainer strings used by CharacterSheet tooltips, RacialPanel tooltips,
// and the Journal drawer. Kept plain, punchy, in-fiction where possible.

export const STAT_HINTS = {
    // Main stats
    might:      "Physical damage & melee attacks. Drives every swing of a weapon.",
    grace:      "Accuracy, dodge, and ranged aim. Tips dice rolls toward hits and evasion.",
    insight:    "Magical damage & spell effect. Fuels arcane and divine skills.",
    // Life stats
    vitality:   "Base HP pool and physical resilience. More VIT = harder to kill.",
    cognition:  "Mana pool, skill slots, and lore checks. Higher COG = more casts before running dry.",
    essence:    "Racial resource cap (Oath / Inner Blood / Tide, etc.). Powers your bloodline abilities.",
    drive:      "Endurance & recovery. Reduces status-effect duration and speeds Inn rest.",
    // Derived
    armor_bonus:"Flat damage reduction on top of your armor's own value.",
    evasion_mod:"Modifier to your evasion chance. Positive = dodgier, negative = clumsier.",
    // Meters
    hp:         "Health. Reach 0 and you're downed — visit an Inn or use a potion to recover.",
    xp:         "Experience toward the next level. Every level nudges every stat up.",
    gold:       "Currency for markets, inns, fast travel, and trainers.",
};

export const STATUS_HINTS = {
    bleeding: "Bleeding — lose HP each action until it wears off.",
    poisoned: "Poisoned — lose HP each action and your gathers can spoil.",
    weary:    "Weary — reduced accuracy for a couple of turns; NOT the same as the Exhaustion meter.",
    sick:     "Sick — reduced stats and slower recovery until it clears.",
    cursed:   "Cursed — dice rolls skew slightly worse until removed by a priest.",
    burning:  "Burning — heavy per-turn HP loss.",
    stunned:  "Stunned — you skip your next action.",
    shaken:   "Shaken — reduced accuracy from recent trauma.",
    blinded:  "Blinded — hits often miss until vision returns.",
    ensnared: "Ensnared — you can't flee or move biomes.",
    blessed:  "Blessed — small bonus to your rolls.",
    focused:  "Focused — improved accuracy and skill effects.",
    warded:   "Warded — reduced incoming magic damage.",
    hidden:   "Hidden — enemies can't detect you next action.",
    evasive:  "Evasive — extra evasion chance for a few turns.",
};

export const EXHAUSTION_HINT = "Exhaustion (numeric resource, 0–100). Rises as you push through actions; NOT the 'Weary' status. Wildbloods weaponise it via Inner Blood; Orcs at high exhaust see Defiance spike.";
export const RESOLVE_HINT    = "Resolve (0–100). Mental steel — buffers against fear and rout effects. Drops on grim outcomes, recovers slowly with rest.";

export const RESOURCE_META = {
    oath_progress:    { label: "Oath Progress",    max: 100, hint: "Fulfilling your Sacred Oath fills this meter. At 100 you awaken a Human ability." },
    celestial_charge: { label: "Celestial Charge", max: 5,   hint: "Charges gained by acting under the right sky (☀ Solar / ☾ Lunar). Spend on Elven arts." },
    stoneguard:       { label: "Stoneguard",       max: 5,   hint: "Dwarven grit — earned in successful stands, spent to shrug off a hit." },
    harmony:          { label: "Harmony",          max: 5,   hint: "Half-Elf's balance between two heritages. Peak Harmony unlocks the awakened hybrid gift." },
    defiance:         { label: "Defiance",         max: 100, hint: "Orc rage from broken chains. Grows on hardship, spent on furious counter-strikes." },
    inner_blood:      { label: "Inner Blood",      max: 100, hint: "Wildblood beast-fury. Rises with Exhaustion, unleashed in a single savage turn." },
    tide:             { label: "Tide",             max: 5,   hint: "Hyliondrian sea-charge. Full pool = your Marine Adaptation triggers next action." },
    verdant_essence:  { label: "Verdant Essence",  max: 5,   hint: "Sylvan grove-bond. Roots you to a biome and heals over time when full." },
};

export const RACE_TO_RESOURCE = {
    human: "oath_progress",
    elf: "celestial_charge",
    dwarf: "stoneguard",
    half_elf: "harmony",
    orc: "defiance",
    wildblood: "inner_blood",
    hyliondrian: "tide",
    sylvan: "verdant_essence",
};
