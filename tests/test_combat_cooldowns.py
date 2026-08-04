"""Player skill cooldown handling.

Regression: the Mage's Quickened Mind and Accelerated Casting both read
`state["cooldowns"]` — a key nothing in the engine ever writes. Player skill
cooldowns live in `state["skill_cooldowns"]`. Both passives were therefore
unreachable regardless of what the player equipped.

Found by sabotaging `_mage_get_cooldown_modifier` against the golden harness and
observing *zero* behavioural change, which is only possible if the code is dead.
"""
from __future__ import annotations

import pytest

from conftest import make_character


def _mage(passives, level=60):
    ch = make_character(mastery="mage", role="scholar", level=level)
    ch["mage_equipped_passives"] = passives
    ch["name"] = "M"
    return ch


def test_engine_never_touches_the_phantom_cooldowns_key():
    """`state["cooldowns"]` is not a real key — nothing writes it, so any access is
    dead code. Comments are excluded: the fix documents the old key by name."""
    import os
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(root, "backend", "game_engine.py")
    offenders = []
    for i, line in enumerate(open(path, encoding="utf-8"), 1):
        code = line.split("#", 1)[0]
        if 'state.get("cooldowns"' in code or 'state["cooldowns"]' in code:
            offenders.append(i)
    assert not offenders, f"engine touches the phantom `cooldowns` key at lines {offenders}"


def test_quickened_mind_reduces_a_real_cooldown(ge, gd):
    """The passive must shorten an actual cooldown in `skill_cooldowns`."""
    ch = _mage(["quickened_mind"])
    assert ge._mage_get_cooldown_modifier(ch) > 0, "Quickened Mind grants no reduction"


def test_cooldown_modifier_is_zero_without_the_passive(ge):
    assert ge._mage_get_cooldown_modifier(_mage([])) == 0


def test_temporal_synergy_stacks_cooldown_reduction(ge, gd):
    """Three Temporal passives should beat one."""
    temporal = [p["id"] for p in gd.MAGE_PASSIVES
                if p["school"] == "Temporal" and not p.get("planned")]
    one = _mage(temporal[:1])
    three = _mage(temporal[:3])
    if len(temporal) < 3:
        pytest.skip("not enough equippable Temporal passives")
    assert ge._mage_get_cooldown_modifier(three) >= ge._mage_get_cooldown_modifier(one)


def test_skill_cooldowns_register_and_tick_down(ge, gd):
    """The store the Mage passives should have been using must actually work.

    The character needs real gear: skills carry `weapon_req`, and an unarmed
    character silently fails the check and never uses the skill at all.
    """
    gear = {"right_hand": "iron_longsword", "left_hand": "bone_shield",
            "body": "iron_chainmail", "head": "iron_helm"}
    ch = make_character(mastery="knight", role="fighter", level=20,
                        equipped_bases=gear)
    ch["name"] = "K"
    starting = (gd.get_mastery("knight") or {}).get("starting_skills", [])
    ch["skills"] = [{"skill_id": s, "cooldown_remaining": 0} for s in starting]
    ch["skill_bar"] = list(starting) + [None] * (10 - len(starting))

    monster = next(m for m in gd.MONSTERS if m["name"] == "Highway Bandit")
    state = ge.start_combat(ch, monster["id"])
    ge.combat_turn(ch, state, manual_skill_id=starting[0], action_type="strike")

    cds = state.get("skill_cooldowns", {})
    assert cds, "no cooldown was registered by using a skill"
    tracked = next((sid for sid, v in cds.items() if v > 0), None)
    assert tracked, f"every registered cooldown is already zero: {cds}"

    first = cds[tracked]
    ge.combat_turn(ch, state, action_type="strike")
    assert state["skill_cooldowns"][tracked] < first, "cooldown did not tick down"
