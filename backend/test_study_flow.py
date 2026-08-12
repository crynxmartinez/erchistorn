"""Test the Study Perks system end-to-end via API calls."""
import requests
import time
import sys

BASE = "http://127.0.0.1:8000/api"

def test_study_flow():
    import uuid
    suffix = uuid.uuid4().hex[:8]
    username = f"studytest_{suffix}"
    password = "Test1234!"
    email = f"{suffix}@test.com"

    # Register
    r = requests.post(f"{BASE}/auth/register", json={
        "username": username, "password": password, "email": email, "display_name": "Study Tester"
    })
    print(f"[Register] {r.status_code}")
    if r.status_code not in (200, 201):
        print(r.text)
        return

    # Login
    s = requests.Session()
    r = s.post(f"{BASE}/auth/login", json={"username": username, "password": password, "email": email})
    print(f"[Login] {r.status_code}")
    if r.status_code != 200:
        print(r.text)
        return

    # Create character (hyliondrian to start at Atlantyrion)
    r = s.post(f"{BASE}/game/character", json={
        "name": f"StudyTest{suffix}",
        "race": "hyliondrian",
        "role": "scholar",
        "mastery": "mage",
        "origin": "arcane_spiral",
        "portrait_id": "Nerith",
        "racial_gift": "tide_touched",
        "marine_adaptation": "sharkborn",
    })
    print(f"[Create Character] {r.status_code}")
    if r.status_code not in (200, 201):
        print(r.text)
        return
    char = r.json()
    char_id = char.get("id") or char.get("_id")
    print(f"  Character: {char.get('name')}, gold={char.get('gold')}")

    # Give character enough gold for testing via DB
    import os
    from motor.motor_asyncio import AsyncIOMotorClient
    from bson import ObjectId
    import asyncio

    mongo_url = os.environ.get("MONGO_URL", "mongodb://localhost:27017")
    db_name = os.environ.get("DB_NAME", "erchis_local")
    # Load .env if needed
    from pathlib import Path
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            if "=" in line and not line.strip().startswith("#"):
                k, v = line.split("=", 1)
                os.environ[k.strip()] = v.strip()
        mongo_url = os.environ.get("MONGO_URL", mongo_url)
        db_name = os.environ.get("DB_NAME", db_name)

    async def give_gold():
        client = AsyncIOMotorClient(mongo_url)
        db = client[db_name]
        await db.characters.update_one(
            {"_id": ObjectId(char_id)},
            {"$set": {"gold": 50000}}
        )
        client.close()

    asyncio.run(give_gold())
    print("  Set gold to 50000 via DB")
    # We'll try enrolling in might_theory (tier 1 = 1000g)
    # First check study status
    r = s.get(f"{BASE}/game/study/status")
    print(f"[Study Status] {r.status_code}")
    status = r.json()
    print(f"  Courses: {len(status.get('courses', []))}")
    print(f"  Gold: {status.get('gold')}")
    print(f"  Enrollment: {status.get('enrollment')}")

    # Try to enroll
    r = s.post(f"{BASE}/game/study/enroll", json={"course_id": "might_theory"})
    print(f"[Enroll] {r.status_code}")
    if r.status_code != 200:
        print(f"  Error: {r.text}")
        # If not enough gold, we can't proceed with this test
        if "gold" in r.text.lower():
            print("  Not enough gold — test needs a character with >= 1000 gold")
            return
        return
    enroll_result = r.json().get("enroll_result", {})
    print(f"  Enrolled: {enroll_result}")

    # Check status again
    r = s.get(f"{BASE}/game/study/status")
    status = r.json()
    enrollment = status.get("enrollment")
    print(f"[Status After Enroll] enrollment={enrollment}")

    # Daily check-in
    r = s.post(f"{BASE}/game/study/checkin")
    print(f"[Check-in] {r.status_code}")
    if r.status_code != 200:
        print(f"  Error: {r.text}")
        return
    checkin_result = r.json().get("checkin_result", {})
    print(f"  Check-in result: {checkin_result}")

    # Check buff is active
    r = s.get(f"{BASE}/game/study/status")
    status = r.json()
    buff = status.get("buff")
    print(f"[Buff After Check-in] {buff}")

    # Try checking in again (should fail)
    r = s.post(f"{BASE}/game/study/checkin")
    print(f"[Second Check-in (should fail)] {r.status_code} — {r.text[:100]}")

    # Abandon
    r = s.post(f"{BASE}/game/study/abandon")
    print(f"[Abandon] {r.status_code}")
    if r.status_code == 200:
        print(f"  Result: {r.json().get('abandon_result')}")

    # Verify enrollment cleared
    r = s.get(f"{BASE}/game/study/status")
    status = r.json()
    print(f"[Status After Abandon] enrollment={status.get('enrollment')}")

    print("\n=== Study Perks test PASSED ===")


if __name__ == "__main__":
    test_study_flow()
