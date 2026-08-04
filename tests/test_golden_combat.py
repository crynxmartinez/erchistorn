"""Golden-log regression gate for `combat_turn`.

The full sweep is 1,584 scenarios / ~19,800 turns and takes a couple of minutes,
which is too slow for every `pytest` run. So:

  - a fast subset runs by default (one scenario per mastery),
  - the full sweep runs when `GOLDEN_FULL=1` is set, or via
    `python -m tests.golden verify`.

Run the full sweep after any change to combat_turn or a mastery helper. It is the
only thing standing between a refactor and a silently broken mastery.
"""
from __future__ import annotations

import json
import os

import pytest

from golden import (FIXTURE_PATH, LOADOUTS, _digest, build_hashes,
                    run_scenario)

FULL = os.environ.get("GOLDEN_FULL") == "1"


@pytest.fixture(scope="module")
def fixtures():
    if not os.path.exists(FIXTURE_PATH):
        pytest.skip("no golden fixtures — run `python -m tests.golden record`")
    with open(FIXTURE_PATH, encoding="utf-8") as fh:
        return json.load(fh)


def test_fixtures_exist_and_cover_every_mastery(fixtures):
    """A missing mastery means the net has a hole for that mastery."""
    for mastery, _role, _gear in LOADOUTS:
        assert any(k.startswith(f"{mastery}|") for k in fixtures), \
            f"no golden scenarios for {mastery}"


def test_fixture_count_is_stable(fixtures):
    """Scenario ids are generated, so a change in count means the matrix moved —
    which invalidates comparisons until fixtures are re-recorded."""
    assert len(fixtures) == 1584, (
        f"expected 1584 scenarios, fixture has {len(fixtures)}. "
        "Re-record if the scenario matrix changed on purpose."
    )


@pytest.mark.parametrize("mastery,role,gear", LOADOUTS)
def test_representative_scenario_matches_golden(fixtures, mastery, role, gear):
    """One scenario per mastery — the fast gate."""
    key = f"{mastery}|L20|Highway Bandit|strike|s7"
    if key not in fixtures:
        pytest.skip(f"{key} not in fixtures")
    trace = run_scenario(mastery, role, gear, 20, "Highway Bandit", "strike", 7)
    assert trace is not None, f"{key} failed to run"
    expected_turns, expected_digest = fixtures[key]
    assert len(trace) == expected_turns, (
        f"{key}: turn count {len(trace)} != {expected_turns}"
    )
    assert _digest(trace) == expected_digest, (
        f"{key}: behaviour changed. Replay with:\n"
        f'  python -m tests.golden diff "{key}"'
    )


@pytest.mark.skipif(not FULL, reason="set GOLDEN_FULL=1 for the full 1,584-scenario sweep")
def test_full_golden_sweep(fixtures):
    actual = build_hashes()
    missing = sorted(set(fixtures) - set(actual))
    added = sorted(set(actual) - set(fixtures))
    changed = [k for k in sorted(set(fixtures) & set(actual)) if fixtures[k] != actual[k]]
    assert not missing, f"{len(missing)} scenarios no longer run: {missing[:5]}"
    assert not added, f"{len(added)} new scenarios appeared: {added[:5]}"
    assert not changed, (
        f"{len(changed)} scenarios changed behaviour, e.g. {changed[:5]}\n"
        f'Replay with: python -m tests.golden diff "{changed[0]}"'
    )
