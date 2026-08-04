"""Static integrity checks over server.py.

Motivation: `import server` succeeding proves almost nothing. A name referenced
only inside a route body raises `NameError` at *request* time, so the module
imports cleanly, the route registers, `len(app.routes)` looks right — and the
endpoint 500s the moment anyone calls it.

Two real cases found exactly this way, both invisible to every other check:

  - `PRIEST_PASSIVES` / `ALCHEMIST_PASSIVES` — the routes were added but the
    imports were not, so `/game/priest/passives` and `/game/alchemist/passives`
    both 500'd.
  - `RECIPES_BY_ID` — **`POST /game/craft` raised NameError on every call.**
    Pre-existing, and the entire crafting endpoint was dead.

This mirrors `test_engine_integrity.py`, which catches the same class in the
engine (`_mage_get_cooldown_modifier` was called but never defined).
"""
from __future__ import annotations

import ast
import builtins
import os

import pytest

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SERVER = os.path.join(_ROOT, "backend", "server.py")

# Names Python provides implicitly at module scope.
_IMPLICIT = {"__file__", "__name__", "__doc__", "__package__", "__spec__", "__loader__"}


def _tree():
    with open(SERVER, encoding="utf-8") as fh:
        return ast.parse(fh.read(), filename="server.py")


def _module_scope(tree: ast.Module) -> set[str]:
    """Names visible at module scope only.

    Deliberately does NOT walk into function bodies. An earlier version of this
    check used `ast.walk` over the whole tree, so a name assigned or imported
    inside *any* function counted as bound *everywhere*. That false-negative hid
    two live 500s:

      - `PROFESSION_RANKS` was imported locally in one function and read by two
        others — `/game/professions/catalog` NameError'd on every call.
      - `ch` is assigned in dozens of route bodies, so a route that read it
        *without* assigning it looked fine — `/game/heritage/current` NameError'd.

    Per-function scoping is the whole point of this check.
    """
    bound = set(dir(builtins)) | _IMPLICIT
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            bound.add(node.name)
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            for a in node.names:
                bound.add((a.asname or a.name).split(".")[0])
        elif isinstance(node, ast.Assign):
            for t in node.targets:
                for sub in ast.walk(t):
                    if isinstance(sub, ast.Name):
                        bound.add(sub.id)
        elif isinstance(node, (ast.AnnAssign, ast.AugAssign)):
            for sub in ast.walk(node.target):
                if isinstance(sub, ast.Name):
                    bound.add(sub.id)
        elif isinstance(node, (ast.For, ast.AsyncFor)):
            for sub in ast.walk(node.target):
                if isinstance(sub, ast.Name):
                    bound.add(sub.id)
        elif isinstance(node, (ast.With, ast.AsyncWith)):
            for item in node.items:
                if item.optional_vars:
                    for sub in ast.walk(item.optional_vars):
                        if isinstance(sub, ast.Name):
                            bound.add(sub.id)
        elif isinstance(node, (ast.If, ast.Try)):
            # Conditional module-level definitions (e.g. try/except imports).
            for sub in ast.walk(node):
                if isinstance(sub, ast.alias):
                    bound.add((sub.asname or sub.name).split(".")[0])
                elif isinstance(sub, ast.Name) and isinstance(sub.ctx, ast.Store):
                    bound.add(sub.id)
    return bound


def _function_locals(fn) -> set[str]:
    """Names bound inside one function: params, assignments, imports, loops."""
    local = set()
    for a in list(fn.args.args) + list(fn.args.kwonlyargs) + list(fn.args.posonlyargs):
        local.add(a.arg)
    if fn.args.vararg:
        local.add(fn.args.vararg.arg)
    if fn.args.kwarg:
        local.add(fn.args.kwarg.arg)
    for node in ast.walk(fn):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
            local.add(node.id)
        elif isinstance(node, ast.alias):
            local.add((node.asname or node.name).split(".")[0])
        elif isinstance(node, ast.arg):
            local.add(node.arg)
        elif isinstance(node, ast.ExceptHandler) and node.name:
            local.add(node.name)
        elif isinstance(node, ast.Global):
            local.update(node.names)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            local.add(node.name)
    return local


def test_no_undefined_names_in_server():
    """Every name a route body reads must be visible from that function's scope.

    Scoped per function — see `_module_scope` for why that matters.
    """
    tree = _tree()
    module = _module_scope(tree)
    missing = {}
    for fn in ast.walk(tree):
        if not isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        visible = module | _function_locals(fn)
        for node in ast.walk(fn):
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                if node.id not in visible:
                    missing.setdefault(node.id, (fn.name, node.lineno))
    assert not missing, (
        "server.py reads names not visible in scope — these raise NameError at "
        "request time, not import time: "
        + ", ".join(f"{k} in {v[0]}() line {v[1]}"
                    for k, v in sorted(missing.items(), key=lambda x: x[1][1]))
    )


def test_passive_tables_are_imported_for_every_mastery():
    """Each mastery's passive route needs its table in scope."""
    import sys
    sys.path.insert(0, os.path.join(_ROOT, "backend"))
    import game_data as gd

    tree = _tree()
    bound = _module_scope(tree)
    with open(SERVER, encoding="utf-8") as fh:
        src = fh.read()

    for mastery in [m["id"] for m in gd.MASTERIES]:
        table = f"{mastery.upper()}_PASSIVES"
        if table not in src:
            continue  # no route references it
        assert table in bound, (
            f"{table} is used in server.py but never imported — the "
            f"/game/{mastery}/passives route will 500"
        )


def test_every_mastery_has_a_passives_route():
    """The per-mastery passives path must answer for all eleven masteries.

    Druid and Rogue were the only two without one, so `/game/druid/passives`
    and `/game/rogue/passives` 404'd while the other nine answered. The earlier
    check above could not catch it: it `continue`s when the table is absent from
    the source, which is exactly the missing-route case.
    """
    import sys
    sys.path.insert(0, os.path.join(_ROOT, "backend"))
    import game_data as gd

    with open(SERVER, encoding="utf-8") as fh:
        src = fh.read()
    missing = [m["id"] for m in gd.MASTERIES
               if f'"/game/{m["id"]}/passives"' not in src]
    assert not missing, f"masteries with no /game/<id>/passives route: {missing}"


def _local_modules() -> set[str]:
    return {f[:-3] for f in os.listdir(os.path.join(_ROOT, "backend"))
            if f.endswith(".py") and not f.startswith("__")}


def test_every_from_import_resolves():
    """`from <local module> import <name>` must name something that exists.

    Import-time checks miss this entirely when the import sits *inside* a
    function: the module loads, the route registers, and the call raises
    ImportError only when a request arrives. `points_to_next_rank` was imported
    this way inside `my_professions` but never defined — its body had been left
    stranded after the `return` in `rank_from_xp` with the `def` line lost — so
    **GET /game/professions/mine raised ImportError on every call.**
    """
    import importlib
    import sys
    sys.path.insert(0, os.path.join(_ROOT, "backend"))

    local = _local_modules()
    bad = []
    for path in sorted(_local_modules()):
        fname = os.path.join(_ROOT, "backend", f"{path}.py")
        with open(fname, encoding="utf-8") as fh:
            tree = ast.parse(fh.read(), filename=f"{path}.py")
        for node in ast.walk(tree):
            if not isinstance(node, ast.ImportFrom) or node.module not in local:
                continue
            try:
                mod = importlib.import_module(node.module)
            except Exception as exc:  # pragma: no cover - import failure is its own bug
                bad.append(f"{path}.py:{node.lineno} cannot import {node.module}: {exc}")
                continue
            for alias in node.names:
                if alias.name == "*":
                    continue
                if not hasattr(mod, alias.name):
                    bad.append(f"{path}.py:{node.lineno} "
                               f"`from {node.module} import {alias.name}` "
                               f"— {node.module} has no such name")
    assert not bad, "unresolvable imports (these raise at request time):\n  " + "\n  ".join(bad)


def test_no_route_uses_mongo_id_from_the_serializing_helper():
    """`_get_character_or_404` pops `_id`, so `ch["_id"]` after it is a KeyError.

    The helper runs its result through `_serialize_doc`, which replaces the raw
    ObjectId `_id` with a string `id`. Five Mage routes (equip/unequip passive,
    research, loadout save/load) filtered on `ch["_id"]` anyway and raised
    `KeyError: '_id'` the moment they reached their update. Only one surfaced in
    testing because the other four 4xx'd on argument validation first — so the
    crash count was understated and a static check is the only reliable gate.
    The correct filter is the one 68 other call sites already use:
    `{"_id": ObjectId(ch["id"])}`.
    """
    tree = _tree()
    offenders = []
    for fn in ast.walk(tree):
        if not isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        # Variables assigned from the serializing helper.
        serialized = set()
        for node in ast.walk(fn):
            if not isinstance(node, ast.Assign):
                continue
            call = node.value
            if isinstance(call, ast.Await):
                call = call.value
            if (isinstance(call, ast.Call) and isinstance(call.func, ast.Name)
                    and call.func.id == "_get_character_or_404"):
                for t in node.targets:
                    if isinstance(t, ast.Name):
                        serialized.add(t.id)
        if not serialized:
            continue
        for node in ast.walk(fn):
            if (isinstance(node, ast.Subscript)
                    and isinstance(node.value, ast.Name)
                    and node.value.id in serialized
                    and isinstance(node.slice, ast.Constant)
                    and node.slice.value == "_id"):
                offenders.append(f'{fn.name}() line {node.lineno}: '
                                 f'{node.value.id}["_id"]')
    assert not offenders, (
        "these read `_id` off a doc that `_get_character_or_404` already "
        'serialized (use ObjectId(ch["id"])): ' + ", ".join(offenders)
    )


def test_every_route_has_a_unique_path_and_method():
    """A duplicate registration silently shadows the earlier handler."""
    tree = _tree()
    seen = {}
    dupes = []
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        for dec in node.decorator_list:
            if not isinstance(dec, ast.Call) or not isinstance(dec.func, ast.Attribute):
                continue
            method = dec.func.attr
            if method not in ("get", "post", "put", "delete", "patch"):
                continue
            if not dec.args or not isinstance(dec.args[0], ast.Constant):
                continue
            key = (method, dec.args[0].value)
            if key in seen:
                dupes.append(f"{method.upper()} {key[1]} ({seen[key]} and {node.name})")
            else:
                seen[key] = node.name
    assert not dupes, f"duplicate route registrations: {dupes}"


def test_no_route_body_is_empty():
    """A route whose body is only `pass` or a bare docstring returns None."""
    tree = _tree()
    stubs = []
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        if not any(isinstance(d, ast.Call) and isinstance(d.func, ast.Attribute)
                   and d.func.attr in ("get", "post", "put", "delete", "patch")
                   for d in node.decorator_list):
            continue
        body = [s for s in node.body
                if not (isinstance(s, ast.Expr) and isinstance(s.value, ast.Constant))]
        if not body or all(isinstance(s, ast.Pass) for s in body):
            stubs.append(node.name)
    assert not stubs, f"route handlers with no implementation: {stubs}"
