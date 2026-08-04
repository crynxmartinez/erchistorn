"""A new character's granted skills must be reachable by the combat engine.

`create_character` granted 2-3 `starting_skills` per mastery but set
`skill_bar` to `[None] * 10`. `_pick_next_skill` iterates `skill_bar` and
nothing else, so the auto-picker always returned None and a fresh character
never used a skill in combat — measured over real HTTP: 0 skill uses in 18
turns before the fix, 11 in 20 after. Everything downstream of skill use was
inert too: Combo Flow, Crescendo, Oath stacks and elemental imbue all build
from skills firing, which is why an Alchemist's combo-flow endpoint answered
"Insufficient CF" no matter how long the fight ran.

These tests assert the data contract (bar is populated, in the engine's shape,
with skills the character actually knows) rather than the HTTP behaviour, so
they run without a server or a database.
"""
from __future__ import annotations

import ast
import os

import pytest

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SERVER = os.path.join(_ROOT, "backend", "server.py")


def _create_character_source() -> str:
    with open(SERVER, encoding="utf-8") as fh:
        tree = ast.parse(fh.read(), filename="server.py")
    for node in ast.walk(tree):
        if (isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
                and node.name == "create_character"):
            with open(SERVER, encoding="utf-8") as fh:
                lines = fh.readlines()
            return "".join(lines[node.lineno - 1:node.end_lineno])
    pytest.fail("create_character not found in server.py")


def test_creation_does_not_hardcode_an_empty_skill_bar():
    """The literal that made every starting skill unreachable must be gone."""
    src = _create_character_source()
    assert '"skill_bar": [None] * 10' not in src, (
        "create_character sets skill_bar to an all-None list, so "
        "_pick_next_skill can never find a skill and starting skills are "
        "unreachable in combat"
    )


def test_creation_seeds_the_bar_from_starting_skills():
    src = _create_character_source()
    assert "starting_bar" in src and '"skill_bar": starting_bar' in src, (
        "create_character should seed skill_bar from starting_skills"
    )


def test_every_mastery_grants_at_least_one_startable_skill(gd):
    """A mastery with no grantable starting skill would ship an empty bar."""
    empty = [m["id"] for m in gd.MASTERIES if not m.get("starting_skills")]
    assert not empty, f"masteries with no starting_skills: {empty}"


def test_starting_skills_all_exist(gd):
    """A typo'd id would silently occupy a bar slot that can never fire."""
    unknown = []
    for m in gd.MASTERIES:
        for sid in m.get("starting_skills", []):
            if sid not in gd.SKILLS_BY_ID:
                unknown.append(f"{m['id']}:{sid}")
    assert not unknown, f"starting_skills referencing unknown skills: {unknown}"


def test_auto_picker_finds_a_seeded_skill(ge, gd):
    """`_pick_next_skill` must return a skill when the bar holds a usable one.

    Guards the actual mechanism: bar entries are bare skill-id strings (the same
    shape `/game/skill/assign` writes), and the picker reads them in slot order.
    """
    mastery = next(m for m in gd.MASTERIES if m.get("starting_skills"))
    # Pick a mastery skill with no weapon requirement and no trigger condition,
    # so the assertion tests the picker and not the gating rules.
    usable = [s for s in mastery["starting_skills"]
              if gd.SKILLS_BY_ID.get(s, {}).get("weapon_req", "none") == "none"
              and gd.SKILLS_BY_ID.get(s, {}).get("trigger", "always") == "always"]
    if not usable:
        pytest.skip(f"{mastery['id']} has no unconditional starting skill")

    character = {
        "name": "T", "level": 1, "mastery": mastery["id"],
        "masteries": [mastery["id"]], "hp": 100, "max_hp": 100,
        "stats": {"might": 5, "grace": 5, "insight": 5, "resilience": 5,
                  "vitality": 10, "cognition": 10, "essence": 10,
                  "durability": 10},
        "skills": [{"skill_id": s, "cooldown_remaining": 0} for s in usable],
        "skill_bar": list(usable) + [None] * (10 - len(usable)),
        "equipped": {}, "inventory": [],
    }
    state = {"turn": 0, "active": True, "monster_hp": 20, "monster_max_hp": 20,
             "skill_cooldowns": {}, "skill_capacity_used": 0,
             "max_skill_capacity": 8, "player_statuses": [],
             "monster_statuses": []}

    picked = ge._pick_next_skill(character, state, 1.0, 1.0, 0)
    assert picked in usable, (
        f"auto-picker returned {picked!r} for a bar holding {usable}"
    )

    # And the pre-fix state must genuinely yield nothing, so this test would
    # have failed before the fix rather than passing vacuously.
    character["skill_bar"] = [None] * 10
    assert ge._pick_next_skill(character, state, 1.0, 1.0, 0) is None
