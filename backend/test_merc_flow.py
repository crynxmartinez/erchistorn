"""Quick integration test: register → create character → explore → hunt → hire merc → collect."""
import requests
import time
import json

BASE = "http://127.0.0.1:8000/api"
s = requests.Session()

# 1. Register a test user
test_user = f"merctest_{int(time.time())}"
print(f"1. Registering user: {test_user}...")
r = s.post(f"{BASE}/auth/register", json={
    "username": test_user,
    "password": "Test1234!",
    "email": f"{test_user}@test.com",
    "display_name": "Merc Tester",
})
print(f"   Register: {r.status_code}")
if r.status_code != 200:
    print(f"   Error: {r.text}")
    exit(1)
print(f"   Cookies: {dict(s.cookies)}")

# 2. Create character
print("2. Creating character...")
r = s.post(f"{BASE}/game/character", json={
    "name": "MercTestHero",
    "race": "human",
    "role": "fighter",
    "mastery": "knight",
    "origin": "guardians_shield",
    "portrait_id": "Aldric",
    "racial_gift": "oathbound",
    "oath": "protect_the_weak",
})
print(f"   Create: {r.status_code}")
if r.status_code != 200:
    print(f"   Error: {r.text}")
    exit(1)
char = r.json().get("character", r.json())
print(f"   Character: {char.get('name')} | Gold: {char.get('gold')} | Biome: {char.get('current_biome')}")

# 3. Explore the biome a few times to get exploration %
biome = char.get("current_biome", "golden_plains")
print(f"3. Exploring {biome} (5 times)...")
for i in range(5):
    r = s.post(f"{BASE}/game/action", json={"action_id": "explore", "biome_id": biome})
    if r.status_code == 200:
        data = r.json()
        print(f"   Explore {i+1}: outcome={data.get('outcome')} progress={data.get('new_progress_pct')}")
    else:
        print(f"   Explore {i+1}: {r.status_code} {r.text[:100]}")

# 4. Hunt a monster
print("4. Hunting a monster...")
r = s.get(f"{BASE}/game/data/biome/{biome}/actions")
if r.status_code == 200:
    actions = r.json().get("actions", [])
    hunt_action = next((a for a in actions if a.get("id") == "hunt"), None)
    if hunt_action and hunt_action.get("monsters"):
        monster = hunt_action["monsters"][0]
        print(f"   Target: {monster.get('name')} (id={monster.get('id')})")
        r = s.post(f"{BASE}/game/combat/start", json={"biome_id": biome, "monster_id": monster["id"]})
        print(f"   Combat start: {r.status_code}")
        if r.status_code == 200:
            combat = r.json()
            state = combat.get("state", combat)
            print(f"   Combat started! Enemy: {state.get('enemy_name', 'unknown')} HP: {state.get('enemy_hp')}")
            # Auto-fight: just attack until done
            turn = 0
            while state.get("enemy_hp", 0) > 0 and state.get("player_hp", 0) > 0 and turn < 20:
                turn += 1
                r = s.post(f"{BASE}/game/combat/action", json={"action": "attack"})
                if r.status_code != 200:
                    print(f"   Combat action {turn}: {r.status_code} {r.text[:100]}")
                    break
                state = r.json().get("state", r.json())
                if state.get("combat_over"):
                    print(f"   Combat over! Won: {state.get('victory')} | Gold earned: {state.get('gold_earned', 0)}")
                    break
            else:
                print(f"   Combat ended after {turn} turns (timeout or limit)")
        else:
            print(f"   Error: {r.text[:200]}")
    else:
        print("   No hunt action or monsters found")
else:
    print(f"   Actions fetch: {r.status_code}")

# 5. Check character gold
print("5. Checking character state...")
r = s.get(f"{BASE}/character")
if r.status_code == 200:
    char = r.json().get("character", r.json())
    print(f"   Gold: {char.get('gold')} | XP: {char.get('xp')} | Level: {char.get('level')}")
    print(f"   Exploration: {char.get('exploration_progress', {})}")
else:
    print(f"   Error: {r.status_code}")

# 6. Get merc info for current biome
print(f"6. Getting merc info for {biome}...")
r = s.get(f"{BASE}/game/expedition/merc/{biome}")
print(f"   Merc info: {r.status_code}")
if r.status_code == 200:
    data = r.json()
    merc = data.get("merc", {})
    print(f"   Merc: {merc.get('name')} | Rank: {merc.get('rank')} | Specialty: {merc.get('specialty')}")
    print(f"   Rate: {merc.get('hourly_rate')}g/hr | Efficiency: {merc.get('efficiency')}")
    print(f"   Quirk: {merc.get('quirk')} | Loyalty: {merc.get('loyalty_hires', 0)} hires")
    print(f"   Loot preview: {merc.get('loot_preview', [])}")
    print(f"   Rare preview: {merc.get('rare_preview', [])}")
    print(f"   Exploration: {data.get('exploration_pct')}% (min: {data.get('min_exploration')}%)")
    print(f"   Queue: {data.get('queue')}")
    print(f"   Cooldown: {data.get('cooldown_until')}")
else:
    print(f"   Error: {r.text[:200]}")

# 7. Hire merc for 1 hour
print("7. Hiring merc for 1 hour...")
r = s.post(f"{BASE}/game/expedition/start", json={"biome_id": biome, "hours": 1})
print(f"   Start: {r.status_code}")
if r.status_code == 200:
    result = r.json()
    exp_result = result.get("expedition_result", {})
    char = result.get("character", {})
    print(f"   Success! Gold spent: {exp_result.get('gold_spent')} | Gold left: {char.get('gold')}")
    queue = char.get("expedition_queue", {})
    print(f"   Queue: merc={queue.get('merc_name')} finishes_at={queue.get('finishes_at')}")
else:
    print(f"   Error: {r.text[:200]}")

# 8. Try to collect (will fail - not done yet)
print("8. Trying to collect (should fail - not done)...")
r = s.post(f"{BASE}/game/expedition/collect")
print(f"   Collect: {r.status_code}")
if r.status_code == 200:
    print(f"   Unexpected success: {r.json()}")
else:
    print(f"   Expected error: {r.text[:150]}")

# 9. Simulate time passing by directly updating the queue in DB
print("9. Simulating time passage (updating queue in DB)...")
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta
from pathlib import Path

load_dotenv(Path(__file__).parent / ".env")

async def fast_forward():
    client = AsyncIOMotorClient(os.environ["MONGO_URL"])
    db = client[os.environ["DB_NAME"]]
    # Find our character
    char = await db.characters.find_one({"name": "MercTestHero"})
    if not char:
        print("   Character not found in DB!")
        return
    queue = char.get("expedition_queue")
    if not queue:
        print("   No expedition queue found!")
        return
    # Set finishes_at to 1 second ago
    queue["finishes_at"] = (datetime.now(timezone.utc) - timedelta(seconds=1)).isoformat()
    await db.characters.update_one(
        {"_id": char["_id"]},
        {"$set": {"expedition_queue": queue}},
    )
    print(f"   Queue fast-forwarded! finishes_at set to past.")
    client.close()

asyncio.run(fast_forward())

# 10. Collect the expedition
print("10. Collecting expedition...")
r = s.post(f"{BASE}/game/expedition/collect")
print(f"   Collect: {r.status_code}")
if r.status_code == 200:
    result = r.json()
    exp = result.get("expedition_result", {})
    char = result.get("character", {})
    print(f"   Success! Merc: {exp.get('merc_name')}")
    print(f"   Loot: {exp.get('loot')}")
    print(f"   Rare found: {exp.get('rare_found')}")
    print(f"   XP gain: {exp.get('xp_gain')}")
    print(f"   Exploration gain: {exp.get('exploration_gain')}")
    print(f"   Loyalty hires: {exp.get('loyalty_hires')}")
    print(f"   Gold after: {char.get('gold')}")
else:
    print(f"   Error: {r.text[:200]}")

# 11. Try to hire again immediately (should hit cooldown)
print("11. Trying to hire again immediately (should hit cooldown)...")
r = s.post(f"{BASE}/game/expedition/start", json={"biome_id": biome, "hours": 1})
print(f"   Start: {r.status_code}")
if r.status_code == 200:
    print(f"   Unexpected success!")
else:
    print(f"   Expected cooldown error: {r.text[:150]}")

print("\n=== TEST COMPLETE ===")
