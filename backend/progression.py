"""Character progression — XP curve and deterministic stat growth on level-up.

Extracted from server.py so it is importable and testable without Mongo.

Why this module exists
----------------------
Level-up used to do this:

    stat_keys = ["vitality", "cognition", "essence", "durability"]
    pick = random.choice(stat_keys)
    base[pick] = base.get(pick, 0) + 1

Two problems, both severe:

1. **Random.** The central progression moment of an RPG was an invisible coin
   flip. It also made every playthrough non-reproducible, so balance testing
   and seeded combat goldens were impossible.

2. **It could not raise the stats that matter.** Might drives physical damage,
   Insight magical, Grace accuracy, Resilience defense — none of them appear in
   that list, and none are derived from the four primaries. So leveling never
   improved damage, accuracy, or defense. Meanwhile 70 of 90 base items gate on
   `req_stats`, most heavily on Might (up to 28), Grace (22) and Insight (24) —
   while the maximum reachable at character creation is about 13. The entire
   tier-2 and tier-3 gear tree was permanently unequippable by every character
   in the game.

The replacement is fully deterministic: growth follows each mastery's declared
affinities (`MASTERY_MAIN_STATS`, already used at character creation), so a
Knight reliably grows Might and a Mage reliably grows Insight. No RNG, so the
same XP always produces the same character.
"""
from __future__ import annotations

from game_data import compute_starting_hp
from origins import MASTERY_MAIN_STATS

# ============================================================
# XP curve
# ============================================================
# The old curve was linear: 100 + (level - 1) * 40. Levels arrived at a
# near-constant rate while power compounded, which made the level-100 mastery
# capstones (Paladin's Avatar of Faith, etc.) both trivially reachable in
# pacing terms and absurdly distant in absolute XP.
#
# This curve is super-linear, so each tier of levels is a real commitment,
# while early levels stay brisk enough to teach the game.
XP_BASE = 100
XP_EXPONENT = 1.45


def xp_for_next(level: int) -> int:
    """XP required to advance FROM `level` to `level + 1`."""
    if level < 1:
        level = 1
    return int(XP_BASE * (level ** XP_EXPONENT))


def total_xp_for_level(level: int) -> int:
    """Cumulative XP needed to reach `level` from level 1."""
    return sum(xp_for_next(lv) for lv in range(1, max(1, level)))


# ============================================================
# Stat growth
# ============================================================
# Per level a character gains:
#   MAIN_POINTS_PER_LEVEL    into might / grace / insight / resilience
#   PRIMARY_POINTS_PER_LEVEL into vitality / cognition / essence / durability
#
# MAIN_POINTS_PER_LEVEL = 2 is calibrated against the gear gates: tier-3 items
# require up to 28 in a main stat and unlock at req_level 15. A focused mastery
# receives roughly 60% of its main points in its top stat, so by level 15 a
# Knight has gained ~18 Might on top of ~10-13 from creation — clearing the
# tier-3 gate right as the tier becomes level-appropriate.
MAIN_POINTS_PER_LEVEL = 2
PRIMARY_POINTS_PER_LEVEL = 1

MAIN_STATS = ("might", "grace", "insight", "resilience")
PRIMARY_STATS = ("vitality", "cognition", "essence", "durability")

# HP gained per level on top of the Vitality-derived base.
HP_PER_LEVEL = 4

# Which primary stats each mastery leans on, in award order. Every mastery
# gets vitality somewhere — no build should be unable to survive.
MASTERY_PRIMARY_AFFINITY: dict[str, tuple[str, ...]] = {
    "knight":    ("vitality", "durability", "vitality", "cognition"),
    "paladin":   ("vitality", "essence", "durability", "cognition"),
    "lancer":    ("vitality", "durability", "cognition", "essence"),
    "rogue":     ("vitality", "cognition", "durability", "essence"),
    "bard":      ("cognition", "vitality", "essence", "durability"),
    "alchemist": ("cognition", "essence", "vitality", "durability"),
    "mage":      ("cognition", "essence", "vitality", "durability"),
    "priest":    ("essence", "cognition", "vitality", "durability"),
    "druid":     ("essence", "vitality", "cognition", "durability"),
    "assassin":  ("cognition", "vitality", "durability", "essence"),
    "hunter":    ("vitality", "cognition", "durability", "essence"),
}

_DEFAULT_PRIMARY_AFFINITY = ("vitality", "cognition", "essence", "durability")

# Masteries whose defensive identity warrants Resilience in the main rotation.
# Resilience feeds armor (see game_data.compute_armor), so this is the tank tax.
_RESILIENCE_WEIGHT: dict[str, int] = {
    "knight": 2,
    "paladin": 2,
    "druid": 1,
    "priest": 1,
    "lancer": 1,
}


def main_stat_cycle(mastery: str) -> list[str]:
    """Deterministic award order for main stats, weighted by mastery affinity.

    Built from MASTERY_MAIN_STATS (the same table character creation uses) so a
    mastery's growth matches its declared identity. Interleaved rather than
    grouped, so partial progress through the cycle is still proportional.
    """
    weights = dict(MASTERY_MAIN_STATS.get(mastery) or {})
    if not weights:
        weights = {"might": 1, "grace": 1, "insight": 1}

    resilience = _RESILIENCE_WEIGHT.get(mastery, 0)
    if resilience:
        weights["resilience"] = resilience

    # Keep only real main stats with positive weight, in canonical order for
    # stable output regardless of dict insertion order.
    ordered = [(s, int(weights.get(s, 0))) for s in MAIN_STATS if int(weights.get(s, 0)) > 0]
    if not ordered:
        return ["might", "grace", "insight"]

    # Interleave: emit one point to each stat still owed, round after round.
    cycle: list[str] = []
    remaining = {stat: count for stat, count in ordered}
    while any(remaining.values()):
        for stat, _ in ordered:
            if remaining[stat] > 0:
                cycle.append(stat)
                remaining[stat] -= 1
    return cycle


def primary_stat_cycle(mastery: str) -> list[str]:
    """Deterministic award order for primary stats."""
    return list(MASTERY_PRIMARY_AFFINITY.get(mastery) or _DEFAULT_PRIMARY_AFFINITY)


def stat_gains_for_levels(mastery: str, from_level: int, to_level: int) -> dict[str, int]:
    """Total stat points granted by advancing from `from_level` to `to_level`.

    Pure and deterministic: same arguments always produce the same result, and
    the award order depends only on the level index, so growth can be
    recomputed or backfilled from scratch at any time.
    """
    gains: dict[str, int] = {}
    if to_level <= from_level:
        return gains

    main_cycle = main_stat_cycle(mastery)
    primary_cycle = primary_stat_cycle(mastery)

    # Level N is the (N - 2)th level-up (advancing 1 -> 2 is the first).
    for level in range(from_level + 1, to_level + 1):
        step = level - 2
        for k in range(MAIN_POINTS_PER_LEVEL):
            stat = main_cycle[(step * MAIN_POINTS_PER_LEVEL + k) % len(main_cycle)]
            gains[stat] = gains.get(stat, 0) + 1
        for k in range(PRIMARY_POINTS_PER_LEVEL):
            stat = primary_cycle[(step * PRIMARY_POINTS_PER_LEVEL + k) % len(primary_cycle)]
            gains[stat] = gains.get(stat, 0) + 1

    return gains


def max_hp_for(base_stats: dict, level: int) -> int:
    """Max HP from Vitality plus a flat per-level gain."""
    return compute_starting_hp(base_stats) + (max(1, level) - 1) * HP_PER_LEVEL


def apply_level_ups(character: dict) -> list[dict]:
    """Spend banked XP into levels, mutating `character` in place.

    Returns one entry per level gained describing what was awarded, so callers
    can surface it to the player instead of silently changing their sheet.
    """
    base = character.setdefault("base_stats", dict(character.get("stats", {})))
    mastery = character.get("mastery") or ""
    events: list[dict] = []

    # Guard against a corrupt/absent level rather than looping forever.
    if not isinstance(character.get("level"), int) or character["level"] < 1:
        character["level"] = 1
    if not isinstance(character.get("xp"), int) or character["xp"] < 0:
        character["xp"] = 0

    while character["xp"] >= xp_for_next(character["level"]):
        cost = xp_for_next(character["level"])
        character["xp"] -= cost
        old_level = character["level"]
        character["level"] = old_level + 1

        gains = stat_gains_for_levels(mastery, old_level, character["level"])
        for stat, amount in gains.items():
            base[stat] = base.get(stat, 0) + amount

        character["max_hp"] = max_hp_for(base, character["level"])
        events.append({"level": character["level"], "stat_gains": gains})

    character["base_stats"] = base
    return events
