"""Phase C — per-character biome Exploration Progress.
Phase D — formal Profession system (3 slots, ~20 professions, tool durability, node cooldowns, ranks).

Spec:
- Every biome tracks 0-100% exploration per character.
- Explore rolls (via the /api/game/action `explore` action) nudge progress.
- Thresholds unlock content: 10% name, 25% gathering, 50% NPCs, 75% rares, 100% mastery.
- Every character may hold up to 3 professions. Slots unlock at Lv 1 / 10 / 25.
- Professions rank Novice → Grandmaster (0-6). Each rank raises the ceiling of what recipes are usable.
"""
from __future__ import annotations
from datetime import datetime, timezone


# ============================================================
# EXPLORATION PROGRESS
# ============================================================
EXPLORATION_THRESHOLDS = [
    (10,   "The biome's name and general environment are revealed."),
    (25,   "Common gathering areas become available."),
    (50,   "Local NPCs, monsters, and minor locations become available."),
    (75,   "Rare gathering nodes and hidden quests become available."),
    (100,  "The biome is fully mapped."),
]


def exploration_delta_from_outcome(outcome: int) -> int:
    """Convert a 6-sided dice outcome into an exploration-progress delta.
    Larger swings on high rolls, tiny nudges on failure."""
    return {
        1:  -2,   # critical failure — you got lost
        2:  0,
        3:  2,
        4:  6,
        5:  12,
        6:  20,   # critical success — huge map jump
    }.get(int(outcome), 0)


def apply_exploration_progress(character: dict, biome_id: str, delta: int) -> tuple[int, int, list[str]]:
    """Add delta to exploration progress; returns (old_pct, new_pct, threshold_hits).
    threshold_hits contains descriptions of any thresholds *newly crossed*."""
    ep = character.setdefault("exploration_progress", {})
    old = int(ep.get(biome_id, 0))
    new = max(0, min(100, old + int(delta)))
    ep[biome_id] = new
    hits = []
    for pct, desc in EXPLORATION_THRESHOLDS:
        if old < pct <= new:
            hits.append(desc)
    return old, new, hits


def is_biome_unlocked_for_gathering(character: dict, biome_id: str) -> bool:
    """Gathering nodes require ≥25% exploration progress (per spec)."""
    return int(character.get("exploration_progress", {}).get(biome_id, 0)) >= 25


# ============================================================
# PROFESSIONS
# ============================================================
PROFESSIONS: list[dict] = [
    # ------- GATHERING -------
    {"id": "mining",       "name": "Mining",       "kind": "gathering",
     "desc": "Ore, stone, crystals, gems, coal.",
     "best_continents": ["khardrum"],
     "tool":   {"id": "pickaxe",         "name": "Pickaxe",         "max_durability": 100},
     "gathers_kinds": ["material"],
     "gather_biomes": ["ember_mines", "granite_foothills", "crystal_caverns", "deep_forges", "iron_scar"]},
    {"id": "herbalism",    "name": "Herbalism",    "kind": "gathering",
     "desc": "Herbs, flowers, roots, fungi, magical plants.",
     "best_continents": ["haya", "daw_ul_talalu"],
     "tool":   {"id": "herbalist_knife", "name": "Herbalist Knife", "max_durability": 80},
     "gathers_kinds": ["material"],
     "gather_biomes": ["sunlit_canopy", "moonveil_woods", "mistwood", "lumina_grove", "crownwood_forest"]},
    {"id": "logging",      "name": "Logging",      "kind": "gathering",
     "desc": "Timber, magical wood, bark, sap, resin.",
     "best_continents": ["valeria", "gennel", "daw_ul_talalu"],
     "tool":   {"id": "logging_axe",     "name": "Logging Axe",     "max_durability": 100},
     "gathers_kinds": ["material"],
     "gather_biomes": ["crownwood_forest", "beastwood", "elderroot_hollow", "thorn_labyrinth"]},
    {"id": "hunting",      "name": "Hunting",      "kind": "gathering",
     "desc": "Hide, meat, bone, fangs, beast materials.",
     "best_continents": ["gennel", "mushkara"],
     "tool":   {"id": "hunting_bow",     "name": "Hunter's Kit",    "max_durability": 90},
     "gathers_kinds": ["material"],
     "gather_biomes": ["golden_plains", "beastwood", "roaring_savanna", "red_steppe"]},
    {"id": "fishing",      "name": "Fishing",      "kind": "gathering",
     "desc": "Fish, shells, pearls, aquatic plants, sea-monster materials.",
     "best_continents": ["hylion"],
     "tool":   {"id": "fishing_rod",     "name": "Fishing Rod",     "max_durability": 60},
     "gathers_kinds": ["material"],
     "gather_biomes": ["coral_gardens", "kelp_forest", "storm_reefs", "abyssal_trench", "imperial_riverlands"]},
    {"id": "excavation",   "name": "Excavation",   "kind": "gathering",
     "desc": "Relics, fossils, ancient coins, ruin fragments, historical artifacts.",
     "best_continents": ["valeria", "concordia", "azurea"],
     "tool":   {"id": "excavator_brush", "name": "Excavator's Brush","max_durability": 60},
     "gathers_kinds": ["material", "relic"],
     "gather_biomes": ["ashen_border", "demonfall_crater", "diplomats_highlands", "elderroot_hollow"]},

    # ------- CRAFTING -------
    {"id": "blacksmithing","name": "Blacksmithing","kind": "crafting",
     "desc": "Swords, axes, spears, hammers, metal tools.",
     "best_continents": ["khardrum"], "tool": None,
     "gathers_kinds": [], "gather_biomes": []},
    {"id": "armorsmithing","name": "Armorsmithing","kind": "crafting",
     "desc": "Heavy armor, shields, helmets, armor repair kits.",
     "best_continents": ["khardrum", "mushkara"], "tool": None,
     "gathers_kinds": [], "gather_biomes": []},
    {"id": "leatherworking","name": "Leatherworking","kind": "crafting",
     "desc": "Light armor, bags, belts, hunting gear, animal equipment.",
     "best_continents": ["gennel"], "tool": None,
     "gathers_kinds": [], "gather_biomes": []},
    {"id": "tailoring",    "name": "Tailoring",    "kind": "crafting",
     "desc": "Robes, clothing, cloth armor, enchanted fabrics.",
     "best_continents": ["concordia", "haya"], "tool": None,
     "gathers_kinds": [], "gather_biomes": []},
    {"id": "alchemy",      "name": "Alchemy",      "kind": "crafting",
     "desc": "Healing potions, buffs, poisons, bombs, transformations.",
     "best_continents": ["haya", "hylion", "daw_ul_talalu"], "tool": None,
     "gathers_kinds": [], "gather_biomes": []},
    {"id": "cooking",      "name": "Cooking",      "kind": "crafting",
     "desc": "Meals, recovery food, profession food, travel food, temporary buffs.",
     "best_continents": ["valeria", "gennel"], "tool": None,
     "gathers_kinds": [], "gather_biomes": []},
    {"id": "enchanting",   "name": "Enchanting",   "kind": "crafting",
     "desc": "Adds magical effects to equipment.",
     "best_continents": ["haya", "daw_ul_talalu"], "tool": None,
     "gathers_kinds": [], "gather_biomes": []},
    {"id": "jewelcrafting","name": "Jewelcrafting","kind": "crafting",
     "desc": "Rings, amulets, gem upgrades, magical accessories.",
     "best_continents": ["concordia", "khardrum", "hylion"], "tool": None,
     "gathers_kinds": [], "gather_biomes": []},
    {"id": "engineering",  "name": "Engineering",  "kind": "crafting",
     "desc": "Traps, gathering tools, siege gear, mechanical companions, teleporter parts.",
     "best_continents": ["khardrum", "vael_turog"], "tool": None,
     "gathers_kinds": [], "gather_biomes": []},
    {"id": "bow_crafting", "name": "Bow Crafting", "kind": "crafting",
     "desc": "Bows, crossbows, arrows, magical ammunition.",
     "best_continents": ["daw_ul_talalu", "gennel"], "tool": None,
     "gathers_kinds": [], "gather_biomes": []},

    # ------- SERVICE -------
    {"id": "merchant",     "name": "Merchant",     "kind": "service",
     "desc": "Reduced market fees, improved NPC prices, better caravans, trade contracts.",
     "best_continents": ["valeria", "concordia"], "tool": None,
     "gathers_kinds": [], "gather_biomes": []},
    {"id": "cartography",  "name": "Cartography",  "kind": "service",
     "desc": "Faster Exploration Progress, hidden-location detection, map creation.",
     "best_continents": [], "tool": None,
     "gathers_kinds": [], "gather_biomes": []},
    {"id": "beast_taming", "name": "Beast Taming", "kind": "service",
     "desc": "Animal companions, mounts, beast breeding, companion equipment.",
     "best_continents": ["gennel"], "tool": None,
     "gathers_kinds": [], "gather_biomes": []},
]

PROFESSIONS_BY_ID: dict[str, dict] = {p["id"]: p for p in PROFESSIONS}


# ------- Slots + Ranks -------
def profession_slots_unlocked(character_level: int) -> int:
    """Spec: first slot at Lv 1, second at Lv 10, third at Lv 25."""
    if character_level >= 25:
        return 3
    if character_level >= 10:
        return 2
    return 1


PROFESSION_RANKS = ["novice", "apprentice", "journeyman", "expert", "master", "grandmaster"]

# 100-point tier system: each rank requires 100 points to advance.
# Points are earned by crafting (1 per craft, 2 on roll 5-6) and refining (1 per refine, 2 on roll 5-6).
POINTS_PER_TIER = 100

# Legacy XP thresholds kept for backward-compat migration of old characters.
PROFESSION_RANK_XP = {
    "novice":       100,
    "apprentice":   100,
    "journeyman":   100,
    "expert":       100,
    "master":       100,
    "grandmaster":  10_000_000,   # max rank
}


def _migrate_xp_to_points(xp: int) -> int:
    """Convert legacy XP value to new point system.
    Old thresholds were 200/600/1500/3500/8000 cumulative.
    New system: 100 points per tier, 600 total for grandmaster.
    Map proportionally, capped at 600."""
    if xp <= 0:
        return 0
    # Old cumulative thresholds: 200, 800, 2300, 5800, 13800
    old_total = 13800
    return min(600, int(xp / old_total * 600))


def rank_from_xp(xp: int) -> str:
    """Determine rank from point value. 100 points per tier.
    Kept name 'rank_from_xp' for backward compat with existing callers."""
    points = xp  # In new system, xp field stores points directly
    tier_idx = min(points // POINTS_PER_TIER, len(PROFESSION_RANKS) - 1)
    return PROFESSION_RANKS[tier_idx]
    current_tier = min(points // POINTS_PER_TIER, len(PROFESSION_RANKS) - 1)
    if current_tier >= len(PROFESSION_RANKS) - 1:
        return 0  # max rank
    return (current_tier + 1) * POINTS_PER_TIER - points


def craft_points_for_roll(outcome: int) -> int:
    """Points earned per craft based on dice roll.
    Roll 1: 0 (critical fail, materials lost)
    Roll 2-4: 1 point
    Roll 5-6: 2 points (quality bonus)
    """
    if outcome <= 1:
        return 0
    if outcome >= 5:
        return 2
    return 1


def learn_profession(character: dict, profession_id: str) -> tuple[bool, str]:
    if profession_id not in PROFESSIONS_BY_ID:
        return False, "Unknown profession."
    profs = character.setdefault("professions", [])
    if any(p["id"] == profession_id for p in profs):
        return False, "You already know this profession."
    # 7-day cooldown after abandoning the same profession (spec: seven-day change cooldown).
    abandoned = (character.get("abandoned_professions") or {}).get(profession_id)
    if abandoned and abandoned.get("abandoned"):
        try:
            since = datetime.fromisoformat(abandoned["abandoned"])
            days = (datetime.now(timezone.utc) - since).days
            if days < 7:
                remaining = 7 - days
                return False, f"You set this trade aside recently. {remaining} more day(s) before you may take it up again."
        except ValueError:
            pass
    profs.append({
        "id":       profession_id,
        "xp":       int((character.get("abandoned_professions") or {}).get(profession_id, {}).get("xp", 0)),  # restore 25% saved
        "rank":     "novice",
        "learned":  datetime.now(timezone.utc).isoformat(),
    })
    # After successful relearn, clear the abandoned record so a new 7-day timer starts fresh next time.
    if abandoned:
        character["abandoned_professions"].pop(profession_id, None)
    # If we restored xp, recalc rank
    # Migrate legacy XP to points on relearn
    raw_xp = profs[-1].get("xp", 0)
    if raw_xp > 600:
        profs[-1]["xp"] = _migrate_xp_to_points(raw_xp)
    profs[-1]["rank"] = rank_from_xp(profs[-1]["xp"])
    return True, f"You have taken up {PROFESSIONS_BY_ID[profession_id]['name']}."


def abandon_profession(character: dict, profession_id: str, cooldown_days: int = 7) -> tuple[bool, str]:
    profs = character.get("professions", []) or []
    idx = next((i for i, p in enumerate(profs) if p["id"] == profession_id), None)
    if idx is None:
        return False, "You don't have that profession."
    # Save 25% xp for potential relearn
    old = profs[idx]
    saved_xp = int(old.get("xp", 0)) // 4
    saved = character.setdefault("abandoned_professions", {})
    saved[profession_id] = {"xp": saved_xp, "abandoned": datetime.now(timezone.utc).isoformat()}
    profs.pop(idx)
    # Simple cooldown: block relearn for 7 days by storing abandoned timestamp
    return True, f"You have set aside your {PROFESSIONS_BY_ID[profession_id]['name']} tools. 25% xp retained."


def gain_profession_xp(character: dict, profession_id: str, delta: int) -> tuple[str, str] | None:
    """Add points to a profession. Kept name for backward compat.
    In the new system, 'delta' is craft points (1 or 2 based on roll).
    Returns (new_rank, old_rank) if the character ranked up, else None."""
    profs = character.get("professions", []) or []
    prof = next((p for p in profs if p["id"] == profession_id), None)
    if not prof:
        return None
    old_rank = prof.get("rank", "novice")
    # Migrate legacy XP if detected (old values were > 600)
    current = prof.get("xp", 0)
    if current > 600:
        current = _migrate_xp_to_points(current)
    prof["xp"] = current + int(delta)
    new_rank = rank_from_xp(prof["xp"])
    prof["rank"] = new_rank
    if new_rank != old_rank:
        return new_rank, old_rank
    return None
def has_profession_rank(character: dict, profession_id: str, min_rank: str) -> bool:
    """True if character has the profession at or above min_rank."""
    if not profession_id:
        return True
    prof = next((p for p in character.get("professions", []) if p["id"] == profession_id), None)
    if not prof:
        return False
    rank_idx = PROFESSION_RANKS.index(prof.get("rank", "novice"))
    min_idx = PROFESSION_RANKS.index(min_rank) if min_rank in PROFESSION_RANKS else 0
    return rank_idx >= min_idx
