"""No player-facing text may name a town or continent that no longer exists.

The canon rename (Aetheria->Valeria, Ironhold->Oathspire, ...) is applied to
*ids* at import by `_migrate_teachers_to_canon` and to saved characters by the
v1 schema migration. Neither touches free text, so prose kept describing a world
the game no longer has. Found by playing the game: the Adventurer's Lounge in
Oathspire offered a bounty from "Ironhold's smiths", and the opening announcement
welcomed players to "the gates of Aetheria".

Three quest briefs and one announcement were affected. This test fails if any
come back.
"""
from __future__ import annotations

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "backend"))

# Pre-canon display name -> canon replacement.
RENAMED_TOWNS = {
    "Ironhold": "Oathspire",
    "Willowmere": "Riverguard",
    "Emberhold": "Grunhold",
    "Ashvault": "Warforge",
    "Mourngate": "Elaris",
    "Black Hollow": "Silvergate",
    "Frostwatch": "Deepstone",
    "Sun-Moon Haven": "Solunara",
    "Windrest": "Starfall Watch",
    "Sun Bazaar": "Rindivar Grove",
    "Whispering Cairns": "Beastcairn",
    "Emerald Bough": "Veilgrove",
}
RENAMED_CONTINENTS = {"Aetheria": "Valeria", "Zephyria": "Haya"}
DEAD_NAMES = {**RENAMED_TOWNS, **RENAMED_CONTINENTS}

# Keys whose values a player reads verbatim.
PROSE_KEYS = ("brief", "body", "desc", "description", "text", "title", "name", "flavor")


def _walk(node, path="", out=None):
    """Yield (path, key, string) for every prose-bearing string in a structure."""
    if out is None:
        out = []
    if isinstance(node, dict):
        for k, v in node.items():
            if isinstance(v, str) and k in PROSE_KEYS:
                out.append((path, k, v))
            else:
                _walk(v, f"{path}.{k}" if path else str(k), out)
    elif isinstance(node, (list, tuple)):
        for i, v in enumerate(node):
            _walk(v, f"{path}[{i}]", out)
    return out


def _collections():
    """Every content table that carries player-visible prose."""
    import game_data as gd

    tables = {}
    for name in dir(gd):
        if name.startswith("_") or not name.isupper():
            continue
        val = getattr(gd, name)
        if isinstance(val, (list, dict)) and val:
            tables[name] = val
    return tables


def test_no_prose_names_a_renamed_town_or_continent():
    offenders = []
    for table, data in _collections().items():
        for path, key, text in _walk(data):
            for dead, canon in DEAD_NAMES.items():
                # Word-ish check: avoid matching a canon name that merely
                # contains a dead one as a substring.
                if dead in text:
                    offenders.append(f"{table}.{path}[{key}]: {dead!r} (use {canon!r}) -- {text[:70]}")
    assert not offenders, (
        f"{len(offenders)} player-facing string(s) name a town/continent that no "
        "longer exists:\n  " + "\n  ".join(sorted(offenders)[:20])
    )


@pytest.mark.parametrize("dead,canon", sorted(DEAD_NAMES.items()))
def test_canon_target_actually_exists(dead, canon):
    """Guard the guard: every replacement must name something real.

    Without this, a typo in the map above would make the test above pass while
    the prose points at a town that does not exist either.
    """
    import game_data as gd

    haystack = ""
    for name in ("TOWNS", "TOWNS_BY_ID", "CONTINENTS"):
        val = getattr(gd, name, None)
        if val:
            haystack += str(val)
    import world_data as wd
    haystack += str(getattr(wd, "TOWN_ID_MAP", {}))
    assert canon.lower().replace(" ", "_") in haystack.lower().replace(" ", "_"), (
        f"canon replacement {canon!r} for {dead!r} does not exist in the town or "
        "continent tables -- the rename map itself is wrong"
    )
