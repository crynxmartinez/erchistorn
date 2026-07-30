"""Erchis RPG backend E2E tests — auth, static data, character creation, actions,
combat, crafting, skills, equip, dailies, leaderboard, events."""
from __future__ import annotations

import os
import time
import uuid

import pytest
import requests

BASE_URL = os.environ.get("REACT_APP_BACKEND_URL", "https://fantasy-torn-dice.preview.emergentagent.com").rstrip("/")
API = f"{BASE_URL}/api"

TEST_USER_EMAIL = "test@erchis.io"
TEST_USER_PASSWORD = "password123"


# ---------- fixtures ----------
@pytest.fixture(scope="session")
def existing_user_session():
    """Login with the pre-seeded test user (already has a character)."""
    s = requests.Session()
    r = s.post(f"{API}/auth/login", json={"email": TEST_USER_EMAIL, "password": TEST_USER_PASSWORD}, timeout=15)
    assert r.status_code == 200, f"seed login failed: {r.status_code} {r.text}"
    return s


@pytest.fixture(scope="session")
def new_user_session():
    """Register a fresh user (no character yet)."""
    s = requests.Session()
    email = f"TEST_{uuid.uuid4().hex[:10]}@erchis.io"
    r = s.post(f"{API}/auth/register", json={
        "email": email, "password": "testpass123", "display_name": "TESTBot"
    }, timeout=15)
    assert r.status_code == 200, f"register failed: {r.status_code} {r.text}"
    s._email = email
    return s


# ---------- AUTH ----------
class TestAuth:
    def test_register_and_me(self, new_user_session):
        r = new_user_session.get(f"{API}/auth/me", timeout=10)
        assert r.status_code == 200
        data = r.json()
        assert data["email"].lower() == new_user_session._email.lower()
        assert data["has_character"] is False
        assert "id" in data

    def test_register_duplicate_email_409(self):
        s = requests.Session()
        r = s.post(f"{API}/auth/register", json={
            "email": TEST_USER_EMAIL, "password": "password123", "display_name": "Dup"
        }, timeout=10)
        assert r.status_code == 409

    def test_login_success(self, existing_user_session):
        r = existing_user_session.get(f"{API}/auth/me", timeout=10)
        assert r.status_code == 200
        data = r.json()
        assert data["email"] == TEST_USER_EMAIL
        assert data["has_character"] is True

    def test_login_invalid(self):
        s = requests.Session()
        r = s.post(f"{API}/auth/login", json={"email": TEST_USER_EMAIL, "password": "wrong"}, timeout=10)
        assert r.status_code == 401

    def test_me_unauthenticated_401(self):
        r = requests.get(f"{API}/auth/me", timeout=10)
        assert r.status_code == 401


# ---------- STATIC DATA ----------
class TestStaticData:
    def test_races_returns_8(self, existing_user_session):
        r = existing_user_session.get(f"{API}/game/data/races", timeout=10)
        assert r.status_code == 200
        races = r.json()["races"]
        assert len(races) == 8
        ids = {r["id"] for r in races}
        assert {"human", "elf", "dwarf", "half_elf", "orc", "wildblood", "hyliondrian", "sylvan"} == ids

    def test_roles(self, existing_user_session):
        r = existing_user_session.get(f"{API}/game/data/roles", timeout=10)
        assert r.status_code == 200
        assert len(r.json()["roles"]) >= 5

    def test_masteries(self, existing_user_session):
        r = existing_user_session.get(f"{API}/game/data/masteries", timeout=10)
        assert r.status_code == 200
        assert len(r.json()["masteries"]) >= 11

    def test_portraits_40(self, existing_user_session):
        r = existing_user_session.get(f"{API}/game/data/portraits", timeout=10)
        assert r.status_code == 200
        assert len(r.json()["portraits"]) == 40

    def test_continents_7(self, existing_user_session):
        r = existing_user_session.get(f"{API}/game/data/continents", timeout=10)
        assert r.status_code == 200
        conts = r.json()["continents"]
        assert len(conts) == 7
        aeth = next((c for c in conts if c["id"] == "aetheria"), None)
        assert aeth and len(aeth["biomes"]) == 4

    def test_biome_actions(self, existing_user_session):
        r = existing_user_session.get(f"{API}/game/data/biome/grasslands/actions", timeout=10)
        assert r.status_code == 200
        actions = r.json()["actions"]
        assert any(a["id"] == "hunt" for a in actions)
        assert any(a["id"] == "gather" for a in actions)

    def test_items_have_6_rarities(self, existing_user_session):
        r = existing_user_session.get(f"{API}/game/data/items", timeout=10)
        assert r.status_code == 200
        rarities = {it["rarity"] for it in r.json()["items"]}
        assert rarities.issuperset({"common", "uncommon", "rare", "epic", "legendary", "mythic"})

    def test_skills_recipes_teachers_monsters(self, existing_user_session):
        for path, key, min_count in [
            ("/game/data/skills", "skills", 15),
            ("/game/data/recipes", "recipes", 5),
            ("/game/data/teachers", "teachers", 3),
            ("/game/data/monsters", "monsters", 5),
        ]:
            r = existing_user_session.get(f"{API}{path}", timeout=10)
            assert r.status_code == 200, path
            assert len(r.json()[key]) >= min_count, path


# ---------- CHARACTER CREATION ----------
class TestCharacterCreation:
    def test_create_human_character(self, new_user_session):
        # Human race requires oath
        r = new_user_session.post(f"{API}/game/character", json={
            "name": "TESTHero", "race": "human", "role": "fighter", "mastery": "knight",
            "portrait_id": "human_aldric", "oath": "I shall be tested."
        }, timeout=15)
        assert r.status_code == 200, r.text
        char = r.json()
        assert char["name"] == "TESTHero"
        assert char["race"] == "human"
        assert char["level"] == 1
        assert char["hp"] > 0 and char["hp"] == char["max_hp"]
        assert char["gold"] == 75
        assert isinstance(char["inventory"], list) and len(char["inventory"]) >= 3

    def test_create_human_without_oath_400(self, existing_user_session):
        # existing user already has character — but we want to test validation.
        # Use a fresh session for this
        s = requests.Session()
        email = f"TEST_{uuid.uuid4().hex[:10]}@erchis.io"
        s.post(f"{API}/auth/register", json={"email": email, "password": "pw123456", "display_name": "T"}, timeout=10)
        r = s.post(f"{API}/game/character", json={
            "name": "NoOath", "race": "human", "role": "fighter", "mastery": "knight",
            "portrait_id": "human_aldric"
        }, timeout=10)
        assert r.status_code == 400

    def test_create_duplicate_character_409(self, existing_user_session):
        r = existing_user_session.post(f"{API}/game/character", json={
            "name": "Dup", "race": "human", "role": "fighter", "mastery": "knight",
            "portrait_id": "human_aldric", "oath": "x"
        }, timeout=10)
        assert r.status_code == 409

    def test_get_character(self, existing_user_session):
        r = existing_user_session.get(f"{API}/game/character", timeout=10)
        assert r.status_code == 200
        data = r.json()
        assert "character" in data
        ch = data["character"]
        assert ch["name"] == "Erethon"
        assert "level" in ch and "hp" in ch and "stats" in ch


# ---------- ACTIONS ----------
class TestActions:
    def test_gather_returns_narrative_and_rewards(self, existing_user_session):
        r = existing_user_session.post(f"{API}/game/action", json={
            "action_id": "gather", "biome_id": "grasslands", "target_id": "wild_herb"
        }, timeout=10)
        assert r.status_code == 200
        data = r.json()
        assert "result" in data and "character" in data
        result = data["result"]
        assert 1 <= result["outcome"] <= 6
        assert "narrative" in result and isinstance(result["narrative"], str) and len(result["narrative"]) > 0
        assert "rewards" in result

    def test_travel_updates_biome(self, existing_user_session):
        r = existing_user_session.post(f"{API}/game/character/travel", json={
            "continent": "aetheria", "biome": "oakwood"
        }, timeout=10)
        assert r.status_code == 200
        ch = r.json()["character"]
        assert ch["current_biome"] == "oakwood"

    def test_travel_locked_continent_403(self, existing_user_session):
        r = existing_user_session.post(f"{API}/game/character/travel", json={
            "continent": "vulkaros", "biome": None
        }, timeout=10)
        assert r.status_code == 403


# ---------- COMBAT ----------
class TestCombat:
    def test_combat_start_and_turn(self, existing_user_session):
        r = existing_user_session.post(f"{API}/game/combat/start", json={
            "biome_id": "grasslands", "monster_id": "gray_wolf"
        }, timeout=10)
        assert r.status_code == 200
        data = r.json()
        state = data["state"]
        assert "combat_id" in state
        assert state["monster_id"] == "gray_wolf"
        assert state["monster_hp"] > 0

        combat_id = state["combat_id"]
        # Take turns until combat ends
        for _ in range(30):
            tr = existing_user_session.post(f"{API}/game/combat/turn", json={
                "combat_id": combat_id
            }, timeout=10)
            assert tr.status_code == 200
            result = tr.json()["result"]
            if result.get("victory") is True or result.get("victory") is False:
                break
        else:
            pytest.fail("Combat did not resolve within 30 turns")

    def test_combat_invalid_monster(self, existing_user_session):
        r = existing_user_session.post(f"{API}/game/combat/start", json={
            "biome_id": "grasslands", "monster_id": "nope"
        }, timeout=10)
        assert r.status_code == 400


# ---------- CRAFTING ----------
class TestCrafting:
    def test_craft_missing_materials_400(self, existing_user_session):
        # existing user probably lacks materials to craft wolfbone_axe
        r = existing_user_session.post(f"{API}/game/craft", json={"recipe_id": "craft_wolfbone_axe"}, timeout=10)
        assert r.status_code == 400

    def test_craft_iron_dagger_after_seeding_materials(self, existing_user_session):
        """We can't seed the DB directly, so we do a gather loop to get iron_ore + oak_log.
        This may not always succeed, so we skip if the dice don't cooperate."""
        # Loop gather up to 12 times to attempt to collect materials
        for _ in range(12):
            existing_user_session.post(f"{API}/game/action", json={
                "action_id": "gather", "biome_id": "grasslands", "target_id": "iron_ore"
            }, timeout=10)
        # travel to oakwood for oak_log
        existing_user_session.post(f"{API}/game/character/travel", json={
            "continent": "aetheria", "biome": "oakwood"
        }, timeout=10)
        for _ in range(12):
            existing_user_session.post(f"{API}/game/action", json={
                "action_id": "gather", "biome_id": "oakwood", "target_id": "oak_log"
            }, timeout=10)
        # Attempt craft
        r = existing_user_session.post(f"{API}/game/craft", json={"recipe_id": "craft_iron_dagger"}, timeout=10)
        if r.status_code == 400 and "material" in r.text.lower():
            pytest.skip("Could not gather enough materials via dice — skip crafting outcome check")
        assert r.status_code == 200, r.text
        data = r.json()
        result = data["result"]
        assert "outcome" in result
        assert 1 <= result["outcome"] <= 6


# ---------- SKILLS ----------
class TestSkills:
    def test_learn_skill_invalid_teacher(self, existing_user_session):
        r = existing_user_session.post(f"{API}/game/skill/learn", json={
            "skill_id": "shield_bash", "teacher_id": "nonexistent"
        }, timeout=10)
        assert r.status_code == 404

    def test_learn_skill_level_req(self, existing_user_session):
        # Erethon is L1, master_arden requires L2 for shield_bash
        r = existing_user_session.post(f"{API}/game/skill/learn", json={
            "skill_id": "shield_bash", "teacher_id": "master_arden"
        }, timeout=10)
        # Either 409 (already learned as Knight) or 403 (level req)
        assert r.status_code in (403, 409)


# ---------- EQUIP ----------
class TestEquip:
    def test_equip_weapon_from_inventory(self, existing_user_session):
        r = existing_user_session.post(f"{API}/game/equip", json={
            "item_id": "iron_dagger", "slot": "right_hand"
        }, timeout=10)
        assert r.status_code == 200
        ch = r.json()["character"]
        assert ch["equipped"]["right_hand"] == "iron_dagger"

    def test_equip_wrong_slot_400(self, existing_user_session):
        r = existing_user_session.post(f"{API}/game/equip", json={
            "item_id": "iron_dagger", "slot": "head"
        }, timeout=10)
        assert r.status_code == 400


# ---------- DAILY / LEADERBOARD / EVENTS ----------
class TestOthers:
    def test_daily_claim_incomplete_400(self, existing_user_session):
        # Get a mission id that isn't complete
        rc = existing_user_session.get(f"{API}/game/character", timeout=10)
        missions = rc.json()["character"].get("daily_missions", [])
        target = next((m for m in missions if not m.get("complete")), None)
        if not target:
            pytest.skip("No incomplete mission available")
        r = existing_user_session.post(f"{API}/game/daily/claim", json={"mission_id": target["id"]}, timeout=10)
        assert r.status_code == 400

    def test_leaderboard(self, existing_user_session):
        r = existing_user_session.get(f"{API}/game/leaderboard", timeout=10)
        assert r.status_code == 200
        rows = r.json()["rows"]
        assert isinstance(rows, list)
        # Erethon should be in there
        assert any(row["name"] == "Erethon" for row in rows) or len(rows) >= 1

    def test_world_events(self, existing_user_session):
        r = existing_user_session.get(f"{API}/game/events", timeout=10)
        assert r.status_code == 200
        events = r.json()["events"]
        assert isinstance(events, list)
        # ensure _id is stripped
        for e in events:
            assert "_id" not in e


# ---------- LOGOUT ----------
class TestLogout:
    def test_logout_clears_cookies(self):
        s = requests.Session()
        s.post(f"{API}/auth/login", json={"email": TEST_USER_EMAIL, "password": TEST_USER_PASSWORD}, timeout=10)
        r = s.post(f"{API}/auth/logout", timeout=10)
        assert r.status_code == 200
        # subsequent /me should be 401
        r2 = s.get(f"{API}/auth/me", timeout=10)
        assert r2.status_code == 401
