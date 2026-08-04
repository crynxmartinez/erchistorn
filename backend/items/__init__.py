"""Item system module — procedural item generation, affixes, gems, runes, sets, uniques."""
from .constants import (
    WEAPON_TYPES,
    ARMOR_TYPES,
    EQUIP_SLOTS,
    RARITY_WEIGHTS,
    AFFIX_TIERS,
    ITEM_RARITIES,
    MAX_UPGRADES,
    ARMOR_BONUS_BY_TYPE_TIER,
    MAGIC_RESIST_BY_TYPE_TIER,
    ARMOR_SLOT_MULT,
    SHIELD_ARMOR_BY_TIER,
    ARMOR_PER_RESILIENCE,
)
from .base_items import BASE_ITEMS, BASE_ITEMS_BY_ID
from .affixes import PREFIXES, SUFFIXES, AFFIXES_BY_ID
from .gems import GEMS, GEMS_BY_ID
from .runes import RUNES, RUNES_BY_ID
from .uniques import UNIQUE_ITEMS, UNIQUE_ITEMS_BY_ID
from .sets import SET_BONUSES, SET_ITEMS, SET_ITEMS_BY_ID
from .legendaries import LEGENDARY_POWERS
from .generator import (
    generate_drop, generate_rune_drop, build_item_instance,
    roll_rarity, roll_affixes, compute_item_total_stats, compute_item_bonus_effects,
)
from .upgrades import socket_gem, socket_rune, get_upgrade_count, can_upgrade, get_upgrade_summary

__all__ = [
    "WEAPON_TYPES", "ARMOR_TYPES", "EQUIP_SLOTS", "RARITY_WEIGHTS",
    "AFFIX_TIERS", "ITEM_RARITIES", "MAX_UPGRADES",
    "ARMOR_BONUS_BY_TYPE_TIER", "MAGIC_RESIST_BY_TYPE_TIER",
    "ARMOR_SLOT_MULT", "SHIELD_ARMOR_BY_TIER", "ARMOR_PER_RESILIENCE",
    "BASE_ITEMS", "BASE_ITEMS_BY_ID",
    "PREFIXES", "SUFFIXES", "AFFIXES_BY_ID",
    "GEMS", "GEMS_BY_ID",
    "RUNES", "RUNES_BY_ID",
    "UNIQUE_ITEMS", "UNIQUE_ITEMS_BY_ID",
    "SET_BONUSES", "SET_ITEMS", "SET_ITEMS_BY_ID",
    "LEGENDARY_POWERS",
    "generate_drop", "generate_rune_drop", "build_item_instance",
    "roll_rarity", "roll_affixes",
    "compute_item_total_stats", "compute_item_bonus_effects",
    "socket_gem", "socket_rune", "get_upgrade_count", "can_upgrade", "get_upgrade_summary",
]
