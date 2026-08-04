"""Walk every route and fail on two things: any 5xx, and any route that never
once succeeded.

The second half is the part that earns its keep. `import server` succeeding
proves nothing, and neither does a route returning 4xx — a route that rejects
*every possible input* is as dead as one that raises, and it looks identical from
outside. Tracking "never once succeeded" separately from "crashed" is what
surfaced three dead routes in the last pass:

  - GET /game/professions/mine       ImportError on every call
  - five Mage routes                 KeyError: '_id' on every call
  - /game/{druid,rogue}/passives     the only 2 of 11 masteries with no route

Four of those five Mage routes never even reached their bug under test, because a
wrong-shaped payload 422'd first. That is why `contracts.py` exists.

Run: pytest tests/integration -m integration -s
(`-s` shows the per-route table, which is the useful output when this fails.)
"""
from __future__ import annotations

import ast
import collections
import os
import sys

import pytest

pytestmark = pytest.mark.integration

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_HERE))
SERVER_PY = os.path.join(_ROOT, "backend", "server.py")


def _load_contracts():
    """Load contracts.py by path rather than via sys.path.

    Putting this directory on sys.path shadowed the unit suite: `tests/conftest.py`
    and `tests/integration/conftest.py` are both importable as `conftest`, so
    `from conftest import make_character` in eight unit modules started resolving
    to the integration one and the whole default run died at collection.
    """
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "erchis_test_contracts", os.path.join(_HERE, "contracts.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_c = _load_contracts()
ALCHEMIST_CF_ACTIONS = _c.ALCHEMIST_CF_ACTIONS
BARD_MODES = _c.BARD_MODES
INNATE_ACTIONS = _c.INNATE_ACTIONS
KNIGHT_OATHS = _c.KNIGHT_OATHS
SUMMON_MODES = _c.SUMMON_MODES
TELEPORT_FIELD = _c.TELEPORT_FIELD
TRAVEL_FIELD = _c.TRAVEL_FIELD
combat_body = _c.combat_body


# ---------------------------------------------------------------------------
# Route discovery — from the source, so a new route joins the matrix on its own.
# ---------------------------------------------------------------------------

def discover_routes() -> list[tuple[str, str, str]]:
    """(METHOD, path, handler_name) for every registered route."""
    with open(SERVER_PY, encoding="utf-8") as fh:
        tree = ast.parse(fh.read(), filename="server.py")
    out = []
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        for dec in node.decorator_list:
            if (isinstance(dec, ast.Call) and isinstance(dec.func, ast.Attribute)
                    and dec.func.attr in ("get", "post", "put", "delete", "patch")
                    and dec.args and isinstance(dec.args[0], ast.Constant)):
                out.append((dec.func.attr.upper(), dec.args[0].value, node.name))
    return sorted(set(out))


# ---------------------------------------------------------------------------
# Routes that cannot succeed for a single fresh player, with the reason.
#
# This list is printed on every run. It is a statement of what the matrix does
# NOT cover, not a way to hide failures — a silent cap reads as "covered
# everything" when it did not.
# ---------------------------------------------------------------------------

EXPECTED_UNREACHABLE = {
    "/api/auth/register": "the fixture already consumed the fresh email",
    "/api/game/character": "POST creates one character; a second is rejected",
    "/api/game/guilds/{guild_id}/join": "needs an existing guild",
    "/api/game/guilds/{guild_id}": "needs an existing guild id",
    "/api/game/guilds/{guild_id}/leave": "needs guild membership",
    "/api/game/heritage/boss": "needs heritage rank + an open continent window",
    "/api/game/trade/accept": "needs a counterparty's open offer",
    "/api/game/trade/cancel": "needs an open offer of your own",
    "/api/game/quests/{quest_id}/claim":
        "400 'objectives not complete' — needs a quest actually finished, which "
        "means grinding a kill/gather count the matrix does not attempt",
}

#: Routes whose success requires destructive or irreversible state changes that
#: would invalidate the rest of the walk. Called last, or not at all.
DESTRUCTIVE = {
    "/api/game/character/delete",
    "/api/auth/logout",
}


class Walker:
    """Drives the API and records ok / 4xx / 5xx per route template."""

    def __init__(self, s, base):
        self.s = s
        self.base = base
        self.stats = collections.defaultdict(
            lambda: {"ok": 0, "c4": 0, "c5": 0, "reasons": set()})
        self.ctx = {}

    def call(self, method, template, path=None, **kw):
        url = f"{self.base}{path or template}"
        try:
            r = self.s.request(method, url, timeout=25, **kw)
        except Exception as exc:  # noqa: BLE001
            st = self.stats[f"{method} {template}"]
            st["c5"] += 1
            st["reasons"].add(f"transport: {type(exc).__name__}")
            return None
        st = self.stats[f"{method} {template}"]
        if r.status_code < 400:
            st["ok"] += 1
        elif r.status_code < 500:
            st["c4"] += 1
            detail = ""
            try:
                detail = str(r.json().get("detail", ""))[:70]
            except Exception:  # noqa: BLE001
                detail = r.text[:70]
            st["reasons"].add(f"{r.status_code}: {detail}")
        else:
            st["c5"] += 1
            st["reasons"].add(f"{r.status_code}: {r.text[:120]}")
        return r


def _make_character(w, mastery="knight", race="human", role="fighter"):
    org = w.call("GET", "/api/game/data/origins/{mastery_id}",
                 f"/api/game/data/origins/{mastery}")
    origins = org.json().get("origins", []) if org is not None and org.ok else []
    por = w.call("GET", "/api/game/data/portraits")
    ports = por.json().get("portraits", []) if por is not None and por.ok else []
    if not origins or not ports:
        return None
    body = {"name": f"Mx{os.urandom(3).hex()}", "race": race, "role": role,
            "mastery": mastery, "origin": origins[0]["id"],
            "portrait_id": ports[0]["id"], "racial_gift": "oathbound",
            "oath": "I will hold the line."}
    r = w.call("POST", "/api/game/character", json=body)
    if r is None or not r.ok:
        return None
    ch = w.call("GET", "/api/game/character")
    return ch.json()["character"] if ch is not None and ch.ok else None


def _walk_everything(w, mastery="knight"):
    """Exercise the surface, following the chains from contracts.py."""
    ch = _make_character(w, mastery=mastery)
    if not ch:
        return
    w.ctx["ch"] = ch
    biome = ch.get("current_biome")

    # --- plain GETs: no arguments, must simply not explode -----------------
    for path in ("/api/game/character", "/api/game/data/races",
                 "/api/game/data/roles", "/api/game/data/masteries",
                 "/api/game/data/portraits", "/api/game/data/towns",
                 "/api/game/data/quests", "/api/game/data/heritage",
                 "/api/game/data/mastery-passives", "/api/game/quests/available",
                 "/api/game/announcements", "/api/game/events",
                 "/api/game/events/active", "/api/game/leaderboard",
                 "/api/game/npcs", "/api/game/waystones", "/api/game/reputation",
                 "/api/game/bestiary", "/api/game/exploration",
                 "/api/game/discoveries", "/api/game/tools",
                 "/api/game/tools/all", "/api/game/professions/mine",
                 "/api/game/professions/catalog", "/api/game/craft/queue",
                 "/api/game/world/time", "/api/game/guilds",
                 "/api/game/teleporter/destinations", "/api/game/heritage/current",
                 "/api/game/heritage/tokens", "/api/game/heritage/progress",
                 "/api/game/heritage/milestones", "/api/game/heritage/calendar",
                 "/api/game/heritage/ladder", "/api/game/heritage/history",
                 "/api/game/heritage/quests/daily", "/api/game/mage/library",
                 "/api/game/mage/loadouts", "/api/game/rogue/innate",
                 "/api/auth/me"):
        w.call("GET", path)

    # --- every mastery's passive route ------------------------------------
    for m in ("knight", "paladin", "priest", "lancer", "assassin", "hunter",
              "alchemist", "mage", "rogue", "bard", "druid"):
        w.call("GET", "/api/game/{mastery}/passives", f"/api/game/{m}/passives")

    # --- biome: explore to unlock hunt/gather targets ----------------------
    if biome:
        w.call("GET", "/api/game/data/biome/{biome_id}/actions",
               f"/api/game/data/biome/{biome}/actions")
        for _ in range(14):
            w.call("POST", "/api/game/action",
                   json={"action_id": "explore", "biome_id": biome, "target_id": None})
        acts = w.call("GET", "/api/game/data/biome/{biome_id}/actions",
                      f"/api/game/data/biome/{biome}/actions")
        actions = acts.json().get("actions", []) if acts is not None and acts.ok else []
        for a in actions:
            for node in (a.get("resource_nodes") or [])[:2]:
                w.call("POST", "/api/game/action",
                       json={"action_id": a["id"], "biome_id": biome,
                             "target_id": node["id"]})

        # --- combat chain: start -> turn(s) -> skin/abandon ---------------
        targets = [t for a in actions if a["id"] == "hunt"
                   for t in (a.get("targets") or [])]
        targets.sort(key=lambda t: t.get("threat", 99))
        if targets:
            r = w.call("POST", "/api/game/combat/start",
                       json={"biome_id": biome, "monster_id": targets[0]["id"]})
            if r is not None and r.ok:
                cid = r.json()["state"]["combat_id"]
                w.call("POST", "/api/game/combat/telegraph", json={"combat_id": cid})
                # Real paths, confirmed against server.py. The obvious guesses
                # (/combat/knight/oath, /combat/druid/summon-mode) do not exist
                # and 404 for every payload — which is exactly what a dead route
                # looks like, hence the matrix flagged them.
                if mastery == "knight":
                    for oath in KNIGHT_OATHS:
                        w.call("POST", "/api/game/knight/oath",
                               json={"combat_id": cid, "oath": oath})
                if mastery == "druid":
                    for mode in SUMMON_MODES:
                        w.call("POST", "/api/game/combat/summon_mode",
                               json={"combat_id": cid, "mode": mode})
                won = False
                for i in range(24):
                    rr = w.call("POST", "/api/game/combat/turn",
                                json=combat_body(cid, INNATE_ACTIONS[i % len(INNATE_ACTIONS)]))
                    if rr is None or not rr.ok:
                        break
                    res = rr.json()["result"]
                    if mastery == "alchemist" and i >= 3:
                        for act in ALCHEMIST_CF_ACTIONS:
                            w.call("POST", "/api/game/combat/alchemist/cf",
                                   json={"combat_id": cid, "action": act})
                    if res.get("victory") is not None:
                        won = bool(res.get("victory"))
                        break
                if won:
                    # only reachable on a dead monster
                    w.call("POST", "/api/game/combat/skin", json={"combat_id": cid})
                w.call("POST", "/api/game/combat/abandon", json={})

    # --- quests: accept -> claim -> abandon --------------------------------
    q = w.call("GET", "/api/game/quests/available")
    avail = q.json().get("available", []) if q is not None and q.ok else []
    if avail:
        qid = avail[0]["id"]
        for verb in ("accept", "claim", "abandon"):
            w.call("POST", "/api/game/quests/{quest_id}/" + verb,
                   f"/api/game/quests/{qid}/{verb}", json={})

    # --- towns ------------------------------------------------------------
    t = w.call("GET", "/api/game/data/towns")
    towns = t.json().get("towns", []) if t is not None and t.ok else []
    for town in towns[:2]:
        tid = town["id"]
        w.call("POST", "/api/game/town/visit", json={"town_id": tid})
        for path in ("/api/game/town/market", "/api/game/town/gem-shop"):
            w.call("GET", path, params={"town_id": tid})
        w.call("GET", "/api/game/data/teachers", params={"town_id": tid})
        w.call("POST", "/api/game/town/sanctuary", json={"town_id": tid})

        # Sell gathered materials. This both exercises market/sell and funds the
        # 100g travel fee below — starting gold is 75, so travel is unaffordable
        # for a fresh character and would otherwise never succeed.
        cur = w.call("GET", "/api/game/character")
        if cur is not None and cur.ok:
            c = cur.json()["character"]
            equipped = set((c.get("equipped") or {}).values())
            for it in (c.get("inventory") or []):
                iid = it.get("item_id") or it.get("instance_id")
                if iid:
                    w.call("POST", "/api/game/town/market/sell",
                           json={"item_id": iid, "quantity": int(it.get("quantity", 1))})
            # Materials alone do not cover the 100g teleporter and 100g overland
            # fees, so liquidate spare gear too. Equipped items are left alone.
            for inst in (c.get("item_instances") or []):
                iid = inst.get("instance_id")
                if iid and iid not in equipped:
                    w.call("POST", "/api/game/town/market/sell",
                           json={"item_id": iid, "quantity": 1})
        mk = w.call("GET", "/api/game/town/market", params={"town_id": tid})
        if mk is not None and mk.ok:
            stock = (mk.json().get("items") or mk.json().get("stock") or [])[:1]
            for it in stock:
                w.call("POST", "/api/game/town/market/buy",
                       json={"item_id": it.get("id") or it.get("item_id"),
                             "quantity": 1})

        # The Grand Teleporter is only usable from inside a hometown, so this must
        # happen before town/leave — calling it out in the biome returns 403.
        here = (w.ctx.get("ch") or {}).get("current_continent") or "valeria"
        dest = "mushkara" if here != "mushkara" else "valeria"
        w.call("POST", "/api/game/teleporter/travel", json={TELEPORT_FIELD: dest})
        w.call("POST", "/api/game/character/travel", json={TRAVEL_FIELD: dest})
        w.call("POST", "/api/game/town/leave", json={})

    # --- npcs / items: path params need a real id -------------------------
    n = w.call("GET", "/api/game/npcs")
    npcs = n.json().get("npcs", []) if n is not None and n.ok else []
    for npc in npcs[:2]:
        w.call("GET", "/api/game/npc/{npc_id}", f"/api/game/npc/{npc['id']}")
    ch2 = w.call("GET", "/api/game/character")
    if ch2 is not None and ch2.ok:
        for inst in (ch2.json()["character"].get("item_instances") or [])[:2]:
            w.call("GET", "/api/game/item/{instance_id}/details",
                   f"/api/game/item/{inst['instance_id']}/details")

    # Travel is driven from inside the town loop above: the teleporter is
    # hometown-only and the overland route charges 100g, so both need the town
    # visit and the market sale to have happened first.


@pytest.fixture(scope="module")
def matrix(request):
    """Walk the surface once per module across several masteries."""
    import random
    import requests

    base = os.environ.get("ERCHIS_TEST_BASE", "http://127.0.0.1:8000/api").rsplit("/api", 1)[0]
    try:
        if requests.get(f"{base}/api/health", timeout=5).status_code != 200:
            pytest.skip("server unhealthy")
    except Exception as exc:  # noqa: BLE001
        pytest.skip(f"no server ({type(exc).__name__})")

    combined = collections.defaultdict(
        lambda: {"ok": 0, "c4": 0, "c5": 0, "reasons": set()})
    # Masteries with distinct resource systems, so mastery-specific routes and
    # the hook order are all exercised.
    for mastery, race, role in (("knight", "human", "fighter"),
                                ("mage", "elf", "scholar"),
                                ("alchemist", "human", "scholar"),
                                ("druid", "sylvan", "healer"),
                                ("bard", "half_elf", "scout")):
        s = requests.Session()
        n = random.randint(10 ** 9, 10 ** 10)
        email = f"mx{n}@test.local"
        s.post(f"{base}/api/auth/register",
               json={"email": email, "password": "hunter2hunter2",
                     "display_name": f"MX{n % 9999}"})
        s.post(f"{base}/api/auth/login",
               json={"email": email, "password": "hunter2hunter2"})
        w = Walker(s, base)
        try:
            _walk_everything(w, mastery=mastery)
        finally:
            for k, v in w.stats.items():
                combined[k]["ok"] += v["ok"]
                combined[k]["c4"] += v["c4"]
                combined[k]["c5"] += v["c5"]
                combined[k]["reasons"] |= v["reasons"]
    return dict(combined)


def _report(matrix):
    lines = [f"{'route':<58} {'ok':>4} {'4xx':>4} {'5xx':>4}"]
    for key in sorted(matrix):
        v = matrix[key]
        lines.append(f"{key:<58} {v['ok']:>4} {v['c4']:>4} {v['c5']:>4}")
    return "\n".join(lines)


def test_no_route_returns_5xx(matrix):
    """A 5xx is an unhandled exception in a handler body — always a bug."""
    broken = {k: sorted(v["reasons"])[:2] for k, v in matrix.items() if v["c5"]}
    assert not broken, (
        f"{len(broken)} route(s) returned 5xx:\n"
        + "\n".join(f"  {k}\n      {r}" for k, r in sorted(broken.items()))
        + "\n\n" + _report(matrix)
    )


def test_every_called_route_succeeded_at_least_once(matrix):
    """A route that never succeeds is dead, whatever status it returns.

    This is the check that found the three dead routes. It is deliberately
    separate from the 5xx check: those routes returned 4xx/ImportError-shaped
    failures and would otherwise have been filed as "gated, probably fine".
    """
    never = {}
    for key, v in matrix.items():
        if v["ok"]:
            continue
        template = key.split(" ", 1)[1]
        if template in EXPECTED_UNREACHABLE or template in DESTRUCTIVE:
            continue
        never[key] = sorted(v["reasons"])[:3]
    assert not never, (
        f"{len(never)} route(s) were called but never once succeeded — each is "
        "either dead or needs its contract added to contracts.py:\n"
        + "\n".join(f"  {k}\n      {r}" for k, r in sorted(never.items()))
    )


def test_coverage_is_reported_not_assumed(matrix, capsys):
    """State plainly what the matrix did and did not reach.

    A matrix that silently skips half the surface reads as "everything passes".
    This test always passes; it exists so the numbers are printed.
    """
    # server.py declares routes on a router mounted under /api, so the decorator
    # paths lack the prefix the matrix calls with. Normalise or every route reads
    # as uncalled and the coverage figure is meaningless.
    all_routes = {f"{m} /api{p}" for m, p, _ in discover_routes()}
    called = set(matrix)
    uncalled = sorted(all_routes - called)
    with capsys.disabled():
        print(f"\nroutes discovered: {len(all_routes)}")
        print(f"routes exercised:  {len(called)}")
        print(f"routes not called: {len(uncalled)}")
        print(f"declared unreachable: {len(EXPECTED_UNREACHABLE)} "
              f"(+{len(DESTRUCTIVE)} destructive, skipped by design)")
        if uncalled:
            print("\nnot called by this matrix (no contract yet):")
            for r in uncalled:
                print(f"  {r}")
        print("\n" + _report(matrix))
