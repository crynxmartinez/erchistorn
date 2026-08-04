"""Skill legality — capacity and triggers, for manual *and* auto selection.

Both systems were advisory for manually-selected skills, which is the normal way
to play. `combat_turn` did `skill_id = manual_skill_id or _pick_next_skill(...)`,
so a manual pick skipped the picker entirely; only cooldown and weapon_req were
re-tested further down.

What that allowed, measured:
  - `legend_of_erchis` ("only usable below 25% HP") castable at full health
  - `lions_charge` ("opening move only — there is no second charge") spammable
  - a capacity-3 character burning 6 skills, with the HUD rendering "-3/3"

107 of 350 skills carry a non-`always` trigger. Both gates now run through
`skill_unusable_reason`, the single source of truth for skill legality.
"""
from __future__ import annotations

import random

import pytest

from conftest import make_character

MELEE = {"right_hand": "iron_longsword", "left_hand": "bone_shield",
         "body": "iron_chainmail", "head": "iron_helm"}


def _knight(level=30, **kw):
    ch = make_character(mastery="knight", role="fighter", level=level,
                        equipped_bases=MELEE, **kw)
    ch["name"] = "K"
    return ch


def _fight(ge, gd, ch, skills):
    ch["skills"] = [{"skill_id": s, "cooldown_remaining": 0} for s in skills]
    ch["skill_bar"] = list(skills) + [None] * (10 - len(skills))
    monster = next(m for m in gd.MONSTERS if m["name"] == "Highway Bandit")
    random.seed(5)
    return ge.start_combat(ch, monster["id"])


def _fired(state, skill_id):
    """A registered cooldown is the reliable signal a skill actually resolved."""
    return state.get("skill_cooldowns", {}).get(skill_id, 0) > 0


# ============================================================
# The gate itself
# ============================================================

def test_unusable_reason_returns_none_for_a_legal_skill(ge, gd):
    ch = _knight()
    state = _fight(ge, gd, ch, ["shield_bash"])
    assert ge.skill_unusable_reason("shield_bash", ch, state, 1.0, 1.0, 0) is None


def test_unknown_skill_is_rejected(ge, gd):
    ch = _knight()
    state = _fight(ge, gd, ch, ["shield_bash"])
    assert ge.skill_unusable_reason("not_a_skill", ch, state, 1.0, 1.0, 0)


# ============================================================
# Triggers
# ============================================================

@pytest.mark.parametrize("skill_id,hp_ratio,enemy_ratio,turn,should_pass", [
    # low_hp: only below 50% player HP
    ("guardians_sacrifice", 1.0, 1.0, 0, False),
    ("guardians_sacrifice", 0.2, 1.0, 0, True),
    # opponent_wounded: only below 60% enemy HP
    ("crushing_blow", 1.0, 1.0, 0, False),
    ("crushing_blow", 1.0, 0.3, 0, True),
    # opening_move: turn 0 only
    ("lions_charge", 1.0, 1.0, 0, True),
    ("lions_charge", 1.0, 1.0, 5, False),
])
def test_trigger_conditions_are_enforced(ge, gd, skill_id, hp_ratio, enemy_ratio, turn, should_pass):
    ch = _knight()
    state = _fight(ge, gd, ch, [skill_id])
    reason = ge.skill_unusable_reason(skill_id, ch, state, hp_ratio, enemy_ratio, turn)
    assert (reason is None) is should_pass, f"{skill_id}: unexpected reason {reason!r}"


def test_manual_pick_cannot_bypass_a_low_hp_trigger(ge, gd):
    """The headline regression: a capstone gated on being nearly dead, cast at full HP."""
    ch = _knight()
    state = _fight(ge, gd, ch, ["guardians_sacrifice"])
    ge.combat_turn(ch, state, manual_skill_id="guardians_sacrifice", action_type="strike")
    assert not _fired(state, "guardians_sacrifice"), \
        "low_hp skill fired at full HP via manual selection"


def test_manual_pick_allows_the_skill_once_its_trigger_is_met(ge, gd):
    ch = _knight()
    state = _fight(ge, gd, ch, ["guardians_sacrifice"])
    ch["hp"] = max(1, int(ch["max_hp"] * 0.2))
    state["player_hp"] = ch["hp"]
    ge.combat_turn(ch, state, manual_skill_id="guardians_sacrifice", action_type="strike")
    assert _fired(state, "guardians_sacrifice"), "wounded Knight could not use its low_hp skill"


def test_blocked_manual_pick_is_reported_to_the_player(ge, gd):
    """Silently swallowing the click would be worse than the original bug."""
    ch = _knight()
    state = _fight(ge, gd, ch, ["guardians_sacrifice"])
    result = ge.combat_turn(ch, state, manual_skill_id="guardians_sacrifice",
                            action_type="strike")
    kinds = [e.get("kind") for e in result.get("log", [])]
    assert "skill_blocked" in kinds, f"no explanation logged; kinds were {kinds}"


# ============================================================
# Skill capacity
# ============================================================

def test_capacity_blocks_manual_overspend(ge, gd):
    """A capacity-3 character used to be able to spend 6, and the HUD showed -3/3."""
    ch = _knight()
    skills = [s["id"] for s in gd.SKILLS if s.get("type") == "knight"][:10]
    state = _fight(ge, gd, ch, skills)
    cap = state.get("max_skill_capacity")
    assert cap, "combat has no skill capacity"

    for sid in skills[:8]:
        ge.combat_turn(ch, state, manual_skill_id=sid, action_type="strike")
        if not state.get("active"):
            break
    used = state.get("skill_capacity_used", 0)
    assert used <= cap, f"spent {used} of a {cap} capacity budget"


def test_capacity_never_renders_negative(ge, gd):
    """The HUD shows `max - used`; that must not go below zero."""
    ch = _knight()
    skills = [s["id"] for s in gd.SKILLS if s.get("type") == "knight"][:10]
    state = _fight(ge, gd, ch, skills)
    for sid in skills[:8]:
        ge.combat_turn(ch, state, manual_skill_id=sid, action_type="strike")
        if not state.get("active"):
            break
        remaining = state["max_skill_capacity"] - state.get("skill_capacity_used", 0)
        assert remaining >= 0, f"HUD would show {remaining}/{state['max_skill_capacity']}"


def test_higher_cognition_buys_more_capacity(gd):
    low = make_character(mastery="knight", role="fighter", base_stats={"cognition": 2})
    high = make_character(mastery="knight", role="fighter", base_stats={"cognition": 12})
    assert gd.compute_skill_capacity(high) > gd.compute_skill_capacity(low)


def test_focus_restores_capacity_so_the_action_has_a_purpose(ge, gd):
    """The Focus innate advertises "Restore 2 skill capacity". With capacity
    unenforced that was decorative; now it is the pressure valve.

    The skill bar is cleared before the Focus turn: otherwise the auto-picker
    spends the freed capacity on the same turn and the net change is zero, which
    is correct behaviour but hides what is being measured here.
    """
    ch = _knight()
    skills = [s["id"] for s in gd.SKILLS if s.get("type") == "knight"][:6]
    state = _fight(ge, gd, ch, skills)
    ge.combat_turn(ch, state, manual_skill_id=skills[0], action_type="strike")
    spent = state.get("skill_capacity_used", 0)
    assert spent > 0, "using a skill spent no capacity"

    ch["skill_bar"] = [None] * 10          # nothing for the auto-picker to re-spend on
    ge.combat_turn(ch, state, action_type="focus")
    assert state.get("skill_capacity_used", 0) < spent, "Focus restored nothing"


# ============================================================
# Cooldown and weapon_req still gate (they always did)
# ============================================================

def test_cooldown_still_blocks(ge, gd):
    ch = _knight()
    state = _fight(ge, gd, ch, ["shield_bash"])
    ge.combat_turn(ch, state, manual_skill_id="shield_bash", action_type="strike")
    if state["skill_cooldowns"].get("shield_bash", 0) > 0:
        reason = ge.skill_unusable_reason("shield_bash", ch, state, 1.0, 1.0, 1)
        assert reason and "cooldown" in reason


def test_weapon_requirement_still_blocks(ge, gd):
    """An unarmed character must not be able to use a weapon-gated skill."""
    unarmed = make_character(mastery="knight", role="fighter", level=30)
    unarmed["name"] = "K"
    gated = next((sid for sid, extra in gd.SKILL_EXTRAS.items()
                  if extra.get("weapon_req") not in (None, "none")
                  and sid in gd.SKILLS_BY_ID), None)
    if not gated:
        pytest.skip("no weapon-gated skills in data")
    state = _fight(ge, gd, unarmed, [gated])
    reason = ge.skill_unusable_reason(gated, unarmed, state, 1.0, 1.0, 0)
    assert reason and "requires" in reason


# ============================================================
# The auto-picker must obey the same gate
# ============================================================

def test_auto_picker_and_manual_pick_agree(ge, gd):
    """One gate, one answer — the divergence between them was the bug."""
    ch = _knight()
    skills = [s["id"] for s in gd.SKILLS if s.get("type") == "knight"][:8]
    state = _fight(ge, gd, ch, skills)
    picked = ge._pick_next_skill(ch, state, 1.0, 1.0, 0)
    if picked:
        assert ge.skill_unusable_reason(picked, ch, state, 1.0, 1.0, 0) is None, \
            "the auto-picker chose a skill the gate rejects"


def test_auto_picker_skips_untriggered_skills(ge, gd):
    """Given only a low_hp skill at full HP, the picker must return nothing."""
    ch = _knight()
    state = _fight(ge, gd, ch, ["guardians_sacrifice"])
    assert ge._pick_next_skill(ch, state, 1.0, 1.0, 0) is None
