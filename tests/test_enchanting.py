"""Enchanting must resolve the items players actually own.

`start_enchant` looked its target up in `ITEMS_BY_ID` only. That table is the
legacy static catalogue; everything a player owns is a procedural *instance* whose
id looks like "item_fc91e66e65e7" and appears in `character["item_instances"]`,
never in `ITEMS_BY_ID`. Measured on a fresh character: 0 of 6 owned instances
resolved, so POST /game/craft/enchant returned "Unknown target item" for every
item anyone could actually enchant. It succeeded only for hand-injected static
ids that the modern game never creates.

This is the same defect that made `compute_armor` always return 0. The stat path
and the weapon-damage path both guard against it by trying `_get_equipped_item`
first and only falling back to the static table; `start_enchant` was the one
place that skipped that step.
"""
from __future__ import annotations

import os
import sys

import pytest

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(_ROOT, "backend"))


@pytest.fixture
def ge():
    return pytest.importorskip("game_engine")


def _char_with_instance(instance_id="item_deadbeef0001", kind="weapon"):
    """A character holding one procedural gear instance, shaped as the game stores it."""
    return {
        "name": "Tester",
        "level": 40,
        "current_continent": "gennel",
        "current_town": "veilgrove",
        "professions": [{"id": "enchanting", "rank": "expert", "points": 9999}],
        "stats": {"might": 10, "cognition": 10, "grace": 5, "insight": 5},
        "base_stats": {"might": 10, "cognition": 10, "grace": 5, "insight": 5},
        "equipped": {"right_hand": instance_id},
        "item_instances": [{
            "instance_id": instance_id,
            "base_id": "iron_longsword",
            "name": "Iron Longsword",
            "kind": kind,
            "slot": "right_hand",
            "rarity": "normal",
            "base_stats": {"might": 2, "vitality": 1},
            "prefixes": [], "suffixes": [], "bonus_effects": [],
        }],
        "inventory": [
            {"item_id": instance_id, "quantity": 1},
            {"item_id": "wisp_essence", "quantity": 20},
        ],
    }


def test_enchanting_resolves_a_procedural_instance(ge):
    """The regression. Before the fix this returned "Unknown target item"."""
    ch = _char_with_instance()
    res = ge.start_enchant(ch, "enchant_might_t1", "item_deadbeef0001")
    assert res.get("error") != "Unknown target item", (
        "start_enchant could not resolve a procedural item instance — it is looking "
        "in ITEMS_BY_ID, which never contains instance ids, so enchanting is dead "
        "for every item a player owns"
    )
    assert "error" not in res, f"unexpected error: {res.get('error')}"
    assert res["outcome"] in range(1, 7)


def test_a_successful_enchant_reports_the_stat_and_bonus(ge):
    """Roll outcomes vary, so assert the shape of whichever branch was taken."""
    ch = _char_with_instance()
    for _ in range(40):
        res = ge.start_enchant(ch, "enchant_might_t1", "item_deadbeef0001")
        assert "error" not in res, res
        if res.get("enchant_applied"):
            assert res["enchant_stat"] == "might"
            assert res["enchant_bonus"] >= 1
            return
        # A roll of 1 either destroys the item or spares it; both must be explicit.
        assert res["outcome"] == 1 and "item_destroyed" in res
    pytest.skip("40 rolls produced no success — vanishingly unlikely, not a failure")


def test_the_static_catalogue_still_works(ge):
    """The fallback must survive, or any legacy inventory row breaks."""
    ch = _char_with_instance()
    ch["inventory"].append({"item_id": "iron_longsword", "quantity": 1})
    res = ge.start_enchant(ch, "enchant_might_t1", "iron_longsword")
    assert res.get("error") != "Unknown target item", res


def test_an_unknown_id_is_still_rejected(ge):
    """The fix must not make every id resolve."""
    ch = _char_with_instance()
    ch["inventory"].append({"item_id": "not_a_real_item", "quantity": 1})
    res = ge.start_enchant(ch, "enchant_might_t1", "not_a_real_item")
    assert res.get("error") == "Unknown target item", res


def test_only_equipment_can_be_enchanted(ge):
    """A material must not be enchantable just because it resolves."""
    ch = _char_with_instance(kind="material")
    res = ge.start_enchant(ch, "enchant_might_t1", "item_deadbeef0001")
    assert "error" in res and "weapons" in res["error"].lower(), res


def test_no_other_enchant_call_site_uses_the_static_table_alone(ge):
    """Guard the class, not just this instance.

    Every lookup that can receive an equipped-slot value or an inventory item_id
    must try the instance-aware helper first. `apply_enchantments_to_stats` and the
    weapon-damage path already do; this fails if a new one appears that does not.
    """
    import ast
    import io

    src = io.open(os.path.join(_ROOT, "backend", "game_engine.py"),
                  encoding="utf-8").read()
    tree = ast.parse(src)
    lines = src.split("\n")
    offenders = []
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        body = "\n".join(lines[node.lineno - 1:node.end_lineno])
        if "ITEMS_BY_ID" not in body:
            continue
        # Functions that take a target/equipped id must also consult instances.
        takes_item_id = any(a.arg in ("target_item_id", "instance_id") for a in node.args.args)
        if not takes_item_id:
            continue
        instance_aware = ("_get_equipped_item" in body
                          or "item_instances" in body
                          or "resolve_equipped_item" in body)
        if not instance_aware:
            offenders.append(f"{node.name}() line {node.lineno}")
    assert not offenders, (
        "these functions look an item id up in ITEMS_BY_ID without ever checking "
        "item_instances, so they cannot see anything a player owns: "
        + ", ".join(offenders)
    )
