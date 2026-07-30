export const HERITAGE_LABEL = {
    human: "Sacred Oath",
    elf: "Sun & Moon",
    dwarf: "Mountain Resilience",
    half_elf: "Dual Heritage",
    orc: "Blood of Liberated",
    wildblood: "Beast Aspect",
    hyliondrian: "Children of Sea",
    sylvan: "Shrink",
};

export const HERITAGE_RANK_LEVEL_REQS = [10, 20, 30, 40];
export const HERITAGE_RANK_MULT = [1.0, 1.25, 1.5, 1.75, 2.0];
export const MAX_HERITAGE_RANK = 5;

export const HERITAGE_SURGE_RANK_CONFIG = [
    { duration: 3, cooldown_hours: 24 },
    { duration: 4, cooldown_hours: 18 },
    { duration: 5, cooldown_hours: 12 },
    { duration: 5, cooldown_hours: 8 },
];

export const HERITAGE_SURGES = {
    human:       { id: "oathbreaker_resolve",   name: "Oathbreaker's Resolve",   desc: "All actions count as critical success for the surge duration." },
    elf:         { id: "celestial_conjunction", name: "Celestial Conjunction",   desc: "Both solar and lunar bonuses active at once: +6 strike, -30% damage taken, +10% heal." },
    dwarf:       { id: "mountain_wrath",        name: "Mountain's Wrath",        desc: "Take 50% less damage, immune to debuffs, and repair armor 10% per action." },
    half_elf:    { id: "dual_awakening",        name: "Dual Awakening",          desc: "Both heritages fully active: full elf + full human bonuses, +2 to all racial resources." },
    orc:         { id: "unchained_fury",        name: "Unchained Fury",          desc: "+10 strike, immune to control/fear, every hit deals double damage." },
    wildblood:   { id: "primal_overdrive",      name: "Primal Overdrive",        desc: "+8 strike, +15% evasion, 25% lifesteal for the surge duration." },
    hyliondrian: { id: "tidal_cataclysm",       name: "Tidal Cataclysm",         desc: "Instantly heal 50% HP, then +10% heal per action, immune to debuffs." },
    sylvan:      { id: "verdant_bloom",         name: "Verdant Bloom",           desc: "+20% evasion, +30% stealth, gather yields 3x materials, immune to detection." },
};
