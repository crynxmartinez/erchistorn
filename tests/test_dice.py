"""The weighted d6 — the single mechanic every action in the game funnels through.

If these tables drift, every success rate in the game drifts with them and
nothing else would catch it.
"""
from __future__ import annotations

import pytest


OUTCOMES = [1, 2, 3, 4, 5, 6]


def _expected_outcome(weights: list[int]) -> float:
    total = sum(weights)
    return sum(o * w for o, w in zip(OUTCOMES, weights)) / total


# ============================================================
# Table integrity
# ============================================================

def test_delta_weight_tables_are_well_formed(ge):
    for threshold, weights in ge.DELTA_WEIGHTS:
        assert len(weights) == 6, f"delta {threshold}: expected 6 weights, got {len(weights)}"
        assert all(w >= 0 for w in weights), f"delta {threshold}: negative weight"
        assert sum(weights) == 100, f"delta {threshold}: weights sum to {sum(weights)}, not 100"


def test_advantage_weight_tables_are_well_formed(ge):
    for level, weights in ge.ADVANTAGE_WEIGHTS.items():
        assert len(weights) == 6, f"{level}: expected 6 weights, got {len(weights)}"
        assert all(w >= 0 for w in weights), f"{level}: negative weight"
        assert sum(weights) == 100, f"{level}: weights sum to {sum(weights)}, not 100"


def test_delta_thresholds_are_ascending(ge):
    thresholds = [t for t, _ in ge.DELTA_WEIGHTS]
    assert thresholds == sorted(thresholds), "DELTA_WEIGHTS must be sorted by threshold"


# ============================================================
# Monotonicity — the property players actually feel
# ============================================================

def test_higher_delta_is_never_worse(ge):
    """Out-powering the target must never lower your expected outcome."""
    expectations = [_expected_outcome(w) for _, w in ge.DELTA_WEIGHTS]
    assert expectations == sorted(expectations), (
        f"expected outcome not monotonic in power delta: {expectations}"
    )


def test_accuracy_advantage_ladder_is_monotonic(ge):
    ladder = ["evas_adv_3", "evas_adv_2", "evas_adv_1",
              "neutral", "acc_adv_1", "acc_adv_2", "acc_adv_3"]
    expectations = [_expected_outcome(ge.ADVANTAGE_WEIGHTS[k]) for k in ladder]
    assert expectations == sorted(expectations), (
        f"advantage ladder not monotonic: {dict(zip(ladder, expectations))}"
    )


@pytest.mark.parametrize("diff,expected", [
    (0, "neutral"), (2, "neutral"), (-2, "neutral"),
    (3, "acc_adv_1"), (5, "acc_adv_1"),
    (6, "acc_adv_2"), (9, "acc_adv_2"),
    (10, "acc_adv_3"), (99, "acc_adv_3"),
    (-3, "evas_adv_1"), (-5, "evas_adv_1"),
    (-6, "evas_adv_2"), (-9, "evas_adv_2"),
    (-10, "evas_adv_3"), (-99, "evas_adv_3"),
])
def test_advantage_level_boundaries(ge, diff, expected):
    assert ge._advantage_level(diff) == expected


# ============================================================
# Roll shape
# ============================================================

def test_roll_dice_stays_in_range(ge):
    for delta in (-40, -15, -5, 0, 5, 15, 40):
        for _ in range(200):
            out = ge.roll_dice(10 + delta, 10)["outcome"]
            assert out in OUTCOMES


def test_roll_accuracy_evasion_stays_in_range(ge):
    for acc, evas in ((0, 30), (10, 10), (30, 0)):
        for _ in range(200):
            assert ge.roll_accuracy_evasion(acc, evas)["outcome"] in OUTCOMES


def test_luck_shifts_mass_upward_without_breaking_total(ge):
    """The luck shift moves probability toward better outcomes and must keep
    the table a valid distribution."""
    base = ge._weights_for_delta(0, luck_shift=0)
    lucky = ge._weights_for_delta(0, luck_shift=3)

    assert sum(base) == sum(lucky), "luck shift changed the weight total"
    assert all(w >= 0 for w in lucky), "luck shift produced a negative weight"
    assert _expected_outcome(lucky) >= _expected_outcome(base)


def test_extreme_deltas_are_clamped_not_extrapolated(ge):
    """A delta of 1000 must behave exactly like the top bucket, not overflow it."""
    assert ge._weights_for_delta(1000) == ge._weights_for_delta(15)
    assert ge._weights_for_delta(-1000) == ge._weights_for_delta(-15)
