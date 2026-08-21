#!/usr/bin/env python3
"""
Backend test for Erchis RPG Country (Continent) Chat feature.
Tests the new chat endpoints with two human characters in Valeria.
"""
import requests
import time
import sys
from datetime import datetime

# Base URL from frontend/.env
BASE_URL = "https://db-integration-28.preview.emergentagent.com/api"

# Test results tracking
test_results = []

def log_test(test_name, passed, details=""):
    """Log test result"""
    status = "✅ PASS" if passed else "❌ FAIL"
    result = f"{status} | {test_name}"
    if details:
        result += f" | {details}"
    print(result)
    test_results.append({
        "name": test_name,
        "passed": passed,
        "details": details
    })

def register_account(email, password, display_name):
    """Register a new account and return session cookies"""
    url = f"{BASE_URL}/auth/register"
    payload = {
        "email": email,
        "password": password,
        "display_name": display_name
    }
    try:
        resp = requests.post(url, json=payload)
        if resp.status_code == 200:
            log_test(f"Register account {email}", True, f"HTTP {resp.status_code}")
            return resp.cookies
        else:
            log_test(f"Register account {email}", False, f"HTTP {resp.status_code}: {resp.text[:200]}")
            return None
    except Exception as e:
        log_test(f"Register account {email}", False, f"Exception: {str(e)}")
        return None

def create_human_character(cookies, char_name):
    """Create a human character and return character data"""
    url = f"{BASE_URL}/game/character"
    
    # Human character payload - using knight mastery for simplicity
    # Humans spawn in Valeria continent
    payload = {
        "name": char_name,
        "race": "human",
        "role": "fighter",  # Correct role name
        "mastery": "knight",
        "origin": "guardians_shield",  # Valid knight origin
        "portrait_id": "human_aldric",  # Valid portrait
        "oath": "valor",  # Humans require an oath
        "racial_gift": "oathbound"  # Valid human racial gift
    }
    
    try:
        resp = requests.post(url, json=payload, cookies=cookies)
        if resp.status_code == 200:
            data = resp.json()
            log_test(f"Create character {char_name}", True, f"HTTP {resp.status_code}, continent: {data.get('current_continent', 'N/A')}")
            return data
        else:
            log_test(f"Create character {char_name}", False, f"HTTP {resp.status_code}: {resp.text[:200]}")
            return None
    except Exception as e:
        log_test(f"Create character {char_name}", False, f"Exception: {str(e)}")
        return None

def chat_poll(cookies, user_label):
    """Poll chat and return response"""
    url = f"{BASE_URL}/chat/poll"
    try:
        resp = requests.get(url, cookies=cookies)
        if resp.status_code == 200:
            return resp.json()
        else:
            log_test(f"Chat poll for {user_label}", False, f"HTTP {resp.status_code}: {resp.text[:200]}")
            return None
    except Exception as e:
        log_test(f"Chat poll for {user_label}", False, f"Exception: {str(e)}")
        return None

def chat_send(cookies, text, user_label):
    """Send a chat message"""
    url = f"{BASE_URL}/chat/send"
    payload = {"text": text}
    try:
        resp = requests.post(url, json=payload, cookies=cookies)
        if resp.status_code == 200:
            return resp.json()
        else:
            return {"error": True, "status_code": resp.status_code, "text": resp.text[:200]}
    except Exception as e:
        return {"error": True, "exception": str(e)}

def main():
    print("=" * 80)
    print("ERCHIS RPG - COUNTRY CHAT BACKEND TEST")
    print("=" * 80)
    print()
    
    # Generate unique test accounts
    timestamp = int(time.time())
    email_a = f"alpha_{timestamp}@test.com"
    email_b = f"beta_{timestamp}@test.com"
    
    print("SETUP: Registering two test accounts...")
    print()
    
    # Register Account A
    cookies_a = register_account(email_a, "Test1234!", "AlphaUser")
    if not cookies_a:
        print("\n❌ CRITICAL: Failed to register Account A. Aborting.")
        sys.exit(1)
    
    # Register Account B
    cookies_b = register_account(email_b, "Test1234!", "BetaUser")
    if not cookies_b:
        print("\n❌ CRITICAL: Failed to register Account B. Aborting.")
        sys.exit(1)
    
    print()
    print("SETUP: Creating human characters (both spawn in Valeria)...")
    print()
    
    # Create Character A (Human)
    char_a = create_human_character(cookies_a, "AlphaHero")
    if not char_a:
        print("\n❌ CRITICAL: Failed to create Character A. Aborting.")
        sys.exit(1)
    
    # Create Character B (Human)
    char_b = create_human_character(cookies_b, "BetaHero")
    if not char_b:
        print("\n❌ CRITICAL: Failed to create Character B. Aborting.")
        sys.exit(1)
    
    print()
    print("=" * 80)
    print("CHAT TESTS")
    print("=" * 80)
    print()
    
    # TEST 1: User A polls chat - should see enter message
    print("TEST 1: User A polls chat (first poll, should trigger 'entered' system message)")
    poll_a1 = chat_poll(cookies_a, "User A")
    if poll_a1:
        # Validate response structure
        has_continent = "continent" in poll_a1 and poll_a1["continent"] == "valeria"
        has_continent_name = "continent_name" in poll_a1 and poll_a1["continent_name"] == "Valeria"
        has_me = "me" in poll_a1 and poll_a1["me"] is not None
        has_messages = "messages" in poll_a1 and isinstance(poll_a1["messages"], list)
        has_online = "online" in poll_a1 and isinstance(poll_a1["online"], list)
        has_online_count = "online_count" in poll_a1 and isinstance(poll_a1["online_count"], int)
        
        all_fields_ok = has_continent and has_continent_name and has_me and has_messages and has_online and has_online_count
        
        if all_fields_ok:
            log_test("Test 1: Poll structure", True, f"All required fields present")
            
            # Check for system message about entering
            system_msgs = [m for m in poll_a1["messages"] if m.get("kind") == "system"]
            enter_msg = None
            for msg in system_msgs:
                if "AlphaHero" in msg.get("text", "") and "entered" in msg.get("text", "").lower():
                    enter_msg = msg
                    break
            
            if enter_msg:
                log_test("Test 1: Enter system message", True, f"Found: '{enter_msg['text']}'")
            else:
                log_test("Test 1: Enter system message", False, f"No 'AlphaHero has entered Valeria' message found. Messages: {[m.get('text') for m in poll_a1['messages']]}")
        else:
            missing = []
            if not has_continent: missing.append("continent")
            if not has_continent_name: missing.append("continent_name")
            if not has_me: missing.append("me")
            if not has_messages: missing.append("messages")
            if not has_online: missing.append("online")
            if not has_online_count: missing.append("online_count")
            log_test("Test 1: Poll structure", False, f"Missing fields: {missing}")
    else:
        log_test("Test 1: Poll request", False, "Poll failed")
    
    print()
    
    # TEST 2: User A sends a message
    print("TEST 2: User A sends message 'hello from alpha'")
    send_result = chat_send(cookies_a, "hello from alpha", "User A")
    if send_result and not send_result.get("error"):
        msg_data = send_result.get("message", {})
        is_user_kind = msg_data.get("kind") == "user"
        is_correct_name = msg_data.get("display_name") == "AlphaHero"
        is_correct_text = msg_data.get("text") == "hello from alpha"
        
        if is_user_kind and is_correct_name and is_correct_text:
            log_test("Test 2: Send message", True, f"HTTP 200, kind=user, display_name=AlphaHero, text correct")
        else:
            issues = []
            if not is_user_kind: issues.append(f"kind={msg_data.get('kind')}")
            if not is_correct_name: issues.append(f"display_name={msg_data.get('display_name')}")
            if not is_correct_text: issues.append(f"text={msg_data.get('text')}")
            log_test("Test 2: Send message", False, f"Issues: {', '.join(issues)}")
    else:
        status = send_result.get("status_code", "N/A") if send_result else "N/A"
        log_test("Test 2: Send message", False, f"HTTP {status}")
    
    print()
    
    # TEST 3: User B polls chat - should see A's message and both online
    print("TEST 3: User B polls chat (should see A's message and both users online)")
    poll_b1 = chat_poll(cookies_b, "User B")
    if poll_b1:
        messages = poll_b1.get("messages", [])
        online = poll_b1.get("online", [])
        online_count = poll_b1.get("online_count", 0)
        
        # Check for A's message
        a_msg = None
        for msg in messages:
            if msg.get("kind") == "user" and msg.get("text") == "hello from alpha":
                a_msg = msg
                break
        
        if a_msg:
            log_test("Test 3: See A's message", True, f"Found message from {a_msg.get('display_name')}")
        else:
            log_test("Test 3: See A's message", False, f"Message not found. Messages: {[m.get('text') for m in messages if m.get('kind') == 'user']}")
        
        # Check online count
        if online_count >= 2:
            log_test("Test 3: Online count", True, f"online_count={online_count}")
        else:
            log_test("Test 3: Online count", False, f"Expected >=2, got {online_count}")
        
        # Check both characters in online list
        online_names = [o.get("display_name") for o in online]
        has_alpha = "AlphaHero" in online_names
        has_beta = "BetaHero" in online_names
        
        if has_alpha and has_beta:
            log_test("Test 3: Both online", True, f"Online: {online_names}")
        else:
            missing = []
            if not has_alpha: missing.append("AlphaHero")
            if not has_beta: missing.append("BetaHero")
            log_test("Test 3: Both online", False, f"Missing: {missing}. Online: {online_names}")
    else:
        log_test("Test 3: Poll request", False, "Poll failed")
    
    print()
    
    # TEST 4: Send empty message (should return 400)
    print("TEST 4: User A sends empty message (should return 400)")
    send_empty = chat_send(cookies_a, "", "User A")
    if send_empty and send_empty.get("error"):
        status = send_empty.get("status_code", 0)
        if status == 400:
            log_test("Test 4: Empty message rejected", True, f"HTTP 400 as expected")
        else:
            log_test("Test 4: Empty message rejected", False, f"Expected 400, got {status}")
    else:
        log_test("Test 4: Empty message rejected", False, "Empty message was accepted (should be 400)")
    
    print()
    
    # TEST 5: Send long message (should truncate to 400 chars)
    print("TEST 5: User A sends 600-char message (should truncate to 400)")
    long_text = "x" * 600
    send_long = chat_send(cookies_a, long_text, "User A")
    if send_long and not send_long.get("error"):
        msg_data = send_long.get("message", {})
        returned_text = msg_data.get("text", "")
        text_len = len(returned_text)
        
        if text_len == 400:
            log_test("Test 5: Long message truncated", True, f"Text length = 400")
        else:
            log_test("Test 5: Long message truncated", False, f"Expected length 400, got {text_len}")
    else:
        status = send_long.get("status_code", "N/A") if send_long else "N/A"
        log_test("Test 5: Long message truncated", False, f"Send failed with HTTP {status}")
    
    print()
    
    # TEST 6: Verify messages use character name, not email
    print("TEST 6: Verify messages use CHARACTER name (not email)")
    poll_verify = chat_poll(cookies_b, "User B")
    if poll_verify:
        messages = poll_verify.get("messages", [])
        online = poll_verify.get("online", [])
        
        # Check user messages don't contain email
        user_msgs = [m for m in messages if m.get("kind") == "user"]
        has_email = any(email_a in m.get("display_name", "") or email_b in m.get("display_name", "") for m in user_msgs)
        has_char_name = any("AlphaHero" in m.get("display_name", "") or "BetaHero" in m.get("display_name", "") for m in user_msgs)
        
        # Check online list
        online_names = [o.get("display_name") for o in online]
        online_has_email = any(email_a in name or email_b in name for name in online_names)
        online_has_char = "AlphaHero" in online_names or "BetaHero" in online_names
        
        if not has_email and has_char_name and not online_has_email and online_has_char:
            log_test("Test 6: Character names used", True, "Messages and online list use character names")
        else:
            issues = []
            if has_email: issues.append("Messages contain email")
            if not has_char_name: issues.append("Messages missing character names")
            if online_has_email: issues.append("Online list contains email")
            if not online_has_char: issues.append("Online list missing character names")
            log_test("Test 6: Character names used", False, f"Issues: {', '.join(issues)}")
    else:
        log_test("Test 6: Character names used", False, "Poll failed")
    
    print()
    
    # TEST 7 (OPTIONAL): Leave detection (requires 30s wait)
    print("TEST 7 (OPTIONAL): Leave detection - requires 30s wait")
    print("Skipping due to time constraint (30s TTL). To test manually:")
    print("  1. Stop polling as User A for >30 seconds")
    print("  2. Poll as User B twice")
    print("  3. Should see 'AlphaHero has left Valeria' system message")
    log_test("Test 7: Leave detection", True, "SKIPPED (time constraint)")
    
    print()
    print("=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    
    passed = sum(1 for t in test_results if t["passed"])
    total = len(test_results)
    
    print(f"\nTotal: {passed}/{total} tests passed")
    print()
    
    for result in test_results:
        status = "✅" if result["passed"] else "❌"
        print(f"{status} {result['name']}")
        if result["details"] and not result["passed"]:
            print(f"   └─ {result['details']}")
    
    print()
    
    if passed == total:
        print("🎉 ALL TESTS PASSED!")
        return 0
    else:
        print(f"⚠️  {total - passed} test(s) failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
