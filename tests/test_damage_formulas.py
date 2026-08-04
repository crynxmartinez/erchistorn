"""Damage, mitigation, healing and derived-stat formulas.

The spec these pin down (from the docstrings in game_data.py):
  physical = (weapon + skill) x (1 + Might   x 0.03)
  magical  = (spell  + skill) x (1 + Insight x 0.03)
  healing  =  base           x (1 + Essence x 0.03)
  taken    =  raw x 100 / (100 + defense), capped at MAX_DMG_REDUCTION
"""
from __future__ import annotations

import pytest

from conftest import make_character


# ============================================================
# Offensive scaling
# ============================================================

def test_physical_damage_scales_with_might(gd):
    weak = make_character(base_stats={"might": 0})
    strong = make_character(base_stats={"might": 20})
    assert gd.compute_physical_damage(strong, 10, 5) > gd.compute_physical_damage(weak, 10, 5)


def test_physical_damage_matches_spec(gd):
    ch = make_character(base_stats={"might": 10})
    assert gd.compute_physical_damage(ch, 10, 10) == int(20 * (1 + 10 * 0.03))


def test_magical_damage_scales_with_insight(gd):
    weak = make_character(base_stats={"insight": 0})
    strong = make_character(base_stats={"insight": 20})
    assert gd.compute_magical_damage(strong, 10, 5) > gd.compute_magical_damage(weak, 10, 5)


def test_magical_damage_matches_spec(gd):
    ch = make_character(base_stats={"insight": 10})
    assert gd.compute_magical_damage(ch, 10, 10) == int(20 * (1 + 10 * 0.03))


def test_might_does_not_scale_magical_damage(gd):
    """The two damage types must stay on separate stats, or builds collapse."""
    brute = make_character(base_stats={"might": 30, "insight": 0})
    plain = make_character(base_stats={"might": 0, "insight": 0})
    assert gd.compute_magical_damage(brute, 10, 0) == gd.compute_magical_damage(plain, 10, 0)


def test_insight_does_not_scale_physical_damage(gd):
    scholar = make_character(base_stats={"insight": 30, "might": 0})
    plain = make_character(base_stats={"insight": 0, "might": 0})
    assert gd.compute_physical_damage(scholar, 10, 0) == gd.compute_physical_damage(plain, 10, 0)


# ============================================================
# Mitigation
# ============================================================

@pytest.mark.parametrize("defense", [1, 10, 50, 100, 500])
def test_more_armor_never_increases_damage_taken(gd, defense):
    raw = 100
    assert gd.apply_armor(raw, defense) <= raw


def test_armor_is_monotonic(gd):
    raw = 200
    taken = [gd.apply_armor(raw, a) for a in (0, 10, 25, 50, 100, 200)]
    assert taken == sorted(taken, reverse=True), f"armor not monotonic: {taken}"


def test_magic_resistance_is_monotonic(gd):
    raw = 200
    taken = [gd.apply_magic_resistance(raw, m) for m in (0, 10, 25, 50, 100, 200)]
    assert taken == sorted(taken, reverse=True), f"MR not monotonic: {taken}"


def test_armor_penetration_increases_damage(gd):
    raw, armor = 100, 100
    assert gd.apply_armor(raw, armor, armor_pen_pct=0.5) > gd.apply_armor(raw, armor)


def test_full_penetration_ignores_armor(gd):
    raw = 100
    assert gd.apply_armor(raw, 250, armor_pen_pct=1.0) == raw


def test_negative_defense_does_not_amplify_damage(gd):
    """Debuffs can push armor negative (skills apply armor_bonus: -999).
    That must not turn mitigation into a damage multiplier."""
    raw = 100
    assert gd.apply_armor(raw, -50) == raw
    assert gd.apply_magic_resistance(raw, -50) == raw


def test_compute_armor_never_negative(gd):
    ch = make_character(base_stats={"armor_bonus": -999, "resilience": 0})
    assert gd.compute_armor(ch) >= 0


# ============================================================
# Healing / barrier
# ============================================================

def test_healing_scales_with_essence(gd):
    plain = make_character(base_stats={"essence": 0})
    holy = make_character(base_stats={"essence": 20})
    assert gd.compute_healing(holy, 50) > gd.compute_healing(plain, 50)


def test_barrier_scales_with_essence(gd):
    plain = make_character(base_stats={"essence": 0})
    holy = make_character(base_stats={"essence": 20})
    assert gd.compute_barrier(holy, 50) > gd.compute_barrier(plain, 50)


# ============================================================
# Derived stats
# ============================================================

def test_max_hp_scales_with_vitality(gd):
    assert gd.compute_starting_hp({"vitality": 10}) > gd.compute_starting_hp({"vitality": 3})


def test_max_hp_matches_spec(gd):
    assert gd.compute_starting_hp({"vitality": 7}) == 50 + 7 * 10


def test_skill_capacity_is_bounded(gd):
    assert gd.compute_skill_capacity(make_character(base_stats={"cognition": 0})) >= 2
    assert gd.compute_skill_capacity(make_character(base_stats={"cognition": 999})) <= 8


def test_status_duration_reduction_is_bounded(gd):
    """Durability reduces debuff duration but must never invert it."""
    for dur in (0, 5, 12, 50, 999):
        mult = gd.compute_status_duration_mult(make_character(base_stats={"durability": dur}))
        assert 0.5 <= mult <= 1.0, f"durability {dur} gave multiplier {mult}"
