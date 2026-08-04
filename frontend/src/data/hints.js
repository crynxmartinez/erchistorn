// Shared explainer strings used by CharacterSheet tooltips, RacialPanel tooltips,
// and the Journal drawer. Kept plain, punchy, in-fiction where possible.

export const STAT_HINTS = {
    // Main stats
    might:      "Physical damage & melee attacks. +3% Physical Damage per point. Drives every swing of a weapon.",
    grace:      "Accuracy and Evasion. Determines hit chance via advantage levels and reduces incoming hit odds.",
    insight:    "Magical damage & spell effect. +3% Magical Damage per point. Fuels arcane and divine skills.",
    resilience: "Innate toughness. Each point adds +2 Armor, reducing physical damage. Granted by the Guardian role and by defensive masteries as they level.",
    // Life stats
    vitality:   "Maximum Health = 50 + VIT × 10. Resists Bleed, Poison, and Disease. More VIT = harder to kill.",
    cognition:  "Skill Capacity = 2 + COG ÷ 2 (max 8). Determines how many skills you can use per encounter.",
    essence:    "Healing power (+3%/pt), Barrier strength (+3%/pt), Base Magic Resistance (×2), and curse resistance.",
    durability: "Recovery & endurance. Reduces negative status duration by 4%/pt (max 50%). Improves HP regeneration.",
    // Derived
    armor_bonus:"Flat damage reduction on top of your armor's own value.",
    evasion_mod:"Modifier to your evasion chance. Positive = dodgier, negative = clumsier.",
    armor:      "Reduces incoming physical damage. Heavy armor and shields give the most; Resilience adds to it. Caps at 80% reduction.",
    magic_resistance: "Reduces incoming magical damage. Light armor gives the most, and Essence adds ×2. Caps at 80% reduction.",
    // Meters
    hp:         "Health. Reach 0 and you're downed — visit a Sanctuary or use a potion to recover. Racial HP regen restores HP passively over time, even while logged out.",
    xp:         "Experience toward the next level. Each level raises your mastery's signature stats — a Knight grows Might, a Mage grows Insight.",
    gold:       "Currency for markets, inns, fast travel, and trainers.",
};

export const STATUS_HINTS = {
    bleeding:  { desc: "Open wounds drain your vitality with every movement.", effect: "Lose {mag} HP per action", type: "DoT (Physical)" },
    poisoned:  { desc: "Toxin courses through your veins, festering with time.", effect: "Lose {mag} HP per action; gathers may spoil", type: "DoT (Magical)" },
    weary:     { desc: "Fatigue weighs on your limbs, dulling your reflexes.", effect: "Reduced accuracy", type: "Debuff" },
    sick:      { desc: "Illness saps your strength and slows recovery.", effect: "Reduced stats, slower HP recovery", type: "Debuff" },
    cursed:    { desc: "A dark omen clings to your shadow, tilting fortune against you.", effect: "Dice rolls skew worse", type: "Debuff" },
    burning:   { desc: "Flames sear your flesh, consuming you with every heartbeat.", effect: "Lose {mag} HP per action", type: "DoT (Magical)" },
    stunned:   { desc: "A concussive blow leaves you reeling, unable to act.", effect: "Skip your next action", type: "Control" },
    shaken:    { desc: "Recent trauma frays your nerves, throwing off your aim.", effect: "Reduced accuracy", type: "Debuff" },
    blinded:   { desc: "Your vision swims with dark spots and flashes of light.", effect: "Hits frequently miss", type: "Debuff" },
    ensnared:  { desc: "Vines, webs, or bonds grip your legs — you cannot flee.", effect: "Cannot flee or travel", type: "Control" },
    blessed:   { desc: "Divine favor rests upon you, steadying your hand and heart.", effect: "+{mag} to dice rolls", type: "Buff" },
    focused:   { desc: "Your mind is sharp, your body responsive, your aim true.", effect: "+{mag} accuracy and skill effectiveness", type: "Buff" },
    warded:    { desc: "A shimmering barrier deflects the worst of incoming magic.", effect: "Reduced incoming magic damage", type: "Buff" },
    hidden:    { desc: "You blend into the terrain, invisible to hostile eyes.", effect: "Enemies cannot detect you", type: "Buff" },
    evasive:   { desc: "Your footing is light, your movements unpredictable.", effect: "+{mag} evasion chance", type: "Buff" },
    recovering: { desc: "You woke from death's door in the Sanctuary — your body is still mending.", effect: "-10% damage for {dur} actions", type: "Debuff" },
    sanctuary_blessing: { desc: "The Sanctuary's sacred oil anoints your brow, sharpening your growth.", effect: "+5% XP gain for {dur} actions", type: "Buff" },
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

export const PROFESSION_HINT = "Professions are independent of race, role and mastery. You may know up to three at a time; slots unlock at level 1, 10 and 25. Tools wear down with use and must be repaired or replaced.";

export const EXPLORATION_HINT = "Each biome has 0-100% exploration. Hit 25% to unlock common gathering areas, 50% for NPCs/monsters, 75% for rare nodes, and 100% for map rewards and hidden lore.";

export const NODE_HINT = "Resource nodes have Common, Uncommon, Rare and Legendary tiers. Higher tiers require the right profession rank, a durable tool, and may enter cooldown after use.";

export const CONTINENT_BONUS_HINT = "Every continent grants activity bonuses to any character working there. The bonus is tied to the land, not the native race, though natives begin with friendlier reputation.";

export const REPUTATION_HINT = "Reputation improves by helping each continent: quests, kills, gathering, and exploration. Higher reputation unlocks recipes, vendors, reduced teleporter fees, and hidden biomes.";
