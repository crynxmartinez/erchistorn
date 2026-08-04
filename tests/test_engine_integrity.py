"""Static integrity checks over the engine modules.

Motivation: `_mage_get_cooldown_modifier` was *called* by combat_turn but defined
nowhere in the codebase. Every Mage who cast a skill hit a bare NameError and got
a 500 — the mastery was unplayable, and nothing caught it because combat_turn is
2,100+ lines with 137 mastery branch points and no test exercised that path.

A NameError inside a rarely-taken branch of a huge function is invisible until a
player finds it. These tests find it at CI time instead.
"""
from __future__ import annotations

import ast
import builtins
import os

import pytest

from _scope import undefined_names

_BACKEND = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "backend")

# Modules worth sweeping: the large hand-written logic files where a typo'd or
# never-implemented helper can hide inside a branch.
ENGINE_MODULES = ["game_engine.py", "game_data.py", "progression.py", "racial.py",
                  "heritage_system.py", "professions.py", "market.py", "exploration.py",
                  # The mastery extraction moved ~1,300 lines out of combat_turn into
                  # this package, and the sweep did not follow them. `outgoing.py`
                  # read a bare `turn` that the extraction had left out of its ctx
                  # unpack, so every Knight sworn to Vanguard 500'd on their strike.
                  "mastery_hooks.py",
                  os.path.join("mastery", "core.py"),
                  os.path.join("mastery", "lancer.py"),
                  os.path.join("mastery", "mitigation.py"),
                  os.path.join("mastery", "outgoing.py"),
                  os.path.join("mastery", "skill_effects.py")]


def _collect_bound_names(tree: ast.Module) -> set[str]:
    """Every name that module-level code could bind."""
    bound: set[str] = set(dir(builtins))

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            bound.add(node.name)
        elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
            bound.add(node.id)
        elif isinstance(node, ast.arg):
            bound.add(node.arg)
        elif isinstance(node, ast.alias):
            bound.add((node.asname or node.name).split(".")[0])
        elif isinstance(node, ast.ExceptHandler) and node.name:
            bound.add(node.name)
        elif isinstance(node, ast.Global):
            bound.update(node.names)
        elif isinstance(node, (ast.comprehension,)):
            for sub in ast.walk(node.target):
                if isinstance(sub, ast.Name):
                    bound.add(sub.id)
    return bound


def _collect_called_names(tree: ast.Module) -> set[str]:
    """Bare function names that get called, e.g. `foo(...)` but not `x.foo(...)`."""
    called: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            called.add(node.func.id)
    return called


@pytest.mark.parametrize("module", ENGINE_MODULES)
def test_no_calls_to_undefined_functions(module):
    """Every bare function call must resolve to something the module can see.

    This is the check that would have caught _mage_get_cooldown_modifier.
    """
    path = os.path.join(_BACKEND, module)
    if not os.path.exists(path):
        pytest.skip(f"{module} not present")

    with open(path, encoding="utf-8") as fh:
        tree = ast.parse(fh.read(), filename=module)

    bound = _collect_bound_names(tree)
    undefined = sorted(n for n in _collect_called_names(tree) if n not in bound)

    assert not undefined, (
        f"{module} calls functions that are never defined or imported: {undefined}"
    )


@pytest.mark.parametrize("module", ENGINE_MODULES)
def test_module_imports_cleanly(module):
    """Importing must not raise — catches syntax errors and bad import-time work."""
    path = os.path.join(_BACKEND, module)
    if not os.path.exists(path):
        pytest.skip(f"{module} not present")
    # Package members arrive as "mastery/core.py"; turn that into "mastery.core".
    __import__(module[:-3].replace(os.sep, ".").replace("/", "."))


@pytest.mark.parametrize("module", ENGINE_MODULES)
def test_no_undefined_names(module):
    """Every name a function *reads* must be visible from that function's scope.

    Distinct from `test_no_calls_to_undefined_functions`, which only inspects
    `ast.Call` nodes. A bare variable read is not a call, so that check could
    never catch `mastery/outgoing.py` reading `turn` — a name the extraction had
    dropped from the ctx unpack. Every Knight who swore the Oath of Vanguard got
    a 500 on their first strike; no golden scenario and no playthrough had ever
    selected that oath, so only a static read-scope sweep closes it.
    """
    path = os.path.join(_BACKEND, module)
    if not os.path.exists(path):
        pytest.skip(f"{module} not present")

    with open(path, encoding="utf-8") as fh:
        tree = ast.parse(fh.read(), filename=module)

    missing = undefined_names(tree)
    assert not missing, (
        f"{module} reads names not visible in scope — these raise at call time, "
        "not import time: "
        + ", ".join(f"{k} in {v[0]}() line {v[1]}"
                    for k, v in sorted(missing.items(), key=lambda x: x[1][1]))
    )


# ============================================================
# Mage regressions specifically
# ============================================================

def test_mage_cooldown_modifier_exists_and_returns_int(ge):
    from conftest import make_character
    ch = make_character(mastery="mage", role="scholar")
    result = ge._mage_get_cooldown_modifier(ch)
    assert isinstance(result, int)
    assert result >= 0


def test_mage_cooldown_modifier_rewards_quickened_mind(ge):
    from conftest import make_character
    plain = make_character(mastery="mage", role="scholar")
    plain["mage_equipped_passives"] = []
    quick = make_character(mastery="mage", role="scholar")
    quick["mage_equipped_passives"] = ["quickened_mind"]
    assert ge._mage_get_cooldown_modifier(quick) > ge._mage_get_cooldown_modifier(plain)


def test_mage_skill_tag_helpers_tolerate_no_skill(ge):
    """Innate actions pass skill=None. Regression: this raised AttributeError,
    so a Mage taking a basic strike with an empty skill bar got a 500."""
    from conftest import make_character
    ch = make_character(mastery="mage", role="scholar")

    assert ge._mage_get_skill_tags(None) == set()
    assert ge._mage_apply_passive_modifiers({}, ch, None, 10.0, []) is not None
    assert ge._mage_get_status_override(ch, None) is None
    assert ge._mage_get_extra_status(ch, None) is None
    ge._mage_check_phobia_implant({}, ch, None, [])  # must not raise
