"""Phase D/E — Regional resource nodes, rarity tiers, tool durability, and node cooldowns.

Design:
- Each biome exposes a set of gathering nodes.
- Nodes have rarity (common/uncommon/rare/legendary), a required profession + rank,
  a cooldown per character, and a tool-durability cost.
- Gathering without the matching profession falls back to a generic "scavenge" result
  with reduced rewards.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone


# ============================================================
# RARITY TIERS
# ============================================================
RARITY_TIERS = ["common", "uncommon", "rare", "epic", "legendary"]

# Base cooldown per rarity (seconds) when a node is depleted.
NODE_COOLDOWN_SECONDS = {
    "common": 30,
    "uncommon": 120,
    "rare": 600,
    "epic": 3600,
    "legendary": 86400,  # daily / event-based
}

# Tool durability cost per gather attempt.
TOOL_DURABILITY_COST = {
    "common": 1,
    "uncommon": 2,
    "rare": 4,
    "epic": 7,
    "legendary": 10,
}

# Extra quantity on critical success by rarity.
CRIT_QUANTITY_BONUS = {
    "common": 1,
    "uncommon": 1,
    "rare": 2,
    "epic": 3,
    "legendary": 3,
}

# Rank ordering for min_rank checks.
RANK_ORDER = {"novice": 0, "apprentice": 1, "journeyman": 2, "expert": 3, "master": 4, "grandmaster": 5}


def rank_gte(a: str, b: str) -> bool:
    return RANK_ORDER.get(a, 0) >= RANK_ORDER.get(b, 0)


# ============================================================
# RESOURCE NODES per biome
# ============================================================
# Each node: id, name, item_id, profession, min_rank, rarity
RESOURCE_NODES: dict[str, list[dict]] = {
    # ---------------- VALERIA ----------------
    "golden_plains": [
        {"id": "node_sunwheat",       "name": "Sunwheat Field",     "item_id": "sunwheat",        "profession": "hunting",   "min_rank": "novice",    "rarity": "common"},
        {"id": "node_wild_herb",      "name": "Wild Herb Patch",    "item_id": "wild_herb",       "profession": "herbalism", "min_rank": "novice",    "rarity": "common"},
        {"id": "node_ironbloom",      "name": "Ironbloom Outcrop",  "item_id": "iron_ore",        "profession": "mining",    "min_rank": "novice",    "rarity": "common"},
        {"id": "node_golden_honey",   "name": "Golden Honey Hive",  "item_id": "golden_honey",    "profession": "hunting",   "min_rank": "apprentice","rarity": "uncommon"},
    ],
    "crownwood_forest": [
        {"id": "node_oak_log",        "name": "Oak Grove",          "item_id": "oak_log",         "profession": "logging",   "min_rank": "novice",    "rarity": "common"},
        {"id": "node_wild_herb",      "name": "Forest Herb Patch",  "item_id": "wild_herb",       "profession": "herbalism", "min_rank": "novice",    "rarity": "common"},
        {"id": "node_oathwood",       "name": "Oathwood Stand",     "item_id": "oathwood",        "profession": "logging",   "min_rank": "apprentice","rarity": "uncommon"},
        {"id": "node_crownwood_timber","name": "Crownwood Timber",  "item_id": "crownwood_timber","profession": "logging",   "min_rank": "journeyman","rarity": "rare"},
    ],
    "imperial_riverlands": [
        {"id": "node_river_pearl",    "name": "Pearl Bed",          "item_id": "river_pearl",     "profession": "fishing",   "min_rank": "novice",    "rarity": "common"},
        {"id": "node_river_stone",    "name": "River Stone Bar",    "item_id": "river_stone",     "profession": "mining",    "min_rank": "novice",    "rarity": "common"},
        {"id": "node_imperial_flax",  "name": "Imperial Flax",      "item_id": "imperial_flax",   "profession": "herbalism", "min_rank": "apprentice","rarity": "uncommon"},
    ],
    "ashen_border": [
        {"id": "node_iron_ore",       "name": "Iron Vein",          "item_id": "iron_ore",        "profession": "mining",    "min_rank": "apprentice","rarity": "common"},
        {"id": "node_ghast_dust",     "name": "Ghast Dust",         "item_id": "ghast_dust",      "profession": "excavation","min_rank": "apprentice","rarity": "uncommon"},
        {"id": "node_oath_seal",      "name": "Oath Seal Fragment", "item_id": "oath_seal_part",  "profession": "excavation","min_rank": "expert",   "rarity": "rare"},
    ],

    # ---------------- MUSHKARA ----------------
    "red_steppe": [
        {"id": "node_warhide",        "name": "Warhide Beast",      "item_id": "warhide",         "profession": "hunting",   "min_rank": "novice",    "rarity": "common"},
        {"id": "node_ashroot",        "name": "Ashroot Cluster",    "item_id": "ashroot",         "profession": "herbalism", "min_rank": "novice",    "rarity": "common"},
        {"id": "node_bloodiron",      "name": "Bloodiron Outcrop",  "item_id": "iron_ore",        "profession": "mining",    "min_rank": "apprentice","rarity": "uncommon"},
    ],
    "iron_scar": [
        {"id": "node_iron_ore",       "name": "Scar Iron",          "item_id": "iron_ore",        "profession": "mining",    "min_rank": "apprentice","rarity": "common"},
        {"id": "node_black_salt",     "name": "Black Salt Deposit", "item_id": "black_salt",      "profession": "mining",    "min_rank": "journeyman","rarity": "uncommon"},
        {"id": "node_liberator_ore",  "name": "Liberator Ore",      "item_id": "liberator_ore",   "profession": "mining",    "min_rank": "expert",   "rarity": "rare"},
    ],
    "ash_barrens": [
        {"id": "node_embercoal",      "name": "Embercoal Seam",     "item_id": "embercoal",       "profession": "mining",    "min_rank": "apprentice","rarity": "common"},
        {"id": "node_demonbone",      "name": "Demonbone Scatter",  "item_id": "demonbone_part",  "profession": "excavation","min_rank": "journeyman","rarity": "uncommon"},
        {"id": "node_ember_fang",     "name": "Ember Fang Cache",   "item_id": "ember_fang",      "profession": "hunting",   "min_rank": "expert",   "rarity": "rare"},
    ],
    "demonfall_crater": [
        {"id": "node_infernal_core",  "name": "Infernal Core",      "item_id": "infernal_core",   "profession": "mining",    "min_rank": "expert",   "rarity": "uncommon"},
        {"id": "node_chainbreaker",   "name": "Chainbreaker Fragment","item_id": "chainbreaker_fragment_part","profession": "excavation","min_rank": "master","rarity": "rare"},
        {"id": "node_orc_war_banner", "name": "Orc War Banner",     "item_id": "orc_war_banner",  "profession": "excavation","min_rank": "grandmaster","rarity": "legendary"},
    ],

    # ---------------- CONCORDIA ----------------
    "mosaic_coast": [
        {"id": "node_mosaic_shell",   "name": "Mosaic Shell",       "item_id": "mosaic_shell",    "profession": "fishing",   "min_rank": "novice",    "rarity": "common"},
        {"id": "node_concord_flax",   "name": "Concord Flax",       "item_id": "concord_flax",    "profession": "herbalism", "min_rank": "novice",    "rarity": "common"},
        {"id": "node_silk_vine",      "name": "Silk Vine",          "item_id": "silk_vine",       "profession": "herbalism", "min_rank": "apprentice","rarity": "uncommon"},
    ],
    "amber_vineyards": [
        {"id": "node_amberglass",     "name": "Amberglass",         "item_id": "amberglass",      "profession": "herbalism", "min_rank": "novice",    "rarity": "common"},
        {"id": "node_wild_nectar",    "name": "Wild Nectar",        "item_id": "wild_nectar",     "profession": "herbalism", "min_rank": "apprentice","rarity": "uncommon"},
        {"id": "node_prism_gem",      "name": "Prism Gem Vein",     "item_id": "prism_gem",       "profession": "mining",    "min_rank": "expert",   "rarity": "rare"},
    ],
    "silverroad": [
        {"id": "node_twinwood",       "name": "Twinwood",           "item_id": "twinwood",        "profession": "logging",   "min_rank": "novice",    "rarity": "common"},
        {"id": "node_diplomat_ink",   "name": "Diplomat's Ink",     "item_id": "diplomat_ink",    "profession": "herbalism", "min_rank": "apprentice","rarity": "uncommon"},
    ],
    "diplomats_highlands": [
        {"id": "node_ancient_treaty", "name": "Ancient Treaty Fragment","item_id": "ancient_treaty_fragment","profession": "excavation","min_rank": "journeyman","rarity": "uncommon"},
        {"id": "node_federation_seal","name": "Federation Seal",    "item_id": "federation_seal_part","profession": "excavation","min_rank": "expert",   "rarity": "rare"},
        {"id": "node_hybrid_manual",  "name": "Hybrid Crafting Manual","item_id": "hybrid_crafting_manual","profession": "excavation","min_rank": "master","rarity": "legendary"},
    ],

    # ---------------- KHARDRUM ----------------
    "granite_foothills": [
        {"id": "node_copper_ore",     "name": "Copper Vein",        "item_id": "copper_ore",      "profession": "mining",    "min_rank": "novice",    "rarity": "common"},
        {"id": "node_stone_mushroom", "name": "Stone Mushroom",     "item_id": "stone_mushroom",  "profession": "herbalism", "min_rank": "novice",    "rarity": "common"},
        {"id": "node_mountain_silver","name": "Mountain Silver",    "item_id": "mountain_silver", "profession": "mining",    "min_rank": "apprentice","rarity": "uncommon"},
    ],
    "ember_mines": [
        {"id": "node_coal",           "name": "Coal Seam",          "item_id": "embercoal",       "profession": "mining",    "min_rank": "apprentice","rarity": "common"},
        {"id": "node_forge_salt",     "name": "Forge Salt",         "item_id": "forge_salt",      "profession": "mining",    "min_rank": "apprentice","rarity": "uncommon"},
        {"id": "node_molten_core",    "name": "Molten Core Ore",    "item_id": "molten_core_ore", "profession": "mining",    "min_rank": "expert",   "rarity": "rare"},
    ],
    "crystal_caverns": [
        {"id": "node_deep_crystal",   "name": "Deep Crystal",       "item_id": "deep_crystal",    "profession": "mining",    "min_rank": "journeyman","rarity": "common"},
        {"id": "node_jahra_ore",      "name": "Jahra Ore",          "item_id": "jahra_ore",       "profession": "mining",    "min_rank": "expert",   "rarity": "rare"},
        {"id": "node_ancient_dwarven_rune","name": "Ancient Dwarven Rune","item_id": "ancient_dwarven_rune","profession": "excavation","min_rank": "master","rarity": "rare"},
    ],
    "deep_forges": [
        {"id": "node_forge_core",     "name": "Forge Core",         "item_id": "forge_core",      "profession": "mining",    "min_rank": "expert",   "rarity": "uncommon"},
        {"id": "node_jahra_fragment", "name": "Jahra Fragment",     "item_id": "jahra_fragment_part","profession": "mining",   "min_rank": "master",   "rarity": "rare"},
        {"id": "node_master_smith_bp","name": "Master Smith Blueprint","item_id": "master_smith_blueprint","profession": "blacksmithing","min_rank": "grandmaster","rarity": "legendary"},
    ],

    # ---------------- HAYA ----------------
    "sunlit_canopy": [
        {"id": "node_sunpetal",       "name": "Sunpetal",           "item_id": "sunpetal",        "profession": "herbalism", "min_rank": "apprentice","rarity": "common"},
        {"id": "node_solar_amber",    "name": "Solar Amber",        "item_id": "solar_amber",     "profession": "mining",    "min_rank": "apprentice","rarity": "uncommon"},
        {"id": "node_haya_sap",       "name": "Haya Sap",           "item_id": "haya_sap",        "profession": "herbalism", "min_rank": "journeyman","rarity": "uncommon"},
    ],
    "moonveil_woods": [
        {"id": "node_moonleaf",       "name": "Moonleaf",           "item_id": "moonleaf",        "profession": "herbalism", "min_rank": "apprentice","rarity": "common"},
        {"id": "node_lunar_crystal",  "name": "Lunar Crystal",      "item_id": "lunar_crystal",   "profession": "mining",    "min_rank": "journeyman","rarity": "uncommon"},
        {"id": "node_moon_thread",    "name": "Moon Thread",        "item_id": "moon_thread",     "profession": "herbalism", "min_rank": "expert",   "rarity": "rare"},
    ],
    "celestial_lake": [
        {"id": "node_celestial_water","name": "Celestial Water",    "item_id": "celestial_water", "profession": "fishing",   "min_rank": "apprentice","rarity": "common"},
        {"id": "node_star_silver",    "name": "Star-Silver",        "item_id": "star_silver",     "profession": "mining",    "min_rank": "expert",   "rarity": "rare"},
        {"id": "node_celestial_shard","name": "Celestial Shard",    "item_id": "celestial_shard", "profession": "fishing",   "min_rank": "master",   "rarity": "legendary"},
    ],
    "starfall_cliffs": [
        {"id": "node_sunstone_core",  "name": "Sunstone Core",      "item_id": "sunstone_core",   "profession": "mining",    "min_rank": "expert",   "rarity": "uncommon"},
        {"id": "node_ancient_haya_bark","name": "Ancient Haya Bark","item_id": "ancient_haya_bark","profession": "logging",  "min_rank": "master",   "rarity": "rare"},
        {"id": "node_star_shard",     "name": "Starfall Shard",     "item_id": "star_shard_part", "profession": "mining",    "min_rank": "master",   "rarity": "rare"},
    ],

    # ---------------- GENNEL ----------------
    "blooming_desert": [
        {"id": "node_wild_nectar",    "name": "Desert Nectar",      "item_id": "wild_nectar",     "profession": "herbalism", "min_rank": "expert",   "rarity": "common"},
        {"id": "node_totem_stone",    "name": "Totem Stone",        "item_id": "totem_stone",     "profession": "mining",    "min_rank": "expert",   "rarity": "uncommon"},
        {"id": "node_spirit_moss",    "name": "Spirit Moss",        "item_id": "spirit_moss",     "profession": "herbalism", "min_rank": "expert",   "rarity": "uncommon"},
    ],
    "beastwood": [
        {"id": "node_fangwood",       "name": "Fangwood",           "item_id": "fangwood",        "profession": "logging",   "min_rank": "expert",   "rarity": "common"},
        {"id": "node_primal_hide",    "name": "Primal Hide Beast",  "item_id": "primal_hide",     "profession": "hunting",   "min_rank": "expert",   "rarity": "common"},
        {"id": "node_beast_resin",    "name": "Beast Resin",        "item_id": "beast_resin",     "profession": "logging",   "min_rank": "expert",   "rarity": "uncommon"},
    ],
    "roaring_savanna": [
        {"id": "node_alpha_bone",     "name": "Alpha Bone",         "item_id": "alpha_bone",      "profession": "hunting",   "min_rank": "expert",   "rarity": "common"},
        {"id": "node_warhide",        "name": "Savanna Warhide",    "item_id": "warhide",         "profession": "hunting",   "min_rank": "expert",   "rarity": "uncommon"},
        {"id": "node_alpha_fang",     "name": "Alpha Fang",         "item_id": "alpha_fang_part", "profession": "hunting",   "min_rank": "master",   "rarity": "rare"},
    ],
    "ancient_den": [
        {"id": "node_ancient_totem",  "name": "Ancient Totem Fragment","item_id": "ancient_totem_fragment","profession": "excavation","min_rank": "expert","rarity": "uncommon"},
        {"id": "node_primal_blood_crystal","name": "Primal Blood Crystal","item_id": "primal_blood_crystal_part","profession": "excavation","min_rank": "master","rarity": "rare"},
        {"id": "node_rindivar_relic", "name": "Rindivar Relic",     "item_id": "rindivar_relic",  "profession": "excavation","min_rank": "grandmaster","rarity": "legendary"},
    ],

    # ---------------- HYLION ----------------
    "coral_gardens": [
        {"id": "node_coral",          "name": "Coral Bed",          "item_id": "coral",           "profession": "fishing",   "min_rank": "expert",   "rarity": "common"},
        {"id": "node_abyss_kelp",     "name": "Abyss Kelp",         "item_id": "abyss_kelp",      "profession": "fishing",   "min_rank": "expert",   "rarity": "common"},
        {"id": "node_tide_pearl",     "name": "Tide Pearl",         "item_id": "tide_pearl",      "profession": "fishing",   "min_rank": "expert",   "rarity": "uncommon"},
    ],
    "kelp_forest": [
        {"id": "node_eel_crystal",    "name": "Eel Crystal",        "item_id": "eel_crystal",     "profession": "fishing",   "min_rank": "expert",   "rarity": "common"},
        {"id": "node_sea_glass",      "name": "Sea Glass",          "item_id": "sea_glass",       "profession": "fishing",   "min_rank": "expert",   "rarity": "uncommon"},
        {"id": "node_moonwater",      "name": "Moonwater",          "item_id": "moonwater",       "profession": "fishing",   "min_rank": "expert",   "rarity": "rare"},
    ],
    "storm_reefs": [
        {"id": "node_storm_shell",    "name": "Storm Shell",        "item_id": "storm_shell",     "profession": "fishing",   "min_rank": "expert",   "rarity": "uncommon"},
        {"id": "node_coral_ore",      "name": "Coral Ore",          "item_id": "coral_ore",       "profession": "mining",    "min_rank": "expert",   "rarity": "rare"},
        {"id": "node_ancient_tide_tablet","name": "Ancient Tide Tablet","item_id": "ancient_tide_tablet","profession": "excavation","min_rank": "master","rarity": "legendary"},
    ],
    "abyssal_trench": [
        {"id": "node_abyssal_fang",   "name": "Abyssal Fang",       "item_id": "abyssal_fang",    "profession": "fishing",   "min_rank": "expert",   "rarity": "uncommon"},
        {"id": "node_sea_core",       "name": "Sea Core",           "item_id": "sea_core",        "profession": "fishing",   "min_rank": "master",   "rarity": "rare"},
        {"id": "node_divine_water",   "name": "Divine Water Fragment","item_id": "divine_water_part","profession": "fishing","min_rank": "grandmaster","rarity": "legendary"},
    ],

    # ---------------- DAW'UL TALALU ----------------
    "mistwood": [
        {"id": "node_dreamleaf",      "name": "Dreamleaf",          "item_id": "dreamleaf",       "profession": "herbalism", "min_rank": "expert",   "rarity": "common"},
        {"id": "node_whisperwood",    "name": "Whisperwood",        "item_id": "whisperwood",     "profession": "logging",   "min_rank": "expert",   "rarity": "uncommon"},
        {"id": "node_veil_flower",    "name": "Veil Flower",        "item_id": "veil_flower",     "profession": "herbalism", "min_rank": "expert",   "rarity": "uncommon"},
    ],
    "thorn_labyrinth": [
        {"id": "node_thorn_silk",     "name": "Thorn Silk",         "item_id": "thorn_silk",      "profession": "herbalism", "min_rank": "expert",   "rarity": "common"},
        {"id": "node_glowcap",        "name": "Glowcap",            "item_id": "glowcap",         "profession": "herbalism", "min_rank": "expert",   "rarity": "uncommon"},
        {"id": "node_living_bark",    "name": "Living Bark",        "item_id": "living_bark",     "profession": "logging",   "min_rank": "master",   "rarity": "rare"},
    ],
    "lumina_grove": [
        {"id": "node_glowcap",        "name": "Glowcap Grove",      "item_id": "glowcap",         "profession": "herbalism", "min_rank": "expert",   "rarity": "common"},
        {"id": "node_elderroot_sap",  "name": "Elderroot Sap",      "item_id": "elderroot_sap",   "profession": "herbalism", "min_rank": "master",   "rarity": "rare"},
        {"id": "node_veil_essence",   "name": "Veil Essence",       "item_id": "veil_essence",    "profession": "herbalism", "min_rank": "master",   "rarity": "rare"},
    ],
    "elderroot_hollow": [
        {"id": "node_living_wood",    "name": "Living Wood Core",   "item_id": "living_wood_part","profession": "logging",   "min_rank": "master",   "rarity": "rare"},
        {"id": "node_ancient_seed",   "name": "Ancient Seed",       "item_id": "ancient_seed",    "profession": "herbalism", "min_rank": "master",   "rarity": "rare"},
        {"id": "node_mystleaf_rune",  "name": "Mystleaf Rune",      "item_id": "mystleaf_rune",   "profession": "excavation","min_rank": "grandmaster","rarity": "legendary"},
    ],
}


RESOURCE_NODES_BY_ID: dict[str, dict] = {}
for _biome_nodes in RESOURCE_NODES.values():
    for _node in _biome_nodes:
        RESOURCE_NODES_BY_ID[_node["id"]] = _node

# Merge content-plan resource nodes (from content_plan_data.py) on top.
from content_plan_data import PLAN_RESOURCE_NODES  # noqa: E402
for _biome_id, _plan_nodes in PLAN_RESOURCE_NODES.items():
    _existing_ids = {n["id"] for n in RESOURCE_NODES.get(_biome_id, [])}
    for _pn in _plan_nodes:
        if _pn["id"] not in _existing_ids:
            RESOURCE_NODES.setdefault(_biome_id, []).append(_pn)
            RESOURCE_NODES_BY_ID[_pn["id"]] = _pn


# ============================================================
# TOOL DURABILITY
# ============================================================
# Profession tool ids map to the values stored on professions.PROFESSIONS.
def get_profession_tool(character: dict, profession_id: str) -> dict | None:
    """Return the character's tool record for a profession, or None if not owned.
    Checks inventory first (kind='tool' items), falls back to character['tools'] dict."""
    from professions import PROFESSIONS_BY_ID
    prof = PROFESSIONS_BY_ID.get(profession_id)
    if not prof or not prof.get("tool"):
        return None
    tool_id = prof["tool"]["id"]
    # Check inventory for tool item
    for slot in character.get("inventory", []):
        if slot.get("item_id") == tool_id and slot.get("quantity", 0) > 0:
            return {
                "id": tool_id,
                "name": prof["tool"]["name"],
                "durability": slot.get("durability", prof["tool"]["max_durability"]),
                "max_durability": prof["tool"]["max_durability"],
                "_inventory_slot": slot,
            }
    # Fallback to legacy tools dict
    return character.setdefault("tools", {}).get(tool_id)
def consume_tool_durability(character: dict, profession_id: str, cost: int) -> tuple[int, bool]:
    """Subtract cost from the profession's tool. Returns (remaining, broken).
    If no tool owned, returns (0, True) — caller should block the action."""
    tool = get_profession_tool(character, profession_id)
    if not tool:
        return 0, True
    before = int(tool.get("durability", 0))
    after = max(0, before - cost)
    # Update in inventory slot if present
    slot = tool.get("_inventory_slot")
    if slot is not None:
        slot["durability"] = after
    else:
        tool["durability"] = after
    return after, after <= 0


def repair_tool(character: dict, profession_id: str, amount: int | None = None) -> int:
    """Repair a profession tool by amount (or to max if None). Returns 0 if not owned."""
    tool = get_profession_tool(character, profession_id)
    if not tool:
        return 0
    max_dur = tool.get("max_durability", 100)
    if amount is None:
        new_dur = max_dur
    else:
        new_dur = min(max_dur, int(tool.get("durability", 0)) + amount)
    # Update in inventory slot if present
    slot = tool.get("_inventory_slot")
    if slot is not None:
        slot["durability"] = new_dur
    else:
        tool["durability"] = new_dur
    return int(new_dur)


# ============================================================
# NODE COOLDOWNS
# ============================================================
def node_on_cooldown(character: dict, node_id: str, now: datetime | None = None) -> bool:
    cd = character.setdefault("node_cooldowns", {})
    until = cd.get(node_id)
    if not until:
        return False
    now = now or datetime.now(timezone.utc)
    try:
        until_dt = datetime.fromisoformat(until)
    except (ValueError, TypeError):
        return False
    return until_dt > now


def set_node_cooldown(character: dict, node_id: str, rarity: str, now: datetime | None = None) -> None:
    now = now or datetime.now(timezone.utc)
    seconds = NODE_COOLDOWN_SECONDS.get(rarity, 60)
    until = (now.replace(tzinfo=timezone.utc) + timedelta(seconds=seconds)).isoformat()
    character.setdefault("node_cooldowns", {})[node_id] = until


def seconds_until_node_ready(character: dict, node_id: str, now: datetime | None = None) -> int:
    cd = character.setdefault("node_cooldowns", {})
    until = cd.get(node_id)
    if not until:
        return 0
    now = now or datetime.now(timezone.utc)
    try:
        until_dt = datetime.fromisoformat(until)
    except (ValueError, TypeError):
        return 0
    return max(0, int((until_dt - now).total_seconds()))


# ============================================================
# HELPERS
# ============================================================
def nodes_for_biome(biome_id: str) -> list[dict]:
    return RESOURCE_NODES.get(biome_id, [])


def pick_resource_node(character: dict, biome_id: str, action_id: str, target_id: str | None = None) -> dict | None:
    """Choose a resource node for a gather/fish action. Honours explicit target_id if it matches a node id."""
    nodes = nodes_for_biome(biome_id)
    if not nodes:
        return None
    # Explicit target
    if target_id:
        for n in nodes:
            if n["id"] == target_id or n["item_id"] == target_id:
                return n
    # Filter by action and profession/skill
    if action_id == "fish":
        pool = [n for n in nodes if n["profession"] == "fishing"]
    elif action_id == "gather":
        profs = [p.get("id") for p in character.get("professions", [])]
        pool = [n for n in nodes if n["profession"] in profs]
    else:
        pool = list(nodes)
    # Exclude on cooldown; prefer the character's highest profession rank then rarity.
    from professions import rank_from_xp
    now = datetime.now(timezone.utc)
    valid = [n for n in pool if not node_on_cooldown(character, n["id"], now)]
    if not valid:
        valid = pool  # all on cooldown — still allow fallback with warning
    valid.sort(key=lambda n: (RANK_ORDER.get(n["min_rank"], 0), {"common": 0, "uncommon": 1, "rare": 2, "epic": 3, "legendary": 4}.get(n["rarity"], 0)), reverse=True)
    return valid[0] if valid else None


def has_profession_for_node(character: dict, node: dict) -> tuple[bool, str]:
    """Return (has_required_rank, reason_or_rank)."""
    prof_id = node["profession"]
    prof = next((p for p in character.get("professions", []) if p.get("id") == prof_id), None)
    if not prof:
        return False, f"requires {prof_id}"
    if not rank_gte(prof.get("rank", "novice"), node["min_rank"]):
        return False, f"requires {node['min_rank']} {prof_id}"
    return True, prof.get("rank", "novice")


# ============================================================
# ITEMS — add the new regional materials to ITEMS if not present
# ============================================================
# This list is merged into game_data.ITEMS at import time in server.py.
REGIONAL_ITEMS: list[dict] = [
    # Valeria
    {"id": "sunwheat", "name": "Sunwheat", "kind": "material", "rarity": "common"},
    {"id": "oathwood", "name": "Oathwood", "kind": "material", "rarity": "uncommon"},
    {"id": "crownwood_timber", "name": "Crownwood Timber", "kind": "material", "rarity": "rare"},
    {"id": "river_pearl", "name": "River Pearl", "kind": "material", "rarity": "common"},
    {"id": "imperial_flax", "name": "Imperial Flax", "kind": "material", "rarity": "uncommon"},
    {"id": "golden_honey", "name": "Golden Honey", "kind": "material", "rarity": "uncommon"},
    {"id": "river_stone", "name": "River Stone", "kind": "material", "rarity": "common"},
    # Mushkara
    {"id": "warhide", "name": "Warhide", "kind": "material", "rarity": "common"},
    {"id": "ashroot", "name": "Ashroot", "kind": "material", "rarity": "common"},
    {"id": "black_salt", "name": "Black Salt", "kind": "material", "rarity": "uncommon"},
    {"id": "liberator_ore", "name": "Liberator Ore", "kind": "material", "rarity": "rare"},
    {"id": "embercoal", "name": "Embercoal", "kind": "material", "rarity": "common"},
    {"id": "ember_fang", "name": "Ember Fang", "kind": "material", "rarity": "rare"},
    {"id": "infernal_core", "name": "Infernal Core", "kind": "material", "rarity": "uncommon"},
    {"id": "orc_war_banner", "name": "Orc War Banner", "kind": "material", "rarity": "legendary"},
    # Concordia
    {"id": "mosaic_shell", "name": "Mosaic Shell", "kind": "material", "rarity": "common"},
    {"id": "concord_flax", "name": "Concord Flax", "kind": "material", "rarity": "common"},
    {"id": "silk_vine", "name": "Silk Vine", "kind": "material", "rarity": "uncommon"},
    {"id": "amberglass", "name": "Amberglass", "kind": "material", "rarity": "common"},
    {"id": "wild_nectar", "name": "Wild Nectar", "kind": "material", "rarity": "uncommon"},
    {"id": "prism_gem", "name": "Prism Gem", "kind": "material", "rarity": "rare"},
    {"id": "twinwood", "name": "Twinwood", "kind": "material", "rarity": "common"},
    {"id": "diplomat_ink", "name": "Diplomat's Ink", "kind": "material", "rarity": "uncommon"},
    {"id": "ancient_treaty_fragment", "name": "Ancient Treaty Fragment", "kind": "material", "rarity": "uncommon"},
    {"id": "hybrid_crafting_manual", "name": "Hybrid Crafting Manual", "kind": "material", "rarity": "legendary"},
    # Khardrum
    {"id": "stone_mushroom", "name": "Stone Mushroom", "kind": "material", "rarity": "common"},
    {"id": "mountain_silver", "name": "Mountain Silver", "kind": "material", "rarity": "uncommon"},
    {"id": "forge_salt", "name": "Forge Salt", "kind": "material", "rarity": "uncommon"},
    {"id": "molten_core_ore", "name": "Molten Core Ore", "kind": "material", "rarity": "rare"},
    {"id": "deep_crystal", "name": "Deep Crystal", "kind": "material", "rarity": "common"},
    {"id": "jahra_ore", "name": "Jahra Ore", "kind": "material", "rarity": "rare"},
    {"id": "ancient_dwarven_rune", "name": "Ancient Dwarven Rune", "kind": "material", "rarity": "rare"},
    {"id": "forge_core", "name": "Forge Core", "kind": "material", "rarity": "uncommon"},
    {"id": "master_smith_blueprint", "name": "Master Smith Blueprint", "kind": "material", "rarity": "legendary"},
    # Haya
    {"id": "sunpetal", "name": "Sunpetal", "kind": "material", "rarity": "common"},
    {"id": "solar_amber", "name": "Solar Amber", "kind": "material", "rarity": "uncommon"},
    {"id": "haya_sap", "name": "Haya Sap", "kind": "material", "rarity": "uncommon"},
    {"id": "moonleaf", "name": "Moonleaf", "kind": "material", "rarity": "common"},
    {"id": "lunar_crystal", "name": "Lunar Crystal", "kind": "material", "rarity": "uncommon"},
    {"id": "moon_thread", "name": "Moon Thread", "kind": "material", "rarity": "rare"},
    {"id": "celestial_water", "name": "Celestial Water", "kind": "material", "rarity": "common"},
    {"id": "star_silver", "name": "Star-Silver", "kind": "material", "rarity": "rare"},
    {"id": "celestial_shard", "name": "Celestial Shard", "kind": "material", "rarity": "legendary"},
    {"id": "sunstone_core", "name": "Sunstone Core", "kind": "material", "rarity": "uncommon"},
    {"id": "ancient_haya_bark", "name": "Ancient Haya Bark", "kind": "material", "rarity": "rare"},
    # Gennel
    {"id": "totem_stone", "name": "Totem Stone", "kind": "material", "rarity": "uncommon"},
    {"id": "spirit_moss", "name": "Spirit Moss", "kind": "material", "rarity": "uncommon"},
    {"id": "fangwood", "name": "Fangwood", "kind": "material", "rarity": "common"},
    {"id": "primal_hide", "name": "Primal Hide", "kind": "material", "rarity": "common"},
    {"id": "beast_resin", "name": "Beast Resin", "kind": "material", "rarity": "uncommon"},
    {"id": "alpha_bone", "name": "Alpha Bone", "kind": "material", "rarity": "common"},
    {"id": "ancient_totem_fragment", "name": "Ancient Totem Fragment", "kind": "material", "rarity": "uncommon"},
    {"id": "rindivar_relic", "name": "Rindivar Relic", "kind": "material", "rarity": "legendary"},
    # Hylion
    {"id": "coral", "name": "Coral", "kind": "material", "rarity": "common"},
    {"id": "abyss_kelp", "name": "Abyss Kelp", "kind": "material", "rarity": "common"},
    {"id": "tide_pearl", "name": "Tide Pearl", "kind": "material", "rarity": "uncommon"},
    {"id": "eel_crystal", "name": "Eel Crystal", "kind": "material", "rarity": "common"},
    {"id": "sea_glass", "name": "Sea Glass", "kind": "material", "rarity": "uncommon"},
    {"id": "moonwater", "name": "Moonwater", "kind": "material", "rarity": "rare"},
    {"id": "storm_shell", "name": "Storm Shell", "kind": "material", "rarity": "uncommon"},
    {"id": "coral_ore", "name": "Coral Ore", "kind": "material", "rarity": "rare"},
    {"id": "ancient_tide_tablet", "name": "Ancient Tide Tablet", "kind": "material", "rarity": "legendary"},
    {"id": "abyssal_fang", "name": "Abyssal Fang", "kind": "material", "rarity": "uncommon"},
    {"id": "sea_core", "name": "Sea Core", "kind": "material", "rarity": "rare"},
    # Daw'ul Talalu
    {"id": "dreamleaf", "name": "Dreamleaf", "kind": "material", "rarity": "common"},
    {"id": "whisperwood", "name": "Whisperwood", "kind": "material", "rarity": "uncommon"},
    {"id": "veil_flower", "name": "Veil Flower", "kind": "material", "rarity": "uncommon"},
    {"id": "thorn_silk", "name": "Thorn Silk", "kind": "material", "rarity": "common"},
    {"id": "glowcap", "name": "Glowcap", "kind": "material", "rarity": "uncommon"},
    {"id": "living_bark", "name": "Living Bark", "kind": "material", "rarity": "rare"},
    {"id": "elderroot_sap", "name": "Elderroot Sap", "kind": "material", "rarity": "rare"},
    {"id": "veil_essence", "name": "Veil Essence", "kind": "material", "rarity": "rare"},
    {"id": "ancient_seed", "name": "Ancient Seed", "kind": "material", "rarity": "rare"},
    {"id": "mystleaf_rune", "name": "Mystleaf Rune", "kind": "material", "rarity": "legendary"},
]
