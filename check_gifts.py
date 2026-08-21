#!/usr/bin/env python3
import requests
import json

BASE_URL = "https://db-integration-28.preview.emergentagent.com/api"
session = requests.Session()

# Login first
login_resp = session.post(f"{BASE_URL}/auth/login", json={
    "email": "theron_2h84zr9f@erchis.test",
    "password": "DragonSlayer2024!"
})

if login_resp.status_code == 200:
    print("✅ Logged in successfully\n")
    
    # Get races with full details
    races_resp = session.get(f"{BASE_URL}/game/data/races")
    if races_resp.status_code == 200:
        races = races_resp.json().get('races', [])
        human = next((r for r in races if r.get('id') == 'human'), None)
        if human:
            print("HUMAN RACE:")
            print(f"  Gifts: {json.dumps(human.get('gifts', []), indent=4)}")
else:
    print(f"❌ Login failed: {login_resp.status_code}")
