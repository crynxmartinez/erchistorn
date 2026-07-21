"""Erchis Fantasy Dice RPG — main FastAPI server."""
from __future__ import annotations

import logging
import os
import random
import sys
from datetime import date, datetime, timezone
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / ".env")
sys.path.insert(0, str(ROOT_DIR))

from bson import ObjectId  # noqa: E402
from fastapi import APIRouter, Depends, FastAPI, HTTPException, Request, Response  # noqa: E402
from motor.motor_asyncio import AsyncIOMotorClient  # noqa: E402
from starlette.middleware.cors import CORSMiddleware  # noqa: E402

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
    BIOME_ACTIONS,
    CONTINENTS,
    DAILY_MISSION_POOL,
    ITEMS,
    ITEMS_BY_ID,
    LOGIN_REWARDS,
    MASTERIES,
    MONSTERS,
    PORTRAITS,
    RACES,
    RECIPES,
    ROLES,
    SKILLS,
    SKILLS_BY_ID,
    TEACHERS,
    compute_starting_hp,
    get_mastery,
    get_race,
    get_role,
)
from game_engine import combat_turn, resolve_action, resolve_craft, start_combat  # noqa: E402
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
    rep_level_from_points,
)
from professions import (  # noqa: E402
    PROFESSIONS,
    PROFESSIONS_BY_ID,
    PROFESSION_RANKS,
    profession_slots_unlocked,
    learn_profession,
    abandon_profession,
    gain_profession_xp,
    rank_from_xp,
    apply_exploration_progress,
    exploration_delta_from_outcome,
    EXPLORATION_THRESHOLDS,
    is_biome_unlocked_for_gathering,
)
from models import (  # noqa: E402
    ActionPayload,
    CombatStartPayload,
    CombatTurnPayload,
    CraftPayload,
    CreateCharacterPayload,
    LearnSkillPayload,
    LoginPayload,
    RegisterPayload,
)

# ---------------- setup ----------------
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("erchis")

mongo_url = os.environ["MONGO_URL"]
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ["DB_NAME"]]

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


async def _get_character_or_404(user_id: str) -> dict:
    ch = await db.characters.find_one({"user_id": user_id})
    if not ch:
        raise HTTPException(status_code=404, detail="Character not found — create one first")
    ch = _serialize_doc(ch)
    ensure_racial_defaults(ch)
    return ch


def _today_str() -> str:
    return date.today().isoformat()


def _xp_for_next(level: int) -> int:
    return 100 + (level - 1) * 40


def _apply_rewards_to_character(character: dict, rewards: dict) -> None:
    character["gold"] = character.get("gold", 0) + int(rewards.get("gold", 0))
    character["xp"] = character.get("xp", 0) + int(rewards.get("xp", 0))
    while character["xp"] >= _xp_for_next(character["level"]):
        character["xp"] -= _xp_for_next(character["level"])
        character["level"] += 1
        stat_keys = ["vitality", "cognition", "essence", "drive"]
        pick = random.choice(stat_keys)
        character["stats"][pick] += 1
        character["max_hp"] = compute_starting_hp(character["stats"]) + (character["level"] - 1) * 4
    for it in rewards.get("items", []) or []:
        if isinstance(it, (list, tuple)):
            item_id, qty = it[0], it[1]
        else:
            item_id, qty = it, 1
        _add_item_to_inventory(character, item_id, int(qty))


def _apply_status_to_character(character: dict, new_status: dict) -> None:
    """Add a status, or refresh duration if it already exists (no duplicates)."""
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


def _add_item_to_inventory(character: dict, item_id: str, qty: int) -> None:
    if not item_id:
        return
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
    return {"biome_id": biome_id, "actions": BIOME_ACTIONS.get(biome_id, [])}


@api.get("/game/data/items")
async def get_items(user: dict = Depends(_get_current_user)):
    return {"items": ITEMS}


@api.get("/game/data/skills")
async def get_skills_route(user: dict = Depends(_get_current_user)):
    return {"skills": SKILLS}


@api.get("/game/data/recipes")
async def get_recipes(user: dict = Depends(_get_current_user)):
    return {"recipes": RECIPES}


@api.get("/game/data/teachers")
async def get_teachers(user: dict = Depends(_get_current_user)):
    return {"teachers": TEACHERS}


@api.get("/game/data/monsters")
async def get_monsters(user: dict = Depends(_get_current_user)):
    return {"monsters": MONSTERS}


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
        "level": 1,
        "xp": 0,
        "gold": 75,
        "hp": max_hp,
        "max_hp": max_hp,
        "stats": stats,
        "inventory": [
            {"item_id": "traveler_garb", "quantity": 1},
            {"item_id": "iron_dagger", "quantity": 1},
            {"item_id": "minor_healing_potion", "quantity": 2},
            {"item_id": "wild_herb", "quantity": 3},
        ],
        "equipped": {"weapon": "iron_dagger", "armor": "traveler_garb", "trinket": None},
        "skills": skills,
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
        "current_town": None,
        "visited_towns": [default_home_town_for_race(payload.race)],
        "known_waystones": [],
        "active_waystones": [],
        "teleporter_last_used": None,
        "professions": [],                 # Phase D — up to 3 slots
        "abandoned_professions": {},       # keeps 25% xp for relearn
        "exploration_progress": {},        # Phase C — per-biome %
        "guild_id": None,
        "guild_rank": None,
        "active_quests": [],
        "completed_quests": [],
        "kills": 0,
        "crafts": 0,
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
    await db.characters.update_one({"_id": ObjectId(ch["id"])}, {"$set": {
        "login_streak": ch["login_streak"],
        "last_login_date": ch["last_login_date"],
        "last_daily_refresh": ch["last_daily_refresh"],
        "daily_missions": ch.get("daily_missions", []),
        "_biomes_today": ch.get("_biomes_today", []),
        "gold": ch["gold"],
        "xp": ch["xp"],
        "level": ch["level"],
        "stats": ch["stats"],
        "max_hp": ch["max_hp"],
        "inventory": ch["inventory"],
    }})
    return {"character": ch, "login_reward": reward}


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
    valid_biomes = [b["id"] for b in cont.get("biomes", [])]
    if valid_biomes and biome not in valid_biomes:
        biome = valid_biomes[0]
    ch["current_continent"] = continent
    ch["current_biome"] = biome or ch["current_biome"]
    _update_daily_mission_progress(ch, {"kind": "explore", "biome": ch["current_biome"]})
    await db.characters.update_one({"_id": ObjectId(ch["id"])}, {"$set": {
        "current_continent": ch["current_continent"],
        "current_biome": ch["current_biome"],
        "daily_missions": ch.get("daily_missions", []),
        "_biomes_today": ch.get("_biomes_today", []),
    }})
    return {"character": ch}


# ---------------- ACTIONS ----------------
@api.post("/game/action")
async def do_action(payload: ActionPayload, user: dict = Depends(_get_current_user)):
    ch = await _get_character_or_404(user["_id"])
    result = resolve_action(ch, payload.action_id, payload.biome_id, payload.target_id)
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

    # Phase D — Profession XP: gathering-family actions grant profession XP for
    # the matching profession the character has learned.
    profession_ranks: list[tuple[str, str]] = []
    action_prof_map = {"gather": ["herbalism", "logging", "mining"], "fish": ["fishing"],
                       "hunt": ["hunting"], "loot_ruins": ["excavation"]}
    for pid in action_prof_map.get(payload.action_id, []):
        has = any(p.get("id") == pid for p in ch.get("professions", []))
        if has and result["outcome"] >= 3:
            xp_gain = {3: 4, 4: 8, 5: 14, 6: 22}.get(result["outcome"], 0)
            rank_change = gain_profession_xp(ch, pid, xp_gain)
            if rank_change:
                profession_ranks.append(rank_change)

    # Tick status durations so debuffs (Bleeding, Weary, Poisoned, etc.) expire naturally.
    _tick_character_statuses(ch)

    if ch["hp"] <= 0:
        ch["hp"] = 1

    await db.characters.update_one({"_id": ObjectId(ch["id"])}, {"$set": {
        "hp": ch["hp"], "max_hp": ch["max_hp"], "gold": ch["gold"], "xp": ch["xp"],
        "level": ch["level"], "stats": ch["stats"], "inventory": ch["inventory"],
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
        "exploration_progress": ch.get("exploration_progress", {}),
        "professions": ch.get("professions", []),
    }})

    if result["outcome"] == 6:
        target_disp = result.get("target_name") or "the unknown"
        await _push_world_event(ch["name"], f"{ch['name']} achieved a critical {payload.action_id} against {target_disp}.", "loot")

    return {"result": result, "character": ch, "racial_msgs": racial_msgs,
            "explore_hits": explore_hits, "profession_ranks": profession_ranks}


# ---------------- COMBAT ----------------
@api.post("/game/combat/start")
async def combat_start(payload: CombatStartPayload, user: dict = Depends(_get_current_user)):
    ch = await _get_character_or_404(user["_id"])
    state = start_combat(ch, payload.monster_id)
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
    result = combat_turn(ch, state, payload.manual_skill_id, payload.manual_item_id)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    updates = {
        "hp": ch["hp"], "statuses": ch.get("statuses", []),
        "inventory": ch.get("inventory", []),
    }
    if result.get("victory"):
        _apply_rewards_to_character(ch, result["rewards"])
        ch["kills"] = ch.get("kills", 0) + 1
        _update_daily_mission_progress(ch, {"kind": "kill", "id": combat["state"]["monster_id"], "count": 1})
        _update_quest_progress(ch, {"kind": "kill", "id": combat["state"]["monster_id"], "count": 1})
        updates.update({
            "gold": ch["gold"], "xp": ch["xp"], "level": ch["level"], "stats": ch["stats"],
            "max_hp": ch["max_hp"], "kills": ch["kills"],
            "daily_missions": ch.get("daily_missions", []),
            "active_quests": ch.get("active_quests", []),
            "inner_blood": ch.get("inner_blood", 0),
            "exhaustion": ch.get("exhaustion", 0),
        })
        monster = next((m for m in MONSTERS if m["id"] == combat["state"]["monster_id"]), None)
        m_name = monster["name"] if monster else "a beast"
        await _push_world_event(ch["name"], f"{ch['name']} slew {m_name}.", "kill")
    elif result.get("victory") is False:
        loss = min(ch.get("gold", 0), 20)
        ch["gold"] -= loss
        updates["gold"] = ch["gold"]

    await db.characters.update_one({"_id": ObjectId(ch["id"])}, {"$set": updates})
    await db.combats.update_one({"_id": ObjectId(payload.combat_id)}, {"$set": {"state": state}})

    return {"result": result, "character": ch, "combat_id": payload.combat_id}


# ---------------- CRAFTING ----------------
@api.post("/game/craft")
async def craft(payload: CraftPayload, user: dict = Depends(_get_current_user)):
    ch = await _get_character_or_404(user["_id"])
    result = resolve_craft(ch, payload.recipe_id)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    for mat_id, qty in result["materials_consumed"]:
        _remove_item_from_inventory(ch, mat_id, qty)

    if not result["lost_materials"] and result.get("output_item"):
        _add_item_to_inventory(ch, result["output_item"], 1)
        ch["crafts"] = ch.get("crafts", 0) + 1
        _update_daily_mission_progress(ch, {"kind": "craft", "count": 1})
        _update_quest_progress(ch, {"kind": "craft", "count": 1})

    _apply_rewards_to_character(ch, {"gold": 0, "xp": 10, "items": []})

    await db.characters.update_one({"_id": ObjectId(ch["id"])}, {"$set": {
        "inventory": ch["inventory"], "gold": ch["gold"], "xp": ch["xp"], "level": ch["level"],
        "stats": ch["stats"], "max_hp": ch["max_hp"], "crafts": ch["crafts"],
        "daily_missions": ch.get("daily_missions", []),
    }})

    if result["outcome"] == 6:
        await _push_world_event(ch["name"], f"{ch['name']} crafted a masterwork item.", "craft")

    return {"result": result, "character": ch}


# ---------------- SKILLS ----------------
@api.post("/game/skill/learn")
async def learn_skill(payload: LearnSkillPayload, user: dict = Depends(_get_current_user)):
    ch = await _get_character_or_404(user["_id"])
    skill_id = payload.skill_id
    if skill_id not in SKILLS_BY_ID:
        raise HTTPException(status_code=400, detail="Unknown skill")
    if any(s.get("skill_id") == skill_id for s in ch.get("skills", [])):
        raise HTTPException(status_code=409, detail="Skill already learned")

    if payload.skillbook_item_id:
        item = ITEMS_BY_ID.get(payload.skillbook_item_id)
        if not item or item.get("kind") != "skillbook" or item.get("teaches") != skill_id:
            raise HTTPException(status_code=400, detail="Invalid skillbook for this skill")
        if not _remove_item_from_inventory(ch, payload.skillbook_item_id, 1):
            raise HTTPException(status_code=400, detail="Skillbook not in inventory")
    elif payload.teacher_id:
        teacher = next((t for t in TEACHERS if t["id"] == payload.teacher_id), None)
        if not teacher:
            raise HTTPException(status_code=404, detail="Unknown teacher")
        offer = next((o for o in teacher["teaches"] if o["skill_id"] == skill_id), None)
        if not offer:
            raise HTTPException(status_code=400, detail="This teacher does not teach that skill")
        if ch["level"] < offer["level_req"]:
            raise HTTPException(status_code=403, detail=f"Requires level {offer['level_req']}")
        if ch["gold"] < offer["cost_gold"]:
            raise HTTPException(status_code=400, detail="Not enough gold")
        ch["gold"] -= offer["cost_gold"]
    else:
        raise HTTPException(status_code=400, detail="Provide either teacher_id or skillbook_item_id")

    ch.setdefault("skills", []).append({"skill_id": skill_id, "cooldown_remaining": 0})
    await db.characters.update_one({"_id": ObjectId(ch["id"])}, {"$set": {
        "skills": ch["skills"], "gold": ch["gold"], "inventory": ch["inventory"],
    }})
    return {"character": ch, "learned": skill_id}


# ---------------- INVENTORY ----------------
@api.post("/game/equip")
async def equip(request: Request, user: dict = Depends(_get_current_user)):
    body = await request.json()
    item_id = body.get("item_id")
    slot = body.get("slot")
    if slot not in ("weapon", "armor", "trinket"):
        raise HTTPException(status_code=400, detail="Invalid slot")
    ch = await _get_character_or_404(user["_id"])
    item = ITEMS_BY_ID.get(item_id)
    if not item:
        raise HTTPException(status_code=400, detail="Unknown item")
    if item.get("slot") != slot:
        raise HTTPException(status_code=400, detail=f"Item is not a {slot}")
    if not any(i.get("item_id") == item_id for i in ch.get("inventory", [])):
        raise HTTPException(status_code=400, detail="Item not in inventory")
    ch["equipped"][slot] = item_id
    await db.characters.update_one({"_id": ObjectId(ch["id"])}, {"$set": {"equipped": ch["equipped"]}})
    return {"character": ch}


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
    _apply_rewards_to_character(ch, reward)
    await db.characters.update_one({"_id": ObjectId(ch["id"])}, {"$set": {
        "daily_missions": ch["daily_missions"], "gold": ch["gold"], "xp": ch["xp"],
        "level": ch["level"], "stats": ch["stats"], "max_hp": ch["max_hp"],
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
    return {"heritage_rank_1": HERITAGE_RANK_1}


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
async def available_quests(user: dict = Depends(_get_current_user)):
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
        rows.append(q)
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
    return {"character": ch}


@api.post("/game/quests/{quest_id}/abandon")
async def abandon_quest(quest_id: str, user: dict = Depends(_get_current_user)):
    ch = await _get_character_or_404(user["_id"])
    before = len(ch.get("active_quests", []))
    ch["active_quests"] = [a for a in ch.get("active_quests", []) if a["quest_id"] != quest_id]
    if len(ch["active_quests"]) == before:
        raise HTTPException(status_code=404, detail="Not an active quest")
    await db.characters.update_one({"_id": ObjectId(ch["id"])}, {"$set": {"active_quests": ch["active_quests"]}})
    return {"character": ch}


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
    })
    ch["active_quests"] = [a for a in ch["active_quests"] if a["quest_id"] != quest_id]
    ch.setdefault("completed_quests", []).append(quest_id)
    await db.characters.update_one({"_id": ObjectId(ch["id"])}, {"$set": {
        "active_quests": ch["active_quests"],
        "completed_quests": ch["completed_quests"],
        "gold": ch["gold"], "xp": ch["xp"], "level": ch["level"],
        "stats": ch["stats"], "max_hp": ch["max_hp"], "inventory": ch["inventory"],
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
    await db.characters.update_one({"_id": ObjectId(ch["id"])}, {"$set": {
        "current_town": ch["current_town"],
        "visited_towns": ch["visited_towns"],
    }})
    return {"character": ch, "town": town}


@api.post("/game/town/leave")
async def leave_town(user: dict = Depends(_get_current_user)):
    ch = await _get_character_or_404(user["_id"])
    ch["current_town"] = None
    await db.characters.update_one({"_id": ObjectId(ch["id"])}, {"$set": {"current_town": None}})
    return {"character": ch}


@api.post("/game/town/inn")
async def rest_at_inn(user: dict = Depends(_get_current_user)):
    ch = await _get_character_or_404(user["_id"])
    town = get_town(ch.get("current_town"))
    if not town:
        raise HTTPException(status_code=400, detail="You must be in a town to rest")
    cost = town.get("inn_cost", 10)
    if ch["gold"] < cost:
        raise HTTPException(status_code=400, detail="Not enough gold")
    ch["gold"] -= cost
    ch["hp"] = ch["max_hp"]
    # clear all debuff statuses
    ch["statuses"] = [s for s in ch.get("statuses", []) if s.get("kind") != "debuff"]
    ch["exhaustion"] = max(0, ch.get("exhaustion", 0) - 20)
    ch["resolve"] = min(100, ch.get("resolve", 100) + 10)
    await db.characters.update_one({"_id": ObjectId(ch["id"])}, {"$set": {
        "gold": ch["gold"], "hp": ch["hp"], "statuses": ch["statuses"],
        "exhaustion": ch["exhaustion"], "resolve": ch["resolve"],
    }})
    return {"character": ch, "cost": cost}


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
    dests = []
    for c in CONTINENTS:
        if c.get("locked"):
            continue
        hometown = HOMETOWN_BY_CONTINENT.get(c["id"])
        town = TOWNS_BY_ID.get(hometown) if hometown else None
        dests.append({
            "continent_id": c["id"],
            "continent_name": c["name"],
            "hometown_id": hometown,
            "hometown_name": town["name"] if town else hometown,
            "fee": TELEPORTER_FEE if c["id"] != ch.get("current_continent") else 0,
            "is_current": c["id"] == ch.get("current_continent"),
        })
    return {"destinations": dests, "cooldown_secs": TELEPORTER_COOLDOWN_SECS, "fee_base": TELEPORTER_FEE}


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
    # Fee
    if ch["gold"] < TELEPORTER_FEE:
        raise HTTPException(status_code=400, detail=f"Teleporter fee is {TELEPORTER_FEE}g.")
    hometown = HOMETOWN_BY_CONTINENT.get(target_continent)
    if not hometown:
        raise HTTPException(status_code=500, detail="No hometown mapped for this continent.")
    # Apply
    ch["gold"] -= TELEPORTER_FEE
    ch["current_continent"] = target_continent
    ch["current_town"] = hometown
    if hometown not in ch.get("visited_towns", []):
        ch.setdefault("visited_towns", []).append(hometown)
    # Land in the tier-1 biome of the new continent
    if dest_cont.get("biomes"):
        ch["current_biome"] = dest_cont["biomes"][0]["id"]
    ch["teleporter_last_used"] = datetime.now(timezone.utc).isoformat()
    await db.characters.update_one({"_id": ObjectId(ch["id"])}, {"$set": {
        "gold": ch["gold"],
        "current_continent": ch["current_continent"],
        "current_town": ch["current_town"],
        "current_biome": ch["current_biome"],
        "visited_towns": ch["visited_towns"],
        "teleporter_last_used": ch["teleporter_last_used"],
    }})
    return {"character": ch, "fee": TELEPORTER_FEE, "hometown": hometown, "narrative":
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
    return {
        "catalog": PROFESSIONS,
        "ranks": PROFESSION_RANKS,
        "slots_unlocked": profession_slots_unlocked(int(ch.get("level", 1))),
        "next_slot_at": [1, 10, 25],
    }


@api.get("/game/professions/mine")
async def my_professions(user: dict = Depends(_get_current_user)):
    ch = await _get_character_or_404(user["_id"])
    out = []
    for p in ch.get("professions", []):
        meta = PROFESSIONS_BY_ID.get(p["id"], {})
        out.append({
            "id": p["id"],
            "name": meta.get("name", p["id"]),
            "kind": meta.get("kind"),
            "rank": p.get("rank", "novice"),
            "xp": p.get("xp", 0),
            "learned": p.get("learned"),
        })
    return {"professions": out, "slots_unlocked": profession_slots_unlocked(int(ch.get("level", 1)))}


@api.post("/game/professions/learn")
async def learn_profession_endpoint(request: Request, user: dict = Depends(_get_current_user)):
    body = await request.json()
    pid = body.get("profession_id")
    ch = await _get_character_or_404(user["_id"])
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


# ============================================================
# EXPLORATION PROGRESS (Phase C)
# ============================================================
@api.get("/game/exploration")
async def exploration_state(user: dict = Depends(_get_current_user)):
    """Return per-biome exploration % for the current continent."""
    ch = await _get_character_or_404(user["_id"])
    cont_id = ch.get("current_continent")
    cont = next((c for c in CONTINENTS if c["id"] == cont_id), None)
    biomes = cont.get("biomes", []) if cont else []
    ep = ch.get("exploration_progress", {}) or {}
    out = []
    for b in biomes:
        pct = int(ep.get(b["id"], 0))
        thresholds_met = [pct >= t[0] for t in EXPLORATION_THRESHOLDS]
        out.append({
            "biome_id": b["id"],
            "biome_name": b["name"],
            "level_req": b.get("level_req", 1),
            "progress_pct": pct,
            "thresholds_met": thresholds_met,   # [10%, 25%, 50%, 75%, 100%]
        })
    return {"continent_id": cont_id, "biomes": out,
            "thresholds": [{"pct": t[0], "desc": t[1]} for t in EXPLORATION_THRESHOLDS]}


@api.post("/game/town/market/buy")
async def market_buy(request: Request, user: dict = Depends(_get_current_user)):
    body = await request.json()
    item_id = body.get("item_id")
    qty = int(body.get("quantity", 1))
    ch = await _get_character_or_404(user["_id"])
    town = get_town(ch.get("current_town"))
    if not town or item_id not in town.get("market_items", []):
        raise HTTPException(status_code=404, detail="Item not sold here")
    item = ITEMS_BY_ID.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Unknown item")
    price = _price_of(item) * qty
    if ch["gold"] < price:
        raise HTTPException(status_code=400, detail="Not enough gold")
    ch["gold"] -= price
    _add_item_to_inventory(ch, item_id, qty)
    await db.characters.update_one({"_id": ObjectId(ch["id"])}, {"$set": {
        "gold": ch["gold"], "inventory": ch["inventory"],
    }})
    return {"character": ch, "paid": price}


@api.post("/game/town/market/sell")
async def market_sell(request: Request, user: dict = Depends(_get_current_user)):
    body = await request.json()
    item_id = body.get("item_id")
    qty = int(body.get("quantity", 1))
    ch = await _get_character_or_404(user["_id"])
    town = get_town(ch.get("current_town"))
    if not town:
        raise HTTPException(status_code=400, detail="Must be in a town")
    item = ITEMS_BY_ID.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Unknown item")
    if not _remove_item_from_inventory(ch, item_id, qty):
        raise HTTPException(status_code=400, detail="Not enough in inventory")
    payout = int(_price_of(item) * 0.5) * qty
    ch["gold"] += payout
    await db.characters.update_one({"_id": ObjectId(ch["id"])}, {"$set": {
        "gold": ch["gold"], "inventory": ch["inventory"],
    }})
    return {"character": ch, "received": payout}


def _price_of(item: dict) -> int:
    rarity_price = {
        "common": 10, "uncommon": 40, "rare": 120,
        "epic": 350, "legendary": 900, "mythic": 2500,
    }
    return rarity_price.get(item.get("rarity", "common"), 10)


# ---------------- GUILDS ----------------
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


# ---------------- ROOT ----------------
@api.get("/")
async def root():
    return {"service": "Erchis RPG", "status": "ok"}


@api.get("/health")
async def health():
    return {"status": "healthy"}


# ---------------- WIRE ----------------
app.include_router(api)

frontend_url = os.environ.get("FRONTEND_URL", "http://localhost:3000")
origins = [frontend_url, "http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
        if updates:
            await db.characters.update_one({"_id": ch_doc["_id"]}, {"$set": updates})
            total_updated += 1
    if total_updated:
        logger.info("Canon v2 rename applied on %d character(s).", total_updated)
    logger.info("Erchis server up. Frontend origin: %s", frontend_url)


@app.on_event("shutdown")
async def shutdown():
    client.close()
