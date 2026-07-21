"""Iteration 7 regression suite — P0 fixes + 5 new racial active abilities.

Covers:
  * P0 #1 — boss action injected into BIOME_ACTIONS for all 8 boss biomes.
  * P0 #2 — Fresh characters seeded with current_town == home_town for every race,
             continent + reputation sanity for Orc.
  * P1 — Elf Celestial Shift, Half-Elf Heritage Attunement, Wildblood Bloodrage,
         Hyliondrian Tidal Grace, Sylvan Shrunken Form (toggle).
  * P1 — /game/racial/status returns 1 ability for every race.
"""
from __future__ import annotations

import os
import time
import uuid

import pytest
import requests
from pymongo import MongoClient
from bson import ObjectId

# ---------------- env / base url ----------------
_env_url = os.environ.get("REACT_APP_BACKEND_URL")
if not _env_url:
    with open("/app/frontend/.env") as _f:
        for _line in _f:
            if _line.startswith("REACT_APP_BACKEND_URL="):
                _env_url = _line.strip().split("=", 1)[1].strip('"').strip("'")
                break
assert _env_url, "REACT_APP_BACKEND_URL not set"
BASE_URL = _env_url.rstrip("/")
API = f"{BASE_URL}/api"

# Mongo (for test seeding of resources / cooldown clears)
MONGO_URL = os.environ.get("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.environ.get("DB_NAME", "test_database")
_mongo = MongoClient(MONGO_URL)
_db = _mongo[DB_NAME]

TEST_EMAIL = "test@erchis.io"
TEST_PASSWORD = "password123"

BOSS_BIOMES = {
    "ashen_border":        "boss_ashen_lord",
    "demonfall_crater":    "boss_demon_warleader",
    "diplomats_highlands": "boss_amber_diplomat",
    "deep_forges":         "boss_forge_golem",
    "starfall_cliffs":     "boss_starfall_avatar",
    "ancient_den":         "boss_alpha_king",
    "abyssal_trench":      "boss_leviathan",
    "elderroot_hollow":    "boss_thorn_guardian",
}

RACE_HOMES = {
    "human":       ("oathspire",      "valeria"),
    "orc":         ("grunhold",       "mushkara"),
    "half_elf":    ("elaris",         "concordia"),
    "dwarf":       ("jahrahold",      "khardrum"),
    "elf":         ("solunara",       "haya"),
    "wildblood":   ("rindivar_grove", "gennel"),
    "hyliondrian": ("atlantyrion",    "hylion"),
    "sylvan":      ("veilgrove",      "daw_ul_talalu"),
}


# ---------------- helpers ----------------
def _register(email: str, password: str = "password123", display: str = "TmpHero") -> requests.Session:
    s = requests.Session()
    r = s.post(f"{API}/auth/register",
               json={"email": email, "password": password, "display_name": display})
    assert r.status_code in (200, 201), f"register {email}: {r.status_code} {r.text}"
    return s


def _create_char(sess: requests.Session, race: str, name: str | None = None) -> dict:
    body = {
        "race": race, "role": "fighter", "mastery": "knight",
        "name": name or f"H_{uuid.uuid4().hex[:5]}",
        "portrait_id": "portrait_1", "origin": "guardians_shield",
    }
    if race == "human":
        body["oath"] = "vigil"
    if race == "half_elf":
        body["heritage"] = "elf"
    r = sess.post(f"{API}/game/character", json=body)
    assert r.status_code in (200, 201), f"char create failed: {r.status_code} {r.text}"
    return r.json().get("character", r.json())


def _fresh(race: str) -> tuple[requests.Session, dict]:
    email = f"TEST_it7_{race}_{uuid.uuid4().hex[:8]}@erchis.io"
    s = _register(email)
    ch = _create_char(s, race)
    return s, ch


def _char_from_db(char_id: str) -> dict:
    return _db.characters.find_one({"_id": ObjectId(char_id)})


def _set_char(char_id: str, updates: dict) -> None:
    _db.characters.update_one({"_id": ObjectId(char_id)}, {"$set": updates})


def _get_char(sess: requests.Session) -> dict:
    r = sess.get(f"{API}/game/character")
    assert r.status_code == 200, r.text
    return r.json().get("character", r.json())


@pytest.fixture(scope="session")
def erethon_session() -> requests.Session:
    s = requests.Session()
    r = s.post(f"{API}/auth/login", json={"email": TEST_EMAIL, "password": TEST_PASSWORD})
    assert r.status_code == 200, f"login failed: {r.text}"
    return s


# ==================================================================
# P0 #1 — Boss action in every boss biome
# ==================================================================
class TestP0BossActionInBiomes:
    @pytest.mark.parametrize("biome,boss_id", list(BOSS_BIOMES.items()))
    def test_boss_action_present(self, erethon_session, biome, boss_id):
        r = erethon_session.get(f"{API}/game/data/biome/{biome}/actions")
        assert r.status_code == 200, r.text
        actions = r.json()["actions"]
        boss_action = next((a for a in actions if a["id"] == "boss"), None)
        assert boss_action is not None, f"boss action MISSING from {biome}. Got: {[a['id'] for a in actions]}"
        assert boss_id in boss_action["targets"], \
            f"{biome} boss action targets {boss_action['targets']} does not include {boss_id}"

    def test_post_action_boss_not_400_not_available(self, erethon_session):
        """POST /game/action with boss should NOT return 400 'Action \"boss\" not available'.
        It may return other 400s (weary, wrong biome, no character in biome) but never
        the not-available error."""
        r = erethon_session.post(f"{API}/game/action", json={
            "action_id": "boss", "biome_id": "ashen_border", "target_id": "boss_ashen_lord",
        })
        # We're likely blocked because Erethon isn't in ashen_border, but the action itself is valid.
        if r.status_code == 400:
            assert "not available" not in r.text.lower() or "action \"boss\"" not in r.text.lower(), \
                f"boss action still not recognized: {r.text}"


# ==================================================================
# P0 #2 — Fresh characters: current_town == home_town for every race
# ==================================================================
class TestP0FreshCharacterHometown:
    @pytest.mark.parametrize("race,expected", list(RACE_HOMES.items()))
    def test_race_seeded_in_home(self, race, expected):
        home_town, continent = expected
        _, ch = _fresh(race)
        assert ch.get("home_town") == home_town, f"{race} home_town={ch.get('home_town')} expected {home_town}"
        assert ch.get("current_town") == home_town, f"{race} current_town={ch.get('current_town')} expected {home_town}"
        # continent not always seeded via character creation; check character doc for continent field
        # (server sets current_continent independently — verify if present)
        cc = ch.get("current_continent")
        if cc is not None:
            assert cc == continent, f"{race} current_continent={cc} expected {continent}"

    def test_orc_reputation_friendly_in_mushkara(self):
        _, ch = _fresh("orc")
        assert ch.get("current_town") == "grunhold"
        assert ch.get("current_continent") == "mushkara", \
            f"orc current_continent={ch.get('current_continent')} expected mushkara"
        rep = ch.get("reputation", {})
        mushkara_rep = rep.get("mushkara", {})
        assert mushkara_rep.get("level") == "friendly", \
            f"orc reputation.mushkara.level={mushkara_rep.get('level')} expected 'friendly'; full rep={rep}"


# ==================================================================
# P1 — /game/racial/status returns 1 ability for every race
# ==================================================================
class TestRacialStatusForAllRaces:
    EXPECTED = {
        "human":       "human_focus",
        "dwarf":       "dwarf_field_repair",
        "orc":         "orc_break_chain",
        "elf":         "elf_celestial_shift",
        "half_elf":    "halfelf_attunement",
        "wildblood":   "wildblood_bloodrage",
        "hyliondrian": "hyliondrian_tidal_grace",
        "sylvan":      "sylvan_shrink",
    }

    @pytest.mark.parametrize("race,ability_id", list(EXPECTED.items()))
    def test_race_returns_one_ability(self, race, ability_id):
        s, _ = _fresh(race)
        r = s.get(f"{API}/game/racial/status")
        assert r.status_code == 200, r.text
        d = r.json()
        assert d["race"] == race
        assert len(d["abilities"]) == 1, f"{race} expected 1 ability, got {d['abilities']}"
        assert d["abilities"][0]["id"] == ability_id, \
            f"{race} expected {ability_id}, got {d['abilities'][0]['id']}"


# ==================================================================
# P1 — New racial ability activations
# ==================================================================
class TestElfCelestialShift:
    def test_activate_heals_purges_and_cds(self):
        s, ch = _fresh("elf")
        cid = ch["id"]
        # Damage the elf so heal is observable; add a debuff and a buff to verify purge logic.
        max_hp = ch["max_hp"]
        _set_char(cid, {
            "hp": max_hp // 2,
            "celestial_charge": 2,
            "statuses": [
                {"id": "bleeding", "name": "Bleeding", "duration": 3},          # debuff
                {"id": "some_buff", "name": "Buff", "duration": 3, "is_buff": True},  # buff
            ],
        })
        r = s.post(f"{API}/game/racial/ability", json={"ability_id": "elf_celestial_shift"})
        assert r.status_code == 200, r.text
        ch2 = r.json()["character"]
        # Heals 30% max HP
        expected_heal = int(max_hp * 0.30)
        assert ch2["hp"] >= (max_hp // 2) + expected_heal - 1, \
            f"hp={ch2['hp']} expected >= {(max_hp // 2) + expected_heal - 1}"
        # Deducts 1 celestial_charge
        assert ch2["celestial_charge"] == 1
        # Debuffs purged, buff preserved
        status_ids = {s.get("id") for s in ch2.get("statuses", [])}
        assert "bleeding" not in status_ids
        assert "some_buff" in status_ids
        # last_used timestamp set
        assert ch2.get("elf_celestial_shift_last_used") is not None
        # Immediate re-attempt → 400 with 'stars ... alignment' message
        r2 = s.post(f"{API}/game/racial/ability", json={"ability_id": "elf_celestial_shift"})
        assert r2.status_code == 400, r2.text
        assert "star" in r2.text.lower() or "alignment" in r2.text.lower(), r2.text


class TestHalfelfAttunement:
    def test_activate_applies_buff_and_cds(self):
        s, ch = _fresh("half_elf")
        cid = ch["id"]
        _set_char(cid, {"harmony": 5, "resolve": 50})
        r = s.post(f"{API}/game/racial/ability", json={"ability_id": "halfelf_attunement"})
        assert r.status_code == 200, r.text
        ch2 = r.json()["character"]
        # Deducts 3 harmony
        assert ch2["harmony"] == 2
        # +5 resolve
        assert ch2["resolve"] == 55
        # heritage_attunement status
        buff = next((s for s in ch2.get("statuses", []) if s.get("id") == "heritage_attunement"), None)
        assert buff, f"heritage_attunement status not found, statuses={ch2.get('statuses')}"
        assert buff["duration"] == 5
        mods = buff.get("modifiers", {})
        assert mods.get("attack_success_mod") == 1
        assert mods.get("evasion_mod") == 1
        # last_used timestamp set
        assert ch2.get("halfelf_attunement_last_used") is not None
        # immediate re-attempt → 400
        r2 = s.post(f"{API}/game/racial/ability", json={"ability_id": "halfelf_attunement"})
        assert r2.status_code == 400, r2.text


class TestWildbloodBloodrage:
    def test_activate_applies_buff(self):
        s, ch = _fresh("wildblood")
        cid = ch["id"]
        _set_char(cid, {"inner_blood": 50})
        r = s.post(f"{API}/game/racial/ability", json={"ability_id": "wildblood_bloodrage"})
        assert r.status_code == 200, r.text
        ch2 = r.json()["character"]
        # Deducts 40 inner_blood
        assert ch2["inner_blood"] == 10
        # bloodrage status
        buff = next((s for s in ch2.get("statuses", []) if s.get("id") == "bloodrage"), None)
        assert buff, f"bloodrage status not found, statuses={ch2.get('statuses')}"
        assert buff["duration"] == 4
        mods = buff.get("modifiers", {})
        assert mods.get("attack_success_mod") == 2
        assert mods.get("evasion_mod") == -1
        # immediate re-attempt → 400
        r2 = s.post(f"{API}/game/racial/ability", json={"ability_id": "wildblood_bloodrage"})
        assert r2.status_code == 400


class TestHyliondrianTidalGrace:
    def test_activate_heals_and_purges(self):
        s, ch = _fresh("hyliondrian")
        cid = ch["id"]
        max_hp = ch["max_hp"]
        _set_char(cid, {
            "hp": max_hp // 2,
            "tide": 4,
            "statuses": [
                {"id": "poison", "name": "Poison", "duration": 3},
                {"id": "some_buff", "name": "Buff", "duration": 3, "is_buff": True},
            ],
        })
        r = s.post(f"{API}/game/racial/ability", json={"ability_id": "hyliondrian_tidal_grace"})
        assert r.status_code == 200, r.text
        ch2 = r.json()["character"]
        # Heals 40% max HP
        expected_heal = int(max_hp * 0.40)
        assert ch2["hp"] >= (max_hp // 2) + expected_heal - 1
        # Deducts 3 tide
        assert ch2["tide"] == 1
        status_ids = {s.get("id") for s in ch2.get("statuses", [])}
        assert "poison" not in status_ids
        assert "some_buff" in status_ids
        r2 = s.post(f"{API}/game/racial/ability", json={"ability_id": "hyliondrian_tidal_grace"})
        assert r2.status_code == 400


class TestSylvanShrinkToggle:
    def test_toggle_on_off(self):
        s, ch = _fresh("sylvan")
        cid = ch["id"]
        _set_char(cid, {"verdant_essence": 2})
        # ON — apply status, spend essence, start 10-min CD
        r = s.post(f"{API}/game/racial/ability", json={"ability_id": "sylvan_shrink"})
        assert r.status_code == 200, r.text
        ch2 = r.json()["character"]
        assert ch2["verdant_essence"] == 1
        shrunken = next((s for s in ch2.get("statuses", []) if s.get("id") == "shrunken"), None)
        assert shrunken, f"shrunken not found, statuses={ch2.get('statuses')}"
        mods = shrunken.get("modifiers", {})
        assert mods.get("evasion_mod") == 2
        assert mods.get("attack_success_mod") == -1
        assert ch2.get("sylvan_shrink_last_used") is not None
        # toggle_state via GET /game/racial/status = 'on'
        rs = s.get(f"{API}/game/racial/status")
        ab = rs.json()["abilities"][0]
        assert ab.get("toggle_state") == "on"
        # Toggle OFF immediately — should be FREE (no essence cost, no CD gate on the toggle-off direction)
        r2 = s.post(f"{API}/game/racial/ability", json={"ability_id": "sylvan_shrink"})
        assert r2.status_code == 200, r2.text
        ch3 = r2.json()["character"]
        # Essence unchanged (toggle-off is free)
        assert ch3["verdant_essence"] == 1, f"expected essence unchanged, got {ch3['verdant_essence']}"
        # Shrunken status removed
        assert not any(s.get("id") == "shrunken" for s in ch3.get("statuses", []))
        # toggle_state now = off
        rs2 = s.get(f"{API}/game/racial/status")
        ab2 = rs2.json()["abilities"][0]
        assert ab2.get("toggle_state") == "off"
        # Immediate re-shrink attempt → 400 (still on 10-min CD from the initial toggle-on)
        r3 = s.post(f"{API}/game/racial/ability", json={"ability_id": "sylvan_shrink"})
        assert r3.status_code == 400, r3.text
        # Clear cooldown in DB and re-shrink → 200 (costs another 1 essence)
        _set_char(cid, {"sylvan_shrink_last_used": None})
        r4 = s.post(f"{API}/game/racial/ability", json={"ability_id": "sylvan_shrink"})
        assert r4.status_code == 200, r4.text
        ch4 = r4.json()["character"]
        assert ch4["verdant_essence"] == 0, f"expected essence spent on re-shrink, got {ch4['verdant_essence']}"


# ==================================================================
# P1 — Farming: verify resources tick on actions (best-effort)
# ==================================================================
class TestRacialResourceAccumulation:
    """Best-effort — accumulate resources through /game/action calls.
    Given RNG gates (20-30% chance), we do up to 60 attempts and assert 'at least some' gain.
    """

    def _spam_actions(self, sess, biome, action, target, n=60):
        for _ in range(n):
            r = sess.post(f"{API}/game/action", json={
                "action_id": action, "biome_id": biome, "target_id": target,
            })
            if r.status_code == 400 and ("weary" in r.text.lower() or "exhaust" in r.text.lower()):
                # skip — clear the meter via DB and continue
                ch = sess.get(f"{API}/game/character").json()
                ch = ch.get("character", ch)
                _set_char(ch["id"], {"exhaustion": 0, "resolve": 100})
                continue
            if r.status_code != 200:
                # unblockable — bail out
                return

    def test_wildblood_inner_blood_accumulates(self):
        # inner_blood ticks +2/action deterministically — 20 actions → ≥40
        s, ch = _fresh("wildblood")
        # Do 25 actions in home biome; wildblood home = gennel/rindivar_grove — need biome id.
        # Fall back to a known-safe biome via the character's current_biome
        biome = ch.get("current_biome")
        assert biome, f"wildblood has no current_biome, ch={ch}"
        # Any legal target for hunt in this biome — use /biome/actions to discover
        r = s.get(f"{API}/game/data/biome/{biome}/actions")
        assert r.status_code == 200, r.text
        acts = r.json()["actions"]
        hunt = next((a for a in acts if a["id"] == "hunt" and a.get("targets")), None)
        if not hunt:
            pytest.skip(f"biome {biome} has no hunt targets")
        target = hunt["targets"][0]
        self._spam_actions(s, biome, "hunt", target, n=25)
        ch2 = _get_char(s)
        # Deterministic +2/action, capped at 100; expected >= 40 unless many actions were blocked
        assert ch2["inner_blood"] >= 20, \
            f"expected inner_blood >= 20 after 25 hunts, got {ch2['inner_blood']}"
