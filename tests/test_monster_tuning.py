"""Monster tuning consistency — post-`power` removal.

The MVP-era `power` scalar is gone. Threat is now derived from each monster's own
stats via `compute_monster_threat(monster, level)`, so it is internally
consistent, comparable across every monster, and honest about level scaling.

History: `power` did two jobs — it fed the dice delta for non-combat actions and
it was shown to the player as "PWR n". It tracked the actual stats so poorly that
measured rank concordance between `power` and a stats-derived rating was 51%, no
better than chance. Two stat formats coexisted (flat vs growth), so "PWR 4" meant
one thing for a flat-stat monster and something 6-9x deadlier for a growth-stat
monster once the player levelled. These tests pin the replacement.
"""
from __future__ import annotations

import pytest


def _stat_at(monster: dict, stat: str, level: int) -> float:
    from game_engine import _compute_creature_stat
    val = (monster.get("stats") or {}).get(stat, 0)
    if isinstance(val, dict):
        return _compute_creature_stat(val, level)
    return val


def _uses_growth(monster: dict) -> bool:
    return any(isinstance(v, dict) for v in (monster.get("stats") or {}).values())


# ============================================================
# `power` must stay gone
# ============================================================

def test_no_monster_carries_a_power_field(gd):
    """The scalar is retired — nothing should reintroduce it."""
    bad = [m["id"] for m in gd.MONSTERS if "power" in m]
    assert not bad, f"monsters still carrying a `power` field: {bad[:10]}"


def test_no_item_carries_a_power_field(gd):
    bad = [i["id"] for i in gd.ITEMS if i.get("power")]
    assert not bad, f"items still carrying a `power` field: {bad[:10]}"


def test_skills_use_damage_not_power(gd):
    with_power = [s["id"] for s in gd.SKILLS if "power" in s]
    assert not with_power, f"skills still using `power`: {with_power[:10]}"
    assert sum(1 for s in gd.SKILLS if "damage" in s) > 0, "no skill declares `damage`"


def test_every_monster_has_stats(gd):
    """Threat is stats-derived, so a monster without stats has no threat."""
    bad = [m["id"] for m in gd.MONSTERS if not (m.get("stats") or {})]
    assert not bad, f"monsters with no stats block: {bad[:10]}"


def test_every_monster_has_positive_hp(gd):
    bad = [m["id"] for m in gd.MONSTERS if not isinstance(m.get("hp"), int) or m["hp"] <= 0]
    assert not bad, f"monsters with non-positive hp: {bad[:10]}"


# ============================================================
# Threat behaviour
# ============================================================

def test_threat_is_positive_for_every_monster(gd):
    bad = [m["id"] for m in gd.MONSTERS if gd.compute_monster_threat(m) < 1]
    assert not bad, f"monsters with non-positive threat: {bad[:10]}"


def test_threat_rises_with_level_for_scaling_monsters(gd):
    """A growth-stat monster must report a higher threat as the player levels —
    this is the honesty the old static `power` lacked."""
    growth = [m for m in gd.MONSTERS if _uses_growth(m)]
    assert growth, "no growth-stat monsters found"
    for m in growth[:40]:
        values = [gd.compute_monster_threat(m, lv) for lv in (1, 10, 20, 40)]
        assert values == sorted(values), f"{m['id']} threat not monotonic: {values}"
        assert values[-1] > values[0], f"{m['id']} threat never grows: {values}"


def test_threat_tracks_stats(gd):
    """Threat must correlate with the stats it is derived from — the property the
    old `power` field failed (51% rank concordance, i.e. chance)."""
    import itertools
    pairs = [(_stat_at(m, "might", 1) + _stat_at(m, "insight", 1),
              gd.compute_monster_threat(m, 1)) for m in gd.MONSTERS]
    concordant = total = 0
    for (o1, t1), (o2, t2) in itertools.islice(itertools.combinations(pairs, 2), 20000):
        if o1 == o2:
            continue
        total += 1
        if (o1 - o2) * (t1 - t2) >= 0:
            concordant += 1
    rate = concordant / max(1, total)
    # Threat blends offence with grace/durability/essence, so it deliberately does
    # not track offence alone perfectly. 0.85 is well clear of the 0.51 (chance)
    # that the old `power` scalar managed, while leaving room for the defensive
    # terms to reorder genuinely comparable monsters.
    assert rate > 0.85, f"threat only {rate:.0%} concordant with offensive stats"


def test_stronger_stats_mean_higher_threat(gd):
    weak = {"stats": {"might": 5, "grace": 3, "durability": 3, "essence": 2}}
    strong = {"stats": {"might": 50, "grace": 30, "durability": 30, "essence": 20}}
    assert gd.compute_monster_threat(strong) > gd.compute_monster_threat(weak)


def test_growth_stats_are_well_formed(gd):
    bad = []
    for m in gd.MONSTERS:
        for stat, val in (m.get("stats") or {}).items():
            if isinstance(val, dict):
                if not isinstance(val.get("base"), (int, float)) or                    not isinstance(val.get("growth"), (int, float)):
                    bad.append(f"{m['id']}.{stat}")
    assert not bad, f"malformed growth stat entries: {bad[:10]}"


def test_monster_hp_scaling_is_monotonic(ge, gd):
    for m in gd.MONSTERS[:60]:
        values = [ge._compute_creature_hp(m, lv) for lv in (1, 5, 10, 20, 40)]
        assert values == sorted(values), f"{m['id']} hp not monotonic: {values}"


def test_heritage_bosses_have_stats():
    """Heritage bosses shipped with only power+hp. After the removal they need
    explicit stats or _ensure_monster_fields' weak fallback makes them trivial."""
    import heritage_system as hs
    bosses = getattr(hs, "HERITAGE_BOSSES", {})
    assert bosses, "no heritage bosses found"
    missing = [k for k, v in bosses.items() if not (v.get("stats") or {})]
    assert not missing, f"heritage bosses with no stats: {missing}"


def test_heritage_boss_threat_exceeds_normal_monsters(gd):
    import heritage_system as hs
    normal_max = max(gd.compute_monster_threat(m, 1)
                     for m in gd.MONSTERS if m.get("rarity") == "common")
    for key, boss in getattr(hs, "HERITAGE_BOSSES", {}).items():
        assert gd.compute_monster_threat(boss, 1) > normal_max, (
            f"heritage boss {key} is no more threatening than a common monster"
        )
