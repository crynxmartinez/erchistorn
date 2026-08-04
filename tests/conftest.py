"""Pytest configuration and shared fixtures for the Erchistorn engine tests.

These are pure unit tests over the game engine's arithmetic. They do not need
Mongo, a running server, or network access — everything imported here is
deterministic data + pure functions.
"""
from __future__ import annotations

import os
import sys

import pytest

# The backend package is not installed; add it to sys.path so `import game_data`
# and `import game_engine` resolve the same way they do under uvicorn.
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_BACKEND = os.path.join(_REPO_ROOT, "backend")
if _BACKEND not in sys.path:
    sys.path.insert(0, _BACKEND)

# auth.py reads JWT_SECRET at call time, but importing server would require it.
# Set a dummy so any incidental import doesn't explode.
os.environ.setdefault("JWT_SECRET", "test-secret-not-used")


# ============================================================
# Character builders
# ============================================================

def make_character(
    *,
    level: int = 1,
    mastery: str = "knight",
    role: str = "fighter",
    race: str = "human",
    base_stats: dict | None = None,
    equipped_bases: dict | None = None,
    equipped_instances: list[dict] | None = None,
) -> dict:
    """Build a character dict with real item instances in the given slots.

    equipped_bases: {slot: base_item_id} — each is built into a real instance
    via build_item_instance, exactly as character creation and drops do.
    equipped_instances: pre-built instances to place in their own `slot`.
    """
    import game_data as g
    from items.constants import EQUIP_SLOTS

    stats = {"vitality": 5, "cognition": 3, "essence": 3, "durability": 5,
             "might": 0, "grace": 0, "insight": 0, "resilience": 0,
             "armor_bonus": 0, "evasion_mod": 0, "attack_success_mod": 0}
    if base_stats:
        stats.update(base_stats)

    equipped = {slot: None for slot in EQUIP_SLOTS}
    instances: list[dict] = []
    inventory: list[dict] = []

    for slot, base_id in (equipped_bases or {}).items():
        base = g.BASE_ITEMS_BY_ID.get(base_id)
        assert base is not None, f"unknown base item {base_id!r}"
        inst = g.build_item_instance(base, [], [], quality=0, rarity="normal")
        instances.append(inst)
        equipped[slot] = inst["instance_id"]
        inventory.append({"item_id": inst["instance_id"], "quantity": 1})

    for inst in (equipped_instances or []):
        instances.append(inst)
        equipped[inst["slot"]] = inst["instance_id"]
        inventory.append({"item_id": inst["instance_id"], "quantity": 1})

    ch = {
        "level": level,
        "mastery": mastery,
        # The engine's mastery gates (`_is_mage`, `_is_hunter`, ...) all read the
        # `masteries` LIST, not the singular `mastery` field. Character creation
        # sets both, so tests must too or every mastery mechanic silently no-ops.
        "masteries": [mastery],
        "role": role,
        "race": race,
        "base_stats": dict(stats),
        "stats": dict(stats),
        "equipped": equipped,
        "item_instances": instances,
        "inventory": inventory,
        "statuses": [],
        "skills": [],
        "hp": 100,
        "max_hp": 100,
        "xp": 0,
    }
    recompute(ch)
    return ch


def recompute(ch: dict) -> dict:
    """Recompute effective stats from base_stats + gear, mutating in place."""
    import game_engine as ge
    ch["stats"] = ge.apply_enchantments_to_stats(ch)
    return ch


def make_set_loadout(set_id: str, n_set_pieces: int, n_filler: int = 0) -> dict:
    """Character wearing n_set_pieces of `set_id` plus n_filler unrelated items.

    Uses synthetic instances so the test controls piece count exactly and does
    not depend on which real base items happen to carry a set_id.
    """
    slots = ["head", "body", "legs", "feet", "neck", "back", "ring_l", "ring_r"]
    assert n_set_pieces + n_filler <= len(slots), "not enough slots for loadout"

    instances = []
    for i in range(n_set_pieces):
        instances.append({
            "instance_id": f"set_{i}", "slot": slots[i], "set_id": set_id,
            "base_stats": {}, "prefixes": [], "suffixes": [], "upgrades": {},
            "kind": "armor", "rarity": "set",
        })
    for j in range(n_filler):
        instances.append({
            "instance_id": f"filler_{j}", "slot": slots[n_set_pieces + j],
            "base_stats": {}, "prefixes": [], "suffixes": [], "upgrades": {},
            "kind": "armor", "rarity": "normal",
        })

    return make_character(
        base_stats={"might": 0, "vitality": 0, "grace": 0, "insight": 0},
        equipped_instances=instances,
    )


# ============================================================
# Fixtures
# ============================================================

@pytest.fixture
def gd():
    import game_data
    return game_data


@pytest.fixture
def ge():
    import game_engine
    return game_engine


@pytest.fixture
def naked_knight():
    return make_character(mastery="knight", role="fighter")


@pytest.fixture
def plated_knight():
    """Level-1 Knight in the full starter plate set, as character creation grants it."""
    import game_data as g
    gear = g.STARTER_GEAR_BY_MASTERY["knight"]
    bases = {"right_hand": gear["weapon"], "left_hand": gear["shield"]}
    for armor_id in gear["armor"]:
        base = g.BASE_ITEMS_BY_ID.get(armor_id)
        if base:
            bases[base["slot"]] = armor_id
    return make_character(mastery="knight", role="fighter", equipped_bases=bases)
