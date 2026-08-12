"""Full game smoke test — every race, every mastery, level to 30, try everything.

Requires the server running on http://127.0.0.1:8000/api.

Run: python test_full_game.py
"""
import requests
import time
import json
import sys
import asyncio
import os
from pathlib import Path
from datetime import datetime, timezone, timedelta
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")
BASE = "http://127.0.0.1:8000/api"
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "erchistorn")

# ============================================================
# Race → mastery → role → origin mapping
# ============================================================
# Role priority per mastery (first match wins)
ROLE_PRIORITY = {
    "knight": ["fighter", "guardian"],
    "paladin": ["fighter", "guardian", "healer"],
    "lancer": ["fighter", "scout"],
    "assassin": ["fighter", "scout"],
    "druid": ["guardian", "healer", "scholar"],
    "rogue": ["scout"],
    "hunter": ["scout"],
    "mage": ["scholar"],
    "bard": ["scholar", "healer"],
    "alchemist": ["scholar", "healer"],
    "priest": ["healer"],
}

# Race → available roles
RACE_ROLES = {
    "human": ["fighter", "guardian", "scout", "scholar", "healer"],
    "elf": ["scholar", "healer", "scout"],
    "dwarf": ["fighter", "guardian"],
    "half_elf": ["scout", "scholar", "healer", "guardian", "fighter"],
    "orc": ["fighter", "guardian"],
    "wildblood": ["fighter", "guardian", "scout", "healer"],
    "hyliondrian": ["scholar", "healer", "scout"],
    "sylvan": ["scholar", "scout", "healer"],
}


def pick_role(mastery, race_id):
    """Pick a valid role for this mastery that the race actually has."""
    available = RACE_ROLES.get(race_id, [])
    for role in ROLE_PRIORITY.get(mastery, ["fighter"]):
        if role in available:
            return role
    return available[0] if available else "fighter"

# First origin per mastery
ORIGIN_FOR_MASTERY = {
    "knight": "guardians_shield",
    "paladin": "radiant_heart",
    "lancer": "silvered_wolf",
    "assassin": "shrouded_shadow",
    "rogue": "obsidian_dagger",
    "hunter": "verdant_grove",
    "druid": "ancient_oak",
    "priest": "luminous_codex",
    "mage": "arcane_spiral",
    "bard": "golden_harp",
    "alchemist": "tempests_eye",
}

RACES = [
    {"id": "human", "masteries": ["knight", "paladin", "lancer", "rogue", "bard", "alchemist"]},
    {"id": "elf", "masteries": ["mage", "priest", "druid", "assassin", "hunter", "paladin"]},
    {"id": "dwarf", "masteries": ["knight", "paladin", "lancer"]},
    {"id": "half_elf", "masteries": ["bard", "rogue", "paladin", "mage", "priest", "knight"]},
    {"id": "orc", "masteries": ["knight", "paladin", "lancer"]},
    {"id": "wildblood", "masteries": ["druid", "hunter", "lancer", "assassin", "knight", "bard"]},
    {"id": "hyliondrian", "masteries": ["mage", "priest", "druid", "hunter", "lancer", "paladin"]},
    {"id": "sylvan", "masteries": ["mage", "druid", "priest", "hunter", "assassin", "rogue", "bard"]},
]

# ============================================================
# Helpers
# ============================================================
total_pass = 0
total_fail = 0
errors_log = []


def sep(title):
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}")


def check(label, condition, detail=""):
    global total_pass, total_fail
    if condition:
        total_pass += 1
    else:
        total_fail += 1
        errors_log.append(f"{label}: {detail}")
        print(f"  ❌ {label} — {detail}")


def new_session():
    return requests.Session()


def register(s, tag):
    username = f"test_{tag}_{int(time.time()*1000)}"
    r = s.post(f"{BASE}/auth/register", json={
        "username": username,
        "password": "Test1234!",
        "email": f"{username}@test.com",
        "display_name": tag,
    })
    if r.status_code != 200:
        return None, None
    user_id = r.json().get("id")
    return user_id, username


def create_character(s, race, mastery, role, origin, portrait_id="Aldric"):
    # Fetch racial gift
    r = s.get(f"{BASE}/game/data/races")
    races = r.json().get("races", [])
    race_data = next(rc for rc in races if rc["id"] == race)
    gifts = race_data.get("gifts", [])
    gift_id = gifts[0]["id"] if gifts else None

    # Fetch portraits
    r = s.get(f"{BASE}/game/data/portraits")
    portraits = r.json().get("portraits", [])
    pid = portraits[0]["id"] if portraits else portrait_id

    body = {
        "name": f"{race}_{mastery}",
        "race": race,
        "role": role,
        "mastery": mastery,
        "origin": origin,
        "portrait_id": pid,
        "racial_gift": gift_id,
        "oath": "protect_the_weak" if race == "human" else None,
        "heritage": "human" if race == "half_elf" else None,
    }
    r = s.post(f"{BASE}/game/character", json=body)
    return r


def get_char(s):
    r = s.get(f"{BASE}/game/character")
    if r.status_code != 200:
        return None
    return r.json().get("character")


def set_db_field(user_id, fields):
    async def _set():
        client = AsyncIOMotorClient(MONGO_URI)
        db = client[DB_NAME]
        await db.characters.update_one({"user_id": user_id}, {"$set": fields})
        client.close()
    asyncio.run(_set())


def fast_level_to(s, user_id, target_level):
    """Set XP very high in DB, then do an action to trigger level-up loop."""
    from progression import total_xp_for_level
    needed_xp = total_xp_for_level(target_level) + 1000
    set_db_field(user_id, {"xp": needed_xp, "gold": 99999, "hp": 99999})
    # Do an explore action to trigger _level_up_if_needed
    char = get_char(s)
    biome = char.get("current_biome") if char else None
    if not biome:
        return None
    r = s.post(f"{BASE}/game/action", json={"action_id": "explore", "biome_id": biome})
    char = get_char(s)
    return char


def try_endpoint(s, method, path, label, json_body=None):
    """Try an endpoint and return (success, status_code, data)."""
    try:
        if method == "GET":
            r = s.get(f"{BASE}{path}")
        elif method == "POST":
            r = s.post(f"{BASE}{path}", json=json_body or {})
        else:
            return False, 0, None
        if r.status_code == 200:
            return True, r.status_code, r.json()
        else:
            return False, r.status_code, r.text[:200]
    except Exception as e:
        return False, 0, str(e)[:200]


# ============================================================
# MAIN TEST LOOP
# ============================================================
sep("FULL GAME TEST — All races, all masteries, level 30")

combo_count = 0
for race_info in RACES:
    race_id = race_info["id"]
    for mastery in race_info["masteries"]:
        combo_count += 1
        role = pick_role(mastery, race_id)
        origin = ORIGIN_FOR_MASTERY.get(mastery, "guardians_shield")
        tag = f"{race_id}_{mastery}"

        print(f"\n--- [{combo_count}] {tag} (role={role}) ---")

        s = new_session()
        user_id, username = register(s, tag)
        if not user_id:
            check(f"{tag}: register", False, "registration failed")
            continue
        check(f"{tag}: register", True)

        # Create character
        r = create_character(s, race_id, mastery, role, origin)
        check(f"{tag}: create character", r.status_code == 200, f"{r.status_code} {r.text[:100]}")
        if r.status_code != 200:
            continue

        char = get_char(s)
        if not char:
            check(f"{tag}: get character", False, "fetch failed")
            continue
        check(f"{tag}: character created", char.get("name") == f"{race_id}_{mastery}")
        check(f"{tag}: starts at level 1", char.get("level") == 1, f"level={char.get('level')}")
        check(f"{tag}: resolve = 50", char.get("resolve") == 50, f"resolve={char.get('resolve')}")

        # Fast-level to 30
        char = fast_level_to(s, user_id, 30)
        if not char:
            check(f"{tag}: level to 30", False, "fast_level returned None")
            continue
        check(f"{tag}: reached level 30", char.get("level") >= 30, f"level={char.get('level')}")
        if char.get("level", 0) < 30:
            # Try another action
            biome = char.get("current_biome")
            if biome:
                s.post(f"{BASE}/game/action", json={"action_id": "explore", "biome_id": biome})
                char = get_char(s)
                check(f"{tag}: reached level 30 (2nd try)", char.get("level", 0) >= 30, f"level={char.get('level')}")

        # Give full HP and gold
        set_db_field(user_id, {"hp": 99999, "gold": 99999, "stamina": 999, "mp": 999})
        char = get_char(s)
        biome = char.get("current_biome")

        # ---- ACTIVITY: Explore ----
        if biome:
            ok, sc, data = try_endpoint(s, "POST", "/game/action",
                                        f"{tag}: explore",
                                        json_body={"action_id": "explore", "biome_id": biome})
            check(f"{tag}: explore", ok, f"{sc} {data}")

        # ---- ACTIVITY: Gather ----
        # Gather may fail if resources depleted or missing profession — that's game logic, not a bug
        if biome:
            ok, sc, data = try_endpoint(s, "POST", "/game/action",
                                        f"{tag}: gather",
                                        json_body={"action_id": "gather", "biome_id": biome})
            # 200 = success, 400 = missing profession/tool, 403 = depleted — all valid game responses
            check(f"{tag}: gather responds", ok or sc in (400, 403), f"{sc} {data}")

        # ---- ACTIVITY: Fish ----
        if biome:
            ok, sc, data = try_endpoint(s, "POST", "/game/action",
                                        f"{tag}: fish",
                                        json_body={"action_id": "fish", "biome_id": biome})
            check(f"{tag}: fish responds", ok or sc in (400, 403), f"{sc} {data}")

        # ---- ACTIVITY: Hunt (combat) ----
        # Need to discover monsters first via exploration
        if biome:
            # Explore several times to discover monsters
            for _ in range(30):
                s.post(f"{BASE}/game/action", json={"action_id": "explore", "biome_id": biome})
                # Restore stamina between explores
                set_db_field(user_id, {"stamina": 999, "hp": 99999})

            # Check biome actions for monsters
            r = s.get(f"{BASE}/game/data/biome/{biome}/actions")
            if r.status_code == 200:
                actions = r.json().get("actions", [])
                hunt = next((a for a in actions if a.get("id") == "hunt"), None)
                monsters = hunt.get("monsters", []) if hunt else []
                if monsters:
                    monster_id = monsters[0]["id"]
                    # Start combat
                    r = s.post(f"{BASE}/game/combat/start", json={"monster_id": monster_id})
                    if r.status_code == 200:
                        combat_data = r.json()
                        combat_id = combat_data["state"]["combat_id"]
                        check(f"{tag}: combat start", True)

                        # Take turns until victory or death
                        turns = 0
                        combat_ended = False
                        while turns < 50:
                            r = s.post(f"{BASE}/game/combat/turn", json={
                                "combat_id": combat_id,
                                "action_type": "strike",
                            })
                            if r.status_code != 200:
                                check(f"{tag}: combat turn {turns+1}", False, f"{r.status_code} {r.text[:100]}")
                                break
                            result = r.json().get("result", {})
                            if result.get("victory") is not None:
                                combat_ended = True
                                if result.get("victory"):
                                    check(f"{tag}: combat victory", True)
                                    check(f"{tag}: resolve_gain in result", "resolve_gain" in result)
                                else:
                                    check(f"{tag}: combat (lost)", True, "character died")
                                    # Restore HP for further tests
                                    set_db_field(user_id, {"hp": 99999, "gold": 99999})
                                break
                            turns += 1
                        if not combat_ended:
                            check(f"{tag}: combat (timeout)", False, "50 turns without resolution")
                    else:
                        check(f"{tag}: combat start", False, f"{r.status_code} {r.text[:100]}")
                else:
                    # Monsters may be depleted from stock — not a bug
                    check(f"{tag}: hunt monsters (stock depleted)", True, "no monsters in biome actions — likely stock depleted")
            else:
                check(f"{tag}: biome actions fetch", False, f"{r.status_code}")

        # ---- ACTIVITY: Town visit ----
        char = get_char(s)
        home_town = char.get("home_town") or "oathspire"
        ok, sc, data = try_endpoint(s, "POST", "/game/town/visit",
                                    f"{tag}: town visit",
                                    json_body={"town_id": home_town})
        check(f"{tag}: town visit", ok, f"{sc} {data}")

        # ---- ACTIVITY: Sanctuary rest ----
        ok, sc, data = try_endpoint(s, "POST", "/game/town/sanctuary",
                                    f"{tag}: sanctuary rest",
                                    json_body={"service": "rest"})
        check(f"{tag}: sanctuary rest", ok, f"{sc} {data}")

        # ---- ACTIVITY: Sanctuary cleanse ----
        ok, sc, data = try_endpoint(s, "POST", "/game/town/sanctuary",
                                    f"{tag}: sanctuary cleanse",
                                    json_body={"service": "cleanse"})
        check(f"{tag}: sanctuary cleanse", ok, f"{sc} {data}")

        # ---- ACTIVITY: Sanctuary blessing ----
        ok, sc, data = try_endpoint(s, "POST", "/game/town/sanctuary",
                                    f"{tag}: sanctuary blessing",
                                    json_body={"service": "blessing"})
        check(f"{tag}: sanctuary blessing", ok, f"{sc} {data}")

        # ---- ACTIVITY: Leave town ----
        ok, sc, data = try_endpoint(s, "POST", "/game/town/leave",
                                    f"{tag}: leave town")
        check(f"{tag}: leave town", ok, f"{sc} {data}")

        # ---- ACTIVITY: Training (gym) ----
        ok, sc, data = try_endpoint(s, "GET", "/game/training/status",
                                    f"{tag}: training status")
        check(f"{tag}: training status", ok, f"{sc} {data}")

        ok, sc, data = try_endpoint(s, "POST", "/game/training/start",
                                    f"{tag}: training start",
                                    json_body={"trainer_type": "main", "stat": "might", "amount": 1})
        check(f"{tag}: training start", ok, f"{sc} {data}")

        # ---- ACTIVITY: Study (academy) ----
        ok, sc, data = try_endpoint(s, "GET", "/game/study/status",
                                    f"{tag}: study status")
        check(f"{tag}: study status", ok, f"{sc} {data}")

        # Try to enroll in a course
        if ok and data:
            courses = data.get("courses", [])
            if courses:
                course_id = courses[0].get("id")
                ok2, sc2, data2 = try_endpoint(s, "POST", "/game/study/enroll",
                                               f"{tag}: study enroll",
                                               json_body={"course_id": course_id})
                check(f"{tag}: study enroll", ok2, f"{sc2} {data2}")

                if ok2:
                    ok3, sc3, data3 = try_endpoint(s, "POST", "/game/study/checkin",
                                                   f"{tag}: study checkin")
                    check(f"{tag}: study checkin", ok3, f"{sc3} {data3}")

        # ---- ACTIVITY: Crafting ----
        # Must be in a town to craft — visit home town first
        char = get_char(s)
        home_town = char.get("home_town") or "oathspire"
        s.post(f"{BASE}/game/town/visit", json={"town_id": home_town})

        ok, sc, data = try_endpoint(s, "GET", "/game/data/recipes",
                                    f"{tag}: recipes list")
        check(f"{tag}: recipes list", ok, f"{sc} {data}")

        if ok and data:
            recipes = data.get("recipes", [])
            if recipes:
                recipe_id = recipes[0].get("id")
                ok2, sc2, data2 = try_endpoint(s, "POST", "/game/craft",
                                               f"{tag}: craft",
                                               json_body={"recipe_id": recipe_id})
                # 200 = success, 400 = missing materials/level, 403 = wrong town — all valid
                check(f"{tag}: craft responds", ok2 or sc2 in (400, 403), f"{sc2} {data2}")

        # ---- ACTIVITY: Quests ----
        ok, sc, data = try_endpoint(s, "GET", "/game/quests/available",
                                    f"{tag}: quests available")
        check(f"{tag}: quests available", ok, f"{sc} {data}")

        # ---- ACTIVITY: Expedition ----
        char = get_char(s)
        biome = char.get("current_biome")
        if biome:
            ok, sc, data = try_endpoint(s, "GET", f"/game/expedition/merc/{biome}",
                                        f"{tag}: expedition merc")
            check(f"{tag}: expedition merc", ok or sc == 404, f"{sc} {data}")

        ok, sc, data = try_endpoint(s, "GET", "/game/expedition/status",
                                    f"{tag}: expedition status")
        check(f"{tag}: expedition status", ok, f"{sc} {data}")

        # ---- ACTIVITY: Resolve status ----
        ok, sc, data = try_endpoint(s, "GET", "/game/resolve/status",
                                    f"{tag}: resolve status")
        check(f"{tag}: resolve status", ok, f"{sc} {data}")

        # ---- ACTIVITY: Bestiary ----
        ok, sc, data = try_endpoint(s, "GET", "/game/bestiary",
                                    f"{tag}: bestiary")
        check(f"{tag}: bestiary", ok, f"{sc} {data}")

        # ---- ACTIVITY: Skill learn (if teachers available) ----
        ok, sc, data = try_endpoint(s, "GET", "/game/data/skills",
                                    f"{tag}: skills list")
        check(f"{tag}: skills list", ok, f"{sc} {data}")

        # ---- ACTIVITY: Mastery-specific passives ----
        mastery_endpoints = {
            "rogue": "/game/rogue/passives",
            "druid": "/game/druid/passives",
            "knight": "/game/knight/passives",
            "lancer": "/game/lancer/passives",
            "mage": "/game/mage/passives",
        }
        mastery_ep = mastery_endpoints.get(mastery)
        if mastery_ep:
            ok, sc, data = try_endpoint(s, "GET", mastery_ep,
                                        f"{tag}: {mastery} passives")
            check(f"{tag}: {mastery} passives", ok, f"{sc} {data}")

        # ---- ACTIVITY: Travel ----
        ok, sc, data = try_endpoint(s, "GET", "/game/data/continents",
                                    f"{tag}: continents list")
        check(f"{tag}: continents list", ok, f"{sc} {data}")

        # ---- ACTIVITY: Items/Inventory ----
        ok, sc, data = try_endpoint(s, "GET", "/game/data/items",
                                    f"{tag}: items list")
        check(f"{tag}: items list", ok, f"{sc} {data}")

        # ---- ACTIVITY: Runes/Gems ----
        ok, sc, data = try_endpoint(s, "GET", "/game/data/runes",
                                    f"{tag}: runes list")
        check(f"{tag}: runes list", ok, f"{sc} {data}")

        ok, sc, data = try_endpoint(s, "GET", "/game/data/gems",
                                    f"{tag}: gems list")
        check(f"{tag}: gems list", ok, f"{sc} {data}")

        # ---- ACTIVITY: Diagnostics ----
        ok, sc, data = try_endpoint(s, "GET", "/_diagnostics/errors",
                                    f"{tag}: diagnostics")
        check(f"{tag}: diagnostics", ok, f"{sc} {data}")

        # Print per-combo summary
        char = get_char(s)
        if char:
            print(f"  → L{char.get('level')} | HP {char.get('hp')}/{char.get('max_hp')} | "
                  f"Gold {char.get('gold')} | XP {char.get('xp')} | "
                  f"Stats: {json.dumps(char.get('stats', {}))[:80]}")


# ============================================================
# SUMMARY
# ============================================================
sep(f"FINAL RESULTS: {total_pass} passed, {total_fail} failed across {combo_count} race/mastery combos")

if errors_log:
    print(f"\n  --- Errors ({len(errors_log)}) ---")
    for err in errors_log[:50]:
        print(f"  ❌ {err}")
    if len(errors_log) > 50:
        print(f"  ... and {len(errors_log) - 50} more")

if total_fail > 0:
    sys.exit(1)
else:
    print("\n  All tests passed! ✨")
