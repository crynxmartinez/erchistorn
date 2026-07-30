"""Upgrade system — socket gems and runes into items.
Gems give flat +1 stat. Runes give +1% bonus effect.
Items have a max of 10 upgrades (any mix of gems + runes).
Gems and runes are consumed on socket — cannot be removed.
"""
from __future__ import annotations

from .constants import MAX_UPGRADES
from .gems import GEMS_BY_ID
from .runes import RUNES_BY_ID


def get_upgrade_count(item: dict) -> int:
    """Get the current number of upgrades on an item."""
    upgrades = item.get("upgrades", {})
    return upgrades.get("count", len(upgrades.get("gems", [])) + len(upgrades.get("runes", [])))


def can_upgrade(item: dict) -> bool:
    """Check if an item can receive more upgrades."""
    return get_upgrade_count(item) < MAX_UPGRADES


def socket_gem(item: dict, gem_id: str) -> tuple[bool, str]:
    """Socket a gem into an item. Returns (success, message).
    The gem is consumed (caller must remove from inventory).
    """
    if not can_upgrade(item):
        return False, "Item has reached maximum upgrades (10/10)."

    gem = GEMS_BY_ID.get(gem_id)
    if not gem:
        return False, f"Unknown gem: {gem_id}"

    # Initialize upgrades dict if missing
    if "upgrades" not in item:
        item["upgrades"] = {"gems": [], "runes": [], "count": 0, "max": MAX_UPGRADES}

    # Add gem to socket
    item["upgrades"]["gems"].append({
        "gem_id": gem_id,
        "stat": gem["stat"],
        "value": gem["value"],
    })
    item["upgrades"]["count"] = get_upgrade_count(item)

    return True, f"Socketed {gem['name']} (+1 {gem['stat']}). Upgrades: {get_upgrade_count(item)}/10."


def socket_rune(item: dict, rune_id: str) -> tuple[bool, str]:
    """Socket a rune into an item. Returns (success, message).
    The rune is consumed (caller must remove from inventory).
    """
    if not can_upgrade(item):
        return False, "Item has reached maximum upgrades (10/10)."

    rune = RUNES_BY_ID.get(rune_id)
    if not rune:
        return False, f"Unknown rune: {rune_id}"

    # Initialize upgrades dict if missing
    if "upgrades" not in item:
        item["upgrades"] = {"gems": [], "runes": [], "count": 0, "max": MAX_UPGRADES}

    # Add rune to socket
    item["upgrades"]["runes"].append({
        "rune_id": rune_id,
        "type": rune["effect_type"],
        "value": rune["value"],
    })
    item["upgrades"]["count"] = get_upgrade_count(item)

    return True, f"Socketed {rune['name']} (+1% {rune['effect_type']}). Upgrades: {get_upgrade_count(item)}/10."


def get_upgrade_summary(item: dict) -> dict:
    """Get a summary of upgrades on an item for display."""
    upgrades = item.get("upgrades", {"gems": [], "runes": [], "count": 0, "max": MAX_UPGRADES})
    return {
        "count": upgrades.get("count", 0),
        "max": MAX_UPGRADES,
        "gems": upgrades.get("gems", []),
        "runes": upgrades.get("runes", []),
        "remaining": MAX_UPGRADES - upgrades.get("count", 0),
    }
