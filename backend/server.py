"""Erchis Fantasy Dice RPG — main FastAPI server."""
from __future__ import annotations

import logging
import os
import random
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / ".env")
sys.path.insert(0, str(ROOT_DIR))

from bson import ObjectId  # noqa: E402
from fastapi import APIRouter, Depends, FastAPI, HTTPException, Request, Response  # noqa: E402
from fastapi.middleware.cors import CORSMiddleware  # noqa: E402
from motor.motor_asyncio import AsyncIOMotorClient  # noqa: E402

from auth import (  # noqa: E402
    clear_auth_cookies,
    create_access_token,
    create_refresh_token,
    get_current_user,
    hash_password,
    set_auth_cookies,
    verify_password,
)
from game_data import (  # noqa: E402
    ASSASSIN_PASSIVES,
    BARD_PASSIVES,
    BASE_ITEMS_BY_ID,
    BIOME_ACTIONS,
    CONTINENTS,
    DAILY_MISSION_POOL,
    DRUID_PASSIVES,
    EQUIP_SLOTS,
    HUNTER_PASSIVES,
    ITEMS,
    ITEMS_BY_ID,
    KNIGHT_PASSIVES,
    LANCER_PASSIVES,
    MAGE_PASSIVES,
    PALADIN_PASSIVES,
    LOGIN_REWARDS,
    MASTERIES,
    MONSTERS,
    PORTRAITS,
    RACES,
    RECIPES,
    ROGUE_INNATE_SKILLS,
    ROGUE_PASSIVES,
    ROLES,
    SKILLS,
    SKILLS_BY_ID,
    SLOT_LABELS,
    STARTER_GEAR_BY_MASTERY,
    TEACHERS,
    TEACHERS_BY_ID,
    build_item_instance,
    compute_starting_hp,
    get_mastery,
    get_race,
    get_role,
)
from game_engine import combat_turn, resolve_action, start_combat, start_craft, finish_craft, start_enchant, skin_monster, generate_telegraph, _alch_spend_cf, attempt_tame, _is_druid, _druid_summon_creature, _druid_unsummon_creature, _druid_fuse, _druid_end_fusion, _druid_get_max_summons, _get_weapon_range_for_combat  # noqa: E402
from game_data_p2 import (  # noqa: E402
    BEAST_ASPECTS,
    EVENTS,
    EVENTS_BY_ID,
    HERITAGE_RANK_1,
    MARINE_ADAPTATIONS,
    QUESTS,
    QUESTS_BY_ID,
    REGIONS,
    STATIC_ANNOUNCEMENTS,
    TOWNS,
    TOWNS_BY_ID,
    default_home_town_for_race,
    default_home_continent_for_race,
    default_home_biome_for_race,
    get_active_events,
    get_quest,
    get_town,
)
from racial import (  # noqa: E402
    current_time_of_day,
    ensure_racial_defaults,
    tick_racial_resources_on_action,
    tick_surge_on_action,
)
from origins import (  # noqa: E402
    ORIGINS,
    ROLE_AVAILABLE_MASTERIES,
    ROLE_MAIN_STATS,
    MASTERY_MAIN_STATS,
    compute_final_stats,
    get_origin,
    origins_for_mastery,
)
from world_travel import (  # noqa: E402
    TELEPORTER_FEE,
    TELEPORTER_COOLDOWN_SECS,
    teleporter_can_use,
    WAYSTONES,
    WAYSTONES_BY_ID,
    REP_LEVELS,
    REP_THRESHOLDS,
    initial_reputation_for_race,
    add_reputation,
)
from professions import (  # noqa: E402
    PROFESSIONS,
    PROFESSIONS_BY_ID,
    learn_profession,
    abandon_profession,
    gain_profession_xp,
    has_profession_rank,
    apply_exploration_progress,
    exploration_delta_from_outcome,
    EXPLORATION_THRESHOLDS,
)
from biome_encounters import (  # noqa: E402
    maybe_trigger_encounter,
    tick_encounter_cooldowns,
    resolve_encounter_action,
)
from exploration import (  # noqa: E402
    initialize_world_stocks,
    get_stock,
    get_stock_max,
    consume_stock,
    is_discovered,
    reveal_on_explore,
    discovered_monsters,
    discovered_nodes,
    monsters_for_biome,
    nodes_for_biome,
    get_resource_node,
    node_tool_info,
)
from models import (  # noqa: E402
    ActionPayload,
    CombatStartPayload,
    CombatTurnPayload,
    CombatTelegraphPayload,
    AlchemistCFPayload,
    AlchemistPreImbuePayload,
    TamePayload,
    SkinPayload,
    SummonPayload,
    UnsummonPayload,
    FusePayload,
    EndFusionPayload,
    SummonModePayload,
    ReleaseCreaturePayload,
    CraftPayload,
    CreateCharacterPayload,
    EncounterResolvePayload,
    LearnSkillPayload,
    LoginPayload,
    RegisterPayload,
)
from market import (  # noqa: E402
    get_or_generate_market,
    decrement_stock,
    get_sell_price,
    record_price_history,
    get_price_history,
    compute_trend,
    time_until_refresh,
)
from heritage_system import (  # noqa: E402
    HERITAGE_MONTHS,
    HERITAGE_MONTH_BY_CONTINENT,
    HERITAGE_MILESTONES,
    HERITAGE_MASTER_ACHIEVEMENT,
    get_active_heritage_month,
    get_heritage_continent,
    is_heritage_month_for,
    get_heritage_boss,
    get_heritage_bonuses,
    get_heritage_daily_quests,
    get_heritage_vendor_items,
    get_heritage_vendor_item,
    get_all_heritage_continents,
    get_heritage_meta_achievement,
    get_heritage_ladder_score,
)

# ---------------- setup ----------------
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("erchis")

mongo_url = os.environ["MONGO_URL"]
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ["DB_NAME"]]
initialize_world_stocks()

app = FastAPI(title="Erchis RPG")
api = APIRouter(prefix="/api")


# ---------------- helpers ----------------
def _serialize_doc(doc: dict) -> dict:
    if not doc:
        return doc
    if "_id" in doc:
        doc["id"] = str(doc["_id"])
        doc.pop("_id", None)
    return doc


async def _get_current_user(request: Request) -> dict:
    return await get_current_user(request, db)


def _migrate_legacy_tools(ch: dict) -> None:
    """One-time migration: move tools from legacy character['tools'] dict into inventory."""
    legacy = ch.get("tools", {})
    if not legacy:
        return
    inv = ch.setdefault("inventory", [])
    inv_ids = {s.get("item_id") for s in inv if s.get("quantity", 0) > 0}
    changed = False
    for tool_id, tool_data in legacy.items():
        if tool_id in inv_ids:
            continue
        inv.append({
            "item_id": tool_id,
            "quantity": 1,
            "durability": int(tool_data.get("durability", 0)),
        })
        changed = True
    if changed:
        try:
            import asyncio
            asyncio.get_event_loop().create_task(
                db.characters.update_one(
                    {"_id": ObjectId(ch["id"])},
                    {"$set": {"inventory": inv}},
                )
            )
        except Exception:
            pass


async def _get_character_or_404(user_id: str) -> dict:
    ch = await db.characters.find_one({"user_id": user_id})
    if not ch:
        raise HTTPException(status_code=404, detail="Character not found — create one first")
    ch = _serialize_doc(ch)
    ensure_racial_defaults(ch)
    # Clean up zero-quantity inventory items
    if ch.get("inventory"):
        ch["inventory"] = [x for x in ch["inventory"] if x.get("quantity", 0) > 0]
    # Migrate legacy tools dict into inventory so they show as items
    _migrate_legacy_tools(ch)
    ch.setdefault("skill_bar", [None] * 10)
    ch.setdefault("item_bar", [None] * 5)
    ch.setdefault("masteries", [])
    # Migration: ensure character's chosen mastery is in the masteries list
    _mastery = ch.get("mastery")
    if _mastery and _mastery not in ch.get("masteries", []):
        ch["masteries"].insert(0, _mastery)
    ch.setdefault("training_skill_id", None)
    ch.setdefault("training_until", None)
    # Bard: quest passives list
    ch.setdefault("quest_passives", [])
    # Rogue: innate skill equip slots (default first 5 equipped)
    if "rogue_innate_equipped" not in ch:
        ch["rogue_innate_equipped"] = [s["id"] for s in ROGUE_INNATE_SKILLS[:5]]
    # Compute effective stats = base_stats + equipment stats + enchantments
    _recompute_stats(ch)
    return ch


def _recompute_stats(ch: dict) -> None:
    """Recompute effective stats from base_stats + equipped item stats + enchantments.
    Also applies Paladin faith scaling based on current HP.
    Mutates ch['stats'] in place. Does not touch base_stats."""
    from game_data import EQUIP_SLOTS
    from game_engine import apply_enchantments_to_stats, _is_paladin, _paladin_get_faith_tier, _paladin_compute_faith_bonuses, FAITH_MAIN_STATS
    # Ensure all 12 slots exist
    equipped = ch.setdefault("equipped", {})
    # Migrate old slot names if present
    if "weapon" in equipped or "armor" in equipped or "trinket" in equipped:
        old = dict(equipped)
        equipped.clear()
        for s in EQUIP_SLOTS:
            equipped[s] = None
        if old.get("weapon"):
            equipped["right_hand"] = old["weapon"]
        if old.get("armor"):
            equipped["body"] = old["armor"]
    for s in EQUIP_SLOTS:
        equipped.setdefault(s, None)
    base = ch.get("base_stats") or ch.get("stats") or {}
    ch["base_stats"] = dict(base)
    ch["stats"] = apply_enchantments_to_stats(ch)
    # Paladin: apply faith scaling based on current HP (out-of-combat)
    if _is_paladin(ch):
        hp_ratio = ch.get("hp", 1) / max(1, ch.get("max_hp", 1))
        tier = _paladin_get_faith_tier(hp_ratio)
        bonuses = _paladin_compute_faith_bonuses(tier, ch["base_stats"], ch.get("level", 1))
        for stat in FAITH_MAIN_STATS:
            val = bonuses.get(stat, 0)
            if val:
                ch["stats"][stat] = ch["stats"].get(stat, 0) + val
        ch["paladin_faith_tier"] = tier
        ch["paladin_faith_bonuses"] = {k: v for k, v in bonuses.items() if k != "heal_amp"}
    else:
        ch.pop("paladin_faith_tier", None)
        ch.pop("paladin_faith_bonuses", None)


def _today_str() -> str:
    return date.today().isoformat()


def _xp_for_next(level: int) -> int:
    return 100 + (level - 1) * 40


def _apply_rewards_to_character(character: dict, rewards: dict, reduce: bool = True) -> None:
    mult = 0.5 if reduce else 1.0
    character["gold"] = character.get("gold", 0) + int(rewards.get("gold", 0) * mult)
    character["xp"] = character.get("xp", 0) + int(rewards.get("xp", 0) * mult)
    # Also add items to inventory (supports both static items and procedural instances)
    for it in rewards.get("items", []) or []:
        if isinstance(it, (list, tuple)):
            item_id, qty = it[0], it[1]
        else:
            item_id, qty = it, 1
        _add_item_to_inventory(character, item_id, int(qty) if not isinstance(item_id, dict) else 1)


# ---------------- exploration gating ----------------
# Action thresholds (percent of biome exploration required)
ACTION_EXPLORE_THRESHOLD = 0
ACTION_GATHER_THRESHOLD = 0
ACTION_HUNT_THRESHOLD = 0
ACTION_FISH_THRESHOLD = 0
ACTION_LOOT_THRESHOLD = 50
NEXT_BIOME_THRESHOLD = 50


def _biome_index(continent: dict, biome_id: str) -> int:
    return next((i for i, b in enumerate(continent.get("biomes", [])) if b["id"] == biome_id), -1)


def _biome_exploration_pct(character: dict, biome_id: str) -> int:
    return int(character.get("exploration_progress", {}).get(biome_id, 0))


def _is_action_unlocked(character: dict, biome_id: str, action_id: str) -> tuple[bool, int]:
    """Return (unlocked, required_pct) for an action in a biome."""
    pct = _biome_exploration_pct(character, biome_id)
    thresholds = {
        "explore": ACTION_EXPLORE_THRESHOLD,
        "gather": ACTION_GATHER_THRESHOLD,
        "fish": ACTION_FISH_THRESHOLD,
        "hunt": ACTION_HUNT_THRESHOLD,
        "loot_ruins": ACTION_LOOT_THRESHOLD,
    }
    req = thresholds.get(action_id, ACTION_EXPLORE_THRESHOLD)
    return pct >= req, req


def _is_biome_unlocked(character: dict, continent: dict, biome_id: str) -> tuple[bool, int, str | None]:
    """Return (unlocked, required_pct, prerequisite_biome_id) for a biome on a continent."""
    idx = _biome_index(continent, biome_id)
    if idx <= 0:
        return True, 0, None
    prev = continent["biomes"][idx - 1]
    prev_pct = _biome_exploration_pct(character, prev["id"])
    return prev_pct >= NEXT_BIOME_THRESHOLD, NEXT_BIOME_THRESHOLD, prev["id"]
def _level_up_if_needed(character: dict, rewards: dict) -> None:
    base = character.setdefault("base_stats", dict(character.get("stats", {})))
    while character["xp"] >= _xp_for_next(character["level"]):
        character["xp"] -= _xp_for_next(character["level"])
        character["level"] += 1
        stat_keys = ["vitality", "cognition", "essence", "durability"]
        pick = random.choice(stat_keys)
        base[pick] = base.get(pick, 0) + 1
        character["max_hp"] = compute_starting_hp(base) + (character["level"] - 1) * 4
    character["base_stats"] = base
    _recompute_stats(character)


def _apply_status_to_character(character: dict, new_status: dict) -> None:
    """Add a status, or refresh duration if it already exists (no duplicates).
    Negative statuses have their duration reduced by the character's Durability."""
    # Apply Durability-based duration reduction for debuffs
    if new_status.get("kind") == "debuff":
        from game_data import compute_status_duration_mult
        dur_mult = compute_status_duration_mult(character)
        new_status = dict(new_status)
        new_status["duration"] = max(1, int(int(new_status.get("duration", 2)) * dur_mult))
    statuses = character.setdefault("statuses", [])
    for s in statuses:
        if s.get("id") == new_status.get("id"):
            # refresh duration to the greater of the two, keep magnitude
            s["duration"] = max(int(s.get("duration", 0)), int(new_status.get("duration", 0)))
            return
    statuses.append(new_status)


def _tick_character_statuses(character: dict) -> None:
    """Decrement each status duration by 1 and drop any that have expired.
    Called at the end of every action so debuffs like Weary / Bleeding / Poisoned
    eventually clear themselves, rather than sticking until an Inn visit."""
    kept = []
    for s in character.get("statuses", []):
        dur = int(s.get("duration", 0)) - 1
        if dur > 0:
            s["duration"] = dur
            kept.append(s)
    character["statuses"] = kept


def _add_item_to_inventory(character: dict, item_id, qty: int) -> None:
    if not item_id:
        return
    # Handle procedural item instances (dicts with instance_id)
    if isinstance(item_id, dict):
        inst = item_id
        instances = character.setdefault("item_instances", [])
        instances.append(inst)
        # Use instance_id as the inventory reference
        inv_id = inst.get("instance_id", inst.get("id", ""))
        if inv_id:
            inv = character.setdefault("inventory", [])
            inv.append({"item_id": inv_id, "quantity": 1})
        return
    # Normal static item
    inv = character.setdefault("inventory", [])
    for i in inv:
        if i.get("item_id") == item_id:
            i["quantity"] = i.get("quantity", 0) + qty
            return
    inv.append({"item_id": item_id, "quantity": qty})


def _remove_item_from_inventory(character: dict, item_id: str, qty: int) -> bool:
    for i in character.get("inventory", []):
        if i.get("item_id") == item_id:
            if i.get("quantity", 0) < qty:
                return False
            i["quantity"] -= qty
            if i["quantity"] <= 0:
                character["inventory"] = [x for x in character["inventory"] if x.get("item_id") != item_id]
            return True
    return False


async def _push_world_event(character_name: str, text: str, kind: str = "general") -> None:
    await db.world_events.insert_one({
        "character_name": character_name,
        "text": text,
        "kind": kind,
        "created_at": datetime.now(timezone.utc).isoformat(),
    })


def _refresh_dailies_if_needed(character: dict) -> None:
    today = _today_str()
    if character.get("last_daily_refresh") == today:
        return
    picks = random.sample(DAILY_MISSION_POOL, 3)
    character["daily_missions"] = [
        {**p, "progress": 0, "complete": False, "claimed": False} for p in picks
    ]
    character["last_daily_refresh"] = today
    character["_biomes_today"] = []


def _touch_login_streak(character: dict) -> dict | None:
    today = _today_str()
    last = character.get("last_login_date")
    if last == today:
        return None
    if last:
        yesterday = date.fromisoformat(last)
        delta = (date.today() - yesterday).days
        if delta == 1:
            character["login_streak"] = min(7, character.get("login_streak", 0) + 1)
        else:
            character["login_streak"] = 1
    else:
        character["login_streak"] = 1
    character["last_login_date"] = today
    streak = character["login_streak"]
    payout = next((r for r in LOGIN_REWARDS if r["day"] == streak), None)
    if payout:
        rewards = {"gold": payout["reward"].get("gold", 0), "items": []}
        if "item" in payout["reward"]:
            it_id, q = payout["reward"]["item"]
            rewards["items"].append((it_id, q))
        _apply_rewards_to_character(character, rewards)
        return {"day": streak, "reward": payout["reward"]}
    return None


def _update_daily_mission_progress(character: dict, event: dict) -> None:
    missions = character.get("daily_missions", [])
    biomes_today = character.setdefault("_biomes_today", [])
    if event.get("kind") == "explore":
        b = event.get("biome")
        if b and b not in biomes_today:
            biomes_today.append(b)
    for m in missions:
        if m.get("complete") or m.get("claimed"):
            continue
        tgt = m.get("target", {})
        if tgt.get("kind") == "kill" and event.get("kind") == "kill" and tgt.get("id") == event.get("id"):
            m["progress"] = m.get("progress", 0) + int(event.get("count", 1))
        elif tgt.get("kind") == "gather" and event.get("kind") == "gather" and tgt.get("id") == event.get("id"):
            m["progress"] = m.get("progress", 0) + int(event.get("count", 1))
        elif tgt.get("kind") == "action" and event.get("kind") == "action" and tgt.get("id") == event.get("id"):
            m["progress"] = m.get("progress", 0) + int(event.get("count", 1))
        elif tgt.get("kind") == "craft" and event.get("kind") == "craft":
            m["progress"] = m.get("progress", 0) + int(event.get("count", 1))
        elif tgt.get("kind") == "explore_variety":
            m["progress"] = len(biomes_today)
        if m.get("progress", 0) >= tgt.get("count", 1):
            m["complete"] = True


# ---------------- AUTH ROUTES ----------------
@api.post("/auth/register")
async def register(payload: RegisterPayload, response: Response):
    email = payload.email.strip().lower()
    if not email or not payload.password or len(payload.password) < 6:
        raise HTTPException(status_code=400, detail="Email and password (6+ chars) required")
    existing = await db.users.find_one({"email": email})
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered")
    doc = {
        "email": email,
        "password_hash": hash_password(payload.password),
        "display_name": payload.display_name.strip() or email.split("@")[0],
        "role": "player",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    result = await db.users.insert_one(doc)
    uid = str(result.inserted_id)
    access = create_access_token(uid, email)
    refresh = create_refresh_token(uid)
    set_auth_cookies(response, access, refresh)
    return {
        "id": uid, "email": email, "display_name": doc["display_name"],
        "role": "player", "created_at": doc["created_at"], "has_character": False,
    }


@api.post("/auth/login")
async def login(payload: LoginPayload, response: Response):
    email = payload.email.strip().lower()
    user = await db.users.find_one({"email": email})
    if not user or not verify_password(payload.password, user.get("password_hash", "")):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    uid = str(user["_id"])
    access = create_access_token(uid, email)
    refresh = create_refresh_token(uid)
    set_auth_cookies(response, access, refresh)
    ch = await db.characters.find_one({"user_id": uid})
    return {
        "id": uid, "email": email, "display_name": user["display_name"],
        "role": user.get("role", "player"), "created_at": user.get("created_at"),
        "has_character": bool(ch),
    }


@api.post("/auth/logout")
async def logout(response: Response, user: dict = Depends(_get_current_user)):
    clear_auth_cookies(response)
    return {"ok": True}


@api.get("/auth/me")
async def me(user: dict = Depends(_get_current_user)):
    ch = await db.characters.find_one({"user_id": user["_id"]})
    return {
        "id": user["_id"], "email": user["email"], "display_name": user.get("display_name", ""),
        "role": user.get("role", "player"), "created_at": user.get("created_at"),
        "has_character": bool(ch),
    }


# ---------------- STATIC GAME DATA ----------------
@api.get("/game/data/races")
async def get_races(user: dict = Depends(_get_current_user)):
    return {"races": RACES}


@api.get("/game/data/roles")
async def get_roles_route(user: dict = Depends(_get_current_user)):
    result = []
    for r in ROLES:
        rr = dict(r)
        rr["main_stats"] = ROLE_MAIN_STATS.get(r["id"], {})
        rr["available_masteries"] = ROLE_AVAILABLE_MASTERIES.get(r["id"], [])
        result.append(rr)
    return {"roles": result}


@api.get("/game/data/masteries")
async def get_masteries_route(user: dict = Depends(_get_current_user)):
    # Attach main_stats and available_to for each mastery
    result = []
    for m in MASTERIES:
        mm = dict(m)
        mm["main_stats"] = MASTERY_MAIN_STATS.get(m["id"], {})
        mm["available_to"] = [r for r, masteries in ROLE_AVAILABLE_MASTERIES.items() if m["id"] in masteries]
        result.append(mm)
    return {"masteries": result}


@api.get("/game/data/origins")
async def get_origins(user: dict = Depends(_get_current_user)):
    return {"origins": ORIGINS}


@api.get("/game/data/origins/{mastery_id}")
async def get_origins_by_mastery(mastery_id: str, user: dict = Depends(_get_current_user)):
    return {"origins": origins_for_mastery(mastery_id)}





@api.get("/game/data/portraits")
async def get_portraits(user: dict = Depends(_get_current_user)):
    return {"portraits": PORTRAITS}


@api.get("/game/data/continents")
async def get_continents(user: dict = Depends(_get_current_user)):
    return {"continents": CONTINENTS}


@api.get("/game/data/biome/{biome_id}/actions")
async def biome_actions(biome_id: str, user: dict = Depends(_get_current_user)):
    """Return actions for a biome, enriched with discovery, stocks, and cooldowns."""
    ch = await _get_character_or_404(user["_id"])
    cont = next((c for c in CONTINENTS if any(b["id"] == biome_id for b in c.get("biomes", []))), None)
    biome_unlocked, biome_req, _ = _is_biome_unlocked(ch, cont, biome_id) if cont else (True, 0, None)
    disc_mons = discovered_monsters(ch, biome_id)
    disc_nodes = discovered_nodes(ch, biome_id)
    profs = {p.get("id"): p.get("rank", "novice") for p in ch.get("professions", [])}
    from regional_resources import RANK_ORDER
    base_actions = {a["id"]: a for a in BIOME_ACTIONS.get(biome_id, [])}
    action_order = ["explore"]
    if monsters_for_biome(biome_id):
        action_order.append("hunt")
    biome_nodes = nodes_for_biome(biome_id)
    if any(n["profession"] != "fishing" for n in biome_nodes):
        action_order.append("gather")
    if any(n["profession"] == "fishing" for n in biome_nodes):
        action_order.append("fish")
    if "loot_ruins" in base_actions:
        action_order.append("loot_ruins")
    default_names = {
        "explore": "Explore",
        "hunt": "Hunt",
        "gather": "Gather",
        "fish": "Fish",
        "loot_ruins": "Loot Ruins",
    }
    actions = []
    for aid in action_order:
        a = base_actions.get(aid) or {"id": aid, "name": default_names.get(aid, aid.title()), "targets": []}
        entry = dict(a)
        action_unlocked, action_req = _is_action_unlocked(ch, biome_id, a["id"])
        entry["unlocked"] = biome_unlocked and action_unlocked
        entry["required_pct"] = 0 if (biome_unlocked and action_unlocked) else (biome_req if not biome_unlocked else action_req)
        if a["id"] == "hunt":
            targets = []
            from regional_resources import get_profession_tool as _gpt
            hunt_tool = _gpt(ch, "hunting")
            hunt_tool_ok = hunt_tool and int(hunt_tool.get("durability", 0)) > 0
            for m in monsters_for_biome(biome_id):
                if m["id"] not in disc_mons:
                    continue
                stock = get_stock("monster", biome_id, m["id"])
                targets.append({
                    "id": m["id"],
                    "name": m["name"],
                    "rarity": m.get("rarity", "common"),
                    "power": m.get("power", 5),
                    "stock": stock,
                    "max_stock": get_stock_max("monster", biome_id, m["id"]),
                })
            entry["targets"] = targets
            entry["discovered_count"] = len(targets)
            entry["total_count"] = len(monsters_for_biome(biome_id))
            entry["tool_required"] = {"id": "hunting_bow", "name": "Hunter's Kit", "profession": "hunting"}
            entry["tool_ok"] = hunt_tool_ok
        elif a["id"] in ("gather", "fish"):
            nodes = []
            for n in nodes_for_biome(biome_id):
                if a["id"] == "fish" and n["profession"] != "fishing":
                    continue
                if a["id"] == "gather" and n["profession"] == "fishing":
                    continue
                if n["id"] not in disc_nodes:
                    continue
                has = profs.get(n["profession"])
                rank_ok = has and RANK_ORDER.get(has, 0) >= RANK_ORDER.get(n["min_rank"], 0)
                stock = get_stock("node", biome_id, n["id"])
                tool = node_tool_info(n)
                tool_ok = False
                if tool:
                    from regional_resources import get_profession_tool as _gpt
                    ct = _gpt(ch, n["profession"])
                    tool_ok = ct and int(ct.get("durability", 0)) > 0
                nodes.append({
                    "id": n["id"],
                    "name": n["name"],
                    "item_id": n["item_id"],
                    "profession": n["profession"],
                    "min_rank": n["min_rank"],
                    "rarity": n["rarity"],
                    "rank_ok": rank_ok,
                    "has_profession": bool(has),
                    "cooldown_secs": seconds_until_node_ready(ch, n["id"]),
                    "stock_current": stock,
                    "stock_max": get_stock_max("node", biome_id, n["id"]),
                    "required_tool": tool,
                    "tool_ok": tool_ok,
                })
            entry["resource_nodes"] = nodes
            entry["discovered_count"] = len(nodes)
            entry["total_count"] = len(nodes_for_biome(biome_id))
        actions.append(entry)
    return {"biome_id": biome_id, "actions": actions, "biome_unlocked": biome_unlocked, "biome_required_pct": biome_req}


@api.get("/game/data/items")
async def get_items(user: dict = Depends(_get_current_user)):
    return {"items": ITEMS}


@api.get("/game/data/runes")
async def get_runes(user: dict = Depends(_get_current_user)):
    from items.runes import RUNES
    return {"runes": RUNES}


@api.get("/game/data/skills")
async def get_skills_route(user: dict = Depends(_get_current_user)):
    return {"skills": SKILLS}


def _recipe_available_here(ch: dict, recipe: dict) -> bool:
    """A recipe can be crafted at a town whose trade NPC teaches the recipe's profession.
    Old recipes with explicit continent_id/town_id still respect those constraints."""
    current_town = ch.get("current_town")
    if not current_town:
        return False
    town = TOWNS_BY_ID.get(current_town)
    trade_specialties = set(town.get("trade_npc", {}).get("specialties", [])) if town else set()
    prof_id = recipe.get("profession_id")
    if prof_id and prof_id not in trade_specialties:
        return False
    # Old recipes with explicit location constraints still enforce them
    c_id = recipe.get("continent_id")
    t_id = recipe.get("town_id")
    if c_id and c_id != ch.get("current_continent"):
        return False
    if t_id and t_id != current_town:
        return False
    # Recipes with no profession (intro recipes) require any town with a trade NPC
    if not prof_id and not town:
        return False
    return True


@api.get("/game/data/recipes")
async def get_recipes(
    continent_id: str | None = None,
    town_id: str | None = None,
    user: dict = Depends(_get_current_user),
):
    ch = await _get_character_or_404(user["_id"])
    # Default to character's current location if not provided
    continent = continent_id or ch.get("current_continent")
    town = town_id or ch.get("current_town")
    # Only return recipes for professions the character has learned + intro recipes
    known_prof_ids = {p["id"] for p in ch.get("professions", [])}
    out = []
    for r in RECIPES:
        prof_id = r.get("profession_id")
        # Skip recipes for professions the character hasn't learned
        if prof_id and prof_id not in known_prof_ids:
            continue
        min_rank = r.get("profession_min_rank")
        has = has_profession_rank(ch, prof_id, min_rank) if prof_id else True
        prof_name = PROFESSIONS_BY_ID.get(prof_id, {}).get("name") if prof_id else None
        available = _recipe_available_here(ch, r)
        out.append({
            **r,
            "profession_name": prof_name,
            "rank_ok": has,
            "has_profession": prof_id in known_prof_ids if prof_id else True,
            "available_here": available,
        })
    return {"recipes": out, "queue": ch.get("crafting_queue", [])}


@api.get("/game/data/teachers")
async def get_teachers(
    town_id: str | None = None,
    continent_id: str | None = None,
    user: dict = Depends(_get_current_user),
):
    """Return skill teachers, optionally filtered by town or continent."""
    teachers = TEACHERS
    if town_id:
        teachers = [t for t in teachers if t.get("town_id") == town_id]
    if continent_id:
        teachers = [t for t in teachers if t.get("continent_id") == continent_id]
    return {"teachers": teachers}


@api.get("/game/data/monsters")
async def get_monsters(user: dict = Depends(_get_current_user)):
    return {"monsters": MONSTERS}


@api.get("/game/data/rogue-innates")
async def get_rogue_innate_data(user: dict = Depends(_get_current_user)):
    return {"innate_skills": ROGUE_INNATE_SKILLS, "passives": ROGUE_PASSIVES}


@api.get("/game/data/mastery-passives")
async def get_mastery_passives_data(user: dict = Depends(_get_current_user)):
    return {
        "rogue": ROGUE_PASSIVES,
        "assassin": ASSASSIN_PASSIVES,
        "bard": BARD_PASSIVES,
        "druid": DRUID_PASSIVES,
        "hunter": HUNTER_PASSIVES,
        "knight": KNIGHT_PASSIVES,
        "lancer": LANCER_PASSIVES,
        "mage": MAGE_PASSIVES,
        "paladin": PALADIN_PASSIVES,
    }


# ---------------- CHARACTER ----------------
@api.post("/game/character")
async def create_character(payload: CreateCharacterPayload, user: dict = Depends(_get_current_user)):
    existing = await db.characters.find_one({"user_id": user["_id"]})
    if existing:
        raise HTTPException(status_code=409, detail="Character already exists")
    race = get_race(payload.race)
    role = get_role(payload.role)
    mastery = get_mastery(payload.mastery)
    if not race or not role or not mastery:
        raise HTTPException(status_code=400, detail="Invalid race/role/mastery")
    if payload.mastery not in ROLE_AVAILABLE_MASTERIES.get(payload.role, []):
        raise HTTPException(status_code=400, detail=f"Mastery '{payload.mastery}' not available to Role '{payload.role}'")
    origin = get_origin(payload.origin)
    if not origin:
        raise HTTPException(status_code=400, detail="Invalid origin")
    if origin["mastery"] != payload.mastery:
        raise HTTPException(status_code=400, detail=f"Origin '{payload.origin}' does not belong to Mastery '{payload.mastery}'")
    if payload.race == "human" and not payload.oath:
        raise HTTPException(status_code=400, detail="Humans must swear a Sacred Oath")
    if payload.race == "half_elf" and not payload.heritage:
        raise HTTPException(status_code=400, detail="Half-Elves must choose a heritage")

    # Layered stat computation: Race + Role + Mastery + Origin
    layered = compute_final_stats(race["starting_stats"], payload.role, payload.mastery, payload.origin)
    stats = layered["stats"]

    # Racial gift validation and application
    gifts = race.get("gifts") or []
    gift_ids = [g["id"] for g in gifts]
    if payload.racial_gift not in gift_ids:
        raise HTTPException(status_code=400, detail="Choose a valid racial gift")
    selected_gift = next(g for g in gifts if g["id"] == payload.racial_gift)
    for k, v in (selected_gift.get("bonus") or {}).items():
        stats[k] = stats.get(k, 0) + v
    # Re-apply min-1 rule after gift bonus
    for k in ("vitality", "cognition", "essence", "durability", "might", "grace", "insight"):
        if stats.get(k, 0) < 1:
            stats[k] = 1

    # Race-specific creation validation
    beast_aspect = None
    marine_adaptation = None
    if payload.race == "wildblood":
        beast_aspect = payload.beast_aspect or "predator"
        if beast_aspect not in [b["id"] for b in BEAST_ASPECTS]:
            raise HTTPException(status_code=400, detail="Invalid beast aspect")
    elif payload.beast_aspect:
        raise HTTPException(status_code=400, detail="Only Wildbloods may choose a Beast Aspect")
    if payload.race == "hyliondrian" and payload.marine_adaptation:
        if payload.marine_adaptation not in [m["id"] for m in MARINE_ADAPTATIONS]:
            raise HTTPException(status_code=400, detail="Invalid marine adaptation")
        marine_adaptation = payload.marine_adaptation
    elif payload.race != "hyliondrian" and payload.marine_adaptation:
        raise HTTPException(status_code=400, detail="Only Hyliondrians may choose a Marine Adaptation")

    max_hp = compute_starting_hp(stats)
    starting_skills = list(mastery.get("starting_skills", []))
    starting_skills += list(role.get("starting_skills", []))
    skills = [{"skill_id": sid, "cooldown_remaining": 0} for sid in starting_skills]

    # Generate proper item instances for starting equipment (mastery-based)
    _gear_def = STARTER_GEAR_BY_MASTERY.get(payload.mastery, {})
    _starter_instances = []
    _starter_inv = []
    _starter_equipped = {
        "head": None, "body": None,
        "left_hand": None, "right_hand": None,
        "legs": None, "feet": None,
        "earring_l": None, "earring_r": None,
        "ring_l": None, "ring_r": None,
        "neck": None, "back": None,
    }
    # Build list of (base_item_id, equip_slot) pairs from mastery gear definition
    _gear_pairs = []
    _weapon_id = _gear_def.get("weapon")
    if _weapon_id:
        _gear_pairs.append((_weapon_id, "right_hand"))
    _shield_id = _gear_def.get("shield")
    if _shield_id:
        _gear_pairs.append((_shield_id, "left_hand"))
    for _armor_id in _gear_def.get("armor", []):
        _armor_base = BASE_ITEMS_BY_ID.get(_armor_id)
        _slot = _armor_base.get("slot") if _armor_base else None
        if _slot:
            _gear_pairs.append((_armor_id, _slot))
    for _bid, _slot in _gear_pairs:
        _base = BASE_ITEMS_BY_ID.get(_bid)
        if not _base:
            continue
        _inst = build_item_instance(_base, [], [], quality=0, rarity="normal")
        _starter_instances.append(_inst)
        _iid = _inst["instance_id"]
        _starter_inv.append({"item_id": _iid, "quantity": 1})
        if _slot:
            _starter_equipped[_slot] = _iid
    # Consumables stay as static items
    _starter_inv.append({"item_id": "minor_healing_potion", "quantity": 2})
    _starter_inv.append({"item_id": "wild_herb", "quantity": 3})

    # Compute weapon_range from starter gear
    _starter_char = {"equipped": _starter_equipped, "item_instances": _starter_instances}
    _starter_weapon_range = _get_weapon_range_for_combat(_starter_char)

    doc = {
        "user_id": user["_id"],
        "name": payload.name.strip(),
        "race": payload.race,
        "role": payload.role,
        "mastery": payload.mastery,
        "origin": payload.origin,
        "portrait_id": payload.portrait_id,
        "oath": payload.oath,
        "heritage": payload.heritage,
        "racial_gift": payload.racial_gift,
        "level": 1,
        "xp": 0,
        "gold": 75,
        "hp": max_hp,
        "max_hp": max_hp,
        "base_stats": dict(stats),
        "stats": dict(stats),
        "item_instances": _starter_instances,
        "inventory": _starter_inv,
        "equipped": _starter_equipped,
        "weapon_range": _starter_weapon_range,
        "skills": skills,
        "skill_bar": [None] * 10,
        "item_bar": [None] * 5,
        "masteries": [payload.mastery],
        "training_skill_id": None,
        "training_until": None,
        "rogue_innate_equipped": [s["id"] for s in ROGUE_INNATE_SKILLS[:5]] if payload.mastery == "rogue" else [],
        "quest_passives": [],
        "statuses": [],
        "reputation": initial_reputation_for_race(
            payload.race,
            default_home_continent_for_race(payload.race),
            [c["id"] for c in CONTINENTS if not c.get("locked")],
        ),
        "tutorial_step": 0,
        "tutorial_complete": False,
        "current_continent": default_home_continent_for_race(payload.race),
        "current_biome": default_home_biome_for_race(payload.race),
        "login_streak": 0,
        "last_login_date": None,
        "last_daily_refresh": None,
        "daily_missions": [],
        "_biomes_today": [],
        # racial resources
        "exhaustion": 0,
        "resolve": 100,
        "heritage_rank": 1,
        "heritage_surge_active": 0,
        "heritage_surge_last_used": None,
        "oath_progress": 0,
        "celestial_charge": 0,
        "stoneguard": 0,
        "harmony": 0,
        "defiance": 0,
        "inner_blood": 0,
        "tide": 0,
        "verdant_essence": 0,
        "beast_aspect": beast_aspect,
        "marine_adaptation": marine_adaptation,
        "zone_active": False,
        # towns / guild / quests
        "home_town": default_home_town_for_race(payload.race),
        "current_town": default_home_town_for_race(payload.race),
        "visited_towns": [default_home_town_for_race(payload.race)],
        "known_waystones": [],
        "active_waystones": [],
        "teleporter_last_used": None,
        "professions": [],                 # Phase D — up to 3 slots
        "abandoned_professions": {},       # keeps 25% xp for relearn
        "exploration_progress": {},        # Phase C — per-biome %
        "npc_relationships": initial_npc_relationships(),  # Phase F — story quests
        "active_npc_quests": [],
        "completed_npc_quests": [],
        "npc_quest_progress": {},
        "heritage_surge_active": 0,
        "heritage_surge_last_used": None,
        "guild_id": None,
        "guild_rank": None,
        "active_quests": [],
        "completed_quests": [],
        "kills": 0,
        "crafts": 0,
        "deaths": 0,
        "last_death": None,
        "last_sanctuary_town": default_home_town_for_race(payload.race),
        "last_hp_regen_at": datetime.now(timezone.utc).isoformat(),
        "last_screen": None,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    result = await db.characters.insert_one(doc)
    doc["_id"] = str(result.inserted_id)
    await _push_world_event(doc["name"],
                            f"{doc['name']} the {mastery['name']} enters Erchis for the first time.",
                            kind="general")
    return _serialize_doc(doc)


@api.get("/game/character")
async def get_character(user: dict = Depends(_get_current_user)):
    ch = await _get_character_or_404(user["_id"])
    reward = _touch_login_streak(ch)
    _refresh_dailies_if_needed(ch)

    # Real-time racial HP regen — applies hp_regen_per_min × minutes elapsed since last check
    race = get_race(ch.get("race", ""))
    regen_per_min = race.get("hp_regen_per_min", 0) if race else 0
    regen_applied = 0
    now = datetime.now(timezone.utc)
    if regen_per_min > 0 and ch.get("hp", 0) < ch.get("max_hp", 1):
        last_regen = ch.get("last_hp_regen_at")
        if last_regen:
            if isinstance(last_regen, str):
                try:
                    last_regen = datetime.fromisoformat(last_regen)
                except Exception:
                    last_regen = None
            if last_regen:
                if last_regen.tzinfo is None:
                    last_regen = last_regen.replace(tzinfo=timezone.utc)
                elapsed_min = (now - last_regen).total_seconds() / 60.0
                if elapsed_min >= 1.0:
                    regen_applied = int(elapsed_min * regen_per_min)
                    if regen_applied > 0:
                        ch["hp"] = min(ch["max_hp"], ch["hp"] + regen_applied)
    ch["last_hp_regen_at"] = now.isoformat()
    ch["hp_regen_per_min"] = regen_per_min

    # Compute aggregated item bonus effects, legendary powers, and set bonuses for frontend display
    from game_engine import _aggregate_item_bonus_effects, _aggregate_legendary_powers, _check_set_bonuses, _LEGENDARY_POWERS, _SET_BONUSES
    ch["item_bonus_effects_summary"] = _aggregate_item_bonus_effects(ch)
    ch["legendary_powers_summary"] = [
        {"id": lp_id, "name": _LEGENDARY_POWERS.get(lp_id, {}).get("name", lp_id),
         "desc": _LEGENDARY_POWERS.get(lp_id, {}).get("desc", "")}
        for lp_id in _aggregate_legendary_powers(ch)
    ]
    _sb = _check_set_bonuses(ch)
    ch["set_bonuses_summary"] = [
        {"set_id": sid, "count": count,
         "set_name": _SET_BONUSES.get(sid, {}).get("name", sid)}
        for sid, count in _sb.items()
    ]
    await db.characters.update_one({"_id": ObjectId(ch["id"])}, {"$set": {
        "login_streak": ch["login_streak"],
        "last_login_date": ch["last_login_date"],
        "last_daily_refresh": ch["last_daily_refresh"],
        "daily_missions": ch.get("daily_missions", []),
        "_biomes_today": ch.get("_biomes_today", []),
        "gold": ch["gold"],
        "xp": ch["xp"],
        "level": ch["level"],
        "base_stats": ch.get("base_stats", ch["stats"]),
        "stats": ch["stats"],
        "max_hp": ch["max_hp"],
        "hp": ch["hp"],
        "last_hp_regen_at": ch["last_hp_regen_at"],
        "inventory": ch["inventory"],
    }})
    return {"character": ch, "login_reward": reward, "hp_regen_applied": regen_applied}


@api.delete("/game/character")
async def delete_character(response: Response, user: dict = Depends(_get_current_user)):
    ch = await db.characters.find_one({"user_id": user["_id"]})
    if not ch:
        raise HTTPException(status_code=404, detail="No character found.")
    await db.characters.delete_one({"_id": ch["_id"]})
    await db.combats.delete_many({"user_id": user["_id"]})
    clear_auth_cookies(response)
    return {"ok": True, "message": "Character deleted. You must log in again."}


@api.post("/game/character/tutorial")
async def update_tutorial(request: Request, user: dict = Depends(_get_current_user)):
    body = await request.json()
    step = int(body.get("step", 0))
    complete = bool(body.get("complete", False))
    ch = await _get_character_or_404(user["_id"])
    await db.characters.update_one(
        {"_id": ObjectId(ch["id"])},
        {"$set": {"tutorial_step": step, "tutorial_complete": complete}}
    )
    return {"ok": True, "step": step, "complete": complete}


@api.post("/game/character/travel")
async def travel(request: Request, user: dict = Depends(_get_current_user)):
    body = await request.json()
    continent = body.get("continent")
    biome = body.get("biome")
    ch = await _get_character_or_404(user["_id"])
    cont = next((c for c in CONTINENTS if c["id"] == continent), None)
    if not cont:
        raise HTTPException(status_code=400, detail="Unknown continent")
    if ch["level"] < cont.get("level_req", 1):
        raise HTTPException(status_code=403, detail=f"Requires level {cont['level_req']}")
    changing_continent = continent != ch.get("current_continent")
    # Heritage month bonus: free travel to/from heritage continent
    _heritage_free = False
    if changing_continent:
        _from_hc = is_heritage_month_for(ch.get("current_continent", ""))
        _to_hc = is_heritage_month_for(continent)
        if _from_hc or _to_hc:
            _hb = get_heritage_bonuses(continent if _to_hc else ch.get("current_continent", ""))
            if _hb and _hb.get("free_travel"):
                _heritage_free = True
    # Inter-continental travel costs gold (road/walk version of the teleporter)
    if changing_continent and not _heritage_free:
        if ch["gold"] < TELEPORTER_FEE:
            raise HTTPException(status_code=400, detail=f"Travel fee is {TELEPORTER_FEE}g.")
        ch["gold"] -= TELEPORTER_FEE
    valid_biomes = [b["id"] for b in cont.get("biomes", [])]
    if valid_biomes and biome not in valid_biomes:
        biome = valid_biomes[0]
    ch["current_continent"] = continent
    ch["current_biome"] = biome or ch["current_biome"]
    _update_daily_mission_progress(ch, {"kind": "explore", "biome": ch["current_biome"]})
    update_fields = {
        "current_continent": ch["current_continent"],
        "current_biome": ch["current_biome"],
        "daily_missions": ch.get("daily_missions", []),
        "_biomes_today": ch.get("_biomes_today", []),
    }
    if changing_continent and not _heritage_free:
        update_fields["gold"] = ch["gold"]
    await db.characters.update_one({"_id": ObjectId(ch["id"])}, {"$set": update_fields})
    return {"character": ch, "fee": 0 if _heritage_free else (TELEPORTER_FEE if changing_continent else 0)}


# ---------------- ACTIONS ----------------
@api.post("/game/action")
async def do_action(payload: ActionPayload, user: dict = Depends(_get_current_user)):
    ch = await _get_character_or_404(user["_id"])
    cont = next((c for c in CONTINENTS if c["id"] == ch.get("current_continent")), None)
    if cont:
        biome_unlocked, biome_req, _ = _is_biome_unlocked(ch, cont, payload.biome_id)
        if not biome_unlocked:
            raise HTTPException(status_code=403, detail=f"This region is still unknown. Explore {biome_req}% of the previous region to unlock it.")
        action_unlocked, action_req = _is_action_unlocked(ch, payload.biome_id, payload.action_id)
        if not action_unlocked:
            raise HTTPException(status_code=403, detail=f"You need {action_req}% exploration to {payload.action_id.replace('_', ' ')} here.")
    target_id = payload.target_id
    biome = payload.biome_id
    if payload.action_id == "hunt":
        candidates = discovered_monsters(ch, biome)
        if target_id and not is_discovered(ch, biome, "monster", target_id):
            raise HTTPException(status_code=403, detail="You have not discovered that creature yet.")
        if target_id and get_stock("monster", biome, target_id) <= 0:
            raise HTTPException(status_code=403, detail="There are no more of that creature in this area.")
        if not target_id:
            available = [
                m for m in monsters_for_biome(biome)
                if m["id"] in candidates and get_stock("monster", biome, m["id"]) > 0
            ]
            if not available:
                raise HTTPException(status_code=403, detail="No quarry remains to hunt here.")
            target_id = random.choice(available)["id"]
    elif payload.action_id in ("gather", "fish"):
        disc_nodes = discovered_nodes(ch, biome)
        if target_id:
            node = get_resource_node(target_id)
            if not node:
                raise HTTPException(status_code=404, detail="Unknown resource node.")
            if not is_discovered(ch, biome, "node", node["id"]):
                raise HTTPException(status_code=403, detail="You have not discovered that resource yet.")
            if get_stock("node", biome, node["id"]) <= 0:
                raise HTTPException(status_code=403, detail="That resource is depleted here.")
            target_id = node["id"]
        else:
            from regional_resources import node_on_cooldown
            pool = [
                n for n in nodes_for_biome(biome)
                if n["id"] in disc_nodes
                and get_stock("node", biome, n["id"]) > 0
                and not node_on_cooldown(ch, n["id"])
            ]
            if payload.action_id == "fish":
                pool = [n for n in pool if n["profession"] == "fishing"]
            elif payload.action_id == "gather":
                pool = [n for n in pool if n["profession"] != "fishing"]
            if not pool:
                raise HTTPException(status_code=403, detail="No gatherable resources remain here.")
            target_id = random.choice(pool)["id"]

    result = resolve_action(ch, payload.action_id, biome, target_id)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    ch["hp"] = max(0, min(ch["max_hp"], ch["hp"] + result["hp_delta"]))
    if result.get("status_applied"):
        _apply_status_to_character(ch, {
            "id": result["status_applied"],
            "name": result["status_applied"].title(),
            "kind": "debuff",
            "duration": 3,
            "magnitude": 1,
        })

    _apply_rewards_to_character(ch, result["rewards"])
    _level_up_if_needed(ch, result["rewards"])
    if result.get("monster_slain"):
        ch["kills"] = ch.get("kills", 0) + 1
        _update_daily_mission_progress(ch, {"kind": "kill", "id": result["monster_slain"], "count": 1})
    if payload.action_id in ("gather", "fish"):
        for it in result["rewards"].get("items", []):
            iid, q = it if isinstance(it, (list, tuple)) else (it, 1)
            _update_daily_mission_progress(ch, {"kind": "gather", "id": iid, "count": q})
    _update_daily_mission_progress(ch, {"kind": "action", "id": payload.action_id, "count": 1})

    # Update accepted quest progress
    _update_quest_progress(ch, {"kind": "action", "id": payload.action_id, "count": 1})
    if result.get("monster_slain"):
        _update_quest_progress(ch, {"kind": "kill", "id": result["monster_slain"], "count": 1})
    if payload.action_id in ("gather", "fish"):
        for it in result["rewards"].get("items", []):
            iid, q = it if isinstance(it, (list, tuple)) else (it, 1)
            _update_quest_progress(ch, {"kind": "gather", "id": iid, "count": q})
            _update_quest_progress(ch, {"kind": "gather_any", "count": q})

    # Racial resource ticking
    racial_msgs = tick_racial_resources_on_action(ch, result["outcome"], payload.action_id)

    # Heritage surge ticking
    surge_msgs = tick_surge_on_action(ch)

    # NPC quest progress — check if this action's outcome (success ≥4) satisfies
    # any active quest's kill/gather objective.
    quest_progress_updates: list[dict] = []
    if result["outcome"] >= 4:
        target_id = payload.target_id
        prog_dict = ch.setdefault("npc_quest_progress", {})
        for qid in list(ch.get("active_npc_quests", [])):
            q = NPC_QUESTS_BY_ID.get(qid)
            if not q:
                continue
            reqs = q.get("requirements", {}) or {}
            qp = prog_dict.setdefault(qid, {"kills": {}, "gathers": {}})
            bumped = False
            if payload.action_id in ("hunt", "boss") and target_id:
                for tgt, needed in reqs.get("kills", []) or []:
                    if tgt == target_id and qp["kills"].get(tgt, 0) < needed:
                        qp["kills"][tgt] = qp["kills"].get(tgt, 0) + 1
                        bumped = True
            if payload.action_id in ("gather", "fish") and target_id:
                for tgt, needed in reqs.get("gathers", []) or []:
                    if tgt == target_id and qp["gathers"].get(tgt, 0) < needed:
                        qp["gathers"][tgt] = qp["gathers"].get(tgt, 0) + 1
                        bumped = True
            if bumped:
                quest_progress_updates.append({"quest_id": qid, "progress": qp,
                                               "complete": _quest_progress_complete(q, qp)})

    # Phase C — Exploration progress: every action nudges progress for the
    # current biome (bigger nudges on explore actions, smaller on gather/hunt).
    biome_key = payload.biome_id or ch.get("current_biome")
    explore_hits: list[str] = []
    if biome_key:
        delta = exploration_delta_from_outcome(int(result["outcome"]))
        if payload.action_id != "explore":
            delta = max(0, delta // 2)  # non-explore actions still map the terrain, but slower
        if delta:
            _, _, explore_hits = apply_exploration_progress(ch, biome_key, delta)

    # Waystone discovery on exploration critical successes (Result 6) or high exploration progress.
    waystone_discovered: dict | None = None
    if payload.action_id == "explore" and result["outcome"] >= 5 and biome_key:
        from world_travel import WAYSTONES, WAYSTONES_BY_ID
        candidates = [w for w in WAYSTONES if w["biome"] == biome_key and w["id"] not in ch.get("known_waystones", [])]
        chance = 0.25 if result["outcome"] == 6 else 0.10
        if candidates and random.random() < chance:
            ws = random.choice(candidates)
            ch.setdefault("known_waystones", []).append(ws["id"])
            waystone_discovered = {"id": ws["id"], "name": ws["name"]}

    # Discoveries on explore and stock consumption on gather/fish
    discoveries: list[dict] = []
    if payload.action_id == "explore" and biome_key:
        discoveries = reveal_on_explore(ch, biome_key, result["outcome"])
        result["discoveries"] = discoveries
        if waystone_discovered:
            discoveries.append({
                "id": waystone_discovered["id"],
                "name": waystone_discovered["name"],
                "kind": "waystone",
                "rarity": "legendary",
            })
        if discoveries:
            from discovery_narratives import discovery_narrative
            result["narrative"] = result.get("narrative", "") + discovery_narrative(discoveries)
    elif payload.action_id in ("gather", "fish"):
        node = result.get("node")
        if node and biome_key:
            stock_id = node["id"] if not node.get("scavenge") else result.get("target_id")
            if stock_id and consume_stock("node", biome_key, stock_id):
                node["stock_remaining"] = get_stock("node", biome_key, stock_id)

    # Phase D — Profession XP: gathering-family actions grant profession XP for
    # the matching profession the character has learned. Prefer the node profession.
    profession_ranks: list[tuple[str, str]] = []
    node_prof = (result.get("node") or {}).get("profession")
    if node_prof and not (result.get("node") or {}).get("scavenge") and result["outcome"] >= 3:
        from professions import craft_points_for_roll
        pts = craft_points_for_roll(result["outcome"])
        # Continental multiplier for profession points
        from world_data import xp_multiplier_for
        pts = int(pts * xp_multiplier_for(ch.get("current_continent"), node_prof))
        if pts > 0:
            rank_change = gain_profession_xp(ch, node_prof, pts)
            if rank_change:
                profession_ranks.append(rank_change)
    else:
        # legacy fallback for actions without a resource node
        action_prof_map = {"gather": ["herbalism", "logging", "mining"], "fish": ["fishing"],
                           "hunt": ["hunting"], "loot_ruins": ["excavation"]}
        for pid in action_prof_map.get(payload.action_id, []):
            has = any(p.get("id") == pid for p in ch.get("professions", []))
            if has and result["outcome"] >= 3:
                from professions import craft_points_for_roll
                pts = craft_points_for_roll(result["outcome"])
                if pts > 0:
                    rank_change = gain_profession_xp(ch, pid, pts)
                    if rank_change:
                        profession_ranks.append(rank_change)

    # Reputation gains for successful regional actions (hunt/gather/fish/explore) on the current continent.
    rep_change: tuple[str, str, str] | None = None
    if result["outcome"] >= 4 and payload.action_id in ("hunt", "gather", "fish", "explore"):
        cont = ch.get("current_continent")
        if cont:
            rep_delta = {"hunt": 3, "gather": 2, "fish": 2, "explore": 5}.get(payload.action_id, 0)
            if result["outcome"] == 6:
                rep_delta += 5
            # Continental bonus: Concordia foreign_reputation
            from world_data import continental_bonus_for
            _fr = continental_bonus_for(cont, "foreign_reputation")
            if _fr:
                rep_delta = int(rep_delta * float(_fr))
            new_level, old_level = add_reputation(ch, cont, rep_delta)
            rep_change = (new_level, cont, old_level)

    # Tick status durations so debuffs (Bleeding, Weary, Poisoned, etc.) expire naturally.
    _tick_character_statuses(ch)

    # Heritage progress tracking: gather/craft on heritage continent
    _hcont = ch.get("current_continent", "")
    if _hcont and is_heritage_month_for(_hcont) and result["outcome"] >= 3:
        _yr = date.today().year
        if payload.action_id in ("gather", "fish"):
            _items = result.get("rewards", {}).get("items", [])
            _qty = sum(q for _, q in _items if isinstance(q, int)) if _items else 1
            await _heritage_update_progress(ch["id"], _hcont, _yr, resources_gathered=_qty)
            await _heritage_record_participation(ch["id"], _hcont, _yr)
        elif payload.action_id == "hunt":
            await _heritage_update_progress(ch["id"], _hcont, _yr, resources_gathered=1)
            await _heritage_record_participation(ch["id"], _hcont, _yr)

    # --- Biome encounter roll ---
    encounter: dict | None = None
    if biome_key and not ch.get("pending_encounter"):
        tick_encounter_cooldowns(ch, biome_key)
        rolled = maybe_trigger_encounter(ch, biome_key, payload.action_id, result["outcome"])
        if rolled:
            encounter = rolled
            ch["pending_encounter"] = encounter

    if ch["hp"] <= 0:
        ch["hp"] = 1

    await db.characters.update_one({"_id": ObjectId(ch["id"])}, {"$set": {
        "hp": ch["hp"], "max_hp": ch["max_hp"], "gold": ch["gold"], "xp": ch["xp"],
        "level": ch["level"], "base_stats": ch.get("base_stats", ch["stats"]), "stats": ch["stats"], "inventory": ch["inventory"],
        "item_instances": ch.get("item_instances", []),
        "statuses": ch["statuses"], "kills": ch["kills"],
        "daily_missions": ch.get("daily_missions", []),
        "_biomes_today": ch.get("_biomes_today", []),
        "active_quests": ch.get("active_quests", []),
        "exhaustion": ch.get("exhaustion", 0),
        "resolve": ch.get("resolve", 100),
        "oath_progress": ch.get("oath_progress", 0),
        "celestial_charge": ch.get("celestial_charge", 0),
        "stoneguard": ch.get("stoneguard", 0),
        "harmony": ch.get("harmony", 0),
        "defiance": ch.get("defiance", 0),
        "inner_blood": ch.get("inner_blood", 0),
        "tide": ch.get("tide", 0),
        "verdant_essence": ch.get("verdant_essence", 0),
        "heritage_surge_active": ch.get("heritage_surge_active", 0),
        "heritage_surge_last_used": ch.get("heritage_surge_last_used"),
        "exploration_progress": ch.get("exploration_progress", {}),
        "biome_discoveries": ch.get("biome_discoveries", {}),
        "professions": ch.get("professions", []),
        "npc_quest_progress": ch.get("npc_quest_progress", {}),
        "tools": ch.get("tools", {}),
        "node_cooldowns": ch.get("node_cooldowns", {}),
        "known_waystones": ch.get("known_waystones", []),
        "active_waystones": ch.get("active_waystones", []),
        "reputation": ch.get("reputation", {}),
        "encounter_cooldowns": ch.get("encounter_cooldowns", {}),
        "pending_encounter": ch.get("pending_encounter"),
    }})

    if result["outcome"] == 6:
        target_disp = result.get("target_name") or "the unknown"
        await _push_world_event(ch["name"], f"{ch['name']} achieved a critical {payload.action_id} against {target_disp}.", "loot")

    return {"result": result, "character": ch, "racial_msgs": racial_msgs,
            "surge_msgs": surge_msgs,
            "explore_hits": explore_hits, "profession_ranks": profession_ranks,
            "quest_progress_updates": quest_progress_updates,
            "rep_change": rep_change, "waystone_discovered": waystone_discovered,
            "discoveries": discoveries, "encounter": encounter}


# ---------------- ENCOUNTERS ----------------
@api.post("/game/encounter/resolve")
async def resolve_encounter(payload: EncounterResolvePayload, user: dict = Depends(_get_current_user)):
    ch = await _get_character_or_404(user["_id"])
    encounter = ch.get("pending_encounter")
    if not encounter:
        raise HTTPException(status_code=400, detail="No pending encounter to resolve.")

    resolution = resolve_encounter_action(encounter, payload.action_id)
    if "error" in resolution:
        raise HTTPException(status_code=400, detail=resolution["error"])

    effects = resolution.get("effects", {})

    # Apply gold effect (50% reduction)
    gold_delta = effects.get("gold", 0)
    if gold_delta:
        ch["gold"] = max(0, ch.get("gold", 0) + int(gold_delta * 0.5))

    # Apply HP effect
    hp_delta = effects.get("hp", 0)
    if hp_delta:
        ch["hp"] = max(0, min(ch["max_hp"], ch["hp"] + hp_delta))

    # Apply XP effect (50% reduction)
    xp_delta = effects.get("xp", 0)
    if xp_delta:
        xp_reduced = int(xp_delta * 0.5)
        ch["xp"] = ch.get("xp", 0) + xp_reduced
        _level_up_if_needed(ch, {"xp": xp_reduced})

    # Apply item effects
    items = effects.get("items", [])
    for item_tuple in items:
        item_id, qty = item_tuple if isinstance(item_tuple, (list, tuple)) else (item_tuple, 1)
        if qty > 0:
            _apply_rewards_to_character(ch, {"items": [(item_id, qty)]})
        elif qty < 0:
            inv = ch.get("inventory", [])
            for entry in inv:
                if entry.get("item_id") == item_id:
                    entry["qty"] = max(0, entry.get("qty", 0) + qty)
                    break

    # Clear the pending encounter
    ch["pending_encounter"] = None

    # If the encounter triggers combat, return combat monster id
    combat_monster_id = resolution.get("combat")

    await db.characters.update_one({"_id": ObjectId(ch["id"])}, {"$set": {
        "hp": ch["hp"], "gold": ch["gold"], "xp": ch["xp"], "level": ch["level"],
        "inventory": ch["inventory"], "item_instances": ch.get("item_instances", []),
        "pending_encounter": None,
    }})

    return {
        "character": ch,
        "resolution": resolution,
        "combat_monster_id": combat_monster_id,
    }


# ---------------- COMBAT ----------------
@api.post("/game/combat/start")
async def combat_start(payload: CombatStartPayload, user: dict = Depends(_get_current_user)):
    ch = await _get_character_or_404(user["_id"])
    biome = payload.biome_id or ch.get("current_biome")
    if not is_discovered(ch, biome, "monster", payload.monster_id):
        raise HTTPException(status_code=403, detail="You have not discovered that creature yet.")
    if get_stock("monster", biome, payload.monster_id) <= 0:
        raise HTTPException(status_code=403, detail="There are no more of that creature in this area.")
    state = start_combat(ch, payload.monster_id)
    state["biome_id"] = biome
    if "error" in state:
        raise HTTPException(status_code=400, detail=state["error"])
    combat_doc = {"user_id": user["_id"], "character_id": ch["id"], "state": state,
                  "created_at": datetime.now(timezone.utc).isoformat()}
    r = await db.combats.insert_one(combat_doc)
    state["combat_id"] = str(r.inserted_id)
    return {"state": state, "character": ch}


@api.post("/game/combat/turn")
async def combat_take_turn(payload: CombatTurnPayload, user: dict = Depends(_get_current_user)):
    ch = await _get_character_or_404(user["_id"])
    combat = await db.combats.find_one({"_id": ObjectId(payload.combat_id), "user_id": user["_id"]})
    if not combat:
        raise HTTPException(status_code=404, detail="Combat not found")
    state = combat["state"]
    result = combat_turn(ch, state, payload.manual_skill_id, payload.manual_item_id, payload.action_type)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    updates = {
        "hp": ch["hp"], "statuses": ch.get("statuses", []),
        "inventory": ch.get("inventory", []),
        "item_instances": ch.get("item_instances", []),
    }
    if result.get("victory"):
        _apply_rewards_to_character(ch, result["rewards"])
        _level_up_if_needed(ch, result["rewards"])
        ch["kills"] = ch.get("kills", 0) + 1
        biome = combat["state"].get("biome_id") or ch.get("current_biome")
        consume_stock("monster", biome, combat["state"]["monster_id"])
        _update_daily_mission_progress(ch, {"kind": "kill", "id": combat["state"]["monster_id"], "count": 1})
        _update_quest_progress(ch, {"kind": "kill", "id": combat["state"]["monster_id"], "count": 1})
        # Hunting profession XP on victory
        hunt_prof = next((p for p in ch.get("professions", []) if p.get("id") == "hunting"), None)
        if hunt_prof:
            from professions import craft_points_for_roll, gain_profession_xp
            from world_data import xp_multiplier_for
            # Use combat outcome from the last log entry as proxy for roll quality
            outcome = 4  # default to success for victory
            for entry in reversed(result.get("log", [])):
                if entry.get("outcome"):
                    outcome = entry["outcome"]
                    break
            pts = craft_points_for_roll(outcome)
            pts = int(pts * xp_multiplier_for(ch.get("current_continent"), "hunting"))
            if pts > 0:
                rank_change = gain_profession_xp(ch, "hunting", pts)
                if rank_change:
                    result.setdefault("profession_ranks", []).append(rank_change)
                updates["professions"] = ch.get("professions", [])
        updates.update({
            "gold": ch["gold"], "xp": ch["xp"], "level": ch["level"], "base_stats": ch.get("base_stats", ch["stats"]), "stats": ch["stats"],
            "max_hp": ch["max_hp"], "kills": ch["kills"],
            "daily_missions": ch.get("daily_missions", []),
            "active_quests": ch.get("active_quests", []),
            "inner_blood": ch.get("inner_blood", 0),
            "exhaustion": ch.get("exhaustion", 0),
        })
        monster = next((m for m in MONSTERS if m["id"] == combat["state"]["monster_id"]), None)
        m_name = monster["name"] if monster else combat["state"].get("monster_name", "a beast")
        await _push_world_event(ch["name"], f"{ch['name']} slew {m_name}.", "kill")
        # Heritage boss victory — award tokens + track progress
        if combat["state"].get("monster_is_heritage_boss"):
            _hcont = combat["state"].get("heritage_continent")
            _htok = combat["state"].get("heritage_token_count", 5)
            if _hcont:
                _yr = date.today().year
                await _heritage_add_tokens(ch["id"], _hcont, _htok)
                await _heritage_update_progress(ch["id"], _hcont, _yr,
                    boss_kills=1, tokens_earned=_htok)
                await _heritage_record_participation(ch["id"], _hcont, _yr)
                result.setdefault("heritage_reward", {
                    "continent": _hcont,
                    "tokens": _htok,
                    "boss_name": combat["state"].get("monster_name", "Heritage Boss"),
                })
    elif result.get("victory") is False:
        loss = min(ch.get("gold", 0), 20)
        ch["gold"] -= loss
        updates["gold"] = ch["gold"]
        # Death → Sanctuary teleport
        from world_data import HOMETOWN_BY_CONTINENT
        sanctuary_town = ch.get("last_sanctuary_town") or ch.get("home_town") or \
            HOMETOWN_BY_CONTINENT.get(ch.get("current_continent", "valeria"), "oathspire")
        sanctuary_town_obj = get_town(sanctuary_town)
        sanctuary_continent = sanctuary_town_obj["continent"] if sanctuary_town_obj else ch.get("current_continent", "valeria")
        ch["hp"] = ch["max_hp"] // 2  # 50% HP on respawn
        ch["current_town"] = sanctuary_town
        ch["current_continent"] = sanctuary_continent
        ch["current_biome"] = None
        ch["deaths"] = ch.get("deaths", 0) + 1
        monster_name = state.get("monster_name", "a beast")
        ch["last_death"] = {
            "cause": monster_name,
            "location": state.get("biome_id", ch.get("current_biome")),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        # Apply Recovering debuff
        from game_engine import make_status
        recovering = make_status("recovering")
        ch["statuses"] = [s for s in ch.get("statuses", []) if s.get("id") != "recovering"]
        ch["statuses"].append(recovering)
        # Ensure sanctuary town is in visited_towns
        if sanctuary_town not in ch.get("visited_towns", []):
            ch.setdefault("visited_towns", []).append(sanctuary_town)
        updates.update({
            "hp": ch["hp"],
            "current_town": ch["current_town"],
            "current_continent": ch["current_continent"],
            "current_biome": ch["current_biome"],
            "deaths": ch["deaths"],
            "last_death": ch["last_death"],
            "statuses": ch["statuses"],
            "visited_towns": ch["visited_towns"],
        })
        result["sanctuary_teleport"] = {
            "town": sanctuary_town,
            "town_name": sanctuary_town_obj["name"] if sanctuary_town_obj else sanctuary_town,
            "continent": sanctuary_continent,
        }

    # Recompute stats with faith scaling based on post-combat HP
    _recompute_stats(ch)
    updates["stats"] = dict(ch["stats"])  # save base stats to DB (without combat-only bonuses)
    updates["paladin_faith_tier"] = ch.get("paladin_faith_tier")
    updates["paladin_faith_bonuses"] = ch.get("paladin_faith_bonuses")

    # Attach combat-only bonuses to character for frontend display
    knight_bonuses = state.get("knight_current_oath_bonuses")
    if knight_bonuses and state.get("active"):
        ch["knight_current_oath_bonuses"] = knight_bonuses
        # Add bonuses to stats so totals reflect combat state (not persisted to DB)
        for stat, val in knight_bonuses.items():
            if val and not stat.startswith("enemy_"):
                ch["stats"][stat] = ch["stats"].get(stat, 0) + val
    else:
        ch.pop("knight_current_oath_bonuses", None)

    # Re-apply active knight self stat_mods (from skills like Iron Stance) for frontend display
    knight_self_mods = state.get("knight_self_stat_mods", [])
    if knight_self_mods and state.get("active"):
        ch["knight_self_stat_mods"] = {}
        for entry in knight_self_mods:
            for stat, val in entry.get("mods", {}).items():
                ch["stats"][stat] = ch["stats"].get(stat, 0) + val
                ch["knight_self_stat_mods"][stat] = ch["knight_self_stat_mods"].get(stat, 0) + val
    else:
        ch.pop("knight_self_stat_mods", None)

    await db.characters.update_one({"_id": ObjectId(ch["id"])}, {"$set": updates})
    await db.combats.update_one({"_id": ObjectId(payload.combat_id)}, {"$set": {"state": state}})

    return {"result": result, "character": ch, "combat_id": payload.combat_id}


@api.post("/game/combat/telegraph")
async def combat_telegraph(payload: CombatTelegraphPayload, user: dict = Depends(_get_current_user)):
    """Get a telegraph of the monster's next intended action (read-only, no state mutation)."""
    combat = await db.combats.find_one({"_id": ObjectId(payload.combat_id), "user_id": user["_id"]})
    if not combat:
        raise HTTPException(status_code=404, detail="Combat not found")
    state = combat["state"]
    ch = await _get_character_or_404(user["_id"])
    telegraph = generate_telegraph(state, ch)
    return {"telegraph": telegraph}


@api.post("/game/combat/alchemist/cf")
async def combat_alchemist_cf(payload: AlchemistCFPayload, user: dict = Depends(_get_current_user)):
    """Spend Combo Flow points on an adaptive action (Alchemist only)."""
    combat = await db.combats.find_one({"_id": ObjectId(payload.combat_id), "user_id": user["_id"]})
    if not combat:
        raise HTTPException(status_code=404, detail="Combat not found")
    state = combat["state"]
    ch = await _get_character_or_404(user["_id"])

    if "alchemist" not in (ch.get("masteries") or []):
        raise HTTPException(status_code=403, detail="Alchemist mastery required")

    if not state.get("active"):
        raise HTTPException(status_code=400, detail="Combat is not active")

    log: list[dict] = []
    success = _alch_spend_cf(state, ch, {}, log, payload.action, payload.choice)
    if not success:
        raise HTTPException(status_code=400, detail=f"Insufficient CF for {payload.action}")

    await db.combats.update_one({"_id": ObjectId(payload.combat_id)}, {"$set": {"state": state}})
    return {"state": state, "log": log, "cf": state.get("alchemist_cf", 0)}


@api.post("/game/combat/alchemist/pre-imbue")
async def combat_alchemist_pre_imbue(payload: AlchemistPreImbuePayload, user: dict = Depends(_get_current_user)):
    """Set pre-combat imbue for Alchemist (auto-loaded at combat start, no turn cost)."""
    combat = await db.combats.find_one({"_id": ObjectId(payload.combat_id), "user_id": user["_id"]})
    if not combat:
        raise HTTPException(status_code=404, detail="Combat not found")
    state = combat["state"]
    ch = await _get_character_or_404(user["_id"])

    if "alchemist" not in (ch.get("masteries") or []):
        raise HTTPException(status_code=403, detail="Alchemist mastery required")

    sk = SKILLS_BY_ID.get(payload.skill_id)
    if not sk or sk.get("power_type") != "imbue":
        raise HTTPException(status_code=400, detail="Invalid imbue skill")

    state["alchemist_pre_imbue"] = payload.skill_id
    await db.combats.update_one({"_id": ObjectId(payload.combat_id)}, {"$set": {"state": state}})
    return {"state": state, "pre_imbue": payload.skill_id}


@api.post("/game/combat/skin")
async def combat_skin_monster(payload: SkinPayload, user: dict = Depends(_get_current_user)):
    """Skin a defeated monster for bonus materials."""
    ch = await _get_character_or_404(user["_id"])
    combat = await db.combats.find_one({"_id": ObjectId(payload.combat_id), "user_id": user["_id"]})
    if not combat:
        raise HTTPException(status_code=404, detail="Combat not found")
    state = combat["state"]
    result = skin_monster(ch, state)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    updates = {"inventory": ch.get("inventory", []), "item_instances": ch.get("item_instances", [])}
    if result.get("rank_change"):
        updates["professions"] = ch.get("professions", [])

    await db.characters.update_one({"_id": ObjectId(ch["id"])}, {"$set": updates})
    await db.combats.update_one({"_id": ObjectId(payload.combat_id)}, {"$set": {"state": state}})

    return {"result": result, "character": ch}


@api.post("/game/combat/tame")
async def combat_tame_monster(payload: TamePayload, user: dict = Depends(_get_current_user)):
    """Attempt to tame the current monster in combat."""
    ch = await _get_character_or_404(user["_id"])
    combat = await db.combats.find_one({"_id": ObjectId(payload.combat_id), "user_id": user["_id"]})
    if not combat:
        raise HTTPException(status_code=404, detail="Combat not found")
    state = combat["state"]

    result = attempt_tame(ch, state)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    # On success, add to bestiary
    if result.get("success"):
        bestiary = ch.get("bestiary", [])
        monster = result["monster"]
        # Bestiary cap: 50 tamed creatures
        if len(bestiary) >= 50:
            raise HTTPException(status_code=400, detail="Bestiary is full (50/50). Release a creature first.")
        bestiary.append({
            "id": monster["id"],
            "name": monster["name"],
            "creature_tier": monster.get("creature_tier", "normal"),
            "power": monster.get("power", 5),
            "stats": monster.get("stats", {}),
            "passive_buff": monster.get("passive_buff", []),
            "profile_skills": monster.get("profile_skills", {}),
            "signature_fusion": monster.get("signature_fusion", []),
            "boss_aura": monster.get("boss_aura"),
            "legendary_passive": monster.get("legendary_passive"),
            "personality": monster.get("personality", "aggressive"),
            "archetype": monster.get("archetype", "striker"),
        })
        await db.characters.update_one({"_id": ObjectId(ch["id"])}, {"$set": {"bestiary": bestiary}})
        ch["bestiary"] = bestiary

    await db.combats.update_one({"_id": ObjectId(payload.combat_id)}, {"$set": {"state": state}})

    return {"result": result, "character": ch, "combat_id": payload.combat_id}


# ---------------- DRUID SUMMON SYSTEM ----------------

@api.post("/game/combat/summon")
async def combat_summon_creature(payload: SummonPayload, user: dict = Depends(_get_current_user)):
    """Summon a tamed creature from the bestiary onto the battlefield."""
    ch = await _get_character_or_404(user["_id"])
    if not _is_druid(ch):
        raise HTTPException(status_code=403, detail="Druid mastery required.")
    combat = await db.combats.find_one({"_id": ObjectId(payload.combat_id), "user_id": user["_id"]})
    if not combat:
        raise HTTPException(status_code=404, detail="Combat not found")
    state = combat["state"]
    if not state.get("active"):
        raise HTTPException(status_code=400, detail="Combat is not active")

    bestiary = ch.get("bestiary", [])
    entry = next((b for b in bestiary if b["id"] == payload.creature_id), None)
    if not entry:
        raise HTTPException(status_code=404, detail="Creature not found in bestiary")

    log: list[dict] = []
    result = _druid_summon_creature(ch, state, entry, log)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    state["log"].extend(log)
    await db.combats.update_one({"_id": ObjectId(payload.combat_id)}, {"$set": {"state": state}})
    await db.characters.update_one({"_id": ObjectId(ch["id"])}, {"$set": {"stats": ch.get("stats", {})}})

    return {"result": result, "character": ch, "combat_id": payload.combat_id}


@api.post("/game/combat/unsummon")
async def combat_unsummon_creature(payload: UnsummonPayload, user: dict = Depends(_get_current_user)):
    """Unsummon a creature from the battlefield."""
    ch = await _get_character_or_404(user["_id"])
    if not _is_druid(ch):
        raise HTTPException(status_code=403, detail="Druid mastery required.")
    combat = await db.combats.find_one({"_id": ObjectId(payload.combat_id), "user_id": user["_id"]})
    if not combat:
        raise HTTPException(status_code=404, detail="Combat not found")
    state = combat["state"]
    if not state.get("active"):
        raise HTTPException(status_code=400, detail="Combat is not active")

    log: list[dict] = []
    result = _druid_unsummon_creature(ch, state, payload.creature_id, log)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    state["log"].extend(log)
    await db.combats.update_one({"_id": ObjectId(payload.combat_id)}, {"$set": {"state": state}})
    await db.characters.update_one({"_id": ObjectId(ch["id"])}, {"$set": {"stats": ch.get("stats", {})}})

    return {"result": result, "character": ch, "combat_id": payload.combat_id}


@api.post("/game/combat/fuse")
async def combat_fuse_with_summon(payload: FusePayload, user: dict = Depends(_get_current_user)):
    """Fuse with an active summon for stat stacking and ability riders."""
    ch = await _get_character_or_404(user["_id"])
    if not _is_druid(ch):
        raise HTTPException(status_code=403, detail="Druid mastery required.")
    combat = await db.combats.find_one({"_id": ObjectId(payload.combat_id), "user_id": user["_id"]})
    if not combat:
        raise HTTPException(status_code=404, detail="Combat not found")
    state = combat["state"]
    if not state.get("active"):
        raise HTTPException(status_code=400, detail="Combat is not active")

    log: list[dict] = []
    result = _druid_fuse(ch, state, payload.creature_id, log)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    state["log"].extend(log)
    await db.combats.update_one({"_id": ObjectId(payload.combat_id)}, {"$set": {"state": state}})
    await db.characters.update_one({"_id": ObjectId(ch["id"])}, {"$set": {"stats": ch.get("stats", {})}})

    return {"result": result, "character": ch, "combat_id": payload.combat_id}


@api.post("/game/combat/end_fusion")
async def combat_end_fusion(payload: EndFusionPayload, user: dict = Depends(_get_current_user)):
    """End fusion with a summon early."""
    ch = await _get_character_or_404(user["_id"])
    if not _is_druid(ch):
        raise HTTPException(status_code=403, detail="Druid mastery required.")
    combat = await db.combats.find_one({"_id": ObjectId(payload.combat_id), "user_id": user["_id"]})
    if not combat:
        raise HTTPException(status_code=404, detail="Combat not found")
    state = combat["state"]
    if not state.get("active"):
        raise HTTPException(status_code=400, detail="Combat is not active")
    if not state.get("druid_fusion_active"):
        raise HTTPException(status_code=400, detail="No active fusion to end.")

    log: list[dict] = []
    _druid_end_fusion(state, ch, log)
    state["log"].extend(log)
    await db.combats.update_one({"_id": ObjectId(payload.combat_id)}, {"$set": {"state": state}})
    await db.characters.update_one({"_id": ObjectId(ch["id"])}, {"$set": {"stats": ch.get("stats", {})}})

    return {"result": {"success": True}, "character": ch, "combat_id": payload.combat_id}


@api.post("/game/combat/summon_mode")
async def combat_set_summon_mode(payload: SummonModePayload, user: dict = Depends(_get_current_user)):
    """Set a summon's AI mode (auto/manual)."""
    ch = await _get_character_or_404(user["_id"])
    if not _is_druid(ch):
        raise HTTPException(status_code=403, detail="Druid mastery required.")
    combat = await db.combats.find_one({"_id": ObjectId(payload.combat_id), "user_id": user["_id"]})
    if not combat:
        raise HTTPException(status_code=404, detail="Combat not found")
    state = combat["state"]
    if not state.get("active"):
        raise HTTPException(status_code=400, detail="Combat is not active")

    active = state.get("druid_active_summons", [])
    summon = next((s for s in active if s["id"] == payload.creature_id), None)
    if not summon:
        raise HTTPException(status_code=404, detail="That creature is not currently summoned.")
    if payload.mode not in ("auto", "manual"):
        raise HTTPException(status_code=400, detail="Mode must be 'auto' or 'manual'.")

    summon["mode"] = payload.mode
    await db.combats.update_one({"_id": ObjectId(payload.combat_id)}, {"$set": {"state": state}})

    return {"result": {"success": True, "mode": payload.mode}, "combat_id": payload.combat_id}


@api.get("/game/bestiary")
async def get_bestiary(user: dict = Depends(_get_current_user)):
    """View the character's bestiary of tamed creatures."""
    ch = await _get_character_or_404(user["_id"])
    bestiary = ch.get("bestiary", [])
    max_summons = _druid_get_max_summons(ch) if _is_druid(ch) else 0
    return {
        "bestiary": bestiary,
        "count": len(bestiary),
        "cap": 50,
        "max_active_summons": max_summons,
        "is_druid": _is_druid(ch),
    }


@api.post("/game/bestiary/release")
async def release_bestiary_creature(payload: ReleaseCreaturePayload, user: dict = Depends(_get_current_user)):
    """Release a tamed creature from the bestiary to free up a slot."""
    ch = await _get_character_or_404(user["_id"])
    bestiary = ch.get("bestiary", [])
    entry = next((b for b in bestiary if b["id"] == payload.creature_id), None)
    if not entry:
        raise HTTPException(status_code=404, detail="Creature not found in bestiary.")

    bestiary = [b for b in bestiary if b["id"] != payload.creature_id]
    await db.characters.update_one({"_id": ObjectId(ch["id"])}, {"$set": {"bestiary": bestiary}})
    ch["bestiary"] = bestiary

    return {"result": {"success": True, "released": entry["name"]}, "character": ch}


# ---------------- CRAFTING ----------------
CRAFTING_QUEUE_SIZE = 1


def _tick_crafting_queue(character: dict):
    """Auto-complete any queued crafts whose timer has elapsed. Returns ready entries."""
    now = datetime.now(timezone.utc)
    ready = []
    for entry in character.get("crafting_queue", []):
        if entry.get("claimed"):
            continue
        try:
            finishes = datetime.fromisoformat(entry["finishes_at"])
            if now >= finishes:
                ready.append(entry)
        except (ValueError, TypeError):
            continue
    return ready


@api.post("/game/craft")
async def craft(payload: CraftPayload, user: dict = Depends(_get_current_user)):
    ch = await _get_character_or_404(user["_id"])
    recipe = RECIPES_BY_ID.get(payload.recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Unknown recipe")
    if not _recipe_available_here(ch, recipe):
        raise HTTPException(status_code=403, detail="The local forge cannot craft that recipe here.")
    # Tick any existing finished crafts before starting a new one
    _tick_crafting_queue(ch)
    result = start_craft(ch, payload.recipe_id)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    # Consume materials up front (queued or instant)
    for mat_id, qty in result["materials_consumed"]:
        _remove_item_from_inventory(ch, mat_id, qty)

    if result.get("queued"):
        await db.characters.update_one({"_id": ObjectId(ch["id"])}, {"$set": {
            "inventory": ch["inventory"],
            "crafting_queue": ch.get("crafting_queue", []),
        }})
        return {"queued": True, "result": result, "character": ch}

    # Instant craft — finish immediately
    if not result.get("lost_materials") and result.get("output_item"):
        _add_item_to_inventory(ch, result["output_item"], 1)
        ch["crafts"] = ch.get("crafts", 0) + 1
        _update_daily_mission_progress(ch, {"kind": "craft", "count": 1})
        _update_quest_progress(ch, {"kind": "craft", "count": 1})

    _apply_rewards_to_character(ch, {"gold": 0, "xp": 10, "items": []})

    await db.characters.update_one({"_id": ObjectId(ch["id"])}, {"$set": {
        "inventory": ch["inventory"], "gold": ch["gold"], "xp": ch["xp"], "level": ch["level"],
        "base_stats": ch.get("base_stats", ch["stats"]), "stats": ch["stats"], "max_hp": ch["max_hp"], "crafts": ch["crafts"],
        "daily_missions": ch.get("daily_missions", []),
    }})

    if result["outcome"] == 6:
        await _push_world_event(ch["name"], f"{ch['name']} crafted a masterwork item.", "craft")

    return {"result": result, "character": ch}


@api.get("/game/craft/queue")
async def craft_queue(user: dict = Depends(_get_current_user)):
    ch = await _get_character_or_404(user["_id"])
    ready = _tick_crafting_queue(ch)
    return {"queue": ch.get("crafting_queue", []), "ready": [r["recipe_id"] for r in ready], "character": ch}


@api.post("/game/craft/claim")
async def claim_craft(request: Request, user: dict = Depends(_get_current_user)):
    body = await request.json()
    ch = await _get_character_or_404(user["_id"])
    queue = ch.get("crafting_queue", [])
    if not queue:
        raise HTTPException(status_code=400, detail="No craft to claim")

    entry = queue[0]
    now = datetime.now(timezone.utc)
    try:
        finishes = datetime.fromisoformat(entry["finishes_at"])
    except (ValueError, TypeError):
        raise HTTPException(status_code=400, detail="Invalid craft timer")
    if now < finishes:
        raise HTTPException(status_code=400, detail="Craft is not yet finished")

    result = finish_craft(ch, entry)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    if not result.get("lost_materials") and result.get("output_item"):
        _add_item_to_inventory(ch, result["output_item"], 1)
        ch["crafts"] = ch.get("crafts", 0) + 1
        _update_daily_mission_progress(ch, {"kind": "craft", "count": 1})
        _update_quest_progress(ch, {"kind": "craft", "count": 1})
        # Heritage progress tracking: craft on heritage continent
        _hcont = ch.get("current_continent", "")
        if _hcont and is_heritage_month_for(_hcont):
            _yr = date.today().year
            await _heritage_update_progress(ch["id"], _hcont, _yr, items_crafted=1)
            await _heritage_record_participation(ch["id"], _hcont, _yr)

    _apply_rewards_to_character(ch, {"gold": 0, "xp": 10, "items": []})

    # Remove completed entry from queue
    ch["crafting_queue"] = [q for q in queue if q is not entry]

    await db.characters.update_one({"_id": ObjectId(ch["id"])}, {"$set": {
        "inventory": ch["inventory"], "gold": ch["gold"], "xp": ch["xp"], "level": ch["level"],
        "base_stats": ch.get("base_stats", ch["stats"]), "stats": ch["stats"], "max_hp": ch["max_hp"], "crafts": ch["crafts"],
        "crafting_queue": ch["crafting_queue"],
        "daily_missions": ch.get("daily_missions", []),
        "professions": ch.get("professions", []),
    }})

    if result["outcome"] == 6:
        await _push_world_event(ch["name"], f"{ch['name']} crafted a masterwork item.", "craft")

    return {"result": result, "character": ch}


@api.post("/game/craft/cancel")
async def cancel_craft(user: dict = Depends(_get_current_user)):
    ch = await _get_character_or_404(user["_id"])
    queue = ch.get("crafting_queue", [])
    if not queue:
        raise HTTPException(status_code=400, detail="No craft to cancel")
    entry = queue[0]
    recipe = RECIPES_BY_ID.get(entry["recipe_id"])
    if recipe:
        # Refund half the materials
        for mat_id, qty in recipe["materials"]:
            _add_item_to_inventory(ch, mat_id, qty // 2)
    ch["crafting_queue"] = []
    await db.characters.update_one({"_id": ObjectId(ch["id"])}, {"$set": {
        "inventory": ch["inventory"], "crafting_queue": [],
    }})
    return {"character": ch, "message": "Craft cancelled. Half the materials were recovered."}


@api.post("/game/craft/enchant")
async def enchant_item(request: Request, user: dict = Depends(_get_current_user)):
    body = await request.json()
    recipe_id = body.get("recipe_id")
    target_item_id = body.get("target_item_id")
    if not recipe_id or not target_item_id:
        raise HTTPException(status_code=400, detail="recipe_id and target_item_id are required")

    ch = await _get_character_or_404(user["_id"])
    recipe = RECIPES_BY_ID.get(recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Unknown recipe")
    if not recipe.get("is_enchantment"):
        raise HTTPException(status_code=400, detail="Not an enchantment recipe")
    if not _recipe_available_here(ch, recipe):
        raise HTTPException(status_code=403, detail="Cannot enchant here — need the right trade NPC.")

    result = start_enchant(ch, recipe_id, target_item_id)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    # Consume materials
    for mat_id, qty in result["materials_consumed"]:
        _remove_item_from_inventory(ch, mat_id, qty)

    # Handle item destruction or enchantment application
    inv = ch.get("inventory", [])
    if result.get("item_destroyed"):
        # Remove the target item from inventory
        for i, entry in enumerate(inv):
            if entry.get("item_id") == target_item_id:
                if entry.get("quantity", 1) > 1:
                    entry["quantity"] -= 1
                else:
                    inv.pop(i)
                break
    elif result.get("enchant_applied"):
        # Add enchantment to the inventory entry
        for entry in inv:
            if entry.get("item_id") == target_item_id:
                enchants = entry.setdefault("enchantments", [])
                enchants.append({
                    "stat": result["enchant_stat"],
                    "bonus": result["enchant_bonus"],
                    "recipe_id": recipe_id,
                })
                break

    _apply_rewards_to_character(ch, {"gold": 0, "xp": 10, "items": []})

    await db.characters.update_one({"_id": ObjectId(ch["id"])}, {"$set": {
        "inventory": ch["inventory"], "gold": ch["gold"], "xp": ch["xp"], "level": ch["level"],
        "base_stats": ch.get("base_stats", ch["stats"]), "stats": ch["stats"], "max_hp": ch["max_hp"],
        "professions": ch.get("professions", []),
    }})

    if result["outcome"] == 6:
        await _push_world_event(ch["name"], f"{ch['name']} enchanted a masterwork item.", "craft")

    return {"result": result, "character": ch}


# ---------------- SKILLS ----------------
@api.post("/game/skill/learn")
async def learn_skill(payload: LearnSkillPayload, user: dict = Depends(_get_current_user)):
    ch = await _get_character_or_404(user["_id"])
    skill_id = payload.skill_id
    skill = SKILLS_BY_ID.get(skill_id)
    if not skill:
        raise HTTPException(status_code=400, detail="Unknown skill")
    if any(s.get("skill_id") == skill_id for s in ch.get("skills", [])):
        raise HTTPException(status_code=409, detail="Skill already learned")
    if ch.get("training_skill_id"):
        raise HTTPException(status_code=409, detail="Already training a skill")

    if payload.skillbook_item_id:
        item = ITEMS_BY_ID.get(payload.skillbook_item_id)
        if not item or item.get("kind") != "skillbook" or item.get("teaches") != skill_id:
            raise HTTPException(status_code=400, detail="Invalid skillbook for this skill")
        if not _remove_item_from_inventory(ch, payload.skillbook_item_id, 1):
            raise HTTPException(status_code=400, detail="Skillbook not in inventory")
        ch.setdefault("skills", []).append({"skill_id": skill_id, "cooldown_remaining": 0})
        await db.characters.update_one({"_id": ObjectId(ch["id"])}, {"$set": {
            "skills": ch["skills"], "inventory": ch["inventory"],
        }})
        return {"character": ch, "learned": skill_id}

    if not payload.teacher_id:
        raise HTTPException(status_code=400, detail="Provide either teacher_id or skillbook_item_id")

    teacher = TEACHERS_BY_ID.get(payload.teacher_id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Unknown teacher")
    t_town = teacher.get("town_id")
    if t_town and ch.get("current_town") != t_town:
        raise HTTPException(status_code=403, detail=f"Visit {teacher['name']} in {t_town.replace('_', ' ').title()} to learn this skill")
    offer_ids = {o["skill_id"] if isinstance(o, dict) else o for o in teacher.get("teaches", [])}
    if skill_id not in offer_ids:
        raise HTTPException(status_code=400, detail="This teacher does not teach that skill")
    if ch["level"] < skill.get("level_req", 1):
        raise HTTPException(status_code=403, detail=f"Requires level {skill['level_req']}")
    mastery_req = skill.get("mastery_req") or []
    if mastery_req and not any(m in (ch.get("masteries") or []) for m in mastery_req):
        raise HTTPException(status_code=403, detail="Requires mastery: " + ", ".join(mastery_req))
    quest_req = skill.get("quest_req")
    if quest_req and quest_req not in (ch.get("completed_quests") or []):
        raise HTTPException(status_code=403, detail=f"Requires quest: {quest_req}")
    cost = skill.get("cost_gold", 0)
    if ch["gold"] < cost:
        raise HTTPException(status_code=400, detail="Not enough gold")

    ch["gold"] -= cost
    learn_seconds = max(1, skill.get("learn_seconds", 10))
    # Rogue: Quick Learner (L20) — 25% faster training
    if "rogue" in (ch.get("masteries") or []) and ch.get("level", 1) >= 20:
        learn_seconds = max(1, int(learn_seconds * 0.75))
    until = (datetime.now(timezone.utc) + timedelta(seconds=learn_seconds)).isoformat()
    ch["training_skill_id"] = skill_id
    ch["training_until"] = until
    await db.characters.update_one({"_id": ObjectId(ch["id"])}, {"$set": {
        "gold": ch["gold"], "training_skill_id": skill_id, "training_until": until,
    }})
    return {"character": ch, "started": skill_id, "seconds": learn_seconds}


@api.post("/game/skill/finish_learn")
async def finish_learn(user: dict = Depends(_get_current_user)):
    ch = await _get_character_or_404(user["_id"])
    training_id = ch.get("training_skill_id")
    if not training_id:
        raise HTTPException(status_code=400, detail="Not training anything")
    until = ch.get("training_until")
    if until and datetime.now(timezone.utc).timestamp() < datetime.fromisoformat(until).timestamp():
        raise HTTPException(status_code=403, detail="Training not finished yet")
    if not any(s.get("skill_id") == training_id for s in ch.get("skills", [])):
        ch.setdefault("skills", []).append({"skill_id": training_id, "cooldown_remaining": 0})
    ch["training_skill_id"] = None
    ch["training_until"] = None
    await db.characters.update_one({"_id": ObjectId(ch["id"])}, {"$set": {
        "skills": ch["skills"], "training_skill_id": None, "training_until": None,
    }})
    return {"character": ch, "learned": training_id}


@api.post("/game/skill/assign")
async def assign_skill(request: Request, user: dict = Depends(_get_current_user)):
    body = await request.json()
    slot = body.get("slot")
    skill_id = body.get("skill_id")
    ch = await _get_character_or_404(user["_id"])
    if not isinstance(slot, int) or slot < 0 or slot >= 10:
        raise HTTPException(status_code=400, detail="Invalid skill slot")
    if skill_id not in SKILLS_BY_ID:
        raise HTTPException(status_code=404, detail="Unknown skill")
    if not any(s.get("skill_id") == skill_id for s in ch.get("skills", [])):
        raise HTTPException(status_code=403, detail="Skill not learned")
    bar = ch.setdefault("skill_bar", [None] * 10)
    while len(bar) < 10:
        bar.append(None)
    for i in range(10):
        if bar[i] == skill_id and i != slot:
            bar[i] = None
    bar[slot] = skill_id
    await db.characters.update_one({"_id": ObjectId(ch["id"])}, {"$set": {"skill_bar": bar}})
    return {"character": ch}


@api.post("/game/skill/unassign")
async def unassign_skill(request: Request, user: dict = Depends(_get_current_user)):
    body = await request.json()
    slot = body.get("slot")
    ch = await _get_character_or_404(user["_id"])
    if not isinstance(slot, int) or slot < 0 or slot >= 10:
        raise HTTPException(status_code=400, detail="Invalid skill slot")
    bar = ch.setdefault("skill_bar", [None] * 10)
    while len(bar) < 10:
        bar.append(None)
    bar[slot] = None
    await db.characters.update_one({"_id": ObjectId(ch["id"])}, {"$set": {"skill_bar": bar}})
    return {"character": ch}


@api.post("/game/rogue/innate/equip")
async def equip_rogue_innate(request: Request, user: dict = Depends(_get_current_user)):
    """Equip a Rogue innate skill to a slot (max 5 slots, +1 at level 10/100)."""
    body = await request.json()
    innate_id = body.get("innate_id")
    slot = body.get("slot")
    ch = await _get_character_or_404(user["_id"])
    if ch.get("mastery") != "rogue" and "rogue" not in (ch.get("masteries") or []):
        raise HTTPException(status_code=403, detail="Rogue mastery required")
    valid_ids = {s["id"] for s in ROGUE_INNATE_SKILLS}
    if innate_id not in valid_ids:
        raise HTTPException(status_code=404, detail="Unknown innate skill")
    from game_engine import _rogue_get_innate_slots
    max_slots = _rogue_get_innate_slots(ch)
    if not isinstance(slot, int) or slot < 0 or slot >= max_slots:
        raise HTTPException(status_code=400, detail=f"Invalid slot (0-{max_slots - 1})")
    equipped = ch.setdefault("rogue_innate_equipped", [])
    while len(equipped) < max_slots:
        equipped.append(None)
    # Remove from any other slot
    for i in range(len(equipped)):
        if equipped[i] == innate_id and i != slot:
            equipped[i] = None
    equipped[slot] = innate_id
    await db.characters.update_one({"_id": ObjectId(ch["id"])}, {"$set": {"rogue_innate_equipped": equipped}})
    return {"character": ch, "rogue_innate_skills": ROGUE_INNATE_SKILLS, "rogue_passives": ROGUE_PASSIVES}


@api.post("/game/rogue/innate/unequip")
async def unequip_rogue_innate(request: Request, user: dict = Depends(_get_current_user)):
    """Unequip a Rogue innate skill from a slot."""
    body = await request.json()
    slot = body.get("slot")
    ch = await _get_character_or_404(user["_id"])
    if ch.get("mastery") != "rogue" and "rogue" not in (ch.get("masteries") or []):
        raise HTTPException(status_code=403, detail="Rogue mastery required")
    from game_engine import _rogue_get_innate_slots
    max_slots = _rogue_get_innate_slots(ch)
    if not isinstance(slot, int) or slot < 0 or slot >= max_slots:
        raise HTTPException(status_code=400, detail=f"Invalid slot (0-{max_slots - 1})")
    equipped = ch.setdefault("rogue_innate_equipped", [])
    while len(equipped) < max_slots:
        equipped.append(None)
    equipped[slot] = None
    await db.characters.update_one({"_id": ObjectId(ch["id"])}, {"$set": {"rogue_innate_equipped": equipped}})
    return {"character": ch}


@api.get("/game/rogue/innate")
async def get_rogue_innates(request: Request, user: dict = Depends(_get_current_user)):
    """Get Rogue innate skills, passives, and currently equipped loadout."""
    ch = await _get_character_or_404(user["_id"])
    from game_engine import _rogue_get_innate_slots
    max_slots = _rogue_get_innate_slots(ch)
    return {
        "innate_skills": ROGUE_INNATE_SKILLS,
        "passives": ROGUE_PASSIVES,
        "equipped": ch.get("rogue_innate_equipped", []),
        "max_slots": max_slots,
    }


@api.post("/game/rogue/innate/swap")
async def swap_rogue_innate_combat(request: Request, user: dict = Depends(_get_current_user)):
    """Swap an innate skill mid-combat (Adaptive passive, L30+, once per fight)."""
    body = await request.json()
    combat_id = body.get("combat_id")
    innate_id = body.get("innate_id")
    slot = body.get("slot")
    ch = await _get_character_or_404(user["_id"])
    if "rogue" not in (ch.get("masteries") or []):
        raise HTTPException(status_code=403, detail="Rogue mastery required")
    if ch.get("level", 1) < 30:
        raise HTTPException(status_code=403, detail="Adaptive passive requires level 30")
    valid_innates = {s["id"] for s in ROGUE_INNATE_SKILLS}
    if innate_id not in valid_innates:
        raise HTTPException(status_code=400, detail="Invalid innate skill")
    from game_engine import _rogue_get_innate_slots
    max_slots = _rogue_get_innate_slots(ch)
    if not isinstance(slot, int) or slot < 0 or slot >= max_slots:
        raise HTTPException(status_code=400, detail=f"Invalid slot (0-{max_slots - 1})")
    combat = await db.combats.find_one({"_id": ObjectId(combat_id), "user_id": user["_id"]})
    if not combat:
        raise HTTPException(status_code=404, detail="Combat not found")
    state = combat["state"]
    if not state.get("active"):
        raise HTTPException(status_code=400, detail="Combat is not active")
    if state.get("rogue_adaptive_used"):
        raise HTTPException(status_code=400, detail="Adaptive already used this fight")
    equipped = ch.setdefault("rogue_innate_equipped", [])
    while len(equipped) < max_slots:
        equipped.append(None)
    # Remove innate from any other slot
    for i in range(len(equipped)):
        if equipped[i] == innate_id and i != slot:
            equipped[i] = None
    equipped[slot] = innate_id
    state["rogue_adaptive_used"] = True
    await db.characters.update_one({"_id": ObjectId(ch["id"])}, {"$set": {"rogue_innate_equipped": equipped}})
    await db.combats.update_one({"_id": ObjectId(combat_id)}, {"$set": {"state": state}})
    return {"character": ch, "state": state, "swapped": innate_id}


# ---------------- KNIGHT ----------------
@api.post("/game/knight/oath")
async def knight_select_oath(request: Request, user: dict = Depends(_get_current_user)):
    """Select a Knight Oath during combat."""
    body = await request.json()
    combat_id = body.get("combat_id")
    oath_id = body.get("oath")
    valid_oaths = ("iron", "wrath", "bulwark", "endurance", "vanguard")
    if oath_id not in valid_oaths:
        raise HTTPException(status_code=400, detail=f"Oath must be one of {valid_oaths}")
    ch = await _get_character_or_404(user["_id"])
    if ch.get("mastery") != "knight" and "knight" not in (ch.get("masteries") or []):
        raise HTTPException(status_code=403, detail="Knight mastery required")
    combat = await db.combats.find_one({"_id": ObjectId(combat_id), "user_id": user["_id"]})
    if not combat:
        raise HTTPException(status_code=404, detail="Combat not found")
    state = combat["state"]
    if not state.get("active"):
        raise HTTPException(status_code=400, detail="Combat is not active")
    if state.get("knight_oath"):
        # Oath switching: allowed but resets stacks (Second Wind L90 / Eternal Oath L100 saves 3)
        old_oath = state["knight_oath"]
        if old_oath == oath_id:
            raise HTTPException(status_code=400, detail="That Oath is already active")
        # Determine saved stacks
        saved = 0
        if ch.get("level", 1) >= 90:  # Second Wind
            saved = 3
        if ch.get("level", 1) >= 100:  # Eternal Oath also saves 3
            saved = 3
        state["knight_oath"] = oath_id
        state["knight_oath_stacks"] = saved
        if saved > 0:
            log_msg = f"Oath switched to {oath_id} — {saved} stacks preserved!"
        else:
            log_msg = f"Oath switched to {oath_id} — stacks reset to 0!"
        await db.combats.update_one({"_id": ObjectId(combat_id)}, {"$set": {"state": state}})
        return {"state": state, "oath": oath_id, "switched": True, "message": log_msg}
    state["knight_oath"] = oath_id
    # Oath Sworn (level 10): start with 2 stacks
    if ch.get("level", 1) >= 10:
        state["knight_oath_stacks"] = 2
    await db.combats.update_one({"_id": ObjectId(combat_id)}, {"$set": {"state": state}})
    return {"state": state, "oath": oath_id}


@api.get("/game/knight/passives")
async def get_knight_passives(user: dict = Depends(_get_current_user)):
    """Get Knight passives list."""
    ch = await _get_character_or_404(user["_id"])
    return {
        "passives": KNIGHT_PASSIVES,
    }


# ---------------- LANCER ----------------
@api.get("/game/lancer/passives")
async def get_lancer_passives(user: dict = Depends(_get_current_user)):
    """Get Lancer passives list."""
    ch = await _get_character_or_404(user["_id"])
    return {
        "passives": LANCER_PASSIVES,
    }


@api.post("/game/lancer/overload")
async def lancer_activate_overload(request: Request, user: dict = Depends(_get_current_user)):
    """Activate Elemental Overload (L90 passive) — all 6 elements for 2 turns."""
    body = await request.json()
    combat_id = body.get("combat_id")
    ch = await _get_character_or_404(user["_id"])
    if ch.get("mastery") != "lancer" and "lancer" not in (ch.get("masteries") or []):
        raise HTTPException(status_code=403, detail="Lancer mastery required")
    if ch.get("level", 1) < 90:
        raise HTTPException(status_code=403, detail="Elemental Overload requires level 90")
    combat = await db.combats.find_one({"_id": ObjectId(combat_id), "user_id": user["_id"]})
    if not combat:
        raise HTTPException(status_code=404, detail="Combat not found")
    state = combat["state"]
    if not state.get("active"):
        raise HTTPException(status_code=400, detail="Combat is not active")
    if state.get("lancer_overload_charges", 0) <= 0:
        raise HTTPException(status_code=400, detail="No Elemental Overload charges remaining")
    # Activate all 6 elements
    state["lancer_overload_used"] = True
    state["lancer_overload_charges"] = max(0, state.get("lancer_overload_charges", 1) - 1)
    state["lancer_overload_turns"] = 2
    for elem_id in ("fire", "ice", "lightning", "earth", "wind", "thunder"):
        state.setdefault("lancer_active_imbues", {})[elem_id] = {
            "skill_id": f"overload_{elem_id}",
            "duration": 2,
            "stat_mods": {},
        }
    await db.combats.update_one({"_id": ObjectId(combat_id)}, {"$set": {"state": state}})
    return {"state": state, "message": "Elemental Overload activated — all 6 elements for 2 turns!"}


# ---------------- MAGE ----------------
@api.get("/game/mage/passives")
async def get_mage_passives(user: dict = Depends(_get_current_user)):
    """Get Mage Arcane Library passives list (50 passives across 5 schools)."""
    ch = await _get_character_or_404(user["_id"])
    return {
        "passives": MAGE_PASSIVES,
        "equipped": ch.get("mage_equipped_passives", []),
        "researched": ch.get("mage_researched_passives", []),
        "loadouts": ch.get("mage_loadouts", {}),
    }


@api.post("/game/mage/library/equip")
async def mage_equip_passive(request: Request, user: dict = Depends(_get_current_user)):
    """Equip an Arcane Library passive to a slot."""
    body = await request.json()
    passive_id = body.get("passive_id")
    slot = body.get("slot")  # 0-4
    ch = await _get_character_or_404(user["_id"])
    if "mage" not in (ch.get("masteries") or []):
        raise HTTPException(status_code=403, detail="Mage mastery required")
    if slot is None or slot < 0 or slot > 4:
        raise HTTPException(status_code=400, detail="Slot must be 0-4")
    # Check slot unlock level
    slot_levels = [10, 20, 30, 40, 50]
    if ch.get("level", 1) < slot_levels[slot]:
        raise HTTPException(status_code=403, detail=f"Slot {slot} unlocks at level {slot_levels[slot]}")
    # Check passive exists
    passive_ids = {p["id"] for p in MAGE_PASSIVES}
    if passive_id not in passive_ids:
        raise HTTPException(status_code=400, detail="Invalid passive ID")
    # Check research
    researched = ch.get("mage_researched_passives", [])
    if passive_id not in researched:
        raise HTTPException(status_code=403, detail="Passive not yet researched")
    # Equip
    equipped = ch.get("mage_equipped_passives", [])
    # Ensure list has 5 slots
    while len(equipped) < 5:
        equipped.append(None)
    # Check if passive is already equipped in another slot
    for i, pid in enumerate(equipped):
        if pid == passive_id and i != slot:
            raise HTTPException(status_code=400, detail="Passive already equipped in another slot")
    equipped[slot] = passive_id
    update = {f"mage_equipped_passives": equipped}
    await db.characters.update_one({"_id": ch["_id"]}, {"$set": update})
    return {"equipped": equipped, "message": f"Equipped {passive_id} to slot {slot}"}


@api.post("/game/mage/library/unequip")
async def mage_unequip_passive(request: Request, user: dict = Depends(_get_current_user)):
    """Unequip an Arcane Library passive from a slot."""
    body = await request.json()
    slot = body.get("slot")
    ch = await _get_character_or_404(user["_id"])
    if "mage" not in (ch.get("masteries") or []):
        raise HTTPException(status_code=403, detail="Mage mastery required")
    if slot is None or slot < 0 or slot > 4:
        raise HTTPException(status_code=400, detail="Slot must be 0-4")
    equipped = ch.get("mage_equipped_passives", [])
    while len(equipped) < 5:
        equipped.append(None)
    equipped[slot] = None
    await db.characters.update_one({"_id": ch["_id"]}, {"$set": {"mage_equipped_passives": equipped}})
    return {"equipped": equipped, "message": f"Unequipped slot {slot}"}


@api.post("/game/mage/research")
async def mage_research_passive(request: Request, user: dict = Depends(_get_current_user)):
    """Mark a passive as researched (unlocked). Called when the research requirement is met."""
    body = await request.json()
    passive_id = body.get("passive_id")
    ch = await _get_character_or_404(user["_id"])
    if "mage" not in (ch.get("masteries") or []):
        raise HTTPException(status_code=403, detail="Mage mastery required")
    passive_ids = {p["id"] for p in MAGE_PASSIVES}
    if passive_id not in passive_ids:
        raise HTTPException(status_code=400, detail="Invalid passive ID")
    researched = ch.get("mage_researched_passives", [])
    if passive_id not in researched:
        researched.append(passive_id)
        await db.characters.update_one({"_id": ch["_id"]}, {"$set": {"mage_researched_passives": researched}})
    return {"researched": researched, "message": f"Researched {passive_id}"}


@api.get("/game/mage/library")
async def mage_get_library(user: dict = Depends(_get_current_user)):
    """Get the Mage's Arcane Library state: equipped passives, researched passives, school synergy."""
    ch = await _get_character_or_404(user["_id"])
    equipped = ch.get("mage_equipped_passives", [])
    researched = ch.get("mage_researched_passives", [])
    # Compute school synergy
    passive_map = {p["id"]: p for p in MAGE_PASSIVES}
    school_counts: dict[str, int] = {}
    for pid in equipped:
        if pid and pid in passive_map:
            school = passive_map[pid].get("school", "")
            school_counts[school] = school_counts.get(school, 0) + 1
    synergy = {}
    for school, count in school_counts.items():
        if count >= 5:
            synergy[school] = 5
        elif count >= 3:
            synergy[school] = 3
    # Slot unlock levels
    slot_levels = [10, 20, 30, 40, 50]
    available_slots = sum(1 for lv in slot_levels if ch.get("level", 1) >= lv)
    return {
        "equipped": equipped,
        "researched": researched,
        "synergy": synergy,
        "available_slots": available_slots,
        "all_passives": MAGE_PASSIVES,
    }


@api.post("/game/mage/loadouts/save")
async def mage_save_loadout(request: Request, user: dict = Depends(_get_current_user)):
    """Save current equipped passives as a named loadout."""
    body = await request.json()
    name = body.get("name", "").strip()
    if not name or len(name) > 30:
        raise HTTPException(status_code=400, detail="Loadout name required (max 30 chars)")
    ch = await _get_character_or_404(user["_id"])
    if "mage" not in (ch.get("masteries") or []):
        raise HTTPException(status_code=403, detail="Mage mastery required")
    loadouts = ch.get("mage_loadouts", {})
    equipped = ch.get("mage_equipped_passives", [])
    loadouts[name] = list(equipped)
    await db.characters.update_one({"_id": ch["_id"]}, {"$set": {"mage_loadouts": loadouts}})
    return {"loadouts": loadouts, "message": f"Loadout '{name}' saved"}


@api.post("/game/mage/loadouts/load")
async def mage_load_loadout(request: Request, user: dict = Depends(_get_current_user)):
    """Load a named loadout."""
    body = await request.json()
    name = body.get("name", "").strip()
    ch = await _get_character_or_404(user["_id"])
    if "mage" not in (ch.get("masteries") or []):
        raise HTTPException(status_code=403, detail="Mage mastery required")
    loadouts = ch.get("mage_loadouts", {})
    if name not in loadouts:
        raise HTTPException(status_code=404, detail="Loadout not found")
    equipped = loadouts[name]
    await db.characters.update_one({"_id": ch["_id"]}, {"$set": {"mage_equipped_passives": equipped}})
    return {"equipped": equipped, "message": f"Loadout '{name}' loaded"}


@api.get("/game/mage/loadouts")
async def mage_list_loadouts(user: dict = Depends(_get_current_user)):
    """List all saved Mage loadouts."""
    ch = await _get_character_or_404(user["_id"])
    return {"loadouts": ch.get("mage_loadouts", {})}


# ---------------- PALADIN ----------------
@api.get("/game/paladin/passives")
async def get_paladin_passives(user: dict = Depends(_get_current_user)):
    """Get Paladin passives list."""
    ch = await _get_character_or_404(user["_id"])
    return {
        "passives": PALADIN_PASSIVES,
    }


# ---------------- ASSASSIN ----------------
@api.get("/game/assassin/passives")
async def get_assassin_passives(user: dict = Depends(_get_current_user)):
    """Get Assassin passives list."""
    ch = await _get_character_or_404(user["_id"])
    return {
        "passives": ASSASSIN_PASSIVES,
    }


# ---------------- BARD ----------------
@api.get("/game/bard/passives")
async def get_bard_passives(user: dict = Depends(_get_current_user)):
    """Get Bard passives list."""
    ch = await _get_character_or_404(user["_id"])
    return {
        "passives": BARD_PASSIVES,
        "quest_passives": ch.get("quest_passives", []),
    }


# ---------------- HUNTER ----------------
@api.get("/game/hunter/passives")
async def get_hunter_passives(user: dict = Depends(_get_current_user)):
    """Get Hunter passives list."""
    ch = await _get_character_or_404(user["_id"])
    return {
        "passives": HUNTER_PASSIVES,
        "quest_passives": ch.get("quest_passives", []),
    }


@api.post("/game/bard/mode-switch")
async def bard_switch_mode(request: Request, user: dict = Depends(_get_current_user)):
    """Switch Bard performance mode (song/dance) during combat."""
    body = await request.json()
    combat_id = body.get("combat_id")
    new_mode = body.get("mode")
    if new_mode not in ("song", "dance"):
        raise HTTPException(status_code=400, detail="Mode must be 'song' or 'dance'")
    ch = await _get_character_or_404(user["_id"])
    if ch.get("mastery") != "bard" and "bard" not in (ch.get("masteries") or []):
        raise HTTPException(status_code=403, detail="Bard mastery required")
    combat = await db.combats.find_one({"_id": ObjectId(combat_id), "user_id": user["_id"]})
    if not combat:
        raise HTTPException(status_code=404, detail="Combat not found")
    state = combat["state"]
    if not state.get("active"):
        raise HTTPException(status_code=400, detail="Combat is not active")
    from game_engine import _bard_switch_mode
    log: list[dict] = []
    success = _bard_switch_mode(state, ch, new_mode, log)
    if not success:
        raise HTTPException(status_code=400, detail=f"Already in {new_mode} mode or invalid mode")
    await db.combats.update_one({"_id": ObjectId(combat_id)}, {"$set": {"state": state}})
    return {"state": state, "log": log, "mode": state.get("bard_mode", "song")}


@api.post("/game/item/assign")
async def assign_item(request: Request, user: dict = Depends(_get_current_user)):
    body = await request.json()
    slot = body.get("slot")
    item_id = body.get("item_id")
    ch = await _get_character_or_404(user["_id"])
    if not isinstance(slot, int) or slot < 0 or slot >= 5:
        raise HTTPException(status_code=400, detail="Invalid item hotbar slot")
    if item_id is not None:
        item = ITEMS_BY_ID.get(item_id)
        if not item or item.get("kind") != "consumable":
            raise HTTPException(status_code=400, detail="Only consumables can go on the item hotbar")
        if not any(inv.get("item_id") == item_id and inv.get("quantity", 0) > 0 for inv in ch.get("inventory", [])):
            raise HTTPException(status_code=400, detail="Item not in inventory")
    bar = ch.setdefault("item_bar", [None] * 5)
    while len(bar) < 5:
        bar.append(None)
    for i in range(5):
        if bar[i] == item_id and i != slot:
            bar[i] = None
    bar[slot] = item_id
    await db.characters.update_one({"_id": ObjectId(ch["id"])}, {"$set": {"item_bar": bar}})
    return {"character": ch}


@api.post("/game/item/unassign")
async def unassign_item(request: Request, user: dict = Depends(_get_current_user)):
    body = await request.json()
    slot = body.get("slot")
    ch = await _get_character_or_404(user["_id"])
    if not isinstance(slot, int) or slot < 0 or slot >= 5:
        raise HTTPException(status_code=400, detail="Invalid item hotbar slot")
    bar = ch.setdefault("item_bar", [None] * 5)
    while len(bar) < 5:
        bar.append(None)
    bar[slot] = None
    await db.characters.update_one({"_id": ObjectId(ch["id"])}, {"$set": {"item_bar": bar}})
    return {"character": ch}


# ---------------- INVENTORY ----------------
@api.post("/game/equip")
async def equip(request: Request, user: dict = Depends(_get_current_user)):
    body = await request.json()
    item_id = body.get("item_id")
    slot = body.get("slot")
    if slot not in EQUIP_SLOTS:
        raise HTTPException(status_code=400, detail="Invalid slot")
    ch = await _get_character_or_404(user["_id"])
    # Try static items first
    item = ITEMS_BY_ID.get(item_id)
    # Try item instances (new procedural system)
    item_instance = None
    if not item:
        for inst in ch.get("item_instances", []):
            if isinstance(inst, dict) and inst.get("instance_id") == item_id:
                item_instance = inst
                break
        if item_instance:
            item = item_instance
    if not item:
        raise HTTPException(status_code=400, detail="Unknown item")
    # Validate item can go in requested slot
    item_slot = item.get("slot")
    is_shield = item.get("is_shield", False) or item.get("weapon_type") == "shield"
    is_two_handed = item.get("two_handed", False) or item.get("two_handed", False)
    # Rings and earrings can go in either left or right slot
    if item_slot in ("ring_l",):
        if slot not in ("ring_l", "ring_r"):
            raise HTTPException(status_code=400, detail=f"Item is not a ring")
    elif item_slot in ("earring_l",):
        if slot not in ("earring_l", "earring_r"):
            raise HTTPException(status_code=400, detail=f"Item is not an earring")
    elif item_slot in ("left_hand", "right_hand"):
        # Weapons/shields/tools can go in either hand
        if slot not in ("left_hand", "right_hand"):
            # Shields can also go on back
            if is_shield and slot == "back":
                pass
            else:
                raise HTTPException(status_code=400, detail=f"Item must go in a hand slot")
    elif item_slot != slot:
        raise HTTPException(status_code=400, detail=f"Item is not for {SLOT_LABELS.get(slot, slot)}")
    # Check stat requirements for new-style items
    if item_instance and item_instance.get("req_stats"):
        char_stats = ch.get("base_stats") or ch.get("stats", {})
        for stat, req_val in item_instance["req_stats"].items():
            if int(char_stats.get(stat, 0)) < int(req_val):
                raise HTTPException(status_code=400, detail=f"Requires {stat} >= {req_val}")
    if not any(i.get("item_id") == item_id for i in ch.get("inventory", [])):
        raise HTTPException(status_code=400, detail="Item not in inventory")
    equipped = ch["equipped"]
    # Handle two-handed weapons: equipping fills both hands
    if item.get("two_handed"):
        equipped["left_hand"] = item_id
        equipped["right_hand"] = item_id
    else:
        equipped[slot] = item_id
        # If equipping 1H to a slot that currently holds a 2H weapon, clear the other hand
        other_hand = "left_hand" if slot == "right_hand" else "right_hand" if slot == "left_hand" else None
        if other_hand:
            other_item_id = equipped.get(other_hand)
            if other_item_id:
                other_item = ITEMS_BY_ID.get(other_item_id)
                if not other_item:
                    for inst in ch.get("item_instances", []):
                        if isinstance(inst, dict) and inst.get("instance_id") == other_item_id:
                            other_item = inst
                            break
                if other_item and other_item.get("two_handed"):
                    equipped[other_hand] = None
    _recompute_stats(ch)
    ch["weapon_range"] = _get_weapon_range_for_combat(ch)
    _equip_updates = {"equipped": ch["equipped"], "stats": ch["stats"], "weapon_range": ch["weapon_range"]}
    if ch.get("paladin_faith_tier") is not None:
        _equip_updates["paladin_faith_tier"] = ch["paladin_faith_tier"]
        _equip_updates["paladin_faith_bonuses"] = ch["paladin_faith_bonuses"]
    await db.characters.update_one({"_id": ObjectId(ch["id"])}, {"$set": _equip_updates})
    return {"character": ch}


@api.post("/game/unequip")
async def unequip(request: Request, user: dict = Depends(_get_current_user)):
    body = await request.json()
    slot = body.get("slot")
    if slot not in EQUIP_SLOTS:
        raise HTTPException(status_code=400, detail="Invalid slot")
    ch = await _get_character_or_404(user["_id"])
    equipped = ch["equipped"]
    item_id = equipped.get(slot)
    if not item_id:
        raise HTTPException(status_code=400, detail="Nothing equipped in that slot")
    # Check if it's a 2H weapon occupying both hands
    item = ITEMS_BY_ID.get(item_id)
    if item and item.get("two_handed"):
        equipped["left_hand"] = None
        equipped["right_hand"] = None
    else:
        equipped[slot] = None
    _recompute_stats(ch)
    ch["weapon_range"] = _get_weapon_range_for_combat(ch)
    _unequip_updates = {"equipped": ch["equipped"], "stats": ch["stats"], "weapon_range": ch["weapon_range"]}
    if ch.get("paladin_faith_tier") is not None:
        _unequip_updates["paladin_faith_tier"] = ch["paladin_faith_tier"]
        _unequip_updates["paladin_faith_bonuses"] = ch["paladin_faith_bonuses"]
    await db.characters.update_one({"_id": ObjectId(ch["id"])}, {"$set": _unequip_updates})
    return {"character": ch}


@api.post("/game/inventory/favorite")
async def favorite_item(request: Request, user: dict = Depends(_get_current_user)):
    body = await request.json()
    item_id = body.get("item_id")
    favorite = body.get("favorite", True)
    ch = await _get_character_or_404(user["_id"])
    inv = ch.get("inventory", [])
    entry = next((i for i in inv if i.get("item_id") == item_id), None)
    if not entry:
        raise HTTPException(status_code=400, detail="Item not in inventory")
    entry["favorite"] = bool(favorite)
    await db.characters.update_one({"_id": ObjectId(ch["id"])}, {"$set": {"inventory": inv}})
    return {"character": ch}


@api.post("/game/inventory/trash")
async def trash_item(request: Request, user: dict = Depends(_get_current_user)):
    body = await request.json()
    item_id = body.get("item_id")
    qty = max(1, int(body.get("quantity", 1)))
    ch = await _get_character_or_404(user["_id"])
    inv = ch.get("inventory", [])
    idx = next((i for i, it in enumerate(inv) if it.get("item_id") == item_id), -1)
    if idx < 0:
        raise HTTPException(status_code=400, detail="Item not in inventory")
    # Block trashing equipped or favorited items
    if any(ch.get("equipped", {}).get(slot) == item_id for slot in EQUIP_SLOTS):
        raise HTTPException(status_code=400, detail="Cannot trash an equipped item.")
    if inv[idx].get("favorite"):
        raise HTTPException(status_code=400, detail="Cannot trash a favorited item.")
    if inv[idx].get("quantity", 1) <= qty:
        inv.pop(idx)
    else:
        inv[idx]["quantity"] -= qty
    await db.characters.update_one({"_id": ObjectId(ch["id"])}, {"$set": {"inventory": inv}})
    return {"character": ch, "trashed": item_id, "quantity": qty}


@api.post("/game/inventory/use")
async def use_item(request: Request, user: dict = Depends(_get_current_user)):
    body = await request.json()
    item_id = body.get("item_id")
    ch = await _get_character_or_404(user["_id"])
    item = ITEMS_BY_ID.get(item_id)
    if not item:
        raise HTTPException(status_code=400, detail="Unknown item")
    if item.get("kind") != "consumable":
        raise HTTPException(status_code=400, detail="Item is not usable")
    inv = ch.get("inventory", [])
    idx = next((i for i, it in enumerate(inv) if it.get("item_id") == item_id), -1)
    if idx < 0:
        raise HTTPException(status_code=400, detail="Item not in inventory")
    effect = item.get("effect", {})
    message = f"You used {item['name']}."
    if "heal" in effect:
        from game_data import compute_healing
        from world_data import continental_bonus_for
        _hq = continental_bonus_for(ch.get("current_continent", ""), "healing_quality")
        heal = compute_healing(ch, int(int(effect["heal"]) * (float(_hq) if _hq else 1.0)))
        ch["hp"] = min(ch["max_hp"], ch["hp"] + heal)
        message = f"You recovered {heal} HP."
    elif "cure" in effect:
        status = effect["cure"]
        ch["statuses"] = [s for s in ch.get("statuses", []) if s.get("id") != status]
        message = f"You cured {status}."
    else:
        message = f"You used {item['name']}, but nothing happened."
    if inv[idx].get("quantity", 1) <= 1:
        inv.pop(idx)
    else:
        inv[idx]["quantity"] -= 1
    await db.characters.update_one({"_id": ObjectId(ch["id"])}, {"$set": {
        "inventory": inv, "hp": ch["hp"], "statuses": ch.get("statuses", [])
    }})
    return {"character": ch, "message": message}


# ---------------- DAILY ----------------
@api.post("/game/daily/claim")
async def claim_daily(request: Request, user: dict = Depends(_get_current_user)):
    body = await request.json()
    mission_id = body.get("mission_id")
    ch = await _get_character_or_404(user["_id"])
    mission = next((m for m in ch.get("daily_missions", []) if m.get("id") == mission_id), None)
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    if not mission.get("complete"):
        raise HTTPException(status_code=400, detail="Mission not yet complete")
    if mission.get("claimed"):
        raise HTTPException(status_code=400, detail="Already claimed")
    mission["claimed"] = True
    reward = {"gold": mission["reward"].get("gold", 0), "xp": mission["reward"].get("xp", 0), "items": []}
    _apply_rewards_to_character(ch, reward, reduce=False)
    await db.characters.update_one({"_id": ObjectId(ch["id"])}, {"$set": {
        "daily_missions": ch["daily_missions"], "gold": ch["gold"], "xp": ch["xp"],
        "level": ch["level"], "base_stats": ch.get("base_stats", ch["stats"]), "stats": ch["stats"], "max_hp": ch["max_hp"],
    }})
    return {"character": ch, "reward": reward}


# ---------------- LEADERBOARD / EVENTS ----------------
@api.get("/game/leaderboard")
async def leaderboard(user: dict = Depends(_get_current_user)):
    cursor = db.characters.find({}, {
        "name": 1, "level": 1, "xp": 1, "gold": 1, "kills": 1, "crafts": 1,
        "race": 1, "role": 1, "mastery": 1
    }).sort([("level", -1), ("xp", -1)]).limit(50)
    rows = []
    async for doc in cursor:
        rows.append({
            "id": str(doc["_id"]),
            "name": doc.get("name", ""),
            "level": doc.get("level", 1),
            "xp": doc.get("xp", 0),
            "gold": doc.get("gold", 0),
            "kills": doc.get("kills", 0),
            "crafts": doc.get("crafts", 0),
            "race": doc.get("race", ""),
            "role": doc.get("role", ""),
            "mastery": doc.get("mastery", ""),
        })
    return {"rows": rows}


@api.get("/game/events")
async def world_events(user: dict = Depends(_get_current_user)):
    cursor = db.world_events.find({}).sort("created_at", -1).limit(30)
    rows = []
    async for doc in cursor:
        doc["id"] = str(doc["_id"])
        doc.pop("_id", None)
        rows.append(doc)
    return {"events": rows}


# ---------------- QUEST HELPERS ----------------
def _update_quest_progress(character: dict, event: dict) -> None:
    """Advance progress on any active quest matching the event."""
    for aq in character.get("active_quests", []):
        if aq.get("complete"):
            continue
        q = QUESTS_BY_ID.get(aq["quest_id"]) or EVENTS_BY_ID.get(aq["quest_id"])
        if not q:
            continue
        objs = q.get("objectives", [])
        progress_list = aq.setdefault("progress", [0] * len(objs))
        while len(progress_list) < len(objs):
            progress_list.append(0)
        for idx, obj in enumerate(objs):
            match = False
            if obj.get("kind") == event.get("kind"):
                if "id" in obj and obj.get("id") == event.get("id"):
                    match = True
                elif "id" not in obj:
                    match = True
            if match:
                progress_list[idx] += int(event.get("count", 1))
        # check overall completion
        if all(progress_list[i] >= obj.get("count", 1) for i, obj in enumerate(objs)):
            aq["complete"] = True


# ---------------- PHASE 2 STATIC DATA ROUTES ----------------
@api.get("/game/data/regions")
async def get_regions(user: dict = Depends(_get_current_user)):
    return {"regions": REGIONS}


@api.get("/game/data/towns")
async def get_towns(user: dict = Depends(_get_current_user)):
    return {"towns": TOWNS}


@api.get("/game/data/beast_aspects")
async def get_beast_aspects(user: dict = Depends(_get_current_user)):
    return {"beast_aspects": BEAST_ASPECTS}


@api.get("/game/data/marine_adaptations")
async def get_marine_adaptations(user: dict = Depends(_get_current_user)):
    return {"marine_adaptations": MARINE_ADAPTATIONS}


@api.get("/game/data/heritage")
async def get_heritage(user: dict = Depends(_get_current_user)):
    from game_data_p2 import HERITAGE_SURGES, HERITAGE_SURGE_RANK_CONFIG, HERITAGE_RANK_LEVEL_REQS, HERITAGE_RANK_MULT
    return {
        "heritage_rank_1": HERITAGE_RANK_1,
        "surges": HERITAGE_SURGES,
        "surge_rank_config": HERITAGE_SURGE_RANK_CONFIG,
        "rank_level_reqs": HERITAGE_RANK_LEVEL_REQS,
        "rank_mult": HERITAGE_RANK_MULT,
    }


@api.post("/game/heritage/rankup")
async def heritage_rankup(user: dict = Depends(_get_current_user)):
    from racial import apply_rank_up
    ch = await _get_character_or_404(user["_id"])
    ok, msg = apply_rank_up(ch)
    if not ok:
        raise HTTPException(status_code=400, detail=msg)
    from racial import _RACE_TO_RESOURCE
    resource_key = _RACE_TO_RESOURCE.get(ch.get("race"))
    update_fields = {
        "heritage_rank": ch["heritage_rank"],
    }
    if resource_key:
        update_fields[resource_key] = ch.get(resource_key, 0)
    await db.characters.update_one({"_id": ObjectId(ch["id"])}, {"$set": update_fields})
    return {"character": ch, "message": msg}


@api.get("/game/heritage/info")
async def heritage_info(user: dict = Depends(_get_current_user)):
    from racial import can_rank_up, can_activate_surge, get_active_surge_info, _RACE_TO_RESOURCE
    from game_data_p2 import HERITAGE_RANK_LEVEL_REQS, HERITAGE_RANK_MULT, HERITAGE_SURGES, HERITAGE_SURGE_RANK_CONFIG, HERITAGE_RANK_1
    ch = await _get_character_or_404(user["_id"])
    rank = ch.get("heritage_rank", 1)
    level = ch.get("level", 1)

    race = ch.get("race")
    resource_key = _RACE_TO_RESOURCE.get(race)
    meta = HERITAGE_RANK_1.get(race, {})
    max_val = meta.get("resource_max", 1)
    current = ch.get(resource_key, 0) if resource_key else 0
    resource_full = current >= max_val

    rankup_ok, rankup_reason, rankup_info = can_rank_up(ch)
    surge_ok, surge_reason, surge_info = can_activate_surge(ch)
    active_surge = get_active_surge_info(ch)

    next_rank = rank + 1 if rank < 5 else None
    next_level_req = HERITAGE_RANK_LEVEL_REQS[rank - 1] if next_rank else None
    surge = HERITAGE_SURGES.get(race, {})

    surge_config = None
    if rank >= 2:
        idx = min(rank - 2, len(HERITAGE_SURGE_RANK_CONFIG) - 1)
        surge_config = HERITAGE_SURGE_RANK_CONFIG[idx]

    return {
        "heritage_rank": rank,
        "level": level,
        "resource_key": resource_key,
        "resource_current": current,
        "resource_max": max_val,
        "resource_full": resource_full,
        "can_rank_up": rankup_ok,
        "rankup_reason": rankup_reason,
        "next_rank": next_rank,
        "next_level_req": next_level_req,
        "surge": surge,
        "surge_config": surge_config,
        "can_activate_surge": surge_ok,
        "surge_reason": surge_reason,
        "active_surge": active_surge,
        "passive_mult": HERITAGE_RANK_MULT[rank - 1],
        "max_rank": 5,
    }


@api.get("/game/data/quests")
async def get_all_quests(user: dict = Depends(_get_current_user)):
    return {"quests": QUESTS}


@api.get("/game/world/time")
async def world_time(user: dict = Depends(_get_current_user)):
    return {"time_of_day": current_time_of_day(),
            "hour": datetime.now(timezone.utc).hour,
            "weekday": datetime.now(timezone.utc).weekday()}


# ---------------- ANNOUNCEMENTS ----------------
@api.get("/game/announcements")
async def announcements(user: dict = Depends(_get_current_user)):
    cursor = db.announcements.find({}).sort("created_at", -1).limit(20)
    dyn = []
    async for doc in cursor:
        doc["id"] = str(doc["_id"])
        doc.pop("_id", None)
        dyn.append(doc)
    return {"announcements": STATIC_ANNOUNCEMENTS + dyn}


# ---------------- QUESTS ----------------
@api.get("/game/quests/available")
async def available_quests(
    user: dict = Depends(_get_current_user),
    town_id: str | None = None,
    board: str | None = None,
):
    ch = await _get_character_or_404(user["_id"])
    active_ids = {q["quest_id"] for q in ch.get("active_quests", [])}
    completed = set(ch.get("completed_quests", []))
    rows = []
    for q in QUESTS:
        if q["id"] in active_ids or q["id"] in completed:
            continue
        if ch["level"] < q.get("level_req", 1):
            continue
        if q.get("unlocked_by") and q["unlocked_by"] not in completed:
            continue
        if town_id and q.get("town_id") != town_id:
            continue
        if board and q.get("board") != board:
            continue
        rows.append(q)
    # Continental bonus: Valeria contract_quest_chance — daily bonus contract quest
    if ch.get("current_continent") == "valeria" and (not board or board == "notice"):
        from world_data import continental_bonus_for
        import random as _rng
        from datetime import date as _date
        _cqc = continental_bonus_for("valeria", "contract_quest_chance")
        if _cqc:
            _day = _date.today().isoformat()
            _seed = hash(f"{ch['id']}_contract_{_day}") % (2**31)
            _rng.seed(_seed)
            if _rng.random() < float(_cqc):
                contract_id = f"valeria_daily_contract_{_day}"
                if contract_id not in active_ids and contract_id not in completed:
                    rows.append({
                        "id": contract_id,
                        "name": "Daily Trade Contract",
                        "brief": "A broker in Valeria needs a reliable hand for a special delivery.",
                        "level_req": 1,
                        "town_id": ch.get("current_town"),
                        "board": "notice",
                        "repeatable": True,
                        "is_contract": True,
                    })
    return {"available": rows, "active": ch.get("active_quests", []), "completed": list(completed)}


@api.post("/game/quests/{quest_id}/accept")
async def accept_quest(quest_id: str, user: dict = Depends(_get_current_user)):
    ch = await _get_character_or_404(user["_id"])
    q = get_quest(quest_id) or EVENTS_BY_ID.get(quest_id)
    if not q:
        raise HTTPException(status_code=404, detail="Unknown quest")
    if any(a["quest_id"] == quest_id for a in ch.get("active_quests", [])):
        raise HTTPException(status_code=409, detail="Quest already active")
    if quest_id in ch.get("completed_quests", []) and q.get("category") != "event":
        raise HTTPException(status_code=409, detail="Quest already completed")
    if ch["level"] < q.get("level_req", 1):
        raise HTTPException(status_code=403, detail=f"Requires level {q['level_req']}")
    ch.setdefault("active_quests", []).append({
        "quest_id": quest_id,
        "progress": [0] * len(q.get("objectives", [])),
        "complete": False,
        "accepted_at": datetime.now(timezone.utc).isoformat(),
    })
    await db.characters.update_one({"_id": ObjectId(ch["id"])}, {"$set": {"active_quests": ch["active_quests"]}})
    accept_narrative = q.get("narrative", {}).get("accept") if isinstance(q.get("narrative"), dict) else None
    if not accept_narrative:
        accept_narrative = f"You take up the task: \"{q.get('title', q.get('name', quest_id))}.\" {q.get('brief', '')}"
    return {"character": ch, "quest": q, "narrative": accept_narrative}


@api.post("/game/quests/{quest_id}/abandon")
async def abandon_quest(quest_id: str, user: dict = Depends(_get_current_user)):
    ch = await _get_character_or_404(user["_id"])
    before = len(ch.get("active_quests", []))
    ch["active_quests"] = [a for a in ch.get("active_quests", []) if a["quest_id"] != quest_id]
    if len(ch["active_quests"]) == before:
        raise HTTPException(status_code=404, detail="Not an active quest")
    await db.characters.update_one({"_id": ObjectId(ch["id"])}, {"$set": {"active_quests": ch["active_quests"]}})
    q = get_quest(quest_id) or EVENTS_BY_ID.get(quest_id)
    abandon_narrative = q.get("narrative", {}).get("abandon") if isinstance(q.get("narrative"), dict) else None
    if not abandon_narrative:
        abandon_narrative = f"You set aside \"{q.get('title', q.get('name', quest_id))}.\" Perhaps another day."
    return {"character": ch, "quest": q, "narrative": abandon_narrative}


@api.post("/game/quests/{quest_id}/claim")
async def claim_quest(quest_id: str, user: dict = Depends(_get_current_user)):
    ch = await _get_character_or_404(user["_id"])
    aq = next((a for a in ch.get("active_quests", []) if a["quest_id"] == quest_id), None)
    if not aq:
        raise HTTPException(status_code=404, detail="Not an active quest")
    if not aq.get("complete"):
        raise HTTPException(status_code=400, detail="Quest objectives not complete")
    q = get_quest(quest_id) or EVENTS_BY_ID.get(quest_id)
    if not q:
        raise HTTPException(status_code=404, detail="Unknown quest")
    reward = q.get("reward", {})
    # Convert item chances to concrete drops
    items_out = []
    for it in reward.get("items", []) or []:
        if isinstance(it, (list, tuple)) and len(it) == 2:
            item_id, val = it
            if isinstance(val, float) and val <= 1.0:
                if random.random() <= val:
                    items_out.append((item_id, 1))
            else:
                items_out.append((item_id, int(val)))
    _apply_rewards_to_character(ch, {
        "gold": reward.get("gold", 0),
        "xp": reward.get("xp", 0),
        "items": items_out,
    }, reduce=False)
    ch["active_quests"] = [a for a in ch["active_quests"] if a["quest_id"] != quest_id]
    ch.setdefault("completed_quests", []).append(quest_id)
    await db.characters.update_one({"_id": ObjectId(ch["id"])}, {"$set": {
        "active_quests": ch["active_quests"],
        "completed_quests": ch["completed_quests"],
        "gold": ch["gold"], "xp": ch["xp"], "level": ch["level"],
        "base_stats": ch.get("base_stats", ch["stats"]), "stats": ch["stats"], "max_hp": ch["max_hp"], "inventory": ch["inventory"],
        "item_instances": ch.get("item_instances", []),
    }})
    await _push_world_event(ch["name"], f"{ch['name']} completed \"{q['title'] if 'title' in q else q['name']}\".", "quest")
    return {"character": ch, "claimed": {"gold": reward.get("gold", 0), "xp": reward.get("xp", 0), "items": items_out}}


# ---------------- EVENTS ----------------
@api.get("/game/events/active")
async def active_events(user: dict = Depends(_get_current_user)):
    wd = datetime.now(timezone.utc).weekday()
    return {"weekday": wd, "events": get_active_events(wd)}


@api.post("/game/events/{event_id}/join")
async def join_event(event_id: str, user: dict = Depends(_get_current_user)):
    ev = EVENTS_BY_ID.get(event_id)
    if not ev:
        raise HTTPException(status_code=404, detail="Unknown event")
    wd = datetime.now(timezone.utc).weekday()
    if -1 not in ev["schedule_days"] and wd not in ev["schedule_days"]:
        raise HTTPException(status_code=403, detail="Event not currently active")
    ch = await _get_character_or_404(user["_id"])
    if ch["level"] < ev.get("level_req", 1):
        raise HTTPException(status_code=403, detail=f"Requires level {ev['level_req']}")
    if any(a["quest_id"] == event_id for a in ch.get("active_quests", [])):
        raise HTTPException(status_code=409, detail="Already joined")
    ch.setdefault("active_quests", []).append({
        "quest_id": event_id,
        "progress": [0] * len(ev.get("objectives", [])),
        "complete": False,
        "accepted_at": datetime.now(timezone.utc).isoformat(),
        "is_event": True,
    })
    await db.characters.update_one({"_id": ObjectId(ch["id"])}, {"$set": {"active_quests": ch["active_quests"]}})
    return {"character": ch}


# ---------------- TOWNS ----------------
@api.post("/game/town/visit")
async def visit_town(request: Request, user: dict = Depends(_get_current_user)):
    body = await request.json()
    town_id = body.get("town_id")
    town = get_town(town_id)
    if not town:
        raise HTTPException(status_code=404, detail="Unknown town")
    ch = await _get_character_or_404(user["_id"])
    # Level check — you can only enter towns on continents you can travel to
    cont = next((c for c in CONTINENTS if c["id"] == town["continent"]), None)
    if cont and ch["level"] < cont.get("level_req", 1):
        raise HTTPException(status_code=403, detail=f"{town['name']} lies in {cont['name']}. Requires level {cont['level_req']}.")
    # Must be on same continent to enter on foot (fast-travel is a separate route)
    if ch.get("current_continent") != town["continent"]:
        raise HTTPException(status_code=403, detail=f"You must travel to {cont['name'] if cont else town['continent']} before entering {town['name']}.")
    ch["current_town"] = town_id
    if town_id not in ch.get("visited_towns", []):
        ch.setdefault("visited_towns", []).append(town_id)
    # Update last_sanctuary_town if this town has a sanctuary service
    update_fields = {
        "current_town": ch["current_town"],
        "visited_towns": ch["visited_towns"],
    }
    if "sanctuary" in town.get("services", []):
        ch["last_sanctuary_town"] = town_id
        update_fields["last_sanctuary_town"] = town_id
    await db.characters.update_one({"_id": ObjectId(ch["id"])}, {"$set": update_fields})
    return {"character": ch, "town": town}


@api.post("/game/town/leave")
async def leave_town(user: dict = Depends(_get_current_user)):
    ch = await _get_character_or_404(user["_id"])
    ch["current_town"] = None
    await db.characters.update_one({"_id": ObjectId(ch["id"])}, {"$set": {"current_town": None}})
    return {"character": ch}


@api.post("/game/town/sanctuary")
async def rest_at_sanctuary(request: Request, user: dict = Depends(_get_current_user)):
    body = await request.json()
    service = body.get("service", "rest")  # "rest" | "cleanse" | "blessing"
    ch = await _get_character_or_404(user["_id"])
    town = get_town(ch.get("current_town"))
    if not town:
        raise HTTPException(status_code=400, detail="You must be in a town to use the Sanctuary")
    if "sanctuary" not in town.get("services", []):
        raise HTTPException(status_code=400, detail="This town has no Sanctuary.")
    base_cost = town.get("sanctuary_cost", 10)
    if service == "cleanse":
        cost = base_cost * 2
    elif service == "blessing":
        cost = base_cost * 3
    else:
        cost = base_cost
    if ch["gold"] < cost:
        raise HTTPException(status_code=400, detail=f"Not enough gold ({cost}g required)")
    ch["gold"] -= cost
    if service == "rest":
        ch["hp"] = ch["max_hp"]
        ch["statuses"] = [s for s in ch.get("statuses", []) if s.get("kind") != "debuff"]
        ch["exhaustion"] = max(0, ch.get("exhaustion", 0) - 20)
        ch["resolve"] = min(100, ch.get("resolve", 100) + 10)
    elif service == "cleanse":
        ch["statuses"] = [s for s in ch.get("statuses", []) if s.get("id") != "recovering"]
    elif service == "blessing":
        existing = [s for s in ch.get("statuses", []) if s.get("id") == "sanctuary_blessing"]
        if existing:
            raise HTTPException(status_code=400, detail="You already have a Sanctuary Blessing active.")
        from game_engine import make_status
        blessing = make_status("sanctuary_blessing")
        ch["statuses"].append(blessing)
    # Update last_sanctuary_town when visiting any sanctuary
    ch["last_sanctuary_town"] = ch["current_town"]
    await db.characters.update_one({"_id": ObjectId(ch["id"])}, {"$set": {
        "gold": ch["gold"], "hp": ch["hp"], "statuses": ch["statuses"],
        "exhaustion": ch["exhaustion"], "resolve": ch["resolve"],
        "last_sanctuary_town": ch["last_sanctuary_town"],
    }})
    # Narrative text for each service
    sanctuary_name = town.get("name", "the Sanctuary")
    narratives = {
        "rest": f"The sanctuary keeper leads you to a quiet alcove overlooking the valley. Soft candlelight dances across ancient stone as you sink into a bed of fresh rushes. You sleep deeply — dreamless, safe — and wake with your strength restored. \"Rest easy, traveler. The road will wait,\" the keeper murmurs.",
        "cleanse": f"You kneel before the sanctum's altar. The keeper pours water over your brow, tracing old sigils across your shoulders. A warmth spreads through your limbs — the shadow of death loosens its grip and fades like morning mist. \"You are clean of it now. Go forward unburdened,\" they whisper.",
        "blessing": f"The keeper anoints your brow with sacred oil, pressing a thumb to the old mark above your eyes. Golden light pulses through the sanctuary's vaulted ceiling, and for a moment you hear distant chanting. \"Carry the Sanctuary's favor with you. May your blade strike true and your spirit grow swift.\"",
    }
    return {"character": ch, "cost": cost, "service": service,
            "narrative": narratives.get(service, ""), "sanctuary_name": sanctuary_name}


@api.get("/game/town/sanctuary/roster")
async def sanctuary_roster(user: dict = Depends(_get_current_user)):
    """List players who recently died or are currently resting in any sanctuary.
    Like Torn's hospital — shows who's recovering."""
    from world_data import HOMETOWN_BY_CONTINENT
    ch = await _get_character_or_404(user["_id"])
    town = get_town(ch.get("current_town"))
    if not town or "sanctuary" not in town.get("services", []):
        raise HTTPException(status_code=400, detail="You must be in a Sanctuary to view the roster.")
    # All sanctuary town IDs (hometowns)
    sanctuary_town_ids = list(HOMETOWN_BY_CONTINENT.values())
    # Find players who are currently in a sanctuary town OR have recovering debuff
    query = {
        "$or": [
            {"current_town": {"$in": sanctuary_town_ids}},
            {"statuses.id": "recovering"},
        ],
    }
    cursor = db.characters.find(query, {
        "name": 1, "level": 1, "race": 1, "current_town": 1,
        "deaths": 1, "last_death": 1, "statuses": 1, "hp": 1, "max_hp": 1,
    }).limit(50)
    roster = []
    async for doc in cursor:
        statuses = doc.get("statuses", [])
        has_recovering = any(s.get("id") == "recovering" for s in statuses)
        last_death = doc.get("last_death") or {}
        town_id = doc.get("current_town")
        town_obj = get_town(town_id) if town_id else None
        roster.append({
            "name": doc.get("name", "Unknown"),
            "level": doc.get("level", 1),
            "race": doc.get("race", "unknown"),
            "town": town_obj["name"] if town_obj else town_id,
            "recovering": has_recovering,
            "deaths": doc.get("deaths", 0),
            "cause": last_death.get("cause"),
            "hp": doc.get("hp", 0),
            "max_hp": doc.get("max_hp", 1),
        })
    # Sort: recovering first, then by level desc
    roster.sort(key=lambda r: (not r["recovering"], -r["level"]))
    return {"roster": roster, "town_name": town["name"]}


@api.post("/game/character/logout-screen")
async def update_logout_screen(request: Request, user: dict = Depends(_get_current_user)):
    """Track what screen the player was on when they logged out.
    Used for PvP safety: if logged out in sanctuary, cannot be attacked."""
    try:
        body = await request.json()
    except Exception:
        raw = await request.body()
        import json as _json
        body = _json.loads(raw) if raw else {}
    screen = body.get("screen", "unknown")
    ch = await _get_character_or_404(user["_id"])
    ch["last_screen"] = screen
    await db.characters.update_one({"_id": ObjectId(ch["id"])}, {"$set": {"last_screen": screen}})
    return {"ok": True}


@api.post("/game/town/fast_travel")
async def fast_travel(request: Request, user: dict = Depends(_get_current_user)):
    body = await request.json()
    dest_id = body.get("town_id")
    dest = get_town(dest_id)
    if not dest:
        raise HTTPException(status_code=404, detail="Unknown town")
    ch = await _get_character_or_404(user["_id"])
    if dest_id not in ch.get("visited_towns", []):
        raise HTTPException(status_code=403, detail="You have not yet visited this town")
    cost = dest.get("fast_travel_cost", 25)
    if ch["gold"] < cost:
        raise HTTPException(status_code=400, detail="Not enough gold")
    ch["gold"] -= cost
    ch["current_town"] = dest_id
    ch["current_continent"] = dest["continent"]
    # place them at a biome in the region if possible
    region = next((r for r in REGIONS if r["id"] == dest["region"]), None)
    if region and region.get("biomes"):
        ch["current_biome"] = region["biomes"][0]
    await db.characters.update_one({"_id": ObjectId(ch["id"])}, {"$set": {
        "gold": ch["gold"], "current_town": ch["current_town"],
        "current_continent": ch["current_continent"],
        "current_biome": ch["current_biome"],
    }})
    return {"character": ch, "cost": cost}


# ============================================================
# GRAND TELEPORTER (Phase B) — hometown-hub inter-continental travel
# ============================================================
@api.get("/game/teleporter/destinations")
async def teleporter_destinations(user: dict = Depends(_get_current_user)):
    """List accessible continents + their hometowns. Home continent is excluded from the fee list."""
    from world_data import HOMETOWN_BY_CONTINENT
    ch = await _get_character_or_404(user["_id"])
    allowed, block_reason = teleporter_can_use(ch)
    dests = []
    _active_hc = get_heritage_continent()
    _active_hm = get_active_heritage_month()
    for c in CONTINENTS:
        if c.get("locked"):
            continue
        hometown = HOMETOWN_BY_CONTINENT.get(c["id"])
        town = TOWNS_BY_ID.get(hometown) if hometown else None
        is_current = c["id"] == ch.get("current_continent")
        is_heritage = c["id"] == _active_hc
        # Heritage month: free travel to/from heritage continent
        base_fee = TELEPORTER_FEE if not is_current else 0
        if is_heritage and not is_current:
            _hb = get_heritage_bonuses(c["id"])
            if _hb and _hb.get("free_travel"):
                base_fee = 0
        dests.append({
            "continent_id": c["id"],
            "continent_name": c["name"],
            "hometown_id": hometown,
            "hometown_name": town["name"] if town else hometown,
            "fee": base_fee,
            "is_current": is_current,
            "is_available": allowed and not is_current,
            "is_heritage": is_heritage,
            "heritage_name": _active_hm["name"] if is_heritage and _active_hm else None,
            "heritage_desc": _active_hm["desc"] if is_heritage and _active_hm else None,
            "heritage_bonuses": get_heritage_bonuses(c["id"]) if is_heritage else None,
            "desc": c.get("desc", ""),
            "specialty": c.get("specialty", ""),
            "home_race": c.get("home_race", ""),
            "bonus_desc": c.get("bonus_desc", ""),
        })
    return {"destinations": dests, "cooldown_secs": TELEPORTER_COOLDOWN_SECS,
            "fee_base": TELEPORTER_FEE, "block_reason": block_reason,
            "active_heritage_continent": _active_hc,
            "active_heritage_name": _active_hm["name"] if _active_hm else None}


@api.post("/game/teleporter/travel")
async def teleporter_travel(request: Request, user: dict = Depends(_get_current_user)):
    from world_data import HOMETOWN_BY_CONTINENT
    body = await request.json()
    target_continent = body.get("continent_id")
    if not target_continent:
        raise HTTPException(status_code=400, detail="continent_id required")
    ch = await _get_character_or_404(user["_id"])
    # Validate: destination is accessible + not the current continent
    dest_cont = next((c for c in CONTINENTS if c["id"] == target_continent), None)
    if not dest_cont:
        raise HTTPException(status_code=404, detail="Unknown continent")
    if dest_cont.get("locked"):
        raise HTTPException(status_code=403, detail=f"{dest_cont['name']} is sealed to travellers.")
    if target_continent == ch.get("current_continent"):
        raise HTTPException(status_code=400, detail="You are already on this continent.")
    # Guard-check
    allowed, reason = teleporter_can_use(ch)
    if not allowed:
        raise HTTPException(status_code=403, detail=reason)
    # Fee — heritage month: free travel to/from heritage continent
    _heritage_free = False
    _from_hc = is_heritage_month_for(ch.get("current_continent", ""))
    _to_hc = is_heritage_month_for(target_continent)
    if _from_hc or _to_hc:
        _hb = get_heritage_bonuses(target_continent if _to_hc else ch.get("current_continent", ""))
        if _hb and _hb.get("free_travel"):
            _heritage_free = True
    if not _heritage_free and ch["gold"] < TELEPORTER_FEE:
        raise HTTPException(status_code=400, detail=f"Teleporter fee is {TELEPORTER_FEE}g.")
    hometown = HOMETOWN_BY_CONTINENT.get(target_continent)
    if not hometown:
        raise HTTPException(status_code=500, detail="No hometown mapped for this continent.")
    # Apply
    if not _heritage_free:
        ch["gold"] -= TELEPORTER_FEE
    ch["current_continent"] = target_continent
    ch["current_town"] = hometown
    if hometown not in ch.get("visited_towns", []):
        ch.setdefault("visited_towns", []).append(hometown)
    # Arrive INSIDE the hometown itself — biome is null until the player walks
    # out. Matches the /waystone/travel pattern of a single-authoritative location.
    ch["current_biome"] = None
    ch["teleporter_last_used"] = datetime.now(timezone.utc).isoformat()
    ch["last_sanctuary_town"] = hometown
    await db.characters.update_one({"_id": ObjectId(ch["id"])}, {"$set": {
        "gold": ch["gold"],
        "current_continent": ch["current_continent"],
        "current_town": ch["current_town"],
        "current_biome": ch["current_biome"],
        "visited_towns": ch["visited_towns"],
        "teleporter_last_used": ch["teleporter_last_used"],
        "last_sanctuary_town": ch["last_sanctuary_town"],
    }})
    _fee = 0 if _heritage_free else TELEPORTER_FEE
    _is_heritage = is_heritage_month_for(target_continent)
    return {"character": ch, "fee": _fee, "hometown": hometown,
            "is_heritage_arrival": _is_heritage,
            "heritage_continent": target_continent if _is_heritage else None,
            "narrative":
            f"The Grand Teleporter hums awake. The world folds, and you step into {dest_cont['name']}."}


# ============================================================
# WAYSTONES (Phase B) — discover + activate + local fast-travel
# ============================================================
@api.get("/game/waystones")
async def list_waystones(user: dict = Depends(_get_current_user)):
    ch = await _get_character_or_404(user["_id"])
    known = set(ch.get("known_waystones", []))
    active = set(ch.get("active_waystones", []))
    ws_list = []
    for w in WAYSTONES:
        ws_list.append({
            **w,
            "discovered": w["id"] in known,
            "activated":  w["id"] in active,
        })
    return {"waystones": ws_list}


@api.post("/game/waystone/discover")
async def waystone_discover(request: Request, user: dict = Depends(_get_current_user)):
    body = await request.json()
    ws_id = body.get("waystone_id")
    ws = WAYSTONES_BY_ID.get(ws_id)
    if not ws:
        raise HTTPException(status_code=404, detail="Unknown waystone")
    ch = await _get_character_or_404(user["_id"])
    # must be in the correct biome
    if ch.get("current_biome") != ws["biome"]:
        raise HTTPException(status_code=403, detail=f"You are not standing near this waystone.")
    known = ch.setdefault("known_waystones", [])
    if ws_id in known:
        return {"character": ch, "waystone": ws, "already_known": True}
    known.append(ws_id)
    await db.characters.update_one({"_id": ObjectId(ch["id"])}, {"$set": {"known_waystones": known}})
    return {"character": ch, "waystone": ws, "already_known": False,
            "narrative": f"You brush the stone. The {ws['name']} answers."}


@api.post("/game/waystone/activate")
async def waystone_activate(request: Request, user: dict = Depends(_get_current_user)):
    body = await request.json()
    ws_id = body.get("waystone_id")
    ws = WAYSTONES_BY_ID.get(ws_id)
    if not ws:
        raise HTTPException(status_code=404, detail="Unknown waystone")
    ch = await _get_character_or_404(user["_id"])
    if ws_id not in ch.get("known_waystones", []):
        raise HTTPException(status_code=403, detail="You must first discover this waystone.")
    if ws_id in ch.get("active_waystones", []):
        raise HTTPException(status_code=400, detail="Already activated.")
    cost = ws["activation_gold"]
    if ch["gold"] < cost:
        raise HTTPException(status_code=400, detail=f"Activation cost is {cost}g.")
    ch["gold"] -= cost
    active = ch.setdefault("active_waystones", [])
    active.append(ws_id)
    await db.characters.update_one({"_id": ObjectId(ch["id"])}, {"$set": {
        "gold": ch["gold"], "active_waystones": active,
    }})
    return {"character": ch, "waystone": ws, "cost": cost,
            "narrative": f"The {ws['name']} drinks in your gold and hums to life."}


@api.post("/game/waystone/travel")
async def waystone_travel(request: Request, user: dict = Depends(_get_current_user)):
    body = await request.json()
    ws_id = body.get("waystone_id")
    ws = WAYSTONES_BY_ID.get(ws_id)
    if not ws:
        raise HTTPException(status_code=404, detail="Unknown waystone")
    ch = await _get_character_or_404(user["_id"])
    if ws_id not in ch.get("active_waystones", []):
        raise HTTPException(status_code=403, detail="This waystone is not yet activated.")
    if ch.get("current_continent") != ws["continent"]:
        raise HTTPException(status_code=403, detail="Waystones only work within their continent.")
    ch["current_biome"] = ws["biome"]
    ch["current_town"] = None
    await db.characters.update_one({"_id": ObjectId(ch["id"])}, {"$set": {
        "current_biome": ch["current_biome"], "current_town": None,
    }})
    return {"character": ch, "waystone": ws,
            "narrative": f"You step into the {ws['name']} and step out at the far side of the map."}


# ============================================================
# HOMELAND REPUTATION (Phase B) — view + admin-style adjustments
# ============================================================
@api.get("/game/reputation")
async def get_reputation(user: dict = Depends(_get_current_user)):
    from world_data import HOMETOWN_BY_CONTINENT
    ch = await _get_character_or_404(user["_id"])
    rep = ch.get("reputation") or {}
    out = []
    for c in CONTINENTS:
        if c.get("locked"):
            continue
        entry = rep.get(c["id"], {"points": 0, "level": "neutral"})
        out.append({
            "continent_id": c["id"],
            "continent_name": c["name"],
            "hometown": HOMETOWN_BY_CONTINENT.get(c["id"]),
            "is_native": ch.get("race") and c.get("home_race") == ch["race"],
            "points": int(entry.get("points", 0)),
            "level": entry.get("level", "neutral"),
        })
    return {"reputation": out, "levels": REP_LEVELS, "thresholds": REP_THRESHOLDS}


# ============================================================
# PROFESSIONS (Phase D)
# ============================================================
@api.get("/game/professions/catalog")
async def profession_catalog(user: dict = Depends(_get_current_user)):
    ch = await _get_character_or_404(user["_id"])
    current_town = ch.get("current_town")
    town = TOWNS_BY_ID.get(current_town) if current_town else None
    trade_specialties = town.get("trade_npc", {}).get("specialties", []) if town else []
    catalog = [p for p in PROFESSIONS if p["id"] in trade_specialties]
    return {
        "catalog": catalog,
        "ranks": PROFESSION_RANKS,
    }


@api.get("/game/professions/mine")
async def my_professions(user: dict = Depends(_get_current_user)):
    ch = await _get_character_or_404(user["_id"])
    out = []
    for p in ch.get("professions", []):
        meta = PROFESSIONS_BY_ID.get(p["id"], {})
        points = p.get("xp", 0)
        # Migrate legacy XP if needed
        if points > 600:
            from professions import _migrate_xp_to_points
            points = _migrate_xp_to_points(points)
        rank = p.get("rank", "novice")
        rank_idx = PROFESSION_RANKS.index(rank) if rank in PROFESSION_RANKS else 0
        from professions import points_to_next_rank, POINTS_PER_TIER
        out.append({
            "id": p["id"],
            "name": meta.get("name", p["id"]),
            "kind": meta.get("kind"),
            "rank": rank,
            "tier": rank_idx,
            "points": points,
            "points_in_tier": points - (rank_idx * POINTS_PER_TIER),
            "points_to_next": points_to_next_rank(points),
            "points_per_tier": POINTS_PER_TIER,
            "learned": p.get("learned"),
        })
    return {"professions": out}


@api.post("/game/professions/learn")
async def learn_profession_endpoint(request: Request, user: dict = Depends(_get_current_user)):
    body = await request.json()
    pid = body.get("profession_id")
    ch = await _get_character_or_404(user["_id"])
    if not ch.get("current_town"):
        raise HTTPException(status_code=403, detail="You must be in a town to learn a trade.")
    prof = PROFESSIONS_BY_ID.get(pid)
    if not prof:
        raise HTTPException(status_code=404, detail="Unknown profession")
    current_town = ch.get("current_town")
    town = TOWNS_BY_ID.get(current_town)
    trade_specialties = town.get("trade_npc", {}).get("specialties", []) if town else []
    if pid not in trade_specialties:
        raise HTTPException(status_code=403, detail=f"{prof['name']} is not taught by this town's trade master.")
    ok, msg = learn_profession(ch, pid)
    if not ok:
        raise HTTPException(status_code=400, detail=msg)
    await db.characters.update_one({"_id": ObjectId(ch["id"])}, {"$set": {
        "professions": ch["professions"],
    }})
    return {"character": ch, "message": msg}


@api.post("/game/professions/abandon")
async def abandon_profession_endpoint(request: Request, user: dict = Depends(_get_current_user)):
    body = await request.json()
    pid = body.get("profession_id")
    ch = await _get_character_or_404(user["_id"])
    ok, msg = abandon_profession(ch, pid)
    if not ok:
        raise HTTPException(status_code=400, detail=msg)
    await db.characters.update_one({"_id": ObjectId(ch["id"])}, {"$set": {
        "professions": ch["professions"],
        "abandoned_professions": ch.get("abandoned_professions", {}),
    }})
    return {"character": ch, "message": msg}


@api.get("/game/tools")
async def my_tools(user: dict = Depends(_get_current_user)):
    """Return tool durability for each profession the character knows."""
    from regional_resources import get_profession_tool
    ch = await _get_character_or_404(user["_id"])
    out = []
    for p in ch.get("professions", []):
        meta = PROFESSIONS_BY_ID.get(p["id"], {})
        if meta.get("tool"):
            tool = get_profession_tool(ch, p["id"])
            if tool:
                out.append({
                    "profession_id": p["id"],
                    "profession": meta.get("name"),
                    "tool_id": tool.get("id"),
                    "tool_name": tool.get("name"),
                    "durability": tool.get("durability", 0),
                    "max_durability": tool.get("max_durability", 100),
                })
    return {"tools": out}


REPAIR_COST_PER_POINT = 2
TOOL_PURCHASE_COST = 50


@api.post("/game/tools/repair")
async def repair_tool_endpoint(request: Request, user: dict = Depends(_get_current_user)):
    """Repair a profession tool to full durability for gold. Only available in town."""
    from regional_resources import get_profession_tool, repair_tool
    body = await request.json()
    profession_id = body.get("profession_id")
    ch = await _get_character_or_404(user["_id"])
    if not ch.get("current_town"):
        raise HTTPException(status_code=400, detail="You must be in a town to repair tools.")
    meta = PROFESSIONS_BY_ID.get(profession_id, {})
    if not meta or not meta.get("tool"):
        raise HTTPException(status_code=400, detail="That profession has no tool.")
    tool = get_profession_tool(ch, profession_id)
    if not tool:
        raise HTTPException(status_code=400, detail="You don't own that tool.")
    max_dur = int(tool.get("max_durability", 100))
    current = int(tool.get("durability", 0))
    missing = max_dur - current
    if missing <= 0:
        raise HTTPException(status_code=400, detail="Tool is already at full durability.")
    cost = missing * REPAIR_COST_PER_POINT
    # Continental bonus: Khardrum repair cost reduction
    from world_data import continental_bonus_for
    repair_reduction = continental_bonus_for(ch.get("current_continent", ""), "repair_cost_reduction")
    if repair_reduction:
        cost = max(1, int(cost * (1.0 - repair_reduction)))
    if ch["gold"] < cost:
        raise HTTPException(status_code=400, detail=f"Repair costs {cost}g — you have {ch['gold']}g.")
    ch["gold"] -= cost
    repair_tool(ch, profession_id)
    await db.characters.update_one({"_id": ObjectId(ch["id"])}, {"$set": {
        "gold": ch["gold"], "tools": ch.get("tools", {}),
        "inventory": ch.get("inventory", []),
    }})
    return {"character": ch, "profession_id": profession_id, "paid": cost,
            "durability": max_dur, "max_durability": max_dur}


@api.post("/game/tools/buy")
async def buy_tool_endpoint(request: Request, user: dict = Depends(_get_current_user)):
    """Buy a basic tool for a gathering profession. Only available in town."""
    body = await request.json()
    profession_id = body.get("profession_id")
    ch = await _get_character_or_404(user["_id"])
    if not ch.get("current_town"):
        raise HTTPException(status_code=400, detail="You must be in a town to buy tools.")
    meta = PROFESSIONS_BY_ID.get(profession_id, {})
    if not meta or not meta.get("tool"):
        raise HTTPException(status_code=400, detail="That profession has no tool.")
    if meta.get("kind") != "gathering":
        raise HTTPException(status_code=400, detail="Only gathering professions need tools.")
    tool_id = meta["tool"]["id"]
    # Check if already owned (in inventory or legacy tools dict)
    from regional_resources import get_profession_tool
    existing = get_profession_tool(ch, profession_id)
    if existing and int(existing.get("durability", 0)) > 0:
        raise HTTPException(status_code=400, detail="You already own that tool.")
    if ch["gold"] < TOOL_PURCHASE_COST:
        raise HTTPException(status_code=400, detail=f"Tool costs {TOOL_PURCHASE_COST}g — you have {ch['gold']}g.")
    ch["gold"] -= TOOL_PURCHASE_COST
    max_dur = meta["tool"]["max_durability"]
    # Add to inventory as a tool item with durability
    inv = ch.setdefault("inventory", [])
    found = False
    for slot in inv:
        if slot.get("item_id") == tool_id:
            slot["quantity"] = slot.get("quantity", 0) + 1
            slot["durability"] = max_dur
            found = True
            break
    if not found:
        inv.append({"item_id": tool_id, "quantity": 1, "durability": max_dur})
    # Also update legacy tools dict for backwards compat
    tools = ch.setdefault("tools", {})
    tools[tool_id] = {"id": tool_id, "name": meta["tool"]["name"],
                      "durability": max_dur, "max_durability": max_dur}
    await db.characters.update_one({"_id": ObjectId(ch["id"])}, {"$set": {
        "gold": ch["gold"], "inventory": inv, "tools": tools,
    }})
    return {"character": ch, "profession_id": profession_id, "paid": TOOL_PURCHASE_COST,
            "tool_name": meta["tool"]["name"]}


@api.get("/game/tools/all")
async def all_tools(user: dict = Depends(_get_current_user)):
    """Return all gathering profession tools with purchase/repair info."""
    ch = await _get_character_or_404(user["_id"])
    from regional_resources import get_profession_tool
    out = []
    for prof in PROFESSIONS:
        if prof.get("kind") != "gathering" or not prof.get("tool"):
            continue
        tool = get_profession_tool(ch, prof["id"])
        owned = tool is not None
        durability = int(tool.get("durability", 0)) if tool else 0
        max_dur = prof["tool"]["max_durability"]
        repair_cost = (max_dur - durability) * REPAIR_COST_PER_POINT if owned else 0
        if repair_cost:
            from world_data import continental_bonus_for
            _rr = continental_bonus_for(ch.get("current_continent", ""), "repair_cost_reduction")
            if _rr:
                repair_cost = max(1, int(repair_cost * (1.0 - _rr)))
        out.append({
            "profession_id": prof["id"],
            "profession": prof["name"],
            "tool_id": prof["tool"]["id"],
            "tool_name": prof["tool"]["name"],
            "owned": owned,
            "durability": durability,
            "max_durability": max_dur,
            "repair_cost": repair_cost,
            "purchase_cost": TOOL_PURCHASE_COST,
        })
    return {"tools": out}


# ============================================================
# EXPLORATION PROGRESS (Phase C)
# ============================================================
@api.get("/game/exploration")
async def exploration_state(user: dict = Depends(_get_current_user)):
    """Return per-biome exploration % for the current continent, plus unlock status."""
    ch = await _get_character_or_404(user["_id"])
    cont_id = ch.get("current_continent")
    cont = next((c for c in CONTINENTS if c["id"] == cont_id), None)
    biomes = cont.get("biomes", []) if cont else []
    ep = ch.get("exploration_progress", {}) or {}
    out = []
    for b in biomes:
        pct = int(ep.get(b["id"], 0))
        thresholds_met = [pct >= t[0] for t in EXPLORATION_THRESHOLDS]
        unlocked, req, prereq = _is_biome_unlocked(ch, cont, b["id"]) if cont else (True, 0, None)
        out.append({
            "biome_id": b["id"],
            "biome_name": b["name"],
            "level_req": b.get("level_req", 1),
            "progress_pct": pct,
            "thresholds_met": thresholds_met,
            "unlocked": unlocked,
            "required_pct": req,
            "prerequisite_biome": prereq,
        })
    return {"continent_id": cont_id, "biomes": out,
            "thresholds": [{"pct": t[0], "desc": t[1]} for t in EXPLORATION_THRESHOLDS]}


@api.get("/game/discoveries")
async def discoveries_state(user: dict = Depends(_get_current_user)):
    """Return per-biome discovery status for monsters and nodes across all continents.

    Discovered entries include full details; undiscovered entries show as {'id': None, 'name': '???'}.
    """
    ch = await _get_character_or_404(user["_id"])
    all_disc = ch.get("biome_discoveries", {}) or {}
    out = []

    for cont in CONTINENTS:
        for b in cont.get("biomes", []):
            bid = b["id"]
            disc = all_disc.get(bid, {"monsters": [], "nodes": []})
            disc_mons = set(disc.get("monsters", []))
            disc_nodes = set(disc.get("nodes", []))

            monsters_out = []
            for m in monsters_for_biome(bid):
                if m["id"] in disc_mons:
                    monsters_out.append({
                        "id": m["id"], "name": m["name"], "power": m.get("power", 1),
                        "hp": m.get("hp", 10), "rarity": m.get("rarity", "common"),
                        "discovered": True,
                    })
                else:
                    monsters_out.append({
                        "id": None, "name": "???", "rarity": m.get("rarity", "common"),
                        "discovered": False,
                    })

            nodes_out = []
            for n in nodes_for_biome(bid):
                if n["id"] in disc_nodes:
                    nodes_out.append({
                        "id": n["id"], "name": n.get("name", n["id"]),
                        "profession": n.get("profession"), "rarity": n.get("rarity", "common"),
                        "discovered": True,
                    })
                else:
                    nodes_out.append({
                        "id": None, "name": "???", "rarity": n.get("rarity", "common"),
                        "discovered": False,
                    })

            ep = ch.get("exploration_progress", {})
            pct = int(ep.get(bid, 0))
            out.append({
                "continent_id": cont["id"],
                "continent_name": cont["name"],
                "biome_id": bid,
                "biome_name": b["name"],
                "exploration_pct": pct,
                "monsters": monsters_out,
                "nodes": nodes_out,
                "discovered_monsters": len(disc_mons),
                "total_monsters": len(monsters_out),
                "discovered_nodes": len(disc_nodes),
                "total_nodes": len(nodes_out),
            })

    return {"biomes": out}


@api.get("/game/town/market")
async def get_market(user: dict = Depends(_get_current_user)):
    """Return today's dynamic market for the character's current town."""
    ch = await _get_character_or_404(user["_id"])
    town_id = ch.get("current_town")
    town = get_town(town_id)
    if not town:
        raise HTTPException(status_code=400, detail="Must be in a town")
    market = get_or_generate_market(ch, town_id)
    # Persist the market cache
    await db.characters.update_one(
        {"_id": ObjectId(ch["id"])},
        {"$set": {"market_cache": ch["market_cache"]}},
    )
    # Record price history
    await record_price_history(db, town_id, market["listings"])
    # Get price history for trend indicators
    item_ids = [l["item_id"] for l in market["listings"]]
    history = await get_price_history(db, town_id, item_ids)
    # Add trend info to each listing
    for listing in market["listings"]:
        iid = listing["item_id"]
        prices = history.get(iid, [])
        listing["trend"] = compute_trend(prices)
        listing["price_history"] = prices
    return {
        "town_id": town_id,
        "day": market["day"],
        "listings": market["listings"],
        "refreshes_in": time_until_refresh(),
    }


@api.post("/game/town/market/buy")
async def market_buy(request: Request, user: dict = Depends(_get_current_user)):
    try:
        body = await request.json()
        item_id = body.get("item_id")
        qty = int(body.get("quantity", 1))
        ch = await _get_character_or_404(user["_id"])
        town_id = ch.get("current_town")
        town = get_town(town_id)
        if not town:
            raise HTTPException(status_code=400, detail="Must be in a town")
        market = get_or_generate_market(ch, town_id)
        listing = next((l for l in market["listings"] if l["item_id"] == item_id), None)
        if not listing:
            raise HTTPException(status_code=404, detail="Item not sold here today")
        if listing["stock"] < qty:
            raise HTTPException(status_code=400, detail=f"Only {listing['stock']} left in stock")
        # Handle procedural item instances vs static items
        inst = listing.get("instance")
        if inst:
            item = inst
        else:
            item = ITEMS_BY_ID.get(item_id)
            if not item:
                raise HTTPException(status_code=404, detail="Unknown item")
        price = listing["final_price"] * qty
        # Heritage month bonus: 10% market discount on heritage continent
        _hc = ch.get("current_continent", "")
        if _hc and is_heritage_month_for(_hc):
            _hb = get_heritage_bonuses(_hc)
            if _hb:
                _disc = _hb.get("market_discount", 0.0)
                if _disc:
                    price = int(price * (1.0 - _disc))
        if ch["gold"] < price:
            raise HTTPException(status_code=400, detail="Not enough gold")
        ch["gold"] -= price
        decrement_stock(ch, item_id, qty)
        if inst:
            _add_item_to_inventory(ch, inst, 1)
        else:
            _add_item_to_inventory(ch, item_id, qty)
        await db.characters.update_one({"_id": ObjectId(ch["id"])}, {"$set": {
            "gold": ch["gold"], "inventory": ch["inventory"],
            "item_instances": ch.get("item_instances", []),
            "market_cache": ch["market_cache"],
        }})
        return {
            "character": ch,
            "paid": price,
            "unit_price": listing["final_price"],
            "stock_remaining": listing["stock"],
            "discount_pct": listing["discount_pct"],
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"market_buy error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================
# Gem Shop & Item Upgrades (New Item System)
# ============================================================
@api.get("/game/town/gem-shop")
async def gem_shop_list(user: dict = Depends(_get_current_user)):
    """List all gems available for purchase."""
    from game_data import GEMS
    return {"gems": GEMS}


@api.post("/game/town/gem-shop/buy")
async def gem_shop_buy(request: Request, user: dict = Depends(_get_current_user)):
    """Buy a gem from the gem shop."""
    from game_data import GEMS_BY_ID
    body = await request.json()
    gem_id = body.get("gem_id")
    qty = int(body.get("quantity", 1))
    ch = await _get_character_or_404(user["_id"])
    town_id = ch.get("current_town")
    town = get_town(town_id)
    if not town:
        raise HTTPException(status_code=400, detail="Must be in a town")
    gem = GEMS_BY_ID.get(gem_id)
    if not gem:
        raise HTTPException(status_code=404, detail="Unknown gem")
    total_price = gem["price"] * qty
    if ch["gold"] < total_price:
        raise HTTPException(status_code=400, detail="Not enough gold")
    ch["gold"] -= total_price
    _add_item_to_inventory(ch, gem_id, qty)
    await db.characters.update_one({"_id": ObjectId(ch["id"])}, {"$set": {
        "gold": ch["gold"], "inventory": ch["inventory"],
    }})
    return {"character": ch, "paid": total_price, "gem": gem}


@api.post("/game/item/upgrade/gem")
async def item_upgrade_gem(request: Request, user: dict = Depends(_get_current_user)):
    """Socket a gem into an item instance."""
    from game_data import socket_gem as _socket_gem, can_upgrade as _can_upgrade
    body = await request.json()
    instance_id = body.get("instance_id")
    gem_id = body.get("gem_id")
    ch = await _get_character_or_404(user["_id"])
    # Find the item instance
    instances = ch.get("item_instances", [])
    item = None
    for inst in instances:
        if isinstance(inst, dict) and inst.get("instance_id") == instance_id:
            item = inst
            break
    if not item:
        raise HTTPException(status_code=404, detail="Item instance not found")
    if not _can_upgrade(item):
        raise HTTPException(status_code=400, detail="Item has reached maximum upgrades (10/10)")
    if not _remove_item_from_inventory(ch, gem_id, 1):
        raise HTTPException(status_code=400, detail="Gem not in inventory")
    success, msg = _socket_gem(item, gem_id)
    if not success:
        # Refund the gem
        _add_item_to_inventory(ch, gem_id, 1)
        raise HTTPException(status_code=400, detail=msg)
    await db.characters.update_one({"_id": ObjectId(ch["id"])}, {"$set": {
        "item_instances": ch["item_instances"],
        "inventory": ch["inventory"],
    }})
    return {"character": ch, "message": msg, "item": item}


@api.post("/game/item/upgrade/rune")
async def item_upgrade_rune(request: Request, user: dict = Depends(_get_current_user)):
    """Socket a rune into an item instance."""
    from game_data import socket_rune as _socket_rune, can_upgrade as _can_upgrade
    body = await request.json()
    instance_id = body.get("instance_id")
    rune_id = body.get("rune_id")
    ch = await _get_character_or_404(user["_id"])
    instances = ch.get("item_instances", [])
    item = None
    for inst in instances:
        if isinstance(inst, dict) and inst.get("instance_id") == instance_id:
            item = inst
            break
    if not item:
        raise HTTPException(status_code=404, detail="Item instance not found")
    if not _can_upgrade(item):
        raise HTTPException(status_code=400, detail="Item has reached maximum upgrades (10/10)")
    if not _remove_item_from_inventory(ch, rune_id, 1):
        raise HTTPException(status_code=400, detail="Rune not in inventory")
    success, msg = _socket_rune(item, rune_id)
    if not success:
        _add_item_to_inventory(ch, rune_id, 1)
        raise HTTPException(status_code=400, detail=msg)
    await db.characters.update_one({"_id": ObjectId(ch["id"])}, {"$set": {
        "item_instances": ch["item_instances"],
        "inventory": ch["inventory"],
    }})
    return {"character": ch, "message": msg, "item": item}


@api.post("/game/item/runesmith")
async def item_runesmith(request: Request, user: dict = Depends(_get_current_user)):
    """Socket multiple runes into an item at once (runesmithing service).
    Body: { instance_id: str, rune_ids: [str, ...] }
    Each rune is consumed from inventory and socketed into the item.
    """
    from game_data import socket_rune as _socket_rune, can_upgrade as _can_upgrade, get_upgrade_summary
    body = await request.json()
    instance_id = body.get("instance_id")
    rune_ids = body.get("rune_ids", [])
    if not instance_id or not rune_ids:
        raise HTTPException(status_code=400, detail="Missing instance_id or rune_ids")
    ch = await _get_character_or_404(user["_id"])
    instances = ch.get("item_instances", [])
    item = None
    for inst in instances:
        if isinstance(inst, dict) and inst.get("instance_id") == instance_id:
            item = inst
            break
    if not item:
        raise HTTPException(status_code=404, detail="Item instance not found")
    socketed = []
    failed = []
    for rune_id in rune_ids:
        if not _can_upgrade(item):
            failed.append({"rune_id": rune_id, "reason": "Item has reached maximum upgrades (10/10)"})
            break
        if not _remove_item_from_inventory(ch, rune_id, 1):
            failed.append({"rune_id": rune_id, "reason": "Rune not in inventory"})
            continue
        success, msg = _socket_rune(item, rune_id)
        if not success:
            _add_item_to_inventory(ch, rune_id, 1)
            failed.append({"rune_id": rune_id, "reason": msg})
        else:
            socketed.append(rune_id)
    if socketed:
        await db.characters.update_one({"_id": ObjectId(ch["id"])}, {"$set": {
            "item_instances": ch["item_instances"],
            "inventory": ch["inventory"],
        }})
    summary = get_upgrade_summary(item)
    msg_parts = []
    if socketed:
        msg_parts.append(f"Socketed {len(socketed)} rune(s).")
    if failed:
        msg_parts.append(f"{len(failed)} failed.")
    return {
        "character": ch,
        "message": " ".join(msg_parts) or "No runes socketed.",
        "item": item,
        "upgrade_summary": summary,
        "socketed": socketed,
        "failed": failed,
    }


@api.get("/game/item/{instance_id}/details")
async def item_instance_details(instance_id: str, user: dict = Depends(_get_current_user)):
    """Get full details of an item instance including upgrades."""
    from game_data import get_upgrade_summary
    ch = await _get_character_or_404(user["_id"])
    instances = ch.get("item_instances", [])
    for inst in instances:
        if isinstance(inst, dict) and inst.get("instance_id") == instance_id:
            summary = get_upgrade_summary(inst)
            return {"item": inst, "upgrade_summary": summary}
    raise HTTPException(status_code=404, detail="Item instance not found")


# ============================================================
# NPCs & RELATIONSHIP-GATED QUESTS (Phase F/NPC system)
# ============================================================
from npcs import (  # noqa: E402
    NPCS,
    NPCS_BY_ID,
    NPC_QUESTS_BY_ID,
    RELATIONSHIP_TIERS,
    RELATIONSHIP_THRESHOLDS,
    initial_npc_relationships,
    add_npc_relationship,
    tier_meets,
)
from world_content import (  # noqa: E402
    BOSSES,
    BOSS_PARTS,
    CROSS_CONTINENT_RECIPES,
)
from regional_resources import (  # noqa: E402
    REGIONAL_ITEMS,
    nodes_for_biome,
    seconds_until_node_ready,
)

# Merge regional materials into the global item tables so they can be gathered & traded.
for _it in REGIONAL_ITEMS:
    if _it["id"] not in ITEMS_BY_ID:
        ITEMS.append(_it)
        ITEMS_BY_ID[_it["id"]] = _it


def _npc_view(character: dict, npc: dict) -> dict:
    """Serialise an NPC with relationship + quest states appended for this character."""
    rels = character.get("npc_relationships", {})
    entry = rels.get(npc["id"]) or {"points": 0, "level": "stranger"}
    active_ids = set(character.get("active_npc_quests", []) or [])
    done_ids = set(character.get("completed_npc_quests", []) or [])
    quest_views = []
    for q in npc["quests"]:
        # Available if the tier is met and prior chain quests are complete
        is_repeatable = q.get("repeatable", False)
        chain_ok = True
        if not is_repeatable:
            for prev in npc["quests"]:
                if (prev["order"] < q["order"]
                        and not prev.get("repeatable", False)
                        and prev["id"] not in done_ids):
                    chain_ok = False
                    break
        tier_ok = tier_meets(entry["level"], q["tier"])
        if is_repeatable and q["id"] in done_ids:
            # Repeatable quests show as completed but still available to re-accept
            state = ("active" if q["id"] in active_ids
                     else "available" if (chain_ok and tier_ok)
                     else "locked")
        else:
            state = ("completed" if q["id"] in done_ids
                     else "active" if q["id"] in active_ids
                     else "available" if (chain_ok and tier_ok)
                     else "locked")
        quest_views.append({
            "id": q["id"], "name": q["name"], "order": q["order"], "tier": q["tier"],
            "brief": q["brief"], "requirements": q["requirements"], "rewards": q["rewards"],
            "state": state, "repeatable": is_repeatable,
        })
    return {
        "id": npc["id"], "name": npc["name"], "race": npc["race"],
        "title": npc["title"], "town": npc["town"], "continent": npc["continent"],
        "description": npc["description"], "personality": npc["personality"],
        "relationship": {"points": entry["points"], "level": entry["level"]},
        "quests": quest_views,
    }


@api.get("/game/npcs")
async def list_npcs(user: dict = Depends(_get_current_user)):
    ch = await _get_character_or_404(user["_id"])
    return {"npcs": [_npc_view(ch, n) for n in NPCS],
            "relationship_tiers": RELATIONSHIP_TIERS,
            "relationship_thresholds": RELATIONSHIP_THRESHOLDS}


@api.get("/game/npc/{npc_id}")
async def get_npc(npc_id: str, user: dict = Depends(_get_current_user)):
    npc = NPCS_BY_ID.get(npc_id)
    if not npc:
        raise HTTPException(status_code=404, detail="Unknown NPC")
    ch = await _get_character_or_404(user["_id"])
    return {"npc": _npc_view(ch, npc)}


@api.post("/game/npc/quest/accept")
async def accept_npc_quest(request: Request, user: dict = Depends(_get_current_user)):
    body = await request.json()
    quest_id = body.get("quest_id")
    quest = NPC_QUESTS_BY_ID.get(quest_id)
    if not quest:
        raise HTTPException(status_code=404, detail="Unknown quest")
    ch = await _get_character_or_404(user["_id"])
    npc = NPCS_BY_ID.get(quest["npc_id"])
    # Must be in the same town as the NPC
    if ch.get("current_town") != npc["town"]:
        raise HTTPException(status_code=403, detail=f"You must speak with {npc['name']} in {npc['town'].title()}.")
    # Check tier + chain
    rel = (ch.get("npc_relationships", {}) or {}).get(npc["id"]) or {"level": "stranger"}
    if not tier_meets(rel["level"], quest["tier"]):
        raise HTTPException(status_code=403, detail=f"{npc['name']} does not yet trust you with this task.")
    done = set(ch.get("completed_npc_quests", []) or [])
    for prev in npc["quests"]:
        if (prev["order"] < quest["order"]
                and not prev.get("repeatable", False)
                and prev["id"] not in done):
            raise HTTPException(status_code=403, detail=f"Finish {prev['name']} first.")
    active = ch.setdefault("active_npc_quests", [])
    if quest_id in active:
        raise HTTPException(status_code=400, detail="Already active.")
    if quest_id in done and not quest.get("repeatable", False):
        raise HTTPException(status_code=400, detail="Already completed.")
    # Character level requirement
    req_lvl = quest.get("requirements", {}).get("character_level", 1)
    if int(ch.get("level", 1)) < req_lvl:
        raise HTTPException(status_code=400, detail=f"Requires character level {req_lvl}.")
    active.append(quest_id)
    # Initialise progress counters
    prog = ch.setdefault("npc_quest_progress", {})
    prog[quest_id] = {"kills": {}, "gathers": {}}
    await db.characters.update_one({"_id": ObjectId(ch["id"])}, {"$set": {
        "active_npc_quests": active, "npc_quest_progress": prog,
    }})
    return {"character": ch, "quest": quest, "narrative": quest["narrative"]["accept"]}


def _quest_progress_complete(quest: dict, progress: dict) -> bool:
    reqs = quest.get("requirements", {}) or {}
    for target, needed in reqs.get("kills", []) or []:
        if int(progress.get("kills", {}).get(target, 0)) < needed:
            return False
    for target, needed in reqs.get("gathers", []) or []:
        if int(progress.get("gathers", {}).get(target, 0)) < needed:
            return False
    return True


@api.post("/game/npc/quest/complete")
async def complete_npc_quest(request: Request, user: dict = Depends(_get_current_user)):
    body = await request.json()
    quest_id = body.get("quest_id")
    quest = NPC_QUESTS_BY_ID.get(quest_id)
    if not quest:
        raise HTTPException(status_code=404, detail="Unknown quest")
    ch = await _get_character_or_404(user["_id"])
    npc = NPCS_BY_ID.get(quest["npc_id"])
    if ch.get("current_town") != npc["town"]:
        raise HTTPException(status_code=403, detail=f"Return to {npc['name']} in {npc['town'].title()} to hand in the quest.")
    active = ch.setdefault("active_npc_quests", [])
    if quest_id not in active:
        raise HTTPException(status_code=400, detail="This quest is not active.")
    progress = ch.setdefault("npc_quest_progress", {}).get(quest_id, {"kills": {}, "gathers": {}})
    if not _quest_progress_complete(quest, progress):
        raise HTTPException(status_code=400, detail="You have not yet completed the objectives.")
    # Apply rewards
    rewards = quest.get("rewards", {}) or {}
    ch["gold"] = int(ch.get("gold", 0)) + int(rewards.get("gold", 0))
    ch["xp"] = int(ch.get("xp", 0)) + int(rewards.get("xp", 0))
    rank_change = add_npc_relationship(ch, npc["id"], int(rewards.get("relationship", 0)))
    for item_id, qty in (rewards.get("items", []) or []):
        _add_item_to_inventory(ch, item_id, qty)
    if rewards.get("unique_item"):
        uniq = rewards["unique_item"]
        # Register the unique item into the runtime ITEMS registry so it can be equipped/used later.
        if uniq["id"] not in ITEMS_BY_ID:
            ITEMS.append(uniq)
            ITEMS_BY_ID[uniq["id"]] = uniq
        _add_item_to_inventory(ch, uniq["id"], 1)
    # Move quest from active → completed
    active.remove(quest_id)
    done = ch.setdefault("completed_npc_quests", [])
    is_repeatable = quest.get("repeatable", False)
    if not is_repeatable and quest_id not in done:
        done.append(quest_id)
    # Clean up progress for repeatable quests so they can be re-accepted fresh
    prog = ch.setdefault("npc_quest_progress", {})
    if quest_id in prog:
        del prog[quest_id]
    await db.characters.update_one({"_id": ObjectId(ch["id"])}, {"$set": {
        "gold": ch["gold"], "xp": ch["xp"], "inventory": ch["inventory"],
        "item_instances": ch.get("item_instances", []),
        "npc_relationships": ch.get("npc_relationships", {}),
        "active_npc_quests": active, "completed_npc_quests": done,
        "npc_quest_progress": prog,
    }})
    return {"character": ch, "quest": quest, "narrative": quest["narrative"]["complete"],
            "rewards": rewards, "relationship_rank_change": rank_change}


@api.post("/game/npc/quest/abandon")
async def abandon_npc_quest(request: Request, user: dict = Depends(_get_current_user)):
    body = await request.json()
    quest_id = body.get("quest_id")
    quest = NPC_QUESTS_BY_ID.get(quest_id)
    if not quest:
        raise HTTPException(status_code=404, detail="Unknown quest")
    ch = await _get_character_or_404(user["_id"])
    active = ch.setdefault("active_npc_quests", [])
    if quest_id not in active:
        raise HTTPException(status_code=400, detail="This quest is not active.")
    active.remove(quest_id)
    prog = ch.setdefault("npc_quest_progress", {})
    prog.pop(quest_id, None)
    npc = NPCS_BY_ID.get(quest["npc_id"])
    npc_name = npc["name"] if npc else "the quest giver"
    abandon_narrative = (
        quest.get("narrative", {}).get("abandon")
        or f"You walk away from \"{quest['name']}\". {npc_name} will remember this."
    )
    await db.characters.update_one({"_id": ObjectId(ch["id"])}, {"$set": {
        "active_npc_quests": active, "npc_quest_progress": prog,
    }})
    return {"character": ch, "quest": quest, "narrative": abandon_narrative}


# ============================================================
# RACIAL ABILITIES — Heritage Surge (replaces old Phase E abilities)
# ============================================================
@api.get("/game/racial/status")
async def racial_status(user: dict = Depends(_get_current_user)):
    ch = await _get_character_or_404(user["_id"])
    race = ch.get("race")
    out = {"race": race, "abilities": []}

    # Heritage Surge — the one and only racial active ability, unlocked at Rank 2+
    heritage_rank = ch.get("heritage_rank", 1)
    from game_data_p2 import HERITAGE_SURGES, HERITAGE_SURGE_RANK_CONFIG, HERITAGE_RANK_1
    from racial import _RACE_TO_RESOURCE, get_active_surge_info
    surge = HERITAGE_SURGES.get(race, {})
    resource_key = _RACE_TO_RESOURCE.get(race)
    meta = HERITAGE_RANK_1.get(race, {})
    max_val = meta.get("resource_max", 1)
    # Use rank-2 config as preview for locked state; actual config for unlocked
    idx = min(max(heritage_rank - 2, 0), len(HERITAGE_SURGE_RANK_CONFIG) - 1)
    config = HERITAGE_SURGE_RANK_CONFIG[idx]

    ability_data = {
        "id": "heritage_surge",
        "name": surge.get("name", "Heritage Surge"),
        "cost": max_val,
        "cost_resource": resource_key,
        "cooldown_hours": config["cooldown_hours"],
        "duration": config["duration"],
        "description": surge.get("desc", ""),
        "narrative": surge.get("narrative", ""),
        "heritage_rank": heritage_rank,
        "available": False,
        "reason": "Unlocks at Heritage Rank 2.",
        "seconds_remaining": 0,
        "active_surge": None,
    }

    if heritage_rank >= 2:
        from racial import can_activate_surge
        surge_ok, surge_reason, surge_cd = can_activate_surge(ch)
        active_surge = get_active_surge_info(ch)
        ability_data.update({
            "available": surge_ok,
            "reason": surge_reason,
            "seconds_remaining": surge_cd,
            "active_surge": active_surge,
        })

    out["abilities"].append(ability_data)

    return out


@api.post("/game/racial/ability")
async def use_racial_ability(request: Request, user: dict = Depends(_get_current_user)):
    body = await request.json()
    ability = body.get("ability_id")
    ch = await _get_character_or_404(user["_id"])
    ok, msg = False, "Unknown ability"
    narrative = ""
    if ability == "heritage_surge":
        from racial import apply_surge
        result = apply_surge(ch)
        if len(result) == 3:
            ok, msg, narrative = result
        else:
            ok, msg = result
            narrative = ""
    if not ok:
        raise HTTPException(status_code=400, detail=msg)
    await db.characters.update_one({"_id": ObjectId(ch["id"])}, {"$set": {
        "hp": ch.get("hp"),
        "statuses": ch.get("statuses", []),
        "heritage_surge_active": ch.get("heritage_surge_active", 0),
        "heritage_surge_last_used": ch.get("heritage_surge_last_used"),
    }})
    # Also save racial resource if surge consumed it
    if ability == "heritage_surge":
        from racial import _RACE_TO_RESOURCE
        resource_key = _RACE_TO_RESOURCE.get(ch.get("race"))
        if resource_key:
            await db.characters.update_one({"_id": ObjectId(ch["id"])}, {"$set": {resource_key: ch.get(resource_key, 0)}})
    return {"character": ch, "message": msg, "narrative": narrative}


# ============================================================
# BOSSES + CROSS-CONTINENT RECIPES (Phase G, endpoints)
# ============================================================
@api.get("/game/bosses")
async def list_bosses(user: dict = Depends(_get_current_user)):
    return {"bosses": BOSSES}


@api.get("/game/recipes/cross_continent")
async def cross_continent_recipes(user: dict = Depends(_get_current_user)):
    return {"recipes": CROSS_CONTINENT_RECIPES, "boss_parts": BOSS_PARTS}


@api.post("/game/craft/legendary")
async def craft_legendary(request: Request, user: dict = Depends(_get_current_user)):
    body = await request.json()
    rid = body.get("recipe_id")
    recipe = next((r for r in CROSS_CONTINENT_RECIPES if r["id"] == rid), None)
    if not recipe:
        raise HTTPException(status_code=404, detail="Unknown legendary recipe")
    ch = await _get_character_or_404(user["_id"])
    # Verify inventory has all required materials
    inv = {i["item_id"]: int(i.get("quantity", 0)) for i in ch.get("inventory", [])}
    for mat_id, needed in recipe["requires"].items():
        if inv.get(mat_id, 0) < needed:
            raise HTTPException(status_code=400,
                                detail=f"Missing {needed - inv.get(mat_id, 0)} × {mat_id}.")
    # Verify profession + rank if the recipe demands it
    prof_req = recipe.get("profession")
    rank_req = recipe.get("profession_min_rank")
    if prof_req:
        prof = next((p for p in ch.get("professions", []) if p["id"] == prof_req), None)
        if not prof:
            raise HTTPException(status_code=403,
                                detail=f"Requires the {prof_req} profession.")
        if rank_req:
            from professions import PROFESSION_RANKS
            if PROFESSION_RANKS.index(prof.get("rank", "novice")) < PROFESSION_RANKS.index(rank_req):
                raise HTTPException(status_code=403,
                                    detail=f"Requires {rank_req} rank in {prof_req}.")
    # Consume materials
    for mat_id, needed in recipe["requires"].items():
        _remove_item_from_inventory(ch, mat_id, needed)
    # Produce
    produced = recipe["produces"]
    if produced["id"] not in ITEMS_BY_ID:
        ITEMS.append(produced)
        ITEMS_BY_ID[produced["id"]] = produced
    _add_item_to_inventory(ch, produced["id"], 1)
    await db.characters.update_one({"_id": ObjectId(ch["id"])}, {"$set": {
        "inventory": ch["inventory"],
    }})
    return {"character": ch, "produced": produced}


@api.post("/game/town/market/sell")
async def market_sell(request: Request, user: dict = Depends(_get_current_user)):
    body = await request.json()
    item_id = body.get("item_id")
    qty = int(body.get("quantity", 1))
    ch = await _get_character_or_404(user["_id"])
    town_id = ch.get("current_town")
    town = get_town(town_id)
    if not town:
        raise HTTPException(status_code=400, detail="Must be in a town")
    # Check for procedural item instance first
    item = None
    instances = ch.get("item_instances", [])
    inst = next((i for i in instances if i.get("instance_id") == item_id), None)
    if inst:
        item = inst
    if not item:
        item = ITEMS_BY_ID.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Unknown item")
    # For procedural instances, qty must be 1 and we remove the instance
    if inst:
        if not _remove_item_from_inventory(ch, item_id, 1):
            raise HTTPException(status_code=400, detail="Item not in inventory")
        ch["item_instances"] = [i for i in instances if i.get("instance_id") != item_id]
    else:
        if not _remove_item_from_inventory(ch, item_id, qty):
            raise HTTPException(status_code=400, detail="Not enough in inventory")
    unit_payout, sell_mod = get_sell_price(item, town_id)
    payout = unit_payout * qty
    ch["gold"] += payout
    await db.characters.update_one({"_id": ObjectId(ch["id"])}, {"$set": {
        "gold": ch["gold"], "inventory": ch["inventory"],
        "item_instances": ch.get("item_instances", []),
    }})
    return {"character": ch, "received": payout, "unit_payout": unit_payout, "sell_mod": sell_mod}
@api.get("/game/guilds")
async def list_guilds(user: dict = Depends(_get_current_user)):
    cursor = db.guilds.find({}).sort("member_count", -1).limit(50)
    rows = []
    async for doc in cursor:
        doc["id"] = str(doc["_id"])
        doc.pop("_id", None)
        rows.append(doc)
    return {"guilds": rows}


@api.get("/game/guilds/{guild_id}")
async def get_guild(guild_id: str, user: dict = Depends(_get_current_user)):
    doc = await db.guilds.find_one({"_id": ObjectId(guild_id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Guild not found")
    doc["id"] = str(doc["_id"])
    doc.pop("_id", None)
    # populate members' basic info
    members = []
    for m in doc.get("members", []):
        mch = await db.characters.find_one({"_id": ObjectId(m["character_id"])}, {"name": 1, "race": 1, "mastery": 1, "level": 1})
        if mch:
            members.append({
                "id": str(mch["_id"]),
                "name": mch.get("name"),
                "race": mch.get("race"),
                "mastery": mch.get("mastery"),
                "level": mch.get("level"),
                "rank": m.get("rank"),
                "joined_at": m.get("joined_at"),
            })
    doc["members_populated"] = members
    return {"guild": doc}


@api.post("/game/guilds")
async def create_guild(request: Request, user: dict = Depends(_get_current_user)):
    body = await request.json()
    name = (body.get("name") or "").strip()
    emblem = body.get("emblem") or "⚜"
    tagline = (body.get("tagline") or "").strip()
    if not name or len(name) < 3 or len(name) > 30:
        raise HTTPException(status_code=400, detail="Name must be 3-30 characters")
    ch = await _get_character_or_404(user["_id"])
    if ch.get("guild_id"):
        raise HTTPException(status_code=409, detail="Already in a guild")
    if ch["gold"] < 5000:
        raise HTTPException(status_code=400, detail="Guild creation costs 5,000 gold")
    existing = await db.guilds.find_one({"name": name})
    if existing:
        raise HTTPException(status_code=409, detail="Guild name taken")
    now = datetime.now(timezone.utc).isoformat()
    guild_doc = {
        "name": name,
        "emblem": emblem,
        "tagline": tagline,
        "leader_id": ch["id"],
        "treasury": 0,
        "member_count": 1,
        "members": [{"character_id": ch["id"], "rank": "grandmaster", "joined_at": now}],
        "created_at": now,
        "hall_unlocked": False,  # unlocks at 3+ members
    }
    r = await db.guilds.insert_one(guild_doc)
    guild_id = str(r.inserted_id)
    ch["gold"] -= 5000
    ch["guild_id"] = guild_id
    ch["guild_rank"] = "grandmaster"
    await db.characters.update_one({"_id": ObjectId(ch["id"])}, {"$set": {
        "gold": ch["gold"], "guild_id": ch["guild_id"], "guild_rank": ch["guild_rank"],
    }})
    await _push_world_event(ch["name"], f"{ch['name']} founded the guild \"{name}\".", "guild")
    return {"character": ch, "guild_id": guild_id}


@api.post("/game/guilds/{guild_id}/join")
async def join_guild(guild_id: str, user: dict = Depends(_get_current_user)):
    doc = await db.guilds.find_one({"_id": ObjectId(guild_id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Guild not found")
    ch = await _get_character_or_404(user["_id"])
    if ch.get("guild_id"):
        raise HTTPException(status_code=409, detail="Already in a guild")
    if doc.get("member_count", 0) >= 30:
        raise HTTPException(status_code=403, detail="Guild is full")
    now = datetime.now(timezone.utc).isoformat()
    doc["members"].append({"character_id": ch["id"], "rank": "member", "joined_at": now})
    doc["member_count"] = len(doc["members"])
    doc["hall_unlocked"] = doc["member_count"] >= 3
    await db.guilds.update_one({"_id": ObjectId(guild_id)}, {"$set": {
        "members": doc["members"], "member_count": doc["member_count"], "hall_unlocked": doc["hall_unlocked"],
    }})
    ch["guild_id"] = guild_id
    ch["guild_rank"] = "member"
    await db.characters.update_one({"_id": ObjectId(ch["id"])}, {"$set": {
        "guild_id": ch["guild_id"], "guild_rank": ch["guild_rank"],
    }})
    return {"character": ch, "guild_id": guild_id}


@api.post("/game/guilds/leave")
async def leave_guild(user: dict = Depends(_get_current_user)):
    ch = await _get_character_or_404(user["_id"])
    if not ch.get("guild_id"):
        raise HTTPException(status_code=400, detail="Not in a guild")
    doc = await db.guilds.find_one({"_id": ObjectId(ch["guild_id"])})
    if doc:
        doc["members"] = [m for m in doc.get("members", []) if m.get("character_id") != ch["id"]]
        doc["member_count"] = len(doc["members"])
        doc["hall_unlocked"] = doc["member_count"] >= 3
        if doc["member_count"] == 0:
            await db.guilds.delete_one({"_id": ObjectId(ch["guild_id"])})
        else:
            # promote first remaining to grandmaster if leader left
            if doc.get("leader_id") == ch["id"]:
                if doc["members"]:
                    doc["leader_id"] = doc["members"][0]["character_id"]
                    doc["members"][0]["rank"] = "grandmaster"
            await db.guilds.update_one({"_id": ObjectId(ch["guild_id"])}, {"$set": doc})
    ch["guild_id"] = None
    ch["guild_rank"] = None
    await db.characters.update_one({"_id": ObjectId(ch["id"])}, {"$set": {"guild_id": None, "guild_rank": None}})
    return {"character": ch}


@api.post("/game/guilds/{guild_id}/donate")
async def donate_guild(guild_id: str, request: Request, user: dict = Depends(_get_current_user)):
    body = await request.json()
    amt = int(body.get("amount", 0))
    if amt <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")
    ch = await _get_character_or_404(user["_id"])
    if ch.get("guild_id") != guild_id:
        raise HTTPException(status_code=403, detail="You are not in this guild")
    if ch["gold"] < amt:
        raise HTTPException(status_code=400, detail="Not enough gold")
    ch["gold"] -= amt
    await db.guilds.update_one({"_id": ObjectId(guild_id)}, {"$inc": {"treasury": amt}})
    await db.characters.update_one({"_id": ObjectId(ch["id"])}, {"$set": {"gold": ch["gold"]}})
    return {"character": ch, "donated": amt}


# ============================================================
# HERITAGE SYSTEM — Continental Heritage Months
# ============================================================

# --- DB helpers ---

async def _heritage_get_tokens(character_id: str) -> dict:
    """Get or initialize heritage token balances for a character."""
    doc = await db.heritage_tokens.find_one({"character_id": character_id})
    if not doc:
        doc = {"character_id": character_id}
        for cid in get_all_heritage_continents():
            doc[cid] = 0
        await db.heritage_tokens.insert_one(doc)
    return {k: v for k, v in doc.items() if k != "_id"}


async def _heritage_add_tokens(character_id: str, continent: str, amount: int) -> dict:
    """Add heritage tokens for a character."""
    token_id = continent
    await db.heritage_tokens.update_one(
        {"character_id": character_id},
        {"$inc": {token_id: amount}},
        upsert=True,
    )
    return await _heritage_get_tokens(character_id)


async def _heritage_spend_tokens(character_id: str, continent: str, amount: int) -> bool:
    """Spend heritage tokens. Returns True if successful, False if insufficient."""
    tokens = await _heritage_get_tokens(character_id)
    if tokens.get(continent, 0) < amount:
        return False
    await db.heritage_tokens.update_one(
        {"character_id": character_id},
        {"$inc": {continent: -amount}},
    )
    return True


async def _heritage_get_progress(character_id: str, continent: str, year: int) -> dict:
    """Get or initialize heritage progress for a character/continent/year."""
    key = f"{character_id}_{continent}_{year}"
    today_str = date.today().isoformat()
    doc = await db.heritage_progress.find_one({"key": key})
    if not doc:
        doc = {
            "key": key,
            "character_id": character_id,
            "continent": continent,
            "year": year,
            "daily_quests_completed": 0,
            "boss_kills": 0,
            "events_participated": 0,
            "resources_gathered": 0,
            "items_crafted": 0,
            "tokens_earned": 0,
            "meta_complete": False,
            "daily_quest_claims": {},
            "daily_counters": {"date": today_str, "kills": 0, "gathered": 0, "crafted": 0},
            "updated_at": datetime.now(timezone.utc),
        }
        await db.heritage_progress.insert_one(doc)
    # Reset daily counters if the date has changed
    daily = doc.get("daily_counters", {})
    if daily.get("date") != today_str:
        daily = {"date": today_str, "kills": 0, "gathered": 0, "crafted": 0}
        await db.heritage_progress.update_one({"key": key}, {"$set": {"daily_counters": daily}})
        doc["daily_counters"] = daily
    return {k: v for k, v in doc.items() if k != "_id"}


async def _heritage_update_progress(character_id: str, continent: str, year: int, **fields) -> dict:
    """Update heritage progress fields."""
    key = f"{character_id}_{continent}_{year}"
    today_str = date.today().isoformat()
    inc_fields = {}
    set_fields = {"updated_at": datetime.now(timezone.utc)}
    daily_inc = {}
    for k, v in fields.items():
        if isinstance(v, (int, float)) and k in ("daily_quests_completed", "boss_kills",
                                                   "events_participated", "resources_gathered",
                                                   "items_crafted", "tokens_earned"):
            inc_fields[k] = v
            # Map yearly fields to daily counter fields
            if k == "boss_kills":
                daily_inc["daily_counters.kills"] = v
            elif k == "resources_gathered":
                daily_inc["daily_counters.gathered"] = v
            elif k == "items_crafted":
                daily_inc["daily_counters.crafted"] = v
        else:
            set_fields[k] = v
    # Ensure daily_counters is for today (reset if stale)
    progress = await _heritage_get_progress(character_id, continent, year)
    if progress.get("daily_counters", {}).get("date") != today_str:
        set_fields["daily_counters"] = {"date": today_str, "kills": 0, "gathered": 0, "crafted": 0}
    update = {}
    if inc_fields:
        update["$inc"] = inc_fields
    if daily_inc and "daily_counters" not in set_fields:
        update.setdefault("$inc", {}).update(daily_inc)
    update["$set"] = set_fields
    await db.heritage_progress.update_one({"key": key}, update, upsert=True)
    return await _heritage_get_progress(character_id, continent, year)


async def _heritage_get_milestones(character_id: str) -> dict:
    """Get or initialize heritage milestone tracking for a character."""
    doc = await db.heritage_milestones.find_one({"character_id": character_id})
    if not doc:
        doc = {
            "character_id": character_id,
            "continents": {},
            "master_achieved_years": [],
            "claimed_rewards": [],
        }
        for cid in get_all_heritage_continents():
            doc["continents"][cid] = {
                "years_participated": 0,
                "participated_years": [],
                "last_participated_year": None,
            }
        await db.heritage_milestones.insert_one(doc)
    return {k: v for k, v in doc.items() if k != "_id"}


async def _heritage_record_participation(character_id: str, continent: str, year: int):
    """Record that a character participated in a continent's heritage month for a given year."""
    ms = await _heritage_get_milestones(character_id)
    cont_data = ms["continents"].get(continent, {})
    participated = cont_data.get("participated_years", [])
    if year not in participated:
        participated.append(year)
    await db.heritage_milestones.update_one(
        {"character_id": character_id},
        {"$set": {
            f"continents.{continent}.participated_years": participated,
            f"continents.{continent}.years_participated": len(participated),
            f"continents.{continent}.last_participated_year": year,
        }},
        upsert=True,
    )


async def _heritage_check_master(character_id: str, year: int) -> bool:
    """Check if character participated in all 8 heritage months in a given year."""
    ms = await _heritage_get_milestones(character_id)
    count = 0
    for cid in get_all_heritage_continents():
        if year in ms["continents"].get(cid, {}).get("participated_years", []):
            count += 1
    return count >= 8


# --- Heritage endpoints ---

@api.get("/game/heritage/current")
async def heritage_current(user: dict = Depends(_get_current_user)):
    """Get current heritage month info + active bonuses."""
    hm = get_active_heritage_month()
    if not hm:
        return {"active": False, "message": "No heritage month active. September is a break month."}
    continent = hm["continent"]
    boss = get_heritage_boss(continent)
    bonuses = get_heritage_bonuses(continent)
    return {
        "active": True,
        "continent": continent,
        "name": hm["name"],
        "theme": hm["theme"],
        "desc": hm["desc"],
        "decoration": hm["decoration"],
        "month": HERITAGE_MONTH_BY_CONTINENT[continent],
        "bonuses": bonuses,
        "boss": {
            "id": boss["id"],
            "name": boss["name"],
            "biome": boss["biome"],
            "power": boss["power"],
            "hp": boss["hp"],
            "mechanic": boss["mechanic"],
        } if boss else None,
    }


@api.get("/game/heritage/tokens")
async def heritage_tokens(user: dict = Depends(_get_current_user)):
    """Get player's heritage token balances for all 8 continents."""
    ch = await _get_character_or_404(user["_id"])
    tokens = await _heritage_get_tokens(ch["id"])
    return {"tokens": tokens}


@api.get("/game/heritage/progress")
async def heritage_progress(user: dict = Depends(_get_current_user)):
    """Get player's meta-achievement progress for the current heritage month."""
    ch = await _get_character_or_404(user["_id"])
    hm = get_active_heritage_month()
    if not hm:
        return {"active": False}
    continent = hm["continent"]
    year = date.today().year
    progress = await _heritage_get_progress(ch["id"], continent, year)
    meta = get_heritage_meta_achievement(continent, year)
    ladder_score = get_heritage_ladder_score(progress)
    return {
        "active": True,
        "continent": continent,
        "year": year,
        "progress": progress,
        "meta": meta,
        "ladder_score": ladder_score,
    }


@api.get("/game/heritage/milestones")
async def heritage_milestones(user: dict = Depends(_get_current_user)):
    """Get player's milestone progress across all continents."""
    ch = await _get_character_or_404(user["_id"])
    ms = await _heritage_get_milestones(ch["id"])
    return {
        "milestones": ms,
        "definitions": HERITAGE_MILESTONES,
        "master_achievement": HERITAGE_MASTER_ACHIEVEMENT,
    }


# --- Heritage vendor ---

@api.get("/game/heritage/vendor/{continent}")
async def heritage_vendor(continent: str, user: dict = Depends(_get_current_user)):
    """Browse vendor items for a continent's heritage vendor."""
    ch = await _get_character_or_404(user["_id"])
    items = get_heritage_vendor_items(continent)
    if not items and continent not in get_all_heritage_continents():
        raise HTTPException(status_code=404, detail="Unknown continent")
    tokens = await _heritage_get_tokens(ch["id"])
    purchased = await db.heritage_purchases.find(
        {"character_id": ch["id"], "continent": continent}
    ).to_list(length=None)
    purchased_ids = {p["item_id"] for p in purchased}
    return {
        "continent": continent,
        "items": items,
        "token_balance": tokens.get(continent, 0),
        "purchased": list(purchased_ids),
    }


@api.post("/game/heritage/vendor/{continent}/buy")
async def heritage_vendor_buy(continent: str, request: Request, user: dict = Depends(_get_current_user)):
    """Purchase an item from a continent's heritage vendor."""
    ch = await _get_character_or_404(user["_id"])
    body = await request.json()
    item_id = body.get("item_id")
    if not item_id:
        raise HTTPException(status_code=400, detail="item_id required")
    item = get_heritage_vendor_item(continent, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    # Check if already purchased (one-time purchases)
    existing = await db.heritage_purchases.find_one({
        "character_id": ch["id"], "item_id": item_id,
    })
    if existing:
        raise HTTPException(status_code=400, detail="Already purchased")
    # Check token balance
    tokens = await _heritage_get_tokens(ch["id"])
    if tokens.get(continent, 0) < item["cost"]:
        raise HTTPException(status_code=400, detail=f"Insufficient tokens. Need {item['cost']}, have {tokens.get(continent, 0)}")
    # Spend tokens
    success = await _heritage_spend_tokens(ch["id"], continent, item["cost"])
    if not success:
        raise HTTPException(status_code=400, detail="Failed to spend tokens")
    # Record purchase
    await db.heritage_purchases.insert_one({
        "character_id": ch["id"],
        "continent": continent,
        "item_id": item_id,
        "item_name": item["name"],
        "category": item["category"],
        "cost": item["cost"],
        "purchased_at": datetime.now(timezone.utc),
    })
    # Apply effects based on category
    if item["category"] == "title":
        titles = ch.get("titles", [])
        if item["name"] not in titles:
            titles.append(item["name"])
        await db.characters.update_one(
            {"_id": ObjectId(ch["id"])},
            {"$set": {"titles": titles}},
        )
    elif item["category"] == "buff":
        heritage_buffs = ch.get("heritage_buffs", {})
        heritage_buffs[f"{continent}_{item['id']}"] = True
        await db.characters.update_one(
            {"_id": ObjectId(ch["id"])},
            {"$set": {"heritage_buffs": heritage_buffs}},
        )
    elif item["category"] == "material":
        inv = ch.get("inventory", [])
        inv.append({"item_id": item_id, "qty": 1})
        await db.characters.update_one(
            {"_id": ObjectId(ch["id"])},
            {"$set": {"inventory": inv}},
        )
    elif item["category"] == "pet":
        pets = ch.get("pets", [])
        pets.append({"id": item_id, "name": item["name"], "source": "heritage_vendor"})
        await db.characters.update_one(
            {"_id": ObjectId(ch["id"])},
            {"$set": {"pets": pets}},
        )
    # Refresh character
    ch = await _get_character_or_404(user["_id"])
    new_tokens = await _heritage_get_tokens(ch["id"])
    return {
        "character": ch,
        "purchased_item": item,
        "token_balance": new_tokens.get(continent, 0),
        "message": f"Purchased {item['name']}!",
    }


# --- Heritage boss ---

@api.get("/game/heritage/boss")
async def heritage_boss_info(user: dict = Depends(_get_current_user)):
    """Get current heritage boss info + player's kill count."""
    ch = await _get_character_or_404(user["_id"])
    hm = get_active_heritage_month()
    if not hm:
        return {"active": False}
    continent = hm["continent"]
    boss = get_heritage_boss(continent)
    if not boss:
        return {"active": False}
    year = date.today().year
    progress = await _heritage_get_progress(ch["id"], continent, year)
    return {
        "active": True,
        "boss": {
            "id": boss["id"],
            "name": boss["name"],
            "biome": boss["biome"],
            "continent": boss["continent"],
            "power": boss["power"],
            "hp": boss["hp"],
            "mechanic": boss["mechanic"],
            "token_reward": boss.get("heritage_token_count", 5),
        },
        "kill_count": progress.get("boss_kills", 0),
        "continent": continent,
    }


@api.post("/game/heritage/boss/start")
async def heritage_boss_start(user: dict = Depends(_get_current_user)):
    """Start combat with the heritage boss."""
    ch = await _get_character_or_404(user["_id"])
    hm = get_active_heritage_month()
    if not hm:
        raise HTTPException(status_code=400, detail="No heritage month active")
    continent = hm["continent"]
    boss = get_heritage_boss(continent)
    if not boss:
        raise HTTPException(status_code=400, detail="No heritage boss available")
    # Check player is on the right continent
    if ch.get("current_continent") != continent:
        raise HTTPException(status_code=400, detail=f"You must be in {continent} to fight the heritage boss")
    # Check level requirement
    level_reqs = {
        "valeria": 3, "mushkara": 5, "concordia": 8, "khardrum": 10,
        "haya": 15, "gennel": 20, "hylion": 25, "daw_ul_talalu": 30,
    }
    if ch["level"] < level_reqs.get(continent, 1):
        raise HTTPException(status_code=400, detail=f"Requires level {level_reqs.get(continent, 1)}")
    # Build boss monster dict for combat system
    monster = {
        "id": boss["id"],
        "name": boss["name"],
        "biome": boss["biome"],
        "power": boss["power"],
        "hp": boss["hp"],
        "max_hp": boss["hp"],
        "is_boss": True,
        "is_heritage_boss": True,
        "drops": boss["drops"],
        "heritage_continent": continent,
        "heritage_token_count": boss.get("heritage_token_count", 5),
    }
    state = start_combat(ch, monster)
    if "error" in state:
        raise HTTPException(status_code=400, detail=state["error"])
    state["biome_id"] = boss["biome"]
    combat_doc = {"user_id": user["_id"], "character_id": ch["id"], "state": state,
                  "created_at": datetime.now(timezone.utc).isoformat()}
    r = await db.combats.insert_one(combat_doc)
    state["combat_id"] = str(r.inserted_id)
    return {"combat": state, "character": ch}


# --- Heritage daily quests ---

@api.get("/game/heritage/quests/daily")
async def heritage_daily_quests(user: dict = Depends(_get_current_user)):
    """Get today's 3 heritage quests + completion status."""
    ch = await _get_character_or_404(user["_id"])
    hm = get_active_heritage_month()
    if not hm:
        return {"active": False}
    continent = hm["continent"]
    templates = get_heritage_daily_quests(continent)
    today_str = date.today().isoformat()
    year = date.today().year
    progress = await _heritage_get_progress(ch["id"], continent, year)
    print(f"[DEBUG heritage quests] ch_id={ch['id']} continent={continent} progress={progress}")
    claims = progress.get("daily_quest_claims", {})
    daily = progress.get("daily_counters", {})
    quests = []
    for tmpl in templates:
        quest_id = f"heritage_{continent}_{tmpl['id_suffix']}_{today_str}"
        claimed = claims.get(quest_id, False)
        if tmpl["kind"] == "kill":
            current = daily.get("kills", 0) + daily.get("gathered", 0)
        elif tmpl["kind"] == "gather":
            current = daily.get("gathered", 0)
        elif tmpl["kind"] == "craft":
            current = daily.get("crafted", 0)
        else:
            current = 0
        current = min(current, tmpl["count"])
        print(f"[DEBUG heritage quests] quest={tmpl['name']} kind={tmpl['kind']} current={current} count={tmpl['count']}")
        quests.append({
            "id": quest_id,
            "name": tmpl["name"],
            "brief": tmpl["brief"],
            "kind": tmpl["kind"],
            "count": tmpl["count"],
            "current": current,
            "token_reward": tmpl["token_reward"],
            "biome_filter": tmpl.get("biome_filter"),
            "claimed": claimed,
        })
    all_claimed = all(q["claimed"] for q in quests) if quests else False
    return {
        "active": True,
        "continent": continent,
        "date": today_str,
        "quests": quests,
        "all_claimed": all_claimed,
        "bonus_tokens": 5 if all_claimed else 0,
    }


@api.post("/game/heritage/quests/claim")
async def heritage_quest_claim(request: Request, user: dict = Depends(_get_current_user)):
    """Claim a completed heritage daily quest reward."""
    ch = await _get_character_or_404(user["_id"])
    body = await request.json()
    quest_id = body.get("quest_id")
    if not quest_id:
        raise HTTPException(status_code=400, detail="quest_id required")
    hm = get_active_heritage_month()
    if not hm:
        raise HTTPException(status_code=400, detail="No heritage month active")
    continent = hm["continent"]
    year = date.today().year
    progress = await _heritage_get_progress(ch["id"], continent, year)
    claims = progress.get("daily_quest_claims", {})
    if claims.get(quest_id):
        raise HTTPException(status_code=400, detail="Quest already claimed")
    # Find the quest template
    templates = get_heritage_daily_quests(continent)
    today_str = date.today().isoformat()
    tmpl = None
    for t in templates:
        if quest_id == f"heritage_{continent}_{t['id_suffix']}_{today_str}":
            tmpl = t
            break
    if not tmpl:
        raise HTTPException(status_code=400, detail="Quest not found or expired")
    # Verify the player has enough daily progress for this quest type
    daily = progress.get("daily_counters", {})
    if tmpl["kind"] == "kill":
        cur = daily.get("kills", 0) + daily.get("gathered", 0)
        if cur < tmpl["count"]:
            raise HTTPException(status_code=400, detail=f"You haven't defeated enough creatures yet ({cur}/{tmpl['count']})")
    elif tmpl["kind"] == "gather":
        cur = daily.get("gathered", 0)
        if cur < tmpl["count"]:
            raise HTTPException(status_code=400, detail=f"You haven't gathered enough yet ({cur}/{tmpl['count']})")
    elif tmpl["kind"] == "craft":
        cur = daily.get("crafted", 0)
        if cur < tmpl["count"]:
            raise HTTPException(status_code=400, detail=f"You haven't crafted enough yet ({cur}/{tmpl['count']})")
    token_reward = tmpl["token_reward"]
    await _heritage_add_tokens(ch["id"], continent, token_reward)
    await _heritage_update_progress(
        ch["id"], continent, year,
        daily_quests_completed=1,
        tokens_earned=token_reward,
    )
    # Mark quest as claimed
    claims[quest_id] = True
    await _heritage_update_progress(ch["id"], continent, year, daily_quest_claims=claims)
    # Record participation
    await _heritage_record_participation(ch["id"], continent, year)
    # Check if all 3 quests claimed today → bonus
    all_claimed = all(
        claims.get(f"heritage_{continent}_{t['id_suffix']}_{today_str}")
        for t in templates
    )
    bonus = 0
    if all_claimed:
        bonus = 5
        await _heritage_add_tokens(ch["id"], continent, bonus)
        await _heritage_update_progress(ch["id"], continent, year, tokens_earned=bonus)
    new_tokens = await _heritage_get_tokens(ch["id"])
    return {
        "claimed": quest_id,
        "tokens_earned": token_reward + bonus,
        "bonus": bonus > 0,
        "token_balance": new_tokens.get(continent, 0),
    }


# --- Heritage ladder ---

@api.get("/game/heritage/ladder")
async def heritage_ladder(user: dict = Depends(_get_current_user)):
    """Get current heritage month ladder rankings."""
    hm = get_active_heritage_month()
    if not hm:
        return {"active": False}
    continent = hm["continent"]
    year = date.today().year
    # Aggregate progress docs for this continent+year, sorted by score
    cursor = db.heritage_progress.find(
        {"continent": continent, "year": year}
    ).limit(100)
    docs = await cursor.to_list(length=100)
    # Get character names
    char_ids = [d["character_id"] for d in docs]
    chars = await db.characters.find(
        {"_id": {"$in": [ObjectId(cid) for cid in char_ids if ObjectId.is_valid(cid)]}},
        {"name": 1}
    ).to_list(length=None)
    name_map = {str(c["_id"]): c.get("name", "Unknown") for c in chars}
    entries = []
    for d in docs:
        score = get_heritage_ladder_score(d)
        entries.append({
            "character_id": d["character_id"],
            "name": name_map.get(d["character_id"], "Unknown"),
            "score": score,
            "tokens_earned": d.get("tokens_earned", 0),
            "boss_kills": d.get("boss_kills", 0),
            "daily_quests_completed": d.get("daily_quests_completed", 0),
        })
    entries.sort(key=lambda x: x["score"], reverse=True)
    return {
        "active": True,
        "continent": continent,
        "year": year,
        "rankings": entries[:50],
    }


@api.get("/game/heritage/history")
async def heritage_history(user: dict = Depends(_get_current_user)):
    """Get past heritage month results (hall of fame)."""
    # Get archived heritage progress grouped by continent+year
    pipeline = [
        {"$group": {
            "_id": {"continent": "$continent", "year": "$year"},
            "top_score": {"$max": 1},  # placeholder, real scoring done in app
            "participant_count": {"$sum": 1},
        }},
        {"$sort": {"_id.year": -1, "_id.continent": 1}},
    ]
    results = await db.heritage_progress.aggregate(pipeline).to_list(length=None)
    history = []
    for r in results:
        history.append({
            "continent": r["_id"]["continent"],
            "year": r["_id"]["year"],
            "participants": r["participant_count"],
        })
    return {"history": history}


# --- Heritage milestones ---

@api.post("/game/heritage/milestones/claim")
async def heritage_milestone_claim(request: Request, user: dict = Depends(_get_current_user)):
    """Claim a milestone reward for a continent."""
    ch = await _get_character_or_404(user["_id"])
    body = await request.json()
    continent = body.get("continent")
    years = body.get("years")
    if not continent or not years:
        raise HTTPException(status_code=400, detail="continent and years required")
    ms = await _heritage_get_milestones(ch["id"])
    cont_data = ms["continents"].get(continent, {})
    actual_years = cont_data.get("years_participated", 0)
    if actual_years < years:
        raise HTTPException(status_code=400, detail=f"Only {actual_years} years participated, need {years}")
    claim_key = f"{continent}_{years}"
    if claim_key in ms.get("claimed_rewards", []):
        raise HTTPException(status_code=400, detail="Already claimed")
    # Find milestone definition
    milestone = None
    for m in HERITAGE_MILESTONES:
        if m["years"] == years:
            milestone = m
            break
    if not milestone:
        raise HTTPException(status_code=400, detail="Unknown milestone")
    # Record claim
    await db.heritage_milestones.update_one(
        {"character_id": ch["id"]},
        {"$push": {"claimed_rewards": claim_key}},
    )
    return {
        "claimed": claim_key,
        "milestone": milestone,
        "message": f"Claimed {milestone['name']} for {continent}!",
    }


@api.get("/game/heritage/calendar")
async def heritage_calendar(user: dict = Depends(_get_current_user)):
    """Get the full heritage calendar (all 8 months)."""
    calendar = []
    for month in sorted(HERITAGE_MONTHS.keys()):
        hm = HERITAGE_MONTHS[month]
        calendar.append({
            "month": month,
            "continent": hm["continent"],
            "name": hm["name"],
            "theme": hm["theme"],
            "decoration": hm["decoration"],
        })
    return {"calendar": calendar, "master_achievement": HERITAGE_MASTER_ACHIEVEMENT}


@api.post("/game/heritage/dismiss")
async def heritage_dismiss_arrival(request: Request, user: dict = Depends(_get_current_user)):
    """Dismiss the heritage arrival modal for a specific continent+year."""
    body = await request.json()
    continent = body.get("continent")
    year = int(body.get("year", date.today().year))
    if not continent:
        raise HTTPException(status_code=400, detail="continent required")
    ch = await _get_character_or_404(user["_id"])
    key = f"{continent}_{year}"
    dismissed = ch.get("heritage_dismissed", [])
    if key not in dismissed:
        dismissed.append(key)
        await db.characters.update_one(
            {"_id": ObjectId(ch["id"])},
            {"$set": {"heritage_dismissed": dismissed}},
        )
    return {"ok": True, "dismissed": dismissed}


# ---------------- ROOT ----------------
@api.get("/")
async def root():
    return {"service": "Erchis RPG", "status": "ok"}


@api.get("/health")
async def health():
    return {"status": "healthy"}


# ---------------- WIRE ----------------
# CORS — support multiple origins (comma-separated in FRONTEND_URL env var) PLUS
# a regex allow for any Emergent-hosted preview/production domain. This handles
# the production case where the API is at a custom domain (e.g. erchis.online)
# but the app is served from *.emergent.host / *.emergentagent.com.
_frontend_url_env = os.environ.get("FRONTEND_URL", "http://localhost:3000")
_env_origins = [o.strip() for o in _frontend_url_env.split(",") if o.strip()]
origins = list({*_env_origins, "http://localhost:3000", "https://erchis.online"})
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=r"^https://([a-z0-9-]+\.)*(emergent\.host|emergentagent\.com|erchis\.online)$",
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
)

app.include_router(api)


@app.on_event("startup")
async def startup():
    await db.users.create_index("email", unique=True)
    await db.characters.create_index("user_id", unique=True)
    await db.world_events.create_index("created_at")
    # One-time migration: rename any legacy "exhausted" debuff → "weary" (the
    # numeric racial `exhaustion` meter kept the old name, this only touches
    # the status badge that read "EXHAUSTED" and confused players).
    mig = await db.characters.update_many(
        {"statuses.id": "exhausted"},
        {"$set": {"statuses.$[el].id": "weary", "statuses.$[el].name": "Weary"}},
        array_filters=[{"el.id": "exhausted"}],
    )
    if mig.modified_count:
        logger.info("Renamed legacy 'exhausted' status on %d characters.", mig.modified_count)
    # Canon v2 migration: rewrite legacy continent/biome/town IDs on every
    # existing character record. Idempotent — safe to run every boot.
    from world_data import CONTINENT_ID_MAP, BIOME_ID_MAP, TOWN_ID_MAP  # noqa: E402
    total_updated = 0
    async for ch_doc in db.characters.find({}):
        updates = {}
        # continent
        cc = ch_doc.get("current_continent")
        if cc in CONTINENT_ID_MAP:
            updates["current_continent"] = CONTINENT_ID_MAP[cc]
        # biome
        cb = ch_doc.get("current_biome")
        if cb in BIOME_ID_MAP:
            updates["current_biome"] = BIOME_ID_MAP[cb]
        # town
        ct = ch_doc.get("current_town")
        if ct in TOWN_ID_MAP:
            updates["current_town"] = TOWN_ID_MAP[ct]
        # home_town
        ht = ch_doc.get("home_town")
        if ht in TOWN_ID_MAP:
            updates["home_town"] = TOWN_ID_MAP[ht]
        # visited_towns
        vt = ch_doc.get("visited_towns") or []
        new_vt = [TOWN_ID_MAP.get(t, t) for t in vt]
        if new_vt != vt:
            updates["visited_towns"] = new_vt
        # Phase-B seed: reputation dict for existing characters that never had one
        rep = ch_doc.get("reputation") or {}
        if not rep:
            from world_travel import initial_reputation_for_race
            from game_data_p2 import default_home_continent_for_race
            new_cc = updates.get("current_continent") or ch_doc.get("current_continent")
            race = ch_doc.get("race", "human")
            updates["reputation"] = initial_reputation_for_race(
                race,
                default_home_continent_for_race(race),
                [c["id"] for c in CONTINENTS if not c.get("locked")],
            )
        # Phase-B seed: known_waystones / active_waystones fields (default empty)
        if "known_waystones" not in ch_doc:
            updates["known_waystones"] = []
        if "active_waystones" not in ch_doc:
            updates["active_waystones"] = []
        # Phase-F seed: NPC relationships + quest state (default empty for existing chars)
        if "npc_relationships" not in ch_doc:
            updates["npc_relationships"] = initial_npc_relationships()
        if "active_npc_quests" not in ch_doc:
            updates["active_npc_quests"] = []
        if "completed_npc_quests" not in ch_doc:
            updates["completed_npc_quests"] = []
        if "npc_quest_progress" not in ch_doc:
            updates["npc_quest_progress"] = {}
        if updates:
            await db.characters.update_one({"_id": ch_doc["_id"]}, {"$set": updates})
            total_updated += 1
    if total_updated:
        logger.info("Canon v2 rename applied on %d character(s).", total_updated)

    # Item system migration: ensure item_instances field exists on all characters
    item_mig = await db.characters.update_many(
        {"item_instances": {"$exists": False}},
        {"$set": {"item_instances": []}},
    )
    if item_mig.modified_count:
        logger.info("Added item_instances field to %d character(s).", item_mig.modified_count)

    # Item system migration: give compensation gems to existing characters who
    # don't have any gems in their inventory yet (one-time)
    from game_data import GEMS  # noqa: E402
    _compensation_gem_ids = [g["id"] for g in GEMS[:3]]  # first 3 gems as compensation
    async for ch_doc in db.characters.find({"item_system_migrated": {"$ne": True}}):
        ch_inv = ch_doc.get("inventory") or []
        _has_gems = any(
            (slot.get("item_id", "") in _compensation_gem_ids)
            for slot in ch_inv
        )
        _updates = {}
        if not _has_gems:
            for gid in _compensation_gem_ids:
                _existing = next((s for s in ch_inv if s.get("item_id") == gid), None)
                if _existing:
                    _existing["quantity"] = _existing.get("quantity", 0) + 1
                else:
                    ch_inv.append({"item_id": gid, "quantity": 1, "favorite": False})
            _updates["inventory"] = ch_inv
        _updates["item_system_migrated"] = True
        await db.characters.update_one({"_id": ch_doc["_id"]}, {"$set": _updates})
    logger.info("Item system migration complete.")

    logger.info("Erchis server up. Allowed origins: %s", origins)


@app.on_event("shutdown")
async def shutdown():
    client.close()
