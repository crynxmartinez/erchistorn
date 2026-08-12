"""Play Erchis as a normal player — Human Knight, no cheating, level to 50.

Plays like a real player: combat, explore, gather, fish, quests, events,
crafting, skill learning, equipment management, market trading, mercenary
expeditions, stat training, continent travel, and more.

Requires the server running on http://127.0.0.1:8000/api.
Run: python play_game.py
"""
import requests
import time
import json
import sys
import random
import os
from datetime import datetime, timezone

BASE = "http://127.0.0.1:8000/api"
TARGET_LEVEL = 50
MAX_ACTIONS = 20000

# ============================================================
# Session & Globals
# ============================================================
s = requests.Session()
char = None
user_id = None
username = None
action_round = 0
combat_count = 0
gather_count = 0
fish_count = 0
explore_count = 0
deaths = 0
rests = 0
craft_count = 0
quests_claimed = 0
events_joined = 0
skills_learned = 0
items_equipped = 0
market_buys = 0
expeditions_started = 0
level_milestones = {}
errors = []

# Towns with sanctuary on each continent (hometowns)
HOMETOWN_BY_CONTINENT = {
    "valeria": "oathspire",
    "mushkara": "grunhold",
    "concordia": "elaris",
    "khardrum": "jahrahold",
    "haya": "solunara",
    "gennel": "rindivar_grove",
    "hylion": "atlantyrion",
    "daw_ul_talalu": "veilgrove",
}

SANCTUARY_COST_BY_TOWN = {
    "oathspire": 10, "grunhold": 25, "elaris": 30, "jahrahold": 40,
    "solunara": 55, "rindivar_grove": 70, "atlantyrion": 90, "veilgrove": 85,
}


# ============================================================
# Utilities
# ============================================================
def log(msg):
    print(f"  {msg}", flush=True)


def sep(title):
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}", flush=True)


def api_get(path):
    try:
        r = s.get(f"{BASE}{path}", timeout=30)
        if r.status_code != 200:
            return None
        return r.json()
    except Exception as e:
        log(f"  [ERROR] GET {path}: {e}")
        errors.append(f"GET {path}: {e}")
        return None


def api_post(path, body=None):
    try:
        r = s.post(f"{BASE}{path}", json=body or {}, timeout=30)
        return r
    except Exception as e:
        log(f"  [ERROR] POST {path}: {e}")
        errors.append(f"POST {path}: {e}")
        return None


def get_char():
    r = s.get(f"{BASE}/game/character", timeout=30)
    if r.status_code != 200:
        return None
    return r.json().get("character")


def refresh():
    global char
    char = get_char()
    return char


def get_rest_town():
    cont = char.get("current_continent", "valeria")
    return HOMETOWN_BY_CONTINENT.get(cont, "oathspire")


def get_rest_cost():
    town = get_rest_town()
    return SANCTUARY_COST_BY_TOWN.get(town, 10)


def best_biome_for_level(cont_id=None):
    """Return the highest-level unlocked biome on the current/given continent."""
    cont = cont_id or char.get("current_continent", "valeria")
    level = char.get("level", 1)
    # Fetch continents data to get biome list with level reqs
    data = api_get("/game/data/continents")
    if not data:
        return "golden_plains"
    continents = data.get("continents", [])
    continent = next((c for c in continents if c["id"] == cont), None)
    if not continent:
        return "golden_plains"
    biomes = continent.get("biomes", [])
    best = biomes[0]["id"] if biomes else "golden_plains"
    for b in biomes:
        if level >= b.get("level_req", 1):
            best = b["id"]
    return best


def has_item(item_id):
    for entry in char.get("inventory", []):
        if entry.get("item_id") == item_id and entry.get("quantity", 0) > 0:
            return True
    return False


def has_profession(prof_id):
    return any(p.get("id") == prof_id for p in char.get("professions", []))


def has_tool(prof_id):
    tools_data = api_get("/game/tools")
    if not tools_data:
        return False
    for t in tools_data.get("tools", []):
        if t.get("profession_id") == prof_id and t.get("durability", 0) > 0:
            return True
    return False


# ============================================================
# Account & Character Creation
# ============================================================
sep("STARTING PLAYTHROUGH: Human Knight -> Level 50")

username = f"playtest_knight_{int(time.time())}"
log(f"Registering account: {username}")
r = s.post(f"{BASE}/auth/register", json={
    "username": username,
    "password": "Test1234!",
    "email": f"{username}@test.com",
    "display_name": "Aldric the Knight",
})
if r.status_code != 200:
    print(f"  Registration failed: {r.status_code} {r.text[:200]}")
    sys.exit(1)
user_id = r.json().get("id")
log(f"Account created. User ID: {user_id}")

# Fetch races to get gift
r = s.get(f"{BASE}/game/data/races")
races = r.json().get("races", [])
human = next((rc for rc in races if rc["id"] == "human"), None)
gifts = human.get("gifts", []) if human else []
gift_id = gifts[0]["id"] if gifts else ""
log(f"Racial gift: {gift_id}")

# Fetch origins for knight mastery
r = s.get(f"{BASE}/game/data/origins/knight")
origins = r.json().get("origins", [])
origin_id = origins[0]["id"] if origins else ""
log(f"Origin: {origin_id}")

# Fetch portraits
r = s.get(f"{BASE}/game/data/portraits")
portraits = r.json().get("portraits", [])
portrait_id = portraits[0]["id"] if portraits else "p1"
log(f"Portrait: {portrait_id}")

# Create character
log("Creating character: Human Knight (fighter)")
r = s.post(f"{BASE}/game/character", json={
    "name": "Aldric",
    "race": "human",
    "mastery": "knight",
    "role": "fighter",
    "origin": origin_id,
    "portrait_id": portrait_id,
    "racial_gift": gift_id,
    "oath": "iron",
})
if r.status_code != 200:
    print(f"  Character creation failed: {r.status_code} {r.text[:200]}")
    sys.exit(1)

refresh()
log(f"Character created: {char.get('name')} the Human Knight")
log(f"Starting: Level {char['level']} | HP {char['hp']}/{char['max_hp']} | "
    f"Gold {char.get('gold', 0)} | Stats: {json.dumps(char.get('stats', {}))}")
log(f"Continent: {char.get('current_continent')} | Biome: {char.get('current_biome')} | "
    f"Town: {char.get('current_town')}")


# ============================================================
# Core Actions
# ============================================================
def do_explore(biome):
    global explore_count
    r = api_post("/game/action", {"biome_id": biome, "action_id": "explore"})
    if not r or r.status_code != 200:
        if r and r.status_code == 403:
            log(f"  ⚠️ Explore blocked: {r.text[:80]}")
        return False
    explore_count += 1
    data = r.json()
    discoveries = data.get("discoveries", [])
    for d in discoveries:
        kind = d.get("kind", "?")
        name = d.get("name", "?")
        emoji = "🔍" if kind == "node" else "🐺"
        log(f"    {emoji} Discovered {kind}: {name}")
    return True


def get_available_monsters(biome):
    """Get discovered monsters with stock from the discoveries endpoint."""
    r = api_get("/game/discoveries")
    if not r:
        return []
    biomes = r.get("biomes", [])
    biome_data = next((b for b in biomes if b.get("biome_id") == biome), None)
    if not biome_data:
        return []
    monsters = []
    for m in biome_data.get("monsters", []):
        if m.get("discovered") and m.get("id"):
            monsters.append({
                "id": m["id"],
                "name": m.get("name", m["id"]),
                "threat": m.get("threat", 0),
                "hp": m.get("hp", 10),
                "rarity": m.get("rarity", "common"),
            })
    return monsters


def do_combat(monster_id, monster_name, biome_id):
    global combat_count, deaths
    combat_count += 1
    r = api_post("/game/combat/start", {"monster_id": monster_id, "biome_id": biome_id})
    if not r or r.status_code != 200:
        log(f"  [ERROR] Combat start failed vs {monster_name}: {r.text[:100] if r else 'no response'}")
        return False, 0, 0

    combat_data = r.json()
    combat_id = combat_data.get("combat_id")
    state = combat_data.get("state", {})

    turns = 0
    while turns < 50:
        r = api_post("/game/combat/turn", {
            "combat_id": combat_id,
            "action_type": "strike",
        })
        if not r or r.status_code != 200:
            break
        resp = r.json()
        result = resp.get("result", {})
        if result.get("victory") is not None:
            rewards = result.get("rewards", {})
            if result.get("victory"):
                xp = rewards.get("xp", 0)
                gold = rewards.get("gold", 0)
                resolve_gain = result.get("resolve_gain", 0)
                log(f"  ⚔️ #{combat_count} VICTORY vs {monster_name} ({turns+1}t) | "
                    f"+{xp} XP, +{gold}g"
                    f"{f', +{resolve_gain} resolve' if resolve_gain else ''}")
                refresh()
                return True, xp, gold
            else:
                deaths += 1
                log(f"  💀 #{combat_count} DEFEATED by {monster_name}")
                refresh()
                log(f"  💀 Respawning at {char.get('current_town')} with {char['hp']}/{char['max_hp']} HP")
                # Leave town and go to best biome
                api_post("/game/town/leave")
                refresh()
                if not char.get("current_biome"):
                    target = best_biome_for_level()
                    api_post("/game/character/travel", {
                        "continent": char.get("current_continent", "valeria"),
                        "biome": target,
                    })
                    refresh()
                return False, 0, 0
        turns += 1

    api_post("/game/combat/abandon")
    log(f"  ⏱️ #{combat_count} timeout vs {monster_name}")
    refresh()
    return False, 0, 0


def get_available_nodes(biome, profession=None):
    """Get discovered resource nodes from the discoveries endpoint."""
    r = api_get("/game/discoveries")
    if not r:
        return []
    biomes = r.get("biomes", [])
    biome_data = next((b for b in biomes if b.get("biome_id") == biome), None)
    if not biome_data:
        return []
    nodes = []
    for n in biome_data.get("nodes", []):
        if n.get("discovered") and n.get("id"):
            if profession is None or n.get("profession") == profession:
                nodes.append(n)
    return nodes


def do_gather(biome):
    global gather_count
    # Find a node we can gather from (matching our profession)
    nodes = get_available_nodes(biome)
    # Filter to nodes we have the profession for
    viable = []
    for n in nodes:
        prof = n.get("profession", "")
        if prof and has_profession(prof) and has_tool(prof):
            viable.append(n)
    if not viable:
        return False, 0
    target = random.choice(viable)
    r = api_post("/game/action", {"biome_id": biome, "action_id": "gather", "target_id": target["id"]})
    if not r or r.status_code != 200:
        if r and r.status_code in [400, 403]:
            pass  # Node depleted or on cooldown
        return False, 0
    gather_count += 1
    data = r.json()
    result = data.get("result", {})
    rewards = result.get("rewards", {})
    xp = rewards.get("xp", 0)
    items = rewards.get("items", [])
    log(f"  🌿 Gather ({target.get('name','?')}): +{xp} XP, items: {items}")
    return True, xp


def do_fish(biome):
    global fish_count
    # Find fishing nodes
    nodes = get_available_nodes(biome, profession="fishing")
    if not nodes:
        return False, 0
    target = random.choice(nodes)
    r = api_post("/game/action", {"biome_id": biome, "action_id": "fish", "target_id": target["id"]})
    if not r or r.status_code != 200:
        if r and r.status_code in [400, 403]:
            pass
        return False, 0
    fish_count += 1
    data = r.json()
    result = data.get("result", {})
    rewards = result.get("rewards", {})
    xp = rewards.get("xp", 0)
    items = rewards.get("items", [])
    log(f"  🎣 Fish ({target.get('name','?')}): +{xp} XP, items: {items}")
    return True, xp


def go_rest():
    global rests
    rest_town = get_rest_town()
    log(f"  💤 HP low ({char['hp']}/{char['max_hp']}) — heading to sanctuary at {rest_town}")
    r = api_post("/game/town/visit", {"town_id": rest_town})
    if not r or r.status_code != 200:
        log(f"  ⚠️ Could not visit town: {r.text[:100] if r else 'no response'}")
        return False
    r = api_post("/game/town/sanctuary", {"service": "rest"})
    if not r or r.status_code != 200:
        log(f"  ⚠️ Could not rest: {r.text[:100] if r else 'no response'}")
        api_post("/game/town/leave")
        refresh()
        return False
    rests += 1
    refresh()
    log(f"  ✅ Rested! HP {char['hp']}/{char['max_hp']} | Gold {char.get('gold', 0)}")
    api_post("/game/town/leave")
    refresh()
    return True


def need_to_rest():
    if not char:
        return False
    hp = char.get("hp", 0)
    max_hp = char.get("max_hp", 1)
    gold = char.get("gold", 0)
    return hp < max_hp * 0.4 and gold >= get_rest_cost()


# ============================================================
# Town Activities
# ============================================================
def visit_town(town_id):
    r = api_post("/game/town/visit", {"town_id": town_id})
    if not r or r.status_code != 200:
        return False
    refresh()
    return True


def leave_town():
    api_post("/game/town/leave")
    refresh()


def learn_profession_in_town(town_id, prof_id):
    if not visit_town(town_id):
        return False
    r = api_post("/game/professions/learn", {"profession_id": prof_id})
    if r and r.status_code == 200:
        log(f"  📖 Learned profession: {prof_id} at {town_id}")
        refresh()
        leave_town()
        return True
    log(f"  ⚠️ Could not learn {prof_id}: {r.text[:80] if r else 'no response'}")
    leave_town()
    return False


def buy_tool_in_town(town_id, prof_id):
    if not visit_town(town_id):
        return False
    r = api_post("/game/tools/buy", {"profession_id": prof_id})
    if r and r.status_code == 200:
        log(f"  🔧 Bought {prof_id} tool at {town_id}")
        refresh()
        leave_town()
        return True
    log(f"  ⚠️ Could not buy {prof_id} tool: {r.text[:80] if r else 'no response'}")
    leave_town()
    return False


def try_market_buy(town_id):
    """Visit market and buy useful items (potions, gear)."""
    global market_buys
    if not visit_town(town_id):
        return
    market = api_get("/game/town/market")
    if not market:
        leave_town()
        return
    listings = market.get("listings", [])
    for listing in listings:
        item_id = listing.get("item_id")
        price = listing.get("final_price", 999)
        stock = listing.get("stock", 0)
        if stock <= 0 or price > char.get("gold", 0) * 0.3:
            continue
        item_name = listing.get("name", item_id)
        if any(kw in item_name.lower() for kw in ["healing", "potion", "bandage"]):
            if price <= char.get("gold", 0):
                r = api_post("/game/town/market/buy", {"item_id": item_id, "quantity": 1})
                if r and r.status_code == 200:
                    market_buys += 1
                    log(f"  🛒 Bought {item_name} for {price}g")
                    refresh()
                    break
    leave_town()


def try_learn_skill(town_id):
    """Try to learn a skill from a teacher in town."""
    global skills_learned
    if not visit_town(town_id):
        return
    teachers_data = api_get(f"/game/data/teachers")
    if not teachers_data:
        leave_town()
        return
    teachers = teachers_data.get("teachers", [])
    # Filter teachers in this town
    town_teachers = [t for t in teachers if t.get("town_id") == town_id]
    skills_data = api_get("/game/data/skills")
    all_skills = skills_data.get("skills", []) if skills_data else []

    for teacher in town_teachers:
        teaches = teacher.get("teaches", [])
        for offer in teaches:
            skill_id = offer.get("skill_id") if isinstance(offer, dict) else offer
            if any(sk.get("skill_id") == skill_id for sk in char.get("skills", [])):
                continue
            skill_data = next((sk for sk in all_skills if sk.get("id") == skill_id), None)
            if not skill_data:
                continue
            if char.get("level", 1) < skill_data.get("level_req", 99):
                continue
            cost = skill_data.get("cost_gold", 0)
            if char.get("gold", 0) < cost + 50:
                continue
            r = api_post("/game/skill/learn", {"skill_id": skill_id, "teacher_id": teacher.get("id")})
            if r and r.status_code == 200:
                skills_learned += 1
                log(f"  📚 Learning skill: {skill_data.get('name', skill_id)} (training...)")
                learn_seconds = skill_data.get("learn_seconds", 10)
                time.sleep(min(learn_seconds + 1, 15))
                r2 = api_post("/game/skill/finish_learn")
                if r2 and r2.status_code == 200:
                    log(f"  ✅ Learned skill: {skill_data.get('name', skill_id)}")
                    refresh()
                    skill_bar = char.get("skill_bar", [None] * 10)
                    empty_slot = next((i for i, v in enumerate(skill_bar) if v is None), None)
                    if empty_slot is not None:
                        api_post("/game/skill/assign", {"slot": empty_slot, "skill_id": skill_id})
                        log(f"  🎯 Assigned {skill_data.get('name', skill_id)} to slot {empty_slot}")
                        refresh()
                leave_town()
                return
    leave_town()


def try_craft(town_id):
    """Try to craft items using available recipes and materials."""
    global craft_count
    if not visit_town(town_id):
        return
    # Check craft queue first
    queue_data = api_get("/game/craft/queue")
    if queue_data:
        ready = queue_data.get("ready", [])
        if ready:
            for r_id in ready:
                r = api_post("/game/craft/claim", {"recipe_id": r_id})
                if r and r.status_code == 200:
                    craft_count += 1
                    log(f"  ✅ Crafted: {r_id}")
                    refresh()

    recipes_data = api_get("/game/data/recipes")
    if not recipes_data:
        leave_town()
        return
    recipes = recipes_data.get("recipes", [])
    for recipe in recipes:
        recipe_id = recipe.get("id")
        ingredients = recipe.get("ingredients", [])
        can_craft = True
        for ing in ingredients:
            ing_id = ing.get("id") or ing.get("item_id")
            ing_qty = ing.get("quantity", 1) if isinstance(ing, dict) else 1
            if not has_item(ing_id):
                can_craft = False
                break
        if not can_craft:
            continue
        cost = recipe.get("cost_gold", 0)
        if char.get("gold", 0) < cost + 20:
            continue
        r = api_post("/game/craft", {"recipe_id": recipe_id})
        if r and r.status_code == 200:
            craft_count += 1
            log(f"  🔨 Crafting: {recipe.get('name', recipe_id)}")
            # If queued, wait for it
            resp = r.json()
            if resp.get("queued"):
                craft_seconds = recipe.get("time_seconds", 5)
                time.sleep(min(craft_seconds + 1, 15))
                r2 = api_post("/game/craft/claim", {"recipe_id": recipe_id})
                if r2 and r2.status_code == 200:
                    log(f"  ✅ Crafted: {recipe.get('name', recipe_id)}")
                    refresh()
            else:
                log(f"  ✅ Instant craft: {recipe.get('name', recipe_id)}")
                refresh()
            leave_town()
            return
    leave_town()


def try_equip_better_gear():
    """Equip better gear from inventory."""
    global items_equipped
    inv = char.get("inventory", [])
    equipped = char.get("equipped", {})
    equipped_ids = set(equipped.values())
    for entry in inv:
        item_id = entry.get("item_id")
        if not item_id or entry.get("quantity", 0) <= 0:
            continue
        if item_id in equipped_ids:
            continue
        for slot in ["right_hand", "left_hand", "head", "chest", "legs", "feet",
                      "ring_l", "ring_r", "earring_l", "earring_r", "back", "neck"]:
            r = api_post("/game/equip", {"item_id": item_id, "slot": slot})
            if r and r.status_code == 200:
                items_equipped += 1
                log(f"  👕 Equipped {item_id} in {slot}")
                refresh()
                equipped_ids.add(item_id)
                break


def use_healing_item():
    """Use a healing potion if HP is low and we have one."""
    inv = char.get("inventory", [])
    for entry in inv:
        item_id = entry.get("item_id")
        if not entry.get("quantity", 0) > 0:
            continue
        name = item_id.lower()
        if any(kw in name for kw in ["healing_potion", "bandage"]):
            r = api_post("/game/inventory/use", {"item_id": item_id})
            if r and r.status_code == 200:
                log(f"  💊 Used {item_id} for healing")
                refresh()
                return True
    return False


# ============================================================
# Quests & Events
# ============================================================
def check_quests():
    """Accept available quests and claim completed ones."""
    global quests_claimed
    refresh()
    active = char.get("active_quests", [])
    for aq in active:
        if aq.get("complete"):
            qid = aq.get("quest_id")
            r = api_post(f"/game/quests/{qid}/claim")
            if r and r.status_code == 200:
                quests_claimed += 1
                reward = r.json().get("claimed", {})
                log(f"  📜 Claimed quest {qid}: +{reward.get('gold', 0)}g, +{reward.get('xp', 0)} XP")
                refresh()
            else:
                log(f"  ⚠️ Could not claim quest {qid}: {r.text[:80] if r else 'no response'}")

    q_data = api_get("/game/quests/available")
    if not q_data:
        return
    available = q_data.get("available", [])
    accepted = 0
    for q in available:
        if accepted >= 3:
            break
        qid = q.get("id")
        # Skip board quests from distant towns — only accept story and regional
        if qid.startswith("board_") and not q.get("is_contract"):
            continue
        r = api_post(f"/game/quests/{qid}/accept")
        if r and r.status_code == 200:
            accepted += 1
            log(f"  📜 Accepted quest: {q.get('name', qid)}")
            refresh()
        elif r and r.status_code not in [409, 403]:
            log(f"  ⚠️ Could not accept quest {qid}: {r.text[:80]}")


def check_events():
    """Join active events/festivals."""
    global events_joined
    ev_data = api_get("/game/events/active")
    if not ev_data:
        return
    events = ev_data.get("events", [])
    for ev in events:
        ev_id = ev.get("id")
        if ev_id and char.get("level", 1) >= ev.get("level_req", 1):
            r = api_post(f"/game/events/{ev_id}/join")
            if r and r.status_code == 200:
                events_joined += 1
                log(f"  🎪 Joined event: {ev.get('name', ev_id)}")
                refresh()


def check_daily_missions():
    """Claim completed daily missions."""
    refresh()
    missions = char.get("daily_missions", [])
    for m in missions:
        if m.get("complete") and not m.get("claimed"):
            r = api_post("/game/daily/claim", {"mission_id": m.get("id")})
            if r and r.status_code == 200:
                reward = r.json().get("reward", {})
                log(f"  📋 Claimed daily mission: +{reward.get('gold', 0)}g, +{reward.get('xp', 0)} XP")
                refresh()


# ============================================================
# Expeditions & Training
# ============================================================
def check_expedition():
    """Collect finished expeditions and start new ones."""
    global expeditions_started
    status = api_get("/game/expedition/status")
    if not status:
        return
    queue = status.get("queue")
    if queue:
        cooldown = queue.get("finish_at") if isinstance(queue, dict) else None
        if cooldown:
            try:
                finish = datetime.fromisoformat(cooldown)
                if finish.tzinfo is None:
                    finish = finish.replace(tzinfo=timezone.utc)
                if datetime.now(timezone.utc) >= finish:
                    r = api_post("/game/expedition/collect")
                    if r and r.status_code == 200:
                        result = r.json().get("expedition_result", {})
                        log(f"  🏕️ Collected expedition: {result.get('summary', 'done')}")
                        refresh()
                        queue = None
            except Exception:
                pass
    if not queue:
        biome = char.get("current_biome")
        if biome:
            r = api_post("/game/expedition/start", {"biome_id": biome, "hours": 1})
            if r and r.status_code == 200:
                expeditions_started += 1
                log(f"  🏕️ Started expedition in {biome}")
                refresh()


def check_training():
    """Collect finished stat training and start new training."""
    status = api_get("/game/training/status")
    if not status:
        return
    for qtype in ["main", "life"]:
        queue = status.get(f"queue_{qtype}")
        if queue:
            finish = queue.get("finish_at") if isinstance(queue, dict) else None
            if finish:
                try:
                    finish_dt = datetime.fromisoformat(finish)
                    if finish_dt.tzinfo is None:
                        finish_dt = finish_dt.replace(tzinfo=timezone.utc)
                    if datetime.now(timezone.utc) >= finish_dt:
                        r = api_post("/game/training/collect", {"trainer_type": qtype})
                        if r and r.status_code == 200:
                            log(f"  💪 Collected {qtype} training")
                            refresh()
                except Exception:
                    pass


def check_heritage():
    """Rank up heritage if possible."""
    info = api_get("/game/heritage/info")
    if not info:
        return
    if info.get("can_rank_up"):
        r = api_post("/game/heritage/rankup")
        if r and r.status_code == 200:
            log(f"  ⬆️ Heritage rank up! Now rank {r.json().get('character', {}).get('heritage_rank', '?')}")
            refresh()


# ============================================================
# Setup Phase
# ============================================================
sep("PHASE 1: Setup")

starting_biome = char.get("current_biome") or "golden_plains"
log(f"Starting biome: {starting_biome}")
log(f"Starting gold: {char.get('gold', 0)}g")

# Leave town if we're in one
if char.get("current_town"):
    api_post("/game/town/leave")
    refresh()

# Travel to starting biome if not already there
if not char.get("current_biome"):
    api_post("/game/character/travel", {
        "continent": char.get("current_continent", "valeria"),
        "biome": starting_biome,
    })
    refresh()
    starting_biome = char.get("current_biome", starting_biome)

# Explore starting biome to discover monsters and nodes
log("--- Exploring starting biome ---")
for _ in range(15):
    do_explore(starting_biome)
refresh()
log(f"After exploration: L{char['level']} | HP {char['hp']}/{char['max_hp']} | Gold {char.get('gold', 0)}")

# Learn herbalism at Riverguard (on Valeria, same continent)
log("--- Learning herbalism at Riverguard ---")
learn_profession_in_town("riverguard", "herbalism")
buy_tool_in_town("riverguard", "herbalism")
refresh()
log(f"Setup complete: L{char['level']} | HP {char['hp']}/{char['max_hp']} | Gold {char.get('gold', 0)}g")
log(f"Professions: {char.get('professions', [])}")

# Accept any available quests
log("--- Checking for quests ---")
check_quests()

# Join any active events
log("--- Checking for events ---")
check_events()

# Claim any daily missions
log("--- Checking daily missions ---")
check_daily_missions()

# Go back to biome for adventure
if char.get("current_town"):
    leave_town()
if not char.get("current_biome"):
    target = best_biome_for_level()
    api_post("/game/character/travel", {
        "continent": char.get("current_continent", "valeria"),
        "biome": target,
    })
    refresh()


# ============================================================
# Main Game Loop
# ============================================================
sep("PHASE 2: Adventure — Playing to Level 50")

last_level = char.get("level", 1)
biome = char.get("current_biome") or best_biome_for_level()
last_quest_check = 0
last_event_check = 0
last_expedition_check = 0
last_training_check = 0
last_heritage_check = 0
last_craft_check = 0
last_skill_check = 0
last_market_check = 0
last_gear_check = 0

while action_round < MAX_ACTIONS:
    action_round += 1
    refresh()

    if not char:
        log("  [ERROR] Could not fetch character — stopping")
        break

    current_level = char.get("level", 1)
    if current_level >= TARGET_LEVEL:
        sep(f"🎉 TARGET REACHED! Level {current_level}")
        break

    # Level up notification
    if current_level > last_level:
        level_milestones[current_level] = {
            "round": action_round,
            "combats": combat_count,
            "deaths": deaths,
            "hp": char["hp"],
            "max_hp": char["max_hp"],
            "gold": char.get("gold", 0),
            "stats": dict(char.get("stats", {})),
        }
        log(f"  🎉 LEVEL UP! Now level {current_level}! "
            f"(round {action_round}, {combat_count} combats, {deaths} deaths)")
        last_level = current_level

        # On level up, do town stuff
        rest_town = get_rest_town()
        if visit_town(rest_town):
            try_learn_skill(rest_town)
            check_quests()
            check_heritage()
            try_craft(rest_town)
            try_market_buy(rest_town)
            leave_town()

    # Move to best biome for our level
    best = best_biome_for_level()
    if best != biome:
        log(f"  🗺️ Moving to {best} (L{current_level})")
        r = api_post("/game/character/travel", {
            "continent": char.get("current_continent", "valeria"),
            "biome": best,
        })
        if r and r.status_code == 200:
            refresh()
            biome = char.get("current_biome", best)
            for _ in range(5):
                do_explore(biome)
            refresh()
        else:
            log(f"  ⚠️ Travel to {best} failed: {r.text[:80] if r else 'no response'}")

    # Periodic tasks
    if action_round - last_quest_check >= 100:
        check_quests()
        check_daily_missions()
        last_quest_check = action_round

    if action_round - last_event_check >= 200:
        check_events()
        last_event_check = action_round

    if action_round - last_expedition_check >= 50:
        check_expedition()
        last_expedition_check = action_round

    if action_round - last_training_check >= 100:
        check_training()
        last_training_check = action_round

    if action_round - last_heritage_check >= 500:
        check_heritage()
        last_heritage_check = action_round

    if action_round - last_craft_check >= 100:
        rest_town = get_rest_town()
        try_craft(rest_town)
        last_craft_check = action_round

    if action_round - last_skill_check >= 200:
        rest_town = get_rest_town()
        try_learn_skill(rest_town)
        last_skill_check = action_round

    if action_round - last_market_check >= 200:
        rest_town = get_rest_town()
        try_market_buy(rest_town)
        last_market_check = action_round

    if action_round - last_gear_check >= 100:
        try_equip_better_gear()
        last_gear_check = action_round

    # Use healing potion if HP is low
    hp_pct = char["hp"] / max(1, char["max_hp"])
    if hp_pct < 0.3:
        if use_healing_item():
            hp_pct = char["hp"] / max(1, char["max_hp"])

    # Rest if needed
    if need_to_rest():
        go_rest()
        refresh()
        biome = char.get("current_biome") or best_biome_for_level()
        continue

    # Ensure we're in a biome
    if not biome:
        api_post("/game/town/leave")
        refresh()
        biome = char.get("current_biome")
        if not biome:
            target = best_biome_for_level()
            api_post("/game/character/travel", {
                "continent": char.get("current_continent", "valeria"),
                "biome": target,
            })
            refresh()
            biome = char.get("current_biome", target)
            if not biome:
                log("  ⚠️ No biome — can't continue")
                break
        continue

    # Weighted activity selection — play like a real player
    roll = random.random()

    if roll < 0.55:
        # Primary: combat (55%)
        monsters = get_available_monsters(biome)
        if monsters:
            char_level = char.get("level", 1)
            safe_monsters = [m for m in monsters if m.get("threat", 99) <= char_level * 3 + 10]
            if not safe_monsters:
                safe_monsters = monsters
            monster = random.choice(safe_monsters)
            monster_id = monster.get("id")
            monster_name = monster.get("name", monster_id)
            do_combat(monster_id, monster_name, biome_id=biome)
            refresh()
            biome = char.get("current_biome") or biome
        else:
            do_explore(biome)
            refresh()
            biome = char.get("current_biome") or biome

    elif roll < 0.70 and has_profession("herbalism") and has_tool("herbalism"):
        # Gather (15%)
        ok, _ = do_gather(biome)
        if not ok:
            do_explore(biome)
        refresh()
        biome = char.get("current_biome") or biome

    elif roll < 0.78:
        # Fish (8%)
        if has_profession("fishing") and has_tool("fishing"):
            ok, _ = do_fish(biome)
            if not ok:
                do_explore(biome)
        else:
            do_explore(biome)
        refresh()
        biome = char.get("current_biome") or biome

    elif roll < 0.90:
        # Explore (12%)
        do_explore(biome)
        refresh()
        biome = char.get("current_biome") or biome

    else:
        # Town activities (10%)
        rest_town = get_rest_town()
        if visit_town(rest_town):
            if char["hp"] < char["max_hp"] * 0.8 and char.get("gold", 0) >= get_rest_cost():
                api_post("/game/town/sanctuary", {"service": "rest"})
                refresh()
                log(f"  ✅ Rested at sanctuary | HP {char['hp']}/{char['max_hp']}")
            try_craft(rest_town)
            try_market_buy(rest_town)
            check_quests()
            try_equip_better_gear()
            leave_town()
        refresh()
        biome = char.get("current_biome") or best_biome_for_level()

    # Periodic checkpoint
    if action_round % 500 == 0:
        log(f"\n  --- Checkpoint (round {action_round}) ---")
        log(f"  L{char['level']} | HP {char['hp']}/{char['max_hp']} | XP {char.get('xp', 0)} | "
            f"Gold {char.get('gold', 0)} | Resolve {char.get('resolve', 50)}")
        log(f"  Combats: {combat_count} | Gathers: {gather_count} | Fish: {fish_count} | "
            f"Explores: {explore_count} | Deaths: {deaths} | Rests: {rests}")
        log(f"  Quests claimed: {quests_claimed} | Events joined: {events_joined} | "
            f"Skills learned: {skills_learned} | Items equipped: {items_equipped}")
        log(f"  Market buys: {market_buys} | Expeditions: {expeditions_started} | "
            f"Crafts: {craft_count}")
        log(f"  Continent: {char.get('current_continent')} | Biome: {char.get('current_biome')} | "
            f"Town: {char.get('current_town')}")
        log("")


# ============================================================
# Final Report
# ============================================================
sep("FINAL PLAYTHROUGH REPORT")

refresh()
if char:
    log(f"  L{char['level']} | HP {char['hp']}/{char['max_hp']} | XP {char.get('xp', 0)} | "
        f"Gold {char.get('gold', 0)} | Resolve {char.get('resolve', 50)}")
    log(f"  Stats: {json.dumps(char.get('stats', {}))}")
    log("")
    log(f"  Total actions: {action_round}")
    log(f"    Combats fought: {combat_count}")
    log(f"    Gathers: {gather_count}")
    log(f"    Fish: {fish_count}")
    log(f"    Explores: {explore_count}")
    log(f"    Deaths: {deaths}")
    log(f"    Sanctuary rests: {rests}")
    log(f"    Quests claimed: {quests_claimed}")
    log(f"    Events joined: {events_joined}")
    log(f"    Skills learned: {skills_learned}")
    log(f"    Items equipped: {items_equipped}")
    log(f"    Market buys: {market_buys}")
    log(f"    Expeditions: {expeditions_started}")
    log(f"    Crafts: {craft_count}")
    log("")

    if level_milestones:
        log("  Level milestones:")
        for lvl in sorted(level_milestones.keys()):
            ms = level_milestones[lvl]
            log(f"      Level {lvl}: round {ms['round']} | HP {ms['hp']}/{ms['max_hp']} | "
                f"Gold {ms['gold']} | Stats {json.dumps(ms.get('stats', {}))[:60]}")

    log("")
    if char.get("level", 0) >= TARGET_LEVEL:
        log(f"  ✅ SUCCESS: Reached level {TARGET_LEVEL}!")
    else:
        log(f"  ⚠️ Ended at level {char.get('level', 0)} (target was {TARGET_LEVEL})")

    log("")
    log("  Final Character Sheet:")
    log(f"      Name: {char.get('name')}")
    log(f"      Race: {char.get('race')}")
    log(f"      Mastery: {char.get('mastery')}")
    log(f"      Role: {char.get('role')}")
    log(f"      Level: {char.get('level')}")
    log(f"      XP: {char.get('xp')}")
    log(f"      HP: {char.get('hp')}/{char.get('max_hp')}")
    log(f"      Gold: {char.get('gold')}")
    log(f"      Resolve: {char.get('resolve')}")
    log(f"      Kills: {char.get('kills')}")
    log(f"      Stats: {json.dumps(char.get('stats', {}))}")
    log(f"      Professions: {json.dumps(char.get('professions', []))}")
    log(f"      Inventory items: {len(char.get('inventory', []))}")
    log(f"      Visited towns: {char.get('visited_towns', [])}")
    log(f"      Current continent: {char.get('current_continent')}")
    log(f"      Current biome: {char.get('current_biome')}")
    log(f"      Active quests: {len(char.get('active_quests', []))}")
    log(f"      Completed quests: {len(char.get('completed_quests', []))}")
    log(f"      Skills: {[s.get('skill_id') for s in char.get('skills', [])]}")
    log(f"      Skill bar: {char.get('skill_bar', [])}")

if errors:
    log(f"\n  Errors encountered ({len(errors)}):")
    for e in errors[:10]:
        log(f"      {e}")
