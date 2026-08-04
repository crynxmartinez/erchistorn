"""Origins — 33 celestial birth Origins (3 per Mastery). Adds final bonus stats + drawback."""
from __future__ import annotations


# Each Origin has:
#   id, name, mastery, story, bonus (dict of stat->int), drawback (dict of stat->int),
#   best_for (str), mythicode_theme (str)
#
# Applicable stat keys:
#   vitality, cognition, essence, durability, might, grace, insight,
#   armor_bonus, evasion_mod, attack_success_mod

ORIGINS: list[dict] = [
    # ---------- KNIGHT ----------
    {"id": "guardians_shield", "name": "The Guardian's Shield", "mastery": "knight",
     "story": "Born under the constellation of the Bulwark. Chosen to protect.",
     "bonus": {"might": 3, "armor_bonus": 7}, "drawback": {"evasion_mod": -2},
     "best_for": "Heavy defense and protecting allies.", "mythicode": "Bulwark"},
    {"id": "iron_heart", "name": "The Iron Heart", "mastery": "knight",
     "story": "Forged in the Ember Furnace of the sky.",
     "bonus": {"vitality": 2, "might": 1}, "drawback": {"evasion_mod": -3},
     "best_for": "Health, endurance, and front-line survival.", "mythicode": "Furnace"},
    {"id": "gilded_scales", "name": "The Gilded Scales", "mastery": "knight",
     "story": "Justice-bearer of the Balanced Star.",
     "bonus": {"insight": 3, "essence": 3}, "drawback": {"might": -1},
     "best_for": "Leadership, justice, and magical defense.", "mythicode": "Balance"},

    # ---------- PALADIN ----------
    {"id": "radiant_heart", "name": "The Radiant Heart", "mastery": "paladin",
     "story": "Born beneath a solar eclipse — carrier of holy light.",
     "bonus": {"essence": 3, "attack_success_mod": 2}, "drawback": {"armor_bonus": -6},
     "best_for": "Healing, holy attacks, and accuracy.", "mythicode": "Radiance"},
    {"id": "eternal_gate", "name": "The Eternal Gate", "mastery": "paladin",
     "story": "Keeper of thresholds between world and spirit.",
     "bonus": {"vitality": 3, "essence": 2}, "drawback": {"might": -2},
     "best_for": "Defensive and healing Paladins.", "mythicode": "Threshold"},
    {"id": "celestial_archer", "name": "The Celestial Archer", "mastery": "paladin",
     "story": "Marked at birth by a comet's tail.",
     "bonus": {"grace": 3, "insight": 2}, "drawback": {"essence": -1},
     "best_for": "Fast and accurate Paladins.", "mythicode": "Arrow"},

    # ---------- LANCER ----------
    {"id": "silvered_wolf", "name": "The Silvered Wolf", "mastery": "lancer",
     "story": "Bound to the Wolfstar — swift and cunning.",
     "bonus": {"grace": 3, "insight": 2}, "drawback": {"durability": -1},
     "best_for": "Speed, accuracy, and instinct.", "mythicode": "Wolfstar"},
    {"id": "frosted_peak", "name": "The Frosted Peak", "mastery": "lancer",
     "story": "Born in the shadow of the Mountain That Never Melts.",
     "bonus": {"might": 3, "vitality": 2}, "drawback": {"cognition": -2},
     "best_for": "Heavy attacks and physical endurance.", "mythicode": "Peak"},
    {"id": "shattered_blade", "name": "The Shattered Blade", "mastery": "lancer",
     "story": "Wielder of a broken star — deals more, receives more.",
     "bonus": {"grace": 2, "might": 3}, "drawback": {"armor_bonus": -6},
     "best_for": "High-damage and high-risk combat.", "mythicode": "Shatter"},

    # ---------- ASSASSIN ----------
    {"id": "shrouded_shadow", "name": "The Shrouded Shadow", "mastery": "assassin",
     "story": "Born in the darkest hour of a new moon.",
     "bonus": {"grace": 3, "evasion_mod": 2}, "drawback": {"vitality": -1},
     "best_for": "Stealth and avoiding attacks.", "mythicode": "Umbra"},
    {"id": "whispering_wind", "name": "The Whispering Wind", "mastery": "assassin",
     "story": "The stars whispered their name at birth — unhearable, unheard.",
     "bonus": {"grace": 3, "evasion_mod": 2}, "drawback": {"armor_bonus": -7},
     "best_for": "Extreme speed and evasive combat.", "mythicode": "Whisper"},
    {"id": "serpents_coil", "name": "The Serpent's Coil", "mastery": "assassin",
     "story": "Marked by the Coiled Constellation — venom and precision.",
     "bonus": {"grace": 3, "evasion_mod": 2}, "drawback": {"essence": -1},
     "best_for": "Poison, precision, and transformation.", "mythicode": "Serpent"},

    # ---------- ROGUE ----------
    {"id": "obsidian_dagger", "name": "The Obsidian Dagger", "mastery": "rogue",
     "story": "Born under a black-star omen — sudden, sharp, decisive.",
     "bonus": {"grace": 3, "might": 2}, "drawback": {"essence": -2},
     "best_for": "Aggressive Rogues and ambush combat.", "mythicode": "Obsidian"},
    {"id": "hidden_cove", "name": "The Hidden Cove", "mastery": "rogue",
     "story": "The stars formed a sheltered inlet at the hour of their birth.",
     "bonus": {"evasion_mod": 2, "grace": 2}, "drawback": {"insight": -1},
     "best_for": "Escaping, hiding, and exploration.", "mythicode": "Cove"},
    {"id": "veiled_maiden", "name": "The Veiled Maiden", "mastery": "rogue",
     "story": "Under the Veil, all faces are false — and true.",
     "bonus": {"grace": 3, "insight": 3}, "drawback": {"vitality": -2},
     "best_for": "Deception, diplomacy, and clever actions.", "mythicode": "Veil"},

    # ---------- HUNTER ----------
    {"id": "verdant_grove", "name": "The Verdant Grove", "mastery": "hunter",
     "story": "Grown from the Greenstar — friend of wild things.",
     "bonus": {"essence": 2, "vitality": 1}, "drawback": {"might": -1},
     "best_for": "Nature abilities and animal companions.", "mythicode": "Greenstar"},
    {"id": "ember_hawk", "name": "The Ember Hawk", "mastery": "hunter",
     "story": "A hawk of flame led their birth — sharp-eyed and swift.",
     "bonus": {"grace": 3, "insight": 2}, "drawback": {"vitality": -1},
     "best_for": "Ranged accuracy and scouting.", "mythicode": "Hawk"},
    {"id": "howling_beast", "name": "The Howling Beast", "mastery": "hunter",
     "story": "The Beast-star howled at their first breath.",
     "bonus": {"might": 3, "vitality": 2}, "drawback": {"cognition": -2},
     "best_for": "Aggressive hunters and powerful companions.", "mythicode": "Howl"},

    # ---------- DRUID ----------
    {"id": "ancient_oak", "name": "The Ancient Oak", "mastery": "druid",
     "story": "Rooted under the Oakstar — old, patient, deep.",
     "bonus": {"vitality": 2, "essence": 2}, "drawback": {"grace": -2},
     "best_for": "Durability, healing, and defensive nature magic.", "mythicode": "Oak"},
    {"id": "verdant_harvester", "name": "The Verdant Harvester", "mastery": "druid",
     "story": "Born at harvest — hands blessed by the wild bounty.",
     "bonus": {"vitality": 3, "grace": 2}, "drawback": {"insight": -1},
     "best_for": "Gathering, survival, and mobile nature builds.", "mythicode": "Harvest"},
    {"id": "winding_stream", "name": "The Winding Stream", "mastery": "druid",
     "story": "The Riverstar bent for them — flowing, adapting, never still.",
     "bonus": {"grace": 2, "evasion_mod": 1}, "drawback": {"might": -2},
     "best_for": "Mobility, adaptation, and water-based Druids.", "mythicode": "Stream"},

    # ---------- PRIEST ----------
    {"id": "luminous_codex", "name": "The Luminous Codex", "mastery": "priest",
     "story": "Scribe of the star-libraries — carrier of forbidden knowledge.",
     "bonus": {"cognition": 5, "essence": 1}, "drawback": {"vitality": -1},
     "best_for": "Knowledge, rituals, and mental defense.", "mythicode": "Codex"},
    {"id": "crystal_lotus", "name": "The Crystal Lotus", "mastery": "priest",
     "story": "The Lotus of Light bloomed at their birth.",
     "bonus": {"essence": 3, "vitality": 2}, "drawback": {"evasion_mod": -3},
     "best_for": "Healing and spiritual resilience.", "mythicode": "Lotus"},
    {"id": "twilight_gate", "name": "The Twilight Gate", "mastery": "priest",
     "story": "Born between light and dark — walker of the boundary.",
     "bonus": {"insight": 3, "evasion_mod": 2}, "drawback": {"armor_bonus": -6},
     "best_for": "Spirit magic and mobile support.", "mythicode": "Twilight"},

    # ---------- MAGE ----------
    {"id": "arcane_spiral", "name": "The Arcane Spiral", "mastery": "mage",
     "story": "Bound to the endless spiral of raw magic.",
     "bonus": {"essence": 2, "cognition": 1}, "drawback": {"vitality": -1},
     "best_for": "General spellcasting and magical power.", "mythicode": "Spiral"},
    {"id": "cosmic_loom", "name": "The Cosmic Loom", "mastery": "mage",
     "story": "A weaver-star charted every thread of their fate.",
     "bonus": {"cognition": 3, "insight": 3}, "drawback": {"might": -2},
     "best_for": "Powerful magic, rituals, and investigation.", "mythicode": "Loom"},
    {"id": "opal_gate", "name": "The Opal Gate", "mastery": "mage",
     "story": "The Opalstar cracked at their birth — hinting at portals unseen.",
     "bonus": {"essence": 2, "cognition": 1}, "drawback": {"might": -2},
     "best_for": "Portals, hidden knowledge, and dimensional magic.", "mythicode": "Opal"},

    # ---------- BARD ----------
    {"id": "golden_harp", "name": "The Golden Harp", "mastery": "bard",
     "story": "The Harpstar sang at their first cry.",
     "bonus": {"grace": 3, "insight": 2}, "drawback": {"might": -1},
     "best_for": "Music, buffs, and social abilities.", "mythicode": "Harp"},
    {"id": "wandering_minstrel", "name": "The Wandering Minstrel", "mastery": "bard",
     "story": "The Wander-star pulls them ever forward.",
     "bonus": {"grace": 2, "cognition": 1}, "drawback": {"vitality": -1},
     "best_for": "Travel, storytelling, and exploration.", "mythicode": "Wander"},
    {"id": "dancers_grace", "name": "The Dancer's Grace", "mastery": "bard",
     "story": "Born to the rhythm of the spinning stars.",
     "bonus": {"grace": 5, "evasion_mod": 1}, "drawback": {"might": -2},
     "best_for": "Extreme mobility, performance, and Evasion.", "mythicode": "Dance"},

    # ---------- ALCHEMIST ----------
    {"id": "tempests_eye", "name": "The Tempest's Eye", "mastery": "alchemist",
     "story": "Born at the storm's center — calm within chaos.",
     "bonus": {"evasion_mod": 3, "insight": 2}, "drawback": {"vitality": -1},
     "best_for": "Bombs, elemental mixtures, and mobile Alchemists.", "mythicode": "Tempest"},
    {"id": "pierced_heart", "name": "The Pierced Heart", "mastery": "alchemist",
     "story": "The Heartstar was speared at their birth — life given for knowledge.",
     "bonus": {"essence": 3, "vitality": 2}, "drawback": {"armor_bonus": -6},
     "best_for": "Life transmutation, healing potions, and risky experiments.", "mythicode": "Pierce"},
    {"id": "navigators_star", "name": "The Navigator's Star", "mastery": "alchemist",
     "story": "Guide-star of the questing spirit.",
     "bonus": {"insight": 3, "durability": 1}, "drawback": {"evasion_mod": -2},
     "best_for": "Discovery, crafting, and exploration.", "mythicode": "Navigator"},
]

ORIGINS_BY_ID: dict[str, dict] = {o["id"]: o for o in ORIGINS}


def origins_for_mastery(mastery_id: str) -> list[dict]:
    return [o for o in ORIGINS if o["mastery"] == mastery_id]


def get_origin(origin_id: str) -> dict | None:
    return ORIGINS_BY_ID.get(origin_id)


# ============================================================
# ROLE/MASTERY MAIN STAT DATA (per new spec)
# ============================================================
# Role total: 10 Main Stat points (Might/Grace/Insight)
ROLE_MAIN_STATS: dict[str, dict] = {
    "fighter":  {"might": 6, "grace": 2, "insight": 2},
    "guardian": {"might": 5, "grace": 3, "insight": 2},
    "scout":    {"might": 3, "grace": 4, "insight": 3},
    "scholar":  {"might": 2, "grace": 2, "insight": 6},
    "healer":   {"might": 2, "grace": 3, "insight": 5},
}

# Mastery total: +5 Main Stat points
MASTERY_MAIN_STATS: dict[str, dict] = {
    "knight":    {"might": 3, "grace": 1, "insight": 1},
    "paladin":   {"might": 2, "grace": 1, "insight": 2},
    "lancer":    {"might": 3, "grace": 2, "insight": 0},
    "assassin":  {"might": 1, "grace": 3, "insight": 1},
    "rogue":     {"might": 1, "grace": 3, "insight": 1},
    "hunter":    {"might": 2, "grace": 2, "insight": 1},
    "druid":     {"might": 1, "grace": 1, "insight": 3},
    "priest":    {"might": 0, "grace": 2, "insight": 3},
    "mage":      {"might": 0, "grace": 2, "insight": 3},
    "bard":      {"might": 1, "grace": 2, "insight": 2},
    "alchemist": {"might": 1, "grace": 1, "insight": 3},
}

# Role → available Masteries (new spec)
ROLE_AVAILABLE_MASTERIES: dict[str, list[str]] = {
    "fighter":  ["knight", "paladin", "lancer", "assassin"],
    "guardian": ["knight", "paladin", "druid"],
    "scout":    ["lancer", "assassin", "rogue", "hunter"],
    "scholar":  ["druid", "mage", "bard", "alchemist"],
    "healer":   ["paladin", "druid", "priest", "bard", "alchemist"],
}


def compute_final_stats(race_life_stats: dict, role_id: str, mastery_id: str, origin_id: str | None) -> dict:
    """Layer Race + Role + Mastery + Origin. Applies min-1 rule."""
    stats = {
        "vitality":            int(race_life_stats.get("vitality", 3)),
        "cognition":           int(race_life_stats.get("cognition", 3)),
        "essence":             int(race_life_stats.get("essence", 3)),
        "durability":           int(race_life_stats.get("durability", 3)),
        "might":               0,
        "grace":               0,
        "insight":             0,
        # `resilience` feeds armor (game_data.compute_armor) and `magic_resist`
        # carries gear MR. Neither key existed here, so the Guardian role's
        # declared "+2 Resilience" had nowhere to land and was silently dropped.
        "resilience":          0,
        "magic_resist":        0,
        "armor_bonus":         0,
        "evasion_mod":         0,
        "attack_success_mod":  0,
    }
    # Role — main-stat allocation (might/grace/insight)
    role_stats = ROLE_MAIN_STATS.get(role_id, {})
    for k, v in role_stats.items():
        stats[k] += v

    # Role — the flat `bonus` declared on ROLES.
    #
    # This was never read by anything. All five roles advertise a stat bonus in
    # their own description ("Front-line combatant. +2 Vitality", "Defender and
    # protector. +2 Resilience", ...) and not one of them was granted:
    #   fighter +2 vitality · guardian +2 resilience · scout +2 grace
    #   scholar +2 cognition · healer +2 essence
    from game_data import ROLES as _ROLES
    role_def = next((r for r in _ROLES if r["id"] == role_id), None)
    role_bonus = dict((role_def or {}).get("bonus") or {})
    for k, v in role_bonus.items():
        stats[k] = stats.get(k, 0) + v
    # Mastery
    mastery_stats = MASTERY_MAIN_STATS.get(mastery_id, {})
    for k, v in mastery_stats.items():
        stats[k] += v
    # Origin
    breakdown = {
        "race": dict(race_life_stats),
        "role": {**role_stats, **role_bonus},
        "mastery": mastery_stats,
        "origin_bonus": {},
        "origin_drawback": {},
    }
    if origin_id:
        origin = get_origin(origin_id)
        if origin:
            for k, v in origin.get("bonus", {}).items():
                stats[k] = stats.get(k, 0) + v
                breakdown["origin_bonus"][k] = v
            for k, v in origin.get("drawback", {}).items():
                stats[k] = stats.get(k, 0) + v
                breakdown["origin_drawback"][k] = v

    # Minimum-1 rule for Life & Main stats
    for k in ("vitality", "cognition", "essence", "durability", "might", "grace", "insight"):
        if stats[k] < 1:
            stats[k] = 1
    # Armor cannot fall below 0
    if stats["armor_bonus"] < 0:
        # Keep it — armor_bonus IS a modifier that can be negative in the model,
        # but display floor is 0. We'll expose both.
        pass
    return {"stats": stats, "breakdown": breakdown}
