"""Static game data — races, roles, masteries, continents, biomes, monsters,
materials, items, skills, recipes, portraits."""
from __future__ import annotations


# ============================================================
# RACES — from Erchis Lore
# ============================================================
RACES: list[dict] = [
    {
        "id": "human",
        "name": "Human",
        "title": "The Diverse Civilization of the Human Empire",
        "starting_stats": {"vitality": 4, "cognition": 3, "essence": 3, "durability": 5},
        "hp_regen_per_min": 1,
        "perk": {"id": "sacred_oath", "name": "Sacred Oath",
                 "desc": "Fulfil your oath in the world of Erchis to regain Durability and gain milestone rewards."},
        "gifts": [
            {"id": "oathbound", "name": "Oathbound", "desc": "+1 Durability from a life of kept promises.", "bonus": {"durability": 1}},
            {"id": "diplomat", "name": "Silver Tongue", "desc": "+1 Cognition from courtly training.", "bonus": {"cognition": 1}},
        ],
        "story": "Within the sprawling Human Empire of Erchis, a person's word is considered sacred. Legends say a ruler's promise could rally armies, forge alliances, and shape destiny itself. Their greatest magic is a promise kept.",
        "roles": ["fighter", "guardian", "scout", "scholar", "healer"],
        "masteries": ["knight", "paladin", "lancer", "rogue", "bard", "alchemist"],
        "portrait_seeds": ["Aldric", "Selene", "Corvus", "Isolde", "Roland"],
    },
    {
        "id": "elf",
        "name": "Elf",
        "title": "The Higher Enclave of Haya",
        "starting_stats": {"vitality": 3, "cognition": 4, "essence": 5, "durability": 5},
        "hp_regen_per_min": 0.5,
        "perk": {"id": "children_of_sun_moon", "name": "Children of the Sun and Moon",
                 "desc": "By day, +3 healing received. By night, +3 evasion and +3 attack success."},
        "gifts": [
            {"id": "sunwarden", "name": "Sunwarden", "desc": "+1 Essence from sun-forged discipline.", "bonus": {"essence": 1}},
            {"id": "moonchild", "name": "Moonchild", "desc": "+1 Cognition from lunar meditation.", "bonus": {"cognition": 1}},
        ],
        "story": "Once bound to the Great Tree of Haya, the Elves now walk beneath the light of the sun and the glow of the moon. Sun-forged armour, moon-touched weapons — rebirth through adaptation.",
        "roles": ["scholar", "healer", "scout"],
        "masteries": ["mage", "priest", "druid", "assassin", "hunter", "paladin"],
        "portrait_seeds": ["Aelindra", "Thaelor", "Sylwen", "Erevan", "Naeris"],
    },
    {
        "id": "dwarf",
        "name": "Dwarf",
        "title": "The Dwarves of the Undermountain Realm",
        "starting_stats": {"vitality": 5, "cognition": 3, "essence": 2, "durability": 6},
        "hp_regen_per_min": 2,
        "perk": {"id": "mountain_resilience", "name": "Mountain Resilience",
                 "desc": "Each point of Resilience also directly increases Vitality (bonus HP)."},
        "gifts": [
            {"id": "stoneheart", "name": "Stoneheart", "desc": "+1 Vitality from living stone.", "bonus": {"vitality": 1}},
            {"id": "forgeborn", "name": "Forgeborn", "desc": "+1 Durability from anvil and flame.", "bonus": {"durability": 1}},
        ],
        "story": "Forged of stone and endurance, the Dwarves carved mighty halls beneath the mountains. Masters of forge, drink, and defence — masters of Jahra, a metal light as breath yet strong as fate.",
        "roles": ["fighter", "guardian"],
        # `alchemist` was listed here but is unreachable: Alchemist requires the
        # scholar or healer role (ROLE_AVAILABLE_MASTERIES) and Dwarves can only be
        # fighter or guardian, so the combo could never be created. Removed rather
        # than widened — giving Dwarves the scholar role would also unlock mage,
        # druid and bard for them, which is a much larger change than fixing this.
        # To restore it, add a role to this race or add alchemist to fighter/guardian.
        "masteries": ["knight", "paladin", "lancer"],
        "portrait_seeds": ["Borin", "Thora", "Durgin", "Helga", "Krogan"],
    },
    {
        "id": "half_elf",
        "name": "Half-Elf",
        "title": "The Half-Elf Diplomatic Federation",
        "starting_stats": {"vitality": 3, "cognition": 4, "essence": 4, "durability": 7},
        "hp_regen_per_min": 1,
        "perk": {"id": "dual_heritage", "name": "Dual Heritage",
                 "desc": "Choose one heritage — Human (Sacred Oath) or Elven (Children of Sun and Moon)."},
        "gifts": [
            {"id": "human_legacy", "name": "Human Legacy", "desc": "+1 Durability from your human parent.", "bonus": {"durability": 1}},
            {"id": "elven_legacy", "name": "Elven Legacy", "desc": "+1 Essence from your elven blood.", "bonus": {"essence": 1}},
        ],
        "story": "Rejected once, celebrated now. Born between worlds, Half-Elves forged a federation where blood matters less than deed. Diplomats, mediators, bridge-walkers.",
        "roles": ["scout", "scholar", "healer", "guardian", "fighter"],
        "masteries": ["bard", "rogue", "paladin", "mage", "priest", "knight"],
        "portrait_seeds": ["Kaelira", "Varric", "Ambrose", "Lyriel", "Serath"],
    },
    {
        "id": "orc",
        "name": "Orc",
        "title": "The Military Force of the Orc Dominion",
        "starting_stats": {"vitality": 5, "cognition": 2, "essence": 3, "durability": 6},
        "hp_regen_per_min": 2,
        "perk": {"id": "blood_of_liberated", "name": "Blood of the Liberated",
                 "desc": "When attacking while Exhausted, roll 1d3 and restore that much HP (once per fight)."},
        "gifts": [
            {"id": "liberator", "name": "Liberator's Might", "desc": "+1 Might from broken chains.", "bonus": {"might": 1}},
            {"id": "iron_will", "name": "Iron Will", "desc": "+1 Durability from surviving the crucible.", "bonus": {"durability": 1}},
        ],
        "story": "Chained by demon lords for centuries, the Orcs broke free under Zaheer al-Orc the Liberator. They now guard freedom itself — not conquerors, but liberators armoured in the memory of chains.",
        "roles": ["fighter", "guardian"],
        # `hunter` (needs scout) and `alchemist` (needs scholar/healer) were both
        # unreachable for Orcs, who can only be fighter or guardian. Same reasoning
        # as the Dwarf entry above — removed rather than widened.
        "masteries": ["knight", "paladin", "lancer"],
        "portrait_seeds": ["Zaheer", "Grosh", "Mora", "Karnak", "Ulga"],
    },
    {
        "id": "wildblood",
        "name": "Wildblood",
        "title": "The Primal Sovereignty of Wildblood",
        "starting_stats": {"vitality": 4, "cognition": 3, "essence": 4, "durability": 4},
        "hp_regen_per_min": 1.5,
        "perk": {"id": "inner_blood", "name": "Inner Blood",
                 "desc": "Each Exhaust point grants Inner Blood. At 5 Inner Blood, enter The Zone (buffed state)."},
        "gifts": [
            {"id": "feral_might", "name": "Feral Might", "desc": "+1 Might from the predator's path.", "bonus": {"might": 1}},
            {"id": "primal_resilience", "name": "Primal Resilience", "desc": "+1 Vitality from the guardian's path.", "bonus": {"vitality": 1}},
        ],
        "story": "Children of Rindivar. Bearing fangs, tails, feathers, or scales — they turned barren Gennel into a living forest. Their strength grows from the bonds they protect.",
        "roles": ["fighter", "guardian", "scout", "healer"],
        "masteries": ["druid", "hunter", "lancer", "assassin", "knight", "bard"],
        "portrait_seeds": ["Fenros", "Talia", "Vaska", "Rhun", "Sable"],
    },
    {
        "id": "hyliondrian",
        "name": "Hyliondrian",
        "title": "The Underwater Kingdom of the Hyliondrians",
        "starting_stats": {"vitality": 3, "cognition": 4, "essence": 5, "durability": 6},
        "hp_regen_per_min": 1,
        "perk": {"id": "children_of_sea", "name": "Children of the Sea",
                 "desc": "Breathe underwater freely. Movement in water increases by your Grace."},
        "gifts": [
            {"id": "tide_touched", "name": "Tide-Touched", "desc": "+1 Essence from the deep currents.", "bonus": {"essence": 1}},
            {"id": "coral_blessed", "name": "Coral-Blessed", "desc": "+1 Durability from coral-hard scales.", "bonus": {"durability": 1}},
        ],
        "story": "From Atlantyrion beneath the waves, the Hyliondrians guard the Orb of Hyliondrias — treasure of the gods. Tide Mothers, coral cities, prophecies old as tide.",
        "roles": ["scholar", "healer", "scout"],
        "masteries": ["mage", "priest", "druid", "hunter", "lancer", "paladin"],
        "portrait_seeds": ["Nerith", "Coralia", "Thalos", "Vaela", "Murrin"],
    },
    {
        "id": "sylvan",
        "name": "Sylvan",
        "title": "The Sylvans of Daw'ul Talalu",
        "starting_stats": {"vitality": 2, "cognition": 5, "essence": 4, "durability": 5},
        "hp_regen_per_min": 0.5,
        "perk": {"id": "shrink", "name": "Shrink",
                 "desc": "Reduce your body to a tiny form: +5 Evasion but -5 Strike. Toggle with an action."},
        "gifts": [
            {"id": "tiny_blessing", "name": "Tiny Blessing", "desc": "+1 Grace from small and nimble form.", "bonus": {"grace": 1}},
            {"id": "forest_whisper", "name": "Forest Whisper", "desc": "+1 Cognition from the old wood.", "bonus": {"cognition": 1}},
        ],
        "story": "The Mystleaf of the hidden forest. Their homes grow from living wood; their songs carry natural enchantment. Gentle, but never underestimated — they woke the forest against invaders.",
        "roles": ["scholar", "scout", "healer"],
        "masteries": ["mage", "druid", "priest", "hunter", "assassin", "rogue", "bard"],
        "portrait_seeds": ["Ilvyria", "Faenor", "Whisper", "Sylas", "Mirielle"],
    },
]


# ============================================================
# ROLES
# ============================================================
ROLES: list[dict] = [
    {"id": "fighter", "name": "Fighter", "desc": "Front-line combatant. +2 Vitality, +1 Strike in combat.",
     "bonus": {"vitality": 2}, "combat_bonus": 1},
    {"id": "guardian", "name": "Guardian", "desc": "Defender and protector. +2 Resilience, +1 defence rolls.",
     "bonus": {"resilience": 2}, "defense_bonus": 1},
    {"id": "scout", "name": "Scout", "desc": "Trailblazer and hunter. +2 Grace, +1 gather/hunt rolls.",
     "bonus": {"grace": 2}, "gather_bonus": 1, "hunt_bonus": 1},
    {"id": "scholar", "name": "Scholar", "desc": "Seeker of arcane and lost knowledge. +2 Cognition, +1 to craft rolls.",
     "bonus": {"cognition": 2}, "craft_bonus": 1},
    {"id": "healer", "name": "Healer", "desc": "Mender of body and spirit. +2 Essence, gain Mend skill at creation.",
     "bonus": {"essence": 2}, "starting_skills": ["mend"]},
]


# ============================================================
# MASTERIES
# ============================================================
MASTERIES: list[dict] = [
    {"id": "knight",    "name": "Knight",    "desc": "The Oathbound — heavy armor frontline warrior who commits to a sacred Oath before battle, growing stronger each turn they hold it.", "starting_skills": ["shield_bash", "iron_stance"]},
    {"id": "paladin",   "name": "Paladin",   "desc": "Holy warrior of oath and light — divine tank whose power grows as HP falls.", "starting_skills": ["shield_of_faith", "blessed_strike"]},
    {"id": "lancer",    "name": "Lancer",    "desc": "The Elemental Lance Master — imbues their lance with elemental buffs, each changing what their strikes do.", "starting_skills": ["thrust", "flame_imbue"]},
    {"id": "rogue",     "name": "Rogue",     "desc": "The Adaptive Trickster — a cunning combatant who customizes their passive kit through innate skills, fighting dirty with misdirection, traps, and counter-attacks.",  "starting_skills": ["dirty_trick", "hidden_blade"]},
    {"id": "bard",      "name": "Bard",      "desc": "The Master of Control — a performer who commands the battlefield through Song and Dance. In Song mode, the Bard changes the rules for allies. In Dance mode, the Bard controls enemy behavior.",  "starting_skills": ["song_of_heroes", "mocking_verse"]},
    {"id": "alchemist", "name": "Alchemist", "desc": "The Transmuter — a close-range katar fighter who imbues skills onto their blade and adapts through Combo Flow.", "starting_skills": ["acid_bomb", "quick_jab"]},
    {"id": "mage",      "name": "Mage",      "desc": "Arcane fire, arcane truth, arcane cost.",            "starting_skills": ["arcane_bolt", "ward"]},
    {"id": "priest",    "name": "Priest",    "desc": "Voice of the gods, hand of mercy.",                  "starting_skills": ["divine_light", "purge"]},
    {"id": "druid",     "name": "Druid",     "desc": "The wild answers when called.",                      "starting_skills": ["thornlash", "beast_call"]},
    {"id": "assassin",  "name": "Assassin",  "desc": "The Shadow Reaper — a burst-damage glass cannon who accumulates shadows through kills and combat, then unleashes them in a devastating BURST at 100.", "starting_skills": ["shadow_strike", "smoke_veil"]},
    {"id": "hunter",    "name": "Hunter",    "desc": "The Master of Precision — a ranged killer who grows deadlier with every arrow. Spirit Guidance builds with each hit, transforming skills at stack 10. It's not the first shot that kills you. It's the tenth.", "starting_skills": ["rapid_shot", "camouflage"]},
]


# ============================================================
# STARTER GEAR BY MASTERY
# ============================================================
# Each mastery gets a weapon, shield (if applicable), and armor set.
# req_stats are bypassed for starter gear (gifted at character creation).
STARTER_GEAR_BY_MASTERY: dict[str, dict] = {
    "knight": {
        "weapon": "iron_longsword",
        "shield": "bone_shield",
        "armor": ["iron_helm", "iron_chainmail", "iron_greaves", "ironshod_boots"],
    },
    "paladin": {
        "weapon": "iron_longsword",
        "shield": "bone_shield",
        "armor": ["iron_helm", "iron_chainmail", "iron_greaves", "ironshod_boots"],
    },
    "lancer": {
        "weapon": "iron_spear",
        "shield": None,
        "armor": ["leather_cap", "leather_vest", "leather_leggings", "leather_boots"],
    },
    "rogue": {
        "weapon": "iron_dagger",
        "shield": None,
        "armor": ["leather_cap", "leather_vest", "leather_leggings", "leather_boots"],
    },
    "assassin": {
        "weapon": "iron_dagger",
        "shield": None,
        "armor": ["leather_cap", "leather_vest", "leather_leggings", "leather_boots"],
    },
    "hunter": {
        "weapon": "oak_shortbow",
        "shield": None,
        "armor": ["leather_cap", "leather_vest", "leather_leggings", "leather_boots"],
    },
    "bard": {
        "weapon": "travelers_lute",
        "shield": None,
        "armor": ["leather_cap", "leather_vest", "leather_leggings", "leather_boots"],
    },
    "alchemist": {
        "weapon": "iron_katar",
        "shield": None,
        "armor": ["leather_cap", "leather_vest", "leather_leggings", "leather_boots"],
    },
    "mage": {
        "weapon": "apprentice_tome",
        "shield": None,
        "armor": ["sages_hood", "sages_robe", "sages_trousers", "sages_sandals"],
    },
    "priest": {
        "weapon": "moonstone_orb",
        "shield": None,
        "armor": ["sages_hood", "sages_robe", "sages_trousers", "sages_sandals"],
    },
    "druid": {
        "weapon": "moonstone_orb",
        "shield": None,
        "armor": ["sages_hood", "sages_robe", "sages_trousers", "sages_sandals"],
    },
}


# ============================================================
# ROGUE INNATE SKILLS — 10 passives/reactions, 5 equip slots
# ============================================================
ROGUE_INNATE_SKILLS: list[dict] = [
    {"id": "quick_hands",    "name": "Quick Hands",    "type": "action",    "desc": "The Rogue acts first every turn — the player phase happens before the enemy phase. Always."},
    {"id": "counter_strike", "name": "Counter Strike", "type": "reaction",  "desc": "When the enemy's dice roll is 3 or less (miss/glancing/partial), the Rogue automatically counter-attacks for free damage (0.5x weapon damage)."},
    {"id": "dirty_fighter",  "name": "Dirty Fighter",  "type": "passive",   "desc": "All strikes apply a random debuff (shaken, bleeding, or blinded)."},
    {"id": "light_feet",     "name": "Light Feet",     "type": "passive",   "desc": "Immune to ensnared. The Rogue cannot be trapped or immobilized."},
    {"id": "opportunist",    "name": "Opportunist",    "type": "passive",   "desc": "+30% damage against enemies with any status effect."},
    {"id": "slippery",       "name": "Slippery",       "type": "reaction",  "desc": "25% chance to shake off any debuff each turn."},
    {"id": "trap_master",    "name": "Trap Master",    "type": "passive",   "desc": "The first strike each combat applies ensnared."},
    {"id": "second_story",   "name": "Second Story",   "type": "passive",   "desc": "+5 permanent grace. The Rogue is naturally agile."},
    {"id": "con_artist",     "name": "Con Artist",     "type": "passive",   "desc": "All debuffs applied by the Rogue last +1 turn longer."},
    {"id": "lucky_dodger",   "name": "Lucky Dodger",   "type": "passive",   "desc": "Each time the enemy misses, gain +5% evasion (stacking, resets when hit)."},
]

ROGUE_PASSIVES: list[dict] = [
    {"id": "tricksters_eye",    "name": "Trickster's Eye",    "level": 10, "desc": "+1 innate skill slot (6 total instead of 5)."},
    {"id": "quick_learner",     "name": "Quick Learner",     "level": 20, "desc": "Learn skills 25% faster from trainers."},
    {"id": "adaptive",          "name": "Adaptive",          "level": 30, "desc": "Swap innate skills during combat (once per fight)."},
    {"id": "dirty_mastery",     "name": "Dirty Mastery",     "level": 40, "desc": "Dirty Fighter innate now applies 2 debuffs instead of 1."},
    {"id": "counter_precision", "name": "Counter Precision", "level": 50, "desc": "Counter Strike innate now triggers on enemy roll <=4 and deals 0.75x weapon damage."},
    {"id": "evasion_training",  "name": "Evasion Training",  "level": 60, "desc": "Lucky Dodger innate stacks to +10% per miss instead of +5%."},
    {"id": "trap_specialist",   "name": "Trap Specialist",   "level": 70, "desc": "Trap Master innate applies ensnared on first 2 strikes each combat."},
    {"id": "con_master",        "name": "Con Master",        "level": 80, "desc": "Con Artist innate now makes debuffs last +2 turns instead of +1."},
    {"id": "slippery_soul",     "name": "Slippery Soul",     "level": 90, "desc": "Slippery innate now has 50% chance to shake debuffs each turn."},
    {"id": "master_of_tricks",  "name": "Master of Tricks",  "level": 100, "desc": "+1 innate skill slot (7 total). All innate effects doubled."},
]


# ============================================================
# ASSASSIN PASSIVES — 10 Auto-Learned
# ============================================================
ASSASSIN_PASSIVES: list[dict] = [
    {"id": "shadow_born",         "name": "Shadow Born",         "level": 10,  "desc": "Start every combat with 10 shadows. Night: start with 20."},
    {"id": "shadow_harvest",      "name": "Shadow Harvest",      "level": 20,  "desc": "Each kill grants +5 bonus shadows (total +15 per kill)."},
    {"id": "shadow_precision",    "name": "Shadow Precision",    "level": 30,  "desc": "Shadows now also increase accuracy: +1% accuracy per 10 shadows."},
    {"id": "shadow_crit",         "name": "Shadow Crit",         "level": 40,  "desc": "Shadows now also increase crit damage: +10% at 50+, +20% at 75+."},
    {"id": "fear_mastery",        "name": "Fear Mastery",        "level": 50,  "desc": "Fear deposits are 50% stronger — each shadow reduces enemy stats by 1.5 instead of 1."},
    {"id": "shadow_step",         "name": "Shadow Step",         "level": 60,  "desc": "After a kill, 50% chance to re-enter hidden. Night: 75% chance."},
    {"id": "night_child",         "name": "Night Child",         "level": 70,  "desc": "During night, all shadow threshold effects doubled. Passive shadow gen increased to +5/turn."},
    {"id": "shadow_convergence",  "name": "Shadow Convergence",  "level": 80,  "desc": "At 75+ shadows, all strikes apply shaken (fear). Fear deposits cost no shadows."},
    {"id": "eclipse_mastery",     "name": "Eclipse Mastery",     "level": 90,  "desc": "BURST at 100 shadows now deals 4x damage instead of 3x. After BURST, retain 25 shadows instead of resetting to 0."},
    {"id": "avatar_of_shadow",    "name": "Avatar of Shadow",    "level": 100, "desc": "Always at minimum 50 shadows. BURST threshold lowered to 75. Night: always at 75 shadows. Stealth breaks grant 75% evasion for 1 turn. Stealth skill cooldowns reduced by 50%."},
]


# ============================================================
# BARD PASSIVES — 10 Auto-Learned + 1 Legendary Quest Passive
# ============================================================
BARD_PASSIVES: list[dict] = [
    {"id": "tuned_ear",          "name": "Tuned Ear",          "level": 10,  "desc": "Performance effect chance +10%."},
    {"id": "steady_rhythm",      "name": "Steady Rhythm",      "level": 20,  "desc": "Crescendo builds +1 extra per turn (2 stacks/turn)."},
    {"id": "charismatic",        "name": "Charismatic",        "level": 30,  "desc": "+10 permanent grace (innate, always active)."},
    {"id": "harmonic",           "name": "Harmonic",           "level": 40,  "desc": "Encore chance +15% (base 20% -> 35%)."},
    {"id": "resonant",           "name": "Resonant",           "level": 50,  "desc": "Crescendo max increased to 7."},
    {"id": "free_reprise",       "name": "Free Reprise",       "level": 60,  "desc": "Switching modes keeps 50% of Crescendo instead of resetting to 0."},
    {"id": "crowd_pleaser",      "name": "Crowd Pleaser",      "level": 70,  "desc": "Audience appears faster — visual Crescendo at +1 stack."},
    {"id": "unbreakable_voice",  "name": "Unbreakable Voice",  "level": 80,  "desc": "Crescendo no longer resets when stunned (only when silenced)."},
    {"id": "masterful_encore",   "name": "Masterful Encore",   "level": 90,  "desc": "Encore chance +30% (total 65%). Encore lasts 2 turns instead of 1."},
    {"id": "legend_of_the_stage","name": "Legend of the Stage","level": 100, "desc": "Crescendo max 10. Encore guaranteed at max Crescendo. Mode switch is instant and unlimited. Performances cannot be silenced."},
    {"id": "voice_of_the_world", "name": "Voice of the World", "level": 100, "desc": "Legendary passive. Song + Dance active simultaneously.", "quest": True},
]


# ============================================================
# DRUID PASSIVES — 12 Auto-Learned (every 10 levels, every 5 at endgame)
# ============================================================
DRUID_PASSIVES: list[dict] = [
    {"id": "wild_heart",       "name": "Wild Heart",       "level": 10,  "desc": "Unlocks the Tame button. +5% tame success chance on normal creatures."},
    {"id": "pack_leader",      "name": "Pack Leader",      "level": 20,  "desc": "+1 max active summon above the level-based cap. The pack grows."},
    {"id": "bonded_senses",    "name": "Bonded Senses",    "level": 30,  "desc": "While a summon is active, the Druid also gains the summon's Attack skill as a passive rider (weaker version — no status apply, just damage)."},
    {"id": "fusion_adept",     "name": "Fusion Adept",      "level": 40,  "desc": "Fusion duration extended to 4 turns. Recovery reduced to 1 turn."},
    {"id": "apex_tamer",       "name": "Apex Tamer",       "level": 50,  "desc": "Unlocks taming mini-boss creatures. +10% tame success chance on all creatures."},
    {"id": "twin_fusion",      "name": "Twin Fusion",      "level": 60,  "desc": "Can fuse with 2 summons simultaneously. Both creatures' stats, attack riders, defense passives, and signature abilities stack."},
    {"id": "sovereigns_will",  "name": "Sovereign's Will",  "level": 70,  "desc": "Pack Synergy thresholds reduced: 2+ = Pack Bond, 4+ = Pack Hunt, 6+ = Pack Alpha, 9+ = The Wild Sovereign."},
    {"id": "eternal_bond",     "name": "Eternal Bond",     "level": 80,  "desc": "Summons that die in combat can be re-summoned same combat (1 turn cooldown instead of next combat)."},
    {"id": "mythic_tamer",     "name": "Mythic Tamer",     "level": 85,  "desc": "Unlocks taming boss creatures. +15% tame success chance on boss+ creatures."},
    {"id": "wild_sovereign",   "name": "Wild Sovereign",   "level": 90,  "desc": "All Pack Synergy bonuses doubled. Pack Bond = +40% damage, +10% stats. Pack Hunt = +2 hits, +20% stats. Pack Alpha = extra action every turn. Wild Sovereign = double-shared buffs, +40% stats."},
    {"id": "eternal_wild",     "name": "Eternal Wild",     "level": 95,  "desc": "Fusion has no recovery time. The Druid can fuse, unfuse, and re-fuse freely. Multi-Fusion can be re-entered immediately after ending."},
    {"id": "alpha_world",     "name": "Alpha World",      "level": 100, "desc": "Max active summons cap removed (still 1 per 5 levels — 20 summons at level 100). The Druid is the wild."},
]


# ============================================================
# HUNTER PASSIVES — 10 Auto-Learned + 1 Legendary Quest Passive
# ============================================================
HUNTER_PASSIVES: list[dict] = [
    {"id": "keen_eye",          "name": "Keen Eye",          "level": 10,  "desc": "Spirit Guidance +7% per hit instead of +5%. Communion: +12% per hit instead of +7%."},
    {"id": "quick_draw",        "name": "Quick Draw",        "level": 20,  "desc": "+1 starting Range from weapon. Communion: +2 starting Range from weapon."},
    {"id": "spirit_touched",    "name": "Spirit Touched",    "level": 30,  "desc": "+10 permanent grace. Communion: +10 permanent cognition (both active)."},
    {"id": "trap_master",       "name": "Trap Master",       "level": 40,  "desc": "Thrown traps affect all enemies, not just one. Communion: Traps also apply +1 Spirit Guidance stack per enemy hit."},
    {"id": "eagle_vision",      "name": "Eagle Vision",       "level": 50,  "desc": "Crit damage +25% baseline. Communion: Crit damage +50% baseline."},
    {"id": "ghost_step",        "name": "Ghost Step",        "level": 60,  "desc": "Spirit Walk also grants +2 Range when used. Communion: Spirit Walk grants intangible for 2 turns (no communion needed)."},
    {"id": "ancestors_voice",   "name": "Ancestor's Voice",  "level": 70,  "desc": "Spirit Communion triggers at stack 8 instead of 10. Communion: also instantly grants +2 stacks (starts at 12)."},
    {"id": "unbreakable_focus", "name": "Unbreakable Focus", "level": 80,  "desc": "Spirit Guidance doesn't reset when stunned. Communion: Spirit Guidance doesn't reset when silenced either."},
    {"id": "master_marksman",   "name": "Master Marksman",   "level": 90,  "desc": "Multi-hit skills gain +1 hit. Communion: Multi-hit skills gain +2 hits."},
    {"id": "legend_of_the_hunt", "name": "Legend of the Hunt","level": 100, "desc": "Spirit Guidance has no cap. +2 starting Range from weapon. Ambush grants 2 guaranteed crits. Communion triggers at stack 6. Crit damage +200% at communion."},
    {"id": "spirit_of_the_wild","name": "Spirit of the Wild","level": 100, "quest": True, "desc": "Legendary passive. Spirit Copy is permanent (always active, fights alongside you). The ancestor is always there. Communion: Spirit Copy also casts Spirit Bind every 3 turns automatically."},
]


# ============================================================
# KNIGHT PASSIVES — 10 Auto-Learned (every 10 levels)
# ============================================================
KNIGHT_PASSIVES: list[dict] = [
    {"id": "oath_sworn",       "name": "Oath Sworn",       "level": 10,  "desc": "Start every combat with 2 Oath stacks instead of 0."},
    {"id": "extended_vow",     "name": "Extended Vow",     "level": 20,  "desc": "Each stack-gain event gives +1 extra stack (stacks build twice as fast)."},
    {"id": "battle_hardened",  "name": "Battle Hardened",  "level": 30,  "desc": "+10 permanent armor_bonus (innate, always active)."},
    {"id": "adrenal_surge",    "name": "Adrenal Surge",    "level": 40,  "desc": "When HP drops below 50%, gain might +15 for 3 turns (once per combat)."},
    {"id": "iron_will",        "name": "Iron Will",        "level": 50,  "desc": "Immune to shaken and stunned status effects — the Oath cannot be broken."},
    {"id": "oath_mastery",     "name": "Oath Mastery",      "level": 60,  "desc": "At 5+ Oath stacks, the Oath's effect doubles."},
    {"id": "fortress",         "name": "Fortress",         "level": 70,  "desc": "At 10+ Oath stacks, all incoming damage reduced by 25%."},
    {"id": "unbreakable",      "name": "Unbreakable",      "level": 80,  "desc": "When below 25% HP, reduce all incoming damage by 30%."},
    {"id": "second_wind",      "name": "Second Wind",      "level": 90,  "desc": "Switching Oaths saves 3 stacks instead of resetting to 0."},
    {"id": "eternal_oath",     "name": "Eternal Oath",     "level": 100, "desc": "All Oath effects tripled. Switching Oaths saves 3 stacks. Oath Milestone bonuses (5-stack and 10-stack) are always active."},
]


# ============================================================
# LANCER PASSIVES — 10 Auto-Learned (every 10 levels)
# ============================================================
LANCER_PASSIVES: list[dict] = [
    {"id": "elemental_initiation",  "name": "Elemental Initiation",  "level": 10,  "desc": "Start every combat with one random elemental imbue active."},
    {"id": "lingering_elements",    "name": "Lingering Elements",    "level": 20,  "desc": "Elemental buffs last +1 turn longer than listed."},
    {"id": "elemental_harmony",     "name": "Elemental Harmony",     "level": 30,  "desc": "When 2+ elements are active, strikes deal +10% bonus damage."},
    {"id": "critical_imbue",        "name": "Critical Imbue",        "level": 40,  "desc": "While any elemental imbue is active, +10% crit chance."},
    {"id": "elemental_mastery",     "name": "Elemental Mastery",     "level": 50,  "desc": "All elemental imbue stat_mods increased by +1."},
    {"id": "elemental_cascade",     "name": "Elemental Cascade",     "level": 60,  "desc": "When an elemental buff expires, 50% chance to auto-apply a different element."},
    {"id": "storm_rider",           "name": "Storm Rider",           "level": 70,  "desc": "While Lightning imbue is active, +15% damage on all strikes."},
    {"id": "elemental_fusion",      "name": "Elemental Fusion",      "level": 80,  "desc": "When 3+ elements are active, strikes deal +25% bonus damage and apply 2 statuses."},
    {"id": "elemental_overload",    "name": "Elemental Overload",     "level": 90,  "desc": "Once per combat, can activate all 6 elements simultaneously for 2 turns."},
    {"id": "avatar_of_elements",    "name": "Avatar of Elements",    "level": 100, "desc": "All elemental imbue durations increased by +3 turns. Elemental Overload can be used twice per combat. When all 6 elements active, strikes deal +10% bonus damage."},
]


# ============================================================
# MAGE PASSIVES — 50 Arcane Library Passives (5 Schools)
# ============================================================
# Passives are NOT auto-learned. The Mage chooses 5 to equip.
# Slots unlock at levels 10, 20, 30, 40, 50.
# Passives are earned through Research (kill specific creatures, clear biomes, etc.)
MAGE_PASSIVES: list[dict] = [
    # --- School of Elements (1-10) — Transmute What Skills Apply ---
    {"id": "frostfire",         "name": "Frostfire",         "school": "Elements", "desc": "Fire-tagged skills apply frostburn instead of burning — frostburn deals damage AND slows (ensnared for 1 turn).", "research_req": "Kill a Frost Salamander"},
    {"id": "storm_earth",       "name": "Storm Earth",       "school": "Elements", "desc": "Stone-tagged skills apply shocked instead of bleeding — shocked targets take +25% damage from all sources.", "research_req": "Kill a Stone Golem"},
    {"id": "void_lightning",    "name": "Void Lightning",    "school": "Elements", "desc": "Lightning-tagged skills apply voidmarked instead of stunned — voidmarked targets take true damage from the next hit.", "research_req": "Kill a Thunder Titan"},
    {"id": "caustic_wind",      "name": "Caustic Wind",       "school": "Elements", "desc": "Wind-tagged skills apply corroded instead of their normal status — corroded reduces armor_bonus by 3 per turn (stacks).", "research_req": "Kill a Wind Wraith"},
    {"id": "shadow_ice",        "name": "Shadow Ice",        "school": "Elements", "desc": "Ice-tagged skills apply shadowfrost instead of ensnared — shadowfrost = ensnared + the target cannot be healed.", "research_req": "Kill a Frost Giant"},
    {"id": "magma_skin",        "name": "Magma Skin",         "school": "Elements", "desc": "Stone-tagged skills apply magma instead of bleeding — magma deals burning damage over 3 turns AND spreads to adjacent enemies.", "research_req": "Kill a Magma Elemental"},
    {"id": "thunderblood",      "name": "Thunderblood",      "school": "Elements", "desc": "Lightning-tagged skills also apply bleeding in addition to their normal status.", "research_req": "Kill a Storm Drake"},
    {"id": "absolute_zero",     "name": "Absolute Zero",     "school": "Elements", "desc": "Ice-tagged skills: if the target is already ensnared, they become frozen (can't act at all) for 1 turn.", "research_req": "Kill a Frost Giant"},
    {"id": "wildfire",          "name": "Wildfire",           "school": "Elements", "desc": "Fire-tagged skills: if the target is already burning, the flames intensify — burning damage per turn is doubled.", "research_req": "Kill a Fire Dragon"},
    {"id": "elemental_overload_mage","name": "Elemental Overload","school": "Elements","desc": "All elemental skills apply their status at +2 stacks instead of +1.", "research_req": "Kill 5 Elementals"},
    # --- School of Arcane (11-20) — Transmute How Skills Deal Damage ---
    {"id": "true_strike",       "name": "True Strike",       "school": "Arcane",   "desc": "Strike-tagged skills convert 25% of damage to true damage.", "research_req": "Kill a Crystal Wraith"},
    {"id": "overchannel",       "name": "Overchannel",       "school": "Arcane",   "desc": "Strike-tagged skills deal +50% damage but cost +50% MP.", "research_req": "Kill a Mana Wraith"},
    {"id": "chain_reaction",    "name": "Chain Reaction",    "school": "Arcane",   "desc": "Single-Target + Strike-tagged skills hit 2 targets (spreads to nearest enemy at 50% power).", "research_req": "Kill a Chain Beast"},
    {"id": "echo_chamber",      "name": "Echo Chamber",      "school": "Arcane",   "desc": "Strike-tagged skills repeat at 50% power on the following turn (free, no action cost).", "research_req": "Kill an Echo Spirit"},
    {"id": "implosion",         "name": "Implosion",         "school": "Arcane",   "desc": "Single-Target + Strike-tagged skills deal AoE damage to adjacent enemies.", "research_req": "Kill an Implosion Beast"},
    {"id": "spell_penetration", "name": "Spell Penetration", "school": "Arcane",   "desc": "Strike-tagged skills ignore 50% of target's essence (magic resistance).", "research_req": "Kill a Barrier Construct"},
    {"id": "critical_theory",   "name": "Critical Theory",   "school": "Arcane",   "desc": "Strike-tagged skills have 20% chance to deal double damage (crit).", "research_req": "Kill a Mirror Beast"},
    {"id": "mana_vampire",      "name": "Mana Vampire",      "school": "Arcane",   "desc": "Strike-tagged skills restore MP equal to 10% of damage dealt.", "research_req": "Kill a Mana Leech"},
    {"id": "glass_cannon",      "name": "Glass Cannon",      "school": "Arcane",   "desc": "Strike-tagged skills deal +100% damage but you take +50% damage while casting.", "research_req": "Defeat 3 Bosses"},
    {"id": "arcane_surge",      "name": "Arcane Surge",      "school": "Arcane",   "desc": "Every 3rd Strike-tagged skill in combat deals true damage automatically.", "research_req": "Kill an Arcane Titan"},
    # --- School of Spatial (21-34) — Transmute Range, Targeting, Positioning ---
    {"id": "long_range",        "name": "Long Range",        "school": "Spatial",  "desc": "+1 Range to all skills (range 2 to 3).", "research_req": "Kill a Sniper Wraith"},
    {"id": "point_blank",       "name": "Point Blank",       "school": "Spatial",  "desc": "-1 Range but +30% damage at range 0-1.", "research_req": "Kill a Point Blank Beast"},
    {"id": "expanding_radius",  "name": "Expanding Radius",  "school": "Spatial",  "desc": "Single-target skills hit target + 1 adjacent enemy.", "research_req": "Kill an Expanding Slime"},
    {"id": "blink_step",        "name": "Blink Step",        "school": "Spatial",  "desc": "Teleport-tagged skills also grant hidden for 1 turn.", "research_req": "Kill a Blink Hound"},
    {"id": "portal_mastery", "planned": True,    "name": "Portal Mastery",    "school": "Spatial",  "desc": "Portals last 2 turns (enemy can be lured into them).", "research_req": "Clear the Portal Rift event"},
    {"id": "reposition",        "name": "Reposition",        "school": "Spatial",  "desc": "Defend-tagged skills also move you +1 range away from the enemy.", "research_req": "Kill a Reposition Wraith"},
    {"id": "gravity_shift",     "name": "Gravity Shift",     "school": "Spatial",  "desc": "Debuff-tagged skills also pull the enemy 1 range closer.", "research_req": "Kill a Gravity Beast"},
    {"id": "mirror_position",   "name": "Mirror Position",   "school": "Spatial",  "desc": "When you dodge, you swap positions with the enemy (confuses melee).", "research_req": "Kill a Mirror Construct"},
    {"id": "spatial_tear", "planned": True,      "name": "Spatial Tear",      "school": "Spatial",  "desc": "Buff-tagged skills create a 1-turn portal behind the enemy for flanking.", "research_req": "Kill a Spatial Rift"},
    {"id": "far_strike",        "name": "Far Strike",        "school": "Spatial",  "desc": "Strike-tagged skills can be cast at any range (no minimum).", "research_req": "Kill a Far Strike Beast"},
    {"id": "portal_behind_ally", "planned": True,"name": "Portal Behind Ally","school": "Spatial",  "desc": "Teleport-tagged skills can place the exit portal behind an ally for flanking support.", "research_req": "Kill a Flanking Wraith"},
    {"id": "portal_behind_enemy", "planned": True,"name": "Portal Behind Enemy","school":"Spatial",  "desc": "Teleport-tagged skills can place the exit portal behind the enemy — melee allies get backstab bonus.", "research_req": "Kill a Backstab Beast"},
    {"id": "portal_through_wall", "planned": True,"name": "Portal Through Wall","school":"Spatial",  "desc": "Teleport-tagged skills ignore terrain — portals can pass through walls, doors, and obstacles.", "research_req": "Clear the Sealed Crypt"},
    {"id": "portal_through_trap", "planned": True,"name": "Portal Through Trap","school":"Spatial",  "desc": "Teleport-tagged skills can redirect a portal exit onto a trap — the enemy walks through and triggers it.", "research_req": "Kill a Trap Guardian"},
    # --- School of Temporal (35-40) — Transmute Timing, Cooldowns, Turn Order ---
    {"id": "quickened_mind",    "name": "Quickened Mind",    "school": "Temporal",  "desc": "All cooldowns reduced by 1.", "research_req": "Kill a Time Wraith"},
    {"id": "time_dilation",     "name": "Time Dilation",     "school": "Temporal",  "desc": "Debuff-tagged skills last +1 turn.", "research_req": "Kill a Time Beast"},
    {"id": "rewind",            "name": "Rewind",             "school": "Temporal",  "desc": "Once per combat, rewind to your previous turn's HP and position.", "research_req": "Clear the Void Rift event"},
    {"id": "temporal_echo",     "name": "Temporal Echo",     "school": "Temporal",  "desc": "Dual Cast skills echo at 25% power on the next odd turn.", "research_req": "Kill an Echo Titan"},
    {"id": "time_loop",         "name": "Time Loop",         "school": "Temporal",  "desc": "Enemies with stunned repeat their last action next turn (wastes their turn).", "research_req": "Kill a Time Guardian"},
    {"id": "accelerated_casting","name": "Accelerated Casting","school":"Temporal","desc": "Spells with cooldown 5+ have cooldown reduced to 4.", "research_req": "Kill a Quickened Beast"},
    # --- School of Mental (41-50) — Transmute Debuffs, Illusions, Mind Effects ---
    {"id": "overload_mage",     "name": "Overload",          "school": "Mental",   "desc": "Single-Target + Debuff-tagged skills become AoE (hit all enemies).", "research_req": "Kill a Mind Beast"},
    {"id": "double_jeopardy",   "name": "Double Jeopardy",   "school": "Mental",   "desc": "Debuff-tagged skills apply 2 different statuses instead of 1.", "research_req": "Kill a Twin Wraith"},
    {"id": "mind_fracture",     "name": "Mind Fracture",     "school": "Mental",   "desc": "Shaken targets also lose 1 random stat per turn.", "research_req": "Kill a Mind Flayer"},
    {"id": "paranoia",          "name": "Paranoia",          "school": "Mental",   "desc": "Shaken targets cannot receive buffs (they don't trust allies).", "research_req": "Kill a Paranoia Beast"},
    {"id": "hallucination",     "name": "Hallucination",     "school": "Mental",   "desc": "Illusion-tagged skills create extra decoys — while evasive, enemy attacks have a 30% chance to strike a copy and miss entirely.", "research_req": "Kill a Hallucination Wraith"},
    {"id": "mass_hysteria",     "name": "Mass Hysteria",     "school": "Mental",   "desc": "Debuff-tagged skills bite deeper — every debuff you apply lasts 50% longer.", "research_req": "Kill a Hysteria Beast"},
    {"id": "delirium",          "name": "Delirium",          "school": "Mental",   "desc": "Enemies with 2+ debuffs are so addled they have a 25% chance to turn their attack on themselves.", "research_req": "Kill a Delirium Wraith"},
    {"id": "phobia_implant",    "name": "Phobia Implant",    "school": "Mental",   "desc": "The first Debuff-tagged skill each combat also applies stunned for 1 turn.", "research_req": "Kill a Phobia Beast"},
    {"id": "mind_control",      "name": "Mind Control",      "school": "Mental",   "desc": "Shaken enemies have 15% chance to skip their turn.", "research_req": "Kill a Mind Controller"},
    {"id": "illusion_mastery",  "name": "Illusion Mastery",  "school": "Mental",   "desc": "Evasive also grants hidden — the Mage vanishes on dodge.", "research_req": "Kill an Illusion Beast"},
]


# ============================================================
# PALADIN PASSIVES — 10 Auto-Learned (every 10 levels)
# ============================================================
PALADIN_PASSIVES: list[dict] = [
    {"id": "divine_shield",       "name": "Divine Shield",       "level": 10,  "desc": "Start every combat with warded status."},
    {"id": "holy_fortitude",      "name": "Holy Fortitude",      "level": 20,  "desc": "All self-heals increased by +15%."},
    {"id": "blessed_armor",       "name": "Blessed Armor",       "level": 30,  "desc": "+2 permanent armor_bonus and +2 permanent essence (innate, always active)."},
    {"id": "faith_unbroken",      "name": "Faith Unbroken",      "level": 40,  "desc": "When Faith bar is active (tier 1+), gain +8 armor_bonus."},
    {"id": "divine_retribution",  "name": "Divine Retribution",  "level": 50,  "desc": "Bonus damage (x1.5) against undead and devil enemies on all strikes."},
    {"id": "martyrs_resolve",     "name": "Martyr's Resolve",    "level": 60,  "desc": "When Faith reaches tier 3 (≤50% HP), gain +15 armor_bonus and +8 essence."},
    {"id": "aura_of_warding",     "name": "Aura of Warding",     "level": 70,  "desc": "When warded, reduce all incoming damage by an additional 10%."},
    {"id": "last_light",          "name": "Last Light",          "level": 80,  "desc": "When Faith reaches tier 4 (≤25% HP), gain +25 armor_bonus, +15 essence, and +30% heal amplification."},
    {"id": "resurrection",        "name": "Resurrection",        "level": 90,  "desc": "When HP would reach 0, survive with 1 HP instead. Cannot trigger again for 1 day (real-time cooldown)."},
    {"id": "avatar_of_faith",     "name": "Avatar of Faith",     "level": 100, "desc": "All low-HP scaling bonuses are permanent (always active, regardless of HP)."},
]


# ============================================================
# PRIEST PASSIVES — 10 Auto-Learned (every 10 levels) + 1 Legendary Quest
# ============================================================
# ============================================================
# ALCHEMIST PASSIVES — 10 Auto-Learned (every 10 levels)
# ============================================================
# The Alchemist was the only mastery in the game with NO passive table, so it
# gained nothing at all from level 10 to 100 while every other mastery got ten
# upgrades. These sit on the two axes the Alchemist actually plays with — Combo
# Flow generation/spending and blade imbues — mirroring the shape the other
# tables use: early quality-of-life, a power engine in the 60-70 band, and a
# capstone at 100.
ALCHEMIST_PASSIVES: list[dict] = [
    {"id": "steady_hands",       "name": "Steady Hands",       "level": 10,  "desc": "Combo Flow gain +1 per strike — the katar finds its rhythm sooner."},
    {"id": "deep_reserves",      "name": "Deep Reserves",      "level": 20,  "desc": "Maximum Combo Flow raised from 20 to 25."},
    {"id": "stable_compound",    "name": "Stable Compound",    "level": 30,  "desc": "Imbues carry +1 charge before the coating burns away."},
    {"id": "reactive_coating",   "name": "Reactive Coating",   "level": 40,  "desc": "Imbue riders trigger their mini-rule one hit earlier."},
    {"id": "transmuters_insight","name": "Transmuter's Insight","level": 50,  "desc": "Combo Flow actions cost 1 less (minimum 1)."},
    {"id": "catalytic_surge",    "name": "Catalytic Surge",    "level": 60,  "desc": "THE POWER ENGINE — at 15+ Combo Flow, all imbue rider damage is doubled."},
    {"id": "volatile_mixture",   "name": "Volatile Mixture",   "level": 70,  "desc": "Imbue enemy stat_mods are 50% stronger and last +1 turn."},
    {"id": "dual_imbue",         "name": "Dual Imbue",         "level": 80,  "desc": "The blade holds two imbues at once — both riders apply on every strike."},
    {"id": "endless_reaction",   "name": "Endless Reaction",   "level": 90,  "desc": "Imbue charges never deplete while Combo Flow is 10 or higher."},
    {"id": "perfect_transmutation","name": "Perfect Transmutation","level": 100,"desc": "All mini-rules fire simultaneously, Combo Flow actions are free, and Perfect Formula may be used every turn."},
]


PRIEST_PASSIVES: list[dict] = [
    {"id": "sanctified",          "name": "Sanctified",          "level": 10,  "desc": "Sanctity bonus starts at 90% enemy HP instead of 75%."},
    {"id": "holy_fire",           "name": "Holy Fire",           "level": 20,  "desc": "Holy strikes deal +75% to undead/devils (was +50%)."},
    {"id": "divine_fortitude",    "name": "Divine Fortitude",   "level": 30,  "desc": "+10 permanent essence (innate, always active)."},
    {"id": "smite",              "name": "Smite",              "level": 40,  "desc": "When enemy drops below 50% HP, gain insight +10 for 3 turns."},
    {"id": "exorcist",           "name": "Exorcist",           "level": 50,  "desc": "Holy strikes apply burning to undead/devils."},
    {"id": "deep_faith",         "name": "Deep Faith",         "level": 60,  "desc": "Sanctity bonuses increased: +35% / +75% / +150%. Miracle chance +15%."},
    {"id": "judgment",           "name": "Judgment",           "level": 70,  "desc": "At 50% enemy HP or lower, all strikes deal +20% damage."},
    {"id": "divine_wrath_priest","name": "Divine Wrath",       "level": 80,  "desc": "At 25% enemy HP or lower, all cooldowns reduced by 1 turn."},
    {"id": "redemption",         "name": "Redemption",         "level": 90,  "desc": "At full enemy HP, skills still get +10% effect. Shield Wall gains +50% HP."},
    {"id": "avatar_of_faith_priest","name": "Avatar of Faith",  "level": 100, "desc": "Sanctity bonuses doubled. Holy damage doubled (+100% to undead/devils). When healing allies, Miracle chance is doubled. Heals on allies also apply a Shield Wall (10% max HP) on the target. bind and blind durations +1 turn. Shield Wall Sanctity scaling doubled. Enemy cannot heal below current HP."},
    {"id": "hand_of_god",        "name": "Hand of God",         "level": 100, "quest": True, "desc": "Legendary passive. Miracle is guaranteed (100%) when target is below 25% HP. All heals cleanse debuffs on the target before healing. Shield Walls heal the Priest for 50% of damage absorbed. When Miracle triggers on a strike, also applies blind. When Miracle triggers on a heal, also applies inspired (+grace for 3 turns). Sanctity bonuses tripled."},
]


# ============================================================
# CONTINENTS + BIOMES (canon v2 — see world_data.py for the master list)
# ============================================================
from world_data import CONTINENTS_V2, BIOME_ID_MAP  # noqa: E402

CONTINENTS: list[dict] = CONTINENTS_V2


# ============================================================
# MONSTERS (Aetheria for MVP)
# ============================================================
MONSTERS: list[dict] = [
    # ==================== VALERIA ====================
    # ---- Golden Plains (Lv 1) ----
    {"id": "gray_wolf", "name": "Gray Wolf", "biome": "golden_plains", "rarity": "common", "hp": 18,
     "creature_tier": "normal", "species": "beast", "archetype": "striker", "personality": "aggressive",
     "stats": {"might": {"base": 12, "growth": 1.2}, "grace": {"base": 14, "growth": 1.3}, "cognition": {"base": 6, "growth": 0.8},
               "insight": {"base": 5, "growth": 0.7}, "essence": {"base": 7, "growth": 0.9}, "durability": {"base": 10, "growth": 1.0}},
     "life": {"mp": 0, "stamina": 100, "shield": 0},
     "passive_buff": {"type": "might_bonus", "value": 0.10, "secondary": {"type": "grace_bonus", "value": 0.07}},
     "profile_skills": {
         "attack": [{"id": "gray_wolf_savage_bite", "name": "Savage Bite", "power_type": "strike", "damage_type": "physical", "damage": 6, "cost_mp": 0, "cost_stamina": 20, "cooldown": 1, "trigger": "always",
                     "status_apply": "bleeding", "stat_mod": {"enemy": {"might": -2}}, "mod_duration": 2}],
         "defense": [{"id": "gray_wolf_guard_howl", "name": "Guard Howl", "power_type": "buff", "cost_mp": 0, "cost_stamina": 30, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 3}}, "mod_duration": 2}],
         "utility": [{"id": "gray_wolf_pack_call", "name": "Pack Call", "power_type": "buff", "cost_mp": 0, "cost_stamina": 30, "cooldown": 3, "trigger": "always",
                      "self_status": "inspired", "stat_mod": {"self": {"might": 3}}, "mod_duration": 2}],
     },
     "signature_fusion": {"id": "gray_wolf_predators_fury", "name": "Predator's Fury", "power_type": "strike", "damage_type": "physical", "damage": 10, "cost_mp": 0, "cost_stamina": 50, "cooldown": 4, "hits": 3, "is_signature": True,
                          "status_apply": "bleeding", "lifesteal": 0.20, "stat_mod": {"enemy": {"grace": -3}}, "mod_duration": 3},
     "drops": {"common": [{"id": "wolf_pelt", "chance": 0.7, "qty": [1, 1]}, {"id": "wolf_fang", "chance": 0.4, "qty": [1, 1]}], "rare": [], "boss": [], "gold": [2, 8], "xp_mult": 1.0}},
    {"id": "highway_bandit", "name": "Highway Bandit", "biome": "golden_plains", "rarity": "uncommon", "hp": 24,
     "creature_tier": "normal", "species": "humanoid", "archetype": "striker", "personality": "aggressive",
     "stats": {"might": {"base": 14, "growth": 1.3}, "grace": {"base": 12, "growth": 1.1}, "cognition": {"base": 8, "growth": 0.9},
               "insight": {"base": 6, "growth": 0.7}, "essence": {"base": 5, "growth": 0.5}, "durability": {"base": 12, "growth": 1.1}},
     "life": {"mp": 0, "stamina": 100, "shield": 0},
     "passive_buff": {"type": "might_bonus", "value": 0.13, "secondary": {"type": "grace_bonus", "value": 0.09}},
     "profile_skills": {
         "attack": [{"id": "highway_bandit_slash", "name": "Quick Slash", "power_type": "strike", "damage_type": "physical", "damage": 7, "cost_mp": 0, "cost_stamina": 25, "cooldown": 1, "trigger": "always",
                     "status_apply": "bleeding", "stat_mod": {"enemy": {"grace": -1}}, "mod_duration": 2},
                    {"id": "highway_bandit_stomp", "name": "Stomp", "power_type": "strike", "damage_type": "physical", "damage": 9, "cost_mp": 0, "cost_stamina": 35, "cooldown": 2, "trigger": "always",
                     "status_apply": "stunned", "stat_mod": {"enemy": {"armor_bonus": -2}}, "mod_duration": 2}],
         "defense": [{"id": "highway_bandit_parry", "name": "Parry Stance", "power_type": "buff", "cost_mp": 0, "cost_stamina": 25, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "warded", "stat_mod": {"self": {"grace": 3, "armor_bonus": 2}}, "mod_duration": 2}],
         "utility": [{"id": "highway_bandit_war_cry", "name": "War Cry", "power_type": "buff", "cost_mp": 0, "cost_stamina": 30, "cooldown": 3, "trigger": "always",
                      "self_status": "inspired", "stat_mod": {"self": {"might": 3}}, "mod_duration": 2}],
     },
     "signature_fusion": {"id": "highway_bandit_outlaw_fury", "name": "Outlaw's Fury", "power_type": "strike", "damage_type": "physical", "damage": 12, "cost_mp": 0, "cost_stamina": 50, "cooldown": 4, "hits": 2, "is_signature": True,
                          "status_apply": "stunned", "armor_ignore": True, "stat_mod": {"enemy": {"might": -3}}, "mod_duration": 3},
     "drops": {"common": [{"id": "coin_purse", "chance": 0.8, "qty": [1, 1]}, {"id": "iron_dagger", "chance": 0.15, "qty": [1, 1]}], "rare": [], "boss": [], "gold": [5, 15], "xp_mult": 1.0}},
    {"id": "grove_wisp", "name": "Grove Wisp", "biome": "crownwood_forest", "rarity": "uncommon", "hp": 15,
     "creature_tier": "normal", "species": "magical", "archetype": "caster", "personality": "opportunist",
     "stats": {"might": {"base": 5, "growth": 0.5}, "grace": {"base": 12, "growth": 1.1}, "cognition": {"base": 14, "growth": 1.3},
               "insight": {"base": 13, "growth": 1.2}, "essence": {"base": 12, "growth": 1.1}, "durability": {"base": 6, "growth": 0.6}},
     "life": {"mp": 10, "stamina": 80, "shield": 0},
     "passive_buff": {"type": "grace_bonus", "value": 0.13, "secondary": {"type": "evasion_bonus", "value": 0.09}},
     "profile_skills": {
         "attack": [{"id": "grove_wisp_thorn_whip", "name": "Thorn Whip", "power_type": "strike", "damage_type": "magical", "damage": 6, "cost_mp": 2, "cost_stamina": 0, "cooldown": 1, "trigger": "always",
                     "status_apply": "bleeding", "stat_mod": {"enemy": {"grace": -2}}, "mod_duration": 2}],
         "defense": [{"id": "grove_wisp_bark_skin", "name": "Bark Skin", "power_type": "buff", "cost_mp": 2, "cost_stamina": 0, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 3, "essence": 2}}, "mod_duration": 2}],
         "utility": [{"id": "grove_wisp_root_trap", "name": "Root Trap", "power_type": "debuff", "damage_type": "magical", "damage": 3, "cost_mp": 3, "cost_stamina": 0, "cooldown": 2, "trigger": "opening_move",
                      "status_apply": "ensnared", "stat_mod": {"enemy": {"grace": -3, "might": -2}}, "mod_duration": 2}],
     },
     "signature_fusion": {"id": "grove_wisp_wild_overgrowth", "name": "Wild Overgrowth", "power_type": "strike", "damage_type": "magical", "damage": 10, "cost_mp": 5, "cost_stamina": 0, "cooldown": 4, "hits": 3, "is_signature": True,
                          "status_apply": "poisoned", "lifesteal": 0.15, "stat_mod": {"enemy": {"might": -3}}, "mod_duration": 3},
     "drops": {"common": [{"id": "wisp_essence", "chance": 0.6, "qty": [1, 1]}], "rare": [{"id": "skillbook_ward", "chance": 0.03, "qty": [1, 1]}], "boss": [], "gold": [3, 10], "xp_mult": 1.1}},
    {"id": "boar", "name": "Feral Boar", "biome": "crownwood_forest", "rarity": "common", "hp": 30,
     "creature_tier": "normal", "species": "beast", "archetype": "bruiser", "personality": "aggressive",
     "stats": {"might": {"base": 16, "growth": 1.4}, "grace": {"base": 8, "growth": 0.8}, "cognition": {"base": 4, "growth": 0.5},
               "insight": {"base": 5, "growth": 0.6}, "essence": {"base": 6, "growth": 0.6}, "durability": {"base": 16, "growth": 1.4}},
     "life": {"mp": 0, "stamina": 120, "shield": 0},
     "passive_buff": {"type": "durability_bonus", "value": 0.12, "secondary": {"type": "might_bonus", "value": 0.08}},
     "profile_skills": {
         "attack": [{"id": "boar_tusk_charge", "name": "Tusk Charge", "power_type": "strike", "damage_type": "physical", "damage": 8, "cost_mp": 0, "cost_stamina": 25, "cooldown": 1, "trigger": "always",
                     "status_apply": "bleeding", "stat_mod": {"enemy": {"armor_bonus": -2}}, "mod_duration": 2}],
         "defense": [{"id": "boar_iron_hide", "name": "Iron Hide", "power_type": "buff", "cost_mp": 0, "cost_stamina": 30, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 4, "durability": 2}}, "mod_duration": 3}],
         "utility": [{"id": "boar_rage", "name": "Feral Rage", "power_type": "buff", "cost_mp": 0, "cost_stamina": 20, "cooldown": 3, "trigger": "always",
                      "self_status": "inspired", "stat_mod": {"self": {"might": 4}}, "mod_duration": 2}],
     },
     "signature_fusion": {"id": "boar_unstoppable_charge", "name": "Unstoppable Charge", "power_type": "strike", "damage_type": "physical", "damage": 14, "cost_mp": 0, "cost_stamina": 50, "cooldown": 4, "hits": 1, "is_signature": True,
                          "status_apply": "stunned", "armor_ignore": True, "stat_mod": {"enemy": {"might": -3, "armor_bonus": -3}}, "mod_duration": 3},
     "drops": {"common": [{"id": "boar_hide", "chance": 0.7, "qty": [1, 1]}, {"id": "boar_tusk", "chance": 0.5, "qty": [1, 1]}], "rare": [], "boss": [], "gold": [3, 10], "xp_mult": 1.0}},
    {"id": "river_serpent", "name": "River Serpent", "biome": "imperial_riverlands", "rarity": "rare", "hp": 28,
     "creature_tier": "normal", "species": "beast", "archetype": "speed", "personality": "opportunist",
     "stats": {"might": {"base": 10, "growth": 1.0}, "grace": {"base": 14, "growth": 1.3}, "cognition": {"base": 10, "growth": 1.0},
               "insight": {"base": 12, "growth": 1.1}, "essence": {"base": 10, "growth": 1.0}, "durability": {"base": 8, "growth": 0.8}},
     "life": {"mp": 15, "stamina": 90, "shield": 0},
     "passive_buff": {"type": "essence_bonus", "value": 0.15, "secondary": {"type": "magic_resist", "value": 0.10}},
     "profile_skills": {
         "attack": [{"id": "river_serpent_venom_strike", "name": "Venom Strike", "power_type": "strike", "damage_type": "physical", "damage": 7, "cost_mp": 0, "cost_stamina": 20, "cooldown": 1, "trigger": "always",
                     "status_apply": "poisoned", "stat_mod": {"enemy": {"might": -2}}, "mod_duration": 3},
                    {"id": "river_serpent_drown", "name": "Drowning Grip", "power_type": "strike", "damage_type": "magical", "damage": 9, "cost_mp": 5, "cost_stamina": 0, "cooldown": 2, "trigger": "opponent_wounded",
                     "status_apply": "weary", "stat_mod": {"enemy": {"grace": -3}}, "mod_duration": 2}],
         "defense": [{"id": "river_serpent_shed_skin", "name": "Shed Skin", "power_type": "heal", "cost_mp": 4, "cost_stamina": 0, "cooldown": 3, "trigger": "low_hp",
                      "heal_percent": 0.08, "self_status": "evasive", "cleanses": True}],
         "utility": [{"id": "river_serpent_constrict", "name": "Constrict", "power_type": "debuff", "damage_type": "physical", "damage": 3, "cost_mp": 3, "cost_stamina": 15, "cooldown": 2, "trigger": "always",
                      "status_apply": "ensnared", "stat_mod": {"enemy": {"grace": -3, "might": -2}}, "mod_duration": 3}],
     },
     "signature_fusion": {"id": "river_serpent_venom_cascade", "name": "Venom Cascade", "power_type": "strike", "damage_type": "physical", "damage": 14, "cost_mp": 8, "cost_stamina": 0, "cooldown": 4, "hits": 3, "is_signature": True,
                          "status_apply": "poisoned", "uncleansable": True, "stat_mod": {"enemy": {"might": -4}}, "mod_duration": 4},
     "drops": {"common": [{"id": "serpent_scale", "chance": 0.7, "qty": [1, 1]}, {"id": "serpent_venom", "chance": 0.3, "qty": [1, 1]}], "rare": [], "boss": [], "gold": [5, 15], "xp_mult": 1.2}},
    {"id": "ruin_ghast", "name": "Ruin Ghast", "biome": "ashen_border", "rarity": "legendary", "hp": 38,
     "creature_tier": "normal", "species": "undead", "archetype": "caster", "personality": "opportunist",
     "tags": ["undead"],
     "stats": {"might": {"base": 6, "growth": 0.6}, "grace": {"base": 10, "growth": 1.0}, "cognition": {"base": 14, "growth": 1.3},
               "insight": {"base": 16, "growth": 1.4}, "essence": {"base": 12, "growth": 1.2}, "durability": {"base": 10, "growth": 1.0}},
     "life": {"mp": 20, "stamina": 80, "shield": 0},
     "passive_buff": {"type": "cognition_bonus", "value": 0.20, "secondary": {"type": "lifesteal", "value": 0.10}},
     "profile_skills": {
         "attack": [{"id": "ruin_ghast_life_drain", "name": "Life Drain", "power_type": "strike", "damage_type": "magical", "damage": 7, "cost_mp": 3, "cost_stamina": 0, "cooldown": 1, "trigger": "always",
                     "lifesteal": 0.15, "stat_mod": {"enemy": {"essence": -2}}, "mod_duration": 2},
                    {"id": "ruin_ghast_hexing_curse", "name": "Hexing Curse", "power_type": "debuff", "damage_type": "magical", "damage": 3, "cost_mp": 4, "cost_stamina": 0, "cooldown": 2, "trigger": "opening_move",
                     "status_apply": "poisoned", "stat_mod": {"enemy": {"cognition": -3, "insight": -2}}, "mod_duration": 3}],
         "defense": [{"id": "ruin_ghast_bone_armor", "name": "Bone Armor", "power_type": "buff", "cost_mp": 3, "cost_stamina": 0, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 4, "essence": 3}}, "mod_duration": 3}],
         "utility": [{"id": "ruin_ghast_fear_aura", "name": "Fear Aura", "power_type": "debuff", "damage_type": "magical", "damage": 3, "cost_mp": 3, "cost_stamina": 0, "cooldown": 2, "trigger": "opening_move",
                      "status_apply": "weary", "stat_mod": {"enemy": {"might": -3, "grace": -2}}, "mod_duration": 3}],
     },
     "signature_fusion": {"id": "ruin_ghast_death_coil", "name": "Death Coil", "power_type": "strike", "damage_type": "magical", "damage": 14, "cost_mp": 8, "cost_stamina": 0, "cooldown": 4, "hits": 1, "is_signature": True,
                          "status_apply": "poisoned", "lifesteal": 0.20, "stat_mod": {"enemy": {"essence": -4, "insight": -3}}, "mod_duration": 4},
     "drops": {"common": [{"id": "ghast_dust", "chance": 0.6, "qty": [1, 1]}, {"id": "relic_shard", "chance": 0.4, "qty": [1, 1]}], "rare": [{"id": "skillbook_purge", "chance": 0.05, "qty": [1, 1]}], "boss": [], "gold": [8, 20], "xp_mult": 1.3}},
    # ---- Bloodwind Plains (Mushkara starter) ----
    {"id": "scavenger_hound", "name": "Scavenger Hound", "biome": "bloodwind_plains", "rarity": "common", "hp": 20,
     "creature_tier": "normal", "species": "beast", "archetype": "striker", "personality": "aggressive",
     "stats": {"might": {"base": 13, "growth": 1.2}, "grace": {"base": 12, "growth": 1.1}, "cognition": {"base": 6, "growth": 0.7},
               "insight": {"base": 5, "growth": 0.6}, "essence": {"base": 6, "growth": 0.7}, "durability": {"base": 11, "growth": 1.0}},
     "life": {"mp": 0, "stamina": 100, "shield": 0},
     "passive_buff": {"type": "might_bonus", "value": 0.12, "secondary": {"type": "grace_bonus", "value": 0.08}},
     "profile_skills": {
         "attack": [{"id": "scavenger_hound_ravage", "name": "Ravage", "power_type": "strike", "damage_type": "physical", "damage": 6, "cost_mp": 0, "cost_stamina": 20, "cooldown": 1, "trigger": "always",
                     "status_apply": "bleeding", "stat_mod": {"enemy": {"might": -2}}, "mod_duration": 2}],
         "defense": [{"id": "scavenger_hound_bone_guard", "name": "Bone Guard", "power_type": "buff", "cost_mp": 0, "cost_stamina": 30, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 3}}, "mod_duration": 2}],
         "utility": [{"id": "scavenger_hound_pack_howl", "name": "Pack Howl", "power_type": "buff", "cost_mp": 0, "cost_stamina": 30, "cooldown": 3, "trigger": "always",
                      "self_status": "inspired", "stat_mod": {"self": {"might": 3, "grace": 2}}, "mod_duration": 2}],
     },
     "signature_fusion": {"id": "scavenger_hound_war_feast", "name": "War Feast", "power_type": "strike", "damage_type": "physical", "damage": 10, "cost_mp": 0, "cost_stamina": 50, "cooldown": 4, "hits": 2, "is_signature": True,
                          "status_apply": "bleeding", "lifesteal": 0.20, "stat_mod": {"enemy": {"might": -3}}, "mod_duration": 3},
     "drops": {"common": [{"id": "scrap_bone", "chance": 0.7, "qty": [1, 1]}, {"id": "wolf_fang", "chance": 0.4, "qty": [1, 1]}], "rare": [], "boss": [], "gold": [2, 8], "xp_mult": 1.0}},
    {"id": "orc_grunt", "name": "Orc Grunt", "biome": "bloodwind_plains", "rarity": "uncommon", "hp": 28,
     "creature_tier": "normal", "species": "humanoid", "archetype": "bruiser", "personality": "aggressive",
     "stats": {"might": {"base": 16, "growth": 1.4}, "grace": {"base": 8, "growth": 0.8}, "cognition": {"base": 6, "growth": 0.7},
               "insight": {"base": 5, "growth": 0.6}, "essence": {"base": 6, "growth": 0.6}, "durability": {"base": 14, "growth": 1.2}},
     "life": {"mp": 0, "stamina": 120, "shield": 0},
     "passive_buff": {"type": "might_bonus", "value": 0.15, "secondary": {"type": "durability_bonus", "value": 0.08}},
     "profile_skills": {
         "attack": [{"id": "orc_grunt_cleave", "name": "Cleaving Blow", "power_type": "strike", "damage_type": "physical", "damage": 8, "cost_mp": 0, "cost_stamina": 25, "cooldown": 1, "trigger": "always",
                     "status_apply": "bleeding", "stat_mod": {"enemy": {"armor_bonus": -2}}, "mod_duration": 2},
                    {"id": "orc_grunt_war_stomp", "name": "War Stomp", "power_type": "strike", "damage_type": "physical", "damage": 10, "cost_mp": 0, "cost_stamina": 35, "cooldown": 2, "trigger": "always",
                     "status_apply": "stunned", "stat_mod": {"enemy": {"grace": -2}}, "mod_duration": 2}],
         "defense": [{"id": "orc_grunt_blood_fury", "name": "Blood Fury", "power_type": "buff", "cost_mp": 0, "cost_stamina": 30, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "inspired", "stat_mod": {"self": {"might": 4, "armor_bonus": 2}}, "mod_duration": 3}],
         "utility": [{"id": "orc_grunt_battle_cry", "name": "Battle Cry", "power_type": "buff", "cost_mp": 0, "cost_stamina": 25, "cooldown": 3, "trigger": "always",
                      "self_status": "inspired", "stat_mod": {"self": {"might": 3}}, "mod_duration": 2}],
     },
     "signature_fusion": {"id": "orc_grunt_waaagh", "name": "WAAAGH!", "power_type": "strike", "damage_type": "physical", "damage": 14, "cost_mp": 0, "cost_stamina": 50, "cooldown": 4, "hits": 2, "is_signature": True,
                          "status_apply": "stunned", "armor_ignore": True, "stat_mod": {"enemy": {"might": -4}}, "mod_duration": 3},
     "drops": {"common": [{"id": "scrap_bone", "chance": 0.6, "qty": [1, 1]}, {"id": "iron_ore", "chance": 0.4, "qty": [1, 1]}], "rare": [{"id": "coin_purse", "chance": 0.3, "qty": [1, 1]}], "boss": [], "gold": [5, 15], "xp_mult": 1.1}},
    # ---- Trade Road Outpost (Concordia starter) ----
    {"id": "road_bandit", "name": "Road Bandit", "biome": "trade_road_outpost", "rarity": "common", "hp": 22,
     "creature_tier": "normal", "species": "humanoid", "archetype": "speed", "personality": "opportunist",
     "stats": {"might": {"base": 12, "growth": 1.1}, "grace": {"base": 14, "growth": 1.3}, "cognition": {"base": 8, "growth": 0.9},
               "insight": {"base": 7, "growth": 0.8}, "essence": {"base": 5, "growth": 0.5}, "durability": {"base": 10, "growth": 1.0}},
     "life": {"mp": 0, "stamina": 100, "shield": 0},
     "passive_buff": {"type": "grace_bonus", "value": 0.12, "secondary": {"type": "might_bonus", "value": 0.08}},
     "profile_skills": {
         "attack": [{"id": "road_bandit_slash", "name": "Quick Slash", "power_type": "strike", "damage_type": "physical", "damage": 6, "cost_mp": 0, "cost_stamina": 20, "cooldown": 1, "trigger": "always",
                     "status_apply": "bleeding", "stat_mod": {"enemy": {"grace": -1}}, "mod_duration": 2},
                    {"id": "road_bandit_kick", "name": "Kick", "power_type": "strike", "damage_type": "physical", "damage": 5, "cost_mp": 0, "cost_stamina": 25, "cooldown": 2, "trigger": "always",
                     "status_apply": "stunned", "stat_mod": {"enemy": {"might": -2}}, "mod_duration": 2}],
         "defense": [{"id": "road_bandit_sidestep", "name": "Sidestep", "power_type": "buff", "cost_mp": 0, "cost_stamina": 20, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "evasive", "stat_mod": {"self": {"grace": 3}}, "mod_duration": 2}],
         "utility": [{"id": "road_bandit_feint", "name": "Feint", "power_type": "debuff", "damage_type": "physical", "damage": 2, "cost_mp": 0, "cost_stamina": 15, "cooldown": 2, "trigger": "opening_move",
                      "status_apply": "weary", "stat_mod": {"enemy": {"grace": -2}}, "mod_duration": 2}],
     },
     "signature_fusion": {"id": "road_bandit_ambush_strike", "name": "Ambush Strike", "power_type": "strike", "damage_type": "physical", "damage": 10, "cost_mp": 0, "cost_stamina": 50, "cooldown": 4, "hits": 2, "is_signature": True,
                          "status_apply": "stunned", "armor_ignore": True, "stat_mod": {"enemy": {"grace": -3}}, "mod_duration": 3},
     "drops": {"common": [{"id": "coin_purse", "chance": 0.8, "qty": [1, 1]}], "rare": [{"id": "iron_dagger", "chance": 0.15, "qty": [1, 1]}], "boss": [], "gold": [5, 15], "xp_mult": 1.0}},
    {"id": "stray_wolf", "name": "Stray Wolf", "biome": "trade_road_outpost", "rarity": "uncommon", "hp": 18,
     "creature_tier": "normal", "species": "beast", "archetype": "striker", "personality": "aggressive",
     "stats": {"might": {"base": 13, "growth": 1.2}, "grace": {"base": 13, "growth": 1.2}, "cognition": {"base": 6, "growth": 0.7},
               "insight": {"base": 5, "growth": 0.6}, "essence": {"base": 7, "growth": 0.8}, "durability": {"base": 9, "growth": 0.9}},
     "life": {"mp": 0, "stamina": 100, "shield": 0},
     "passive_buff": {"type": "grace_bonus", "value": 0.13, "secondary": {"type": "might_bonus", "value": 0.07}},
     "profile_skills": {
         "attack": [{"id": "stray_wolf_savage_bite", "name": "Savage Bite", "power_type": "strike", "damage_type": "physical", "damage": 7, "cost_mp": 0, "cost_stamina": 20, "cooldown": 1, "trigger": "always",
                     "status_apply": "bleeding", "stat_mod": {"enemy": {"might": -2}}, "mod_duration": 2}],
         "defense": [{"id": "stray_wolf_guard_howl", "name": "Guard Howl", "power_type": "buff", "cost_mp": 0, "cost_stamina": 30, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 3}}, "mod_duration": 2}],
         "utility": [{"id": "stray_wolf_pack_howl", "name": "Pack Howl", "power_type": "buff", "cost_mp": 0, "cost_stamina": 30, "cooldown": 3, "trigger": "always",
                      "self_status": "inspired", "stat_mod": {"self": {"might": 3}}, "mod_duration": 2}],
     },
     "signature_fusion": {"id": "stray_wolf_hunters_frenzy", "name": "Hunter's Frenzy", "power_type": "strike", "damage_type": "physical", "damage": 10, "cost_mp": 0, "cost_stamina": 50, "cooldown": 4, "hits": 3, "is_signature": True,
                          "status_apply": "bleeding", "lifesteal": 0.15, "stat_mod": {"enemy": {"grace": -3}}, "mod_duration": 3},
     "drops": {"common": [{"id": "wolf_pelt", "chance": 0.7, "qty": [1, 1]}, {"id": "wolf_fang", "chance": 0.4, "qty": [1, 1]}], "rare": [], "boss": [], "gold": [3, 10], "xp_mult": 1.0}},
    # ---- Stone Ridge (Frosthelm starter) ----
    {"id": "rock_crawler", "name": "Rock Crawler", "biome": "stone_ridge", "rarity": "common", "hp": 26,
     "creature_tier": "normal", "species": "monster", "archetype": "tank", "personality": "guardian",
     "stats": {"might": {"base": 14, "growth": 1.3}, "grace": {"base": 6, "growth": 0.6}, "cognition": {"base": 4, "growth": 0.5},
               "insight": {"base": 4, "growth": 0.5}, "essence": {"base": 6, "growth": 0.6}, "durability": {"base": 18, "growth": 1.5}},
     "life": {"mp": 0, "stamina": 100, "shield": 0},
     "passive_buff": {"type": "durability_bonus", "value": 0.15, "secondary": {"type": "might_bonus", "value": 0.08}},
     "profile_skills": {
         "attack": [{"id": "rock_crawler_crush", "name": "Crushing Blow", "power_type": "strike", "damage_type": "physical", "damage": 7, "cost_mp": 0, "cost_stamina": 25, "cooldown": 1, "trigger": "always",
                     "status_apply": "stunned", "stat_mod": {"enemy": {"armor_bonus": -2}}, "mod_duration": 2}],
         "defense": [{"id": "rock_crawler_shell", "name": "Stone Shell", "power_type": "buff", "cost_mp": 0, "cost_stamina": 30, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 5, "durability": 3}}, "mod_duration": 3}],
         "utility": [{"id": "rock_crawler_quake", "name": "Quake", "power_type": "debuff", "damage_type": "physical", "damage": 3, "cost_mp": 0, "cost_stamina": 25, "cooldown": 2, "trigger": "always",
                      "status_apply": "ensnared", "stat_mod": {"enemy": {"grace": -2}}, "mod_duration": 2}],
     },
     "signature_fusion": {"id": "rock_crawler_boulder_crash", "name": "Boulder Crash", "power_type": "strike", "damage_type": "physical", "damage": 11, "cost_mp": 0, "cost_stamina": 50, "cooldown": 4, "hits": 1, "is_signature": True,
                          "status_apply": "stunned", "armor_ignore": True, "stat_mod": {"enemy": {"might": -3, "armor_bonus": -3}}, "mod_duration": 3},
     "drops": {"common": [{"id": "copper_ore", "chance": 0.7, "qty": [1, 1]}, {"id": "iron_ore", "chance": 0.3, "qty": [1, 1]}], "rare": [], "boss": [], "gold": [3, 10], "xp_mult": 1.0}},
    {"id": "cave_bat", "name": "Cave Bat", "biome": "stone_ridge", "rarity": "uncommon", "hp": 14,
     "creature_tier": "normal", "species": "beast", "archetype": "speed", "personality": "opportunist",
     "stats": {"might": {"base": 8, "growth": 0.8}, "grace": {"base": 16, "growth": 1.4}, "cognition": {"base": 8, "growth": 0.9},
               "insight": {"base": 6, "growth": 0.7}, "essence": {"base": 6, "growth": 0.6}, "durability": {"base": 6, "growth": 0.6}},
     "life": {"mp": 0, "stamina": 90, "shield": 0},
     "passive_buff": {"type": "grace_bonus", "value": 0.15, "secondary": {"type": "evasion_bonus", "value": 0.10}},
     "profile_skills": {
         "attack": [{"id": "cave_bat_talon_dive", "name": "Talon Dive", "power_type": "strike", "damage_type": "physical", "damage": 5, "cost_mp": 0, "cost_stamina": 15, "cooldown": 1, "trigger": "always",
                     "status_apply": "bleeding", "stat_mod": {"enemy": {"grace": -2}}, "mod_duration": 2}],
         "defense": [{"id": "cave_bat_evasion", "name": "Wing Shield", "power_type": "buff", "cost_mp": 0, "cost_stamina": 20, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "evasive", "stat_mod": {"self": {"grace": 3}}, "mod_duration": 2}],
         "utility": [{"id": "cave_bat_screech", "name": "Disorienting Screech", "power_type": "debuff", "damage_type": "physical", "damage": 2, "cost_mp": 0, "cost_stamina": 20, "cooldown": 2, "trigger": "opening_move",
                      "status_apply": "weary", "stat_mod": {"enemy": {"cognition": -2, "grace": -2}}, "mod_duration": 3}],
     },
     "signature_fusion": {"id": "cave_bat_swarm_frenzy", "name": "Swarm Frenzy", "power_type": "strike", "damage_type": "physical", "damage": 9, "cost_mp": 0, "cost_stamina": 50, "cooldown": 4, "hits": 4, "is_signature": True,
                          "status_apply": "bleeding", "lifesteal": 0.10, "stat_mod": {"enemy": {"grace": -3}}, "mod_duration": 3},
     "drops": {"common": [{"id": "scrap_bone", "chance": 0.5, "qty": [1, 1]}, {"id": "copper_ore", "chance": 0.3, "qty": [1, 1]}], "rare": [], "boss": [], "gold": [2, 8], "xp_mult": 1.0}},
    # ---- Verdant Edge (Verdania starter) ----
    {"id": "thorn_sprite", "name": "Thorn Sprite", "biome": "verdant_edge", "rarity": "common", "hp": 16,
     "creature_tier": "normal", "species": "magical", "archetype": "caster", "personality": "opportunist",
     "stats": {"might": {"base": 5, "growth": 0.5}, "grace": {"base": 12, "growth": 1.1}, "cognition": {"base": 12, "growth": 1.1},
               "insight": {"base": 10, "growth": 1.0}, "essence": {"base": 14, "growth": 1.3}, "durability": {"base": 6, "growth": 0.6}},
     "life": {"mp": 15, "stamina": 60, "shield": 0},
     "passive_buff": {"type": "essence_bonus", "value": 0.12, "secondary": {"type": "grace_bonus", "value": 0.08}},
     "profile_skills": {
         "attack": [{"id": "thorn_sprite_thornlash", "name": "Thornlash", "power_type": "strike", "damage_type": "magical", "damage": 5, "cost_mp": 2, "cost_stamina": 0, "cooldown": 1, "trigger": "always",
                     "status_apply": "poisoned", "stat_mod": {"enemy": {"grace": -2}}, "mod_duration": 2}],
         "defense": [{"id": "thorn_sprite_bark_skin", "name": "Bark Skin", "power_type": "buff", "cost_mp": 2, "cost_stamina": 0, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 3, "essence": 2}}, "mod_duration": 2}],
         "utility": [{"id": "thorn_sprite_root_trap", "name": "Root Trap", "power_type": "debuff", "damage_type": "magical", "damage": 2, "cost_mp": 3, "cost_stamina": 0, "cooldown": 2, "trigger": "opening_move",
                      "status_apply": "ensnared", "stat_mod": {"enemy": {"grace": -3, "might": -2}}, "mod_duration": 2}],
     },
     "signature_fusion": {"id": "thorn_sprite_wild_overgrowth", "name": "Wild Overgrowth", "power_type": "strike", "damage_type": "magical", "damage": 10, "cost_mp": 5, "cost_stamina": 0, "cooldown": 4, "hits": 3, "is_signature": True,
                          "status_apply": "poisoned", "lifesteal": 0.15, "stat_mod": {"enemy": {"might": -3}}, "mod_duration": 3},
     "drops": {"common": [{"id": "wild_herb", "chance": 0.6, "qty": [1, 1]}, {"id": "wisp_essence", "chance": 0.3, "qty": [1, 1]}], "rare": [], "boss": [], "gold": [2, 8], "xp_mult": 1.0}},
    {"id": "forest_fox", "name": "Forest Fox", "biome": "verdant_edge", "rarity": "uncommon", "hp": 20,
     "creature_tier": "normal", "species": "beast", "archetype": "speed", "personality": "opportunist",
     "stats": {"might": {"base": 10, "growth": 1.0}, "grace": {"base": 16, "growth": 1.4}, "cognition": {"base": 10, "growth": 1.0},
               "insight": {"base": 8, "growth": 0.8}, "essence": {"base": 8, "growth": 0.8}, "durability": {"base": 8, "growth": 0.8}},
     "life": {"mp": 5, "stamina": 100, "shield": 0},
     "passive_buff": {"type": "grace_bonus", "value": 0.14, "secondary": {"type": "evasion_bonus", "value": 0.10}},
     "profile_skills": {
         "attack": [{"id": "forest_fox_talon_dive", "name": "Talon Dive", "power_type": "strike", "damage_type": "physical", "damage": 6, "cost_mp": 0, "cost_stamina": 20, "cooldown": 1, "trigger": "always",
                     "status_apply": "bleeding", "stat_mod": {"enemy": {"grace": -2}}, "mod_duration": 2}],
         "defense": [{"id": "forest_fox_night_veil", "name": "Night Veil", "power_type": "buff", "cost_mp": 0, "cost_stamina": 20, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "evasive", "stat_mod": {"self": {"grace": 4, "essence": 2}}, "mod_duration": 2}],
         "utility": [{"id": "forest_fox_prowl", "name": "Prowl", "power_type": "buff", "cost_mp": 0, "cost_stamina": 20, "cooldown": 3, "trigger": "always",
                      "self_status": "evasive", "stat_mod": {"self": {"grace": 3, "might": 2}}, "mod_duration": 2}],
     },
     "signature_fusion": {"id": "forest_fox_shadow_frenzy", "name": "Shadow Frenzy", "power_type": "strike", "damage_type": "physical", "damage": 10, "cost_mp": 0, "cost_stamina": 50, "cooldown": 4, "hits": 4, "is_signature": True,
                          "status_apply": "bleeding", "unevadable": True, "lifesteal": 0.15, "stat_mod": {"enemy": {"grace": -3}}, "mod_duration": 3},
     "drops": {"common": [{"id": "wolf_pelt", "chance": 0.5, "qty": [1, 1]}, {"id": "wild_herb", "chance": 0.4, "qty": [1, 1]}], "rare": [], "boss": [], "gold": [3, 10], "xp_mult": 1.1}},
    # ---- Oasis Outskirts (Sablewaste starter) ----
    {"id": "sand_scarab", "name": "Sand Scarab", "biome": "oasis_outskirts", "rarity": "common", "hp": 16,
     "creature_tier": "normal", "species": "monster", "archetype": "tank", "personality": "guardian",
     "stats": {"might": {"base": 12, "growth": 1.1}, "grace": {"base": 8, "growth": 0.8}, "cognition": {"base": 4, "growth": 0.5},
               "insight": {"base": 4, "growth": 0.5}, "essence": {"base": 6, "growth": 0.6}, "durability": {"base": 14, "growth": 1.3}},
     "life": {"mp": 0, "stamina": 90, "shield": 0},
     "passive_buff": {"type": "durability_bonus", "value": 0.12, "secondary": {"type": "might_bonus", "value": 0.08}},
     "profile_skills": {
         "attack": [{"id": "sand_scarab_pinch", "name": "Crushing Pincer", "power_type": "strike", "damage_type": "physical", "damage": 5, "cost_mp": 0, "cost_stamina": 20, "cooldown": 1, "trigger": "always",
                     "status_apply": "bleeding", "stat_mod": {"enemy": {"armor_bonus": -1}}, "mod_duration": 2}],
         "defense": [{"id": "sand_scarab_shell", "name": "Hardened Carapace", "power_type": "buff", "cost_mp": 0, "cost_stamina": 25, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 4, "durability": 2}}, "mod_duration": 3}],
         "utility": [{"id": "sand_scarab_burrow", "name": "Burrow", "power_type": "buff", "cost_mp": 0, "cost_stamina": 20, "cooldown": 3, "trigger": "always",
                      "self_status": "evasive", "stat_mod": {"self": {"grace": 2}}, "mod_duration": 2}],
     },
     "signature_fusion": {"id": "sand_scarab_sand_devour", "name": "Sand Devour", "power_type": "strike", "damage_type": "physical", "damage": 9, "cost_mp": 0, "cost_stamina": 50, "cooldown": 4, "hits": 2, "is_signature": True,
                          "status_apply": "stunned", "armor_ignore": True, "stat_mod": {"enemy": {"might": -2}}, "mod_duration": 3},
     "drops": {"common": [{"id": "scrap_bone", "chance": 0.5, "qty": [1, 1]}, {"id": "copper_ore", "chance": 0.3, "qty": [1, 1]}], "rare": [], "boss": [], "gold": [2, 8], "xp_mult": 1.0}},
    {"id": "desert_lizard", "name": "Desert Lizard", "biome": "oasis_outskirts", "rarity": "uncommon", "hp": 22,
     "creature_tier": "normal", "species": "beast", "archetype": "caster", "personality": "aggressive",
     "stats": {"might": {"base": 12, "growth": 1.1}, "grace": {"base": 10, "growth": 1.0}, "cognition": {"base": 8, "growth": 0.9},
               "insight": {"base": 12, "growth": 1.1}, "essence": {"base": 12, "growth": 1.1}, "durability": {"base": 10, "growth": 1.0}},
     "life": {"mp": 10, "stamina": 80, "shield": 0},
     "passive_buff": {"type": "might_bonus", "value": 0.13, "secondary": {"type": "evasion_bonus", "value": 0.10}},
     "profile_skills": {
         "attack": [{"id": "desert_lizard_bite", "name": "Savage Bite", "power_type": "strike", "damage_type": "physical", "damage": 6, "cost_mp": 0, "cost_stamina": 20, "cooldown": 1, "trigger": "always",
                     "status_apply": "bleeding", "stat_mod": {"enemy": {"might": -2}}, "mod_duration": 2},
                    {"id": "desert_lizard_acid_spit", "name": "Acid Spit", "power_type": "strike", "damage_type": "magical", "damage": 5, "cost_mp": 3, "cost_stamina": 0, "cooldown": 2, "trigger": "always",
                     "status_apply": "poisoned", "stat_mod": {"enemy": {"armor_bonus": -3}}, "mod_duration": 3}],
         "defense": [{"id": "desert_lizard_sand_veil", "name": "Sand Veil", "power_type": "buff", "cost_mp": 0, "cost_stamina": 25, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "evasive", "stat_mod": {"self": {"grace": 3}}, "mod_duration": 2}],
         "utility": [{"id": "desert_lizard_heat_bask", "name": "Heat Bask", "power_type": "heal", "cost_mp": 0, "cost_stamina": 20, "cooldown": 3, "trigger": "low_hp",
                      "heal_percent": 0.08, "self_status": "inspired"}],
     },
     "signature_fusion": {"id": "desert_lizard_solar_burn", "name": "Solar Burn", "power_type": "strike", "damage_type": "magical", "damage": 10, "cost_mp": 5, "cost_stamina": 0, "cooldown": 4, "hits": 2, "is_signature": True,
                          "status_apply": "burning", "stat_mod": {"enemy": {"might": -3, "armor_bonus": -3}}, "mod_duration": 3},
     "drops": {"common": [{"id": "scrap_bone", "chance": 0.5, "qty": [1, 1]}, {"id": "wild_herb", "chance": 0.3, "qty": [1, 1]}], "rare": [], "boss": [], "gold": [3, 10], "xp_mult": 1.1}},
    # ---- Tide Pools (Hylion starter) ----
    {"id": "tide_crab", "name": "Tide Crab", "biome": "tide_pools", "rarity": "common", "hp": 24,
     "creature_tier": "normal", "species": "beast", "archetype": "tank", "personality": "guardian",
     "stats": {"might": {"base": 13, "growth": 1.2}, "grace": {"base": 8, "growth": 0.8}, "cognition": {"base": 4, "growth": 0.5},
               "insight": {"base": 5, "growth": 0.5}, "essence": {"base": 6, "growth": 0.6}, "durability": {"base": 16, "growth": 1.4}},
     "life": {"mp": 0, "stamina": 90, "shield": 0},
     "passive_buff": {"type": "durability_bonus", "value": 0.14, "secondary": {"type": "might_bonus", "value": 0.08}},
     "profile_skills": {
         "attack": [{"id": "tide_crab_pinch", "name": "Crushing Pincer", "power_type": "strike", "damage_type": "physical", "damage": 6, "cost_mp": 0, "cost_stamina": 20, "cooldown": 1, "trigger": "always",
                     "status_apply": "bleeding", "stat_mod": {"enemy": {"armor_bonus": -2}}, "mod_duration": 2}],
         "defense": [{"id": "tide_crab_shell", "name": "Hardened Shell", "power_type": "buff", "cost_mp": 0, "cost_stamina": 25, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 5, "durability": 3}}, "mod_duration": 3}],
         "utility": [{"id": "tide_crab_bubble", "name": "Blinding Bubble", "power_type": "debuff", "damage_type": "magical", "damage": 2, "cost_mp": 2, "cost_stamina": 0, "cooldown": 2, "trigger": "opening_move",
                      "status_apply": "weary", "stat_mod": {"enemy": {"grace": -2, "cognition": -2}}, "mod_duration": 2}],
     },
     "signature_fusion": {"id": "tide_crab_tidal_crash", "name": "Tidal Crash", "power_type": "strike", "damage_type": "physical", "damage": 10, "cost_mp": 0, "cost_stamina": 50, "cooldown": 4, "hits": 2, "is_signature": True,
                          "status_apply": "stunned", "armor_ignore": True, "stat_mod": {"enemy": {"might": -3}}, "mod_duration": 3},
     "drops": {"common": [{"id": "sea_shell", "chance": 0.7, "qty": [1, 1]}, {"id": "sea_salt", "chance": 0.4, "qty": [1, 1]}], "rare": [], "boss": [], "gold": [2, 8], "xp_mult": 1.0}},
    {"id": "tide_crawler", "name": "Tide Crawler", "biome": "tide_pools", "rarity": "uncommon", "hp": 20,
     "creature_tier": "normal", "species": "beast", "archetype": "speed", "personality": "opportunist",
     "stats": {"might": {"base": 10, "growth": 1.0}, "grace": {"base": 14, "growth": 1.3}, "cognition": {"base": 10, "growth": 1.0},
               "insight": {"base": 12, "growth": 1.1}, "essence": {"base": 10, "growth": 1.0}, "durability": {"base": 8, "growth": 0.8}},
     "life": {"mp": 15, "stamina": 90, "shield": 0},
     "passive_buff": {"type": "grace_bonus", "value": 0.13, "secondary": {"type": "evasion_bonus", "value": 0.10}},
     "profile_skills": {
         "attack": [{"id": "tide_crawler_bite", "name": "Savage Bite", "power_type": "strike", "damage_type": "physical", "damage": 6, "cost_mp": 0, "cost_stamina": 20, "cooldown": 1, "trigger": "always",
                     "status_apply": "bleeding", "stat_mod": {"enemy": {"grace": -2}}, "mod_duration": 2},
                    {"id": "tide_crawler_water_splash", "name": "Water Splash", "power_type": "strike", "damage_type": "magical", "damage": 5, "cost_mp": 3, "cost_stamina": 0, "cooldown": 2, "trigger": "always",
                     "status_apply": "weary", "stat_mod": {"enemy": {"grace": -2}}, "mod_duration": 2}],
         "defense": [{"id": "tide_crawler_mist_veil", "name": "Mist Veil", "power_type": "buff", "cost_mp": 3, "cost_stamina": 0, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "evasive", "stat_mod": {"self": {"grace": 3, "essence": 2}}, "mod_duration": 2}],
         "utility": [{"id": "tide_crawler_healing_mist", "name": "Healing Mist", "power_type": "heal", "cost_mp": 4, "cost_stamina": 0, "cooldown": 3, "trigger": "low_hp",
                      "heal_percent": 0.08, "self_status": "warded"}],
     },
     "signature_fusion": {"id": "tide_crawler_tidal_devastation", "name": "Tidal Devastation", "power_type": "strike", "damage_type": "magical", "damage": 12, "cost_mp": 6, "cost_stamina": 0, "cooldown": 4, "hits": 2, "is_signature": True,
                          "status_apply": "weary", "unevadable": True, "stat_mod": {"enemy": {"grace": -4}}, "mod_duration": 3},
     "drops": {"common": [{"id": "sea_shell", "chance": 0.6, "qty": [1, 1]}, {"id": "sea_salt", "chance": 0.5, "qty": [1, 1]}], "rare": [{"id": "sea_pearl", "chance": 0.2, "qty": [1, 1]}], "boss": [], "gold": [5, 15], "xp_mult": 1.2}},
    # ---- Red Steppe (Mushkara Lv 6) ----
    {"id": "steppe_wolf", "name": "Steppe Wolf", "biome": "red_steppe", "rarity": "common", "hp": 36,
     "creature_tier": "normal", "species": "beast", "archetype": "striker", "personality": "aggressive",
     "stats": {"might": {"base": 18, "growth": 1.5}, "grace": {"base": 16, "growth": 1.4}, "cognition": {"base": 8, "growth": 0.9},
               "insight": {"base": 7, "growth": 0.8}, "essence": {"base": 8, "growth": 0.9}, "durability": {"base": 14, "growth": 1.2}},
     "life": {"mp": 0, "stamina": 110, "shield": 0},
     "passive_buff": {"type": "might_bonus", "value": 0.14, "secondary": {"type": "grace_bonus", "value": 0.10}},
     "profile_skills": {
         "attack": [{"id": "steppe_wolf_savage_maul", "name": "Savage Maul", "power_type": "strike", "damage_type": "physical", "damage": 10, "cost_mp": 0, "cost_stamina": 20, "cooldown": 1, "trigger": "always",
                     "status_apply": "bleeding", "stat_mod": {"enemy": {"might": -3}}, "mod_duration": 2}],
         "defense": [{"id": "steppe_wolf_pack_guard", "name": "Pack Guard", "power_type": "buff", "cost_mp": 0, "cost_stamina": 30, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 4, "grace": 3}}, "mod_duration": 2}],
         "utility": [{"id": "steppe_wolf_hunting_cry", "name": "Hunting Cry", "power_type": "buff", "cost_mp": 0, "cost_stamina": 30, "cooldown": 3, "trigger": "always",
                      "self_status": "inspired", "stat_mod": {"self": {"might": 4, "grace": 3}}, "mod_duration": 2}],
     },
     "signature_fusion": {"id": "steppe_wolf_blood_hunt", "name": "Blood Hunt", "power_type": "strike", "damage_type": "physical", "damage": 16, "cost_mp": 0, "cost_stamina": 50, "cooldown": 4, "hits": 3, "is_signature": True,
                          "status_apply": "bleeding", "lifesteal": 0.20, "stat_mod": {"enemy": {"grace": -4}}, "mod_duration": 3},
     "drops": {"common": [{"id": "wolf_pelt", "chance": 0.7, "qty": [1, 1]}, {"id": "wolf_fang", "chance": 0.5, "qty": [1, 1]}], "rare": [], "boss": [], "gold": [8, 20], "xp_mult": 1.2}},
    {"id": "warbeast_rhino", "name": "Warbeast Rhino", "biome": "red_steppe", "rarity": "uncommon", "hp": 50,
     "creature_tier": "normal", "species": "beast", "archetype": "bruiser", "personality": "aggressive",
     "stats": {"might": {"base": 22, "growth": 1.8}, "grace": {"base": 8, "growth": 0.8}, "cognition": {"base": 5, "growth": 0.5},
               "insight": {"base": 6, "growth": 0.6}, "essence": {"base": 8, "growth": 0.8}, "durability": {"base": 20, "growth": 1.6}},
     "life": {"mp": 0, "stamina": 130, "shield": 0},
     "passive_buff": {"type": "durability_bonus", "value": 0.15, "secondary": {"type": "might_bonus", "value": 0.12}},
     "profile_skills": {
         "attack": [{"id": "warbeast_rhino_gore", "name": "Goring Charge", "power_type": "strike", "damage_type": "physical", "damage": 12, "cost_mp": 0, "cost_stamina": 25, "cooldown": 1, "trigger": "always",
                     "status_apply": "stunned", "stat_mod": {"enemy": {"armor_bonus": -3}}, "mod_duration": 2},
                    {"id": "warbeast_rhio_stomp", "name": "Thunder Stomp", "power_type": "strike", "damage_type": "physical", "damage": 14, "cost_mp": 0, "cost_stamina": 35, "cooldown": 2, "trigger": "always",
                     "status_apply": "stunned", "stat_mod": {"enemy": {"grace": -3}}, "mod_duration": 2}],
         "defense": [{"id": "warbeast_rhino_iron_hide", "name": "Iron Hide", "power_type": "buff", "cost_mp": 0, "cost_stamina": 30, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 6, "durability": 4}}, "mod_duration": 3}],
         "utility": [{"id": "warbeast_rhino_rage", "name": "Beast Rage", "power_type": "buff", "cost_mp": 0, "cost_stamina": 25, "cooldown": 3, "trigger": "always",
                      "self_status": "inspired", "stat_mod": {"self": {"might": 5}}, "mod_duration": 2}],
     },
     "signature_fusion": {"id": "warbeast_rhino_apocalypse_charge", "name": "Apocalypse Charge", "power_type": "strike", "damage_type": "physical", "damage": 20, "cost_mp": 0, "cost_stamina": 50, "cooldown": 4, "hits": 1, "is_signature": True,
                          "status_apply": "stunned", "armor_ignore": True, "stat_mod": {"enemy": {"might": -5, "armor_bonus": -4}}, "mod_duration": 3},
     "drops": {"common": [{"id": "rhino_hide", "chance": 0.7, "qty": [1, 1]}, {"id": "rhino_horn", "chance": 0.3, "qty": [1, 1]}], "rare": [], "boss": [], "gold": [10, 25], "xp_mult": 1.3}},
    {"id": "steppe_warchief", "name": "Steppe Warchief", "biome": "red_steppe", "rarity": "rare", "hp": 65,
     "creature_tier": "mini_boss", "species": "humanoid", "archetype": "bruiser", "personality": "aggressive",
     "stats": {"might": {"base": 26, "growth": 2.0}, "grace": {"base": 12, "growth": 1.1}, "cognition": {"base": 10, "growth": 1.0},
               "insight": {"base": 8, "growth": 0.8}, "essence": {"base": 10, "growth": 1.0}, "durability": {"base": 22, "growth": 1.8}},
     "life": {"mp": 10, "stamina": 140, "shield": 0},
     "passive_buff": [{"type": "might_bonus", "value": 0.18}, {"type": "durability_bonus", "value": 0.12}],
     "profile_skills": {
         "attack": [{"id": "steppe_warchief_cleave", "name": "Warlord's Cleave", "power_type": "strike", "damage_type": "physical", "damage": 16, "cost_mp": 0, "cost_stamina": 25, "cooldown": 1, "trigger": "always",
                     "status_apply": "bleeding", "stat_mod": {"enemy": {"armor_bonus": -3}}, "mod_duration": 2},
                    {"id": "steppe_warchief_skull_crush", "name": "Skull Crusher", "power_type": "strike", "damage_type": "physical", "damage": 20, "cost_mp": 0, "cost_stamina": 35, "cooldown": 2, "trigger": "always",
                     "status_apply": "stunned", "stat_mod": {"enemy": {"cognition": -4}}, "mod_duration": 3}],
         "defense": [{"id": "steppe_warchief_iron_will", "name": "Iron Will", "power_type": "buff", "cost_mp": 0, "cost_stamina": 30, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 6, "might": 5}}, "mod_duration": 3}],
         "utility": [{"id": "steppe_warchief_rally", "name": "Rally Horde", "power_type": "buff", "cost_mp": 5, "cost_stamina": 30, "cooldown": 3, "trigger": "always",
                      "self_status": "inspired", "stat_mod": {"self": {"might": 5, "grace": 3}}, "mod_duration": 3}],
     },
     "signature_fusion": {"id": "steppe_warchief_bloodlust", "name": "Bloodlust Frenzy", "power_type": "strike", "damage_type": "physical", "damage": 24, "cost_mp": 0, "cost_stamina": 50, "cooldown": 4, "hits": 3, "is_signature": True,
                          "status_apply": "bleeding", "lifesteal": 0.25, "stat_mod": {"enemy": {"might": -5}}, "mod_duration": 4},
     "drops": {"common": [{"id": "iron_ore", "chance": 0.8, "qty": [1, 2]}], "rare": [{"id": "warchief_bloodblade", "chance": 0.15, "qty": [1, 1]}], "boss": [{"id": "bloodiron_ingot", "chance": 0.3, "qty": [1, 1]}], "gold": [20, 40], "xp_mult": 1.5}},
    # ---- Iron Scar (Mushkara Lv 10) ----
    {"id": "iron_wolf", "name": "Iron Wolf", "biome": "iron_scar", "rarity": "common", "hp": 48,
     "creature_tier": "normal", "species": "beast", "archetype": "striker", "personality": "aggressive",
     "stats": {"might": {"base": 22, "growth": 1.8}, "grace": {"base": 18, "growth": 1.5}, "cognition": {"base": 10, "growth": 1.0},
               "insight": {"base": 8, "growth": 0.8}, "essence": {"base": 10, "growth": 1.0}, "durability": {"base": 16, "growth": 1.4}},
     "life": {"mp": 0, "stamina": 110, "shield": 0},
     "passive_buff": {"type": "might_bonus", "value": 0.16, "secondary": {"type": "grace_bonus", "value": 0.12}},
     "profile_skills": {
         "attack": [{"id": "iron_wolf_fang_rip", "name": "Fang Rip", "power_type": "strike", "damage_type": "physical", "damage": 14, "cost_mp": 0, "cost_stamina": 20, "cooldown": 1, "trigger": "always",
                     "status_apply": "bleeding", "stat_mod": {"enemy": {"might": -3}}, "mod_duration": 2}],
         "defense": [{"id": "iron_wolf_guard", "name": "Iron Guard", "power_type": "buff", "cost_mp": 0, "cost_stamina": 30, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 5, "grace": 3}}, "mod_duration": 2}],
         "utility": [{"id": "iron_wolf_ferocious_howl", "name": "Ferocious Howl", "power_type": "debuff", "damage_type": "physical", "damage": 4, "cost_mp": 0, "cost_stamina": 25, "cooldown": 2, "trigger": "opening_move",
                      "status_apply": "weary", "stat_mod": {"enemy": {"might": -3, "grace": -3}}, "mod_duration": 3}],
     },
     "signature_fusion": {"id": "iron_wolf_metal_storm", "name": "Metal Storm", "power_type": "strike", "damage_type": "physical", "damage": 18, "cost_mp": 0, "cost_stamina": 50, "cooldown": 4, "hits": 3, "is_signature": True,
                          "status_apply": "bleeding", "lifesteal": 0.20, "stat_mod": {"enemy": {"grace": -4}}, "mod_duration": 3},
     "drops": {"common": [{"id": "iron_ore", "chance": 0.7, "qty": [1, 1]}, {"id": "wolf_fang", "chance": 0.5, "qty": [1, 1]}], "rare": [], "boss": [], "gold": [10, 25], "xp_mult": 1.3}},
    {"id": "battle_wraith", "name": "Battle Wraith", "biome": "iron_scar", "rarity": "uncommon", "hp": 42,
     "creature_tier": "normal", "species": "undead", "archetype": "caster", "personality": "opportunist",
     "tags": ["undead"],
     "stats": {"might": {"base": 8, "growth": 0.8}, "grace": {"base": 14, "growth": 1.3}, "cognition": {"base": 18, "growth": 1.6},
               "insight": {"base": 20, "growth": 1.7}, "essence": {"base": 16, "growth": 1.4}, "durability": {"base": 12, "growth": 1.0}},
     "life": {"mp": 25, "stamina": 80, "shield": 0},
     "passive_buff": {"type": "cognition_bonus", "value": 0.18, "secondary": {"type": "lifesteal", "value": 0.12}},
     "profile_skills": {
         "attack": [{"id": "battle_wraith_soul_drain", "name": "Soul Drain", "power_type": "strike", "damage_type": "magical", "damage": 12, "cost_mp": 4, "cost_stamina": 0, "cooldown": 1, "trigger": "always",
                     "lifesteal": 0.20, "stat_mod": {"enemy": {"essence": -3}}, "mod_duration": 2},
                    {"id": "battle_wraith_death_grip", "name": "Death Grip", "power_type": "strike", "damage_type": "magical", "damage": 14, "cost_mp": 6, "cost_stamina": 0, "cooldown": 2, "trigger": "opponent_wounded",
                     "status_apply": "weary", "stat_mod": {"enemy": {"grace": -4}}, "mod_duration": 3}],
         "defense": [{"id": "battle_wraith_phase_shift", "name": "Phase Shift", "power_type": "buff", "cost_mp": 4, "cost_stamina": 0, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "evasive", "stat_mod": {"self": {"grace": 5, "essence": 3}}, "mod_duration": 2}],
         "utility": [{"id": "battle_wraith_terror", "name": "Terror", "power_type": "debuff", "damage_type": "magical", "damage": 4, "cost_mp": 4, "cost_stamina": 0, "cooldown": 2, "trigger": "opening_move",
                      "status_apply": "weary", "stat_mod": {"enemy": {"might": -4, "cognition": -3}}, "mod_duration": 3}],
     },
     "signature_fusion": {"id": "battle_wraith_soul_tempest", "name": "Soul Tempest", "power_type": "strike", "damage_type": "magical", "damage": 20, "cost_mp": 10, "cost_stamina": 0, "cooldown": 4, "hits": 2, "is_signature": True,
                          "status_apply": "poisoned", "lifesteal": 0.25, "stat_mod": {"enemy": {"essence": -5, "insight": -4}}, "mod_duration": 4},
     "drops": {"common": [{"id": "relic_shard", "chance": 0.6, "qty": [1, 1]}, {"id": "ghast_dust", "chance": 0.4, "qty": [1, 1]}], "rare": [{"id": "bloodiron_ingot", "chance": 0.1, "qty": [1, 1]}], "boss": [], "gold": [15, 30], "xp_mult": 1.4}},
    {"id": "iron_scar_titan", "name": "Iron Scar Titan", "biome": "iron_scar", "rarity": "rare", "hp": 80,
     "creature_tier": "mini_boss", "species": "construct", "archetype": "tank", "personality": "guardian",
     "tags": ["construct"],
     "stats": {"might": {"base": 28, "growth": 2.2}, "grace": {"base": 8, "growth": 0.8}, "cognition": {"base": 6, "growth": 0.6},
               "insight": {"base": 6, "growth": 0.6}, "essence": {"base": 12, "growth": 1.0}, "durability": {"base": 28, "growth": 2.2}},
     "life": {"mp": 0, "stamina": 150, "shield": 10},
     "passive_buff": [{"type": "durability_bonus", "value": 0.20}, {"type": "might_bonus", "value": 0.15}],
     "profile_skills": {
         "attack": [{"id": "iron_titan_slam", "name": "Iron Slam", "power_type": "strike", "damage_type": "physical", "damage": 20, "cost_mp": 0, "cost_stamina": 25, "cooldown": 1, "trigger": "always",
                     "status_apply": "stunned", "stat_mod": {"enemy": {"armor_bonus": -4}}, "mod_duration": 2},
                    {"id": "iron_titan_quake", "name": "Scar Quake", "power_type": "strike", "damage_type": "physical", "damage": 24, "cost_mp": 0, "cost_stamina": 35, "cooldown": 2, "trigger": "always",
                     "status_apply": "stunned", "stat_mod": {"enemy": {"grace": -4, "might": -3}}, "mod_duration": 3}],
         "defense": [{"id": "iron_titan_bulwark", "name": "Iron Bulwark", "power_type": "buff", "cost_mp": 0, "cost_stamina": 30, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 8, "durability": 5}}, "mod_duration": 3}],
         "utility": [{"id": "iron_titan_metal_shriek", "name": "Metal Shriek", "power_type": "debuff", "damage_type": "physical", "damage": 5, "cost_mp": 0, "cost_stamina": 30, "cooldown": 2, "trigger": "opening_move",
                      "status_apply": "weary", "stat_mod": {"enemy": {"cognition": -4, "grace": -3}}, "mod_duration": 3}],
     },
     "signature_fusion": {"id": "iron_titan_cataclysm_slam", "name": "Cataclysm Slam", "power_type": "strike", "damage_type": "physical", "damage": 30, "cost_mp": 0, "cost_stamina": 50, "cooldown": 4, "hits": 1, "is_signature": True,
                          "status_apply": "stunned", "armor_ignore": True, "stat_mod": {"enemy": {"might": -6, "armor_bonus": -5}}, "mod_duration": 4},
     "drops": {"common": [{"id": "iron_ore", "chance": 0.9, "qty": [2, 3]}], "rare": [{"id": "bloodiron_ingot", "chance": 0.2, "qty": [1, 1]}], "boss": [{"id": "titan_core", "chance": 0.25, "qty": [1, 1]}], "gold": [25, 50], "xp_mult": 1.6}},
    # ---- Ash Barrens (Mushkara Lv 16) ----
    {"id": "ash_crawler", "name": "Ash Crawler", "biome": "ash_barrens", "rarity": "common", "hp": 55,
     "creature_tier": "normal", "species": "monster", "archetype": "bruiser", "personality": "aggressive",
     "stats": {"might": {"base": 24, "growth": 2.0}, "grace": {"base": 10, "growth": 1.0}, "cognition": {"base": 8, "growth": 0.8},
               "insight": {"base": 10, "growth": 1.0}, "essence": {"base": 14, "growth": 1.2}, "durability": {"base": 20, "growth": 1.6}},
     "life": {"mp": 10, "stamina": 100, "shield": 0},
     "passive_buff": {"type": "might_bonus", "value": 0.16, "secondary": {"type": "essence_bonus", "value": 0.12}},
     "profile_skills": {
         "attack": [{"id": "ash_crawler_ember_claw", "name": "Ember Claw", "power_type": "strike", "damage_type": "magical", "damage": 16, "cost_mp": 3, "cost_stamina": 20, "cooldown": 1, "trigger": "always",
                     "status_apply": "burning", "stat_mod": {"enemy": {"armor_bonus": -3}}, "mod_duration": 2}],
         "defense": [{"id": "ash_crawler_ash_armor", "name": "Ash Armor", "power_type": "buff", "cost_mp": 3, "cost_stamina": 25, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 6, "essence": 4}}, "mod_duration": 3}],
         "utility": [{"id": "ash_crawler_smoke_veil", "name": "Smoke Veil", "power_type": "buff", "cost_mp": 3, "cost_stamina": 20, "cooldown": 3, "trigger": "always",
                      "self_status": "evasive", "stat_mod": {"self": {"grace": 4}}, "mod_duration": 2}],
     },
     "signature_fusion": {"id": "ash_crawler_ember_storm", "name": "Ember Storm", "power_type": "strike", "damage_type": "magical", "damage": 22, "cost_mp": 8, "cost_stamina": 0, "cooldown": 4, "hits": 3, "is_signature": True,
                          "status_apply": "burning", "stat_mod": {"enemy": {"might": -4, "armor_bonus": -4}}, "mod_duration": 3},
     "drops": {"common": [{"id": "ash_dust", "chance": 0.7, "qty": [1, 1]}, {"id": "ember_shard", "chance": 0.4, "qty": [1, 1]}], "rare": [], "boss": [], "gold": [15, 30], "xp_mult": 1.4}},
    {"id": "magma_serpent", "name": "Magma Serpent", "biome": "ash_barrens", "rarity": "uncommon", "hp": 60,
     "creature_tier": "normal", "species": "beast", "archetype": "caster", "personality": "aggressive",
     "stats": {"might": {"base": 14, "growth": 1.2}, "grace": {"base": 16, "growth": 1.4}, "cognition": {"base": 16, "growth": 1.4},
               "insight": {"base": 18, "growth": 1.5}, "essence": {"base": 20, "growth": 1.6}, "durability": {"base": 14, "growth": 1.2}},
     "life": {"mp": 30, "stamina": 80, "shield": 0},
     "passive_buff": {"type": "essence_bonus", "value": 0.18, "secondary": {"type": "magic_resist", "value": 0.12}},
     "profile_skills": {
         "attack": [{"id": "magma_serpent_lava_spit", "name": "Lava Spit", "power_type": "strike", "damage_type": "magical", "damage": 16, "cost_mp": 4, "cost_stamina": 0, "cooldown": 1, "trigger": "always",
                     "status_apply": "burning", "stat_mod": {"enemy": {"armor_bonus": -4}}, "mod_duration": 3},
                    {"id": "magma_serpent_magma_bite", "name": "Magma Bite", "power_type": "strike", "damage_type": "magical", "damage": 18, "cost_mp": 6, "cost_stamina": 0, "cooldown": 2, "trigger": "always",
                     "status_apply": "burning", "stat_mod": {"enemy": {"might": -4}}, "mod_duration": 3}],
         "defense": [{"id": "magma_serpent_heat_shield", "name": "Heat Shield", "power_type": "buff", "cost_mp": 5, "cost_stamina": 0, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 5, "essence": 4}}, "mod_duration": 3}],
         "utility": [{"id": "magma_serpent_volcanic_gas", "name": "Volcanic Gas", "power_type": "debuff", "damage_type": "magical", "damage": 5, "cost_mp": 5, "cost_stamina": 0, "cooldown": 2, "trigger": "opening_move",
                      "status_apply": "poisoned", "stat_mod": {"enemy": {"cognition": -4, "grace": -3}}, "mod_duration": 3}],
     },
     "signature_fusion": {"id": "magma_serpent_eruption", "name": "Eruption", "power_type": "strike", "damage_type": "magical", "damage": 24, "cost_mp": 12, "cost_stamina": 0, "cooldown": 4, "hits": 2, "is_signature": True,
                          "status_apply": "burning", "unevadable": True, "stat_mod": {"enemy": {"might": -5, "armor_bonus": -5}}, "mod_duration": 4},
     "drops": {"common": [{"id": "ember_shard", "chance": 0.6, "qty": [1, 1]}, {"id": "magma_scale", "chance": 0.4, "qty": [1, 1]}], "rare": [{"id": "fire_crystal", "chance": 0.1, "qty": [1, 1]}], "boss": [], "gold": [20, 35], "xp_mult": 1.5}},
    {"id": "ash_barrens_warlord", "name": "Ash Barrens Warlord", "biome": "ash_barrens", "rarity": "rare", "hp": 95,
     "creature_tier": "mini_boss", "species": "humanoid", "archetype": "bruiser", "personality": "aggressive",
     "stats": {"might": {"base": 32, "growth": 2.5}, "grace": {"base": 14, "growth": 1.2}, "cognition": {"base": 12, "growth": 1.0},
               "insight": {"base": 10, "growth": 0.9}, "essence": {"base": 16, "growth": 1.4}, "durability": {"base": 26, "growth": 2.0}},
     "life": {"mp": 20, "stamina": 150, "shield": 5},
     "passive_buff": [{"type": "might_bonus", "value": 0.22}, {"type": "essence_bonus", "value": 0.15}],
     "profile_skills": {
         "attack": [{"id": "ash_warlord_flame_cleave", "name": "Flame Cleave", "power_type": "strike", "damage_type": "magical", "damage": 24, "cost_mp": 5, "cost_stamina": 25, "cooldown": 1, "trigger": "always",
                     "status_apply": "burning", "stat_mod": {"enemy": {"armor_bonus": -4}}, "mod_duration": 3},
                    {"id": "ash_warlord_meteor_slam", "name": "Meteor Slam", "power_type": "strike", "damage_type": "magical", "damage": 28, "cost_mp": 8, "cost_stamina": 35, "cooldown": 2, "trigger": "always",
                     "status_apply": "stunned", "stat_mod": {"enemy": {"might": -5}}, "mod_duration": 3}],
         "defense": [{"id": "ash_warlord_magma_skin", "name": "Magma Skin", "power_type": "buff", "cost_mp": 5, "cost_stamina": 30, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 8, "essence": 5}}, "mod_duration": 3}],
         "utility": [{"id": "ash_warlord_battle_roar", "name": "Battle Roar", "power_type": "buff", "cost_mp": 5, "cost_stamina": 30, "cooldown": 3, "trigger": "always",
                      "self_status": "inspired", "stat_mod": {"self": {"might": 6, "essence": 4}}, "mod_duration": 3}],
     },
     "signature_fusion": {"id": "ash_warlord_inferno", "name": "Warlord's Inferno", "power_type": "strike", "damage_type": "magical", "damage": 34, "cost_mp": 15, "cost_stamina": 0, "cooldown": 4, "hits": 3, "is_signature": True,
                          "status_apply": "burning", "armor_ignore": True, "stat_mod": {"enemy": {"might": -6, "armor_bonus": -6}}, "mod_duration": 4},
     "drops": {"common": [{"id": "ember_shard", "chance": 0.8, "qty": [1, 2]}], "rare": [{"id": "fire_crystal", "chance": 0.2, "qty": [1, 1]}], "boss": [{"id": "warlord_crown", "chance": 0.2, "qty": [1, 1]}], "gold": [30, 60], "xp_mult": 1.7}},
    # ---- Demonfall Crater (Mushkara Lv 24) ----
    {"id": "demon_spawn", "name": "Demon Spawn", "biome": "demonfall_crater", "rarity": "common", "hp": 70,
     "creature_tier": "normal", "species": "demon", "archetype": "striker", "personality": "aggressive",
     "tags": ["demon"],
     "stats": {"might": {"base": 30, "growth": 2.4}, "grace": {"base": 18, "growth": 1.5}, "cognition": {"base": 12, "growth": 1.0},
               "insight": {"base": 14, "growth": 1.2}, "essence": {"base": 18, "growth": 1.5}, "durability": {"base": 20, "growth": 1.6}},
     "life": {"mp": 20, "stamina": 120, "shield": 0},
     "passive_buff": {"type": "might_bonus", "value": 0.20, "secondary": {"type": "essence_bonus", "value": 0.15}},
     "profile_skills": {
         "attack": [{"id": "demon_spawn_hellstrike", "name": "Hellstrike", "power_type": "strike", "damage_type": "magical", "damage": 22, "cost_mp": 4, "cost_stamina": 20, "cooldown": 1, "trigger": "always",
                     "status_apply": "burning", "stat_mod": {"enemy": {"might": -4}}, "mod_duration": 3}],
         "defense": [{"id": "demon_spawn_infernal_hide", "name": "Infernal Hide", "power_type": "buff", "cost_mp": 4, "cost_stamina": 25, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 7, "essence": 5}}, "mod_duration": 3}],
         "utility": [{"id": "demon_spawn_fear_aura", "name": "Demonic Fear", "power_type": "debuff", "damage_type": "magical", "damage": 6, "cost_mp": 5, "cost_stamina": 0, "cooldown": 2, "trigger": "opening_move",
                      "status_apply": "weary", "stat_mod": {"enemy": {"might": -5, "cognition": -4}}, "mod_duration": 3}],
     },
     "signature_fusion": {"id": "demon_spawn_hellfire", "name": "Hellfire Burst", "power_type": "strike", "damage_type": "magical", "damage": 28, "cost_mp": 10, "cost_stamina": 0, "cooldown": 4, "hits": 3, "is_signature": True,
                          "status_apply": "burning", "lifesteal": 0.20, "stat_mod": {"enemy": {"might": -5}}, "mod_duration": 4},
     "drops": {"common": [{"id": "demon_ash", "chance": 0.7, "qty": [1, 1]}, {"id": "infernal_shard", "chance": 0.3, "qty": [1, 1]}], "rare": [], "boss": [], "gold": [25, 50], "xp_mult": 1.6}},
    {"id": "demonfall_warden", "name": "Demonfall Warden", "biome": "demonfall_crater", "rarity": "legendary", "hp": 140,
     "creature_tier": "boss", "species": "demon", "archetype": "bruiser", "personality": "aggressive",
     "tags": ["demon"],
     "stats": {"might": {"base": 40, "growth": 3.0}, "grace": {"base": 18, "growth": 1.5}, "cognition": {"base": 16, "growth": 1.3},
               "insight": {"base": 18, "growth": 1.5}, "essence": {"base": 24, "growth": 2.0}, "durability": {"base": 34, "growth": 2.6}},
     "life": {"mp": 40, "stamina": 160, "shield": 15},
     "is_boss": True,
     "passive_buff": [{"type": "might_bonus", "value": 0.25}, {"type": "essence_bonus", "value": 0.20}, {"type": "durability_bonus", "value": 0.18}],
     "boss_aura": {"id": "infernal_aura", "name": "Infernal Aura", "effect": "burning", "desc": "All enemies take burn damage each turn."},
     "profile_skills": {
         "attack": [{"id": "demon_warden_hell_cleave", "name": "Hell Cleave", "power_type": "strike", "damage_type": "magical", "damage": 30, "cost_mp": 6, "cost_stamina": 25, "cooldown": 1, "trigger": "always",
                     "status_apply": "burning", "stat_mod": {"enemy": {"armor_bonus": -5}}, "mod_duration": 3},
                    {"id": "demon_warden_doom_strike", "name": "Doom Strike", "power_type": "strike", "damage_type": "magical", "damage": 36, "cost_mp": 10, "cost_stamina": 35, "cooldown": 2, "trigger": "always",
                     "status_apply": "stunned", "stat_mod": {"enemy": {"might": -6}}, "mod_duration": 3}],
         "defense": [{"id": "demon_warden_infernal_bulwark", "name": "Infernal Bulwark", "power_type": "buff", "cost_mp": 6, "cost_stamina": 30, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 10, "essence": 6}}, "mod_duration": 3},
                    {"id": "demon_warden_soul_armor", "name": "Soul Armor", "power_type": "heal", "cost_mp": 8, "cost_stamina": 0, "cooldown": 4, "trigger": "low_hp",
                      "heal_percent": 0.12, "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 5}}, "mod_duration": 3}],
         "utility": [{"id": "demon_warden_demonic_roar", "name": "Demonic Roar", "power_type": "debuff", "damage_type": "magical", "damage": 8, "cost_mp": 8, "cost_stamina": 0, "cooldown": 3, "trigger": "opening_move",
                      "status_apply": "weary", "stat_mod": {"enemy": {"might": -6, "cognition": -5, "grace": -4}}, "mod_duration": 4}],
     },
     "signature_fusion": [{"id": "demon_warden_cataclysm", "name": "Cataclysm", "power_type": "strike", "damage_type": "magical", "damage": 48, "cost_mp": 20, "cost_stamina": 0, "cooldown": 5, "hits": 3, "is_signature": True,
                          "status_apply": "burning", "armor_ignore": True, "stat_mod": {"enemy": {"might": -8, "armor_bonus": -8}}, "mod_duration": 4},
                         {"id": "demon_warden_soul_devour", "name": "Soul Devour", "power_type": "strike", "damage_type": "magical", "damage": 40, "cost_mp": 15, "cost_stamina": 0, "cooldown": 4, "hits": 1, "is_signature": True,
                          "lifesteal": 0.40, "stat_mod": {"enemy": {"essence": -8, "insight": -6}}, "mod_duration": 4}],
     "drops": {"common": [{"id": "infernal_shard", "chance": 0.9, "qty": [1, 2]}], "rare": [{"id": "demon_heart", "chance": 0.3, "qty": [1, 1]}], "boss": [{"id": "warden_helm", "chance": 0.15, "qty": [1, 1]}, {"id": "demon_soul", "chance": 0.1, "qty": [1, 1]}], "gold": [50, 100], "xp_mult": 2.0}},
    # ---- Mosaic Coast (Concordia Lv 12) ----
    {"id": "smuggler_rogue", "name": "Smuggler Rogue", "biome": "mosaic_coast", "rarity": "common", "hp": 48,
     "creature_tier": "normal", "species": "humanoid", "archetype": "speed", "personality": "opportunist",
     "stats": {"might": {"base": 16, "growth": 1.4}, "grace": {"base": 20, "growth": 1.6}, "cognition": {"base": 14, "growth": 1.2},
               "insight": {"base": 16, "growth": 1.3}, "essence": {"base": 8, "growth": 0.8}, "durability": {"base": 12, "growth": 1.0}},
     "life": {"mp": 5, "stamina": 110, "shield": 0},
     "passive_buff": {"type": "grace_bonus", "value": 0.16, "secondary": {"type": "evasion_bonus", "value": 0.12}},
     "profile_skills": {
         "attack": [{"id": "smuggler_backstab", "name": "Backstab", "power_type": "strike", "damage_type": "physical", "damage": 14, "cost_mp": 0, "cost_stamina": 20, "cooldown": 1, "trigger": "always",
                     "status_apply": "bleeding", "stat_mod": {"enemy": {"grace": -3}}, "mod_duration": 2}],
         "defense": [{"id": "smuggler_dodge", "name": "Slippery Dodge", "power_type": "buff", "cost_mp": 0, "cost_stamina": 20, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "evasive", "stat_mod": {"self": {"grace": 5}}, "mod_duration": 2}],
         "utility": [{"id": "smuggler_smoke_bomb", "name": "Smoke Bomb", "power_type": "debuff", "damage_type": "physical", "damage": 3, "cost_mp": 0, "cost_stamina": 25, "cooldown": 2, "trigger": "opening_move",
                      "status_apply": "weary", "stat_mod": {"enemy": {"cognition": -4, "grace": -3}}, "mod_duration": 3}],
     },
     "signature_fusion": {"id": "smuggler_shadow_strike", "name": "Shadow Strike", "power_type": "strike", "damage_type": "physical", "damage": 18, "cost_mp": 0, "cost_stamina": 50, "cooldown": 4, "hits": 3, "is_signature": True,
                          "status_apply": "bleeding", "unevadable": True, "stat_mod": {"enemy": {"grace": -4}}, "mod_duration": 3},
     "drops": {"common": [{"id": "coin_purse", "chance": 0.8, "qty": [1, 1]}], "rare": [{"id": "smuggler_dagger", "chance": 0.1, "qty": [1, 1]}], "boss": [], "gold": [15, 30], "xp_mult": 1.3}},
    {"id": "coastal_serpent", "name": "Coastal Serpent", "biome": "mosaic_coast", "rarity": "uncommon", "hp": 55,
     "creature_tier": "normal", "species": "beast", "archetype": "caster", "personality": "opportunist",
     "stats": {"might": {"base": 12, "growth": 1.0}, "grace": {"base": 16, "growth": 1.4}, "cognition": {"base": 16, "growth": 1.4},
               "insight": {"base": 18, "growth": 1.5}, "essence": {"base": 18, "growth": 1.5}, "durability": {"base": 14, "growth": 1.2}},
     "life": {"mp": 25, "stamina": 80, "shield": 0},
     "passive_buff": {"type": "essence_bonus", "value": 0.16, "secondary": {"type": "grace_bonus", "value": 0.12}},
     "profile_skills": {
         "attack": [{"id": "coastal_serpent_venom_bite", "name": "Venom Bite", "power_type": "strike", "damage_type": "physical", "damage": 12, "cost_mp": 0, "cost_stamina": 20, "cooldown": 1, "trigger": "always",
                     "status_apply": "poisoned", "stat_mod": {"enemy": {"might": -3}}, "mod_duration": 3},
                    {"id": "coastal_serpent_water_jet", "name": "Water Jet", "power_type": "strike", "damage_type": "magical", "damage": 14, "cost_mp": 4, "cost_stamina": 0, "cooldown": 2, "trigger": "always",
                     "status_apply": "weary", "stat_mod": {"enemy": {"grace": -3}}, "mod_duration": 2}],
         "defense": [{"id": "coastal_serpent_scales", "name": "Wet Scales", "power_type": "buff", "cost_mp": 3, "cost_stamina": 0, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 5, "essence": 3}}, "mod_duration": 2}],
         "utility": [{"id": "coastal_serpent_ink_cloud", "name": "Ink Cloud", "power_type": "debuff", "damage_type": "magical", "damage": 3, "cost_mp": 4, "cost_stamina": 0, "cooldown": 2, "trigger": "opening_move",
                      "status_apply": "weary", "stat_mod": {"enemy": {"cognition": -4, "grace": -3}}, "mod_duration": 3}],
     },
     "signature_fusion": {"id": "coastal_serpent_tidal_surge", "name": "Tidal Surge", "power_type": "strike", "damage_type": "magical", "damage": 20, "cost_mp": 10, "cost_stamina": 0, "cooldown": 4, "hits": 2, "is_signature": True,
                          "status_apply": "poisoned", "unevadable": True, "stat_mod": {"enemy": {"grace": -5}}, "mod_duration": 3},
     "drops": {"common": [{"id": "sea_shell", "chance": 0.6, "qty": [1, 1]}, {"id": "sea_pearl", "chance": 0.2, "qty": [1, 1]}], "rare": [], "boss": [], "gold": [15, 30], "xp_mult": 1.4}},
    {"id": "mosaic_coast_pirate_lord", "name": "Pirate Lord", "biome": "mosaic_coast", "rarity": "rare", "hp": 85,
     "creature_tier": "mini_boss", "species": "humanoid", "archetype": "bruiser", "personality": "aggressive",
     "stats": {"might": {"base": 26, "growth": 2.0}, "grace": {"base": 18, "growth": 1.5}, "cognition": {"base": 16, "growth": 1.3},
               "insight": {"base": 14, "growth": 1.2}, "essence": {"base": 12, "growth": 1.0}, "durability": {"base": 20, "growth": 1.6}},
     "life": {"mp": 10, "stamina": 140, "shield": 0},
     "passive_buff": [{"type": "grace_bonus", "value": 0.18}, {"type": "might_bonus", "value": 0.15}],
     "profile_skills": {
         "attack": [{"id": "pirate_lord_cutlass", "name": "Cutlass Flurry", "power_type": "strike", "damage_type": "physical", "damage": 20, "cost_mp": 0, "cost_stamina": 25, "cooldown": 1, "trigger": "always",
                     "status_apply": "bleeding", "stat_mod": {"enemy": {"armor_bonus": -3}}, "mod_duration": 2},
                    {"id": "pirate_lord_pistol_shot", "name": "Pistol Shot", "power_type": "strike", "damage_type": "physical", "damage": 24, "cost_mp": 0, "cost_stamina": 35, "cooldown": 2, "trigger": "always",
                     "status_apply": "stunned", "armor_ignore": True, "stat_mod": {"enemy": {"grace": -4}}, "mod_duration": 2}],
         "defense": [{"id": "pirate_lord_parrry", "name": "Parry Stance", "power_type": "buff", "cost_mp": 0, "cost_stamina": 30, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "warded", "stat_mod": {"self": {"grace": 5, "armor_bonus": 5}}, "mod_duration": 3}],
         "utility": [{"id": "pirate_lord_crew_rally", "name": "Crew Rally", "power_type": "buff", "cost_mp": 5, "cost_stamina": 30, "cooldown": 3, "trigger": "always",
                      "self_status": "inspired", "stat_mod": {"self": {"might": 5, "grace": 4}}, "mod_duration": 3}],
     },
     "signature_fusion": {"id": "pirate_lord_broadside", "name": "Broadside Barrage", "power_type": "strike", "damage_type": "physical", "damage": 28, "cost_mp": 0, "cost_stamina": 50, "cooldown": 4, "hits": 4, "is_signature": True,
                          "status_apply": "stunned", "armor_ignore": True, "stat_mod": {"enemy": {"might": -5, "grace": -5}}, "mod_duration": 3},
     "drops": {"common": [{"id": "coin_purse", "chance": 0.9, "qty": [1, 2]}], "rare": [{"id": "pirate_cutlass", "chance": 0.15, "qty": [1, 1]}], "boss": [{"id": "captain_compass", "chance": 0.2, "qty": [1, 1]}], "gold": [30, 60], "xp_mult": 1.6}},
    # ---- Amber Vineyards (Concordia Lv 14) ----
    {"id": "amber_wasp", "name": "Amber Wasp", "biome": "amber_vineyards", "rarity": "common", "hp": 40,
     "creature_tier": "normal", "species": "beast", "archetype": "speed", "personality": "aggressive",
     "stats": {"might": {"base": 14, "growth": 1.2}, "grace": {"base": 20, "growth": 1.6}, "cognition": {"base": 10, "growth": 0.9},
               "insight": {"base": 12, "growth": 1.0}, "essence": {"base": 14, "growth": 1.2}, "durability": {"base": 10, "growth": 0.9}},
     "life": {"mp": 10, "stamina": 100, "shield": 0},
     "passive_buff": {"type": "grace_bonus", "value": 0.18, "secondary": {"type": "essence_bonus", "value": 0.10}},
     "profile_skills": {
         "attack": [{"id": "amber_wasp_stinger", "name": "Venom Stinger", "power_type": "strike", "damage_type": "physical", "damage": 12, "cost_mp": 0, "cost_stamina": 15, "cooldown": 1, "trigger": "always",
                     "status_apply": "poisoned", "stat_mod": {"enemy": {"grace": -3}}, "mod_duration": 3}],
         "defense": [{"id": "amber_wasp_swift_dart", "name": "Swift Dart", "power_type": "buff", "cost_mp": 0, "cost_stamina": 20, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "evasive", "stat_mod": {"self": {"grace": 5}}, "mod_duration": 2}],
         "utility": [{"id": "amber_wasp_buzz", "name": "Disorienting Buzz", "power_type": "debuff", "damage_type": "magical", "damage": 3, "cost_mp": 2, "cost_stamina": 0, "cooldown": 2, "trigger": "opening_move",
                      "status_apply": "weary", "stat_mod": {"enemy": {"cognition": -3, "grace": -2}}, "mod_duration": 2}],
     },
     "signature_fusion": {"id": "amber_wasp_swarm_assault", "name": "Swarm Assault", "power_type": "strike", "damage_type": "physical", "damage": 16, "cost_mp": 5, "cost_stamina": 0, "cooldown": 4, "hits": 4, "is_signature": True,
                          "status_apply": "poisoned", "lifesteal": 0.10, "stat_mod": {"enemy": {"grace": -4}}, "mod_duration": 3},
     "drops": {"common": [{"id": "amber_resin", "chance": 0.7, "qty": [1, 1]}, {"id": "wild_herb", "chance": 0.4, "qty": [1, 1]}], "rare": [], "boss": [], "gold": [12, 25], "xp_mult": 1.3}},
    {"id": "golden_beetle", "name": "Golden Beetle", "biome": "amber_vineyards", "rarity": "uncommon", "hp": 52,
     "creature_tier": "normal", "species": "beast", "archetype": "tank", "personality": "guardian",
     "stats": {"might": {"base": 18, "growth": 1.5}, "grace": {"base": 10, "growth": 0.9}, "cognition": {"base": 8, "growth": 0.7},
               "insight": {"base": 10, "growth": 0.9}, "essence": {"base": 16, "growth": 1.4}, "durability": {"base": 20, "growth": 1.6}},
     "life": {"mp": 15, "stamina": 90, "shield": 5},
     "passive_buff": {"type": "durability_bonus", "value": 0.16, "secondary": {"type": "essence_bonus", "value": 0.12}},
     "profile_skills": {
         "attack": [{"id": "golden_beetle_charge", "name": "Golden Charge", "power_type": "strike", "damage_type": "physical", "damage": 14, "cost_mp": 0, "cost_stamina": 25, "cooldown": 1, "trigger": "always",
                     "status_apply": "stunned", "stat_mod": {"enemy": {"armor_bonus": -3}}, "mod_duration": 2}],
         "defense": [{"id": "golden_beetle_gold_shell", "name": "Gold Shell", "power_type": "buff", "cost_mp": 3, "cost_stamina": 25, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 7, "essence": 4}}, "mod_duration": 3}],
         "utility": [{"id": "golden_beetle_amber_spit", "name": "Amber Spit", "power_type": "debuff", "damage_type": "magical", "damage": 4, "cost_mp": 3, "cost_stamina": 0, "cooldown": 2, "trigger": "opening_move",
                      "status_apply": "ensnared", "stat_mod": {"enemy": {"grace": -4}}, "mod_duration": 3}],
     },
     "signature_fusion": {"id": "golden_beetle_amber_prison", "name": "Amber Prison", "power_type": "strike", "damage_type": "magical", "damage": 20, "cost_mp": 10, "cost_stamina": 0, "cooldown": 4, "hits": 1, "is_signature": True,
                          "status_apply": "ensnared", "unevadable": True, "stat_mod": {"enemy": {"grace": -5, "might": -4}}, "mod_duration": 4},
     "drops": {"common": [{"id": "amber_resin", "chance": 0.6, "qty": [1, 1]}], "rare": [{"id": "golden_chitin", "chance": 0.15, "qty": [1, 1]}], "boss": [], "gold": [15, 30], "xp_mult": 1.4}},
    {"id": "vineyard_matriarch", "name": "Vineyard Matriarch", "biome": "amber_vineyards", "rarity": "rare", "hp": 80,
     "creature_tier": "mini_boss", "species": "magical", "archetype": "caster", "personality": "opportunist",
     "stats": {"might": {"base": 14, "growth": 1.2}, "grace": {"base": 18, "growth": 1.5}, "cognition": {"base": 24, "growth": 2.0},
               "insight": {"base": 22, "growth": 1.8}, "essence": {"base": 22, "growth": 1.8}, "durability": {"base": 16, "growth": 1.3}},
     "life": {"mp": 40, "stamina": 80, "shield": 0},
     "passive_buff": [{"type": "essence_bonus", "value": 0.20}, {"type": "cognition_bonus", "value": 0.15}],
     "profile_skills": {
         "attack": [{"id": "matriarch_amber_lance", "name": "Amber Lance", "power_type": "strike", "damage_type": "magical", "damage": 22, "cost_mp": 6, "cost_stamina": 0, "cooldown": 1, "trigger": "always",
                     "status_apply": "ensnared", "stat_mod": {"enemy": {"grace": -4}}, "mod_duration": 3},
                    {"id": "matriarch_vine_whip", "name": "Vine Whip", "power_type": "strike", "damage_type": "magical", "damage": 26, "cost_mp": 8, "cost_stamina": 0, "cooldown": 2, "trigger": "always",
                     "status_apply": "bleeding", "stat_mod": {"enemy": {"might": -4}}, "mod_duration": 2}],
         "defense": [{"id": "matriarch_amber_cocoon", "name": "Amber Cocoon", "power_type": "buff", "cost_mp": 8, "cost_stamina": 0, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 8, "essence": 5}}, "mod_duration": 3}],
         "utility": [{"id": "matriarch_intoxicating_scent", "name": "Intoxicating Scent", "power_type": "debuff", "damage_type": "magical", "damage": 5, "cost_mp": 6, "cost_stamina": 0, "cooldown": 2, "trigger": "opening_move",
                      "status_apply": "weary", "stat_mod": {"enemy": {"cognition": -5, "insight": -4}}, "mod_duration": 3}],
     },
     "signature_fusion": {"id": "matriarch_amber_deluge", "name": "Amber Deluge", "power_type": "strike", "damage_type": "magical", "damage": 30, "cost_mp": 15, "cost_stamina": 0, "cooldown": 4, "hits": 3, "is_signature": True,
                          "status_apply": "ensnared", "unevadable": True, "stat_mod": {"enemy": {"grace": -6, "might": -5}}, "mod_duration": 4},
     "drops": {"common": [{"id": "amber_resin", "chance": 0.9, "qty": [1, 2]}], "rare": [{"id": "golden_chitin", "chance": 0.2, "qty": [1, 1]}], "boss": [{"id": "matriarch_crown", "chance": 0.2, "qty": [1, 1]}], "gold": [25, 50], "xp_mult": 1.6}},
    # ---- Silverroad (Concordia Lv 18) ----
    {"id": "highway_knight", "name": "Highway Knight", "biome": "silverroad", "rarity": "common", "hp": 60,
     "creature_tier": "normal", "species": "humanoid", "archetype": "bruiser", "personality": "guardian",
     "stats": {"might": {"base": 22, "growth": 1.8}, "grace": {"base": 14, "growth": 1.2}, "cognition": {"base": 12, "growth": 1.0},
               "insight": {"base": 10, "growth": 0.9}, "essence": {"base": 10, "growth": 0.9}, "durability": {"base": 20, "growth": 1.6}},
     "life": {"mp": 5, "stamina": 120, "shield": 5},
     "passive_buff": {"type": "might_bonus", "value": 0.16, "secondary": {"type": "durability_bonus", "value": 0.12}},
     "profile_skills": {
         "attack": [{"id": "highway_knight_slash", "name": "Knight's Slash", "power_type": "strike", "damage_type": "physical", "damage": 16, "cost_mp": 0, "cost_stamina": 25, "cooldown": 1, "trigger": "always",
                     "status_apply": "bleeding", "stat_mod": {"enemy": {"armor_bonus": -3}}, "mod_duration": 2}],
         "defense": [{"id": "highway_knight_shield_wall", "name": "Shield Wall", "power_type": "buff", "cost_mp": 0, "cost_stamina": 30, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 7, "durability": 4}}, "mod_duration": 3}],
         "utility": [{"id": "highway_knight_rally", "name": "Rally Cry", "power_type": "buff", "cost_mp": 0, "cost_stamina": 25, "cooldown": 3, "trigger": "always",
                      "self_status": "inspired", "stat_mod": {"self": {"might": 4, "grace": 3}}, "mod_duration": 2}],
     },
     "signature_fusion": {"id": "highway_knight_charge", "name": "Knight's Charge", "power_type": "strike", "damage_type": "physical", "damage": 22, "cost_mp": 0, "cost_stamina": 50, "cooldown": 4, "hits": 2, "is_signature": True,
                          "status_apply": "stunned", "armor_ignore": True, "stat_mod": {"enemy": {"might": -4}}, "mod_duration": 3},
     "drops": {"common": [{"id": "iron_ore", "chance": 0.6, "qty": [1, 1]}, {"id": "coin_purse", "chance": 0.5, "qty": [1, 1]}], "rare": [], "boss": [], "gold": [15, 30], "xp_mult": 1.4}},
    {"id": "silverroad_bandit", "name": "Silverroad Bandit", "biome": "silverroad", "rarity": "uncommon", "hp": 50,
     "creature_tier": "normal", "species": "humanoid", "archetype": "speed", "personality": "opportunist",
     "stats": {"might": {"base": 18, "growth": 1.5}, "grace": {"base": 22, "growth": 1.7}, "cognition": {"base": 16, "growth": 1.3},
               "insight": {"base": 18, "growth": 1.4}, "essence": {"base": 8, "growth": 0.7}, "durability": {"base": 12, "growth": 1.0}},
     "life": {"mp": 5, "stamina": 110, "shield": 0},
     "passive_buff": {"type": "grace_bonus", "value": 0.18, "secondary": {"type": "might_bonus", "value": 0.10}},
     "profile_skills": {
         "attack": [{"id": "silverroad_bandit_dual_slash", "name": "Dual Slash", "power_type": "strike", "damage_type": "physical", "damage": 16, "cost_mp": 0, "cost_stamina": 20, "cooldown": 1, "trigger": "always",
                     "status_apply": "bleeding", "stat_mod": {"enemy": {"grace": -3}}, "mod_duration": 2},
                    {"id": "silverroad_bandit_kick", "name": "Knockback Kick", "power_type": "strike", "damage_type": "physical", "damage": 14, "cost_mp": 0, "cost_stamina": 25, "cooldown": 2, "trigger": "always",
                     "status_apply": "stunned", "stat_mod": {"enemy": {"might": -3}}, "mod_duration": 2}],
         "defense": [{"id": "silverroad_bandit_evasion", "name": "Dagger Parry", "power_type": "buff", "cost_mp": 0, "cost_stamina": 20, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "evasive", "stat_mod": {"self": {"grace": 5, "armor_bonus": 3}}, "mod_duration": 2}],
         "utility": [{"id": "silverroad_bandit_intimidate", "name": "Intimidate", "power_type": "debuff", "damage_type": "physical", "damage": 4, "cost_mp": 0, "cost_stamina": 25, "cooldown": 2, "trigger": "opening_move",
                      "status_apply": "weary", "stat_mod": {"enemy": {"might": -4, "cognition": -3}}, "mod_duration": 3}],
     },
     "signature_fusion": {"id": "silverroad_bandit_ambush", "name": "Ambush Frenzy", "power_type": "strike", "damage_type": "physical", "damage": 24, "cost_mp": 0, "cost_stamina": 50, "cooldown": 4, "hits": 4, "is_signature": True,
                          "status_apply": "bleeding", "unevadable": True, "stat_mod": {"enemy": {"grace": -5}}, "mod_duration": 3},
     "drops": {"common": [{"id": "coin_purse", "chance": 0.8, "qty": [1, 1]}], "rare": [{"id": "silver_dagger", "chance": 0.1, "qty": [1, 1]}], "boss": [], "gold": [20, 35], "xp_mult": 1.5}},
    {"id": "silverroad_warlord", "name": "Silverroad Warlord", "biome": "silverroad", "rarity": "rare", "hp": 90,
     "creature_tier": "mini_boss", "species": "humanoid", "archetype": "bruiser", "personality": "aggressive",
     "stats": {"might": {"base": 30, "growth": 2.3}, "grace": {"base": 16, "growth": 1.3}, "cognition": {"base": 14, "growth": 1.2},
               "insight": {"base": 12, "growth": 1.0}, "essence": {"base": 14, "growth": 1.2}, "durability": {"base": 24, "growth": 1.8}},
     "life": {"mp": 15, "stamina": 140, "shield": 5},
     "passive_buff": [{"type": "might_bonus", "value": 0.20}, {"type": "durability_bonus", "value": 0.15}],
     "profile_skills": {
         "attack": [{"id": "silverroad_warlord_cleave", "name": "Warlord's Cleave", "power_type": "strike", "damage_type": "physical", "damage": 24, "cost_mp": 0, "cost_stamina": 25, "cooldown": 1, "trigger": "always",
                     "status_apply": "bleeding", "stat_mod": {"enemy": {"armor_bonus": -4}}, "mod_duration": 2},
                    {"id": "silverroad_warlord_shield_bash", "name": "Shield Bash", "power_type": "strike", "damage_type": "physical", "damage": 28, "cost_mp": 0, "cost_stamina": 35, "cooldown": 2, "trigger": "always",
                     "status_apply": "stunned", "stat_mod": {"enemy": {"might": -5}}, "mod_duration": 3}],
         "defense": [{"id": "silverroad_warlord_fortress", "name": "Fortress Stance", "power_type": "buff", "cost_mp": 0, "cost_stamina": 30, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 10, "durability": 6}}, "mod_duration": 3}],
         "utility": [{"id": "silverroad_warlord_command", "name": "Warlord's Command", "power_type": "buff", "cost_mp": 5, "cost_stamina": 30, "cooldown": 3, "trigger": "always",
                      "self_status": "inspired", "stat_mod": {"self": {"might": 6, "grace": 4}}, "mod_duration": 3}],
     },
     "signature_fusion": {"id": "silverroad_warlord_decimation", "name": "Decimation", "power_type": "strike", "damage_type": "physical", "damage": 32, "cost_mp": 0, "cost_stamina": 50, "cooldown": 4, "hits": 3, "is_signature": True,
                          "status_apply": "stunned", "armor_ignore": True, "stat_mod": {"enemy": {"might": -6, "armor_bonus": -5}}, "mod_duration": 4},
     "drops": {"common": [{"id": "iron_ore", "chance": 0.8, "qty": [1, 2]}], "rare": [{"id": "silver_ingot", "chance": 0.15, "qty": [1, 1]}], "boss": [{"id": "warlord_greaves", "chance": 0.2, "qty": [1, 1]}], "gold": [30, 55], "xp_mult": 1.7}},
    # ---- Diplomat's Highlands (Concordia Lv 22) ----
    {"id": "enclave_sentinel", "name": "Enclave Sentinel", "biome": "diplomats_highlands", "rarity": "common", "hp": 65,
     "creature_tier": "normal", "species": "humanoid", "archetype": "tank", "personality": "guardian",
     "stats": {"might": {"base": 22, "growth": 1.8}, "grace": {"base": 14, "growth": 1.2}, "cognition": {"base": 14, "growth": 1.2},
               "insight": {"base": 16, "growth": 1.3}, "essence": {"base": 14, "growth": 1.2}, "durability": {"base": 22, "growth": 1.7}},
     "life": {"mp": 10, "stamina": 120, "shield": 5},
     "passive_buff": {"type": "durability_bonus", "value": 0.18, "secondary": {"type": "insight_bonus", "value": 0.12}},
     "profile_skills": {
         "attack": [{"id": "enclave_sentinel_halberd", "name": "Halberd Strike", "power_type": "strike", "damage_type": "physical", "damage": 18, "cost_mp": 0, "cost_stamina": 25, "cooldown": 1, "trigger": "always",
                     "status_apply": "bleeding", "stat_mod": {"enemy": {"armor_bonus": -3}}, "mod_duration": 2}],
         "defense": [{"id": "enclave_sentinel_guard", "name": "Sentinel's Guard", "power_type": "buff", "cost_mp": 0, "cost_stamina": 30, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 8, "durability": 5}}, "mod_duration": 3}],
         "utility": [{"id": "enclave_sentinel_intercept", "name": "Intercept", "power_type": "debuff", "damage_type": "physical", "damage": 5, "cost_mp": 0, "cost_stamina": 25, "cooldown": 2, "trigger": "opening_move",
                      "status_apply": "ensnared", "stat_mod": {"enemy": {"grace": -4}}, "mod_duration": 2}],
     },
     "signature_fusion": {"id": "enclave_sentinel_judgement", "name": "Judgement Strike", "power_type": "strike", "damage_type": "physical", "damage": 26, "cost_mp": 0, "cost_stamina": 50, "cooldown": 4, "hits": 2, "is_signature": True,
                          "status_apply": "stunned", "armor_ignore": True, "stat_mod": {"enemy": {"might": -5}}, "mod_duration": 3},
     "drops": {"common": [{"id": "iron_ore", "chance": 0.6, "qty": [1, 1]}, {"id": "coin_purse", "chance": 0.4, "qty": [1, 1]}], "rare": [], "boss": [], "gold": [20, 35], "xp_mult": 1.5}},
    {"id": "highlands_wizard", "name": "Highlands Wizard", "biome": "diplomats_highlands", "rarity": "uncommon", "hp": 55,
     "creature_tier": "normal", "species": "humanoid", "archetype": "caster", "personality": "opportunist",
     "stats": {"might": {"base": 8, "growth": 0.7}, "grace": {"base": 14, "growth": 1.2}, "cognition": {"base": 24, "growth": 2.0},
               "insight": {"base": 22, "growth": 1.8}, "essence": {"base": 24, "growth": 2.0}, "durability": {"base": 12, "growth": 1.0}},
     "life": {"mp": 40, "stamina": 70, "shield": 0},
     "passive_buff": {"type": "essence_bonus", "value": 0.20, "secondary": {"type": "cognition_bonus", "value": 0.15}},
     "profile_skills": {
         "attack": [{"id": "highlands_wizard_arcane_bolt", "name": "Arcane Bolt", "power_type": "strike", "damage_type": "magical", "damage": 18, "cost_mp": 4, "cost_stamina": 0, "cooldown": 1, "trigger": "always",
                     "status_apply": "weary", "stat_mod": {"enemy": {"essence": -4}}, "mod_duration": 2},
                    {"id": "highlands_wizard_ice_lance", "name": "Ice Lance", "power_type": "strike", "damage_type": "magical", "damage": 20, "cost_mp": 6, "cost_stamina": 0, "cooldown": 2, "trigger": "always",
                     "status_apply": "ensnared", "stat_mod": {"enemy": {"grace": -4}}, "mod_duration": 3}],
         "defense": [{"id": "highlands_wizard_arcane_barrier", "name": "Arcane Barrier", "power_type": "buff", "cost_mp": 6, "cost_stamina": 0, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 6, "essence": 5}}, "mod_duration": 3}],
         "utility": [{"id": "highlands_wizard_slow", "name": "Slow Spell", "power_type": "debuff", "damage_type": "magical", "damage": 5, "cost_mp": 5, "cost_stamina": 0, "cooldown": 2, "trigger": "opening_move",
                      "status_apply": "weary", "stat_mod": {"enemy": {"grace": -5, "cognition": -4}}, "mod_duration": 3}],
     },
     "signature_fusion": {"id": "highlands_wizard_meteor", "name": "Meteor Strike", "power_type": "strike", "damage_type": "magical", "damage": 28, "cost_mp": 15, "cost_stamina": 0, "cooldown": 4, "hits": 2, "is_signature": True,
                          "status_apply": "burning", "unevadable": True, "stat_mod": {"enemy": {"might": -5, "armor_bonus": -5}}, "mod_duration": 4},
     "drops": {"common": [{"id": "relic_shard", "chance": 0.6, "qty": [1, 1]}], "rare": [{"id": "arcane_crystal", "chance": 0.1, "qty": [1, 1]}], "boss": [], "gold": [25, 40], "xp_mult": 1.6}},
    {"id": "diplomat_chancellor", "name": "Highlands Chancellor", "biome": "diplomats_highlands", "rarity": "rare", "hp": 100,
     "creature_tier": "mini_boss", "species": "humanoid", "archetype": "caster", "personality": "opportunist",
     "stats": {"might": {"base": 14, "growth": 1.2}, "grace": {"base": 18, "growth": 1.5}, "cognition": {"base": 30, "growth": 2.4},
               "insight": {"base": 28, "growth": 2.2}, "essence": {"base": 28, "growth": 2.2}, "durability": {"base": 18, "growth": 1.4}},
     "life": {"mp": 60, "stamina": 80, "shield": 0},
     "passive_buff": [{"type": "essence_bonus", "value": 0.22}, {"type": "cognition_bonus", "value": 0.18}],
     "profile_skills": {
         "attack": [{"id": "chancellor_arcane_storm", "name": "Arcane Storm", "power_type": "strike", "damage_type": "magical", "damage": 26, "cost_mp": 8, "cost_stamina": 0, "cooldown": 1, "trigger": "always",
                     "status_apply": "weary", "stat_mod": {"enemy": {"essence": -5}}, "mod_duration": 3},
                    {"id": "chancellor_gravity_well", "name": "Gravity Well", "power_type": "strike", "damage_type": "magical", "damage": 30, "cost_mp": 10, "cost_stamina": 0, "cooldown": 2, "trigger": "always",
                     "status_apply": "ensnared", "stat_mod": {"enemy": {"grace": -5, "might": -4}}, "mod_duration": 3}],
         "defense": [{"id": "chancellor_arcane_fortress", "name": "Arcane Fortress", "power_type": "buff", "cost_mp": 10, "cost_stamina": 0, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 10, "essence": 7}}, "mod_duration": 3}],
         "utility": [{"id": "chancellor_mind_dominance", "name": "Mind Dominance", "power_type": "debuff", "damage_type": "magical", "damage": 8, "cost_mp": 10, "cost_stamina": 0, "cooldown": 3, "trigger": "opening_move",
                      "status_apply": "weary", "stat_mod": {"enemy": {"cognition": -6, "insight": -5, "might": -4}}, "mod_duration": 4}],
     },
     "signature_fusion": {"id": "chancellor_apocalypse", "name": "Arcane Apocalypse", "power_type": "strike", "damage_type": "magical", "damage": 38, "cost_mp": 20, "cost_stamina": 0, "cooldown": 4, "hits": 3, "is_signature": True,
                          "status_apply": "burning", "unevadable": True, "stat_mod": {"enemy": {"essence": -7, "cognition": -6}}, "mod_duration": 4},
     "drops": {"common": [{"id": "arcane_crystal", "chance": 0.7, "qty": [1, 1]}], "rare": [{"id": "chancellor_staff", "chance": 0.15, "qty": [1, 1]}], "boss": [{"id": "chancellor_seal", "chance": 0.2, "qty": [1, 1]}], "gold": [35, 70], "xp_mult": 1.8}},
    # ---- Misty Thicket (Daw'ul Talalu starter) ----
    {"id": "mist_sprite", "name": "Mist Sprite", "biome": "misty_thicket", "rarity": "common", "hp": 16,
     "creature_tier": "normal", "species": "magical", "archetype": "caster", "personality": "opportunist",
     "stats": {"might": {"base": 5, "growth": 0.5}, "grace": {"base": 12, "growth": 1.1}, "cognition": {"base": 14, "growth": 1.3},
               "insight": {"base": 14, "growth": 1.3}, "essence": {"base": 12, "growth": 1.1}, "durability": {"base": 6, "growth": 0.6}},
     "life": {"mp": 15, "stamina": 60, "shield": 0},
     "passive_buff": {"type": "essence_bonus", "value": 0.14, "secondary": {"type": "evasion_bonus", "value": 0.10}},
     "profile_skills": {
         "attack": [{"id": "mist_sprite_mist_bolt", "name": "Mist Bolt", "power_type": "strike", "damage_type": "magical", "damage": 5, "cost_mp": 2, "cost_stamina": 0, "cooldown": 1, "trigger": "always",
                     "status_apply": "weary", "stat_mod": {"enemy": {"grace": -2}}, "mod_duration": 2}],
         "defense": [{"id": "mist_sprite_mist_veil", "name": "Mist Veil", "power_type": "buff", "cost_mp": 3, "cost_stamina": 0, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "evasive", "stat_mod": {"self": {"grace": 4, "essence": 2}}, "mod_duration": 2}],
         "utility": [{"id": "mist_sprite_illusion", "name": "Illusion Pulse", "power_type": "debuff", "damage_type": "magical", "damage": 2, "cost_mp": 3, "cost_stamina": 0, "cooldown": 2, "trigger": "opening_move",
                      "status_apply": "weary", "stat_mod": {"enemy": {"cognition": -3, "grace": -2}}, "mod_duration": 3}],
     },
     "signature_fusion": {"id": "mist_sprite_dream_eater", "name": "Dream Eater", "power_type": "strike", "damage_type": "magical", "damage": 9, "cost_mp": 5, "cost_stamina": 0, "cooldown": 4, "hits": 3, "is_signature": True,
                          "status_apply": "weary", "lifesteal": 0.15, "stat_mod": {"enemy": {"cognition": -4}}, "mod_duration": 3},
     "drops": {"common": [{"id": "shadow_herb", "chance": 0.6, "qty": [1, 1]}, {"id": "wisp_essence", "chance": 0.3, "qty": [1, 1]}], "rare": [], "boss": [], "gold": [2, 8], "xp_mult": 1.1}},
    {"id": "thorn_crawler", "name": "Thorn Crawler", "biome": "misty_thicket", "rarity": "uncommon", "hp": 22,
     "creature_tier": "normal", "species": "monster", "archetype": "bruiser", "personality": "aggressive",
     "stats": {"might": {"base": 14, "growth": 1.3}, "grace": {"base": 10, "growth": 1.0}, "cognition": {"base": 6, "growth": 0.7},
               "insight": {"base": 8, "growth": 0.8}, "essence": {"base": 8, "growth": 0.8}, "durability": {"base": 12, "growth": 1.1}},
     "life": {"mp": 5, "stamina": 90, "shield": 0},
     "passive_buff": {"type": "might_bonus", "value": 0.12, "secondary": {"type": "durability_bonus", "value": 0.10}},
     "profile_skills": {
         "attack": [{"id": "thorn_crawler_bite", "name": "Savage Bite", "power_type": "strike", "damage_type": "physical", "damage": 6, "cost_mp": 0, "cost_stamina": 20, "cooldown": 1, "trigger": "always",
                     "status_apply": "bleeding", "stat_mod": {"enemy": {"might": -2}}, "mod_duration": 2},
                    {"id": "thorn_crawler_thornlash", "name": "Thornlash", "power_type": "strike", "damage_type": "physical", "damage": 5, "cost_mp": 0, "cost_stamina": 25, "cooldown": 2, "trigger": "always",
                     "status_apply": "poisoned", "stat_mod": {"enemy": {"grace": -2}}, "mod_duration": 3}],
         "defense": [{"id": "thorn_crawler_bark_skin", "name": "Bark Skin", "power_type": "buff", "cost_mp": 0, "cost_stamina": 25, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 4, "durability": 2}}, "mod_duration": 3}],
         "utility": [{"id": "thorn_crawler_root_trap", "name": "Root Trap", "power_type": "debuff", "damage_type": "physical", "damage": 3, "cost_mp": 0, "cost_stamina": 25, "cooldown": 2, "trigger": "opening_move",
                      "status_apply": "ensnared", "stat_mod": {"enemy": {"grace": -3, "might": -2}}, "mod_duration": 2}],
     },
     "signature_fusion": {"id": "thorn_crawler_thorn_storm", "name": "Thorn Storm", "power_type": "strike", "damage_type": "physical", "damage": 10, "cost_mp": 0, "cost_stamina": 50, "cooldown": 4, "hits": 3, "is_signature": True,
                          "status_apply": "poisoned", "lifesteal": 0.15, "stat_mod": {"enemy": {"might": -3, "grace": -3}}, "mod_duration": 3},
     "drops": {"common": [{"id": "shadow_herb", "chance": 0.5, "qty": [1, 1]}, {"id": "thorn_vine", "chance": 0.4, "qty": [1, 1]}], "rare": [], "boss": [], "gold": [3, 10], "xp_mult": 1.1}},
    # ---- Granite Foothills (Khardrum Lv 16) ----
    {"id": "stone_troll", "name": "Stone Troll", "biome": "granite_foothills", "rarity": "common", "hp": 70,
     "creature_tier": "normal", "species": "monster", "archetype": "tank", "personality": "guardian",
     "stats": {"might": {"base": 24, "growth": 2.0}, "grace": {"base": 8, "growth": 0.7}, "cognition": {"base": 6, "growth": 0.5},
               "insight": {"base": 8, "growth": 0.7}, "essence": {"base": 10, "growth": 0.8}, "durability": {"base": 26, "growth": 2.2}},
     "life": {"mp": 0, "stamina": 120, "shield": 5},
     "passive_buff": {"type": "durability_bonus", "value": 0.20, "secondary": {"type": "might_bonus", "value": 0.12}},
     "profile_skills": {
         "attack": [{"id": "stone_troll_boulder_fist", "name": "Boulder Fist", "power_type": "strike", "damage_type": "physical", "damage": 18, "cost_mp": 0, "cost_stamina": 25, "cooldown": 1, "trigger": "always",
                     "status_apply": "stunned", "stat_mod": {"enemy": {"armor_bonus": -3}}, "mod_duration": 2}],
         "defense": [{"id": "stone_troll_stone_skin", "name": "Stone Skin", "power_type": "buff", "cost_mp": 0, "cost_stamina": 30, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 8, "durability": 5}}, "mod_duration": 3}],
         "utility": [{"id": "stone_troll_rock_throw", "name": "Rock Throw", "power_type": "strike", "damage_type": "physical", "damage": 14, "cost_mp": 0, "cost_stamina": 20, "cooldown": 2, "trigger": "opening_move",
                      "status_apply": "stunned", "stat_mod": {"enemy": {"grace": -3}}, "mod_duration": 2}],
     },
     "signature_fusion": {"id": "stone_trolL_quake_stomp", "name": "Quake Stomp", "power_type": "strike", "damage_type": "physical", "damage": 24, "cost_mp": 0, "cost_stamina": 50, "cooldown": 4, "hits": 1, "is_signature": True,
                          "status_apply": "stunned", "armor_ignore": True, "stat_mod": {"enemy": {"might": -5, "grace": -4}}, "mod_duration": 3},
     "drops": {"common": [{"id": "granite_shard", "chance": 0.7, "qty": [1, 1]}, {"id": "iron_ore", "chance": 0.4, "qty": [1, 1]}], "rare": [], "boss": [], "gold": [15, 30], "xp_mult": 1.4}},
    {"id": "ore_golem", "name": "Ore Golem", "biome": "granite_foothills", "rarity": "uncommon", "hp": 80,
     "creature_tier": "normal", "species": "construct", "archetype": "tank", "personality": "guardian",
     "tags": ["construct"],
     "stats": {"might": {"base": 26, "growth": 2.2}, "grace": {"base": 6, "growth": 0.5}, "cognition": {"base": 4, "growth": 0.4},
               "insight": {"base": 6, "growth": 0.5}, "essence": {"base": 12, "growth": 1.0}, "durability": {"base": 28, "growth": 2.4}},
     "life": {"mp": 0, "stamina": 130, "shield": 10},
     "passive_buff": {"type": "durability_bonus", "value": 0.22, "secondary": {"type": "might_bonus", "value": 0.14}},
     "profile_skills": {
         "attack": [{"id": "ore_golem_crush", "name": "Ore Crush", "power_type": "strike", "damage_type": "physical", "damage": 20, "cost_mp": 0, "cost_stamina": 25, "cooldown": 1, "trigger": "always",
                     "status_apply": "stunned", "stat_mod": {"enemy": {"armor_bonus": -4}}, "mod_duration": 2}],
         "defense": [{"id": "ore_golem_iron_body", "name": "Iron Body", "power_type": "buff", "cost_mp": 0, "cost_stamina": 30, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 10, "durability": 6}}, "mod_duration": 3}],
         "utility": [{"id": "ore_golem_magnetic_pull", "name": "Magnetic Pull", "power_type": "debuff", "damage_type": "physical", "damage": 5, "cost_mp": 0, "cost_stamina": 25, "cooldown": 2, "trigger": "opening_move",
                      "status_apply": "ensnared", "stat_mod": {"enemy": {"grace": -4}}, "mod_duration": 3}],
     },
     "signature_fusion": {"id": "ore_golem_meteor_slam", "name": "Meteor Slam", "power_type": "strike", "damage_type": "physical", "damage": 28, "cost_mp": 0, "cost_stamina": 50, "cooldown": 4, "hits": 1, "is_signature": True,
                          "status_apply": "stunned", "armor_ignore": True, "stat_mod": {"enemy": {"might": -6, "armor_bonus": -5}}, "mod_duration": 4},
     "drops": {"common": [{"id": "iron_ore", "chance": 0.8, "qty": [1, 2]}, {"id": "copper_ore", "chance": 0.5, "qty": [1, 1]}], "rare": [{"id": "silver_ore", "chance": 0.1, "qty": [1, 1]}], "boss": [], "gold": [20, 35], "xp_mult": 1.5}},
    {"id": "granite_foreman", "name": "Granite Foreman", "biome": "granite_foothills", "rarity": "rare", "hp": 95,
     "creature_tier": "mini_boss", "species": "humanoid", "archetype": "bruiser", "personality": "aggressive",
     "stats": {"might": {"base": 32, "growth": 2.5}, "grace": {"base": 14, "growth": 1.2}, "cognition": {"base": 16, "growth": 1.3},
               "insight": {"base": 14, "growth": 1.2}, "essence": {"base": 12, "growth": 1.0}, "durability": {"base": 26, "growth": 2.0}},
     "life": {"mp": 10, "stamina": 140, "shield": 5},
     "passive_buff": [{"type": "might_bonus", "value": 0.20}, {"type": "durability_bonus", "value": 0.16}],
     "profile_skills": {
         "attack": [{"id": "granite_foreman_war_hammer", "name": "War Hammer", "power_type": "strike", "damage_type": "physical", "damage": 26, "cost_mp": 0, "cost_stamina": 25, "cooldown": 1, "trigger": "always",
                     "status_apply": "stunned", "stat_mod": {"enemy": {"armor_bonus": -4}}, "mod_duration": 2},
                    {"id": "granite_foreman_quake_slam", "name": "Quake Slam", "power_type": "strike", "damage_type": "physical", "damage": 30, "cost_mp": 0, "cost_stamina": 35, "cooldown": 2, "trigger": "always",
                     "status_apply": "stunned", "stat_mod": {"enemy": {"might": -5, "grace": -4}}, "mod_duration": 3}],
         "defense": [{"id": "granite_foreman_stone_aegis", "name": "Stone Aegis", "power_type": "buff", "cost_mp": 0, "cost_stamina": 30, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 10, "durability": 7}}, "mod_duration": 3}],
         "utility": [{"id": "granite_foreman_rally_miners", "name": "Rally Miners", "power_type": "buff", "cost_mp": 5, "cost_stamina": 30, "cooldown": 3, "trigger": "always",
                      "self_status": "inspired", "stat_mod": {"self": {"might": 6, "durability": 4}}, "mod_duration": 3}],
     },
     "signature_fusion": {"id": "granite_foreman_avalanche", "name": "Avalanche", "power_type": "strike", "damage_type": "physical", "damage": 36, "cost_mp": 0, "cost_stamina": 50, "cooldown": 4, "hits": 3, "is_signature": True,
                          "status_apply": "stunned", "armor_ignore": True, "stat_mod": {"enemy": {"might": -6, "armor_bonus": -6}}, "mod_duration": 4},
     "drops": {"common": [{"id": "iron_ore", "chance": 0.9, "qty": [2, 3]}], "rare": [{"id": "silver_ore", "chance": 0.2, "qty": [1, 1]}], "boss": [{"id": "foreman_gauntlets", "chance": 0.2, "qty": [1, 1]}], "gold": [30, 55], "xp_mult": 1.7}},
    # ---- Ember Mines (Khardrum Lv 20) ----
    {"id": "magma_rat", "name": "Magma Rat", "biome": "ember_mines", "rarity": "common", "hp": 55,
     "creature_tier": "normal", "species": "beast", "archetype": "speed", "personality": "aggressive",
     "stats": {"might": {"base": 18, "growth": 1.5}, "grace": {"base": 20, "growth": 1.6}, "cognition": {"base": 10, "growth": 0.9},
               "insight": {"base": 12, "growth": 1.0}, "essence": {"base": 16, "growth": 1.4}, "durability": {"base": 14, "growth": 1.2}},
     "life": {"mp": 10, "stamina": 100, "shield": 0},
     "passive_buff": {"type": "grace_bonus", "value": 0.16, "secondary": {"type": "essence_bonus", "value": 0.12}},
     "profile_skills": {
         "attack": [{"id": "magma_rat_fire_gnaw", "name": "Fire Gnaw", "power_type": "strike", "damage_type": "magical", "damage": 18, "cost_mp": 3, "cost_stamina": 15, "cooldown": 1, "trigger": "always",
                     "status_apply": "burning", "stat_mod": {"enemy": {"armor_bonus": -3}}, "mod_duration": 2}],
         "defense": [{"id": "magma_rat_scurry", "name": "Hot Scurry", "power_type": "buff", "cost_mp": 0, "cost_stamina": 20, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "evasive", "stat_mod": {"self": {"grace": 5}}, "mod_duration": 2}],
         "utility": [{"id": "magma_rat_smoke_screen", "name": "Smoke Screen", "power_type": "debuff", "damage_type": "magical", "damage": 3, "cost_mp": 3, "cost_stamina": 0, "cooldown": 2, "trigger": "opening_move",
                      "status_apply": "weary", "stat_mod": {"enemy": {"cognition": -3, "grace": -3}}, "mod_duration": 2}],
     },
     "signature_fusion": {"id": "magma_rat_ember_swarm", "name": "Ember Swarm", "power_type": "strike", "damage_type": "magical", "damage": 24, "cost_mp": 8, "cost_stamina": 0, "cooldown": 4, "hits": 4, "is_signature": True,
                          "status_apply": "burning", "lifesteal": 0.10, "stat_mod": {"enemy": {"grace": -4}}, "mod_duration": 3},
     "drops": {"common": [{"id": "ember_shard", "chance": 0.7, "qty": [1, 1]}, {"id": "fire_crystal", "chance": 0.2, "qty": [1, 1]}], "rare": [], "boss": [], "gold": [20, 35], "xp_mult": 1.5}},
    {"id": "ember_elemental", "name": "Ember Elemental", "biome": "ember_mines", "rarity": "uncommon", "hp": 65,
     "creature_tier": "normal", "species": "magical", "archetype": "caster", "personality": "aggressive",
     "stats": {"might": {"base": 10, "growth": 0.8}, "grace": {"base": 14, "growth": 1.2}, "cognition": {"base": 18, "growth": 1.5},
               "insight": {"base": 20, "growth": 1.6}, "essence": {"base": 24, "growth": 2.0}, "durability": {"base": 14, "growth": 1.2}},
     "life": {"mp": 35, "stamina": 60, "shield": 0},
     "passive_buff": {"type": "essence_bonus", "value": 0.20, "secondary": {"type": "magic_resist", "value": 0.15}},
     "profile_skills": {
         "attack": [{"id": "ember_elemental_fire_bolt", "name": "Fire Bolt", "power_type": "strike", "damage_type": "magical", "damage": 20, "cost_mp": 4, "cost_stamina": 0, "cooldown": 1, "trigger": "always",
                     "status_apply": "burning", "stat_mod": {"enemy": {"armor_bonus": -4}}, "mod_duration": 3},
                    {"id": "ember_elemental_flame_nova", "name": "Flame Nova", "power_type": "strike", "damage_type": "magical", "damage": 24, "cost_mp": 8, "cost_stamina": 0, "cooldown": 2, "trigger": "always",
                     "status_apply": "burning", "unevadable": True, "stat_mod": {"enemy": {"might": -4}}, "mod_duration": 3}],
         "defense": [{"id": "ember_elemental_fire_shield", "name": "Fire Shield", "power_type": "buff", "cost_mp": 6, "cost_stamina": 0, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 6, "essence": 5}}, "mod_duration": 3}],
         "utility": [{"id": "ember_elemental_heat_wave", "name": "Heat Wave", "power_type": "debuff", "damage_type": "magical", "damage": 6, "cost_mp": 5, "cost_stamina": 0, "cooldown": 2, "trigger": "opening_move",
                      "status_apply": "weary", "stat_mod": {"enemy": {"might": -4, "grace": -3}}, "mod_duration": 3}],
     },
     "signature_fusion": {"id": "ember_elemental_inferno", "name": "Inferno Burst", "power_type": "strike", "damage_type": "magical", "damage": 30, "cost_mp": 15, "cost_stamina": 0, "cooldown": 4, "hits": 3, "is_signature": True,
                          "status_apply": "burning", "unevadable": True, "stat_mod": {"enemy": {"might": -5, "armor_bonus": -5}}, "mod_duration": 4},
     "drops": {"common": [{"id": "ember_shard", "chance": 0.7, "qty": [1, 1]}], "rare": [{"id": "fire_crystal", "chance": 0.15, "qty": [1, 1]}], "boss": [], "gold": [25, 40], "xp_mult": 1.6}},
    {"id": "ember_mines_overseer", "name": "Ember Overseer", "biome": "ember_mines", "rarity": "rare", "hp": 105,
     "creature_tier": "mini_boss", "species": "construct", "archetype": "bruiser", "personality": "aggressive",
     "tags": ["construct"],
     "stats": {"might": {"base": 30, "growth": 2.4}, "grace": {"base": 12, "growth": 1.0}, "cognition": {"base": 14, "growth": 1.2},
               "insight": {"base": 16, "growth": 1.3}, "essence": {"base": 20, "growth": 1.6}, "durability": {"base": 28, "growth": 2.2}},
     "life": {"mp": 20, "stamina": 130, "shield": 10},
     "passive_buff": [{"type": "might_bonus", "value": 0.20}, {"type": "essence_bonus", "value": 0.16}],
     "profile_skills": {
         "attack": [{"id": "ember_overseer_magma_hammer", "name": "Magma Hammer", "power_type": "strike", "damage_type": "magical", "damage": 28, "cost_mp": 5, "cost_stamina": 25, "cooldown": 1, "trigger": "always",
                     "status_apply": "burning", "stat_mod": {"enemy": {"armor_bonus": -4}}, "mod_duration": 3},
                    {"id": "ember_overseer_flame_burst", "name": "Flame Burst", "power_type": "strike", "damage_type": "magical", "damage": 32, "cost_mp": 8, "cost_stamina": 0, "cooldown": 2, "trigger": "always",
                     "status_apply": "burning", "unevadable": True, "stat_mod": {"enemy": {"might": -5}}, "mod_duration": 3}],
         "defense": [{"id": "ember_overseer_magma_armor", "name": "Magma Armor", "power_type": "buff", "cost_mp": 5, "cost_stamina": 30, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 10, "essence": 6}}, "mod_duration": 3}],
         "utility": [{"id": "ember_overseer_heat_blast", "name": "Heat Blast", "power_type": "debuff", "damage_type": "magical", "damage": 8, "cost_mp": 8, "cost_stamina": 0, "cooldown": 2, "trigger": "opening_move",
                      "status_apply": "weary", "stat_mod": {"enemy": {"might": -5, "grace": -4, "cognition": -3}}, "mod_duration": 3}],
     },
     "signature_fusion": {"id": "ember_overseer_volcanic_eruption", "name": "Volcanic Eruption", "power_type": "strike", "damage_type": "magical", "damage": 40, "cost_mp": 15, "cost_stamina": 0, "cooldown": 4, "hits": 3, "is_signature": True,
                          "status_apply": "burning", "armor_ignore": True, "stat_mod": {"enemy": {"might": -6, "armor_bonus": -6}}, "mod_duration": 4},
     "drops": {"common": [{"id": "fire_crystal", "chance": 0.7, "qty": [1, 1]}], "rare": [{"id": "magma_scale", "chance": 0.2, "qty": [1, 1]}], "boss": [{"id": "overseer_helm", "chance": 0.2, "qty": [1, 1]}], "gold": [35, 65], "xp_mult": 1.8}},
    # ---- Crystal Caverns (Khardrum Lv 24) ----
    {"id": "crystal_spider", "name": "Crystal Spider", "biome": "crystal_caverns", "rarity": "common", "hp": 60,
     "creature_tier": "normal", "species": "beast", "archetype": "speed", "personality": "opportunist",
     "stats": {"might": {"base": 16, "growth": 1.4}, "grace": {"base": 22, "growth": 1.8}, "cognition": {"base": 14, "growth": 1.2},
               "insight": {"base": 16, "growth": 1.3}, "essence": {"base": 18, "growth": 1.5}, "durability": {"base": 12, "growth": 1.0}},
     "life": {"mp": 15, "stamina": 100, "shield": 0},
     "passive_buff": {"type": "grace_bonus", "value": 0.18, "secondary": {"type": "essence_bonus", "value": 0.12}},
     "profile_skills": {
         "attack": [{"id": "crystal_spider_shard_bite", "name": "Shard Bite", "power_type": "strike", "damage_type": "physical", "damage": 18, "cost_mp": 0, "cost_stamina": 20, "cooldown": 1, "trigger": "always",
                     "status_apply": "poisoned", "stat_mod": {"enemy": {"grace": -3}}, "mod_duration": 3}],
         "defense": [{"id": "crystal_spider_prism_shift", "name": "Prism Shift", "power_type": "buff", "cost_mp": 3, "cost_stamina": 0, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "evasive", "stat_mod": {"self": {"grace": 5, "essence": 3}}, "mod_duration": 2}],
         "utility": [{"id": "crystal_spider_web_trap", "name": "Crystal Web", "power_type": "debuff", "damage_type": "magical", "damage": 4, "cost_mp": 3, "cost_stamina": 0, "cooldown": 2, "trigger": "opening_move",
                      "status_apply": "ensnared", "stat_mod": {"enemy": {"grace": -4}}, "mod_duration": 3}],
     },
     "signature_fusion": {"id": "crystal_spider_shard_storm", "name": "Shard Storm", "power_type": "strike", "damage_type": "physical", "damage": 26, "cost_mp": 8, "cost_stamina": 0, "cooldown": 4, "hits": 4, "is_signature": True,
                          "status_apply": "poisoned", "unevadable": True, "stat_mod": {"enemy": {"grace": -5}}, "mod_duration": 3},
     "drops": {"common": [{"id": "crystal_shard", "chance": 0.7, "qty": [1, 1]}], "rare": [{"id": "gem_fragment", "chance": 0.1, "qty": [1, 1]}], "boss": [], "gold": [25, 40], "xp_mult": 1.6}},
    {"id": "gem_elemental", "name": "Gem Elemental", "biome": "crystal_caverns", "rarity": "uncommon", "hp": 70,
     "creature_tier": "normal", "species": "magical", "archetype": "caster", "personality": "opportunist",
     "stats": {"might": {"base": 14, "growth": 1.2}, "grace": {"base": 16, "growth": 1.3}, "cognition": {"base": 20, "growth": 1.6},
               "insight": {"base": 22, "growth": 1.8}, "essence": {"base": 24, "growth": 2.0}, "durability": {"base": 16, "growth": 1.3}},
     "life": {"mp": 35, "stamina": 60, "shield": 5},
     "passive_buff": {"type": "essence_bonus", "value": 0.20, "secondary": {"type": "magic_resist", "value": 0.15}},
     "profile_skills": {
         "attack": [{"id": "gem_elemental_prism_beam", "name": "Prism Beam", "power_type": "strike", "damage_type": "magical", "damage": 22, "cost_mp": 5, "cost_stamina": 0, "cooldown": 1, "trigger": "always",
                     "status_apply": "weary", "stat_mod": {"enemy": {"essence": -4}}, "mod_duration": 2},
                    {"id": "gem_elemental_refract_burst", "name": "Refract Burst", "power_type": "strike", "damage_type": "magical", "damage": 26, "cost_mp": 8, "cost_stamina": 0, "cooldown": 2, "trigger": "always",
                     "status_apply": "ensnared", "unevadable": True, "stat_mod": {"enemy": {"grace": -4}}, "mod_duration": 3}],
         "defense": [{"id": "gem_elemental_crystal_shell", "name": "Crystal Shell", "power_type": "buff", "cost_mp": 6, "cost_stamina": 0, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 8, "essence": 5}}, "mod_duration": 3}],
         "utility": [{"id": "gem_elemental_dazzle", "name": "Dazzle", "power_type": "debuff", "damage_type": "magical", "damage": 5, "cost_mp": 5, "cost_stamina": 0, "cooldown": 2, "trigger": "opening_move",
                      "status_apply": "weary", "stat_mod": {"enemy": {"cognition": -5, "insight": -4}}, "mod_duration": 3}],
     },
     "signature_fusion": {"id": "gem_elemental_spectral_nova", "name": "Spectral Nova", "power_type": "strike", "damage_type": "magical", "damage": 32, "cost_mp": 15, "cost_stamina": 0, "cooldown": 4, "hits": 3, "is_signature": True,
                          "status_apply": "weary", "unevadable": True, "stat_mod": {"enemy": {"essence": -6, "cognition": -5}}, "mod_duration": 4},
     "drops": {"common": [{"id": "crystal_shard", "chance": 0.7, "qty": [1, 1]}], "rare": [{"id": "gem_fragment", "chance": 0.15, "qty": [1, 1]}], "boss": [], "gold": [30, 45], "xp_mult": 1.7}},
    {"id": "crystal_caverns_warden", "name": "Crystal Warden", "biome": "crystal_caverns", "rarity": "rare", "hp": 110,
     "creature_tier": "mini_boss", "species": "magical", "archetype": "caster", "personality": "guardian",
     "stats": {"might": {"base": 18, "growth": 1.5}, "grace": {"base": 20, "growth": 1.6}, "cognition": {"base": 28, "growth": 2.2},
               "insight": {"base": 26, "growth": 2.0}, "essence": {"base": 28, "growth": 2.2}, "durability": {"base": 20, "growth": 1.6}},
     "life": {"mp": 50, "stamina": 80, "shield": 10},
     "passive_buff": [{"type": "essence_bonus", "value": 0.22}, {"type": "cognition_bonus", "value": 0.18}],
     "profile_skills": {
         "attack": [{"id": "crystal_warden_prism_cannon", "name": "Prism Cannon", "power_type": "strike", "damage_type": "magical", "damage": 30, "cost_mp": 8, "cost_stamina": 0, "cooldown": 1, "trigger": "always",
                     "status_apply": "weary", "stat_mod": {"enemy": {"essence": -5}}, "mod_duration": 3},
                    {"id": "crystal_warden_shard_prison", "name": "Shard Prison", "power_type": "strike", "damage_type": "magical", "damage": 34, "cost_mp": 10, "cost_stamina": 0, "cooldown": 2, "trigger": "always",
                     "status_apply": "ensnared", "unevadable": True, "stat_mod": {"enemy": {"grace": -5, "might": -4}}, "mod_duration": 3}],
         "defense": [{"id": "crystal_warden_diamond_shell", "name": "Diamond Shell", "power_type": "buff", "cost_mp": 10, "cost_stamina": 0, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 12, "essence": 7}}, "mod_duration": 3}],
         "utility": [{"id": "crystal_warden_resonance", "name": "Crystal Resonance", "power_type": "debuff", "damage_type": "magical", "damage": 8, "cost_mp": 10, "cost_stamina": 0, "cooldown": 3, "trigger": "opening_move",
                      "status_apply": "weary", "stat_mod": {"enemy": {"cognition": -6, "insight": -5, "essence": -4}}, "mod_duration": 4}],
     },
     "signature_fusion": {"id": "crystal_warden_spectral_apocalypse", "name": "Spectral Apocalypse", "power_type": "strike", "damage_type": "magical", "damage": 42, "cost_mp": 20, "cost_stamina": 0, "cooldown": 4, "hits": 3, "is_signature": True,
                          "status_apply": "ensnared", "unevadable": True, "stat_mod": {"enemy": {"essence": -7, "grace": -6}}, "mod_duration": 4},
     "drops": {"common": [{"id": "gem_fragment", "chance": 0.8, "qty": [1, 2]}], "rare": [{"id": "rare_gem", "chance": 0.2, "qty": [1, 1]}], "boss": [{"id": "warden_crystal_core", "chance": 0.2, "qty": [1, 1]}], "gold": [40, 75], "xp_mult": 1.9}},
    # ---- Deep Forges (Khardrum Lv 30) ----
    {"id": "forge_automaton", "name": "Forge Automaton", "biome": "deep_forges", "rarity": "common", "hp": 80,
     "creature_tier": "normal", "species": "construct", "archetype": "bruiser", "personality": "guardian",
     "tags": ["construct"],
     "stats": {"might": {"base": 30, "growth": 2.4}, "grace": {"base": 10, "growth": 0.8}, "cognition": {"base": 8, "growth": 0.7},
               "insight": {"base": 10, "growth": 0.8}, "essence": {"base": 14, "growth": 1.2}, "durability": {"base": 26, "growth": 2.0}},
     "life": {"mp": 0, "stamina": 140, "shield": 10},
     "passive_buff": {"type": "might_bonus", "value": 0.18, "secondary": {"type": "durability_bonus", "value": 0.14}},
     "profile_skills": {
         "attack": [{"id": "forge_automaton_hammer_swing", "name": "Hammer Swing", "power_type": "strike", "damage_type": "physical", "damage": 24, "cost_mp": 0, "cost_stamina": 25, "cooldown": 1, "trigger": "always",
                     "status_apply": "stunned", "stat_mod": {"enemy": {"armor_bonus": -4}}, "mod_duration": 2}],
         "defense": [{"id": "forge_automaton_plate_armor", "name": "Plate Armor", "power_type": "buff", "cost_mp": 0, "cost_stamina": 30, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 10, "durability": 6}}, "mod_duration": 3}],
         "utility": [{"id": "forge_automaton_steam_vent", "name": "Steam Vent", "power_type": "debuff", "damage_type": "magical", "damage": 6, "cost_mp": 0, "cost_stamina": 25, "cooldown": 2, "trigger": "opening_move",
                      "status_apply": "weary", "stat_mod": {"enemy": {"grace": -4, "cognition": -3}}, "mod_duration": 3}],
     },
     "signature_fusion": {"id": "forge_automaton_grand_slam", "name": "Grand Slam", "power_type": "strike", "damage_type": "physical", "damage": 34, "cost_mp": 0, "cost_stamina": 50, "cooldown": 4, "hits": 2, "is_signature": True,
                          "status_apply": "stunned", "armor_ignore": True, "stat_mod": {"enemy": {"might": -5, "armor_bonus": -5}}, "mod_duration": 3},
     "drops": {"common": [{"id": "iron_ore", "chance": 0.7, "qty": [1, 2]}, {"id": "steel_ingot", "chance": 0.3, "qty": [1, 1]}], "rare": [], "boss": [], "gold": [30, 50], "xp_mult": 1.7}},
    {"id": "molten_titan", "name": "Molten Titan", "biome": "deep_forges", "rarity": "uncommon", "hp": 90,
     "creature_tier": "normal", "species": "construct", "archetype": "tank", "personality": "aggressive",
     "tags": ["construct"],
     "stats": {"might": {"base": 32, "growth": 2.6}, "grace": {"base": 8, "growth": 0.7}, "cognition": {"base": 6, "growth": 0.5},
               "insight": {"base": 8, "growth": 0.7}, "essence": {"base": 18, "growth": 1.5}, "durability": {"base": 30, "growth": 2.4}},
     "life": {"mp": 10, "stamina": 140, "shield": 15},
     "passive_buff": {"type": "durability_bonus", "value": 0.22, "secondary": {"type": "essence_bonus", "value": 0.14}},
     "profile_skills": {
         "attack": [{"id": "molten_titan_magma_fist", "name": "Magma Fist", "power_type": "strike", "damage_type": "magical", "damage": 26, "cost_mp": 5, "cost_stamina": 25, "cooldown": 1, "trigger": "always",
                     "status_apply": "burning", "stat_mod": {"enemy": {"armor_bonus": -4}}, "mod_duration": 3},
                    {"id": "molten_titan_heat_wave", "name": "Heat Wave Slam", "power_type": "strike", "damage_type": "magical", "damage": 30, "cost_mp": 8, "cost_stamina": 35, "cooldown": 2, "trigger": "always",
                     "status_apply": "burning", "unevadable": True, "stat_mod": {"enemy": {"might": -5}}, "mod_duration": 3}],
         "defense": [{"id": "molten_titan_magma_skin", "name": "Magma Skin", "power_type": "buff", "cost_mp": 5, "cost_stamina": 30, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 12, "essence": 6}}, "mod_duration": 3}],
         "utility": [{"id": "molten_titan_earthquake", "name": "Earthquake", "power_type": "debuff", "damage_type": "physical", "damage": 8, "cost_mp": 5, "cost_stamina": 30, "cooldown": 2, "trigger": "opening_move",
                      "status_apply": "stunned", "stat_mod": {"enemy": {"grace": -5, "might": -4}}, "mod_duration": 3}],
     },
     "signature_fusion": {"id": "molten_titan_volcanic_fist", "name": "Volcanic Fist", "power_type": "strike", "damage_type": "magical", "damage": 38, "cost_mp": 15, "cost_stamina": 0, "cooldown": 4, "hits": 2, "is_signature": True,
                          "status_apply": "burning", "armor_ignore": True, "stat_mod": {"enemy": {"might": -6, "armor_bonus": -6}}, "mod_duration": 4},
     "drops": {"common": [{"id": "steel_ingot", "chance": 0.6, "qty": [1, 1]}, {"id": "fire_crystal", "chance": 0.3, "qty": [1, 1]}], "rare": [{"id": "jahra_ingot", "chance": 0.1, "qty": [1, 1]}], "boss": [], "gold": [35, 55], "xp_mult": 1.8}},
    {"id": "deep_forges_master", "name": "Forge Master", "biome": "deep_forges", "rarity": "rare", "hp": 130,
     "creature_tier": "boss", "species": "humanoid", "archetype": "bruiser", "personality": "aggressive",
     "is_boss": True,
     "stats": {"might": {"base": 40, "growth": 3.0}, "grace": {"base": 16, "growth": 1.3}, "cognition": {"base": 18, "growth": 1.5},
               "insight": {"base": 16, "growth": 1.3}, "essence": {"base": 22, "growth": 1.8}, "durability": {"base": 32, "growth": 2.5}},
     "life": {"mp": 30, "stamina": 160, "shield": 15},
     "passive_buff": [{"type": "might_bonus", "value": 0.25}, {"type": "durability_bonus", "value": 0.20}, {"type": "essence_bonus", "value": 0.15}],
     "boss_aura": {"id": "forge_heat", "name": "Forge Heat", "effect": "burning", "desc": "All enemies take burn damage each turn and have reduced armor."},
     "profile_skills": {
         "attack": [{"id": "forge_master_god_hammer", "name": "God Hammer", "power_type": "strike", "damage_type": "magical", "damage": 34, "cost_mp": 6, "cost_stamina": 25, "cooldown": 1, "trigger": "always",
                     "status_apply": "burning", "stat_mod": {"enemy": {"armor_bonus": -5}}, "mod_duration": 3},
                    {"id": "forge_master_anvil_crash", "name": "Anvil Crash", "power_type": "strike", "damage_type": "physical", "damage": 40, "cost_mp": 0, "cost_stamina": 35, "cooldown": 2, "trigger": "always",
                     "status_apply": "stunned", "armor_ignore": True, "stat_mod": {"enemy": {"might": -6}}, "mod_duration": 3}],
         "defense": [{"id": "forge_master_jahra_bulwark", "name": "Jahra Bulwark", "power_type": "buff", "cost_mp": 6, "cost_stamina": 30, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 12, "durability": 8}}, "mod_duration": 3},
                    {"id": "forge_master_mend_steel", "name": "Mend Steel", "power_type": "heal", "cost_mp": 10, "cost_stamina": 0, "cooldown": 4, "trigger": "low_hp",
                      "heal_percent": 0.15, "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 6}}, "mod_duration": 3}],
         "utility": [{"id": "forge_master_forge_roar", "name": "Forge Roar", "power_type": "debuff", "damage_type": "magical", "damage": 10, "cost_mp": 8, "cost_stamina": 0, "cooldown": 3, "trigger": "opening_move",
                      "status_apply": "weary", "stat_mod": {"enemy": {"might": -6, "cognition": -5, "grace": -4}}, "mod_duration": 4}],
     },
     "signature_fusion": [{"id": "forge_master_cataclysm_forge", "name": "Cataclysm Forge", "power_type": "strike", "damage_type": "magical", "damage": 50, "cost_mp": 20, "cost_stamina": 0, "cooldown": 5, "hits": 3, "is_signature": True,
                          "status_apply": "burning", "armor_ignore": True, "stat_mod": {"enemy": {"might": -8, "armor_bonus": -8}}, "mod_duration": 4},
                         {"id": "forge_master_iron_will", "name": "Iron Will", "power_type": "strike", "damage_type": "physical", "damage": 42, "cost_mp": 0, "cost_stamina": 50, "cooldown": 4, "hits": 2, "is_signature": True,
                          "status_apply": "stunned", "armor_ignore": True, "stat_mod": {"enemy": {"might": -7, "grace": -6}}, "mod_duration": 4}],
     "drops": {"common": [{"id": "steel_ingot", "chance": 0.9, "qty": [2, 3]}], "rare": [{"id": "jahra_ingot", "chance": 0.3, "qty": [1, 1]}], "boss": [{"id": "forge_master_hammer", "chance": 0.15, "qty": [1, 1]}, {"id": "jahra_blueprint", "chance": 0.1, "qty": [1, 1]}], "gold": [60, 120], "xp_mult": 2.2}},
    # ---- Sunlit Canopy (Haya Lv 26) ----
    {"id": "sunbeam_sprite", "name": "Sunbeam Sprite", "biome": "sunlit_canopy", "rarity": "common", "hp": 55,
     "creature_tier": "normal", "species": "magical", "archetype": "caster", "personality": "opportunist",
     "stats": {"might": {"base": 8, "growth": 0.7}, "grace": {"base": 18, "growth": 1.5}, "cognition": {"base": 22, "growth": 1.8},
               "insight": {"base": 24, "growth": 2.0}, "essence": {"base": 26, "growth": 2.2}, "durability": {"base": 10, "growth": 0.9}},
     "life": {"mp": 35, "stamina": 60, "shield": 0},
     "passive_buff": {"type": "essence_bonus", "value": 0.20, "secondary": {"type": "insight_bonus", "value": 0.12}},
     "profile_skills": {
         "attack": [{"id": "sunbeam_sprite_solar_lance", "name": "Solar Lance", "power_type": "strike", "damage_type": "magical", "damage": 22, "cost_mp": 5, "cost_stamina": 0, "cooldown": 1, "trigger": "always",
                     "status_apply": "burning", "stat_mod": {"enemy": {"essence": -4}}, "mod_duration": 2}],
         "defense": [{"id": "sunbeam_sprite_light_veil", "name": "Light Veil", "power_type": "buff", "cost_mp": 5, "cost_stamina": 0, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "evasive", "stat_mod": {"self": {"grace": 5, "essence": 3}}, "mod_duration": 2}],
         "utility": [{"id": "sunbeam_sprite_healing_light", "name": "Healing Light", "power_type": "heal", "cost_mp": 6, "cost_stamina": 0, "cooldown": 3, "trigger": "low_hp",
                      "heal_percent": 0.10, "self_status": "warded"}],
     },
     "signature_fusion": {"id": "sunbeam_sprite_solar_burst", "name": "Solar Burst", "power_type": "strike", "damage_type": "magical", "damage": 30, "cost_mp": 12, "cost_stamina": 0, "cooldown": 4, "hits": 3, "is_signature": True,
                          "status_apply": "burning", "unevadable": True, "stat_mod": {"enemy": {"essence": -5}}, "mod_duration": 3},
     "drops": {"common": [{"id": "solar_petal", "chance": 0.7, "qty": [1, 1]}, {"id": "light_essence", "chance": 0.3, "qty": [1, 1]}], "rare": [], "boss": [], "gold": [25, 40], "xp_mult": 1.6}},
    {"id": "canopy_stag", "name": "Canopy Stag", "biome": "sunlit_canopy", "rarity": "uncommon", "hp": 70,
     "creature_tier": "normal", "species": "beast", "archetype": "bruiser", "personality": "guardian",
     "stats": {"might": {"base": 28, "growth": 2.2}, "grace": {"base": 18, "growth": 1.5}, "cognition": {"base": 14, "growth": 1.2},
               "insight": {"base": 16, "growth": 1.3}, "essence": {"base": 20, "growth": 1.6}, "durability": {"base": 20, "growth": 1.6}},
     "life": {"mp": 15, "stamina": 110, "shield": 0},
     "passive_buff": {"type": "might_bonus", "value": 0.18, "secondary": {"type": "essence_bonus", "value": 0.14}},
     "profile_skills": {
         "attack": [{"id": "canopy_stag_antler_charge", "name": "Antler Charge", "power_type": "strike", "damage_type": "physical", "damage": 24, "cost_mp": 0, "cost_stamina": 25, "cooldown": 1, "trigger": "always",
                     "status_apply": "stunned", "stat_mod": {"enemy": {"armor_bonus": -4}}, "mod_duration": 2},
                    {"id": "canopy_stag_solar_antlers", "name": "Solar Antlers", "power_type": "strike", "damage_type": "magical", "damage": 26, "cost_mp": 5, "cost_stamina": 0, "cooldown": 2, "trigger": "always",
                     "status_apply": "burning", "stat_mod": {"enemy": {"might": -4}}, "mod_duration": 3}],
         "defense": [{"id": "canopy_stag_bark_hide", "name": "Bark Hide", "power_type": "buff", "cost_mp": 3, "cost_stamina": 25, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 8, "essence": 4}}, "mod_duration": 3}],
         "utility": [{"id": "canopy_stag_forest_blessing", "name": "Forest Blessing", "power_type": "heal", "cost_mp": 5, "cost_stamina": 0, "cooldown": 3, "trigger": "low_hp",
                      "heal_percent": 0.12, "self_status": "inspired", "stat_mod": {"self": {"might": 3, "essence": 3}}, "mod_duration": 2}],
     },
     "signature_fusion": {"id": "canopy_stag_solar_charge", "name": "Solar Charge", "power_type": "strike", "damage_type": "magical", "damage": 34, "cost_mp": 10, "cost_stamina": 25, "cooldown": 4, "hits": 2, "is_signature": True,
                          "status_apply": "stunned", "armor_ignore": True, "stat_mod": {"enemy": {"might": -5, "essence": -5}}, "mod_duration": 3},
     "drops": {"common": [{"id": "solar_petal", "chance": 0.6, "qty": [1, 1]}, {"id": "stag_antler", "chance": 0.4, "qty": [1, 1]}], "rare": [{"id": "light_essence", "chance": 0.15, "qty": [1, 1]}], "boss": [], "gold": [30, 45], "xp_mult": 1.7}},
    {"id": "sunlit_warden", "name": "Sunlit Warden", "biome": "sunlit_canopy", "rarity": "rare", "hp": 115,
     "creature_tier": "mini_boss", "species": "magical", "archetype": "caster", "personality": "guardian",
     "stats": {"might": {"base": 16, "growth": 1.3}, "grace": {"base": 20, "growth": 1.6}, "cognition": {"base": 28, "growth": 2.2},
               "insight": {"base": 30, "growth": 2.4}, "essence": {"base": 30, "growth": 2.4}, "durability": {"base": 18, "growth": 1.4}},
     "life": {"mp": 60, "stamina": 70, "shield": 5},
     "passive_buff": [{"type": "essence_bonus", "value": 0.24}, {"type": "insight_bonus", "value": 0.18}],
     "profile_skills": {
         "attack": [{"id": "sunlit_warden_solar_beam", "name": "Solar Beam", "power_type": "strike", "damage_type": "magical", "damage": 32, "cost_mp": 8, "cost_stamina": 0, "cooldown": 1, "trigger": "always",
                     "status_apply": "burning", "unevadable": True, "stat_mod": {"enemy": {"essence": -5}}, "mod_duration": 3},
                    {"id": "sunlit_warden_photonic_lance", "name": "Photonic Lance", "power_type": "strike", "damage_type": "magical", "damage": 36, "cost_mp": 10, "cost_stamina": 0, "cooldown": 2, "trigger": "always",
                     "status_apply": "weary", "stat_mod": {"enemy": {"cognition": -5, "insight": -4}}, "mod_duration": 3}],
         "defense": [{"id": "sunlit_warden_radiant_barrier", "name": "Radiant Barrier", "power_type": "buff", "cost_mp": 10, "cost_stamina": 0, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 10, "essence": 7}}, "mod_duration": 3}],
         "utility": [{"id": "sunlit_warden_solar_mend", "name": "Solar Mend", "power_type": "heal", "cost_mp": 12, "cost_stamina": 0, "cooldown": 3, "trigger": "low_hp",
                      "heal_percent": 0.15, "self_status": "inspired", "stat_mod": {"self": {"essence": 5}}, "mod_duration": 3}],
     },
     "signature_fusion": {"id": "sunlit_warden_dawn_breaker", "name": "Dawn Breaker", "power_type": "strike", "damage_type": "magical", "damage": 44, "cost_mp": 20, "cost_stamina": 0, "cooldown": 4, "hits": 3, "is_signature": True,
                          "status_apply": "burning", "unevadable": True, "armor_ignore": True, "stat_mod": {"enemy": {"essence": -7, "cognition": -6}}, "mod_duration": 4},
     "drops": {"common": [{"id": "light_essence", "chance": 0.8, "qty": [1, 2]}], "rare": [{"id": "solar_crystal", "chance": 0.2, "qty": [1, 1]}], "boss": [{"id": "warden_solar_crown", "chance": 0.2, "qty": [1, 1]}], "gold": [40, 75], "xp_mult": 1.9}},
    # ---- Moonveil Woods (Haya Lv 30) ----
    {"id": "moonveil_wisp", "name": "Moonveil Wisp", "biome": "moonveil_woods", "rarity": "common", "hp": 60,
     "creature_tier": "normal", "species": "magical", "archetype": "caster", "personality": "opportunist",
     "stats": {"might": {"base": 6, "growth": 0.5}, "grace": {"base": 20, "growth": 1.6}, "cognition": {"base": 24, "growth": 2.0},
               "insight": {"base": 26, "growth": 2.1}, "essence": {"base": 28, "growth": 2.2}, "durability": {"base": 10, "growth": 0.8}},
     "life": {"mp": 40, "stamina": 50, "shield": 0},
     "passive_buff": {"type": "essence_bonus", "value": 0.22, "secondary": {"type": "evasion_bonus", "value": 0.14}},
     "profile_skills": {
         "attack": [{"id": "moonveil_wisp_lunar_bolt", "name": "Lunar Bolt", "power_type": "strike", "damage_type": "magical", "damage": 24, "cost_mp": 5, "cost_stamina": 0, "cooldown": 1, "trigger": "always",
                     "status_apply": "weary", "stat_mod": {"enemy": {"essence": -4}}, "mod_duration": 2},
                    {"id": "moonveil_wisp_illusion_strike", "name": "Illusion Strike", "power_type": "strike", "damage_type": "magical", "damage": 26, "cost_mp": 7, "cost_stamina": 0, "cooldown": 2, "trigger": "always",
                     "status_apply": "weary", "unevadable": True, "stat_mod": {"enemy": {"cognition": -4, "grace": -3}}, "mod_duration": 3}],
         "defense": [{"id": "moonveil_wisp_phase", "name": "Moon Phase", "power_type": "buff", "cost_mp": 6, "cost_stamina": 0, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "evasive", "stat_mod": {"self": {"grace": 6, "essence": 4}}, "mod_duration": 2}],
         "utility": [{"id": "moonveil_wisp_hypnotic_glow", "name": "Hypnotic Glow", "power_type": "debuff", "damage_type": "magical", "damage": 6, "cost_mp": 6, "cost_stamina": 0, "cooldown": 2, "trigger": "opening_move",
                      "status_apply": "weary", "stat_mod": {"enemy": {"cognition": -5, "insight": -4}}, "mod_duration": 3}],
     },
     "signature_fusion": {"id": "moonveil_wisp_lunar_eclipse", "name": "Lunar Eclipse", "power_type": "strike", "damage_type": "magical", "damage": 34, "cost_mp": 15, "cost_stamina": 0, "cooldown": 4, "hits": 3, "is_signature": True,
                          "status_apply": "weary", "unevadable": True, "stat_mod": {"enemy": {"essence": -6, "cognition": -5}}, "mod_duration": 4},
     "drops": {"common": [{"id": "moonveil_petal", "chance": 0.7, "qty": [1, 1]}, {"id": "lunar_essence", "chance": 0.3, "qty": [1, 1]}], "rare": [], "boss": [], "gold": [30, 45], "xp_mult": 1.7}},
    {"id": "shadow_stalker", "name": "Shadow Stalker", "biome": "moonveil_woods", "rarity": "uncommon", "hp": 65,
     "creature_tier": "normal", "species": "beast", "archetype": "striker", "personality": "opportunist",
     "stats": {"might": {"base": 26, "growth": 2.0}, "grace": {"base": 24, "growth": 2.0}, "cognition": {"base": 14, "growth": 1.2},
               "insight": {"base": 18, "growth": 1.5}, "essence": {"base": 16, "growth": 1.3}, "durability": {"base": 14, "growth": 1.2}},
     "life": {"mp": 10, "stamina": 110, "shield": 0},
     "passive_buff": {"type": "grace_bonus", "value": 0.20, "secondary": {"type": "evasion_bonus", "value": 0.14}},
     "profile_skills": {
         "attack": [{"id": "shadow_stalker_ambush", "name": "Shadow Ambush", "power_type": "strike", "damage_type": "physical", "damage": 26, "cost_mp": 0, "cost_stamina": 20, "cooldown": 1, "trigger": "always",
                     "status_apply": "bleeding", "unevadable": True, "stat_mod": {"enemy": {"grace": -4}}, "mod_duration": 3},
                    {"id": "shadow_stalker_shadow_rip", "name": "Shadow Rip", "power_type": "strike", "damage_type": "magical", "damage": 28, "cost_mp": 5, "cost_stamina": 0, "cooldown": 2, "trigger": "always",
                     "status_apply": "weary", "stat_mod": {"enemy": {"might": -4, "grace": -3}}, "mod_duration": 3}],
         "defense": [{"id": "shadow_stalker_vanish", "name": "Vanish", "power_type": "buff", "cost_mp": 5, "cost_stamina": 0, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "evasive", "stat_mod": {"self": {"grace": 6}}, "mod_duration": 2}],
         "utility": [{"id": "shadow_stalker_terror", "name": "Shadow Terror", "power_type": "debuff", "damage_type": "magical", "damage": 6, "cost_mp": 5, "cost_stamina": 0, "cooldown": 2, "trigger": "opening_move",
                      "status_apply": "weary", "stat_mod": {"enemy": {"might": -5, "cognition": -4}}, "mod_duration": 3}],
     },
     "signature_fusion": {"id": "shadow_stalker_eclipse_fang", "name": "Eclipse Fang", "power_type": "strike", "damage_type": "magical", "damage": 36, "cost_mp": 10, "cost_stamina": 0, "cooldown": 4, "hits": 3, "is_signature": True,
                          "status_apply": "bleeding", "unevadable": True, "lifesteal": 0.20, "stat_mod": {"enemy": {"grace": -5}}, "mod_duration": 4},
     "drops": {"common": [{"id": "moonveil_petal", "chance": 0.6, "qty": [1, 1]}, {"id": "shadow_pelt", "chance": 0.4, "qty": [1, 1]}], "rare": [{"id": "lunar_essence", "chance": 0.15, "qty": [1, 1]}], "boss": [], "gold": [35, 50], "xp_mult": 1.8}},
    {"id": "moonveil_illusionist", "name": "Moonveil Illusionist", "biome": "moonveil_woods", "rarity": "rare", "hp": 100,
     "creature_tier": "mini_boss", "species": "magical", "archetype": "caster", "personality": "opportunist",
     "stats": {"might": {"base": 10, "growth": 0.8}, "grace": {"base": 22, "growth": 1.8}, "cognition": {"base": 32, "growth": 2.5},
               "insight": {"base": 34, "growth": 2.6}, "essence": {"base": 32, "growth": 2.5}, "durability": {"base": 16, "growth": 1.3}},
     "life": {"mp": 70, "stamina": 60, "shield": 0},
     "passive_buff": [{"type": "essence_bonus", "value": 0.24}, {"type": "cognition_bonus", "value": 0.20}],
     "profile_skills": {
         "attack": [{"id": "moonveil_illusionist_lunar_storm", "name": "Lunar Storm", "power_type": "strike", "damage_type": "magical", "damage": 34, "cost_mp": 8, "cost_stamina": 0, "cooldown": 1, "trigger": "always",
                     "status_apply": "weary", "unevadable": True, "stat_mod": {"enemy": {"essence": -5}}, "mod_duration": 3},
                    {"id": "moonveil_illusionist_mirror_image", "name": "Mirror Image Strike", "power_type": "strike", "damage_type": "magical", "damage": 38, "cost_mp": 10, "cost_stamina": 0, "cooldown": 2, "trigger": "always",
                     "status_apply": "weary", "unevadable": True, "stat_mod": {"enemy": {"cognition": -6, "grace": -4}}, "mod_duration": 3}],
         "defense": [{"id": "moonveil_illusionist_phase_shift", "name": "Phase Shift", "power_type": "buff", "cost_mp": 10, "cost_stamina": 0, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "evasive", "stat_mod": {"self": {"grace": 8, "essence": 5}}, "mod_duration": 3}],
         "utility": [{"id": "moonveil_illusionist_mass_hallucination", "name": "Mass Hallucination", "power_type": "debuff", "damage_type": "magical", "damage": 10, "cost_mp": 12, "cost_stamina": 0, "cooldown": 3, "trigger": "opening_move",
                      "status_apply": "weary", "stat_mod": {"enemy": {"cognition": -7, "insight": -6, "might": -4}}, "mod_duration": 4}],
     },
     "signature_fusion": {"id": "moonveil_illusionist_eclipse_realm", "name": "Eclipse Realm", "power_type": "strike", "damage_type": "magical", "damage": 46, "cost_mp": 20, "cost_stamina": 0, "cooldown": 4, "hits": 3, "is_signature": True,
                          "status_apply": "weary", "unevadable": True, "armor_ignore": True, "stat_mod": {"enemy": {"essence": -7, "cognition": -7}}, "mod_duration": 4},
     "drops": {"common": [{"id": "lunar_essence", "chance": 0.8, "qty": [1, 2]}], "rare": [{"id": "illusion_shard", "chance": 0.2, "qty": [1, 1]}], "boss": [{"id": "illusionist_mask", "chance": 0.2, "qty": [1, 1]}], "gold": [45, 80], "xp_mult": 2.0}},
    # ---- Celestial Lake (Haya Lv 34) ----
    {"id": "lake_spirit", "name": "Lake Spirit", "biome": "celestial_lake", "rarity": "common", "hp": 65,
     "creature_tier": "normal", "species": "magical", "archetype": "caster", "personality": "opportunist",
     "stats": {"might": {"base": 8, "growth": 0.7}, "grace": {"base": 20, "growth": 1.6}, "cognition": {"base": 26, "growth": 2.0},
               "insight": {"base": 28, "growth": 2.2}, "essence": {"base": 30, "growth": 2.4}, "durability": {"base": 12, "growth": 1.0}},
     "life": {"mp": 45, "stamina": 50, "shield": 0},
     "passive_buff": {"type": "essence_bonus", "value": 0.22, "secondary": {"type": "insight_bonus", "value": 0.14}},
     "profile_skills": {
         "attack": [{"id": "lake_spirit_water_lance", "name": "Water Lance", "power_type": "strike", "damage_type": "magical", "damage": 26, "cost_mp": 5, "cost_stamina": 0, "cooldown": 1, "trigger": "always",
                     "status_apply": "weary", "stat_mod": {"enemy": {"essence": -4}}, "mod_duration": 2},
                    {"id": "lake_spirit_song_bolt", "name": "Song Bolt", "power_type": "strike", "damage_type": "magical", "damage": 28, "cost_mp": 7, "cost_stamina": 0, "cooldown": 2, "trigger": "always",
                     "status_apply": "ensnared", "unevadable": True, "stat_mod": {"enemy": {"grace": -4}}, "mod_duration": 3}],
         "defense": [{"id": "lake_spirit_water_veil", "name": "Water Veil", "power_type": "buff", "cost_mp": 6, "cost_stamina": 0, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "evasive", "stat_mod": {"self": {"grace": 6, "essence": 4}}, "mod_duration": 2}],
         "utility": [{"id": "lake_spirit_healing_song", "name": "Healing Song", "power_type": "heal", "cost_mp": 8, "cost_stamina": 0, "cooldown": 3, "trigger": "low_hp",
                      "heal_percent": 0.12, "self_status": "warded"}],
     },
     "signature_fusion": {"id": "lake_spirit_celestial_tide", "name": "Celestial Tide", "power_type": "strike", "damage_type": "magical", "damage": 36, "cost_mp": 15, "cost_stamina": 0, "cooldown": 4, "hits": 3, "is_signature": True,
                          "status_apply": "ensnared", "unevadable": True, "stat_mod": {"enemy": {"essence": -6, "grace": -5}}, "mod_duration": 4},
     "drops": {"common": [{"id": "lake_crystal", "chance": 0.7, "qty": [1, 1]}, {"id": "water_essence", "chance": 0.3, "qty": [1, 1]}], "rare": [], "boss": [], "gold": [35, 50], "xp_mult": 1.8}},
    {"id": "starlight_serppent", "name": "Starlight Serpent", "biome": "celestial_lake", "rarity": "uncommon", "hp": 75,
     "creature_tier": "normal", "species": "beast", "archetype": "caster", "personality": "opportunist",
     "stats": {"might": {"base": 14, "growth": 1.2}, "grace": {"base": 22, "growth": 1.8}, "cognition": {"base": 24, "growth": 2.0},
               "insight": {"base": 26, "growth": 2.0}, "essence": {"base": 28, "growth": 2.2}, "durability": {"base": 16, "growth": 1.3}},
     "life": {"mp": 40, "stamina": 70, "shield": 0},
     "passive_buff": {"type": "essence_bonus", "value": 0.22, "secondary": {"type": "grace_bonus", "value": 0.14}},
     "profile_skills": {
         "attack": [{"id": "starlight_serpent_star_breath", "name": "Star Breath", "power_type": "strike", "damage_type": "magical", "damage": 28, "cost_mp": 6, "cost_stamina": 0, "cooldown": 1, "trigger": "always",
                     "status_apply": "burning", "stat_mod": {"enemy": {"essence": -4}}, "mod_duration": 3},
                    {"id": "starlight_serpent_constellation", "name": "Constellation Strike", "power_type": "strike", "damage_type": "magical", "damage": 30, "cost_mp": 8, "cost_stamina": 0, "cooldown": 2, "trigger": "always",
                     "status_apply": "ensnared", "unevadable": True, "stat_mod": {"enemy": {"grace": -5}}, "mod_duration": 3}],
         "defense": [{"id": "starlight_serpent_celestial_scales", "name": "Celestial Scales", "power_type": "buff", "cost_mp": 6, "cost_stamina": 0, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 8, "essence": 5}}, "mod_duration": 3}],
         "utility": [{"id": "starlight_serpent_lullaby", "name": "Star Lullaby", "power_type": "debuff", "damage_type": "magical", "damage": 6, "cost_mp": 6, "cost_stamina": 0, "cooldown": 2, "trigger": "opening_move",
                      "status_apply": "weary", "stat_mod": {"enemy": {"cognition": -5, "insight": -4}}, "mod_duration": 3}],
     },
     "signature_fusion": {"id": "starlight_serpent_supernova", "name": "Supernova", "power_type": "strike", "damage_type": "magical", "damage": 40, "cost_mp": 15, "cost_stamina": 0, "cooldown": 4, "hits": 3, "is_signature": True,
                          "status_apply": "burning", "unevadable": True, "armor_ignore": True, "stat_mod": {"enemy": {"essence": -6, "grace": -5}}, "mod_duration": 4},
     "drops": {"common": [{"id": "lake_crystal", "chance": 0.6, "qty": [1, 1]}, {"id": "starlight_scale", "chance": 0.4, "qty": [1, 1]}], "rare": [{"id": "water_essence", "chance": 0.15, "qty": [1, 1]}], "boss": [], "gold": [40, 55], "xp_mult": 1.9}},
    {"id": "celestial_lake_oracle", "name": "Lake Oracle", "biome": "celestial_lake", "rarity": "rare", "hp": 110,
     "creature_tier": "mini_boss", "species": "magical", "archetype": "caster", "personality": "guardian",
     "stats": {"might": {"base": 12, "growth": 1.0}, "grace": {"base": 22, "growth": 1.8}, "cognition": {"base": 34, "growth": 2.6},
               "insight": {"base": 36, "growth": 2.8}, "essence": {"base": 36, "growth": 2.8}, "durability": {"base": 18, "growth": 1.4}},
     "life": {"mp": 80, "stamina": 50, "shield": 5},
     "passive_buff": [{"type": "essence_bonus", "value": 0.26}, {"type": "cognition_bonus", "value": 0.20}],
     "profile_skills": {
         "attack": [{"id": "lake_oracle_celestial_judgement", "name": "Celestial Judgement", "power_type": "strike", "damage_type": "magical", "damage": 36, "cost_mp": 10, "cost_stamina": 0, "cooldown": 1, "trigger": "always",
                     "status_apply": "weary", "unevadable": True, "stat_mod": {"enemy": {"essence": -6}}, "mod_duration": 3},
                    {"id": "lake_oracle_starfall", "name": "Starfall", "power_type": "strike", "damage_type": "magical", "damage": 40, "cost_mp": 12, "cost_stamina": 0, "cooldown": 2, "trigger": "always",
                     "status_apply": "burning", "unevadable": True, "armor_ignore": True, "stat_mod": {"enemy": {"might": -5, "essence": -5}}, "mod_duration": 3}],
         "defense": [{"id": "lake_oracle_celestial_barrier", "name": "Celestial Barrier", "power_type": "buff", "cost_mp": 12, "cost_stamina": 0, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 12, "essence": 8}}, "mod_duration": 3}],
         "utility": [{"id": "lake_oracle_oracle_vision", "name": "Oracle Vision", "power_type": "debuff", "damage_type": "magical", "damage": 10, "cost_mp": 12, "cost_stamina": 0, "cooldown": 3, "trigger": "opening_move",
                      "status_apply": "weary", "stat_mod": {"enemy": {"cognition": -7, "insight": -6, "essence": -5}}, "mod_duration": 4}],
     },
     "signature_fusion": {"id": "lake_oracle_celestial_apocalypse", "name": "Celestial Apocalypse", "power_type": "strike", "damage_type": "magical", "damage": 50, "cost_mp": 25, "cost_stamina": 0, "cooldown": 4, "hits": 3, "is_signature": True,
                          "status_apply": "burning", "unevadable": True, "armor_ignore": True, "stat_mod": {"enemy": {"essence": -8, "cognition": -7}}, "mod_duration": 4},
     "drops": {"common": [{"id": "water_essence", "chance": 0.8, "qty": [1, 2]}], "rare": [{"id": "celestial_shard", "chance": 0.2, "qty": [1, 1]}], "boss": [{"id": "oracle_diadem", "chance": 0.2, "qty": [1, 1]}], "gold": [50, 90], "xp_mult": 2.1}},
    # ---- Starfall Cliffs (Haya Lv 38) ----
    {"id": "starfall_hawk", "name": "Starfall Hawk", "biome": "starfall_cliffs", "rarity": "common", "hp": 65,
     "creature_tier": "normal", "species": "beast", "archetype": "speed", "personality": "aggressive",
     "stats": {"might": {"base": 24, "growth": 2.0}, "grace": {"base": 28, "growth": 2.2}, "cognition": {"base": 16, "growth": 1.3},
               "insight": {"base": 18, "growth": 1.5}, "essence": {"base": 20, "growth": 1.6}, "durability": {"base": 14, "growth": 1.2}},
     "life": {"mp": 15, "stamina": 110, "shield": 0},
     "passive_buff": {"type": "grace_bonus", "value": 0.22, "secondary": {"type": "might_bonus", "value": 0.14}},
     "profile_skills": {
         "attack": [{"id": "starfall_hawk_dive_bomb", "name": "Dive Bomb", "power_type": "strike", "damage_type": "physical", "damage": 28, "cost_mp": 0, "cost_stamina": 20, "cooldown": 1, "trigger": "always",
                     "status_apply": "stunned", "armor_ignore": True, "stat_mod": {"enemy": {"grace": -4}}, "mod_duration": 2},
                    {"id": "starfall_hawk_star_talons", "name": "Star Talons", "power_type": "strike", "damage_type": "magical", "damage": 30, "cost_mp": 5, "cost_stamina": 0, "cooldown": 2, "trigger": "always",
                     "status_apply": "bleeding", "stat_mod": {"enemy": {"might": -4}}, "mod_duration": 3}],
         "defense": [{"id": "starfall_hawk_aerial_dodge", "name": "Aerial Dodge", "power_type": "buff", "cost_mp": 0, "cost_stamina": 20, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "evasive", "stat_mod": {"self": {"grace": 7}}, "mod_duration": 2}],
         "utility": [{"id": "starfall_hawk_wind_buffet", "name": "Wind Buffet", "power_type": "debuff", "damage_type": "magical", "damage": 6, "cost_mp": 5, "cost_stamina": 0, "cooldown": 2, "trigger": "opening_move",
                      "status_apply": "weary", "stat_mod": {"enemy": {"grace": -5, "cognition": -3}}, "mod_duration": 3}],
     },
     "signature_fusion": {"id": "starfall_hawk_meteor_dive", "name": "Meteor Dive", "power_type": "strike", "damage_type": "physical", "damage": 40, "cost_mp": 5, "cost_stamina": 25, "cooldown": 4, "hits": 3, "is_signature": True,
                          "status_apply": "stunned", "armor_ignore": True, "unevadable": True, "stat_mod": {"enemy": {"might": -5, "grace": -5}}, "mod_duration": 3},
     "drops": {"common": [{"id": "starfall_feather", "chance": 0.7, "qty": [1, 1]}, {"id": "sky_shard", "chance": 0.3, "qty": [1, 1]}], "rare": [], "boss": [], "gold": [35, 55], "xp_mult": 1.8}},
    {"id": "meteor_golem", "name": "Meteor Golem", "biome": "starfall_cliffs", "rarity": "uncommon", "hp": 85,
     "creature_tier": "normal", "species": "construct", "archetype": "bruiser", "personality": "aggressive",
     "tags": ["construct"],
     "stats": {"might": {"base": 32, "growth": 2.6}, "grace": {"base": 10, "growth": 0.8}, "cognition": {"base": 8, "growth": 0.7},
               "insight": {"base": 10, "growth": 0.8}, "essence": {"base": 22, "growth": 1.8}, "durability": {"base": 28, "growth": 2.2}},
     "life": {"mp": 15, "stamina": 120, "shield": 10},
     "passive_buff": {"type": "might_bonus", "value": 0.20, "secondary": {"type": "essence_bonus", "value": 0.14}},
     "profile_skills": {
         "attack": [{"id": "meteor_golem_meteor_fist", "name": "Meteor Fist", "power_type": "strike", "damage_type": "magical", "damage": 30, "cost_mp": 5, "cost_stamina": 25, "cooldown": 1, "trigger": "always",
                     "status_apply": "burning", "stat_mod": {"enemy": {"armor_bonus": -4}}, "mod_duration": 3},
                    {"id": "meteor_golem_cosmic_slam", "name": "Cosmic Slam", "power_type": "strike", "damage_type": "magical", "damage": 34, "cost_mp": 8, "cost_stamina": 30, "cooldown": 2, "trigger": "always",
                     "status_apply": "stunned", "armor_ignore": True, "stat_mod": {"enemy": {"might": -5}}, "mod_duration": 3}],
         "defense": [{"id": "meteor_golem_stone_core", "name": "Stone Core", "power_type": "buff", "cost_mp": 5, "cost_stamina": 30, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 12, "durability": 7}}, "mod_duration": 3}],
         "utility": [{"id": "meteor_golem_gravity_well", "name": "Gravity Well", "power_type": "debuff", "damage_type": "magical", "damage": 8, "cost_mp": 8, "cost_stamina": 0, "cooldown": 2, "trigger": "opening_move",
                      "status_apply": "ensnared", "stat_mod": {"enemy": {"grace": -5, "might": -4}}, "mod_duration": 3}],
     },
     "signature_fusion": {"id": "meteor_golem_apocalypse_slam", "name": "Apocalypse Slam", "power_type": "strike", "damage_type": "magical", "damage": 42, "cost_mp": 15, "cost_stamina": 0, "cooldown": 4, "hits": 2, "is_signature": True,
                          "status_apply": "burning", "armor_ignore": True, "stat_mod": {"enemy": {"might": -6, "armor_bonus": -6}}, "mod_duration": 4},
     "drops": {"common": [{"id": "sky_shard", "chance": 0.7, "qty": [1, 1]}, {"id": "meteor_fragment", "chance": 0.4, "qty": [1, 1]}], "rare": [{"id": "starsteel_ore", "chance": 0.1, "qty": [1, 1]}], "boss": [], "gold": [40, 60], "xp_mult": 1.9}},
    {"id": "starfall_sovereign", "name": "Starfall Sovereign", "biome": "starfall_cliffs", "rarity": "rare", "hp": 120,
     "creature_tier": "boss", "species": "magical", "archetype": "caster", "personality": "aggressive",
     "is_boss": True,
     "stats": {"might": {"base": 24, "growth": 2.0}, "grace": {"base": 22, "growth": 1.8}, "cognition": {"base": 30, "growth": 2.4},
               "insight": {"base": 32, "growth": 2.5}, "essence": {"base": 36, "growth": 2.8}, "durability": {"base": 24, "growth": 1.8}},
     "life": {"mp": 60, "stamina": 100, "shield": 10},
     "passive_buff": [{"type": "essence_bonus", "value": 0.28}, {"type": "might_bonus", "value": 0.18}, {"type": "grace_bonus", "value": 0.15}],
     "boss_aura": {"id": "starfall_aura", "name": "Starfall Aura", "effect": "burning", "desc": "Cosmic energy burns all enemies each turn, reducing their essence."},
     "profile_skills": {
         "attack": [{"id": "starfall_sovereign_meteor_storm", "name": "Meteor Storm", "power_type": "strike", "damage_type": "magical", "damage": 38, "cost_mp": 10, "cost_stamina": 0, "cooldown": 1, "trigger": "always",
                     "status_apply": "burning", "unevadable": True, "stat_mod": {"enemy": {"essence": -6}}, "mod_duration": 3},
                    {"id": "starfall_sovereign_cosmic_lance", "name": "Cosmic Lance", "power_type": "strike", "damage_type": "magical", "damage": 44, "cost_mp": 12, "cost_stamina": 0, "cooldown": 2, "trigger": "always",
                     "status_apply": "stunned", "armor_ignore": True, "stat_mod": {"enemy": {"might": -6, "essence": -5}}, "mod_duration": 3}],
         "defense": [{"id": "starfall_sovereign_star_barrier", "name": "Star Barrier", "power_type": "buff", "cost_mp": 12, "cost_stamina": 0, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 14, "essence": 8}}, "mod_duration": 3},
                    {"id": "starfall_sovereign_celestial_mend", "name": "Celestial Mend", "power_type": "heal", "cost_mp": 15, "cost_stamina": 0, "cooldown": 4, "trigger": "low_hp",
                      "heal_percent": 0.18, "self_status": "warded", "stat_mod": {"self": {"essence": 6}}, "mod_duration": 3}],
         "utility": [{"id": "starfall_sovereign_gravity_descent", "name": "Gravity Descent", "power_type": "debuff", "damage_type": "magical", "damage": 12, "cost_mp": 12, "cost_stamina": 0, "cooldown": 3, "trigger": "opening_move",
                      "status_apply": "ensnared", "stat_mod": {"enemy": {"might": -6, "grace": -6, "cognition": -5}}, "mod_duration": 4}],
     },
     "signature_fusion": [{"id": "starfall_sovereign_supernova", "name": "Supernova", "power_type": "strike", "damage_type": "magical", "damage": 54, "cost_mp": 25, "cost_stamina": 0, "cooldown": 5, "hits": 3, "is_signature": True,
                          "status_apply": "burning", "unevadable": True, "armor_ignore": True, "stat_mod": {"enemy": {"essence": -8, "might": -7}}, "mod_duration": 4},
                         {"id": "starfall_sovereign_starfall_judgement", "name": "Starfall Judgement", "power_type": "strike", "damage_type": "magical", "damage": 46, "cost_mp": 18, "cost_stamina": 0, "cooldown": 4, "hits": 2, "is_signature": True,
                          "status_apply": "stunned", "armor_ignore": True, "stat_mod": {"enemy": {"grace": -7, "essence": -6}}, "mod_duration": 4}],
     "drops": {"common": [{"id": "sky_shard", "chance": 0.9, "qty": [1, 2]}], "rare": [{"id": "starsteel_ore", "chance": 0.3, "qty": [1, 1]}], "boss": [{"id": "sovereign_crown", "chance": 0.15, "qty": [1, 1]}, {"id": "starfall_core", "chance": 0.1, "qty": [1, 1]}], "gold": [70, 130], "xp_mult": 2.3}},
    # ---- Blooming Desert (Gennel Lv 32) ----
    {"id": "bloom_scorpion", "name": "Blooming Scorpion", "biome": "blooming_desert", "rarity": "common", "hp": 70,
     "creature_tier": "normal", "species": "beast", "archetype": "striker", "personality": "aggressive",
     "stats": {"might": {"base": 26, "growth": 2.2}, "grace": {"base": 20, "growth": 1.6}, "cognition": {"base": 10, "growth": 0.9},
               "insight": {"base": 12, "growth": 1.0}, "essence": {"base": 16, "growth": 1.3}, "durability": {"base": 20, "growth": 1.6}},
     "life": {"mp": 10, "stamina": 110, "shield": 5},
     "passive_buff": {"type": "might_bonus", "value": 0.18, "secondary": {"type": "grace_bonus", "value": 0.12}},
     "profile_skills": {
         "attack": [{"id": "bloom_scorpion_venom_sting", "name": "Venom Sting", "power_type": "strike", "damage_type": "physical", "damage": 26, "cost_mp": 0, "cost_stamina": 20, "cooldown": 1, "trigger": "always",
                     "status_apply": "poisoned", "stat_mod": {"enemy": {"might": -4}}, "mod_duration": 3},
                    {"id": "bloom_scorpion_pincer_crush", "name": "Pincer Crush", "power_type": "strike", "damage_type": "physical", "damage": 28, "cost_mp": 0, "cost_stamina": 25, "cooldown": 2, "trigger": "always",
                     "status_apply": "stunned", "stat_mod": {"enemy": {"armor_bonus": -4}}, "mod_duration": 2}],
         "defense": [{"id": "bloom_scorpion_sand_carapace", "name": "Sand Carapace", "power_type": "buff", "cost_mp": 0, "cost_stamina": 25, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 8, "durability": 5}}, "mod_duration": 3}],
         "utility": [{"id": "bloom_scorpion_burrow", "name": "Sand Burrow", "power_type": "buff", "cost_mp": 0, "cost_stamina": 20, "cooldown": 3, "trigger": "always",
                      "self_status": "evasive", "stat_mod": {"self": {"grace": 5}}, "mod_duration": 2}],
     },
     "signature_fusion": {"id": "bloom_scorpion_desert_fury", "name": "Desert Fury", "power_type": "strike", "damage_type": "physical", "damage": 36, "cost_mp": 0, "cost_stamina": 50, "cooldown": 4, "hits": 3, "is_signature": True,
                          "status_apply": "poisoned", "lifesteal": 0.15, "stat_mod": {"enemy": {"might": -5}}, "mod_duration": 3},
     "drops": {"common": [{"id": "scorpion_chitin", "chance": 0.7, "qty": [1, 1]}, {"id": "desert_herb", "chance": 0.4, "qty": [1, 1]}], "rare": [], "boss": [], "gold": [30, 45], "xp_mult": 1.7}},
    {"id": "oasis_naga", "name": "Oasis Naga", "biome": "blooming_desert", "rarity": "uncommon", "hp": 75,
     "creature_tier": "normal", "species": "beast", "archetype": "caster", "personality": "opportunist",
     "stats": {"might": {"base": 14, "growth": 1.2}, "grace": {"base": 22, "growth": 1.8}, "cognition": {"base": 24, "growth": 2.0},
               "insight": {"base": 26, "growth": 2.0}, "essence": {"base": 28, "growth": 2.2}, "durability": {"base": 16, "growth": 1.3}},
     "life": {"mp": 40, "stamina": 70, "shield": 0},
     "passive_buff": {"type": "essence_bonus", "value": 0.22, "secondary": {"type": "grace_bonus", "value": 0.14}},
     "profile_skills": {
         "attack": [{"id": "oasis_naga_water_whip", "name": "Water Whip", "power_type": "strike", "damage_type": "magical", "damage": 26, "cost_mp": 5, "cost_stamina": 0, "cooldown": 1, "trigger": "always",
                     "status_apply": "ensnared", "stat_mod": {"enemy": {"grace": -4}}, "mod_duration": 3},
                    {"id": "oasis_naga_mirage_bolt", "name": "Mirage Bolt", "power_type": "strike", "damage_type": "magical", "damage": 28, "cost_mp": 7, "cost_stamina": 0, "cooldown": 2, "trigger": "always",
                     "status_apply": "weary", "unevadable": True, "stat_mod": {"enemy": {"cognition": -4}}, "mod_duration": 3}],
         "defense": [{"id": "oasis_naga_water_shield", "name": "Water Shield", "power_type": "buff", "cost_mp": 6, "cost_stamina": 0, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 7, "essence": 5}}, "mod_duration": 3}],
         "utility": [{"id": "oasis_naga_healing_oasis", "name": "Healing Oasis", "power_type": "heal", "cost_mp": 8, "cost_stamina": 0, "cooldown": 3, "trigger": "low_hp",
                      "heal_percent": 0.12, "self_status": "warded"}],
     },
     "signature_fusion": {"id": "oasis_naga_mirage_storm", "name": "Mirage Storm", "power_type": "strike", "damage_type": "magical", "damage": 38, "cost_mp": 15, "cost_stamina": 0, "cooldown": 4, "hits": 3, "is_signature": True,
                          "status_apply": "weary", "unevadable": True, "stat_mod": {"enemy": {"essence": -6, "cognition": -5}}, "mod_duration": 4},
     "drops": {"common": [{"id": "naga_scale", "chance": 0.6, "qty": [1, 1]}, {"id": "oasis_water", "chance": 0.4, "qty": [1, 1]}], "rare": [{"id": "mirage_crystal", "chance": 0.1, "qty": [1, 1]}], "boss": [], "gold": [35, 50], "xp_mult": 1.8}},
    {"id": "blooming_desert_chieftain", "name": "Desert Chieftain", "biome": "blooming_desert", "rarity": "rare", "hp": 110,
     "creature_tier": "mini_boss", "species": "humanoid", "archetype": "bruiser", "personality": "aggressive",
     "stats": {"might": {"base": 36, "growth": 2.8}, "grace": {"base": 18, "growth": 1.5}, "cognition": {"base": 16, "growth": 1.3},
               "insight": {"base": 14, "growth": 1.2}, "essence": {"base": 18, "growth": 1.5}, "durability": {"base": 28, "growth": 2.2}},
     "life": {"mp": 15, "stamina": 140, "shield": 5},
     "passive_buff": [{"type": "might_bonus", "value": 0.22}, {"type": "durability_bonus", "value": 0.16}],
     "profile_skills": {
         "attack": [{"id": "desert_chieftain_sand_cleave", "name": "Sand Cleave", "power_type": "strike", "damage_type": "physical", "damage": 34, "cost_mp": 0, "cost_stamina": 25, "cooldown": 1, "trigger": "always",
                     "status_apply": "bleeding", "stat_mod": {"enemy": {"armor_bonus": -4}}, "mod_duration": 2},
                    {"id": "desert_chieftain_dune_crash", "name": "Dune Crash", "power_type": "strike", "damage_type": "physical", "damage": 38, "cost_mp": 0, "cost_stamina": 35, "cooldown": 2, "trigger": "always",
                     "status_apply": "stunned", "armor_ignore": True, "stat_mod": {"enemy": {"might": -5}}, "mod_duration": 3}],
         "defense": [{"id": "desert_chieftain_sand_armor", "name": "Sand Armor", "power_type": "buff", "cost_mp": 0, "cost_stamina": 30, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 10, "durability": 6}}, "mod_duration": 3}],
         "utility": [{"id": "desert_chieftain_war_drum", "name": "War Drum", "power_type": "buff", "cost_mp": 5, "cost_stamina": 30, "cooldown": 3, "trigger": "always",
                      "self_status": "inspired", "stat_mod": {"self": {"might": 6, "grace": 4}}, "mod_duration": 3}],
     },
     "signature_fusion": {"id": "desert_chieftain_sandstorm", "name": "Sandstorm Devastation", "power_type": "strike", "damage_type": "physical", "damage": 44, "cost_mp": 0, "cost_stamina": 50, "cooldown": 4, "hits": 3, "is_signature": True,
                          "status_apply": "weary", "armor_ignore": True, "stat_mod": {"enemy": {"might": -6, "grace": -5}}, "mod_duration": 4},
     "drops": {"common": [{"id": "scorpion_chitin", "chance": 0.8, "qty": [1, 2]}], "rare": [{"id": "chieftain_boneblade", "chance": 0.15, "qty": [1, 1]}], "boss": [{"id": "chieftain_headdress", "chance": 0.2, "qty": [1, 1]}], "gold": [45, 80], "xp_mult": 2.0}},
    # ---- Beastwood (Gennel Lv 36) ----
    {"id": "beastwood_panther", "name": "Beastwood Panther", "biome": "beastwood", "rarity": "common", "hp": 70,
     "creature_tier": "normal", "species": "beast", "archetype": "striker", "personality": "aggressive",
     "stats": {"might": {"base": 28, "growth": 2.2}, "grace": {"base": 26, "growth": 2.0}, "cognition": {"base": 14, "growth": 1.2},
               "insight": {"base": 16, "growth": 1.3}, "essence": {"base": 14, "growth": 1.2}, "durability": {"base": 18, "growth": 1.4}},
     "life": {"mp": 5, "stamina": 120, "shield": 0},
     "passive_buff": {"type": "grace_bonus", "value": 0.20, "secondary": {"type": "might_bonus", "value": 0.14}},
     "profile_skills": {
         "attack": [{"id": "beastwood_panther_ravage", "name": "Ravage", "power_type": "strike", "damage_type": "physical", "damage": 28, "cost_mp": 0, "cost_stamina": 20, "cooldown": 1, "trigger": "always",
                     "status_apply": "bleeding", "stat_mod": {"enemy": {"grace": -4}}, "mod_duration": 3},
                    {"id": "beastwood_panther_pounce", "name": "Pounce", "power_type": "strike", "damage_type": "physical", "damage": 30, "cost_mp": 0, "cost_stamina": 25, "cooldown": 2, "trigger": "always",
                     "status_apply": "stunned", "unevadable": True, "stat_mod": {"enemy": {"might": -4}}, "mod_duration": 2}],
         "defense": [{"id": "beastwood_panther_shadow_step", "name": "Shadow Step", "power_type": "buff", "cost_mp": 0, "cost_stamina": 20, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "evasive", "stat_mod": {"self": {"grace": 6}}, "mod_duration": 2}],
         "utility": [{"id": "beastwood_panther_hunt_instinct", "name": "Hunt Instinct", "power_type": "buff", "cost_mp": 0, "cost_stamina": 25, "cooldown": 3, "trigger": "always",
                      "self_status": "inspired", "stat_mod": {"self": {"might": 5, "grace": 4}}, "mod_duration": 2}],
     },
     "signature_fusion": {"id": "beastwood_panther_blood_frenzy", "name": "Blood Frenzy", "power_type": "strike", "damage_type": "physical", "damage": 40, "cost_mp": 0, "cost_stamina": 50, "cooldown": 4, "hits": 4, "is_signature": True,
                          "status_apply": "bleeding", "lifesteal": 0.20, "stat_mod": {"enemy": {"grace": -5}}, "mod_duration": 3},
     "drops": {"common": [{"id": "panther_pelt", "chance": 0.7, "qty": [1, 1]}, {"id": "panther_claw", "chance": 0.4, "qty": [1, 1]}], "rare": [], "boss": [], "gold": [35, 50], "xp_mult": 1.8}},
    {"id": "beastwood_gorilla", "name": "Beastwood Gorilla", "biome": "beastwood", "rarity": "uncommon", "hp": 85,
     "creature_tier": "normal", "species": "beast", "archetype": "bruiser", "personality": "aggressive",
     "stats": {"might": {"base": 34, "growth": 2.6}, "grace": {"base": 14, "growth": 1.2}, "cognition": {"base": 12, "growth": 1.0},
               "insight": {"base": 14, "growth": 1.2}, "essence": {"base": 12, "growth": 1.0}, "durability": {"base": 24, "growth": 1.8}},
     "life": {"mp": 0, "stamina": 130, "shield": 0},
     "passive_buff": {"type": "might_bonus", "value": 0.22, "secondary": {"type": "durability_bonus", "value": 0.14}},
     "profile_skills": {
         "attack": [{"id": "beastwood_gorilla_smash", "name": "Gorilla Smash", "power_type": "strike", "damage_type": "physical", "damage": 30, "cost_mp": 0, "cost_stamina": 25, "cooldown": 1, "trigger": "always",
                     "status_apply": "stunned", "stat_mod": {"enemy": {"armor_bonus": -4}}, "mod_duration": 2},
                    {"id": "beastwood_gorilla_ground_pound", "name": "Ground Pound", "power_type": "strike", "damage_type": "physical", "damage": 34, "cost_mp": 0, "cost_stamina": 35, "cooldown": 2, "trigger": "always",
                     "status_apply": "stunned", "stat_mod": {"enemy": {"grace": -4, "might": -3}}, "mod_duration": 3}],
         "defense": [{"id": "beastwood_gorilla_thick_hide", "name": "Thick Hide", "power_type": "buff", "cost_mp": 0, "cost_stamina": 30, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 10, "durability": 6}}, "mod_duration": 3}],
         "utility": [{"id": "beastwood_gorilla_chest_beat", "name": "Chest Beat", "power_type": "buff", "cost_mp": 0, "cost_stamina": 25, "cooldown": 3, "trigger": "always",
                      "self_status": "inspired", "stat_mod": {"self": {"might": 6, "durability": 4}}, "mod_duration": 2}],
     },
     "signature_fusion": {"id": "beastwood_gorilla_rampage", "name": "Primal Rampage", "power_type": "strike", "damage_type": "physical", "damage": 42, "cost_mp": 0, "cost_stamina": 50, "cooldown": 4, "hits": 3, "is_signature": True,
                          "status_apply": "stunned", "armor_ignore": True, "stat_mod": {"enemy": {"might": -6, "armor_bonus": -5}}, "mod_duration": 3},
     "drops": {"common": [{"id": "gorilla_pelt", "chance": 0.7, "qty": [1, 1]}, {"id": "beast_bone", "chance": 0.4, "qty": [1, 1]}], "rare": [], "boss": [], "gold": [40, 55], "xp_mult": 1.9}},
    {"id": "beastwood_apex", "name": "Beastwood Apex", "biome": "beastwood", "rarity": "rare", "hp": 115,
     "creature_tier": "mini_boss", "species": "beast", "archetype": "striker", "personality": "aggressive",
     "stats": {"might": {"base": 38, "growth": 2.8}, "grace": {"base": 24, "growth": 2.0}, "cognition": {"base": 16, "growth": 1.3},
               "insight": {"base": 18, "growth": 1.5}, "essence": {"base": 16, "growth": 1.3}, "durability": {"base": 26, "growth": 2.0}},
     "life": {"mp": 10, "stamina": 140, "shield": 5},
     "passive_buff": [{"type": "might_bonus", "value": 0.24}, {"type": "grace_bonus", "value": 0.16}],
     "profile_skills": {
         "attack": [{"id": "beastwood_apex_savage_rip", "name": "Savage Rip", "power_type": "strike", "damage_type": "physical", "damage": 36, "cost_mp": 0, "cost_stamina": 25, "cooldown": 1, "trigger": "always",
                     "status_apply": "bleeding", "stat_mod": {"enemy": {"might": -5}}, "mod_duration": 3},
                    {"id": "beastwood_apex_maul", "name": "Apex Maul", "power_type": "strike", "damage_type": "physical", "damage": 40, "cost_mp": 0, "cost_stamina": 35, "cooldown": 2, "trigger": "always",
                     "status_apply": "stunned", "armor_ignore": True, "stat_mod": {"enemy": {"grace": -5}}, "mod_duration": 3}],
         "defense": [{"id": "beastwood_apex_predator_hide", "name": "Predator Hide", "power_type": "buff", "cost_mp": 0, "cost_stamina": 30, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 10, "grace": 5}}, "mod_duration": 3}],
         "utility": [{"id": "beastwood_apex_territorial_roar", "name": "Territorial Roar", "power_type": "debuff", "damage_type": "physical", "damage": 8, "cost_mp": 0, "cost_stamina": 30, "cooldown": 2, "trigger": "opening_move",
                      "status_apply": "weary", "stat_mod": {"enemy": {"might": -5, "cognition": -4}}, "mod_duration": 3}],
     },
     "signature_fusion": {"id": "beastwood_apex_apex_predator", "name": "Apex Predator Strike", "power_type": "strike", "damage_type": "physical", "damage": 48, "cost_mp": 0, "cost_stamina": 50, "cooldown": 4, "hits": 4, "is_signature": True,
                          "status_apply": "bleeding", "lifesteal": 0.25, "armor_ignore": True, "stat_mod": {"enemy": {"might": -6, "grace": -6}}, "mod_duration": 4},
     "drops": {"common": [{"id": "apex_fang", "chance": 0.7, "qty": [1, 1]}, {"id": "apex_pelt", "chance": 0.5, "qty": [1, 1]}], "rare": [{"id": "apex_claw", "chance": 0.15, "qty": [1, 1]}], "boss": [{"id": "apex_skull", "chance": 0.2, "qty": [1, 1]}], "gold": [50, 85], "xp_mult": 2.1}},
    # ---- Roaring Savanna (Gennel Lv 40) ----
    {"id": "savanna_lion", "name": "Savanna Lion", "biome": "roaring_savanna", "rarity": "common", "hp": 80,
     "creature_tier": "normal", "species": "beast", "archetype": "striker", "personality": "aggressive",
     "stats": {"might": {"base": 32, "growth": 2.4}, "grace": {"base": 24, "growth": 2.0}, "cognition": {"base": 14, "growth": 1.2},
               "insight": {"base": 16, "growth": 1.3}, "essence": {"base": 14, "growth": 1.2}, "durability": {"base": 22, "growth": 1.6}},
     "life": {"mp": 5, "stamina": 120, "shield": 0},
     "passive_buff": {"type": "might_bonus", "value": 0.20, "secondary": {"type": "grace_bonus", "value": 0.14}},
     "profile_skills": {
         "attack": [{"id": "savanna_lion_savage_bite", "name": "Savage Bite", "power_type": "strike", "damage_type": "physical", "damage": 30, "cost_mp": 0, "cost_stamina": 20, "cooldown": 1, "trigger": "always",
                     "status_apply": "bleeding", "stat_mod": {"enemy": {"might": -4}}, "mod_duration": 3},
                    {"id": "savanna_lion_mane_swipe", "name": "Mane Swipe", "power_type": "strike", "damage_type": "physical", "damage": 32, "cost_mp": 0, "cost_stamina": 25, "cooldown": 2, "trigger": "always",
                     "status_apply": "stunned", "stat_mod": {"enemy": {"grace": -4}}, "mod_duration": 2}],
         "defense": [{"id": "savanna_lion_pride_guard", "name": "Pride Guard", "power_type": "buff", "cost_mp": 0, "cost_stamina": 30, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 8, "might": 4}}, "mod_duration": 3}],
         "utility": [{"id": "savanna_lion_roar", "name": "Savanna Roar", "power_type": "debuff", "damage_type": "physical", "damage": 6, "cost_mp": 0, "cost_stamina": 25, "cooldown": 2, "trigger": "opening_move",
                      "status_apply": "weary", "stat_mod": {"enemy": {"might": -5, "cognition": -3}}, "mod_duration": 3}],
     },
     "signature_fusion": {"id": "savanna_lion_king_roar", "name": "King's Roar", "power_type": "strike", "damage_type": "physical", "damage": 42, "cost_mp": 0, "cost_stamina": 50, "cooldown": 4, "hits": 3, "is_signature": True,
                          "status_apply": "stunned", "armor_ignore": True, "lifesteal": 0.15, "stat_mod": {"enemy": {"might": -5}}, "mod_duration": 3},
     "drops": {"common": [{"id": "lion_mane", "chance": 0.7, "qty": [1, 1]}, {"id": "lion_fang", "chance": 0.4, "qty": [1, 1]}], "rare": [], "boss": [], "gold": [40, 55], "xp_mult": 1.9}},
    {"id": "savanna_rhino_beast", "name": "Savanna Behemoth", "biome": "roaring_savanna", "rarity": "uncommon", "hp": 95,
     "creature_tier": "normal", "species": "beast", "archetype": "tank", "personality": "aggressive",
     "stats": {"might": {"base": 36, "growth": 2.8}, "grace": {"base": 10, "growth": 0.8}, "cognition": {"base": 8, "growth": 0.7},
               "insight": {"base": 10, "growth": 0.8}, "essence": {"base": 14, "growth": 1.2}, "durability": {"base": 30, "growth": 2.4}},
     "life": {"mp": 0, "stamina": 140, "shield": 5},
     "passive_buff": {"type": "durability_bonus", "value": 0.22, "secondary": {"type": "might_bonus", "value": 0.16}},
     "profile_skills": {
         "attack": [{"id": "savanna_behemoth_charge", "name": "Behemoth Charge", "power_type": "strike", "damage_type": "physical", "damage": 32, "cost_mp": 0, "cost_stamina": 25, "cooldown": 1, "trigger": "always",
                     "status_apply": "stunned", "armor_ignore": True, "stat_mod": {"enemy": {"armor_bonus": -4}}, "mod_duration": 2},
                    {"id": "savanna_behemoth_stomp", "name": "Quake Stomp", "power_type": "strike", "damage_type": "physical", "damage": 36, "cost_mp": 0, "cost_stamina": 35, "cooldown": 2, "trigger": "always",
                     "status_apply": "stunned", "stat_mod": {"enemy": {"grace": -5, "might": -4}}, "mod_duration": 3}],
         "defense": [{"id": "savanna_behemoth_iron_hide", "name": "Iron Hide", "power_type": "buff", "cost_mp": 0, "cost_stamina": 30, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 12, "durability": 7}}, "mod_duration": 3}],
         "utility": [{"id": "savanna_behemoth_rage", "name": "Primal Rage", "power_type": "buff", "cost_mp": 0, "cost_stamina": 25, "cooldown": 3, "trigger": "always",
                      "self_status": "inspired", "stat_mod": {"self": {"might": 7}}, "mod_duration": 2}],
     },
     "signature_fusion": {"id": "savanna_behemoth_apocalypse_charge", "name": "Apocalypse Charge", "power_type": "strike", "damage_type": "physical", "damage": 46, "cost_mp": 0, "cost_stamina": 50, "cooldown": 4, "hits": 2, "is_signature": True,
                          "status_apply": "stunned", "armor_ignore": True, "stat_mod": {"enemy": {"might": -7, "armor_bonus": -6}}, "mod_duration": 4},
     "drops": {"common": [{"id": "behemoth_hide", "chance": 0.7, "qty": [1, 1]}, {"id": "behemoth_horn", "chance": 0.3, "qty": [1, 1]}], "rare": [], "boss": [], "gold": [45, 60], "xp_mult": 2.0}},
    {"id": "roaring_savanna_alpha", "name": "Savanna Alpha", "biome": "roaring_savanna", "rarity": "rare", "hp": 125,
     "creature_tier": "mini_boss", "species": "beast", "archetype": "bruiser", "personality": "aggressive",
     "stats": {"might": {"base": 42, "growth": 3.2}, "grace": {"base": 22, "growth": 1.8}, "cognition": {"base": 18, "growth": 1.5},
               "insight": {"base": 20, "growth": 1.6}, "essence": {"base": 18, "growth": 1.5}, "durability": {"base": 30, "growth": 2.4}},
     "life": {"mp": 15, "stamina": 150, "shield": 5},
     "passive_buff": [{"type": "might_bonus", "value": 0.26}, {"type": "grace_bonus", "value": 0.18}],
     "profile_skills": {
         "attack": [{"id": "savanna_alpha_alpha_strike", "name": "Alpha Strike", "power_type": "strike", "damage_type": "physical", "damage": 38, "cost_mp": 0, "cost_stamina": 25, "cooldown": 1, "trigger": "always",
                     "status_apply": "bleeding", "stat_mod": {"enemy": {"might": -5}}, "mod_duration": 3},
                    {"id": "savanna_alpha_savage_maul", "name": "Savage Maul", "power_type": "strike", "damage_type": "physical", "damage": 42, "cost_mp": 0, "cost_stamina": 35, "cooldown": 2, "trigger": "always",
                     "status_apply": "stunned", "armor_ignore": True, "stat_mod": {"enemy": {"grace": -5}}, "mod_duration": 3}],
         "defense": [{"id": "savanna_alpha_dominance", "name": "Alpha Dominance", "power_type": "buff", "cost_mp": 0, "cost_stamina": 30, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 12, "might": 6}}, "mod_duration": 3}],
         "utility": [{"id": "savanna_alpha_pack_hunt", "name": "Pack Hunt", "power_type": "buff", "cost_mp": 5, "cost_stamina": 30, "cooldown": 3, "trigger": "always",
                      "self_status": "inspired", "stat_mod": {"self": {"might": 7, "grace": 5}}, "mod_duration": 3}],
     },
     "signature_fusion": {"id": "savanna_alpha_apex_hunt", "name": "Apex Hunt", "power_type": "strike", "damage_type": "physical", "damage": 50, "cost_mp": 0, "cost_stamina": 50, "cooldown": 4, "hits": 4, "is_signature": True,
                          "status_apply": "bleeding", "lifesteal": 0.25, "armor_ignore": True, "stat_mod": {"enemy": {"might": -7, "grace": -6}}, "mod_duration": 4},
     "drops": {"common": [{"id": "alpha_mane", "chance": 0.8, "qty": [1, 1]}, {"id": "alpha_fang", "chance": 0.5, "qty": [1, 1]}], "rare": [{"id": "alpha_claw", "chance": 0.2, "qty": [1, 1]}], "boss": [{"id": "alpha_crown", "chance": 0.2, "qty": [1, 1]}], "gold": [55, 95], "xp_mult": 2.2}},
    # ---- Ancient Den (Gennel Lv 44) ----
    {"id": "ancient_bear", "name": "Ancient Bear", "biome": "ancient_den", "rarity": "common", "hp": 90,
     "creature_tier": "normal", "species": "beast", "archetype": "bruiser", "personality": "aggressive",
     "stats": {"might": {"base": 36, "growth": 2.8}, "grace": {"base": 16, "growth": 1.3}, "cognition": {"base": 14, "growth": 1.2},
               "insight": {"base": 16, "growth": 1.3}, "essence": {"base": 16, "growth": 1.3}, "durability": {"base": 28, "growth": 2.2}},
     "life": {"mp": 10, "stamina": 130, "shield": 0},
     "passive_buff": {"type": "might_bonus", "value": 0.22, "secondary": {"type": "durability_bonus", "value": 0.16}},
     "profile_skills": {
         "attack": [{"id": "ancient_bear_crushing_blow", "name": "Crushing Blow", "power_type": "strike", "damage_type": "physical", "damage": 32, "cost_mp": 0, "cost_stamina": 25, "cooldown": 1, "trigger": "always",
                     "status_apply": "stunned", "stat_mod": {"enemy": {"armor_bonus": -4}}, "mod_duration": 2},
                    {"id": "ancient_bear_maul", "name": "Ancient Maul", "power_type": "strike", "damage_type": "physical", "damage": 34, "cost_mp": 0, "cost_stamina": 30, "cooldown": 2, "trigger": "always",
                     "status_apply": "bleeding", "stat_mod": {"enemy": {"might": -5}}, "mod_duration": 3}],
         "defense": [{"id": "ancient_bear_thick_fur", "name": "Thick Fur", "power_type": "buff", "cost_mp": 0, "cost_stamina": 30, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 10, "durability": 6}}, "mod_duration": 3}],
         "utility": [{"id": "ancient_bear_primal_roar", "name": "Primal Roar", "power_type": "debuff", "damage_type": "physical", "damage": 8, "cost_mp": 0, "cost_stamina": 30, "cooldown": 2, "trigger": "opening_move",
                      "status_apply": "weary", "stat_mod": {"enemy": {"might": -5, "cognition": -4}}, "mod_duration": 3}],
     },
     "signature_fusion": {"id": "ancient_bear_ancient_rampage", "name": "Ancient Rampage", "power_type": "strike", "damage_type": "physical", "damage": 44, "cost_mp": 0, "cost_stamina": 50, "cooldown": 4, "hits": 3, "is_signature": True,
                          "status_apply": "stunned", "armor_ignore": True, "lifesteal": 0.20, "stat_mod": {"enemy": {"might": -6}}, "mod_duration": 4},
     "drops": {"common": [{"id": "bear_pelt", "chance": 0.7, "qty": [1, 1]}, {"id": "bear_claw", "chance": 0.4, "qty": [1, 1]}], "rare": [], "boss": [], "gold": [45, 60], "xp_mult": 2.0}},
    {"id": "totem_spirit", "name": "Totem Spirit", "biome": "ancient_den", "rarity": "uncommon", "hp": 80,
     "creature_tier": "normal", "species": "magical", "archetype": "caster", "personality": "guardian",
     "stats": {"might": {"base": 14, "growth": 1.2}, "grace": {"base": 20, "growth": 1.6}, "cognition": {"base": 28, "growth": 2.2},
               "insight": {"base": 30, "growth": 2.4}, "essence": {"base": 30, "growth": 2.4}, "durability": {"base": 16, "growth": 1.3}},
     "life": {"mp": 50, "stamina": 60, "shield": 5},
     "passive_buff": {"type": "essence_bonus", "value": 0.24, "secondary": {"type": "insight_bonus", "value": 0.16}},
     "profile_skills": {
         "attack": [{"id": "totem_spirit_ancestral_strike", "name": "Ancestral Strike", "power_type": "strike", "damage_type": "magical", "damage": 32, "cost_mp": 6, "cost_stamina": 0, "cooldown": 1, "trigger": "always",
                     "status_apply": "weary", "unevadable": True, "stat_mod": {"enemy": {"essence": -5}}, "mod_duration": 3},
                    {"id": "totem_spirit_totem_blast", "name": "Totem Blast", "power_type": "strike", "damage_type": "magical", "damage": 34, "cost_mp": 8, "cost_stamina": 0, "cooldown": 2, "trigger": "always",
                     "status_apply": "stunned", "stat_mod": {"enemy": {"cognition": -5}}, "mod_duration": 3}],
         "defense": [{"id": "totem_spirit_ancestral_ward", "name": "Ancestral Ward", "power_type": "buff", "cost_mp": 8, "cost_stamina": 0, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 10, "essence": 6}}, "mod_duration": 3}],
         "utility": [{"id": "totem_spirit_spirit_mend", "name": "Spirit Mend", "power_type": "heal", "cost_mp": 10, "cost_stamina": 0, "cooldown": 3, "trigger": "low_hp",
                      "heal_percent": 0.15, "self_status": "inspired", "stat_mod": {"self": {"essence": 4}}, "mod_duration": 2}],
     },
     "signature_fusion": {"id": "totem_spirit_ancestral_storm", "name": "Ancestral Storm", "power_type": "strike", "damage_type": "magical", "damage": 44, "cost_mp": 18, "cost_stamina": 0, "cooldown": 4, "hits": 3, "is_signature": True,
                          "status_apply": "weary", "unevadable": True, "armor_ignore": True, "stat_mod": {"enemy": {"essence": -7, "cognition": -6}}, "mod_duration": 4},
     "drops": {"common": [{"id": "totem_shard", "chance": 0.7, "qty": [1, 1]}, {"id": "ancestral_essence", "chance": 0.3, "qty": [1, 1]}], "rare": [{"id": "spirit_totem", "chance": 0.1, "qty": [1, 1]}], "boss": [], "gold": [50, 65], "xp_mult": 2.1}},
    {"id": "ancient_den_patriarch", "name": "Den Patriarch", "biome": "ancient_den", "rarity": "rare", "hp": 130,
     "creature_tier": "boss", "species": "beast", "archetype": "bruiser", "personality": "aggressive",
     "is_boss": True,
     "stats": {"might": {"base": 46, "growth": 3.4}, "grace": {"base": 20, "growth": 1.6}, "cognition": {"base": 18, "growth": 1.5},
               "insight": {"base": 20, "growth": 1.6}, "essence": {"base": 22, "growth": 1.8}, "durability": {"base": 36, "growth": 2.8}},
     "life": {"mp": 20, "stamina": 160, "shield": 10},
     "passive_buff": [{"type": "might_bonus", "value": 0.28}, {"type": "durability_bonus", "value": 0.22}, {"type": "grace_bonus", "value": 0.14}],
     "boss_aura": {"id": "primal_aura", "name": "Primal Aura", "effect": "weary", "desc": "All enemies feel the weight of ancient power, reducing their might and cognition."},
     "profile_skills": {
         "attack": [{"id": "den_patriarch_ancient_maul", "name": "Ancient Maul", "power_type": "strike", "damage_type": "physical", "damage": 42, "cost_mp": 0, "cost_stamina": 25, "cooldown": 1, "trigger": "always",
                     "status_apply": "bleeding", "stat_mod": {"enemy": {"might": -6}}, "mod_duration": 3},
                    {"id": "den_patriarch_apex_crush", "name": "Apex Crush", "power_type": "strike", "damage_type": "physical", "damage": 48, "cost_mp": 0, "cost_stamina": 35, "cooldown": 2, "trigger": "always",
                     "status_apply": "stunned", "armor_ignore": True, "stat_mod": {"enemy": {"might": -7, "armor_bonus": -6}}, "mod_duration": 3}],
         "defense": [{"id": "den_patriarch_iron_fur", "name": "Iron Fur", "power_type": "buff", "cost_mp": 0, "cost_stamina": 30, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 14, "durability": 8}}, "mod_duration": 3},
                    {"id": "den_patriarch_primal_mend", "name": "Primal Mend", "power_type": "heal", "cost_mp": 10, "cost_stamina": 0, "cooldown": 4, "trigger": "low_hp",
                      "heal_percent": 0.18, "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 6, "might": 5}}, "mod_duration": 3}],
         "utility": [{"id": "den_patriarch_ancient_roar", "name": "Ancient Roar", "power_type": "debuff", "damage_type": "physical", "damage": 12, "cost_mp": 0, "cost_stamina": 30, "cooldown": 3, "trigger": "opening_move",
                      "status_apply": "weary", "stat_mod": {"enemy": {"might": -7, "cognition": -6, "grace": -5}}, "mod_duration": 4}],
     },
     "signature_fusion": [{"id": "den_patriarch_primal_devastation", "name": "Primal Devastation", "power_type": "strike", "damage_type": "physical", "damage": 56, "cost_mp": 0, "cost_stamina": 50, "cooldown": 5, "hits": 3, "is_signature": True,
                          "status_apply": "stunned", "armor_ignore": True, "lifesteal": 0.25, "stat_mod": {"enemy": {"might": -8, "armor_bonus": -8}}, "mod_duration": 4},
                         {"id": "den_patriarch_ancient_fury", "name": "Ancient Fury", "power_type": "strike", "damage_type": "physical", "damage": 48, "cost_mp": 0, "cost_stamina": 40, "cooldown": 4, "hits": 2, "is_signature": True,
                          "status_apply": "bleeding", "armor_ignore": True, "stat_mod": {"enemy": {"might": -7, "grace": -6}}, "mod_duration": 4}],
     "drops": {"common": [{"id": "patriarch_pelt", "chance": 0.9, "qty": [1, 2]}], "rare": [{"id": "patriarch_claw", "chance": 0.3, "qty": [1, 1]}], "boss": [{"id": "patriarch_crown", "chance": 0.15, "qty": [1, 1]}, {"id": "ancient_totem", "chance": 0.1, "qty": [1, 1]}], "gold": [80, 140], "xp_mult": 2.5}},
    # ---- Coral Gardens (Hylion Lv 34) ----
    {"id": "coral_drake", "name": "Coral Drake", "biome": "coral_gardens", "rarity": "common", "hp": 70,
     "creature_tier": "normal", "species": "beast", "archetype": "striker", "personality": "aggressive",
     "stats": {"might": {"base": 28, "growth": 2.2}, "grace": {"base": 22, "growth": 1.8}, "cognition": {"base": 14, "growth": 1.2},
               "insight": {"base": 16, "growth": 1.3}, "essence": {"base": 18, "growth": 1.5}, "durability": {"base": 20, "growth": 1.6}},
     "life": {"mp": 15, "stamina": 100, "shield": 5},
     "passive_buff": {"type": "might_bonus", "value": 0.18, "secondary": {"type": "essence_bonus", "value": 0.12}},
     "profile_skills": {
         "attack": [{"id": "coral_drake_reef_bite", "name": "Reef Bite", "power_type": "strike", "damage_type": "physical", "damage": 28, "cost_mp": 0, "cost_stamina": 20, "cooldown": 1, "trigger": "always",
                     "status_apply": "bleeding", "stat_mod": {"enemy": {"grace": -4}}, "mod_duration": 3},
                    {"id": "coral_drake_coral_shard", "name": "Coral Shard Spit", "power_type": "strike", "damage_type": "magical", "damage": 30, "cost_mp": 5, "cost_stamina": 0, "cooldown": 2, "trigger": "always",
                     "status_apply": "poisoned", "stat_mod": {"enemy": {"might": -4}}, "mod_duration": 3}],
         "defense": [{"id": "coral_drake_coral_armor", "name": "Coral Armor", "power_type": "buff", "cost_mp": 5, "cost_stamina": 0, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 8, "durability": 5}}, "mod_duration": 3}],
         "utility": [{"id": "coral_drake_ink_cloud", "name": "Ink Cloud", "power_type": "debuff", "damage_type": "magical", "damage": 4, "cost_mp": 5, "cost_stamina": 0, "cooldown": 2, "trigger": "opening_move",
                      "status_apply": "weary", "stat_mod": {"enemy": {"cognition": -4, "grace": -3}}, "mod_duration": 3}],
     },
     "signature_fusion": {"id": "coral_drake_reef_devastator", "name": "Reef Devastator", "power_type": "strike", "damage_type": "physical", "damage": 40, "cost_mp": 10, "cost_stamina": 25, "cooldown": 4, "hits": 3, "is_signature": True,
                          "status_apply": "bleeding", "lifesteal": 0.15, "stat_mod": {"enemy": {"grace": -5}}, "mod_duration": 3},
     "drops": {"common": [{"id": "coral_fragment", "chance": 0.7, "qty": [1, 1]}, {"id": "reef_scale", "chance": 0.4, "qty": [1, 1]}], "rare": [], "boss": [], "gold": [35, 50], "xp_mult": 1.8}},
    {"id": "anemone_elemental", "name": "Anemone Elemental", "biome": "coral_gardens", "rarity": "uncommon", "hp": 75,
     "creature_tier": "normal", "species": "magical", "archetype": "caster", "personality": "opportunist",
     "stats": {"might": {"base": 10, "growth": 0.8}, "grace": {"base": 20, "growth": 1.6}, "cognition": {"base": 24, "growth": 2.0},
               "insight": {"base": 26, "growth": 2.0}, "essence": {"base": 28, "growth": 2.2}, "durability": {"base": 16, "growth": 1.3}},
     "life": {"mp": 45, "stamina": 60, "shield": 0},
     "passive_buff": {"type": "essence_bonus", "value": 0.22, "secondary": {"type": "insight_bonus", "value": 0.14}},
     "profile_skills": {
         "attack": [{"id": "anemone_elemental_tentacle_lash", "name": "Tentacle Lash", "power_type": "strike", "damage_type": "magical", "damage": 28, "cost_mp": 5, "cost_stamina": 0, "cooldown": 1, "trigger": "always",
                     "status_apply": "poisoned", "stat_mod": {"enemy": {"essence": -4}}, "mod_duration": 3},
                    {"id": "anemone_elemental_reef_pulse", "name": "Reef Pulse", "power_type": "strike", "damage_type": "magical", "damage": 30, "cost_mp": 7, "cost_stamina": 0, "cooldown": 2, "trigger": "always",
                     "status_apply": "ensnared", "unevadable": True, "stat_mod": {"enemy": {"grace": -4}}, "mod_duration": 3}],
         "defense": [{"id": "anemone_elemental_coral_ward", "name": "Coral Ward", "power_type": "buff", "cost_mp": 6, "cost_stamina": 0, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 8, "essence": 5}}, "mod_duration": 3}],
         "utility": [{"id": "anemone_elemental_healing_tide", "name": "Healing Tide", "power_type": "heal", "cost_mp": 8, "cost_stamina": 0, "cooldown": 3, "trigger": "low_hp",
                      "heal_percent": 0.12, "self_status": "warded"}],
     },
     "signature_fusion": {"id": "anemone_elemental_coral_nova", "name": "Coral Nova", "power_type": "strike", "damage_type": "magical", "damage": 40, "cost_mp": 15, "cost_stamina": 0, "cooldown": 4, "hits": 3, "is_signature": True,
                          "status_apply": "poisoned", "unevadable": True, "stat_mod": {"enemy": {"essence": -6, "grace": -5}}, "mod_duration": 4},
     "drops": {"common": [{"id": "coral_fragment", "chance": 0.6, "qty": [1, 1]}, {"id": "anemone_tentacle", "chance": 0.4, "qty": [1, 1]}], "rare": [{"id": "reef_essence", "chance": 0.1, "qty": [1, 1]}], "boss": [], "gold": [40, 55], "xp_mult": 1.9}},
    {"id": "coral_gardens_queen", "name": "Coral Queen", "biome": "coral_gardens", "rarity": "rare", "hp": 110,
     "creature_tier": "mini_boss", "species": "magical", "archetype": "caster", "personality": "guardian",
     "stats": {"might": {"base": 14, "growth": 1.2}, "grace": {"base": 22, "growth": 1.8}, "cognition": {"base": 30, "growth": 2.4},
               "insight": {"base": 32, "growth": 2.5}, "essence": {"base": 34, "growth": 2.6}, "durability": {"base": 20, "growth": 1.6}},
     "life": {"mp": 70, "stamina": 60, "shield": 5},
     "passive_buff": [{"type": "essence_bonus", "value": 0.24}, {"type": "cognition_bonus", "value": 0.18}],
     "profile_skills": {
         "attack": [{"id": "coral_queen_coral_lance", "name": "Coral Lance", "power_type": "strike", "damage_type": "magical", "damage": 36, "cost_mp": 8, "cost_stamina": 0, "cooldown": 1, "trigger": "always",
                     "status_apply": "poisoned", "unevadable": True, "stat_mod": {"enemy": {"essence": -5}}, "mod_duration": 3},
                    {"id": "coral_queen_reef_blast", "name": "Reef Blast", "power_type": "strike", "damage_type": "magical", "damage": 40, "cost_mp": 10, "cost_stamina": 0, "cooldown": 2, "trigger": "always",
                     "status_apply": "ensnared", "unevadable": True, "stat_mod": {"enemy": {"grace": -5}}, "mod_duration": 3}],
         "defense": [{"id": "coral_queen_coral_bastion", "name": "Coral Bastion", "power_type": "buff", "cost_mp": 10, "cost_stamina": 0, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 12, "essence": 7}}, "mod_duration": 3}],
         "utility": [{"id": "coral_queen_tidal_mend", "name": "Tidal Mend", "power_type": "heal", "cost_mp": 12, "cost_stamina": 0, "cooldown": 3, "trigger": "low_hp",
                      "heal_percent": 0.15, "self_status": "warded", "stat_mod": {"self": {"essence": 5}}, "mod_duration": 2}],
     },
     "signature_fusion": {"id": "coral_queen_ocean_apocalypse", "name": "Ocean Apocalypse", "power_type": "strike", "damage_type": "magical", "damage": 48, "cost_mp": 20, "cost_stamina": 0, "cooldown": 4, "hits": 3, "is_signature": True,
                          "status_apply": "poisoned", "unevadable": True, "armor_ignore": True, "stat_mod": {"enemy": {"essence": -7, "grace": -6}}, "mod_duration": 4},
     "drops": {"common": [{"id": "reef_essence", "chance": 0.8, "qty": [1, 2]}], "rare": [{"id": "coral_pearl", "chance": 0.2, "qty": [1, 1]}], "boss": [{"id": "queen_coral_tiara", "chance": 0.2, "qty": [1, 1]}], "gold": [50, 85], "xp_mult": 2.1}},
    # ---- Kelp Forest (Hylion Lv 38) ----
    {"id": "kelp_strangler", "name": "Kelp Strangler", "biome": "kelp_forest", "rarity": "common", "hp": 75,
     "creature_tier": "normal", "species": "monster", "archetype": "striker", "personality": "aggressive",
     "stats": {"might": {"base": 28, "growth": 2.2}, "grace": {"base": 24, "growth": 2.0}, "cognition": {"base": 12, "growth": 1.0},
               "insight": {"base": 14, "growth": 1.2}, "essence": {"base": 16, "growth": 1.3}, "durability": {"base": 18, "growth": 1.4}},
     "life": {"mp": 10, "stamina": 110, "shield": 0},
     "passive_buff": {"type": "grace_bonus", "value": 0.20, "secondary": {"type": "might_bonus", "value": 0.14}},
     "profile_skills": {
         "attack": [{"id": "kelp_strangler_constrict", "name": "Constrict", "power_type": "strike", "damage_type": "physical", "damage": 30, "cost_mp": 0, "cost_stamina": 20, "cooldown": 1, "trigger": "always",
                     "status_apply": "ensnared", "stat_mod": {"enemy": {"grace": -4}}, "mod_duration": 3},
                    {"id": "kelp_strangler_choke", "name": "Kelp Choke", "power_type": "strike", "damage_type": "physical", "damage": 32, "cost_mp": 0, "cost_stamina": 25, "cooldown": 2, "trigger": "always",
                     "status_apply": "weary", "stat_mod": {"enemy": {"might": -4}}, "mod_duration": 3}],
         "defense": [{"id": "kelp_strangler_camouflage", "name": "Kelp Camouflage", "power_type": "buff", "cost_mp": 0, "cost_stamina": 20, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "evasive", "stat_mod": {"self": {"grace": 6}}, "mod_duration": 2}],
         "utility": [{"id": "kelp_strangler_drag_down", "name": "Drag Down", "power_type": "debuff", "damage_type": "physical", "damage": 6, "cost_mp": 0, "cost_stamina": 25, "cooldown": 2, "trigger": "opening_move",
                      "status_apply": "ensnared", "stat_mod": {"enemy": {"grace": -5, "might": -3}}, "mod_duration": 3}],
     },
     "signature_fusion": {"id": "kelp_strangler_ocean_grasp", "name": "Ocean Grasp", "power_type": "strike", "damage_type": "physical", "damage": 42, "cost_mp": 0, "cost_stamina": 50, "cooldown": 4, "hits": 3, "is_signature": True,
                          "status_apply": "ensnared", "lifesteal": 0.20, "stat_mod": {"enemy": {"grace": -6}}, "mod_duration": 4},
     "drops": {"common": [{"id": "kelp_strand", "chance": 0.7, "qty": [1, 1]}, {"id": "sea_vine", "chance": 0.4, "qty": [1, 1]}], "rare": [], "boss": [], "gold": [40, 55], "xp_mult": 1.9}},
    {"id": "kelp_forest_shaman", "name": "Kelp Shaman", "biome": "kelp_forest", "rarity": "uncommon", "hp": 70,
     "creature_tier": "normal", "species": "humanoid", "archetype": "caster", "personality": "guardian",
     "stats": {"might": {"base": 12, "growth": 1.0}, "grace": {"base": 20, "growth": 1.6}, "cognition": {"base": 28, "growth": 2.2},
               "insight": {"base": 30, "growth": 2.4}, "essence": {"base": 30, "growth": 2.4}, "durability": {"base": 14, "growth": 1.2}},
     "life": {"mp": 55, "stamina": 50, "shield": 0},
     "passive_buff": {"type": "essence_bonus", "value": 0.24, "secondary": {"type": "cognition_bonus", "value": 0.14}},
     "profile_skills": {
         "attack": [{"id": "kelp_shaman_water_blast", "name": "Water Blast", "power_type": "strike", "damage_type": "magical", "damage": 30, "cost_mp": 6, "cost_stamina": 0, "cooldown": 1, "trigger": "always",
                     "status_apply": "ensnared", "stat_mod": {"enemy": {"essence": -4}}, "mod_duration": 3},
                    {"id": "kelp_shaman_kelp_bolt", "name": "Kelp Bolt", "power_type": "strike", "damage_type": "magical", "damage": 32, "cost_mp": 8, "cost_stamina": 0, "cooldown": 2, "trigger": "always",
                     "status_apply": "poisoned", "unevadable": True, "stat_mod": {"enemy": {"grace": -4}}, "mod_duration": 3}],
         "defense": [{"id": "kelp_shaman_kelp_ward", "name": "Kelp Ward", "power_type": "buff", "cost_mp": 8, "cost_stamina": 0, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 8, "essence": 6}}, "mod_duration": 3}],
         "utility": [{"id": "kelp_shaman_tidal_heal", "name": "Tidal Heal", "power_type": "heal", "cost_mp": 10, "cost_stamina": 0, "cooldown": 3, "trigger": "low_hp",
                      "heal_percent": 0.15, "self_status": "warded", "stat_mod": {"self": {"essence": 4}}, "mod_duration": 2}],
     },
     "signature_fusion": {"id": "kelp_shaman_ocean_wrath", "name": "Ocean Wrath", "power_type": "strike", "damage_type": "magical", "damage": 44, "cost_mp": 18, "cost_stamina": 0, "cooldown": 4, "hits": 3, "is_signature": True,
                          "status_apply": "ensnared", "unevadable": True, "stat_mod": {"enemy": {"essence": -7, "grace": -6}}, "mod_duration": 4},
     "drops": {"common": [{"id": "kelp_strand", "chance": 0.6, "qty": [1, 1]}, {"id": "shaman_relic", "chance": 0.3, "qty": [1, 1]}], "rare": [{"id": "ocean_essence", "chance": 0.1, "qty": [1, 1]}], "boss": [], "gold": [45, 60], "xp_mult": 2.0}},
    {"id": "kelp_forest_warden", "name": "Kelp Warden", "biome": "kelp_forest", "rarity": "rare", "hp": 115,
     "creature_tier": "mini_boss", "species": "monster", "archetype": "bruiser", "personality": "guardian",
     "stats": {"might": {"base": 34, "growth": 2.6}, "grace": {"base": 22, "growth": 1.8}, "cognition": {"base": 24, "growth": 2.0},
               "insight": {"base": 26, "growth": 2.0}, "essence": {"base": 28, "growth": 2.2}, "durability": {"base": 28, "growth": 2.2}},
     "life": {"mp": 40, "stamina": 100, "shield": 10},
     "passive_buff": [{"type": "might_bonus", "value": 0.22}, {"type": "essence_bonus", "value": 0.18}],
     "profile_skills": {
         "attack": [{"id": "kelp_warden_kelp_smash", "name": "Kelp Smash", "power_type": "strike", "damage_type": "physical", "damage": 36, "cost_mp": 5, "cost_stamina": 25, "cooldown": 1, "trigger": "always",
                     "status_apply": "ensnared", "stat_mod": {"enemy": {"armor_bonus": -4}}, "mod_duration": 3},
                    {"id": "kelp_warden_ocean_crush", "name": "Ocean Crush", "power_type": "strike", "damage_type": "magical", "damage": 40, "cost_mp": 8, "cost_stamina": 0, "cooldown": 2, "trigger": "always",
                     "status_apply": "ensnared", "unevadable": True, "armor_ignore": True, "stat_mod": {"enemy": {"might": -5}}, "mod_duration": 3}],
         "defense": [{"id": "kelp_warden_ocean_bulwark", "name": "Ocean Bulwark", "power_type": "buff", "cost_mp": 8, "cost_stamina": 0, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 12, "essence": 7}}, "mod_duration": 3}],
         "utility": [{"id": "kelp_warden_drown", "name": "Drowning Depths", "power_type": "debuff", "damage_type": "magical", "damage": 10, "cost_mp": 10, "cost_stamina": 0, "cooldown": 3, "trigger": "opening_move",
                      "status_apply": "ensnared", "stat_mod": {"enemy": {"might": -6, "grace": -5, "cognition": -4}}, "mod_duration": 4}],
     },
     "signature_fusion": {"id": "kelp_warden_ocean_dominator", "name": "Ocean Dominator", "power_type": "strike", "damage_type": "magical", "damage": 50, "cost_mp": 20, "cost_stamina": 0, "cooldown": 4, "hits": 3, "is_signature": True,
                          "status_apply": "ensnared", "unevadable": True, "armor_ignore": True, "stat_mod": {"enemy": {"might": -7, "essence": -6}}, "mod_duration": 4},
     "drops": {"common": [{"id": "ocean_essence", "chance": 0.8, "qty": [1, 2]}], "rare": [{"id": "kelp_heart", "chance": 0.2, "qty": [1, 1]}], "boss": [{"id": "warden_trident", "chance": 0.2, "qty": [1, 1]}], "gold": [55, 90], "xp_mult": 2.2}},
    # ---- Storm Reefs (Hylion Lv 42) ----
    {"id": "storm_ray", "name": "Storm Ray", "biome": "storm_reefs", "rarity": "common", "hp": 75,
     "creature_tier": "normal", "species": "beast", "archetype": "caster", "personality": "aggressive",
     "stats": {"might": {"base": 16, "growth": 1.3}, "grace": {"base": 22, "growth": 1.8}, "cognition": {"base": 24, "growth": 2.0},
               "insight": {"base": 26, "growth": 2.0}, "essence": {"base": 30, "growth": 2.4}, "durability": {"base": 16, "growth": 1.3}},
     "life": {"mp": 40, "stamina": 70, "shield": 0},
     "passive_buff": {"type": "essence_bonus", "value": 0.22, "secondary": {"type": "grace_bonus", "value": 0.14}},
     "profile_skills": {
         "attack": [{"id": "storm_ray_thunder_bolt", "name": "Thunder Bolt", "power_type": "strike", "damage_type": "magical", "damage": 32, "cost_mp": 6, "cost_stamina": 0, "cooldown": 1, "trigger": "always",
                     "status_apply": "stunned", "stat_mod": {"enemy": {"essence": -4}}, "mod_duration": 2},
                    {"id": "storm_ray_storm_blast", "name": "Storm Blast", "power_type": "strike", "damage_type": "magical", "damage": 34, "cost_mp": 8, "cost_stamina": 0, "cooldown": 2, "trigger": "always",
                     "status_apply": "stunned", "unevadable": True, "stat_mod": {"enemy": {"grace": -4}}, "mod_duration": 3}],
         "defense": [{"id": "storm_ray_static_field", "name": "Static Field", "power_type": "buff", "cost_mp": 8, "cost_stamina": 0, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 6, "essence": 5}}, "mod_duration": 3}],
         "utility": [{"id": "storm_ray_charge_surge", "name": "Charge Surge", "power_type": "buff", "cost_mp": 5, "cost_stamina": 0, "cooldown": 3, "trigger": "always",
                      "self_status": "inspired", "stat_mod": {"self": {"essence": 6}}, "mod_duration": 2}],
     },
     "signature_fusion": {"id": "storm_ray_lightning_storm", "name": "Lightning Storm", "power_type": "strike", "damage_type": "magical", "damage": 44, "cost_mp": 15, "cost_stamina": 0, "cooldown": 4, "hits": 3, "is_signature": True,
                          "status_apply": "stunned", "unevadable": True, "armor_ignore": True, "stat_mod": {"enemy": {"essence": -6}}, "mod_duration": 4},
     "drops": {"common": [{"id": "storm_scale", "chance": 0.7, "qty": [1, 1]}, {"id": "lightning_shard", "chance": 0.3, "qty": [1, 1]}], "rare": [], "boss": [], "gold": [45, 60], "xp_mult": 2.0}},
    {"id": "reef_golem", "name": "Reef Golem", "biome": "storm_reefs", "rarity": "uncommon", "hp": 90,
     "creature_tier": "normal", "species": "construct", "archetype": "tank", "personality": "guardian",
     "tags": ["construct"],
     "stats": {"might": {"base": 34, "growth": 2.6}, "grace": {"base": 10, "growth": 0.8}, "cognition": {"base": 8, "growth": 0.7},
               "insight": {"base": 10, "growth": 0.8}, "essence": {"base": 20, "growth": 1.6}, "durability": {"base": 30, "growth": 2.4}},
     "life": {"mp": 15, "stamina": 120, "shield": 10},
     "passive_buff": {"type": "durability_bonus", "value": 0.22, "secondary": {"type": "essence_bonus", "value": 0.14}},
     "profile_skills": {
         "attack": [{"id": "reef_golem_storm_fist", "name": "Storm Fist", "power_type": "strike", "damage_type": "magical", "damage": 32, "cost_mp": 5, "cost_stamina": 25, "cooldown": 1, "trigger": "always",
                     "status_apply": "stunned", "stat_mod": {"enemy": {"armor_bonus": -4}}, "mod_duration": 2},
                    {"id": "reef_golem_thunder_slam", "name": "Thunder Slam", "power_type": "strike", "damage_type": "magical", "damage": 36, "cost_mp": 8, "cost_stamina": 30, "cooldown": 2, "trigger": "always",
                     "status_apply": "stunned", "armor_ignore": True, "stat_mod": {"enemy": {"might": -5}}, "mod_duration": 3}],
         "defense": [{"id": "reef_golem_coral_plating", "name": "Coral Plating", "power_type": "buff", "cost_mp": 5, "cost_stamina": 30, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 12, "durability": 7}}, "mod_duration": 3}],
         "utility": [{"id": "reef_golem_ground_surge", "name": "Ground Surge", "power_type": "debuff", "damage_type": "magical", "damage": 8, "cost_mp": 8, "cost_stamina": 0, "cooldown": 2, "trigger": "opening_move",
                      "status_apply": "stunned", "stat_mod": {"enemy": {"grace": -5, "cognition": -3}}, "mod_duration": 3}],
     },
     "signature_fusion": {"id": "reef_golem_storm_breaker", "name": "Storm Breaker", "power_type": "strike", "damage_type": "magical", "damage": 46, "cost_mp": 15, "cost_stamina": 0, "cooldown": 4, "hits": 2, "is_signature": True,
                          "status_apply": "stunned", "armor_ignore": True, "stat_mod": {"enemy": {"might": -6, "armor_bonus": -6}}, "mod_duration": 4},
     "drops": {"common": [{"id": "reef_stone", "chance": 0.7, "qty": [1, 1]}, {"id": "lightning_shard", "chance": 0.4, "qty": [1, 1]}], "rare": [{"id": "storm_crystal", "chance": 0.1, "qty": [1, 1]}], "boss": [], "gold": [50, 65], "xp_mult": 2.1}},
    {"id": "storm_reefs_titan", "name": "Storm Titan", "biome": "storm_reefs", "rarity": "rare", "hp": 125,
     "creature_tier": "boss", "species": "construct", "archetype": "bruiser", "personality": "aggressive",
     "is_boss": True,
     "tags": ["construct"],
     "stats": {"might": {"base": 38, "growth": 2.8}, "grace": {"base": 14, "growth": 1.2}, "cognition": {"base": 12, "growth": 1.0},
               "insight": {"base": 14, "growth": 1.2}, "essence": {"base": 30, "growth": 2.4}, "durability": {"base": 32, "growth": 2.5}},
     "life": {"mp": 40, "stamina": 130, "shield": 15},
     "passive_buff": [{"type": "might_bonus", "value": 0.24}, {"type": "essence_bonus", "value": 0.22}, {"type": "durability_bonus", "value": 0.18}],
     "boss_aura": {"id": "storm_aura", "name": "Storm Aura", "effect": "stunned", "desc": "Crackling electricity stuns and damages all enemies each turn."},
     "profile_skills": {
         "attack": [{"id": "storm_titan_thunder_hammer", "name": "Thunder Hammer", "power_type": "strike", "damage_type": "magical", "damage": 42, "cost_mp": 8, "cost_stamina": 25, "cooldown": 1, "trigger": "always",
                     "status_apply": "stunned", "stat_mod": {"enemy": {"armor_bonus": -5}}, "mod_duration": 3},
                    {"id": "storm_titan_lightning_cascade", "name": "Lightning Cascade", "power_type": "strike", "damage_type": "magical", "damage": 48, "cost_mp": 12, "cost_stamina": 0, "cooldown": 2, "trigger": "always",
                     "status_apply": "stunned", "unevadable": True, "armor_ignore": True, "stat_mod": {"enemy": {"essence": -6}}, "mod_duration": 3}],
         "defense": [{"id": "storm_titan_storm_barrier", "name": "Storm Barrier", "power_type": "buff", "cost_mp": 12, "cost_stamina": 0, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 14, "essence": 8}}, "mod_duration": 3},
                    {"id": "storm_titan_jolt_repair", "name": "Jolt Repair", "power_type": "heal", "cost_mp": 15, "cost_stamina": 0, "cooldown": 4, "trigger": "low_hp",
                      "heal_percent": 0.18, "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 6}}, "mod_duration": 3}],
         "utility": [{"id": "storm_titan_tempest_roar", "name": "Tempest Roar", "power_type": "debuff", "damage_type": "magical", "damage": 12, "cost_mp": 12, "cost_stamina": 0, "cooldown": 3, "trigger": "opening_move",
                      "status_apply": "stunned", "stat_mod": {"enemy": {"might": -6, "grace": -6, "cognition": -5}}, "mod_duration": 4}],
     },
     "signature_fusion": [{"id": "storm_titan_apocalypse_storm", "name": "Apocalypse Storm", "power_type": "strike", "damage_type": "magical", "damage": 56, "cost_mp": 25, "cost_stamina": 0, "cooldown": 5, "hits": 3, "is_signature": True,
                          "status_apply": "stunned", "unevadable": True, "armor_ignore": True, "stat_mod": {"enemy": {"essence": -8, "might": -7}}, "mod_duration": 4},
                         {"id": "storm_titan_thunder_judgement", "name": "Thunder Judgement", "power_type": "strike", "damage_type": "magical", "damage": 48, "cost_mp": 18, "cost_stamina": 0, "cooldown": 4, "hits": 2, "is_signature": True,
                          "status_apply": "stunned", "armor_ignore": True, "stat_mod": {"enemy": {"grace": -7, "essence": -6}}, "mod_duration": 4}],
     "drops": {"common": [{"id": "storm_crystal", "chance": 0.9, "qty": [1, 2]}], "rare": [{"id": "lightning_core", "chance": 0.3, "qty": [1, 1]}], "boss": [{"id": "titan_hammer", "chance": 0.15, "qty": [1, 1]}, {"id": "storm_core", "chance": 0.1, "qty": [1, 1]}], "gold": [75, 135], "xp_mult": 2.4}},
    # ---- Abyssal Trench (Hylion Lv 46) ----
    {"id": "abyssal_horror", "name": "Abyssal Horror", "biome": "abyssal_trench", "rarity": "common", "hp": 85,
     "creature_tier": "normal", "species": "monster", "archetype": "striker", "personality": "aggressive",
     "stats": {"might": {"base": 32, "growth": 2.4}, "grace": {"base": 24, "growth": 2.0}, "cognition": {"base": 16, "growth": 1.3},
               "insight": {"base": 18, "growth": 1.5}, "essence": {"base": 22, "growth": 1.8}, "durability": {"base": 22, "growth": 1.6}},
     "life": {"mp": 20, "stamina": 100, "shield": 5},
     "passive_buff": {"type": "might_bonus", "value": 0.20, "secondary": {"type": "essence_bonus", "value": 0.16}},
     "profile_skills": {
         "attack": [{"id": "abyssal_horror_void_bite", "name": "Void Bite", "power_type": "strike", "damage_type": "magical", "damage": 34, "cost_mp": 5, "cost_stamina": 20, "cooldown": 1, "trigger": "always",
                     "status_apply": "weary", "stat_mod": {"enemy": {"essence": -5}}, "mod_duration": 3},
                    {"id": "abyssal_horror_tentacle_drain", "name": "Tentacle Drain", "power_type": "strike", "damage_type": "magical", "damage": 36, "cost_mp": 8, "cost_stamina": 0, "cooldown": 2, "trigger": "always",
                     "status_apply": "weary", "lifesteal": 0.15, "stat_mod": {"enemy": {"might": -5}}, "mod_duration": 3}],
         "defense": [{"id": "abyssal_horror_void_shift", "name": "Void Shift", "power_type": "buff", "cost_mp": 8, "cost_stamina": 0, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "evasive", "stat_mod": {"self": {"grace": 6, "essence": 4}}, "mod_duration": 2}],
         "utility": [{"id": "abyssal_horror_terror_gaze", "name": "Terror Gaze", "power_type": "debuff", "damage_type": "magical", "damage": 6, "cost_mp": 8, "cost_stamina": 0, "cooldown": 2, "trigger": "opening_move",
                      "status_apply": "weary", "stat_mod": {"enemy": {"cognition": -6, "insight": -5}}, "mod_duration": 3}],
     },
     "signature_fusion": {"id": "abyssal_horror_void_devour", "name": "Void Devour", "power_type": "strike", "damage_type": "magical", "damage": 46, "cost_mp": 15, "cost_stamina": 0, "cooldown": 4, "hits": 3, "is_signature": True,
                          "status_apply": "weary", "lifesteal": 0.25, "unevadable": True, "stat_mod": {"enemy": {"essence": -7}}, "mod_duration": 4},
     "drops": {"common": [{"id": "abyssal_flesh", "chance": 0.7, "qty": [1, 1]}, {"id": "void_essence", "chance": 0.3, "qty": [1, 1]}], "rare": [], "boss": [], "gold": [50, 65], "xp_mult": 2.1}},
    {"id": "deep_leviathan_spawn", "name": "Leviathan Spawn", "biome": "abyssal_trench", "rarity": "uncommon", "hp": 95,
     "creature_tier": "normal", "species": "beast", "archetype": "bruiser", "personality": "aggressive",
     "stats": {"might": {"base": 36, "growth": 2.8}, "grace": {"base": 18, "growth": 1.5}, "cognition": {"base": 14, "growth": 1.2},
               "insight": {"base": 16, "growth": 1.3}, "essence": {"base": 24, "growth": 2.0}, "durability": {"base": 26, "growth": 2.0}},
     "life": {"mp": 25, "stamina": 110, "shield": 5},
     "passive_buff": {"type": "might_bonus", "value": 0.22, "secondary": {"type": "essence_bonus", "value": 0.16}},
     "profile_skills": {
         "attack": [{"id": "leviathan_spawn_abyssal_slam", "name": "Abyssal Slam", "power_type": "strike", "damage_type": "magical", "damage": 34, "cost_mp": 5, "cost_stamina": 25, "cooldown": 1, "trigger": "always",
                     "status_apply": "stunned", "stat_mod": {"enemy": {"armor_bonus": -4}}, "mod_duration": 3},
                    {"id": "leviathan_spawn_deep_crush", "name": "Deep Crush", "power_type": "strike", "damage_type": "magical", "damage": 38, "cost_mp": 8, "cost_stamina": 30, "cooldown": 2, "trigger": "always",
                     "status_apply": "ensnared", "armor_ignore": True, "stat_mod": {"enemy": {"might": -5}}, "mod_duration": 3}],
         "defense": [{"id": "leviathan_spawn_deep_scales", "name": "Deep Scales", "power_type": "buff", "cost_mp": 5, "cost_stamina": 30, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 12, "essence": 6}}, "mod_duration": 3}],
         "utility": [{"id": "leviathan_spawn_abyssal_roar", "name": "Abyssal Roar", "power_type": "debuff", "damage_type": "magical", "damage": 8, "cost_mp": 8, "cost_stamina": 0, "cooldown": 2, "trigger": "opening_move",
                      "status_apply": "weary", "stat_mod": {"enemy": {"might": -6, "cognition": -4}}, "mod_duration": 3}],
     },
     "signature_fusion": {"id": "leviathan_spawn_abyssal_devastation", "name": "Abyssal Devastation", "power_type": "strike", "damage_type": "magical", "damage": 48, "cost_mp": 15, "cost_stamina": 25, "cooldown": 4, "hits": 3, "is_signature": True,
                          "status_apply": "ensnared", "armor_ignore": True, "lifesteal": 0.20, "stat_mod": {"enemy": {"might": -6, "essence": -5}}, "mod_duration": 4},
     "drops": {"common": [{"id": "leviathan_scale", "chance": 0.7, "qty": [1, 1]}, {"id": "abyssal_flesh", "chance": 0.4, "qty": [1, 1]}], "rare": [{"id": "void_essence", "chance": 0.15, "qty": [1, 1]}], "boss": [], "gold": [55, 70], "xp_mult": 2.2}},
    {"id": "abyssal_trench_leviathan", "name": "Abyssal Leviathan", "biome": "abyssal_trench", "rarity": "rare", "hp": 140,
     "creature_tier": "boss", "species": "beast", "archetype": "bruiser", "personality": "aggressive",
     "is_boss": True,
     "stats": {"might": {"base": 44, "growth": 3.2}, "grace": {"base": 20, "growth": 1.6}, "cognition": {"base": 18, "growth": 1.5},
               "insight": {"base": 20, "growth": 1.6}, "essence": {"base": 30, "growth": 2.4}, "durability": {"base": 36, "growth": 2.8}},
     "life": {"mp": 40, "stamina": 150, "shield": 15},
     "passive_buff": [{"type": "might_bonus", "value": 0.28}, {"type": "essence_bonus", "value": 0.22}, {"type": "durability_bonus", "value": 0.18}],
     "boss_aura": {"id": "abyssal_aura", "name": "Abyssal Aura", "effect": "weary", "desc": "The crushing depths drain all enemies, reducing their might and essence each turn."},
     "profile_skills": {
         "attack": [{"id": "abyssal_leviathan_void_maul", "name": "Void Maul", "power_type": "strike", "damage_type": "magical", "damage": 44, "cost_mp": 8, "cost_stamina": 25, "cooldown": 1, "trigger": "always",
                     "status_apply": "weary", "lifesteal": 0.15, "stat_mod": {"enemy": {"essence": -6}}, "mod_duration": 3},
                    {"id": "abyssal_leviathan_deep_crush", "name": "Deep Crush", "power_type": "strike", "damage_type": "magical", "damage": 50, "cost_mp": 12, "cost_stamina": 30, "cooldown": 2, "trigger": "always",
                     "status_apply": "ensnared", "armor_ignore": True, "stat_mod": {"enemy": {"might": -7, "essence": -5}}, "mod_duration": 3}],
         "defense": [{"id": "abyssal_leviathan_abyssal_carapace", "name": "Abyssal Carapace", "power_type": "buff", "cost_mp": 12, "cost_stamina": 0, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 16, "essence": 8}}, "mod_duration": 3},
                    {"id": "abyssal_leviathan_void_mend", "name": "Void Mend", "power_type": "heal", "cost_mp": 15, "cost_stamina": 0, "cooldown": 4, "trigger": "low_hp",
                      "heal_percent": 0.20, "self_status": "warded", "lifesteal": 0.10, "stat_mod": {"self": {"essence": 6}}, "mod_duration": 3}],
         "utility": [{"id": "abyssal_leviathan_abyssal_dread", "name": "Abyssal Dread", "power_type": "debuff", "damage_type": "magical", "damage": 14, "cost_mp": 15, "cost_stamina": 0, "cooldown": 3, "trigger": "opening_move",
                      "status_apply": "weary", "stat_mod": {"enemy": {"might": -7, "cognition": -6, "essence": -5}}, "mod_duration": 4}],
     },
     "signature_fusion": [{"id": "abyssal_leviathan_void_apocalypse", "name": "Void Apocalypse", "power_type": "strike", "damage_type": "magical", "damage": 60, "cost_mp": 25, "cost_stamina": 0, "cooldown": 5, "hits": 3, "is_signature": True,
                          "status_apply": "weary", "unevadable": True, "armor_ignore": True, "lifesteal": 0.30, "stat_mod": {"enemy": {"essence": -9, "might": -8}}, "mod_duration": 4},
                         {"id": "abyssal_leviathan_ocean_dominator", "name": "Ocean Dominator", "power_type": "strike", "damage_type": "magical", "damage": 52, "cost_mp": 18, "cost_stamina": 25, "cooldown": 4, "hits": 2, "is_signature": True,
                          "status_apply": "ensnared", "armor_ignore": True, "lifesteal": 0.20, "stat_mod": {"enemy": {"might": -7, "grace": -6}}, "mod_duration": 4}],
     "drops": {"common": [{"id": "leviathan_scale", "chance": 0.9, "qty": [1, 2]}], "rare": [{"id": "void_essence", "chance": 0.3, "qty": [1, 1]}], "boss": [{"id": "leviathan_crown", "chance": 0.15, "qty": [1, 1]}, {"id": "abyssal_core", "chance": 0.1, "qty": [1, 1]}], "gold": [90, 150], "xp_mult": 2.6}},
    # ---- Mistwood (Daw'ul Talalu Lv 36) ----
    {"id": "mistwood_stalker", "name": "Mistwood Stalker", "biome": "mistwood", "rarity": "common", "hp": 75,
     "creature_tier": "normal", "species": "beast", "archetype": "striker", "personality": "opportunist",
     "stats": {"might": {"base": 28, "growth": 2.2}, "grace": {"base": 26, "growth": 2.0}, "cognition": {"base": 14, "growth": 1.2},
               "insight": {"base": 18, "growth": 1.5}, "essence": {"base": 16, "growth": 1.3}, "durability": {"base": 18, "growth": 1.4}},
     "life": {"mp": 10, "stamina": 110, "shield": 0},
     "passive_buff": {"type": "grace_bonus", "value": 0.20, "secondary": {"type": "evasion_bonus", "value": 0.14}},
     "profile_skills": {
         "attack": [{"id": "mistwood_stalker_mist_claw", "name": "Mist Claw", "power_type": "strike", "damage_type": "physical", "damage": 30, "cost_mp": 0, "cost_stamina": 20, "cooldown": 1, "trigger": "always",
                     "status_apply": "bleeding", "unevadable": True, "stat_mod": {"enemy": {"grace": -4}}, "mod_duration": 3},
                    {"id": "mistwood_stalker_shadow_pounce", "name": "Shadow Pounce", "power_type": "strike", "damage_type": "physical", "damage": 32, "cost_mp": 0, "cost_stamina": 25, "cooldown": 2, "trigger": "always",
                     "status_apply": "stunned", "stat_mod": {"enemy": {"might": -4}}, "mod_duration": 2}],
         "defense": [{"id": "mistwood_stalker_mist_veil", "name": "Mist Veil", "power_type": "buff", "cost_mp": 0, "cost_stamina": 20, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "evasive", "stat_mod": {"self": {"grace": 6}}, "mod_duration": 2}],
         "utility": [{"id": "mistwood_stalker_fog_breath", "name": "Fog Breath", "power_type": "debuff", "damage_type": "magical", "damage": 6, "cost_mp": 5, "cost_stamina": 0, "cooldown": 2, "trigger": "opening_move",
                      "status_apply": "weary", "stat_mod": {"enemy": {"cognition": -5, "grace": -3}}, "mod_duration": 3}],
     },
     "signature_fusion": {"id": "mistwood_stalker_phantom_fang", "name": "Phantom Fang", "power_type": "strike", "damage_type": "physical", "damage": 42, "cost_mp": 0, "cost_stamina": 50, "cooldown": 4, "hits": 3, "is_signature": True,
                          "status_apply": "bleeding", "unevadable": True, "lifesteal": 0.20, "stat_mod": {"enemy": {"grace": -5}}, "mod_duration": 4},
     "drops": {"common": [{"id": "mistwood_pelt", "chance": 0.7, "qty": [1, 1]}, {"id": "shadow_herb", "chance": 0.4, "qty": [1, 1]}], "rare": [], "boss": [], "gold": [40, 55], "xp_mult": 1.9}},
    {"id": "mistwood_wraith", "name": "Mistwood Wraith", "biome": "mistwood", "rarity": "uncommon", "hp": 70,
     "creature_tier": "normal", "species": "undead", "archetype": "caster", "personality": "opportunist",
     "tags": ["undead"],
     "stats": {"might": {"base": 10, "growth": 0.8}, "grace": {"base": 22, "growth": 1.8}, "cognition": {"base": 26, "growth": 2.0},
               "insight": {"base": 28, "growth": 2.2}, "essence": {"base": 30, "growth": 2.4}, "durability": {"base": 12, "growth": 1.0}},
     "life": {"mp": 50, "stamina": 50, "shield": 0},
     "passive_buff": {"type": "essence_bonus", "value": 0.24, "secondary": {"type": "evasion_bonus", "value": 0.14}},
     "profile_skills": {
         "attack": [{"id": "mistwood_wraith_spectral_bolt", "name": "Spectral Bolt", "power_type": "strike", "damage_type": "magical", "damage": 30, "cost_mp": 6, "cost_stamina": 0, "cooldown": 1, "trigger": "always",
                     "status_apply": "weary", "stat_mod": {"enemy": {"essence": -5}}, "mod_duration": 3},
                    {"id": "mistwood_wraith_wail", "name": "Phantom Wail", "power_type": "strike", "damage_type": "magical", "damage": 32, "cost_mp": 8, "cost_stamina": 0, "cooldown": 2, "trigger": "always",
                     "status_apply": "weary", "unevadable": True, "stat_mod": {"enemy": {"cognition": -5, "grace": -3}}, "mod_duration": 3}],
         "defense": [{"id": "mistwood_wraith_phase_out", "name": "Phase Out", "power_type": "buff", "cost_mp": 8, "cost_stamina": 0, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "evasive", "stat_mod": {"self": {"grace": 7, "essence": 4}}, "mod_duration": 2}],
         "utility": [{"id": "mistwood_wraith_soul_drain", "name": "Soul Drain", "power_type": "debuff", "damage_type": "magical", "damage": 6, "cost_mp": 8, "cost_stamina": 0, "cooldown": 2, "trigger": "opening_move",
                      "status_apply": "weary", "lifesteal": 0.15, "stat_mod": {"enemy": {"essence": -5, "cognition": -4}}, "mod_duration": 3}],
     },
     "signature_fusion": {"id": "mistwood_wraith_spectral_storm", "name": "Spectral Storm", "power_type": "strike", "damage_type": "magical", "damage": 44, "cost_mp": 18, "cost_stamina": 0, "cooldown": 4, "hits": 3, "is_signature": True,
                          "status_apply": "weary", "unevadable": True, "lifesteal": 0.20, "stat_mod": {"enemy": {"essence": -7, "cognition": -6}}, "mod_duration": 4},
     "drops": {"common": [{"id": "wraith_essence", "chance": 0.6, "qty": [1, 1]}, {"id": "mistwood_pelt", "chance": 0.4, "qty": [1, 1]}], "rare": [{"id": "spectral_shard", "chance": 0.1, "qty": [1, 1]}], "boss": [], "gold": [45, 60], "xp_mult": 2.0}},
    {"id": "mistwood_revenant", "name": "Mistwood Revenant", "biome": "mistwood", "rarity": "rare", "hp": 110,
     "creature_tier": "mini_boss", "species": "undead", "archetype": "caster", "personality": "aggressive",
     "tags": ["undead"],
     "stats": {"might": {"base": 16, "growth": 1.3}, "grace": {"base": 22, "growth": 1.8}, "cognition": {"base": 30, "growth": 2.4},
               "insight": {"base": 32, "growth": 2.5}, "essence": {"base": 34, "growth": 2.6}, "durability": {"base": 18, "growth": 1.4}},
     "life": {"mp": 70, "stamina": 50, "shield": 5},
     "passive_buff": [{"type": "essence_bonus", "value": 0.26}, {"type": "cognition_bonus", "value": 0.18}],
     "profile_skills": {
         "attack": [{"id": "mistwood_revenant_spectral_lance", "name": "Spectral Lance", "power_type": "strike", "damage_type": "magical", "damage": 36, "cost_mp": 8, "cost_stamina": 0, "cooldown": 1, "trigger": "always",
                     "status_apply": "weary", "unevadable": True, "stat_mod": {"enemy": {"essence": -6}}, "mod_duration": 3},
                    {"id": "mistwood_revenant_wail_of_doom", "name": "Wail of Doom", "power_type": "strike", "damage_type": "magical", "damage": 40, "cost_mp": 10, "cost_stamina": 0, "cooldown": 2, "trigger": "always",
                     "status_apply": "weary", "unevadable": True, "armor_ignore": True, "stat_mod": {"enemy": {"cognition": -6, "might": -4}}, "mod_duration": 3}],
         "defense": [{"id": "mistwood_revenant_spectral_form", "name": "Spectral Form", "power_type": "buff", "cost_mp": 10, "cost_stamina": 0, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "evasive", "stat_mod": {"self": {"grace": 8, "essence": 6}}, "mod_duration": 3}],
         "utility": [{"id": "mistwood_revenant_mass_despair", "name": "Mass Despair", "power_type": "debuff", "damage_type": "magical", "damage": 10, "cost_mp": 12, "cost_stamina": 0, "cooldown": 3, "trigger": "opening_move",
                      "status_apply": "weary", "stat_mod": {"enemy": {"cognition": -7, "insight": -6, "might": -5}}, "mod_duration": 4}],
     },
     "signature_fusion": {"id": "mistwood_revenant_spectral_apocalypse", "name": "Spectral Apocalypse", "power_type": "strike", "damage_type": "magical", "damage": 50, "cost_mp": 20, "cost_stamina": 0, "cooldown": 4, "hits": 3, "is_signature": True,
                          "status_apply": "weary", "unevadable": True, "armor_ignore": True, "lifesteal": 0.25, "stat_mod": {"enemy": {"essence": -8, "cognition": -7}}, "mod_duration": 4},
     "drops": {"common": [{"id": "wraith_essence", "chance": 0.8, "qty": [1, 2]}], "rare": [{"id": "spectral_shard", "chance": 0.2, "qty": [1, 1]}], "boss": [{"id": "revenant_hood", "chance": 0.2, "qty": [1, 1]}], "gold": [55, 90], "xp_mult": 2.2}},
    # ---- Thorn Labyrinth (Daw'ul Talalu Lv 40) ----
    {"id": "thorn_beast", "name": "Thorn Beast", "biome": "thorn_labyrinth", "rarity": "common", "hp": 80,
     "creature_tier": "normal", "species": "monster", "archetype": "bruiser", "personality": "aggressive",
     "stats": {"might": {"base": 30, "growth": 2.4}, "grace": {"base": 16, "growth": 1.3}, "cognition": {"base": 10, "growth": 0.9},
               "insight": {"base": 12, "growth": 1.0}, "essence": {"base": 18, "growth": 1.5}, "durability": {"base": 24, "growth": 1.8}},
     "life": {"mp": 10, "stamina": 110, "shield": 5},
     "passive_buff": {"type": "might_bonus", "value": 0.20, "secondary": {"type": "durability_bonus", "value": 0.14}},
     "profile_skills": {
         "attack": [{"id": "thorn_beast_thorn_spike", "name": "Thorn Spike", "power_type": "strike", "damage_type": "physical", "damage": 32, "cost_mp": 0, "cost_stamina": 20, "cooldown": 1, "trigger": "always",
                     "status_apply": "poisoned", "stat_mod": {"enemy": {"grace": -4}}, "mod_duration": 3},
                    {"id": "thorn_beast_vine_whip", "name": "Vine Whip", "power_type": "strike", "damage_type": "physical", "damage": 34, "cost_mp": 0, "cost_stamina": 25, "cooldown": 2, "trigger": "always",
                     "status_apply": "ensnared", "stat_mod": {"enemy": {"might": -4}}, "mod_duration": 3}],
         "defense": [{"id": "thorn_beast_thorn_shell", "name": "Thorn Shell", "power_type": "buff", "cost_mp": 0, "cost_stamina": 25, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 10, "durability": 5}}, "mod_duration": 3}],
         "utility": [{"id": "thorn_beast_root_grab", "name": "Root Grab", "power_type": "debuff", "damage_type": "physical", "damage": 6, "cost_mp": 0, "cost_stamina": 25, "cooldown": 2, "trigger": "opening_move",
                      "status_apply": "ensnared", "stat_mod": {"enemy": {"grace": -5}}, "mod_duration": 3}],
     },
     "signature_fusion": {"id": "thorn_beast_thorn_rampage", "name": "Thorn Rampage", "power_type": "strike", "damage_type": "physical", "damage": 44, "cost_mp": 0, "cost_stamina": 50, "cooldown": 4, "hits": 3, "is_signature": True,
                          "status_apply": "poisoned", "lifesteal": 0.15, "stat_mod": {"enemy": {"might": -5, "grace": -5}}, "mod_duration": 4},
     "drops": {"common": [{"id": "thorn_vine", "chance": 0.7, "qty": [1, 1]}, {"id": "thorn_barb", "chance": 0.4, "qty": [1, 1]}], "rare": [], "boss": [], "gold": [45, 60], "xp_mult": 2.0}},
    {"id": "labyrinth_minotaur", "name": "Labyrinth Minotaur", "biome": "thorn_labyrinth", "rarity": "uncommon", "hp": 90,
     "creature_tier": "normal", "species": "monster", "archetype": "bruiser", "personality": "aggressive",
     "stats": {"might": {"base": 36, "growth": 2.8}, "grace": {"base": 14, "growth": 1.2}, "cognition": {"base": 12, "growth": 1.0},
               "insight": {"base": 14, "growth": 1.2}, "essence": {"base": 16, "growth": 1.3}, "durability": {"base": 26, "growth": 2.0}},
     "life": {"mp": 5, "stamina": 130, "shield": 5},
     "passive_buff": {"type": "might_bonus", "value": 0.22, "secondary": {"type": "durability_bonus", "value": 0.16}},
     "profile_skills": {
         "attack": [{"id": "labyrinth_minotaur_horn_charge", "name": "Horn Charge", "power_type": "strike", "damage_type": "physical", "damage": 34, "cost_mp": 0, "cost_stamina": 25, "cooldown": 1, "trigger": "always",
                     "status_apply": "stunned", "armor_ignore": True, "stat_mod": {"enemy": {"armor_bonus": -4}}, "mod_duration": 2},
                    {"id": "labyrinth_minotaur_labyrinth_smash", "name": "Labyrinth Smash", "power_type": "strike", "damage_type": "physical", "damage": 38, "cost_mp": 0, "cost_stamina": 35, "cooldown": 2, "trigger": "always",
                     "status_apply": "stunned", "stat_mod": {"enemy": {"might": -5, "grace": -4}}, "mod_duration": 3}],
         "defense": [{"id": "labyrinth_minotaur_thick_hide", "name": "Thick Hide", "power_type": "buff", "cost_mp": 0, "cost_stamina": 30, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 12, "durability": 7}}, "mod_duration": 3}],
         "utility": [{"id": "labyrinth_minotaur_bellowing_roar", "name": "Bellowing Roar", "power_type": "debuff", "damage_type": "physical", "damage": 8, "cost_mp": 0, "cost_stamina": 30, "cooldown": 2, "trigger": "opening_move",
                      "status_apply": "weary", "stat_mod": {"enemy": {"might": -5, "cognition": -4}}, "mod_duration": 3}],
     },
     "signature_fusion": {"id": "labyrinth_minotaur_labyrinth_devastation", "name": "Labyrinth Devastation", "power_type": "strike", "damage_type": "physical", "damage": 48, "cost_mp": 0, "cost_stamina": 50, "cooldown": 4, "hits": 3, "is_signature": True,
                          "status_apply": "stunned", "armor_ignore": True, "lifesteal": 0.20, "stat_mod": {"enemy": {"might": -6, "armor_bonus": -6}}, "mod_duration": 4},
     "drops": {"common": [{"id": "minotaur_horn", "chance": 0.6, "qty": [1, 1]}, {"id": "thorn_vine", "chance": 0.4, "qty": [1, 1]}], "rare": [{"id": "labyrinth_relic", "chance": 0.1, "qty": [1, 1]}], "boss": [], "gold": [50, 65], "xp_mult": 2.1}},
    {"id": "thorn_labyrinth_guardian", "name": "Labyrinth Guardian", "biome": "thorn_labyrinth", "rarity": "rare", "hp": 120,
     "creature_tier": "mini_boss", "species": "monster", "archetype": "bruiser", "personality": "guardian",
     "stats": {"might": {"base": 40, "growth": 3.0}, "grace": {"base": 18, "growth": 1.5}, "cognition": {"base": 16, "growth": 1.3},
               "insight": {"base": 18, "growth": 1.5}, "essence": {"base": 22, "growth": 1.8}, "durability": {"base": 30, "growth": 2.4}},
     "life": {"mp": 20, "stamina": 140, "shield": 10},
     "passive_buff": [{"type": "might_bonus", "value": 0.24}, {"type": "durability_bonus", "value": 0.18}],
     "profile_skills": {
         "attack": [{"id": "labyrinth_guardian_thorn_cleave", "name": "Thorn Cleave", "power_type": "strike", "damage_type": "physical", "damage": 38, "cost_mp": 0, "cost_stamina": 25, "cooldown": 1, "trigger": "always",
                     "status_apply": "poisoned", "stat_mod": {"enemy": {"armor_bonus": -5}}, "mod_duration": 3},
                    {"id": "labyrinth_guardian_labyrinth_slam", "name": "Labyrinth Slam", "power_type": "strike", "damage_type": "physical", "damage": 42, "cost_mp": 0, "cost_stamina": 35, "cooldown": 2, "trigger": "always",
                     "status_apply": "stunned", "armor_ignore": True, "stat_mod": {"enemy": {"might": -6, "grace": -5}}, "mod_duration": 3}],
         "defense": [{"id": "labyrinth_guardian_thorn_bastion", "name": "Thorn Bastion", "power_type": "buff", "cost_mp": 0, "cost_stamina": 30, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 14, "durability": 8}}, "mod_duration": 3}],
         "utility": [{"id": "labyrinth_guardian_entangle", "name": "Mass Entangle", "power_type": "debuff", "damage_type": "physical", "damage": 10, "cost_mp": 5, "cost_stamina": 30, "cooldown": 3, "trigger": "opening_move",
                      "status_apply": "ensnared", "stat_mod": {"enemy": {"grace": -6, "might": -5, "cognition": -4}}, "mod_duration": 4}],
     },
     "signature_fusion": {"id": "labyrinth_guardian_thorn_apocalypse", "name": "Thorn Apocalypse", "power_type": "strike", "damage_type": "physical", "damage": 52, "cost_mp": 0, "cost_stamina": 50, "cooldown": 4, "hits": 3, "is_signature": True,
                          "status_apply": "poisoned", "armor_ignore": True, "lifesteal": 0.25, "stat_mod": {"enemy": {"might": -7, "grace": -6}}, "mod_duration": 4},
     "drops": {"common": [{"id": "thorn_vine", "chance": 0.9, "qty": [1, 2]}], "rare": [{"id": "labyrinth_relic", "chance": 0.2, "qty": [1, 1]}], "boss": [{"id": "guardian_vineblade", "chance": 0.2, "qty": [1, 1]}], "gold": [60, 95], "xp_mult": 2.3}},
    # ---- Lumina Grove (Daw'ul Talalu Lv 44) ----
    {"id": "lumina_sprite", "name": "Lumina Sprite", "biome": "lumina_grove", "rarity": "common", "hp": 70,
     "creature_tier": "normal", "species": "magical", "archetype": "caster", "personality": "guardian",
     "stats": {"might": {"base": 8, "growth": 0.7}, "grace": {"base": 22, "growth": 1.8}, "cognition": {"base": 28, "growth": 2.2},
               "insight": {"base": 30, "growth": 2.4}, "essence": {"base": 32, "growth": 2.6}, "durability": {"base": 12, "growth": 1.0}},
     "life": {"mp": 50, "stamina": 50, "shield": 0},
     "passive_buff": {"type": "essence_bonus", "value": 0.24, "secondary": {"type": "insight_bonus", "value": 0.16}},
     "profile_skills": {
         "attack": [{"id": "lumina_sprite_radiant_bolt", "name": "Radiant Bolt", "power_type": "strike", "damage_type": "magical", "damage": 32, "cost_mp": 6, "cost_stamina": 0, "cooldown": 1, "trigger": "always",
                     "status_apply": "burning", "unevadable": True, "stat_mod": {"enemy": {"essence": -5}}, "mod_duration": 3},
                    {"id": "lumina_sprite_light_nova", "name": "Light Nova", "power_type": "strike", "damage_type": "magical", "damage": 34, "cost_mp": 8, "cost_stamina": 0, "cooldown": 2, "trigger": "always",
                     "status_apply": "weary", "unevadable": True, "stat_mod": {"enemy": {"cognition": -5}}, "mod_duration": 3}],
         "defense": [{"id": "lumina_sprite_light_shield", "name": "Light Shield", "power_type": "buff", "cost_mp": 8, "cost_stamina": 0, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 8, "essence": 5}}, "mod_duration": 3}],
         "utility": [{"id": "lumina_sprite_healing_glow", "name": "Healing Glow", "power_type": "heal", "cost_mp": 10, "cost_stamina": 0, "cooldown": 3, "trigger": "low_hp",
                      "heal_percent": 0.12, "self_status": "inspired", "stat_mod": {"self": {"essence": 4}}, "mod_duration": 2}],
     },
     "signature_fusion": {"id": "lumina_sprite_radiant_burst", "name": "Radiant Burst", "power_type": "strike", "damage_type": "magical", "damage": 46, "cost_mp": 18, "cost_stamina": 0, "cooldown": 4, "hits": 3, "is_signature": True,
                          "status_apply": "burning", "unevadable": True, "armor_ignore": True, "stat_mod": {"enemy": {"essence": -7, "cognition": -6}}, "mod_duration": 4},
     "drops": {"common": [{"id": "lumina_petal", "chance": 0.7, "qty": [1, 1]}, {"id": "radiant_essence", "chance": 0.3, "qty": [1, 1]}], "rare": [], "boss": [], "gold": [50, 65], "xp_mult": 2.1}},
    {"id": "lumina_dryad", "name": "Lumina Dryad", "biome": "lumina_grove", "rarity": "uncommon", "hp": 80,
     "creature_tier": "normal", "species": "magical", "archetype": "caster", "personality": "guardian",
     "stats": {"might": {"base": 14, "growth": 1.2}, "grace": {"base": 20, "growth": 1.6}, "cognition": {"base": 28, "growth": 2.2},
               "insight": {"base": 30, "growth": 2.4}, "essence": {"base": 32, "growth": 2.6}, "durability": {"base": 16, "growth": 1.3}},
     "life": {"mp": 55, "stamina": 60, "shield": 5},
     "passive_buff": {"type": "essence_bonus", "value": 0.26, "secondary": {"type": "cognition_bonus", "value": 0.16}},
     "profile_skills": {
         "attack": [{"id": "lumina_dryad_lumina_strike", "name": "Lumina Strike", "power_type": "strike", "damage_type": "magical", "damage": 34, "cost_mp": 6, "cost_stamina": 0, "cooldown": 1, "trigger": "always",
                     "status_apply": "burning", "unevadable": True, "stat_mod": {"enemy": {"essence": -5}}, "mod_duration": 3},
                    {"id": "lumina_dryad_radiant_lance", "name": "Radiant Lance", "power_type": "strike", "damage_type": "magical", "damage": 36, "cost_mp": 8, "cost_stamina": 0, "cooldown": 2, "trigger": "always",
                     "status_apply": "weary", "unevadable": True, "armor_ignore": True, "stat_mod": {"enemy": {"cognition": -6}}, "mod_duration": 3}],
         "defense": [{"id": "lumina_dryad_grove_ward", "name": "Grove Ward", "power_type": "buff", "cost_mp": 8, "cost_stamina": 0, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 10, "essence": 6}}, "mod_duration": 3}],
         "utility": [{"id": "lumina_dryad_grove_mend", "name": "Grove Mend", "power_type": "heal", "cost_mp": 12, "cost_stamina": 0, "cooldown": 3, "trigger": "low_hp",
                      "heal_percent": 0.15, "self_status": "inspired", "stat_mod": {"self": {"essence": 5}}, "mod_duration": 2}],
     },
     "signature_fusion": {"id": "lumina_dryad_radiant_storm", "name": "Radiant Storm", "power_type": "strike", "damage_type": "magical", "damage": 48, "cost_mp": 18, "cost_stamina": 0, "cooldown": 4, "hits": 3, "is_signature": True,
                          "status_apply": "burning", "unevadable": True, "armor_ignore": True, "stat_mod": {"enemy": {"essence": -7, "cognition": -6}}, "mod_duration": 4},
     "drops": {"common": [{"id": "lumina_petal", "chance": 0.6, "qty": [1, 1]}, {"id": "dryad_bark", "chance": 0.4, "qty": [1, 1]}], "rare": [{"id": "radiant_essence", "chance": 0.15, "qty": [1, 1]}], "boss": [], "gold": [55, 70], "xp_mult": 2.2}},
    {"id": "lumina_grove_oracle", "name": "Lumina Oracle", "biome": "lumina_grove", "rarity": "rare", "hp": 115,
     "creature_tier": "mini_boss", "species": "magical", "archetype": "caster", "personality": "guardian",
     "stats": {"might": {"base": 12, "growth": 1.0}, "grace": {"base": 22, "growth": 1.8}, "cognition": {"base": 34, "growth": 2.6},
               "insight": {"base": 36, "growth": 2.8}, "essence": {"base": 38, "growth": 3.0}, "durability": {"base": 18, "growth": 1.4}},
     "life": {"mp": 80, "stamina": 50, "shield": 5},
     "passive_buff": [{"type": "essence_bonus", "value": 0.28}, {"type": "cognition_bonus", "value": 0.22}],
     "profile_skills": {
         "attack": [{"id": "lumina_oracle_radiant_judgement", "name": "Radiant Judgement", "power_type": "strike", "damage_type": "magical", "damage": 40, "cost_mp": 10, "cost_stamina": 0, "cooldown": 1, "trigger": "always",
                     "status_apply": "burning", "unevadable": True, "armor_ignore": True, "stat_mod": {"enemy": {"essence": -6}}, "mod_duration": 3},
                    {"id": "lumina_oracle_light_cascade", "name": "Light Cascade", "power_type": "strike", "damage_type": "magical", "damage": 44, "cost_mp": 12, "cost_stamina": 0, "cooldown": 2, "trigger": "always",
                     "status_apply": "weary", "unevadable": True, "armor_ignore": True, "stat_mod": {"enemy": {"cognition": -7, "essence": -5}}, "mod_duration": 3}],
         "defense": [{"id": "lumina_oracle_radiant_bastion", "name": "Radiant Bastion", "power_type": "buff", "cost_mp": 12, "cost_stamina": 0, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 14, "essence": 8}}, "mod_duration": 3}],
         "utility": [{"id": "lumina_oracle_grove_mend", "name": "Grove Mend", "power_type": "heal", "cost_mp": 15, "cost_stamina": 0, "cooldown": 3, "trigger": "low_hp",
                      "heal_percent": 0.18, "self_status": "inspired", "stat_mod": {"self": {"essence": 6}}, "mod_duration": 3}],
     },
     "signature_fusion": {"id": "lumina_oracle_radiant_apocalypse", "name": "Radiant Apocalypse", "power_type": "strike", "damage_type": "magical", "damage": 54, "cost_mp": 25, "cost_stamina": 0, "cooldown": 4, "hits": 3, "is_signature": True,
                          "status_apply": "burning", "unevadable": True, "armor_ignore": True, "stat_mod": {"enemy": {"essence": -9, "cognition": -8}}, "mod_duration": 4},
     "drops": {"common": [{"id": "radiant_essence", "chance": 0.8, "qty": [1, 2]}], "rare": [{"id": "lumina_crystal", "chance": 0.2, "qty": [1, 1]}], "boss": [{"id": "oracle_staff", "chance": 0.2, "qty": [1, 1]}], "gold": [65, 100], "xp_mult": 2.4}},
    # ---- Elderroot Hollow (Daw'ul Talalu Lv 48) ----
    {"id": "elderroot_guardian", "name": "Elderroot Guardian", "biome": "elderroot_hollow", "rarity": "common", "hp": 95,
     "creature_tier": "normal", "species": "monster", "archetype": "tank", "personality": "guardian",
     "stats": {"might": {"base": 34, "growth": 2.6}, "grace": {"base": 12, "growth": 1.0}, "cognition": {"base": 14, "growth": 1.2},
               "insight": {"base": 16, "growth": 1.3}, "essence": {"base": 22, "growth": 1.8}, "durability": {"base": 32, "growth": 2.5}},
     "life": {"mp": 20, "stamina": 120, "shield": 10},
     "passive_buff": {"type": "durability_bonus", "value": 0.24, "secondary": {"type": "essence_bonus", "value": 0.16}},
     "profile_skills": {
         "attack": [{"id": "elderroot_guardian_root_crush", "name": "Root Crush", "power_type": "strike", "damage_type": "physical", "damage": 34, "cost_mp": 5, "cost_stamina": 25, "cooldown": 1, "trigger": "always",
                     "status_apply": "stunned", "stat_mod": {"enemy": {"armor_bonus": -5}}, "mod_duration": 3},
                    {"id": "elderroot_guardian_elder_slam", "name": "Elder Slam", "power_type": "strike", "damage_type": "magical", "damage": 36, "cost_mp": 8, "cost_stamina": 30, "cooldown": 2, "trigger": "always",
                     "status_apply": "ensnared", "armor_ignore": True, "stat_mod": {"enemy": {"might": -5}}, "mod_duration": 3}],
         "defense": [{"id": "elderroot_guardian_bark_armor", "name": "Elder Bark", "power_type": "buff", "cost_mp": 5, "cost_stamina": 30, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 14, "durability": 8}}, "mod_duration": 3}],
         "utility": [{"id": "elderroot_guardian_root_trap", "name": "Elder Root Trap", "power_type": "debuff", "damage_type": "physical", "damage": 8, "cost_mp": 5, "cost_stamina": 30, "cooldown": 2, "trigger": "opening_move",
                      "status_apply": "ensnared", "stat_mod": {"enemy": {"grace": -6, "might": -4}}, "mod_duration": 3}],
     },
     "signature_fusion": {"id": "elderroot_guardian_elderroot_devastation", "name": "Elderroot Devastation", "power_type": "strike", "damage_type": "magical", "damage": 48, "cost_mp": 15, "cost_stamina": 0, "cooldown": 4, "hits": 3, "is_signature": True,
                          "status_apply": "ensnared", "armor_ignore": True, "lifesteal": 0.20, "stat_mod": {"enemy": {"might": -6, "grace": -5}}, "mod_duration": 4},
     "drops": {"common": [{"id": "elderroot_bark", "chance": 0.7, "qty": [1, 1]}, {"id": "ancient_root", "chance": 0.3, "qty": [1, 1]}], "rare": [], "boss": [], "gold": [55, 70], "xp_mult": 2.2}},
    {"id": "elderroot_wisp", "name": "Elderroot Wisp", "biome": "elderroot_hollow", "rarity": "uncommon", "hp": 75,
     "creature_tier": "normal", "species": "magical", "archetype": "caster", "personality": "opportunist",
     "stats": {"might": {"base": 8, "growth": 0.7}, "grace": {"base": 24, "growth": 2.0}, "cognition": {"base": 30, "growth": 2.4},
               "insight": {"base": 32, "growth": 2.5}, "essence": {"base": 34, "growth": 2.8}, "durability": {"base": 12, "growth": 1.0}},
     "life": {"mp": 60, "stamina": 40, "shield": 0},
     "passive_buff": {"type": "essence_bonus", "value": 0.28, "secondary": {"type": "evasion_bonus", "value": 0.16}},
     "profile_skills": {
         "attack": [{"id": "elderroot_wisp_ancient_bolt", "name": "Ancient Bolt", "power_type": "strike", "damage_type": "magical", "damage": 36, "cost_mp": 6, "cost_stamina": 0, "cooldown": 1, "trigger": "always",
                     "status_apply": "weary", "unevadable": True, "stat_mod": {"enemy": {"essence": -6}}, "mod_duration": 3},
                    {"id": "elderroot_wisp_spectral_blast", "name": "Spectral Blast", "power_type": "strike", "damage_type": "magical", "damage": 38, "cost_mp": 8, "cost_stamina": 0, "cooldown": 2, "trigger": "always",
                     "status_apply": "weary", "unevadable": True, "armor_ignore": True, "stat_mod": {"enemy": {"cognition": -6}}, "mod_duration": 3}],
         "defense": [{"id": "elderroot_wisp_ancient_phase", "name": "Ancient Phase", "power_type": "buff", "cost_mp": 8, "cost_stamina": 0, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "evasive", "stat_mod": {"self": {"grace": 8, "essence": 5}}, "mod_duration": 2}],
         "utility": [{"id": "elderroot_wisp_ancient_mend", "name": "Ancient Mend", "power_type": "heal", "cost_mp": 12, "cost_stamina": 0, "cooldown": 3, "trigger": "low_hp",
                      "heal_percent": 0.15, "self_status": "warded", "stat_mod": {"self": {"essence": 5}}, "mod_duration": 2}],
     },
     "signature_fusion": {"id": "elderroot_wisp_ancient_storm", "name": "Ancient Storm", "power_type": "strike", "damage_type": "magical", "damage": 50, "cost_mp": 20, "cost_stamina": 0, "cooldown": 4, "hits": 3, "is_signature": True,
                          "status_apply": "weary", "unevadable": True, "armor_ignore": True, "lifesteal": 0.20, "stat_mod": {"enemy": {"essence": -8, "cognition": -7}}, "mod_duration": 4},
     "drops": {"common": [{"id": "ancient_root", "chance": 0.6, "qty": [1, 1]}, {"id": "wisp_essence", "chance": 0.4, "qty": [1, 1]}], "rare": [{"id": "elder_essence", "chance": 0.15, "qty": [1, 1]}], "boss": [], "gold": [60, 75], "xp_mult": 2.3}},
    {"id": "elderroot_hollow_ancient", "name": "Elderroot Ancient", "biome": "elderroot_hollow", "rarity": "rare", "hp": 140,
     "creature_tier": "boss", "species": "monster", "archetype": "bruiser", "personality": "guardian",
     "is_boss": True,
     "stats": {"might": {"base": 42, "growth": 3.2}, "grace": {"base": 18, "growth": 1.5}, "cognition": {"base": 24, "growth": 2.0},
               "insight": {"base": 26, "growth": 2.0}, "essence": {"base": 34, "growth": 2.8}, "durability": {"base": 40, "growth": 3.0}},
     "life": {"mp": 50, "stamina": 150, "shield": 15},
     "passive_buff": [{"type": "durability_bonus", "value": 0.28}, {"type": "essence_bonus", "value": 0.24}, {"type": "might_bonus", "value": 0.18}],
     "boss_aura": {"id": "elderroot_aura", "name": "Elderroot Aura", "effect": "ensnared", "desc": "Ancient roots ensnare all enemies each turn, reducing their grace and might."},
     "profile_skills": {
         "attack": [{"id": "elderroot_ancient_elder_crush", "name": "Elder Crush", "power_type": "strike", "damage_type": "magical", "damage": 44, "cost_mp": 8, "cost_stamina": 25, "cooldown": 1, "trigger": "always",
                     "status_apply": "stunned", "armor_ignore": True, "stat_mod": {"enemy": {"armor_bonus": -6}}, "mod_duration": 3},
                    {"id": "elderroot_ancient_root_apocalypse", "name": "Root Apocalypse", "power_type": "strike", "damage_type": "magical", "damage": 50, "cost_mp": 12, "cost_stamina": 30, "cooldown": 2, "trigger": "always",
                     "status_apply": "ensnared", "unevadable": True, "armor_ignore": True, "stat_mod": {"enemy": {"might": -7, "grace": -6}}, "mod_duration": 3}],
         "defense": [{"id": "elderroot_ancient_elder_bark", "name": "Elder Bark Bastion", "power_type": "buff", "cost_mp": 12, "cost_stamina": 0, "cooldown": 3, "trigger": "low_hp",
                      "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 18, "durability": 10}}, "mod_duration": 3},
                    {"id": "elderroot_ancient_elder_mend", "name": "Elder Mend", "power_type": "heal", "cost_mp": 15, "cost_stamina": 0, "cooldown": 4, "trigger": "low_hp",
                      "heal_percent": 0.20, "self_status": "warded", "lifesteal": 0.10, "stat_mod": {"self": {"armor_bonus": 8, "essence": 6}}, "mod_duration": 3}],
         "utility": [{"id": "elderroot_ancient_mass_entangle", "name": "Mass Entangle", "power_type": "debuff", "damage_type": "magical", "damage": 14, "cost_mp": 15, "cost_stamina": 0, "cooldown": 3, "trigger": "opening_move",
                      "status_apply": "ensnared", "unevadable": True, "stat_mod": {"enemy": {"might": -7, "grace": -7, "cognition": -5}}, "mod_duration": 4}],
     },
     "signature_fusion": [{"id": "elderroot_ancient_elderroot_annihilation", "name": "Elderroot Annihilation", "power_type": "strike", "damage_type": "magical", "damage": 60, "cost_mp": 25, "cost_stamina": 0, "cooldown": 5, "hits": 3, "is_signature": True,
                          "status_apply": "ensnared", "unevadable": True, "armor_ignore": True, "lifesteal": 0.30, "stat_mod": {"enemy": {"might": -9, "grace": -8}}, "mod_duration": 4},
                         {"id": "elderroot_ancient_natures_wrath", "name": "Nature's Wrath", "power_type": "strike", "damage_type": "magical", "damage": 52, "cost_mp": 18, "cost_stamina": 25, "cooldown": 4, "hits": 2, "is_signature": True,
                          "status_apply": "stunned", "armor_ignore": True, "stat_mod": {"enemy": {"might": -7, "essence": -6}}, "mod_duration": 4}],
     "drops": {"common": [{"id": "elder_essence", "chance": 0.9, "qty": [1, 2]}], "rare": [{"id": "ancient_heartwood", "chance": 0.3, "qty": [1, 1]}], "boss": [{"id": "elder_crown", "chance": 0.15, "qty": [1, 1]}, {"id": "elderroot_core", "chance": 0.1, "qty": [1, 1]}], "gold": [100, 160], "xp_mult": 2.8}},
]


# ============================================================
# MATERIALS + ITEMS
# ============================================================
# rarity: common | uncommon | rare | epic | legendary | mythic
# kind: material | weapon | armor | consumable | skillbook | relic
ITEMS: list[dict] = [
    # --- Materials (common) ---
    {"id": "wild_herb",     "name": "Wild Herb",     "rarity": "common",   "kind": "material", "biome_gather": ["grasslands", "oakwood"], "desc": "A common herb found along roadsides and forest edges. Healers boil it into bitter draughts."},
    {"id": "iron_ore",      "name": "Iron Ore",      "rarity": "common",   "kind": "material", "biome_gather": ["grasslands", "old_ruins"], "desc": "Rust-flecked nuggets pried from shallow deposits. The backbone of every frontier smithy."},
    {"id": "oak_log",       "name": "Oak Log",       "rarity": "common",   "kind": "material", "biome_gather": ["oakwood"], "desc": "A sturdy log from the old oaks of Crownwood. Resists fire, splits true, and holds a nail like a friend."},
    {"id": "river_stone",   "name": "River Stone",   "rarity": "common",   "kind": "material", "biome_gather": ["riverlands"], "desc": "Smooth and grey, worn by centuries of current. Used for grinding, throwing, and the occasional crude hammer."},
    {"id": "copper_ore",    "name": "Copper Ore",    "rarity": "common",   "kind": "material", "biome_gather": ["grasslands"], "desc": "Green-veined rock that sweats red when heated. Too soft for blades, but it rings beautifully in bells."},
    # --- Materials (uncommon) ---
    {"id": "wolf_pelt",     "name": "Wolf Pelt",     "rarity": "uncommon", "kind": "material", "desc": "Thick grey fur from a plains wolf. Still carries the scent of the hunt."},
    {"id": "wolf_fang",     "name": "Wolf Fang",     "rarity": "uncommon", "kind": "material", "desc": "A curved fang pulled from a wolf's jaw. Bone-workers pay well for these."},
    {"id": "boar_hide",     "name": "Boar Hide",     "rarity": "uncommon", "kind": "material", "desc": "Tough and bristled. Takes dye poorly, but turns a blade almost as well as leather."},
    {"id": "boar_tusk",     "name": "Boar Tusk",     "rarity": "uncommon", "kind": "material", "desc": "A yellowed tusk from an old boar. Carved into pins, handles, and the occasional lucky charm."},
    {"id": "serpent_scale", "name": "Serpent Scale", "rarity": "uncommon", "kind": "material", "desc": "Iridescent and cool to the touch. Alchemists grind it into poultices; smiths laminate it into armor."},
    {"id": "wisp_essence",  "name": "Wisp Essence",  "rarity": "uncommon", "kind": "material", "desc": "A flickering mote of light captured in glass. It hums faintly when held near enchanted things."},
    # --- Materials (rare) ---
    {"id": "serpent_venom", "name": "Serpent Venom", "rarity": "rare",     "kind": "material", "desc": "A few drops could stop a horse. Alchemists dilute it; assassins do not."},
    {"id": "ghast_dust",    "name": "Ghast Dust",    "rarity": "rare",     "kind": "material", "desc": "Pale powder scraped from a defeated ghast. It smells of crypt air and old candles."},
    {"id": "relic_shard",   "name": "Relic Shard",   "rarity": "epic",     "kind": "relic", "desc": "A fragment of something ancient and powerful. It vibrates when brought near other shards."},
    # --- Gold pouch / drops ---
    {"id": "coin_purse",    "name": "Coin Purse",    "rarity": "common",   "kind": "consumable", "effect": {"gold": 15}, "desc": "A small leather pouch jingling with someone else's bad luck."},
    # --- Consumables ---
    {"id": "minor_healing_potion","name":"Minor Healing Potion","rarity":"common", "kind":"consumable",
     "effect": {"heal": 15}, "trigger": "hp_below_50", "desc": "A bitter draught brewed from wild herbs and river water. Tastes like survival."},
    {"id": "greater_healing_potion","name":"Greater Healing Potion","rarity":"uncommon","kind":"consumable",
     "effect": {"heal": 35}, "trigger": "hp_below_40", "desc": "Refined herbs suspended in honeyed wine. Closes wounds faster than they open."},
    {"id": "antidote",       "name": "Antidote",       "rarity": "common",   "kind": "consumable",
     "effect": {"cure": "poison"}, "trigger": "status_poison", "desc": "A chalky paste dissolved in warm water. Tastes terrible, works instantly."},
    {"id": "bandage",        "name": "Bandage",        "rarity": "common",   "kind": "consumable",
     "effect": {"cure": "bleeding"}, "trigger": "status_bleeding", "desc": "Strips of clean linen. Not glamorous, but it has saved more lives than any sword."},
    {"id": "acid_flask_item","name": "Acid Flask",     "rarity": "uncommon", "kind": "consumable",
     "effect": {"damage": 20}, "trigger": "opponent_hp_high", "desc": "A glass vial of greenish liquid that eats through leather, flesh, and ambition."},
    # --- Skillbooks ---
    {"id": "skillbook_ward",  "name":"Skillbook: Ward",  "rarity":"rare","kind":"skillbook","teaches":"ward", "desc": "A worn tome bound in white leather. The pages describe a shield of pure will — the first lesson every priest learns."},
    {"id": "skillbook_purge", "name":"Skillbook: Purge", "rarity":"rare","kind":"skillbook","teaches":"purge", "desc": "Inscribed with cleansing rites from the priories of Nyxmoor. The ink smudges when held near corruption."},
    {"id": "skillbook_thornlash","name":"Skillbook: Thornlash","rarity":"epic","kind":"skillbook","teaches":"thornlash", "desc": "Written in a hand that might have been a root system. Teaches the old sylvan art of turning vines into whips."},
    {"id": "skillbook_smite", "name":"Skillbook: Smite", "rarity":"epic","kind":"skillbook","teaches":"smite", "desc": "A heavy book that crackles when opened. The first chapter reads: 'There are those who deserve the lightning. Begin.'"},
    # --- Legendary / Mythic teasers ---
    {"id": "jahra_ingot",    "name":"Jahra Ingot",    "rarity":"legendary","kind":"material","desc":"A rare Dwarven metal, light as breath yet strong as fate. Only the deepest forges of Khardrum can work it."},
    {"id": "orb_fragment",   "name":"Orb Fragment",   "rarity":"mythic",   "kind":"relic",   "desc":"A shard fallen from the Orb of Hyliondrias. It pulses with a warmth that has nothing to do with fire."},
    # --- Gathering Tools ---
    {"id": "pickaxe",          "name": "Pickaxe",           "rarity": "common", "kind": "tool", "profession": "mining",     "max_durability": 100, "desc": "A sturdy iron pickaxe. The head rings true against stone, and the haft has seen a thousand veins."},
    {"id": "herbalist_knife",  "name": "Herbalist Knife",  "rarity": "common", "kind": "tool", "profession": "herbalism",  "max_durability": 80,  "desc": "A curved blade for cutting stems and scraping roots. Smells of old sap and newer medicine."},
    {"id": "logging_axe",      "name": "Logging Axe",      "rarity": "common", "kind": "tool", "profession": "logging",     "max_durability": 100, "desc": "A broad-bladed felling axe. Heavy enough to do the work, light enough to carry home."},
    {"id": "hunting_bow",      "name": "Hunter's Kit",     "rarity": "common", "kind": "tool", "profession": "hunting",     "max_durability": 90,  "desc": "A satchel of snares, calls, and skinning tools. Everything a hunter needs but the patience."},
    {"id": "fishing_rod",      "name": "Fishing Rod",      "rarity": "common", "kind": "tool", "profession": "fishing",     "max_durability": 60,  "desc": "A supple cane pole with a bone hook and twine line. It bends but does not break — mostly."},
    {"id": "excavator_brush",  "name": "Excavator's Brush","rarity": "common", "kind": "tool", "profession": "excavation",  "max_durability": 60,  "desc": "Soft bristles and a pointed trowel. For dusting away centuries without disturbing what lies beneath."},
]

ITEMS_BY_ID: dict[str, dict] = {it["id"]: it for it in ITEMS}

# ============================================================
# New Item System — import procedural item module
# ============================================================
from items import (  # noqa: E402
    WEAPON_TYPES,
    ARMOR_TYPES,
    ARMOR_PER_RESILIENCE,
    BASE_ITEMS,
    BASE_ITEMS_BY_ID,
    PREFIXES,
    SUFFIXES,
    GEMS,
    GEMS_BY_ID,
    RUNES,
    RUNES_BY_ID,
    UNIQUE_ITEMS,
    UNIQUE_ITEMS_BY_ID,
    SET_BONUSES,
    SET_ITEMS,
    SET_ITEMS_BY_ID,
    LEGENDARY_POWERS,
    generate_drop,
    generate_rune_drop,
    build_item_instance,
    compute_item_total_stats,
    compute_item_bonus_effects,
    socket_gem,
    socket_rune,
    get_upgrade_count,
    can_upgrade,
    get_upgrade_summary,
)

# Merge base items into ITEMS for backward compatibility lookups
_existing_item_ids = {it["id"] for it in ITEMS}
for _bi in BASE_ITEMS:
    if _bi["id"] not in _existing_item_ids:
        ITEMS.append(_bi)
        ITEMS_BY_ID[_bi["id"]] = _bi
        _existing_item_ids.add(_bi["id"])

# Merge set items into ITEMS
for _si in SET_ITEMS:
    if _si["id"] not in _existing_item_ids:
        ITEMS.append(_si)
        ITEMS_BY_ID[_si["id"]] = _si
        _existing_item_ids.add(_si["id"])

# Merge unique items into ITEMS (as templates)
for _ui in UNIQUE_ITEMS:
    if _ui["id"] not in _existing_item_ids:
        ITEMS.append(_ui)
        ITEMS_BY_ID[_ui["id"]] = _ui
        _existing_item_ids.add(_ui["id"])

# Merge gems into ITEMS
for _g in GEMS:
    if _g["id"] not in _existing_item_ids:
        _g_copy = dict(_g)
        _g_copy["kind"] = "gem"
        _g_copy["rarity"] = "uncommon"
        ITEMS.append(_g_copy)
        ITEMS_BY_ID[_g["id"]] = _g_copy
        _existing_item_ids.add(_g["id"])

# Merge runes into ITEMS
for _r in RUNES:
    if _r["id"] not in _existing_item_ids:
        _r_copy = dict(_r)
        _r_copy["kind"] = "rune"
        _r_copy["rarity"] = "uncommon"
        ITEMS.append(_r_copy)
        ITEMS_BY_ID[_r["id"]] = _r_copy
        _existing_item_ids.add(_r["id"])

# 12 equipment slots
EQUIP_SLOTS = [
    "head", "body", "left_hand", "right_hand",
    "legs", "feet", "hands", "earring_l", "earring_r",
    "ring_l", "ring_r", "neck", "back",
]

# Map old generic weapon_req values to new weapon_types
WEAPON_REQ_MAP: dict[str, list[str]] = {
    "sword":   ["sword_1h", "sword_2h"],
    "dagger":  ["dagger"],
    "spear":   ["spear"],
    "bow":     ["bow", "crossbow"],
    "mace":    ["hammer_1h", "great_hammer"],
    "shield":  ["shield"],
    "katar":   ["katar"],
    "tome":    ["tome", "orb"],
    "axe":     ["axe_1h", "great_axe"],
    "scythe":  ["scythe"],
    "instrument": ["instrument"],
    "none":    [],  # no weapon requirement
}

SLOT_LABELS = {
    "head": "Head",
    "body": "Body",
    "left_hand": "Left Hand",
    "right_hand": "Right Hand",
    "legs": "Legs",
    "feet": "Feet",
    "hands": "Hands",
    "earring_l": "Earring (L)",
    "earring_r": "Earring (R)",
    "ring_l": "Ring (L)",
    "ring_r": "Ring (R)",
    "neck": "Necklace",
    "back": "Back",
}

# Slots that accept weapons (for power calculation)
WEAPON_SLOTS = ["left_hand", "right_hand"]
# Slots that contribute to armor power. "hands" is included — gloves and
# gauntlets exist as base items but were previously unequippable because
# "hands" was missing from EQUIP_SLOTS entirely.
ARMOR_SLOTS = ["head", "body", "legs", "feet", "hands", "back"]


# ============================================================
# SKILLS
# ============================================================
# power_type: strike | defend | heal | debuff | crit_boost
# damage_type: physical | magical | true  (only relevant for strike/debuff)
# skill_capacity_cost: 1 (basic) | 2 (advanced) | 3 (ultimate) | 0 (free action / defend / heal)
# trigger: always | low_hp | opponent_wounded | opponent_status | opening_move
SKILLS: list[dict] = [
    {"id": "shield_bash",   "name": "Shield Bash",   "cooldown": 2, "damage": 6,  "power_type": "strike",  "damage_type": "physical", "skill_capacity_cost": 1, "trigger": "always",           "status_apply": "stunned"},
    {"id": "sworn_strike",  "name": "Sworn Strike",  "cooldown": 3, "damage": 10, "power_type": "strike",  "damage_type": "physical", "skill_capacity_cost": 2, "trigger": "always"},
    {"id": "smite",         "name": "Smite",         "cooldown": 3, "damage": 12, "power_type": "strike",  "damage_type": "magical",  "skill_capacity_cost": 2, "trigger": "opponent_wounded"},
    {"id": "lay_on_hands",  "name": "Lay on Hands",  "cooldown": 4, "damage": 25, "power_type": "heal",    "skill_capacity_cost": 2, "trigger": "low_hp"},
    {"id": "thrust",        "name": "Thrust",        "cooldown": 1, "damage": 5,  "power_type": "strike",  "damage_type": "physical", "skill_capacity_cost": 1, "trigger": "always"},
    {"id": "impale",        "name": "Impale",        "cooldown": 4, "damage": 15, "power_type": "strike",  "damage_type": "physical", "skill_capacity_cost": 2, "trigger": "opening_move", "status_apply": "bleeding"},
    {"id": "backstab",      "name": "Backstab",      "type": "assassin", "cooldown": 3, "damage": 14, "power_type": "strike",  "damage_type": "physical", "skill_capacity_cost": 1, "trigger": "opening_move", "status_apply": "bleeding", "stat_mod": {"enemy": {"grace": -3, "might": -2}}, "mod_duration": 2},
    {"id": "vanish",        "name": "Vanish",        "cooldown": 5, "damage": 0,  "power_type": "defend",  "skill_capacity_cost": 0, "trigger": "low_hp",           "self_status": "hidden"},
    {"id": "mocking_verse", "name": "Mocking Verse", "type": "bard", "cooldown": 3, "damage": 3,  "power_type": "debuff",  "damage_type": "magical",  "skill_capacity_cost": 1, "trigger": "always",           "status_apply": "shaken", "stat_mod": {"enemy": {"might": -2, "grace": -1}}, "mod_duration": 2},
    {"id": "rally",         "name": "Rally",         "cooldown": 4, "damage": 15, "power_type": "heal",    "skill_capacity_cost": 2, "trigger": "low_hp"},
    {"id": "mix_potion",    "name": "Mix Potion",    "cooldown": 6, "damage": 20, "power_type": "heal",    "skill_capacity_cost": 1, "trigger": "low_hp"},
    {"id": "acid_flask",    "name": "Acid Flask",    "cooldown": 2, "damage": 7,  "power_type": "strike",  "damage_type": "magical",  "skill_capacity_cost": 1, "trigger": "always",           "status_apply": "burning"},
    {"id": "arcane_bolt",   "name": "Arcane Bolt",   "cooldown": 1, "damage": 6,  "power_type": "strike",  "damage_type": "magical",  "skill_capacity_cost": 1, "trigger": "always"},
    {"id": "ward",          "name": "Ward",          "cooldown": 4, "damage": 0,  "power_type": "defend",  "skill_capacity_cost": 0, "trigger": "always",           "self_status": "warded"},
    {"id": "divine_light",  "name": "Divine Light",  "cooldown": 3, "damage": 10, "power_type": "strike",  "damage_type": "magical",  "skill_capacity_cost": 2, "trigger": "opponent_status", "status_apply": "blinded"},
    {"id": "purge",         "name": "Purge",         "cooldown": 3, "damage": 0,  "power_type": "defend",  "skill_capacity_cost": 0, "trigger": "self_debuff"},
    {"id": "thornlash",     "name": "Thornlash",     "cooldown": 2, "damage": 8,  "power_type": "strike",  "damage_type": "physical", "skill_capacity_cost": 1, "trigger": "always",           "status_apply": "bleeding"},
    {"id": "beast_call",    "name": "Beast Call",    "cooldown": 5, "damage": 12, "power_type": "strike",  "damage_type": "physical", "skill_capacity_cost": 2, "trigger": "always"},
    {"id": "shadow_step",   "name": "Shadow Step",   "cooldown": 3, "damage": 0,  "power_type": "defend",  "skill_capacity_cost": 0, "trigger": "always",           "self_status": "evasive"},
    {"id": "poison_blade",  "name": "Poison Blade",  "cooldown": 3, "damage": 8,  "power_type": "strike",  "damage_type": "physical", "skill_capacity_cost": 1, "trigger": "always",           "status_apply": "poisoned"},
    {"id": "aimed_shot",    "name": "Aimed Shot",    "cooldown": 2, "damage": 10, "power_type": "strike",  "damage_type": "physical", "skill_capacity_cost": 2, "trigger": "opening_move"},
    {"id": "trap",          "name": "Trap",          "cooldown": 4, "damage": 6,  "power_type": "debuff",  "damage_type": "physical", "skill_capacity_cost": 1, "trigger": "always",           "status_apply": "ensnared"},
    {"id": "mend",          "name": "Mend",          "cooldown": 3, "damage": 18, "power_type": "heal",    "skill_capacity_cost": 1, "trigger": "low_hp"},
    # --- Alchemist Mastery: Transmutation Arts ---
    # Basic Tier (Level 1)
    {"id": "acid_bomb",              "name": "Acid Bomb",              "type": "imbuable", "power_type": "imbue",    "damage_type": "physical", "cooldown": 4, "damage": 0,  "skill_capacity_cost": 1, "trigger": "always",           "imbue_charges": 3, "imbue_status": "burning",  "imbue_stat_mod": {"enemy": {"armor_bonus": -3}},                     "imbue_mod_duration": 2, "imbue_mini_rule": "stacking_armor_shred",      "blade_shape": "liquid"},
    {"id": "flash_powder_alch",      "name": "Flash Powder",           "type": "imbuable", "power_type": "imbue",    "damage_type": "physical", "cooldown": 4, "damage": 0,  "skill_capacity_cost": 1, "trigger": "always",           "imbue_charges": 3, "imbue_status": "blinded",  "imbue_stat_mod": {"enemy": {"grace": -2}},                           "imbue_mod_duration": 2, "imbue_mini_rule": "stacking_accuracy_drain",   "blade_shape": "mirror"},
    {"id": "quick_jab",              "name": "Quick Jab",              "type": "strike",   "power_type": "strike",   "damage_type": "physical", "cooldown": 1, "damage": 4,  "skill_capacity_cost": 1, "trigger": "always",           "hits": 1, "cf_gain": 1, "strike_rule": "never_misses"},
    {"id": "heavy_crush",            "name": "Heavy Crush",            "type": "strike",   "power_type": "strike",   "damage_type": "physical", "cooldown": 2, "damage": 10, "skill_capacity_cost": 1, "trigger": "always",           "hits": 1, "cf_gain": 1, "strike_rule": "armor_break"},
    {"id": "healing_draught",        "name": "Healing Draught",        "type": "cast",     "power_type": "heal",     "damage_type": "physical", "cooldown": 3, "damage": 12, "skill_capacity_cost": 1, "trigger": "low_hp",           "self_status": "warded", "heal_percent": 0.10, "stat_mod": {"self": {"essence": 1}}, "mod_duration": 2},
    {"id": "iron_skin_transmutation","name": "Iron Skin Transmutation","type": "cast",     "power_type": "buff",     "damage_type": "physical", "cooldown": 4, "damage": 0,  "skill_capacity_cost": 1, "trigger": "always",           "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 4}}, "mod_duration": 3},
    # Advanced Tier (Level 3)
    {"id": "frost_mixture",          "name": "Frost Mixture",          "type": "imbuable", "power_type": "imbue",    "damage_type": "physical", "cooldown": 4, "damage": 0,  "skill_capacity_cost": 2, "trigger": "always",           "imbue_charges": 3, "imbue_status": "ensnared", "imbue_stat_mod": {"enemy": {"grace": -2, "might": -2}},                "imbue_mod_duration": 3, "imbue_mini_rule": "freeze_on_4th_hit",        "blade_shape": "ice_spike"},
    {"id": "lightning_bottle",       "name": "Lightning Bottle",       "type": "imbuable", "power_type": "imbue",    "damage_type": "physical", "cooldown": 5, "damage": 0,  "skill_capacity_cost": 2, "trigger": "always",           "imbue_charges": 2, "imbue_status": "stunned",  "imbue_stat_mod": {"enemy": {"grace": -2, "armor_bonus": -2}},           "imbue_mod_duration": 2, "imbue_mini_rule": "chain_on_3rd_hit",          "blade_shape": "claw"},
    {"id": "poison_capsule",         "name": "Poison Capsule",         "type": "imbuable", "power_type": "imbue",    "damage_type": "physical", "cooldown": 4, "damage": 0,  "skill_capacity_cost": 2, "trigger": "always",           "imbue_charges": 4, "imbue_status": "poisoned", "imbue_stat_mod": {"enemy": {"might": -3, "cognition": -2}},             "imbue_mod_duration": 3, "imbue_mini_rule": "scaling_damage_over_time",  "blade_shape": "needle"},
    {"id": "flurry",                 "name": "Flurry",                 "type": "strike",   "power_type": "strike",   "damage_type": "physical", "cooldown": 3, "damage": 3,  "skill_capacity_cost": 2, "trigger": "always",           "hits": 3, "cf_gain": 3, "strike_rule": "cf_builder"},
    {"id": "rushing_strike",         "name": "Rushing Strike",         "type": "strike",   "power_type": "strike",   "damage_type": "physical", "cooldown": 2, "damage": 6,  "skill_capacity_cost": 1, "trigger": "always",           "hits": 1, "cf_gain": 1, "strike_rule": "gap_close_and_reload"},
    {"id": "swift_transmutation",    "name": "Swift Transmutation",    "type": "cast",     "power_type": "buff",     "damage_type": "physical", "cooldown": 4, "damage": 0,  "skill_capacity_cost": 2, "trigger": "always",           "self_status": "evasive", "stat_mod": {"self": {"grace": 4, "might": 1}}, "mod_duration": 3},
    {"id": "stone_wall",             "name": "Stone Wall",             "type": "cast",     "power_type": "defend",   "damage_type": "physical", "cooldown": 4, "damage": 0,  "skill_capacity_cost": 1, "trigger": "always",           "self_status": "warded", "stat_mod": {"self": {"grace": 2}}, "mod_duration": 2},
    # Expert Tier (Level 8)
    {"id": "corrosive_mist",         "name": "Corrosive Mist",         "type": "imbuable", "power_type": "imbue",    "damage_type": "physical", "cooldown": 5, "damage": 0,  "skill_capacity_cost": 2, "trigger": "opponent_status",  "imbue_charges": 3, "imbue_status": "burning",  "imbue_stat_mod": {"enemy": {"armor_bonus": -4, "might": -2}},           "imbue_mod_duration": 3, "imbue_mini_rule": "feeds_on_existing_statuses","blade_shape": "eroding"},
    {"id": "living_slime",           "name": "Living Slime",           "type": "imbuable", "power_type": "imbue",    "damage_type": "physical", "cooldown": 5, "damage": 0,  "skill_capacity_cost": 2, "trigger": "always",           "imbue_charges": 2, "imbue_status": "ensnared", "imbue_stat_mod": {"enemy": {"grace": -3, "might": -3, "armor_bonus": -2}}, "imbue_mod_duration": 3, "imbue_mini_rule": "immobilize_on_3rd_hit",    "blade_shape": "whip"},
    {"id": "transmutation_touch",    "name": "Transmutation Touch",    "type": "imbuable", "power_type": "imbue",    "damage_type": "physical", "cooldown": 5, "damage": 0,  "skill_capacity_cost": 2, "trigger": "opponent_wounded", "imbue_charges": 2, "imbue_status": "shaken",   "imbue_stat_mod": {"enemy": {"armor_bonus": -5, "might": -3, "essence": -2}},"imbue_mod_duration": 3, "imbue_mini_rule": "armor_to_paper_on_2nd_hit","blade_shape": "dull_edge"},
    {"id": "explosive_chain",        "name": "Explosive Chain",        "type": "imbuable", "power_type": "imbue",    "damage_type": "physical", "cooldown": 5, "damage": 0,  "skill_capacity_cost": 2, "trigger": "always",           "imbue_charges": 2, "imbue_status": "burning",  "imbue_stat_mod": {"enemy": {"armor_bonus": -3, "grace": -2}},           "imbue_mod_duration": 2, "imbue_mini_rule": "double_hit_detonation",    "blade_shape": "jagged"},
    {"id": "spinning_strike",        "name": "Spinning Strike",        "type": "strike",   "power_type": "strike",   "damage_type": "physical", "cooldown": 3, "damage": 7,  "skill_capacity_cost": 2, "trigger": "always",           "hits": 1, "cf_gain": 1, "strike_rule": "reposition"},
    {"id": "piercing_strike",        "name": "Piercing Strike",        "type": "strike",   "power_type": "strike",   "damage_type": "physical", "cooldown": 2, "damage": 8,  "skill_capacity_cost": 2, "trigger": "always",           "hits": 1, "cf_gain": 1, "strike_rule": "ignores_50_percent_armor"},
    {"id": "counter_strike",         "name": "Counter Strike",         "type": "strike",   "power_type": "strike",   "damage_type": "physical", "cooldown": 2, "damage": 7,  "skill_capacity_cost": 2, "trigger": "always",           "hits": 1, "cf_gain": 1, "strike_rule": "interrupt"},
    # Master Tier (Level 15)
    {"id": "forbidden_formula",      "name": "Forbidden Formula",      "type": "imbuable", "power_type": "imbue",    "damage_type": "true",     "cooldown": 6, "damage": 0,  "skill_capacity_cost": 3, "trigger": "low_hp",           "imbue_charges": 1, "imbue_status": "burning",  "imbue_stat_mod": {"enemy": {"armor_bonus": -5, "grace": -4, "might": -3}}, "imbue_mod_duration": 3, "imbue_mini_rule": "all_statuses_true_damage", "blade_shape": "shifting"},
    {"id": "guard_break",            "name": "Guard Break",            "type": "strike",   "power_type": "strike",   "damage_type": "physical", "cooldown": 3, "damage": 6,  "skill_capacity_cost": 2, "trigger": "always",           "hits": 1, "cf_gain": 1, "strike_rule": "stance_break"},
    {"id": "rising_strike",          "name": "Rising Strike",          "type": "strike",   "power_type": "strike",   "damage_type": "physical", "cooldown": 3, "damage": 8,  "skill_capacity_cost": 2, "trigger": "always",           "hits": 1, "cf_gain": 1, "strike_rule": "launch"},
    {"id": "executioner_strike",     "name": "Executioner Strike",     "type": "strike",   "power_type": "strike",   "damage_type": "physical", "cooldown": 4, "damage": 12, "skill_capacity_cost": 3, "trigger": "always",           "hits": 1, "cf_gain": 0, "strike_rule": "cf_consumer"},
    {"id": "mutagen_injection",      "name": "Mutagen Injection",      "type": "cast",     "power_type": "buff",     "damage_type": "physical", "cooldown": 5, "damage": 0,  "skill_capacity_cost": 2, "trigger": "always",           "self_status": "inspired", "stat_mod": {"self": {"might": 4, "grace": 3, "durability": 2}}, "mod_duration": 3},
    {"id": "phoenix_mixture",        "name": "Phoenix Mixture",        "type": "cast",     "power_type": "defend",   "damage_type": "physical", "cooldown": 6, "damage": 25, "skill_capacity_cost": 2, "trigger": "low_hp",           "self_status": "warded", "heal_percent": 0.15, "stat_mod": {"self": {"armor_bonus": 4, "essence": 3, "durability": 2}}, "mod_duration": 3},
    {"id": "smoke_transmutation",    "name": "Smoke Transmutation",    "type": "cast",     "power_type": "defend",   "damage_type": "physical", "cooldown": 4, "damage": 0,  "skill_capacity_cost": 2, "trigger": "always",           "self_status": "hidden", "stat_mod": {"self": {"grace": 2}}, "mod_duration": 2},
    {"id": "spike_field",            "name": "Spike Field",            "type": "cast",     "power_type": "debuff",   "damage_type": "physical", "cooldown": 5, "damage": 5,  "skill_capacity_cost": 2, "trigger": "always",           "status_apply": "bleeding", "stat_mod": {"enemy": {"grace": -3, "might": -2}}, "mod_duration": 3},
    # Legendary Tier (Level 20)
    {"id": "philosophers_transmutation", "name": "Philosopher's Transmutation", "type": "cast",     "power_type": "heal",     "damage_type": "physical", "cooldown": 7, "damage": 40, "skill_capacity_cost": 3, "trigger": "low_hp",           "self_status": "inspired", "heal_percent": 0.30, "stat_mod": {"self": {"might": 3, "grace": 3, "essence": 3, "durability": 3, "insight": 3, "cognition": 3}}, "mod_duration": 4, "legendary_rule": "infinite_charges_max_mini_rules"},
    {"id": "legend_of_alchemy",      "name": "Legend of Alchemy",      "type": "strike",   "power_type": "strike",   "damage_type": "true",     "cooldown": 10,"damage": 15, "skill_capacity_cost": 3, "trigger": "low_hp",           "hits": 8, "cf_gain": 0, "strike_rule": "legendary_strike", "legendary_rule": "auto_adapt_katar", "self_status": "inspired", "heal_percent": 0.25, "status_apply": "stunned", "stat_mod": {"enemy": {"might": -6, "grace": -6, "armor_bonus": -8, "cognition": -5, "essence": -4, "insight": -4, "durability": -4}}, "mod_duration": 5},
    # --- Paladin Mastery: Divine Guardian --- (inverse_hp_scaling = True on all)
    # Basic Tier (Level 1)
    {"id": "shield_of_faith",       "name": "Shield of Faith",       "type": "paladin",       "power_type": "defend",  "trigger": "always",        "cooldown": 3, "damage": 0,  "skill_capacity_cost": 0, "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 3, "essence": 2}}, "mod_duration": 3, "inverse_hp_scaling": True},
    {"id": "blessed_strike",        "name": "Blessed Strike",        "type": "paladin",        "power_type": "strike",  "damage_type": "magical",  "trigger": "always",        "cooldown": 2, "damage": 8,  "skill_capacity_cost": 1, "status_apply": "shaken", "stat_mod": {"enemy": {"might": -2}}, "mod_duration": 2, "inverse_hp_scaling": True},
    {"id": "merciful_touch",        "name": "Merciful Touch",        "type": "paladin",        "power_type": "heal",    "trigger": "low_hp",       "cooldown": 4, "damage": 0,  "skill_capacity_cost": 1, "self_status": "warded", "heal_percent": 0.10, "stat_mod": {"self": {"essence": 2, "armor_bonus": 2}}, "mod_duration": 3, "inverse_hp_scaling": True},
    {"id": "hammer_of_light",       "name": "Hammer of Light",       "type": "paladin",       "power_type": "strike",  "damage_type": "physical", "trigger": "always",        "cooldown": 3, "damage": 10, "skill_capacity_cost": 1, "status_apply": "stunned", "stat_mod": {"enemy": {"armor_bonus": -2}}, "mod_duration": 2, "inverse_hp_scaling": True},
    {"id": "divine_aegis",          "name": "Divine Aegis",          "type": "paladin",          "power_type": "buff",    "trigger": "always",        "cooldown": 4, "damage": 0,  "skill_capacity_cost": 1, "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 3, "essence": 3, "durability": 2}}, "mod_duration": 3, "inverse_hp_scaling": True},
    {"id": "lightbearers_oath",     "name": "Lightbearer's Oath",     "type": "paladin",    "power_type": "buff",    "trigger": "opening_move",  "cooldown": 4, "damage": 0,  "skill_capacity_cost": 1, "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 2, "essence": 2, "durability": 2}}, "mod_duration": 3, "inverse_hp_scaling": True},
    # Advanced Tier (Level 3)
    {"id": "sacred_charge",         "name": "Sacred Charge",         "type": "paladin",         "power_type": "strike",  "damage_type": "physical", "trigger": "opening_move",  "cooldown": 3, "damage": 12, "skill_capacity_cost": 2, "status_apply": "stunned", "stat_mod": {"enemy": {"armor_bonus": -3, "might": -2}}, "mod_duration": 2, "inverse_hp_scaling": True},
    {"id": "judgment_hammer",        "name": "Judgment Hammer",        "type": "paladin",       "power_type": "strike",  "damage_type": "magical",  "trigger": "always",        "cooldown": 4, "damage": 14, "skill_capacity_cost": 2, "status_apply": "shaken", "stat_mod": {"enemy": {"might": -3, "essence": -2}}, "mod_duration": 3, "inverse_hp_scaling": True},
    {"id": "holy_barrier",          "name": "Holy Barrier",          "type": "paladin",          "power_type": "defend",  "trigger": "always",        "cooldown": 4, "damage": 0,  "skill_capacity_cost": 1, "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 4, "essence": 3}}, "mod_duration": 3, "inverse_hp_scaling": True},
    {"id": "consecrate_blade",      "name": "Consecrate Blade",      "type": "paladin",      "power_type": "buff",    "trigger": "always",        "cooldown": 5, "damage": 0,  "skill_capacity_cost": 2, "self_status": "warded", "stat_mod": {"self": {"essence": 3, "might": 2}}, "mod_duration": 4, "inverse_hp_scaling": True},
    {"id": "sunburst",               "name": "Sunburst",               "type": "paladin",               "power_type": "debuff",  "damage_type": "magical",  "trigger": "always",        "cooldown": 4, "damage": 6,  "skill_capacity_cost": 1, "status_apply": "blinded", "stat_mod": {"enemy": {"grace": -3}}, "mod_duration": 2, "inverse_hp_scaling": True},
    {"id": "divine_radiance",        "name": "Divine Radiance",        "type": "paladin",        "power_type": "heal",    "trigger": "low_hp",       "cooldown": 5, "damage": 0,  "skill_capacity_cost": 2, "self_status": "warded", "heal_percent": 0.12, "stat_mod": {"self": {"essence": 3, "armor_bonus": 3}}, "mod_duration": 3, "inverse_hp_scaling": True},
    {"id": "guardians_blessing",    "name": "Guardian's Blessing",    "type": "paladin",    "power_type": "buff",    "trigger": "always",        "cooldown": 5, "damage": 0,  "skill_capacity_cost": 2, "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 3, "essence": 3, "durability": 2}}, "mod_duration": 4, "inverse_hp_scaling": True},
    # Expert Tier (Level 8)
    {"id": "divine_intercession",   "name": "Divine Intercession",   "type": "paladin",   "power_type": "defend",  "trigger": "low_hp",       "cooldown": 5, "damage": 0,  "skill_capacity_cost": 1, "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 5, "essence": 4}}, "mod_duration": 3, "inverse_hp_scaling": True},
    {"id": "lay_on_hands_paladin",  "name": "Lay on Hands",          "type": "paladin",          "power_type": "heal",    "trigger": "low_hp",       "cooldown": 5, "damage": 0,  "skill_capacity_cost": 2, "self_status": "warded", "heal_percent": 0.15, "stat_mod": {"self": {"essence": 3, "durability": 2}}, "mod_duration": 3, "inverse_hp_scaling": True},
    {"id": "exorcism",               "name": "Exorcism",               "type": "paladin",               "power_type": "debuff",  "damage_type": "magical",  "trigger": "opponent_status","cooldown": 4, "damage": 8,  "skill_capacity_cost": 2, "status_apply": "shaken", "stat_mod": {"enemy": {"might": -4, "essence": -3}}, "mod_duration": 3, "inverse_hp_scaling": True},
    {"id": "celestial_spear",        "name": "Celestial Spear",        "type": "paladin",        "power_type": "strike",  "damage_type": "magical",  "trigger": "always",        "cooldown": 4, "damage": 16, "skill_capacity_cost": 2, "status_apply": "bleeding", "stat_mod": {"enemy": {"armor_bonus": -3, "essence": -2}}, "mod_duration": 3, "inverse_hp_scaling": True},
    {"id": "divine_resolve",         "name": "Divine Resolve",         "type": "paladin",         "power_type": "defend",  "trigger": "self_debuff",  "cooldown": 4, "damage": 0,  "skill_capacity_cost": 1, "self_status": "warded", "stat_mod": {"self": {"durability": 3, "essence": 3, "armor_bonus": 3}}, "mod_duration": 3, "inverse_hp_scaling": True},
    {"id": "faiths_bulwark",         "name": "Faith's Bulwark",        "type": "paladin",        "power_type": "buff",    "trigger": "always",        "cooldown": 5, "damage": 0,  "skill_capacity_cost": 2, "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 4, "essence": 4, "durability": 3}}, "mod_duration": 4, "inverse_hp_scaling": True},
    {"id": "last_stand",              "name": "Last Stand",              "type": "paladin",              "power_type": "heal",    "trigger": "low_hp",       "cooldown": 5, "damage": 0,  "skill_capacity_cost": 2, "self_status": "warded", "heal_percent": 0.20, "stat_mod": {"self": {"armor_bonus": 4, "essence": 4}}, "mod_duration": 3, "inverse_hp_scaling": True},
    # Master Tier (Level 15)
    {"id": "holy_nova",               "name": "Holy Nova",               "type": "paladin",               "power_type": "heal",    "trigger": "always",        "cooldown": 6, "damage": 0,  "skill_capacity_cost": 2, "self_status": "warded", "heal_percent": 0.15, "stat_mod": {"self": {"essence": 4, "armor_bonus": 3}}, "mod_duration": 4, "inverse_hp_scaling": True},
    {"id": "sanctuary",               "name": "Sanctuary",               "type": "paladin",               "power_type": "defend",  "trigger": "always",        "cooldown": 6, "damage": 0,  "skill_capacity_cost": 2, "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 5, "essence": 5, "durability": 3}}, "mod_duration": 4, "inverse_hp_scaling": True},
    {"id": "justice_descends",        "name": "Justice Descends",        "type": "paladin",        "power_type": "strike",  "damage_type": "magical",  "trigger": "opponent_wounded","cooldown": 5, "damage": 20, "skill_capacity_cost": 3, "status_apply": "stunned", "stat_mod": {"enemy": {"might": -4, "armor_bonus": -4, "essence": -3}}, "mod_duration": 3, "inverse_hp_scaling": True},
    {"id": "guardians_crown",         "name": "Guardian's Crown",        "type": "paladin",        "power_type": "buff",    "trigger": "always",        "cooldown": 6, "damage": 0,  "skill_capacity_cost": 3, "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 6, "essence": 5, "durability": 4}}, "mod_duration": 4, "inverse_hp_scaling": True},
    {"id": "resurrection_prayer",     "name": "Resurrection Prayer",     "type": "paladin",     "power_type": "heal",    "trigger": "low_hp",       "cooldown": 7, "damage": 0,  "skill_capacity_cost": 3, "self_status": "warded", "heal_percent": 0.35, "stat_mod": {"self": {"essence": 4, "armor_bonus": 4, "durability": 3}}, "mod_duration": 4, "inverse_hp_scaling": True},
    {"id": "consecrated_ground",      "name": "Consecrated Ground",      "type": "paladin",      "power_type": "buff",    "trigger": "always",        "cooldown": 6, "damage": 0,  "skill_capacity_cost": 3, "self_status": "warded", "heal_percent": 0.10, "stat_mod": {"self": {"armor_bonus": 4, "essence": 4, "durability": 3}}, "mod_duration": 4, "inverse_hp_scaling": True},
    {"id": "divine_wrath",            "name": "Divine Wrath",            "type": "paladin",            "power_type": "strike",  "damage_type": "physical", "trigger": "opponent_wounded","cooldown": 5, "damage": 22, "skill_capacity_cost": 3, "status_apply": "stunned", "stat_mod": {"enemy": {"armor_bonus": -5, "might": -4}}, "mod_duration": 3, "inverse_hp_scaling": True},
    {"id": "guardian_angel",          "name": "Guardian Angel",          "type": "paladin",          "power_type": "heal",    "trigger": "low_hp",       "cooldown": 6, "damage": 0,  "skill_capacity_cost": 3, "self_status": "warded", "heal_percent": 0.25, "stat_mod": {"self": {"armor_bonus": 5, "essence": 5, "durability": 3}}, "mod_duration": 4, "inverse_hp_scaling": True},
    # Legendary Tier (Level 20)
    {"id": "last_judgment",           "name": "Last Judgment",           "type": "paladin", "power_type": "strike",  "damage_type": "true",     "trigger": "opponent_wounded","cooldown": 8, "damage": 30, "skill_capacity_cost": 3, "status_apply": "stunned", "stat_mod": {"enemy": {"might": -5, "armor_bonus": -6, "essence": -5}}, "mod_duration": 4, "inverse_hp_scaling": True, "holy_bonus": True, "quest_req": "the_final_verdict"},
    {"id": "ascension_of_the_light",  "name": "Ascension of the Light",  "type": "paladin", "power_type": "strike",  "damage_type": "true",     "trigger": "low_hp",       "cooldown": 10,"damage": 35, "skill_capacity_cost": 3, "status_apply": "stunned", "stat_mod": {"enemy": {"might": -6, "armor_bonus": -8, "essence": -6}}, "mod_duration": 5, "self_status": "warded", "heal_percent": 0.30, "inverse_hp_scaling": True, "holy_bonus": True, "quest_req": "ascension_of_the_light_quest"},
    # --- Priest Mastery: The Holy Judge --- (sanctity_scaling on all, no power/skill_capacity_cost)
    # Basic Tier (Level 1) — 1 Heal, 1 Strike, 1 Buff, 1 Debuff, 1 Shield Wall, 1 Defend
    {"id": "swift_prayer",          "name": "Swift Prayer",          "type": "priest", "power_type": "heal",        "heal_type": "fast",    "trigger": "always",         "cooldown": 0, "target": "ally",  "heal_percent": 0.02},
    {"id": "light_barrier",         "name": "Light Barrier",         "type": "priest", "power_type": "shield_wall",                          "trigger": "always",         "cooldown": 3, "shield_hp": 0.20},
    {"id": "bless",                 "name": "Bless",                 "type": "priest", "power_type": "buff",                                 "trigger": "always",         "cooldown": 4, "self_status": "inspired", "stat_mod": {"self": {"insight": 2, "grace": 2}}, "mod_duration": 3},
    {"id": "holy_water",            "name": "Holy Water",            "type": "priest", "power_type": "strike",      "damage_type": "holy",  "trigger": "always",         "cooldown": 3, "status_apply": "burning", "stat_mod": {"enemy": {"might": -2}}, "mod_duration": 2},
    {"id": "blinding_light",        "name": "Blinding Light",        "type": "priest", "power_type": "debuff",      "damage_type": "holy",  "trigger": "always",         "cooldown": 4, "status_apply": "blind", "stat_mod": {"enemy": {"grace": -2}}, "mod_duration": 2},
    {"id": "soul_ward",             "name": "Soul Ward",            "type": "priest", "power_type": "defend",                               "trigger": "always",         "cooldown": 4, "self_status": "warded", "stat_mod": {"self": {"essence": 3, "armor_bonus": 2}}, "mod_duration": 3},
    # Advanced Tier (Level 3) — 1 Heal, 1 Strike, 1 Buff, 3 Debuffs, 1 Defend
    {"id": "blessing_of_renewal",   "name": "Blessing of Renewal",  "type": "priest", "power_type": "heal",        "heal_type": "hot",     "trigger": "always",         "cooldown": 5, "target": "ally",  "self_status": "inspired", "heal_percent": 0.10, "mod_duration": 3},
    {"id": "chain_of_light",        "name": "Chain of Light",        "type": "priest", "power_type": "debuff",      "damage_type": "holy",  "trigger": "always",         "cooldown": 5, "status_apply": "bind", "stat_mod": {"enemy": {"might": -3, "grace": -2}}, "mod_duration": 1},
    {"id": "cleansing_flame",       "name": "Cleansing Flame",      "type": "priest", "power_type": "debuff",      "damage_type": "holy",  "trigger": "opponent_status","cooldown": 4, "status_apply": "burning", "stat_mod": {"enemy": {"might": -3, "essence": -2}}, "mod_duration": 3},
    {"id": "angels_grace",          "name": "Angel's Grace",         "type": "priest", "power_type": "buff",                                 "trigger": "always",         "cooldown": 5, "self_status": "inspired", "stat_mod": {"self": {"grace": 3, "essence": 2, "durability": 2}}, "mod_duration": 3},
    {"id": "judgment_strike",       "name": "Judgment Strike",      "type": "priest", "power_type": "strike",      "damage_type": "holy",  "trigger": "always",         "cooldown": 4, "status_apply": "shaken", "stat_mod": {"enemy": {"grace": -3, "might": -2}}, "mod_duration": 3},
    {"id": "divine_rebuke",         "name": "Divine Rebuke",        "type": "priest", "power_type": "debuff",      "damage_type": "holy",  "trigger": "always",         "cooldown": 4, "status_apply": "shaken", "stat_mod": {"enemy": {"might": -3, "grace": -3, "cognition": -2}}, "mod_duration": 3},
    {"id": "light_of_hope",         "name": "Light of Hope",        "type": "priest", "power_type": "defend",                               "trigger": "self_debuff",    "cooldown": 4, "self_status": "warded", "stat_mod": {"self": {"essence": 2, "grace": 2}}, "mod_duration": 3},
    # Expert Tier (Level 8) — 1 Heal, 1 Strike, 1 Buff, 2 Debuffs, 1 Shield Wall, 1 Defend
    {"id": "divine_light_priest",   "name": "Divine Light",         "type": "priest", "power_type": "heal",        "heal_type": "normal",  "trigger": "always",         "cooldown": 0, "target": "ally",  "self_status": "warded", "heal_percent": 0.20, "stat_mod": {"self": {"essence": 3, "durability": 2}}, "mod_duration": 3},
    {"id": "mass_purify",           "name": "Mass Purify",          "type": "priest", "power_type": "defend",                               "trigger": "self_debuff",    "cooldown": 5, "self_status": "warded", "stat_mod": {"self": {"essence": 3, "durability": 2}}, "mod_duration": 3},
    {"id": "heavens_judgment",      "name": "Heaven's Judgment",    "type": "priest", "power_type": "strike",      "damage_type": "holy",  "trigger": "always",         "cooldown": 5, "status_apply": "shaken", "stat_mod": {"enemy": {"might": -3, "grace": -3, "armor_bonus": -2}}, "mod_duration": 3},
    {"id": "radiant_prison",        "name": "Radiant Prison",       "type": "priest", "power_type": "debuff",      "damage_type": "holy",  "trigger": "always",         "cooldown": 6, "status_apply": "bind", "stat_mod": {"enemy": {"grace": -3, "might": -2}}, "mod_duration": 2},
    {"id": "beacon_of_faith",       "name": "Beacon of Faith",      "type": "priest", "power_type": "buff",                                 "trigger": "always",         "cooldown": 5, "self_status": "inspired", "heal_percent": 0.08, "stat_mod": {"self": {"essence": 4, "cognition": 2}}, "mod_duration": 4},
    {"id": "sunflare",              "name": "Sunflare",             "type": "priest", "power_type": "debuff",      "damage_type": "holy",  "trigger": "always",         "cooldown": 6, "status_apply": "blind", "stat_mod": {"enemy": {"might": -3, "grace": -3}}, "mod_duration": 3},
    {"id": "radiant_bulwark",       "name": "Radiant Bulwark",      "type": "priest", "power_type": "shield_wall",                          "trigger": "always",         "cooldown": 6, "shield_hp": 0.35, "status_apply": "blind", "self_status": "warded"},
    # Master Tier (Level 15) — 1 Shield Wall, 1 Strike, 2 Heals, 1 Debuff, 3 Buffs
    {"id": "sanctuary_priest",      "name": "Sanctuary",            "type": "priest", "power_type": "shield_wall",                          "trigger": "always",         "cooldown": 6, "shield_hp": 0.50, "self_status": "warded", "stat_mod": {"self": {"essence": 4, "durability": 3}}, "mod_duration": 4},
    {"id": "holy_lance",            "name": "Holy Lance",           "type": "priest", "power_type": "strike",      "damage_type": "holy",  "trigger": "always",         "cooldown": 6, "status_apply": "bleeding", "stat_mod": {"enemy": {"might": -4, "armor_bonus": -3}}, "mod_duration": 3},
    {"id": "promise_of_heaven",    "name": "Promise of Heaven",    "type": "priest", "power_type": "heal",        "heal_type": "delayed", "trigger": "always",         "cooldown": 7, "target": "ally",  "self_status": "inspired", "heal_percent": 0.35, "mod_duration": 2},
    {"id": "hymn_of_salvation",     "name": "Hymn of Salvation",   "type": "priest", "power_type": "heal",        "heal_type": "group",   "trigger": "always",         "cooldown": 7, "target": "all_allies", "self_status": "inspired", "heal_percent": 0.15, "stat_mod": {"self": {"essence": 4, "durability": 3}}, "mod_duration": 3},
    {"id": "final_judgment",        "name": "Final Judgment",       "type": "priest", "power_type": "debuff",      "damage_type": "holy",  "trigger": "opponent_wounded","cooldown": 8, "status_apply": ["bind", "blind"], "stat_mod": {"enemy": {"might": -5, "grace": -5, "essence": -3}}, "mod_duration": 3},
    {"id": "holy_revelation",       "name": "Holy Revelation",      "type": "priest", "power_type": "buff",                                 "trigger": "always",         "cooldown": 6, "self_status": "inspired", "stat_mod": {"self": {"cognition": 4, "insight": 3, "essence": 2}}, "mod_duration": 4},
    {"id": "prayer_circle",         "name": "Prayer Circle",        "type": "priest", "power_type": "buff",                                 "trigger": "always",         "cooldown": 6, "self_status": "inspired", "heal_percent": 0.10, "stat_mod": {"self": {"insight": 3, "grace": 3, "essence": 3, "cognition": 2}}, "mod_duration": 4},
    {"id": "divine_covenant",       "name": "Divine Covenant",      "type": "priest", "power_type": "buff",                                 "trigger": "always",         "cooldown": 6, "self_status": "inspired", "heal_percent": 0.12, "stat_mod": {"self": {"insight": 4, "essence": 4, "grace": 3, "durability": 2}}, "mod_duration": 4},
    # Legendary Tier (Level 20) — 2 Holy True-Damage Strikes (Quest-gated)
    {"id": "choir_of_heaven",       "name": "Choir of Heaven",      "type": "priest", "power_type": "strike",      "damage_type": "true",  "trigger": "always",         "cooldown": 8, "status_apply": "stunned", "self_status": "inspired", "heal_percent": 0.15, "stat_mod": {"enemy": {"might": -5, "grace": -5, "armor_bonus": -6, "essence": -4, "cognition": -3}}, "mod_duration": 4, "quest_req": "the_celestial_choir"},
    {"id": "legend_of_the_faithful","name": "Legend of the Faithful","type": "priest","power_type": "strike",      "damage_type": "true",  "trigger": "low_hp",        "cooldown": 10, "status_apply": ["stunned", "blind"], "self_status": "inspired", "heal_percent": 0.25, "stat_mod": {"enemy": {"might": -6, "grace": -6, "armor_bonus": -8, "essence": -5, "cognition": -4, "durability": -4}}, "mod_duration": 5, "quest_req": "legend_of_the_faithful_quest"},
    # --- Knight Mastery: The Oathbound --- (type="knight" preserves mastery_req)
    # Basic Tier (Level 1) — 4 Buffs, 2 Strikes (shield_bash already exists)
    {"id": "iron_stance",       "name": "Iron Stance",       "type": "knight", "power_type": "buff",    "trigger": "always",       "cooldown": 3, "damage": 0,  "skill_capacity_cost": 1, "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 2, "might": 2}}, "mod_duration": 3},
    {"id": "war_cry",           "name": "War Cry",           "type": "knight", "power_type": "buff",    "trigger": "opening_move", "cooldown": 4, "damage": 0,  "skill_capacity_cost": 1, "self_status": "warded", "stat_mod": {"self": {"might": 3}}, "mod_duration": 3},
    {"id": "vanguard_step",     "name": "Vanguard Step",     "type": "knight", "power_type": "buff",    "trigger": "always",       "cooldown": 3, "damage": 0,  "skill_capacity_cost": 1, "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 3}}, "mod_duration": 3},
    {"id": "pommel_strike",     "name": "Pommel Strike",     "type": "knight", "power_type": "strike",  "damage_type": "physical", "trigger": "always",       "cooldown": 2, "damage": 5,  "skill_capacity_cost": 1, "status_apply": "stunned", "stat_mod": {"enemy": {"might": -2, "grace": -1}}, "mod_duration": 2},
    {"id": "steady_grip",       "name": "Steady Grip",       "type": "knight", "power_type": "buff",    "trigger": "always",       "cooldown": 3, "damage": 0,  "skill_capacity_cost": 1, "self_status": "warded", "stat_mod": {"self": {"might": 2, "armor_bonus": 2}}, "mod_duration": 3},
    # Advanced Tier (Level 3) — 3 Buffs, 3 Strikes, 1 Debuff
    {"id": "kings_challenge",   "name": "King's Challenge",  "type": "knight", "power_type": "debuff",  "damage_type": "physical", "trigger": "always",       "cooldown": 4, "damage": 4,  "skill_capacity_cost": 1, "status_apply": "shaken", "stat_mod": {"enemy": {"might": -3}}, "mod_duration": 3},
    {"id": "lions_charge",      "name": "Lion's Charge",     "type": "knight", "power_type": "strike",  "damage_type": "physical", "trigger": "opening_move",  "cooldown": 3, "damage": 8,  "skill_capacity_cost": 2, "status_apply": "stunned", "stat_mod": {"enemy": {"armor_bonus": -3}}, "mod_duration": 2},
    {"id": "heavy_strike",      "name": "Heavy Strike",      "type": "knight", "power_type": "strike",  "damage_type": "physical", "trigger": "always",       "cooldown": 3, "damage": 9,  "skill_capacity_cost": 2, "status_apply": "shaken", "stat_mod": {"enemy": {"armor_bonus": -3}}, "mod_duration": 3},
    {"id": "bulwark",           "name": "Bulwark",           "type": "knight", "power_type": "buff",    "trigger": "always",       "cooldown": 5, "damage": 0,  "skill_capacity_cost": 2, "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 4, "might": 3}}, "mod_duration": 4},
    {"id": "banner_of_valor",  "name": "Banner of Valor",   "type": "knight", "power_type": "buff",    "trigger": "always",       "cooldown": 5, "damage": 0,  "skill_capacity_cost": 2, "self_status": "warded", "stat_mod": {"self": {"might": 3, "armor_bonus": 2}}, "mod_duration": 4},
    {"id": "fortress_breaker",  "name": "Fortress Breaker",  "type": "knight", "power_type": "strike",  "damage_type": "physical", "trigger": "always",       "cooldown": 4, "damage": 10, "skill_capacity_cost": 2, "status_apply": "bleeding", "stat_mod": {"enemy": {"armor_bonus": -4}}, "mod_duration": 3},
    {"id": "plate_armor_mastery","name": "Plate Armor Mastery","type": "knight", "power_type": "buff",   "trigger": "always",       "cooldown": 5, "damage": 0,  "skill_capacity_cost": 2, "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 5, "durability": 3}}, "mod_duration": 4},
    # Expert Tier (Level 8) — 2 Buffs, 2 Strikes, 3 Defends
    {"id": "shield_wall",       "name": "Shield Wall",       "type": "knight", "power_type": "defend",  "trigger": "always",       "cooldown": 5, "damage": 0,  "skill_capacity_cost": 1, "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 5, "durability": 2}}, "mod_duration": 4},
    {"id": "guardians_sacrifice","name": "Guardian's Sacrifice","type":"knight", "power_type":"defend",  "trigger": "low_hp",       "cooldown": 5, "damage": 0,  "skill_capacity_cost": 1, "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 5, "might": 3}}, "mod_duration": 3},
    {"id": "commanding_presence","name": "Commanding Presence","type":"knight", "power_type":"buff",    "trigger": "always",       "cooldown": 5, "damage": 0,  "skill_capacity_cost": 2, "self_status": "warded", "stat_mod": {"self": {"might": 4, "armor_bonus": 3}}, "mod_duration": 4},
    {"id": "crushing_blow",     "name": "Crushing Blow",     "type": "knight", "power_type": "strike",  "damage_type": "physical", "trigger": "opponent_wounded","cooldown": 4, "damage": 14, "skill_capacity_cost": 2, "status_apply": "shaken", "stat_mod": {"enemy": {"armor_bonus": -5, "might": -3}}, "mod_duration": 3},
    {"id": "unbreakable_will",  "name": "Unbreakable Will",  "type": "knight", "power_type": "defend",  "trigger": "self_debuff",  "cooldown": 4, "damage": 0,  "skill_capacity_cost": 1, "self_status": "warded", "stat_mod": {"self": {"durability": 3, "armor_bonus": 3}}, "mod_duration": 3},
    {"id": "titans_strength",   "name": "Titan's Strength",  "type": "knight", "power_type": "buff",    "trigger": "always",       "cooldown": 5, "damage": 0,  "skill_capacity_cost": 2, "self_status": "warded", "stat_mod": {"self": {"might": 5, "armor_bonus": 2}}, "mod_duration": 4},
    {"id": "ground_slam",       "name": "Ground Slam",       "type": "knight", "power_type": "strike",  "damage_type": "physical", "trigger": "always",       "cooldown": 4, "damage": 12, "skill_capacity_cost": 2, "status_apply": "stunned", "stat_mod": {"enemy": {"might": -3, "armor_bonus": -3}}, "mod_duration": 3},
    # Master Tier (Level 15) — 4 Buffs, 2 Strikes, 2 Defends
    {"id": "iron_formation",    "name": "Iron Formation",    "type": "knight", "power_type": "defend",  "trigger": "always",       "cooldown": 6, "damage": 0,  "skill_capacity_cost": 2, "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 8, "durability": 4}}, "mod_duration": 4},
    {"id": "royal_execution",   "name": "Royal Execution",   "type": "knight", "power_type": "strike",  "damage_type": "physical", "trigger": "opponent_wounded","cooldown": 5, "damage": 18, "skill_capacity_cost": 3, "status_apply": "bleeding", "stat_mod": {"enemy": {"might": -4, "armor_bonus": -3}}, "mod_duration": 3},
    {"id": "guardians_oath",    "name": "Guardian's Oath",   "type": "knight", "power_type": "buff",    "trigger": "always",       "cooldown": 6, "damage": 0,  "skill_capacity_cost": 3, "self_status": "warded", "stat_mod": {"self": {"might": 4, "armor_bonus": 4, "durability": 3}}, "mod_duration": 4},
    {"id": "warlords_fury",     "name": "Warlord's Fury",    "type": "knight", "power_type": "buff",    "trigger": "low_hp",       "cooldown": 6, "damage": 0,  "skill_capacity_cost": 3, "self_status": "warded", "stat_mod": {"self": {"might": 6, "armor_bonus": 3}}, "mod_duration": 4},
    {"id": "crown_of_iron",    "name": "Crown of Iron",     "type": "knight", "power_type": "buff",    "trigger": "always",       "cooldown": 6, "damage": 0,  "skill_capacity_cost": 3, "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 6, "might": 4, "durability": 3}}, "mod_duration": 4},
    {"id": "kings_command",    "name": "King's Command",    "type": "knight", "power_type": "buff",    "trigger": "always",       "cooldown": 6, "damage": 0,  "skill_capacity_cost": 3, "self_status": "warded", "stat_mod": {"self": {"might": 5, "armor_bonus": 3, "durability": 2}}, "mod_duration": 4},
    {"id": "last_bastion",     "name": "Last Bastion",      "type": "knight", "power_type": "defend",  "trigger": "low_hp",       "cooldown": 7, "damage": 0,  "skill_capacity_cost": 2, "self_status": "warded", "stat_mod": {"self": {"armor_bonus": 7, "durability": 5, "might": 3}}, "mod_duration": 4},
    {"id": "oath_strike",      "name": "Oath Strike",       "type": "knight", "power_type": "strike",  "damage_type": "physical", "trigger": "always",       "cooldown": 4, "damage": 16, "skill_capacity_cost": 3, "status_apply": "bleeding", "stat_mod": {"enemy": {"might": -3, "armor_bonus": -3, "grace": -2}}, "mod_duration": 3},
    # Legendary Tier (Level 20) — 2 Strikes
    {"id": "final_duel",       "name": "Final Duel",        "type": "knight", "power_type": "strike",  "damage_type": "true",     "trigger": "always",       "cooldown": 8, "damage": 25, "skill_capacity_cost": 3, "status_apply": "bleeding", "stat_mod": {"enemy": {"might": -5, "grace": -5, "armor_bonus": -5}}, "mod_duration": 4, "quest_req": "the_broken_oath"},
    {"id": "legend_of_erchis", "name": "Legend of Erchis",  "type": "knight", "power_type": "strike",  "damage_type": "true",     "trigger": "low_hp",       "cooldown": 10,"damage": 30, "skill_capacity_cost": 3, "status_apply": "stunned", "stat_mod": {"enemy": {"might": -6, "grace": -6, "armor_bonus": -8, "durability": -4}}, "mod_duration": 5, "self_status": "warded", "quest_req": "legend_of_erchis_quest"},
    # --- Lancer Mastery: The Elemental Lance Master --- (type="lancer" preserves mastery_req)
    # Basic Tier (Level 1) — 2 Imbues, 2 Strikes, 1 Defend, 1 Buff
    {"id": "flame_imbue",       "name": "Flame Imbue",       "type": "lancer", "power_type": "buff",    "trigger": "always",       "cooldown": 3, "damage": 0,  "skill_capacity_cost": 1, "stat_mod": {"self": {"might": 2}}, "mod_duration": 3, "element": "fire"},
    {"id": "frost_imbue",       "name": "Frost Imbue",       "type": "lancer", "power_type": "buff",    "trigger": "always",       "cooldown": 3, "damage": 0,  "skill_capacity_cost": 1, "stat_mod": {"self": {"might": 2, "grace": 1}, "enemy": {"grace": -2}}, "mod_duration": 3, "element": "ice"},
    {"id": "gale_thrust",       "name": "Gale Thrust",       "type": "lancer", "power_type": "strike",  "damage_type": "physical", "trigger": "always",       "cooldown": 1, "damage": 6,  "skill_capacity_cost": 1, "stat_mod": {"enemy": {"grace": -1}}, "mod_duration": 2},
    {"id": "lancer_guard_break","name": "Guard Break",       "type": "lancer", "power_type": "strike",  "damage_type": "physical", "trigger": "always",       "cooldown": 3, "damage": 7,  "skill_capacity_cost": 1, "stat_mod": {"enemy": {"armor_bonus": -3}}, "mod_duration": 2},
    {"id": "cyclone_wall",      "name": "Cyclone Wall",      "type": "lancer", "power_type": "defend",  "trigger": "always",       "cooldown": 3, "damage": 0,  "skill_capacity_cost": 1, "self_status": "evasive", "stat_mod": {"self": {"grace": 2}}, "mod_duration": 2},
    {"id": "warriors_focus",    "name": "Warrior's Focus",   "type": "lancer", "power_type": "buff",    "trigger": "always",       "cooldown": 3, "damage": 0,  "skill_capacity_cost": 1, "stat_mod": {"self": {"grace": 2, "might": 2}}, "mod_duration": 3},
    # Advanced Tier (Level 3) — 2 Imbues, 3 Strikes, 1 Debuff, 1 Buff
    {"id": "storm_imbue",       "name": "Storm Imbue",       "type": "lancer", "power_type": "buff",    "trigger": "always",       "cooldown": 4, "damage": 0,  "skill_capacity_cost": 2, "stat_mod": {"self": {"might": 3, "grace": 2}}, "mod_duration": 3, "element": "lightning"},
    {"id": "stone_imbue",       "name": "Stone Imbue",       "type": "lancer", "power_type": "buff",    "trigger": "always",       "cooldown": 4, "damage": 0,  "skill_capacity_cost": 2, "stat_mod": {"self": {"might": 3, "armor_bonus": 2}, "enemy": {"armor_bonus": -2}}, "mod_duration": 3, "element": "earth"},
    {"id": "sky_piercer",       "name": "Sky Piercer",       "type": "lancer", "power_type": "strike",  "damage_type": "physical", "trigger": "always",       "cooldown": 3, "damage": 10, "skill_capacity_cost": 2, "status_apply": "bleeding", "stat_mod": {"enemy": {"armor_bonus": -4}}, "mod_duration": 3},
    {"id": "falcon_rush",       "name": "Falcon Rush",       "type": "lancer", "power_type": "strike",  "damage_type": "physical", "trigger": "opening_move",  "cooldown": 3, "damage": 9,  "skill_capacity_cost": 2, "status_apply": "stunned", "stat_mod": {"enemy": {"grace": -2}}, "mod_duration": 2},
    {"id": "dragon_fang",       "name": "Dragon Fang",       "type": "lancer", "power_type": "strike",  "damage_type": "physical", "trigger": "always",       "cooldown": 4, "damage": 11, "skill_capacity_cost": 2, "status_apply": "bleeding", "stat_mod": {"enemy": {"armor_bonus": -3, "might": -2}}, "mod_duration": 3},
    {"id": "elemental_weakness","name": "Elemental Weakness","type": "lancer", "power_type": "debuff",  "damage_type": "magical",  "trigger": "always",       "cooldown": 4, "damage": 5,  "skill_capacity_cost": 2, "stat_mod": {"enemy": {"might": -3, "grace": -3, "armor_bonus": -2}}, "mod_duration": 3},
    {"id": "battle_readiness",  "name": "Battle Readiness",  "type": "lancer", "power_type": "buff",    "trigger": "opening_move", "cooldown": 4, "damage": 0,  "skill_capacity_cost": 2, "self_status": "evasive", "stat_mod": {"self": {"grace": 3, "might": 2}}, "mod_duration": 3},
    # Expert Tier (Level 8) — 2 Imbues, 1 Strike, 1 Defend, 2 Debuffs, 1 Buff
    {"id": "gale_imbue",        "name": "Gale Imbue",        "type": "lancer", "power_type": "buff",    "trigger": "always",       "cooldown": 4, "damage": 0,  "skill_capacity_cost": 2, "self_status": "evasive", "stat_mod": {"self": {"grace": 4, "might": 2}}, "mod_duration": 3, "element": "wind"},
    {"id": "thunder_imbue",     "name": "Thunder Imbue",     "type": "lancer", "power_type": "buff",    "trigger": "always",       "cooldown": 5, "damage": 0,  "skill_capacity_cost": 2, "stat_mod": {"self": {"insight": 4, "might": 2}, "enemy": {"essence": -2}}, "mod_duration": 3, "element": "thunder"},
    {"id": "dragon_dive",       "name": "Dragon Dive",       "type": "lancer", "power_type": "strike",  "damage_type": "physical", "trigger": "opening_move",  "cooldown": 4, "damage": 14, "skill_capacity_cost": 2, "status_apply": "stunned", "stat_mod": {"enemy": {"armor_bonus": -4, "might": -2}}, "mod_duration": 2},
    {"id": "frostbite",         "name": "Frostbite",         "type": "lancer", "power_type": "debuff",  "damage_type": "magical",  "trigger": "opponent_status","cooldown": 4, "damage": 6,  "skill_capacity_cost": 2, "status_apply": "ensnared", "stat_mod": {"enemy": {"grace": -4, "might": -3}}, "mod_duration": 3},
    {"id": "shock_lock",        "name": "Shock Lock",        "type": "lancer", "power_type": "debuff",  "damage_type": "magical",  "trigger": "opponent_status","cooldown": 4, "damage": 6,  "skill_capacity_cost": 2, "status_apply": "stunned", "stat_mod": {"enemy": {"might": -4, "grace": -3}}, "mod_duration": 3},
    {"id": "iron_breeze",       "name": "Iron Breeze",       "type": "lancer", "power_type": "defend",  "trigger": "always",       "cooldown": 4, "damage": 0,  "skill_capacity_cost": 1, "self_status": "evasive", "stat_mod": {"self": {"grace": 3, "armor_bonus": 2}}, "mod_duration": 2},
    {"id": "elemental_surge",   "name": "Elemental Surge",   "type": "lancer", "power_type": "buff",    "trigger": "always",       "cooldown": 5, "damage": 0,  "skill_capacity_cost": 2, "self_status": "evasive", "stat_mod": {"self": {"grace": 3, "insight": 3, "might": 2}}, "mod_duration": 3},
    # Master Tier (Level 15) — 4 Imbues, 3 Strikes, 1 Debuff
    {"id": "inferno_imbue",     "name": "Inferno Imbue",     "type": "lancer", "power_type": "buff",    "trigger": "always",       "cooldown": 5, "damage": 0,  "skill_capacity_cost": 3, "stat_mod": {"self": {"might": 5, "grace": 2}, "enemy": {"armor_bonus": -3}}, "mod_duration": 4, "element": "fire"},
    {"id": "glacier_imbue",     "name": "Glacier Imbue",     "type": "lancer", "power_type": "buff",    "trigger": "always",       "cooldown": 5, "damage": 0,  "skill_capacity_cost": 3, "stat_mod": {"self": {"might": 4, "grace": 3}, "enemy": {"grace": -4, "might": -2}}, "mod_duration": 4, "element": "ice"},
    {"id": "tempest_imbue",     "name": "Tempest Imbue",     "type": "lancer", "power_type": "buff",    "trigger": "always",       "cooldown": 5, "damage": 0,  "skill_capacity_cost": 3, "stat_mod": {"self": {"might": 5, "grace": 3}, "enemy": {"might": -3, "grace": -3}}, "mod_duration": 4, "element": "lightning"},
    {"id": "volcano_imbue",     "name": "Volcano Imbue",     "type": "lancer", "power_type": "buff",    "trigger": "always",       "cooldown": 6, "damage": 0,  "skill_capacity_cost": 3, "stat_mod": {"self": {"might": 5, "armor_bonus": 3}, "enemy": {"armor_bonus": -4, "might": -3}}, "mod_duration": 4, "element": "fire_earth"},
    {"id": "thunder_pursuit",   "name": "Thunder Pursuit",  "type": "lancer", "power_type": "strike",  "damage_type": "magical",  "trigger": "opponent_wounded","cooldown": 4, "damage": 16, "skill_capacity_cost": 3, "status_apply": "stunned", "stat_mod": {"enemy": {"grace": -3, "might": -3}}, "mod_duration": 3},
    {"id": "world_splitter",    "name": "World Splitter",   "type": "lancer", "power_type": "strike",  "damage_type": "physical", "trigger": "opponent_wounded","cooldown": 6, "damage": 20, "skill_capacity_cost": 3, "status_apply": "stunned", "stat_mod": {"enemy": {"armor_bonus": -6, "might": -3}}, "mod_duration": 3},
    {"id": "crimson_spear",     "name": "Crimson Spear",    "type": "lancer", "power_type": "strike",  "damage_type": "physical", "trigger": "low_hp",       "cooldown": 5, "damage": 18, "skill_capacity_cost": 3, "status_apply": "bleeding", "stat_mod": {"self": {"might": 5}, "enemy": {"armor_bonus": -4, "might": -3}}, "mod_duration": 3},
    {"id": "elemental_collapse","name": "Elemental Collapse","type": "lancer", "power_type": "debuff",  "damage_type": "magical",  "trigger": "opponent_wounded","cooldown": 6, "damage": 8,  "skill_capacity_cost": 3, "stat_mod": {"enemy": {"might": -5, "grace": -5, "armor_bonus": -4, "essence": -3}}, "mod_duration": 4},
    # Legendary Tier (Level 20) — 2 True-Damage Strikes
    {"id": "celestial_javelin", "name": "Celestial Javelin","type": "lancer", "power_type": "strike",  "damage_type": "true",     "trigger": "always",       "cooldown": 8, "damage": 25, "skill_capacity_cost": 3, "status_apply": "bleeding", "stat_mod": {"enemy": {"might": -5, "grace": -5, "armor_bonus": -6}}, "mod_duration": 4, "quest_req": "the_spear_that_pierced_heaven"},
    {"id": "avatar_of_the_storm","name": "Avatar of the Storm","type":"lancer","power_type": "strike",  "damage_type": "true",     "trigger": "low_hp",       "cooldown": 10,"damage": 30, "skill_capacity_cost": 3, "status_apply": "stunned", "stat_mod": {"enemy": {"might": -6, "grace": -6, "armor_bonus": -8, "essence": -4}}, "mod_duration": 5, "self_status": "evasive", "quest_req": "avatar_of_the_storm_quest"},
    # --- Mage Mastery: The Architect --- (type="mage" preserves mastery_req)
    # Basic Tier (Level 1) — 4 Strikes, 1 Defend, 1 Buff
    {"id": "arcane_burst",      "name": "Arcane Burst",      "type": "mage", "power_type": "strike",  "damage_type": "magical", "trigger": "always",       "cooldown": 2, "damage": 6,  "skill_capacity_cost": 1, "stat_mod": {"enemy": {"grace": -1}}, "mod_duration": 2, "spell_tags": ["Strike", "Single-Target", "Projectile"]},
    {"id": "wind_blade",        "name": "Wind Blade",        "type": "mage", "power_type": "strike",  "damage_type": "magical", "trigger": "always",       "cooldown": 2, "damage": 7,  "skill_capacity_cost": 1, "status_apply": "bleeding", "stat_mod": {"enemy": {"grace": -2}}, "mod_duration": 2, "spell_tags": ["Strike", "Single-Target", "Wind"]},
    {"id": "stone_spear",       "name": "Stone Spear",       "type": "mage", "power_type": "strike",  "damage_type": "physical","trigger": "always",       "cooldown": 3, "damage": 8,  "skill_capacity_cost": 1, "status_apply": "bleeding", "stat_mod": {"enemy": {"armor_bonus": -2}}, "mod_duration": 2, "spell_tags": ["Strike", "Single-Target", "Stone"]},
    {"id": "arcane_ward",       "name": "Arcane Ward",       "type": "mage", "power_type": "defend",                            "trigger": "always",       "cooldown": 4, "damage": 0,  "skill_capacity_cost": 1, "self_status": "warded", "stat_mod": {"self": {"essence": 3}}, "mod_duration": 3, "spell_tags": ["Defend"]},
    {"id": "blink",             "name": "Blink",             "type": "mage", "power_type": "buff",                              "trigger": "always",       "cooldown": 3, "damage": 0,  "skill_capacity_cost": 1, "self_status": "evasive", "stat_mod": {"self": {"grace": 4}}, "mod_duration": 2, "spell_tags": ["Buff", "Teleport"]},
    {"id": "water_lash",        "name": "Water Lash",        "type": "mage", "power_type": "strike",  "damage_type": "magical", "trigger": "always",       "cooldown": 3, "damage": 8,  "skill_capacity_cost": 1, "status_apply": "stunned", "stat_mod": {"enemy": {"grace": -2}}, "mod_duration": 2, "spell_tags": ["Strike", "Single-Target"]},
    # Advanced Tier (Level 3) — 2 Strikes, 3 Debuffs, 1 Defend, 1 Buff
    {"id": "fireball",          "name": "Fireball",          "type": "mage", "power_type": "strike",  "damage_type": "magical", "trigger": "always",       "cooldown": 3, "damage": 10, "skill_capacity_cost": 2, "status_apply": "burning", "stat_mod": {"enemy": {"armor_bonus": -3}}, "mod_duration": 3, "spell_tags": ["Strike", "Single-Target", "Fire", "Explosion"]},
    {"id": "frost_prison",      "name": "Frost Prison",      "type": "mage", "power_type": "debuff",  "damage_type": "magical", "trigger": "always",       "cooldown": 4, "damage": 4,  "skill_capacity_cost": 2, "status_apply": "ensnared", "stat_mod": {"enemy": {"grace": -3, "might": -2}}, "mod_duration": 3, "spell_tags": ["Debuff", "Single-Target", "Ice"]},
    {"id": "chain_lightning",   "name": "Chain Lightning",   "type": "mage", "power_type": "strike",  "damage_type": "magical", "trigger": "always",       "cooldown": 4, "damage": 9,  "skill_capacity_cost": 2, "hits": 2, "status_apply": "stunned", "stat_mod": {"enemy": {"grace": -2}}, "mod_duration": 2, "spell_tags": ["Strike", "Lightning"]},
    {"id": "mana_shield",       "name": "Mana Shield",       "type": "mage", "power_type": "defend",                            "trigger": "always",       "cooldown": 4, "damage": 0,  "skill_capacity_cost": 2, "self_status": "warded", "stat_mod": {"self": {"essence": 4, "armor_bonus": 2}}, "mod_duration": 3, "spell_tags": ["Defend"]},
    {"id": "spell_seal",        "name": "Spell Seal",        "type": "mage", "power_type": "debuff",  "damage_type": "magical", "trigger": "always",       "cooldown": 4, "damage": 3,  "skill_capacity_cost": 2, "status_apply": "shaken", "stat_mod": {"enemy": {"insight": -4, "cognition": -3, "might": -2}}, "mod_duration": 3, "spell_tags": ["Debuff", "Single-Target"]},
    {"id": "arcane_chains",     "name": "Arcane Chains",     "type": "mage", "power_type": "debuff",  "damage_type": "magical", "trigger": "opponent_status","cooldown": 4, "damage": 3,  "skill_capacity_cost": 2, "status_apply": "ensnared", "stat_mod": {"enemy": {"grace": -3, "might": -3}}, "mod_duration": 3, "spell_tags": ["Debuff", "Single-Target"]},
    {"id": "illusory_double",   "name": "Illusory Double",   "type": "mage", "power_type": "buff",                              "trigger": "always",       "cooldown": 5, "damage": 0,  "skill_capacity_cost": 2, "self_status": "evasive", "stat_mod": {"self": {"grace": 5}}, "mod_duration": 3, "spell_tags": ["Buff", "Illusion"]},
    # Expert Tier (Level 8) — 1 Strike, 3 Debuffs, 1 Defend, 2 Buffs
    {"id": "gravity_well",      "name": "Gravity Well",      "type": "mage", "power_type": "debuff",  "damage_type": "magical", "trigger": "always",       "cooldown": 5, "damage": 5,  "skill_capacity_cost": 2, "status_apply": "ensnared", "stat_mod": {"enemy": {"grace": -4, "might": -3, "cognition": -2}}, "mod_duration": 3, "spell_tags": ["Debuff", "Single-Target"]},
    {"id": "telekinetic_crush", "name": "Telekinetic Crush", "type": "mage", "power_type": "strike",  "damage_type": "magical", "trigger": "opponent_wounded","cooldown": 5, "damage": 14, "skill_capacity_cost": 3, "status_apply": "stunned", "stat_mod": {"enemy": {"might": -4, "armor_bonus": -3}}, "mod_duration": 3, "spell_tags": ["Strike", "Single-Target"]},
    {"id": "mirror_spell",      "name": "Mirror Spell",      "type": "mage", "power_type": "defend",                            "trigger": "always",       "cooldown": 5, "damage": 0,  "skill_capacity_cost": 2, "self_status": "warded", "stat_mod": {"self": {"essence": 4, "grace": 2}}, "mod_duration": 3, "spell_tags": ["Defend"]},
    {"id": "mind_maze",         "name": "Mind Maze",         "type": "mage", "power_type": "debuff",  "damage_type": "magical", "trigger": "opponent_status","cooldown": 5, "damage": 4,  "skill_capacity_cost": 2, "status_apply": "shaken", "stat_mod": {"enemy": {"cognition": -5, "grace": -3, "might": -2}}, "mod_duration": 3, "spell_tags": ["Debuff", "Single-Target", "Illusion"]},
    {"id": "void_portal",       "name": "Void Portal",       "type": "mage", "power_type": "buff",                              "trigger": "always",       "cooldown": 5, "damage": 0,  "skill_capacity_cost": 2, "self_status": "evasive", "stat_mod": {"self": {"grace": 4, "essence": 2}}, "mod_duration": 3, "spell_tags": ["Buff", "Teleport", "Portal"]},
    {"id": "phantom_terrain",   "name": "Phantom Terrain",   "type": "mage", "power_type": "debuff",  "damage_type": "magical", "trigger": "always",       "cooldown": 5, "damage": 4,  "skill_capacity_cost": 2, "status_apply": "shaken", "stat_mod": {"enemy": {"grace": -3, "cognition": -3, "might": -2}}, "mod_duration": 3, "spell_tags": ["Debuff", "Single-Target", "Illusion"]},
    {"id": "dream_step",        "name": "Dream Step",        "type": "mage", "power_type": "buff",                              "trigger": "always",       "cooldown": 5, "damage": 0,  "skill_capacity_cost": 2, "self_status": "hidden", "stat_mod": {"self": {"grace": 4, "cognition": 2}}, "mod_duration": 2, "spell_tags": ["Buff", "Teleport", "Illusion"]},
    # Master Tier (Level 15) — 4 Strikes, 3 Debuffs, 1 Buff
    {"id": "meteor_storm",      "name": "Meteor Storm",      "type": "mage", "power_type": "strike",  "damage_type": "magical", "trigger": "always",       "cooldown": 6, "damage": 16, "skill_capacity_cost": 3, "hits": 3, "status_apply": "burning", "stat_mod": {"enemy": {"armor_bonus": -4, "grace": -3}}, "mod_duration": 3, "spell_tags": ["Strike", "Fire", "AoE", "Explosion"]},
    {"id": "blizzard",          "name": "Blizzard",          "type": "mage", "power_type": "debuff",  "damage_type": "magical", "trigger": "always",       "cooldown": 6, "damage": 6,  "skill_capacity_cost": 3, "status_apply": "ensnared", "stat_mod": {"enemy": {"grace": -4, "might": -3, "cognition": -2}}, "mod_duration": 3, "spell_tags": ["Debuff", "Ice", "AoE"]},
    {"id": "thunderfield",      "name": "Thunderfield",      "type": "mage", "power_type": "strike",  "damage_type": "magical", "trigger": "always",       "cooldown": 6, "damage": 14, "skill_capacity_cost": 3, "status_apply": "stunned", "stat_mod": {"enemy": {"grace": -3, "armor_bonus": -3, "might": -2}}, "mod_duration": 3, "spell_tags": ["Strike", "Lightning", "AoE"]},
    {"id": "time_slow",         "name": "Time Slow",         "type": "mage", "power_type": "debuff",  "damage_type": "magical", "trigger": "always",       "cooldown": 6, "damage": 5,  "skill_capacity_cost": 3, "status_apply": "shaken", "stat_mod": {"enemy": {"grace": -5, "might": -4, "cognition": -3}}, "mod_duration": 3, "spell_tags": ["Debuff", "Single-Target"]},
    {"id": "elemental_convergence","name": "Elemental Convergence","type": "mage","power_type": "strike","damage_type": "magical","trigger": "always",      "cooldown": 6, "damage": 15, "skill_capacity_cost": 3, "hits": 2, "status_apply": "burning", "stat_mod": {"enemy": {"armor_bonus": -4, "grace": -3, "might": -2}}, "mod_duration": 3, "spell_tags": ["Strike", "Fire", "Ice", "Lightning", "Stone", "Wind", "AoE"]},
    {"id": "mana_explosion",    "name": "Mana Explosion",    "type": "mage", "power_type": "strike",  "damage_type": "magical", "trigger": "low_hp",       "cooldown": 6, "damage": 18, "skill_capacity_cost": 3, "status_apply": "stunned", "stat_mod": {"self": {"might": 3}, "enemy": {"armor_bonus": -5, "grace": -4, "might": -3}}, "mod_duration": 3, "spell_tags": ["Strike", "AoE", "Explosion"]},
    {"id": "reality_fracture",  "name": "Reality Fracture",  "type": "mage", "power_type": "debuff",  "damage_type": "magical", "trigger": "opponent_wounded","cooldown": 6, "damage": 6, "skill_capacity_cost": 3, "status_apply": "stunned", "stat_mod": {"enemy": {"might": -5, "grace": -5, "armor_bonus": -4, "cognition": -3}}, "mod_duration": 4, "spell_tags": ["Debuff", "Single-Target"]},
    {"id": "time_stop",         "name": "Time Stop",         "type": "mage", "power_type": "buff",                              "trigger": "low_hp",       "cooldown": 7, "damage": 0,  "skill_capacity_cost": 3, "self_status": "warded", "heal_percent": 0.10, "stat_mod": {"self": {"grace": 5, "essence": 3, "cognition": 2}}, "mod_duration": 3, "spell_tags": ["Buff"]},
    # Legendary Tier (Level 20) — 2 True-Damage Strikes
    {"id": "cosmic_convergence","name": "Cosmic Convergence","type": "mage","power_type": "strike",  "damage_type": "true",     "trigger": "always",       "cooldown": 8, "damage": 25, "skill_capacity_cost": 3, "status_apply": "stunned", "self_status": "inspired", "stat_mod": {"enemy": {"might": -5, "grace": -5, "armor_bonus": -6, "essence": -4, "cognition": -3}}, "mod_duration": 4, "spell_tags": ["Strike", "Single-Target", "Void"], "quest_req": "the_arcane_ascension"},
    {"id": "legend_of_the_arcane","name": "Legend of the Arcane","type": "mage","power_type": "strike","damage_type": "true",   "trigger": "low_hp",       "cooldown": 10,"damage": 30, "skill_capacity_cost": 3, "hits": 8, "status_apply": "stunned", "self_status": "inspired", "heal_percent": 0.15, "stat_mod": {"enemy": {"might": -6, "grace": -6, "armor_bonus": -8, "essence": -5, "cognition": -4, "insight": -4, "durability": -4}}, "mod_duration": 5, "spell_tags": ["Fire", "Ice", "Lightning", "Stone", "Wind", "Void", "Strike", "AoE"], "quest_req": "the_arcane_ascension_2"},
    # --- Assassin Mastery: The Shadow Reaper --- (type="assassin" preserves mastery_req)
    # Basic Tier (Level 1) — 3 Strikes, 1 Stealth, 1 Debuff, 1 Buff (backstab already exists as skill #2)
    {"id": "shadow_strike",     "name": "Shadow Strike",     "type": "assassin", "power_type": "strike",  "damage_type": "physical", "trigger": "always",       "cooldown": 2, "damage": 6,  "skill_capacity_cost": 1, "status_apply": "bleeding", "stat_mod": {"enemy": {"grace": -2}}, "mod_duration": 2},
    {"id": "heart_piercer",     "name": "Heart Piercer",     "type": "assassin", "power_type": "strike",  "damage_type": "physical", "trigger": "always",       "cooldown": 2, "damage": 7,  "skill_capacity_cost": 1, "stat_mod": {"enemy": {"armor_bonus": -2, "might": -1}}, "mod_duration": 2},
    {"id": "smoke_veil",        "name": "Smoke Veil",        "type": "assassin", "power_type": "buff",    "trigger": "always",       "cooldown": 4, "damage": 0,  "skill_capacity_cost": 1, "self_status": "hidden", "stat_mod": {"self": {"grace": 3}}, "mod_duration": 2},
    {"id": "death_mark",        "name": "Death Mark",        "type": "assassin", "power_type": "debuff",  "damage_type": "physical", "trigger": "always",       "cooldown": 4, "damage": 4,  "skill_capacity_cost": 1, "status_apply": "shaken", "stat_mod": {"enemy": {"grace": -3, "armor_bonus": -3, "might": -2}}, "mod_duration": 3},
    {"id": "shadow_focus",      "name": "Shadow Focus",      "type": "assassin", "power_type": "buff",    "trigger": "always",       "cooldown": 3, "damage": 0,  "skill_capacity_cost": 1, "stat_mod": {"self": {"grace": 3, "might": 2}}, "mod_duration": 3},
    # Advanced Tier (Level 3) — 3 Strikes, 1 Stealth, 1 Debuff, 1 Buff, 1 Defend
    {"id": "silent_execution", "name": "Silent Execution",  "type": "assassin", "power_type": "strike",  "damage_type": "physical", "trigger": "opening_move",  "cooldown": 4, "damage": 10, "skill_capacity_cost": 2, "status_apply": "bleeding", "stat_mod": {"enemy": {"grace": -3, "might": -2}}, "mod_duration": 3},
    {"id": "phantom_strike",    "name": "Phantom Strike",    "type": "assassin", "power_type": "strike",  "damage_type": "physical", "trigger": "always",       "cooldown": 4, "damage": 8,  "skill_capacity_cost": 2, "hits": 2, "status_apply": "bleeding", "stat_mod": {"enemy": {"grace": -2}}, "mod_duration": 2},
    {"id": "crimson_dash",      "name": "Crimson Dash",      "type": "assassin", "power_type": "strike",  "damage_type": "physical", "trigger": "always",       "cooldown": 3, "damage": 9,  "skill_capacity_cost": 2, "status_apply": "bleeding", "stat_mod": {"enemy": {"grace": -2, "armor_bonus": -2}}, "mod_duration": 2},
    {"id": "night_veil",        "name": "Night Veil",        "type": "assassin", "power_type": "buff",    "trigger": "always",       "cooldown": 5, "damage": 0,  "skill_capacity_cost": 2, "self_status": "hidden", "stat_mod": {"self": {"grace": 4, "might": 2}}, "mod_duration": 3},
    {"id": "shadow_terror",     "name": "Shadow Terror",     "type": "assassin", "power_type": "debuff",  "damage_type": "magical",  "trigger": "always",       "cooldown": 5, "damage": 5,  "skill_capacity_cost": 2, "status_apply": "shaken", "stat_mod": {"enemy": {"might": -4, "grace": -3, "cognition": -2}}, "mod_duration": 3},
    {"id": "shadowstep",        "name": "Shadowstep",        "type": "assassin", "power_type": "defend",  "trigger": "always",       "cooldown": 3, "damage": 0,  "skill_capacity_cost": 1, "self_status": "evasive", "stat_mod": {"self": {"grace": 4}}, "mod_duration": 2},
    {"id": "dark_pursuit",      "name": "Dark Pursuit",      "type": "assassin", "power_type": "strike",  "damage_type": "physical", "trigger": "opponent_wounded","cooldown": 3, "damage": 11, "skill_capacity_cost": 2, "status_apply": "bleeding", "stat_mod": {"enemy": {"grace": -3, "might": -2}}, "mod_duration": 2},
    # Expert Tier (Level 8) — 3 Strikes, 1 Stealth, 1 Debuff, 1 Buff, 1 Defend
    {"id": "vanishing_kill",    "name": "Vanishing Kill",    "type": "assassin", "power_type": "strike",  "damage_type": "physical", "trigger": "opponent_status","cooldown": 5, "damage": 13, "skill_capacity_cost": 2, "status_apply": "bleeding", "self_status": "hidden", "stat_mod": {"enemy": {"grace": -3, "might": -2}}, "mod_duration": 2},
    {"id": "shadow_flurry",     "name": "Shadow Flurry",     "type": "assassin", "power_type": "strike",  "damage_type": "physical", "trigger": "always",       "cooldown": 5, "damage": 10, "skill_capacity_cost": 2, "hits": 3, "status_apply": "bleeding", "stat_mod": {"enemy": {"grace": -3, "armor_bonus": -2}}, "mod_duration": 2},
    {"id": "soul_sever",        "name": "Soul Sever",        "type": "assassin", "power_type": "strike",  "damage_type": "magical",  "trigger": "always",       "cooldown": 4, "damage": 12, "skill_capacity_cost": 2, "status_apply": "shaken", "stat_mod": {"enemy": {"might": -3, "essence": -3, "grace": -2}}, "mod_duration": 3},
    {"id": "shadow_clone",      "name": "Shadow Clone",      "type": "assassin", "power_type": "buff",    "trigger": "always",       "cooldown": 5, "damage": 0,  "skill_capacity_cost": 2, "self_status": "hidden", "stat_mod": {"self": {"grace": 5}}, "mod_duration": 3},
    {"id": "shadow_prison",    "name": "Shadow Prison",     "type": "assassin", "power_type": "debuff",  "damage_type": "magical",  "trigger": "always",       "cooldown": 6, "damage": 6,  "skill_capacity_cost": 2, "status_apply": "shaken", "stat_mod": {"enemy": {"grace": -4, "might": -3, "cognition": -2}}, "mod_duration": 3},
    {"id": "black_feathers",    "name": "Black Feathers",    "type": "assassin", "power_type": "defend",  "trigger": "low_hp",       "cooldown": 6, "damage": 0,  "skill_capacity_cost": 2, "self_status": "hidden", "stat_mod": {"self": {"grace": 5}}, "mod_duration": 3},
    {"id": "eclipse_blade",     "name": "Eclipse Blade",     "type": "assassin", "power_type": "buff",    "trigger": "always",       "cooldown": 5, "damage": 0,  "skill_capacity_cost": 2, "stat_mod": {"self": {"might": 4, "grace": 3, "insight": 2}}, "mod_duration": 4},
    # Master Tier (Level 15) — 4 Strikes, 1 Stealth, 1 Debuff, 1 Buff, 1 Defend
    {"id": "shadow_convergence","name": "Shadow Convergence","type": "assassin","power_type": "buff",    "trigger": "always",       "cooldown": 6, "damage": 0,  "skill_capacity_cost": 3, "stat_mod": {"self": {"grace": 5, "might": 4, "insight": 3}}, "mod_duration": 4},
    {"id": "night_requiem",    "name": "Night Requiem",     "type": "assassin", "power_type": "strike",  "damage_type": "physical", "trigger": "always",       "cooldown": 6, "damage": 16, "skill_capacity_cost": 3, "hits": 3, "status_apply": "bleeding", "stat_mod": {"enemy": {"grace": -3, "armor_bonus": -3, "might": -2}}, "mod_duration": 3},
    {"id": "deaths_whisper",    "name": "Death's Whisper",   "type": "assassin", "power_type": "debuff",  "damage_type": "magical",  "trigger": "opponent_wounded","cooldown": 5, "damage": 8,  "skill_capacity_cost": 3, "status_apply": "shaken", "stat_mod": {"enemy": {"might": -5, "grace": -4, "cognition": -3, "essence": -2}}, "mod_duration": 3},
    {"id": "umbral_cloak",      "name": "Umbral Cloak",      "type": "assassin", "power_type": "buff",    "trigger": "always",       "cooldown": 6, "damage": 0,  "skill_capacity_cost": 3, "self_status": "hidden", "stat_mod": {"self": {"grace": 5, "might": 3}}, "mod_duration": 4},
    {"id": "final_contract",   "name": "Final Contract",   "type": "assassin", "power_type": "strike",  "damage_type": "physical", "trigger": "low_hp",       "cooldown": 6, "damage": 18, "skill_capacity_cost": 3, "status_apply": "bleeding", "stat_mod": {"self": {"might": 4, "grace": 3}, "enemy": {"armor_bonus": -5, "might": -4, "grace": -3}}, "mod_duration": 3},
    {"id": "king_slayer",      "name": "King Slayer",      "type": "assassin", "power_type": "strike",  "damage_type": "physical", "trigger": "opponent_wounded","cooldown": 6, "damage": 20, "skill_capacity_cost": 3, "status_apply": "bleeding", "stat_mod": {"enemy": {"might": -5, "armor_bonus": -5, "grace": -4, "durability": -3}}, "mod_duration": 4},
    {"id": "shadow_devour",    "name": "Shadow Devour",    "type": "assassin", "power_type": "strike",  "damage_type": "magical",  "trigger": "opponent_status","cooldown": 6, "damage": 16, "skill_capacity_cost": 3, "status_apply": "stunned", "stat_mod": {"enemy": {"might": -5, "grace": -5, "essence": -4, "cognition": -3}}, "mod_duration": 3},
    {"id": "eclipse_burst",    "name": "Eclipse Burst",    "type": "assassin", "power_type": "strike",  "damage_type": "physical", "trigger": "always",       "cooldown": 8, "damage": 22, "skill_capacity_cost": 3, "status_apply": "stunned", "stat_mod": {"enemy": {"might": -5, "grace": -5, "armor_bonus": -5}}, "mod_duration": 3},
    # Legendary Tier (Level 20) — 2 True-Damage Strikes
    {"id": "reapers_arrival",  "name": "Reaper's Arrival",  "type": "assassin", "power_type": "strike",  "damage_type": "true",     "trigger": "always",       "cooldown": 8, "damage": 25, "skill_capacity_cost": 3, "status_apply": "stunned", "stat_mod": {"enemy": {"might": -5, "grace": -5, "armor_bonus": -6, "cognition": -4}}, "mod_duration": 4, "self_status": "hidden"},
    {"id": "eclipse_of_shadows","name": "Eclipse of Shadows","type":"assassin","power_type": "strike",  "damage_type": "true",     "trigger": "low_hp",       "cooldown": 10,"damage": 30, "skill_capacity_cost": 3, "status_apply": "stunned", "stat_mod": {"enemy": {"might": -6, "grace": -6, "armor_bonus": -8, "cognition": -5, "essence": -4}}, "mod_duration": 5, "self_status": "hidden"},
    # --- Hunter Mastery: Master of Precision --- (type="hunter" preserves mastery_req)
    # Basic Tier (Level 1) — 3 Strikes, 1 Trap, 2 Buffs
    {"id": "rapid_shot",      "name": "Rapid Shot",      "type": "hunter", "power_type": "strike",  "damage_type": "physical", "trigger": "always",       "cooldown": 2, "damage": 4,  "skill_capacity_cost": 1, "hits": 2, "stat_mod": {"enemy": {"grace": -1}}, "mod_duration": 2, "spirit_communion": "hits: 3, third_hit_deals_magical"},
    {"id": "piercing_shot",   "name": "Piercing Shot",   "type": "hunter", "power_type": "strike",  "damage_type": "physical", "trigger": "always",       "cooldown": 3, "damage": 7,  "skill_capacity_cost": 1, "stat_mod": {"enemy": {"armor_bonus": -3}}, "mod_duration": 2, "spirit_communion": "damage_type: true, ignores_all_armor"},
    {"id": "snare_trap",      "name": "Snare Trap",      "type": "hunter", "power_type": "trap",    "damage_type": "physical", "trigger": "always",       "cooldown": 4, "damage": 5,  "skill_capacity_cost": 1, "status_apply": "ensnared", "stat_mod": {"enemy": {"grace": -2, "might": -2}}, "mod_duration": 3, "spirit_communion": "ensnared + silenced"},
    {"id": "camouflage",      "name": "Camouflage",      "type": "hunter", "power_type": "buff",    "trigger": "always",       "cooldown": 4, "damage": 0,  "skill_capacity_cost": 1, "self_status": "hidden", "stat_mod": {"self": {"grace": 3}}, "mod_duration": 2, "spirit_communion": "hidden + summons_spirit_copy_decoy"},
    {"id": "eagle_eye",       "name": "Eagle Eye",       "type": "hunter", "power_type": "buff",    "trigger": "always",       "cooldown": 3, "damage": 0,  "skill_capacity_cost": 1, "self_status": "inspired", "stat_mod": {"self": {"grace": 4}}, "mod_duration": 3, "spirit_communion": "next_3_hits_guaranteed_crit"},
    {"id": "crippling_shot",  "name": "Crippling Shot",  "type": "hunter", "power_type": "strike",  "damage_type": "physical", "trigger": "always",       "cooldown": 3, "damage": 6,  "skill_capacity_cost": 1, "status_apply": "ensnared", "stat_mod": {"enemy": {"might": -3, "grace": -2}}, "mod_duration": 2, "spirit_communion": "spirit_root, cant_act, +1_range"},
    # Advanced Tier (Level 3) — 3 Strikes, 2 Traps, 1 Debuff, 1 Spirit
    {"id": "poison_arrow",    "name": "Poison Arrow",    "type": "hunter", "power_type": "strike",  "damage_type": "physical", "trigger": "always",       "cooldown": 3, "damage": 6,  "skill_capacity_cost": 2, "status_apply": "poisoned", "stat_mod": {"enemy": {"might": -2}}, "mod_duration": 3, "spirit_communion": "spirit_venom, uncleansable"},
    {"id": "flash_bang",      "name": "Flash Bang",      "type": "hunter", "power_type": "trap",    "damage_type": "magical",  "trigger": "always",       "cooldown": 4, "damage": 4,  "skill_capacity_cost": 2, "status_apply": "stunned", "stat_mod": {"enemy": {"grace": -3}}, "mod_duration": 2, "spirit_communion": "stunned + blinded, +1_range"},
    {"id": "twin_shot",       "name": "Twin Shot",       "type": "hunter", "power_type": "strike",  "damage_type": "physical", "trigger": "always",       "cooldown": 3, "damage": 5,  "skill_capacity_cost": 2, "hits": 2, "status_apply": "bleeding", "stat_mod": {"enemy": {"grace": -2}}, "mod_duration": 2, "spirit_communion": "hits: 3, bleeding_cant_be_stopped"},
    {"id": "smoke_bomb",      "name": "Smoke Bomb",      "type": "hunter", "power_type": "trap",    "damage_type": "magical",  "trigger": "always",       "cooldown": 4, "damage": 0,  "skill_capacity_cost": 2, "self_status": "hidden", "range_modifier": 1, "stat_mod": {"enemy": {"grace": -2}}, "mod_duration": 2, "spirit_communion": "+2_range, all_allies_hidden"},
    {"id": "hunters_mark",    "name": "Hunter's Mark",   "type": "hunter", "power_type": "debuff",  "damage_type": "physical", "trigger": "always",       "cooldown": 4, "damage": 3,  "skill_capacity_cost": 2, "status_apply": "shaken", "stat_mod": {"enemy": {"grace": -3, "armor_bonus": -3}}, "mod_duration": 3, "spirit_communion": "all_allies_gain_crit"},
    {"id": "falcon_strike",   "name": "Falcon Strike",   "type": "hunter", "power_type": "strike",  "damage_type": "physical", "trigger": "opening_move",  "cooldown": 4, "damage": 9,  "skill_capacity_cost": 2, "status_apply": "bleeding", "stat_mod": {"enemy": {"grace": -3}}, "mod_duration": 2, "spirit_communion": "spirit_falcon_persists_2_turns"},
    {"id": "spirit_walk",     "name": "Spirit Walk",      "type": "hunter", "power_type": "spirit",  "trigger": "always",       "cooldown": 5, "damage": 0,  "skill_capacity_cost": 2, "self_status": "evasive", "range_modifier": 2, "stat_mod": {"self": {"grace": 2}}, "mod_duration": 1, "spirit_communion": "intangible_2_turns, +3_range, heals_5_percent"},
    # Expert Tier (Level 8) — 3 Strikes, 2 Traps, 2 Buffs
    {"id": "rain_of_arrows",  "name": "Rain of Arrows",  "type": "hunter", "power_type": "strike",  "damage_type": "physical", "trigger": "always",       "cooldown": 5, "damage": 6,  "skill_capacity_cost": 2, "hits": 3, "status_apply": "bleeding", "stat_mod": {"enemy": {"grace": -3, "armor_bonus": -2}}, "mod_duration": 2, "spirit_communion": "hits: 5, all_arrows_unevadable"},
    {"id": "wolf_companion",  "name": "Wolf Companion",  "type": "hunter", "power_type": "strike",  "damage_type": "physical", "trigger": "always",       "cooldown": 5, "damage": 8,  "skill_capacity_cost": 2, "status_apply": "bleeding", "stat_mod": {"enemy": {"might": -3, "grace": -2}}, "mod_duration": 3, "spirit_communion": "spirit_wolf_persists_3_turns"},
    {"id": "explosive_trap",  "name": "Explosive Trap",  "type": "hunter", "power_type": "trap",    "damage_type": "magical",  "trigger": "always",       "cooldown": 4, "damage": 8,  "skill_capacity_cost": 2, "status_apply": "burning", "stat_mod": {"enemy": {"armor_bonus": -3, "might": -2}}, "mod_duration": 3, "spirit_communion": "spirit_explosion, true_damage, hits_all_enemies"},
    {"id": "hawk_vision",     "name": "Hawk Vision",     "type": "hunter", "power_type": "buff",    "trigger": "always",       "cooldown": 5, "damage": 0,  "skill_capacity_cost": 2, "self_status": "inspired", "stat_mod": {"self": {"grace": 3, "cognition": 3, "insight": 2}}, "mod_duration": 3, "spirit_communion": "guaranteed_crits_3_turns, sees_through_stealth"},
    {"id": "backflip",        "name": "Backflip",        "type": "hunter", "power_type": "buff",    "trigger": "always",       "cooldown": 4, "damage": 0,  "skill_capacity_cost": 2, "self_status": "evasive", "range_modifier": 2, "stat_mod": {"self": {"grace": 3}}, "mod_duration": 2, "spirit_communion": "+3_range, leaves_spirit_copy"},
    {"id": "monster_slayer",  "name": "Monster Slayer",  "type": "hunter", "power_type": "strike",  "damage_type": "physical", "trigger": "opponent_wounded","cooldown": 4, "damage": 10, "skill_capacity_cost": 2, "status_apply": "bleeding", "stat_mod": {"enemy": {"armor_bonus": -4, "might": -3}}, "mod_duration": 3, "spirit_communion": "true_damage, execute_threshold_20_percent"},
    {"id": "bear_trap",       "name": "Bear Trap",       "type": "hunter", "power_type": "trap",    "damage_type": "physical", "trigger": "always",       "cooldown": 5, "damage": 7,  "skill_capacity_cost": 2, "status_apply": "ensnared", "stat_mod": {"enemy": {"might": -4, "grace": -3, "armor_bonus": -2}}, "mod_duration": 3, "spirit_communion": "spirit_jaws, +2_range"},
    # Master Tier (Level 15) — 2 Strikes, 2 Buffs, 1 Debuff, 1 Heal, 1 Defend, 1 Spirit
    {"id": "volley_master",   "name": "Volley Master",   "type": "hunter", "power_type": "strike",  "damage_type": "physical", "trigger": "always",       "cooldown": 6, "damage": 10, "skill_capacity_cost": 3, "hits": 3, "status_apply": "bleeding", "stat_mod": {"enemy": {"grace": -3, "armor_bonus": -4, "might": -2}}, "mod_duration": 3, "spirit_communion": "hits: 5, each_hit_different_debuff"},
    {"id": "spirit_bind",     "name": "Spirit Bind",     "type": "hunter", "power_type": "spirit",  "damage_type": "magical",  "trigger": "always",       "cooldown": 6, "damage": 8,  "skill_capacity_cost": 3, "status_apply": "ensnared", "stat_mod": {"enemy": {"might": -4, "grace": -4}}, "mod_duration": 3, "spirit_communion": "spirit_prison, cant_act, true_damage_per_turn, +2_range"},
    {"id": "storm_arrow",     "name": "Storm Arrow",     "type": "hunter", "power_type": "strike",  "damage_type": "magical",  "trigger": "always",       "cooldown": 5, "damage": 12, "skill_capacity_cost": 3, "status_apply": "stunned", "stat_mod": {"enemy": {"grace": -3, "armor_bonus": -3, "might": -2}}, "mod_duration": 3, "spirit_communion": "true_damage + chains_to_nearby_enemies"},
    {"id": "natures_blessing","name": "Nature's Blessing","type": "hunter", "power_type": "heal",    "trigger": "low_hp",       "cooldown": 6, "damage": 0,  "skill_capacity_cost": 3, "self_status": "warded", "heal_percent": 0.15, "stat_mod": {"self": {"essence": 3, "durability": 2}}, "mod_duration": 3, "spirit_communion": "cleanses_all_debuffs, heals_25_percent, +2_range"},
    {"id": "survival_instinct","name": "Survival Instinct","type": "hunter","power_type": "defend",  "trigger": "low_hp",       "cooldown": 6, "damage": 0,  "skill_capacity_cost": 3, "self_status": "evasive", "heal_percent": 0.10, "stat_mod": {"self": {"grace": 4, "durability": 3}}, "mod_duration": 3, "spirit_communion": "immune_1_turn, +3_range, spirit_copy_absorbs_hit"},
    {"id": "alpha_command",   "name": "Alpha Command",   "type": "hunter", "power_type": "buff",    "trigger": "always",       "cooldown": 6, "damage": 0,  "skill_capacity_cost": 3, "self_status": "inspired", "stat_mod": {"self": {"might": 4, "grace": 3, "cognition": 2}}, "mod_duration": 4, "spirit_communion": "spirit_bow, next_3_strikes_true_damage"},
    {"id": "ancient_tracker", "name": "Ancient Tracker", "type": "hunter", "power_type": "buff",    "trigger": "always",       "cooldown": 5, "damage": 0,  "skill_capacity_cost": 3, "self_status": "inspired", "stat_mod": {"self": {"cognition": 4, "grace": 3, "insight": 2}}, "mod_duration": 4, "spirit_communion": "spirit_guidance_gains_2_per_hit"},
    {"id": "tracking_instinct","name": "Tracking Instinct","type":"hunter", "power_type": "debuff",  "damage_type": "physical", "trigger": "opponent_status","cooldown": 5, "damage": 6,  "skill_capacity_cost": 3, "status_apply": "shaken", "stat_mod": {"enemy": {"grace": -4, "cognition": -3, "might": -2}}, "mod_duration": 3, "spirit_communion": "enemy_cant_evade + spirit_guidance_+1_per_hit"},
    # Legendary Tier (Level 20) — 2 True-Damage Strikes
    {"id": "world_hunt",      "name": "World Hunt",      "type": "hunter", "power_type": "strike",  "damage_type": "true",     "trigger": "opponent_wounded","cooldown": 8, "damage": 20, "skill_capacity_cost": 3, "hits": 3, "status_apply": "bleeding", "stat_mod": {"enemy": {"might": -5, "grace": -5, "armor_bonus": -6, "cognition": -3}}, "mod_duration": 4, "spirit_communion": "infinite_range, repeats_every_turn", "quest_req": "the_endless_pursuit"},
    {"id": "legend_of_the_wild","name": "Legend of the Wild","type":"hunter","power_type": "strike", "damage_type": "true",     "trigger": "low_hp",       "cooldown": 10,"damage": 25, "skill_capacity_cost": 3, "hits": 5, "status_apply": "stunned", "self_status": "inspired", "heal_percent": 0.15, "stat_mod": {"enemy": {"might": -6, "grace": -6, "armor_bonus": -8, "cognition": -5, "durability": -4}}, "mod_duration": 5, "spirit_communion": "ancestor_army, 10_hits, full_party_inspired, resets_guidance_to_20", "quest_req": "the_endless_pursuit"},
    # --- Rogue Mastery: The Adaptive Trickster --- (type="rogue" preserves mastery_req)
    # Basic Tier (Level 1) — 3 Strikes, 1 Debuff, 1 Defend, 1 Buff
    {"id": "dirty_trick",       "name": "Dirty Trick",       "type": "rogue", "power_type": "debuff",  "damage_type": "physical", "trigger": "always",        "cooldown": 2, "damage": 4,  "skill_capacity_cost": 1, "status_apply": "shaken", "stat_mod": {"enemy": {"grace": -2, "might": -1}}, "mod_duration": 2},
    {"id": "hidden_blade",      "name": "Hidden Blade",      "type": "rogue", "power_type": "strike",  "damage_type": "physical", "trigger": "opening_move",   "cooldown": 3, "damage": 8,  "skill_capacity_cost": 1, "status_apply": "bleeding", "stat_mod": {"enemy": {"grace": -2}}, "mod_duration": 2},
    {"id": "opportunist_strike", "name": "Opportunist Strike","type": "rogue", "power_type": "strike",  "damage_type": "physical", "trigger": "opponent_status","cooldown": 2, "damage": 7,  "skill_capacity_cost": 1, "status_apply": "bleeding", "stat_mod": {"enemy": {"might": -2}}, "mod_duration": 2},
    {"id": "acrobatic_roll",    "name": "Acrobatic Roll",    "type": "rogue", "power_type": "defend",  "trigger": "always",        "cooldown": 3, "damage": 0,  "skill_capacity_cost": 0, "self_status": "evasive", "stat_mod": {"self": {"grace": 3}}, "mod_duration": 2},
    {"id": "quick_step",        "name": "Quick Step",        "type": "rogue", "power_type": "buff",    "trigger": "always",        "cooldown": 3, "damage": 0,  "skill_capacity_cost": 1, "self_status": "evasive", "stat_mod": {"self": {"grace": 3, "might": 2}}, "mod_duration": 3},
    {"id": "pocket_sand",       "name": "Pocket Sand",       "type": "rogue", "power_type": "debuff",  "damage_type": "physical", "trigger": "always",        "cooldown": 3, "damage": 3,  "skill_capacity_cost": 1, "status_apply": "blinded", "stat_mod": {"enemy": {"grace": -3}}, "mod_duration": 2},
    # Advanced Tier (Level 3) — 3 Strikes, 2 Debuffs, 1 Buff, 1 Defend
    {"id": "flash_powder",      "name": "Flash Powder",      "type": "rogue", "power_type": "debuff",  "damage_type": "magical",  "trigger": "always",        "cooldown": 4, "damage": 4,  "skill_capacity_cost": 2, "status_apply": "blinded", "stat_mod": {"enemy": {"grace": -3, "might": -2}}, "mod_duration": 3},
    {"id": "tripwire",          "name": "Tripwire",          "type": "rogue", "power_type": "debuff",  "damage_type": "physical", "trigger": "always",        "cooldown": 4, "damage": 4,  "skill_capacity_cost": 2, "status_apply": "ensnared", "stat_mod": {"enemy": {"grace": -3, "might": -2}}, "mod_duration": 3},
    {"id": "knife_fan",         "name": "Knife Fan",         "type": "rogue", "power_type": "strike",  "damage_type": "physical", "trigger": "always",        "cooldown": 4, "damage": 5,  "skill_capacity_cost": 2, "hits": 2, "status_apply": "bleeding", "stat_mod": {"enemy": {"grace": -2}}, "mod_duration": 2},
    {"id": "hook_chain",        "name": "Hook Chain",        "type": "rogue", "power_type": "strike",  "damage_type": "physical", "trigger": "always",        "cooldown": 4, "damage": 6,  "skill_capacity_cost": 2, "status_apply": "ensnared", "stat_mod": {"enemy": {"grace": -2, "armor_bonus": -2}}, "mod_duration": 2},
    {"id": "feign_death",       "name": "Feign Death",       "type": "rogue", "power_type": "defend",  "trigger": "low_hp",        "cooldown": 5, "damage": 0,  "skill_capacity_cost": 0, "self_status": "hidden", "stat_mod": {"self": {"grace": 3}}, "mod_duration": 3},
    {"id": "wall_run",          "name": "Wall Run",          "type": "rogue", "power_type": "buff",    "trigger": "always",        "cooldown": 4, "damage": 0,  "skill_capacity_cost": 2, "self_status": "evasive", "stat_mod": {"self": {"grace": 4, "might": 2}}, "mod_duration": 3},
    {"id": "sleight_of_hand",   "name": "Sleight of Hand",   "type": "rogue", "power_type": "strike",  "damage_type": "physical", "trigger": "opponent_status","cooldown": 4, "damage": 7,  "skill_capacity_cost": 2, "status_apply": "shaken", "stat_mod": {"self": {"might": 2}, "enemy": {"might": -3, "grace": -2}}, "mod_duration": 3},
    # Expert Tier (Level 8) — 3 Strikes, 1 Debuff, 1 Buff, 2 Defends
    {"id": "mirror_image",      "name": "Mirror Image",      "type": "rogue", "power_type": "buff",    "trigger": "always",        "cooldown": 5, "damage": 0,  "skill_capacity_cost": 2, "self_status": "evasive", "stat_mod": {"self": {"grace": 5}}, "mod_duration": 3},
    {"id": "smoke_bomb_rogue",  "name": "Smoke Bomb",        "type": "rogue", "power_type": "defend",  "trigger": "always",        "cooldown": 5, "damage": 0,  "skill_capacity_cost": 0, "self_status": "hidden", "stat_mod": {"self": {"grace": 3, "cognition": 2}}, "mod_duration": 3},
    {"id": "false_surrender",   "name": "False Surrender",   "type": "rogue", "power_type": "strike",  "damage_type": "physical", "trigger": "low_hp",        "cooldown": 5, "damage": 10, "skill_capacity_cost": 2, "status_apply": "stunned", "stat_mod": {"enemy": {"grace": -3, "might": -3}}, "mod_duration": 3},
    {"id": "misdirection",      "name": "Misdirection",      "type": "rogue", "power_type": "debuff",  "damage_type": "magical",  "trigger": "always",        "cooldown": 5, "damage": 5,  "skill_capacity_cost": 2, "status_apply": "shaken", "stat_mod": {"enemy": {"cognition": -4, "grace": -3, "might": -2}}, "mod_duration": 3},
    {"id": "counter_stab",      "name": "Counter Stab",      "type": "rogue", "power_type": "strike",  "damage_type": "physical", "trigger": "opponent_status","cooldown": 5, "damage": 8,  "skill_capacity_cost": 2, "hits": 2, "status_apply": "bleeding", "stat_mod": {"self": {"might": 3, "grace": 2}, "enemy": {"might": -3, "grace": -2}}, "mod_duration": 3},
    {"id": "escape_artist",     "name": "Escape Artist",     "type": "rogue", "power_type": "defend",  "trigger": "self_debuff",   "cooldown": 4, "damage": 0,  "skill_capacity_cost": 0, "self_status": "evasive", "stat_mod": {"self": {"grace": 4, "cognition": 2}}, "mod_duration": 3},
    {"id": "tricksters_flurry", "name": "Trickster's Flurry","type": "rogue", "power_type": "strike",  "damage_type": "physical", "trigger": "always",        "cooldown": 5, "damage": 6,  "skill_capacity_cost": 2, "hits": 3, "status_apply": "bleeding", "stat_mod": {"self": {"might": 3, "grace": 2}, "enemy": {"grace": -3, "might": -2}}, "mod_duration": 3},
    # Master Tier (Level 15) — 4 Strikes, 1 Debuff, 1 Buff, 2 Defends
    {"id": "lucky_escape",      "name": "Lucky Escape",      "type": "rogue", "power_type": "defend",  "trigger": "low_hp",        "cooldown": 6, "damage": 0,  "skill_capacity_cost": 0, "self_status": "evasive", "stat_mod": {"self": {"grace": 5, "cognition": 3}}, "mod_duration": 3},
    {"id": "ambush_master",     "name": "Ambush Master",     "type": "rogue", "power_type": "buff",    "trigger": "opening_move",  "cooldown": 6, "damage": 0,  "skill_capacity_cost": 3, "self_status": "hidden", "stat_mod": {"self": {"might": 4, "grace": 4, "cognition": 2}}, "mod_duration": 4},
    {"id": "grand_heist",       "name": "Grand Heist",       "type": "rogue", "power_type": "strike",  "damage_type": "physical", "trigger": "opponent_wounded","cooldown": 6, "damage": 12, "skill_capacity_cost": 3, "status_apply": "shaken", "stat_mod": {"self": {"might": 3, "grace": 3}, "enemy": {"armor_bonus": -5, "might": -3}}, "mod_duration": 4},
    {"id": "coin_toss",         "name": "Coin Toss",         "type": "rogue", "power_type": "debuff",  "damage_type": "magical",  "trigger": "always",        "cooldown": 5, "damage": 6,  "skill_capacity_cost": 3, "status_apply": "shaken", "stat_mod": {"enemy": {"cognition": -4, "grace": -3, "might": -3, "insight": -2}}, "mod_duration": 3},
    {"id": "shadow_step_rogue", "name": "Shadow Step",       "type": "rogue", "power_type": "defend",  "trigger": "always",        "cooldown": 6, "damage": 0,  "skill_capacity_cost": 0, "self_status": "hidden", "stat_mod": {"self": {"grace": 4, "cognition": 3}}, "mod_duration": 3},
    {"id": "master_picklock",   "name": "Master Picklock",   "type": "rogue", "power_type": "strike",  "damage_type": "physical", "trigger": "opponent_wounded","cooldown": 6, "damage": 14, "skill_capacity_cost": 3, "status_apply": "ensnared", "stat_mod": {"enemy": {"armor_bonus": -6, "grace": -3, "cognition": -2}}, "mod_duration": 3},
    {"id": "king_of_thieves",   "name": "King of Thieves",   "type": "rogue", "power_type": "strike",  "damage_type": "physical", "trigger": "opponent_status","cooldown": 6, "damage": 13, "skill_capacity_cost": 3, "status_apply": "shaken", "stat_mod": {"self": {"might": 4, "grace": 3, "cognition": 2}, "enemy": {"might": -4, "grace": -3, "cognition": -3}}, "mod_duration": 4},
    {"id": "tricksters_gambit", "name": "Trickster's Gambit","type": "rogue", "power_type": "strike",  "damage_type": "physical", "trigger": "always",        "cooldown": 6, "damage": 10, "skill_capacity_cost": 3, "hits": 3, "status_apply": "bleeding", "stat_mod": {"self": {"might": 4, "grace": 3}, "enemy": {"might": -3, "grace": -3, "armor_bonus": -3}}, "mod_duration": 4},
    # Legendary Tier (Level 20) — 2 True-Damage Strikes
    {"id": "perfect_crime",     "name": "Perfect Crime",     "type": "rogue", "power_type": "strike",  "damage_type": "true",     "trigger": "opponent_wounded","cooldown": 8, "damage": 18, "skill_capacity_cost": 3, "status_apply": "bleeding", "self_status": "hidden", "stat_mod": {"enemy": {"might": -5, "grace": -5, "armor_bonus": -6, "cognition": -4}}, "mod_duration": 4},
    {"id": "legend_of_trickery","name": "Legend of Trickery","type": "rogue", "power_type": "strike",  "damage_type": "true",     "trigger": "low_hp",        "cooldown": 10,"damage": 25, "skill_capacity_cost": 3, "status_apply": "stunned", "self_status": "hidden", "stat_mod": {"enemy": {"might": -6, "grace": -6, "armor_bonus": -8, "cognition": -5, "insight": -4}}, "mod_duration": 5},
    # --- Bard Mastery: The Master of Control --- (type="bard" preserves mastery_req)
    # Basic Tier (Level 1) — 2 Performances, 1 Debuff (mocking_verse already above), 1 Strike, 2 Defends
    {"id": "song_of_heroes",     "name": "Song of Heroes",     "type": "bard", "power_type": "performance", "mode": "both", "trigger": "always", "cooldown": 0, "damage": 0, "skill_capacity_cost": 0, "crescendo": True, "encore": True, "song_effect": "physical_attacks_unevadable", "dance_effect": "confuse", "base_chance": 0.10, "crescendo_scale": 0.08},
    {"id": "song_of_hope",       "name": "Song of Hope",       "type": "bard", "power_type": "performance", "mode": "both", "trigger": "always", "cooldown": 0, "damage": 0, "skill_capacity_cost": 0, "crescendo": True, "encore": True, "song_effect": "death_save", "dance_effect": "pull_mesmerize", "base_chance": 0.15, "crescendo_scale": 0.05},
    {"id": "resonant_strike",    "name": "Resonant Strike",    "type": "bard", "power_type": "strike",  "damage_type": "magical", "trigger": "always",        "cooldown": 3, "damage": 6,  "skill_capacity_cost": 1, "stat_mod": {"enemy": {"grace": -1}}, "mod_duration": 2},
    {"id": "harmony_shield",     "name": "Harmony Shield",     "type": "bard", "power_type": "defend",  "trigger": "always",        "cooldown": 4, "damage": 0,  "skill_capacity_cost": 1, "self_status": "warded", "stat_mod": {"all_allies": {"armor_bonus": 2, "essence": 1}}, "mod_duration": 3},
    {"id": "sunrise_chorus",     "name": "Sunrise Chorus",     "type": "bard", "power_type": "defend",  "trigger": "self_debuff",   "cooldown": 4, "damage": 0,  "skill_capacity_cost": 1, "self_status": "warded", "stat_mod": {"all_allies": {"essence": 2, "grace": 1}}, "mod_duration": 3},
    # Advanced Tier (Level 3) — 1 Performance, 1 Buff, 2 Debuffs, 1 Strike, 1 Heal
    {"id": "song_of_wisdom",     "name": "Song of Wisdom",     "type": "bard", "power_type": "performance", "mode": "both", "trigger": "always", "cooldown": 0, "damage": 0, "skill_capacity_cost": 0, "crescendo": True, "encore": True, "song_effect": "cooldown_reset", "dance_effect": "silence", "base_chance": 0.20, "crescendo_scale": 0.08},
    {"id": "festival_rhythm",    "name": "Festival Rhythm",    "type": "bard", "power_type": "buff",    "trigger": "always",        "cooldown": 4, "damage": 0,  "skill_capacity_cost": 1, "self_status": "inspired", "stat_mod": {"all_allies": {"grace": 2, "might": 1, "cognition": 1}}, "mod_duration": 3},
    {"id": "discord",            "name": "Discord",            "type": "bard", "power_type": "debuff",  "damage_type": "magical", "trigger": "always",        "cooldown": 4, "damage": 4,  "skill_capacity_cost": 1, "status_apply": "shaken", "stat_mod": {"enemy": {"cognition": -3, "grace": -2, "might": -2}}, "mod_duration": 3},
    {"id": "dance_of_blades",    "name": "Dance of Blades",    "type": "bard", "power_type": "strike",  "damage_type": "magical", "trigger": "always",        "cooldown": 4, "damage": 7,  "skill_capacity_cost": 1, "status_apply": "bleeding", "stat_mod": {"enemy": {"grace": -2}}, "mod_duration": 2},
    {"id": "sirens_call",        "name": "Siren's Call",       "type": "bard", "power_type": "debuff",  "damage_type": "magical", "trigger": "always",        "cooldown": 4, "damage": 4,  "skill_capacity_cost": 1, "status_apply": "ensnared", "stat_mod": {"enemy": {"grace": -3, "cognition": -2}}, "mod_duration": 2},
    {"id": "ballad_of_hope",     "name": "Ballad of Hope",     "type": "bard", "power_type": "heal",    "trigger": "low_hp",        "cooldown": 5, "damage": 0,  "skill_capacity_cost": 2, "self_status": "inspired", "heal_percent": 0.10, "stat_mod": {"all_allies": {"essence": 1, "grace": 1}}, "mod_duration": 3},
    {"id": "lullaby_of_fallen_kings","name": "Lullaby of Fallen Kings","type": "bard","power_type": "debuff","damage_type": "magical","trigger": "always",       "cooldown": 5, "damage": 5,  "skill_capacity_cost": 2, "status_apply": "stunned", "stat_mod": {"enemy": {"grace": -3, "might": -2, "cognition": -1}}, "mod_duration": 2},
    # Expert Tier (Level 8) — 1 Performance, 5 Buffs, 1 Debuff
    {"id": "song_of_freedom",    "name": "Song of Freedom",    "type": "bard", "power_type": "performance", "mode": "both", "trigger": "always", "cooldown": 0, "damage": 0, "skill_capacity_cost": 0, "crescendo": True, "encore": True, "song_effect": "cc_immune", "dance_effect": "friendly_fire", "base_chance": 0.10, "crescendo_scale": 0.08},
    {"id": "moon_serenade",      "name": "Moon Serenade",      "type": "bard", "power_type": "buff",    "trigger": "always",        "cooldown": 5, "damage": 0,  "skill_capacity_cost": 2, "self_status": "warded", "heal_percent": 0.08, "stat_mod": {"all_allies": {"essence": 2, "grace": 1, "insight": 1}}, "mod_duration": 4},
    {"id": "inspiring_solo",     "name": "Inspiring Solo",     "type": "bard", "power_type": "buff",    "trigger": "always",        "cooldown": 5, "damage": 0,  "skill_capacity_cost": 2, "self_status": "inspired", "stat_mod": {"all_allies": {"might": 3, "grace": 2}}, "mod_duration": 3},
    {"id": "echo_verse",         "name": "Echo Verse",         "type": "bard", "power_type": "buff",    "trigger": "opponent_status","cooldown": 5, "damage": 0,  "skill_capacity_cost": 2, "self_status": "inspired", "stat_mod": {"all_allies": {"might": 2, "grace": 2, "essence": 1}}, "mod_duration": 3},
    {"id": "epic_tale",          "name": "Epic Tale",          "type": "bard", "power_type": "buff",    "trigger": "always",        "cooldown": 5, "damage": 0,  "skill_capacity_cost": 2, "self_status": "inspired", "heal_percent": 0.08, "stat_mod": {"all_allies": {"might": 2, "grace": 2, "durability": 2, "essence": 1}}, "mod_duration": 4},
    {"id": "muses_blessing",     "name": "Muse's Blessing",    "type": "bard", "power_type": "buff",    "trigger": "always",        "cooldown": 5, "damage": 0,  "skill_capacity_cost": 2, "self_status": "inspired", "stat_mod": {"all_allies": {"insight": 3, "cognition": 2, "essence": 1}}, "mod_duration": 4},
    {"id": "curtain_call",       "name": "Curtain Call",       "type": "bard", "power_type": "debuff",  "damage_type": "magical", "trigger": "opponent_status","cooldown": 5, "damage": 8,  "skill_capacity_cost": 2, "status_apply": "shaken", "stat_mod": {"enemy": {"might": -4, "grace": -3, "cognition": -3, "insight": -2}}, "mod_duration": 3},
    # Master Tier (Level 15) — 1 Performance, 4 Buffs, 2 Debuffs, 1 Defend
    {"id": "song_of_fortune",    "name": "Song of Fortune",    "type": "bard", "power_type": "performance", "mode": "both", "trigger": "always", "cooldown": 0, "damage": 0, "skill_capacity_cost": 0, "crescendo": True, "encore": True, "song_effect": "reroll", "dance_effect": "burn", "dpt_percent": 0.05, "crescendo_scale": 0.02},
    {"id": "heros_anthem",       "name": "Hero's Anthem",      "type": "bard", "power_type": "buff",    "trigger": "opening_move",  "cooldown": 6, "damage": 0,  "skill_capacity_cost": 2, "self_status": "inspired", "stat_mod": {"all_allies": {"might": 3, "grace": 2, "armor_bonus": 2}}, "mod_duration": 4},
    {"id": "world_orchestra",    "name": "World Orchestra",    "type": "bard", "power_type": "buff",    "trigger": "always",        "cooldown": 6, "damage": 0,  "skill_capacity_cost": 3, "self_status": "inspired", "heal_percent": 0.10, "stat_mod": {"all_allies": {"might": 2, "grace": 2, "insight": 2, "essence": 1}}, "mod_duration": 4},
    {"id": "grand_performance",  "name": "Grand Performance",  "type": "bard", "power_type": "debuff",  "damage_type": "magical", "trigger": "always",        "cooldown": 6, "damage": 10, "skill_capacity_cost": 3, "status_apply": "stunned", "stat_mod": {"enemy": {"might": -4, "grace": -4, "cognition": -3, "insight": -2}}, "mod_duration": 3},
    {"id": "memory_song",        "name": "Memory Song",        "type": "bard", "power_type": "buff",    "trigger": "always",        "cooldown": 5, "damage": 0,  "skill_capacity_cost": 2, "self_status": "inspired", "stat_mod": {"all_allies": {"cognition": 3, "insight": 2, "grace": 1}}, "mod_duration": 4},
    {"id": "legend_keeper",      "name": "Legend Keeper",      "type": "bard", "power_type": "buff",    "trigger": "always",        "cooldown": 6, "damage": 0,  "skill_capacity_cost": 3, "self_status": "warded", "heal_percent": 0.10, "stat_mod": {"all_allies": {"might": 2, "grace": 2, "essence": 2, "durability": 1, "cognition": 1}}, "mod_duration": 4},
    {"id": "whispered_melody",   "name": "Whispered Melody",   "type": "bard", "power_type": "debuff",  "damage_type": "magical", "trigger": "always",        "cooldown": 5, "damage": 10, "skill_capacity_cost": 2, "status_apply": "shaken", "stat_mod": {"enemy": {"cognition": -4, "grace": -3, "might": -2, "insight": -2}}, "mod_duration": 3},
    {"id": "travelers_tune",     "name": "Traveler's Tune",    "type": "bard", "power_type": "defend",  "trigger": "always",        "cooldown": 6, "damage": 0,  "skill_capacity_cost": 2, "self_status": "warded", "heal_percent": 0.08, "stat_mod": {"all_allies": {"grace": 2, "durability": 2, "essence": 1}}, "mod_duration": 4},
    # Legendary Tier (Level 20) — 2 Performances
    {"id": "requiem_of_the_heavens","name": "Requiem of the Heavens","type": "bard","power_type": "performance","mode": "both","trigger": "always","cooldown": 0,"damage": 0,"skill_capacity_cost": 0,"crescendo": True,"encore": True,"song_effect": "all_rules_active","dance_effect": "total_control","heal_percent": 0.10,"damage_type": "true","dpt_percent": 0.08,"stun_chance": 0.15,"base_chance": 0.25,"crescendo_scale": 0.05},
    {"id": "symphony_of_creation","name": "Symphony of Creation","type": "bard","power_type": "performance","mode": "both","trigger": "low_hp","cooldown": 0,"damage": 0,"skill_capacity_cost": 0,"crescendo": True,"encore": True,"song_effect": "rewrite_existence","dance_effect": "total_domination","heal_percent": 0.15,"damage_type": "true","dpt_percent": 0.12,"stun_chance": 0.25,"base_chance": 0.40,"crescendo_scale": 0.08,"status_apply": "mesmerized"},
]

SKILL_EXTRAS: dict[str, dict] = {
    "shield_bash":    {"desc": "Bash the target with your shield, staggering them and inflicting Stunned.", "level_req": 1, "mastery_req": ["tank", "defender"], "weapon_req": "shield"},
    "sworn_strike":   {"desc": "A zealous overhead blow charged by oath and duty.", "level_req": 2, "mastery_req": ["paladin", "knight"], "weapon_req": "sword"},
    "smite":          {"desc": "Channel divine light to burn a wounded foe. Only usable when the enemy is already wounded.", "level_req": 3, "mastery_req": ["saint", "paladin"], "weapon_req": "mace"},
    "lay_on_hands":   {"desc": "Pour healing light into yourself or an ally. Usable only when your HP is low.", "level_req": 4, "mastery_req": ["saint", "druid"], "weapon_req": "none"},
    "thrust":         {"desc": "A quick, precise lunge to exploit an opening.", "level_req": 1, "mastery_req": ["duelist", "ranger"], "weapon_req": "spear"},
    "impale":         {"desc": "Drive your weapon deep into the enemy at the start of the fight. Causes Bleeding.", "level_req": 2, "mastery_req": ["duelist"], "weapon_req": "spear"},
    "backstab":       {"desc": "Strike from the shadows at the opening. Inflicts Bleeding.", "level_req": 2, "mastery_req": ["assassin"], "weapon_req": "dagger"},
    "vanish":         {"desc": "Fade into shadow, becoming Hidden. Usable only when your HP is low.", "level_req": 3, "mastery_req": ["assassin"], "weapon_req": "none"},
    "mocking_verse":  {"desc": "Sing a taunting verse that unnerves the target. Inflicts Shaken and reduces Might, Grace.", "level_req": 1, "mastery_req": ["bard"], "weapon_req": "none"},
    "rally":          {"desc": "Bolster allies with a rallying cry. Usable only when an ally is low on health.", "level_req": 3, "mastery_req": ["bard", "commander"], "weapon_req": "none"},
    "mix_potion":     {"desc": "Improvise a restorative draught from your pack. Usable only when your HP is low.", "level_req": 2, "mastery_req": ["alchemist", "druid"], "weapon_req": "none"},
    "acid_flask":     {"desc": "Hurl a flask of caustic liquid. Burns the target with acid.", "level_req": 2, "mastery_req": ["alchemist", "ranger"], "weapon_req": "none"},
    "arcane_bolt":    {"desc": "Loose a simple bolt of raw arcane energy.", "level_req": 1, "mastery_req": ["mage", "elementalist"], "weapon_req": "none"},
    "ward":           {"desc": "Raise a protective ward around yourself. Grants Warded.", "level_req": 2, "mastery_req": ["mage", "saint"], "weapon_req": "none"},
    "divine_light":   {"desc": "Blast the target with searing radiance when they are suffering an effect. Blinds them.", "level_req": 3, "mastery_req": ["saint"], "weapon_req": "none"},
    "purge":          {"desc": "Cleanse yourself of debilitating effects. Usable only when you are debuffed.", "level_req": 2, "mastery_req": ["saint", "druid"], "weapon_req": "none"},
    "thornlash":      {"desc": "Whip the foe with thorned vines. Causes Bleeding.", "level_req": 1, "mastery_req": ["druid", "ranger"], "weapon_req": "none"},
    "beast_call":     {"desc": "Call a beast companion to strike the target.", "level_req": 3, "mastery_req": ["druid", "ranger"], "weapon_req": "none"},
    "shadow_step":    {"desc": "Step through shadows, becoming Evasive.", "level_req": 3, "mastery_req": ["assassin", "shadow"], "weapon_req": "none"},
    "poison_blade":   {"desc": "Coat your blade in venom and cut the target. Inflicts Poisoned.", "level_req": 2, "mastery_req": ["assassin", "rogue"], "weapon_req": "dagger"},
    "aimed_shot":     {"desc": "Fire a carefully aimed shot at the start of combat.", "level_req": 2, "mastery_req": ["ranger", "hunter"], "weapon_req": "bow"},
    "trap":           {"desc": "Lay a snare that Ensnares the target.", "level_req": 2, "mastery_req": ["ranger", "hunter"], "weapon_req": "none"},
    "mend":           {"desc": "Weave flesh and spirit back together. Usable only when your HP is low.", "level_req": 3, "mastery_req": ["druid", "saint"], "weapon_req": "none"},
    # --- Alchemist Skills ---
    "acid_bomb":              {"desc": "Imbue the katar with acid. Each hit stacks armor shred (-1 more per hit). Liquid blade.", "level_req": 1, "mastery_req": ["alchemist"], "weapon_req": "katar"},
    "flash_powder_alch":      {"desc": "Imbue the katar with blinding powder. Each hit stacks accuracy drain. Mirror blade.", "level_req": 1, "mastery_req": ["alchemist"], "weapon_req": "katar"},
    "quick_jab":              {"desc": "A fast katar jab that never misses — ignores evasive and hidden.", "level_req": 1, "mastery_req": ["alchemist"], "weapon_req": "katar"},
    "heavy_crush":            {"desc": "A devastating overhead katar smash that permanently breaks armor.", "level_req": 1, "mastery_req": ["alchemist"], "weapon_req": "katar"},
    "healing_draught":        {"desc": "Drink a healing draught. Restores 10% HP and grants Warded.", "level_req": 1, "mastery_req": ["alchemist"], "weapon_req": "none"},
    "iron_skin_transmutation":{"desc": "Transmute your skin to iron. +4 Armor for 3 turns.", "level_req": 1, "mastery_req": ["alchemist"], "weapon_req": "none"},
    "frost_mixture":          {"desc": "Imbue the katar with frost. 4th hit freezes the enemy (skip turn). Ice spike blade.", "level_req": 3, "mastery_req": ["alchemist"], "weapon_req": "katar"},
    "lightning_bottle":       {"desc": "Imbue the katar with lightning. 3rd hit chains to adjacent enemy. Claw blade.", "level_req": 3, "mastery_req": ["alchemist"], "weapon_req": "katar"},
    "poison_capsule":         {"desc": "Imbue the katar with poison. Damage scales +10% per turn. Needle blade.", "level_req": 3, "mastery_req": ["alchemist"], "weapon_req": "katar"},
    "flurry":                 {"desc": "Three rapid katar hits. Triple CF gain and triple imbue mini-rule procs.", "level_req": 3, "mastery_req": ["alchemist"], "weapon_req": "katar"},
    "rushing_strike":         {"desc": "Gap-close strike that re-imbues the katar AND punches in the same action.", "level_req": 3, "mastery_req": ["alchemist"], "weapon_req": "katar"},
    "swift_transmutation":    {"desc": "Transmute your legs for speed. +4 Grace, +1 Might, Evasive for 3 turns.", "level_req": 3, "mastery_req": ["alchemist"], "weapon_req": "none"},
    "stone_wall":             {"desc": "Transmute your body to stone. Warded, +2 Grace for 2 turns.", "level_req": 3, "mastery_req": ["alchemist"], "weapon_req": "none"},
    "corrosive_mist":         {"desc": "Imbue with corrosive mist. +50% armor reduction per status on enemy. Eroding blade.", "level_req": 8, "mastery_req": ["alchemist"], "weapon_req": "katar"},
    "living_slime":           {"desc": "Imbue with living slime. 3rd hit immobilizes (no movement, can attack). Whip blade.", "level_req": 8, "mastery_req": ["alchemist"], "weapon_req": "katar"},
    "transmutation_touch":    {"desc": "Imbue with transmutation. 2nd hit sets enemy armor to 0. Dull edge blade.", "level_req": 8, "mastery_req": ["alchemist"], "weapon_req": "katar"},
    "explosive_chain":        {"desc": "Imbue with explosive reactive surface. Every strike hits 2x. Jagged blade.", "level_req": 8, "mastery_req": ["alchemist"], "weapon_req": "katar"},
    "spinning_strike":        {"desc": "Spin with katar extended, hitting primary + adjacent, then reposition behind enemy.", "level_req": 8, "mastery_req": ["alchemist"], "weapon_req": "katar"},
    "piercing_strike":        {"desc": "Focused thrust ignoring 50% of enemy armor. Deep imbue delivery.", "level_req": 8, "mastery_req": ["alchemist"], "weapon_req": "katar"},
    "counter_strike":         {"desc": "Reactive strike that interrupts enemy casting, canceling their skill.", "level_req": 8, "mastery_req": ["alchemist"], "weapon_req": "katar"},
    "forbidden_formula":      {"desc": "Forbidden imbue — all statuses + true damage, 1 charge. Shifting blade. Cracks katar after.", "level_req": 15, "mastery_req": ["alchemist"], "weapon_req": "katar"},
    "guard_break":            {"desc": "Breaks enemy stance — removes Warded and prevents re-warding for 2 turns.", "level_req": 15, "mastery_req": ["alchemist"], "weapon_req": "katar"},
    "rising_strike":          {"desc": "Upward slash launching enemy airborne — they can't act next turn.", "level_req": 15, "mastery_req": ["alchemist"], "weapon_req": "katar"},
    "executioner_strike":     {"desc": "Consumes ALL Combo Flow for +10% damage per CF. +50% below 30% HP.", "level_req": 15, "mastery_req": ["alchemist"], "weapon_req": "katar"},
    "mutagen_injection":      {"desc": "Inject mutagen — +4 Might, +3 Grace, +2 Durability, Inspired for 3 turns.", "level_req": 15, "mastery_req": ["alchemist"], "weapon_req": "none"},
    "phoenix_mixture":        {"desc": "Transmute blood to fire. Heals 15%, Warded, +4 Armor for 3 turns.", "level_req": 15, "mastery_req": ["alchemist"], "weapon_req": "none"},
    "smoke_transmutation":    {"desc": "Transmute to smoke. Hidden, +3 Grace for 2 turns.", "level_req": 15, "mastery_req": ["alchemist"], "weapon_req": "none"},
    "spike_field":            {"desc": "Transmute the ground to spikes. Ensnares enemy, -2 Might and Grace for 3 turns.", "level_req": 15, "mastery_req": ["alchemist"], "weapon_req": "none"},
    "philosophers_transmutation": {"desc": "Transmute body to perfect form. Heals 30%, all stats +3, infinite imbue charges + max mini-rules for 4 turns.", "level_req": 20, "mastery_req": ["alchemist"], "weapon_req": "none"},
    "legend_of_alchemy":      {"desc": "8-hit true damage strike. Katar auto-adapts each hit to optimal imbue. Heals 25%, Inspired.", "level_req": 20, "mastery_req": ["alchemist"], "weapon_req": "katar"},
    # --- Paladin Skills ---
    "shield_of_faith":       {"desc": "A glowing crest surrounds the Paladin, raising armor and magical resistance with divine protection.", "level_req": 1, "mastery_req": ["paladin"], "weapon_req": "none"},
    "blessed_strike":        {"desc": "Holy symbols ignite along the blade, dealing magical damage and shaking the enemy's resolve.", "level_req": 1, "mastery_req": ["paladin"], "weapon_req": "sword"},
    "merciful_touch":        {"desc": "The Paladin places a hand upon their wounds, restoring 10% HP. Amplified by low-HP scaling.", "level_req": 1, "mastery_req": ["paladin"], "weapon_req": "none"},
    "hammer_of_light":       {"desc": "The Paladin's hammer crashes down with divine weight, stunning the enemy and denting armor.", "level_req": 1, "mastery_req": ["paladin"], "weapon_req": "mace"},
    "divine_aegis":          {"desc": "Channels faith into a protective aura reinforcing armor, magical resistance, and vitality.", "level_req": 1, "mastery_req": ["paladin"], "weapon_req": "none"},
    "lightbearers_oath":     {"desc": "An oath echoes with celestial authority, strengthening defenses as battle begins. Opening move.", "level_req": 1, "mastery_req": ["paladin"], "weapon_req": "none"},
    "sacred_charge":         {"desc": "The Paladin charges with divine momentum, crashing into the enemy and shattering their guard.", "level_req": 3, "mastery_req": ["paladin"], "weapon_req": "mace"},
    "judgment_hammer":        {"desc": "A pillar of light crashes from the heavens, hammering the enemy with divine judgment.", "level_req": 3, "mastery_req": ["paladin"], "weapon_req": "mace"},
    "holy_barrier":          {"desc": "A luminous sigil expands into a radiant dome, shielding from both physical and magical harm.", "level_req": 3, "mastery_req": ["paladin"], "weapon_req": "none"},
    "consecrate_blade":      {"desc": "Runes crawl across the weapon, enchanting it with holy power. Boosts essence and might.", "level_req": 3, "mastery_req": ["paladin"], "weapon_req": "sword"},
    "sunburst":               {"desc": "An explosion of sunlight erupts outward, blinding the enemy and reducing accuracy.", "level_req": 3, "mastery_req": ["paladin"], "weapon_req": "none"},
    "divine_radiance":        {"desc": "Warm holy light washes over the Paladin, healing 12% HP and fortifying defenses. Amplified at low HP.", "level_req": 3, "mastery_req": ["paladin"], "weapon_req": "none"},
    "guardians_blessing":    {"desc": "A sacred emblem glows, reinforcing armor, magical resistance, and vitality.", "level_req": 3, "mastery_req": ["paladin"], "weapon_req": "none"},
    "divine_intercession":   {"desc": "When near death, divine power surges — massively boosting armor and magical resistance.", "level_req": 8, "mastery_req": ["paladin"], "weapon_req": "none"},
    "lay_on_hands_paladin":  {"desc": "Channels raw divine energy through the body, healing 15% HP. Amplified by low-HP scaling.", "level_req": 8, "mastery_req": ["paladin"], "weapon_req": "none"},
    "exorcism":               {"desc": "Sacred words force darkness to flee, shattering the enemy's resolve and weakening power.", "level_req": 8, "mastery_req": ["paladin"], "weapon_req": "none"},
    "celestial_spear":        {"desc": "A blazing lance of light pierces the enemy, leaving them bleeding and vulnerable.", "level_req": 8, "mastery_req": ["paladin"], "weapon_req": "sword"},
    "divine_resolve":         {"desc": "Faith overcomes despair, cleansing debuffs and fortifying body and spirit.", "level_req": 8, "mastery_req": ["paladin"], "weapon_req": "none"},
    "faiths_bulwark":         {"desc": "Faith crystallizes into a living fortress — boosting armor, magical resistance, and vitality.", "level_req": 8, "mastery_req": ["paladin"], "weapon_req": "none"},
    "last_stand":              {"desc": "When on the brink, faith erupts — healing 20% HP and hardening defenses. Amplified at low HP.", "level_req": 8, "mastery_req": ["paladin"], "weapon_req": "none"},
    "holy_nova":               {"desc": "Light expands in every direction — healing 15% HP and hardening defenses.", "level_req": 15, "mastery_req": ["paladin"], "weapon_req": "none"},
    "sanctuary":               {"desc": "A peaceful aura surrounds the Paladin, declaring the ground sacred. Massive defensive boost.", "level_req": 15, "mastery_req": ["paladin"], "weapon_req": "none"},
    "justice_descends":        {"desc": "A divine verdict falls from above, punishing the wounded enemy with heavenly force.", "level_req": 15, "mastery_req": ["paladin"], "weapon_req": "mace"},
    "guardians_crown":         {"desc": "A glowing crown appears above the Paladin, boosting all defenses with divine authority.", "level_req": 15, "mastery_req": ["paladin"], "weapon_req": "none"},
    "resurrection_prayer":     {"desc": "A heartfelt prayer rekindles fading life, restoring 35% HP when on the brink. Amplified at low HP.", "level_req": 15, "mastery_req": ["paladin"], "weapon_req": "none"},
    "consecrated_ground":      {"desc": "The Paladin consecrates the battlefield, bathing it in holy light that heals and fortifies.", "level_req": 15, "mastery_req": ["paladin"], "weapon_req": "none"},
    "divine_wrath":            {"desc": "The Paladin's hammer descends with divine fury, crushing the wounded enemy's armor.", "level_req": 15, "mastery_req": ["paladin"], "weapon_req": "mace"},
    "guardian_angel":          {"desc": "A translucent angel hovers near the Paladin, mending wounds and fortifying defenses.", "level_req": 15, "mastery_req": ["paladin"], "weapon_req": "none"},
    "last_judgment":           {"desc": "A heavenly sword descends from the sky, delivering true damage execution. Bonus vs undead/devils.", "level_req": 20, "mastery_req": ["paladin"], "weapon_req": "sword"},
    "ascension_of_the_light":  {"desc": "The Paladin becomes an avatar of divine endurance. True damage, heals 30%, devastates enemy stats.", "level_req": 20, "mastery_req": ["paladin"], "weapon_req": "sword"},
    # --- Knight Skills ---
    "iron_stance":       {"desc": "Plant feet, lock stance. +2 Armor, +2 Might for 3 turns.", "level_req": 1, "mastery_req": ["knight"], "weapon_req": "none"},
    "war_cry":           {"desc": "A battle cry hardening resolve. +3 Might for 3 turns. Opening move.", "level_req": 1, "mastery_req": ["knight"], "weapon_req": "none"},
    "vanguard_step":     {"desc": "Step forward, shield raised. +3 Armor for 3 turns.", "level_req": 1, "mastery_req": ["knight"], "weapon_req": "none"},
    "pommel_strike":     {"desc": "Reverse grip, drive pommel into face. Stuns, -2 Might and -1 Grace.", "level_req": 1, "mastery_req": ["knight"], "weapon_req": "sword"},
    "steady_grip":       {"desc": "Adjust grip on sword and shield. +2 Might, +2 Armor for 3 turns.", "level_req": 1, "mastery_req": ["knight"], "weapon_req": "none"},
    "kings_challenge":   {"desc": "Plant sword, raise shield, roar a challenge. Shaken, -3 Might.", "level_req": 3, "mastery_req": ["knight"], "weapon_req": "none"},
    "lions_charge":      {"desc": "Lower shoulder and charge. Stuns, -3 Armor. Opening move.", "level_req": 3, "mastery_req": ["knight"], "weapon_req": "none"},
    "heavy_strike":      {"desc": "Overhead blow with full weight. Shaken, -3 Armor for 3 turns.", "level_req": 3, "mastery_req": ["knight"], "weapon_req": "sword"},
    "bulwark":           {"desc": "Brace into a fortified position. +4 Armor, +3 Might for 4 turns.", "level_req": 3, "mastery_req": ["knight"], "weapon_req": "none"},
    "banner_of_valor":   {"desc": "Plant personal banner. +3 Might, +2 Armor for 4 turns.", "level_req": 3, "mastery_req": ["knight"], "weapon_req": "none"},
    "fortress_breaker":  {"desc": "Two-handed overhead that shatters defenses. Bleeding, -4 Armor.", "level_req": 3, "mastery_req": ["knight"], "weapon_req": "sword"},
    "plate_armor_mastery":{"desc": "Align every strap and plate. +5 Armor, +3 Durability for 4 turns.", "level_req": 3, "mastery_req": ["knight"], "weapon_req": "none"},
    "shield_wall":       {"desc": "Slam shield forward and lock. +5 Armor, +2 Durability for 4 turns.", "level_req": 8, "mastery_req": ["knight"], "weapon_req": "shield"},
    "guardians_sacrifice":{"desc": "Wounded and cornered, channel pain into defiance. +5 Armor, +3 Might. Low HP.", "level_req": 8, "mastery_req": ["knight"], "weapon_req": "none"},
    "commanding_presence":{"desc": "Stand to full height, radiate authority. +4 Might, +3 Armor for 4 turns.", "level_req": 8, "mastery_req": ["knight"], "weapon_req": "none"},
    "crushing_blow":     {"desc": "Capitalize on wounded enemy. Shaken, -5 Armor, -3 Might. Opponent wounded.", "level_req": 8, "mastery_req": ["knight"], "weapon_req": "sword"},
    "unbreakable_will":  {"desc": "Burn away debuffs through oath. +3 Durability, +3 Armor. Self-debuff trigger.", "level_req": 8, "mastery_req": ["knight"], "weapon_req": "none"},
    "titans_strength":   {"desc": "Channel raw physical power. +5 Might, +2 Armor for 4 turns.", "level_req": 8, "mastery_req": ["knight"], "weapon_req": "none"},
    "ground_slam":       {"desc": "Drive weapon into earth, shockwave. Stuns, -3 Might, -3 Armor.", "level_req": 8, "mastery_req": ["knight"], "weapon_req": "none"},
    "iron_formation":    {"desc": "Become an immovable fortress. +8 Armor, +4 Durability for 4 turns.", "level_req": 15, "mastery_req": ["knight"], "weapon_req": "none"},
    "royal_execution":   {"desc": "Patient executioner's strike on wounded enemy. Bleeding, -4 Might, -3 Armor.", "level_req": 15, "mastery_req": ["knight"], "weapon_req": "sword"},
    "guardians_oath":    {"desc": "Speak the Oath aloud. +4 Might, +4 Armor, +3 Durability for 4 turns.", "level_req": 15, "mastery_req": ["knight"], "weapon_req": "none"},
    "warlords_fury":     {"desc": "Wounded fury, massive might surge. +6 Might, +3 Armor. Low HP.", "level_req": 15, "mastery_req": ["knight"], "weapon_req": "none"},
    "crown_of_iron":     {"desc": "Assume the stance of a ruler. +6 Armor, +4 Might, +3 Durability for 4 turns.", "level_req": 15, "mastery_req": ["knight"], "weapon_req": "none"},
    "kings_command":    {"desc": "A royal decree to yourself. +5 Might, +3 Armor, +2 Durability for 4 turns.", "level_req": 15, "mastery_req": ["knight"], "weapon_req": "none"},
    "last_bastion":      {"desc": "Surrounded and wounded, refuse to fall. +7 Armor, +5 Durability, +3 Might. Low HP.", "level_req": 15, "mastery_req": ["knight"], "weapon_req": "none"},
    "oath_strike":       {"desc": "Channel every Oath stack into one blow. Bleeding, -3 Might, -3 Armor, -2 Grace.", "level_req": 15, "mastery_req": ["knight"], "weapon_req": "sword"},
    "final_duel":        {"desc": "Challenge to single combat. True damage, bleeding, -5 Might/Grace/Armor.", "level_req": 20, "mastery_req": ["knight"], "weapon_req": "sword"},
    "legend_of_erchis": {"desc": "Channel every Oath ever sworn. True damage, stuns, devastates enemy stats. Low HP.", "level_req": 20, "mastery_req": ["knight"], "weapon_req": "sword"},
    # --- Lancer Skills ---
    "flame_imbue":        {"desc": "Ignite lance with fire. +2 Might. Strikes apply burning.", "level_req": 1, "mastery_req": ["lancer"], "weapon_req": "spear"},
    "frost_imbue":        {"desc": "Encase lance in ice. +2 Might, +1 Grace, -2 enemy Grace. Strikes apply ensnared.", "level_req": 1, "mastery_req": ["lancer"], "weapon_req": "spear"},
    "gale_thrust":        {"desc": "Lightning-fast thrust with wind spiral. -1 enemy Grace.", "level_req": 1, "mastery_req": ["lancer"], "weapon_req": "spear"},
    "lancer_guard_break": {"desc": "Precise thrust through shields. -3 enemy Armor.", "level_req": 1, "mastery_req": ["lancer"], "weapon_req": "spear"},
    "cyclone_wall":       {"desc": "Spin spear to deflect projectiles. Evasive, +2 Grace.", "level_req": 1, "mastery_req": ["lancer"], "weapon_req": "spear"},
    "warriors_focus":     {"desc": "Center yourself. +2 Grace, +2 Might for 3 turns.", "level_req": 1, "mastery_req": ["lancer"], "weapon_req": "none"},
    "storm_imbue":        {"desc": "Call lightning into lance. +3 Might, +2 Grace. Strikes apply stunned.", "level_req": 3, "mastery_req": ["lancer"], "weapon_req": "spear"},
    "stone_imbue":        {"desc": "Reinforce lance with earth. +3 Might, +2 Armor, -2 enemy Armor. Strikes apply shaken.", "level_req": 3, "mastery_req": ["lancer"], "weapon_req": "spear"},
    "sky_piercer":        {"desc": "Explode forward, spear tearing through armor. Bleeding, -4 enemy Armor.", "level_req": 3, "mastery_req": ["lancer"], "weapon_req": "spear"},
    "falcon_rush":        {"desc": "Close distance and strike before enemy reacts. Stunned, -2 enemy Grace. Opening move.", "level_req": 3, "mastery_req": ["lancer"], "weapon_req": "spear"},
    "dragon_fang":        {"desc": "Brutal armor-piercing stab. Bleeding, -3 enemy Armor, -2 enemy Might.", "level_req": 3, "mastery_req": ["lancer"], "weapon_req": "spear"},
    "elemental_weakness": {"desc": "Exploit gaps in defenses. -3 enemy Might/Grace, -2 Armor.", "level_req": 3, "mastery_req": ["lancer"], "weapon_req": "spear"},
    "battle_readiness":   {"desc": "Enter combat with heightened reflexes. Evasive, +3 Grace, +2 Might. Opening move.", "level_req": 3, "mastery_req": ["lancer"], "weapon_req": "none"},
    "gale_imbue":         {"desc": "Wrap lance in wind. Evasive, +4 Grace, +2 Might. Strikes gain accuracy/crit.", "level_req": 8, "mastery_req": ["lancer"], "weapon_req": "spear"},
    "thunder_imbue":      {"desc": "Channel thunder into lance. +4 Insight, +2 Might, -2 enemy Essence. Strikes apply shaken.", "level_req": 8, "mastery_req": ["lancer"], "weapon_req": "spear"},
    "dragon_dive":        {"desc": "Vault skyward, descend like a falling dragon. Stunned, -4 enemy Armor, -2 Might. Opening move.", "level_req": 8, "mastery_req": ["lancer"], "weapon_req": "spear"},
    "frostbite":           {"desc": "Drive ice into enemy wounds. Ensnared, -4 enemy Grace, -3 Might. Opponent status.", "level_req": 8, "mastery_req": ["lancer"], "weapon_req": "spear"},
    "shock_lock":          {"desc": "Channel lightning into wounds. Stunned, -4 enemy Might, -3 Grace. Opponent status.", "level_req": 8, "mastery_req": ["lancer"], "weapon_req": "spear"},
    "iron_breeze":         {"desc": "Weave wind and steel defensively. Evasive, +3 Grace, +2 Armor.", "level_req": 8, "mastery_req": ["lancer"], "weapon_req": "spear"},
    "elemental_surge":     {"desc": "Surge all elemental energy. Evasive, +3 Grace/Insight, +2 Might.", "level_req": 8, "mastery_req": ["lancer"], "weapon_req": "none"},
    "inferno_imbue":       {"desc": "Advanced fire imbue. +5 Might, +2 Grace, -3 enemy Armor. Strikes apply burning.", "level_req": 15, "mastery_req": ["lancer"], "weapon_req": "spear"},
    "glacier_imbue":       {"desc": "Advanced ice imbue. +4 Might, +3 Grace, -4 enemy Grace, -2 Might. Strikes apply ensnared.", "level_req": 15, "mastery_req": ["lancer"], "weapon_req": "spear"},
    "tempest_imbue":       {"desc": "Advanced lightning imbue. +5 Might, +3 Grace, -3 enemy Might/Grace. Strikes apply stunned.", "level_req": 15, "mastery_req": ["lancer"], "weapon_req": "spear"},
    "volcano_imbue":       {"desc": "Fire+earth fusion imbue. +5 Might, +3 Armor, -4 enemy Armor, -3 Might. Strikes apply burning+shaken.", "level_req": 15, "mastery_req": ["lancer"], "weapon_req": "spear"},
    "thunder_pursuit":     {"desc": "Chase fleeing enemies with thunder. Stunned, -3 enemy Grace/Might. Opponent wounded.", "level_req": 15, "mastery_req": ["lancer"], "weapon_req": "spear"},
    "world_splitter":     {"desc": "Split the ground with one thrust. Stunned, -6 enemy Armor, -3 Might. Opponent wounded.", "level_req": 15, "mastery_req": ["lancer"], "weapon_req": "spear"},
    "crimson_spear":      {"desc": "Channel desperation into power. Bleeding, +5 Might, -4 enemy Armor, -3 Might. Low HP.", "level_req": 15, "mastery_req": ["lancer"], "weapon_req": "spear"},
    "elemental_collapse": {"desc": "Detonate all elemental energy in enemy wounds. -5 Might/Grace, -4 Armor, -3 Essence. Opponent wounded.", "level_req": 15, "mastery_req": ["lancer"], "weapon_req": "spear"},
    "celestial_javelin":  {"desc": "Divine spear of pure elemental light. True damage, bleeding, devastates enemy stats.", "level_req": 20, "mastery_req": ["lancer"], "weapon_req": "spear"},
    "avatar_of_the_storm":{"desc": "Become one with all elements. True damage, stuns, all stats crushed. Low HP.", "level_req": 20, "mastery_req": ["lancer"], "weapon_req": "spear"},
    # --- Mage Skills ---
    "arcane_burst":       {"desc": "Compress arcane energy into a sphere and hurl it. -1 enemy Grace.", "level_req": 1, "mastery_req": ["mage"], "weapon_req": "none"},
    "wind_blade":         {"desc": "Sweep compressed wind at the enemy. Bleeding, -2 enemy Grace.", "level_req": 1, "mastery_req": ["mage"], "weapon_req": "none"},
    "stone_spear":        {"desc": "Tear stone from the ground and launch it. Bleeding, -2 enemy Armor.", "level_req": 1, "mastery_req": ["mage"], "weapon_req": "none"},
    "arcane_ward":        {"desc": "Draw interlocking runes of blue energy. Grants Warded, +3 Essence.", "level_req": 1, "mastery_req": ["mage"], "weapon_req": "none"},
    "blink":              {"desc": "Vanish and reappear nearby. Grants Evasive, +4 Grace.", "level_req": 1, "mastery_req": ["mage"], "weapon_req": "none"},
    "water_lash":         {"desc": "Draw moisture and snap it forward. Stunned, -2 enemy Grace.", "level_req": 1, "mastery_req": ["mage"], "weapon_req": "none"},
    "fireball":           {"desc": "Trace a burning circle and launch fire. Burning, -3 enemy Armor.", "level_req": 3, "mastery_req": ["mage"], "weapon_req": "none"},
    "frost_prison":       {"desc": "Ice climbs the enemy's body and seals them. Ensnared, -3 Grace, -2 Might.", "level_req": 3, "mastery_req": ["mage"], "weapon_req": "none"},
    "chain_lightning":    {"desc": "Lightning crashes and leaps between foes. 2 hits, stunned, -2 Grace.", "level_req": 3, "mastery_req": ["mage"], "weapon_req": "none"},
    "mana_shield":        {"desc": "Mana spreads across skin, dispersing attacks. Warded, +4 Essence, +2 Armor.", "level_req": 3, "mastery_req": ["mage"], "weapon_req": "none"},
    "spell_seal":         {"desc": "Lock-shaped sigil silences enemy magic. Shaken, -4 Insight, -3 Cognition.", "level_req": 3, "mastery_req": ["mage"], "weapon_req": "none"},
    "arcane_chains":      {"desc": "Chains of energy rise from runes beneath the enemy. Ensnared, -3 Grace/Might. Opponent has status.", "level_req": 3, "mastery_req": ["mage"], "weapon_req": "none"},
    "illusory_double":    {"desc": "Split into identical figures. Grants Evasive, +5 Grace.", "level_req": 3, "mastery_req": ["mage"], "weapon_req": "none"},
    "gravity_well":       {"desc": "A dark sphere pulls everything inward. Ensnared, -4 Grace, -3 Might, -2 Cognition.", "level_req": 8, "mastery_req": ["mage"], "weapon_req": "none"},
    "telekinetic_crush":  {"desc": "Lift and squeeze the enemy with invisible force. Stunned, -4 Might, -3 Armor. Opponent wounded.", "level_req": 8, "mastery_req": ["mage"], "weapon_req": "none"},
    "mirror_spell":       {"desc": "Reflect incoming spells back at the caster. Warded, +4 Essence, +2 Grace.", "level_req": 8, "mastery_req": ["mage"], "weapon_req": "none"},
    "mind_maze":          {"desc": "Whisper a word that turns the battlefield into a labyrinth. Shaken, -5 Cognition. Opponent has status.", "level_req": 8, "mastery_req": ["mage"], "weapon_req": "none"},
    "void_portal":        {"desc": "Tear space open and step through. Grants Evasive, +4 Grace, +2 Essence.", "level_req": 8, "mastery_req": ["mage"], "weapon_req": "none"},
    "phantom_terrain":    {"desc": "Distort the battlefield with false terrain. Shaken, -3 Grace/Cognition, -2 Might.", "level_req": 8, "mastery_req": ["mage"], "weapon_req": "none"},
    "dream_step":         {"desc": "Fade into mist and travel through the enemy's mind. Grants Hidden, +4 Grace, +2 Cognition.", "level_req": 8, "mastery_req": ["mage"], "weapon_req": "none"},
    "meteor_storm":       {"desc": "Rain burning stones from the sky. 3 hits, burning, -4 Armor, -3 Grace.", "level_req": 15, "mastery_req": ["mage"], "weapon_req": "none"},
    "blizzard":           {"desc": "Snow and ice roar outward in a blinding storm. Ensnared, -4 Grace, -3 Might, -2 Cognition.", "level_req": 15, "mastery_req": ["mage"], "weapon_req": "none"},
    "thunderfield":       {"desc": "Lightning hammers a marked zone repeatedly. Stunned, -3 Grace/Armor, -2 Might.", "level_req": 15, "mastery_req": ["mage"], "weapon_req": "none"},
    "time_slow":          {"desc": "Turn an invisible wheel and slow the world. Shaken, -5 Grace, -4 Might, -3 Cognition.", "level_req": 15, "mastery_req": ["mage"], "weapon_req": "none"},
    "elemental_convergence":{"desc": "All five elements compress and detonate. 2 hits, burning, -4 Armor, -3 Grace, -2 Might.", "level_req": 15, "mastery_req": ["mage"], "weapon_req": "none"},
    "mana_explosion":     {"desc": "Release all mana in a circular wave of force. Stunned, +3 Might, -5 Armor, -4 Grace, -3 Might. Low HP.", "level_req": 15, "mastery_req": ["mage"], "weapon_req": "none"},
    "reality_fracture":   {"desc": "Crack reality itself. Stunned, -5 Might/Grace, -4 Armor, -3 Cognition. Opponent wounded.", "level_req": 15, "mastery_req": ["mage"], "weapon_req": "none"},
    "time_stop":          {"desc": "Freeze the world and reposition. Warded, heals 10%, +5 Grace, +3 Essence. Low HP.", "level_req": 15, "mastery_req": ["mage"], "weapon_req": "none"},
    "cosmic_convergence": {"desc": "Align symbols like stars and descend a celestial beam. True damage, stunned, inspired, devastates enemy stats.", "level_req": 20, "mastery_req": ["mage"], "weapon_req": "none"},
    "legend_of_the_arcane":{"desc": "Cast every element in sequence — 8 hits, all true damage. Stunned, inspired, heals 15%. Low HP.", "level_req": 20, "mastery_req": ["mage"], "weapon_req": "none"},
    # --- Assassin Skills ---
    "shadow_strike":      {"desc": "Quick slash infused with shadow. Bleeding, -2 enemy Grace.", "level_req": 1, "mastery_req": ["assassin"], "weapon_req": "dagger"},
    "backstab":           {"desc": "Strike from behind for devastating damage. Bleeding, -3 Grace, -2 Might. Opening move.", "level_req": 1, "mastery_req": ["assassin"], "weapon_req": "dagger"},
    "heart_piercer":      {"desc": "Blade slips between armor plates. -2 enemy Armor, -1 Might.", "level_req": 1, "mastery_req": ["assassin"], "weapon_req": "dagger"},
    "smoke_veil":         {"desc": "Throw smoke pellet and become hidden. +3 Grace. 100% evasion until attack.", "level_req": 1, "mastery_req": ["assassin"], "weapon_req": "none"},
    "death_mark":         {"desc": "Mark enemy with shadow sigil. Shaken, -3 Grace/Armor, -2 Might.", "level_req": 1, "mastery_req": ["assassin"], "weapon_req": "dagger"},
    "shadow_focus":       {"desc": "Draw ambient shadows inward. +3 Grace, +2 Might for 3 turns.", "level_req": 1, "mastery_req": ["assassin"], "weapon_req": "none"},
    "silent_execution":   {"desc": "One clean slash ends the encounter. Bleeding, -3 Grace, -2 Might. Opening move.", "level_req": 3, "mastery_req": ["assassin"], "weapon_req": "dagger"},
    "phantom_strike":     {"desc": "Two rapid strikes with afterimages. Bleeding, -2 Grace. 2 hits.", "level_req": 3, "mastery_req": ["assassin"], "weapon_req": "dagger"},
    "crimson_dash":       {"desc": "Dash through enemy leaving shadow and blood. Bleeding, -2 Grace/Armor.", "level_req": 3, "mastery_req": ["assassin"], "weapon_req": "dagger"},
    "night_veil":         {"desc": "Wrap in living shadow, become hidden. +4 Grace, +2 Might. Stronger stealth.", "level_req": 3, "mastery_req": ["assassin"], "weapon_req": "none"},
    "shadow_terror":       {"desc": "Flood enemy mind with shadow. Shaken, -4 Might, -3 Grace, -2 Cognition.", "level_req": 3, "mastery_req": ["assassin"], "weapon_req": "dagger"},
    "shadowstep":          {"desc": "Melt into darkness and reappear. Evasive, +4 Grace. Quick repositioning.", "level_req": 3, "mastery_req": ["assassin"], "weapon_req": "none"},
    "dark_pursuit":       {"desc": "Relentlessly chase fleeing prey. Bleeding, -3 Grace, -2 Might. Opponent wounded.", "level_req": 3, "mastery_req": ["assassin"], "weapon_req": "dagger"},
    "vanishing_kill":      {"desc": "Strike and vanish in same motion. Bleeding, hidden, -3 Grace, -2 Might. Opponent status.", "level_req": 8, "mastery_req": ["assassin"], "weapon_req": "dagger"},
    "shadow_flurry":      {"desc": "Three rapid shadow-infused strikes. Bleeding, -3 Grace, -2 Armor. 3 hits.", "level_req": 8, "mastery_req": ["assassin"], "weapon_req": "dagger"},
    "soul_sever":         {"desc": "Blade glows with shadow, damages body and spirit. Shaken, -3 Might/Essence, -2 Grace.", "level_req": 8, "mastery_req": ["assassin"], "weapon_req": "dagger"},
    "shadow_clone":       {"desc": "Split into illusionary duplicate, become hidden. +5 Grace. +20 shadows on break.", "level_req": 8, "mastery_req": ["assassin"], "weapon_req": "none"},
    "shadow_prison":      {"desc": "Living shadows bind enemy. Shaken, -4 Grace, -3 Might, -2 Cognition.", "level_req": 8, "mastery_req": ["assassin"], "weapon_req": "dagger"},
    "black_feathers":     {"desc": "Dark feathers fill air as you escape. Hidden, +5 Grace. Low HP.", "level_req": 8, "mastery_req": ["assassin"], "weapon_req": "none"},
    "eclipse_blade":      {"desc": "Blade absorbs light, empowered by darkness. +4 Might, +3 Grace, +2 Insight.", "level_req": 8, "mastery_req": ["assassin"], "weapon_req": "dagger"},
    "shadow_convergence": {"desc": "Draw all nearby shadows into yourself. +5 Grace, +4 Might, +3 Insight. Surges shadows +25.", "level_req": 15, "mastery_req": ["assassin"], "weapon_req": "none"},
    "night_requiem":     {"desc": "Dance through enemy with 3 shadow cuts. Bleeding, -3 Grace/Armor, -2 Might. 3 hits.", "level_req": 15, "mastery_req": ["assassin"], "weapon_req": "dagger"},
    "deaths_whisper":     {"desc": "Chilling whisper devastates all stats. Shaken, -5 Might, -4 Grace, -3 Cognition, -2 Essence. Opponent wounded.", "level_req": 15, "mastery_req": ["assassin"], "weapon_req": "dagger"},
    "umbral_cloak":       {"desc": "Wrap in cloak of pure shadow, hidden. +5 Grace, +3 Might. Strongest stealth.", "level_req": 15, "mastery_req": ["assassin"], "weapon_req": "none"},
    "final_contract":    {"desc": "Accept any price for victory. Bleeding, +4 Might, +3 Grace, -5 enemy Armor/Might/Grace. Low HP.", "level_req": 15, "mastery_req": ["assassin"], "weapon_req": "dagger"},
    "king_slayer":       {"desc": "Technique to eliminate high-value targets. Bleeding, -5 Might/Armor, -4 Grace, -3 Durability. Opponent wounded.", "level_req": 15, "mastery_req": ["assassin"], "weapon_req": "dagger"},
    "shadow_devour":     {"desc": "Devour all fear on enemy into devastating strike. Stunned, -5 Might/Grace, -4 Essence, -3 Cognition. Opponent status.", "level_req": 15, "mastery_req": ["assassin"], "weapon_req": "dagger"},
    "eclipse_burst":     {"desc": "Channel all shadows into one strike. Stunned, -5 Might/Grace/Armor. Triggers BURST at 100.", "level_req": 15, "mastery_req": ["assassin"], "weapon_req": "dagger"},
    "reapers_arrival":   {"desc": "Battlefield grows silent as you approach. True damage, stuns, hidden. Devastates all stats.", "level_req": 20, "mastery_req": ["assassin"], "weapon_req": "dagger"},
    "eclipse_of_shadows":{"desc": "Become the ultimate shadow. True damage, stuns, hidden. All stats crushed. Low HP. Auto-BURST.", "level_req": 20, "mastery_req": ["assassin"], "weapon_req": "dagger"},
    # --- Hunter Skills ---
    "rapid_shot":        {"desc": "Two quick arrows. Low damage each, builds Spirit Guidance fast. -1 enemy Grace.", "level_req": 1, "mastery_req": ["hunter"], "weapon_req": "bow"},
    "piercing_shot":     {"desc": "Arrow drilled through defenses. -3 enemy Armor. Finds the gaps.", "level_req": 1, "mastery_req": ["hunter"], "weapon_req": "bow"},
    "snare_trap":        {"desc": "Thrown net of steel cables. Ensnared, -2 enemy Grace/Might. Buys time.", "level_req": 1, "mastery_req": ["hunter"], "weapon_req": "none"},
    "camouflage":        {"desc": "Blend into terrain, become hidden. +3 Grace. Enables Ambush.", "level_req": 1, "mastery_req": ["hunter"], "weapon_req": "none"},
    "eagle_eye":         {"desc": "Narrow vision to only the target. +4 Grace, inspired for 3 turns.", "level_req": 1, "mastery_req": ["hunter"], "weapon_req": "none"},
    "crippling_shot":    {"desc": "Arrow strikes the leg. Ensnared, -3 Might, -2 Grace. Enemy can't close distance.", "level_req": 1, "mastery_req": ["hunter"], "weapon_req": "bow"},
    "poison_arrow":      {"desc": "Dark green venom on arrowhead. Poisoned, -2 Might. Damage over time.", "level_req": 3, "mastery_req": ["hunter"], "weapon_req": "bow"},
    "flash_bang":        {"desc": "Thrown charge detonates in light and noise. Stunned, -3 Grace. Favorite opener.", "level_req": 3, "mastery_req": ["hunter"], "weapon_req": "none"},
    "twin_shot":         {"desc": "Two arrows fired simultaneously. Bleeding, -2 Grace. 2 hits.", "level_req": 3, "mastery_req": ["hunter"], "weapon_req": "bow"},
    "smoke_bomb":        {"desc": "Thrown canister erupts in smoke. Hidden, +1 Range, -2 enemy Grace.", "level_req": 3, "mastery_req": ["hunter"], "weapon_req": "none"},
    "hunters_mark":      {"desc": "Glowing sigil on enemy chest. Shaken, -3 Grace/Armor. The enemy has been chosen.", "level_req": 3, "mastery_req": ["hunter"], "weapon_req": "bow"},
    "falcon_strike":     {"desc": "Hunting falcon dives from above. Bleeding, -3 Grace. Opening move.", "level_req": 3, "mastery_req": ["hunter"], "weapon_req": "bow"},
    "spirit_walk":       {"desc": "Step into spirit world. Evasive, +2 Range, +2 Grace. Intangible repositioning.", "level_req": 3, "mastery_req": ["hunter"], "weapon_req": "none"},
    "rain_of_arrows":    {"desc": "Arrows arc upward and descend. Bleeding, -3 Grace, -2 Armor. 3 hits.", "level_req": 8, "mastery_req": ["hunter"], "weapon_req": "bow"},
    "wolf_companion":    {"desc": "Wolf answers the whistle. Bleeding, -3 Might, -2 Grace. Hits low and fast.", "level_req": 8, "mastery_req": ["hunter"], "weapon_req": "none"},
    "explosive_trap":    {"desc": "Thrown charge detonates in fire and shrapnel. Burning, -3 Armor, -2 Might.", "level_req": 8, "mastery_req": ["hunter"], "weapon_req": "none"},
    "hawk_vision":       {"desc": "Eyes change focus. +3 Grace/Cognition, +2 Insight, inspired. Every movement is a trajectory.", "level_req": 8, "mastery_req": ["hunter"], "weapon_req": "none"},
    "backflip":          {"desc": "Flip backward creating distance. Evasive, +2 Range, +3 Grace.", "level_req": 8, "mastery_req": ["hunter"], "weapon_req": "none"},
    "monster_slayer":    {"desc": "Years of experience reveal weak points. Bleeding, -4 Armor, -3 Might. Opponent wounded.", "level_req": 8, "mastery_req": ["hunter"], "weapon_req": "bow"},
    "bear_trap":         {"desc": "Heavy thrown trap, iron jaws snap shut. Ensnared, -4 Might, -3 Grace, -2 Armor.", "level_req": 8, "mastery_req": ["hunter"], "weapon_req": "none"},
    "volley_master":     {"desc": "Arrows leave the bow in a stream. Bleeding, -3 Grace, -4 Armor, -2 Might. 3 hits.", "level_req": 15, "mastery_req": ["hunter"], "weapon_req": "bow"},
    "spirit_bind":       {"desc": "Giant spirit hand erupts from ground. Ensnared, -4 Might/Grace. The dead hold the enemy.", "level_req": 15, "mastery_req": ["hunter"], "weapon_req": "none"},
    "storm_arrow":       {"desc": "Lightning channeled into arrow. Stunned, -3 Grace/Armor, -2 Might. Thunder follows.", "level_req": 15, "mastery_req": ["hunter"], "weapon_req": "bow"},
    "natures_blessing":  {"desc": "Press hand to earth, forest answers. Heals 15%, warded, +3 Essence, +2 Durability. Low HP.", "level_req": 15, "mastery_req": ["hunter"], "weapon_req": "none"},
    "survival_instinct": {"desc": "Instinct guides away from danger. Evasive, heals 10%, +4 Grace, +3 Durability. Low HP.", "level_req": 15, "mastery_req": ["hunter"], "weapon_req": "none"},
    "alpha_command":     {"desc": "Every beast straightens. +4 Might, +3 Grace, +2 Cognition, inspired for 4 turns.", "level_req": 15, "mastery_req": ["hunter"], "weapon_req": "none"},
    "ancient_tracker":   {"desc": "Read the ground like a book. +4 Cognition, +3 Grace, +2 Insight, inspired for 4 turns.", "level_req": 15, "mastery_req": ["hunter"], "weapon_req": "none"},
    "tracking_instinct":  {"desc": "Reveal enemy movement patterns. Shaken, -4 Grace, -3 Cognition, -2 Might. Opponent status.", "level_req": 15, "mastery_req": ["hunter"], "weapon_req": "bow"},
    "world_hunt":        {"desc": "No matter how far prey runs, escape is impossible. True damage, bleeding, 3 hits. Devastates all stats. Opponent wounded.", "level_req": 20, "mastery_req": ["hunter"], "weapon_req": "bow"},
    "legend_of_the_wild":{"desc": "The Hunter and the wild become one. True damage, 5 hits, stuns, heals 15%, inspired. Devastates all stats. Low HP.", "level_req": 20, "mastery_req": ["hunter"], "weapon_req": "bow"},
    # Rogue skills
    "dirty_trick":        {"desc": "Flick dirt, a coin, or debris into the opponent's face. Shaken, -2 Grace, -1 Might.", "level_req": 1, "mastery_req": ["rogue"], "weapon_req": "none"},
    "hidden_blade":       {"desc": "A blade appears from an unsuspected place. Bleeding, -2 Grace. Opening move.", "level_req": 1, "mastery_req": ["rogue"], "weapon_req": "dagger"},
    "opportunist_strike": {"desc": "Strike distracted enemies at their weakest. Bleeding, -2 Might. Opponent has status.", "level_req": 1, "mastery_req": ["rogue"], "weapon_req": "dagger"},
    "acrobatic_roll":     {"desc": "Tumble beneath danger, rolling through incoming attacks. Evasive, +3 Grace.", "level_req": 1, "mastery_req": ["rogue"], "weapon_req": "none"},
    "quick_step":         {"desc": "Shift stance, boosting grace and might while becoming evasive.", "level_req": 1, "mastery_req": ["rogue"], "weapon_req": "none"},
    "pocket_sand":        {"desc": "Throw sand directly into the enemy's eyes. Blinded, -3 Grace.", "level_req": 1, "mastery_req": ["rogue"], "weapon_req": "none"},
    "flash_powder":       {"desc": "A pouch bursts into brilliant powder, blinding and disorienting. Blinded, -3 Grace, -2 Might.", "level_req": 3, "mastery_req": ["rogue"], "weapon_req": "none"},
    "tripwire":           {"desc": "Lay a hidden snare. Ensnared, -3 Grace, -2 Might.", "level_req": 3, "mastery_req": ["rogue"], "weapon_req": "none"},
    "knife_fan":          {"desc": "Throw multiple daggers in a wide arc. 2 hits, bleeding, -2 Grace.", "level_req": 3, "mastery_req": ["rogue"], "weapon_req": "dagger"},
    "hook_chain":         {"desc": "A hooked chain pulls the enemy off balance. Ensnared, -2 Grace, -2 Armor.", "level_req": 3, "mastery_req": ["rogue"], "weapon_req": "none"},
    "feign_death":        {"desc": "Lie motionless, pretending defeat. Hidden, +3 Grace. Low HP.", "level_req": 3, "mastery_req": ["rogue"], "weapon_req": "none"},
    "wall_run":           {"desc": "Sprint across walls, fighting from impossible angles. Evasive, +4 Grace, +2 Might.", "level_req": 3, "mastery_req": ["rogue"], "weapon_req": "none"},
    "sleight_of_hand":    {"desc": "Hands move faster than the eye. Steal a small item. Shaken, +2 Might self, -3 Might, -2 Grace enemy. Opponent has status.", "level_req": 3, "mastery_req": ["rogue"], "weapon_req": "dagger"},
    "mirror_image":       {"desc": "Several identical Rogues scatter. Evasive, +5 Grace.", "level_req": 8, "mastery_req": ["rogue"], "weapon_req": "none"},
    "smoke_bomb_rogue":   {"desc": "Dark smoke fills the battlefield. Hidden, +3 Grace, +2 Cognition.", "level_req": 8, "mastery_req": ["rogue"], "weapon_req": "none"},
    "false_surrender":    {"desc": "Kneel in apparent defeat, then strike unexpectedly. Stunned, -3 Grace, -3 Might. Low HP.", "level_req": 8, "mastery_req": ["rogue"], "weapon_req": "dagger"},
    "misdirection":       {"desc": "Redirect enemy attention with masterful misdirection. Shaken, -4 Cognition, -3 Grace, -2 Might.", "level_req": 8, "mastery_req": ["rogue"], "weapon_req": "none"},
    "counter_stab":       {"desc": "Exploit a debuffed enemy with a devastating two-hit counter. 2 hits, bleeding, +3 Might, +2 Grace self, -3 Might, -2 Grace enemy. Opponent has status.", "level_req": 8, "mastery_req": ["rogue"], "weapon_req": "dagger"},
    "escape_artist":      {"desc": "Break free from any restraint. Evasive, +4 Grace, +2 Cognition. Self debuffed.", "level_req": 8, "mastery_req": ["rogue"], "weapon_req": "none"},
    "tricksters_flurry":  {"desc": "A flurry of three strikes, each a different dirty trick. 3 hits, bleeding, +3 Might, +2 Grace self, -3 Grace, -2 Might enemy.", "level_req": 8, "mastery_req": ["rogue"], "weapon_req": "dagger"},
    "lucky_escape":       {"desc": "Uncanny luck — every deadly attack narrowly misses. Evasive, +5 Grace, +3 Cognition. Low HP.", "level_req": 15, "mastery_req": ["rogue"], "weapon_req": "none"},
    "ambush_master":      {"desc": "The perfect hiding place becomes a deadly trap. Hidden, +4 Might, +4 Grace, +2 Cognition. Opening move.", "level_req": 15, "mastery_req": ["rogue"], "weapon_req": "dagger"},
    "grand_heist":        {"desc": "Steal the enemy's armor protection mid-fight. Shaken, +3 Might, +3 Grace self, -5 Armor, -3 Might enemy. Opponent wounded.", "level_req": 15, "mastery_req": ["rogue"], "weapon_req": "dagger"},
    "coin_toss":          {"desc": "A spinning coin catches the target's eyes. Shaken, -4 Cognition, -3 Grace, -3 Might, -2 Insight.", "level_req": 15, "mastery_req": ["rogue"], "weapon_req": "none"},
    "shadow_step_rogue":  {"desc": "Vanish from one position and appear in another. Hidden, +4 Grace, +3 Cognition.", "level_req": 15, "mastery_req": ["rogue"], "weapon_req": "none"},
    "master_picklock":    {"desc": "Unlock the enemy's defenses, dismantling their protection. Ensnared, -6 Armor, -3 Grace, -2 Cognition. Opponent wounded.", "level_req": 15, "mastery_req": ["rogue"], "weapon_req": "dagger"},
    "king_of_thieves":    {"desc": "Steal the enemy's power and claim it for yourself. Shaken, +4 Might, +3 Grace, +2 Cognition self, -4 Might, -3 Grace, -3 Cognition enemy. Opponent has status.", "level_req": 15, "mastery_req": ["rogue"], "weapon_req": "dagger"},
    "tricksters_gambit":  {"desc": "Bet everything on one impossible sequence — three strikes, each a different trick. 3 hits, bleeding, +4 Might, +3 Grace self, -3 Might, -3 Grace, -3 Armor enemy.", "level_req": 15, "mastery_req": ["rogue"], "weapon_req": "dagger"},
    "perfect_crime":      {"desc": "Nothing suggests the Rogue was ever there. True damage, bleeding, hidden. Devastates all stats. Opponent wounded.", "level_req": 20, "mastery_req": ["rogue"], "weapon_req": "dagger"},
    "legend_of_trickery": {"desc": "Reality bends around every deception. True damage, stunned, hidden. Devastates every stat. Low HP.", "level_req": 20, "mastery_req": ["rogue"], "weapon_req": "dagger"},
    # --- Bard Mastery ---
    "song_of_heroes":          {"desc": "Song: physical attacks can't be evaded. Dance: confuse the enemy. Crescendo builds, Encore may linger.", "level_req": 1, "mastery_req": ["bard"], "weapon_req": "none"},
    "song_of_hope":            {"desc": "Song: allies survive lethal damage once. Dance: pull enemy in and mesmerize. Crescendo builds, Encore may linger.", "level_req": 1, "mastery_req": ["bard"], "weapon_req": "none"},
    "resonant_strike":         {"desc": "A magical strike that resonates with the enemy's weaknesses, reducing their Grace.", "level_req": 1, "mastery_req": ["bard"], "weapon_req": "none"},
    "harmony_shield":          {"desc": "A protective harmony that shields all allies and grants Warded.", "level_req": 1, "mastery_req": ["bard"], "weapon_req": "none"},
    "sunrise_chorus":          {"desc": "A cleansing chorus that removes debuffs and empowers all allies. Only when debuffed.", "level_req": 1, "mastery_req": ["bard"], "weapon_req": "none"},
    "song_of_wisdom":          {"desc": "Song: reset a random ally cooldown. Dance: silence the enemy. Crescendo builds, Encore may linger.", "level_req": 3, "mastery_req": ["bard"], "weapon_req": "none"},
    "festival_rhythm":         {"desc": "A lively rhythm that inspires all allies with Grace, Might, and Cognition.", "level_req": 3, "mastery_req": ["bard"], "weapon_req": "none"},
    "discord":                 {"desc": "A jarring dissonance that shatters the enemy's focus. Shaken, reduces Cognition, Grace, Might.", "level_req": 3, "mastery_req": ["bard"], "weapon_req": "none"},
    "dance_of_blades":         {"desc": "A whirling performance that cuts the enemy with magical force. Causes Bleeding.", "level_req": 3, "mastery_req": ["bard"], "weapon_req": "none"},
    "sirens_call":             {"desc": "A haunting call that ensnares the enemy's mind and body. Ensnared, reduces Grace, Cognition.", "level_req": 3, "mastery_req": ["bard"], "weapon_req": "none"},
    "ballad_of_hope":          {"desc": "A stirring ballad that heals and inspires all allies. Low HP trigger.", "level_req": 3, "mastery_req": ["bard"], "weapon_req": "none"},
    "lullaby_of_fallen_kings": {"desc": "A lullaby so powerful it stuns the enemy. Reduces Grace, Might, Cognition.", "level_req": 3, "mastery_req": ["bard"], "weapon_req": "none"},
    "song_of_freedom":         {"desc": "Song: allies immune to crowd control. Dance: enemy attacks their own allies. Crescendo builds, Encore may linger.", "level_req": 8, "mastery_req": ["bard"], "weapon_req": "none"},
    "moon_serenade":           {"desc": "A serene melody that heals and wards all allies. Boosts Essence, Grace, Insight.", "level_req": 8, "mastery_req": ["bard"], "weapon_req": "none"},
    "inspiring_solo":          {"desc": "An uplifting solo that boosts Might and Grace for all allies.", "level_req": 8, "mastery_req": ["bard"], "weapon_req": "none"},
    "echo_verse":              {"desc": "A verse that echoes the enemy's affliction back at them. Boosts all allies. Opponent has status.", "level_req": 8, "mastery_req": ["bard"], "weapon_req": "none"},
    "epic_tale":               {"desc": "A grand tale that heals and empowers all allies with Might, Grace, Durability, Essence.", "level_req": 8, "mastery_req": ["bard"], "weapon_req": "none"},
    "muses_blessing":          {"desc": "A divine blessing that boosts Insight, Cognition, and Essence for all allies.", "level_req": 8, "mastery_req": ["bard"], "weapon_req": "none"},
    "curtain_call":            {"desc": "A devastating finale that shatters the enemy's confidence. Shaken, reduces Might, Grace, Cognition, Insight. Opponent has status.", "level_req": 8, "mastery_req": ["bard"], "weapon_req": "none"},
    "song_of_fortune":         {"desc": "Song: reroll the enemy's worst die. Dance: burn the enemy for true damage per turn. Crescendo builds, Encore may linger.", "level_req": 15, "mastery_req": ["bard"], "weapon_req": "none"},
    "heros_anthem":            {"desc": "An opening anthem that boosts Might, Grace, and Armor for all allies. Opening move.", "level_req": 15, "mastery_req": ["bard"], "weapon_req": "none"},
    "world_orchestra":         {"desc": "A symphony that heals and empowers all allies with Might, Grace, Insight, Essence.", "level_req": 15, "mastery_req": ["bard"], "weapon_req": "none"},
    "grand_performance":       {"desc": "A performance so overwhelming it stuns the enemy. Reduces Might, Grace, Cognition, Insight.", "level_req": 15, "mastery_req": ["bard"], "weapon_req": "none"},
    "memory_song":             {"desc": "A nostalgic song that boosts Cognition, Insight, and Grace for all allies.", "level_req": 15, "mastery_req": ["bard"], "weapon_req": "none"},
    "legend_keeper":           {"desc": "A legendary ballad that heals and wards all allies. Boosts Might, Grace, Essence, Durability, Cognition.", "level_req": 15, "mastery_req": ["bard"], "weapon_req": "none"},
    "whispered_melody":        {"desc": "A haunting melody that shatters the enemy's mind. Shaken, reduces Cognition, Grace, Might, Insight.", "level_req": 15, "mastery_req": ["bard"], "weapon_req": "none"},
    "travelers_tune":          {"desc": "A walking song that heals and wards all allies. Boosts Grace, Durability, Essence.", "level_req": 15, "mastery_req": ["bard"], "weapon_req": "none"},
    "requiem_of_the_heavens":  {"desc": "All five Song rules and all five Dance effects active simultaneously. Heals allies, true DPT, stun chance. Crescendo and Encore.", "level_req": 20, "mastery_req": ["bard"], "weapon_req": "none"},
    "symphony_of_creation":    {"desc": "All rules at maximum power + heals + true DPT + guaranteed mesmerized. The ultimate performance. Low HP trigger.", "level_req": 20, "mastery_req": ["bard"], "weapon_req": "none"},
    # --- Priest Skills ---
    "swift_prayer":            {"desc": "A flash of divine light — small but instant. Heals 2% of target's max HP. Always acts first. No cooldown.", "level_req": 1, "mastery_req": ["priest"], "weapon_req": "none"},
    "light_barrier":           {"desc": "A wall of holy light with its own HP pool that absorbs damage. Shield Wall HP = 20% of max HP, scaled by Sanctity.", "level_req": 1, "mastery_req": ["priest"], "weapon_req": "none"},
    "bless":                   {"desc": "The Priest blesses themselves with divine favor. Sanctity amplifies the blessing as the enemy crumbles.", "level_req": 1, "mastery_req": ["priest"], "weapon_req": "none"},
    "holy_water":              {"desc": "Consecrated water thrown as a weapon. Holy damage burns undead and devils with +50% force.", "level_req": 1, "mastery_req": ["priest"], "weapon_req": "none"},
    "blinding_light":          {"desc": "A flash of holy radiance that sears the enemy's vision. Enemy can act but attacks miss.", "level_req": 1, "mastery_req": ["priest"], "weapon_req": "none"},
    "soul_ward":               {"desc": "A shimmering seal protecting against spiritual attacks. Sanctity deepens the ward.", "level_req": 1, "mastery_req": ["priest"], "weapon_req": "none"},
    "blessing_of_renewal":     {"desc": "A holy buff that heals 10% of owner's max HP each turn for 3 turns. Sanctity boosts each tick.", "level_req": 3, "mastery_req": ["priest"], "weapon_req": "none"},
    "chain_of_light":          {"desc": "Chains of pure holy light bind the enemy completely. Cannot act or dodge.", "level_req": 3, "mastery_req": ["priest"], "weapon_req": "none"},
    "cleansing_flame":         {"desc": "White holy fire purifies the corrupted. Only triggers when the enemy has a status effect.", "level_req": 3, "mastery_req": ["priest"], "weapon_req": "none"},
    "angels_grace":            {"desc": "Soft feathers of light drift around the Priest as divine favor blesses them.", "level_req": 3, "mastery_req": ["priest"], "weapon_req": "none"},
    "judgment_strike":         {"desc": "Holy power channeled into a single divine strike. Scales with Sanctity.", "level_req": 3, "mastery_req": ["priest"], "weapon_req": "none"},
    "divine_rebuke":           {"desc": "Holy power erupts, driving back darkness. Sanctity deepens the rebuke.", "level_req": 3, "mastery_req": ["priest"], "weapon_req": "none"},
    "light_of_hope":           {"desc": "A calming light restores determination, dispelling fear. Only triggers when debuffed.", "level_req": 3, "mastery_req": ["priest"], "weapon_req": "none"},
    "divine_light_priest":     {"desc": "A pillar of holy light heals 20% of target's max HP. No cooldown. Sanctity amplifies the heal.", "level_req": 8, "mastery_req": ["priest"], "weapon_req": "none"},
    "mass_purify":             {"desc": "Cleansing light spreads outward, removing curses and poison. Only triggers when debuffed.", "level_req": 8, "mastery_req": ["priest"], "weapon_req": "none"},
    "heavens_judgment":         {"desc": "A beam of radiant judgment descends from the sky. Holy damage scales with Sanctity.", "level_req": 8, "mastery_req": ["priest"], "weapon_req": "none"},
    "radiant_prison":          {"desc": "A cage of pure holy light forms around the enemy, binding them completely for 2 turns.", "level_req": 8, "mastery_req": ["priest"], "weapon_req": "none"},
    "beacon_of_faith":         {"desc": "A brilliant beacon shines into the heavens, strengthening the faithful and mending wounds.", "level_req": 8, "mastery_req": ["priest"], "weapon_req": "none"},
    "sunflare":                {"desc": "A miniature sun detonates with holy radiance, blinding the enemy for 3 turns.", "level_req": 8, "mastery_req": ["priest"], "weapon_req": "none"},
    "radiant_bulwark":         {"desc": "A towering wall of holy light absorbs 35% of max HP. When struck, flares and blinds the enemy.", "level_req": 8, "mastery_req": ["priest"], "weapon_req": "none"},
    "sanctuary_priest":         {"desc": "Sacred symbols create a holy zone. Shield Wall HP = 50% of max HP. When broken, binds the enemy.", "level_req": 15, "mastery_req": ["priest"], "weapon_req": "none"},
    "holy_lance":              {"desc": "A lance of pure holy light hurled at the enemy. Pierces defenses, causes bleeding on undead/devils.", "level_req": 15, "mastery_req": ["priest"], "weapon_req": "none"},
    "promise_of_heaven":       {"desc": "A holy buff that heals 35% of max HP after 2 turns. High risk/reward. Sanctity amplifies the payoff.", "level_req": 15, "mastery_req": ["priest"], "weapon_req": "none"},
    "hymn_of_salvation":       {"desc": "The Priest's voice echoes with celestial harmony, healing all party members for 15% of their max HP.", "level_req": 15, "mastery_req": ["priest"], "weapon_req": "none"},
    "final_judgment":          {"desc": "The final verdict — holy chains bind and holy light blinds the enemy for 3 turns. Only triggers when enemy is wounded.", "level_req": 15, "mastery_req": ["priest"], "weapon_req": "none"},
    "holy_revelation":         {"desc": "Mystic visions unfold before the faithful. The Priest sees the enemy's weaknesses with divine clarity.", "level_req": 15, "mastery_req": ["priest"], "weapon_req": "none"},
    "prayer_circle":           {"desc": "The Priest combines prayers into overwhelming divine power, empowering all stats and healing.", "level_req": 15, "mastery_req": ["priest"], "weapon_req": "none"},
    "divine_covenant":         {"desc": "Golden threads of light connect the Priest to the divine, forging a sacred bond that empowers and heals.", "level_req": 15, "mastery_req": ["priest"], "weapon_req": "none"},
    "choir_of_heaven":         {"desc": "Angelic hymns fill the battlefield. True damage ignores all defense. Heals the Priest. Quest-gated.", "level_req": 20, "mastery_req": ["priest"], "weapon_req": "none"},
    "legend_of_the_faithful":  {"desc": "Countless wings of light unfold. True damage, stunned + blind, devastating stat debuffs. Heals massively. Low HP trigger. Quest-gated.", "level_req": 20, "mastery_req": ["priest"], "weapon_req": "none"},
}

SKILL_RARITY: dict[str, str] = {
    "shield_bash": "common",
    "sworn_strike": "uncommon",
    "smite": "rare",
    "lay_on_hands": "epic",
    "thrust": "common",
    "impale": "uncommon",
    "backstab": "uncommon",
    "vanish": "rare",
    "mocking_verse": "common",
    "rally": "rare",
    "mix_potion": "uncommon",
    "acid_flask": "uncommon",
    "arcane_bolt": "common",
    "ward": "uncommon",
    "divine_light": "epic",
    "purge": "uncommon",
    "thornlash": "common",
    "beast_call": "epic",
    "shadow_step": "legendary",
    "poison_blade": "uncommon",
    "aimed_shot": "rare",
    "trap": "uncommon",
    "mend": "rare",
    # Alchemist skills
    "acid_bomb": "common",
    "flash_powder_alch": "common",
    "quick_jab": "common",
    "heavy_crush": "common",
    "healing_draught": "common",
    "iron_skin_transmutation": "common",
    "frost_mixture": "uncommon",
    "lightning_bottle": "uncommon",
    "poison_capsule": "uncommon",
    "flurry": "uncommon",
    "rushing_strike": "uncommon",
    "swift_transmutation": "uncommon",
    "stone_wall": "uncommon",
    "corrosive_mist": "rare",
    "living_slime": "rare",
    "transmutation_touch": "rare",
    "explosive_chain": "rare",
    "spinning_strike": "rare",
    "piercing_strike": "rare",
    "counter_strike": "rare",
    "forbidden_formula": "epic",
    "guard_break": "epic",
    "rising_strike": "epic",
    "executioner_strike": "epic",
    "mutagen_injection": "epic",
    "phoenix_mixture": "epic",
    "smoke_transmutation": "epic",
    "spike_field": "epic",
    "philosophers_transmutation": "legendary",
    "legend_of_alchemy": "legendary",
    # Paladin skills
    "shield_of_faith": "common",
    "blessed_strike": "common",
    "merciful_touch": "common",
    "hammer_of_light": "common",
    "divine_aegis": "common",
    "lightbearers_oath": "common",
    "sacred_charge": "uncommon",
    "judgment_hammer": "uncommon",
    "holy_barrier": "uncommon",
    "consecrate_blade": "uncommon",
    "sunburst": "uncommon",
    "divine_radiance": "uncommon",
    "guardians_blessing": "uncommon",
    "divine_intercession": "rare",
    "lay_on_hands_paladin": "rare",
    "exorcism": "rare",
    "celestial_spear": "rare",
    "divine_resolve": "rare",
    "faiths_bulwark": "rare",
    "last_stand": "rare",
    "holy_nova": "epic",
    "sanctuary": "epic",
    "justice_descends": "epic",
    "guardians_crown": "epic",
    "resurrection_prayer": "epic",
    "consecrated_ground": "epic",
    "divine_wrath": "epic",
    "guardian_angel": "epic",
    "last_judgment": "legendary",
    "ascension_of_the_light": "legendary",
    # Knight skills
    "iron_stance": "common",
    "war_cry": "common",
    "vanguard_step": "common",
    "pommel_strike": "common",
    "steady_grip": "common",
    "kings_challenge": "uncommon",
    "lions_charge": "uncommon",
    "heavy_strike": "uncommon",
    "bulwark": "uncommon",
    "banner_of_valor": "uncommon",
    "fortress_breaker": "uncommon",
    "plate_armor_mastery": "uncommon",
    "shield_wall": "rare",
    "guardians_sacrifice": "rare",
    "commanding_presence": "rare",
    "crushing_blow": "rare",
    "unbreakable_will": "rare",
    "titans_strength": "rare",
    "ground_slam": "rare",
    "iron_formation": "epic",
    "royal_execution": "epic",
    "guardians_oath": "epic",
    "warlords_fury": "epic",
    "crown_of_iron": "epic",
    "kings_command": "epic",
    "last_bastion": "epic",
    "oath_strike": "epic",
    "final_duel": "legendary",
    "legend_of_erchis": "legendary",
    # Lancer skills
    "flame_imbue": "common",
    "frost_imbue": "common",
    "gale_thrust": "common",
    "lancer_guard_break": "common",
    "cyclone_wall": "common",
    "warriors_focus": "common",
    "storm_imbue": "uncommon",
    "stone_imbue": "uncommon",
    "sky_piercer": "uncommon",
    "falcon_rush": "uncommon",
    "dragon_fang": "uncommon",
    "elemental_weakness": "uncommon",
    "battle_readiness": "uncommon",
    "gale_imbue": "rare",
    "thunder_imbue": "rare",
    "dragon_dive": "rare",
    "frostbite": "rare",
    "shock_lock": "rare",
    "iron_breeze": "rare",
    "elemental_surge": "rare",
    "inferno_imbue": "epic",
    "glacier_imbue": "epic",
    "tempest_imbue": "epic",
    "volcano_imbue": "epic",
    "thunder_pursuit": "epic",
    "world_splitter": "epic",
    "crimson_spear": "epic",
    "elemental_collapse": "epic",
    "celestial_javelin": "legendary",
    "avatar_of_the_storm": "legendary",
    # Mage skills
    "arcane_burst": "common",
    "wind_blade": "common",
    "stone_spear": "common",
    "arcane_ward": "common",
    "blink": "common",
    "water_lash": "common",
    "fireball": "uncommon",
    "frost_prison": "uncommon",
    "chain_lightning": "uncommon",
    "mana_shield": "uncommon",
    "spell_seal": "uncommon",
    "arcane_chains": "uncommon",
    "illusory_double": "uncommon",
    "gravity_well": "rare",
    "telekinetic_crush": "rare",
    "mirror_spell": "rare",
    "mind_maze": "rare",
    "void_portal": "rare",
    "phantom_terrain": "rare",
    "dream_step": "rare",
    "meteor_storm": "epic",
    "blizzard": "epic",
    "thunderfield": "epic",
    "time_slow": "epic",
    "elemental_convergence": "epic",
    "mana_explosion": "epic",
    "reality_fracture": "epic",
    "time_stop": "epic",
    "cosmic_convergence": "legendary",
    "legend_of_the_arcane": "legendary",
    # Assassin skills
    "shadow_strike": "common",
    "heart_piercer": "common",
    "smoke_veil": "common",
    "death_mark": "common",
    "shadow_focus": "common",
    "silent_execution": "uncommon",
    "phantom_strike": "uncommon",
    "crimson_dash": "uncommon",
    "night_veil": "uncommon",
    "shadow_terror": "uncommon",
    "shadowstep": "uncommon",
    "dark_pursuit": "uncommon",
    "vanishing_kill": "rare",
    "shadow_flurry": "rare",
    "soul_sever": "rare",
    "shadow_clone": "rare",
    "shadow_prison": "rare",
    "black_feathers": "rare",
    "eclipse_blade": "rare",
    "shadow_convergence": "epic",
    "night_requiem": "epic",
    "deaths_whisper": "epic",
    "umbral_cloak": "epic",
    "final_contract": "epic",
    "king_slayer": "epic",
    "shadow_devour": "epic",
    "eclipse_burst": "epic",
    "reapers_arrival": "legendary",
    "eclipse_of_shadows": "legendary",
    # Hunter skills
    "rapid_shot": "common",
    "piercing_shot": "common",
    "snare_trap": "common",
    "camouflage": "common",
    "eagle_eye": "common",
    "crippling_shot": "common",
    "poison_arrow": "uncommon",
    "flash_bang": "uncommon",
    "twin_shot": "uncommon",
    "smoke_bomb": "uncommon",
    "hunters_mark": "uncommon",
    "falcon_strike": "uncommon",
    "spirit_walk": "uncommon",
    "rain_of_arrows": "rare",
    "wolf_companion": "rare",
    "explosive_trap": "rare",
    "hawk_vision": "rare",
    "backflip": "rare",
    "monster_slayer": "rare",
    "bear_trap": "rare",
    "volley_master": "epic",
    "spirit_bind": "epic",
    "storm_arrow": "epic",
    "natures_blessing": "epic",
    "survival_instinct": "epic",
    "alpha_command": "epic",
    "ancient_tracker": "epic",
    "tracking_instinct": "epic",
    "world_hunt": "legendary",
    "legend_of_the_wild": "legendary",
    # Rogue skills
    "dirty_trick": "common",
    "hidden_blade": "common",
    "opportunist_strike": "common",
    "acrobatic_roll": "common",
    "quick_step": "common",
    "pocket_sand": "common",
    "flash_powder": "uncommon",
    "tripwire": "uncommon",
    "knife_fan": "uncommon",
    "hook_chain": "uncommon",
    "feign_death": "uncommon",
    "wall_run": "uncommon",
    "sleight_of_hand": "uncommon",
    "mirror_image": "rare",
    "smoke_bomb_rogue": "rare",
    "false_surrender": "rare",
    "misdirection": "rare",
    "counter_stab": "rare",
    "escape_artist": "rare",
    "tricksters_flurry": "rare",
    "lucky_escape": "epic",
    "ambush_master": "epic",
    "grand_heist": "epic",
    "coin_toss": "epic",
    "shadow_step_rogue": "epic",
    "master_picklock": "epic",
    "king_of_thieves": "epic",
    "tricksters_gambit": "epic",
    "perfect_crime": "legendary",
    "legend_of_trickery": "legendary",
    # --- Bard Mastery ---
    "song_of_heroes": "common",
    "song_of_hope": "common",
    "resonant_strike": "common",
    "harmony_shield": "common",
    "sunrise_chorus": "common",
    "song_of_wisdom": "uncommon",
    "festival_rhythm": "uncommon",
    "discord": "uncommon",
    "dance_of_blades": "uncommon",
    "sirens_call": "uncommon",
    "ballad_of_hope": "uncommon",
    "lullaby_of_fallen_kings": "uncommon",
    "song_of_freedom": "rare",
    "moon_serenade": "rare",
    "inspiring_solo": "rare",
    "echo_verse": "rare",
    "epic_tale": "rare",
    "muses_blessing": "rare",
    "curtain_call": "rare",
    "song_of_fortune": "epic",
    "heros_anthem": "epic",
    "world_orchestra": "epic",
    "grand_performance": "epic",
    "memory_song": "epic",
    "legend_keeper": "epic",
    "whispered_melody": "epic",
    "travelers_tune": "epic",
    "requiem_of_the_heavens": "legendary",
    "symphony_of_creation": "legendary",
    # --- Priest Skills ---
    "swift_prayer": "common",
    "light_barrier": "common",
    "bless": "common",
    "holy_water": "common",
    "blinding_light": "common",
    "soul_ward": "common",
    "blessing_of_renewal": "uncommon",
    "chain_of_light": "uncommon",
    "cleansing_flame": "uncommon",
    "angels_grace": "uncommon",
    "judgment_strike": "uncommon",
    "divine_rebuke": "uncommon",
    "light_of_hope": "uncommon",
    "divine_light_priest": "rare",
    "mass_purify": "rare",
    "heavens_judgment": "rare",
    "radiant_prison": "rare",
    "beacon_of_faith": "rare",
    "sunflare": "rare",
    "radiant_bulwark": "rare",
    "sanctuary_priest": "epic",
    "holy_lance": "epic",
    "promise_of_heaven": "epic",
    "hymn_of_salvation": "epic",
    "final_judgment": "epic",
    "holy_revelation": "epic",
    "prayer_circle": "epic",
    "divine_covenant": "epic",
    "choir_of_heaven": "legendary",
    "legend_of_the_faithful": "legendary",
}

SKILL_EXEC: dict[str, str] = {
    "shield_bash": "You drive your shield into the enemy with a bone-rattling clang.",
    "sworn_strike": "Your weapon falls in a shining arc, weighted by oath and iron.",
    "smite": "A column of searing light erupts beneath the wounded foe.",
    "lay_on_hands": "Warm radiance spills from your palms, closing wounds.",
    "thrust": "You lunge through an opening, steel seeking flesh.",
    "impale": "With a roar, you drive your weapon deep. Blood pools beneath them.",
    "backstab": "Steel kisses from the shadows, opening a crimson line.",
    "vanish": "Shadows fold around you like a second skin.",
    "mocking_verse": "You sing a verse so cutting the enemy flinches.",
    "rally": "Your cry lifts your allies’ hearts and blades alike.",
    "mix_potion": "You crush herbs and vials together, the mixture hissing bright green.",
    "acid_flask": "A glass orb shatters, spraying caustic mist.",
    "arcane_bolt": "Raw arcane energy crackles from your fingertips.",
    "ward": "A shimmering shell of force wraps around you.",
    "divine_light": "Radiance sears through the enemy’s afflictions, blinding them.",
    "purge": "Clean light burns through your body, driving out taint.",
    "thornlash": "Vines whip out, thorns tearing cloth and skin.",
    "beast_call": "The wild answers. Claws and fangs tear into your prey.",
    "shadow_step": "You take one step and vanish, the air itself forgetting you.",
    "poison_blade": "A venomed edge leaves a sickened wound.",
    "aimed_shot": "You exhale, and the arrow finds its mark.",
    "trap": "Steel jaws snap shut with a sharp click.",
    "mend": "Flesh knits beneath your glowing touch.",
    # Alchemist skills
    "acid_bomb": "The katar sweats green acid — the blade becomes liquid, dripping with corrosive potential.",
    "flash_powder_alch": "The katar gleams like a mirror, blinding light dancing on the polished surface.",
    "quick_jab": "A lightning-fast jab — the katar flicks out before the enemy can blink.",
    "heavy_crush": "The Alchemist brings the katar down with full weight — armor crumples like paper.",
    "healing_draught": "The Alchemist drinks deep — warmth spreads, wounds close, skin hardens.",
    "iron_skin_transmutation": "The Alchemist's skin ripples and turns grey — iron to the touch, unyielding.",
    "frost_mixture": "The katar crystallizes into an ice spike — frost crawls from the blade, freezing the air.",
    "lightning_bottle": "The katar splits into crackling claws — arcs of lightning jump between the blades.",
    "poison_capsule": "The katar extends into a thin needle — a single drop of venom glistens at the tip.",
    "flurry": "Three punches in the span of one breath — the katar is a blur of steel and imbued energy.",
    "rushing_strike": "The Alchemist closes the gap in a heartbeat — clapping the katar mid-stride, loading a new imbue and striking in one fluid motion.",
    "swift_transmutation": "The Alchemist's legs shift and elongate — bones hollow, muscles reknit for speed.",
    "stone_wall": "The Alchemist's body turns to living stone — rooted, immovable, patient.",
    "corrosive_mist": "The katar erodes — pitted, smoking, metal degrading and reforming in real time.",
    "living_slime": "The katar extends into a translucent whip — living slime drips and reaches from the strands.",
    "transmutation_touch": "The katar goes dull — flat grey, no reflection. It doesn't cut. It unmakes.",
    "explosive_chain": "The katar goes jagged — sparks fly off the crackling, unstable edge.",
    "spinning_strike": "The Alchemist plants and spins — katar out, full rotation, ending behind the enemy.",
    "piercing_strike": "A surgical thrust — the katar finds the gap between plates and slides through.",
    "counter_strike": "The enemy swings — the Alchemist steps in, katar rising to meet the attack.",
    "forbidden_formula": "The katar can't hold a form — flickering between every blade shape at once, screaming with alchemical power.",
    "guard_break": "The katar comes down at the joint between shield and arm — the guard crumbles.",
    "rising_strike": "The Alchemist drops low and drives upward — the enemy leaves the ground.",
    "executioner_strike": "One punch. Clean. Final. Every experiment, every observation — cashed in at once.",
    "mutagen_injection": "The needle goes into the neck — bones shift, muscles swell, the Alchemist becomes something more.",
    "phoenix_mixture": "Fire replaces blood — the body refuses to die, wounds closing in searing light.",
    "smoke_transmutation": "The Alchemist dissolves into smoke — gone before the enemy can blink.",
    "spike_field": "The ground erupts — spikes of transmuted stone tear up beneath the enemy's feet.",
    "philosophers_transmutation": "The Alchemist presses both palms to their chest — the transmutation starts at the heart. The katar glows with every color at once. The formula is perfect. The Alchemist IS the formula.",
    "legend_of_alchemy": "Eight punches. Each one a different transmutation. The katar reads the enemy and responds. The Alchemist has transcended choosing — they simply understand.",
    # Paladin skills
    "shield_of_faith": "The Paladin raises their shield — not steel, but faith. A sigil blazes to life before it.",
    "blessed_strike": "The Paladin's blade hums with golden symbols. When the edge bites, the enemy feels doubt.",
    "merciful_touch": "The Paladin presses a bare palm to the wound. Warmth flows — the faith says not yet.",
    "hammer_of_light": "The hammer falls like judgment. The impact rings like a church bell — deep, resonant, final.",
    "divine_aegis": "The Paladin believes, and the belief becomes real — a shimmer in the air, a weight on the shoulders that feels like safety.",
    "lightbearers_oath": "The Paladin speaks the Oath of the Light. The words hang in the air like a bell still ringing.",
    "sacred_charge": "The Paladin lowers their shield and runs — light trails from their shoulders like wings that don't exist.",
    "judgment_hammer": "The Paladin raises a fist to the sky. The sky answers. A column of radiance descends — silent, absolute, patient.",
    "holy_barrier": "The Paladin traces a circle in the air. It stays. Light blooms from the line — a dome of gold and white.",
    "consecrate_blade": "The Paladin runs a finger along the blade's edge. Runes bloom in its wake — ancient, golden, alive.",
    "sunburst": "The Paladin opens their palm. The light that comes out is not gentle — it is the sun at noon.",
    "divine_radiance": "The Paladin presses a palm to their chest and speaks a name of light. The darkness screams as it burns away.",
    "guardians_blessing": "The emblem is old — dented, tarnished. But when they raise it, it glows like the first dawn.",
    "divine_intercession": "The blow lands. The Paladin should fall. Instead, they stand. The faith says not yet.",
    "lay_on_hands_paladin": "The Paladin presses both palms to their chest. The light is a river, a flood, a force that will not be denied.",
    "exorcism": "The Paladin speaks the Rite of Banishment. Something behind the enemy's eyes screams and leaves.",
    "celestial_spear": "The Paladin extends a hand. Light gathers, condenses, hardens — and then it flies.",
    "divine_resolve": "The Paladin closes their eyes. They remember the temple. They open their eyes. The fear is gone.",
    "faiths_bulwark": "The Paladin believes, and the belief becomes walls — not visible, not physical, but real.",
    "last_stand": "The Paladin is on one knee. And then — light. Not from the sky. From the Paladin themself.",
    "holy_nova": "The Paladin presses their palms together and speaks the final word. Light detonates.",
    "sanctuary": "The Paladin kneels and presses a palm to the earth. The ground answers — light spreads outward.",
    "justice_descends": "The Paladin looks up. 'It is decided.' The sky agrees. What falls is not lightning — it is a verdict.",
    "guardians_crown": "The crown hovers, spinning slowly, casting light in every direction. It is a symbol of guardians.",
    "resurrection_prayer": "The Paladin whispers a prayer. Something hears. Something answers. The wounds close.",
    "consecrated_ground": "The Paladin's hammer strikes the ground. The crack glows. This ground is sacred now.",
    "divine_wrath": "The Paladin raises the hammer high and brings it down. It is faith on flesh.",
    "guardian_angel": "Wings of light unfurl behind the Paladin. A hand rests on their shoulder. They are not fighting alone.",
    "last_judgment": "The Paladin raises both hands to the sky. The clouds part. A blade of pure light descends — vast as a cathedral spire.",
    "ascension_of_the_light": "The Paladin lets go of everything. Wings unfold — just light, shaped like mercy, moving like judgment.",
    # Knight skills
    "iron_stance": "Nothing fancy. No flash, no roar, no light. The Knight just... stands differently. Feet wider. Knees bent. Weight settled.",
    "war_cry": "A roar splits the silence before the charge. The Knight's voice carries the weight of every war they've survived.",
    "vanguard_step": "The Knight steps forward first — not charging, not running, just advancing. One step. The shield angles. The plate aligns.",
    "pommel_strike": "The blade is for cutting. The pommel is for convincing. The Knight reverses the grip and drives the hard steel knob into the enemy's face.",
    "steady_grip": "A small adjustment — half an inch on the sword, a quarter turn on the shield. It looks like nothing. It changes everything.",
    "kings_challenge": "The blade sinks into the earth. The shield rises. The Knight's voice rolls across the field like a war-drum.",
    "lions_charge": "The Knight explodes from the line — shield first, boots tearing earth. The impact crumples armor like parchment.",
    "heavy_strike": "The Knight doesn't swing — they drop. The blade comes down with the full weight of plate, muscle, and intent.",
    "bulwark": "The Knight doesn't move. They become a structure. Shield locked, shoulders squared, weight distributed.",
    "banner_of_valor": "The banner strikes the ground and the cloth catches a wind that wasn't there before. It's not magic — it's meaning.",
    "fortress_breaker": "Two hands on the grip. One breath. The blade falls — and the enemy's defense shatters beneath it like a gate that forgot how to hold.",
    "plate_armor_mastery": "The Knight takes a breath and adjusts — a buckle here, a pauldron there. The armor goes from worn to integrated.",
    "shield_wall": "The Knight's shield drops into position — not held, but locked. Arm, shoulder, and spine align into a single braced line.",
    "guardians_sacrifice": "The Knight is bleeding. The enemy grins. And then the Knight's eyes change — not desperate, not fearful, but committed.",
    "commanding_presence": "The Knight doesn't shout. They stand. Taller. Straighter. The armor catches the light differently.",
    "crushing_blow": "The enemy is hurt — bleeding, staggering, open. The Knight doesn't hesitate. The blade comes down with every Oath stack behind it.",
    "unbreakable_will": "The whispers crawl in — fear, doubt, the cold voice that says fall. The Knight remembers a name, an oath, a hand that once trusted them.",
    "titans_strength": "The Knight doesn't grow — they densify. The muscles compress, the bones thicken, the frame solidifies.",
    "ground_slam": "The Knight lifts the blade and drives it down. The ground cracks. The shockwave travels. The enemy's feet leave the floor involuntarily.",
    "iron_formation": "The Knight sinks into the earth like a root. Plate aligns with plate, muscle locks with bone, and the world pushes — and the world fails to move them.",
    "royal_execution": "The enemy is bleeding, broken, swaying. The Knight walks forward — not fast, not slow — and raises the blade with the patience of a crown.",
    "guardians_oath": "The Knight speaks — not a prayer, not a spell, but a promise. 'While I stand, I hold.' The words don't echo; they settle.",
    "warlords_fury": "The Knight is bleeding. The enemy is closing in. And the Knight... smiles. Not happiness — recognition. The fury comes.",
    "crown_of_iron": "The Knight doesn't wear a crown. They become one. The posture shifts — not aggressive, not defensive, but regal.",
    "kings_command": "The Knight speaks three words. Not to allies. Not to the enemy. To themselves. A decree. The body obeys.",
    "last_bastion": "They're everywhere. The Knight doesn't count them anymore. Blood in their eyes, cracks in their shield, and still — still — they stand.",
    "oath_strike": "The Knight whispers the Oath as the blade descends — not for the enemy, but for the steel. The edge remembers every promise it has kept.",
    "final_duel": "The Knight lowers their blade and meets the enemy's eyes. 'Just us.' The world falls away — the battle, the noise, the blood. There is only the duel.",
    "legend_of_erchis": "The Knight is on one knee. Blood on the shield. Cracks in the plate. And then — light. Not from the sun. From the Oath itself.",
    # Lancer skills
    "flame_imbue": "The Lancer runs a hand along the spear shaft. Where the fingers pass, metal glows — cherry red, then orange, then white.",
    "frost_imbue": "The Lancer breathes on the spear. The breath is cold — not winter cold, but something older. Frost crawls along the shaft.",
    "gale_thrust": "The spear is a blur — not because it's fast, but because the Lancer is already past. Wind trails the shaft like a ghost.",
    "lancer_guard_break": "The enemy's shield is a wall. The Lancer doesn't aim at it — they aim at the gap, the weld, the inch that was never quite perfect.",
    "cyclone_wall": "The arrows come — three, five, seven. The Lancer spins the spear like a staff, and the shaft becomes a blur. Every shaft splinters.",
    "warriors_focus": "The Lancer plants the spear and breathes. Not a battle cry, not a prayer — just a breath. The kind that comes before everything else.",
    "storm_imbue": "The Lancer raises the spear to the sky. The sky grumbles. Then it agrees. Lightning crawls down the shaft.",
    "stone_imbue": "The Lancer drives the butt of the spear into the ground. The earth trembles. When they raise it, the shaft is heavier, denser.",
    "sky_piercer": "The Lancer folds low — knees bent, spear tucked — and then unfolds like a spring uncoiling. The spear hits armor and doesn't slow.",
    "falcon_rush": "The enemy blinks. The Lancer is gone. Not hidden — just fast. By the time the enemy's eyes open, the spear is already in their ribs.",
    "dragon_fang": "The Lancer commits — full body, full weight, full reach. The spear sinks to the crossguard. The enemy's eyes go wide.",
    "elemental_weakness": "The Lancer doesn't strike — they probe. The spear tip taps armor, tests joints, finds the gaps. Each tap leaves a weakness.",
    "battle_readiness": "The Lancer settles into the stance — feet apart, spear angled, weight centered. It's not a pose. It's a decision.",
    "gale_imbue": "The Lancer swings the spear in a wide arc, and the wind doesn't resist — it follows. Air spirals around the shaft, around the arm.",
    "thunder_imbue": "This is not lightning. Lightning is fast, bright, and done. Thunder is the voice that comes after — the sound that shakes the walls.",
    "dragon_dive": "The Lancer doesn't jump — they launch. For a moment, they're above the battlefield, spear pointed down. Then gravity and intent pull them back.",
    "frostbite": "The enemy is already hurting. The Lancer touches the wound with the spear tip and pushes cold through it. Deep cold, the kind that reaches bones.",
    "shock_lock": "The spear tip finds the existing wound and sends a jolt through it. Not enough to kill. Enough to seize. The enemy's body locks.",
    "iron_breeze": "The enemy swings. The Lancer isn't there — not because they dodged, but because the wind moved them. It looks like a dance.",
    "elemental_surge": "The Lancer closes their eyes for half a second. When they open them, every element flares. The spear becomes a prism.",
    "inferno_imbue": "The basic flame was a candle. This is a bonfire. The spear becomes a brand. The air around it distorts. The ground beneath it chars.",
    "glacier_imbue": "The frost imbue was a coating. This is a glacier. The spear isn't cold — it is cold itself, the concept made metal.",
    "tempest_imbue": "The storm imbue was a spark. This is the whole sky. Lightning doesn't crawl down the shaft — it lives in it, coils around it.",
    "volcano_imbue": "The Lancer drives the spear into the earth and wills two elements at once — fire below, stone above. It is magma made solid.",
    "thunder_pursuit": "The enemy runs. The Lancer follows — not running, but hunting. Each step cracks with thunder, each stride closes the gap.",
    "world_splitter": "The Lancer drives the spear down — not at the enemy, but at the world. The ground splits. The crack runs forward, fast, hungry.",
    "crimson_spear": "The Lancer is bleeding. They should be falling. Instead, the spear begins to glow. Red. Deep. Hungry. 'Take what you need.'",
    "elemental_collapse": "The Lancer snaps their fingers. Every element inside the enemy's wounds detonates at once. The chain reaction is silent. The collapse is not.",
    "celestial_javelin": "The Lancer pulls from the sky itself. What forms in their hand is not metal — it is light, condensed into a shape that remembers what a spear is.",
    "avatar_of_the_storm": "The Lancer closes their eyes and feels all six elements. They don't choose one. They choose all. They are a storm wearing a face.",
    # Mage skills
    "arcane_burst": "The Mage's palms come together. Light gathers — not from the sun, not from a flame, but from the space between thoughts. It compresses, densifies, becomes a sphere the size of a fist. The Mage opens their hands. The sphere leaves. The impact is not loud. It is final.",
    "wind_blade": "The Mage doesn't chant. They gesture — a casual sweep of the hand, like brushing hair from their face. The air disagrees. A crescent of compressed wind leaves the gesture and crosses the battlefield in silence. The enemy feels the cut before they hear it. They don't hear it.",
    "stone_spear": "The Mage stomps. The ground obeys. Stone tears free — not gradually, but violently — and shapes itself into a spear mid-flight. It's not elegant. It's geology with intent. The enemy's armor meets stone, and the stone doesn't care about the armor.",
    "arcane_ward": "The Mage's finger moves — quick, precise, practiced. Lines appear in the air, connect, interlock. The runes glow blue, then solidify. The wall doesn't block attacks. It unmakes them. The enemy's blade hits the ward and the force just... disperses. The Mage is already drawing the next one.",
    "blink": "The enemy swings. The Mage isn't there. Not dodged — gone. Sparks hang in the air where they stood, and a heartbeat later, the sparks gather three meters to the left. The Mage reforms, already casting. The enemy's sword is still falling. The Mage is already finished.",
    "water_lash": "The Mage's hand opens. The air gets drier. The moisture gathers — from breath, from sweat, from the morning dew — and coils around the Mage's arm like a serpent. They snap it forward. The lash hits the enemy's face with the force of a wave and the precision of a whip. The enemy staggers, wet, stunned.",
    "fireball": "The Mage's finger traces a circle. The circle catches fire — not gradually, but instantly, as if the air inside it was always meant to burn. The fireball forms, condenses, and launches. The impact is not subtle. The enemy's armor blackens. Their skin blisters. The Mage is already tracing the next circle.",
    "frost_prison": "The Mage exhales. The breath is cold — not winter cold, but absolute cold, the cold of empty space. Ice forms on the ground, crawls toward the enemy, and climbs. It seals their feet, their legs, their torso. The enemy is locked in ice. The Mage watches. The ice watches too.",
    "chain_lightning": "The Mage raises a hand. The sky doesn't darken — it sharpens. The bolt descends, hits the first enemy, and doesn't stop. It leaps — from enemy to enemy, from body to body — in a chain of white-blue flashes. Two enemies seize simultaneously. The Mage lowers their hand. The thunder arrives late.",
    "mana_shield": "The Mage doesn't raise a shield. They become one. Mana spreads across their skin like a second layer, glowing, humming, alive. The enemy's blade hits it and bends — not the blade, but the force behind it. The mana absorbs, disperses, redirects. The Mage stands inside their own magic, untouched.",
    "spell_seal": "The Mage draws a lock. The lock becomes real. Chains of glowing script wrap around the enemy's wrists, their throat, their magic. The enemy tries to cast. The chains tighten. The spell dies in their throat. The Mage watches, patient, while the enemy learns what silence feels like.",
    "arcane_chains": "The enemy is already suffering — burning, bleeding, frozen. The Mage adds to it. Runes appear beneath the enemy's feet, and chains rise from them like serpents from water. They wrap, tighten, and hold. The enemy can't move. The Mage can. That's the arrangement.",
    "illusory_double": "The Mage doesn't move. They multiply. Three Mages stand where one was. Four. Five. All identical, all casting, all real — or none of them are. The enemy swings at one. It dissipates. They swing at another. Also false. The real Mage is already behind them, and the fireball is already in the air.",
    "gravity_well": "The Mage closes their fist. The world leans. Not metaphorically — physically. A dark sphere appears in the air, and everything starts falling toward it: dust, arrows, the enemy's footing. The enemy slides, stumbles, is pulled inward. The Mage watches. The sphere doesn't let go. It just pulls.",
    "telekinetic_crush": "The enemy is already wounded. The Mage raises a hand. The enemy rises — not jumping, not flying, but lifted. Invisible force wraps around them and tightens. Armor dents. Bones creak. The enemy's eyes go wide. The Mage's hand closes. The enemy drops. The Mage opens their hand.",
    "mirror_spell": "The enemy casts. The spell flies. The Mage doesn't dodge — they reflect. A rune appears, glassy, shimmering. The spell hits it, sinks in, and for a moment, disappears. Then it comes back — reversed, redirected, angry. The enemy takes their own magic to the face. The Mage adjusts the rune. Next.",
    "mind_maze": "The Mage speaks — not a spell, but a word. One word, in a language the enemy doesn't know but somehow understands. And then the world changes. The battlefield becomes a maze — walls where there were none, paths that loop back, exits that lead deeper. The enemy stumbles through their own mind. The Mage watches from outside.",
    "void_portal": "The Mage reaches into the air and pulls. Space tears — not violently, but like fabric parting. A dark oval appears. Another opens across the battlefield. The Mage steps into one and emerges from the other. The enemy charges the first portal. It closes. The Mage is already behind them.",
    "phantom_terrain": "The Mage waves a hand. The battlefield lies. The ground that was flat now looks like a chasm. The wall that was solid now looks like a door. The enemy charges the door and hits the wall. They avoid the chasm and step onto nothing. The Mage watches the enemy fight a battlefield that doesn't exist.",
    "dream_step": "The Mage doesn't teleport. They dream. Their body becomes mist — pale, drifting, intangible. They pass through the enemy's mind, through memories and fears, and emerge on the other side. The enemy sees things that aren't there. The Mage is already casting. The dream is already over.",
    "meteor_storm": "The Mage raises both arms. The sky answers — not with clouds, but with fire. Red cracks appear overhead, and through them, stones fall. Not rocks — meteors. Burning, screaming, patient. Three impacts. Three craters. The enemy is in one of them. The Mage lowers their arms. The sky closes.",
    "blizzard": "The Mage spins their staff. The air freezes. Not gradually — absolutely. Snow erupts from nowhere, wind screams from nothing, and the battlefield becomes a white wall. The enemy can't see. Can't move. Can't feel their fingers. The Mage stands in the eye of the storm, calm, dry, watching.",
    "thunderfield": "The Mage kneels and draws a rune on the ground. The rune crackles. Above it, clouds form — dark, low, angry. Lightning descends. Not once — repeatedly. The zone becomes a prison of thunder. The enemy inside it doesn't just take damage. They take electricity.",
    "time_slow": "The Mage's hands move — not casting, but turning. An invisible wheel. And the world slows. The enemy's sword is still falling, but it falls like it's underwater. Their dodge starts but finishes late. Their thoughts form but arrive slow. The Mage walks between them, normal speed, untouched by the drag.",
    "elemental_convergence": "The Mage stands still. The elements come. Fire circles left. Ice circles right. Lightning spirals up. Stone orbits below. Wind wraps around all of it. They shouldn't coexist. They don't care. The Mage compresses them — all five, into one point — and releases. The blast is every color and none of them.",
    "mana_explosion": "The Mage is cornered. Wounded. Out of options. So they choose the last one. They pull mana inward — not from the surroundings, but from their own reserves, their own life force. Their body glows. Their skin cracks with light. And then they release. The explosion is not fire, not ice, not lightning. It's force.",
    "reality_fracture": "The Mage draws a line. Not on the ground — in reality. The world cracks along it. Gravity tilts. Distance stretches. Up becomes sideways. The enemy tries to run and moves backward. They try to dodge and fall upward. The rules are broken. The Mage wrote new ones.",
    "time_stop": "The Mage snaps their fingers. The world stops. Not slows — stops. The enemy's sword hangs in the air. The arrow is frozen mid-flight. The fireball is a still photograph. The Mage walks through the stillness, adjusts position, casts a spell, and returns. They snap again. Time resumes.",
    "cosmic_convergence": "The Mage looks up. The sky isn't the sky anymore — it's a canvas. Symbols appear, arranged like constellations, each one a word in a language older than the world. They align. They gather. The light condenses into a single point, blinding, absolute. And then it descends — a beam of celestial force that doesn't just pierce armor. It pierces reality.",
    "legend_of_the_arcane": "The Mage is dying. The magic is not. It doesn't gather — it erupts. Fire first. Then ice. Then lightning — through the cracks in the ice. Then stone — through the burns. Then wind — through the wounds. Then void — through the gaps in reality. Then time — the enemy's body ages a decade in a second. Then space. Eight elements. Eight impacts. One turn. The Mage isn't casting anymore. They are the elements.",
    # Assassin skills
    "shadow_strike": "The Assassin's blade doesn't catch the light — it eats it. The cut is shallow but cold, and something worse than blood leaks out.",
    "heart_piercer": "Armor has gaps. Not many — but enough. The blade finds the gap the way water finds a crack. And something darker than the blade settles into the wound.",
    "smoke_veil": "The pellet hits the ground. Smoke blooms — instant. One second the Assassin is there. The next, there is only smoke and footsteps that are already somewhere else.",
    "death_mark": "The Assassin traces a symbol in the air. The mark appears on the enemy's chest, dark as ink, cold as a closing door. 'You are already chosen.'",
    "shadow_focus": "The Assassin closes their eyes. The shadows in the room shift, moving toward the Assassin like water finding a drain. When they open their eyes, they are hungry.",
    "silent_execution": "The enemy is talking. The Assassin is already moving. The blade crosses the distance in silence. The enemy's sentence stops mid-word.",
    "phantom_strike": "The enemy sees the Assassin move. Then they see it again. Two shapes — both striking, both real, both impossible. The afterimages fade, but the cuts don't.",
    "crimson_dash": "The Assassin doesn't run — they cut. The dash is a line drawn through the enemy, red on one side and black on the other.",
    "night_veil": "The darkness thickens, solidifies, wraps around the Assassin like a second skin. The enemy looks at the spot and sees nothing. As if the shadow swallowed them. It did.",
    "shadow_terror": "The Assassin whispers. Not words — a frequency the ear doesn't catch but the mind does. The enemy sees their own death wearing their face.",
    "shadowstep": "The Assassin steps left — and isn't. The shadow swallows them. A heartbeat later, the shadow behind the enemy opens, and the Assassin steps out.",
    "dark_pursuit": "The enemy runs. The Assassin follows — not fast, but inevitable. Every shadow the enemy passes through, the Assassin is already there.",
    "vanishing_kill": "The blade enters. The blade leaves. The Assassin enters the shadow. The enemy falls. It happens in the space between heartbeats.",
    "shadow_flurry": "The Assassin doesn't swing three times. They swing once, and the shadow swings twice more. Three cuts arrive at the same moment.",
    "soul_sever": "The blade changes — not in shape, but in nature. Shadow crawls along the edge, and when it cuts, it parts something deeper than flesh.",
    "shadow_clone": "The Assassin splits — not physically, but perceptually. Two Assassins stand where one was. The enemy swings at one and hits nothing.",
    "shadow_prison": "The Assassin raises a hand. The shadows on the ground rise with it — reaching for the enemy, wrapping around ankles, wrists, throat.",
    "black_feathers": "The enemy swings. The Assassin shatters — not into blood, but into feathers. Black, iridescent, alive. The ravens scatter. The Assassin is gone.",
    "eclipse_blade": "The Assassin raises the blade. The light doesn't dim — it leaves. It pours into the steel like water into a drain, and the weapon becomes a void with an edge.",
    "shadow_convergence": "The Assassin opens their hand. Every shadow in the room rushes toward them like rivers to the sea. The room brightens. The Assassin darkens.",
    "night_requiem": "The Assassin moves through the enemy. The blade visits each one in turn — a whisper of steel and shadow. Three cuts, three breaths of silence.",
    "deaths_whisper": "A whisper behind the enemy's ear, close enough to feel breath that isn't there. The message says: 'Everything you have left belongs to me now.'",
    "umbral_cloak": "Where the Assassin stood, there is only a silhouette. The enemy attacks it. Their blade passes through. The Assassin is already behind them.",
    "final_contract": "The Assassin is dying. They accept it. The contract is signed in blood and intent. The blade rises with the weight of a final promise.",
    "king_slayer": "The blade finds the chink that power hides, the gap that confidence leaves open. The enemy falls. The throne is empty.",
    "shadow_devour": "The shadows on the enemy tear free — all of them — and pour into the Assassin's blade. The enemy screams from the sudden absence.",
    "eclipse_burst": "The Assassin stops. The shadows surge like a dam breaking. The blade becomes a point of absolute darkness. One step. One strike. The world goes dark.",
    "reapers_arrival": "The noise stops. The Assassin walks forward with the patience of someone who has already decided the outcome. This is not a fight. This is an arrival.",
    "eclipse_of_shadows": "The Assassin's body stops being solid. It becomes shadow. Every shadow ever collected surges forward at once. The enemy doesn't see the blade. They see the eclipse.",
    # Hunter skills
    "rapid_shot": "The first arrow is a warning. The second is a lesson. The Hunter's hands blur — the point isn't power, it's building Spirit Guidance fast.",
    "piercing_shot": "The Hunter draws past the chin. The bow bends further than it should. The arrow doesn't punch through armor; it ignores it, the way a needle ignores cloth.",
    "snare_trap": "The Hunter throws — not an arrow, but a net. Steel cables snap tight on impact, and the enemy's legs are locked. They can still swing. They just can't get closer.",
    "camouflage": "The Hunter doesn't vanish — they become. A cloak of leaves, a shift of shadow, a stillness the eye slides past. The enemy scans and sees nothing.",
    "eagle_eye": "The world narrows. The noise fades. Only the target exists. Every movement becomes a trajectory. Every weakness becomes a target.",
    "crippling_shot": "The Hunter aims for the leg — the thigh, the knee, the tendon. The arrow arrives, and the enemy's stride becomes a stumble. They can still fight. They just can't get closer.",
    "poison_arrow": "The Hunter draws the vial — forest green, thick, patient. The arrowhead drinks it. The shot is clean, the wound is small, and the venom does its work.",
    "flash_bang": "The Hunter throws — a small sphere, no bigger than a fist. The flash is white. The bang is deafening. The enemy staggers.",
    "twin_shot": "Two arrows on the string. Two targets — or one target, twice. The arrows leave together, travel together, arrive together. The enemy raises their shield for one. The other finds the gap.",
    "smoke_bomb": "The Hunter throws — a metal egg that hisses on impact. Smoke fills the field. The enemy advances blind, swinging at shapes. The Hunter doesn't.",
    "hunters_mark": "The Hunter nocks an arrow — not to fire, but to mark. The tip glows, and a sigil appears on the enemy's chest. It pulses. Every movement becomes predictable.",
    "falcon_strike": "The Hunter raises a gloved fist. The falcon drops — not flies, drops — like a stone with talons. The enemy hears the shriek before the impact.",
    "spirit_walk": "The Hunter closes their eyes. The battlefield fades — not visually, but dimensionally. They step sideways, into the place where the dead walk. Arrows pass through where they stood.",
    "rain_of_arrows": "The Hunter doesn't aim — they paint. Arrows leave the bow in a stream, each one finding a different angle. The sky darkens with shafts. The enemy raises their shield. It wasn't built for rain.",
    "wolf_companion": "The Hunter whistles — low, short, a sound that belongs to the forest. A wolf answers. It hits the enemy low and fast, teeth finding the hamstring.",
    "explosive_trap": "The Hunter throws — a heavy sphere, iron casing, alchemical core. The explosion is orange and loud and effective. The world becomes heat and noise.",
    "hawk_vision": "The Hunter's eyes change. The battlefield becomes a map — every enemy a dot, every movement a line. Every weakness is a target.",
    "backflip": "The enemy closes. The Hunter flips — not away, but up and over, landing three steps back, bow already rising. The enemy's sword cuts empty air.",
    "monster_slayer": "The Hunter has killed hundreds of these. They know the anatomy — the soft spot, the gap, the vein that pulses before a charge. The arrow finds it.",
    "bear_trap": "The Hunter throws — iron jaws, heavy chain, a spring that could take a leg. The jaws snap shut and the enemy is locked. They're going nowhere.",
    "volley_master": "The Hunter doesn't aim — they paint. Arrows leave the bow in a stream, each one finding a different angle, a different gap. The sky goes dark for a heartbeat.",
    "spirit_bind": "The Hunter stamps a foot. The earth opens — and a hand rises. Translucent, vast, patient. It grips the enemy and holds. The dead are stronger than the living.",
    "storm_arrow": "The Hunter draws. The sky rumbles. The arrowhead glows — blue, white, electric. The string releases. The lightning follows, riding the shaft.",
    "natures_blessing": "The Hunter is bleeding. They press a hand to the earth — not in prayer, but in kinship. The forest answers. Roots wrap the wound. Moss grows over the cut.",
    "survival_instinct": "The blade is coming. The Hunter doesn't think — they react. The body moves before the mind catches up — the way a deer moves at the snap of a twig.",
    "alpha_command": "The Hunter doesn't command — they lead. The wolf howls. The falcon screams. Every beast within earshot straightens. The Hunter's presence shifts from archer to apex.",
    "ancient_tracker": "The Hunter reads the ground like a book. The bent grass. The scuffed stone. The drop of blood that dried three days ago. The enemy thought they escaped.",
    "tracking_instinct": "The Hunter watches. Not the enemy — their trail. The way they favor the left leg. The way their guard drops after a swing. Every move the enemy makes, the Hunter already knows.",
    "world_hunt": "The enemy runs. The Hunter follows. Not fast — relentless. Across the field, through the trees, over the ridge. Always the same distance behind. Escape becomes impossible.",
    "legend_of_the_wild": "The Hunter is on one knee. Blood on the bow. The string is broken. And then — the forest moves. Not the trees, not the wind, but everything alive. Every ancestor who ever lived rises behind the Hunter, each one drawing a bow made of memory.",
    # Rogue skills
    "dirty_trick": "The Rogue flicks dirt, a coin, debris — straight into the enemy's eyes. The enemy blinks. The Rogue grins. By the time they stop blinking, the Rogue is already somewhere else.",
    "hidden_blade": "The enemy searches the Rogue for weapons. They find the obvious ones. They miss the one that matters. The blade slides from the bracer like a whispered secret.",
    "opportunist_strike": "The enemy is rubbing their eyes, pulling at a tripwire. The Rogue watches. Waits. Then the knife arrives — polite, precise, and completely unfair.",
    "acrobatic_roll": "The blade comes down. The Rogue isn't there — they're below it, rolling through the gap between the swing and the ground. They come up on the other side, already moving.",
    "quick_step": "The Rogue bounces on their toes. Left foot forward, weight centered, blade low. It looks casual. It's not. Every muscle is coiled. Every angle is calculated.",
    "pocket_sand": "The hand moves — fast, casual, like brushing dust off a sleeve. The sand follows. Coarse, gritty, aimed. The enemy's eyes flood with tears and the world goes white.",
    "flash_powder": "The Rogue tosses the pouch — underhand, lazy. It bursts. Not smoke. Light. White, searing, absolute. The enemy's world becomes a sun with no edges.",
    "tripwire": "The wire is thin — gut string, nearly invisible. The enemy steps forward. The wire catches. The ground arrives. The Rogue is already above them, knife descending.",
    "knife_fan": "The Rogue's hands move — left, right, left — and three daggers leave the fingers in a spread that covers every angle. Two find their mark. The third was a distraction.",
    "hook_chain": "The chain uncoils from the Rogue's wrist — fast, singing. The hook catches the enemy's belt, their shield strap, their confidence. The Rogue pulls.",
    "feign_death": "The blow lands — or seems to. The Rogue crumples. Goes still. Eyes open, blank, empty. The enemy turns away. And behind them, the corpse sits up and smiles.",
    "wall_run": "The enemy swings low. The Rogue doesn't dodge — they run. Up the wall, across it, boots finding stone like it's flat ground. The Rogue drops from above with gravity on their side.",
    "sleight_of_hand": "The enemy is distracted. The Rogue brushes past them, casual as a pickpocket. When they're done, the enemy's weapon feels lighter. Their pouch feels empty.",
    "mirror_image": "The Rogue splits. Not physically — perceptually. Three Rogues, four, each running a different direction. The enemy chases one. It vanishes. The real one is already behind them.",
    "smoke_bomb_rogue": "The pellet hits the ground and the world goes dark. Not a cloud — a wall. The enemy can't see their own hands. The Rogue moves through the smoke like it's home.",
    "false_surrender": "The Rogue drops to one knee. Hands up. Blade lowered. The enemy grins and steps forward. The Rogue's knife enters from below, from the angle that kneeling created.",
    "misdirection": "The Rogue points. The enemy looks. There's nothing there — but the enemy's body committed before their brain caught up. By the time they turn back, the Rogue has moved.",
    "counter_stab": "The enemy is reeling — blinded, tripped, shaken. The Rogue doesn't wait. Two stabs, fast, precise, from two different angles. The first opens a wound. The second opens a question.",
    "escape_artist": "The chains tighten. The enemy grins. The Rogue doesn't — they work. Fingers find the weak link. Three seconds. The chains fall. The Rogue stretches and looks at the enemy.",
    "tricksters_flurry": "The Rogue moves — not fast, but busy. Left hand flicks sand. Right hand slides a blade across the ribs. Left hand again, a tripwire. Three hits, three tricks, three wounds.",
    "lucky_escape": "The blade is at their throat. The arrow is in the air. And the Rogue... ducks. Not deliberately — instinctively, luckily, impossibly. Everything misses by an inch.",
    "ambush_master": "The enemy walks through the clearing. They check the bushes, the trees. The Rogue is above them — on the branch they forgot to check. The drop is silent. The knife is certain.",
    "grand_heist": "The enemy is wounded, distracted. The Rogue slides in — not to kill, but to take. When they step back, the enemy's chest plate is gone. The knife is in the gap where it used to be.",
    "coin_toss": "The Rogue flips a coin — gold, spinning, catching the light. The enemy's eyes follow it. Up. Down. And while they're watching the money, the Rogue takes everything else.",
    "shadow_step_rogue": "The enemy blinks. The Rogue is gone. Then the knife arrives from a direction that doesn't make sense. The enemy turns toward it. The Rogue is already somewhere else.",
    "master_picklock": "The enemy's guard is a lock. The Rogue is a key. One twist, two, three. The enemy's defense opens like a door that forgot it was supposed to stay shut. The Rogue steps through.",
    "king_of_thieves": "The enemy has power. The Rogue doesn't need it — they need a moment. When it's done, the enemy is slower, weaker, dimmer. The Rogue is faster, sharper, meaner.",
    "tricksters_gambit": "The Rogue looks at the odds and grins. Three strikes, three angles, three tricks. The first takes blood. The second takes balance. The third takes armor. The gamble is insane.",
    "perfect_crime": "The enemy is standing. Then they're not. No sound, no flash, no warning. Just a cut that appears like it was always there. The Rogue was here. The Rogue is gone. There is no evidence.",
    "legend_of_trickery": "The Rogue is cornered. Wounded. And then — they smile. The shadows bend. The light lies. The enemy sees three Rogues, then none, then six. And when the Rogue strikes, the enemy falls without understanding what happened.",
    # --- Bard Mastery ---
    "song_of_heroes": "The Bard plays a chord. The allies feel it — their blades hum, their aim sharpens. The enemy cannot dodge what's coming.",
    "song_of_hope": "A gentle melody rises. The allies feel their hearts steady. The enemy feels a pull — not physical, but inevitable. The Bard's eyes glow. The enemy is coming closer.",
    "resonant_strike": "The Bard plays a note that rings in the enemy's bones. It doesn't just sound — it hurts. The enemy staggers, their grace shattered by the resonance.",
    "harmony_shield": "The Bard hums a protective chord. The air shimmers around every ally, solidifying into a barrier of sound.",
    "sunrise_chorus": "The Bard sings the first note of dawn. The darkness lifts. The debuffs burn away. The allies stand straighter.",
    "song_of_wisdom": "The Bard plays a melody that clears the mind. An ally feels their cooldown reset. The enemy feels their voice vanish — silenced by the music.",
    "festival_rhythm": "The Bard plays a lively tune. The allies can't help but move — faster, sharper, ready. The enemy watches the party come alive.",
    "discord": "The Bard plays a wrong note — on purpose. The sound grates. The enemy flinches. Their thoughts scatter. Their body stiffens.",
    "dance_of_blades": "The Bard spins, and the music spins with them. Invisible blades of sound cut the enemy. Blood follows the rhythm.",
    "sirens_call": "The Bard sings a haunting melody. The enemy's feet move on their own, drawn toward the sound. Their mind clouds. Their body obeys the music.",
    "ballad_of_hope": "The Bard sings a slow, rising ballad. The allies feel their wounds close. The enemy hears the hope in it and despairs.",
    "lullaby_of_fallen_kings": "The Bard sings a lullaby — old, slow, final. The enemy's eyes grow heavy. Their knees buckle. The song says sleep. The enemy obeys.",
    "song_of_freedom": "The Bard plays a soaring melody. Chains break. Curses burn. The allies are free. The enemy turns on its own.",
    "moon_serenade": "The Bard plays a silver melody. The moon answers — or seems to. Wounds close. The allies glow with soft light.",
    "inspiring_solo": "The Bard plays a solo that builds and builds. The allies feel their blood surge. Their blades feel lighter. The enemy feels heavier.",
    "echo_verse": "The Bard plays a verse that mirrors the enemy's affliction. The sound bounces back, empowering every ally who hears it.",
    "epic_tale": "The Bard tells a story — a real one, about the party. The allies hear themselves as heroes. They become heroes. The wounds close.",
    "muses_blessing": "The Bard channels something older than music. The allies feel clarity, insight, purpose. The enemy feels small.",
    "curtain_call": "The Bard plays the final note. It rings. It builds. It shatters the enemy's confidence like glass.",
    "song_of_fortune": "The Bard plays a lucky melody. The dice reroll. The enemy burns. The music doesn't stop.",
    "heros_anthem": "The Bard plays the opening anthem. Every ally stands taller. Every blade sharpens. The enemy hears it and knows: this is a fight they won't win.",
    "world_orchestra": "The Bard conducts the battlefield. Every ally is an instrument. Every note is power. The symphony builds. The enemy is small.",
    "grand_performance": "The Bard performs the ultimate show. The enemy is the audience. The audience is stunned. The show is over.",
    "memory_song": "The Bard plays a song from a forgotten age. The allies remember who they are. The enemy forgets why they came.",
    "legend_keeper": "The Bard sings the legend of the party itself. Every ally feels it — the power, the endurance, the glory. The wounds close. The enemy is not in this legend.",
    "whispered_melody": "The Bard whispers a melody that crawls into the enemy's mind. It doesn't stop. The enemy's thoughts fracture. Their body weakens.",
    "travelers_tune": "The Bard plays a walking song. The allies feel their fatigue lift. Their steps lighten. The enemy is already tired. The Bard is just getting started.",
    "requiem_of_the_heavens": "The Bard plays a chord. The heavens answer. Every song, every dance, every rule — all at once. The battlefield becomes a cathedral. The audience is the heavens.",
    "symphony_of_creation": "The Bard is dying. The instrument is broken. And then — they sing. The world joins. Every rule activates. Every wound closes. The enemy is the instrument. The audience is the world.",
    # --- Priest Skills ---
    "swift_prayer": "The Priest doesn't have time to kneel. They just reach — one hand, one thought, one word. The light is small, barely a spark. But it's first. It's always first.",
    "light_barrier": "The Priest traces a circle in the air. It stays — golden, humming, patient. The enemy's blade meets it and the wall holds — not deflecting, but absorbing.",
    "bless": "The Priest speaks the old words — not loud, not commanding, but inviting. The light that answers is gentle. It settles on the shoulders like a mantle.",
    "holy_water": "The Priest pulls a vial — clear water, blessed this morning. They throw it. The water doesn't splash; it sears. Holy water doesn't negotiate with evil. It just burns.",
    "blinding_light": "The Priest opens their palm. The light is not gentle. It is the light of judgment — white, absolute, and furious. The enemy's vision whites out.",
    "soul_ward": "The Priest draws a sigil in the air — complex, precise, ancient. It solidifies into a seal that orbits them slowly. It doesn't stop blades. It stops the things blades can't.",
    "blessing_of_renewal": "The Priest doesn't heal the wound. They bless the body. The light settles into the target's skin — not a flash, but a glow. Slow. Steady. Persistent.",
    "chain_of_light": "The Priest looks up. The sky looks back. Chains — not iron, but light — descend. They wrap around the enemy with the patience of a verdict.",
    "cleansing_flame": "The Priest opens their palm. The fire is white — not hot, not red, but clean. It wraps around the enemy and finds the corruption. It burns that and nothing else.",
    "angels_grace": "The Priest doesn't summon the feathers. They just arrive — white, soft, impossible, drifting like snow. Each one is a whisper of approval from something vast and kind.",
    "judgment_strike": "The Priest doesn't swing a weapon. They extend a hand. The holy power that erupts is not a spell — it's a verdict. It hits the enemy like a gavel.",
    "divine_rebuke": "The Priest doesn't shout. They point. One finger, one direction, one judgment. The holy power that erupts is not a request. It's a boundary.",
    "light_of_hope": "The fear is a weight — cold, old, pressing. The Priest closes their eyes and remembers why they kneel. The light comes from within, soft and steady. The fear lifts.",
    "divine_light_priest": "The Priest raises both hands. The light doesn't gather — it arrives. A pillar, golden, solid, patient. It falls on the wounded and the wounds close. Completely.",
    "mass_purify": "The relic is old — a shard of something holy. When the Priest raises it, the light doesn't just glow. It cleanses. Poison evaporates. Curses unravel.",
    "heavens_judgment": "The Priest raises both hands. The sky opens — not with clouds, but with purpose. A beam of holy light descends, silent, absolute. It finds the enemy. It doesn't negotiate.",
    "radiant_prison": "The Priest draws a square in the air. The light doesn't descend — it grows. Bars of radiance rise from the ground, locking into place around the enemy. A cage.",
    "beacon_of_faith": "The Priest raises a hand. Light erupts — not outward, but upward. A pillar of radiance punches into the sky. Everyone on the battlefield sees it.",
    "sunflare": "The Priest holds both palms upward. The light gathers — not a flash, but a star. Small, white, burning, impossible. It rises. It detonates. The battlefield whites out.",
    "radiant_bulwark": "The Priest raises both hands. Light doesn't just glow — it towers. A wall of radiance rises from the ground, solid, humming, alive. The enemy swings. The wall holds. And then — the wall flares.",
    "sanctuary_priest": "The Priest speaks the word. The ground answers. Symbols — ancient, golden, burning — bloom across the earth. This isn't just a ward. It's a fortress. And when it breaks? The shards become chains.",
    "holy_lance": "The Priest doesn't throw a weapon. They throw a verdict. The lance forms in their hand — pure holy light compressed into a spear. It flies. It doesn't miss.",
    "promise_of_heaven": "The Priest doesn't heal the wound. They make a promise. The light settles into the target — not as a glow, but as a countdown. Two turns. The promise is growing.",
    "hymn_of_salvation": "The Priest sings. Not a battle cry — a hymn. Old, simple, the kind sung in temples at dawn. Every ally on the battlefield feels it — a warmth, a steadiness, a closing of wounds.",
    "final_judgment": "The Priest speaks the words. Not a prayer — a sentence. Chains of light descend. Light blazes. The enemy is bound and blind at the same time — chained, seared, locked in holy judgment.",
    "holy_revelation": "The Priest closes their eyes. The visions come — not asked for, but given. They see the enemy's past, their fears, the crack in their armor that no one else can see.",
    "prayer_circle": "The Priest begins to pray — not one prayer, but all of them. Every prayer they know, spoken simultaneously, woven together. The light that comes is a cathedral of radiance.",
    "divine_covenant": "The Priest speaks the covenant — not a prayer, but a contract. Golden threads appear, connecting the Priest to the sky, to the earth, to something beyond. The threads pulse with power.",
    "choir_of_heaven": "The Priest opens their mouth. What comes out is not one voice. It's a choir — vast, harmonious, impossible. The sound fills the battlefield, and it's not just sound. It's judgment. It's mercy.",
    "legend_of_the_faithful": "The Priest is dying. The faith is not. They kneel, and the heavens descend. Wings unfold behind the Priest: not two, not four, but countless. The Priest becomes a vessel. The divine pours through them.",
}

RARITY_COST = {"common": 50, "uncommon": 150, "rare": 400, "epic": 1000, "legendary": 5000}
RARITY_TIME = {"common": 10, "uncommon": 30, "rare": 60, "epic": 120, "legendary": 300}
for _s in SKILLS:
    _s.update(SKILL_EXTRAS.get(_s["id"], {}))
    _s["rarity"] = SKILL_RARITY.get(_s["id"], "common")
    _s["execution_text"] = SKILL_EXEC.get(_s["id"], "")
    if _s.get("rarity") != "legendary" and not _s.get("type") and not _s.get("inverse_hp_scaling"):
        _s["mastery_req"] = []
    _s["cost_gold"] = RARITY_COST.get(_s["rarity"], 50) * _s.get("level_req", 1)
    _s["learn_seconds"] = RARITY_TIME.get(_s["rarity"], 10) + (_s.get("level_req", 1) - 1) * 5



# ============================================================
# DRUID SKILLS — 30, transcribed from docs/skills/druid.md
# ============================================================
# The Druid shipped with 2 of these 30 while having the most elaborate
# engine support of any mastery (summons, fusion, pack synergy, 15 helpers).
# `damage` values are calibrated against existing caster-mastery skills by
# (rarity, power_type); everything else comes from the spec.
DRUID_SKILLS: list[dict] = [
    {'id': 'entangling_roots', 'name': 'Entangling Roots', 'type': 'druid', 'rarity': 'common', 'power_type': 'debuff', 'damage_type': 'magical', 'damage': 3, 'cooldown': 3, 'skill_capacity_cost': 1, 'trigger': 'always', 'status_apply': 'ensnared', 'stat_mod': {'enemy': {'grace': -2, 'might': -2}}, 'mod_duration': 2, 'level_req': 1, 'mastery_req': 'druid', 'weapon_req': 'none', 'cost_gold': 50, 'learn_seconds': 10, 'desc': 'The Druid presses a hand to the earth as thick roots erupt and coil around every foe.', 'execution_text': "The Druid's palm touches soil. The soil answers. Roots — thick, gnarled, older than the battle — burst upward and wrap around the enemy's ankles. The enemy stumbles. The roots tighten. The earth has decided they're staying."},
    {'id': 'thorn_barrage', 'name': 'Thorn Barrage', 'type': 'druid', 'rarity': 'common', 'power_type': 'strike', 'damage_type': 'magical', 'damage': 7, 'cooldown': 2, 'skill_capacity_cost': 1, 'trigger': 'always', 'status_apply': 'bleeding', 'stat_mod': {'enemy': {'grace': -1}}, 'mod_duration': 2, 'level_req': 1, 'mastery_req': 'druid', 'weapon_req': 'none', 'cost_gold': 50, 'learn_seconds': 10, 'desc': 'The forest floor erupts with razor-sharp spikes as countless enchanted thorns launch at the enemy.', 'execution_text': "The Druid stamps a foot. The ground between them and the enemy becomes a bed of thorns — not gradual, not growing, but instant. The spikes are thin, sharp, and hungry. The enemy's legs become a map of cuts. The blood feeds the soil. The soil asks for more."},
    {'id': 'ancient_bark', 'name': 'Ancient Bark', 'type': 'druid', 'rarity': 'common', 'power_type': 'defend', 'damage': 0, 'cooldown': 4, 'skill_capacity_cost': 1, 'trigger': 'always', 'self_status': 'warded', 'stat_mod': {'self': {'armor_bonus': 4}}, 'mod_duration': 3, 'level_req': 1, 'mastery_req': 'druid', 'weapon_req': 'none', 'cost_gold': 50, 'learn_seconds': 10, 'desc': "Tree bark spreads across the Druid's body like living armor, hardening their skin against attack.", 'execution_text': "The Druid's skin darkens. Not dirt, not shadow — bark. It crawls up their arms, across their chest, over their face. It doesn't restrict movement. It reinforces it. The first blow that lands sounds like an axe hitting oak. The oak doesn't care."},
    {'id': 'healing_bloom', 'name': 'Healing Bloom', 'type': 'druid', 'rarity': 'common', 'power_type': 'heal', 'damage': 0, 'cooldown': 4, 'skill_capacity_cost': 1, 'trigger': 'low_hp', 'self_status': 'warded', 'heal_percent': 0.1, 'stat_mod': {'self': {'essence': 1}}, 'mod_duration': 2, 'level_req': 1, 'mastery_req': 'druid', 'weapon_req': 'none', 'cost_gold': 50, 'learn_seconds': 10, 'desc': 'A radiant blossom opens, releasing soothing pollen that mends wounds.', 'execution_text': 'The Druid cups their hands. A flower grows — not from the ground, but from their palms. It opens slowly, and the pollen that drifts out smells like rain and morning. The wounds close. The pain fades. The flower wilts, content. Triggers when HP is low.'},
    {'id': 'natures_whisper', 'name': "Nature's Whisper", 'type': 'druid', 'rarity': 'common', 'power_type': 'buff', 'damage': 0, 'cooldown': 4, 'skill_capacity_cost': 1, 'trigger': 'always', 'self_status': 'inspired', 'stat_mod': {'self': {'cognition': 3, 'grace': 2}}, 'mod_duration': 3, 'level_req': 1, 'mastery_req': 'druid', 'weapon_req': 'none', 'cost_gold': 50, 'learn_seconds': 10, 'desc': 'Birds and beasts gather to share information. The Druid reads the battlefield through the eyes of the wild.', 'execution_text': "The Druid tilts their head. Not listening — receiving. A sparrow lands on their shoulder. A fox pauses at the treeline. They tell the Druid what they see: the enemy's position, their fear, the gap in their guard. The Druid opens their eyes. They know everything the forest knows."},
    {'id': 'stone_skin', 'name': 'Stone Skin', 'type': 'druid', 'rarity': 'common', 'power_type': 'buff', 'damage': 0, 'cooldown': 4, 'skill_capacity_cost': 1, 'trigger': 'always', 'self_status': 'warded', 'stat_mod': {'self': {'armor_bonus': 3, 'durability': 2}}, 'mod_duration': 3, 'level_req': 1, 'mastery_req': 'druid', 'weapon_req': 'none', 'cost_gold': 50, 'learn_seconds': 10, 'desc': "Rock and bark reinforce the Druid's body, increasing natural resilience.", 'execution_text': "The Druid's skin shifts — not fully bark, not fully stone, but something between. Grey and brown patches appear along their forearms, their shins, their neck. The enemy's blade lands and skids. The Druid doesn't flinch. They've been hit by harder things than steel."},
    {'id': 'spirit_wolf', 'name': 'Spirit Wolf', 'type': 'druid', 'rarity': 'uncommon', 'power_type': 'strike', 'damage_type': 'magical', 'damage': 9, 'cooldown': 4, 'skill_capacity_cost': 1, 'trigger': 'always', 'status_apply': 'bleeding', 'stat_mod': {'enemy': {'might': -2, 'grace': -2}}, 'mod_duration': 2, 'level_req': 3, 'mastery_req': 'druid', 'weapon_req': 'none', 'cost_gold': 150, 'learn_seconds': 30, 'desc': 'A ghostly wolf steps from the forest mist and stands beside the Druid before lunging at the enemy.', 'execution_text': "The Druid whistles — not loud, not human. The mist answers. A shape forms: silver, translucent, eyes like moonlight. The spirit wolf doesn't growl. It doesn't need to. It simply moves, and the enemy bleeds before they understand what happened. The wolf returns to the mist. It will return again."},
    {'id': 'wild_growth', 'name': 'Wild Growth', 'type': 'druid', 'rarity': 'uncommon', 'power_type': 'heal', 'damage': 0, 'cooldown': 5, 'skill_capacity_cost': 1, 'trigger': 'low_hp', 'self_status': 'inspired', 'heal_percent': 0.12, 'stat_mod': {'self': {'essence': 2, 'durability': 2}}, 'mod_duration': 3, 'level_req': 3, 'mastery_req': 'druid', 'weapon_req': 'none', 'cost_gold': 150, 'learn_seconds': 30, 'desc': 'Flowers bloom instantly while vines wrap gently around the wounded, accelerating nature to heal.', 'execution_text': "The Druid spreads their arms. The ground erupts — not with violence, but with life. Flowers bloom in seconds. Vines uncoil and wrap around wounds, gentle as bandages. The pain doesn't just fade; it's absorbed. The forest takes it. The forest doesn't mind. Triggers when HP is low."},
    {'id': 'vine_prison', 'name': 'Vine Prison', 'type': 'druid', 'rarity': 'uncommon', 'power_type': 'debuff', 'damage_type': 'magical', 'damage': 4, 'cooldown': 4, 'skill_capacity_cost': 1, 'trigger': 'opponent_status', 'status_apply': 'ensnared', 'stat_mod': {'enemy': {'grace': -3, 'might': -3}}, 'mod_duration': 3, 'level_req': 3, 'mastery_req': 'druid', 'weapon_req': 'none', 'cost_gold': 150, 'learn_seconds': 30, 'desc': 'Twisting vines weave into an inescapable cage around the enemy.', 'execution_text': "The enemy is already hindered — bleeding, stunned, slowed. The Druid raises a hand. Vines erupt from every direction, weaving together like fingers lacing. The cage forms in a heartbeat. The enemy can see through the gaps. They can't fit through them. The Druid watches. The vines tighten. Only triggers when the enemy has a status effect."},
    {'id': 'fungal_bloom', 'name': 'Fungal Bloom', 'type': 'druid', 'rarity': 'uncommon', 'power_type': 'debuff', 'damage_type': 'magical', 'damage': 4, 'cooldown': 4, 'skill_capacity_cost': 1, 'trigger': 'always', 'status_apply': 'poisoned', 'stat_mod': {'enemy': {'might': -3, 'cognition': -2}}, 'mod_duration': 3, 'level_req': 3, 'mastery_req': 'druid', 'weapon_req': 'none', 'cost_gold': 150, 'learn_seconds': 30, 'desc': 'Glowing spores drift across the battlefield, poisoning enemies and clouding their minds.', 'execution_text': "The Druid breathes out. The breath isn't air — it's spores. Blue, luminescent, slow. They drift like snow, and every enemy they touch begins to cough. The poison isn't fast. It's patient. It seeps into the lungs, the blood, the thoughts. The enemy's swings get weaker. Their decisions get worse. The spores keep drifting."},
    {'id': 'natures_grasp', 'name': "Nature's Grasp", 'type': 'druid', 'rarity': 'uncommon', 'power_type': 'strike', 'damage_type': 'magical', 'damage': 9, 'cooldown': 4, 'skill_capacity_cost': 1, 'trigger': 'always', 'status_apply': 'ensnared', 'stat_mod': {'enemy': {'grace': -2, 'armor_bonus': -2}}, 'mod_duration': 2, 'level_req': 3, 'mastery_req': 'druid', 'weapon_req': 'none', 'cost_gold': 150, 'learn_seconds': 30, 'desc': 'The ground itself reaches for intruders, pulling enemies toward grasping roots.', 'execution_text': "The enemy tries to advance. The ground disagrees. Hands — not hands, roots shaped like hands — burst from the earth and grab their ankles. The enemy is pulled off-balance, dragged forward into a space they didn't choose. The Druid is waiting. The roots are helping."},
    {'id': 'beast_form', 'name': 'Beast Form', 'type': 'druid', 'rarity': 'uncommon', 'power_type': 'buff', 'damage': 0, 'cooldown': 5, 'skill_capacity_cost': 1, 'trigger': 'always', 'self_status': 'inspired', 'stat_mod': {'self': {'might': 4, 'grace': 2, 'durability': 2}}, 'mod_duration': 3, 'level_req': 3, 'mastery_req': 'druid', 'weapon_req': 'none', 'cost_gold': 150, 'learn_seconds': 30, 'desc': 'Bones and muscles reshape into a powerful animal. The Druid transforms into a wild beast.', 'execution_text': "The Druid drops to all fours. Their spine curves, their fingers curl, their jaw extends. It's not painful — it's liberating. When the transformation completes, a beast stands where the Druid was. It's faster. It's stronger. It's angrier. The enemy just lost their advantage."},
    {'id': 'solar_bloom', 'name': 'Solar Bloom', 'type': 'druid', 'rarity': 'uncommon', 'power_type': 'buff', 'damage': 0, 'cooldown': 5, 'skill_capacity_cost': 1, 'trigger': 'always', 'self_status': 'inspired', 'stat_mod': {'self': {'might': 3, 'insight': 3}}, 'mod_duration': 3, 'level_req': 3, 'mastery_req': 'druid', 'weapon_req': 'none', 'cost_gold': 150, 'learn_seconds': 30, 'desc': 'Golden vines burst into radiant flowers as the Druid harnesses the warmth of the sun.', 'execution_text': "The Druid raises their hands. The light that gathers isn't moonlight — it's solar. Warm, gold, alive. It sinks into the Druid's skin like warmth into cold stone. Muscles swell. Magic sharpens. The enemy sees the Druid glow and understands: the sun is on their side."},
    {'id': 'bear_form', 'name': 'Bear Form', 'type': 'druid', 'rarity': 'rare', 'power_type': 'buff', 'damage': 0, 'cooldown': 5, 'skill_capacity_cost': 2, 'trigger': 'always', 'self_status': 'warded', 'stat_mod': {'self': {'might': 5, 'armor_bonus': 4, 'durability': 3}}, 'mod_duration': 3, 'level_req': 8, 'mastery_req': 'druid', 'weapon_req': 'none', 'cost_gold': 400, 'learn_seconds': 60, 'desc': 'The Druid roars as enormous claws emerge. They transform into a massive bear.', 'execution_text': "The Druid doesn't just shift — they erupt. The transformation is violent, fast, and loud. Where a person stood, a bear now towers — massive, brown, furious. The ground shakes when it plants its feet. The enemy looks up. Way up. The bear shows its teeth. The enemy reconsiders."},
    {'id': 'eagle_form', 'name': 'Eagle Form', 'type': 'druid', 'rarity': 'rare', 'power_type': 'buff', 'damage': 0, 'cooldown': 5, 'skill_capacity_cost': 2, 'trigger': 'always', 'self_status': 'evasive', 'stat_mod': {'self': {'grace': 5, 'might': 2}}, 'mod_duration': 3, 'level_req': 8, 'mastery_req': 'druid', 'weapon_req': 'none', 'cost_gold': 400, 'learn_seconds': 60, 'desc': 'Feathers burst forth as wings spread wide. The Druid takes the form of a giant eagle.', 'execution_text': "The Druid leaps. The leap doesn't end. Feathers replace skin, wings replace arms, and the air catches them. The giant eagle climbs, circles, and dives. The enemy swings upward and hits nothing but sky. The talons arrive from above. The beak follows."},
    {'id': 'earth_guardian', 'name': 'Earth Guardian', 'type': 'druid', 'rarity': 'rare', 'power_type': 'strike', 'damage_type': 'physical', 'damage': 14, 'cooldown': 5, 'skill_capacity_cost': 2, 'trigger': 'always', 'status_apply': 'stunned', 'stat_mod': {'enemy': {'might': -3, 'armor_bonus': -3}}, 'mod_duration': 3, 'level_req': 8, 'mastery_req': 'druid', 'weapon_req': 'none', 'cost_gold': 400, 'learn_seconds': 60, 'desc': 'The ground trembles as a towering guardian of rock rises to protect the Druid and crush the enemy.', 'execution_text': 'The Druid stamps. The earth rises. Not a mound — a figure. A guardian of stone, ten feet tall, moss-covered, patient. It turns toward the enemy with the speed of geology. The fist comes down. The ground cracks. The enemy is in the crack.'},
    {'id': 'forest_wrath', 'name': 'Forest Wrath', 'type': 'druid', 'rarity': 'rare', 'power_type': 'strike', 'damage_type': 'magical', 'damage': 14, 'cooldown': 5, 'skill_capacity_cost': 2, 'trigger': 'always', 'status_apply': 'bleeding', 'stat_mod': {'enemy': {'might': -3, 'grace': -3, 'armor_bonus': -2}}, 'mod_duration': 3, 'level_req': 8, 'mastery_req': 'druid', 'weapon_req': 'none', 'cost_gold': 400, 'learn_seconds': 60, 'desc': 'Branches lash out while ancient trees awaken in anger. The forest itself attacks the enemy.', 'execution_text': 'The Druid speaks a word in a language older than people. The forest hears. The trees — old, patient, tired of being cut — awaken. Branches whip like flails. Roots heave like fists. The enemy is in the forest now, and the forest has been waiting for someone to be angry at.'},
    {'id': 'moonlight_blessing', 'name': 'Moonlight Blessing', 'type': 'druid', 'rarity': 'rare', 'power_type': 'buff', 'damage': 0, 'cooldown': 5, 'skill_capacity_cost': 2, 'trigger': 'always', 'self_status': 'inspired', 'heal_percent': 0.08, 'stat_mod': {'self': {'essence': 3, 'grace': 2, 'insight': 2}}, 'mod_duration': 4, 'level_req': 8, 'mastery_req': 'druid', 'weapon_req': 'none', 'cost_gold': 400, 'learn_seconds': 60, 'desc': "Silver light gently washes over the Druid, empowering them beneath the moon's glow.", 'execution_text': "The moon isn't visible — it's day, or the canopy blocks it. But the light comes anyway. Silver, soft, patient. It settles on the Druid like dew. Wounds close. Magic sharpens. The body lightens. The moon has always favored those who speak for the wild. The Druid is its voice."},
    {'id': 'seed_of_life', 'name': 'Seed of Life', 'type': 'druid', 'rarity': 'rare', 'power_type': 'heal', 'damage': 0, 'cooldown': 5, 'skill_capacity_cost': 2, 'trigger': 'low_hp', 'self_status': 'warded', 'heal_percent': 0.15, 'stat_mod': {'self': {'essence': 3, 'durability': 2}}, 'mod_duration': 3, 'level_req': 8, 'mastery_req': 'druid', 'weapon_req': 'none', 'cost_gold': 400, 'learn_seconds': 60, 'desc': 'A glowing seed takes root and pulses with energy, restoring life to the wounded.', 'execution_text': 'The Druid presses a seed into their own chest. It sinks in. For a moment, nothing. Then the glow — green, warm, spreading from the heart outward. Roots grow inward, not outward. They find the wounds, the breaks, the exhaustion. They replace it with life. The Druid rises. The seed has bloomed. Triggers when HP is low.'},
    {'id': 'living_canopy', 'name': 'Living Canopy', 'type': 'druid', 'rarity': 'rare', 'power_type': 'defend', 'damage': 0, 'cooldown': 5, 'skill_capacity_cost': 2, 'trigger': 'always', 'self_status': 'warded', 'stat_mod': {'self': {'armor_bonus': 4, 'essence': 3}}, 'mod_duration': 3, 'level_req': 8, 'mastery_req': 'druid', 'weapon_req': 'none', 'cost_gold': 400, 'learn_seconds': 60, 'desc': 'Towering trees grow instantly, shielding the Druid from harm beneath a living canopy.', 'execution_text': "The Druid raises both hands. The trees obey. They don't grow — they erupt. In seconds, a canopy of branches and leaves forms overhead, thick enough to block the sky. Arrows stick in the wood. Spells dissipate against the leaves. The Druid stands beneath it, safe, patient, rooted."},
    {'id': 'natures_rebirth', 'name': "Nature's Rebirth", 'type': 'druid', 'rarity': 'epic', 'power_type': 'heal', 'damage': 0, 'cooldown': 7, 'skill_capacity_cost': 2, 'trigger': 'low_hp', 'self_status': 'inspired', 'heal_percent': 0.3, 'stat_mod': {'self': {'essence': 4, 'durability': 3, 'grace': 2}}, 'mod_duration': 4, 'level_req': 15, 'mastery_req': 'druid', 'weapon_req': 'none', 'cost_gold': 1000, 'learn_seconds': 120, 'desc': 'Tiny sprouts surround the fallen as life slowly returns. The Druid revives through the power of nature.', 'execution_text': "The Druid is on the ground. The blood feeds the earth. And the earth gives it back. Sprouts erupt from the soil around the Druid's body — not random, but deliberate. They weave together, form a cocoon of green, and pulse. The Druid's eyes open. The wounds are gone. The forest has decided the Druid isn't done yet. Triggers when HP is low."},
    {'id': 'verdant_storm', 'name': 'Verdant Storm', 'type': 'druid', 'rarity': 'epic', 'power_type': 'strike', 'damage_type': 'magical', 'damage': 16, 'cooldown': 6, 'skill_capacity_cost': 2, 'trigger': 'always', 'status_apply': 'bleeding', 'hits': 2, 'stat_mod': {'enemy': {'grace': -3, 'armor_bonus': -3, 'might': -2}}, 'mod_duration': 3, 'level_req': 15, 'mastery_req': 'druid', 'weapon_req': 'none', 'cost_gold': 1000, 'learn_seconds': 120, 'desc': 'A raging green cyclone engulfs enemies in a storm of leaves, branches, and thorns.', 'execution_text': 'The Druid spins. The wind follows. Leaves become blades, branches become flails, and the cyclone builds — green, roaring, alive. It sweeps across the enemy like a lawnmower made of anger. When it passes, the enemy is bleeding from a hundred cuts and the ground is covered in green. The forest is tidy like that.'},
    {'id': 'animal_bond', 'name': 'Animal Bond', 'type': 'druid', 'rarity': 'epic', 'power_type': 'buff', 'damage': 0, 'cooldown': 6, 'skill_capacity_cost': 2, 'trigger': 'always', 'self_status': 'inspired', 'stat_mod': {'self': {'might': 4, 'grace': 3, 'essence': 2}}, 'mod_duration': 4, 'level_req': 15, 'mastery_req': 'druid', 'weapon_req': 'none', 'cost_gold': 1000, 'learn_seconds': 120, 'desc': 'Every companion responds with renewed vigor. The Druid strengthens all summoned beasts and themselves.', 'execution_text': "The Druid speaks — not a word, but a feeling. Every beast on the battlefield feels it: the wolf, the eagle, the spirit, the bear. A pulse of kinship, of pack, of belonging. They straighten. They sharpen. The enemy sees the animals change and understands: they're not fighting a Druid. They're fighting a family."},
    {'id': 'rivers_blessing', 'name': "River's Blessing", 'type': 'druid', 'rarity': 'epic', 'power_type': 'heal', 'damage': 0, 'cooldown': 6, 'skill_capacity_cost': 2, 'trigger': 'always', 'self_status': 'warded', 'heal_percent': 0.15, 'stat_mod': {'self': {'essence': 3, 'grace': 3, 'durability': 2}}, 'mod_duration': 3, 'level_req': 15, 'mastery_req': 'druid', 'weapon_req': 'none', 'cost_gold': 1000, 'learn_seconds': 120, 'desc': 'Crystal-clear water flows around the Druid, restoring vitality with sacred water.', 'execution_text': "The Druid cups their hands. Water appears — not from a flask, not from the sky, but from the earth itself. It's clear, cold, and alive. It flows over the Druid's hands, up their arms, across their chest. Wounds wash clean. Fatigue drains. The water sinks back into the ground, and the Druid stands refreshed, as if the battle just started."},
    {'id': 'ancient_grove', 'name': 'Ancient Grove', 'type': 'druid', 'rarity': 'epic', 'power_type': 'buff', 'damage': 0, 'cooldown': 6, 'skill_capacity_cost': 2, 'trigger': 'always', 'self_status': 'warded', 'heal_percent': 0.1, 'stat_mod': {'self': {'armor_bonus': 4, 'essence': 3, 'durability': 3}}, 'mod_duration': 4, 'level_req': 15, 'mastery_req': 'druid', 'weapon_req': 'none', 'cost_gold': 1000, 'learn_seconds': 120, 'desc': 'A tranquil grove instantly grows around the Druid, creating a sacred forest zone that heals and protects.', 'execution_text': 'The Druid kneels and presses both palms to the earth. The earth answers big. Trees grow — not saplings, but ancients, tall and wide, their canopies interlocking. The ground softens to moss. The air changes. This is sacred ground now. The enemy steps onto it and feels wrong. The Druid stands in the center, and the grove stands with them.'},
    {'id': 'verdant_ascension', 'name': 'Verdant Ascension', 'type': 'druid', 'rarity': 'epic', 'power_type': 'buff', 'damage': 0, 'cooldown': 6, 'skill_capacity_cost': 2, 'trigger': 'always', 'self_status': 'inspired', 'stat_mod': {'self': {'might': 4, 'grace': 4, 'insight': 4, 'essence': 3, 'durability': 3}}, 'mod_duration': 4, 'level_req': 15, 'mastery_req': 'druid', 'weapon_req': 'none', 'cost_gold': 1000, 'learn_seconds': 120, 'desc': 'The Druid ascends into a pure nature spirit, body glowing with verdant energy. All stats surge as the wild flows through them.', 'execution_text': "The Druid stops. They close their eyes. And then — they rise. Not jump, not float. Rise. Green light pours from their skin, their eyes, their mouth. The forest is inside them now, not around them. Every leaf that ever fell, every root that ever grew, every beast that ever ran — it's all there, behind their eyes. When they open them, the enemy sees not a person, but the wild itself, wearing a person's shape. And the wild is done being patient."},
    {'id': 'worldroot_passage', 'name': 'Worldroot Passage', 'type': 'druid', 'rarity': 'epic', 'power_type': 'buff', 'damage': 0, 'cooldown': 5, 'skill_capacity_cost': 2, 'trigger': 'always', 'self_status': 'evasive', 'stat_mod': {'self': {'grace': 4, 'essence': 2}}, 'mod_duration': 3, 'level_req': 15, 'mastery_req': 'druid', 'weapon_req': 'none', 'cost_gold': 1000, 'learn_seconds': 120, 'desc': 'The Druid disappears into one tree and emerges from another, traveling through ancient roots beneath the battlefield.', 'execution_text': "The Druid steps backward into a tree. Not against it — into it. The bark opens like a door. A moment later, a tree on the other side of the enemy opens the same way, and the Druid steps out. The enemy turns. The Druid is already behind them. The roots beneath the battlefield are older than the war. They don't mind giving a ride."},
    {'id': 'avatar_of_the_forest', 'name': 'Avatar of the Forest', 'type': 'druid', 'rarity': 'epic', 'power_type': 'buff', 'damage': 0, 'cooldown': 6, 'skill_capacity_cost': 2, 'trigger': 'low_hp', 'self_status': 'warded', 'heal_percent': 0.15, 'stat_mod': {'self': {'might': 5, 'armor_bonus': 5, 'essence': 4, 'durability': 3}}, 'mod_duration': 4, 'level_req': 15, 'mastery_req': 'druid', 'weapon_req': 'none', 'cost_gold': 1000, 'learn_seconds': 120, 'desc': 'The Druid merges with a colossal forest guardian, becoming the spirit of the ancient woods.', 'execution_text': "The Druid is failing. The forest disagrees. A guardian — ancient, vast, older than memory — rises from the earth behind the Druid. It doesn't fight for them. It merges with them. The Druid grows — taller, wider, bark-skinned, root-footed. Their voice becomes the forest's voice. Their fists become the forest's fists. The enemy looks up and sees the woods themselves, and the woods are angry. Triggers when HP is low."},
    {'id': 'heart_of_gaia', 'name': 'Heart of Gaia', 'type': 'druid', 'rarity': 'legendary', 'power_type': 'strike', 'damage_type': 'true', 'damage': 28, 'cooldown': 8, 'skill_capacity_cost': 3, 'trigger': 'always', 'status_apply': 'stunned', 'self_status': 'warded', 'stat_mod': {'enemy': {'might': -5, 'grace': -5, 'armor_bonus': -6, 'essence': -4}}, 'mod_duration': 4, 'level_req': 20, 'mastery_req': 'druid', 'weapon_req': 'none', 'cost_gold': 5000, 'learn_seconds': 300, 'desc': "The earth itself answers the Druid's plea. True damage ignores all defense. Devastates enemy stats. Grants Warded.", 'execution_text': "The Druid presses both hands into the earth — not gently, but desperately. They speak a name. Not a word. A name. The world's name. And the world hears. The ground heaves. The roots — not surface roots, but the deep ones, the ones that hold continents together — rise. The enemy is caught in something tectonic, something that was here before people and will be here after. The damage is absolute. The earth doesn't negotiate."},
    {'id': 'legend_of_nature', 'name': 'Legend of Nature', 'type': 'druid', 'rarity': 'legendary', 'power_type': 'strike', 'damage_type': 'true', 'damage': 28, 'cooldown': 10, 'skill_capacity_cost': 3, 'trigger': 'low_hp', 'status_apply': 'stunned', 'self_status': 'inspired', 'heal_percent': 0.2, 'stat_mod': {'enemy': {'might': -6, 'grace': -6, 'armor_bonus': -8, 'essence': -5, 'cognition': -4, 'durability': -4}}, 'mod_duration': 5, 'level_req': 20, 'mastery_req': 'druid', 'weapon_req': 'none', 'cost_gold': 5000, 'learn_seconds': 300, 'desc': 'Ancient spirits gather as every plant and beast bows to the legendary protector. The Druid becomes the eternal guardian of the wild. True damage ignores all defense. Devastates all enemy stats. Heals the Druid. Grants Inspired. Only usable when below 25% HP.', 'execution_text': 'The Druid is on the ground. The forest is quiet. And then — not silent, but listening. Every spirit that ever walked the wood gathers. Every beast that ever lived bows its head. Every tree leans in. The Druid rises, and they are not alone. They are the forest. They are the beast. They are the root and the branch and the claw and the bloom. The enemy sees the wilderness itself stand up, and the wilderness has decided the enemy is finished. The strike that comes is not a spell. It is the world, remembering what it was before the enemy existed. Triggers when HP is low.'},
]

SKILLS.extend(DRUID_SKILLS)

SKILLS_BY_ID: dict[str, dict] = {s["id"]: s for s in SKILLS}


# ============================================================
# CRAFTING RECIPES
# ============================================================
# outcome tier = based on crafting dice roll
RECIPES: list[dict] = [
    # Introductory recipes — no profession, instant (duration 0) to let new players learn the UI
    {"id": "craft_iron_dagger", "name": "Iron Dagger",
     "materials": [("iron_ore", 2), ("oak_log", 1)],
     "min_level": 1, "rarity": "common", "duration_seconds": 0,
     "profession_id": None, "profession_min_rank": None,
     "continent_id": "valeria", "town_id": "oathspire",
     "output_by_tier": {"crude": "iron_dagger", "fine": "iron_dagger", "master": "iron_longsword"}},
    {"id": "craft_oak_shortbow", "name": "Oak Shortbow",
     "materials": [("oak_log", 3), ("wolf_fang", 1)],
     "min_level": 1, "rarity": "common", "duration_seconds": 0,
     "profession_id": None, "profession_min_rank": None,
     "continent_id": "valeria", "town_id": "riverguard",
     "output_by_tier": {"crude": "oak_shortbow", "fine": "oak_shortbow", "master": "oak_shortbow"}},
    {"id": "craft_wolfpelt_cloak", "name": "Wolfpelt Cloak",
     "materials": [("wolf_pelt", 2)],
     "min_level": 2, "rarity": "common", "duration_seconds": 0,
     "profession_id": None, "profession_min_rank": None,
     "continent_id": "valeria", "town_id": "riverguard",
     "output_by_tier": {"crude": "wolfpelt_cloak", "fine": "wolfpelt_cloak", "master": "wolfpelt_cloak"}},
    {"id": "craft_boarhide_vest", "name": "Boarhide Vest",
     "materials": [("boar_hide", 2), ("boar_tusk", 1)],
     "min_level": 2, "rarity": "common", "duration_seconds": 0,
     "profession_id": None, "profession_min_rank": None,
     "continent_id": "valeria", "town_id": "oathspire",
     "output_by_tier": {"crude": "boarhide_vest", "fine": "boarhide_vest", "master": "scaled_hauberk"}},

    # Alchemy — short timers to introduce the timed-crafting loop
    {"id": "craft_minor_healing_potion", "name": "Minor Healing Potion",
     "materials": [("wild_herb", 2), ("river_stone", 1)],
     "min_level": 1, "rarity": "common", "duration_seconds": 10,
     "profession_id": "alchemy", "profession_min_rank": "novice",
     "continent_id": "valeria", "town_id": "riverguard",
     "output_by_tier": {"crude": "minor_healing_potion", "fine": "minor_healing_potion", "master": "greater_healing_potion"}},
    {"id": "craft_antidote", "name": "Antidote",
     "materials": [("wild_herb", 1), ("serpent_scale", 1)],
     "min_level": 2, "rarity": "common", "duration_seconds": 15,
     "profession_id": "alchemy", "profession_min_rank": "novice",
     "continent_id": "valeria", "town_id": "riverguard",
     "output_by_tier": {"crude": "antidote", "fine": "antidote", "master": "antidote"}},
    {"id": "craft_acid_flask", "name": "Acid Flask",
     "materials": [("serpent_venom", 1), ("river_stone", 2)],
     "min_level": 3, "rarity": "uncommon", "duration_seconds": 90,
     "profession_id": "alchemy", "profession_min_rank": "apprentice",
     "continent_id": "valeria", "town_id": "riverguard",
     "output_by_tier": {"crude": "acid_flask_item", "fine": "acid_flask_item", "master": "acid_flask_item"}},
    {"id": "craft_greater_healing_potion", "name": "Greater Healing Potion",
     "materials": [("wild_herb", 4), ("wisp_essence", 1)],
     "min_level": 3, "rarity": "uncommon", "duration_seconds": 120,
     "profession_id": "alchemy", "profession_min_rank": "apprentice",
     "continent_id": "valeria", "town_id": "riverguard",
     "output_by_tier": {"crude": "greater_healing_potion", "fine": "greater_healing_potion", "master": "greater_healing_potion"}},

    # Blacksmithing / metalwork
    {"id": "craft_iron_longsword", "name": "Iron Longsword",
     "materials": [("iron_ore", 4), ("oak_log", 1)],
     "min_level": 3, "rarity": "uncommon", "duration_seconds": 120,
     "profession_id": "blacksmithing", "profession_min_rank": "novice",
     "continent_id": "valeria", "town_id": "oathspire",
     "output_by_tier": {"crude": "iron_dagger", "fine": "iron_longsword", "master": "wolfbone_axe"}},
    {"id": "craft_wolfbone_axe", "name": "Wolfbone Axe",
     "materials": [("iron_ore", 2), ("wolf_fang", 3), ("oak_log", 1)],
     "min_level": 4, "rarity": "uncommon", "duration_seconds": 180,
     "profession_id": "blacksmithing", "profession_min_rank": "apprentice",
     "continent_id": "valeria", "town_id": "oathspire",
     "output_by_tier": {"crude": "iron_longsword", "fine": "wolfbone_axe", "master": "wolfbone_axe"}},

    # Engineering / carving
    {"id": "craft_riverstone_staff", "name": "Riverstone Staff",
     "materials": [("river_stone", 3), ("oak_log", 2), ("wisp_essence", 1)],
     "min_level": 3, "rarity": "uncommon", "duration_seconds": 120,
     "profession_id": "engineering", "profession_min_rank": "novice",
     "continent_id": "valeria", "town_id": "riverguard",
     "output_by_tier": {"crude": "riverstone_staff", "fine": "riverstone_staff", "master": "riverstone_staff"}},
]

RECIPES_BY_ID: dict[str, dict] = {r["id"]: r for r in RECIPES}


# ============================================================
# NPC SKILL TEACHERS
# ============================================================
TEACHERS: list[dict] = [
    {"id": "master_arden", "name": "Master Arden", "biome": "grasslands",
     "continent_id": "aetheria", "town_id": "ironhold", "mastery_focus": "knight",
     "desc": "A retired knight whose axe knows both blood and mercy.",
     "teaches": ["shield_bash", "sworn_strike", "smite"]},
    {"id": "elder_lyria", "name": "Elder Lyria", "biome": "oakwood",
     "continent_id": "aetheria", "town_id": "willowmere", "mastery_focus": "druid",
     "desc": "A grove-keeper who reads the wind and the roots.",
     "teaches": ['mend', 'thornlash', 'beast_call', 'entangling_roots', 'thorn_barrage', 'ancient_bark', 'healing_bloom', 'natures_whisper', 'stone_skin', 'spirit_wolf', 'wild_growth', 'vine_prison', 'fungal_bloom', 'natures_grasp', 'beast_form', 'solar_bloom', 'bear_form', 'eagle_form', 'earth_guardian', 'forest_wrath', 'moonlight_blessing', 'seed_of_life', 'living_canopy']},
    {"id": "trapper_kell", "name": "Trapper Kell", "biome": "riverlands",
     "continent_id": "aetheria", "town_id": "willowmere", "mastery_focus": "hunter",
     "desc": "A hunter with more scars than he has stories.",
     "teaches": ["aimed_shot", "trap", "backstab"]},
    {"id": "warmaster_koruk", "name": "Warmaster Koruk", "biome": "emberreach",
     "continent_id": "vulkaros", "town_id": "emberhold", "mastery_focus": "lancer",
     "desc": "An orc veteran whose war-cries dull the edge of fear.",
     "teaches": ["thrust", "impale", "mocking_verse"]},
    {"id": "rigg_the_sapper", "name": "Rigg the Sapper", "biome": "zaheer_march",
     "continent_id": "vulkaros", "town_id": "ashvault", "mastery_focus": "hunter",
     "desc": "A scarred powder-hand who prefers traps to talk.",
     "teaches": ["aimed_shot", "trap", "acid_flask"]},
    {"id": "thrain_ironfoot", "name": "Thrain Ironfoot", "biome": "undermountain_hall",
     "continent_id": "frosthelm", "town_id": "khaz_moroth", "mastery_focus": "knight",
     "desc": "A dwarven shield-bearer who has held a line for three centuries.",
     "teaches": ["shield_bash", "sworn_strike", "ward"]},
    {"id": "ranger_vex", "name": "Ranger Vex", "biome": "stone_wardens",
     "continent_id": "frosthelm", "town_id": "frostwatch", "mastery_focus": "rogue",
     "desc": "A warden of the tundra who tracks wyrms across the ice.",
     "teaches": ['aimed_shot', 'trap', 'poison_blade', 'dirty_trick', 'hidden_blade', 'opportunist_strike', 'acrobatic_roll', 'quick_step', 'pocket_sand', 'flash_powder', 'tripwire', 'knife_fan', 'hook_chain', 'feign_death', 'wall_run', 'sleight_of_hand', 'mirror_image', 'smoke_bomb_rogue', 'false_surrender', 'misdirection', 'counter_stab', 'escape_artist', 'tricksters_flurry', 'lucky_escape', 'ambush_master', 'grand_heist', 'coin_toss', 'shadow_step_rogue', 'master_picklock', 'king_of_thieves', 'tricksters_gambit', 'perfect_crime', 'legend_of_trickery']},
    {"id": "sylvara_starweaver", "name": "Sylvara Starweaver", "biome": "haya_ascendant",
     "continent_id": "zephyria", "town_id": "sun_moon_haven", "mastery_focus": "mage",
     "desc": "An elven arcanist who weaves starlight into searing threads.",
     "teaches": ["arcane_bolt", "ward", "purge"]},
    {"id": "mirage_savant", "name": "Mirage Savant", "biome": "mirage_dunes",
     "continent_id": "sablewaste", "town_id": "sun_bazaar", "mastery_focus": "alchemist",
     "desc": "A masked merchant who sells poisons and remedies by the same hand.",
     "teaches": ["acid_bomb", "flash_powder_alch", "quick_jab", "heavy_crush", "healing_draught", "iron_skin_transmutation"]},
    {"id": "thazka_emberhand", "name": "Thazka Emberhand", "biome": "emberreach",
     "continent_id": "vulkaros", "town_id": "emberhold", "mastery_focus": "alchemist",
     "desc": "A dwarven alchemist whose katar has taken more forms than most warriors see in a lifetime.",
     "teaches": ["frost_mixture", "lightning_bottle", "poison_capsule", "flurry", "rushing_strike", "swift_transmutation", "stone_wall", "corrosive_mist", "living_slime", "transmutation_touch", "explosive_chain", "spinning_strike", "piercing_strike", "counter_strike"]},
    {"id": "thazka_emberhand_master", "name": "Thazka Emberhand", "biome": "emberreach",
     "continent_id": "vulkaros", "town_id": "emberhold", "mastery_focus": "alchemist",
     "desc": "Thazka's private studio, deep beneath the forge. Only for those who have proven their transmutation arts.",
     "teaches": ["forbidden_formula", "guard_break", "rising_strike", "executioner_strike", "mutagen_injection", "phoenix_mixture", "smoke_transmutation", "spike_field", "philosophers_transmutation", "legend_of_alchemy"]},
    {"id": "leafwhisper", "name": "Leafwhisper", "biome": "deep_verdant",
     "continent_id": "verdania", "town_id": "emerald_bough", "mastery_focus": "druid",
     "desc": "A sylvan druid whose veins run with sap instead of blood.",
     "teaches": ['mend', 'thornlash', 'beast_call', 'natures_rebirth', 'verdant_storm', 'animal_bond', 'rivers_blessing', 'ancient_grove', 'verdant_ascension', 'worldroot_passage', 'avatar_of_the_forest', 'heart_of_gaia', 'legend_of_nature']},
    {"id": "tidepriest_mira", "name": "Tidepriest Mira", "biome": "coral_gates",
     "continent_id": "verdania", "town_id": "atlantyrion_gate", "mastery_focus": "priest",
     "desc": "A tidebound healer who walks between surf and soul.",
     "teaches": ["mend", "purge", "lay_on_hands"]},
    {"id": "serathiel_moonglow", "name": "Serathiel Moonglow", "biome": "haya_ascendant",
     "continent_id": "zephyria", "town_id": "sun_moon_haven", "mastery_focus": "paladin",
     "desc": "A celestial knight whose faith shines like the moon over Solunara.",
     "teaches": ["shield_of_faith", "blessed_strike", "merciful_touch", "hammer_of_light", "divine_aegis", "lightbearers_oath"]},
    {"id": "serathiel_moonglow_adv", "name": "Serathiel Moonglow", "biome": "haya_ascendant",
     "continent_id": "zephyria", "town_id": "sun_moon_haven", "mastery_focus": "paladin",
     "desc": "Serathiel's private chapel. Only for those who have proven their faith.",
     "teaches": ["sacred_charge", "judgment_hammer", "holy_barrier", "consecrate_blade", "sunburst", "divine_radiance", "guardians_blessing"]},
    {"id": "serathiel_moonglow_exp", "name": "Serathiel Moonglow", "biome": "haya_ascendant",
     "continent_id": "zephyria", "town_id": "sun_moon_haven", "mastery_focus": "paladin",
     "desc": "Serathiel's inner sanctum. The faith deepens here.",
     "teaches": ["divine_intercession", "lay_on_hands_paladin", "exorcism", "celestial_spear", "divine_resolve", "faiths_bulwark", "last_stand"]},
    {"id": "serathiel_moonglow_master", "name": "Serathiel Moonglow", "biome": "haya_ascendant",
     "continent_id": "zephyria", "town_id": "sun_moon_haven", "mastery_focus": "paladin",
     "desc": "The Chapel of Ascension. Only the most devout may enter.",
     "teaches": ["holy_nova", "sanctuary", "justice_descends", "guardians_crown", "resurrection_prayer", "consecrated_ground", "divine_wrath", "guardian_angel"]},
    {"id": "serathiel_moonglow_legend", "name": "Serathiel Moonglow", "biome": "haya_ascendant",
     "continent_id": "zephyria", "town_id": "sun_moon_haven", "mastery_focus": "paladin",
     "desc": "The Final Verdict awaits. The blade of light descends only for the worthy.",
     "teaches": ["last_judgment", "ascension_of_the_light"]},
    # Priest teachers — Serathiel Moonglow (Solunara), Elaris, Starfall Watch
    {"id": "serathiel_moonglow_priest_basic", "name": "Serathiel Moonglow", "biome": "haya_ascendant",
     "continent_id": "zephyria", "town_id": "sun_moon_haven", "mastery_focus": "priest",
     "desc": "A celestial priest whose voice carries the weight of the heavens over Solunara.",
     "teaches": ["swift_prayer", "light_barrier", "bless", "holy_water", "blinding_light", "soul_ward"]},
    {"id": "serathiel_moonglow_priest_adv", "name": "Serathiel Moonglow", "biome": "haya_ascendant",
     "continent_id": "zephyria", "town_id": "sun_moon_haven", "mastery_focus": "priest",
     "desc": "Serathiel's chapel. The prayers deepen here.",
     "teaches": ["blessing_of_renewal", "chain_of_light", "cleansing_flame", "angels_grace", "judgment_strike", "divine_rebuke", "light_of_hope"]},
    {"id": "serathiel_moonglow_priest_exp", "name": "Serathiel Moonglow", "biome": "haya_ascendant",
     "continent_id": "zephyria", "town_id": "sun_moon_haven", "mastery_focus": "priest",
     "desc": "Serathiel's inner sanctum. The Sanctity awakens here.",
     "teaches": ["divine_light_priest", "mass_purify", "heavens_judgment", "radiant_prison", "beacon_of_faith", "sunflare", "radiant_bulwark"]},
    {"id": "serathiel_moonglow_priest_master", "name": "Serathiel Moonglow", "biome": "haya_ascendant",
     "continent_id": "zephyria", "town_id": "sun_moon_haven", "mastery_focus": "priest",
     "desc": "The Chapel of Sanctity. Only the most faithful may enter.",
     "teaches": ["sanctuary_priest", "holy_lance", "promise_of_heaven", "hymn_of_salvation", "final_judgment", "holy_revelation", "prayer_circle", "divine_covenant"]},
    {"id": "serathiel_moonglow_priest_legend", "name": "Serathiel Moonglow", "biome": "haya_ascendant",
     "continent_id": "zephyria", "town_id": "sun_moon_haven", "mastery_focus": "priest",
     "desc": "The Celestial Choir awaits. The heavens descend only for the worthy.",
     "teaches": ["choir_of_heaven", "legend_of_the_faithful"]},
    # Knight teachers
    {"id": "master_arden_basic", "name": "Master Arden", "biome": "grasslands",
     "continent_id": "aetheria", "town_id": "oathspire", "mastery_focus": "knight",
     "desc": "A retired knight whose axe knows both blood and mercy.",
     "teaches": ["shield_bash", "iron_stance", "war_cry", "vanguard_step", "pommel_strike", "steady_grip"]},
    {"id": "master_arden_adv", "name": "Master Arden", "biome": "grasslands",
     "continent_id": "aetheria", "town_id": "oathspire", "mastery_focus": "knight",
     "desc": "Master Arden's training yard. Only for those who have proven their stance.",
     "teaches": ["kings_challenge", "lions_charge", "heavy_strike", "bulwark", "banner_of_valor", "fortress_breaker", "plate_armor_mastery"]},
    {"id": "master_arden_exp", "name": "Master Arden", "biome": "grasslands",
     "continent_id": "aetheria", "town_id": "oathspire", "mastery_focus": "knight",
     "desc": "Master Arden's private hall. The Oath deepens here.",
     "teaches": ["shield_wall", "guardians_sacrifice", "commanding_presence", "crushing_blow", "unbreakable_will", "titans_strength", "ground_slam"]},
    {"id": "master_arden_master", "name": "Master Arden", "biome": "grasslands",
     "continent_id": "aetheria", "town_id": "oathspire", "mastery_focus": "knight",
     "desc": "The Hall of Oaths. Only the sworn may enter.",
     "teaches": ["iron_formation", "royal_execution", "guardians_oath", "warlords_fury", "crown_of_iron", "kings_command", "last_bastion", "oath_strike"]},
    {"id": "master_arden_legend", "name": "Master Arden", "biome": "grasslands",
     "continent_id": "aetheria", "town_id": "oathspire", "mastery_focus": "knight",
     "desc": "The Broken Oath awaits. The final trial of the Knight.",
     "teaches": ["final_duel", "legend_of_erchis"]},
    # Lancer teachers
    {"id": "thazka_emberhand_basic", "name": "Thazka Emberhand", "biome": "mountain",
     "continent_id": "aetheria", "town_id": "warforge", "mastery_focus": "lancer",
     "desc": "A scarred lancer who teaches the way of the elemental spear.",
     "teaches": ["flame_imbue", "frost_imbue", "gale_thrust", "lancer_guard_break", "cyclone_wall", "warriors_focus"]},
    {"id": "thazka_emberhand_adv", "name": "Thazka Emberhand", "biome": "mountain",
     "continent_id": "aetheria", "town_id": "warforge", "mastery_focus": "lancer",
     "desc": "Thazka's training ground. The elements deepen here.",
     "teaches": ["storm_imbue", "stone_imbue", "sky_piercer", "falcon_rush", "dragon_fang", "elemental_weakness", "battle_readiness"]},
    {"id": "thazka_emberhand_exp", "name": "Thazka Emberhand", "biome": "mountain",
     "continent_id": "aetheria", "town_id": "warforge", "mastery_focus": "lancer",
     "desc": "Thazka's private forge. Where elements meet steel.",
     "teaches": ["gale_imbue", "thunder_imbue", "dragon_dive", "frostbite", "shock_lock", "iron_breeze", "elemental_surge"]},
    {"id": "thazka_emberhand_master", "name": "Thazka Emberhand", "biome": "mountain",
     "continent_id": "aetheria", "town_id": "warforge", "mastery_focus": "lancer",
     "desc": "The Elemental Chamber. Only those who have mastered the basics may enter.",
     "teaches": ["inferno_imbue", "glacier_imbue", "tempest_imbue", "volcano_imbue", "thunder_pursuit", "world_splitter", "crimson_spear", "elemental_collapse"]},
    {"id": "thazka_emberhand_legend", "name": "Thazka Emberhand", "biome": "mountain",
     "continent_id": "aetheria", "town_id": "warforge", "mastery_focus": "lancer",
     "desc": "The Spear That Pierced Heaven. The final trial of the Lancer.",
     "teaches": ["celestial_javelin", "avatar_of_the_storm"]},
    # Assassin teachers
    {"id": "hildra_coldforge_basic", "name": "Hildra Cold-Forge", "biome": "underground",
     "continent_id": "aetheria", "town_id": "deepstone", "mastery_focus": "assassin",
     "desc": "A silent killer who teaches the way of shadows.",
     "teaches": ["shadow_strike", "heart_piercer", "smoke_veil", "death_mark", "shadow_focus"]},
    {"id": "hildra_coldforge_adv", "name": "Hildra Cold-Forge", "biome": "underground",
     "continent_id": "aetheria", "town_id": "deepstone", "mastery_focus": "assassin",
     "desc": "Hildra's shadow chamber. The dark deepens here.",
     "teaches": ["silent_execution", "phantom_strike", "crimson_dash", "night_veil", "shadow_terror", "shadowstep", "dark_pursuit"]},
    {"id": "hildra_coldforge_exp", "name": "Hildra Cold-Forge", "biome": "underground",
     "continent_id": "aetheria", "town_id": "deepstone", "mastery_focus": "assassin",
     "desc": "The Black Room. No light enters. No shadow leaves.",
     "teaches": ["vanishing_kill", "shadow_flurry", "soul_sever", "shadow_clone", "shadow_prison", "black_feathers", "eclipse_blade"]},
    {"id": "hildra_coldforge_master", "name": "Hildra Cold-Forge", "biome": "underground",
     "continent_id": "aetheria", "town_id": "deepstone", "mastery_focus": "assassin",
     "desc": "The Shadow Convergence. Only those who have mastered the dark may enter.",
     "teaches": ["shadow_convergence", "night_requiem", "deaths_whisper", "umbral_cloak", "final_contract", "king_slayer", "shadow_devour", "eclipse_burst"]},
    {"id": "hildra_coldforge_legend", "name": "Hildra Cold-Forge", "biome": "underground",
     "continent_id": "aetheria", "town_id": "deepstone", "mastery_focus": "assassin",
     "desc": "The Price of Shadows. The final trial of the Assassin.",
     "teaches": ["reapers_arrival", "eclipse_of_shadows"]},
    # Hunter teachers
    {"id": "garren_longshot_basic", "name": "Garren Longshot", "biome": "forest",
     "continent_id": "aetheria", "town_id": "grunhold", "mastery_focus": "hunter",
     "desc": "A grizzled tracker who teaches the way of the bow.",
     "teaches": ["rapid_shot", "piercing_shot", "snare_trap", "camouflage", "eagle_eye", "crippling_shot"]},
    {"id": "garren_longshot_adv", "name": "Garren Longshot", "biome": "forest",
     "continent_id": "aetheria", "town_id": "grunhold", "mastery_focus": "hunter",
     "desc": "Garren's hunting lodge. The arrows fly thicker here.",
     "teaches": ["poison_arrow", "flash_bang", "twin_shot", "smoke_bomb", "hunters_mark", "falcon_strike", "spirit_walk"]},
    {"id": "garren_longshot_exp", "name": "Garren Longshot", "biome": "forest",
     "continent_id": "aetheria", "town_id": "grunhold", "mastery_focus": "hunter",
     "desc": "The Spirit Glade. Where the ancestors watch every shot.",
     "teaches": ["rain_of_arrows", "wolf_companion", "explosive_trap", "hawk_vision", "backflip", "monster_slayer", "bear_trap"]},
    {"id": "garren_longshot_master", "name": "Garren Longshot", "biome": "forest",
     "continent_id": "aetheria", "town_id": "grunhold", "mastery_focus": "hunter",
     "desc": "The Communion Ground. Only those who have heard the ancestors may enter.",
     "teaches": ["volley_master", "spirit_bind", "storm_arrow", "natures_blessing", "survival_instinct", "alpha_command", "ancient_tracker", "tracking_instinct"]},
    {"id": "garren_longshot_legend", "name": "Garren Longshot", "biome": "forest",
     "continent_id": "aetheria", "town_id": "grunhold", "mastery_focus": "hunter",
     "desc": "The Endless Pursuit. The final trial of the Hunter.",
     "teaches": ["world_hunt", "legend_of_the_wild"]},
    # Bard teachers
    {"id": "mira_songweaver_basic", "name": "Mira Songweaver", "biome": "silverroad",
     "continent_id": "concordia", "town_id": "silvergate", "mastery_focus": "bard",
     "desc": "A silver-voiced performer who teaches the way of song and dance.",
     "teaches": ["song_of_heroes", "song_of_hope", "resonant_strike", "harmony_shield", "sunrise_chorus"]},
    {"id": "mira_songweaver_adv", "name": "Mira Songweaver", "biome": "silverroad",
     "continent_id": "concordia", "town_id": "silvergate", "mastery_focus": "bard",
     "desc": "Mira's music hall. The melodies deepen here.",
     "teaches": ["song_of_wisdom", "festival_rhythm", "discord", "dance_of_blades", "sirens_call", "ballad_of_hope", "lullaby_of_fallen_kings"]},
    {"id": "mira_songweaver_exp", "name": "Mira Songweaver", "biome": "mosaic_coast",
     "continent_id": "concordia", "town_id": "elaris", "mastery_focus": "bard",
     "desc": "The Grand Conservatory of Elaris. Where the great compositions are born.",
     "teaches": ["song_of_freedom", "moon_serenade", "inspiring_solo", "echo_verse", "epic_tale", "muses_blessing", "curtain_call"]},
    {"id": "mira_songweaver_master", "name": "Mira Songweaver", "biome": "imperial_riverlands",
     "continent_id": "valeria", "town_id": "riverguard", "mastery_focus": "bard",
     "desc": "The Whispering Amphitheater of Riverguard. Only those who have mastered the stage may enter.",
     "teaches": ["song_of_fortune", "heros_anthem", "world_orchestra", "grand_performance", "memory_song", "legend_keeper", "whispered_melody", "travelers_tune"]},
    {"id": "mira_songweaver_legend", "name": "Mira Songweaver", "biome": "imperial_riverlands",
     "continent_id": "valeria", "town_id": "riverguard", "mastery_focus": "bard",
     "desc": "The Final Symphony. The ultimate performance awaits.",
     "teaches": ["requiem_of_the_heavens", "symphony_of_creation"]},
    # Mage teachers
    {"id": "vex_elenor_basic", "name": "Vex Elenor", "biome": "arcane_tower",
     "continent_id": "aetheria", "town_id": "elaris", "mastery_focus": "mage",
     "desc": "An arcane scholar who teaches the foundations of spellcraft.",
     "teaches": ["arcane_burst", "wind_blade", "stone_spear", "arcane_ward", "blink", "water_lash"]},
    {"id": "vex_elenor_adv", "name": "Vex Elenor", "biome": "arcane_tower",
     "continent_id": "aetheria", "town_id": "elaris", "mastery_focus": "mage",
     "desc": "The elements answer. Fire, ice, lightning — the Mage learns to wield them all.",
     "teaches": ["fireball", "frost_prison", "chain_lightning", "mana_shield", "spell_seal", "arcane_chains", "illusory_double"]},
    {"id": "starfall_watch_expert", "name": "Starfall Watch", "biome": "starfall_peak",
     "continent_id": "hylion", "town_id": "starfall", "mastery_focus": "mage",
     "desc": "The mind bends. The world reshapes. Expert spellcraft awaits.",
     "teaches": ["gravity_well", "telekinetic_crush", "mirror_spell", "mind_maze", "void_portal", "phantom_terrain", "dream_step"]},
    {"id": "atlantyrion_master", "name": "Atlantyrion", "biome": "sunken_archive",
     "continent_id": "hylion", "town_id": "atlantis", "mastery_focus": "mage",
     "desc": "The ancient archive beneath the waves. Power beyond comprehension.",
     "teaches": ["meteor_storm", "blizzard", "thunderfield", "time_slow", "elemental_convergence", "mana_explosion", "reality_fracture", "time_stop"]},
    {"id": "vex_elenor_legend", "name": "Vex Elenor", "biome": "arcane_tower",
     "continent_id": "aetheria", "town_id": "elaris", "mastery_focus": "mage",
     "desc": "The Arcane Ascension. The final trial of the Mage.",
     "teaches": ["cosmic_convergence", "legend_of_the_arcane"]},
]


# ============================================================
# Canon v2 migration for TEACHERS
# ============================================================
# The canon v2 rename remapped continent/biome/town ids and migrated every
# character record, but TEACHERS was never touched. The result: 48 of 53 skill
# teachers pointed at towns and continents that no longer exist, and because
# `/game/data/teachers` filters by `town_id`, visiting a real town surfaced almost
# no trainers. Skill learning was effectively unreachable for most masteries.
#
# Applying the same maps the character migration uses fixes 51 of 53; the two
# stragglers ("atlantis", "starfall") are mapped explicitly below.
_TEACHER_TOWN_FALLBACK: dict[str, str] = {
    "atlantis": "atlantyrion",
    "starfall": "starfall_watch",
}


def _migrate_teachers_to_canon() -> None:
    from world_data import CONTINENT_ID_MAP, TOWN_ID_MAP, BIOME_ID_MAP

    for teacher in TEACHERS:
        town = teacher.get("town_id")
        if town:
            town = TOWN_ID_MAP.get(town, town)
            town = _TEACHER_TOWN_FALLBACK.get(town, town)
            teacher["town_id"] = town
        cont = teacher.get("continent_id")
        if cont:
            teacher["continent_id"] = CONTINENT_ID_MAP.get(cont, cont)
        biome = teacher.get("biome")
        if biome:
            teacher["biome"] = BIOME_ID_MAP.get(biome, biome)


_migrate_teachers_to_canon()

TEACHERS_BY_ID: dict[str, dict] = {t["id"]: t for t in TEACHERS}


# ============================================================
# ACTIONS available per biome
# ============================================================
# action_ids: hunt | gather | explore | fish | loot_ruins
BIOME_ACTIONS: dict[str, list[dict]] = {
    "grasslands": [
        {"id": "hunt",    "name": "Hunt",    "targets": ["gray_wolf", "highway_bandit"]},
        {"id": "gather",  "name": "Gather",  "targets": ["wild_herb", "iron_ore", "copper_ore"]},
        {"id": "explore", "name": "Explore", "targets": []},
    ],
    "oakwood": [
        {"id": "hunt",    "name": "Hunt",    "targets": ["grove_wisp", "boar"]},
        {"id": "gather",  "name": "Gather",  "targets": ["oak_log", "wild_herb"]},
        {"id": "explore", "name": "Explore", "targets": []},
    ],
    "riverlands": [
        {"id": "fish",    "name": "Fish",    "targets": []},
        {"id": "hunt",    "name": "Hunt",    "targets": ["river_serpent"]},
        {"id": "gather",  "name": "Gather",  "targets": ["river_stone"]},
    ],
    "old_ruins": [
        {"id": "loot_ruins","name": "Loot Ruins","targets": []},
        {"id": "hunt",      "name": "Hunt",     "targets": ["ruin_ghast"]},
        {"id": "gather",    "name": "Gather",   "targets": ["iron_ore"]},
    ],
}


# ============================================================
# DAILY MISSION POOL
# ============================================================
DAILY_MISSION_POOL: list[dict] = [
    {"id": "hunt_wolves",   "desc": "Slay 3 Gray Wolves in Aetheria.",           "target": {"kind": "kill", "id": "gray_wolf", "count": 3},   "reward": {"gold": 60, "xp": 50}},
    {"id": "gather_herbs",  "desc": "Gather 5 Wild Herbs.",                       "target": {"kind": "gather", "id": "wild_herb", "count": 5},"reward": {"gold": 40, "xp": 30}},
    {"id": "loot_ruin",     "desc": "Complete one Loot Ruins run in Old Kingdom.","target": {"kind": "action", "id": "loot_ruins", "count": 1},"reward": {"gold": 80, "xp": 60}},
    {"id": "craft_two",     "desc": "Craft any 2 items.",                         "target": {"kind": "craft", "count": 2},                     "reward": {"gold": 70, "xp": 55}},
    {"id": "hunt_bandit",   "desc": "Slay 2 Highway Bandits.",                    "target": {"kind": "kill", "id": "highway_bandit", "count": 2},"reward": {"gold": 90, "xp": 70}},
    {"id": "explore_biomes","desc": "Explore 2 different biomes today.",          "target": {"kind": "explore_variety", "count": 2},           "reward": {"gold": 50, "xp": 40}},
    {"id": "hunt_serpent",  "desc": "Slay a River Serpent.",                      "target": {"kind": "kill", "id": "river_serpent","count": 1},"reward": {"gold": 120,"xp": 90}},
]


# ============================================================
# LOGIN REWARDS (7-day streak)
# ============================================================
LOGIN_REWARDS: list[dict] = [
    {"day": 1, "reward": {"gold": 25}},
    {"day": 2, "reward": {"gold": 40, "item": ("wild_herb", 2)}},
    {"day": 3, "reward": {"gold": 60}},
    {"day": 4, "reward": {"gold": 80, "item": ("minor_healing_potion", 1)}},
    {"day": 5, "reward": {"gold": 120}},
    {"day": 6, "reward": {"gold": 150, "item": ("bandage", 2)}},
    {"day": 7, "reward": {"gold": 300, "item": ("skillbook_ward", 1)}},
]


# ============================================================
# PORTRAITS — DiceBear pixel-art seeds (5 per race = 40 total)
# ============================================================
def build_portraits() -> list[dict]:
    portraits = []
    for race in RACES:
        for seed in race["portrait_seeds"]:
            portraits.append({
                "id": f"{race['id']}_{seed.lower()}",
                "race": race["id"],
                "seed": seed,
                "url": f"https://api.dicebear.com/7.x/pixel-art/svg?seed={seed}&backgroundColor=1c1a17,2a241f&clothing=variant01,variant02,variant03&clothingColor=8b0000,d4af37,4b0082,3a332a",
            })
    return portraits


PORTRAITS: list[dict] = build_portraits()


# ============================================================
# HELPERS
# ============================================================
def get_race(race_id: str) -> dict | None:
    return next((r for r in RACES if r["id"] == race_id), None)


def get_role(role_id: str) -> dict | None:
    return next((r for r in ROLES if r["id"] == role_id), None)


def get_mastery(m_id: str) -> dict | None:
    return next((m for m in MASTERIES if m["id"] == m_id), None)
def get_monster(m_id: str) -> dict | None:
    return next((m for m in MONSTERS if m["id"] == m_id), None)


def compute_starting_hp(stats: dict) -> int:
    """Maximum Health = 50 + Vitality × 10 (per new damage/stat spec)."""
    return 50 + int(stats.get("vitality", 3)) * 10


# ============================================================
# EQUIPPED-GEAR RESOLUTION (single source of truth)
# ============================================================
# `equipped[slot]` may hold either a legacy static item id (a key in ITEMS_BY_ID)
# or a procedural `instance_id` (an entry in character['item_instances']).
#
# Four separate functions used to inline `ITEMS_BY_ID.get(item_id)` and then read
# fields that instances do not carry (`power`, `accuracy`, `evasion`). Because
# character creation builds starter gear as instances, those lookups returned
# None for every character in the game and the terms were silently always zero.
#
# Every gear read now goes through iter_equipped_items() so the two formats can
# never diverge again. Adding a slot or a new item format is a one-line change
# here instead of four parallel edits that are easy to miss.
def resolve_equipped_item(character: dict, slot: str) -> dict | None:
    """Resolve whatever is in `slot` to an item dict, or None if empty/unknown."""
    item_ref = (character.get("equipped") or {}).get(slot)
    if not item_ref:
        return None
    item = ITEMS_BY_ID.get(item_ref)
    if item is not None and not item.get("base_id"):
        return item
    for inst in character.get("item_instances") or []:
        if isinstance(inst, dict) and inst.get("instance_id") == item_ref:
            return inst
    return item


def iter_equipped_items(character: dict, slots: list[str] | None = None):
    """Yield (slot, item) for each filled slot, skipping duplicates.

    Deduplication matters for two-handed weapons, which occupy both hand slots
    with the same reference and must only be counted once.
    """
    equipped = character.get("equipped") or {}
    seen: set[str] = set()
    for slot in (slots if slots is not None else EQUIP_SLOTS):
        ref = equipped.get(slot)
        if not ref or ref in seen:
            continue
        seen.add(ref)
        item = resolve_equipped_item(character, slot)
        if item is not None:
            yield slot, item


def _item_gear_score(item: dict) -> int:
    """A rough 'how good is this piece' number for the action rating.

    Everything is stats now — the legacy scalar `power` field has been removed
    from every item in the game, so there is only one thing to read.
    """
    stats = item.get("base_stats") or item.get("stats") or {}
    # Defensive stats are already reflected via the character's stat block; count
    # only offensive/utility weight here so armor is not double-counted.
    return sum(
        int(v) for k, v in stats.items()
        if isinstance(v, (int, float)) and k not in ("armor_bonus", "magic_resist")
    )


def compute_action_rating(character: dict) -> int:
    """Stats-derived rating used for dice-delta weighting on non-combat actions
    (hunt, gather, fish, explore, loot_ruins).

    Replaces the old `compute_player_power`. Nothing here reads a scalar `power`
    field any more — Might drives physical, Insight magical, Grace accuracy, and
    equipped gear contributes through its stats.
    """
    stats = character.get("stats", {})
    level = character.get("level", 1)
    weapon_score = 0
    gear_score = 0
    for slot, item in iter_equipped_items(character):
        if slot in WEAPON_SLOTS:
            weapon_score += _item_gear_score(item)
        else:
            gear_score += _item_gear_score(item)
    main = stats.get("might", 0) + stats.get("insight", 0) + stats.get("grace", 0) // 2
    life = stats.get("vitality", 0)
    status_atk_mod = 0
    for s in character.get("statuses", []) or []:
        mods = s.get("modifiers") or {}
        status_atk_mod += int(mods.get("attack_success_mod", 0))
    return (level * 2 + main + life // 2 + weapon_score + gear_score // 2
            + stats.get("attack_success_mod", 0) + status_atk_mod)


# Backwards-compatible alias — several call sites and tests referenced the old
# name. Kept as a thin alias rather than a second implementation.
compute_player_power = compute_action_rating


# ============================================================
# MONSTER THREAT (replaces the retired `power` scalar)
# ============================================================
# `monster["power"]` was an MVP-era scalar that never tracked the monster's
# actual stats: measured rank concordance between old `power` and a stats-derived
# rating was 51% — i.e. no better than chance. Two stat formats coexisted, so
# "PWR 4" meant one thing for a flat-stat monster and something 6-9x deadlier for
# a growth-stat monster once the player levelled.
#
# Threat is derived from the monster's own stats at a given level, so it is
# internally consistent, comparable across every monster, and honest about
# level scaling. Weights favour offence because that is what a player feels
# first, with defence and sustain contributing less.
THREAT_WEIGHTS = {"offense": 0.45, "grace": 0.20, "durability": 0.20, "essence": 0.15}


def compute_monster_threat(monster: dict, level: int = 1) -> int:
    """Stats-derived threat rating for a monster at the given player level."""
    from game_engine import _compute_creature_stat

    def _stat(name: str) -> float:
        val = (monster.get("stats") or {}).get(name, 0)
        if isinstance(val, dict):
            return _compute_creature_stat(val, level)
        return val or 0

    offense = max(_stat("might"), _stat("insight"))
    score = (THREAT_WEIGHTS["offense"] * offense
             + THREAT_WEIGHTS["grace"] * _stat("grace")
             + THREAT_WEIGHTS["durability"] * _stat("durability")
             + THREAT_WEIGHTS["essence"] * _stat("essence"))
    return max(1, int(round(score)))


# ============================================================
# DERIVED COMBAT STATS (new damage & stat system)
# ============================================================
MAX_DMG_REDUCTION = 0.80  # 80% cap for armor and magic resistance


def compute_armor(character: dict) -> int:
    """Total armor = Resilience contribution + armor_bonus from stats.

    `stats['armor_bonus']` already includes every equipped piece: armor and
    shield base items carry a derived `armor_bonus`
    (see items/base_items._apply_derived_defenses) and
    `apply_enchantments_to_stats` folds equipped item stats — instances
    included — into the character's stat block. Skills and mastery mechanics
    (Paladin Faith, Knight Oath) also write to `armor_bonus`, so they compose
    here for free.

    """
    stats = character.get("stats", {})
    armor = int(stats.get("armor_bonus", 0))
    armor += int(stats.get("resilience", 0)) * ARMOR_PER_RESILIENCE
    return max(0, armor)


def compute_magic_resistance(character: dict) -> int:
    """Magic Resistance = Essence × 2 + magic_resist from equipped gear.

    Light armor grants the most magic resistance and heavy the least — the
    mirror of the armor curve — so armor_type is a genuine defensive trade-off.
    """
    stats = character.get("stats", {})
    mr = int(stats.get("essence", 0)) * 2
    mr += int(stats.get("magic_resist", 0))
    return max(0, mr)


def compute_skill_capacity(character: dict) -> int:
    """Skill Capacity = 2 + Cognition // 2, max 8."""
    stats = character.get("stats", {})
    cog = int(stats.get("cognition", 0))
    return min(8, 2 + cog // 2)


def compute_status_duration_mult(character: dict) -> float:
    """Durability × 4% reduction, max 50%."""
    stats = character.get("stats", {})
    dri = int(stats.get("durability", 0))
    reduction = min(0.50, dri * 0.04)
    return 1.0 - reduction
def compute_physical_damage(character: dict, weapon_dmg: int, skill_dmg: int) -> int:
    """Final Raw Physical Damage = (Weapon + Skill) × (1 + Might × 0.03)."""
    stats = character.get("stats", {})
    might = int(stats.get("might", 0))
    raw = weapon_dmg + skill_dmg
    return int(raw * (1 + might * 0.03))


def compute_magical_damage(character: dict, spell_dmg: int, skill_dmg: int) -> int:
    """Final Raw Magical Damage = (Spell + Skill) × (1 + Insight × 0.03)."""
    stats = character.get("stats", {})
    insight = int(stats.get("insight", 0))
    raw = spell_dmg + skill_dmg
    return int(raw * (1 + insight * 0.03))


def apply_armor(raw_dmg: int, armor: int, armor_pen_pct: float = 0.0) -> int:
    """Physical Damage Taken = Raw × 100 ÷ (100 + Armor), capped at 80% reduction.
    armor_pen_pct ignores that fraction of armor (0.3 = ignores 30%)."""
    effective_armor = int(armor * (1.0 - armor_pen_pct))
    if effective_armor <= 0:
        return raw_dmg
    reduction = 1.0 - (100.0 / (100.0 + effective_armor))
    reduction = min(reduction, MAX_DMG_REDUCTION)
    return int(raw_dmg * (1.0 - reduction))


def apply_magic_resistance(raw_dmg: int, mr: int, magic_pen_pct: float = 0.0) -> int:
    """Magical Damage Taken = Raw × 100 ÷ (100 + MR), capped at 80% reduction.
    magic_pen_pct ignores that fraction of MR (0.25 = ignores 25%)."""
    effective_mr = int(mr * (1.0 - magic_pen_pct))
    if effective_mr <= 0:
        return raw_dmg
    reduction = 1.0 - (100.0 / (100.0 + effective_mr))
    reduction = min(reduction, MAX_DMG_REDUCTION)
    return int(raw_dmg * (1.0 - reduction))


def compute_healing(character: dict, base_heal: int) -> int:
    """Final Healing = Base × (1 + Essence × 0.03)."""
    stats = character.get("stats", {})
    essence = int(stats.get("essence", 0))
    return int(base_heal * (1 + essence * 0.03))


def compute_barrier(character: dict, base_barrier: int) -> int:
    """Final Barrier = Base × (1 + Essence × 0.03)."""
    stats = character.get("stats", {})
    essence = int(stats.get("essence", 0))
    return int(base_barrier * (1 + essence * 0.03))


def compute_accuracy(character: dict) -> int:
    """Accuracy = Grace + weapon accuracy + skill accuracy + bonuses."""
    stats = character.get("stats", {})
    grace = int(stats.get("grace", 0))
    weapon_acc = 0
    for _slot, item in iter_equipped_items(character, WEAPON_SLOTS):
        weapon_acc += int(item.get("accuracy", 0) or 0)
    return grace + weapon_acc + int(stats.get("attack_success_mod", 0))


def compute_evasion(character: dict) -> int:
    """Evasion = Grace + equipment evasion + skill evasion + bonuses."""
    stats = character.get("stats", {})
    grace = int(stats.get("grace", 0))
    equip_evas = 0
    for _slot, item in iter_equipped_items(character):
        equip_evas += int(item.get("evasion", 0) or 0)
    return grace + equip_evas + int(stats.get("evasion_mod", 0))


# ============================================================
# Merge Phase 3.1 extended world data (higher continents) into base lists
# ============================================================
from game_data_p3 import extend_world_data  # noqa: E402
extend_world_data(ITEMS, MONSTERS, BIOME_ACTIONS, ITEMS_BY_ID)


# ============================================================
# Canon migration — remap all monster.biome, BIOME_ACTIONS keys, and
# ITEMS.biome_gather from the old codenames to the new canon IDs.
# NOTE: Must run BEFORE the Phase-G boss injection so the migration's
# dict rebuild doesn't overwrite freshly-injected 'boss' actions.
# ============================================================
def _apply_biome_id_migration() -> None:
    # 1. Monsters
    for m in MONSTERS:
        old = m.get("biome")
        if old and old in BIOME_ID_MAP:
            m["biome"] = BIOME_ID_MAP[old]
    # 2. BIOME_ACTIONS keys — merge lists on key collision instead of overwriting
    remapped_actions: dict = {}
    for k, v in BIOME_ACTIONS.items():
        new_k = BIOME_ID_MAP.get(k, k)
        if new_k in remapped_actions:
            # Merge: preserve existing actions, extend targets where the same action id appears twice
            existing_by_id = {a["id"]: a for a in remapped_actions[new_k]}
            for act in v:
                if act["id"] in existing_by_id:
                    existing_targets = existing_by_id[act["id"]].setdefault("targets", [])
                    for t in act.get("targets", []):
                        if t not in existing_targets:
                            existing_targets.append(t)
                else:
                    remapped_actions[new_k].append(act)
                    existing_by_id[act["id"]] = act
        else:
            remapped_actions[new_k] = list(v)  # copy list so downstream mutations don't leak
    BIOME_ACTIONS.clear()
    BIOME_ACTIONS.update(remapped_actions)
    # 3. ITEMS biome_gather references
    for it in ITEMS:
        gathers = it.get("biome_gather")
        if gathers:
            it["biome_gather"] = [BIOME_ID_MAP.get(b, b) for b in gathers]

_apply_biome_id_migration()


# ============================================================
# Phase H — merge content plan data (new monsters, items, biome actions)
# Runs AFTER canon migration so plan biome IDs are already canonical.
# Runs BEFORE boss merge so plan boss actions are in place for the
# existing boss-merge logic to append to.
# ============================================================
from content_plan_data import apply_content_plan  # noqa: E402
apply_content_plan(ITEMS, MONSTERS, BIOME_ACTIONS, ITEMS_BY_ID)


# ============================================================
# Phase G — merge bosses + boss parts + cross-continent recipes
# (Runs AFTER canon migration so injected 'boss' actions survive.)
# ============================================================
from world_content import (  # noqa: E402
    BOSSES,
    BOSS_PARTS,
)

# Add bosses to MONSTERS
_existing_monster_ids = {m["id"] for m in MONSTERS}
for _b in BOSSES:
    if _b["id"] not in _existing_monster_ids:
        MONSTERS.append(_b)
        _existing_monster_ids.add(_b["id"])
        # Bosses join a special "boss" action list in their biome, alongside hunt.
        biome_id = _b["biome"]
        if biome_id in BIOME_ACTIONS:
            hunt = next((a for a in BIOME_ACTIONS[biome_id] if a["id"] == "hunt"), None)
            if hunt and _b["id"] not in hunt["targets"]:
                hunt["targets"].append(_b["id"])
            # Also expose a dedicated boss action so the UI can single it out.
            if not any(a["id"] == "boss" for a in BIOME_ACTIONS[biome_id]):
                BIOME_ACTIONS[biome_id].append({"id": "boss", "name": "Boss", "targets": [_b["id"]]})
            else:
                boss_act = next(a for a in BIOME_ACTIONS[biome_id] if a["id"] == "boss")
                if _b["id"] not in boss_act["targets"]:
                    boss_act["targets"].append(_b["id"])

# Add boss parts to ITEMS
_existing_item_ids = {it["id"] for it in ITEMS}
for _p in BOSS_PARTS:
    if _p["id"] not in _existing_item_ids:
        ITEMS.append(_p)
        ITEMS_BY_ID[_p["id"]] = _p


# Sanity assertion — every boss biome MUST expose a dedicated 'boss' action.
for _b in BOSSES:
    _bid = _b["biome"]
    assert _bid in BIOME_ACTIONS, f"Boss biome '{_bid}' missing from BIOME_ACTIONS"
    assert any(a["id"] == "boss" for a in BIOME_ACTIONS[_bid]), \
        f"Boss biome '{_bid}' is missing dedicated 'boss' action"


# ============================================================
# Post-process monsters: add range, gear_drop_chance, rune_drop_chance
# ============================================================
# Range: archers/casters get range, melee get 0
_RANGE_BY_ARCHETYPE = {
    "archer": 3, "caster": 2, "ranger": 3, "shaman": 2,
    "sniper": 4, "artillery": 4, "flying": 2,
}
_RANGE_BY_SPECIES = {
    "dragon": 2, "wyvern": 3, "phoenix": 3, "harpy": 2,
    "sprite": 2, "fairy": 2, "wisp": 3, "ghost": 2,
    "elemental": 2, "specter": 2, "spirit": 2,
}

# Gear drop chances by creature_tier
_GEAR_DROP_CHANCE = {
    "normal": 0.08, "mini_boss": 0.25, "boss": 0.50,
    "legendary": 0.75, "event": 1.0,
}
# Rune drop chances by creature_tier
_RUNE_DROP_CHANCE = {
    "normal": 0.02, "mini_boss": 0.10, "boss": 0.25,
    "legendary": 0.50, "event": 0.80,
}

for _m in MONSTERS:
    # Range
    if "range" not in _m:
        _r = _RANGE_BY_ARCHETYPE.get(_m.get("archetype", ""), 0)
        if _r == 0:
            _r = _RANGE_BY_SPECIES.get(_m.get("species", ""), 0)
        _m["range"] = _r
    # Gear drop chance
    if "gear_drop_chance" not in _m:
        _tier = _m.get("creature_tier", "normal")
        _m["gear_drop_chance"] = _GEAR_DROP_CHANCE.get(_tier, 0.08)
    # Rune drop chance
    if "rune_drop_chance" not in _m:
        _tier = _m.get("creature_tier", "normal")
        _m["rune_drop_chance"] = _RUNE_DROP_CHANCE.get(_tier, 0.02)
    # Gear pool: default to empty list (generator will use fallback)
    if "gear_pool" not in _m:
        _m["gear_pool"] = []


# ============================================================
# Phase I — merge generated crafting data (items + recipes)
# ============================================================
from crafting_data import (  # noqa: E402
    REFINED_ITEMS,
    REFINED_RECIPES,
    GEAR_ITEMS,
    GEAR_RECIPES,
    CONSUMABLE_ITEMS,
    CONSUMABLE_RECIPES,
    ENCHANT_RECIPES,
)

_existing_item_ids = {it["id"] for it in ITEMS}
for _ci in REFINED_ITEMS + GEAR_ITEMS + CONSUMABLE_ITEMS:
    if _ci["id"] not in _existing_item_ids:
        ITEMS.append(_ci)
        ITEMS_BY_ID[_ci["id"]] = _ci
        _existing_item_ids.add(_ci["id"])

# Post-process GEAR_ITEMS: assign weapon_type based on name patterns
_GEAR_WEAPON_TYPE_MAP = {
    "blade": "sword_1h", "sword": "sword_1h",
    "cleaver": "axe_1h", "axe": "axe_1h",
    "hammer": "hammer_1h", "mace": "hammer_1h",
    "spear": "spear", "lance": "spear",
    "shield": "shield",
    "bow": "bow", "crossbow": "crossbow",
    "dagger": "dagger", "knife": "dagger",
    "staff": "tome", "wand": "orb", "orb": "orb", "tome": "tome",
    "katar": "katar",
    "scythe": "scythe",
    "instrument": "instrument", "lute": "instrument", "flute": "instrument",
}
for _gi in GEAR_ITEMS:
    if _gi.get("kind") == "weapon" and not _gi.get("weapon_type"):
        _name_lower = _gi.get("name", "").lower()
        _matched = False
        for _keyword, _wtype in _GEAR_WEAPON_TYPE_MAP.items():
            if _keyword in _name_lower:
                _gi["weapon_type"] = _wtype
                _matched = True
                break
        if not _matched:
            _gi["weapon_type"] = "sword_1h"  # default fallback
        # Update slot from old 'weapon' to proper hand slot
        if _gi.get("slot") == "weapon":
            _gi["slot"] = "right_hand"
    # Map old 'armor' slot to proper body slot
    if _gi.get("slot") == "armor":
        _gi["slot"] = "body"

_existing_recipe_ids = {r["id"] for r in RECIPES}
for _cr in REFINED_RECIPES + GEAR_RECIPES + CONSUMABLE_RECIPES + ENCHANT_RECIPES:
    if _cr["id"] not in _existing_recipe_ids:
        RECIPES.append(_cr)
        RECIPES_BY_ID[_cr["id"]] = _cr
        _existing_recipe_ids.add(_cr["id"])
