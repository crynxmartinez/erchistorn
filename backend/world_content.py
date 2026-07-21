"""Phase G — Biome Bosses, Cross-Continent Recipes, and Regional Prices.

Bosses:
 - One flagship boss per accessible continent (8 total) — spawned into the top-tier biome.
 - Bosses are regular MONSTERS with an `is_boss: True` flag, higher power/hp, and
   a rare-part drop that feeds cross-continent legendary recipes.

Cross-continent recipes:
 - Six legendary recipes that require materials from ≥3 continents. They gate
   the best-in-slot equipment behind cross-continent travel.

Regional prices:
 - Continental market items are cheaper if native to that continent, more
   expensive if foreign. Multipliers applied on the /market/buy path.
"""
from __future__ import annotations


# ============================================================
# BOSSES — 1 per accessible continent, dropped into the top-tier biome.
# Each drops a unique "boss part" used in cross-continent recipes.
# ============================================================
BOSSES: list[dict] = [
    {"id": "boss_ashen_lord",       "name": "The Ashen Lord",           "biome": "ashen_border",     "continent": "valeria",
     "power": 30,  "hp": 400,  "is_boss": True,
     "drops": [("oath_seal_part",           0.40), ("greater_healing_potion", 0.8), ("relic_shard", 0.7)]},
    {"id": "boss_demon_warleader",  "name": "The Demon-Warleader",      "biome": "demonfall_crater", "continent": "mushkara",
     "power": 42,  "hp": 620,  "is_boss": True,
     "drops": [("chainbreaker_fragment_part", 0.40), ("demonbone_part", 0.7), ("jahra_ingot", 0.5)]},
    {"id": "boss_amber_diplomat",   "name": "The Amber Diplomat (Fallen)","biome": "diplomats_highlands","continent": "concordia",
     "power": 50,  "hp": 780,  "is_boss": True,
     "drops": [("federation_seal_part",     0.40), ("prism_gem_part", 0.7), ("orb_fragment", 0.5)]},
    {"id": "boss_forge_golem",      "name": "The Forge Golem of Deepvein","biome": "deep_forges",     "continent": "khardrum",
     "power": 60,  "hp": 950,  "is_boss": True,
     "drops": [("living_stone_heart_part",  0.40), ("jahra_fragment_part", 0.7), ("jahra_ingot", 0.6)]},
    {"id": "boss_starfall_avatar",  "name": "The Starfall Avatar",      "biome": "starfall_cliffs",  "continent": "haya",
     "power": 70,  "hp": 1200, "is_boss": True,
     "drops": [("star_shard_part",          0.40), ("celestial_thread_part", 0.7), ("skillbook_wind_step", 0.15)]},
    {"id": "boss_alpha_king",       "name": "The Alpha King of Ancient Den","biome": "ancient_den",  "continent": "gennel",
     "power": 80,  "hp": 1400, "is_boss": True,
     "drops": [("primal_blood_crystal_part",0.40), ("alpha_fang_part", 0.7), ("skillbook_thornlash", 0.15)]},
    {"id": "boss_leviathan",        "name": "The Leviathan of the Trench","biome": "abyssal_trench", "continent": "hylion",
     "power": 90,  "hp": 1600, "is_boss": True,
     "drops": [("leviathan_scale_part",     0.40), ("divine_water_part", 0.7), ("skillbook_tidefury", 0.15)]},
    {"id": "boss_thorn_guardian",   "name": "The Thorn Guardian Awakened","biome": "elderroot_hollow","continent": "daw_ul_talalu",
     "power": 100, "hp": 1900, "is_boss": True,
     "drops": [("thorn_guardian_core_part", 0.40), ("living_wood_part", 0.7), ("skillbook_sunlance", 0.15)]},
]


# ============================================================
# BOSS-PART ITEMS — the rare crafting materials bosses drop.
# ============================================================
BOSS_PARTS: list[dict] = [
    {"id": "oath_seal_part",              "name": "Oath Seal Fragment",           "rarity": "epic",      "kind": "boss_part"},
    {"id": "chainbreaker_fragment_part",  "name": "Chainbreaker Fragment",        "rarity": "epic",      "kind": "boss_part"},
    {"id": "demonbone_part",              "name": "Demonbone Sliver",             "rarity": "epic",      "kind": "boss_part"},
    {"id": "federation_seal_part",        "name": "Federation Seal Half",         "rarity": "epic",      "kind": "boss_part"},
    {"id": "prism_gem_part",              "name": "Prism Gem Core",               "rarity": "epic",      "kind": "boss_part"},
    {"id": "living_stone_heart_part",     "name": "Living Stone Heart",           "rarity": "epic",      "kind": "boss_part"},
    {"id": "jahra_fragment_part",         "name": "Deep Jahra Fragment",          "rarity": "epic",      "kind": "boss_part"},
    {"id": "star_shard_part",             "name": "Starfall Shard",               "rarity": "epic",      "kind": "boss_part"},
    {"id": "celestial_thread_part",       "name": "Celestial Thread",             "rarity": "epic",      "kind": "boss_part"},
    {"id": "primal_blood_crystal_part",   "name": "Primal Blood Crystal",         "rarity": "epic",      "kind": "boss_part"},
    {"id": "alpha_fang_part",             "name": "Alpha Fang",                   "rarity": "epic",      "kind": "boss_part"},
    {"id": "leviathan_scale_part",        "name": "Leviathan Scale",              "rarity": "legendary", "kind": "boss_part"},
    {"id": "divine_water_part",           "name": "Divine Water Fragment",        "rarity": "legendary", "kind": "boss_part"},
    {"id": "thorn_guardian_core_part",    "name": "Thorn Guardian Core",          "rarity": "legendary", "kind": "boss_part"},
    {"id": "living_wood_part",            "name": "Living Wood Core",             "rarity": "legendary", "kind": "boss_part"},
]


# ============================================================
# CROSS-CONTINENT LEGENDARY RECIPES — each requires materials
# from ≥3 continents to force travel/trade.
# ============================================================
CROSS_CONTINENT_RECIPES: list[dict] = [
    {"id": "craft_moonfang_spear", "name": "Moonfang Spear", "kind": "weapon",
     "requires": {"jahra_fragment_part": 1, "alpha_fang_part": 1, "star_shard_part": 1, "living_wood": 2},
     "produces": {"id": "moonfang_spear", "name": "Moonfang Spear", "rarity": "legendary",
                  "kind": "weapon", "power": 40, "slot": "weapon"},
     "profession": "blacksmithing", "profession_min_rank": "expert",
     "recipe_source": "Cross-continent (Khardrum · Gennel · Haya · Daw'ul Talalu)"},
    {"id": "craft_tidebound_amulet", "name": "Tidebound Amulet", "kind": "relic",
     "requires": {"leviathan_scale_part": 1, "prism_gem_part": 1, "oath_seal_part": 1, "abyss_coral": 3},
     "produces": {"id": "tidebound_amulet", "name": "Tidebound Amulet", "rarity": "legendary",
                  "kind": "relic", "power": 0},
     "profession": "jewelcrafting", "profession_min_rank": "expert",
     "recipe_source": "Cross-continent (Hylion · Concordia · Valeria)"},
    {"id": "craft_ashenlord_greatsword", "name": "Ashen Lord's Greatsword", "kind": "weapon",
     "requires": {"oath_seal_part": 1, "chainbreaker_fragment_part": 1, "demonbone_part": 1, "jahra_ingot": 3},
     "produces": {"id": "ashenlord_greatsword", "name": "Ashen Lord's Greatsword", "rarity": "legendary",
                  "kind": "weapon", "power": 45, "slot": "weapon"},
     "profession": "blacksmithing", "profession_min_rank": "master",
     "recipe_source": "Cross-continent (Valeria · Mushkara · Khardrum)"},
    {"id": "craft_celestial_robes", "name": "Celestial Robes of the Choir", "kind": "armor",
     "requires": {"celestial_thread_part": 1, "star_shard_part": 1, "silverleaf": 5, "moonleaf": 4},
     "produces": {"id": "celestial_robes", "name": "Celestial Robes of the Choir", "rarity": "legendary",
                  "kind": "armor", "power": 30, "slot": "armor"},
     "profession": "tailoring", "profession_min_rank": "expert",
     "recipe_source": "Cross-continent (Haya · Daw'ul Talalu)"},
    {"id": "craft_thorn_bow", "name": "Thornwood Longbow", "kind": "weapon",
     "requires": {"thorn_guardian_core_part": 1, "living_wood_part": 1, "silverleaf": 3, "alpha_fang_part": 1},
     "produces": {"id": "thorn_longbow", "name": "Thornwood Longbow", "rarity": "legendary",
                  "kind": "weapon", "power": 38, "slot": "weapon"},
     "profession": "bow_crafting", "profession_min_rank": "expert",
     "recipe_source": "Cross-continent (Daw'ul Talalu · Haya · Gennel)"},
    {"id": "craft_forgeheart_platemail", "name": "Forgeheart Platemail", "kind": "armor",
     "requires": {"living_stone_heart_part": 1, "jahra_fragment_part": 2, "chainbreaker_fragment_part": 1, "iron_ore": 8},
     "produces": {"id": "forgeheart_platemail", "name": "Forgeheart Platemail", "rarity": "legendary",
                  "kind": "armor", "power": 42, "slot": "armor"},
     "profession": "armorsmithing", "profession_min_rank": "master",
     "recipe_source": "Cross-continent (Khardrum · Mushkara)"},
]


# ============================================================
# REGIONAL PRICE MULTIPLIERS
# ============================================================
# For any item that has a `home_continent` set, prices are:
#   - 0.75x when bought on the home continent
#   - 1.4x when bought on a foreign continent
# Items without a home_continent use 1.0x baseline everywhere.
ITEM_HOME_CONTINENT: dict[str, str] = {
    # Valeria — no unique materials yet in the ITEMS list; use bandit-adjacent goods
    "oak_log":            "valeria",
    "iron_ore":           "mushkara",   # bloodiron feel
    "copper_ore":         "khardrum",
    "wild_herb":          "haya",
    "wisp_essence":       "haya",
    "wolf_pelt":          "gennel",
    "boar_hide":          "gennel",
    "serpent_scale":      "hylion",
    "serpent_venom":      "hylion",
    "orb_fragment":       "hylion",
    "jahra_ingot":        "khardrum",
    "relic_shard":        "concordia",
    "ghast_dust":         "valeria",
    "river_stone":        "valeria",
}


def regional_price_multiplier(item_id: str, continent_id: str | None) -> float:
    home = ITEM_HOME_CONTINENT.get(item_id)
    if not home or not continent_id:
        return 1.0
    return 0.75 if continent_id == home else 1.4
