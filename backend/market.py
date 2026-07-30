"""Dynamic market system — daily rotation, stock limits, random price modifiers.

Each town has a base pool of items (from game_data_p2 TOWNS["market_items"]).
Every real-world day a subset is selected with random stock counts and
price modifiers (discounts / markups). The selection is seeded by
(town_id, date) so all players see the same market on the same day.

Price history is tracked per town in the DB (market_history collection)
so the frontend can show trend indicators.
"""
from __future__ import annotations

import random
from datetime import date, datetime, timedelta, timezone

from game_data import ITEMS_BY_ID
from game_data_p2 import get_town
from world_content import regional_price_multiplier
from items.generator import build_item_instance, roll_affixes
from items.base_items import BASE_ITEMS_BY_ID

# ── tuning constants ──────────────────────────────────────────────
MIN_ITEMS = 6          # minimum items shown per day
MAX_ITEMS = 12         # maximum items shown per day
MIN_EQUIPMENT = 2      # minimum weapon/armor items guaranteed per day
MIN_STOCK = 1          # min stock per item
MAX_STOCK_COMMON = 15  # max stock for common items
MAX_STOCK_RARE = 8     # max stock for rare+ items
PRICE_MOD_MIN = 0.70   # max 30% discount
PRICE_MOD_MAX = 1.50   # max 50% markup
DISCOUNT_THRESHOLD = 0.99  # below this = "discount"
HISTORY_DAYS = 7       # how many days of price history to keep


def _rarity_base_price(item: dict) -> int:
    """SRP (Suggested Retail Price) for any item based on rarity.
    If the item has an explicit 'price' field, use that instead."""
    if item.get("price"):
        return int(item["price"])
    rarity_price = {
        "common": 10, "uncommon": 40, "rare": 120,
        "epic": 350, "legendary": 900, "mythic": 2500,
        # New item system rarities
        "normal": 10, "magic": 40, "unique": 350,
        "set": 600, "legendary": 900,
    }
    _r = item.get("rarity", "common")
    # Procedural instances: scale by quality and upgrade count
    base = rarity_price.get(_r, 10)
    if item.get("instance_id"):
        _quality = item.get("quality", 0)
        _upgrades = item.get("upgrades", {}).get("count", 0)
        base = int(base * (1 + _quality / 100) * (1 + _upgrades * 0.15))
    return base


def _max_stock_for_rarity(rarity: str) -> int:
    if rarity in ("common", "uncommon"):
        return MAX_STOCK_COMMON
    return MAX_STOCK_RARE


def _seed_for(town_id: str, day_str: str) -> int:
    """Deterministic seed from town + date so all players see the same market."""
    h = 0
    for ch in f"{town_id}:{day_str}":
        h = ((h << 5) - h + ord(ch)) & 0xFFFFFFFF
    return h


# Rarity weights for market equipment (max rarity = rare)
_MARKET_RARITY_WEIGHTS = {"normal": 60, "magic": 30, "rare": 10}

# Price multiplier by rarity for procedural market items
_MARKET_RARITY_PRICE_MULT = {"normal": 1.0, "magic": 2.5, "rare": 6.0}


def _roll_market_rarity(rng: random.Random) -> str:
    """Roll rarity for market equipment, capped at rare."""
    rarities = list(_MARKET_RARITY_WEIGHTS.keys())
    weights = list(_MARKET_RARITY_WEIGHTS.values())
    return rng.choices(rarities, weights=weights, k=1)[0]


def generate_daily_market(town_id: str, day_str: str | None = None) -> list[dict]:
    """Generate the market listing for a town on a given day.

    Equipment items (weapons/armor) are generated as procedural item instances
    with random affixes, capped at 'rare' rarity. Each is unique (stock=1).
    Non-equipment items use the traditional static-item system with stock counts.

    Returns a list of dicts:
        { item_id, stock, max_stock, price_mod, base_price, final_price,
          discount_pct, regional_mult, instance? }
    """
    day = day_str or date.today().isoformat()
    town = get_town(town_id)
    if not town:
        return []

    pool = town.get("market_items", [])
    if not pool:
        return []

    rng = random.Random(_seed_for(town_id, day))
    continent = town.get("continent")

    # Separate pool into equipment and non-equipment so we can guarantee gear
    equipment = [iid for iid in pool if ITEMS_BY_ID.get(iid, {}).get("kind") in ("weapon", "armor")]
    non_equipment = [iid for iid in pool if ITEMS_BY_ID.get(iid, {}).get("kind") not in ("weapon", "armor")]

    # Guarantee at least MIN_EQUIPMENT gear items, then fill the rest randomly
    count = min(len(pool), rng.randint(MIN_ITEMS, MAX_ITEMS))
    equip_count = min(len(equipment), MIN_EQUIPMENT) if equipment else 0
    selected_equip = rng.sample(equipment, equip_count) if equipment else []
    remaining = max(0, count - equip_count)
    remaining_pool = [iid for iid in pool if iid not in selected_equip]
    selected_rest = rng.sample(remaining_pool, min(len(remaining_pool), remaining))
    selected = selected_equip + selected_rest
    rng.shuffle(selected)

    listings = []
    for item_id in selected:
        item = ITEMS_BY_ID.get(item_id)
        if not item:
            continue
        kind = item.get("kind", "")

        if kind in ("weapon", "armor"):
            # Generate a procedural item instance for equipment
            base_item = BASE_ITEMS_BY_ID.get(item_id)
            if not base_item:
                continue
            rarity = _roll_market_rarity(rng)
            prefixes, suffixes = roll_affixes(base_item, rarity, monster_level=1)
            quality = rng.randint(0, 10)
            inst = build_item_instance(base_item, prefixes, suffixes, quality, rarity)
            instance_id = inst["instance_id"]

            # Price based on rarity multiplier + quality bonus
            base_price = _rarity_base_price(item)
            rarity_mult = _MARKET_RARITY_PRICE_MULT.get(rarity, 1.0)
            base_price = int(base_price * rarity_mult * (1 + quality / 100))
            regional_mult = regional_price_multiplier(item_id, continent)
            price_mod = round(rng.uniform(PRICE_MOD_MIN, PRICE_MOD_MAX), 2)
            final_price = max(1, int(round(base_price * regional_mult * price_mod)))

            discount_pct = 0
            if price_mod < DISCOUNT_THRESHOLD:
                discount_pct = int(round((1 - price_mod) * 100))
            elif price_mod > 1.01:
                discount_pct = -int(round((price_mod - 1) * 100))

            listings.append({
                "item_id": instance_id,
                "stock": 1,
                "max_stock": 1,
                "price_mod": price_mod,
                "base_price": base_price,
                "regional_price": int(round(base_price * regional_mult)),
                "final_price": final_price,
                "discount_pct": discount_pct,
                "regional_mult": regional_mult,
                "instance": inst,
            })
        else:
            # Non-equipment: use traditional static item system
            rarity = item.get("rarity", "common")
            base_price = _rarity_base_price(item)
            regional_mult = regional_price_multiplier(item_id, continent)
            price_mod = round(rng.uniform(PRICE_MOD_MIN, PRICE_MOD_MAX), 2)
            max_stock = _max_stock_for_rarity(rarity)
            stock = rng.randint(MIN_STOCK, max_stock)

            regional_price = int(round(base_price * regional_mult))
            final_price = max(1, int(round(regional_price * price_mod)))

            discount_pct = 0
            if price_mod < DISCOUNT_THRESHOLD:
                discount_pct = int(round((1 - price_mod) * 100))
            elif price_mod > 1.01:
                discount_pct = -int(round((price_mod - 1) * 100))  # negative = markup

            listings.append({
                "item_id": item_id,
                "stock": stock,
                "max_stock": max_stock,
                "price_mod": price_mod,
                "base_price": base_price,
                "regional_price": regional_price,
                "final_price": final_price,
                "discount_pct": discount_pct,
                "regional_mult": regional_mult,
            })

    return listings


def get_or_generate_market(character: dict, town_id: str) -> dict:
    """Return today's market for the town, using character cache if fresh.

    Character stores: market_cache = { town_id, day, listings: [...] }
    If the cache is stale (different day or different town), regenerate.
    """
    today = date.today().isoformat()
    cache = character.get("market_cache") or {}

    if cache.get("town_id") == town_id and cache.get("day") == today:
        return {
            "town_id": town_id,
            "day": today,
            "listings": cache.get("listings", []),
        }

    listings = generate_daily_market(town_id, today)
    character["market_cache"] = {
        "town_id": town_id,
        "day": today,
        "listings": listings,
    }
    return {
        "town_id": town_id,
        "day": today,
        "listings": listings,
    }


def decrement_stock(character: dict, item_id: str, qty: int) -> bool:
    """Reduce stock for an item in the cached market. Returns False if insufficient."""
    cache = character.get("market_cache") or {}
    listings = cache.get("listings", [])
    for entry in listings:
        if entry["item_id"] == item_id:
            if entry["stock"] < qty:
                return False
            entry["stock"] -= qty
            return True
    return False


def get_sell_price(item: dict, town_id: str, day_str: str | None = None) -> tuple[int, float]:
    """Calculate sell price — flat 20% of SRP for all rarities.

    Returns (payout_per_unit, sell_mod).
    """
    base = _rarity_base_price(item)
    sell_mod = 0.20
    payout = max(1, int(round(base * sell_mod)))
    return payout, sell_mod


# ── Price history ─────────────────────────────────────────────────

async def record_price_history(db, town_id: str, listings: list[dict]) -> None:
    """Record today's prices into the market_history collection."""
    today = date.today().isoformat()
    prices = {}
    for entry in listings:
        prices[entry["item_id"]] = entry["final_price"]

    await db.market_history.update_one(
        {"town_id": town_id, "day": today},
        {"$set": {"town_id": town_id, "day": today, "prices": prices}},
        upsert=True,
    )


async def get_price_history(db, town_id: str, item_ids: list[str]) -> dict[str, list[dict]]:
    """Get last 7 days of price history for given items.

    Returns { item_id: [ {day, price}, ... ] }
    """
    cutoff = (date.today() - timedelta(days=HISTORY_DAYS)).isoformat()
    cursor = db.market_history.find({
        "town_id": town_id,
        "day": {"$gte": cutoff},
    }).sort("day", 1)

    history: dict[str, list[dict]] = {iid: [] for iid in item_ids}
    async for doc in cursor:
        day = doc["day"]
        prices = doc.get("prices", {})
        for iid in item_ids:
            if iid in prices:
                history[iid].append({"day": day, "price": prices[iid]})

    return history


def compute_trend(prices: list[dict]) -> str:
    """Compute a simple trend from price history. Returns 'up', 'down', or 'flat'."""
    if len(prices) < 2:
        return "flat"
    first = prices[0]["price"]
    last = prices[-1]["price"]
    if last > first * 1.05:
        return "up"
    if last < first * 0.95:
        return "down"
    return "flat"


def time_until_refresh() -> str:
    """Human-readable countdown until next daily refresh (midnight UTC)."""
    now = datetime.now(timezone.utc)
    tomorrow = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    delta = tomorrow - now
    hours = int(delta.total_seconds() // 3600)
    minutes = int((delta.total_seconds() % 3600) // 60)
    return f"{hours}h {minutes}m"
