"""Phase 3.1 world content — monsters, materials, and biome actions for the
six late-game continents (Vulkaros, Nyxmoor, Frosthelm, Zephyria, Sablewaste,
Verdania). Power/HP scales roughly with each continent's level_req so the
existing dice-power delta engine stays balanced.

These lists are *merged into* the base MONSTERS / ITEMS / BIOME_ACTIONS in
game_data.py at import time via extend_world_data().
"""
from __future__ import annotations


# ============================================================
# MATERIALS + LOOT DROPS (shared across biomes when sensible)
# ============================================================
EXTRA_ITEMS: list[dict] = [
    # ---------------- VULKAROS ----------------
    {"id": "basalt_shard",    "name": "Basalt Shard",    "rarity": "common",   "kind": "material",
     "biome_gather": ["basalt_steppe", "obsidian_pits"]},
    {"id": "sulphur_crystal", "name": "Sulphur Crystal", "rarity": "uncommon", "kind": "material",
     "biome_gather": ["lava_caves", "obsidian_pits"]},
    {"id": "obsidian_chunk",  "name": "Obsidian Chunk",  "rarity": "uncommon", "kind": "material",
     "biome_gather": ["lava_caves", "obsidian_pits"]},
    {"id": "ash_grass",       "name": "Ash Grass",       "rarity": "common",   "kind": "material",
     "biome_gather": ["ashlands", "basalt_steppe"]},
    {"id": "drake_scale",     "name": "Drake Scale",     "rarity": "rare",     "kind": "material"},
    {"id": "orc_tooth",       "name": "Orc Tooth",       "rarity": "uncommon", "kind": "material"},
    {"id": "slime_ichor",     "name": "Magma Slime Ichor","rarity": "uncommon","kind": "material"},
    {"id": "wraith_essence",  "name": "Wraith Essence",  "rarity": "rare",     "kind": "material"},

    # ---------------- NYXMOOR ----------------
    {"id": "black_reed",      "name": "Black Reed",      "rarity": "common",   "kind": "material",
     "biome_gather": ["bogland", "deadwood"]},
    {"id": "cursed_stone",    "name": "Cursed Stone",    "rarity": "uncommon", "kind": "material",
     "biome_gather": ["cursed_ruins", "ghost_road"]},
    {"id": "hex_moss",        "name": "Hex Moss",        "rarity": "uncommon", "kind": "material",
     "biome_gather": ["bogland", "deadwood"]},
    {"id": "ghost_iron",      "name": "Ghost Iron",      "rarity": "rare",     "kind": "material",
     "biome_gather": ["cursed_ruins", "ghost_road"]},
    {"id": "wraith_lantern",  "name": "Wraith Lantern",  "rarity": "rare",     "kind": "material"},
    {"id": "hag_hair",        "name": "Hag Hair",        "rarity": "uncommon", "kind": "material"},
    {"id": "demon_ash",       "name": "Demon Ash",       "rarity": "rare",     "kind": "material"},

    # ---------------- FROSTHELM ----------------
    {"id": "frost_root",      "name": "Frost Root",      "rarity": "common",   "kind": "material",
     "biome_gather": ["tundra", "frozen_peaks"]},
    {"id": "glacier_shard",   "name": "Glacier Shard",   "rarity": "uncommon", "kind": "material",
     "biome_gather": ["glacier", "ice_caverns"]},
    {"id": "silver_vein",     "name": "Silver Vein Ore", "rarity": "uncommon", "kind": "material",
     "biome_gather": ["frozen_peaks", "ice_caverns"]},
    {"id": "cold_iron",       "name": "Cold Iron",       "rarity": "rare",     "kind": "material",
     "biome_gather": ["glacier", "ice_caverns"]},
    {"id": "wyrm_scale",      "name": "Frost Wyrm Scale","rarity": "rare",     "kind": "material"},
    {"id": "mammoth_tusk",    "name": "Mammoth Tusk",    "rarity": "rare",     "kind": "material"},
    {"id": "yeti_pelt",       "name": "Yeti Pelt",       "rarity": "uncommon", "kind": "material"},

    # ---------------- ZEPHYRIA ----------------
    {"id": "silverleaf",      "name": "Silverleaf",      "rarity": "uncommon", "kind": "material",
     "biome_gather": ["cloud_forest", "sky_isles"]},
    {"id": "storm_glass",     "name": "Storm Glass",     "rarity": "rare",     "kind": "material",
     "biome_gather": ["storm_plateau", "celestial_ruins"]},
    {"id": "sky_iron",        "name": "Sky Iron",        "rarity": "rare",     "kind": "material",
     "biome_gather": ["sky_isles", "celestial_ruins"]},
    {"id": "cloud_silk",      "name": "Cloud Silk",      "rarity": "uncommon", "kind": "material",
     "biome_gather": ["cloud_forest"]},
    {"id": "griffon_feather", "name": "Griffon Feather", "rarity": "rare",     "kind": "material"},
    {"id": "star_shard",      "name": "Star Shard",      "rarity": "epic",     "kind": "material"},
    {"id": "sky_serpent_hide","name": "Sky Serpent Hide","rarity": "rare",     "kind": "material"},

    # ---------------- SABLEWASTE ----------------
    {"id": "sun_bloom",       "name": "Sun Bloom",       "rarity": "uncommon", "kind": "material",
     "biome_gather": ["oasis", "dune_sea"]},
    {"id": "golden_sand",     "name": "Golden Sand",     "rarity": "common",   "kind": "material",
     "biome_gather": ["dune_sea", "djinn_ruins"]},
    {"id": "djinn_glass",     "name": "Djinn Glass",     "rarity": "rare",     "kind": "material",
     "biome_gather": ["djinn_ruins", "sunken_temple"]},
    {"id": "mirage_silk",     "name": "Mirage Silk",     "rarity": "epic",     "kind": "material"},
    {"id": "scarab_shell",    "name": "Scarab Shell",    "rarity": "uncommon", "kind": "material"},
    {"id": "sun_priest_seal", "name": "Sun-Priest Seal", "rarity": "epic",     "kind": "material"},
    {"id": "djinn_bottle_shard","name":"Djinn Bottle Shard","rarity":"legendary","kind":"material",
     "desc": "A cracked lip of a bottle that once held a wish."},

    # ---------------- VERDANIA ----------------
    {"id": "emerald_frond",   "name": "Emerald Frond",   "rarity": "uncommon", "kind": "material",
     "biome_gather": ["rainforest", "canopy_boughs"]},
    {"id": "pearl_shell",     "name": "Pearl Shell",     "rarity": "uncommon", "kind": "material",
     "biome_gather": ["coral_reef", "sunken_atlantyrion"]},
    {"id": "living_wood",     "name": "Living Wood",     "rarity": "rare",     "kind": "material",
     "biome_gather": ["rainforest", "canopy_boughs"]},
    {"id": "abyss_coral",     "name": "Abyss Coral",     "rarity": "rare",     "kind": "material",
     "biome_gather": ["coral_reef", "sunken_atlantyrion"]},
    {"id": "canopy_venom",    "name": "Canopy Venom",    "rarity": "rare",     "kind": "material"},
    {"id": "kraken_ink",      "name": "Kraken Ink",      "rarity": "epic",     "kind": "material"},
    {"id": "sylvan_seed",     "name": "Sylvan Seed",     "rarity": "epic",     "kind": "material"},
    {"id": "tide_priest_ring","name": "Tide-Priest Ring","rarity": "epic",     "kind": "relic"},

    # ---------------- CROSS-CONTINENT WEAPONS/ARMOR (drops only, no recipes yet) ----------------
    {"id": "basalt_axe",      "name": "Basalt War-Axe",  "rarity": "uncommon", "kind": "weapon", "slot": "right_hand"},
    {"id": "cursed_blade",    "name": "Cursed Blade",    "rarity": "rare",     "kind": "weapon", "slot": "right_hand"},
    {"id": "cold_iron_spear", "name": "Cold Iron Spear", "rarity": "rare",     "kind": "weapon", "slot": "right_hand"},
    {"id": "storm_bow",       "name": "Storm Bow",       "rarity": "epic",     "kind": "weapon", "slot": "right_hand", "two_handed": True},
    {"id": "djinn_scimitar",  "name": "Djinn Scimitar",  "rarity": "epic",     "kind": "weapon", "slot": "right_hand"},
    {"id": "sylvan_glaive",   "name": "Sylvan Glaive",   "rarity": "legendary","kind": "weapon", "slot": "right_hand", "two_handed": True},
    {"id": "ashplate",        "name": "Ashplate",        "rarity": "uncommon", "kind": "armor",  "slot": "body"},
    {"id": "mourncloak",      "name": "Mourncloak",      "rarity": "rare",     "kind": "armor",  "slot": "back"},
    {"id": "jahra_hauberk",   "name": "Jahra Hauberk",   "rarity": "rare",     "kind": "armor",  "slot": "body"},
    {"id": "sky_mantle",      "name": "Sky Mantle",      "rarity": "epic",     "kind": "armor",  "slot": "back"},
    {"id": "sunveil_robe",    "name": "Sunveil Robe",    "rarity": "epic",     "kind": "armor",  "slot": "body"},
    {"id": "coral_platemail", "name": "Coral Platemail", "rarity": "legendary","kind": "armor",  "slot": "body"},

    # ---------------- SKILLBOOKS (rare drops in higher continents) ----------------
    {"id": "skillbook_ember_lash",   "name": "Skillbook: Ember Lash",   "rarity": "epic",     "kind": "skillbook", "teaches": "ember_lash"},
    {"id": "skillbook_wraith_ward",  "name": "Skillbook: Wraith Ward",  "rarity": "epic",     "kind": "skillbook", "teaches": "wraith_ward"},
    {"id": "skillbook_frost_edge",   "name": "Skillbook: Frost Edge",   "rarity": "epic",     "kind": "skillbook", "teaches": "frost_edge"},
    {"id": "skillbook_wind_step",    "name": "Skillbook: Wind Step",    "rarity": "legendary","kind": "skillbook", "teaches": "wind_step"},
    {"id": "skillbook_sunlance",     "name": "Skillbook: Sunlance",     "rarity": "legendary","kind": "skillbook", "teaches": "sunlance"},
    {"id": "skillbook_tidefury",     "name": "Skillbook: Tidefury",     "rarity": "legendary","kind": "skillbook", "teaches": "tidefury"},
]


# ============================================================
# MONSTERS (2 per biome × 24 biomes = 48 new)
# ============================================================
EXTRA_MONSTERS: list[dict] = [
    # ================ VULKAROS (Lv 8+) ================
    # ashlands
    {"id": "ash_hound",         "name": "Ash Hound",         "biome": "ashlands",      "hp": 55,
     "stats": {"might": {"base": 11, "growth": 0.9}, "grace": {"base": 5, "growth": 0.9}, "cognition": {"base": 2, "growth": 0.9}, "insight": {"base": 2, "growth": 0.9}, "essence": {"base": 2, "growth": 0.9}, "durability": {"base": 5, "growth": 0.9}},
     "drops": [("ash_grass", 0.5), ("wolf_pelt", 0.5), ("basalt_shard", 0.3)]},
    {"id": "orc_grunt",         "name": "Orc Grunt",         "biome": "ashlands",      "hp": 68,
     "drops": [("orc_tooth", 0.6), ("iron_ore", 0.5), ("basalt_axe", 0.08)]},
    # lava_caves
    {"id": "fire_drake_whelp",  "name": "Fire-Drake Whelp",  "biome": "lava_caves",    "hp": 78,
     "stats": {"might": {"base": 15, "growth": 0.9}, "grace": {"base": 7, "growth": 0.9}, "cognition": {"base": 3, "growth": 0.9}, "insight": {"base": 3, "growth": 0.9}, "essence": {"base": 3, "growth": 0.9}, "durability": {"base": 7, "growth": 0.9}},
     "drops": [("drake_scale", 0.55), ("sulphur_crystal", 0.6), ("skillbook_ember_lash", 0.04)]},
    {"id": "magma_slime",       "name": "Magma Slime",       "biome": "lava_caves",    "hp": 62,
     "stats": {"might": {"base": 12, "growth": 0.9}, "grace": {"base": 6, "growth": 0.9}, "cognition": {"base": 3, "growth": 0.9}, "insight": {"base": 3, "growth": 0.9}, "essence": {"base": 2, "growth": 0.9}, "durability": {"base": 6, "growth": 0.9}},
     "drops": [("slime_ichor", 0.7), ("obsidian_chunk", 0.4)]},
    # basalt_steppe
    {"id": "steppe_raptor",     "name": "Steppe Raptor",     "biome": "basalt_steppe", "hp": 58,
     "stats": {"might": {"base": 12, "growth": 0.9}, "grace": {"base": 6, "growth": 0.9}, "cognition": {"base": 3, "growth": 0.9}, "insight": {"base": 3, "growth": 0.9}, "essence": {"base": 2, "growth": 0.9}, "durability": {"base": 6, "growth": 0.9}},
     "drops": [("basalt_shard", 0.5), ("wolf_fang", 0.4), ("ashplate", 0.05)]},
    {"id": "orc_warhound",      "name": "Orc Warhound",      "biome": "basalt_steppe", "hp": 72,
     "stats": {"might": {"base": 14, "growth": 0.9}, "grace": {"base": 7, "growth": 0.9}, "cognition": {"base": 3, "growth": 0.9}, "insight": {"base": 3, "growth": 0.9}, "essence": {"base": 2, "growth": 0.9}, "durability": {"base": 7, "growth": 0.9}},
     "drops": [("orc_tooth", 0.5), ("boar_hide", 0.5), ("iron_ore", 0.4)]},
    # obsidian_pits
    {"id": "obsidian_wraith",   "name": "Obsidian Wraith",   "biome": "obsidian_pits", "hp": 74,
     "stats": {"might": {"base": 16, "growth": 0.9}, "grace": {"base": 8, "growth": 0.9}, "cognition": {"base": 4, "growth": 0.9}, "insight": {"base": 4, "growth": 0.9}, "essence": {"base": 3, "growth": 0.9}, "durability": {"base": 8, "growth": 0.9}},
     "drops": [("wraith_essence", 0.6), ("obsidian_chunk", 0.6), ("relic_shard", 0.2)]},
    {"id": "ash_kobold",        "name": "Ash Kobold",        "biome": "obsidian_pits", "hp": 60,
     "stats": {"might": {"base": 12, "growth": 0.9}, "grace": {"base": 6, "growth": 0.9}, "cognition": {"base": 3, "growth": 0.9}, "insight": {"base": 3, "growth": 0.9}, "essence": {"base": 2, "growth": 0.9}, "durability": {"base": 6, "growth": 0.9}},
     "drops": [("coin_purse", 0.6), ("sulphur_crystal", 0.4)]},

    # ================ NYXMOOR (Lv 15+) ================
    # bogland
    {"id": "bog_hag",           "name": "Bog Hag",           "biome": "bogland",       "hp": 100,
     "stats": {"might": {"base": 20, "growth": 0.9}, "grace": {"base": 10, "growth": 0.9}, "cognition": {"base": 5, "growth": 0.9}, "insight": {"base": 5, "growth": 0.9}, "essence": {"base": 4, "growth": 0.9}, "durability": {"base": 10, "growth": 0.9}},
     "drops": [("hag_hair", 0.55), ("hex_moss", 0.6), ("skillbook_wraith_ward", 0.05)]},
    {"id": "reed_stalker",      "name": "Reed Stalker",      "biome": "bogland",       "hp": 92,
     "stats": {"might": {"base": 18, "growth": 0.9}, "grace": {"base": 9, "growth": 0.9}, "cognition": {"base": 4, "growth": 0.9}, "insight": {"base": 4, "growth": 0.9}, "essence": {"base": 3, "growth": 0.9}, "durability": {"base": 9, "growth": 0.9}},
     "drops": [("black_reed", 0.7), ("serpent_scale", 0.4)]},
    # cursed_ruins
    {"id": "cursed_knight",     "name": "Cursed Knight",     "biome": "cursed_ruins",  "hp": 118,
     "stats": {"might": {"base": 22, "growth": 0.9}, "grace": {"base": 11, "growth": 0.9}, "cognition": {"base": 5, "growth": 0.9}, "insight": {"base": 5, "growth": 0.9}, "essence": {"base": 4, "growth": 0.9}, "durability": {"base": 11, "growth": 0.9}},
     "drops": [("cursed_stone", 0.55), ("ghost_iron", 0.35), ("cursed_blade", 0.08)]},
    {"id": "wraith_watcher",    "name": "Wraith Watcher",    "biome": "cursed_ruins",  "hp": 98,
     "stats": {"might": {"base": 19, "growth": 0.9}, "grace": {"base": 9, "growth": 0.9}, "cognition": {"base": 4, "growth": 0.9}, "insight": {"base": 4, "growth": 0.9}, "essence": {"base": 3, "growth": 0.9}, "durability": {"base": 9, "growth": 0.9}},
     "drops": [("wraith_lantern", 0.5), ("wraith_essence", 0.5)]},
    # deadwood
    {"id": "dread_treant",      "name": "Dread Treant",      "biome": "deadwood",      "hp": 130,
     "stats": {"might": {"base": 21, "growth": 0.9}, "grace": {"base": 10, "growth": 0.9}, "cognition": {"base": 5, "growth": 0.9}, "insight": {"base": 5, "growth": 0.9}, "essence": {"base": 4, "growth": 0.9}, "durability": {"base": 10, "growth": 0.9}},
     "drops": [("oak_log", 0.8), ("hex_moss", 0.6), ("mourncloak", 0.06)]},
    {"id": "black_wolf",        "name": "Black Wolf",        "biome": "deadwood",      "hp": 88,
     "stats": {"might": {"base": 18, "growth": 0.9}, "grace": {"base": 9, "growth": 0.9}, "cognition": {"base": 4, "growth": 0.9}, "insight": {"base": 4, "growth": 0.9}, "essence": {"base": 3, "growth": 0.9}, "durability": {"base": 9, "growth": 0.9}},
     "drops": [("wolf_pelt", 0.8), ("wolf_fang", 0.5)]},
    # ghost_road
    {"id": "specter_rider",     "name": "Specter Rider",     "biome": "ghost_road",    "hp": 120,
     "stats": {"might": {"base": 23, "growth": 0.9}, "grace": {"base": 11, "growth": 0.9}, "cognition": {"base": 5, "growth": 0.9}, "insight": {"base": 5, "growth": 0.9}, "essence": {"base": 4, "growth": 0.9}, "durability": {"base": 11, "growth": 0.9}},
     "drops": [("wraith_essence", 0.6), ("cursed_stone", 0.5), ("demon_ash", 0.4)]},
    {"id": "chain_wraith",      "name": "Chain Wraith",      "biome": "ghost_road",    "hp": 105,
     "stats": {"might": {"base": 20, "growth": 0.9}, "grace": {"base": 10, "growth": 0.9}, "cognition": {"base": 5, "growth": 0.9}, "insight": {"base": 5, "growth": 0.9}, "essence": {"base": 4, "growth": 0.9}, "durability": {"base": 10, "growth": 0.9}},
     "drops": [("wraith_lantern", 0.55), ("relic_shard", 0.35)]},

    # ================ FROSTHELM (Lv 22+) ================
    # frozen_peaks
    {"id": "yeti_prowler",      "name": "Yeti Prowler",      "biome": "frozen_peaks",  "hp": 145,
     "stats": {"might": {"base": 26, "growth": 0.9}, "grace": {"base": 13, "growth": 0.9}, "cognition": {"base": 6, "growth": 0.9}, "insight": {"base": 6, "growth": 0.9}, "essence": {"base": 5, "growth": 0.9}, "durability": {"base": 13, "growth": 0.9}},
     "drops": [("yeti_pelt", 0.6), ("frost_root", 0.5)]},
    {"id": "sky_falcon",        "name": "Sky Falcon",        "biome": "frozen_peaks",  "hp": 128,
     "stats": {"might": {"base": 24, "growth": 0.9}, "grace": {"base": 12, "growth": 0.9}, "cognition": {"base": 6, "growth": 0.9}, "insight": {"base": 6, "growth": 0.9}, "essence": {"base": 4, "growth": 0.9}, "durability": {"base": 12, "growth": 0.9}},
     "drops": [("silver_vein", 0.5), ("griffon_feather", 0.15)]},
    # glacier
    {"id": "frost_wyrm_kin",    "name": "Frost Wyrm Kin",    "biome": "glacier",       "hp": 175,
     "stats": {"might": {"base": 30, "growth": 0.9}, "grace": {"base": 15, "growth": 0.9}, "cognition": {"base": 7, "growth": 0.9}, "insight": {"base": 7, "growth": 0.9}, "essence": {"base": 6, "growth": 0.9}, "durability": {"base": 15, "growth": 0.9}},
     "drops": [("wyrm_scale", 0.65), ("cold_iron", 0.4), ("skillbook_frost_edge", 0.05)]},
    {"id": "ice_wraith",        "name": "Ice Wraith",        "biome": "glacier",       "hp": 152,
     "stats": {"might": {"base": 27, "growth": 0.9}, "grace": {"base": 13, "growth": 0.9}, "cognition": {"base": 6, "growth": 0.9}, "insight": {"base": 6, "growth": 0.9}, "essence": {"base": 5, "growth": 0.9}, "durability": {"base": 13, "growth": 0.9}},
     "drops": [("glacier_shard", 0.65), ("wraith_essence", 0.35)]},
    # tundra
    {"id": "tundra_mammoth",    "name": "Tundra Mammoth",    "biome": "tundra",        "hp": 200,
     "stats": {"might": {"base": 32, "growth": 0.9}, "grace": {"base": 16, "growth": 0.9}, "cognition": {"base": 8, "growth": 0.9}, "insight": {"base": 8, "growth": 0.9}, "essence": {"base": 6, "growth": 0.9}, "durability": {"base": 16, "growth": 0.9}},
     "drops": [("mammoth_tusk", 0.7), ("boar_hide", 0.8), ("jahra_hauberk", 0.05)]},
    {"id": "snow_wolf_pack",    "name": "Snow Wolf",         "biome": "tundra",        "hp": 132,
     "stats": {"might": {"base": 25, "growth": 0.9}, "grace": {"base": 12, "growth": 0.9}, "cognition": {"base": 6, "growth": 0.9}, "insight": {"base": 6, "growth": 0.9}, "essence": {"base": 5, "growth": 0.9}, "durability": {"base": 12, "growth": 0.9}},
     "drops": [("wolf_pelt", 0.9), ("wolf_fang", 0.6), ("frost_root", 0.4)]},
    # ice_caverns
    {"id": "cavern_troll",      "name": "Cavern Troll",      "biome": "ice_caverns",   "hp": 190,
     "stats": {"might": {"base": 31, "growth": 0.9}, "grace": {"base": 15, "growth": 0.9}, "cognition": {"base": 7, "growth": 0.9}, "insight": {"base": 7, "growth": 0.9}, "essence": {"base": 6, "growth": 0.9}, "durability": {"base": 15, "growth": 0.9}},
     "drops": [("cold_iron", 0.6), ("glacier_shard", 0.5), ("cold_iron_spear", 0.08)]},
    {"id": "crystal_lurker",    "name": "Crystal Lurker",    "biome": "ice_caverns",   "hp": 148,
     "stats": {"might": {"base": 26, "growth": 0.9}, "grace": {"base": 13, "growth": 0.9}, "cognition": {"base": 6, "growth": 0.9}, "insight": {"base": 6, "growth": 0.9}, "essence": {"base": 5, "growth": 0.9}, "durability": {"base": 13, "growth": 0.9}},
     "drops": [("silver_vein", 0.6), ("glacier_shard", 0.5)]},

    # ================ ZEPHYRIA (Lv 30+) ================
    # sky_isles
    {"id": "sky_serpent",       "name": "Sky Serpent",       "biome": "sky_isles",     "hp": 210,
     "stats": {"might": {"base": 35, "growth": 0.9}, "grace": {"base": 17, "growth": 0.9}, "cognition": {"base": 8, "growth": 0.9}, "insight": {"base": 8, "growth": 0.9}, "essence": {"base": 7, "growth": 0.9}, "durability": {"base": 17, "growth": 0.9}},
     "drops": [("sky_serpent_hide", 0.6), ("sky_iron", 0.5), ("storm_bow", 0.06)]},
    {"id": "wind_rider",        "name": "Wind Rider",        "biome": "sky_isles",     "hp": 190,
     "stats": {"might": {"base": 32, "growth": 0.9}, "grace": {"base": 16, "growth": 0.9}, "cognition": {"base": 8, "growth": 0.9}, "insight": {"base": 8, "growth": 0.9}, "essence": {"base": 6, "growth": 0.9}, "durability": {"base": 16, "growth": 0.9}},
     "drops": [("cloud_silk", 0.55), ("silverleaf", 0.5)]},
    # cloud_forest
    {"id": "griffon",           "name": "Griffon",           "biome": "cloud_forest",  "hp": 235,
     "stats": {"might": {"base": 38, "growth": 0.9}, "grace": {"base": 19, "growth": 0.9}, "cognition": {"base": 9, "growth": 0.9}, "insight": {"base": 9, "growth": 0.9}, "essence": {"base": 7, "growth": 0.9}, "durability": {"base": 19, "growth": 0.9}},
     "drops": [("griffon_feather", 0.7), ("wolf_pelt", 0.4), ("skillbook_wind_step", 0.04)]},
    {"id": "silverleaf_dryad",  "name": "Silverleaf Dryad",  "biome": "cloud_forest",  "hp": 200,
     "stats": {"might": {"base": 33, "growth": 0.9}, "grace": {"base": 16, "growth": 0.9}, "cognition": {"base": 8, "growth": 0.9}, "insight": {"base": 8, "growth": 0.9}, "essence": {"base": 6, "growth": 0.9}, "durability": {"base": 16, "growth": 0.9}},
     "drops": [("silverleaf", 0.75), ("wild_herb", 0.5)]},
    # storm_plateau
    {"id": "storm_titan_shard", "name": "Storm Titan Shard", "biome": "storm_plateau", "hp": 260,
     "stats": {"might": {"base": 40, "growth": 0.9}, "grace": {"base": 20, "growth": 0.9}, "cognition": {"base": 10, "growth": 0.9}, "insight": {"base": 10, "growth": 0.9}, "essence": {"base": 8, "growth": 0.9}, "durability": {"base": 20, "growth": 0.9}},
     "drops": [("storm_glass", 0.65), ("star_shard", 0.25), ("sky_mantle", 0.06)]},
    {"id": "sky_kobold",        "name": "Sky Kobold",        "biome": "storm_plateau", "hp": 175,
     "stats": {"might": {"base": 30, "growth": 0.9}, "grace": {"base": 15, "growth": 0.9}, "cognition": {"base": 7, "growth": 0.9}, "insight": {"base": 7, "growth": 0.9}, "essence": {"base": 6, "growth": 0.9}, "durability": {"base": 15, "growth": 0.9}},
     "drops": [("coin_purse", 0.7), ("sky_iron", 0.4)]},
    # celestial_ruins
    {"id": "star_wraith",       "name": "Star Wraith",       "biome": "celestial_ruins","hp": 250,
     "stats": {"might": {"base": 42, "growth": 0.9}, "grace": {"base": 21, "growth": 0.9}, "cognition": {"base": 10, "growth": 0.9}, "insight": {"base": 10, "growth": 0.9}, "essence": {"base": 8, "growth": 0.9}, "durability": {"base": 21, "growth": 0.9}},
     "drops": [("star_shard", 0.45), ("wraith_essence", 0.5), ("relic_shard", 0.5)]},
    {"id": "celestial_guardian","name":"Celestial Guardian", "biome": "celestial_ruins","hp": 240,
     "stats": {"might": {"base": 39, "growth": 0.9}, "grace": {"base": 19, "growth": 0.9}, "cognition": {"base": 9, "growth": 0.9}, "insight": {"base": 9, "growth": 0.9}, "essence": {"base": 7, "growth": 0.9}, "durability": {"base": 19, "growth": 0.9}},
     "drops": [("sky_iron", 0.65), ("skillbook_thornlash", 0.06)]},

    # ================ SABLEWASTE (Lv 38+) ================
    # dune_sea
    {"id": "dune_worm",         "name": "Dune Worm",         "biome": "dune_sea",      "hp": 280,
     "stats": {"might": {"base": 44, "growth": 0.9}, "grace": {"base": 22, "growth": 0.9}, "cognition": {"base": 11, "growth": 0.9}, "insight": {"base": 11, "growth": 0.9}, "essence": {"base": 8, "growth": 0.9}, "durability": {"base": 22, "growth": 0.9}},
     "drops": [("golden_sand", 0.9), ("scarab_shell", 0.4)]},
    {"id": "sand_djinn_lesser", "name": "Sand Djinn (Lesser)","biome":"dune_sea",     "hp": 300,
     "stats": {"might": {"base": 46, "growth": 0.9}, "grace": {"base": 23, "growth": 0.9}, "cognition": {"base": 11, "growth": 0.9}, "insight": {"base": 11, "growth": 0.9}, "essence": {"base": 9, "growth": 0.9}, "durability": {"base": 23, "growth": 0.9}},
     "drops": [("djinn_glass", 0.5), ("mirage_silk", 0.3), ("djinn_scimitar", 0.05)]},
    # oasis
    {"id": "oasis_serpent",     "name": "Oasis Serpent",     "biome": "oasis",         "hp": 258,
     "stats": {"might": {"base": 42, "growth": 0.9}, "grace": {"base": 21, "growth": 0.9}, "cognition": {"base": 10, "growth": 0.9}, "insight": {"base": 10, "growth": 0.9}, "essence": {"base": 8, "growth": 0.9}, "durability": {"base": 21, "growth": 0.9}},
     "drops": [("serpent_venom", 0.7), ("sun_bloom", 0.6), ("serpent_scale", 0.7)]},
    {"id": "mirage_wolf",       "name": "Mirage Wolf",       "biome": "oasis",         "hp": 240,
     "stats": {"might": {"base": 40, "growth": 0.9}, "grace": {"base": 20, "growth": 0.9}, "cognition": {"base": 10, "growth": 0.9}, "insight": {"base": 10, "growth": 0.9}, "essence": {"base": 8, "growth": 0.9}, "durability": {"base": 20, "growth": 0.9}},
     "drops": [("mirage_silk", 0.35), ("wolf_pelt", 0.7)]},
    # djinn_ruins
    {"id": "djinn_guardian",    "name": "Djinn Guardian",    "biome": "djinn_ruins",   "hp": 315,
     "stats": {"might": {"base": 48, "growth": 0.9}, "grace": {"base": 24, "growth": 0.9}, "cognition": {"base": 12, "growth": 0.9}, "insight": {"base": 12, "growth": 0.9}, "essence": {"base": 9, "growth": 0.9}, "durability": {"base": 24, "growth": 0.9}},
     "drops": [("djinn_glass", 0.65), ("djinn_bottle_shard", 0.1), ("sunveil_robe", 0.06)]},
    {"id": "sun_priest_wraith", "name": "Sun-Priest Wraith", "biome": "djinn_ruins",   "hp": 292,
     "stats": {"might": {"base": 45, "growth": 0.9}, "grace": {"base": 22, "growth": 0.9}, "cognition": {"base": 11, "growth": 0.9}, "insight": {"base": 11, "growth": 0.9}, "essence": {"base": 9, "growth": 0.9}, "durability": {"base": 22, "growth": 0.9}},
     "drops": [("sun_priest_seal", 0.35), ("wraith_essence", 0.5)]},
    # sunken_temple
    {"id": "temple_scarab",     "name": "Temple Scarab",     "biome": "sunken_temple", "hp": 268,
     "stats": {"might": {"base": 43, "growth": 0.9}, "grace": {"base": 21, "growth": 0.9}, "cognition": {"base": 10, "growth": 0.9}, "insight": {"base": 10, "growth": 0.9}, "essence": {"base": 8, "growth": 0.9}, "durability": {"base": 21, "growth": 0.9}},
     "drops": [("scarab_shell", 0.8), ("relic_shard", 0.4)]},
    {"id": "sand_ghast",        "name": "Sand Ghast",        "biome": "sunken_temple", "hp": 305,
     "stats": {"might": {"base": 47, "growth": 0.9}, "grace": {"base": 23, "growth": 0.9}, "cognition": {"base": 11, "growth": 0.9}, "insight": {"base": 11, "growth": 0.9}, "essence": {"base": 9, "growth": 0.9}, "durability": {"base": 23, "growth": 0.9}},
     "drops": [("ghast_dust", 0.7), ("sun_priest_seal", 0.3), ("skillbook_sunlance", 0.04)]},

    # ================ VERDANIA (Lv 45+) ================
    # rainforest
    {"id": "jungle_stalker",    "name": "Jungle Stalker",    "biome": "rainforest",    "hp": 335,
     "stats": {"might": {"base": 50, "growth": 0.9}, "grace": {"base": 25, "growth": 0.9}, "cognition": {"base": 12, "growth": 0.9}, "insight": {"base": 12, "growth": 0.9}, "essence": {"base": 10, "growth": 0.9}, "durability": {"base": 25, "growth": 0.9}},
     "drops": [("emerald_frond", 0.6), ("canopy_venom", 0.4), ("wolf_pelt", 0.5)]},
    {"id": "vine_serpent",      "name": "Vine Serpent",      "biome": "rainforest",    "hp": 348,
     "stats": {"might": {"base": 52, "growth": 0.9}, "grace": {"base": 26, "growth": 0.9}, "cognition": {"base": 13, "growth": 0.9}, "insight": {"base": 13, "growth": 0.9}, "essence": {"base": 10, "growth": 0.9}, "durability": {"base": 26, "growth": 0.9}},
     "drops": [("living_wood", 0.45), ("serpent_venom", 0.6), ("canopy_venom", 0.5)]},
    # canopy_boughs
    {"id": "canopy_wyrm",       "name": "Canopy Wyrm",       "biome": "canopy_boughs", "hp": 375,
     "stats": {"might": {"base": 55, "growth": 0.9}, "grace": {"base": 27, "growth": 0.9}, "cognition": {"base": 13, "growth": 0.9}, "insight": {"base": 13, "growth": 0.9}, "essence": {"base": 11, "growth": 0.9}, "durability": {"base": 27, "growth": 0.9}},
     "drops": [("living_wood", 0.6), ("sylvan_seed", 0.25), ("sylvan_glaive", 0.05)]},
    {"id": "sylvan_druid_lost", "name": "Lost Sylvan Druid", "biome": "canopy_boughs", "hp": 330,
     "stats": {"might": {"base": 50, "growth": 0.9}, "grace": {"base": 25, "growth": 0.9}, "cognition": {"base": 12, "growth": 0.9}, "insight": {"base": 12, "growth": 0.9}, "essence": {"base": 10, "growth": 0.9}, "durability": {"base": 25, "growth": 0.9}},
     "drops": [("emerald_frond", 0.7), ("sylvan_seed", 0.3), ("skillbook_thornlash", 0.08)]},
    # coral_reef
    {"id": "reef_shark",        "name": "Reef Shark",        "biome": "coral_reef",    "hp": 350,
     "stats": {"might": {"base": 53, "growth": 0.9}, "grace": {"base": 26, "growth": 0.9}, "cognition": {"base": 13, "growth": 0.9}, "insight": {"base": 13, "growth": 0.9}, "essence": {"base": 10, "growth": 0.9}, "durability": {"base": 26, "growth": 0.9}},
     "drops": [("abyss_coral", 0.55), ("pearl_shell", 0.6), ("serpent_scale", 0.4)]},
    {"id": "coral_construct",   "name": "Coral Construct",   "biome": "coral_reef",    "hp": 345,
     "stats": {"might": {"base": 51, "growth": 0.9}, "grace": {"base": 25, "growth": 0.9}, "cognition": {"base": 12, "growth": 0.9}, "insight": {"base": 12, "growth": 0.9}, "essence": {"base": 10, "growth": 0.9}, "durability": {"base": 25, "growth": 0.9}},
     "drops": [("abyss_coral", 0.7), ("pearl_shell", 0.5), ("coral_platemail", 0.05)]},
    # sunken_atlantyrion
    {"id": "kraken_spawn",      "name": "Kraken Spawn",      "biome": "sunken_atlantyrion","hp": 400,
     "stats": {"might": {"base": 58, "growth": 0.9}, "grace": {"base": 29, "growth": 0.9}, "cognition": {"base": 14, "growth": 0.9}, "insight": {"base": 14, "growth": 0.9}, "essence": {"base": 11, "growth": 0.9}, "durability": {"base": 29, "growth": 0.9}},
     "drops": [("kraken_ink", 0.55), ("abyss_coral", 0.55), ("skillbook_tidefury", 0.05)]},
    {"id": "tide_priest",       "name": "Tide-Priest",       "biome": "sunken_atlantyrion","hp": 372,
     "stats": {"might": {"base": 55, "growth": 0.9}, "grace": {"base": 27, "growth": 0.9}, "cognition": {"base": 13, "growth": 0.9}, "insight": {"base": 13, "growth": 0.9}, "essence": {"base": 11, "growth": 0.9}, "durability": {"base": 27, "growth": 0.9}},
     "drops": [("tide_priest_ring", 0.3), ("orb_fragment", 0.15), ("pearl_shell", 0.7)]},
]


# ============================================================
# BIOME ACTIONS — extends BIOME_ACTIONS dict
# ============================================================
EXTRA_BIOME_ACTIONS: dict[str, list[dict]] = {
    # -------- Vulkaros --------
    "ashlands": [
        {"id": "hunt",    "name": "Hunt",    "targets": ["ash_hound", "orc_grunt"]},
        {"id": "gather",  "name": "Gather",  "targets": ["ash_grass", "basalt_shard"]},
        {"id": "explore", "name": "Explore", "targets": []},
    ],
    "lava_caves": [
        {"id": "hunt",    "name": "Hunt",    "targets": ["fire_drake_whelp", "magma_slime"]},
        {"id": "gather",  "name": "Gather",  "targets": ["sulphur_crystal", "obsidian_chunk"]},
        {"id": "loot_ruins","name":"Delve Caves","targets": []},
    ],
    "basalt_steppe": [
        {"id": "hunt",    "name": "Hunt",    "targets": ["steppe_raptor", "orc_warhound"]},
        {"id": "gather",  "name": "Gather",  "targets": ["basalt_shard", "ash_grass"]},
        {"id": "explore", "name": "Explore", "targets": []},
    ],
    "obsidian_pits": [
        {"id": "loot_ruins","name":"Loot Pits","targets": []},
        {"id": "hunt",    "name": "Hunt",    "targets": ["obsidian_wraith", "ash_kobold"]},
        {"id": "gather",  "name": "Gather",  "targets": ["obsidian_chunk", "sulphur_crystal"]},
    ],
    # -------- Nyxmoor --------
    "bogland": [
        {"id": "hunt",    "name": "Hunt",    "targets": ["bog_hag", "reed_stalker"]},
        {"id": "gather",  "name": "Gather",  "targets": ["black_reed", "hex_moss"]},
        {"id": "fish",    "name": "Fish",    "targets": []},
    ],
    "cursed_ruins": [
        {"id": "loot_ruins","name":"Loot Ruins","targets": []},
        {"id": "hunt",    "name": "Hunt",    "targets": ["cursed_knight", "wraith_watcher"]},
        {"id": "gather",  "name": "Gather",  "targets": ["cursed_stone", "ghost_iron"]},
    ],
    "deadwood": [
        {"id": "hunt",    "name": "Hunt",    "targets": ["dread_treant", "black_wolf"]},
        {"id": "gather",  "name": "Gather",  "targets": ["black_reed", "hex_moss"]},
        {"id": "explore", "name": "Explore", "targets": []},
    ],
    "ghost_road": [
        {"id": "hunt",    "name": "Hunt",    "targets": ["specter_rider", "chain_wraith"]},
        {"id": "gather",  "name": "Gather",  "targets": ["cursed_stone", "ghost_iron"]},
        {"id": "explore", "name": "Explore", "targets": []},
    ],
    # -------- Frosthelm --------
    "frozen_peaks": [
        {"id": "hunt",    "name": "Hunt",    "targets": ["yeti_prowler", "sky_falcon"]},
        {"id": "gather",  "name": "Gather",  "targets": ["frost_root", "silver_vein"]},
        {"id": "explore", "name": "Explore", "targets": []},
    ],
    "glacier": [
        {"id": "hunt",    "name": "Hunt",    "targets": ["frost_wyrm_kin", "ice_wraith"]},
        {"id": "gather",  "name": "Gather",  "targets": ["glacier_shard", "cold_iron"]},
        {"id": "explore", "name": "Explore", "targets": []},
    ],
    "tundra": [
        {"id": "hunt",    "name": "Hunt",    "targets": ["tundra_mammoth", "snow_wolf_pack"]},
        {"id": "gather",  "name": "Gather",  "targets": ["frost_root"]},
        {"id": "explore", "name": "Explore", "targets": []},
    ],
    "ice_caverns": [
        {"id": "loot_ruins","name":"Delve Caverns","targets": []},
        {"id": "hunt",    "name": "Hunt",    "targets": ["cavern_troll", "crystal_lurker"]},
        {"id": "gather",  "name": "Gather",  "targets": ["glacier_shard", "silver_vein", "cold_iron"]},
    ],
    # -------- Zephyria --------
    "sky_isles": [
        {"id": "hunt",    "name": "Hunt",    "targets": ["sky_serpent", "wind_rider"]},
        {"id": "gather",  "name": "Gather",  "targets": ["silverleaf", "sky_iron"]},
        {"id": "explore", "name": "Explore", "targets": []},
    ],
    "cloud_forest": [
        {"id": "hunt",    "name": "Hunt",    "targets": ["griffon", "silverleaf_dryad"]},
        {"id": "gather",  "name": "Gather",  "targets": ["silverleaf", "cloud_silk"]},
        {"id": "explore", "name": "Explore", "targets": []},
    ],
    "storm_plateau": [
        {"id": "hunt",    "name": "Hunt",    "targets": ["storm_titan_shard", "sky_kobold"]},
        {"id": "gather",  "name": "Gather",  "targets": ["storm_glass"]},
        {"id": "explore", "name": "Explore", "targets": []},
    ],
    "celestial_ruins": [
        {"id": "loot_ruins","name":"Loot Ruins","targets": []},
        {"id": "hunt",    "name": "Hunt",    "targets": ["star_wraith", "celestial_guardian"]},
        {"id": "gather",  "name": "Gather",  "targets": ["storm_glass", "sky_iron"]},
    ],
    # -------- Sablewaste --------
    "dune_sea": [
        {"id": "hunt",    "name": "Hunt",    "targets": ["dune_worm", "sand_djinn_lesser"]},
        {"id": "gather",  "name": "Gather",  "targets": ["golden_sand"]},
        {"id": "explore", "name": "Explore", "targets": []},
    ],
    "oasis": [
        {"id": "hunt",    "name": "Hunt",    "targets": ["oasis_serpent", "mirage_wolf"]},
        {"id": "gather",  "name": "Gather",  "targets": ["sun_bloom"]},
        {"id": "fish",    "name": "Fish",    "targets": []},
    ],
    "djinn_ruins": [
        {"id": "loot_ruins","name":"Loot Ruins","targets": []},
        {"id": "hunt",    "name": "Hunt",    "targets": ["djinn_guardian", "sun_priest_wraith"]},
        {"id": "gather",  "name": "Gather",  "targets": ["djinn_glass", "golden_sand"]},
    ],
    "sunken_temple": [
        {"id": "loot_ruins","name":"Loot Temple","targets": []},
        {"id": "hunt",    "name": "Hunt",    "targets": ["temple_scarab", "sand_ghast"]},
        {"id": "gather",  "name": "Gather",  "targets": ["djinn_glass"]},
    ],
    # -------- Verdania --------
    "rainforest": [
        {"id": "hunt",    "name": "Hunt",    "targets": ["jungle_stalker", "vine_serpent"]},
        {"id": "gather",  "name": "Gather",  "targets": ["emerald_frond", "living_wood"]},
        {"id": "explore", "name": "Explore", "targets": []},
    ],
    "canopy_boughs": [
        {"id": "hunt",    "name": "Hunt",    "targets": ["canopy_wyrm", "sylvan_druid_lost"]},
        {"id": "gather",  "name": "Gather",  "targets": ["emerald_frond", "living_wood"]},
        {"id": "explore", "name": "Explore", "targets": []},
    ],
    "coral_reef": [
        {"id": "hunt",    "name": "Hunt",    "targets": ["reef_shark", "coral_construct"]},
        {"id": "gather",  "name": "Gather",  "targets": ["abyss_coral", "pearl_shell"]},
        {"id": "fish",    "name": "Fish",    "targets": []},
    ],
    "sunken_atlantyrion": [
        {"id": "loot_ruins","name":"Explore Atlantyrion","targets": []},
        {"id": "hunt",    "name": "Hunt",    "targets": ["kraken_spawn", "tide_priest"]},
        {"id": "gather",  "name": "Gather",  "targets": ["abyss_coral", "pearl_shell"]},
    ],
}


def extend_world_data(items_list: list[dict], monsters_list: list[dict],
                       biome_actions: dict, items_by_id: dict) -> None:
    """Merge extras into the base game_data structures. Idempotent by id."""
    existing_item_ids = {it["id"] for it in items_list}
    for it in EXTRA_ITEMS:
        if it["id"] not in existing_item_ids:
            items_list.append(it)
            items_by_id[it["id"]] = it

    existing_monster_ids = {m["id"] for m in monsters_list}
    for m in EXTRA_MONSTERS:
        if m["id"] not in existing_monster_ids:
            monsters_list.append(m)

    for biome_id, actions in EXTRA_BIOME_ACTIONS.items():
        # replace only if biome wasn't already populated (Aetheria wins)
        if biome_id not in biome_actions:
            biome_actions[biome_id] = actions
