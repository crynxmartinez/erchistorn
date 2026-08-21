#!/usr/bin/env python3
import requests
import json

BASE_URL = "https://db-integration-28.preview.emergentagent.com/api"
session = requests.Session()

# Login
login_resp = session.post(f"{BASE_URL}/auth/login", json={
    "email": "theron_13i799ft@erchis.test",
    "password": "DragonSlayer2024!"
})

if login_resp.status_code == 200:
    print("✅ Logged in\n")
    
    # Get character
    char_resp = session.get(f"{BASE_URL}/game/character")
    print(f"Status: {char_resp.status_code}")
    if char_resp.status_code == 200:
        data = char_resp.json()
        print(f"\nCharacter keys: {list(data.keys())[:20]}")
        print(f"\nName: {data.get('name')}")
        print(f"Race: {data.get('race')}")
        print(f"Level: {data.get('level')}")
        print(f"XP: {data.get('xp')}")
        print(f"Gold: {data.get('gold')}")
    else:
        print(f"Error: {char_resp.text}")
