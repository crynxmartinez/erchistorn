"""Phase 2 game data — regions, towns, quests, events, racial extras."""
from __future__ import annotations


# ============================================================
# REGIONS (nested inside continents)
# ============================================================
REGIONS: list[dict] = [
    {
        "id": "vale_of_elder_kings",
        "name": "Vale of Elder Kings",
        "continent": "aetheria",
        "desc": "Sun-warmed valley cradling the old capital. Grasslands, oakwoods, and the founding town of the Empire.",
        "biomes": ["grasslands", "oakwood"],
        "town_ids": ["ironhold"],
    },
    {
        "id": "blackmoor_reach",
        "name": "Blackmoor Reach",
        "continent": "aetheria",
        "desc": "Where the rivers slow and the old kingdom ruins jut from the fog. Fewer travelers. More secrets.",
        "biomes": ["riverlands", "old_ruins"],
        "town_ids": ["willowmere"],
    },
]


# ============================================================
# TOWNS
# ============================================================
# services: subset of ["inn", "market", "trainers", "notice_board", "tavern", "alchemist"]
TOWNS: list[dict] = [
    {
        "id": "ironhold",
        "name": "Ironhold",
        "type": "forge_town",
        "region": "vale_of_elder_kings",
        "continent": "aetheria",
        "desc": "A soot-blackened town ringing with hammers. Ironhold's smiths forge armor for kings and killers alike.",
        "specialty": "Master Blacksmith — advanced weapon and armor recipes unlockable only here.",
        "services": ["inn", "market", "trainers", "notice_board", "tavern"],
        "inn_cost": 10,   # gold to rest
        "fast_travel_cost": 25,
        "market_items": ["iron_ore", "oak_log", "wild_herb", "bandage", "minor_healing_potion", "iron_dagger", "traveler_garb"],
        "trainer_ids": ["master_arden"],  # existing NPC from teachers
        "vendor_recipe_ids": ["craft_iron_dagger", "craft_iron_longsword", "craft_wolfbone_axe"],
    },
    {
        "id": "willowmere",
        "name": "Willowmere",
        "type": "sanctuary",
        "region": "blackmoor_reach",
        "continent": "aetheria",
        "desc": "A quiet town of white stone and willow trees. The priests of Willowmere heal any wound — for the right price.",
        "specialty": "Sanctuary — priests remove status effects instantly and train healing skills.",
        "services": ["inn", "market", "notice_board", "alchemist", "trainers"],
        "inn_cost": 15,
        "fast_travel_cost": 25,
        "market_items": ["wild_herb", "river_stone", "wisp_essence", "greater_healing_potion", "antidote", "bandage"],
        "trainer_ids": ["elder_lyria"],
        "vendor_recipe_ids": ["craft_minor_healing_potion", "craft_greater_healing_potion", "craft_antidote"],
    },
]

TOWNS_BY_ID: dict[str, dict] = {t["id"]: t for t in TOWNS}


# ============================================================
# QUESTS — Regional and Story quests (separate from daily missions)
# ============================================================
# category: regional | story | event
QUESTS: list[dict] = [
    # ---------- Regional (Aetheria) ----------
    {
        "id": "regional_wolf_menace",
        "category": "regional",
        "region": "vale_of_elder_kings",
        "title": "Wolf Menace",
        "giver": "ironhold_notice_board",
        "brief": "Wolves are terrorizing the outskirts. Ironhold's smiths post a bounty — slay 5 Gray Wolves and return.",
        "objectives": [{"kind": "kill", "id": "gray_wolf", "count": 5}],
        "reward": {"gold": 150, "xp": 120, "items": [("skillbook_ward", 0.15)]},  # (id, chance)
        "level_req": 1,
    },
    {
        "id": "regional_bandit_hunt",
        "category": "regional",
        "region": "vale_of_elder_kings",
        "title": "Bandit Hunt",
        "giver": "ironhold_notice_board",
        "brief": "Highway bandits prey on merchant caravans. Clear the roads — take down 4 Highway Bandits.",
        "objectives": [{"kind": "kill", "id": "highway_bandit", "count": 4}],
        "reward": {"gold": 220, "xp": 180},
        "level_req": 2,
    },
    {
        "id": "regional_herbal_relief",
        "category": "regional",
        "region": "blackmoor_reach",
        "title": "Herbal Relief",
        "giver": "willowmere_notice_board",
        "brief": "Willowmere's healers need herbs. Gather 12 Wild Herbs and deliver them.",
        "objectives": [{"kind": "gather", "id": "wild_herb", "count": 12}],
        "reward": {"gold": 130, "xp": 100, "items": [("greater_healing_potion", 1.0)]},
        "level_req": 1,
    },
    {
        "id": "regional_ruin_seeker",
        "category": "regional",
        "region": "blackmoor_reach",
        "title": "Ruin Seeker",
        "giver": "willowmere_notice_board",
        "brief": "Old kingdom relics are surfacing in the ruins. Complete 3 Loot Ruins expeditions.",
        "objectives": [{"kind": "action", "id": "loot_ruins", "count": 3}],
        "reward": {"gold": 260, "xp": 210},
        "level_req": 3,
    },

    # ---------- Story (main storyline) ----------
    {
        "id": "story_ch1_first_steps",
        "category": "story",
        "region": "vale_of_elder_kings",
        "title": "Chapter I — First Steps",
        "giver": "master_arden",
        "brief": "Ironhold's Master Arden asks you to prove yourself: slay a Grove Wisp and bring evidence.",
        "objectives": [{"kind": "kill", "id": "grove_wisp", "count": 1}],
        "reward": {"gold": 100, "xp": 150, "items": [("iron_longsword", 1.0)]},
        "level_req": 1,
    },
    {
        "id": "story_ch2_deeper_grove",
        "category": "story",
        "region": "vale_of_elder_kings",
        "title": "Chapter II — The Deeper Grove",
        "giver": "elder_lyria",
        "brief": "Elder Lyria feels an old presence stirring. Hunt 2 Feral Boars and 1 Ruin Ghast to lure it out.",
        "objectives": [
            {"kind": "kill", "id": "boar", "count": 2},
            {"kind": "kill", "id": "ruin_ghast", "count": 1},
        ],
        "reward": {"gold": 350, "xp": 280, "items": [("skillbook_purge", 1.0)]},
        "level_req": 4,
        "unlocked_by": "story_ch1_first_steps",
    },
]

QUESTS_BY_ID: dict[str, dict] = {q["id"]: q for q in QUESTS}


# ============================================================
# EVENTS — Weekly cycle
# ============================================================
# schedule_day: 0=Mon, 1=Tue, 2=Wed, 3=Thu, 4=Fri, 5=Sat, 6=Sun; -1 = always
EVENTS: list[dict] = [
    {
        "id": "event_world_boss_ancient_wisp",
        "name": "World Boss — The Ancient Wisp",
        "kind": "world_boss",
        "brief": "An Ancient Wisp of impossible age has awoken in the Elder Oakwood. All heroes of Erchis are called. Contribute damage; the top hunters share masterwork loot.",
        "schedule_days": [0],   # Monday
        "objectives": [{"kind": "kill", "id": "grove_wisp", "count": 8}],
        "reward": {"gold": 800, "xp": 600, "items": [("skillbook_thornlash", 1.0), ("relic_shard", 3)]},
        "level_req": 3,
    },
    {
        "id": "event_tournament_wolf_slayer",
        "name": "Tournament — Wolf Slayer",
        "kind": "tournament",
        "brief": "A weekly bracket. Slay 10 Gray Wolves before rivals do. The fastest claim glory and gold.",
        "schedule_days": [2],   # Wednesday
        "objectives": [{"kind": "kill", "id": "gray_wolf", "count": 10}],
        "reward": {"gold": 600, "xp": 400},
        "level_req": 1,
    },
    {
        "id": "event_festival_of_the_ledgers",
        "name": "Festival of the Ledgers",
        "kind": "festival",
        "brief": "Ironhold and Willowmere celebrate a founding festival. Craft 5 items and gather 15 materials to earn festival rewards.",
        "schedule_days": [5, 6],  # Sat-Sun
        "objectives": [
            {"kind": "craft", "count": 5},
            {"kind": "gather_any", "count": 15},
        ],
        "reward": {"gold": 500, "xp": 350, "items": [("jahra_ingot", 1.0)]},
        "level_req": 1,
    },
    {
        "id": "event_always_free_bounty",
        "name": "Standing Bounty — River Serpent",
        "kind": "bounty",
        "brief": "A standing bounty from Willowmere. Any hero who slays a River Serpent may claim it once per week.",
        "schedule_days": [-1],
        "objectives": [{"kind": "kill", "id": "river_serpent", "count": 1}],
        "reward": {"gold": 250, "xp": 180, "items": [("serpent_venom", 2)]},
        "level_req": 2,
    },
]

EVENTS_BY_ID: dict[str, dict] = {e["id"]: e for e in EVENTS}


# ============================================================
# BULLETIN — server announcements + world records
# ============================================================
STATIC_ANNOUNCEMENTS: list[dict] = [
    {
        "id": "welcome_v1",
        "kind": "system",
        "title": "Welcome to Erchis",
        "body": "The gates of Aetheria are open. Two towns stand ready: Ironhold for the forge, Willowmere for the priest's touch. May your dice be kind.",
    },
    {
        "id": "guilds_open",
        "kind": "system",
        "title": "Guilds Open in the Guild House",
        "body": "Create a guild for 5,000g. Recruit 3 members to unlock guild hall buffs. Rise to Grandmaster and claim your banner.",
    },
    {
        "id": "event_cycle",
        "kind": "system",
        "title": "Weekly Event Cycle",
        "body": "Monday — World Boss. Wednesday — Tournament. Weekend — Festival. Standing bounties are always live.",
    },
]


# ============================================================
# BEAST ASPECTS (Wildblood) + MARINE ADAPTATIONS (Hyliondrian)
# ============================================================
BEAST_ASPECTS: list[dict] = [
    {"id": "predator",  "name": "Predator",  "examples": "Wolf, Lion, Tiger, Shark",       "bonus_desc": "+3% damage vs wounded targets · +5% tracking success"},
    {"id": "swift",     "name": "Swift",     "examples": "Cat, Deer, Horse, Hare",         "bonus_desc": "+3% Evasion · -5% travel time"},
    {"id": "guardian",  "name": "Guardian",  "examples": "Bear, Boar, Ox, Rhino",          "bonus_desc": "+5% max HP · +3% defense when protecting others"},
    {"id": "keen_sense","name": "Keen-Sense","examples": "Eagle, Owl, Bat, Fox",           "bonus_desc": "+5% scouting · +5% ambush detection"},
    {"id": "venomous",  "name": "Venomous",  "examples": "Snake, Spider, Scorpion, Frog",  "bonus_desc": "Chance to poison on hit · +5% toxin crafting"},
]

MARINE_ADAPTATIONS: list[dict] = [
    {"id": "sharkborn", "name": "Sharkborn", "bonus_desc": "+3% damage vs bleeding · +5% hunt success"},
    {"id": "jelly_kin", "name": "Jelly-Kin", "bonus_desc": "+5% magic resistance · chance to shock melee attackers"},
    {"id": "eelborn",   "name": "Eelborn",   "bonus_desc": "+5% lightning resist · small chance to deal lightning"},
    {"id": "crab_kin",  "name": "Crab-Kin",  "bonus_desc": "+5% Armor Integrity · -2% Evasion"},
    {"id": "rayborn",   "name": "Rayborn",   "bonus_desc": "+5% water Evasion · +5% water travel speed"},
    {"id": "octo_kin",  "name": "Octo-Kin",  "bonus_desc": "+5% escape · +5% tool/trap disarm"},
]


# ============================================================
# HERITAGE RANK I — passive bonuses per race
# ============================================================
# Applied server-side to combat + action rolls; also shown in UI.
HERITAGE_RANK_1: dict[str, dict] = {
    "human": {
        "name": "Adaptable",
        "desc": "Once per day, may choose one specialization (+5% XP in that domain).",
        "resource": "oath_progress",
        "resource_max": 100,
        "resource_label": "Oath Progress",
    },
    "elf": {
        "name": "Child of the Sun and Moon",
        "desc": "Day: +5% healing received. Night: +3% Attack Success, +3% Evasion.",
        "resource": "celestial_charge",
        "resource_max": 5,
        "resource_label": "Celestial Charge",
    },
    "dwarf": {
        "name": "Mountain-Born",
        "desc": "+5% max Armor Integrity · -10% durability loss · +5% mining · +3% extra ore chance.",
        "resource": "stoneguard",
        "resource_max": 5,
        "resource_label": "Stoneguard",
    },
    "half_elf": {
        "name": "Chosen Heritage",
        "desc": "Inherits a diluted version of the chosen heritage's Rank I passive.",
        "resource": "harmony",
        "resource_max": 5,
        "resource_label": "Harmony",
    },
    "orc": {
        "name": "Blood of the Liberated",
        "desc": "HP < 30%: +5% physical damage, +5% resist fear, +5% resist control.",
        "resource": "defiance",
        "resource_max": 100,
        "resource_label": "Defiance",
    },
    "wildblood": {
        "name": "Beast Aspect",
        "desc": "One Beast Aspect chosen at creation. Grants unique passive traits.",
        "resource": "inner_blood",
        "resource_max": 100,
        "resource_label": "Inner Blood",
    },
    "hyliondrian": {
        "name": "Child of the Sea",
        "desc": "Underwater immunity · +10% water movement · +5% fishing/aquatic gather.",
        "resource": "tide",
        "resource_max": 5,
        "resource_label": "Tide",
    },
    "sylvan": {
        "name": "Shrink",
        "desc": "Toggle Shrunken Form: +5% Evasion, +10% stealth, -10% physical damage (10-min cooldown).",
        "resource": "verdant_essence",
        "resource_max": 5,
        "resource_label": "Verdant Essence",
    },
}


def get_town(town_id: str) -> dict | None:
    return TOWNS_BY_ID.get(town_id)


def get_region(region_id: str) -> dict | None:
    return next((r for r in REGIONS if r["id"] == region_id), None)


def get_quest(quest_id: str) -> dict | None:
    return QUESTS_BY_ID.get(quest_id)


def get_event(event_id: str) -> dict | None:
    return EVENTS_BY_ID.get(event_id)


def get_active_events(weekday: int) -> list[dict]:
    """Given today's weekday (0=Mon..6=Sun), return which events are active."""
    active = []
    for e in EVENTS:
        if -1 in e["schedule_days"] or weekday in e["schedule_days"]:
            active.append(e)
    return active


def default_home_town_for_race(race_id: str) -> str:
    """Race's starting town — for now, all Aetheria races start at Ironhold."""
    return "ironhold"
