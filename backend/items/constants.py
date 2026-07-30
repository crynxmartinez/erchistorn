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
    "light":   {"label": "Light",   "desc": "Cloth and robes. Favors casters — high grace and insight."},
    "leather": {"label": "Leather", "desc": "Hide and scale. Balanced — vitality and might."},
    "heavy":   {"label": "Heavy",   "desc": "Plate and iron. Tank — high vitality and durability."},
}

# ============================================================
# Equipment Slots
# ============================================================
EQUIP_SLOTS: list[str] = [
    "head", "body", "left_hand", "right_hand",
    "legs", "feet", "earring_l", "earring_r",
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
