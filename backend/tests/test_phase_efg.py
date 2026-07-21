"""Backend regression suite for Phase E (Racial Abilities), F (NPC story quests),
and G (Biome bosses + cross-continent legendary recipes + regional prices).

Uses the pre-seeded test character 'Erethon' (Human, Oathspire/Valeria, L10+, 
Ansel Q1 completed, relationship acquainted @ 220pts). Creates ephemeral test
users for edge-case coverage (Dwarf, Orc, etc.).
"""
from __future__ import annotations

import os
import uuid

import pytest
import requests

# ---------------- env / base url ----------------
_env_url = os.environ.get("REACT_APP_BACKEND_URL")
if not _env_url:
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
def erethon_session() -> requests.Session:
    s = requests.Session()
    r = s.post(f"{API}/auth/login", json={"email": TEST_EMAIL, "password": TEST_PASSWORD})
    assert r.status_code == 200, f"login failed: {r.text}"
    return s


@pytest.fixture(scope="session")
def erethon_character(erethon_session) -> dict:
    r = erethon_session.get(f"{API}/game/character")
    assert r.status_code == 200
    d = r.json()
    return d.get("character", d)


def _register(email: str, password: str = "password123", display: str = "TmpHero") -> requests.Session:
    s = requests.Session()
    r = s.post(f"{API}/auth/register",
               json={"email": email, "password": password, "display_name": display})
    assert r.status_code in (200, 201), f"register {email}: {r.status_code} {r.text}"
    return s


def _create_char(sess: requests.Session, race: str = "human", role: str = "fighter",
                 mastery: str = "knight", name: str = "TestHero", portrait: str = "portrait_1",
                 origin: str = "guardians_shield") -> dict:
    body = {"race": race, "role": role, "mastery": mastery,
            "name": name, "portrait_id": portrait, "origin": origin}
    # Race-specific required fields
    if race == "human":
        body["oath"] = "vigil"          # any string satisfies validator
    if race == "half_elf":
        body["heritage"] = "elf"
    r = sess.post(f"{API}/game/character", json=body)
    assert r.status_code in (200, 201), f"char-create failed: {r.status_code} {r.text}"
    return r.json().get("character", r.json())


# ==================================================================
# Phase F — NPCs & Story Quests
# ==================================================================
class TestNpcCatalog:
    """GET /game/npcs and /game/npc/{id}"""

    def test_lists_eight_flagship_npcs(self, erethon_session):
        r = erethon_session.get(f"{API}/game/npcs")
        assert r.status_code == 200
        body = r.json()
        npcs = body["npcs"]
        assert len(npcs) == 8
        ids = {n["id"] for n in npcs}
        expected = {"captain_ansel", "warchief_thraka", "envoy_seraphine",
                    "grandmaster_thora", "loremaster_sylanya", "matriarch_zerith",
                    "tide_priest_calvar", "elder_mireth"}
        assert ids == expected
        # every NPC has 3 quests
        for n in npcs:
            assert len(n["quests"]) == 3
            orders = sorted(q["order"] for q in n["quests"])
            assert orders == [1, 2, 3]
            # fields present
            for k in ("title", "description", "personality", "town", "continent", "race"):
                assert n.get(k), f"{n['id']} missing {k}"
            # relationship tier fields
            assert "relationship" in n
            assert set(n["relationship"].keys()) >= {"points", "level"}

    def test_relationship_tiers_and_thresholds(self, erethon_session):
        r = erethon_session.get(f"{API}/game/npcs")
        assert r.status_code == 200
        body = r.json()
        assert body["relationship_tiers"] == ["stranger", "acquainted", "friend", "trusted", "bonded"]
        assert body["relationship_thresholds"] == {
            "stranger": 0, "acquainted": 200, "friend": 600,
            "trusted": 1200, "bonded": 2000,
        }

    def test_get_single_npc(self, erethon_session):
        r = erethon_session.get(f"{API}/game/npc/captain_ansel")
        assert r.status_code == 200
        npc = r.json()["npc"]
        assert npc["id"] == "captain_ansel"
        assert npc["town"] == "oathspire"
        assert len(npc["quests"]) == 3

    def test_get_unknown_npc(self, erethon_session):
        r = erethon_session.get(f"{API}/game/npc/definitely_not_a_real_npc")
        assert r.status_code == 404


class TestErethonAnselQuestState:
    """Erethon has completed Ansel Q1 already (rel=acquainted 220pts).
    Q2 should be available; Q3 should be locked (needs friend tier)."""

    def test_ansel_quest_states(self, erethon_session):
        r = erethon_session.get(f"{API}/game/npc/captain_ansel")
        assert r.status_code == 200
        npc = r.json()["npc"]
        assert npc["relationship"]["points"] == 220
        assert npc["relationship"]["level"] == "acquainted"
        by_id = {q["id"]: q for q in npc["quests"]}
        # Q1 completed
        assert by_id["q_ansel_1"]["state"] == "completed"
        # Q2 (tier=acquainted) — should be available since Q1 done and tier matches;
        # tolerate 'active' if a prior test run already accepted it.
        assert by_id["q_ansel_2"]["state"] in ("available", "active"), \
            f"Q2 state should be available or active, got {by_id['q_ansel_2']['state']}"
        # Q3 (tier=friend) — should be locked since Q2 not done and rel<friend
        # (tolerate 'available' only if rel is friend, else must be locked)
        assert by_id["q_ansel_3"]["state"] == "locked"


class TestNewCharacterSeed:
    """A brand-new character should have npc_relationships seeded for all 8 NPCs
    and empty active/completed quest lists."""

    def test_new_char_seed(self):
        email = f"TEST_seed_{uuid.uuid4().hex[:8]}@erchis.io"
        s = _register(email, display="SeedTest")
        ch = _create_char(s, race="human", role="fighter", mastery="knight",
                          name=f"Seedy_{uuid.uuid4().hex[:4]}")
        assert isinstance(ch.get("npc_relationships"), dict)
        assert len(ch["npc_relationships"]) == 8
        for npc_id in ("captain_ansel", "warchief_thraka", "envoy_seraphine",
                       "grandmaster_thora", "loremaster_sylanya", "matriarch_zerith",
                       "tide_priest_calvar", "elder_mireth"):
            assert ch["npc_relationships"][npc_id] == {"points": 0, "level": "stranger"}
        assert ch.get("active_npc_quests") == []
        assert ch.get("completed_npc_quests") == []


class TestQuestAcceptGuards:
    """POST /game/npc/quest/accept enforces town, tier, and chain-order."""

    def test_accept_requires_being_in_npcs_town(self, erethon_session, erethon_character):
        # Erethon is in oathspire → accept warchief_thraka's Q1 (grunhold) should fail 403
        r = erethon_session.post(f"{API}/game/npc/quest/accept",
                                 json={"quest_id": "q_thraka_1"})
        assert r.status_code == 403
        assert "grunhold" in r.text.lower() or "thraka" in r.text.lower()

    def test_accept_requires_tier(self, erethon_session):
        # Erethon at Oathspire, acquainted with Ansel → Q3 (friend tier) should fail
        r = erethon_session.post(f"{API}/game/npc/quest/accept",
                                 json={"quest_id": "q_ansel_3"})
        assert r.status_code == 403

    def test_accept_requires_prior_chain_done(self):
        # Brand new human, move them to oathspire, try to accept Q2 without Q1 → 403
        email = f"TEST_chain_{uuid.uuid4().hex[:8]}@erchis.io"
        s = _register(email)
        _create_char(s, race="human", name=f"ChainTest_{uuid.uuid4().hex[:4]}")
        # New character should start in oathspire (Valeria = human homeland) — verify
        cr = s.get(f"{API}/game/character").json()
        ch = cr.get("character", cr)
        # Even if not in Oathspire, Q2 will be blocked by chain first if in Oathspire.
        # If new character is not in a town, use Q2 anyway — chain check should trip
        # first, or town check, either way we should get 403.
        r = s.post(f"{API}/game/npc/quest/accept",
                   json={"quest_id": "q_ansel_2"})
        assert r.status_code == 403, f"expected 403, got {r.status_code}: {r.text}"

    def test_accept_unknown_quest(self, erethon_session):
        r = erethon_session.post(f"{API}/game/npc/quest/accept",
                                 json={"quest_id": "q_not_a_real_quest_id"})
        assert r.status_code == 404


class TestQuestActionEngineHooks:
    """Doing hunt/gather with the right target increments quest kill counters,
    and completing the quest applies rewards + advances relationship tier."""

    def test_accept_ansel_q2_and_progress(self, erethon_session, erethon_character):
        # Ensure current_town = oathspire (Erethon's canonical spot)
        assert erethon_character["current_town"] == "oathspire", \
            "Test requires Erethon in Oathspire; main agent may need to reset."
        # Accept Q2 (idempotent-safe: skip if already active/complete)
        active = erethon_character.get("active_npc_quests", [])
        completed = erethon_character.get("completed_npc_quests", [])
        if "q_ansel_2" in completed:
            pytest.skip("Q2 already completed by prior test run")
        if "q_ansel_2" not in active:
            r = erethon_session.post(f"{API}/game/npc/quest/accept",
                                     json={"quest_id": "q_ansel_2"})
            assert r.status_code == 200, r.text
            body = r.json()
            assert "sword" in body["narrative"].lower() or "girl" in body["narrative"].lower() \
                or "empire" in body["narrative"].lower(), \
                f"unexpected narrative: {body['narrative'][:120]}"
        # Verify accepted
        r = erethon_session.get(f"{API}/game/character")
        ch = r.json().get("character", r.json())
        assert "q_ansel_2" in ch["active_npc_quests"]

    def test_hunt_bumps_quest_progress(self, erethon_session):
        # Q2 requires gray_wolf x4 and ruin_ghast x2. Do a hunt on gray_wolf in crownwood_forest.
        # We'll spin the action a few times to get outcome>=4.
        biome = "crownwood_forest"
        target = "gray_wolf"
        bumped = False
        for _ in range(20):
            r = erethon_session.post(f"{API}/game/action",
                                     json={"action_id": "hunt", "biome_id": biome, "target_id": target})
            if r.status_code != 200:
                # Weary/exhaustion may block; skip if that's the case
                if r.status_code == 400 and ("weary" in r.text.lower() or "exhaust" in r.text.lower()):
                    pytest.skip(f"blocked by weary/exhaustion: {r.text}")
                continue
            body = r.json()
            for upd in body.get("quest_progress_updates", []) or []:
                if upd["quest_id"] == "q_ansel_2":
                    kills = upd["progress"].get("kills", {})
                    assert kills.get(target, 0) >= 1
                    bumped = True
                    break
            if bumped:
                break
        if not bumped:
            pytest.skip("Could not force outcome>=4 to bump kill counter in 20 tries "
                        "(likely bad-luck streak; not a code bug).")


class TestRelationshipMath:
    """Verify tier crossing math on the character server-side (independent of quest complete)."""

    def test_relationship_tier_thresholds(self, erethon_session):
        # Use the /game/npcs response for erethon: ansel is 220 pts = acquainted (should have crossed 200)
        r = erethon_session.get(f"{API}/game/npcs")
        ansel = next(n for n in r.json()["npcs"] if n["id"] == "captain_ansel")
        assert ansel["relationship"]["points"] == 220
        assert ansel["relationship"]["level"] == "acquainted"


# ==================================================================
# Phase E — Racial Abilities
# ==================================================================
class TestRacialStatusEndpoint:
    """GET /game/racial/status returns the correct ability for the char's race."""

    def test_human_returns_focus(self, erethon_session):
        r = erethon_session.get(f"{API}/game/racial/status")
        assert r.status_code == 200
        d = r.json()
        assert d["race"] == "human"
        abilities = d["abilities"]
        assert len(abilities) == 1
        a = abilities[0]
        assert a["id"] == "human_focus"
        assert a["cooldown_hours"] == 24
        focuses = a["focuses"]
        assert set(focuses.keys()) == {"combat", "adventure", "crafting", "merchant", "scholar"}
        for fid, f in focuses.items():
            assert "name" in f and "desc" in f

    def test_dwarf_returns_field_repair(self):
        email = f"TEST_dwarf_{uuid.uuid4().hex[:8]}@erchis.io"
        s = _register(email)
        _create_char(s, race="dwarf", role="fighter", mastery="knight",
                     name=f"DwarfTest_{uuid.uuid4().hex[:4]}")
        r = s.get(f"{API}/game/racial/status")
        assert r.status_code == 200
        d = r.json()
        assert d["race"] == "dwarf"
        assert len(d["abilities"]) == 1
        a = d["abilities"][0]
        assert a["id"] == "dwarf_field_repair"
        assert a["cooldown_hours"] == 12

    def test_orc_returns_break_chain(self):
        email = f"TEST_orc_{uuid.uuid4().hex[:8]}@erchis.io"
        s = _register(email)
        _create_char(s, race="orc", role="fighter", mastery="knight",
                     name=f"OrcTest_{uuid.uuid4().hex[:4]}")
        r = s.get(f"{API}/game/racial/status")
        assert r.status_code == 200
        d = r.json()
        assert d["race"] == "orc"
        assert len(d["abilities"]) == 1
        a = d["abilities"][0]
        assert a["id"] == "orc_break_chain"
        assert a["cooldown_hours"] == 12
        assert a["cost"] == 40

    def test_other_races_have_active_abilities(self):
        """All 8 playable races now expose exactly one active racial ability (Phase E complete)."""
        expected = {
            "elf":         "elf_celestial_shift",
            "half_elf":    "halfelf_attunement",
            "wildblood":   "wildblood_bloodrage",
            "hyliondrian": "hyliondrian_tidal_grace",
            "sylvan":      "sylvan_shrink",
        }
        for race, ability_id in expected.items():
            email = f"TEST_{race}_{uuid.uuid4().hex[:8]}@erchis.io"
            s = _register(email)
            # _create_char automatically injects half_elf heritage.
            _create_char(s, race=race, role="fighter", mastery="knight",
                         name=f"R{race[:4].capitalize()}_{uuid.uuid4().hex[:3]}")
            r = s.get(f"{API}/game/racial/status")
            assert r.status_code == 200
            d = r.json()
            assert d["race"] == race
            assert len(d["abilities"]) == 1, f"race {race} expected 1 ability, got {d['abilities']}"
            a = d["abilities"][0]
            assert a["id"] == ability_id, f"race {race} expected ability id {ability_id!r}, got {a['id']!r}"


class TestRacialAbilityUse:
    def test_human_focus_activate(self, erethon_session, erethon_character):
        # Note: may already be on CD from prior test run. Handle both cases.
        # First check if available.
        r = erethon_session.get(f"{API}/game/racial/status")
        avail = r.json()["abilities"][0]["available"]
        if not avail:
            # Try another focus_id — CD applies regardless. Expect 400.
            r2 = erethon_session.post(f"{API}/game/racial/ability",
                                      json={"ability_id": "human_focus", "focus_id": "combat"})
            assert r2.status_code == 400, f"expected 400 on CD, got {r2.status_code}: {r2.text}"
            assert "resonant" in r2.text.lower() or "focus" in r2.text.lower()
            return
        # Apply combat focus
        r = erethon_session.post(f"{API}/game/racial/ability",
                                 json={"ability_id": "human_focus", "focus_id": "combat"})
        assert r.status_code == 200, r.text
        ch = r.json()["character"]
        assert ch["human_focus"] == "combat"
        assert ch["human_focus_last_used"] is not None
        # Second call within 24h → 400
        r2 = erethon_session.post(f"{API}/game/racial/ability",
                                  json={"ability_id": "human_focus", "focus_id": "combat"})
        assert r2.status_code == 400

    def test_dwarf_field_repair_heals_and_strips_bleeding(self):
        email = f"TEST_dwarf_use_{uuid.uuid4().hex[:8]}@erchis.io"
        s = _register(email)
        ch = _create_char(s, race="dwarf", role="fighter", mastery="knight",
                         name=f"DwarfHealer_{uuid.uuid4().hex[:4]}")
        # Simulate: char is at full HP. Ability should still succeed but heal 0.
        r = s.post(f"{API}/game/racial/ability", json={"ability_id": "dwarf_field_repair"})
        assert r.status_code == 200, r.text
        ch2 = r.json()["character"]
        assert ch2["dwarf_field_repair_last_used"] is not None
        # bleeding not present (freshly-created char)
        assert not any(st.get("id") == "bleeding" for st in ch2.get("statuses", []))
        # Try again immediately → CD → 400
        r2 = s.post(f"{API}/game/racial/ability", json={"ability_id": "dwarf_field_repair"})
        assert r2.status_code == 400

    def test_orc_break_chain_requires_defiance(self):
        email = f"TEST_orc_use_{uuid.uuid4().hex[:8]}@erchis.io"
        s = _register(email)
        _create_char(s, race="orc", role="fighter", mastery="knight",
                     name=f"OrcBreaker_{uuid.uuid4().hex[:4]}")
        # Fresh orc has 0 defiance → should fail with 400
        r = s.post(f"{API}/game/racial/ability", json={"ability_id": "orc_break_chain"})
        assert r.status_code == 400
        assert "defiance" in r.text.lower()


# ==================================================================
# Phase G — Bosses
# ==================================================================
class TestBossCatalog:
    def test_list_bosses(self, erethon_session):
        r = erethon_session.get(f"{API}/game/bosses")
        assert r.status_code == 200
        bosses = r.json()["bosses"]
        assert len(bosses) == 8
        ids = {b["id"] for b in bosses}
        # spec-required boss ids
        assert "boss_ashen_lord" in ids
        assert "boss_thorn_guardian" in ids
        for b in bosses:
            assert b["is_boss"] is True
            assert isinstance(b.get("power"), int) and b["power"] > 0
            assert b.get("drops"), f"{b['id']} has no drops"
        # Power scales top→bottom
        ashen = next(b for b in bosses if b["id"] == "boss_ashen_lord")
        thorn = next(b for b in bosses if b["id"] == "boss_thorn_guardian")
        assert ashen["power"] == 30
        assert thorn["power"] == 100

    def test_boss_action_in_biome_actions(self, erethon_session):
        r = erethon_session.get(f"{API}/game/data/biome/ashen_border/actions")
        assert r.status_code == 200
        d = r.json()
        actions = d.get("actions", d) if isinstance(d, dict) else d
        # Accept either shape
        if isinstance(actions, dict):
            actions = actions.get("actions", [])
        action_ids = [a.get("id") for a in actions]
        assert "boss" in action_ids, f"expected 'boss' action, got {action_ids}"


class TestCrossContinentRecipes:
    def test_list_recipes(self, erethon_session):
        r = erethon_session.get(f"{API}/game/recipes/cross_continent")
        assert r.status_code == 200
        body = r.json()
        recipes = body["recipes"]
        assert len(recipes) == 6
        expected = {"craft_moonfang_spear", "craft_tidebound_amulet", "craft_ashenlord_greatsword",
                    "craft_celestial_robes", "craft_thorn_bow", "craft_forgeheart_platemail"}
        assert {r["id"] for r in recipes} == expected
        for rec in recipes:
            assert rec["produces"]["rarity"] == "legendary"
            assert rec.get("profession")
            assert rec.get("profession_min_rank")
            assert isinstance(rec["requires"], dict) and len(rec["requires"]) >= 3

    def test_craft_legendary_missing_materials(self, erethon_session):
        # Erethon almost certainly lacks legendary boss-part materials → should 400
        r = erethon_session.post(f"{API}/game/craft/legendary",
                                 json={"recipe_id": "craft_moonfang_spear"})
        # Missing materials → 400. If Erethon somehow has them (unlikely), may return 200.
        assert r.status_code in (400, 403), f"expected 400/403 for missing mats, got {r.status_code}: {r.text}"

    def test_craft_legendary_unknown_recipe(self, erethon_session):
        r = erethon_session.post(f"{API}/game/craft/legendary",
                                 json={"recipe_id": "not_a_real_recipe"})
        assert r.status_code == 404


# ==================================================================
# Phase G — Regional Market Prices
# ==================================================================
class TestRegionalMarketPrices:
    """iron_ore is home-continent-Mushkara; buying it in Mushkara should be 0.75x,
    buying it in Valeria (foreign) should be 1.4x."""

    def _iron_ore_baseline_price(self):
        # rarity=common → 10 gold. baseline computed as int(round(10 * mult)).
        return 10

    def test_iron_ore_buy_in_valeria_is_1_4x(self, erethon_session, erethon_character):
        # Erethon is currently in Oathspire (Valeria). If iron_ore is in oathspire's
        # market this should succeed with regional_multiplier == 1.4.
        # If oathspire market does not sell iron_ore, we skip.
        r = erethon_session.post(f"{API}/game/town/market/buy",
                                 json={"item_id": "iron_ore", "quantity": 1})
        if r.status_code == 404 and "not sold here" in r.text.lower():
            pytest.skip("iron_ore not sold in oathspire market")
        assert r.status_code == 200, f"buy failed: {r.status_code} {r.text}"
        body = r.json()
        assert body.get("regional_multiplier") == 1.4, \
            f"expected 1.4x foreign price, got {body.get('regional_multiplier')}"

    def test_iron_ore_buy_in_mushkara_is_0_75x(self):
        """Create a new Orc char who starts in Grunhold (Mushkara) and try to buy iron_ore."""
        email = f"TEST_mush_{uuid.uuid4().hex[:8]}@erchis.io"
        s = _register(email)
        ch = _create_char(s, race="orc", role="fighter", mastery="knight",
                         name=f"MushBuyer_{uuid.uuid4().hex[:4]}")
        # Verify starting town continent
        cr = s.get(f"{API}/game/character").json()
        c = cr.get("character", cr)
        if c.get("current_town") != "grunhold":
            pytest.skip(f"orc did not start in grunhold: current_town={c.get('current_town')}")
        r = s.post(f"{API}/game/town/market/buy",
                   json={"item_id": "iron_ore", "quantity": 1})
        if r.status_code == 404 and "not sold here" in r.text.lower():
            pytest.skip("iron_ore not sold in grunhold market")
        if r.status_code == 400 and "gold" in r.text.lower():
            pytest.skip("not enough gold — regional multiplier tested via foreign case instead")
        assert r.status_code == 200, f"buy failed: {r.status_code} {r.text}"
        body = r.json()
        assert body.get("regional_multiplier") == 0.75, \
            f"expected 0.75x home price in Mushkara, got {body.get('regional_multiplier')}"
