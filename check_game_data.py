#!/usr/bin/env python3
import requests
import json

BASE_URL = "https://db-integration-28.preview.emergentagent.com/api"
session = requests.Session()

# Login first
login_resp = session.post(f"{BASE_URL}/auth/login", json={
    "email": "theron_x60egre5@erchis.test",
    "password": "DragonSlayer2024!"
})

if login_resp.status_code == 200:
    print("✅ Logged in successfully\n")
    
    # Get races
    races_resp = session.get(f"{BASE_URL}/game/data/races")
    if races_resp.status_code == 200:
        races = races_resp.json().get('races', [])
        print(f"RACES ({len(races)}):")
        for r in races[:3]:
            print(f"  - {r.get('id')}: {r.get('name')}")
    
    # Get roles
    roles_resp = session.get(f"{BASE_URL}/game/data/roles")
    if roles_resp.status_code == 200:
        roles = roles_resp.json().get('roles', [])
        print(f"\nROLES ({len(roles)}):")
        for r in roles[:3]:
            print(f"  - {r.get('id')}: {r.get('name')}")
            print(f"    Available masteries: {r.get('available_masteries', [])}")
    
    # Get masteries
    masteries_resp = session.get(f"{BASE_URL}/game/data/masteries")
    if masteries_resp.status_code == 200:
        masteries = masteries_resp.json().get('masteries', [])
        print(f"\nMASTERIES ({len(masteries)}):")
        for m in masteries[:5]:
            print(f"  - {m.get('id')}: {m.get('name')}")
            print(f"    Available to roles: {m.get('available_to', [])}")
    
    # Get origins
    origins_resp = session.get(f"{BASE_URL}/game/data/origins")
    if origins_resp.status_code == 200:
        origins = origins_resp.json().get('origins', [])
        print(f"\nORIGINS ({len(origins)}):")
        knight_origins = [o for o in origins if o.get('mastery') == 'knight']
        print(f"  Knight origins: {[o.get('id') for o in knight_origins]}")
else:
    print(f"❌ Login failed: {login_resp.status_code}")
