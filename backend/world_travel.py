"""Phase B — Grand Teleporter, Waystones, and Homeland Reputation.

Spec:
- Grand Teleporter is located in every hometown. Travel between the 8 accessible
  continents. Costs gold + has a 10-min per-character cooldown.
- Waystones are discovered through exploration, activated for a fee, and then
  provide fast local travel within a continent.
- Homeland Reputation starts Friendly for the native race, Neutral for others.
"""
from __future__ import annotations
from datetime import datetime, timedelta, timezone

# ============================================================
# TELEPORTER
# ============================================================
TELEPORTER_FEE = 100          # base gold cost per hop (spec: 100g)
TELEPORTER_COOLDOWN_SECS = 600  # 10-minute cooldown per spec


def teleporter_can_use(character: dict, now: datetime | None = None) -> tuple[bool, str]:
    """Return (allowed, reason) — checks all the spec-mandated block conditions."""
    now = now or datetime.now(timezone.utc)
    if character.get("hp", 0) <= 0:
        return False, "You are downed. Rest first."
    # blocked while in combat / dungeon
    if character.get("in_combat"):
        return False, "You cannot teleport during combat."
    if character.get("in_dungeon"):
        return False, "You cannot teleport from inside a dungeon."
    # must be inside a hometown
    ct = character.get("current_town")
    if not ct:
        return False, "The Grand Teleporter is only in a hometown. Enter a town first."
    last = character.get("teleporter_last_used")
    if last:
        # last is an ISO string
        try:
            last_dt = datetime.fromisoformat(last)
        except ValueError:
            last_dt = None
        if last_dt and (now - last_dt).total_seconds() < TELEPORTER_COOLDOWN_SECS:
            remaining = TELEPORTER_COOLDOWN_SECS - int((now - last_dt).total_seconds())
            mins = remaining // 60
            secs = remaining % 60
            return False, f"Teleporter recharging. {mins}m {secs}s remaining."
    return True, ""


# ============================================================
# WAYSTONES — 2 per continent = 16 total (accessible continents only)
# ============================================================
WAYSTONES: list[dict] = [
    # ---------------- VALERIA ----------------
    {"id": "waystone_crownwood",   "name": "Crownwood Shrine",     "continent": "valeria",
     "biome": "crownwood_forest",   "activation_gold": 200,
     "desc": "A moss-covered ring of standing stones humming just below hearing."},
    {"id": "waystone_ashen_gate",  "name": "Ashen Border Gate",    "continent": "valeria",
     "biome": "ashen_border",       "activation_gold": 350,
     "desc": "An old imperial arch guarding the road east. Reactivate with any surviving oath."},

    # ---------------- MUSHKARA ----------------
    {"id": "waystone_ironscar",    "name": "Iron Scar Cairn",      "continent": "mushkara",
     "biome": "iron_scar",          "activation_gold": 400,
     "desc": "A blackened cairn built from the shields of a lost legion."},
    {"id": "waystone_demonfall",   "name": "Demonfall Wardstone",  "continent": "mushkara",
     "biome": "demonfall_crater",   "activation_gold": 700,
     "desc": "A binding stone that keeps the crater sane. Deep raiders anchor here."},

    # ---------------- CONCORDIA ----------------
    {"id": "waystone_amberwyn",    "name": "Amberwyn Rest",        "continent": "concordia",
     "biome": "amber_vineyards",    "activation_gold": 500,
     "desc": "A quiet vineyard hall where diplomats come to breathe."},
    {"id": "waystone_diplomacy",   "name": "Highlands Court",      "continent": "concordia",
     "biome": "diplomats_highlands","activation_gold": 800,
     "desc": "An ancient meeting-arch marked by all three founding races."},

    # ---------------- KHARDRUM ----------------
    {"id": "waystone_emberdown",   "name": "Emberdown Descent",    "continent": "khardrum",
     "biome": "ember_mines",        "activation_gold": 900,
     "desc": "A lift-shaft crowned with Jahra runes. Rests the miners' knees."},
    {"id": "waystone_deep_forges", "name": "Deep Forges Anvil",    "continent": "khardrum",
     "biome": "deep_forges",        "activation_gold": 1200,
     "desc": "A ceremonial anvil so old the ring lingers for hours after a strike."},

    # ---------------- HAYA ----------------
    {"id": "waystone_moonveil",    "name": "Moonveil Circle",      "continent": "haya",
     "biome": "moonveil_woods",     "activation_gold": 1400,
     "desc": "A silverleaf ring that answers only after moonrise."},
    {"id": "waystone_starfall",    "name": "Starfall Watch",       "continent": "haya",
     "biome": "starfall_cliffs",    "activation_gold": 1800,
     "desc": "A crystal thrown from the celestial ruins, still faintly warm."},

    # ---------------- GENNEL ----------------
    {"id": "waystone_beastwood",   "name": "Beastwood Totem",      "continent": "gennel",
     "biome": "beastwood",          "activation_gold": 2000,
     "desc": "A stack of skulls, painted feathers, and one old spear."},
    {"id": "waystone_ancient_den", "name": "Ancient Den",          "continent": "gennel",
     "biome": "ancient_den",        "activation_gold": 2600,
     "desc": "The first hunt's cave. Every alpha remembers stepping past this stone."},

    # ---------------- HYLION ----------------
    {"id": "waystone_kelp_reef",   "name": "Kelp Reef Shrine",     "continent": "hylion",
     "biome": "kelp_forest",        "activation_gold": 2800,
     "desc": "A ring of pearl-shell, glowing a slow blue with the tide."},
    {"id": "waystone_abyssal",     "name": "Abyssal Cairn",        "continent": "hylion",
     "biome": "abyssal_trench",     "activation_gold": 3600,
     "desc": "A wardstone anchored to the trench floor. Deep travellers offer light before descent."},

    # ---------------- DAW'UL TALALU ----------------
    {"id": "waystone_lumina",      "name": "Lumina Grove",         "continent": "daw_ul_talalu",
     "biome": "lumina_grove",       "activation_gold": 3200,
     "desc": "A ring of glowcap mushrooms and singing insects. Sleep here at your peril."},
    {"id": "waystone_elderroot",   "name": "Elderroot Hollow",     "continent": "daw_ul_talalu",
     "biome": "elderroot_hollow",   "activation_gold": 4000,
     "desc": "A hollow root the size of a temple. Only Sylvans and the initiated may pass its ward."},
]

WAYSTONES_BY_ID: dict[str, dict] = {w["id"]: w for w in WAYSTONES}


def waystones_for_continent(cont_id: str) -> list[dict]:
    return [w for w in WAYSTONES if w["continent"] == cont_id]


# ============================================================
# HOMELAND REPUTATION
# ============================================================
REP_LEVELS = ["hated", "hostile", "unfriendly", "neutral", "friendly", "honored", "exalted"]
# Cumulative thresholds (approximate WoW-style bands).
REP_THRESHOLDS = {
    "hated":       -6000,
    "hostile":     -3000,
    "unfriendly":  -1000,
    "neutral":     0,
    "friendly":    3000,
    "honored":     9000,
    "exalted":     21000,
}


def rep_level_from_points(points: int) -> str:
    lvl = "neutral"
    for name in REP_LEVELS:
        if points >= REP_THRESHOLDS[name]:
            lvl = name
    return lvl


def initial_reputation_for_race(race_id: str, home_continent: str, accessible_continents: list[str]) -> dict:
    """Native continent starts Friendly (3000 points); others start Neutral (0)."""
    out = {}
    for cont in accessible_continents:
        pts = REP_THRESHOLDS["friendly"] if cont == home_continent else 0
        out[cont] = {"points": pts, "level": rep_level_from_points(pts)}
    return out


def add_reputation(character: dict, continent_id: str, delta: int) -> tuple[str, str]:
    """Add reputation points on that continent; returns (new_level, old_level)."""
    rep = character.setdefault("reputation", {})
    entry = rep.setdefault(continent_id, {"points": 0, "level": "neutral"})
    old = entry["level"]
    entry["points"] = int(entry.get("points", 0)) + delta
    entry["level"] = rep_level_from_points(entry["points"])
    return entry["level"], old
