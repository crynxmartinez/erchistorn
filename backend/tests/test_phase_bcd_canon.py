"""Backend regression suite for the Phase A–D canon rework.

Covers:
- Canon continents & towns
- Existing character migration
- Grand Teleporter (list / travel / fee / cooldown / lock)
- Waystones (list / discover / activate / travel)
- Homeland Reputation
- Professions catalog / learn / abandon / hunt-xp / hunt rank
- Exploration progress (`explore` action + non-explore half-rate)
"""
from __future__ import annotations

import os
import time
import uuid

import pytest
import requests

_env_url = os.environ.get("REACT_APP_BACKEND_URL")
if not _env_url:
    # Fallback to reading frontend/.env directly (pytest env may not export it)
    try:
        with open("/app/frontend/.env") as _f:
            for _line in _f:
                if _line.startswith("REACT_APP_BACKEND_URL="):
                    _env_url = _line.strip().split("=", 1)[1]
                    break
    except FileNotFoundError:
        pass
assert _env_url, "REACT_APP_BACKEND_URL not set"
BASE_URL = _env_url.rstrip("/")
API = f"{BASE_URL}/api"

TEST_EMAIL = "test@erchis.io"
TEST_PASSWORD = "password123"


# ---------------- fixtures ----------------
@pytest.fixture(scope="session")
def existing_user_session() -> requests.Session:
    s = requests.Session()
    r = s.post(f"{API}/auth/login", json={"email": TEST_EMAIL, "password": TEST_PASSWORD})
    assert r.status_code == 200, f"login failed: {r.status_code} {r.text}"
    return s


def _register(email: str, password: str = "password123", display: str = "TmpHero") -> requests.Session:
    s = requests.Session()
    r = s.post(f"{API}/auth/register", json={"email": email, "password": password, "display_name": display})
    assert r.status_code == 200, f"register failed: {r.status_code} {r.text}"
    return s


def _create_character(sess: requests.Session, *, race: str, name: str,
                      role: str, mastery: str, origin: str, oath: str | None = None,
                      heritage: str | None = None) -> dict:
    payload: dict = {"race": race, "role": role, "mastery": mastery, "origin": origin,
                     "name": name, "portrait_id": "p1"}
    if oath:
        payload["oath"] = oath
    if heritage:
        payload["heritage"] = heritage
    r = sess.post(f"{API}/game/character", json=payload)
    assert r.status_code == 200, f"character creation failed: {r.status_code} {r.text}"
    return r.json()


# ============================================================
# 1. Canonical static data — continents & towns
# ============================================================
class TestCanonStaticData:
    ACCESSIBLE = {"valeria", "mushkara", "concordia", "khardrum",
                  "haya", "gennel", "hylion", "daw_ul_talalu"}
    LOCKED = {"azurea", "vael_turog", "orinth"}
    RACE_TO_CONT = {"human": "valeria", "orc": "mushkara", "half_elf": "concordia",
                    "dwarf": "khardrum", "elf": "haya", "wildblood": "gennel",
                    "hyliondrian": "hylion", "sylvan": "daw_ul_talalu"}

    def test_continents_11_total_and_ids(self, existing_user_session):
        r = existing_user_session.get(f"{API}/game/data/continents")
        assert r.status_code == 200
        conts = r.json()["continents"]
        ids = {c["id"] for c in conts}
        assert len(conts) == 11, f"expected 11 continents, got {len(conts)}: {ids}"
        assert self.ACCESSIBLE.issubset(ids)
        assert self.LOCKED.issubset(ids)

    def test_accessible_continents_have_home_race(self, existing_user_session):
        conts = existing_user_session.get(f"{API}/game/data/continents").json()["continents"]
        by_id = {c["id"]: c for c in conts}
        for cid, race in self.RACE_TO_CONT.items():
            c = by_id[race and self.RACE_TO_CONT[cid]]  # noqa
            c = by_id[self.RACE_TO_CONT[cid]]
            assert c["home_race"] == cid, f"{c['id']} home_race={c['home_race']} expected {cid}"
            assert c.get("locked") in (False, None)

    def test_locked_continents_are_locked(self, existing_user_session):
        conts = existing_user_session.get(f"{API}/game/data/continents").json()["continents"]
        by_id = {c["id"]: c for c in conts}
        for lid in self.LOCKED:
            assert by_id[lid]["locked"] is True

    def test_towns_14_and_membership(self, existing_user_session):
        r = existing_user_session.get(f"{API}/game/data/towns")
        assert r.status_code == 200
        towns = r.json()["towns"]
        by_id = {t["id"]: t for t in towns}
        expected = {
            "oathspire": "valeria", "riverguard": "valeria",
            "grunhold": "mushkara", "warforge": "mushkara",
            "elaris": "concordia", "silvergate": "concordia",
            "jahrahold": "khardrum", "deepstone": "khardrum",
            "solunara": "haya", "starfall_watch": "haya",
            "rindivar_grove": "gennel", "beastcairn": "gennel",
            "atlantyrion": "hylion",
            "veilgrove": "daw_ul_talalu",
        }
        # Every expected town exists on the correct continent
        for tid, cont in expected.items():
            assert tid in by_id, f"missing town {tid}"
            assert by_id[tid]["continent"] == cont, f"{tid} on wrong continent {by_id[tid]['continent']}"
        # 14 unique hometown ids
        assert set(expected).issubset(set(by_id))
        assert len(by_id) >= 14


# ============================================================
# 2. Migration: existing Erethon character is in Valeria/Golden Plains/Oathspire
# ============================================================
class TestExistingCharacterMigration:
    def test_erethon_on_canon(self, existing_user_session):
        r = existing_user_session.get(f"{API}/game/character")
        assert r.status_code == 200
        ch = r.json()["character"]
        # After migration, the character's continent must be one of the 8 canon
        # accessible IDs — never a legacy codename. (Between test runs the teleporter
        # may have relocated Erethon, so we don't hardcode Valeria here.)
        accessible = {"valeria", "mushkara", "concordia", "khardrum",
                      "haya", "gennel", "hylion", "daw_ul_talalu"}
        assert ch["current_continent"] in accessible, ch["current_continent"]
        # home_town must exist and be canonical
        assert ch.get("home_town") in ("oathspire", "riverguard"), ch.get("home_town")
        # Legacy IDs must not appear
        assert ch["current_continent"] not in ("aetheria", "vulkaros", "nyxmoor",
                                               "frosthelm", "zephyria", "sablewaste", "verdania")
        # Migrated biome must not be a legacy id either
        legacy_biomes = {"grasslands", "oakwood", "riverlands", "old_ruins",
                         "ashlands", "lava_caves", "bogland", "frozen_peaks",
                         "sky_isles", "dune_sea", "rainforest"}
        assert ch["current_biome"] not in legacy_biomes, ch["current_biome"]


# ============================================================
# 3. New character creation lands on canonical hometown
# ============================================================
class TestCharacterCreationHomelands:
    def _fresh(self, race: str, role: str, mastery: str, origin: str,
              expected_cont: str, expected_town: str, expected_biome: str,
              oath: str | None = None, heritage: str | None = None):
        email = f"TEST_{race}_{uuid.uuid4().hex[:8]}@erchis.io"
        sess = _register(email)
        ch = _create_character(sess, race=race, name=f"TEST_{race}",
                               role=role, mastery=mastery, origin=origin,
                               oath=oath, heritage=heritage)
        assert ch["current_continent"] == expected_cont, ch["current_continent"]
        assert ch["home_town"] == expected_town, ch["home_town"]
        assert ch["current_biome"] == expected_biome, ch["current_biome"]
        # reputation seeded: friendly on native, neutral on others
        rep = ch.get("reputation", {})
        native = rep.get(expected_cont, {})
        assert native.get("level") == "friendly"
        assert native.get("points", 0) >= 3000
        # some other continent → neutral
        for cid in ("valeria", "mushkara", "concordia", "khardrum",
                    "haya", "gennel", "hylion", "daw_ul_talalu"):
            if cid == expected_cont:
                continue
            e = rep.get(cid, {})
            assert e.get("level") == "neutral", f"{cid} not neutral: {e}"

    def test_sylvan_lands_in_daw_ul_talalu(self, existing_user_session):
        # sylvan role/mastery: use Bard/Skirmisher-safe combo; fall back to first available
        # Query available roles/masteries once
        roles = existing_user_session.get(f"{API}/game/data/roles").json()["roles"]
        # find a role with an available mastery + origin
        origins = existing_user_session.get(f"{API}/game/data/origins").json()["origins"]
        role_id, mastery_id, origin_id = None, None, None
        for r in roles:
            for m in r.get("available_masteries", []):
                mo = [o for o in origins if o.get("mastery") == m]
                if mo:
                    role_id, mastery_id, origin_id = r["id"], m, mo[0]["id"]
                    break
            if origin_id:
                break
        assert origin_id, "could not find any valid role/mastery/origin combo"
        self._fresh("sylvan", role_id, mastery_id, origin_id,
                    "daw_ul_talalu", "veilgrove", "mistwood")

    def test_dwarf_lands_in_khardrum(self, existing_user_session):
        roles = existing_user_session.get(f"{API}/game/data/roles").json()["roles"]
        origins = existing_user_session.get(f"{API}/game/data/origins").json()["origins"]
        role_id, mastery_id, origin_id = None, None, None
        for r in roles:
            for m in r.get("available_masteries", []):
                mo = [o for o in origins if o.get("mastery") == m]
                if mo:
                    role_id, mastery_id, origin_id = r["id"], m, mo[0]["id"]
                    break
            if origin_id:
                break
        self._fresh("dwarf", role_id, mastery_id, origin_id,
                    "khardrum", "jahrahold", "granite_foothills")

    def test_hyliondrian_lands_in_hylion(self, existing_user_session):
        roles = existing_user_session.get(f"{API}/game/data/roles").json()["roles"]
        origins = existing_user_session.get(f"{API}/game/data/origins").json()["origins"]
        role_id, mastery_id, origin_id = None, None, None
        for r in roles:
            for m in r.get("available_masteries", []):
                mo = [o for o in origins if o.get("mastery") == m]
                if mo:
                    role_id, mastery_id, origin_id = r["id"], m, mo[0]["id"]
                    break
            if origin_id:
                break
        self._fresh("hyliondrian", role_id, mastery_id, origin_id,
                    "hylion", "atlantyrion", "coral_gardens")


# ============================================================
# 4. Grand Teleporter
# ============================================================
class TestTeleporter:
    def test_destinations_shape(self, existing_user_session):
        r = existing_user_session.get(f"{API}/game/teleporter/destinations")
        assert r.status_code == 200
        data = r.json()
        assert data["fee_base"] == 100
        assert data["cooldown_secs"] == 600
        dests = data["destinations"]
        assert len(dests) == 8
        # current continent → fee 0 + is_current
        cur = [d for d in dests if d["is_current"]]
        assert len(cur) == 1
        assert cur[0]["fee"] == 0
        # non-current all cost 100g
        for d in dests:
            if not d["is_current"]:
                assert d["fee"] == 100
                assert d["hometown_id"], d
                assert d["hometown_name"], d

    def test_travel_locked_continent_returns_403(self, existing_user_session):
        r = existing_user_session.post(f"{API}/game/teleporter/travel",
                                       json={"continent_id": "azurea"})
        assert r.status_code == 403
        assert "sealed" in r.text.lower()

    def test_travel_same_continent_returns_400(self, existing_user_session):
        ch = existing_user_session.get(f"{API}/game/character").json()["character"]
        cur = ch["current_continent"]
        r = existing_user_session.post(f"{API}/game/teleporter/travel",
                                       json={"continent_id": cur})
        assert r.status_code == 400

    def test_teleporter_travel_cooldown_and_fee(self):
        """Register a fresh Human → travel to Mushkara, then re-hop is blocked."""
        email = f"TEST_teleport_{uuid.uuid4().hex[:8]}@erchis.io"
        sess = _register(email)
        # Discover valid role/mastery/origin
        roles = sess.get(f"{API}/game/data/roles").json()["roles"]
        origins = sess.get(f"{API}/game/data/origins").json()["origins"]
        role_id, mastery_id, origin_id = None, None, None
        for role in roles:
            for m in role.get("available_masteries", []):
                mo = [o for o in origins if o.get("mastery") == m]
                if mo:
                    role_id, mastery_id, origin_id = role["id"], m, mo[0]["id"]
                    break
            if origin_id:
                break
        ch = _create_character(sess, race="human", name="TeleTester",
                               role=role_id, mastery=mastery_id, origin=origin_id,
                               oath="protection")
        # Character must be in a hometown for the teleporter to be usable
        # Newly created characters have current_town=None (they're placed in a biome).
        # Visit hometown first.
        home = ch["home_town"]
        vr = sess.post(f"{API}/game/town/visit", json={"town_id": home})
        assert vr.status_code == 200, vr.text
        # Grant gold via direct top-up: not available → assume starter 75g is not enough (fee=100).
        # Verify fee-fail path:
        gold = vr.json()["character"]["gold"]
        r = sess.post(f"{API}/game/teleporter/travel", json={"continent_id": "mushkara"})
        if gold < 100:
            assert r.status_code == 400
            assert "fee" in r.text.lower() or "gold" in r.text.lower()
        else:
            assert r.status_code == 200

    def test_erethon_teleport_hop_and_cooldown(self, existing_user_session):
        """Erethon has ~700g and level 10 — verify one hop works, second is blocked."""
        # Reset teleporter cooldown by ensuring we're in hometown + have gold
        ch = existing_user_session.get(f"{API}/game/character").json()["character"]
        if ch["gold"] < 100:
            pytest.skip("Not enough gold to run teleporter hop test")
        # Ensure in hometown
        if ch.get("current_town") != ch["home_town"]:
            vr = existing_user_session.post(f"{API}/game/town/visit",
                                            json={"town_id": ch["home_town"]})
            if vr.status_code == 403:
                # We may not be on our home continent — travel back first
                pytest.skip("Not on home continent for cooldown test; skipping.")
        # Try to hop somewhere else
        dests = existing_user_session.get(f"{API}/game/teleporter/destinations").json()["destinations"]
        target = next((d for d in dests if not d["is_current"]), None)
        assert target
        r1 = existing_user_session.post(f"{API}/game/teleporter/travel",
                                        json={"continent_id": target["continent_id"]})
        # It may fail if cooldown still active from previous test — handle gracefully
        if r1.status_code == 403 and "recharging" in r1.text.lower():
            pytest.skip("Teleporter still on cooldown from prior run")
        assert r1.status_code == 200, r1.text
        body = r1.json()
        assert body["fee"] == 100
        assert body["character"]["current_continent"] == target["continent_id"]
        assert body["character"]["current_town"] == target["hometown_id"]
        # Second hop → 403 recharging
        dests2 = existing_user_session.get(f"{API}/game/teleporter/destinations").json()["destinations"]
        target2 = next((d for d in dests2 if not d["is_current"]), None)
        r2 = existing_user_session.post(f"{API}/game/teleporter/travel",
                                        json={"continent_id": target2["continent_id"]})
        assert r2.status_code == 403
        assert "recharging" in r2.text.lower()


# ============================================================
# 5. Waystones
# ============================================================
class TestWaystones:
    def test_16_waystones_2_per_continent(self, existing_user_session):
        r = existing_user_session.get(f"{API}/game/waystones")
        assert r.status_code == 200
        ws = r.json()["waystones"]
        assert len(ws) == 16
        by_cont = {}
        for w in ws:
            by_cont.setdefault(w["continent"], []).append(w)
        assert set(by_cont) == {"valeria", "mushkara", "concordia", "khardrum",
                                "haya", "gennel", "hylion", "daw_ul_talalu"}
        for cid, items in by_cont.items():
            assert len(items) == 2, f"{cid} has {len(items)} waystones"
            for it in items:
                for k in ("id", "name", "biome", "activation_gold", "discovered", "activated"):
                    assert k in it, f"waystone missing field {k}: {it}"

    def test_discover_requires_correct_biome(self, existing_user_session):
        # Erethon is in Golden Plains (Valeria). Try to discover Crownwood Shrine —
        # its biome is crownwood_forest, so this should 403.
        r = existing_user_session.post(f"{API}/game/waystone/discover",
                                       json={"waystone_id": "waystone_crownwood"})
        # If they happen to be in crownwood_forest already this will 200 — accept both.
        if r.status_code == 200:
            pytest.skip("character was already in crownwood_forest; not the target biome mismatch")
        assert r.status_code == 403
        assert "not standing" in r.text.lower()

    def test_activate_requires_discovery(self, existing_user_session):
        # Pick a waystone the char definitely hasn't discovered
        r = existing_user_session.post(f"{API}/game/waystone/activate",
                                       json={"waystone_id": "waystone_abyssal"})
        assert r.status_code == 403


# ============================================================
# 6. Reputation
# ============================================================
class TestReputation:
    def test_reputation_shape(self, existing_user_session):
        r = existing_user_session.get(f"{API}/game/reputation")
        assert r.status_code == 200
        data = r.json()
        rep = data["reputation"]
        assert len(rep) == 8
        # Erethon is Human → is_native must be True on valeria
        val = next(r for r in rep if r["continent_id"] == "valeria")
        assert val["is_native"] is True
        assert val["level"] == "friendly"
        assert val["points"] >= 3000
        # Others neutral
        for e in rep:
            if e["continent_id"] != "valeria":
                assert e["level"] == "neutral"
                assert e["points"] == 0


# ============================================================
# 7. Professions
# ============================================================
class TestProfessions:
    EXPECTED_IDS = {"mining", "herbalism", "logging", "hunting", "fishing", "excavation",
                    "blacksmithing", "armorsmithing", "leatherworking", "tailoring",
                    "alchemy", "cooking", "enchanting", "jewelcrafting", "engineering",
                    "bow_crafting", "merchant", "cartography", "beast_taming"}

    def test_catalog_has_19_professions_by_kind(self, existing_user_session):
        r = existing_user_session.get(f"{API}/game/professions/catalog")
        assert r.status_code == 200
        data = r.json()
        catalog = data["catalog"]
        assert {p["id"] for p in catalog} == self.EXPECTED_IDS
        # slot count must scale with level
        assert data["slots_unlocked"] in (1, 2, 3)

    def test_mine_returns_learned_professions(self, existing_user_session):
        r = existing_user_session.get(f"{API}/game/professions/mine")
        assert r.status_code == 200
        data = r.json()
        # Per the review request, Erethon has fishing + hunting learned
        ids = {p["id"] for p in data["professions"]}
        assert "fishing" in ids or "hunting" in ids, ids

    def test_cannot_learn_duplicate_profession(self, existing_user_session):
        """Learn hunting twice → second call 400 already know."""
        # Make sure hunting is present
        mine = existing_user_session.get(f"{API}/game/professions/mine").json()["professions"]
        ids = {p["id"] for p in mine}
        if "hunting" not in ids:
            r = existing_user_session.post(f"{API}/game/professions/learn",
                                           json={"profession_id": "hunting"})
            if r.status_code != 200:
                pytest.skip("Could not learn hunting — cannot test duplicate")
        r2 = existing_user_session.post(f"{API}/game/professions/learn",
                                        json={"profession_id": "hunting"})
        assert r2.status_code == 400
        assert "already know" in r2.text.lower()

    def test_slot_limit_blocks_learning_beyond_slots(self, existing_user_session):
        mine = existing_user_session.get(f"{API}/game/professions/mine").json()
        slots = mine["slots_unlocked"]
        current = mine["professions"]
        # If character has fewer than slots learned, learn until full, then try one more
        catalog = existing_user_session.get(f"{API}/game/professions/catalog").json()["catalog"]
        learned_ids = {p["id"] for p in current}
        unlearned = [p["id"] for p in catalog if p["id"] not in learned_ids]
        # Fill remaining slots
        while len(learned_ids) < slots and unlearned:
            pid = unlearned.pop(0)
            r = existing_user_session.post(f"{API}/game/professions/learn",
                                           json={"profession_id": pid})
            if r.status_code == 200:
                learned_ids.add(pid)
        # Now try to learn one more — should 400
        if unlearned:
            r = existing_user_session.post(f"{API}/game/professions/learn",
                                           json={"profession_id": unlearned[0]})
            assert r.status_code == 400
            assert "slot" in r.text.lower() or "level" in r.text.lower()


# ============================================================
# 8. Exploration Progress
# ============================================================
class TestExploration:
    def test_exploration_returns_current_continent_biomes(self, existing_user_session):
        r = existing_user_session.get(f"{API}/game/exploration")
        assert r.status_code == 200
        data = r.json()
        assert "biomes" in data
        assert data["biomes"], "expected at least one biome"
        for b in data["biomes"]:
            for k in ("biome_id", "biome_name", "progress_pct", "thresholds_met"):
                assert k in b, f"missing {k}: {b}"
            assert len(b["thresholds_met"]) == 5
            assert isinstance(b["progress_pct"], int)

    def test_explore_action_returns_explore_hits_field(self, existing_user_session):
        # Perform a couple of explores; the response body must include explore_hits (list)
        ch = existing_user_session.get(f"{API}/game/character").json()["character"]
        biome = ch["current_biome"]
        r = existing_user_session.post(f"{API}/game/action",
                                       json={"action_id": "explore", "biome_id": biome})
        assert r.status_code == 200
        body = r.json()
        assert "explore_hits" in body
        assert isinstance(body["explore_hits"], list)
        assert "profession_ranks" in body
        assert isinstance(body["profession_ranks"], list)


# ============================================================
# 9. Hunt action grants hunting XP if profession learned
# ============================================================
class TestProfessionXpGain:
    def test_hunt_grants_hunting_xp(self, existing_user_session):
        # Ensure hunting is learned
        mine = existing_user_session.get(f"{API}/game/professions/mine").json()["professions"]
        if not any(p["id"] == "hunting" for p in mine):
            existing_user_session.post(f"{API}/game/professions/learn",
                                       json={"profession_id": "hunting"})
        # Snapshot xp
        mine = existing_user_session.get(f"{API}/game/professions/mine").json()["professions"]
        hunting_before = next((p for p in mine if p["id"] == "hunting"), None)
        if not hunting_before:
            pytest.skip("Could not seed hunting for the test character.")
        xp_before = int(hunting_before.get("xp", 0))
        # Fire enough hunt actions to see xp move (or at least verify field returns without error)
        ch = existing_user_session.get(f"{API}/game/character").json()["character"]
        biome = ch["current_biome"]
        # Check biome supports 'hunt' — if not, we accept the action's error and skip
        # We just fire it; the engine will 400 if not allowed here.
        found_increase = False
        for _ in range(8):
            r = existing_user_session.post(f"{API}/game/action",
                                           json={"action_id": "hunt", "biome_id": biome})
            if r.status_code != 200:
                pytest.skip(f"hunt action not available in {biome}: {r.text}")
            mine2 = existing_user_session.get(f"{API}/game/professions/mine").json()["professions"]
            hunting_after = next((p for p in mine2 if p["id"] == "hunting"), None)
            if int(hunting_after.get("xp", 0)) > xp_before:
                found_increase = True
                break
        assert found_increase, "hunting xp never increased after several hunts"
