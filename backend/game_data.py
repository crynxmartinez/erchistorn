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
        "starting_stats": {"vitality": 4, "cognition": 3, "essence": 3, "drive": 5},
        "perk": {"id": "sacred_oath", "name": "Sacred Oath",
                 "desc": "Fulfil your oath in the world of Erchis to regain Drive and gain milestone rewards."},
        "story": "Within the sprawling Human Empire of Erchis, a person's word is considered sacred. Legends say a ruler's promise could rally armies, forge alliances, and shape destiny itself. Their greatest magic is a promise kept.",
        "roles": ["fighter", "guardian", "scout", "scholar", "healer"],
        "masteries": ["knight", "paladin", "lancer", "rogue", "bard", "alchemist"],
        "portrait_seeds": ["Aldric", "Selene", "Corvus", "Isolde", "Roland"],
    },
    {
        "id": "elf",
        "name": "Elf",
        "title": "The Higher Enclave of Haya",
        "starting_stats": {"vitality": 3, "cognition": 4, "essence": 5, "drive": 5},
        "perk": {"id": "children_of_sun_moon", "name": "Children of the Sun and Moon",
                 "desc": "By day, +3 healing received. By night, +3 evasion and +3 attack success."},
        "story": "Once bound to the Great Tree of Haya, the Elves now walk beneath the light of the sun and the glow of the moon. Sun-forged armour, moon-touched weapons — rebirth through adaptation.",
        "roles": ["scholar", "healer", "scout"],
        "masteries": ["mage", "priest", "druid", "assassin", "hunter", "paladin"],
        "portrait_seeds": ["Aelindra", "Thaelor", "Sylwen", "Erevan", "Naeris"],
    },
    {
        "id": "dwarf",
        "name": "Dwarf",
        "title": "The Dwarves of the Undermountain Realm",
        "starting_stats": {"vitality": 5, "cognition": 3, "essence": 2, "drive": 6},
        "perk": {"id": "mountain_resilience", "name": "Mountain Resilience",
                 "desc": "Each point of Resilience also directly increases Vitality (bonus HP)."},
        "story": "Forged of stone and endurance, the Dwarves carved mighty halls beneath the mountains. Masters of forge, drink, and defence — masters of Jahra, a metal light as breath yet strong as fate.",
        "roles": ["fighter", "guardian"],
        "masteries": ["knight", "paladin", "lancer", "alchemist"],
        "portrait_seeds": ["Borin", "Thora", "Durgin", "Helga", "Krogan"],
    },
    {
        "id": "half_elf",
        "name": "Half-Elf",
        "title": "The Half-Elf Diplomatic Federation",
        "starting_stats": {"vitality": 3, "cognition": 4, "essence": 4, "drive": 7},
        "perk": {"id": "dual_heritage", "name": "Dual Heritage",
                 "desc": "Choose one heritage — Human (Sacred Oath) or Elven (Children of Sun and Moon)."},
        "story": "Rejected once, celebrated now. Born between worlds, Half-Elves forged a federation where blood matters less than deed. Diplomats, mediators, bridge-walkers.",
        "roles": ["scout", "scholar", "healer", "guardian", "fighter"],
        "masteries": ["bard", "rogue", "paladin", "mage", "priest", "knight"],
        "portrait_seeds": ["Kaelira", "Varric", "Ambrose", "Lyriel", "Serath"],
    },
    {
        "id": "orc",
        "name": "Orc",
        "title": "The Military Force of the Orc Dominion",
        "starting_stats": {"vitality": 5, "cognition": 2, "essence": 3, "drive": 6},
        "perk": {"id": "blood_of_liberated", "name": "Blood of the Liberated",
                 "desc": "When attacking while Exhausted, roll 1d3 and restore that much HP (once per fight)."},
        "story": "Chained by demon lords for centuries, the Orcs broke free under Zaheer al-Orc the Liberator. They now guard freedom itself — not conquerors, but liberators armoured in the memory of chains.",
        "roles": ["fighter", "guardian"],
        "masteries": ["knight", "paladin", "lancer", "hunter", "alchemist"],
        "portrait_seeds": ["Zaheer", "Grosh", "Mora", "Karnak", "Ulga"],
    },
    {
        "id": "wildblood",
        "name": "Wildblood",
        "title": "The Primal Sovereignty of Wildblood",
        "starting_stats": {"vitality": 4, "cognition": 3, "essence": 4, "drive": 4},
        "perk": {"id": "inner_blood", "name": "Inner Blood",
                 "desc": "Each Exhaust point grants Inner Blood. At 5 Inner Blood, enter The Zone (buffed state)."},
        "story": "Children of Rindivar. Bearing fangs, tails, feathers, or scales — they turned barren Gennel into a living forest. Their strength grows from the bonds they protect.",
        "roles": ["fighter", "guardian", "scout", "healer"],
        "masteries": ["druid", "hunter", "lancer", "assassin", "knight", "bard"],
        "portrait_seeds": ["Fenros", "Talia", "Vaska", "Rhun", "Sable"],
    },
    {
        "id": "hyliondrian",
        "name": "Hyliondrian",
        "title": "The Underwater Kingdom of the Hyliondrians",
        "starting_stats": {"vitality": 3, "cognition": 4, "essence": 5, "drive": 6},
        "perk": {"id": "children_of_sea", "name": "Children of the Sea",
                 "desc": "Breathe underwater freely. Movement in water increases by your Grace."},
        "story": "From Atlantyrion beneath the waves, the Hyliondrians guard the Orb of Hyliondrias — treasure of the gods. Tide Mothers, coral cities, prophecies old as tide.",
        "roles": ["scholar", "healer", "scout"],
        "masteries": ["mage", "priest", "druid", "hunter", "lancer", "paladin"],
        "portrait_seeds": ["Nerith", "Coralia", "Thalos", "Vaela", "Murrin"],
    },
    {
        "id": "sylvan",
        "name": "Sylvan",
        "title": "The Sylvans of Daw'ul Talalu",
        "starting_stats": {"vitality": 2, "cognition": 5, "essence": 4, "drive": 5},
        "perk": {"id": "shrink", "name": "Shrink",
                 "desc": "Reduce your body to a tiny form: +5 Evasion but -5 Strike. Toggle with an action."},
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
    {"id": "knight",    "name": "Knight",    "desc": "Sworn blade, heavy plate, disciplined charge.",       "starting_skills": ["shield_bash", "sworn_strike"]},
    {"id": "paladin",   "name": "Paladin",   "desc": "Holy warrior of oath and light.",                     "starting_skills": ["smite", "lay_on_hands"]},
    {"id": "lancer",    "name": "Lancer",    "desc": "Reach, precision, formation warfare.",               "starting_skills": ["thrust", "impale"]},
    {"id": "rogue",     "name": "Rogue",     "desc": "Shadows, coin, and locks that don't want to open.",  "starting_skills": ["backstab", "vanish"]},
    {"id": "bard",      "name": "Bard",      "desc": "Words that heal, words that harm.",                  "starting_skills": ["mocking_verse", "rally"]},
    {"id": "alchemist", "name": "Alchemist", "desc": "Turn weeds into potions and stone into gold.",       "starting_skills": ["mix_potion", "acid_flask"]},
    {"id": "mage",      "name": "Mage",      "desc": "Arcane fire, arcane truth, arcane cost.",            "starting_skills": ["arcane_bolt", "ward"]},
    {"id": "priest",    "name": "Priest",    "desc": "Voice of the gods, hand of mercy.",                  "starting_skills": ["divine_light", "purge"]},
    {"id": "druid",     "name": "Druid",     "desc": "The wild answers when called.",                      "starting_skills": ["thornlash", "beast_call"]},
    {"id": "assassin",  "name": "Assassin",  "desc": "One blade, one moment, one target.",                 "starting_skills": ["shadow_step", "poison_blade"]},
    {"id": "hunter",    "name": "Hunter",    "desc": "The bow, the trail, the patient shot.",              "starting_skills": ["aimed_shot", "trap"]},
]


# ============================================================
# CONTINENTS + BIOMES + LOCATIONS
# ============================================================
CONTINENTS: list[dict] = [
    {
        "id": "aetheria", "name": "Aetheria", "level_req": 1,
        "desc": "The heartland of the Human Empire. Rolling grasslands, ancient oakwoods, and rivers that whisper old oaths.",
        "biomes": [
            {"id": "grasslands", "name": "Whispering Grasslands", "desc": "Endless sunlit plains where wolves prowl and bandits watch the road."},
            {"id": "oakwood",    "name": "Elder Oakwood",        "desc": "Old trees, older ghosts. Wisps drift between the trunks."},
            {"id": "riverlands", "name": "Riverlands",           "desc": "Slow rivers, silver fish, and stones that hum when touched."},
            {"id": "old_ruins",  "name": "Old Kingdom Ruins",    "desc": "Fallen stones of forgotten kings. Loot the dead, but keep one eye up."},
        ],
    },
    {"id": "vulkaros",    "name": "Vulkaros",    "level_req": 8,
     "desc": "Volcanic ashlands and lava caves. Home to Orc dominions and fire-drakes.",
     "biomes": [
        {"id": "ashlands",      "name": "Ashen Plains",       "desc": "Soot-choked steppes where basalt shards cut the wind. Orc war-camps burn on the horizon."},
        {"id": "lava_caves",    "name": "Lava Caves",          "desc": "Molten veins snake through obsidian tunnels. Fire-drakes coil in the deep."},
        {"id": "basalt_steppe", "name": "Basalt Steppe",       "desc": "Cracked plateaus where the earth still remembers old wars."},
        {"id": "obsidian_pits", "name": "Obsidian Pits",       "desc": "Glassy craters left by fallen sky-stones. Warbands scavenge here."},
     ]},
    {"id": "nyxmoor",     "name": "Nyxmoor",     "level_req": 15,
     "desc": "Cursed bogs where demons once walked. Wraiths and hags remember.",
     "biomes": [
        {"id": "bogland",       "name": "Whispering Bogland",  "desc": "Black water and reeds that murmur in dead tongues."},
        {"id": "cursed_ruins",  "name": "Cursed Ruins",        "desc": "Sunken towers of a fallen coven. Every stone hums with old spite."},
        {"id": "deadwood",      "name": "Deadwood",             "desc": "Trees that never rot but never live. The bark bleeds when cut."},
        {"id": "ghost_road",    "name": "Ghost Road",           "desc": "An old imperial road drowned in mist and dread."},
     ]},
    {"id": "frosthelm",   "name": "Frosthelm",   "level_req": 22,
     "desc": "Tundras and glaciers above the great Dwarven Undermountain.",
     "biomes": [
        {"id": "frozen_peaks",  "name": "Frozen Peaks",         "desc": "Wind-scoured summits where only the sure-footed survive."},
        {"id": "glacier",       "name": "Ancient Glacier",      "desc": "Slow, patient ice that hides bronze-age bones."},
        {"id": "tundra",        "name": "Endless Tundra",       "desc": "White plains under a violet sky. Mammoths trumpet in the distance."},
        {"id": "ice_caverns",   "name": "Ice Caverns",          "desc": "Blue-veined vaults beneath the surface, thick with frost wyrms."},
     ]},
    {"id": "zephyria",    "name": "Zephyria",    "level_req": 30,
     "desc": "Sky islands and storm-peaks — the Higher Enclave of the Elves.",
     "biomes": [
        {"id": "sky_isles",       "name": "Sky Isles",         "desc": "Floating cliffs bound by wind-currents and old elven pacts."},
        {"id": "cloud_forest",    "name": "Cloud Forest",      "desc": "Silver-leaf trees drink the mist. Griffons nest in the crowns."},
        {"id": "storm_plateau",   "name": "Storm Plateau",     "desc": "A high desert of lightning-glass where sky spirits duel."},
        {"id": "celestial_ruins", "name": "Celestial Ruins",   "desc": "Stones of the first Enclave, drifting silent above the storms."},
     ]},
    {"id": "sablewaste",  "name": "Sablewaste",  "level_req": 38,
     "desc": "Dunes and ancient ruins where djinn whisper broken bargains.",
     "biomes": [
        {"id": "dune_sea",        "name": "Dune Sea",           "desc": "Rolling golden dunes that hide caravans and city-bones alike."},
        {"id": "oasis",           "name": "Oasis of Silver Palms","desc": "A jewel of water and shade. Fortunes are made and lost by its wells."},
        {"id": "djinn_ruins",     "name": "Djinn Ruins",        "desc": "Marble bridges to nowhere. Wishes still linger in the sand."},
        {"id": "sunken_temple",   "name": "Sunken Temple",      "desc": "A monastery half-swallowed by the dunes. Its bells still ring."},
     ]},
    {"id": "verdania",    "name": "Verdania",    "level_req": 45,
     "desc": "Deep jungle and coral coasts leading to Atlantyrion.",
     "biomes": [
        {"id": "rainforest",       "name": "Emerald Rainforest", "desc": "Towering canopy woven with vine-bridges and sylvan choirs."},
        {"id": "canopy_boughs",    "name": "Canopy Boughs",      "desc": "Sylvan villages perched on branches thick as roads."},
        {"id": "coral_reef",       "name": "Coral Reef",         "desc": "The living wall between world and undersea kingdom."},
        {"id": "sunken_atlantyrion","name": "Sunken Atlantyrion","desc": "Spiralling towers of pearl and jade beneath the tide."},
     ]},
]


# ============================================================
# MONSTERS (Aetheria for MVP)
# ============================================================
MONSTERS: list[dict] = [
    {"id": "gray_wolf",    "name": "Gray Wolf",    "biome": "grasslands", "power": 3,  "hp": 18,
     "drops": [("wolf_pelt", 0.7), ("wolf_fang", 0.4)]},
    {"id": "highway_bandit","name": "Highway Bandit","biome": "grasslands", "power": 5, "hp": 24,
     "drops": [("coin_purse", 0.8), ("iron_dagger", 0.15)]},
    {"id": "grove_wisp",   "name": "Grove Wisp",   "biome": "oakwood",    "power": 4,  "hp": 15,
     "drops": [("wisp_essence", 0.6), ("skillbook_ward", 0.03)]},
    {"id": "boar",         "name": "Feral Boar",   "biome": "oakwood",    "power": 6,  "hp": 30,
     "drops": [("boar_hide", 0.7), ("boar_tusk", 0.5)]},
    {"id": "river_serpent","name": "River Serpent","biome": "riverlands", "power": 7,  "hp": 28,
     "drops": [("serpent_scale", 0.7), ("serpent_venom", 0.3)]},
    {"id": "ruin_ghast",   "name": "Ruin Ghast",   "biome": "old_ruins",  "power": 9,  "hp": 38,
     "drops": [("ghast_dust", 0.6), ("relic_shard", 0.4), ("skillbook_purge", 0.05)]},
]


# ============================================================
# MATERIALS + ITEMS
# ============================================================
# rarity: common | uncommon | rare | epic | legendary | mythic
# kind: material | weapon | armor | consumable | skillbook | relic
ITEMS: list[dict] = [
    # --- Materials (common) ---
    {"id": "wild_herb",     "name": "Wild Herb",     "rarity": "common",   "kind": "material", "biome_gather": ["grasslands", "oakwood"]},
    {"id": "iron_ore",      "name": "Iron Ore",      "rarity": "common",   "kind": "material", "biome_gather": ["grasslands", "old_ruins"]},
    {"id": "oak_log",       "name": "Oak Log",       "rarity": "common",   "kind": "material", "biome_gather": ["oakwood"]},
    {"id": "river_stone",   "name": "River Stone",   "rarity": "common",   "kind": "material", "biome_gather": ["riverlands"]},
    {"id": "copper_ore",    "name": "Copper Ore",    "rarity": "common",   "kind": "material", "biome_gather": ["grasslands"]},
    # --- Materials (uncommon) ---
    {"id": "wolf_pelt",     "name": "Wolf Pelt",     "rarity": "uncommon", "kind": "material"},
    {"id": "wolf_fang",     "name": "Wolf Fang",     "rarity": "uncommon", "kind": "material"},
    {"id": "boar_hide",     "name": "Boar Hide",     "rarity": "uncommon", "kind": "material"},
    {"id": "boar_tusk",     "name": "Boar Tusk",     "rarity": "uncommon", "kind": "material"},
    {"id": "serpent_scale", "name": "Serpent Scale", "rarity": "uncommon", "kind": "material"},
    {"id": "wisp_essence",  "name": "Wisp Essence",  "rarity": "uncommon", "kind": "material"},
    # --- Materials (rare) ---
    {"id": "serpent_venom", "name": "Serpent Venom", "rarity": "rare",     "kind": "material"},
    {"id": "ghast_dust",    "name": "Ghast Dust",    "rarity": "rare",     "kind": "material"},
    {"id": "relic_shard",   "name": "Relic Shard",   "rarity": "epic",     "kind": "relic"},
    # --- Gold pouch / drops ---
    {"id": "coin_purse",    "name": "Coin Purse",    "rarity": "common",   "kind": "consumable", "effect": {"gold": 15}},
    # --- Weapons ---
    {"id": "iron_dagger",   "name": "Iron Dagger",   "rarity": "common",   "kind": "weapon",   "power": 3,  "slot": "weapon"},
    {"id": "oak_shortbow",  "name": "Oak Shortbow",  "rarity": "uncommon", "kind": "weapon",   "power": 5,  "slot": "weapon"},
    {"id": "iron_longsword","name": "Iron Longsword","rarity": "uncommon", "kind": "weapon",   "power": 6,  "slot": "weapon"},
    {"id": "wolfbone_axe",  "name": "Wolfbone Axe",  "rarity": "rare",     "kind": "weapon",   "power": 9,  "slot": "weapon"},
    {"id": "riverstone_staff","name":"Riverstone Staff","rarity":"rare",   "kind": "weapon",   "power": 8,  "slot": "weapon"},
    # --- Armor ---
    {"id": "traveler_garb", "name": "Traveler's Garb","rarity":"common",   "kind": "armor",    "power": 2,  "slot": "armor"},
    {"id": "boarhide_vest", "name": "Boarhide Vest",  "rarity": "uncommon","kind": "armor",    "power": 4,  "slot": "armor"},
    {"id": "wolfpelt_cloak","name": "Wolfpelt Cloak", "rarity": "uncommon","kind": "armor",    "power": 3,  "slot": "armor"},
    {"id": "scaled_hauberk","name":"Scaled Hauberk",  "rarity": "rare",    "kind": "armor",    "power": 7,  "slot": "armor"},
    # --- Consumables ---
    {"id": "minor_healing_potion","name":"Minor Healing Potion","rarity":"common", "kind":"consumable",
     "effect": {"heal": 15}, "trigger": "hp_below_50"},
    {"id": "greater_healing_potion","name":"Greater Healing Potion","rarity":"uncommon","kind":"consumable",
     "effect": {"heal": 35}, "trigger": "hp_below_40"},
    {"id": "antidote",       "name": "Antidote",       "rarity": "common",   "kind": "consumable",
     "effect": {"cure": "poison"}, "trigger": "status_poison"},
    {"id": "bandage",        "name": "Bandage",        "rarity": "common",   "kind": "consumable",
     "effect": {"cure": "bleeding"}, "trigger": "status_bleeding"},
    {"id": "acid_flask_item","name": "Acid Flask",     "rarity": "uncommon", "kind": "consumable",
     "effect": {"damage": 20}, "trigger": "opponent_hp_high"},
    # --- Skillbooks ---
    {"id": "skillbook_ward",  "name":"Skillbook: Ward",  "rarity":"rare","kind":"skillbook","teaches":"ward"},
    {"id": "skillbook_purge", "name":"Skillbook: Purge", "rarity":"rare","kind":"skillbook","teaches":"purge"},
    {"id": "skillbook_thornlash","name":"Skillbook: Thornlash","rarity":"epic","kind":"skillbook","teaches":"thornlash"},
    {"id": "skillbook_smite", "name":"Skillbook: Smite", "rarity":"epic","kind":"skillbook","teaches":"smite"},
    # --- Legendary / Mythic teasers ---
    {"id": "jahra_ingot",    "name":"Jahra Ingot",    "rarity":"legendary","kind":"material","desc":"A rare Dwarven metal."},
    {"id": "orb_fragment",   "name":"Orb Fragment",   "rarity":"mythic",   "kind":"relic",   "desc":"A shard fallen from the Orb of Hyliondrias."},
]

ITEMS_BY_ID: dict[str, dict] = {it["id"]: it for it in ITEMS}


# ============================================================
# SKILLS
# ============================================================
# power_type: strike | defend | heal | debuff | crit_boost
# trigger: always | low_hp | opponent_wounded | opponent_status | opening_move
SKILLS: list[dict] = [
    {"id": "shield_bash",   "name": "Shield Bash",   "cooldown": 2, "power": 6,  "power_type": "strike",       "trigger": "always",           "status_apply": "stunned"},
    {"id": "sworn_strike",  "name": "Sworn Strike",  "cooldown": 3, "power": 10, "power_type": "strike",       "trigger": "always"},
    {"id": "smite",         "name": "Smite",         "cooldown": 3, "power": 12, "power_type": "strike",       "trigger": "opponent_wounded"},
    {"id": "lay_on_hands",  "name": "Lay on Hands",  "cooldown": 4, "power": 25, "power_type": "heal",         "trigger": "low_hp"},
    {"id": "thrust",        "name": "Thrust",        "cooldown": 1, "power": 5,  "power_type": "strike",       "trigger": "always"},
    {"id": "impale",        "name": "Impale",        "cooldown": 4, "power": 15, "power_type": "strike",       "trigger": "opening_move", "status_apply": "bleeding"},
    {"id": "backstab",      "name": "Backstab",      "cooldown": 3, "power": 14, "power_type": "strike",       "trigger": "opening_move", "status_apply": "bleeding"},
    {"id": "vanish",        "name": "Vanish",        "cooldown": 5, "power": 0,  "power_type": "defend",       "trigger": "low_hp",           "self_status": "hidden"},
    {"id": "mocking_verse", "name": "Mocking Verse", "cooldown": 2, "power": 4,  "power_type": "debuff",       "trigger": "always",           "status_apply": "shaken"},
    {"id": "rally",         "name": "Rally",         "cooldown": 4, "power": 15, "power_type": "heal",         "trigger": "low_hp"},
    {"id": "mix_potion",    "name": "Mix Potion",    "cooldown": 6, "power": 20, "power_type": "heal",         "trigger": "low_hp"},
    {"id": "acid_flask",    "name": "Acid Flask",    "cooldown": 2, "power": 7,  "power_type": "strike",       "trigger": "always",           "status_apply": "burning"},
    {"id": "arcane_bolt",   "name": "Arcane Bolt",   "cooldown": 1, "power": 6,  "power_type": "strike",       "trigger": "always"},
    {"id": "ward",          "name": "Ward",          "cooldown": 4, "power": 0,  "power_type": "defend",       "trigger": "always",           "self_status": "warded"},
    {"id": "divine_light",  "name": "Divine Light",  "cooldown": 3, "power": 10, "power_type": "strike",       "trigger": "opponent_status", "status_apply": "blinded"},
    {"id": "purge",         "name": "Purge",         "cooldown": 3, "power": 0,  "power_type": "defend",       "trigger": "self_debuff"},
    {"id": "thornlash",     "name": "Thornlash",     "cooldown": 2, "power": 8,  "power_type": "strike",       "trigger": "always",           "status_apply": "bleeding"},
    {"id": "beast_call",    "name": "Beast Call",    "cooldown": 5, "power": 12, "power_type": "strike",       "trigger": "always"},
    {"id": "shadow_step",   "name": "Shadow Step",   "cooldown": 3, "power": 0,  "power_type": "defend",       "trigger": "always",           "self_status": "evasive"},
    {"id": "poison_blade",  "name": "Poison Blade",  "cooldown": 3, "power": 8,  "power_type": "strike",       "trigger": "always",           "status_apply": "poisoned"},
    {"id": "aimed_shot",    "name": "Aimed Shot",    "cooldown": 2, "power": 10, "power_type": "strike",       "trigger": "opening_move"},
    {"id": "trap",          "name": "Trap",          "cooldown": 4, "power": 6,  "power_type": "debuff",       "trigger": "always",           "status_apply": "ensnared"},
    {"id": "mend",          "name": "Mend",          "cooldown": 3, "power": 18, "power_type": "heal",         "trigger": "low_hp"},
]

SKILLS_BY_ID: dict[str, dict] = {s["id"]: s for s in SKILLS}


# ============================================================
# CRAFTING RECIPES
# ============================================================
# outcome tier = based on crafting dice roll
RECIPES: list[dict] = [
    {"id": "craft_iron_dagger", "name": "Iron Dagger",
     "materials": [("iron_ore", 2), ("oak_log", 1)],
     "profession_req": [], "min_level": 1,
     "output_by_tier": {"crude": "iron_dagger", "fine": "iron_dagger", "master": "iron_longsword"}},
    {"id": "craft_oak_shortbow", "name": "Oak Shortbow",
     "materials": [("oak_log", 3), ("wolf_fang", 1)],
     "profession_req": [], "min_level": 1,
     "output_by_tier": {"crude": "oak_shortbow", "fine": "oak_shortbow", "master": "oak_shortbow"}},
    {"id": "craft_wolfpelt_cloak", "name": "Wolfpelt Cloak",
     "materials": [("wolf_pelt", 2)],
     "profession_req": [], "min_level": 2,
     "output_by_tier": {"crude": "wolfpelt_cloak", "fine": "wolfpelt_cloak", "master": "wolfpelt_cloak"}},
    {"id": "craft_boarhide_vest", "name": "Boarhide Vest",
     "materials": [("boar_hide", 2), ("boar_tusk", 1)],
     "profession_req": [], "min_level": 2,
     "output_by_tier": {"crude": "boarhide_vest", "fine": "boarhide_vest", "master": "scaled_hauberk"}},
    {"id": "craft_minor_healing_potion", "name": "Minor Healing Potion",
     "materials": [("wild_herb", 2), ("river_stone", 1)],
     "profession_req": ["alchemist"], "min_level": 1,
     "output_by_tier": {"crude": "minor_healing_potion", "fine": "minor_healing_potion", "master": "greater_healing_potion"}},
    {"id": "craft_greater_healing_potion", "name": "Greater Healing Potion",
     "materials": [("wild_herb", 4), ("wisp_essence", 1)],
     "profession_req": ["alchemist"], "min_level": 3,
     "output_by_tier": {"crude": "greater_healing_potion", "fine": "greater_healing_potion", "master": "greater_healing_potion"}},
    {"id": "craft_antidote", "name": "Antidote",
     "materials": [("wild_herb", 1), ("serpent_scale", 1)],
     "profession_req": ["alchemist"], "min_level": 2,
     "output_by_tier": {"crude": "antidote", "fine": "antidote", "master": "antidote"}},
    {"id": "craft_iron_longsword", "name": "Iron Longsword",
     "materials": [("iron_ore", 4), ("oak_log", 1)],
     "profession_req": [], "min_level": 3,
     "output_by_tier": {"crude": "iron_dagger", "fine": "iron_longsword", "master": "wolfbone_axe"}},
    {"id": "craft_wolfbone_axe", "name": "Wolfbone Axe",
     "materials": [("iron_ore", 2), ("wolf_fang", 3), ("oak_log", 1)],
     "profession_req": [], "min_level": 4,
     "output_by_tier": {"crude": "iron_longsword", "fine": "wolfbone_axe", "master": "wolfbone_axe"}},
    {"id": "craft_riverstone_staff", "name": "Riverstone Staff",
     "materials": [("river_stone", 3), ("oak_log", 2), ("wisp_essence", 1)],
     "profession_req": [], "min_level": 3,
     "output_by_tier": {"crude": "riverstone_staff", "fine": "riverstone_staff", "master": "riverstone_staff"}},
    {"id": "craft_acid_flask", "name": "Acid Flask",
     "materials": [("serpent_venom", 1), ("river_stone", 2)],
     "profession_req": ["alchemist"], "min_level": 3,
     "output_by_tier": {"crude": "acid_flask_item", "fine": "acid_flask_item", "master": "acid_flask_item"}},
]

RECIPES_BY_ID: dict[str, dict] = {r["id"]: r for r in RECIPES}


# ============================================================
# NPC SKILL TEACHERS (in Aetheria for MVP)
# ============================================================
TEACHERS: list[dict] = [
    {"id": "master_arden", "name": "Master Arden", "biome": "grasslands",
     "desc": "A retired knight whose axe knows both blood and mercy.",
     "teaches": [{"skill_id": "shield_bash", "cost_gold": 100, "level_req": 2},
                 {"skill_id": "sworn_strike", "cost_gold": 250, "level_req": 4}]},
    {"id": "elder_lyria", "name": "Elder Lyria", "biome": "oakwood",
     "desc": "A grove-keeper who reads the wind and the roots.",
     "teaches": [{"skill_id": "mend", "cost_gold": 80,  "level_req": 1},
                 {"skill_id": "ward", "cost_gold": 300, "level_req": 5}]},
    {"id": "trapper_kell", "name": "Trapper Kell", "biome": "riverlands",
     "desc": "A hunter with more scars than he has stories.",
     "teaches": [{"skill_id": "aimed_shot", "cost_gold": 120, "level_req": 2},
                 {"skill_id": "trap",       "cost_gold": 180, "level_req": 3}]},
]


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


def get_continent(c_id: str) -> dict | None:
    return next((c for c in CONTINENTS if c["id"] == c_id), None)


def get_monster(m_id: str) -> dict | None:
    return next((m for m in MONSTERS if m["id"] == m_id), None)


def compute_starting_hp(stats: dict) -> int:
    """Vitality * 8 + 20 baseline."""
    return int(stats.get("vitality", 3)) * 8 + 20


def compute_player_power(character: dict) -> int:
    """Rough combat power score used for dice-delta weighting.
    New system: Might drives physical, Insight drives magical, Grace tips accuracy."""
    stats = character.get("stats", {})
    level = character.get("level", 1)
    weapon_pow = 0
    armor_pow = 0
    equipped = character.get("equipped", {})
    if equipped.get("weapon"):
        item = ITEMS_BY_ID.get(equipped["weapon"])
        if item:
            weapon_pow = item.get("power", 0)
    if equipped.get("armor"):
        item = ITEMS_BY_ID.get(equipped["armor"])
        if item:
            armor_pow = item.get("power", 0)
    # Combat power: level scales, Might/Insight are primary damage stats, Grace tips accuracy.
    main = stats.get("might", 0) + stats.get("insight", 0) + stats.get("grace", 0) // 2
    life = stats.get("vitality", 0)  # small survivability contribution
    return level * 2 + main + life // 2 + weapon_pow + armor_pow // 2 + stats.get("attack_success_mod", 0)


# ============================================================
# Merge Phase 3.1 extended world data (higher continents) into base lists
# ============================================================
from game_data_p3 import extend_world_data  # noqa: E402
extend_world_data(ITEMS, MONSTERS, BIOME_ACTIONS, ITEMS_BY_ID)
