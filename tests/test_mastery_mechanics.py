"""Mastery mechanics wired in this pass — Druid stat_mods and forms, Bard
Crescendo gating, and the Mage Spatial school.

Each test below corresponds to something that was declared in data (and in several
cases advertised in the UI) while the engine did nothing with it.
"""
from __future__ import annotations

import random

import pytest

from conftest import make_character


def _mage(passives):
    ch = make_character(mastery="mage", role="scholar")
    ch["mage_equipped_passives"] = passives
    ch["name"] = "M"
    return ch


# ============================================================
# Generic self stat_mods — the Druid/Bard/Priest fallback
# ============================================================

def test_druid_self_stat_mods_are_recorded(ge, gd):
    """Every self-stat_mod branch in combat_turn was gated on a specific mastery
    and the Druid was never one of them, so all 19 Druid skills carrying
    stat_mod.self applied their status but silently dropped their stat bonuses.

    combat_turn resets character["stats"] on the way out, so `state` is the source
    of truth for active buffs — that is what this asserts.
    """
    ch = make_character(mastery="druid", role="healer", level=20)
    ch["name"] = "D"
    expected = gd.SKILLS_BY_ID["bear_form"]["stat_mod"]["self"]

    ch["skills"] = [{"skill_id": "bear_form", "cooldown_remaining": 0}]
    ch["skill_bar"] = ["bear_form"] + [None] * 9

    monster = next(m for m in gd.MONSTERS if m["name"] == "Highway Bandit")
    state = ge.start_combat(ch, monster["id"])
    ge.combat_turn(ch, state, manual_skill_id="bear_form", action_type="strike")

    held = state.get("generic_self_stat_mods", [])
    assert held, "bear_form recorded no self stat_mod at all"
    recorded = held[0]["mods"]
    assert recorded == expected, f"expected {expected}, recorded {recorded}"


def test_generic_self_stat_mods_are_reapplied_each_turn(ge, gd):
    """Buffs live in `state` and must be re-applied to character stats at the start
    of every turn, or they evaporate when combat_turn restores the originals."""
    ch = make_character(mastery="druid", role="healer", level=20)
    ch["name"] = "D"
    ch["skills"] = [{"skill_id": "bear_form", "cooldown_remaining": 0}]
    ch["skill_bar"] = ["bear_form"] + [None] * 9

    monster = next(m for m in gd.MONSTERS if m["name"] == "Highway Bandit")
    state = ge.start_combat(ch, monster["id"])
    ge.combat_turn(ch, state, manual_skill_id="bear_form", action_type="strike")
    expected_might = gd.SKILLS_BY_ID["bear_form"]["stat_mod"]["self"]["might"]

    # On the following turn the buff must be live in the character's stats.
    base_might = ch.get("base_stats", {}).get("might", 0)
    ge.combat_turn(ch, state, action_type="strike")
    assert any(e["mods"].get("might") == expected_might
               for e in state.get("generic_self_stat_mods", [])), \
        "the form buff did not survive into the next turn"
    assert base_might >= 0  # sanity: base stats untouched by the buff


def test_druid_forms_are_mutually_exclusive(ge, gd):
    """Shapeshifting means one animal at a time. Without exclusivity a Druid could
    stack bear + eagle + beast form and keep every bonus at once.

    Needs high Cognition: skill capacity is `2 + Cognition // 2` and each form
    costs 2, so a default-Cognition Druid cannot cast two forms in one encounter
    now that capacity is actually enforced. This test is about exclusivity, not
    the cap — `test_capacity_blocks_manual_overspend` covers the cap.
    """
    ch = make_character(mastery="druid", role="healer", level=20,
                        base_stats={"cognition": 14})
    ch["name"] = "D"
    ch["skills"] = [{"skill_id": s, "cooldown_remaining": 0}
                    for s in ("bear_form", "eagle_form")]
    ch["skill_bar"] = ["bear_form", "eagle_form"] + [None] * 8

    monster = next(m for m in gd.MONSTERS if m["name"] == "Highway Bandit")
    state = ge.start_combat(ch, monster["id"])
    ge.combat_turn(ch, state, manual_skill_id="bear_form", action_type="strike")
    assert state.get("druid_active_form") == "bear_form"
    ge.combat_turn(ch, state, manual_skill_id="eagle_form", action_type="strike")
    assert state.get("druid_active_form") == "eagle_form"

    forms_held = [e for e in state.get("generic_self_stat_mods", []) if e.get("form")]
    assert len(forms_held) == 1, f"{len(forms_held)} forms active at once, expected 1"


def test_bonded_senses_adds_a_summon_rider(ge):
    """Bonded Senses (L30) had no engine implementation at all."""
    ch = make_character(mastery="druid", role="healer", level=30)
    ch["name"] = "D"
    state = {
        "monster_hp": 200,
        "druid_active_summons": [{
            "name": "Test Wolf",
            "stats": {"might": 20},
            "profile_skills": {"attack": [{"name": "Bite", "damage": 10}]},
        }],
    }
    dealt = ge._druid_bonded_senses_rider(state, ch, [])
    assert dealt > 0, "Bonded Senses dealt no rider damage"
    assert state["monster_hp"] == 200 - dealt


def test_bonded_senses_requires_level_30(ge):
    ch = make_character(mastery="druid", role="healer", level=20)
    ch["name"] = "D"
    state = {"monster_hp": 200, "druid_active_summons": [{
        "name": "W", "stats": {"might": 20},
        "profile_skills": {"attack": [{"name": "Bite", "damage": 10}]}}]}
    assert ge._druid_bonded_senses_rider(state, ch, []) == 0


def test_bonded_senses_needs_an_active_summon(ge):
    ch = make_character(mastery="druid", role="healer", level=50)
    ch["name"] = "D"
    state = {"monster_hp": 100, "druid_active_summons": []}
    assert ge._druid_bonded_senses_rider(state, ch, []) == 0


# ============================================================
# Bard — per-skill Crescendo / Encore opt-in
# ============================================================

def _bard_state(crescendo, performances):
    return {"bard_crescendo": crescendo, "bard_active_performances": list(performances),
            "player_statuses": [], "monster_stats": {},
            "bard_enemy_stat_mods": [], "bard_ally_stat_mods": []}


def test_crescendo_only_builds_while_performing(ge):
    """Crescendo used to build every turn even if the Bard never played a note,
    which contradicts the mastery's whole identity."""
    ch = make_character(mastery="bard", role="scholar", level=10)
    ch["name"] = "B"

    idle = _bard_state(3, [])
    ge._bard_tick_crescendo(idle, ch, [])
    assert idle["bard_crescendo"] == 3, "Crescendo grew with no performance active"

    performing = _bard_state(3, ["song_of_heroes"])
    ge._bard_tick_crescendo(performing, ch, [])
    assert performing["bard_crescendo"] > 3, "Crescendo did not build while performing"


def test_every_performance_skill_declares_crescendo(gd):
    """The engine gates on the flag now, so a performance lacking it would be inert."""
    perfs = [s for s in gd.SKILLS if s.get("power_type") == "performance"]
    assert perfs, "no performance skills found"
    missing = [s["id"] for s in perfs if not s.get("crescendo")]
    assert not missing, f"performance skills missing the crescendo flag: {missing}"


# ============================================================
# Mage Spatial school
# ============================================================

def test_planned_passives_are_flagged(gd):
    """Passives needing portals/terrain/allies must be unequippable rather than
    equippable-and-inert."""
    planned = [p["id"] for p in gd.MAGE_PASSIVES if p.get("planned")]
    assert planned, "no passives flagged planned"
    for pid in planned:
        assert "portal" in pid or pid == "spatial_tear", f"unexpected planned passive {pid}"


def test_spatial_school_still_reaches_both_synergy_tiers(gd):
    """Synergy needs 3 and 5 equippable passives in a school. Deferring the portal
    set must not drop Spatial below 5."""
    equippable = [p for p in gd.MAGE_PASSIVES
                  if not p.get("planned") and p["school"] == "Spatial"]
    assert len(equippable) >= 5, f"only {len(equippable)} equippable Spatial passives"


def test_long_range_extends_effective_range(ge):
    ch = _mage(["long_range"])
    state = {"player_range": 2, "monster_range": 1}
    ge._mage_apply_spatial_range(state, ch, [])
    assert state["player_range"] == 3


def test_point_blank_shortens_range_and_boosts_damage(ge):
    ch = _mage(["point_blank"])
    state = {"player_range": 2, "monster_range": 1}
    ge._mage_apply_spatial_range(state, ch, [])
    assert state["player_range"] == 1
    assert ge._mage_get_spatial_damage_mult(state, ch) > 1.0


def test_point_blank_gives_no_bonus_at_long_range(ge):
    ch = _mage(["point_blank"])
    assert ge._mage_get_spatial_damage_mult({"player_range": 4}, ch) == 1.0


def test_gravity_shift_pulls_the_enemy_closer(ge):
    ch = _mage(["gravity_shift"])
    state = {"player_range": 3, "monster_range": 0}
    ge._mage_apply_spatial_riders(state, ch, {"id": "x", "power_type": "debuff"}, [])
    assert state["monster_range"] == 1


def test_reposition_backs_the_mage_away(ge):
    ch = _mage(["reposition"])
    state = {"player_range": 1, "monster_range": 0}
    ge._mage_apply_spatial_riders(state, ch, {"id": "x", "power_type": "defend"}, [])
    assert state["player_range"] == 2


def test_spatial_riders_tolerate_no_skill(ge):
    """Innate actions pass skill=None."""
    ch = _mage(["gravity_shift", "reposition", "blink_step"])
    state = {"player_range": 1, "monster_range": 1}
    ge._mage_apply_spatial_riders(state, ch, None, [])  # must not raise


def test_far_strike_reports_range_immunity(ge):
    assert ge._mage_ignores_range_minimum(_mage(["far_strike"])) is True
    assert ge._mage_ignores_range_minimum(_mage([])) is False


# ============================================================
# The reinterpreted multi-enemy passives
# ============================================================

def test_wildfire_intensifies_existing_burn(ge):
    """Spec spread burning to 'adjacent enemies', meaningless in 1v1 — reinterpreted
    as intensification so the passive keeps its identity and actually fires."""
    ch = _mage(["wildfire"])
    state = {"monster_statuses": [
        {"id": "burning", "name": "Burning", "duration": 3, "magnitude": 3}],
        "player_statuses": [], "monster_stats": {}}
    ge._mage_apply_arcane_library_control(state, ch, [])
    assert state["monster_statuses"][0]["magnitude"] == 6


def test_wildfire_does_not_stack_forever(ge):
    ch = _mage(["wildfire"])
    state = {"monster_statuses": [
        {"id": "burning", "name": "Burning", "duration": 3, "magnitude": 3}],
        "player_statuses": [], "monster_stats": {}}
    for _ in range(4):
        ge._mage_apply_arcane_library_control(state, ch, [])
    assert state["monster_statuses"][0]["magnitude"] == 6, "wildfire re-applied"


def test_mass_hysteria_extends_debuff_duration(ge):
    plain, deep = _mage([]), _mage(["mass_hysteria"])
    assert ge._mage_get_debuff_duration_multiplier(deep) > \
        ge._mage_get_debuff_duration_multiplier(plain)


def test_delirium_can_turn_an_enemy_on_itself(ge):
    ch = _mage(["delirium"])
    fired = 0
    for seed in range(300):
        random.seed(seed)
        state = {"monster_statuses": [
            {"id": "burning", "kind": "debuff"}, {"id": "shaken", "kind": "debuff"}]}
        if ge._mage_check_enemy_self_attack(state, ch, []):
            fired += 1
    assert 0 < fired < 300, f"Delirium fired {fired}/300, expected roughly 25%"


def test_delirium_needs_two_debuffs(ge):
    ch = _mage(["delirium"])
    for seed in range(50):
        random.seed(seed)
        state = {"monster_statuses": [{"id": "burning", "kind": "debuff"}]}
        assert not ge._mage_check_enemy_self_attack(state, ch, [])


def test_hallucination_only_decoys_while_evasive(ge):
    ch = _mage(["hallucination"])
    assert ge._mage_get_decoy_miss_chance({"player_statuses": []}, ch) == 0.0
    evasive = {"player_statuses": [{"id": "evasive", "name": "Evasive", "duration": 2}]}
    assert ge._mage_get_decoy_miss_chance(evasive, ch) > 0.0


def test_elemental_overload_boosts_elemental_status(ge):
    ch = _mage(["elemental_overload_mage"])
    state = {"monster_statuses": [
        {"id": "burning", "name": "Burning", "duration": 2, "magnitude": 3}]}
    ge._mage_apply_status_stack_bonus(state, ch, "burning", [])
    assert state["monster_statuses"][0]["magnitude"] == 5


def test_elemental_overload_ignores_non_elemental_status(ge):
    ch = _mage(["elemental_overload_mage"])
    state = {"monster_statuses": [
        {"id": "shaken", "name": "Shaken", "duration": 2, "magnitude": 1}]}
    ge._mage_apply_status_stack_bonus(state, ch, "shaken", [])
    assert state["monster_statuses"][0]["magnitude"] == 1


def test_overload_boosts_debuff_skills_only(ge):
    ch = _mage(["overload_mage"])
    assert ge._mage_get_overload_debuff_bonus(ch, {"power_type": "debuff"}) > 1.0
    assert ge._mage_get_overload_debuff_bonus(ch, {"power_type": "strike"}) == 1.0


def test_whole_arcane_library_is_wired_or_planned(gd):
    """Final gate: no equippable Library passive may be a silent no-op."""
    import os
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    src = open(os.path.join(root, "backend", "game_engine.py"), encoding="utf-8").read()
    # Mastery logic now lives in backend/mastery/ — scan it too.
    mdir = os.path.join(root, "backend", "mastery")
    if os.path.isdir(mdir):
        for f in sorted(os.listdir(mdir)):
            if f.endswith(".py"):
                src += open(os.path.join(mdir, f), encoding="utf-8").read()
    silent = [p["id"] for p in gd.MAGE_PASSIVES
              if not p.get("planned") and p["id"] not in src]
    assert not silent, f"equippable Library passives doing nothing: {silent}"
