#!/usr/bin/env python3
"""
Focused smoke test for Erchis Fantasy Dice RPG backend.
Tests: Auth flow, Character creation, and one game action to verify MongoDB persistence.
"""
import requests
import json
import time
import random
import string

# Backend URL from frontend/.env
BASE_URL = "https://db-integration-28.preview.emergentagent.com/api"

# Generate unique test email
unique_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
TEST_EMAIL = f"theron_{unique_id}@erchis.test"
TEST_PASSWORD = "DragonSlayer2024!"
TEST_DISPLAY_NAME = f"Theron the Brave"

# Session to maintain cookies
session = requests.Session()

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def print_result(test_name, passed, details=""):
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"{status} | {test_name}")
    if details:
        print(f"     Details: {details}")

def test_auth_flow():
    """Test 1: AUTH FLOW - register, me, logout, login"""
    print_section("TEST 1: AUTH FLOW")
    
    # 1.1 Register
    print("\n1.1 Testing POST /auth/register")
    register_payload = {
        "display_name": TEST_DISPLAY_NAME,
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD
    }
    
    try:
        resp = session.post(f"{BASE_URL}/auth/register", json=register_payload)
        print(f"     Status: {resp.status_code}")
        
        if resp.status_code == 200:
            data = resp.json()
            print(f"     Response: {json.dumps(data, indent=2)}")
            print_result("Register", True, f"User created: {data.get('email')}")
            user_id = data.get('id')
        else:
            print(f"     Error: {resp.text}")
            print_result("Register", False, f"Status {resp.status_code}: {resp.text}")
            return False
    except Exception as e:
        print_result("Register", False, f"Exception: {str(e)}")
        return False
    
    # 1.2 Get current user (with cookie)
    print("\n1.2 Testing GET /auth/me (with cookie)")
    try:
        resp = session.get(f"{BASE_URL}/auth/me")
        print(f"     Status: {resp.status_code}")
        
        if resp.status_code == 200:
            data = resp.json()
            print(f"     Response: {json.dumps(data, indent=2)}")
            if data.get('email') == TEST_EMAIL:
                print_result("Get /auth/me", True, f"User verified: {data.get('email')}")
            else:
                print_result("Get /auth/me", False, f"Email mismatch: expected {TEST_EMAIL}, got {data.get('email')}")
                return False
        else:
            print(f"     Error: {resp.text}")
            print_result("Get /auth/me", False, f"Status {resp.status_code}: {resp.text}")
            return False
    except Exception as e:
        print_result("Get /auth/me", False, f"Exception: {str(e)}")
        return False
    
    # 1.3 Logout
    print("\n1.3 Testing POST /auth/logout")
    try:
        resp = session.post(f"{BASE_URL}/auth/logout")
        print(f"     Status: {resp.status_code}")
        
        if resp.status_code == 200:
            data = resp.json()
            print(f"     Response: {json.dumps(data, indent=2)}")
            print_result("Logout", True, "Logged out successfully")
        else:
            print(f"     Error: {resp.text}")
            print_result("Logout", False, f"Status {resp.status_code}: {resp.text}")
            return False
    except Exception as e:
        print_result("Logout", False, f"Exception: {str(e)}")
        return False
    
    # 1.4 Login
    print("\n1.4 Testing POST /auth/login")
    login_payload = {
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD
    }
    
    try:
        resp = session.post(f"{BASE_URL}/auth/login", json=login_payload)
        print(f"     Status: {resp.status_code}")
        
        if resp.status_code == 200:
            data = resp.json()
            print(f"     Response: {json.dumps(data, indent=2)}")
            print_result("Login", True, f"Logged in: {data.get('email')}")
        else:
            print(f"     Error: {resp.text}")
            print_result("Login", False, f"Status {resp.status_code}: {resp.text}")
            return False
    except Exception as e:
        print_result("Login", False, f"Exception: {str(e)}")
        return False
    
    return True

def test_character_creation():
    """Test 2: CHARACTER CREATION - fetch data endpoints and create character"""
    print_section("TEST 2: CHARACTER CREATION FLOW")
    
    # 2.1 Fetch races
    print("\n2.1 Testing GET /game/data/races")
    try:
        resp = session.get(f"{BASE_URL}/game/data/races")
        print(f"     Status: {resp.status_code}")
        
        if resp.status_code == 200:
            data = resp.json()
            races = data.get('races', [])
            print(f"     Found {len(races)} races")
            if races:
                print(f"     Sample race: {races[0].get('id')}")
                print_result("Get races", True, f"{len(races)} races available")
            else:
                print_result("Get races", False, "No races returned")
                return False
        else:
            print(f"     Error: {resp.text}")
            print_result("Get races", False, f"Status {resp.status_code}")
            return False
    except Exception as e:
        print_result("Get races", False, f"Exception: {str(e)}")
        return False
    
    # 2.2 Fetch roles
    print("\n2.2 Testing GET /game/data/roles")
    try:
        resp = session.get(f"{BASE_URL}/game/data/roles")
        print(f"     Status: {resp.status_code}")
        
        if resp.status_code == 200:
            data = resp.json()
            roles = data.get('roles', [])
            print(f"     Found {len(roles)} roles")
            if roles:
                print(f"     Sample role: {roles[0].get('id')}")
                print_result("Get roles", True, f"{len(roles)} roles available")
            else:
                print_result("Get roles", False, "No roles returned")
                return False
        else:
            print(f"     Error: {resp.text}")
            print_result("Get roles", False, f"Status {resp.status_code}")
            return False
    except Exception as e:
        print_result("Get roles", False, f"Exception: {str(e)}")
        return False
    
    # 2.3 Fetch masteries
    print("\n2.3 Testing GET /game/data/masteries")
    try:
        resp = session.get(f"{BASE_URL}/game/data/masteries")
        print(f"     Status: {resp.status_code}")
        
        if resp.status_code == 200:
            data = resp.json()
            masteries = data.get('masteries', [])
            print(f"     Found {len(masteries)} masteries")
            if masteries:
                print(f"     Sample mastery: {masteries[0].get('id')}")
                print_result("Get masteries", True, f"{len(masteries)} masteries available")
            else:
                print_result("Get masteries", False, "No masteries returned")
                return False
        else:
            print(f"     Error: {resp.text}")
            print_result("Get masteries", False, f"Status {resp.status_code}")
            return False
    except Exception as e:
        print_result("Get masteries", False, f"Exception: {str(e)}")
        return False
    
    # 2.4 Fetch origins for a specific mastery (knight)
    print("\n2.4 Testing GET /game/data/origins")
    try:
        resp = session.get(f"{BASE_URL}/game/data/origins")
        print(f"     Status: {resp.status_code}")
        
        if resp.status_code == 200:
            data = resp.json()
            origins = data.get('origins', [])
            print(f"     Found {len(origins)} origins")
            if origins:
                print(f"     Sample origin: {origins[0].get('id')}")
                print_result("Get origins", True, f"{len(origins)} origins available")
            else:
                print_result("Get origins", False, "No origins returned")
                return False
        else:
            print(f"     Error: {resp.text}")
            print_result("Get origins", False, f"Status {resp.status_code}")
            return False
    except Exception as e:
        print_result("Get origins", False, f"Exception: {str(e)}")
        return False
    
    # 2.5 Create character
    print("\n2.5 Testing POST /game/character")
    
    # Build a valid character payload based on the game's requirements
    # Using human knight with oath, which is a common starting combination
    character_payload = {
        "name": "Theron Stormbreaker",
        "race": "human",
        "role": "fighter",
        "mastery": "knight",
        "origin": "guardians_shield",
        "portrait_id": "knight_1",
        "oath": "valor",  # Required for humans
        "racial_gift": "oathbound",  # Valid human racial gift
        "heritage": None,
        "beast_aspect": None,
        "marine_adaptation": None
    }
    
    try:
        resp = session.post(f"{BASE_URL}/game/character", json=character_payload)
        print(f"     Status: {resp.status_code}")
        
        if resp.status_code == 200:
            data = resp.json()
            print(f"     Character created: {data.get('name')} (Level {data.get('level')})")
            print(f"     Race: {data.get('race')}, Mastery: {data.get('mastery')}")
            print(f"     HP: {data.get('hp')}/{data.get('max_hp')}, Gold: {data.get('gold')}")
            print_result("Create character", True, f"Character '{data.get('name')}' created successfully")
            return data
        else:
            print(f"     Error: {resp.text}")
            print_result("Create character", False, f"Status {resp.status_code}: {resp.text}")
            return False
    except Exception as e:
        print_result("Create character", False, f"Exception: {str(e)}")
        return False

def test_character_persistence(initial_character):
    """Test 2.6: Verify character persists in DB"""
    print("\n2.6 Testing GET /game/character (verify persistence)")
    
    try:
        resp = session.get(f"{BASE_URL}/game/character")
        print(f"     Status: {resp.status_code}")
        
        if resp.status_code == 200:
            data = resp.json()
            # The character data is nested under 'character' key
            character = data.get('character', data)
            if character.get('name') == initial_character.get('name'):
                print(f"     Character retrieved: {character.get('name')}")
                print_result("Character persistence", True, "Character persisted in MongoDB")
                return character
            else:
                print_result("Character persistence", False, f"Name mismatch: expected {initial_character.get('name')}, got {character.get('name')}")
                return False
        else:
            print(f"     Error: {resp.text}")
            print_result("Character persistence", False, f"Status {resp.status_code}")
            return False
    except Exception as e:
        print_result("Character persistence", False, f"Exception: {str(e)}")
        return False

def test_game_action(character_before):
    """Test 3: ONE GAME ACTION - perform action and verify state change"""
    print_section("TEST 3: GAME ACTION (Core Play Loop)")
    
    # Get the character's current biome
    current_biome = character_before.get('current_biome', 'forest_1')
    print(f"\n3.1 Character is in biome: {current_biome}")
    
    # Perform an explore action (safest action that doesn't require specific resources)
    print(f"\n3.2 Testing POST /game/action (explore in {current_biome})")
    
    action_payload = {
        "action_id": "explore",
        "biome_id": current_biome,
        "target_id": None  # Let the game choose a random target
    }
    
    try:
        resp = session.post(f"{BASE_URL}/game/action", json=action_payload)
        print(f"     Status: {resp.status_code}")
        
        if resp.status_code == 200:
            data = resp.json()
            print(f"     Action result: {data.get('message', 'Success')}")
            if data.get('rewards'):
                print(f"     Rewards: {json.dumps(data.get('rewards'), indent=2)}")
            print_result("Perform action", True, f"Action completed: {data.get('message', 'gather')}")
        else:
            print(f"     Error: {resp.text}")
            print_result("Perform action", False, f"Status {resp.status_code}: {resp.text}")
            return False
    except Exception as e:
        print_result("Perform action", False, f"Exception: {str(e)}")
        return False
    
    # 3.3 Verify state changed
    print("\n3.3 Testing GET /game/character (verify state change)")
    
    try:
        resp = session.get(f"{BASE_URL}/game/character")
        print(f"     Status: {resp.status_code}")
        
        if resp.status_code == 200:
            data = resp.json()
            # The character data is nested under 'character' key
            character_after = data.get('character', data)
            
            # Check for state changes
            xp_before = character_before.get('xp', 0)
            xp_after = character_after.get('xp', 0)
            
            gold_before = character_before.get('gold', 0)
            gold_after = character_after.get('gold', 0)
            
            inv_before_len = len(character_before.get('inventory', []))
            inv_after_len = len(character_after.get('inventory', []))
            
            print(f"     XP: {xp_before} → {xp_after} (Δ{xp_after - xp_before})")
            print(f"     Gold: {gold_before} → {gold_after} (Δ{gold_after - gold_before})")
            print(f"     Inventory items: {inv_before_len} → {inv_after_len}")
            
            # Check if any state changed
            state_changed = (xp_after != xp_before or 
                           gold_after != gold_before or 
                           inv_after_len != inv_before_len)
            
            if state_changed:
                print_result("State persistence", True, "Character state changed and persisted in MongoDB")
                return True
            else:
                print_result("State persistence", False, "No state change detected after action")
                return False
        else:
            print(f"     Error: {resp.text}")
            print_result("State persistence", False, f"Status {resp.status_code}")
            return False
    except Exception as e:
        print_result("State persistence", False, f"Exception: {str(e)}")
        return False

def main():
    print("\n" + "="*60)
    print("  ERCHIS RPG - FOCUSED SMOKE TEST")
    print("  Testing MongoDB persistence on Emergent environment")
    print("="*60)
    print(f"\nBackend URL: {BASE_URL}")
    print(f"Test User: {TEST_EMAIL}")
    
    # Test 1: Auth Flow
    auth_success = test_auth_flow()
    if not auth_success:
        print("\n❌ AUTH FLOW FAILED - Stopping tests")
        return False
    
    # Test 2: Character Creation
    character = test_character_creation()
    if not character:
        print("\n❌ CHARACTER CREATION FAILED - Stopping tests")
        return False
    
    # Test 2.6: Character Persistence
    character_retrieved = test_character_persistence(character)
    if not character_retrieved:
        print("\n❌ CHARACTER PERSISTENCE FAILED - Stopping tests")
        return False
    
    # Test 3: Game Action
    action_success = test_game_action(character_retrieved)
    if not action_success:
        print("\n❌ GAME ACTION FAILED")
        return False
    
    # Final Summary
    print_section("SMOKE TEST SUMMARY")
    print("✅ Auth Flow: PASSED")
    print("✅ Character Creation: PASSED")
    print("✅ Character Persistence: PASSED")
    print("✅ Game Action & State Persistence: PASSED")
    print("\n🎉 ALL TESTS PASSED - MongoDB persistence working correctly!")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ FATAL ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        exit(1)
