"""Drop generation engine — rolls rarity, picks base item, rolls affixes, builds item instance.
This is the core procedural item generation system (Diablo/PoE-style).
"""
from __future__ import annotations
import random
import uuid

from .constants import (
    WEAPON_TYPES, RARITY_WEIGHTS, RARITY_WEIGHTS_DEFAULT,
    AFFIX_SLOTS_BY_RARITY, MAX_UPGRADES,
)
from .base_items import BASE_ITEMS, BASE_ITEMS_BY_ID, get_weapon_range, is_two_handed
from .affixes import (
    PREFIXES, SUFFIXES, get_valid_prefixes, get_valid_suffixes,
    get_tier_for_level, roll_affix_stats,
)
from .uniques import UNIQUE_ITEMS, UNIQUE_ITEMS_BY_ID
from .sets import SET_ITEMS, SET_ITEMS_BY_ID, SET_BONUSES
from .legendaries import LEGENDARY_POWERS


# ============================================================
# Rarity Rolling
# ============================================================
def roll_rarity(monster_rarity: str, creature_tier: str, luck_bonus: float = 0.0) -> str:
    """Roll item rarity based on monster rarity and creature tier.
    luck_bonus: 0.0-0.20, shifts weight toward higher rarities.
    """
    key = (monster_rarity, creature_tier)
    weights = RARITY_WEIGHTS.get(key, RARITY_WEIGHTS_DEFAULT)

    # Apply luck bonus: shift weight from normal/magic to higher rarities
    if luck_bonus > 0:
        weights = dict(weights)  # copy
        shift = luck_bonus
        for low in ("normal", "magic"):
            if low in weights and weights[low] > 0:
                moved = min(weights[low], int(shift * 100))
                weights[low] = weights[low] - moved
                # Distribute to higher rarities
                for high in ("rare", "unique", "set", "legendary"):
                    if high in weights:
                        weights[high] = weights[high] + moved // 3
                        break

    rarities = list(weights.keys())
    weight_vals = [max(0, w) for w in weights.values()]
    return random.choices(rarities, weights=weight_vals, k=1)[0]


# ============================================================
# Affix Rolling
# ============================================================
def roll_affixes(base_item: dict, rarity: str, monster_level: int) -> tuple[list[dict], list[dict]]:
    """Roll prefixes and suffixes for a base item based on rarity and monster level.
    Returns (prefixes, suffixes) lists of rolled affix dicts.
    """
    tier = get_tier_for_level(monster_level)
    slots = AFFIX_SLOTS_BY_RARITY.get(rarity, AFFIX_SLOTS_BY_RARITY["normal"])

    n_prefix = random.randint(slots["prefix_min"], slots["prefix_max"])
    n_suffix = random.randint(slots["suffix_min"], slots["suffix_max"])

    valid_prefixes = get_valid_prefixes(base_item)
    valid_suffixes = get_valid_suffixes(base_item)

    # Don't roll the same affix twice
    chosen_prefixes = []
    used_prefix_ids = set()
    for _ in range(n_prefix):
        available = [p for p in valid_prefixes if p["id"] not in used_prefix_ids]
        if not available:
            break
        pfx = random.choice(available)
        used_prefix_ids.add(pfx["id"])
        rolled = roll_affix_stats(pfx, tier)
        chosen_prefixes.append({
            "id": pfx["id"], "name": pfx["name"], "tier": tier,
            **rolled,
        })

    chosen_suffixes = []
    used_suffix_ids = set()
    for _ in range(n_suffix):
        available = [s for s in valid_suffixes if s["id"] not in used_suffix_ids]
        if not available:
            break
        sfx = random.choice(available)
        used_suffix_ids.add(sfx["id"])
        rolled = roll_affix_stats(sfx, tier)
        chosen_suffixes.append({
            "id": sfx["id"], "name": sfx["name"], "tier": tier,
            **rolled,
        })

    return chosen_prefixes, chosen_suffixes


# ============================================================
# Item Instance Builder
# ============================================================
def build_item_instance(
    base_item: dict,
    prefixes: list[dict],
    suffixes: list[dict],
    quality: int,
    rarity: str,
    set_id: str | None = None,
    legendary_power: str | None = None,
    fixed_bonus_effects: list[dict] | None = None,
    instance_id: str | None = None,
) -> dict:
    """Build a complete item instance from base + affixes + quality."""
    # Generate instance ID
    if instance_id is None:
        instance_id = f"item_{uuid.uuid4().hex[:12]}"

    # Build name: [Prefix] + [Base Name] + [Suffix]
    name_parts = []
    if prefixes:
        name_parts.append(prefixes[0]["name"])
    name_parts.append(base_item["name"])
    if suffixes:
        name_parts.append(suffixes[0]["name"])
    name = " ".join(name_parts)

    # Compute range and two_handed from weapon_type
    weapon_type = base_item.get("weapon_type")
    range_val = get_weapon_range(weapon_type) if weapon_type else 0
    two_handed = is_two_handed(weapon_type) if weapon_type else False

    # Collect bonus effects from affixes
    bonus_effects = list(fixed_bonus_effects or [])
    for affix in prefixes + suffixes:
        if "bonus_effects" in affix:
            bonus_effects.extend(affix["bonus_effects"])

    # Collect all stats
    base_stats = dict(base_item.get("base_stats", {}))

    # Apply quality boost to base stats
    if quality > 0:
        for stat, val in base_stats.items():
            base_stats[stat] = int(val * (1 + quality / 100))

    # Build the instance
    item = {
        "instance_id": instance_id,
        "base_id": base_item["id"],
        "name": name,
        "kind": base_item["kind"],
        "slot": base_item["slot"],
        "rarity": rarity,
        "quality": quality,
        "base_stats": base_stats,
        "prefixes": prefixes,
        "suffixes": suffixes,
        "bonus_effects": bonus_effects,
        "req_stats": dict(base_item.get("req_stats", {})),
        "req_level": base_item.get("req_level", 1),
        "desc": base_item.get("desc", ""),
        "identified": True,
        "corrupted": False,
        "crafted": False,
        "upgrades": {"gems": [], "runes": [], "count": 0, "max": MAX_UPGRADES},
    }

    # Weapon-specific fields
    if weapon_type:
        item["weapon_type"] = weapon_type
        item["range"] = range_val
        item["two_handed"] = two_handed

    # Armor-specific fields
    if base_item.get("armor_type"):
        item["armor_type"] = base_item["armor_type"]

    # Set/legendary
    if set_id:
        item["set_id"] = set_id
    if legendary_power:
        item["legendary_power"] = legendary_power

    return item


# ============================================================
# Build Fixed Item (unique/set/legendary/mythic)
# ============================================================
def build_fixed_item(template: dict, rarity: str) -> dict:
    """Build a unique or set item from its fixed template."""
    base_id = template["base_id"]
    base_item = BASE_ITEMS_BY_ID.get(base_id)
    if not base_item:
        # If base item not found, use the template directly as base
        base_item = {
            "id": template["id"],
            "name": template["name"],
            "kind": template.get("kind", "weapon"),
            "slot": template.get("slot", "right_hand"),
            "weapon_type": template.get("weapon_type"),
            "armor_type": template.get("armor_type"),
            "base_stats": template.get("base_stats", {}),
            "req_stats": template.get("req_stats", {}),
            "req_level": template.get("req_level", 1),
            "desc": template.get("desc", ""),
        }

    # Use fixed affixes from template
    prefixes = template.get("fixed_prefixes", [])
    suffixes = template.get("fixed_suffixes", [])

    # Build with fixed quality (uniques get 10%)
    quality = template.get("quality", 10)

    item = build_item_instance(
        base_item=base_item,
        prefixes=prefixes,
        suffixes=suffixes,
        quality=quality,
        rarity=rarity,
        set_id=template.get("set_id"),
        legendary_power=template.get("legendary_power"),
        fixed_bonus_effects=template.get("bonus_effects", []),
        instance_id=f"item_{uuid.uuid4().hex[:12]}",
    )

    # Override name with the unique/set name
    item["name"] = template["name"]
    item["desc"] = template.get("desc", base_item.get("desc", ""))

    # Override req if template specifies
    if "req_stats" in template:
        item["req_stats"] = template["req_stats"]
    if "req_level" in template:
        item["req_level"] = template["req_level"]

    return item


# ============================================================
# Main Drop Generator
# ============================================================
def generate_drop(
    monster: dict,
    character_luck: float = 0.0,
    monster_level: int | None = None,
) -> dict | None:
    """Generate a random item drop from a monster.
    Returns an item instance dict, or None if no drop.
    """
    monster_rarity = monster.get("rarity", "common")
    creature_tier = monster.get("creature_tier", "normal")
    drops = monster.get("drops", {})

    # Check if gear drops at all
    gear_drop_chance = drops.get("gear_drop_chance", 0.15)
    if random.random() > gear_drop_chance:
        return None

    # Determine monster level for affix tier
    if monster_level is None:
        # Estimate from monster stats base values
        stats = monster.get("stats", {})
        might_base = stats.get("might", {}).get("base", 5) if isinstance(stats.get("might"), dict) else 5
        monster_level = max(1, might_base - 5)

    # Roll rarity
    rarity = roll_rarity(monster_rarity, creature_tier, character_luck)

    # Handle fixed-rarity items (unique/set/legendary/mythic)
    if rarity in ("unique", "legendary", "mythic"):
        # Pick a random unique item
        if UNIQUE_ITEMS:
            template = random.choice(UNIQUE_ITEMS)
            return build_fixed_item(template, rarity)
        else:
            rarity = "rare"  # fallback

    if rarity == "set":
        # Pick a random set item
        if SET_ITEMS:
            template = random.choice(SET_ITEMS)
            return build_fixed_item(template, "set")
        else:
            rarity = "rare"  # fallback

    # For normal/magic/rare: pick base item from gear pool and roll affixes
    gear_pool = drops.get("gear_pool", [])
    if not gear_pool:
        # Fallback: pick any base item
        base_item = random.choice(BASE_ITEMS)
    else:
        base_id = random.choice(gear_pool)
        base_item = BASE_ITEMS_BY_ID.get(base_id)
        if not base_item:
            base_item = random.choice(BASE_ITEMS)

    # Roll affixes
    prefixes, suffixes = roll_affixes(base_item, rarity, monster_level)

    # Roll quality (0-10)
    quality = random.randint(0, 10)

    # Build instance
    return build_item_instance(base_item, prefixes, suffixes, quality, rarity)


# ============================================================
# Generate Rune Drop
# ============================================================
def generate_rune_drop(monster: dict) -> dict | None:
    """Generate a random rune drop from a monster.
    Returns a rune dict (not an item instance — runes are inventory items).
    Rarity ranges from rare to legendary based on creature tier.
    """
    from .runes import RUNES

    creature_tier = monster.get("creature_tier", "normal")

    # Rarity weights by creature tier — always rare or better
    rarity_weights = {
        "normal":     {"rare": 80, "epic": 18, "legendary": 2},
        "mini_boss":  {"rare": 55, "epic": 35, "legendary": 10},
        "boss":       {"rare": 30, "epic": 45, "legendary": 25},
        "legendary":  {"rare": 10, "epic": 35, "legendary": 55},
        "event":      {"rare": 5,  "epic": 25, "legendary": 70},
    }

    weights = rarity_weights.get(creature_tier, rarity_weights["normal"])
    _total = sum(weights.values())
    _roll = random.randint(1, _total)
    _cumulative = 0
    rarity = "rare"
    for _r, _w in weights.items():
        _cumulative += _w
        if _roll <= _cumulative:
            rarity = _r
            break

    # Value multiplier by rarity — higher rarity = stronger rune
    value_mult = {"rare": 1.0, "epic": 2.0, "legendary": 3.0}.get(rarity, 1.0)

    rune = random.choice(RUNES)
    return {
        "id": rune["id"],
        "name": rune["name"],
        "kind": "rune",
        "effect_type": rune["effect_type"],
        "value": round(rune["value"] * value_mult, 4),
        "desc": rune["desc"],
        "rarity": rarity,
    }


# ============================================================
# Compute Total Stats from Item Instance
# ============================================================
def compute_item_total_stats(item: dict) -> dict[str, int]:
    """Compute the total stats an item provides (base + affixes + gems + quality)."""
    total: dict[str, int] = {}

    # Base stats (already quality-boosted at build time)
    for stat, val in item.get("base_stats", {}).items():
        total[stat] = total.get(stat, 0) + val

    # Prefix stats
    for pfx in item.get("prefixes", []):
        for key, val in pfx.items():
            if key in ("id", "name", "tier", "bonus_effects"):
                continue
            if isinstance(val, (int, float)):
                total[key] = total.get(key, 0) + int(val)

    # Suffix stats
    for sfx in item.get("suffixes", []):
        for key, val in sfx.items():
            if key in ("id", "name", "tier", "bonus_effects"):
                continue
            if isinstance(val, (int, float)):
                total[key] = total.get(key, 0) + int(val)

    # Gem upgrades (flat +1 each)
    for gem in item.get("upgrades", {}).get("gems", []):
        stat = gem.get("stat")
        if stat:
            total[stat] = total.get(stat, 0) + gem.get("value", 1)

    return total


# ============================================================
# Compute Total Bonus Effects from Item Instance
# ============================================================
def compute_item_bonus_effects(item: dict) -> list[dict]:
    """Compute all bonus effects from an item (affixes + fixed + runes)."""
    effects = list(item.get("bonus_effects", []))

    # Rune upgrades (+1% each)
    for rune in item.get("upgrades", {}).get("runes", []):
        effects.append({
            "type": rune.get("effect_type"),
            "value": rune.get("value", 0.01),
        })

    return effects
