"""XP curve and level-up stat growth.

The headline regression: level-up used `random.choice` over the four primary
stats only, so Might / Grace / Insight / Resilience never grew. Because 70 of
90 base items gate on `req_stats` — up to Might 28, Grace 22, Insight 24 — and
the ceiling reachable at character creation is about 13, the whole tier-2 and
tier-3 gear tree was permanently unequippable.
"""
from __future__ import annotations

import random

import pytest

from conftest import make_character


# ============================================================
# XP curve
# ============================================================

def test_xp_curve_is_strictly_increasing():
    import progression as p
    costs = [p.xp_for_next(lv) for lv in range(1, 60)]
    assert costs == sorted(costs)
    assert len(set(costs)) == len(costs), "curve has flat spots"


def test_xp_curve_is_super_linear():
    """Regression: the curve was linear (100 + (level-1)*40), so late levels
    arrived at a near-constant rate while power compounded."""
    import progression as p
    early = p.xp_for_next(10) - p.xp_for_next(9)
    late = p.xp_for_next(50) - p.xp_for_next(49)
    assert late > early * 2, f"curve is not super-linear (early {early}, late {late})"


def test_xp_curve_handles_degenerate_levels():
    import progression as p
    assert p.xp_for_next(0) > 0
    assert p.xp_for_next(-5) > 0


def test_early_levels_stay_brisk():
    """The first few levels must be fast enough to teach the game."""
    import progression as p
    assert p.total_xp_for_level(5) < 2000


# ============================================================
# Determinism
# ============================================================

def test_level_up_is_deterministic():
    """Regression: random.choice made progression a coin flip and made seeded
    combat goldens impossible."""
    import progression as p

    results = []
    for seed in (1, 2, 999):
        random.seed(seed)
        ch = make_character(level=1, mastery="knight")
        ch["xp"] = 50_000
        p.apply_level_ups(ch)
        results.append((ch["level"], dict(ch["base_stats"]), ch["max_hp"]))

    assert results[0] == results[1] == results[2], (
        "level-up outcome depends on the RNG seed"
    )


def test_stat_gains_are_pure():
    import progression as p
    a = p.stat_gains_for_levels("mage", 1, 30)
    b = p.stat_gains_for_levels("mage", 1, 30)
    assert a == b


def test_stat_gains_compose_across_ranges():
    """Growing 1->30 in one call must equal 1->15 then 15->30."""
    import progression as p
    whole = p.stat_gains_for_levels("hunter", 1, 30)

    piecewise: dict[str, int] = {}
    for lo, hi in ((1, 15), (15, 30)):
        for stat, val in p.stat_gains_for_levels("hunter", lo, hi).items():
            piecewise[stat] = piecewise.get(stat, 0) + val

    assert whole == piecewise


def test_no_gain_for_empty_range():
    import progression as p
    assert p.stat_gains_for_levels("knight", 10, 10) == {}
    assert p.stat_gains_for_levels("knight", 10, 5) == {}


# ============================================================
# Main stats must actually grow
# ============================================================

@pytest.mark.parametrize("mastery", [
    "knight", "paladin", "lancer", "rogue", "bard", "alchemist",
    "mage", "priest", "druid", "assassin", "hunter",
])
def test_every_mastery_grows_a_main_stat(mastery):
    """Regression: leveling never raised might/grace/insight/resilience, so it
    never improved damage, accuracy, or defense for anyone."""
    import progression as p
    gains = p.stat_gains_for_levels(mastery, 1, 20)
    main_total = sum(gains.get(s, 0) for s in p.MAIN_STATS)
    assert main_total > 0, f"{mastery} gains no main stats over 19 levels"


@pytest.mark.parametrize("mastery,stat", [
    ("knight", "might"),
    ("lancer", "might"),
    ("mage", "insight"),
    ("priest", "insight"),
    ("assassin", "grace"),
    ("rogue", "grace"),
])
def test_mastery_grows_its_signature_stat(mastery, stat):
    """Growth must follow the mastery's declared identity, not spread evenly."""
    import progression as p
    gains = p.stat_gains_for_levels(mastery, 1, 20)
    assert gains.get(stat, 0) > 0, f"{mastery} gained no {stat}"

    other_mains = [gains.get(s, 0) for s in p.MAIN_STATS if s != stat]
    assert gains[stat] >= max(other_mains or [0]), (
        f"{mastery}: {stat} is not its top main-stat gain ({gains})"
    )


def test_every_mastery_grows_vitality():
    """No build should be unable to survive."""
    import progression as p
    for mastery in p.MASTERY_PRIMARY_AFFINITY:
        gains = p.stat_gains_for_levels(mastery, 1, 12)
        assert gains.get("vitality", 0) > 0, f"{mastery} gains no vitality"


def test_max_hp_grows_with_level():
    import progression as p
    base = {"vitality": 5}
    assert p.max_hp_for(base, 20) > p.max_hp_for(base, 1)


# ============================================================
# The gear gates must be reachable
# ============================================================

def _best_creation_stats(stat: str) -> int:
    """Highest value of `stat` obtainable at character creation.

    Stacks every creation-time source: racial starting_stats, the role's flat
    `bonus`, the role and mastery main-stat allocations, the best origin bonus,
    and a racial gift. Primary stats (vitality/cognition/essence/durability) come
    mostly from `RACES[*].starting_stats`, which is why they must be included —
    omitting them understates the reachable ceiling badly.
    """
    from game_data import RACES, ROLES
    from origins import ROLE_MAIN_STATS, MASTERY_MAIN_STATS, ORIGINS

    race = max((r["starting_stats"].get(stat, 0) for r in RACES), default=0)
    role_bonus = max(((r.get("bonus") or {}).get(stat, 0) for r in ROLES), default=0)
    role_main = max((v.get(stat, 0) for v in ROLE_MAIN_STATS.values()), default=0)
    mastery = max((v.get(stat, 0) for v in MASTERY_MAIN_STATS.values()), default=0)
    origin = max(((o.get("bonus") or {}).get(stat, 0) for o in ORIGINS), default=0)
    gift = 1
    return race + role_bonus + role_main + mastery + origin + gift


def test_all_gear_requirements_are_reachable():
    """Every req_stats gate in the game must be satisfiable by some legal build.

    Regression: T2 gear needed up to Might 20 and T3 up to Might 28, while the
    creation ceiling was ~13 and leveling could not raise Might at all — so the
    entire T2/T3 tree was dead content.
    """
    import progression as p
    from items.base_items import BASE_ITEMS

    LEVEL_CAP = 60
    unreachable = []

    for base in BASE_ITEMS:
        req = base.get("req_stats") or {}
        if not req:
            continue
        req_level = int(base.get("req_level", 1) or 1)

        for stat, needed in req.items():
            # Best case: the mastery that grows this stat fastest, at the
            # generous end of the level band the item unlocks in.
            best_growth = max(
                p.stat_gains_for_levels(m, 1, LEVEL_CAP).get(stat, 0)
                for m in p.MASTERY_PRIMARY_AFFINITY
            )
            reachable = _best_creation_stats(stat) + best_growth
            if reachable < int(needed):
                unreachable.append(
                    f"{base['id']} (req_level {req_level}) needs {stat} {needed}, "
                    f"max reachable {reachable}"
                )

    assert not unreachable, "unreachable gear requirements:\n  " + "\n  ".join(unreachable)


def test_tier3_gear_reachable_near_its_level_gate():
    """A focused build should clear tier-3 gates within a reasonable margin of
    the level the tier unlocks at, not 40 levels later."""
    import progression as p
    from items.base_items import BASE_ITEMS

    t3 = [b for b in BASE_ITEMS if b.get("tier") == 3 and b.get("req_stats")]
    assert t3, "no tier-3 gated items found"

    CHECK_LEVEL = 30
    failures = []
    for base in t3:
        for stat, needed in base["req_stats"].items():
            best_growth = max(
                p.stat_gains_for_levels(m, 1, CHECK_LEVEL).get(stat, 0)
                for m in p.MASTERY_PRIMARY_AFFINITY
            )
            if _best_creation_stats(stat) + best_growth < int(needed):
                failures.append(f"{base['id']}: {stat} {needed}")

    assert not failures, (
        f"tier-3 gear still gated out at level {CHECK_LEVEL}: {failures}"
    )


# ============================================================
# apply_level_ups behaviour
# ============================================================

def test_apply_level_ups_consumes_xp_and_reports_events():
    import progression as p
    ch = make_character(level=1, mastery="knight")
    ch["xp"] = p.xp_for_next(1) + p.xp_for_next(2)

    events = p.apply_level_ups(ch)

    assert ch["level"] == 3
    assert len(events) == 2
    assert all(e["stat_gains"] for e in events)
    assert ch["xp"] < p.xp_for_next(3)


def test_apply_level_ups_is_a_noop_below_threshold():
    import progression as p
    ch = make_character(level=1, mastery="mage")
    ch["xp"] = 1
    before = dict(ch["base_stats"])
    assert p.apply_level_ups(ch) == []
    assert ch["level"] == 1
    assert ch["base_stats"] == before


def test_apply_level_ups_survives_corrupt_state():
    """A bad level/xp must not spin forever."""
    import progression as p
    ch = make_character(mastery="knight")
    ch["level"] = 0
    ch["xp"] = -50
    p.apply_level_ups(ch)
    assert ch["level"] >= 1
    assert ch["xp"] >= 0


def test_leveling_improves_real_combat_output(gd):
    """End to end: a leveled character must hit harder than a fresh one."""
    import progression as p

    fresh = make_character(level=1, mastery="knight", base_stats={"might": 9})
    veteran = make_character(level=1, mastery="knight", base_stats={"might": 9})
    veteran["xp"] = 500_000
    p.apply_level_ups(veteran)
    veteran["stats"] = dict(veteran["base_stats"])

    assert veteran["level"] > 10
    assert gd.compute_physical_damage(veteran, 20, 10) > gd.compute_physical_damage(fresh, 20, 10)
