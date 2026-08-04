"""Mastery passive wiring.

Every mastery ships a passive table. A passive that exists in data but that no
engine code reads is worse than a missing feature: the player sees it unlock (or
researches and equips it, for the Mage) and it silently does nothing.

The Mage's Arcane Library is the strict case — those passives are looked up by id
via `_mage_has_passive`, so an id that never appears in the engine is conclusively
dead. Level-gated passives on other masteries are often implemented as a bare
`if level >= N` with no mention of the passive's name, so they cannot be detected
by text search; those are covered by behavioural tests instead.
"""
from __future__ import annotations

import random

import pytest

from conftest import make_character


# ============================================================
# Mage — Arcane Library (id-based, so absence is conclusive)
# ============================================================

# Passives that describe multi-enemy behaviour ("adjacent enemies", "attack their
# own ally") or a system that does not exist (illusion copies, portals/terrain).
# Combat is 1v1, so these cannot be implemented as written — tracked in
# MASTERY_PLANS.md rather than silently expected to work.
MAGE_NOT_IMPLEMENTABLE_1V1 = {
    # Need portals, terrain or allies — none of which combat represents. These are
    # flagged `planned` in MAGE_PASSIVES and blocked from being equipped, so a
    # player can no longer spend research on a permanent no-op.
    "portal_mastery", "spatial_tear", "portal_behind_ally", "portal_behind_enemy",
    "portal_through_wall", "portal_through_trap",
    # Reinterpreted or superseded elsewhere in the engine.
    "overload_mage", "elemental_overload_mage", "temporal_echo",
}


def _engine_src():
    """Engine source *plus* the extracted mastery modules.

    Mastery logic now lives in backend/mastery/, so scanning game_engine.py alone
    would report extracted passives as unwired.
    """
    import os
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    src = open(os.path.join(root, "backend", "game_engine.py"), encoding="utf-8").read()
    mdir = os.path.join(root, "backend", "mastery")
    if os.path.isdir(mdir):
        for f in sorted(os.listdir(mdir)):
            if f.endswith(".py"):
                src += open(os.path.join(mdir, f), encoding="utf-8").read()
    return src


def test_mage_library_passives_are_wired_or_explicitly_deferred(gd):
    """Every equippable Library passive must either be implemented or be on the
    explicit deferred list. A silent third category is the bug."""
    src = _engine_src()
    silent = [p["id"] for p in gd.MAGE_PASSIVES
              if p["id"] not in src
              and p["id"] not in MAGE_NOT_IMPLEMENTABLE_1V1]
    assert not silent, (
        f"{len(silent)} Library passives are equippable but do nothing and are not "
        f"declared deferred: {silent}"
    )


@pytest.mark.parametrize("passive_id", [
    "absolute_zero", "mind_fracture", "paranoia",
    "mind_control", "time_loop", "illusion_mastery", "double_jeopardy",
])
def test_newly_wired_mage_passives_are_referenced(passive_id):
    assert passive_id in _engine_src(), f"{passive_id} is not referenced by the engine"


def _mage(passives):
    ch = make_character(mastery="mage", role="scholar")
    ch["mage_equipped_passives"] = passives
    ch["name"] = "M"
    return ch


def test_absolute_zero_freezes_an_ensnared_target(ge):
    ch = _mage(["absolute_zero"])
    state = {"monster_statuses": [{"id": "ensnared", "name": "Ensnared", "duration": 2}],
             "player_statuses": [], "monster_stats": {}}
    log = []
    ge._mage_apply_arcane_library_control(state, ch, log)
    assert any(s["id"] == "stunned" for s in state["monster_statuses"]), \
        "Absolute Zero did not freeze an already-ensnared target"


def test_absolute_zero_does_nothing_without_ensnare(ge):
    ch = _mage(["absolute_zero"])
    state = {"monster_statuses": [], "player_statuses": [], "monster_stats": {}}
    ge._mage_apply_arcane_library_control(state, ch, [])
    assert not state["monster_statuses"]


def test_mind_fracture_drains_a_stat_from_shaken_targets(ge):
    ch = _mage(["mind_fracture"])
    state = {"monster_statuses": [{"id": "shaken", "name": "Shaken", "duration": 2}],
             "player_statuses": [], "monster_stats": {"might": 10, "grace": 10}}
    before = dict(state["monster_stats"])
    ge._mage_apply_arcane_library_control(state, ch, [])
    assert state["monster_stats"] != before, "Mind Fracture drained nothing"
    assert sum(state["monster_stats"].values()) == sum(before.values()) - 1


def test_paranoia_flags_buff_denial(ge):
    ch = _mage(["paranoia"])
    state = {"monster_statuses": [{"id": "shaken", "name": "Shaken", "duration": 2}],
             "player_statuses": [], "monster_stats": {}}
    ge._mage_apply_arcane_library_control(state, ch, [])
    assert state.get("mage_paranoia_active") is True


def test_time_loop_consumes_a_stunned_enemy_turn(ge):
    ch = _mage(["time_loop"])
    state = {"monster_statuses": [{"id": "stunned", "name": "Stunned", "duration": 1}]}
    assert ge._mage_check_enemy_turn_skip(state, ch, []) is True


def test_turn_skip_does_not_fire_without_the_passive(ge):
    ch = _mage([])
    state = {"monster_statuses": [{"id": "stunned", "name": "Stunned", "duration": 1}]}
    assert ge._mage_check_enemy_turn_skip(state, ch, []) is False


def test_mind_control_can_steal_a_shaken_enemy_turn(ge):
    """15% chance — assert it fires at least once over many seeded trials."""
    ch = _mage(["mind_control"])
    fired = 0
    for seed in range(300):
        random.seed(seed)
        state = {"monster_statuses": [{"id": "shaken", "name": "Shaken", "duration": 2}]}
        if ge._mage_check_enemy_turn_skip(state, ch, []):
            fired += 1
    assert 0 < fired < 300, f"Mind Control fired {fired}/300 times — expected roughly 15%"


def test_illusion_mastery_adds_hidden_to_evasive(ge):
    ch = _mage(["illusion_mastery"])
    state = {"player_statuses": [{"id": "evasive", "name": "Evasive", "duration": 2}]}
    ge._mage_check_illusion_mastery(state, ch, [])
    assert any(s["id"] == "hidden" for s in state["player_statuses"])


def test_double_jeopardy_adds_a_second_status(ge):
    ch = _mage(["double_jeopardy"])
    skill = {"id": "x", "spell_tags": ["Debuff"], "status_apply": "burning"}
    assert ge._mage_get_extra_status(ch, skill) == "shaken"


# ============================================================
# Hunter — Unbreakable Focus (L80)
# ============================================================

def test_spirit_guidance_breaks_on_stun_below_level_80(ge):
    """The reset had never been implemented, which made Unbreakable Focus a
    no-op — it guarded against something that could not happen."""
    ch = make_character(mastery="hunter", role="scout", level=40)
    ch["name"] = "H"
    state = {"hunter_spirit_guidance": 7,
             "player_statuses": [{"id": "stunned", "name": "Stunned", "duration": 1}],
             "monster_hp": 50}
    ge._hunter_tick_end_of_turn(state, ch, [])
    assert state["hunter_spirit_guidance"] == 0


def test_unbreakable_focus_holds_guidance_through_stun_at_80(ge):
    ch = make_character(mastery="hunter", role="scout", level=80)
    ch["name"] = "H"
    state = {"hunter_spirit_guidance": 7,
             "player_statuses": [{"id": "stunned", "name": "Stunned", "duration": 1}],
             "monster_hp": 50}
    ge._hunter_tick_end_of_turn(state, ch, [])
    assert state["hunter_spirit_guidance"] == 7


def test_guidance_survives_when_not_stunned(ge):
    ch = make_character(mastery="hunter", role="scout", level=40)
    ch["name"] = "H"
    state = {"hunter_spirit_guidance": 5, "player_statuses": [], "monster_hp": 50}
    ge._hunter_tick_end_of_turn(state, ch, [])
    assert state["hunter_spirit_guidance"] == 5


# ============================================================
# Rogue — level-gated upgrades to the innate kit
# ============================================================

def test_con_master_doubles_debuff_extension_at_80(ge):
    base = {"rogue_con_artist": True, "_rogue_level": 40}
    upgraded = {"rogue_con_artist": True, "_rogue_level": 80}
    assert ge._rogue_get_con_artist_bonus(upgraded) > ge._rogue_get_con_artist_bonus(base)
    assert ge._rogue_get_con_artist_bonus(upgraded) == 2


def test_slippery_soul_raises_shake_chance_at_90(ge):
    """Statistical check: 50% at L90 must shed noticeably more debuffs than 25%."""
    def shed(level):
        count = 0
        for seed in range(400):
            random.seed(seed)
            state = {"rogue_slippery": True, "_rogue_level": level,
                     "player_statuses": [{"id": "poisoned", "name": "Poisoned", "duration": 3}]}
            ge._rogue_slippery_tick(state, [])
            if not state["player_statuses"]:
                count += 1
        return count

    assert shed(90) > shed(40), "Slippery Soul did not improve the shake chance"


def test_trap_specialist_grants_two_charges_at_70(ge):
    """Already implemented as a bare level check — pinned so it stays that way."""
    low = make_character(mastery="rogue", role="scout", level=40)
    high = make_character(mastery="rogue", role="scout", level=70)
    for ch in (low, high):
        ch["name"] = "R"
        ch["rogue_innate_equipped"] = ["trap_master"]
    s_low, s_high = {}, {}
    ge._rogue_init_combat(s_low, low, [])
    ge._rogue_init_combat(s_high, high, [])
    assert s_high.get("rogue_trap_master_charges", 0) > s_low.get("rogue_trap_master_charges", 0)


# ============================================================
# Every mastery has a passive table
# ============================================================

MASTERIES = ["knight", "paladin", "lancer", "rogue", "bard", "alchemist",
             "mage", "priest", "druid", "assassin", "hunter"]


@pytest.mark.parametrize("mastery", MASTERIES)
def test_every_mastery_has_a_passive_table(gd, mastery):
    """The Alchemist shipped with no passive table at all, so it was the only
    mastery with a completely flat curve from level 10 to 100."""
    table = getattr(gd, f"{mastery.upper()}_PASSIVES", None)
    assert table, f"{mastery} has no passive table"
    assert len(table) >= 10, f"{mastery} has only {len(table)} passives (expected 10+)"


@pytest.mark.parametrize("mastery", MASTERIES)
def test_passive_entries_are_well_formed(gd, mastery):
    table = getattr(gd, f"{mastery.upper()}_PASSIVES", None) or []
    for p in table:
        assert p.get("id"), f"{mastery} passive with no id: {p}"
        assert p.get("name"), f"{mastery} passive {p.get('id')} has no name"
        assert p.get("desc"), f"{mastery} passive {p.get('id')} has no desc"


# ============================================================
# Alchemist — the table that did not exist
# ============================================================

def _alch(level):
    ch = make_character(mastery="alchemist", role="scholar", level=level)
    ch["name"] = "A"
    return ch


def test_alchemist_passive_levels_are_the_standard_ladder(gd):
    levels = [p["level"] for p in gd.ALCHEMIST_PASSIVES]
    assert levels == [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]


def test_alch_has_passive_respects_level(ge):
    assert not ge._alch_has_passive(_alch(5), "steady_hands")
    assert ge._alch_has_passive(_alch(10), "steady_hands")
    assert not ge._alch_has_passive(_alch(50), "dual_imbue")
    assert ge._alch_has_passive(_alch(80), "dual_imbue")


def test_alch_has_passive_is_false_for_non_alchemists(ge):
    knight = make_character(mastery="knight", role="fighter", level=100)
    assert not ge._alch_has_passive(knight, "steady_hands")


def test_steady_hands_increases_combo_flow_gain(ge):
    skill = {"cf_gain": 1}
    low, high = {}, {}
    ge._alch_gain_cf(low, skill, [], _alch(5))
    ge._alch_gain_cf(high, skill, [], _alch(10))
    assert high["alchemist_cf"] > low.get("alchemist_cf", 0)


def test_deep_reserves_raises_the_combo_flow_ceiling(ge):
    skill = {"cf_gain": 99}
    low, high = {}, {}
    ge._alch_gain_cf(low, skill, [], _alch(15))
    ge._alch_gain_cf(high, skill, [], _alch(20))
    assert low["alchemist_cf"] == 20
    assert high["alchemist_cf"] == 25


def test_stable_compound_adds_an_imbue_charge(ge):
    skill = {"name": "Test Imbue", "imbue_charges": 3, "blade_shape": "needle"}
    low, high = {}, {}
    ge._alch_load_imbue(low, skill, [], _alch(25))
    ge._alch_load_imbue(high, skill, [], _alch(30))
    assert high["alchemist_imbue_charges"] == low["alchemist_imbue_charges"] + 1


def test_transmuters_insight_reduces_combo_flow_cost(ge):
    """Analysis costs 5; at L50 it should cost 4, leaving 1 more CF banked."""
    def remaining(level):
        state = {"alchemist_cf": 5}
        ge._alch_spend_cf(state, _alch(level), {"name": "X"}, [], "analysis")
        return state["alchemist_cf"]
    assert remaining(50) > remaining(45)


def test_perfect_transmutation_makes_combo_flow_free(ge):
    state = {"alchemist_cf": 20}
    ok = ge._alch_spend_cf(state, _alch(100), {"name": "X"}, [], "perfect_formula")
    assert ok
    assert state["alchemist_cf"] == 20, "Perfect Transmutation should cost nothing"
