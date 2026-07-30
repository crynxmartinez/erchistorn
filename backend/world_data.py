"""Erchis canon world data (v2) — matches the master world-design spec.

Contains the eleven continents (8 accessible + 3 locked), each continent's
biomes and hometowns, plus one-way ID migration maps that let us rewrite
existing character records from the old codenames (Aetheria/Vulkaros/etc.)
to the canon (Valeria/Mushkara/etc.).

Design notes:
- All 8 accessible continents are reachable at level 1 via the Grand
  Teleporter (added in Phase B). Progression comes from biome-level, not
  continent-level, so a Lv-1 Sylvan really does start in Daw'ul Talalu.
- Each biome has its own level_req that shapes the dice-delta engine.
- The three locked continents are content milestones (Phase F).
"""
from __future__ import annotations


# ============================================================
# CANON CONTINENTS (spec v2)
# ============================================================
CONTINENTS_V2: list[dict] = [
    # ---------------- VALERIA — Human Empire ----------------
    {"id": "valeria", "name": "Valeria", "home_race": "human", "level_req": 1, "locked": False,
     "desc": ("Kingdoms and farms; caravan roads and cathedral cities. The old heart of "
              "the Human Empire and, by long custom, every traveler's first landfall in Erchis."),
     "specialty": "Trading · Cooking · General crafting · Contracts",
     "biomes": [
        {"id": "golden_plains",       "name": "Golden Plains",        "level_req": 1,
         "desc": "Wheat and windmills for a hundred leagues. Bandit camps flicker among the ranches."},
        {"id": "crownwood_forest",    "name": "Crownwood Forest",     "level_req": 4,
         "desc": "Old-growth timber sheltering hunter camps and imperial ruins from the founding wars."},
        {"id": "imperial_riverlands", "name": "Imperial Riverlands",  "level_req": 8,
         "desc": "Slow rivers, silver fish, and trade ports flying a dozen banners."},
        {"id": "ashen_border",        "name": "Ashen Border",         "level_req": 14,
         "desc": "Old battlefields still guarded by undead soldiers who never received orders to stand down."},
     ]},
    # ---------------- MUSHKARA — Orc Dominion ----------------
    {"id": "mushkara", "name": "Mushkara", "home_race": "orc", "level_req": 1, "locked": False,
     "desc": ("A harsh continent forged out of rebellion. The Orcs turned ruined battlefields "
              "into strongholds — every forge here still remembers a broken chain."),
     "specialty": "Heavy weapons · Siege · Demon-hunting · War supplies",
     "biomes": [
        {"id": "bloodwind_plains", "name": "Bloodwind Plains", "level_req": 1,
         "desc": "War-camp outskirts where scavenger beasts pick at old battlefields and new recruits earn their scars."},
        {"id": "red_steppe",       "name": "Red Steppe",       "level_req": 6,
         "desc": "War-beast herds and orc settlements under a rust-coloured sky."},
        {"id": "iron_scar",        "name": "Iron Scar",        "level_req": 10,
         "desc": "A wound in the earth where bloodiron veins run and battlefield spirits still march."},
        {"id": "ash_barrens",      "name": "Ash Barrens",      "level_req": 16,
         "desc": "Volcanic soil, fire creatures, and demonic remnants from the old invasions."},
        {"id": "demonfall_crater", "name": "Demonfall Crater", "level_req": 24,
         "desc": "The largest scar Mushkara carries. Deep raid content. Infernal materials abound."},
     ]},
    # ---------------- CONCORDIA — Half-Elf Federation ----------------
    {"id": "concordia", "name": "Concordia", "home_race": "half_elf", "level_req": 1, "locked": False,
     "desc": ("A mosaic continent built by Human, Elven, and Wildblood cooperation. "
              "Trade cities, universities, embassies, and multicultural markets everywhere you turn."),
     "specialty": "Diplomacy · Trading · Jewelcrafting · Hybrid crafting",
     "biomes": [
        {"id": "trade_road_outpost", "name": "Trade Road Outpost", "level_req": 1,
         "desc": "Where the roads first reach Concordia. Roadside bandits, stray wildlife, and the first trade posts."},
        {"id": "mosaic_coast",       "name": "Mosaic Coast",       "level_req": 12,
         "desc": "Ports flying every flag. Foreign merchants haggle beside quiet smuggling routes."},
        {"id": "amber_vineyards",    "name": "Amber Vineyards",    "level_req": 14,
         "desc": "Rolling vineyards famous for wine and honey — and for the rare golden insects that live in them."},
        {"id": "silverroad",         "name": "Silverroad",         "level_req": 18,
         "desc": "The great trade highway across the continent. Caravans, bandits, and travelling wonders."},
        {"id": "diplomats_highlands","name": "Diplomat's Highlands","level_req": 22,
         "desc": "Embassies carved into the cliffs, ancient meeting halls, and quiet political intrigues."},
     ]},
    # ---------------- KHARDRUM — Dwarven Undermountain ----------------
    {"id": "khardrum", "name": "Khardrum", "home_race": "dwarf", "level_req": 1, "locked": False,
     "desc": ("A mountainous continent with underground cities, forge-halls, and mines that reach the roots "
              "of the world. The deepest veins yield Jahra — the legendary Dwarven metal."),
     "specialty": "Weapon & armor crafting · Mining · Engineering · Fortress construction",
     "biomes": [
        {"id": "stone_ridge",     "name": "Stone Ridge",     "level_req": 1,
         "desc": "Surface mining camps at the mountain's edge. Rock creatures, cave pests, and copper veins for greenhands."},
        {"id": "granite_foothills", "name": "Granite Foothills", "level_req": 16,
         "desc": "Common ore, stone-flesh creatures, and the mining camps that feed the halls below."},
        {"id": "ember_mines",       "name": "Ember Mines",       "level_req": 20,
         "desc": "Coal, fire crystals, and magma creatures. Every canary died a hundred years ago."},
        {"id": "crystal_caverns",   "name": "Crystal Caverns",   "level_req": 24,
         "desc": "Rare gems, crystal monsters, and mineral-veins that hum a low chord when tapped."},
        {"id": "deep_forges",       "name": "Deep Forges",       "level_req": 30,
         "desc": "The masterwork heart of Khardrum. Ancient forges, weapon quests, and Grandmaster smiths."},
     ]},
    # ---------------- HAYA — Higher Enclave (Elves) ----------------
    {"id": "haya", "name": "Haya", "home_race": "elf", "level_req": 1, "locked": False,
     "desc": ("Celestial forests, magical lakes, ancient ruins, and the remaining roots of the Great Tree of Haya. "
              "Sun and moon shape everything that walks or grows here."),
     "specialty": "Enchanting · Healing · Herbalism · Celestial equipment",
     "biomes": [
        {"id": "verdant_edge",  "name": "Verdant Edge",  "level_req": 1,
         "desc": "The forest's first whisper. Minor spirits, small beasts, and herbs that grow where sunlight still reaches."},
        {"id": "sunlit_canopy",  "name": "Sunlit Canopy",  "level_req": 26,
         "desc": "Solar herbs, healing creatures, and bright forest spirits who trade in favours."},
        {"id": "moonveil_woods", "name": "Moonveil Woods", "level_req": 30,
         "desc": "Lunar herbs, illusion creatures, and moonlit ruins that surface only at midnight."},
        {"id": "celestial_lake", "name": "Celestial Lake", "level_req": 34,
         "desc": "Magical fish, water spirits, and crystals that answer only to elven song."},
        {"id": "starfall_cliffs","name": "Starfall Cliffs","level_req": 38,
         "desc": "Fallen sky-stones and the flying monsters that came down with them."},
     ]},
    # ---------------- GENNEL — Primal Wildblood Sovereignty ----------------
    {"id": "gennel", "name": "Gennel", "home_race": "wildblood", "level_req": 1, "locked": False,
     "desc": ("Once a barren desert, now a continent of savannas, oases, spirit-marshes, and beast-filled wilds. "
              "The Wildbloods sang the sand into life."),
     "specialty": "Hunting · Leatherworking · Beast Taming · Survival",
     "biomes": [
        {"id": "oasis_outskirts", "name": "Oasis Outskirts", "level_req": 1,
         "desc": "Where the desert first blooms. Small scavengers, oasis wildlife, and hardy herbs for new hunters."},
        {"id": "blooming_desert", "name": "Blooming Desert", "level_req": 32,
         "desc": "Desert herbs, oases, and burrowers who remember the old dry-time."},
        {"id": "beastwood",       "name": "Beastwood",       "level_req": 36,
         "desc": "Predator dens, rare animals, and hunting-grounds that hunt back."},
        {"id": "roaring_savanna", "name": "Roaring Savanna", "level_req": 40,
         "desc": "Herd creatures, large monsters, and mount-quests for those who can keep up."},
        {"id": "ancient_den",     "name": "Ancient Den",     "level_req": 44,
         "desc": "Alpha beasts, Wildblood ruins, and totem quests older than any current bloodline."},
     ]},
    # ---------------- HYLION — Underwater Kingdom ----------------
    {"id": "hylion", "name": "Hylion", "home_race": "hyliondrian", "level_req": 1, "locked": False,
     "desc": ("Coral cities, drowned atolls, deep trenches, and magical reefs. Land races may visit — "
              "with the right potion or a Hyliondrian guide."),
     "specialty": "Fishing · Water alchemy · Pearl gathering · Aquatic equipment",
     "biomes": [
        {"id": "tide_pools",  "name": "Tide Pools",  "level_req": 1,
         "desc": "Shallow water and sunlit rocks. Small sea creatures, beach pests, and healing plants that grow in tide-light."},
        {"id": "coral_gardens",  "name": "Coral Gardens",  "level_req": 42,
         "desc": "Living coral, small sea-creatures, and quiet healing plants that grow only in tide-light."},
        {"id": "kelp_forest",    "name": "Kelp Forest",    "level_req": 46,
         "desc": "Aquatic herbs, hidden predators, and gathering nodes worth the deep dive."},
        {"id": "storm_reefs",    "name": "Storm Reefs",    "level_req": 50,
         "desc": "Lightning creatures, shipwreck fields, and crystal-fed storms that never fully break."},
        {"id": "abyssal_trench", "name": "Abyssal Trench", "level_req": 55,
         "desc": "Deep-sea monsters, rare minerals, and ruins older than the surface memory."},
     ]},
    # ---------------- DAW'UL TALALU — Sylvan Mystleaf ----------------
    {"id": "daw_ul_talalu", "name": "Daw'ul Talalu", "home_race": "sylvan", "level_req": 1, "locked": False,
     "desc": ("An ancient forest continent hidden by mist, illusion, and living magic. Cities grown from "
              "living trees. Every path answers your questions with two more."),
     "specialty": "Herbalism · Potion crafting · Magical wood · Bow crafting",
     "biomes": [
        {"id": "misty_thicket",        "name": "Misty Thicket",        "level_req": 1,
         "desc": "The forest's threshold. Illusion sprites, thorn pests, and shadow herbs that grow where the mist is thin."},
        {"id": "mistwood",             "name": "Mistwood",             "level_req": 48,
         "desc": "Illusion creatures, hidden paths, and stealth herbs favoured by every rogue in Erchis."},
        {"id": "thorn_labyrinth",      "name": "Thorn Labyrinth",      "level_req": 52,
         "desc": "Living plants, thorn materials, and traps that grew there before the Sylvans."},
        {"id": "lumina_grove",         "name": "Lumina Grove",         "level_req": 55,
         "desc": "Bioluminescent flora, magical insects, and healing resources the Enclave envies."},
        {"id": "elderroot_hollow",     "name": "Elderroot Hollow",     "level_req": 58,
         "desc": "Ancient trees, forest spirits, and the last magical wood old enough to remember Orinth."},
     ]},
    # ---------------- LOCKED CONTINENTS ----------------
    {"id": "azurea", "name": "Azurea", "home_race": None, "level_req": 999, "locked": True,
     "desc": ("The Fallen Continent — surrounded by demonic storms and unstable portals since the "
              "betrayal of heroes and the corruption of the Tree of Haya."),
     "specialty": "Endgame combat · Demon hunting · Corrupted crafting", "biomes": []},
    {"id": "vael_turog", "name": "Vael'Turog", "home_race": None, "level_req": 999, "locked": True,
     "desc": ("The Shrouded Continent — hidden behind a permanent supernatural storm. Ancient records "
              "hint at civilizations that grew without knowing the eight peoples ever existed."),
     "specialty": "Airships · Engineering · Lightning equipment", "biomes": []},
    {"id": "orinth", "name": "Orinth", "home_race": None, "level_req": 999, "locked": True,
     "desc": ("The First Continent — believed to hold the resting places of the gods and the original "
              "source of the Mythicodes. Known only through myths, ancient tablets, and divine visions."),
     "specialty": "Mythicode awakening · Divine equipment · Origin trials", "biomes": []},
]


# ============================================================
# Race → canonical homeland town (for character creation)
# ============================================================
HOMELAND_TOWN_BY_RACE: dict[str, str] = {
    "human":       "oathspire",
    "orc":         "grunhold",
    "half_elf":    "elaris",
    "dwarf":       "jahrahold",
    "elf":         "solunara",
    "wildblood":   "rindivar_grove",
    "hyliondrian": "atlantyrion",
    "sylvan":      "veilgrove",
}

# Continent → main hometown
HOMETOWN_BY_CONTINENT: dict[str, str] = {
    "valeria":       "oathspire",
    "mushkara":      "grunhold",
    "concordia":     "elaris",
    "khardrum":      "jahrahold",
    "haya":          "solunara",
    "gennel":        "rindivar_grove",
    "hylion":        "atlantyrion",
    "daw_ul_talalu": "veilgrove",
}


# ============================================================
# ONE-WAY MIGRATION MAPS (old codename → new canon)
# ============================================================
CONTINENT_ID_MAP: dict[str, str] = {
    "aetheria":   "valeria",
    "vulkaros":   "mushkara",
    "nyxmoor":    "concordia",   # theme rewritten from cursed bogs → diplomatic federation
    "frosthelm":  "khardrum",
    "zephyria":   "haya",
    "sablewaste": "gennel",
    "verdania":   "hylion",
}

BIOME_ID_MAP: dict[str, str] = {
    # Valeria (was Aetheria)
    "grasslands":       "golden_plains",
    "oakwood":          "crownwood_forest",
    "riverlands":       "imperial_riverlands",
    "old_ruins":        "ashen_border",
    # Mushkara (was Vulkaros)
    "ashlands":         "red_steppe",
    "lava_caves":       "ash_barrens",
    "basalt_steppe":    "iron_scar",
    "obsidian_pits":    "demonfall_crater",
    # Concordia (was Nyxmoor)
    "bogland":          "mosaic_coast",
    "cursed_ruins":     "amber_vineyards",
    "deadwood":         "silverroad",
    "ghost_road":       "diplomats_highlands",
    # Khardrum (was Frosthelm)
    "frozen_peaks":     "granite_foothills",
    "glacier":          "ember_mines",
    "tundra":           "crystal_caverns",
    "ice_caverns":      "deep_forges",
    # Haya (was Zephyria)
    "sky_isles":        "sunlit_canopy",
    "cloud_forest":     "moonveil_woods",
    "storm_plateau":    "celestial_lake",
    "celestial_ruins":  "starfall_cliffs",
    # Gennel (was Sablewaste)
    "dune_sea":         "blooming_desert",
    "oasis":            "beastwood",
    "djinn_ruins":      "roaring_savanna",
    "sunken_temple":    "ancient_den",
    # Hylion (was Verdania — was mixed jungle+coral, keep coral half)
    "coral_reef":       "coral_gardens",
    "sunken_atlantyrion":"abyssal_trench",
    # Daw'ul Talalu (Verdania's jungle half + new content)
    "rainforest":       "mistwood",
    "canopy_boughs":    "elderroot_hollow",
}

TOWN_ID_MAP: dict[str, str] = {
    # Valeria (was Aetheria)
    "ironhold":         "oathspire",
    "willowmere":       "riverguard",
    # Mushkara (was Vulkaros)
    "emberhold":        "grunhold",
    "ashvault":         "warforge",
    # Concordia (was Nyxmoor)
    "mourngate":        "elaris",
    "black_hollow":     "silvergate",
    # Khardrum (was Frosthelm)
    "khaz_moroth":      "jahrahold",
    "frostwatch":       "deepstone",
    # Haya (was Zephyria)
    "sun_moon_haven":   "solunara",
    "windrest":         "starfall_watch",
    # Gennel (was Sablewaste)
    "sun_bazaar":       "rindivar_grove",
    "whispering_cairns":"beastcairn",
    # Hylion (was Verdania coral half)
    "atlantyrion_gate": "atlantyrion",
    "emerald_bough":    "veilgrove",  # relocated to Daw'ul Talalu
}
# ============================================================
# Format: continent_id -> { activity/profession_id: xp_mult or special flag }
CONTINENTAL_BONUSES: dict[str, dict] = {
    "valeria": {
        "merchant":       {"xp_mult": 1.05, "tax_reduction": 0.03},
        "cooking":        {"xp_mult": 1.05},
        "contract_quest_chance": 0.10,
        "desc": "Commercial heart: +5% Trading & Cooking XP, -3% market tax.",
    },
    "haya": {
        "enchanting":     {"xp_mult": 1.05},
        "herbalism":      {"xp_mult": 1.05},
        "healing_quality": 1.05,
        "celestial_equip_chance": 0.10,
        "desc": "Celestial magic: +5% Enchanting & Herbalism XP; better healing items.",
    },
    "khardrum": {
        "mining":         {"xp_mult": 1.05, "gather_speed_mult": 0.95},
        "blacksmithing":  {"xp_mult": 1.05, "craft_speed_mult": 0.90},
        "armorsmithing":  {"xp_mult": 1.02, "craft_speed_mult": 0.92},
        "repair_cost_reduction": 0.05,
        "durable_equip_chance": 0.10,
        "desc": "Forges of the deep: +10-8% faster smithing, +5% Mining & Blacksmithing XP, cheaper repairs.",
    },
    "concordia": {
        "jewelcrafting":  {"xp_mult": 1.05, "craft_speed_mult": 0.95},
        "foreign_reputation": 1.05,
        "hybrid_recipe_chance": 0.10,
        "desc": "Diplomatic federation: +5% faster jewelcrafting, +5% Jewelcrafting XP, +5% foreign reputation gains.",
    },
    "mushkara": {
        "physical_combat_xp": 1.05,
        "blacksmithing":      {"xp_mult": 1.05, "heavy_weapon_focus": True, "craft_speed_mult": 0.93},
        "armorsmithing":      {"xp_mult": 1.02, "craft_speed_mult": 0.95},
        "demon_damage_mult":  1.10,
        "desc": "War-forged: +5% combat & heavy-weapon XP, faster demon-forged smithing, +10% damage vs demons.",
    },
    "gennel": {
        "hunting":        {"xp_mult": 1.05},
        "leatherworking": {"xp_mult": 1.05, "craft_speed_mult": 0.90},
        "beast_taming":   {"xp_mult": 1.05, "duration_reduction": 0.10},
        "beast_material_chance": 0.10,
        "desc": "Primal wilds: +10% faster leatherworking, +5% Hunting, Leatherworking & Beast Taming XP.",
    },
    "hylion": {
        "fishing":        {"xp_mult": 1.05, "gather_success": 1.05},
        "alchemy":        {"xp_mult": 1.05, "water_alchemy": True, "craft_speed_mult": 0.90},
        "pearl_coral_chance": 0.10,
        "desc": "Ocean kingdom: +10% faster water alchemy, +5% Fishing & Water Alchemy XP, better aquatic yields.",
    },
    "daw_ul_talalu": {
        "herbalism":      {"xp_mult": 1.05, "forest_gather_speed": 0.90},
        "alchemy":        {"xp_mult": 1.05, "craft_speed_mult": 0.92},
        "bow_crafting":   {"xp_mult": 1.03, "stealth_evasion_chance": 0.10, "craft_speed_mult": 0.90},
        "magical_plant_chance": 0.10,
        "desc": "Mystleaf forest: +8-10% faster alchemy & bow crafting, +5% Herbalism & Alchemy XP; magical wood & plants.",
    },
}


def continental_bonus_for(continent_id: str, key: str) -> dict | float | None:
    """Return the bonus entry for a continent and activity/profession key."""
    return CONTINENTAL_BONUSES.get(continent_id, {}).get(key)


def xp_multiplier_for(continent_id: str, key: str) -> float:
    """Convenience: get xp_mult for a key, default 1.0."""
    bonus = continental_bonus_for(continent_id, key)
    if isinstance(bonus, dict):
        return bonus.get("xp_mult", 1.0)
    return 1.0


# Attach continental bonus descriptions to each continent for the frontend.
for _c in CONTINENTS_V2:
    _c["bonus_desc"] = CONTINENTAL_BONUSES.get(_c["id"], {}).get("desc", "")
    _c["specialty"] = _c.get("specialty", CONTINENTAL_BONUSES.get(_c["id"], {}).get("desc", "").split(":")[1] if _c.get("id") in CONTINENTAL_BONUSES else "")
