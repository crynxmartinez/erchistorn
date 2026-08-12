import requests, json, time
s = requests.Session()
BASE = 'http://127.0.0.1:8000/api'

# Register fresh account
uname = f"debug_{int(time.time())}"
r = s.post(f'{BASE}/auth/register', json={
    "username": uname,
    "password": "Test1234!",
    "email": f"{uname}@test.com",
    "display_name": "Debug Knight",
})
print(f'Register: {r.status_code} {r.text[:100]}')

# Get races
r = s.get(f'{BASE}/game/data/races')
races = r.json().get("races", [])
human = next((rc for rc in races if rc["id"] == "human"), None)
gifts = human.get("gifts", []) if human else []
gift_id = gifts[0]["id"] if gifts else ""
print(f"Gift: {gift_id}")

# Get origins
r = s.get(f'{BASE}/game/data/origins/knight')
origins = r.json().get("origins", [])
origin_id = origins[0]["id"] if origins else ""
print(f"Origin: {origin_id}")

# Get portraits
r = s.get(f'{BASE}/game/data/portraits')
portraits = r.json().get("portraits", [])
portrait_id = portraits[0]["id"] if portraits else "p1"

# Create character
r = s.post(f'{BASE}/game/character', json={
    "name": "DebugKnight",
    "race": "human",
    "mastery": "knight",
    "role": "fighter",
    "origin": origin_id,
    "portrait_id": portrait_id,
    "racial_gift": gift_id,
    "oath": "iron",
})
print(f'Create char: {r.status_code} {r.text[:200]}')

r = s.get(f'{BASE}/game/character')
ch = r.json().get('character')
print(f"Char: L{ch['level']} HP {ch['hp']}/{ch['max_hp']} biome={ch.get('current_biome')} town={ch.get('current_town')} gold={ch.get('gold')}")

# Leave town
if ch.get('current_town'):
    s.post(f'{BASE}/game/town/leave')
    r = s.get(f'{BASE}/game/character')
    ch = r.json().get('character')

biome = ch.get('current_biome', 'golden_plains')
print(f'Biome: {biome}')

# Explore a few times
for i in range(5):
    r = s.post(f'{BASE}/game/action', json={'biome_id': biome, 'action_id': 'explore'})
    print(f'Explore {i+1}: {r.status_code}')
    if r.status_code == 200:
        data = r.json()
        result = data.get("result", data)
        discoveries = result.get("discoveries", [])
        for d in discoveries:
            print(f"  Found: {d.get('kind')} = {d.get('name')}")

# Check biome actions
r = s.get(f'{BASE}/game/data/biome/{biome}/actions')
data = r.json()
actions = data.get('actions', [])
print(f'\nActions for {biome}: {len(actions)}')
for a in actions[:15]:
    print(f"  kind={a.get('kind')} id={a.get('id')} name={a.get('name')} discovered={a.get('discovered')} stock={a.get('stock')} threat={a.get('threat')}")

# Try gather
r = s.post(f'{BASE}/game/action', json={'biome_id': biome, 'action_id': 'gather'})
print(f'\nGather: {r.status_code}')
if r.status_code == 200:
    print(json.dumps(r.json(), indent=2)[:600])
else:
    print(r.text[:300])

# Try combat
monsters = [a for a in actions if a.get('kind') == 'monster' and a.get('discovered') and a.get('stock', 0) > 0]
print(f'\nAvailable monsters: {len(monsters)}')
if monsters:
    m = monsters[0]
    print(f"Combat with: {m.get('name')} (id={m.get('id')})")
    r = s.post(f'{BASE}/game/combat/start', json={'monster_id': m['id'], 'biome_id': biome})
    print(f'Combat start: {r.status_code}')
    if r.status_code == 200:
        cd = r.json()
        cid = cd.get('combat_id')
        print(f'Combat ID: {cid}')
        for turn in range(10):
            r2 = s.post(f'{BASE}/game/combat/turn', json={'combat_id': cid, 'action_type': 'strike'})
            print(f'Turn {turn+1}: {r2.status_code}')
            if r2.status_code == 200:
                result = r2.json().get('result', {})
                vic = result.get('victory')
                if vic is not None:
                    print(f"  Victory: {vic} rewards: {result.get('rewards')}")
                    break
    else:
        print(r.text[:300])
