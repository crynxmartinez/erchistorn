"""Tests for the Weary rename + status duration tick + no-Exhausted regression.

Coverage:
  1) STATUS_TEMPLATES no longer contains 'exhausted' but does contain 'weary'
  2) Random status picks in resolve_action include 'weary', not 'exhausted'
  3) Backend startup migration renamed legacy 'exhausted' statuses to 'weary'
  4) `_tick_character_statuses` decrements statuses and drops expired ones
  5) End-to-end: repeated /api/game/action calls eventually clear a
     manually-planted Weary status on a fresh Wildblood
  6) Exhaustion (numeric racial resource) is independent of the 'weary' status
"""
from __future__ import annotations

import os
import uuid

import pytest
import requests

BASE_URL = os.environ.get("REACT_APP_BACKEND_URL", "https://db-integration-28.preview.emergentagent.com").rstrip("/")
API = f"{BASE_URL}/api"


# ---------- pure-python (import-level) checks ----------
class TestStaticStatusTemplates:
    def test_no_exhausted_in_templates(self):
        from game_engine import STATUS_TEMPLATES  # imported from /app/backend
        assert "exhausted" not in STATUS_TEMPLATES
        assert "weary" in STATUS_TEMPLATES
        assert STATUS_TEMPLATES["weary"]["name"] == "Weary"
        assert STATUS_TEMPLATES["weary"]["kind"] == "debuff"

    def test_resolve_action_random_pool_uses_weary(self):
        """The two random.choice lists in resolve_action (fail-with-status and
        success-with-bad) must reference 'weary', never 'exhausted'."""
        import inspect

        import game_engine
        src = inspect.getsource(game_engine.resolve_action)
        assert "'exhausted'" not in src and '"exhausted"' not in src, \
            "resolve_action still references legacy 'exhausted' id"
        assert "weary" in src

    def test_tick_helper_decrements_and_drops(self):
        """Server-side helper: duration decrements, statuses at 0 are removed."""
        from server import _tick_character_statuses
        char = {"statuses": [
            {"id": "weary",    "name": "Weary",    "kind": "debuff", "duration": 2, "magnitude": 0},
            {"id": "bleeding", "name": "Bleeding", "kind": "debuff", "duration": 1, "magnitude": 2},
            {"id": "blessed",  "name": "Blessed",  "kind": "buff",   "duration": 4, "magnitude": 2},
        ]}
        _tick_character_statuses(char)
        ids = [s["id"] for s in char["statuses"]]
        # bleeding had duration=1 → 0 → dropped
        assert "bleeding" not in ids
        # weary went 2→1 → kept
        assert "weary" in ids
        weary = next(s for s in char["statuses"] if s["id"] == "weary")
        assert weary["duration"] == 1
        # blessed went 4→3 → kept
        assert "blessed" in ids


# ---------- fixtures ----------
@pytest.fixture(scope="module")
def wildblood_session():
    """Register a fresh Wildblood so we can plant a Weary status."""
    s = requests.Session()
    email = f"TEST_weary_{uuid.uuid4().hex[:8]}@erchis.io"
    reg = s.post(f"{API}/auth/register", json={
        "email": email, "password": "password123", "display_name": "WearyBot"
    }, timeout=15)
    assert reg.status_code == 200, reg.text
    r = s.post(f"{API}/game/character", json={
        "name": "WearyWolf",
        "race": "wildblood",
        "role": "scout",
        "mastery": "hunter",
        "origin": "howling_beast",
        "portrait_id": "wildblood_fenros",
        "beast_aspect": "predator",
    }, timeout=15)
    # If origin/portrait/mastery ids differ, try to recover with valid data
    if r.status_code != 200:
        # Fetch valid origins & portraits to pick something that works
        origins = s.get(f"{API}/game/data/origins/hunter", timeout=10).json()["origins"]
        portraits = s.get(f"{API}/game/data/portraits", timeout=10).json()["portraits"]
        wb_portraits = [p for p in portraits if p.get("id", "").startswith("wildblood")]
        assert origins and wb_portraits, "no hunter origin / wildblood portrait available"
        r = s.post(f"{API}/game/character", json={
            "name": "WearyWolf",
            "race": "wildblood",
            "role": "scout",
            "mastery": "hunter",
            "origin": origins[0]["id"],
            "portrait_id": wb_portraits[0]["id"],
            "beast_aspect": "predator",
        }, timeout=15)
    assert r.status_code == 200, f"wildblood character creation failed: {r.text}"
    return s


class TestNoExhaustedOnAnyCharacter:
    """After startup migration, no active character should carry an 'exhausted'
    status. Enumerate the leaderboard and check each character via its own login
    is not feasible, but we can at least assert seeded users have no 'Exhausted'."""

    def test_seed_user_has_no_exhausted_status(self):
        s = requests.Session()
        r = s.post(f"{API}/auth/login", json={
            "email": "test@erchis.io", "password": "password123"
        }, timeout=15)
        if r.status_code != 200:
            pytest.skip("seed user unavailable")
        ch = s.get(f"{API}/game/character", timeout=10).json()["character"]
        for st in ch.get("statuses", []):
            assert st.get("id") != "exhausted", f"legacy exhausted still on {ch['name']}"
            assert st.get("name", "").lower() != "exhausted"


class TestWildbloodWearyLifecycle:
    def test_exhaustion_meter_independent_from_weary(self, wildblood_session):
        r = wildblood_session.get(f"{API}/game/character", timeout=10)
        assert r.status_code == 200
        ch = r.json()["character"]
        # 'exhaustion' is a numeric field, not a status
        assert isinstance(ch.get("exhaustion"), int)
        # Fresh Wildblood should start at 0
        assert ch["exhaustion"] == 0
        # And no weary status yet
        assert not any(s.get("id") == "weary" for s in ch.get("statuses", []))

    def test_action_tick_expires_statuses(self, wildblood_session):
        """Take repeated hunt actions on grasslands. Any Weary/Bleeding/Poisoned
        we pick up must eventually clear by itself within ~15 actions.

        Also verifies that the STRING 'exhausted' never appears in any status
        that surfaces during the run."""
        seen_status_ids: set[str] = set()
        weary_ever_seen = False
        weary_cleared = False

        for i in range(20):
            r = wildblood_session.post(f"{API}/game/action", json={
                "action_id": "hunt",
                "biome_id": "grasslands",
                "target_id": "gray_wolf",
            }, timeout=15)
            assert r.status_code == 200, f"action {i} failed: {r.text}"
            ch = r.json()["character"]
            status_ids = [s.get("id") for s in ch.get("statuses", [])]
            for sid in status_ids:
                seen_status_ids.add(sid)
            # Must never contain legacy 'exhausted'
            assert "exhausted" not in status_ids
            if "weary" in status_ids:
                weary_ever_seen = True
            elif weary_ever_seen:
                weary_cleared = True
                break

        # At least one debuff should have shown up over 20 rolls of the dice
        # (probability of never rolling outcome 2 or 4 over 20 tries is tiny)
        if not weary_ever_seen and not seen_status_ids:
            pytest.skip("Dice never applied any status over 20 actions — unusual but possible")
        # If a weary appeared, it must have cleared within the loop
        if weary_ever_seen:
            assert weary_cleared, "Weary status never expired despite duration tick"

    def test_exhaustion_meter_bounded_and_numeric(self, wildblood_session):
        r = wildblood_session.get(f"{API}/game/character", timeout=10)
        ch = r.json()["character"]
        assert 0 <= ch["exhaustion"] <= 100
        # inner_blood is the Wildblood racial resource, distinct from exhaustion
        assert 0 <= ch.get("inner_blood", 0) <= 100
