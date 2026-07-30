"""Biome exploration, discovery, and global resource stocks.

- Stocks are in-memory and regenerate over time (per minute).
- Discoveries are per-character and reveal monsters/resource nodes as players explore.
"""
from __future__ import annotations

import random
from datetime import datetime, timezone
from typing import Any

from game_data import MONSTERS, get_monster
from regional_resources import RESOURCE_NODES, nodes_for_biome
from professions import PROFESSIONS_BY_ID

# kind can be "monster" or "node"
# key example: "monster:golden_plains:gray_wolf"
STOCKS: dict[str, dict] = {}
_INITIALIZED = False

# Rarity → base discovery weight (common easiest, legendary/exotic hardest)
DISCOVERY_RARITY_WEIGHTS: dict[str, int] = {
    "common": 100,
    "uncommon": 40,
    "rare": 12,
    "epic": 5,
    "legendary": 3,
    "exotic": 2,
}

# Rarity → (max_stock, regen_per_minute)
RARITY_STOCK_DEFAULTS: dict[str, tuple[int, float]] = {
    "common":    (1000, 1.0),          # 1 per minute
    "uncommon":  (500,  0.5),          # 1 every 2 minutes
    "rare":      (100,  0.2),          # 1 every 5 minutes
    "epic":      (20,   0.1),          # 1 every 10 minutes, max 20
    "legendary": (1,    1.0/1440.0),   # 1 per 24h, max 1
    "exotic":    (5,    1.0/1440.0),   # 1 per 24h, max 5
}


def _stock_key(kind: str, biome_id: str, entity_id: str) -> str:
    return f"{kind}:{biome_id}:{entity_id}"


def initialize_world_stocks() -> None:
    """One-time setup of global stocks from monster and node data."""
    global _INITIALIZED
    STOCKS.clear()
    now = datetime.now(timezone.utc).isoformat()
    for m in MONSTERS:
        biome_id = m.get("biome")
        if not biome_id:
            continue
        key = _stock_key("monster", biome_id, m["id"])
        rarity = m.get("rarity", "common")
        max_stock = int(m.get("max_stock", RARITY_STOCK_DEFAULTS.get(rarity, (1000, 1.0))[0]))
        regen = float(m.get("regen_per_min", RARITY_STOCK_DEFAULTS.get(rarity, (1000, 1.0))[1]))
        STOCKS[key] = {
            "current": max_stock,
            "max": max_stock,
            "regen_per_min": regen,
            "last_update": now,
        }
    for biome_id, nodes in RESOURCE_NODES.items():
        for n in nodes:
            key = _stock_key("node", biome_id, n["id"])
            rarity = n.get("rarity", "common")
            max_stock = int(n.get("max_stock", RARITY_STOCK_DEFAULTS.get(rarity, (1000, 1.0))[0]))
            regen = float(n.get("regen_per_min", RARITY_STOCK_DEFAULTS.get(rarity, (1000, 1.0))[1]))
            STOCKS[key] = {
                "current": max_stock,
                "max": max_stock,
                "regen_per_min": regen,
                "last_update": now,
            }
    _INITIALIZED = True


def _ensure_initialized() -> None:
    if not _INITIALIZED:
        initialize_world_stocks()


def _regenerate(stock: dict) -> int:
    now = datetime.now(timezone.utc)
    try:
        last = datetime.fromisoformat(stock["last_update"])
    except (ValueError, TypeError):
        last = now
    elapsed_minutes = max(0, (now - last).total_seconds() / 60.0)
    new_current = min(
        int(stock["max"]),
        int(stock["current"] + elapsed_minutes * stock.get("regen_per_min", 0)),
    )
    stock["current"] = new_current
    stock["last_update"] = now.isoformat()
    return new_current


def get_stock(kind: str, biome_id: str, entity_id: str) -> int:
    _ensure_initialized()
    key = _stock_key(kind, biome_id, entity_id)
    stock = STOCKS.get(key)
    if not stock:
        return 0
    return _regenerate(stock)


def get_stock_max(kind: str, biome_id: str, entity_id: str) -> int:
    _ensure_initialized()
    key = _stock_key(kind, biome_id, entity_id)
    stock = STOCKS.get(key)
    return int(stock["max"]) if stock else 0


def consume_stock(kind: str, biome_id: str, entity_id: str, amount: int = 1) -> bool:
    _ensure_initialized()
    key = _stock_key(kind, biome_id, entity_id)
    stock = STOCKS.get(key)
    if not stock:
        return False
    current = _regenerate(stock)
    if current < amount:
        return False
    stock["current"] = current - amount
    stock["last_update"] = datetime.now(timezone.utc).isoformat()
    return True
def monsters_for_biome(biome_id: str) -> list[dict]:
    return [m for m in MONSTERS if m.get("biome") == biome_id]


def get_resource_node(node_id: str) -> dict | None:
    for nodes in RESOURCE_NODES.values():
        for n in nodes:
            if n["id"] == node_id:
                return n
    return None


def _discoveries(character: dict) -> dict:
    return character.setdefault("biome_discoveries", {})


def _biome_discoveries(character: dict, biome_id: str) -> dict:
    return _discoveries(character).setdefault(biome_id, {"monsters": [], "nodes": []})


def _list_key(kind: str) -> str:
    return {"monster": "monsters", "node": "nodes"}.get(kind, kind)


def is_discovered(character: dict, biome_id: str, kind: str, entity_id: str) -> bool:
    return entity_id in _biome_discoveries(character, biome_id).get(_list_key(kind), [])


def discover_entity(character: dict, biome_id: str, kind: str, entity_id: str) -> bool:
    disc = _biome_discoveries(character, biome_id)
    key = _list_key(kind)
    lst = disc.setdefault(key, [])
    if entity_id not in lst:
        lst.append(entity_id)
        return True
    return False


def discovered_monsters(character: dict, biome_id: str) -> list[str]:
    return list(_biome_discoveries(character, biome_id).get("monsters", []))


def discovered_nodes(character: dict, biome_id: str) -> list[str]:
    return list(_biome_discoveries(character, biome_id).get("nodes", []))


def reveal_on_explore(character: dict, biome_id: str, outcome: int) -> list[dict]:
    """Reveal new monsters/nodes when exploring.
    Returns a list of newly discovered entities with name, id, rarity, and kind.
    Common things are easiest to discover; higher outcomes can reveal rare/legendary targets
    and may reveal multiple targets at once.
    """
    _ensure_initialized()
    discoveries: list[dict] = []

    # Collect all undiscovered entities in this biome with their rarity.
    options: list[dict] = []
    for m in monsters_for_biome(biome_id):
        if not is_discovered(character, biome_id, "monster", m["id"]):
            rarity = m.get("rarity", "common")
            options.append({
                "kind": "monster",
                "id": m["id"],
                "name": m["name"],
                "rarity": rarity,
            })
    for n in nodes_for_biome(biome_id):
        if not is_discovered(character, biome_id, "node", n["id"]):
            rarity = n.get("rarity", "common")
            options.append({
                "kind": "node",
                "id": n["id"],
                "name": n["name"],
                "rarity": rarity,
                "profession": n.get("profession", ""),
            })

    if not options:
        return discoveries

    # One discovery per Explore. Higher outcomes still increase the chance of a rarer find.
    for _ in range(1):
        if not options:
            break
        weights = [
            DISCOVERY_RARITY_WEIGHTS.get(o["rarity"], 10) * (outcome ** 2)
            for o in options
        ]
        chosen = random.choices(options, weights=weights, k=1)[0]
        if discover_entity(character, biome_id, chosen["kind"], chosen["id"]):
            discoveries.append({
                "id": chosen["id"],
                "name": chosen["name"],
                "kind": chosen["kind"],
                "rarity": chosen["rarity"],
                "profession": chosen.get("profession", ""),
            })
        # Remove from pool so the same explore cannot reveal duplicates.
        options = [o for o in options if o["id"] != chosen["id"] or o["kind"] != chosen["kind"]]

    return discoveries


def node_tool_info(node: dict) -> dict | None:
    prof = PROFESSIONS_BY_ID.get(node.get("profession"))
    tool = prof.get("tool") if prof else None
    if not tool:
        return None
    return {"id": tool["id"], "name": tool["name"], "profession": node.get("profession")}
