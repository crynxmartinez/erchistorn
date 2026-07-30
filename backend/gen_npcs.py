"""Auto-generated NPC + Quest data.

Generates 4-5 NPCs per town (62 new NPCs) with ~20 quests each,
totalling ~1240 new quests.  Quest types:
  - chain (3-5 per NPC): relationship-gated story arcs with unique item rewards
  - bounty (8-10 per NPC): repeatable kill/gather quests
  - story (5-8 per NPC): level-gated one-shot quests with rare rewards

Imported by npcs.py at module load time.
"""
from __future__ import annotations

from world_data import CONTINENTS_V2

# ============================================================
# DATA MAPS
# ============================================================

# Town -> continent
TOWN_CONTINENT: dict[str, str] = {
    "oathspire": "valeria",
    "riverguard": "valeria",
    "grunhold": "mushkara",
    "warforge": "mushkara",
    "elaris": "concordia",
    "silvergate": "concordia",
    "jahrahold": "khardrum",
    "deepstone": "khardrum",
    "solunara": "haya",
    "starfall_watch": "haya",
    "rindivar_grove": "gennel",
    "beastcairn": "gennel",
    "atlantyrion": "hylion",
    "veilgrove": "daw_ul_talalu",
}

# Town -> (display name, type desc)
TOWN_META: dict[str, tuple[str, str]] = {
    "oathspire": ("Oathspire", "imperial capital"),
    "riverguard": ("Riverguard", "river sanctuary"),
    "grunhold": ("Grunhold", "orc warhold"),
    "warforge": ("Warforge", "war outpost"),
    "elaris": ("Elaris", "federation capital"),
    "silvergate": ("Silvergate", "caravan hub"),
    "jahrahold": ("Jahrahold", "dwarven undermountain hall"),
    "deepstone": ("Deepstone", "frontier watch"),
    "solunara": ("Solunara", "elven sky city"),
    "starfall_watch": ("Starfall Watch", "sky watchtower"),
    "rindivar_grove": ("Rindivar Grove", "wildblood grove"),
    "beastcairn": ("Beastcairn", "nomad camp"),
    "atlantyrion": ("Atlantyrion", "undersea capital"),
    "veilgrove": ("Veilgrove", "sylvan tree-city"),
}

# Continent -> home race
CONTINENT_RACE: dict[str, str] = {
    "valeria": "human",
    "mushkara": "orc",
    "concordia": "half_elf",
    "khardrum": "dwarf",
    "haya": "elf",
    "gennel": "wildblood",
    "hylion": "hyliondrian",
    "daw_ul_talalu": "sylvan",
}

# Build biome -> continent map from CONTINENTS_V2
BIOME_CONTINENT: dict[str, str] = {}
CONTINENT_BIOMES: dict[str, list[str]] = {}
for _c in CONTINENTS_V2:
    if _c.get("locked"):
        continue
    cid = _c["id"]
    bids = [b["id"] for b in _c.get("biomes", [])]
    CONTINENT_BIOMES[cid] = bids
    for bid in bids:
        BIOME_CONTINENT[bid] = cid


def _build_monster_index():
    """Return biome_id -> list of (monster_id, monster_name, rarity, power)."""
    from game_data import MONSTERS
    idx: dict[str, list[tuple[str, str, str, int]]] = {}
    for m in MONSTERS:
        bid = m.get("biome", "")
        if not bid:
            continue
        idx.setdefault(bid, []).append((
            m["id"], m["name"], m.get("rarity", "common"), m.get("power", 1),
        ))
    return idx


def _build_item_index():
    """Return biome_id -> list of (item_id, item_name, kind, rarity)."""
    from game_data import ITEMS
    idx: dict[str, list[tuple[str, str, str, str]]] = {}
    for it in ITEMS:
        for bid in it.get("biome_gather", []) or []:
            idx.setdefault(bid, []).append((
                it["id"], it["name"], it.get("kind", "material"), it.get("rarity", "common"),
            ))
        for bid in it.get("biome_fish", []) or []:
            idx.setdefault(bid, []).append((
                it["id"], it["name"], "fish", it.get("rarity", "common"),
            ))
    return idx


# ============================================================
# NPC ROLE TEMPLATES
# ============================================================

# Each town gets NPCs in these roles (skipping flagship which already exists where applicable)
NPC_ROLES: list[dict] = [
    {
        "role": "veteran",
        "title_templates": [
            "Veteran Hunter of {town}",
            "Retired Sargent of {town}",
            "Beast-Slayer of {town}",
            "War Veteran of {town}",
            "Frontier Scout of {town}",
        ],
        "name_pools": [
            ("Sergeant", "Bren", "human"), ("Captain", "Roric", "human"),
            ("Hunter", "Kael", "human"), ("Scout", "Mira", "human"),
            ("Veteran", "Dorn", "human"), ("Sergeant", "Vrag", "orc"),
            ("Hunter", "Grath", "orc"), ("Scout", "Nasha", "orc"),
            ("Veteran", "Torin", "dwarf"), ("Hunter", "Helga", "dwarf"),
            ("Captain", "Aelric", "half_elf"), ("Scout", "Lyra", "half_elf"),
            ("Hunter", "Silas", "elf"), ("Veteran", "Thaniel", "elf"),
            ("Tracker", "Ryk", "wildblood"), ("Huntress", "Sera", "wildblood"),
            ("Tideguard", "Corin", "hyliondrian"), ("Reefhunter", "Vash", "hyliondrian"),
            ("Warden", "Fenrick", "sylvan"), ("Thornhunter", "Pip", "sylvan"),
        ],
        "personalities": [
            "Grim. Watches the treeline. Talks only about what's out there.",
            "Blunt. Counts scars like coins. Pays well for proof of kills.",
            "Quiet. Hands shake unless holding a weapon. Good teacher.",
            "Loud. Laughs at danger. Buys drinks for anyone who brings back trophies.",
            "Cold. Eyes like a hawk. Never misses a track.",
        ],
        "desc_templates": [
            "A seasoned fighter who knows every beast in the region by its tracks. "
            "Pays good coin for proof of kills.",
            "Retired from the garrison but still hunts every dawn. Knows the land "
            "better than any map.",
            "Lost a squad to the wilds and never stopped hunting since. Trains "
            "newcomers who prove their mettle.",
        ],
    },
    {
        "role": "gatherer",
        "title_templates": [
            "Master Gatherer of {town}",
            "Herbalist of {town}",
            "Forager of {town}",
            "Field Collector of {town}",
            "Wildcrafter of {town}",
        ],
        "name_pools": [
            ("Herbalist", "Senna", "human"), ("Gatherer", "Old Tom", "human"),
            ("Forager", "Bram", "human"), ("Wildcrafter", "Dahlia", "human"),
            ("Collector", "Rina", "half_elf"), ("Herbalist", "Fenwick", "half_elf"),
            ("Forager", "Thistle", "elf"), ("Gatherer", "Yavanna", "elf"),
            ("Miner", "Grimdar", "dwarf"), ("Excavator", "Brunn", "dwarf"),
            ("Forager", "Grish", "orc"), ("Scavenger", "Uruk", "orc"),
            ("Tracker", "Nim", "wildblood"), ("Forager", "Bramble", "wildblood"),
            ("Tidegatherer", "Shell", "hyliondrian"), ("Pearldiver", "Coral", "hyliondrian"),
            ("Rootweaver", "Moss", "sylvan"), ("Bloomkeeper", "Petal", "sylvan"),
        ],
        "personalities": [
            "Patient. Knows every plant by smell. Hates waste.",
            "Cheerful. Talks to plants. They talk back, sometimes.",
            "Practical. Weighs everything. Pays by the bundle.",
            "Dreamy. Mixes facts with folklore. Always right about the herbs, though.",
            "Gruff. Hands like bark. Heart like a warm root cellar.",
        ],
        "desc_templates": [
            "Knows every herb, stone, and fish in the region. Pays fair prices "
            "for fresh materials delivered in bulk.",
            "A master of wildcraft who can name every plant by touch. Always "
            "looking for reliable gatherers.",
            "Keeps the town supplied with raw materials. Has a list of needs "
            "that never seems to get shorter.",
        ],
    },
    {
        "role": "merchant",
        "title_templates": [
            "Trade Broker of {town}",
            "Caravan Master of {town}",
            "Merchant of {town}",
            "Supply Contractor of {town}",
            "Import Broker of {town}",
        ],
        "name_pools": [
            ("Broker", "Vance", "human"), ("Merchant", "Olivia", "human"),
            ("Trader", "Pierre", "human"), ("Contractor", "Harsk", "human"),
            ("Broker", "Elara", "half_elf"), ("Merchant", "Dario", "half_elf"),
            ("Trader", "Finwen", "elf"), ("Broker", "Calen", "elf"),
            ("Smith-Broker", "Durgan", "dwarf"), ("Trader", "Bryn", "dwarf"),
            ("War-Broker", "Krug", "orc"), ("Supplier", "Gash", "orc"),
            ("Pack-Master", "Reef", "wildblood"), ("Trader", "Sah", "wildblood"),
            ("Pearl-Broker", "Maris", "hyliondrian"), ("Tide-Merchant", "Kai", "hyliondrian"),
            ("Grove-Broker", "Lichen", "sylvan"), ("Petal-Merchant", "Bloom", "sylvan"),
        ],
        "personalities": [
            "Smooth. Counts coins faster than words. Always has a deal.",
            "Shrewd. Drives a hard bargain but never cheats. Respects results.",
            "Charming. Remembers every name. Forgets every debt.",
            "Nervous. Checks the roads twice. Pays extra for safe deliveries.",
            "Generous. Tips well. Expects loyalty in return.",
        ],
        "desc_templates": [
            "Handles the town's trade contracts. Always needs someone to deal "
            "with problems on the road — bandits, beasts, and worse.",
            "A well-connected broker who moves goods across the continent. "
            "Pays well for trouble-shooting and delivery work.",
            "Runs the supply chain for the town. If something's blocking the "
            "roads or scaring off the caravans, it's their problem — and yours.",
        ],
    },
    {
        "role": "mystic",
        "title_templates": [
            "Lorekeeper of {town}",
            "Scholar of {town}",
            "Mystic of {town}",
            "Arcanist of {town}",
            "Sage of {town}",
        ],
        "name_pools": [
            ("Sage", "Aldus", "human"), ("Scholar", "Wren", "human"),
            ("Lorekeeper", "Faye", "half_elf"), ("Arcanist", "Pell", "half_elf"),
            ("Mystic", "Sienna", "elf"), ("Lorekeeper", "Orin", "elf"),
            ("Runesmith", "Kaldar", "dwarf"), ("Scholar", "Dust", "dwarf"),
            ("Shaman", "Gorak", "orc"), ("Spirit-Talker", "Vraal", "orc"),
            ("Seer", "Leaf", "wildblood"), ("Bone-Reader", "Ash", "wildblood"),
            ("Tide-Sage", "Marlow", "hyliondrian"), ("Deep-Scholar", "Reef", "hyliondrian"),
            ("Mist-Sage", "Willow", "sylvan"), ("Dream-Keeper", "Hush", "sylvan"),
        ],
        "personalities": [
            "Cryptic. Answers questions with older questions. Knows everything.",
            "Eccentric. Mutters to invisible companions. Surprisingly accurate.",
            "Calm. Speaks slowly. Never wrong, never in a hurry.",
            "Intense. Eyes burn with curiosity. Pays for knowledge, not just kills.",
            "Gentle. Smells of old books. Terrifying when angry.",
        ],
        "desc_templates": [
            "A keeper of old knowledge who studies the region's creatures and "
            "ruins. Pays well for samples and exploration reports.",
            "Researches the magical and mundane ecology of the area. Always "
            "needs fieldwork done — and someone to do it safely.",
            "An eccentric scholar with theories about everything. Some are mad. "
            "The ones that aren't pay extremely well.",
        ],
    },
    {
        "role": "guard",
        "title_templates": [
            "Town Guard Captain of {town}",
            "Watch Commander of {town}",
            "Patrol Leader of {town}",
            "Constable of {town}",
            "Sentinel of {town}",
        ],
        "name_pools": [
            ("Captain", "Hale", "human"), ("Commander", "Jorin", "human"),
            ("Constable", "Bea", "human"), ("Sentinel", "Garreth", "human"),
            ("Captain", "Ruk", "orc"), ("Commander", "Thraz", "orc"),
            ("Guard-Captain", "Baldar", "dwarf"), ("Sentinel", "Sten", "dwarf"),
            ("Commander", "Caelis", "half_elf"), ("Constable", "Mira", "half_elf"),
            ("Sentinel", "Faen", "elf"), ("Captain", "Lorien", "elf"),
            ("Pack-Sentinel", "Fang", "wildblood"), ("Watch-Leader", "Cub", "wildblood"),
            ("Reef-Sentinel", "Tide", "hyliondrian"), ("Captain", "Swell", "hyliondrian"),
            ("Thorn-Sentinel", "Burr", "sylvan"), ("Mist-Watch", "Glimmer", "sylvan"),
        ],
        "personalities": [
            "Stoic. Does the job. Doesn't complain. Respects the same.",
            "Tired. Too many threats, not enough hands. Grateful for help.",
            "Strict. Follows the letter of the law. Fair, though.",
            "Watchful. Sleeps with one eye open. Trusts few, rewards loyalty.",
            "Gruff but kind. Feeds the recruits first. Fights last.",
        ],
        "desc_templates": [
            "Commands the town guard and handles threats that come too close "
            "to the walls. Always needs capable hands for patrol work.",
            "Keeps the peace in town and the roads clear nearby. Posts bounties "
            "for anything that threatens the supply lines.",
            "A career soldier who runs the watch. Has seen everything and "
            "expects the worst — but rewards those who deliver.",
        ],
    },
]


# ============================================================
# QUEST GENERATION
# ============================================================

# Reward scaling by relationship tier
TIER_REWARDS: dict[str, dict] = {
    "stranger":    {"gold": (80, 150),   "xp": (60, 120),    "rel": 220},
    "acquainted":  {"gold": (200, 400),  "xp": (150, 280),   "rel": 420},
    "friend":      {"gold": (500, 900),  "xp": (350, 600),   "rel": 600},
    "trusted":     {"gold": (1000, 1800),"xp": (700, 1200),  "rel": 800},
    "bonded":      {"gold": (2000, 3500),"xp": (1400, 2400), "rel": 1000},
}

# Level requirements by tier
TIER_LEVEL: dict[str, int] = {
    "stranger": 1, "acquainted": 5, "friend": 12, "trusted": 25, "bonded": 40,
}

# Unique item templates by role and tier
UNIQUE_ITEMS: dict[str, dict[str, dict]] = {
    "veteran": {
        "friend": {"id": "veteran_blade_{town}", "name": "{Town} Veteran's Blade",
                   "rarity": "rare", "kind": "weapon", "power": 12, "slot": "right_hand"},
        "trusted": {"id": "veteran_greatblade_{town}", "name": "{Town} Master's Greatblade",
                    "rarity": "epic", "kind": "weapon", "power": 20, "slot": "right_hand"},
        "bonded": {"id": "veteran_legendary_{town}", "name": "Legend of {Town}",
                   "rarity": "legendary", "kind": "weapon", "power": 30, "slot": "right_hand"},
    },
    "gatherer": {
        "friend": {"id": "gatherer_satchel_{town}", "name": "{Town} Gatherer's Satchel",
                   "rarity": "rare", "kind": "relic", "power": 0},
        "trusted": {"id": "gatherer_tools_{town}", "name": "Master's Gathering Tools of {Town}",
                    "rarity": "epic", "kind": "relic", "power": 0},
        "bonded": {"id": "gatherer_crown_{town}", "name": "Wildcrafter's Crown of {Town}",
                   "rarity": "legendary", "kind": "relic", "power": 0},
    },
    "merchant": {
        "friend": {"id": "merchant_ring_{town}", "name": "{Town} Broker's Ring",
                   "rarity": "rare", "kind": "relic", "power": 0},
        "trusted": {"id": "merchant_amulet_{town}", "name": "Trade Amulet of {Town}",
                    "rarity": "epic", "kind": "relic", "power": 0},
        "bonded": {"id": "merchant_scepter_{town}", "name": "Golden Scepter of {Town}",
                   "rarity": "legendary", "kind": "relic", "power": 0},
    },
    "mystic": {
        "friend": {"id": "mystic_charm_{town}", "name": "{Town} Mystic's Charm",
                   "rarity": "rare", "kind": "relic", "power": 0},
        "trusted": {"id": "mystic_staff_{town}", "name": "Arcane Staff of {Town}",
                    "rarity": "epic", "kind": "weapon", "power": 18, "slot": "right_hand"},
        "bonded": {"id": "mystic_orb_{town}", "name": "Oracle's Orb of {Town}",
                   "rarity": "legendary", "kind": "relic", "power": 0},
    },
    "guard": {
        "friend": {"id": "guard_shield_{town}", "name": "{Town} Sentinel's Shield",
                   "rarity": "rare", "kind": "armor", "power": 10, "slot": "left_hand"},
        "trusted": {"id": "guard_armor_{town}", "name": "Captain's Plate of {Town}",
                    "rarity": "epic", "kind": "armor", "power": 18, "slot": "body"},
        "bonded": {"id": "guard_helm_{town}", "name": "Warden's Helm of {Town}",
                   "rarity": "legendary", "kind": "armor", "power": 25, "slot": "head"},
    },
}

# Chain quest narrative templates by role
CHAIN_NARRATIVES: dict[str, list[dict]] = {
    "veteran": [
        {"tier": "stranger", "order": 1,
         "name": "First Blood",
         "brief": "Prove you can fight. Bring down {count} {monster} from the {biome}.",
         "accept": "'Fresh face. Fresh blade. Let's see if either holds up. {count} {monster}. Go.'",
         "complete": "'Not bad. Blade's still sharp. So are you. Come back when you want real work.'"},
        {"tier": "acquainted", "order": 2,
         "name": "The Hunt Deepens",
         "brief": "Something tougher this time. {count} {monster} — they're no joke.",
         "accept": "'You've got the basics. Now the hard part. {count} {monster}. Don't come back empty.'",
         "complete": "'You're still standing. That's more than most manage. I'm starting to like you.'"},
        {"tier": "friend", "order": 3,
         "name": "The Trophy",
         "brief": "I want a real trophy. {count} {monster} — the kind that makes legends.",
         "accept": "'This one separates hunters from legends. {count} {monster}. Bring me proof.'",
         "complete": "'Look at that. Beautiful. You've earned this — and my respect.'"},
        {"tier": "trusted", "order": 4,
         "name": "The Old Enemy",
         "brief": "There's a beast that's been killing my people for years. End it.",
         "accept": "'I've lost three squads to this thing. You're the first I've sent who might actually come back.'",
         "complete": "'It's done. I can sleep now. Take this — it's been waiting for a hand worthy of it.'"},
        {"tier": "bonded", "order": 5,
         "name": "The Final Hunt",
         "brief": "One last hunt. The biggest, the worst, the one they sing songs about.",
         "accept": "'You and me, we've spilled enough blood to fill a river. One more. The biggest.'",
         "complete": "'It's over. You're the best I've ever trained. This is yours — earned, not given.'"},
    ],
    "gatherer": [
        {"tier": "stranger", "order": 1,
         "name": "First Harvest",
         "brief": "Bring me {count} {item}. Fresh, not bruised.",
         "accept": "'Start simple. {count} {item}. Don't waste any.'",
         "complete": "'Good quality. You know how to pick without ruining the root. Come back.'"},
        {"tier": "acquainted", "order": 2,
         "name": "The Rare Find",
         "brief": "I need {count} {item}. They're harder to find, but you can manage.",
         "accept": "'{count} {item}. Not common, but not impossible. Mind the wildlife.'",
         "complete": "'Excellent specimens. You have a gift. Let me teach you more.'"},
        {"tier": "friend", "order": 3,
         "name": "The Master's Request",
         "brief": "My masterwork needs {count} {item}. Only the best will do.",
         "accept": "'This is for something special. {count} {item}. Don't settle for less than perfect.'",
         "complete": "'Perfect. Absolutely perfect. You've earned this — made with my own hands.'"},
        {"tier": "trusted", "order": 4,
         "name": "The Dying Harvest",
         "brief": "A blight is killing the {item}. Gather {count} before they're gone forever.",
         "accept": "'If we don't act now, the {item} will be extinct within the season. {count} specimens. Save what we can.'",
         "complete": "'You've saved the harvest. Future generations will thank you. Take this — it's been in my family for generations.'"},
        {"tier": "bonded", "order": 5,
         "name": "The Legendary Bloom",
         "brief": "One last gathering. The rarest material in the region — if it even exists.",
         "accept": "'They say it only grows where the old magic still runs deep. {count} {item}. I'm not even sure it's real.'",
         "complete": "'You found it. You actually found it. I've waited my whole life for this moment. This is yours — it belongs with someone who understands.'"},
    ],
    "merchant": [
        {"tier": "stranger", "order": 1,
         "name": "Road Clearance",
         "brief": "Bandits are blocking the trade route. Clear {count} {monster} off the road.",
         "accept": "'Simple job. {count} {monster} blocking the road. Clear them, get paid.'",
         "complete": "'Road's clear. Caravans are moving. Good work. Come back — I always have work.'"},
        {"tier": "acquainted", "order": 2,
         "name": "Supply Recovery",
         "brief": "A caravan lost its cargo to {monster}. Recover {count} — the goods, not the beasts.",
         "accept": "'The caravan ran off but the cargo's still out there. {count} {monster} in the way. Get my goods back.'",
         "complete": "'My supplies! Good as new. You're reliable — that's worth more than gold in this business.'"},
        {"tier": "friend", "order": 3,
         "name": "The Big Contract",
         "brief": "I need {count} {item} for a special order. This one could make my reputation.",
         "accept": "'This contract is worth ten times what I usually move. {count} {item}. Don't let me down.'",
         "complete": "'You delivered. The client is thrilled. I'm thrilled. This is for you — my way of saying thanks.'"},
        {"tier": "trusted", "order": 4,
         "name": "The Rival",
         "brief": "A rival broker is trying to steal my trade routes. Send a message — {count} {monster} of their thugs.",
         "accept": "'They think they can take my routes. {count} of their hired {monster}. Make it clear they can't.'",
         "complete": "'That should settle it. You're not just a contractor anymore — you're a partner. Take this.'"},
        {"tier": "bonded", "order": 5,
         "name": "The Master Deal",
         "brief": "One last deal. The biggest of my career. I need someone I trust completely.",
         "accept": "'Everything I've built comes down to this. {count} {monster} stand between me and retirement. You're the only one I trust.'",
         "complete": "'We did it. The deal of a lifetime. I couldn't have done this without you. This is yours — a token of a partnership that changed my life.'"},
    ],
    "mystic": [
        {"tier": "stranger", "order": 1,
         "name": "Field Notes",
         "brief": "I need samples from {count} {monster}. For research, of course.",
         "accept": "'Bring me {count} {monster} specimens. Careful — they bite. So does my curiosity.'",
         "complete": "'Fascinating. The mana residue alone... ah, you don't care. Here's your payment.'"},
        {"tier": "acquainted", "order": 2,
         "name": "The Anomaly",
         "brief": "Something strange is happening. {count} {monster} are behaving oddly. Investigate.",
         "accept": "'They shouldn't be this far from their territory. {count} {monster}. Something is driving them out. Find what.'",
         "complete": "'Your observations confirm my theory. Excellent fieldwork. I'll share more with you — if you keep helping.'"},
        {"tier": "friend", "order": 3,
         "name": "The Ritual",
         "brief": "My ritual requires {count} {item}. The magic won't work without them.",
         "accept": "'The alignment is in three days. {count} {item}. Don't ask what the ritual does — you don't want to know.'",
         "complete": "'The ritual worked. I saw... things. Things I cannot unsee. But this — this I can give. Take it.'"},
        {"tier": "trusted", "order": 4,
         "name": "The Forbidden Knowledge",
         "brief": "There are {monster} guarding an old archive. {count} of them. I need what's inside.",
         "accept": "'The archive predates the current age. {count} {monster} guard it. I need those records — they could change everything.'",
         "complete": "'You retrieved it. Do you know what this means? No — you don't. Good. Take this. It's safer with you than with me.'"},
        {"tier": "bonded", "order": 5,
         "name": "The Final Truth",
         "brief": "One last secret. The deepest one. {count} {monster} stand between us and the answer.",
         "accept": "'I have searched my entire life for this. {count} {monster}. If we succeed, we will know the truth about everything.'",
         "complete": "'It's... not what I expected. But it is the truth. And truth is always worth the price. This is yours — you earned the right to carry it.'"},
    ],
    "guard": [
        {"tier": "stranger", "order": 1,
         "name": "Patrol Duty",
         "brief": "Walk the perimeter. If you see {monster}, deal with {count} of them.",
         "accept": "'Standard patrol. {count} {monster} is the quota. Don't engage more than you can handle.'",
         "complete": "'Clean patrol. Good report. You might make a decent sentinel yet.'"},
        {"tier": "acquainted", "order": 2,
         "name": "The Threat",
         "brief": "Something's been picking off stragglers. {count} {monster} — find and neutralize.",
         "accept": "'Three missing this week. {count} {monster} suspected. Find them. Stop them.'",
         "complete": "'Threat neutralized. The streets are safer. You have my thanks — and the town's.'"},
        {"tier": "friend", "order": 3,
         "name": "The Breach",
         "brief": "They're testing our defenses. {count} {monster} hit the wall last night. Push them back.",
         "accept": "'They probed the east gate. {count} {monster}. Hit them before they hit us again.'",
         "complete": "'You held the line. That's what a sentinel does. This is the sentinel's mark — wear it.'"},
        {"tier": "trusted", "order": 4,
         "name": "The Siege",
         "brief": "A warband is massing. {count} {monster} leaders. Cut the head off the snake.",
         "accept": "'If we don't break their command, we'll be fighting a siege by week's end. {count} {monster}. Go.'",
         "complete": "'You broke their command structure. They're scattering. You just saved this town. Take this — it's the captain's privilege.'"},
        {"tier": "bonded", "order": 5,
         "name": "The Last Watch",
         "brief": "One final threat. The biggest this town has ever faced. {count} {monster}. Stand with me.",
         "accept": "'I've held this wall for thirty years. This is the one I might not survive. {count} {monster}. But with you — maybe we both do.'",
         "complete": "'We held. We held! The town stands because you stood. This is the highest honor I can give. It's been waiting for someone worthy.'"},
    ],
}

# Bounty quest templates
BOUNTY_TEMPLATES_KILL = [
    {"name": "Bounty: {monster_name}", "brief": "Slay {count} {monster_name} in the {biome_name}.",
     "accept": "'{count} {monster_name}. Standard bounty. Good pay.'",
     "complete": "'Confirmed kills. Here's your payment.'"},
    {"name": "Cull: {monster_name}", "brief": "The {monster_name} population is growing. Cull {count}.",
     "accept": "'Too many {monster_name}. Thin them by {count}. Simple work.'",
     "complete": "'Good. That should keep them in check. Payment as agreed.'"},
    {"name": "Wanted: {monster_name}", "brief": "{count} {monster_name} wanted dead. Reward posted.",
     "accept": "'{count} {monster_name}. The bounty's posted. Bring proof.'",
     "complete": "'Done. Here's your reward. There's always more.'"},
]

BOUNTY_TEMPLATES_GATHER = [
    {"name": "Order: {item_name}", "brief": "Deliver {count} {item_name} from the {biome_name}.",
     "accept": "'I need {count} {item_name}. Fresh stock. Don't waste any.'",
     "complete": "'Good quality. Payment on delivery. Come back anytime.'"},
    {"name": "Requisition: {item_name}", "brief": "The town needs {count} {item_name}. Gather them.",
     "accept": "'{count} {item_name}. The stores are running low. Don't let me down.'",
     "complete": "'Stocked up. Good work. Same rate next time.'"},
    {"name": "Collection: {item_name}", "brief": "I'm collecting {count} {item_name}. Paying market rate.",
     "accept": "'{count} {item_name}. Market rate. No haggling.'",
     "complete": "'Counted and verified. Here's your coin.'"},
]

# Story quest templates (level-gated one-shots)
STORY_TEMPLATES = [
    {"name": "Lost Caravan", "brief": "A caravan went missing near the {biome_name}. Find them.",
     "accept": "'They were due two days ago. Find the caravan — or what's left of it.'",
     "complete": "'You found them. Not all of them, but enough. The families will have closure. Thank you.'"},
    {"name": "The Wounded Scout", "brief": "One of our scouts is trapped in the {biome_name}. Get them out.",
     "accept": "'They've been hiding for three days. {monster_name} between them and safety. Go.'",
     "complete": "'You brought them home. They'll live. That's worth more than I can pay — but I'll try.'"},
    {"name": "Supply Run", "brief": "Emergency supplies needed from the {biome_name}. {count} {item_name}.",
     "accept": "'The infirmary is running dry. {count} {item_name}. Fast as you can.'",
     "complete": "'You saved lives today. Here's more than the standard rate — you earned it.'"},
    {"name": "The Nest", "brief": "A {monster_name} nest has been found. Destroy {count} of them.",
     "accept": "'If those eggs hatch, we'll have a plague on our hands. {count} {monster_name}. Burn the nest.'",
     "complete": "'Good. No eggs, no hatchlings. Clean work. Here's your pay.'"},
    {"name": "The Missing Person", "brief": "Someone vanished near the {biome_name}. Find evidence.",
     "accept": "'They went gathering and never came back. Look for signs — and watch for {monster_name}.'",
     "complete": "'You found enough. It's not a happy ending, but it's an ending. Their family will know.'"},
    {"name": "Beast Study", "brief": "I need a live report on {monster_name} behavior. Observe and dispatch {count}.",
     "accept": "'Watch them first. Then kill {count}. I need both the data and the results.'",
     "complete": "'Excellent observations. The data is invaluable. Payment and a bonus for thoroughness.'"},
    {"name": "Emergency Repairs", "brief": "The wall needs {count} {item_name}. We're undermanned.",
     "accept": "'The east wall cracked. {count} {item_name} for patching. Now.'",
     "complete": "'The wall holds. You bought us time. Here's your pay — and my thanks.'"},
    {"name": "The Cache", "brief": "There's a hidden cache in the {biome_name}. Clear the {monster_name} and recover it.",
     "accept": "'Old war supplies, buried and marked. {count} {monster_name} guard the area. Clear them, find the cache.'",
     "complete": "'You found it. The supplies are older than I am, but they'll do. Payment as promised.'"},
]


# ============================================================
# GENERATION FUNCTIONS
# ============================================================

import random as _rng


def _pick_name(role_def: dict, race: str, town_id: str) -> tuple[str, str, str]:
    """Pick a name from the role's pool, matching race where possible."""
    pool = [n for n in role_def["name_pools"] if n[2] == race]
    if not pool:
        pool = role_def["name_pools"]
    title, first, r = _rng.choice(pool)
    return title, first, r


def _get_biomes_for_town(town_id: str) -> list[str]:
    """Get biomes for the town's continent, sorted by level_req."""
    cont = TOWN_CONTINENT.get(town_id, "")
    biome_ids = CONTINENT_BIOMES.get(cont, [])
    # Sort by biome level_req
    biome_levels = {}
    for c in CONTINENTS_V2:
        for b in c.get("biomes", []):
            biome_levels[b["id"]] = b.get("level_req", 1)
    return sorted(biome_ids, key=lambda b: biome_levels.get(b, 999))


def _monsters_for_biomes(biome_ids: list[str], monster_idx: dict) -> list[tuple[str, str, str, int]]:
    """Get all monsters for the given biomes, sorted by power."""
    result = []
    seen = set()
    for bid in biome_ids:
        for m in monster_idx.get(bid, []):
            if m[0] not in seen:
                result.append(m)
                seen.add(m[0])
    result.sort(key=lambda x: x[3])
    return result


def _items_for_biomes(biome_ids: list[str], item_idx: dict, kind: str = None) -> list[tuple[str, str, str, str]]:
    """Get all items for the given biomes, optionally filtered by kind."""
    result = []
    seen = set()
    for bid in biome_ids:
        for it in item_idx.get(bid, []):
            if it[0] not in seen and (kind is None or it[2] == kind):
                result.append(it)
                seen.add(it[0])
    return result


def _biome_display_name(biome_id: str) -> str:
    for c in CONTINENTS_V2:
        for b in c.get("biomes", []):
            if b["id"] == biome_id:
                return b["name"]
    return biome_id.replace("_", " ").title()


def _make_chain_quests(npc_id: str, role: str, town_name: str,
                       monsters: list, items: list, biomes: list) -> list[dict]:
    """Generate 3-5 relationship-gated chain quests for an NPC."""
    templates = CHAIN_NARRATIVES.get(role, CHAIN_NARRATIVES["veteran"])
    quests = []
    biome_name = _biome_display_name(biomes[0]) if biomes else "wilds"

    for tmpl in templates:
        tier = tmpl["tier"]
        order = tmpl["order"]
        rewards = TIER_REWARDS[tier]
        level_req = TIER_LEVEL[tier]

        # Defaults for format keys
        fmt_monster = "the beast"
        fmt_item = "the material"

        # Pick monster or item based on role
        if role in ("veteran", "guard"):
            suitable = [m for m in monsters if _monster_suitable(m, level_req)]
            if not suitable:
                suitable = monsters
            if not suitable:
                continue
            m = _rng.choice(suitable)
            fmt_monster = m[1]
            count = _rng.randint(3, 6) if tier in ("stranger", "acquainted") else _rng.randint(2, 4)
            req_key = "kills"
            req_val = [(m[0], count)]
            name = tmpl["name"]
            brief = tmpl["brief"].format(count=count, monster=fmt_monster, item=fmt_item, biome=biome_name)
        elif role == "gatherer":
            suitable = [it for it in items if it[2] == "material"]
            if not suitable:
                suitable = items
            if not suitable:
                continue
            it = _rng.choice(suitable)
            fmt_item = it[1]
            count = _rng.randint(5, 12) if tier in ("stranger", "acquainted") else _rng.randint(3, 8)
            req_key = "gathers"
            req_val = [(it[0], count)]
            name = tmpl["name"]
            brief = tmpl["brief"].format(count=count, monster=fmt_monster, item=fmt_item, biome=biome_name)
        elif role == "merchant":
            if tier in ("stranger", "acquainted") and monsters:
                m = _rng.choice(monsters[:max(1, len(monsters)//2)])
                fmt_monster = m[1]
                count = _rng.randint(3, 6)
                req_key = "kills"
                req_val = [(m[0], count)]
                brief = tmpl["brief"].format(count=count, monster=fmt_monster, item=fmt_item, biome=biome_name)
            elif items:
                it = _rng.choice([i for i in items if i[2] == "material"] or items)
                fmt_item = it[1]
                count = _rng.randint(5, 10)
                req_key = "gathers"
                req_val = [(it[0], count)]
                brief = tmpl["brief"].format(count=count, monster=fmt_monster, item=fmt_item, biome=biome_name)
            else:
                continue
            name = tmpl["name"]
        else:  # mystic
            if monsters:
                m = _rng.choice(monsters[:max(1, len(monsters)//2)] if tier in ("stranger", "acquainted") else monsters)
                fmt_monster = m[1]
                count = _rng.randint(2, 5)
                req_key = "kills"
                req_val = [(m[0], count)]
                brief = tmpl["brief"].format(count=count, monster=fmt_monster, item=fmt_item, biome=biome_name)
            else:
                continue
            name = tmpl["name"]

        accept = tmpl["accept"].format(count=count, monster=fmt_monster, item=fmt_item, biome=biome_name)
        complete = tmpl["complete"]

        # Build requirements
        requirements = {req_key: req_val}
        if tier not in ("stranger", "acquainted"):
            requirements["character_level"] = level_req

        # Build rewards
        reward = {
            "gold": _rng.randint(rewards["gold"][0], rewards["gold"][1]),
            "xp": _rng.randint(rewards["xp"][0], rewards["xp"][1]),
            "relationship": rewards["rel"],
        }

        # Add unique item for friend+ tiers
        unique = UNIQUE_ITEMS.get(role, {}).get(tier)
        if unique:
            uniq = dict(unique)
            uniq["id"] = uniq["id"].format(town=town_name.lower().replace(" ", "_"))
            uniq["name"] = uniq["name"].format(Town=town_name)
            reward["unique_item"] = uniq

        # Add material rewards for lower tiers
        if tier in ("stranger", "acquainted") and items:
            mat = _rng.choice([i for i in items if i[2] == "material"] or items)
            reward["items"] = [(mat[0], _rng.randint(2, 5))]

        quests.append({
            "id": f"q_{npc_id}_chain_{order}",
            "npc_id": npc_id,
            "tier": tier,
            "order": order,
            "name": name,
            "brief": brief,
            "narrative": {"accept": accept, "complete": complete},
            "requirements": requirements,
            "rewards": reward,
        })

    return quests


def _monster_suitable(monster: tuple, level_req: int) -> bool:
    """Check if a monster's power is suitable for the given level."""
    power = monster[3]
    if level_req <= 5:
        return power <= 10
    elif level_req <= 12:
        return power <= 25
    elif level_req <= 25:
        return power <= 45
    else:
        return power > 30


def _make_bounty_quests(npc_id: str, role: str, monsters: list, items: list,
                        biomes: list, count: int = 8) -> list[dict]:
    """Generate repeatable bounty quests."""
    quests = []
    biome_name = _biome_display_name(biomes[0]) if biomes else "wilds"

    # Kill bounties
    kill_count = count // 2
    for i in range(min(kill_count, len(monsters))):
        m = monsters[i % len(monsters)]
        tmpl = _rng.choice(BOUNTY_TEMPLATES_KILL)
        target_count = _rng.randint(3, 8)
        quests.append({
            "id": f"q_{npc_id}_bounty_kill_{i+1}",
            "npc_id": npc_id,
            "tier": "stranger",
            "order": 100 + i,
            "name": tmpl["name"].format(monster_name=m[1]),
            "brief": tmpl["brief"].format(count=target_count, monster_name=m[1], biome_name=biome_name),
            "narrative": {
                "accept": tmpl["accept"].format(count=target_count, monster_name=m[1]),
                "complete": tmpl["complete"],
            },
            "requirements": {"kills": [(m[0], target_count)]},
            "rewards": {
                "gold": _rng.randint(50, 200),
                "xp": _rng.randint(30, 100),
                "relationship": _rng.randint(10, 30),
            },
            "repeatable": True,
        })

    # Gather bounties
    gather_items = [it for it in items if it[2] == "material"]
    gather_count = count - len(quests)
    for i in range(min(gather_count, len(gather_items))):
        it = gather_items[i % len(gather_items)]
        tmpl = _rng.choice(BOUNTY_TEMPLATES_GATHER)
        target_count = _rng.randint(5, 15)
        quests.append({
            "id": f"q_{npc_id}_bounty_gather_{i+1}",
            "npc_id": npc_id,
            "tier": "stranger",
            "order": 200 + i,
            "name": tmpl["name"].format(item_name=it[1]),
            "brief": tmpl["brief"].format(count=target_count, item_name=it[1], biome_name=biome_name),
            "narrative": {
                "accept": tmpl["accept"].format(count=target_count, item_name=it[1]),
                "complete": tmpl["complete"],
            },
            "requirements": {"gathers": [(it[0], target_count)]},
            "rewards": {
                "gold": _rng.randint(40, 150),
                "xp": _rng.randint(20, 80),
                "relationship": _rng.randint(10, 25),
            },
            "repeatable": True,
        })

    # Fish bounties (if available)
    fish_items = [it for it in items if it[2] == "fish"]
    for i in range(min(2, len(fish_items))):
        it = fish_items[i % len(fish_items)]
        target_count = _rng.randint(3, 8)
        quests.append({
            "id": f"q_{npc_id}_bounty_fish_{i+1}",
            "npc_id": npc_id,
            "tier": "stranger",
            "order": 300 + i,
            "name": f"Fishing Order: {it[1]}",
            "brief": f"Deliver {target_count} {it[1]} from the {biome_name}.",
            "narrative": {
                "accept": f"'{target_count} {it[1]}. Fresh catch only.'",
                "complete": "'Good catch. Payment on delivery.'",
            },
            "requirements": {"gathers": [(it[0], target_count)]},
            "rewards": {
                "gold": _rng.randint(40, 120),
                "xp": _rng.randint(20, 60),
                "relationship": _rng.randint(10, 20),
            },
            "repeatable": True,
        })

    return quests


def _make_story_quests(npc_id: str, role: str, monsters: list, items: list,
                       biomes: list, count: int = 6) -> list[dict]:
    """Generate level-gated story quests."""
    quests = []
    biome_name = _biome_display_name(biomes[0]) if biomes else "wilds"

    # Sort monsters by power for level-appropriate selection
    sorted_monsters = sorted(monsters, key=lambda x: x[3])
    materials = [it for it in items if it[2] == "material"]

    for i in range(min(count, len(STORY_TEMPLATES))):
        tmpl = STORY_TEMPLATES[i]
        level_req = 1 + i * 4  # 1, 5, 9, 13, 17, 21

        # Determine quest type
        if "monster" in tmpl["brief"] or "monster_name" in tmpl["brief"]:
            if not sorted_monsters:
                continue
            # Pick a monster appropriate for the level
            suitable = [m for m in sorted_monsters if _monster_suitable(m, level_req)]
            if not suitable:
                suitable = sorted_monsters
            m = suitable[min(i, len(suitable)-1)]
            monster_count = _rng.randint(2, 6)
            brief = tmpl["brief"].format(biome_name=biome_name, monster=m[1],
                                         monster_name=m[1], count=monster_count, item_name="")
            accept = tmpl["accept"].format(monster_name=m[1], count=monster_count)
            requirements = {"kills": [(m[0], monster_count)], "character_level": level_req}
        elif "item_name" in tmpl["brief"]:
            if not materials:
                continue
            it = materials[min(i, len(materials)-1)]
            item_count = _rng.randint(3, 10)
            brief = tmpl["brief"].format(biome_name=biome_name, item_name=it[1],
                                         count=item_count, monster="", monster_name="")
            accept = tmpl["accept"].format(item_name=it[1], count=item_count)
            requirements = {"gathers": [(it[0], item_count)], "character_level": level_req}
        else:
            if not sorted_monsters:
                continue
            m = sorted_monsters[min(i, len(sorted_monsters)-1)]
            monster_count = _rng.randint(2, 5)
            brief = tmpl["brief"].format(biome_name=biome_name, monster=m[1],
                                         monster_name=m[1], count=monster_count, item_name="")
            accept = tmpl["accept"].format(monster_name=m[1], count=monster_count)
            requirements = {"kills": [(m[0], monster_count)], "character_level": level_req}

        complete = tmpl["complete"]

        # Rewards scale with level
        gold = 100 + level_req * 30 + _rng.randint(0, 50)
        xp = 80 + level_req * 25 + _rng.randint(0, 40)

        reward = {"gold": gold, "xp": xp, "relationship": _rng.randint(30, 80)}

        # Add item rewards
        if materials and i % 2 == 0:
            mat = materials[min(i, len(materials)-1)]
            reward["items"] = [(mat[0], _rng.randint(2, 5))]

        quests.append({
            "id": f"q_{npc_id}_story_{i+1}",
            "npc_id": npc_id,
            "tier": "stranger",
            "order": 500 + i,
            "name": tmpl["name"],
            "brief": brief,
            "narrative": {"accept": accept, "complete": complete},
            "requirements": requirements,
            "rewards": reward,
        })

    return quests


def _generate_town_npcs(town_id: str, monster_idx: dict, item_idx: dict,
                        existing_npc_ids: set) -> list[dict]:
    """Generate 4-5 new NPCs for a town."""
    cont = TOWN_CONTINENT[town_id]
    race = CONTINENT_RACE.get(cont, "human")
    town_name, town_type = TOWN_META.get(town_id, (town_id.title(), "town"))
    biomes = _get_biomes_for_town(town_id)
    monsters = _monsters_for_biomes(biomes, monster_idx)
    items = _items_for_biomes(biomes, item_idx)

    if not monsters:
        monsters = [("dummy", "Wild Beast", "common", 1)]
    if not items:
        items = [("dummy_item", "Local Good", "material", "common")]

    npcs = []
    roles_to_gen = list(NPC_ROLES)

    # If town has an existing NPC, only generate 4 new (skip one role)
    if town_id in existing_npc_ids:
        # Skip "guard" role since flagship NPC often serves that purpose
        roles_to_gen = [r for r in NPC_ROLES if r["role"] != "guard"]
    else:
        # No existing NPC — generate all 5 roles
        pass

    for role_def in roles_to_gen:
        role = role_def["role"]
        title, first, npc_race = _pick_name(role_def, race, town_id)
        npc_id = f"{role}_{town_id}_{first.lower()}"

        # Ensure unique id
        base_id = npc_id
        suffix = 2
        while npc_id in existing_npc_ids:
            npc_id = f"{base_id}_{suffix}"
            suffix += 1
        existing_npc_ids.add(npc_id)

        # Build NPC
        title_str = _rng.choice(role_def["title_templates"]).format(town=town_name)
        personality = _rng.choice(role_def["personalities"])
        desc = _rng.choice(role_def["desc_templates"])

        # Generate quests
        chain = _make_chain_quests(npc_id, role, town_name, monsters, items, biomes)
        bounties = _make_bounty_quests(npc_id, role, monsters, items, biomes, count=8)
        stories = _make_story_quests(npc_id, role, monsters, items, biomes, count=6)

        all_quests = chain + bounties + stories

        npcs.append({
            "id": npc_id,
            "name": f"{title} {first}",
            "race": npc_race,
            "town": town_id,
            "continent": cont,
            "title": title_str,
            "description": desc,
            "personality": personality,
            "quests": all_quests,
        })

    return npcs


def generate_all_npcs() -> list[dict]:
    """Generate all new NPCs for every town."""
    _rng.seed(42)  # deterministic output

    monster_idx = _build_monster_index()
    item_idx = _build_item_index()

    # Existing NPC towns
    existing_towns = {"oathspire", "grunhold", "elaris", "jahrahold",
                      "solunara", "rindivar_grove", "atlantyrion", "veilgrove"}
    existing_ids: set = set()

    all_npcs = []
    for town_id in TOWN_CONTINENT:
        town_npcs = _generate_town_npcs(town_id, monster_idx, item_idx, existing_ids)
        all_npcs.extend(town_npcs)

    return all_npcs


# ============================================================
# NOTICE BOARD QUEST GENERATION
# ============================================================

# Region IDs per town (for quest region field)
TOWN_REGION: dict[str, str] = {
    "oathspire": "vale_of_oaths",
    "riverguard": "riverguard_reach",
    "grunhold": "bloodwind_march",
    "warforge": "iron_scar_march",
    "elaris": "concordia_heartland",
    "silvergate": "silverroad_march",
    "jahrahold": "undermountain_hall",
    "deepstone": "stone_wardens",
    "solunara": "haya_ascendant",
    "starfall_watch": "stormpeaks",
    "rindivar_grove": "primal_grove",
    "beastcairn": "nomad_march",
    "atlantyrion": "coral_gates",
    "veilgrove": "deep_verdant",
}

BOARD_QUEST_TEMPLATES = [
    {"title": "Pest Control: {monster_name}", "brief": "The {biome_name} is crawling with {monster_name}. Slay {count}.",
     "kind": "kill", "reward_gold": (80, 200), "reward_xp": (60, 150), "level": 1},
    {"title": "Supply Order: {item_name}", "brief": "The town needs {count} {item_name} from the {biome_name}.",
     "kind": "gather", "reward_gold": (60, 180), "reward_xp": (50, 120), "level": 1},
    {"title": "Thinning the Herd: {monster_name}", "brief": "{monster_name} are overpopulating. Reduce their numbers by {count}.",
     "kind": "kill", "reward_gold": (100, 250), "reward_xp": (80, 200), "level": 2},
    {"title": "Herbalist's Request: {item_name}", "brief": "Gather {count} {item_name} for the town's herbalist.",
     "kind": "gather", "reward_gold": (80, 200), "reward_xp": (60, 160), "level": 2},
    {"title": "Dangerous Game: {monster_name}", "brief": "A {monster_name} has been spotted near the roads. Hunt {count} of them.",
     "kind": "kill", "reward_gold": (150, 350), "reward_xp": (120, 280), "level": 4},
    {"title": "Rare Materials: {item_name}", "brief": "The market seeks {count} {item_name}. Collect them from the {biome_name}.",
     "kind": "gather", "reward_gold": (120, 300), "reward_xp": (100, 240), "level": 4},
    {"title": "Beast Hunt: {monster_name}", "brief": "A fearsome {monster_name} threatens travelers. Slay {count}.",
     "kind": "kill", "reward_gold": (200, 500), "reward_xp": (160, 400), "level": 8},
    {"title": "Expedition: {biome_name}", "brief": "Explore the {biome_name} and complete {count} gathering expeditions.",
     "kind": "action", "action_id": "gather_herbs", "reward_gold": (150, 350), "reward_xp": (120, 300), "level": 5},
    {"title": "Fishing Order: {fish_name}", "brief": "The tavern needs {count} {fish_name} for tonight's menu.",
     "kind": "gather", "reward_gold": (60, 160), "reward_xp": (40, 100), "level": 1},
    {"title": "Cull the Predators: {monster_name}", "brief": "Predators are stalking the outskirts. Put down {count} {monster_name}.",
     "kind": "kill", "reward_gold": (250, 600), "reward_xp": (200, 500), "level": 12},
]


def generate_notice_board_quests() -> list[dict]:
    """Generate ~10 notice board quests per town."""
    _rng.seed(1337)  # deterministic, different seed from NPCs

    monster_idx = _build_monster_index()
    item_idx = _build_item_index()

    all_quests = []
    quest_counter = 0

    for town_id in TOWN_CONTINENT:
        cont = TOWN_CONTINENT[town_id]
        town_name = TOWN_META.get(town_id, (town_id.title(), ""))[0]
        region = TOWN_REGION.get(town_id, town_id)
        biomes = _get_biomes_for_town(town_id)
        monsters = _monsters_for_biomes(biomes, monster_idx)
        items = _items_for_biomes(biomes, item_idx)
        materials = [it for it in items if it[2] == "material"]
        fish = [it for it in items if it[2] == "fish"]

        if not monsters:
            monsters = [("dummy", "Wild Beast", "common", 1)]
        if not materials:
            materials = [("dummy_item", "Local Good", "material", "common")]
        if not fish:
            fish = [("dummy_fish", "Local Fish", "fish", "common")]

        # Generate 10 quests per town
        for i in range(10):
            tmpl = BOARD_QUEST_TEMPLATES[i % len(BOARD_QUEST_TEMPLATES)]
            quest_counter += 1
            qid = f"board_{town_id}_{i+1}"
            biome_name = _biome_display_name(biomes[0]) if biomes else "wilds"

            if tmpl["kind"] == "kill":
                m = monsters[min(i, len(monsters)-1)]
                count = _rng.randint(3, 8)
                title = tmpl["title"].format(monster_name=m[1])
                brief = tmpl["brief"].format(monster_name=m[1], count=count, biome_name=biome_name)
                objectives = [{"kind": "kill", "id": m[0], "count": count}]
            elif tmpl["kind"] == "gather" and "fish_name" in tmpl["title"]:
                f = fish[min(i, len(fish)-1)]
                count = _rng.randint(3, 8)
                title = tmpl["title"].format(fish_name=f[1])
                brief = tmpl["brief"].format(fish_name=f[1], count=count, biome_name=biome_name)
                objectives = [{"kind": "gather", "id": f[0], "count": count}]
            elif tmpl["kind"] == "gather":
                it = materials[min(i, len(materials)-1)]
                count = _rng.randint(5, 12)
                title = tmpl["title"].format(item_name=it[1])
                brief = tmpl["brief"].format(item_name=it[1], count=count, biome_name=biome_name)
                objectives = [{"kind": "gather", "id": it[0], "count": count}]
            elif tmpl["kind"] == "action":
                count = _rng.randint(2, 5)
                title = tmpl["title"].format(biome_name=biome_name)
                brief = tmpl["brief"].format(biome_name=biome_name, count=count)
                objectives = [{"kind": "action", "id": tmpl.get("action_id", "gather_herbs"), "count": count}]
            else:
                continue

            gold = _rng.randint(tmpl["reward_gold"][0], tmpl["reward_gold"][1])
            xp = _rng.randint(tmpl["reward_xp"][0], tmpl["reward_xp"][1])

            # Add item reward chance for higher-level quests
            reward: dict = {"gold": gold, "xp": xp}
            if tmpl["level"] >= 4 and materials:
                mat = materials[min(i, len(materials)-1)]
                reward["items"] = [(mat[0], 0.3)]

            all_quests.append({
                "id": qid,
                "category": "regional",
                "board": "notice",
                "town_id": town_id,
                "region": region,
                "title": title,
                "giver": f"{town_id}_notice_board",
                "brief": brief,
                "objectives": objectives,
                "reward": reward,
                "level_req": tmpl["level"],
            })

    return all_quests
