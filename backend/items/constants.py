"""Item system constants — weapon types, armor types, equip slots, rarity weights, affix tiers."""

# ============================================================
# Weapon Types
# ============================================================
WEAPON_TYPES: dict[str, dict] = {
    "dagger":      {"label": "Dagger",            "hands": 1, "range": 0, "two_handed": False},
    "sword_1h":    {"label": "Sword (1H)",        "hands": 1, "range": 0, "two_handed": False},
    "sword_2h":    {"label": "Sword (2H)",        "hands": 2, "range": 0, "two_handed": True},
    "axe_1h":      {"label": "Axe (1H)",          "hands": 1, "range": 0, "two_handed": False},
    "great_axe":   {"label": "Great Axe (2H)",    "hands": 2, "range": 1, "two_handed": True},
    "hammer_1h":   {"label": "Hammer (1H)",       "hands": 1, "range": 0, "two_handed": False},
    "great_hammer":{"label": "Great Hammer (2H)", "hands": 2, "range": 1, "two_handed": True},
    "spear":       {"label": "Spear (2H)",        "hands": 2, "range": 1, "two_handed": True},
    "scythe":      {"label": "Scythe (2H)",       "hands": 2, "range": 1, "two_handed": True},
    "katar":       {"label": "Katar (2H, dual)",  "hands": 2, "range": 0, "two_handed": True},
    "orb":         {"label": "Orb (1H)",          "hands": 1, "range": 2, "two_handed": False},
    "tome":        {"label": "Tome (1H)",         "hands": 1, "range": 3, "two_handed": False},
    "instrument":  {"label": "Musical Instrument (2H)", "hands": 2, "range": 1, "two_handed": True},
    "bow":         {"label": "Bow (2H)",          "hands": 2, "range": 3, "two_handed": True},
    "crossbow":    {"label": "Crossbow (2H)",     "hands": 2, "range": 2, "two_handed": True},
    "shield":      {"label": "Shield (1H)",       "hands": 1, "range": 0, "two_handed": False},
}

# ============================================================
# Armor Types
# ============================================================
ARMOR_TYPES: dict[str, dict] = {
    "light":   {"label": "Light",   "desc": "Cloth and robes. Favors casters — high grace and insight, and the best magic resistance."},
    "leather": {"label": "Leather", "desc": "Hide and scale. Balanced — vitality and might, with even defenses."},
    "heavy":   {"label": "Heavy",   "desc": "Plate and iron. Tank — high vitality and durability, and the best armor."},
}

# ============================================================
# Defensive Values by Armor Type + Tier
# ============================================================
# Armor pieces grant `armor_bonus` (reduces physical damage) and `magic_resist`
# (reduces magical damage). The two scale in opposite directions across armor
# types, so the choice of armor_type is a real defensive trade-off rather than a
# stat-stick preference:
#
#   heavy   -> best armor,          worst magic resistance
#   leather -> balanced
#   light   -> worst armor,         best magic resistance
#
# Values are for a body piece; other slots scale by ARMOR_SLOT_MULT below.
#
# NOTE: before this table existed, `compute_armor` summed a `power` field that
# item instances never carry, and no base item or affix granted `armor_bonus` at
# all — so every character in the game had exactly 0 armor and took full
# physical damage in full plate. These tables are the fix.
ARMOR_BONUS_BY_TYPE_TIER: dict[tuple[str, int], int] = {
    ("light", 1): 4,   ("light", 2): 8,    ("light", 3): 14,
    ("leather", 1): 7, ("leather", 2): 13, ("leather", 3): 22,
    ("heavy", 1): 11,  ("heavy", 2): 20,   ("heavy", 3): 34,
}

MAGIC_RESIST_BY_TYPE_TIER: dict[tuple[str, int], int] = {
    ("light", 1): 6,   ("light", 2): 11,  ("light", 3): 18,
    ("leather", 1): 4, ("leather", 2): 7, ("leather", 3): 12,
    ("heavy", 1): 2,   ("heavy", 2): 4,   ("heavy", 3): 7,
}

# How much of a body piece's defense each slot carries.
ARMOR_SLOT_MULT: dict[str, float] = {
    "body": 1.0,
    "legs": 0.7,
    "head": 0.6,
    "feet": 0.45,
    "back": 0.45,
    "hands": 0.4,
}

# Shields are the archetypal armor source and are weapon-slot items, so they
# are keyed by tier directly rather than by armor_type.
SHIELD_ARMOR_BY_TIER: dict[int, int] = {1: 10, 2: 18, 3: 30}

# Each point of Resilience contributes this much armor. Resilience is granted by
# the Guardian role ("+2 Resilience, +1 defence rolls") and by level-up for
# defensive masteries. Before this, no formula in the game read the stat at all.
ARMOR_PER_RESILIENCE = 2

# ============================================================
# Equipment Slots
# ============================================================
EQUIP_SLOTS: list[str] = [
    "head", "body", "left_hand", "right_hand",
    "legs", "feet", "hands", "earring_l", "earring_r",
    "ring_l", "ring_r", "neck", "back",
]

# ============================================================
# Item Rarities
# ============================================================
ITEM_RARITIES: list[str] = [
    "normal", "magic", "rare", "unique", "set", "legendary", "mythic",
]

# ============================================================
# Rarity Weights by Monster Rarity + creature_tier
# ============================================================
# Format: (monster_rarity, creature_tier) -> {item_rarity: weight}
RARITY_WEIGHTS: dict[tuple[str, str], dict[str, int]] = {
    ("common", "normal"):        {"normal": 70, "magic": 25, "rare": 5,  "unique": 0,  "set": 0,  "legendary": 0,  "mythic": 0},
    ("uncommon", "normal"):      {"normal": 50, "magic": 35, "rare": 13, "unique": 2,  "set": 0,  "legendary": 0,  "mythic": 0},
    ("rare", "normal"):          {"normal": 30, "magic": 30, "rare": 30, "unique": 8,  "set": 2,  "legendary": 0,  "mythic": 0},
    ("rare", "mini_boss"):       {"normal": 20, "magic": 25, "rare": 35, "unique": 12, "set": 6,  "legendary": 2,  "mythic": 0},
    ("legendary", "normal"):     {"normal": 10, "magic": 15, "rare": 30, "unique": 25, "set": 15, "legendary": 5,  "mythic": 0},
    ("legendary", "boss"):       {"normal": 5,  "magic": 10, "rare": 20, "unique": 30, "set": 25, "legendary": 10, "mythic": 0},
    ("rare", "boss"):            {"normal": 5,  "magic": 10, "rare": 20, "unique": 30, "set": 25, "legendary": 10, "mythic": 0},
    ("legendary", "event"):      {"normal": 0,  "magic": 5,  "rare": 10, "unique": 25, "set": 30, "legendary": 25, "mythic": 5},
}

# Fallback for any combination not explicitly listed
RARITY_WEIGHTS_DEFAULT: dict[str, int] = {"normal": 60, "magic": 25, "rare": 10, "unique": 3, "set": 1.5, "legendary": 0.5, "mythic": 0.1}

# ============================================================
# Affix Tiers — based on monster/area level
# ============================================================
AFFIX_TIERS: list[dict] = [
    {"tier": 5, "level_min": 1,  "level_max": 5,  "label": "T5"},
    {"tier": 4, "level_min": 6,  "level_max": 14, "label": "T4"},
    {"tier": 3, "level_min": 15, "level_max": 24, "label": "T3"},
    {"tier": 2, "level_min": 25, "level_max": 39, "label": "T2"},
    {"tier": 1, "level_min": 40, "level_max": 99, "label": "T1"},
]

# ============================================================
# Upgrade System
# ============================================================
MAX_UPGRADES: int = 10

# ============================================================
# Affix Slots by Rarity
# ============================================================
AFFIX_SLOTS_BY_RARITY: dict[str, dict] = {
    "normal":    {"prefix_min": 0, "prefix_max": 0, "suffix_min": 0, "suffix_max": 0},
    "magic":     {"prefix_min": 0, "prefix_max": 1, "suffix_min": 1, "suffix_max": 1},
    "rare":      {"prefix_min": 1, "prefix_max": 2, "suffix_min": 1, "suffix_max": 2},
    "unique":    {"prefix_min": 0, "prefix_max": 0, "suffix_min": 0, "suffix_max": 0},  # fixed
    "set":       {"prefix_min": 0, "prefix_max": 0, "suffix_min": 0, "suffix_max": 0},  # fixed
    "legendary": {"prefix_min": 0, "prefix_max": 0, "suffix_min": 0, "suffix_max": 0},  # fixed
    "mythic":    {"prefix_min": 0, "prefix_max": 0, "suffix_min": 0, "suffix_max": 0},  # fixed
}
