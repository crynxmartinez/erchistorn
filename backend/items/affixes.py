"""Affix system — prefixes and suffixes with tier-based scaling.
Each affix has 5 tiers (T1 highest, T5 lowest). The tier rolled depends on monster level.
Some affixes also grant bonus_effects (lifesteal, crit, etc.) in addition to stats.
"""
from __future__ import annotations

# ============================================================
# Prefix Definitions
# ============================================================
# Each prefix: id, name, slots (which item kinds/slots it can roll on),
# tiers: {tier_num: {stat: [min, max]}} or {tier_num: {bonus_effects: [...]}}
# kind: "stat" (gives flat stats) or "effect" (gives bonus effects) or "both"

PREFIXES: list[dict] = [
    # --- Stat prefixes ---
    {"id": "sharp", "name": "Sharp", "kind": "stat",
     "slots": ["weapon"],
     "tiers": {
         1: {"might": [9, 14]},
         2: {"might": [6, 9]},
         3: {"might": [4, 6]},
         4: {"might": [2, 4]},
         5: {"might": [1, 2]},
     }},
    {"id": "heavy", "name": "Heavy", "kind": "stat",
     "slots": ["armor", "weapon"],
     "slot_filter": {"weapon": ["shield"]},
     "tiers": {
         1: {"vitality": [9, 14]},
         2: {"vitality": [6, 9]},
         3: {"vitality": [4, 6]},
         4: {"vitality": [2, 4]},
         5: {"vitality": [1, 2]},
     }},
    {"id": "keen", "name": "Keen", "kind": "stat",
     "slots": ["weapon", "armor"],
     "armor_filter": ["light", "leather"],
     "tiers": {
         1: {"grace": [9, 14]},
         2: {"grace": [6, 9]},
         3: {"grace": [4, 6]},
         4: {"grace": [2, 4]},
         5: {"grace": [1, 2]},
     }},
    {"id": "arcane", "name": "Arcane", "kind": "stat",
     "slots": ["weapon", "accessory"],
     "weapon_filter": ["orb", "tome", "instrument"],
     "tiers": {
         1: {"essence": [9, 14]},
         2: {"essence": [6, 9]},
         3: {"essence": [4, 6]},
         4: {"essence": [2, 4]},
         5: {"essence": [1, 2]},
     }},
    {"id": "wise", "name": "Wise", "kind": "stat",
     "slots": ["armor", "accessory"],
     "armor_filter": ["head", "back"],
     "tiers": {
         1: {"insight": [9, 14]},
         2: {"insight": [6, 9]},
         3: {"insight": [4, 6]},
         4: {"insight": [2, 4]},
         5: {"insight": [1, 2]},
     }},
    {"id": "brilliant", "name": "Brilliant", "kind": "stat",
     "slots": ["armor", "accessory"],
     "armor_filter": ["head", "back"],
     "tiers": {
         1: {"cognition": [9, 14]},
         2: {"cognition": [6, 9]},
         3: {"cognition": [4, 6]},
         4: {"cognition": [2, 4]},
         5: {"cognition": [1, 2]},
     }},
    {"id": "sturdy", "name": "Sturdy", "kind": "stat",
     "slots": ["armor", "weapon"],
     "weapon_filter": ["shield"],
     "tiers": {
         1: {"durability": [9, 14]},
         2: {"durability": [6, 9]},
         3: {"durability": [4, 6]},
         4: {"durability": [2, 4]},
         5: {"durability": [1, 2]},
     }},

    # --- Elemental damage prefixes (weapons only, T1-T3) ---
    {"id": "flaming", "name": "Flaming", "kind": "effect",
     "slots": ["weapon"],
     "tiers": {
         1: {"bonus_effects": [{"type": "extra_damage", "element": "fire", "value": 5}]},
         2: {"bonus_effects": [{"type": "extra_damage", "element": "fire", "value": 3}]},
         3: {"bonus_effects": [{"type": "extra_damage", "element": "fire", "value": 2}]},
     }},
    {"id": "frozen", "name": "Frozen", "kind": "effect",
     "slots": ["weapon"],
     "tiers": {
         1: {"bonus_effects": [{"type": "extra_damage", "element": "ice", "value": 5}]},
         2: {"bonus_effects": [{"type": "extra_damage", "element": "ice", "value": 3}]},
         3: {"bonus_effects": [{"type": "extra_damage", "element": "ice", "value": 2}]},
     }},
    {"id": "venomous", "name": "Venomous", "kind": "effect",
     "slots": ["weapon"],
     "tiers": {
         1: {"bonus_effects": [{"type": "extra_damage", "element": "poison", "value": 5}]},
         2: {"bonus_effects": [{"type": "extra_damage", "element": "poison", "value": 3}]},
         3: {"bonus_effects": [{"type": "extra_damage", "element": "poison", "value": 2}]},
     }},
    {"id": "charged", "name": "Charged", "kind": "effect",
     "slots": ["weapon"],
     "tiers": {
         1: {"bonus_effects": [{"type": "extra_damage", "element": "lightning", "value": 5}]},
         2: {"bonus_effects": [{"type": "extra_damage", "element": "lightning", "value": 3}]},
         3: {"bonus_effects": [{"type": "extra_damage", "element": "lightning", "value": 2}]},
     }},

    # --- Combat effect prefixes (weapons + accessories, T1-T3) ---
    {"id": "vampiric", "name": "Vampiric", "kind": "effect",
     "slots": ["weapon"],
     "tiers": {
         1: {"bonus_effects": [{"type": "lifesteal", "value": 0.08}]},
         2: {"bonus_effects": [{"type": "lifesteal", "value": 0.05}]},
     }},
    {"id": "precise", "name": "Precise", "kind": "effect",
     "slots": ["weapon", "accessory"],
     "tiers": {
         1: {"bonus_effects": [{"type": "crit_chance", "value": 0.06}]},
         2: {"bonus_effects": [{"type": "crit_chance", "value": 0.04}]},
         3: {"bonus_effects": [{"type": "crit_chance", "value": 0.02}]},
     }},
    {"id": "furious", "name": "Furious", "kind": "effect",
     "slots": ["weapon"],
     "tiers": {
         1: {"bonus_effects": [{"type": "crit_damage", "value": 0.15}]},
         2: {"bonus_effects": [{"type": "crit_damage", "value": 0.10}]},
         3: {"bonus_effects": [{"type": "crit_damage", "value": 0.05}]},
     }},
    {"id": "piercing", "name": "Piercing", "kind": "effect",
     "slots": ["weapon"],
     "tiers": {
         1: {"bonus_effects": [{"type": "armor_pen", "value": 0.08}]},
         2: {"bonus_effects": [{"type": "armor_pen", "value": 0.05}]},
     }},
    {"id": "swift", "name": "Swift", "kind": "effect",
     "slots": ["armor", "accessory"],
     "armor_filter": ["feet"],
     "tiers": {
         1: {"bonus_effects": [{"type": "action_speed", "value": 0.06}]},
         2: {"bonus_effects": [{"type": "action_speed", "value": 0.04}]},
     }},
    {"id": "regenerating", "name": "Regenerating", "kind": "effect",
     "slots": ["armor", "accessory"],
     "tiers": {
         1: {"bonus_effects": [{"type": "hp_regen", "value": 3}, {"type": "mp_regen", "value": 2}]},
         2: {"bonus_effects": [{"type": "hp_regen", "value": 2}, {"type": "mp_regen", "value": 1}]},
         3: {"bonus_effects": [{"type": "hp_regen", "value": 1}]},
     }},
    {"id": "thorned", "name": "Thorned", "kind": "effect",
     "slots": ["armor"],
     "tiers": {
         1: {"bonus_effects": [{"type": "thorns", "value": 0.10}]},
         2: {"bonus_effects": [{"type": "thorns", "value": 0.05}]},
     }},
    {"id": "warded", "name": "Warded", "kind": "effect",
     "slots": ["armor", "weapon"],
     "weapon_filter": ["shield"],
     "tiers": {
         1: {"bonus_effects": [{"type": "armor_bonus", "value": 6}]},
         2: {"bonus_effects": [{"type": "armor_bonus", "value": 4}]},
         3: {"bonus_effects": [{"type": "armor_bonus", "value": 2}]},
     }},
    {"id": "evasive", "name": "Evasive", "kind": "effect",
     "slots": ["armor"],
     "armor_filter": ["light", "leather"],
     "tiers": {
         1: {"bonus_effects": [{"type": "evasion", "value": 6}]},
         2: {"bonus_effects": [{"type": "evasion", "value": 4}]},
         3: {"bonus_effects": [{"type": "evasion", "value": 2}]},
     }},
]

# ============================================================
# Suffix Definitions
# ============================================================
SUFFIXES: list[dict] = [
    # --- Animal suffixes (all slots, stat-based, T1-T5) ---
    {"id": "of_the_bear", "name": "of the Bear", "kind": "stat",
     "slots": ["weapon", "armor", "accessory"],
     "tiers": {
         1: {"vitality": [9, 14]},
         2: {"vitality": [6, 9]},
         3: {"vitality": [4, 6]},
         4: {"vitality": [2, 4]},
         5: {"vitality": [1, 2]},
     }},
    {"id": "of_the_wolf", "name": "of the Wolf", "kind": "stat",
     "slots": ["weapon", "armor", "accessory"],
     "tiers": {
         1: {"might": [9, 14]},
         2: {"might": [6, 9]},
         3: {"might": [4, 6]},
         4: {"might": [2, 4]},
         5: {"might": [1, 2]},
     }},
    {"id": "of_the_fox", "name": "of the Fox", "kind": "stat",
     "slots": ["weapon", "armor", "accessory"],
     "tiers": {
         1: {"grace": [9, 14]},
         2: {"grace": [6, 9]},
         3: {"grace": [4, 6]},
         4: {"grace": [2, 4]},
         5: {"grace": [1, 2]},
     }},
    {"id": "of_the_owl", "name": "of the Owl", "kind": "stat",
     "slots": ["weapon", "armor", "accessory"],
     "tiers": {
         1: {"insight": [9, 14]},
         2: {"insight": [6, 9]},
         3: {"insight": [4, 6]},
         4: {"insight": [2, 4]},
         5: {"insight": [1, 2]},
     }},
    {"id": "of_the_serpent", "name": "of the Serpent", "kind": "stat",
     "slots": ["weapon", "armor", "accessory"],
     "tiers": {
         1: {"essence": [9, 14]},
         2: {"essence": [6, 9]},
         3: {"essence": [4, 6]},
         4: {"essence": [2, 4]},
         5: {"essence": [1, 2]},
     }},
    {"id": "of_the_turtle", "name": "of the Turtle", "kind": "stat",
     "slots": ["weapon", "armor", "accessory"],
     "tiers": {
         1: {"durability": [9, 14]},
         2: {"durability": [6, 9]},
         3: {"durability": [4, 6]},
         4: {"durability": [2, 4]},
         5: {"durability": [1, 2]},
     }},
    {"id": "of_the_eagle", "name": "of the Eagle", "kind": "stat",
     "slots": ["weapon", "armor", "accessory"],
     "tiers": {
         1: {"cognition": [9, 14]},
         2: {"cognition": [6, 9]},
         3: {"cognition": [4, 6]},
         4: {"cognition": [2, 4]},
         5: {"cognition": [1, 2]},
     }},

    # --- Effect suffixes (T1-T3) ---
    {"id": "of_precision", "name": "of Precision", "kind": "effect",
     "slots": ["weapon", "armor", "accessory"],
     "tiers": {
         1: {"bonus_effects": [{"type": "crit_chance", "value": 0.06}]},
         2: {"bonus_effects": [{"type": "crit_chance", "value": 0.04}]},
         3: {"bonus_effects": [{"type": "crit_chance", "value": 0.02}]},
     }},
    {"id": "of_fury", "name": "of Fury", "kind": "effect",
     "slots": ["weapon", "accessory"],
     "tiers": {
         1: {"bonus_effects": [{"type": "crit_damage", "value": 0.15}]},
         2: {"bonus_effects": [{"type": "crit_damage", "value": 0.10}]},
         3: {"bonus_effects": [{"type": "crit_damage", "value": 0.05}]},
     }},
    {"id": "of_vampirism", "name": "of Vampirism", "kind": "effect",
     "slots": ["weapon"],
     "tiers": {
         1: {"bonus_effects": [{"type": "lifesteal", "value": 0.08}]},
         2: {"bonus_effects": [{"type": "lifesteal", "value": 0.05}]},
     }},
    {"id": "of_warding", "name": "of Warding", "kind": "effect",
     "slots": ["weapon", "armor", "accessory"],
     "tiers": {
         1: {"bonus_effects": [{"type": "armor_bonus", "value": 6}]},
         2: {"bonus_effects": [{"type": "armor_bonus", "value": 4}]},
         3: {"bonus_effects": [{"type": "armor_bonus", "value": 2}]},
     }},
    {"id": "of_evasion", "name": "of Evasion", "kind": "effect",
     "slots": ["weapon", "armor", "accessory"],
     "tiers": {
         1: {"bonus_effects": [{"type": "evasion", "value": 6}]},
         2: {"bonus_effects": [{"type": "evasion", "value": 4}]},
         3: {"bonus_effects": [{"type": "evasion", "value": 2}]},
     }},
    {"id": "of_haste", "name": "of Haste", "kind": "effect",
     "slots": ["armor", "accessory"],
     "armor_filter": ["feet"],
     "tiers": {
         1: {"bonus_effects": [{"type": "action_speed", "value": 0.06}]},
         2: {"bonus_effects": [{"type": "action_speed", "value": 0.04}]},
     }},
    {"id": "of_regen", "name": "of Regen", "kind": "effect",
     "slots": ["weapon", "armor", "accessory"],
     "tiers": {
         1: {"bonus_effects": [{"type": "hp_regen", "value": 3}, {"type": "mp_regen", "value": 2}]},
         2: {"bonus_effects": [{"type": "hp_regen", "value": 2}, {"type": "mp_regen", "value": 1}]},
         3: {"bonus_effects": [{"type": "hp_regen", "value": 1}]},
     }},
    {"id": "of_thorns", "name": "of Thorns", "kind": "effect",
     "slots": ["armor"],
     "tiers": {
         1: {"bonus_effects": [{"type": "thorns", "value": 0.10}]},
         2: {"bonus_effects": [{"type": "thorns", "value": 0.05}]},
     }},
    {"id": "of_resilience", "name": "of Resilience", "kind": "effect",
     "slots": ["weapon", "armor", "accessory"],
     "tiers": {
         1: {"bonus_effects": [{"type": "status_resist", "value": 0.08}]},
         2: {"bonus_effects": [{"type": "status_resist", "value": 0.05}]},
         3: {"bonus_effects": [{"type": "status_resist", "value": 0.03}]},
     }},
    {"id": "of_piercing", "name": "of Piercing", "kind": "effect",
     "slots": ["weapon"],
     "tiers": {
         1: {"bonus_effects": [{"type": "armor_pen", "value": 0.08}]},
         2: {"bonus_effects": [{"type": "armor_pen", "value": 0.05}]},
     }},
    {"id": "of_the_giant", "name": "of the Giant", "kind": "stat",
     "slots": ["weapon", "armor", "accessory"],
     "tiers": {
         1: {"might": [3, 5], "grace": [3, 5], "insight": [3, 5]},
         2: {"might": [2, 3], "grace": [2, 3], "insight": [2, 3]},
     }},
    {"id": "of_the_titan", "name": "of the Titan", "kind": "stat",
     "slots": ["weapon", "armor", "accessory"],
     "tiers": {
         1: {"might": [2, 3], "grace": [2, 3], "insight": [2, 3], "vitality": [2, 3], "essence": [2, 3], "durability": [2, 3], "cognition": [2, 3]},
     }},
    {"id": "of_slaying", "name": "of Slaying", "kind": "effect",
     "slots": ["weapon"],
     "tiers": {
         1: {"bonus_effects": [{"type": "damage_vs_species", "species": "beast", "value": 0.15}]},
         2: {"bonus_effects": [{"type": "damage_vs_species", "species": "beast", "value": 0.10}]},
     }},
]

# ============================================================
# Build lookup dict
# ============================================================
AFFIXES_BY_ID: dict[str, dict] = {}
for p in PREFIXES:
    AFFIXES_BY_ID[p["id"]] = p
for s in SUFFIXES:
    AFFIXES_BY_ID[s["id"]] = s

# ============================================================
# Helper: get affixes valid for a given base item
# ============================================================
def get_valid_prefixes(base_item: dict) -> list[dict]:
    """Return prefixes that can roll on this base item."""
    kind = base_item.get("kind", "")
    slot = base_item.get("slot", "")
    weapon_type = base_item.get("weapon_type", "")
    armor_type = base_item.get("armor_type", "")

    valid = []
    for pfx in PREFIXES:
        if kind not in pfx.get("slots", []):
            continue
        # Check weapon_filter
        if kind == "weapon" and "weapon_filter" in pfx:
            if weapon_type not in pfx["weapon_filter"]:
                continue
        # Check armor_filter (by armor_type or slot)
        if kind == "armor" and "armor_filter" in pfx:
            af = pfx["armor_filter"]
            if armor_type not in af and slot not in af:
                continue
        valid.append(pfx)
    return valid

def get_valid_suffixes(base_item: dict) -> list[dict]:
    """Return suffixes that can roll on this base item."""
    kind = base_item.get("kind", "")
    slot = base_item.get("slot", "")
    weapon_type = base_item.get("weapon_type", "")
    armor_type = base_item.get("armor_type", "")

    valid = []
    for sfx in SUFFIXES:
        if kind not in sfx.get("slots", []):
            continue
        if kind == "weapon" and "weapon_filter" in sfx:
            if weapon_type not in sfx["weapon_filter"]:
                continue
        if kind == "armor" and "armor_filter" in sfx:
            af = sfx["armor_filter"]
            if armor_type not in af and slot not in af:
                continue
        valid.append(sfx)
    return valid

# ============================================================
# Helper: get tier for a given monster level
# ============================================================
def get_tier_for_level(level: int) -> int:
    """Return the affix tier number for a given monster level. T1=highest (40+), T5=lowest (1-5)."""
    if level >= 40:
        return 1
    elif level >= 25:
        return 2
    elif level >= 15:
        return 3
    elif level >= 6:
        return 4
    else:
        return 5

# ============================================================
# Helper: roll affix stat values for a tier
# ============================================================
def roll_affix_stats(affix: dict, tier: int) -> dict:
    """Roll random stat values within the affix's tier range."""
    import random
    tier_data = affix.get("tiers", {}).get(tier)
    if not tier_data:
        # Fall back to closest available tier
        available_tiers = sorted(affix.get("tiers", {}).keys())
        if not available_tiers:
            return {}
        # Find closest tier
        tier_data = affix["tiers"][available_tiers[0]]
        for at in available_tiers:
            if at <= tier:
                tier_data = affix["tiers"][at]

    result = {}
    for key, val in tier_data.items():
        if key == "bonus_effects":
            result["bonus_effects"] = val
        elif isinstance(val, list) and len(val) == 2:
            result[key] = random.randint(val[0], val[1])
        elif isinstance(val, (int, float)):
            result[key] = val
    return result
