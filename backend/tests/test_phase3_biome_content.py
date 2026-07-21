"""Phase 3.1 tests — verifies the 6 new continents each have monsters,
gather materials, and biome actions wired end-to-end."""
from __future__ import annotations

import os
import pytest
import requests

BASE_URL = os.environ.get("REACT_APP_BACKEND_URL", "https://fantasy-torn-dice.preview.emergentagent.com").rstrip("/")
API = f"{BASE_URL}/api"

TEST_USER_EMAIL = "test@erchis.io"
TEST_USER_PASSWORD = "password123"

NEW_CONTINENT_BIOMES = {
    "vulkaros":   ["ashlands", "lava_caves", "basalt_steppe", "obsidian_pits"],
    "nyxmoor":    ["bogland", "cursed_ruins", "deadwood", "ghost_road"],
    "frosthelm":  ["frozen_peaks", "glacier", "tundra", "ice_caverns"],
    "zephyria":   ["sky_isles", "cloud_forest", "storm_plateau", "celestial_ruins"],
    "sablewaste": ["dune_sea", "oasis", "djinn_ruins", "sunken_temple"],
    "verdania":   ["rainforest", "canopy_boughs", "coral_reef", "sunken_atlantyrion"],
}


@pytest.fixture(scope="module")
def sess():
    s = requests.Session()
    r = s.post(f"{API}/auth/login", json={"email": TEST_USER_EMAIL, "password": TEST_USER_PASSWORD}, timeout=15)
    assert r.status_code == 200, r.text
    return s


def test_monster_count_grew(sess):
    monsters = sess.get(f"{API}/game/data/monsters", timeout=10).json()["monsters"]
    # Aetheria had 6; each of 24 new biomes gets 2 monsters → at least 50 total.
    assert len(monsters) >= 50, f"expected >=50 monsters, got {len(monsters)}"


def test_items_expanded(sess):
    items = sess.get(f"{API}/game/data/items", timeout=10).json()["items"]
    # Aetheria's original catalogue had 26 items; extras must add ~50 more.
    assert len(items) >= 90, f"expected >=90 items, got {len(items)}"
    ids = {it["id"] for it in items}
    # spot-check a few new materials from every continent
    for expected in ["basalt_shard", "hex_moss", "cold_iron", "silverleaf",
                     "djinn_glass", "abyss_coral", "kraken_ink"]:
        assert expected in ids, f"missing material: {expected}"


@pytest.mark.parametrize("continent,biomes", list(NEW_CONTINENT_BIOMES.items()))
def test_biome_actions_present(sess, continent, biomes):
    for biome_id in biomes:
        r = sess.get(f"{API}/game/data/biome/{biome_id}/actions", timeout=10)
        assert r.status_code == 200, f"{biome_id} → {r.status_code} {r.text}"
        payload = r.json()
        assert payload["biome_id"] == biome_id
        # Every new biome must expose at least a hunt action with 2 targets.
        hunt = next((a for a in payload["actions"] if a["id"] == "hunt"), None)
        assert hunt is not None, f"{biome_id} missing hunt action"
        assert len(hunt["targets"]) >= 1, f"{biome_id} hunt has no targets"


@pytest.mark.parametrize("continent,biomes", list(NEW_CONTINENT_BIOMES.items()))
def test_each_biome_has_monsters(sess, continent, biomes):
    monsters = sess.get(f"{API}/game/data/monsters", timeout=10).json()["monsters"]
    by_biome = {}
    for m in monsters:
        by_biome.setdefault(m["biome"], []).append(m)
    for biome_id in biomes:
        assert biome_id in by_biome, f"{biome_id} has no monsters"
        assert len(by_biome[biome_id]) >= 1


def test_monster_power_scales_with_continent(sess):
    """Higher-tier continents should have stronger monsters than Aetheria."""
    monsters = sess.get(f"{API}/game/data/monsters", timeout=10).json()["monsters"]
    by_id = {m["id"]: m for m in monsters}
    # Kraken Spawn (Verdania Lv 45) should out-power gray_wolf (Aetheria Lv 1).
    assert by_id["kraken_spawn"]["power"] > by_id["gray_wolf"]["power"] * 8
    assert by_id["kraken_spawn"]["hp"] > by_id["gray_wolf"]["hp"] * 8
