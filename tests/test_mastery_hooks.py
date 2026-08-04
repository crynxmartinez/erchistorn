"""The mastery hook system.

`combat_turn` was 2,270 lines with 140 `_is_<mastery>(character)` guard calls and
441 branches — eleven resource systems interleaved into one spine. These tests pin
the extraction contract so the spine cannot silently regain that shape.

Behaviour equivalence during extraction is guarded by `tests/golden.py`
(1,584 scenarios); this file guards the *structure*.
"""
from __future__ import annotations

import re
import os

import pytest

from conftest import make_character

MASTERIES = ["knight", "paladin", "lancer", "rogue", "bard", "alchemist",
             "mage", "priest", "druid", "assassin", "hunter"]


def _engine_src():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return open(os.path.join(root, "backend", "game_engine.py"), encoding="utf-8").read()


def _combat_turn_body():
    lines = _engine_src().split("\n")
    start = next(i for i, l in enumerate(lines) if l.startswith("def combat_turn("))
    end = next(i for i in range(start + 1, len(lines)) if lines[i].startswith("def "))
    return lines[start:end]


# ============================================================
# Registry contract
# ============================================================

def test_every_mastery_has_registered_hooks():
    import mastery_hooks as mh
    missing = sorted(set(MASTERIES) - set(mh.registered()))
    assert not missing, f"masteries with no hooks registered: {missing}"


def test_hook_order_covers_every_mastery():
    """A mastery absent from HOOK_ORDER would still run, but at the end — a silent
    ordering change. Ordering is observable, so it must be declared."""
    import mastery_hooks as mh
    missing = sorted(set(mh.registered()) - set(mh.HOOK_ORDER))
    assert not missing, f"registered but not in HOOK_ORDER: {missing}"


def test_hooks_for_returns_declared_order():
    import mastery_hooks as mh
    ch = make_character(mastery="knight", role="fighter")
    ch["masteries"] = ["mage", "knight", "priest"]
    got = [h.mastery for h in mh.hooks_for(ch)]
    expected = [m for m in mh.HOOK_ORDER if m in {"mage", "knight", "priest"}]
    assert got == expected, f"hook order {got} does not follow HOOK_ORDER {expected}"


def test_hooks_for_ignores_masteries_the_character_lacks():
    import mastery_hooks as mh
    ch = make_character(mastery="knight", role="fighter")
    ch["masteries"] = ["knight"]
    assert [h.mastery for h in mh.hooks_for(ch)] == ["knight"]


def test_hooks_for_handles_no_masteries():
    import mastery_hooks as mh
    ch = make_character(mastery="knight", role="fighter")
    ch["masteries"] = []
    assert mh.hooks_for(ch) == []


def test_register_rejects_a_class_without_a_mastery_name():
    import mastery_hooks as mh

    class Nameless(mh.BaseHooks):
        pass

    with pytest.raises(ValueError):
        mh.register(Nameless)


# ============================================================
# Hook protocol
# ============================================================

PHASES = ["on_turn_start", "on_action_selected", "on_damage_computed",
          "on_hit_landed", "on_enemy_turn_start", "on_incoming_damage",
          "on_turn_end"]


@pytest.mark.parametrize("phase", PHASES)
def test_base_hooks_supplies_every_phase(phase):
    """A mastery must be able to override only what it participates in."""
    import mastery_hooks as mh
    assert callable(getattr(mh.BaseHooks, phase, None)), f"BaseHooks lacks {phase}"


@pytest.mark.parametrize("mastery", MASTERIES)
def test_every_hook_class_satisfies_the_protocol(mastery):
    import mastery_hooks as mh
    cls = mh._REGISTRY[mastery]
    for phase in PHASES:
        assert callable(getattr(cls, phase, None)), f"{cls.__name__} lacks {phase}"


def test_turn_context_exposes_the_ratios_hooks_need(ge, gd):
    import mastery_hooks as mh
    ch = make_character(mastery="knight", role="fighter")
    ch["hp"] = 50
    ch["max_hp"] = 100
    ctx = mh.TurnContext(character=ch, state={"monster_hp": 30, "monster_max_hp": 60},
                         monster={}, log=[])
    assert ctx.hp_ratio == pytest.approx(0.5)
    assert ctx.enemy_hp_ratio == pytest.approx(0.5)


def test_turn_context_note_appends_to_the_log():
    import mastery_hooks as mh
    log = []
    ctx = mh.TurnContext(character={}, state={}, monster={}, log=log)
    ctx.note("test", "hello")
    assert log == [{"kind": "test", "text": "hello"}]


def test_turn_context_ratios_survive_zero_max():
    """Division guards — a monster with 0 max HP must not crash a hook."""
    import mastery_hooks as mh
    ctx = mh.TurnContext(character={"hp": 0, "max_hp": 0}, monster={},
                         state={"monster_hp": 0, "monster_max_hp": 0}, log=[])
    assert ctx.hp_ratio == 0
    assert ctx.enemy_hp_ratio == 0


# ============================================================
# The spine must not regain its old shape
# ============================================================

def test_combat_turn_guard_count_does_not_regress():
    """46 guards remain, down from 140. Ratchets: may fall, never rise."""
    body = "\n".join(_combat_turn_body())
    guards = len(re.findall(r"_is_(\w+)\(character\)", body))
    assert guards <= 46, (
        f"combat_turn has {guards} mastery guards, up from the 46 baseline. "
        "Add logic to backend/mastery/ rather than inline in the spine."
    )


def test_combat_turn_length_does_not_regress():
    """1,353 lines, down from 2,270 (-40%). Same ratchet."""
    n = len(_combat_turn_body())
    assert n <= 1353, (
        f"combat_turn is {n} lines, up from the 1353 baseline. "
        "New mastery logic belongs in backend/mastery/."
    )


def test_stat_mod_expiry_is_not_re_duplicated():
    """21 copies of the same expiry loop were collapsed into tick_stat_mods().
    8 remain (shapes that differ materially); this stops the count climbing."""
    src = _engine_src()
    assert src.count('if entry["duration"] > 0:') <= 8, (
        "a stat_mod expiry loop was hand-rolled again — use tick_stat_mods()"
    )


def test_shared_stat_mod_helpers_exist(ge):
    for fn in ("tick_stat_mods", "apply_self_stat_mods", "apply_enemy_stat_mods"):
        assert callable(getattr(ge, fn, None)), f"{fn} is missing"


# ============================================================
# The shared helpers behave as the copies did
# ============================================================

def test_tick_stat_mods_refunds_on_expiry(ge):
    stats = {"might": 10}
    state = {"k": [{"mods": {"might": 3}, "duration": 0}]}
    ge.tick_stat_mods(state, "k", stats)
    assert stats["might"] == 7, "expired mod was not refunded"
    assert state["k"] == []


def test_tick_stat_mods_decrements_survivors(ge):
    stats = {"might": 10}
    state = {"k": [{"mods": {"might": 3}, "duration": 2}]}
    ge.tick_stat_mods(state, "k", stats)
    assert stats["might"] == 10, "a live mod was refunded early"
    assert state["k"][0]["duration"] == 1


def test_tick_stat_mods_tolerates_an_empty_bucket(ge):
    state = {}
    ge.tick_stat_mods(state, "missing", {})  # must not raise


def test_apply_self_stat_mods_banks_and_applies(ge):
    ch = {"stats": {"might": 5}}
    state, log = {}, []
    ge.apply_self_stat_mods(state, ch, {"might": 4}, 3, "k", log, "kind", "Label: ")
    assert ch["stats"]["might"] == 9
    assert state["k"] == [{"mods": {"might": 4}, "duration": 3}]
    assert log and log[0]["kind"] == "kind"


def test_apply_self_stat_mods_copies_the_skill_dict(ge):
    """Aliasing the skill's own dict would let a later mutation corrupt the
    static skill definition for every character in the process."""
    ch = {"stats": {}}
    source = {"might": 2}
    state = {}
    ge.apply_self_stat_mods(state, ch, source, 2, "k", [], "", "")
    state["k"][0]["mods"]["might"] = 99
    assert source["might"] == 2, "the skill definition was mutated"


def test_apply_enemy_stat_mods_can_defer_application(ge):
    state = {}
    ge.apply_enemy_stat_mods(state, {"grace": -2}, 2, "k")
    assert state["k"] == [{"mods": {"grace": -2}, "duration": 2}]
    assert "monster_stats" not in state, "deferred mod was applied immediately"


def test_apply_enemy_stat_mods_can_apply_immediately(ge):
    state = {}
    ge.apply_enemy_stat_mods(state, {"grace": -2}, 2, "k", apply_now=True)
    assert state["monster_stats"]["grace"] == -2
