"""Play the game like an actual player — step by step through the API."""
import requests
import time
import json
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta
from pathlib import Path

load_dotenv(Path(__file__).parent / ".env")
BASE = "http://127.0.0.1:8000/api"
s = requests.Session()

def sep(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def step(n, msg):
    print(f"\n[Step {n}] {msg}")

# ============================================================
# 1. REGISTER — "I'm a new player, let me sign up"
# ============================================================
sep("PLAYER REGISTRATION")
username = f"player_{int(time.time())}"
step(1, f"Signing up as {username}...")
r = s.post(f"{BASE}/auth/register", json={
    "username": username,
    "password": "Play1234!",
    "email": f"{username}@test.com",
    "display_name": "Adventurer",
})
assert r.status_code == 200, f"Register failed: {r.text}"
print(f"  ✅ Account created! Welcome, Adventurer.")

# ============================================================
# 2. FETCH GAME DATA — "What races and classes can I pick?"
# ============================================================
sep("CHARACTER CREATION — BROWSING OPTIONS")
step(2, "Fetching available races...")
r = s.get(f"{BASE}/game/data/races")
races = r.json().get("races", [])
print(f"  Available races: {', '.join(r['name'] for r in races)}")

step(3, "Fetching available roles...")
r = s.get(f"{BASE}/game/data/roles")
roles = r.json().get("roles", [])
print(f"  Available roles: {', '.join(r['name'] for r in roles)}")

step(4, "Fetching masteries for Fighter...")
r = s.get(f"{BASE}/game/data/masteries/fighter")
masteries = r.json().get("masteries", [])
print(f"  Fighter masteries: {', '.join(m['name'] for m in masteries)}")

step(5, "Fetching origins for Knight...")
r = s.get(f"{BASE}/game/data/origins/knight")
origins = r.json().get("origins", [])
print(f"  Knight origins: {', '.join(o['name'] for o in origins)}")

step(6, "Fetching racial gifts for Human...")
human = next(rc for rc in races if rc["id"] == "human")
gifts = human.get("gifts", [])
print(f"  Human gifts: {', '.join(g['name'] for g in gifts)}")

step(7, "Fetching portraits...")
r = s.get(f"{BASE}/game/data/portraits")
portraits = r.json().get("portraits", [])
print(f"  Available portraits: {len(portraits)}")

# ============================================================
# 3. CREATE CHARACTER — "I'll be a Human Knight!"
# ============================================================
sep("CHARACTER CREATION — FINALIZING")
step(8, "Creating character: Human Fighter Knight, Guardian's Shield origin...")
r = s.post(f"{BASE}/game/character", json={
    "name": "SirGallant",
    "race": "human",
    "role": "fighter",
    "mastery": "knight",
    "origin": "guardians_shield",
    "portrait_id": portraits[0]["id"] if portraits else "Aldric",
    "racial_gift": gifts[0]["id"],
    "oath": "protect_the_weak",
})
assert r.status_code == 200, f"Character creation failed: {r.text}"
char = r.json().get("character", r.json())
print(f"  ✅ Character created: {char['name']} the {char['race']} {char['role']}")
print(f"     Level: {char.get('level', 1)} | Gold: {char.get('gold', 0)} | XP: {char.get('xp', 0)}")
print(f"     Current biome: {char.get('current_biome')}")
print(f"     Stats: {json.dumps(char.get('stats', {}))}")

# ============================================================
# 4. LOOK AROUND — "What can I do here?"
# ============================================================
biome = char["current_biome"]
sep(f"EXPLORING {biome.upper()}")

step(9, f"Fetching biome actions for {biome}...")
r = s.get(f"{BASE}/game/data/biome/{biome}/actions")
assert r.status_code == 200, f"Actions fetch failed: {r.text}"
data = r.json()
actions = data.get("actions", [])
print(f"  Available actions: {', '.join(a.get('id', a.get('name', '?')) for a in actions)}")

# Show monster list if available
hunt_action = next((a for a in actions if a.get("id") == "hunt"), None)
if hunt_action:
    monsters = hunt_action.get("monsters", [])
    print(f"  Monsters to hunt: {', '.join(m['name'] for m in monsters[:5])}")
else:
    print(f"  No hunt action yet — need to explore more!")

# ============================================================
# 5. EXPLORE — "Let me look around this biome"
# ============================================================
step(10, "Exploring the biome (exploring 8 times to discover monsters)...")
for i in range(8):
    r = s.post(f"{BASE}/game/action", json={"action_id": "explore", "biome_id": biome})
    if r.status_code == 200:
        result = r.json()
        outcome = result.get("outcome", "ok")
        progress = result.get("new_progress_pct")
        msg = result.get("message", "")
        print(f"  Explore {i+1}: progress={progress}% | {msg[:80]}")
        # Check if we got items
        items = result.get("items_found", [])
        if items:
            print(f"    📦 Found items: {items}")
    else:
        print(f"  Explore {i+1}: {r.status_code} {r.text[:100]}")
        break

# ============================================================
# 6. CHECK ACTIONS AGAIN — "Now what can I hunt?"
# ============================================================
step(11, "Re-checking biome actions after exploration...")
r = s.get(f"{BASE}/game/data/biome/{biome}/actions")
data = r.json()
actions = data.get("actions", [])
hunt_action = next((a for a in actions if a.get("id") == "hunt"), None)
if hunt_action:
    monsters = hunt_action.get("monsters", [])
    print(f"  ✅ Monsters now available: {', '.join(m['name'] for m in monsters[:5])}")
else:
    print(f"  Still no hunt action. Let me try gathering instead.")
    gather_action = next((a for a in actions if a.get("id") == "gather"), None)
    if gather_action:
        print(f"  Gather action found! Resources: {gather_action.get('resources', [])}")

# ============================================================
# 7. HUNT — "Time to fight some monsters!"
# ============================================================
sep("COMBAT — HUNTING MONSTERS")
if hunt_action and hunt_action.get("monsters"):
    monster = hunt_action["monsters"][0]
    step(12, f"Starting combat with {monster['name']}...")
    r = s.post(f"{BASE}/game/combat/start", json={"biome_id": biome, "monster_id": monster["id"]})
    if r.status_code == 200:
        combat = r.json()
        state = combat.get("state", combat)
        print(f"  ⚔️  Battle started! Enemy: {state.get('enemy_name')} HP: {state.get('enemy_hp')}")
        print(f"     My HP: {state.get('player_hp')} | My MP: {state.get('player_mp', 'N/A')}")

        # Fight: attack each turn
        turn = 0
        while not state.get("combat_over") and turn < 30:
            turn += 1
            r = s.post(f"{BASE}/game/combat/action", json={"action": "attack"})
            if r.status_code != 200:
                print(f"  Turn {turn}: Error {r.status_code} {r.text[:100]}")
                break
            state = r.json().get("state", r.json())
            if state.get("combat_over"):
                victory = state.get("victory")
                gold = state.get("gold_earned", 0)
                xp = state.get("xp_earned", 0)
                loot = state.get("loot", [])
                print(f"  🏆 Combat over! Victory: {victory}")
                print(f"     Gold earned: {gold} | XP earned: {xp}")
                if loot:
                    print(f"     Loot: {loot}")
                break
            if turn % 5 == 0:
                print(f"  ...turn {turn}: Enemy HP={state.get('enemy_hp')} My HP={state.get('player_hp')}")
        else:
            print(f"  Combat ended after {turn} turns (limit reached)")

        # Hunt a few more monsters for gold
        step(13, "Hunting more monsters for gold...")
        total_gold = 0
        for hunt_num in range(4):
            monster = hunt_action["monsters"][hunt_num % len(hunt_action["monsters"])]
            r = s.post(f"{BASE}/game/combat/start", json={"biome_id": biome, "monster_id": monster["id"]})
            if r.status_code != 200:
                print(f"  Hunt {hunt_num+2}: Can't start — {r.text[:80]}")
                break
            state = r.json().get("state", r.json())
            turn = 0
            while not state.get("combat_over") and turn < 30:
                turn += 1
                r = s.post(f"{BASE}/game/combat/action", json={"action": "attack"})
                if r.status_code != 200:
                    break
                state = r.json().get("state", r.json())
                if state.get("combat_over"):
                    g = state.get("gold_earned", 0)
                    total_gold += g
                    print(f"  Hunt {hunt_num+2}: {monster['name']} — {'Won' if state.get('victory') else 'Lost'} | +{g}g")
                    break
        print(f"  Total gold from hunting: {total_gold}")
    else:
        print(f"  Combat start failed: {r.text[:200]}")
else:
    print("  No monsters to hunt — skipping combat.")

# ============================================================
# 8. CHECK GOLD & CHARACTER STATE
# ============================================================
sep("CHARACTER STATUS CHECK")
step(14, "Fetching current character state...")
r = s.get(f"{BASE}/game/character")
if r.status_code == 200:
    char = r.json().get("character", r.json())
    print(f"  {char['name']} | Level {char.get('level', 1)} | Gold: {char.get('gold', 0)} | XP: {char.get('xp', 0)}")
    print(f"  Exploration: {char.get('exploration_progress', {})}")
else:
    # Try alternate endpoint
    r = s.get(f"{BASE}/game/state")
    if r.status_code == 200:
        char = r.json().get("character", r.json())
        print(f"  {char.get('name')} | Gold: {char.get('gold', 0)} | XP: {char.get('xp', 0)}")
    else:
        print(f"  Could not fetch character: {r.status_code}")

# ============================================================
# 9. MERCENARY — "Let me hire a mercenary!"
# ============================================================
sep("MERCENARY EXPEDITION")
step(15, f"Checking mercenary info for {biome}...")
r = s.get(f"{BASE}/game/expedition/merc/{biome}")
assert r.status_code == 200, f"Merc info failed: {r.text}"
data = r.json()
merc = data.get("merc", {})
print(f"  🧑‍🌾 Mercenary: {merc.get('name')} the {merc.get('rank').title()}")
print(f"     Specialty: {merc.get('specialty')} | Rate: {merc.get('hourly_rate')}g/hr")
print(f"     Efficiency: {merc.get('efficiency')} | Quirk: {merc.get('quirk')}")
print(f"     Loyalty: {data.get('loyalty_hires', 0)} previous hires")
print(f"     Exploration: {data.get('exploration_pct')}% (need {data.get('min_exploration')}%)")
print(f"     Loot preview: {data.get('merc', {}).get('loot_preview', [])[:4]}")
print(f"     Rare preview: {data.get('merc', {}).get('rare_preview', [])[:2]}")

gold = char.get("gold", 0)
if gold >= merc.get("hourly_rate", 999):
    hours = min(2, gold // merc["hourly_rate"])
    step(16, f"Hiring {merc['name']} for {hours} hour(s)...")
    r = s.post(f"{BASE}/game/expedition/start", json={"biome_id": biome, "hours": hours})
    if r.status_code == 200:
        result = r.json()
        exp = result.get("expedition_result", {})
        char = result.get("character", {})
        print(f"  ✅ Hired! Gold spent: {exp.get('gold_spent')} | Gold left: {char.get('gold', 0)}")
        queue = char.get("expedition_queue", {})
        print(f"     Merc: {queue.get('merc_name')} | Finishes: {queue.get('finishes_at')}")
        print(f"     Expected yield: {exp.get('expected_yield', 'N/A')} items")

        step(17, "Trying to collect immediately (should fail)...")
        r = s.post(f"{BASE}/game/expedition/collect")
        print(f"  Collect attempt: {r.status_code} — {r.json().get('detail', r.text[:80])}")

        # Fast-forward time
        step(18, "⏩ Fast-forwarding time (simulating waiting)...")
        async def fast_forward():
            client = AsyncIOMotorClient(os.environ["MONGO_URL"])
            db = client[os.environ["DB_NAME"]]
            c = await db.characters.find_one({"name": "SirGallant"})
            if c and c.get("expedition_queue"):
                q = c["expedition_queue"]
                q["finishes_at"] = (datetime.now(timezone.utc) - timedelta(seconds=1)).isoformat()
                await db.characters.update_one({"_id": c["_id"]}, {"$set": {"expedition_queue": q}})
                print(f"  Time fast-forwarded!")
            client.close()
        asyncio.run(fast_forward())

        step(19, "Collecting expedition rewards...")
        r = s.post(f"{BASE}/game/expedition/collect")
        if r.status_code == 200:
            result = r.json()
            exp = result.get("expedition_result", {})
            char = result.get("character", {})
            print(f"  🎉 Expedition complete!")
            print(f"     Merc: {exp.get('merc_name')}")
            print(f"     Loot: {exp.get('loot')}")
            print(f"     Rare drop: {exp.get('rare_found')}")
            print(f"     XP: +{exp.get('xp_gain')} | Exploration: +{exp.get('exploration_gain')}%")
            print(f"     Loyalty hires: {exp.get('loyalty_hires')}")
            print(f"     Gold after: {char.get('gold', 0)}")
        else:
            print(f"  Collect failed: {r.text[:200]}")

        step(20, "Trying to re-hire immediately (cooldown check)...")
        r = s.post(f"{BASE}/game/expedition/start", json={"biome_id": biome, "hours": 1})
        if r.status_code == 200:
            print(f"  Re-hired (no cooldown?)")
        else:
            print(f"  ⏳ Cooldown active: {r.json().get('detail', r.text[:80])}")
    else:
        print(f"  Hire failed: {r.text[:200]}")
else:
    print(f"  ❌ Not enough gold! Have {gold}g, need {merc.get('hourly_rate')}g/hr")
    print(f"  Need to hunt more monsters first...")

# ============================================================
# 10. FINAL STATUS
# ============================================================
sep("FINAL CHARACTER STATUS")
step(21, "Final character check...")
# Re-fetch character via the game state endpoint
r = s.get(f"{BASE}/game/state")
if r.status_code == 200:
    char = r.json().get("character", r.json())
    print(f"  Name: {char.get('name')}")
    print(f"  Level: {char.get('level', 1)} | XP: {char.get('xp', 0)}")
    print(f"  Gold: {char.get('gold', 0)}")
    print(f"  Biome: {char.get('current_biome')}")
    print(f"  Exploration: {char.get('exploration_progress', {})}")
    inventory = char.get("inventory", [])
    if inventory:
        print(f"  Inventory ({len(inventory)} items):")
        for item in inventory[:10]:
            if isinstance(item, dict):
                print(f"    - {item.get('item_id', item.get('name', '?'))} x{item.get('quantity', 1)}")
            else:
                print(f"    - {item}")
else:
    print(f"  State fetch: {r.status_code} {r.text[:100]}")

print(f"\n{'='*60}")
print(f"  GAME SESSION COMPLETE — Thanks for playing!")
print(f"{'='*60}")
