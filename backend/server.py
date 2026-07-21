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
    return _serialize_doc(ch)


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
    return {"roles": ROLES}


@api.get("/game/data/masteries")
async def get_masteries_route(user: dict = Depends(_get_current_user)):
    return {"masteries": MASTERIES}


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
    if payload.race == "human" and not payload.oath:
        raise HTTPException(status_code=400, detail="Humans must swear a Sacred Oath")
    if payload.race == "half_elf" and not payload.heritage:
        raise HTTPException(status_code=400, detail="Half-Elves must choose a heritage")

    stats = dict(race["starting_stats"])
    stats.setdefault("resilience", 0)
    stats.setdefault("grace", 0)
    for k, v in role.get("bonus", {}).items():
        stats[k] = stats.get(k, 0) + v

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
        "reputation": {},
        "tutorial_step": 0,
        "tutorial_complete": False,
        "current_continent": "aetheria",
        "current_biome": "grasslands",
        "login_streak": 0,
        "last_login_date": None,
        "last_daily_refresh": None,
        "daily_missions": [],
        "_biomes_today": [],
        "inner_blood": 0,
        "exhaust": 0,
        "zone_active": False,
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
        ch.setdefault("statuses", []).append({
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

    if ch["hp"] <= 0:
        ch["hp"] = 1

    await db.characters.update_one({"_id": ObjectId(ch["id"])}, {"$set": {
        "hp": ch["hp"], "max_hp": ch["max_hp"], "gold": ch["gold"], "xp": ch["xp"],
        "level": ch["level"], "stats": ch["stats"], "inventory": ch["inventory"],
        "statuses": ch["statuses"], "kills": ch["kills"],
        "daily_missions": ch.get("daily_missions", []),
        "_biomes_today": ch.get("_biomes_today", []),
    }})

    if result["outcome"] == 6:
        target_disp = result.get("target_name") or "the unknown"
        await _push_world_event(ch["name"], f"{ch['name']} achieved a critical {payload.action_id} against {target_disp}.", "loot")

    return {"result": result, "character": ch}


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
        updates.update({
            "gold": ch["gold"], "xp": ch["xp"], "level": ch["level"], "stats": ch["stats"],
            "max_hp": ch["max_hp"], "kills": ch["kills"],
            "daily_missions": ch.get("daily_missions", []),
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
    logger.info("Erchis server up. Frontend origin: %s", frontend_url)


@app.on_event("shutdown")
async def shutdown():
    client.close()
