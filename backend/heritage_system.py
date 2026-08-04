"""Erchis Heritage System — Continental Heritage Months.

Each of the 8 accessible continents gets a dedicated month celebrating its
culture, history, and specialties. During its month, that continent gets
gameplay bonuses, an exclusive heritage boss, daily quests, a vendor with
carry-over tokens, a ladder tab, and milestone rewards.

Tokens carry over year to year — no FOMO. Players who participate every
year accumulate enough for the most expensive rewards.

Calendar:
  Jan — Valeria      — Festival of the Oath
  Feb — Mushkara     — Chainbreaker's Month
  Mar — Concordia    — Mosaic Festival
  Apr — Khardrum     — Deepforge Jubilee
  May — Haya         — Celestial Accord
  Jun — Gennel       — Great Awakening
  Jul — Hylion       — Tidefall Celebration
  Aug — Daw'ul Talalu— Mystleaf Revel
  Sep — (break month, no heritage)
"""
from __future__ import annotations

from datetime import date


# ============================================================
# HERITAGE MONTHS — month number → continent config
# ============================================================
HERITAGE_MONTHS: dict[int, dict] = {
    1: {
        "continent": "valeria",
        "name": "Festival of the Oath",
        "theme": "Founding of the Human Empire, oaths and contracts, trade caravans",
        "desc": (
            "The oldest kingdoms of Erchis celebrate the founding oaths that "
            "built the Human Empire. Caravans roll across the Golden Plains, "
            "cathedral bells ring in Oathspire, and every promise kept strengthens "
            "the land. Heroes gather to honor the old vows — and break the ones "
            "that should never have been made."
        ),
        "decoration": "Imperial banners, oath stones, golden candles",
    },
    2: {
        "continent": "mushkara",
        "name": "Chainbreaker's Month",
        "theme": "Orc rebellion anniversary, demon-hunting, war games",
        "desc": (
            "The Orcs of Mushkara commemorate the breaking of their chains. "
            "War-camps echo with the songs of liberation, and the forges burn "
            "hot with remembrance. But the demons of Demonfall Crater stir in "
            "the shadows, testing whether the chains are truly broken."
        ),
        "decoration": "Broken chains on statues, war banners, bonfires",
    },
    3: {
        "continent": "concordia",
        "name": "Mosaic Festival",
        "theme": "Federation unity, diplomacy, multicultural trade",
        "desc": (
            "Concordia celebrates the mosaic of peoples who built the Federation. "
            "Embassies open their doors, markets overflow with goods from every "
            "continent, and diplomats trade favors as freely as coin. The Amber "
            "Vineyards flow with wine, and the Silverroad hums with caravans."
        ),
        "decoration": "Mosaic tiles, federation flags, flower garlands",
    },
    4: {
        "continent": "khardrum",
        "name": "Deepforge Jubilee",
        "theme": "Dwarven forging traditions, mining, Jahra reverence",
        "desc": (
            "The deep halls of Khardrum ring with hammer-song. The Deepforge "
            "Jubilee honors the master smiths who first worked Jahra ore, and "
            "the mountain itself is said to open its veins a little wider in "
            "celebration. Miners bring up treasures that the deep earth has "
            "been hoarding all year."
        ),
        "decoration": "Forge lights, Jahra crystal displays, dwarven runes",
    },
    5: {
        "continent": "haya",
        "name": "Celestial Accord",
        "theme": "Elven star/sun/moon worship, magic, healing",
        "desc": (
            "When the stars align over Haya's Starfall Cliffs, the Elves "
            "celebrate the Celestial Accord — the ancient pact between sun "
            "and moon. The Celestial Lake glows with impossible colors, and "
            "the forest itself seems to breathe with ancient power. Herbs "
            "grow richer, and the veil between worlds grows thin."
        ),
        "decoration": "Star lanterns, moon banners, glowing flowers",
    },
    6: {
        "continent": "gennel",
        "name": "Great Awakening",
        "theme": "Wildblood beast heritage, primal spirits, taming",
        "desc": (
            "The Wildbloods of Gennel celebrate the Great Awakening — the "
            "moment the desert first bloomed and the beasts came to life. "
            "Primal spirits walk the savannas, ancient dens stir with alpha "
            "power, and every beast in Gennel seems to remember the old songs "
            "that sang the sand into life."
        ),
        "decoration": "Beast totems, primal paintings, oasis flowers",
    },
    7: {
        "continent": "hylion",
        "name": "Tidefall Celebration",
        "theme": "Hyliondrian ocean culture, fishing, water alchemy",
        "desc": (
            "The coral cities of Hylion shimmer during the Tidefall Celebration. "
            "The great tides recede to reveal hidden treasures, and the deep "
            "trenches grow calm enough for even land-dwellers to explore. Sacred "
            "waters flow with healing power, and the leviathans of the abyss "
            "rise closer to the light than they dare any other time of year."
        ),
        "decoration": "Coral decorations, water fountains, shell banners",
    },
    8: {
        "continent": "daw_ul_talalu",
        "name": "Mystleaf Revel",
        "theme": "Sylvan forest magic, illusions, herbalism",
        "desc": (
            "The living forest of Daw'ul Talalu celebrates the Mystleaf Revel. "
            "The elder trees open their hidden paths, bioluminescent flora "
            "illuminates the night, and the Sylvans share secrets of herbalism "
            "and illusion that they guard jealously the rest of the year. The "
            "Thorn Guardian stirs in Elderroot Hollow, testing all who enter."
        ),
        "decoration": "Living wood archways, mist effects, bioluminescent lights",
    },
}

# Reverse lookup: continent → month
HERITAGE_MONTH_BY_CONTINENT: dict[str, int] = {
    v["continent"]: k for k, v in HERITAGE_MONTHS.items()
}


# ============================================================
# HERITAGE BOSSES — upgraded variants of existing continent bosses
# ============================================================
# Each heritage boss is a significantly stronger version of the base boss,
# with unique mechanics described in "mechanic" and exclusive heritage drops.
HERITAGE_BOSSES: dict[str, dict] = {
    "valeria": {
        "id": "heritage_oathbreaker",
        "name": "The Oathbreaker",
        "base_boss_id": "boss_ashen_lord",
        "biome": "ashen_border",
        "continent": "valeria",
        "hp": 800,
        "stats": {"might": {"base": 58, "growth": 1.0}, "grace": {"base": 29, "growth": 0.9}, "insight": {"base": 25, "growth": 0.9}, "essence": {"base": 20, "growth": 0.8}, "durability": {"base": 29, "growth": 1.0}, "cognition": {"base": 18, "growth": 0.8}},
        "is_boss": True,
        "is_heritage_boss": True,
        "mechanic": "Summons oath-sworn undead adds; must break oath totems before boss is vulnerable",
        "drops": [
            ("oath_seal_part", 0.60),
            ("greater_healing_potion", 1.0),
            ("relic_shard", 0.9),
            ("heritage_valeria_token", 1.0),
        ],
        "heritage_token_count": 5,
    },
    "mushkara": {
        "id": "heritage_demon_reborn",
        "name": "The Demon Reborn",
        "base_boss_id": "boss_demon_warleader",
        "biome": "demonfall_crater",
        "continent": "mushkara",
        "hp": 1100,
        "stats": {"might": {"base": 78, "growth": 1.0}, "grace": {"base": 39, "growth": 0.9}, "insight": {"base": 33, "growth": 0.9}, "essence": {"base": 27, "growth": 0.8}, "durability": {"base": 39, "growth": 1.0}, "cognition": {"base": 24, "growth": 0.8}},
        "is_boss": True,
        "is_heritage_boss": True,
        "mechanic": "Enrage phases — every 25% HP lost, gains a new demon ability",
        "drops": [
            ("chainbreaker_fragment_part", 0.60),
            ("demonbone_part", 0.9),
            ("jahra_ingot", 0.7),
            ("heritage_mushkara_token", 1.0),
        ],
        "heritage_token_count": 5,
    },
    "concordia": {
        "id": "heritage_fallen_ambassador",
        "name": "The Fallen Ambassador",
        "base_boss_id": "boss_amber_diplomat",
        "biome": "diplomats_highlands",
        "continent": "concordia",
        "hp": 1400,
        "stats": {"might": {"base": 94, "growth": 1.0}, "grace": {"base": 47, "growth": 0.9}, "insight": {"base": 40, "growth": 0.9}, "essence": {"base": 32, "growth": 0.8}, "durability": {"base": 47, "growth": 1.0}, "cognition": {"base": 29, "growth": 0.8}},
        "is_boss": True,
        "is_heritage_boss": True,
        "mechanic": "Diplomatic mechanic — must weaken boss through dialogue actions before full combat",
        "drops": [
            ("federation_seal_part", 0.60),
            ("prism_gem_part", 0.9),
            ("orb_fragment", 0.7),
            ("heritage_concordia_token", 1.0),
        ],
        "heritage_token_count": 5,
    },
    "khardrum": {
        "id": "heritage_forge_titan",
        "name": "The Forge Titan",
        "base_boss_id": "boss_forge_golem",
        "biome": "deep_forges",
        "continent": "khardrum",
        "hp": 1700,
        "stats": {"might": {"base": 110, "growth": 1.0}, "grace": {"base": 55, "growth": 0.9}, "insight": {"base": 47, "growth": 0.9}, "essence": {"base": 38, "growth": 0.8}, "durability": {"base": 55, "growth": 1.0}, "cognition": {"base": 34, "growth": 0.8}},
        "is_boss": True,
        "is_heritage_boss": True,
        "mechanic": "Heat mechanic — boss room fills with lava; manage positioning or take burn damage",
        "drops": [
            ("living_stone_heart_part", 0.60),
            ("jahra_fragment_part", 0.9),
            ("jahra_ingot", 0.8),
            ("heritage_khardrum_token", 1.0),
        ],
        "heritage_token_count": 5,
    },
    "haya": {
        "id": "heritage_eclipse_avatar",
        "name": "The Eclipse Avatar",
        "base_boss_id": "boss_starfall_avatar",
        "biome": "starfall_cliffs",
        "continent": "haya",
        "hp": 2100,
        "stats": {"might": {"base": 127, "growth": 1.0}, "grace": {"base": 64, "growth": 0.9}, "insight": {"base": 54, "growth": 0.9}, "essence": {"base": 44, "growth": 0.8}, "durability": {"base": 64, "growth": 1.0}, "cognition": {"base": 39, "growth": 0.8}},
        "is_boss": True,
        "is_heritage_boss": True,
        "mechanic": "Day/night cycle — boss changes abilities based on in-game time of day",
        "drops": [
            ("star_shard_part", 0.60),
            ("celestial_thread_part", 0.9),
            ("skillbook_wind_step", 0.25),
            ("heritage_haya_token", 1.0),
        ],
        "heritage_token_count": 5,
    },
    "gennel": {
        "id": "heritage_primal_sovereign",
        "name": "The Primal Sovereign",
        "base_boss_id": "boss_alpha_king",
        "biome": "ancient_den",
        "continent": "gennel",
        "hp": 2500,
        "stats": {"might": {"base": 146, "growth": 1.0}, "grace": {"base": 73, "growth": 0.9}, "insight": {"base": 62, "growth": 0.9}, "essence": {"base": 50, "growth": 0.8}, "durability": {"base": 73, "growth": 1.0}, "cognition": {"base": 45, "growth": 0.8}},
        "is_boss": True,
        "is_heritage_boss": True,
        "mechanic": "Beast taming — boss summons packs that can be turned against it with the right actions",
        "drops": [
            ("primal_blood_crystal_part", 0.60),
            ("alpha_fang_part", 0.9),
            ("skillbook_thornlash", 0.25),
            ("heritage_gennel_token", 1.0),
        ],
        "heritage_token_count": 5,
    },
    "hylion": {
        "id": "heritage_abyssal_maw",
        "name": "The Abyssal Maw",
        "base_boss_id": "boss_leviathan",
        "biome": "abyssal_trench",
        "continent": "hylion",
        "hp": 2900,
        "stats": {"might": {"base": 164, "growth": 1.0}, "grace": {"base": 82, "growth": 0.9}, "insight": {"base": 69, "growth": 0.9}, "essence": {"base": 57, "growth": 0.8}, "durability": {"base": 82, "growth": 1.0}, "cognition": {"base": 50, "growth": 0.8}},
        "is_boss": True,
        "is_heritage_boss": True,
        "mechanic": "Water mechanic — drowning risk; must manage air supply during the fight",
        "drops": [
            ("leviathan_scale_part", 0.60),
            ("divine_water_part", 0.9),
            ("skillbook_tidefury", 0.25),
            ("heritage_hylion_token", 1.0),
        ],
        "heritage_token_count": 5,
    },
    "daw_ul_talalu": {
        "id": "heritage_dream_eater",
        "name": "The Dream Eater",
        "base_boss_id": "boss_thorn_guardian",
        "biome": "elderroot_hollow",
        "continent": "daw_ul_talalu",
        "hp": 3400,
        "stats": {"might": {"base": 182, "growth": 1.0}, "grace": {"base": 91, "growth": 0.9}, "insight": {"base": 77, "growth": 0.9}, "essence": {"base": 63, "growth": 0.8}, "durability": {"base": 91, "growth": 1.0}, "cognition": {"base": 56, "growth": 0.8}},
        "is_boss": True,
        "is_heritage_boss": True,
        "mechanic": "Illusion — boss creates fake copies; must find the real one to deal damage",
        "drops": [
            ("thorn_guardian_core_part", 0.60),
            ("living_wood_part", 0.9),
            ("skillbook_sunlance", 0.25),
            ("heritage_daw_ul_talalu_token", 1.0),
        ],
        "heritage_token_count": 5,
    },
}


# ============================================================
# HERITAGE BONUSES — per-continent bonuses active during heritage month
# ============================================================
HERITAGE_BONUSES: dict[str, dict] = {
    "valeria": {
        "gather_yield_mult": 1.50,
        "combat_xp_mult": 1.25,
        "craft_success_bonus": 0.15,
        "market_discount": 0.10,
        "free_travel": True,
        "desc": "+50% gather yield, +25% combat XP, +15% craft success, 10% market discount, free travel",
    },
    "mushkara": {
        "gather_yield_mult": 1.50,
        "combat_xp_mult": 1.25,
        "craft_success_bonus": 0.15,
        "market_discount": 0.10,
        "free_travel": True,
        "desc": "+50% gather yield, +25% combat XP, +15% craft success, 10% market discount, free travel",
    },
    "concordia": {
        "gather_yield_mult": 1.50,
        "combat_xp_mult": 1.25,
        "craft_success_bonus": 0.15,
        "market_discount": 0.10,
        "free_travel": True,
        "desc": "+50% gather yield, +25% combat XP, +15% craft success, 10% market discount, free travel",
    },
    "khardrum": {
        "gather_yield_mult": 1.50,
        "combat_xp_mult": 1.25,
        "craft_success_bonus": 0.15,
        "market_discount": 0.10,
        "free_travel": True,
        "desc": "+50% gather yield, +25% combat XP, +15% craft success, 10% market discount, free travel",
    },
    "haya": {
        "gather_yield_mult": 1.50,
        "combat_xp_mult": 1.25,
        "craft_success_bonus": 0.15,
        "market_discount": 0.10,
        "free_travel": True,
        "desc": "+50% gather yield, +25% combat XP, +15% craft success, 10% market discount, free travel",
    },
    "gennel": {
        "gather_yield_mult": 1.50,
        "combat_xp_mult": 1.25,
        "craft_success_bonus": 0.15,
        "market_discount": 0.10,
        "free_travel": True,
        "desc": "+50% gather yield, +25% combat XP, +15% craft success, 10% market discount, free travel",
    },
    "hylion": {
        "gather_yield_mult": 1.50,
        "combat_xp_mult": 1.25,
        "craft_success_bonus": 0.15,
        "market_discount": 0.10,
        "free_travel": True,
        "desc": "+50% gather yield, +25% combat XP, +15% craft success, 10% market discount, free travel",
    },
    "daw_ul_talalu": {
        "gather_yield_mult": 1.50,
        "combat_xp_mult": 1.25,
        "craft_success_bonus": 0.15,
        "market_discount": 0.10,
        "free_travel": True,
        "desc": "+50% gather yield, +25% combat XP, +15% craft success, 10% market discount, free travel",
    },
}


# ============================================================
# HERITAGE DAILY QUESTS — 3 per day per continent
# ============================================================
# Each quest has: id_suffix, name, brief, kind (kill/gather/craft),
# target (monster_id / biome / recipe_category), count, token_reward
HERITAGE_DAILY_QUESTS: dict[str, list[dict]] = {
    "valeria": [
        {
            "id_suffix": "oathkeeper_round",
            "name": "Oathkeeper's Round",
            "brief": "Patrol Valeria's biomes and defeat 8 monsters threatening the homeland.",
            "kind": "kill",
            "biome_filter": ["golden_plains", "crownwood_forest", "imperial_riverlands", "ashen_border"],
            "count": 8,
            "token_reward": 3,
        },
        {
            "id_suffix": "caravan_guard",
            "name": "Caravan Guard Duty",
            "brief": "Gather 10 resources in Valeria to supply the festival caravans.",
            "kind": "gather",
            "biome_filter": ["golden_plains", "crownwood_forest", "imperial_riverlands", "ashen_border"],
            "count": 10,
            "token_reward": 3,
        },
        {
            "id_suffix": "imperial_kitchen",
            "name": "Imperial Kitchen",
            "brief": "Craft 3 items using Valeria's resources for the festival feast.",
            "kind": "craft",
            "count": 3,
            "token_reward": 3,
        },
    ],
    "mushkara": [
        {
            "id_suffix": "war_patrol",
            "name": "War Patrol",
            "brief": "Slay 8 monsters in Mushkara's harsh biomes to prove your strength.",
            "kind": "kill",
            "biome_filter": ["bloodwind_plains", "red_steppe", "iron_scar", "ash_barrens", "demonfall_crater"],
            "count": 8,
            "token_reward": 3,
        },
        {
            "id_suffix": "war_supply_haul",
            "name": "War Supply Haul",
            "brief": "Gather 10 resources in Mushkara to supply the war-camps.",
            "kind": "gather",
            "biome_filter": ["bloodwind_plains", "red_steppe", "iron_scar", "ash_barrens", "demonfall_crater"],
            "count": 10,
            "token_reward": 3,
        },
        {
            "id_suffix": "forge_tribute",
            "name": "Forge Tribute",
            "brief": "Craft 3 items in Mushkara to honor the chainbreaking forges.",
            "kind": "craft",
            "count": 3,
            "token_reward": 3,
        },
    ],
    "concordia": [
        {
            "id_suffix": "diplomatic Escort",
            "name": "Diplomatic Escort",
            "brief": "Defeat 8 threats along Concordia's trade roads to keep the peace.",
            "kind": "kill",
            "biome_filter": ["trade_road_outpost", "mosaic_coast", "amber_vineyards", "silverroad", "diplomats_highlands"],
            "count": 8,
            "token_reward": 3,
        },
        {
            "id_suffix": "festival_goods",
            "name": "Festival Goods",
            "brief": "Gather 10 resources in Concordia for the Mosaic Festival markets.",
            "kind": "gather",
            "biome_filter": ["trade_road_outpost", "mosaic_coast", "amber_vineyards", "silverroad", "diplomats_highlands"],
            "count": 10,
            "token_reward": 3,
        },
        {
            "id_suffix": "embassy_craft",
            "name": "Embassy Craft",
            "brief": "Craft 3 items in Concordia as gifts for the festival embassies.",
            "kind": "craft",
            "count": 3,
            "token_reward": 3,
        },
    ],
    "khardrum": [
        {
            "id_suffix": "deep_patrol",
            "name": "Deep Patrol",
            "brief": "Slay 8 creatures in Khardrum's deep halls to secure the mines.",
            "kind": "kill",
            "biome_filter": ["stone_ridge", "granite_foothills", "ember_mines", "crystal_caverns", "deep_forges"],
            "count": 8,
            "token_reward": 3,
        },
        {
            "id_suffix": "ore_haul",
            "name": "Ore Haul",
            "brief": "Mine 10 ore nodes in Khardrum for the Deepforge Jubilee.",
            "kind": "gather",
            "biome_filter": ["stone_ridge", "granite_foothills", "ember_mines", "crystal_caverns", "deep_forges"],
            "count": 10,
            "token_reward": 3,
        },
        {
            "id_suffix": "forge_test",
            "name": "Forge Test",
            "brief": "Craft 3 weapons or armor pieces at a Khardrum forge.",
            "kind": "craft",
            "count": 3,
            "token_reward": 3,
        },
    ],
    "haya": [
        {
            "id_suffix": "celestial_hunt",
            "name": "Celestial Hunt",
            "brief": "Defeat 8 magical creatures in Haya's enchanted biomes.",
            "kind": "kill",
            "biome_filter": ["verdant_edge", "sunlit_canopy", "moonveil_woods", "celestial_lake", "starfall_cliffs"],
            "count": 8,
            "token_reward": 3,
        },
        {
            "id_suffix": "starlight_gather",
            "name": "Starlight Gathering",
            "brief": "Gather 10 herbs or crystals in Haya during the Celestial Accord.",
            "kind": "gather",
            "biome_filter": ["verdant_edge", "sunlit_canopy", "moonveil_woods", "celestial_lake", "starfall_cliffs"],
            "count": 10,
            "token_reward": 3,
        },
        {
            "id_suffix": "celestial_craft",
            "name": "Celestial Craft",
            "brief": "Craft 3 enchanted items in Haya to honor the sun and moon.",
            "kind": "craft",
            "count": 3,
            "token_reward": 3,
        },
    ],
    "gennel": [
        {
            "id_suffix": "primal_hunt",
            "name": "Primal Hunt",
            "brief": "Slay 8 beasts in Gennel's wild biomes during the Great Awakening.",
            "kind": "kill",
            "biome_filter": ["oasis_outskirts", "blooming_desert", "beastwood", "roaring_savanna", "ancient_den"],
            "count": 8,
            "token_reward": 3,
        },
        {
            "id_suffix": "spirit_gather",
            "name": "Spirit Gathering",
            "brief": "Gather 10 resources in Gennel's awakened lands.",
            "kind": "gather",
            "biome_filter": ["oasis_outskirts", "blooming_desert", "beastwood", "roaring_savanna", "ancient_den"],
            "count": 10,
            "token_reward": 3,
        },
        {
            "id_suffix": "primal_craft",
            "name": "Primal Craft",
            "brief": "Craft 3 leather or beast-themed items in Gennel.",
            "kind": "craft",
            "count": 3,
            "token_reward": 3,
        },
    ],
    "hylion": [
        {
            "id_suffix": "tide_defense",
            "name": "Tide Defense",
            "brief": "Defeat 8 sea creatures threatening Hylion's coral cities.",
            "kind": "kill",
            "biome_filter": ["tide_pools", "coral_gardens", "kelp_forest", "storm_reefs", "abyssal_trench"],
            "count": 8,
            "token_reward": 3,
        },
        {
            "id_suffix": "tidefall_gather",
            "name": "Tidefall Gathering",
            "brief": "Gather 10 fish or pearls in Hylion during the Tidefall Celebration.",
            "kind": "gather",
            "biome_filter": ["tide_pools", "coral_gardens", "kelp_forest", "storm_reefs", "abyssal_trench"],
            "count": 10,
            "token_reward": 3,
        },
        {
            "id_suffix": "water_alchemy",
            "name": "Water Alchemy",
            "brief": "Craft 3 potions or water-alchemy items in Hylion.",
            "kind": "craft",
            "count": 3,
            "token_reward": 3,
        },
    ],
    "daw_ul_talalu": [
        {
            "id_suffix": "mist_patrol",
            "name": "Mist Patrol",
            "brief": "Defeat 8 illusions and creatures in Daw'ul Talalu's misty biomes.",
            "kind": "kill",
            "biome_filter": ["misty_thicket", "mistwood", "thorn_labyrinth", "lumina_grove", "elderroot_hollow"],
            "count": 8,
            "token_reward": 3,
        },
        {
            "id_suffix": "mystleaf_gather",
            "name": "Mystleaf Gathering",
            "brief": "Gather 10 rare herbs or woods in Daw'ul Talalu's living forest.",
            "kind": "gather",
            "biome_filter": ["misty_thicket", "mistwood", "thorn_labyrinth", "lumina_grove", "elderroot_hollow"],
            "count": 10,
            "token_reward": 3,
        },
        {
            "id_suffix": "sylvan_craft",
            "name": "Sylvan Craft",
            "brief": "Craft 3 potions or bow items in Daw'ul Talalu for the Mystleaf Revel.",
            "kind": "craft",
            "count": 3,
            "token_reward": 3,
        },
    ],
}


# ============================================================
# HERITAGE VENDORS — per-continent item catalog
# ============================================================
# Token costs scale by item value. All items are permanent once purchased.
# Categories: cosmetic, title, buff, pet, recipe, material, badge
HERITAGE_VENDORS: dict[str, list[dict]] = {
    "valeria": [
        {"id": "hv_valeria_oathblade_skin", "name": "Oathblade Weapon Skin", "category": "cosmetic", "cost": 80,
         "desc": "A golden weapon skin etched with oath-runes. Purely cosmetic.", "rarity": "rare"},
        {"id": "hv_valeria_imperial_crown", "name": "Imperial Crown", "category": "cosmetic", "cost": 120,
         "desc": "A crown of the old Human Empire. Purely cosmetic.", "rarity": "epic"},
        {"id": "hv_valeria_oathkeeper_title", "name": "Title: Oathkeeper", "category": "title", "cost": 100,
         "desc": "Grants the title 'Oathkeeper of Valeria'.", "rarity": "epic"},
        {"id": "hv_valeria_caravan_boon", "name": "Caravan Master's Boon", "category": "buff", "cost": 300,
         "desc": "Permanent: +5% gold from sales while in Valeria.", "rarity": "legendary"},
        {"id": "hv_valeria_oath_hound", "name": "Oath Hound Pet", "category": "pet", "cost": 400,
         "desc": "A loyal hound sworn to your oath. Follows you on your adventures.", "rarity": "legendary"},
        {"id": "hv_valeria_oath_seal_recipe", "name": "Oath Seal Recipe", "category": "recipe", "cost": 200,
         "desc": "A cross-continent recipe using oath seal fragments.", "rarity": "epic"},
        {"id": "hv_valeria_oath_seal_part", "name": "Oath Seal Fragment", "category": "material", "cost": 75,
         "desc": "A boss part from the Oathbreaker.", "rarity": "epic"},
        {"id": "hv_valeria_badge", "name": "Valeria Heritage Badge", "category": "badge", "cost": 100,
         "desc": "A badge proving your participation in the Festival of the Oath.", "rarity": "epic"},
    ],
    "mushkara": [
        {"id": "hv_mushkara_chainblade_skin", "name": "Chainblade Weapon Skin", "category": "cosmetic", "cost": 80,
         "desc": "A weapon skin wrapped in broken chain links. Purely cosmetic.", "rarity": "rare"},
        {"id": "hv_mushkara_warhelm", "name": "Warhelm of the Rebellion", "category": "cosmetic", "cost": 120,
         "desc": "The horned helm of the Orc rebellion. Purely cosmetic.", "rarity": "epic"},
        {"id": "hv_mushkara_chainbreaker_title", "name": "Title: Chainbreaker", "category": "title", "cost": 100,
         "desc": "Grants the title 'Chainbreaker of Mushkara'.", "rarity": "epic"},
        {"id": "hv_mushkara_warforge_boon", "name": "Warforge Boon", "category": "buff", "cost": 300,
         "desc": "Permanent: +5% blacksmithing XP while in Mushkara.", "rarity": "legendary"},
        {"id": "hv_mushkara_war_beast", "name": "War Beast Pet", "category": "pet", "cost": 400,
         "desc": "A battle-scarred beast from the Orc war-camps.", "rarity": "legendary"},
        {"id": "hv_mushkara_chainbreaker_recipe", "name": "Chainbreaker Recipe", "category": "recipe", "cost": 200,
         "desc": "A cross-continent recipe using chainbreaker fragments.", "rarity": "epic"},
        {"id": "hv_mushkara_chainbreaker_part", "name": "Chainbreaker Fragment", "category": "material", "cost": 75,
         "desc": "A boss part from the Demon Reborn.", "rarity": "epic"},
        {"id": "hv_mushkara_badge", "name": "Mushkara Heritage Badge", "category": "badge", "cost": 100,
         "desc": "A badge proving your participation in Chainbreaker's Month.", "rarity": "epic"},
    ],
    "concordia": [
        {"id": "hv_concordia_mosaic_blade", "name": "Mosaic Blade Skin", "category": "cosmetic", "cost": 80,
         "desc": "A weapon skin inlaid with mosaic tiles. Purely cosmetic.", "rarity": "rare"},
        {"id": "hv_concordia_diplomat_cloak", "name": "Diplomat's Cloak", "category": "cosmetic", "cost": 120,
         "desc": "A cloak of many colors worn by Federation diplomats. Purely cosmetic.", "rarity": "epic"},
        {"id": "hv_concordia_ambassador_title", "name": "Title: Ambassador", "category": "title", "cost": 100,
         "desc": "Grants the title 'Ambassador of Concordia'.", "rarity": "epic"},
        {"id": "hv_concordia_trade_boon", "name": "Trade Boon", "category": "buff", "cost": 300,
         "desc": "Permanent: +5% jewelcrafting XP while in Concordia.", "rarity": "legendary"},
        {"id": "hv_concordia_mosaic_cat", "name": "Mosaic Cat Pet", "category": "pet", "cost": 400,
         "desc": "A cat with mosaic-patterned fur from the Federation markets.", "rarity": "legendary"},
        {"id": "hv_concordia_federation_recipe", "name": "Federation Seal Recipe", "category": "recipe", "cost": 200,
         "desc": "A cross-continent recipe using federation seal parts.", "rarity": "epic"},
        {"id": "hv_concordia_federation_part", "name": "Federation Seal Half", "category": "material", "cost": 75,
         "desc": "A boss part from the Fallen Ambassador.", "rarity": "epic"},
        {"id": "hv_concordia_badge", "name": "Concordia Heritage Badge", "category": "badge", "cost": 100,
         "desc": "A badge proving your participation in the Mosaic Festival.", "rarity": "epic"},
    ],
    "khardrum": [
        {"id": "hv_khardrum_forgehammer_skin", "name": "Forgehammer Weapon Skin", "category": "cosmetic", "cost": 80,
         "desc": "A weapon skin etched with dwarven forge-runes. Purely cosmetic.", "rarity": "rare"},
        {"id": "hv_khardrum_deepvein_helm", "name": "Deepvein Helm", "category": "cosmetic", "cost": 120,
         "desc": "A great helm from the deepest Khardrum forges. Purely cosmetic.", "rarity": "epic"},
        {"id": "hv_khardrum_deepforge_title", "name": "Title: Deepforge", "category": "title", "cost": 100,
         "desc": "Grants the title 'Deepforge Smith of Khardrum'.", "rarity": "epic"},
        {"id": "hv_khardrum_mining_boon", "name": "Miner's Boon", "category": "buff", "cost": 300,
         "desc": "Permanent: +5% mining yield while in Khardrum.", "rarity": "legendary"},
        {"id": "hv_khardrum_stone_warden", "name": "Stone Warden Pet", "category": "pet", "cost": 400,
         "desc": "A small stone construct from the deep halls of Khardrum.", "rarity": "legendary"},
        {"id": "hv_khardrum_jahra_recipe", "name": "Jahra Forge Recipe", "category": "recipe", "cost": 200,
         "desc": "A cross-continent recipe using Jahra fragments and living stone hearts.", "rarity": "epic"},
        {"id": "hv_khardrum_stone_heart_part", "name": "Living Stone Heart", "category": "material", "cost": 75,
         "desc": "A boss part from the Forge Titan.", "rarity": "epic"},
        {"id": "hv_khardrum_badge", "name": "Khardrum Heritage Badge", "category": "badge", "cost": 100,
         "desc": "A badge proving your participation in the Deepforge Jubilee.", "rarity": "epic"},
    ],
    "haya": [
        {"id": "hv_haya_starblade_skin", "name": "Starblade Weapon Skin", "category": "cosmetic", "cost": 80,
         "desc": "A weapon skin that glows with starlight. Purely cosmetic.", "rarity": "rare"},
        {"id": "hv_haya_starfall_crown", "name": "Starfall Crown", "category": "cosmetic", "cost": 120,
         "desc": "A crown of fallen stars from the Starfall Cliffs. Purely cosmetic.", "rarity": "epic"},
        {"id": "hv_haya_celestial_title", "name": "Title: Celestial", "category": "title", "cost": 100,
         "desc": "Grants the title 'Celestial of Haya'.", "rarity": "epic"},
        {"id": "hv_haya_herbalism_boon", "name": "Herbalist's Boon", "category": "buff", "cost": 300,
         "desc": "Permanent: +5% herbalism yield while in Haya.", "rarity": "legendary"},
        {"id": "hv_haya_star_spirit", "name": "Star Spirit Pet", "category": "pet", "cost": 400,
         "desc": "A small spirit of starlight from the Celestial Lake.", "rarity": "legendary"},
        {"id": "hv_haya_celestial_recipe", "name": "Celestial Weave Recipe", "category": "recipe", "cost": 200,
         "desc": "A cross-continent recipe using star shards and celestial thread.", "rarity": "epic"},
        {"id": "hv_haya_star_shard_part", "name": "Starfall Shard", "category": "material", "cost": 75,
         "desc": "A boss part from the Eclipse Avatar.", "rarity": "epic"},
        {"id": "hv_haya_badge", "name": "Haya Heritage Badge", "category": "badge", "cost": 100,
         "desc": "A badge proving your participation in the Celestial Accord.", "rarity": "epic"},
    ],
    "gennel": [
        {"id": "hv_gennel_primal_blade_skin", "name": "Primal Blade Skin", "category": "cosmetic", "cost": 80,
         "desc": "A weapon skin carved from primal bone. Purely cosmetic.", "rarity": "rare"},
        {"id": "hv_gennel_alpha_crown", "name": "Alpha's Crown", "category": "cosmetic", "cost": 120,
         "desc": "A crown of alpha fangs and primal crystals. Purely cosmetic.", "rarity": "epic"},
        {"id": "hv_gennel_primal_title", "name": "Title: Primal Sovereign", "category": "title", "cost": 100,
         "desc": "Grants the title 'Primal Sovereign of Gennel'.", "rarity": "epic"},
        {"id": "hv_gennel_hunting_boon", "name": "Hunter's Boon", "category": "buff", "cost": 300,
         "desc": "Permanent: +5% hunting XP while in Gennel.", "rarity": "legendary"},
        {"id": "hv_gennel_spirit_beast", "name": "Spirit Beast Pet", "category": "pet", "cost": 400,
         "desc": "A primal spirit beast from the Ancient Den.", "rarity": "legendary"},
        {"id": "hv_gennel_primal_recipe", "name": "Primal Blood Recipe", "category": "recipe", "cost": 200,
         "desc": "A cross-continent recipe using primal blood crystals and alpha fangs.", "rarity": "epic"},
        {"id": "hv_gennel_primal_blood_part", "name": "Primal Blood Crystal", "category": "material", "cost": 75,
         "desc": "A boss part from the Primal Sovereign.", "rarity": "epic"},
        {"id": "hv_gennel_badge", "name": "Gennel Heritage Badge", "category": "badge", "cost": 100,
         "desc": "A badge proving your participation in the Great Awakening.", "rarity": "epic"},
    ],
    "hylion": [
        {"id": "hv_hylion_tideblade_skin", "name": "Tideblade Weapon Skin", "category": "cosmetic", "cost": 80,
         "desc": "A weapon skin rippling with water energy. Purely cosmetic.", "rarity": "rare"},
        {"id": "hv_hylion_coral_crown", "name": "Coral Crown", "category": "cosmetic", "cost": 120,
         "desc": "A crown of living coral from the Coral Gardens. Purely cosmetic.", "rarity": "epic"},
        {"id": "hv_hylion_tidefall_title", "name": "Title: Tidecaller", "category": "title", "cost": 100,
         "desc": "Grants the title 'Tidecaller of Hylion'.", "rarity": "epic"},
        {"id": "hv_hylion_fishing_boon", "name": "Fisher's Boon", "category": "buff", "cost": 300,
         "desc": "Permanent: +5% fishing yield while in Hylion.", "rarity": "legendary"},
        {"id": "hv_hylion_tide_spirit", "name": "Tide Spirit Pet", "category": "pet", "cost": 400,
         "desc": "A small water spirit from the Abyssal Trench.", "rarity": "legendary"},
        {"id": "hv_hylion_leviathan_recipe", "name": "Leviathan Scale Recipe", "category": "recipe", "cost": 200,
         "desc": "A cross-continent recipe using leviathan scales and divine water.", "rarity": "epic"},
        {"id": "hv_hylion_leviathan_part", "name": "Leviathan Scale", "category": "material", "cost": 75,
         "desc": "A boss part from the Abyssal Maw.", "rarity": "legendary"},
        {"id": "hv_hylion_badge", "name": "Hylion Heritage Badge", "category": "badge", "cost": 100,
         "desc": "A badge proving your participation in the Tidefall Celebration.", "rarity": "epic"},
    ],
    "daw_ul_talalu": [
        {"id": "hv_dawul_thornblade_skin", "name": "Thornblade Weapon Skin", "category": "cosmetic", "cost": 80,
         "desc": "A weapon skin wrapped in living thorns. Purely cosmetic.", "rarity": "rare"},
        {"id": "hv_dawul_mystleaf_crown", "name": "Mystleaf Crown", "category": "cosmetic", "cost": 120,
         "desc": "A crown of living wood and bioluminescent leaves. Purely cosmetic.", "rarity": "epic"},
        {"id": "hv_dawul_mystleaf_title", "name": "Title: Dreamwalker", "category": "title", "cost": 100,
         "desc": "Grants the title 'Dreamwalker of Daw'ul Talalu'.", "rarity": "epic"},
        {"id": "hv_dawul_herbalism_boon", "name": "Forest Boon", "category": "buff", "cost": 300,
         "desc": "Permanent: +5% herbalism yield while in Daw'ul Talalu.", "rarity": "legendary"},
        {"id": "hv_dawul_mist_spirit", "name": "Mist Spirit Pet", "category": "pet", "cost": 400,
         "desc": "A small spirit of living mist from the Mystleaf forest.", "rarity": "legendary"},
        {"id": "hv_dawul_thorn_recipe", "name": "Thorn Guardian Recipe", "category": "recipe", "cost": 200,
         "desc": "A cross-continent recipe using thorn guardian cores and living wood.", "rarity": "epic"},
        {"id": "hv_dawul_thorn_core_part", "name": "Thorn Guardian Core", "category": "material", "cost": 75,
         "desc": "A boss part from the Dream Eater.", "rarity": "legendary"},
        {"id": "hv_dawul_badge", "name": "Daw'ul Talalu Heritage Badge", "category": "badge", "cost": 100,
         "desc": "A badge proving your participation in the Mystleaf Revel.", "rarity": "epic"},
    ],
}


# ============================================================
# HERITAGE MILESTONES — rewards for multi-year participation
# ============================================================
HERITAGE_MILESTONES: list[dict] = [
    {"years": 1, "reward_type": "badge", "name": "Heritage Badge",
     "desc": "A badge for your first year of participation in this continent's heritage."},
    {"years": 3, "reward_type": "cosmetic", "name": "Heritage Cape",
     "desc": "A continent-themed cape for 3 years of participation."},
    {"years": 5, "reward_type": "cosmetic", "name": "Heritage Weapon Skin",
     "desc": "A continent-themed weapon skin for 5 years of dedication."},
    {"years": 10, "reward_type": "mount", "name": "Heritage Mount",
     "desc": "An exclusive continent-themed mount for 10 years of loyalty."},
]

# Meta-achievement for participating in all 8 heritage months in a single year
HERITAGE_MASTER_ACHIEVEMENT = {
    "id": "heritage_master",
    "name": "Erchis Heritage Master",
    "desc": "Participate in all 8 Continental Heritage Months in a single year.",
    "reward_title": "Erchis Heritage Master",
    "reward_renown": 500,
}


# ============================================================
# HERITAGE TOKEN ITEM DEFINITIONS — for inventory display
# ============================================================
HERITAGE_TOKEN_ITEMS: list[dict] = [
    {"id": f"heritage_{cid}_token", "name": f"{info['name'].split(' of ')[-1] if ' of ' in info['name'] else info['name']} Heritage Token",
     "rarity": "rare", "kind": "heritage_token", "continent": cid,
     "desc": f"A token earned during {info['name']}. Spent at the {cid.title()} Heritage Vendor. Carries over year to year."}
    for cid, info in {c: HERITAGE_MONTHS[HERITAGE_MONTH_BY_CONTINENT[c]] for c in HERITAGE_MONTH_BY_CONTINENT}.items()
]


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_active_heritage_month(today: date | None = None) -> dict | None:
    """Return the heritage month config for the current month, or None if break month (September)."""
    if today is None:
        today = date.today()
    month = today.month
    return HERITAGE_MONTHS.get(month)


def get_heritage_continent(today: date | None = None) -> str | None:
    """Return the continent ID of the current heritage month, or None."""
    hm = get_active_heritage_month(today)
    return hm["continent"] if hm else None


def is_heritage_month_for(continent_id: str, today: date | None = None) -> bool:
    """Check if a given continent is currently in its heritage month."""
    hc = get_heritage_continent(today)
    return hc == continent_id


def get_heritage_boss(continent_id: str) -> dict | None:
    """Return the heritage boss definition for a continent."""
    return HERITAGE_BOSSES.get(continent_id)


def get_active_heritage_boss(today: date | None = None) -> dict | None:
    """Return the heritage boss for the current heritage month, or None."""
    hc = get_heritage_continent(today)
    return get_heritage_boss(hc) if hc else None


def get_heritage_bonuses(continent_id: str) -> dict | None:
    """Return the heritage bonus config for a continent."""
    return HERITAGE_BONUSES.get(continent_id)


def get_active_heritage_bonuses(today: date | None = None) -> dict | None:
    """Return the heritage bonuses for the current heritage month, or None."""
    hc = get_heritage_continent(today)
    return get_heritage_bonuses(hc) if hc else None


def get_heritage_daily_quests(continent_id: str) -> list[dict]:
    """Return the 3 daily heritage quest templates for a continent."""
    return HERITAGE_DAILY_QUESTS.get(continent_id, [])


def get_heritage_vendor_items(continent_id: str) -> list[dict]:
    """Return all vendor items for a continent's heritage vendor."""
    return HERITAGE_VENDORS.get(continent_id, [])


def get_heritage_vendor_item(continent_id: str, item_id: str) -> dict | None:
    """Return a specific vendor item by ID."""
    for item in HERITAGE_VENDORS.get(continent_id, []):
        if item["id"] == item_id:
            return item
    return None


def get_heritage_token_id(continent_id: str) -> str:
    """Return the token item ID for a continent."""
    return f"heritage_{continent_id}_token"


def get_all_heritage_continents() -> list[str]:
    """Return list of all 8 heritage continent IDs in calendar order."""
    return [HERITAGE_MONTHS[m]["continent"] for m in sorted(HERITAGE_MONTHS.keys())]


def get_heritage_meta_achievement(continent_id: str, year: int) -> dict:
    """Return the meta-achievement definition for a continent's heritage month."""
    hm = HERITAGE_MONTHS.get(HERITAGE_MONTH_BY_CONTINENT.get(continent_id, 0))
    name = hm["name"] if hm else continent_id
    return {
        "id": f"heritage_meta_{continent_id}_{year}",
        "name": f"Heritage Champion of {continent_id.title().replace('_', ' ')}",
        "continent": continent_id,
        "year": year,
        "milestones": [
            {"id": "daily_quests_10", "desc": "Complete 10 daily heritage quests", "target": 10, "token_reward": 10},
            {"id": "boss_kills_5", "desc": "Kill the heritage boss 5 times", "target": 5, "token_reward": 15},
            {"id": "gather_50", "desc": "Gather 50 resources on the heritage continent", "target": 50, "token_reward": 5},
            {"id": "craft_10", "desc": "Craft 10 items on the heritage continent", "target": 10, "token_reward": 5},
        ],
        "completion_reward": {
            "tokens": 50,
            "title": f"Heritage Champion of {name}",
        },
    }


def get_heritage_ladder_score(progress: dict) -> int:
    """Calculate ladder score from heritage progress."""
    score = 0
    score += progress.get("daily_quests_completed", 0) * 10
    score += progress.get("boss_kills", 0) * 25
    score += progress.get("resources_gathered", 0) * 1
    score += progress.get("items_crafted", 0) * 3
    score += progress.get("tokens_earned", 0) * 2
    return score
