"""Phase 2 game data — regions, towns, quests, events, racial extras."""
from __future__ import annotations


# ============================================================
# REGIONS (nested inside continents)
# ============================================================
REGIONS: list[dict] = [
    # ==================== VALERIA (Human Empire) ====================
    {"id": "vale_of_oaths",       "name": "Vale of Oaths",       "continent": "valeria",
     "desc": "Sun-warmed valley cradling the imperial capital. Golden fields and forge-lit cities.",
     "biomes": ["golden_plains", "crownwood_forest"], "town_ids": ["oathspire"]},
    {"id": "riverguard_march",    "name": "Riverguard March",    "continent": "valeria",
     "desc": "Where the rivers slow and old kingdom ruins jut from the mist. Fewer travelers, more secrets.",
     "biomes": ["imperial_riverlands", "ashen_border"], "town_ids": ["riverguard"]},
    # ==================== MUSHKARA (Orc Dominion) ====================
    {"id": "liberators_heart",    "name": "Heart of the Liberator", "continent": "mushkara",
     "desc": "The seat of Zaheer's memory. Ash-dark skies and forges that never sleep.",
     "biomes": ["red_steppe", "iron_scar"], "town_ids": ["grunhold"]},
    {"id": "warforge_march",      "name": "Warforge March",      "continent": "mushkara",
     "desc": "A wide black plain where warbands drill in the smoke of Demonfall.",
     "biomes": ["ash_barrens", "demonfall_crater"], "town_ids": ["warforge"]},
    # ==================== CONCORDIA (Half-Elf Federation) ====================
    {"id": "elaris_reach",        "name": "Elaris Reach",        "continent": "concordia",
     "desc": "Where the trade roads meet the sea. Ports fly every flag and inns speak every tongue.",
     "biomes": ["mosaic_coast", "amber_vineyards"], "town_ids": ["elaris"]},
    {"id": "silvergate_pass",     "name": "Silvergate Pass",     "continent": "concordia",
     "desc": "The great trade highway, guarded by federation embassies and clean caravanserais.",
     "biomes": ["silverroad", "diplomats_highlands"], "town_ids": ["silvergate"]},
    # ==================== KHARDRUM (Dwarven Undermountain) ====================
    {"id": "jahra_holdfast",      "name": "Jahra Holdfast",      "continent": "khardrum",
     "desc": "The great vault-city of the Dwarves. Jahra veins run through the walls; every hearth sings.",
     "biomes": ["granite_foothills", "ember_mines"], "town_ids": ["jahrahold"]},
    {"id": "deepstone_watch",     "name": "Deepstone Watch",     "continent": "khardrum",
     "desc": "A palisade fort ringed by crystal caverns and the ancestor-forges of the deep.",
     "biomes": ["crystal_caverns", "deep_forges"], "town_ids": ["deepstone"]},
    # ==================== HAYA (Higher Enclave / Elves) ====================
    {"id": "solunara_ascendant",  "name": "Solunara Ascendant",  "continent": "haya",
     "desc": "The new home of the Higher Enclave — sky-cities suspended by song and sun.",
     "biomes": ["sunlit_canopy", "moonveil_woods"], "town_ids": ["solunara"]},
    {"id": "starfall_march",      "name": "Starfall March",      "continent": "haya",
     "desc": "A vast plateau of lightning-glass where Sky-Riders test their wings.",
     "biomes": ["celestial_lake", "starfall_cliffs"], "town_ids": ["starfall_watch"]},
    # ==================== GENNEL (Wildblood Sovereignty) ====================
    {"id": "rindivar_reach",      "name": "Rindivar Reach",      "continent": "gennel",
     "desc": "The blooming desert basin where the Primal Sovereignty first raised the totems.",
     "biomes": ["blooming_desert", "beastwood"], "town_ids": ["rindivar_grove"]},
    {"id": "beastcairn_pass",     "name": "Beastcairn Pass",     "continent": "gennel",
     "desc": "A moving camp of tents pitched between old totems. The djinn-touched trade dreams for bread.",
     "biomes": ["roaring_savanna", "ancient_den"], "town_ids": ["beastcairn"]},
    # ==================== HYLION (Underwater Kingdom) ====================
    {"id": "atlantyrion_gate",    "name": "Atlantyrion Gate",    "continent": "hylion",
     "desc": "The shining reef-wall where Atlantyrion greets the surface world.",
     "biomes": ["coral_gardens", "kelp_forest"], "town_ids": ["atlantyrion"]},
    {"id": "abyssal_march",       "name": "Abyssal March",       "continent": "hylion",
     "desc": "Storm reefs above the deep trench. Pearl divers, tidebound priests, and shipwreck salvagers.",
     "biomes": ["storm_reefs", "abyssal_trench"], "town_ids": []},
    # ==================== DAW'UL TALALU (Sylvan Mystleaf) ====================
    {"id": "veilgrove_hollow",    "name": "Veilgrove Hollow",    "continent": "daw_ul_talalu",
     "desc": "A living jungle woven with sylvan roads. Every leaf listens.",
     "biomes": ["mistwood", "thorn_labyrinth"], "town_ids": ["veilgrove"]},
    {"id": "elderroot_deep",      "name": "Elderroot Deep",      "continent": "daw_ul_talalu",
     "desc": "The oldest heart of the Mystleaf. Only the initiated cross the outer wards.",
     "biomes": ["lumina_grove", "elderroot_hollow"], "town_ids": []},
]


# ============================================================
# TOWNS
# ============================================================
# services: subset of ["sanctuary", "market", "trainers", "notice_board", "tavern", "alchemist"]
TOWNS: list[dict] = [
    # ==================== AETHERIA ====================
    {
        "id": "ironhold",
        "name": "Ironhold",
        "type": "forge_town",
        "region": "vale_of_elder_kings",
        "continent": "aetheria",
        "desc": "A soot-blackened town ringing with hammers. Ironhold's smiths forge armor for kings and killers alike.",
        "specialty": "Master Blacksmith — advanced weapon and armor recipes unlockable only here.",
        "services": ["sanctuary", "market", "trainers", "notice_board", "tavern"],
        "sanctuary_cost": 10,
        "fast_travel_cost": 25,
        "market_items": ["iron_ore", "oak_log", "wild_herb", "bandage", "minor_healing_potion",
                         "iron_dagger", "iron_longsword", "bronze_mace", "bone_shield", "iron_helm",
                         "iron_greaves", "ironshod_boots", "iron_kite_shield", "traveler_garb", "worn_trousers", "old_boots"],
        "trainer_ids": ["master_arden"],
        "vendor_recipe_ids": ["craft_iron_dagger", "craft_iron_longsword", "craft_wolfbone_axe"],
    },
    {
        "id": "willowmere",
        "name": "Willowmere",
        "type": "river_settlement",
        "region": "blackmoor_reach",
        "continent": "aetheria",
        "desc": "A quiet town of white stone and willow trees. The herbalists of Willowmere brew remedies for any ailment.",
        "specialty": "Herbalist Guild — healing potions, antidotes, and rare herb recipes.",
        "services": ["market", "notice_board", "alchemist", "trainers"],
        "fast_travel_cost": 25,
        "market_items": ["wild_herb", "river_stone", "wisp_essence", "greater_healing_potion", "antidote", "bandage",
                         "leather_cap", "leather_boots", "wolfpelt_cloak", "wolf_tooth_pendant",
                         "copper_ring", "ring_of_grace", "amulet_of_warding", "tattered_cape"],
        "trainer_ids": ["elder_lyria"],
        "vendor_recipe_ids": ["craft_minor_healing_potion", "craft_greater_healing_potion", "craft_antidote"],
    },
    # ==================== VULKAROS (Orc capital, mining outpost) ====================
    {
        "id": "emberhold",
        "name": "Emberhold",
        "type": "warband_capital",
        "region": "emberreach",
        "continent": "vulkaros",
        "desc": "The Liberator's seat. Basalt walls streaked red with vein-forges. Warhorns sound at every hour.",
        "specialty": "Warband Hall — recruit orc mercenaries and train fear-resist skills.",
        "services": ["sanctuary", "market", "trainers", "notice_board", "tavern"],
        "sanctuary_cost": 25,
        "fast_travel_cost": 60,
        "market_items": ["iron_ore", "wolf_pelt", "greater_healing_potion", "bandage",
                         "iron_longsword", "bronze_mace", "bone_shield", "iron_helm",
                         "boarhide_vest", "leather_leggings", "amulet_of_warding", "ring_of_might"],
        "trainer_ids": [],
        "vendor_recipe_ids": ["craft_iron_longsword", "craft_wolfbone_axe"],
    },
    {
        "id": "ashvault",
        "name": "Ashvault",
        "type": "mining_outpost",
        "region": "zaheer_march",
        "continent": "vulkaros",
        "desc": "A grim mining post carved into a basalt bluff. Ore, ash, and iron-hard drink.",
        "specialty": "Mining Foreman — deeper ore veins and volcanic gem recipes.",
        "services": ["market", "notice_board", "trainers"],
        "fast_travel_cost": 60,
        "market_items": ["iron_ore", "copper_ore", "relic_shard", "acid_flask_item", "bandage", "minor_healing_potion",
                         "iron_dagger", "leather_cap", "worn_trousers", "old_boots",
                         "tattered_cape", "copper_ring", "wolf_tooth_pendant", "bone_shield"],
        "trainer_ids": [],
        "vendor_recipe_ids": ["craft_iron_dagger"],
    },
    # ==================== NYXMOOR (Haunted priory, witch outpost) ====================
    {
        "id": "mourngate",
        "name": "Mourngate",
        "type": "haunted_priory",
        "region": "hollow_fen",
        "continent": "nyxmoor",
        "desc": "A pale-stone priory ringed by mist. The wards flicker; the bells never quite stop tolling.",
        "specialty": "Wardkeepers — cleansing rites, curse removal, and rare warding scrolls.",
        "services": ["sanctuary", "market", "notice_board", "alchemist", "runesmith"],
        "sanctuary_cost": 30,
        "fast_travel_cost": 90,
        "market_items": ["wisp_essence", "ghast_dust", "greater_healing_potion", "antidote", "skillbook_ward",
                         "sages_hood", "sages_robe", "pendant_of_insight", "band_of_essence",
                         "essence_stud", "amulet_of_warding", "sages_trousers"],
        "trainer_ids": [],
        "vendor_recipe_ids": ["craft_antidote", "craft_greater_healing_potion"],
    },
    {
        "id": "black_hollow",
        "name": "Black Hollow",
        "type": "witch_outpost",
        "region": "wraith_scar",
        "continent": "nyxmoor",
        "desc": "A sunken hamlet ringed by black willow. Hags trade whispers for coin.",
        "specialty": "Coven Market — curses, hexes, and forbidden alchemy.",
        "services": ["market", "notice_board", "alchemist", "tavern"],
        "fast_travel_cost": 90,
        "market_items": ["ghast_dust", "wisp_essence", "serpent_venom", "acid_flask_item", "skillbook_purge",
                         "sages_trousers", "boots_of_the_mire", "robe_of_the_mire",
                         "earring_of_resolve", "ring_of_grace", "cloak_of_shadows"],
        "trainer_ids": [],
        "vendor_recipe_ids": ["craft_antidote"],
    },
    # ==================== FROSTHELM (Dwarven capital, frontier watch) ====================
    {
        "id": "khaz_moroth",
        "name": "Khaz Moroth",
        "type": "dwarven_capital",
        "region": "undermountain_hall",
        "continent": "frosthelm",
        "desc": "The great hall of the Undermountain. Jahra veins run through the walls; every hearth sings.",
        "specialty": "Jahra Forge — masterwork dwarven weapons and armor unlockable only here.",
        "services": ["sanctuary", "market", "trainers", "notice_board", "tavern"],
        "sanctuary_cost": 40,
        "fast_travel_cost": 120,
        "market_items": ["iron_ore", "copper_ore", "jahra_ingot", "greater_healing_potion",
                         "iron_longsword", "iron_greatsword", "iron_helm", "iron_greaves",
                         "ironshod_boots", "iron_kite_shield", "scaled_hauberk", "bone_shield"],
        "trainer_ids": [],
        "vendor_recipe_ids": ["craft_iron_longsword", "craft_wolfbone_axe"],
    },
    {
        "id": "frostwatch",
        "name": "Frostwatch",
        "type": "frontier_fort",
        "region": "stone_wardens",
        "continent": "frosthelm",
        "desc": "A palisade fort ringed by tundra and wyrm-tracks. The wardens keep the pass at any cost.",
        "specialty": "Warden Hall — pelt tanning, wyrm-hunting bounties, cold-forged bows.",
        "services": ["market", "notice_board", "trainers"],
        "fast_travel_cost": 120,
        "market_items": ["wolf_pelt", "boar_hide", "minor_healing_potion", "bandage",
                         "oak_shortbow", "ashwood_longbow", "leather_cap", "leather_boots",
                         "leather_leggings", "wolfpelt_cloak", "wolf_skull_helm", "wolf_tooth_pendant"],
        "trainer_ids": [],
        "vendor_recipe_ids": ["craft_iron_dagger"],
    },
    # ==================== ZEPHYRIA (Elven sky capital, sky watch) ====================
    {
        "id": "sun_moon_haven",
        "name": "Sun-Moon Haven",
        "type": "sky_capital",
        "region": "haya_ascendant",
        "continent": "zephyria",
        "desc": "A city of silver spires suspended between two suns. Elven choirs guide travellers home.",
        "specialty": "Sun-Moon Sanctum — celestial magic training and star-forged trinkets.",
        "services": ["sanctuary", "market", "trainers", "notice_board", "tavern", "alchemist"],
        "sanctuary_cost": 55,
        "fast_travel_cost": 160,
        "market_items": ["wisp_essence", "relic_shard", "jahra_ingot", "greater_healing_potion",
                         "riverstone_staff", "sages_hood", "sages_robe", "ring_of_twin_moons",
                         "essence_stud", "pendant_of_insight", "scholars_mantle", "sages_trousers"],
        "trainer_ids": [],
        "vendor_recipe_ids": ["craft_greater_healing_potion"],
    },
    {
        "id": "windrest",
        "name": "Windrest",
        "type": "sky_watch",
        "region": "stormpeaks",
        "continent": "zephyria",
        "desc": "A tower-post at the storm's edge. Sky-Riders rest here between lightning-runs.",
        "specialty": "Sky-Rider Post — mounts, wind-forged bows, and storm-charm crafting.",
        "services": ["market", "notice_board"],
        "fast_travel_cost": 160,
        "market_items": ["oak_shortbow", "wisp_essence", "minor_healing_potion", "bandage", "antidote",
                         "leather_boots", "wolfpelt_cloak", "ring_of_grace", "stud_of_the_quiet",
                         "tattered_cape", "leather_cap", "copper_ring"],
        "trainer_ids": [],
        "vendor_recipe_ids": [],
    },
    # ==================== SABLEWASTE (Trade bazaar, nomad camp) ====================
    {
        "id": "sun_bazaar",
        "name": "Sun Bazaar",
        "type": "trade_oasis",
        "region": "mirage_dunes",
        "continent": "sablewaste",
        "desc": "A jewel of gold canvas and running water. Every rare thing is sold here — for a price you may regret.",
        "specialty": "Grand Bazaar — legendary rarities, djinn contracts, mirage silks.",
        "services": ["sanctuary", "market", "trainers", "notice_board", "tavern", "alchemist"],
        "sanctuary_cost": 70,
        "fast_travel_cost": 220,
        "market_items": ["jahra_ingot", "relic_shard", "greater_healing_potion",
                         "scaled_hauberk", "riverstone_staff", "knights_bastard_sword",
                         "crown_of_will", "heartstone_amulet", "signet_of_old_road",
                         "iron_kite_shield", "ironshod_boots", "skillbook_smite"],
        "trainer_ids": [],
        "vendor_recipe_ids": ["craft_greater_healing_potion"],
    },
    {
        "id": "whispering_cairns",
        "name": "Whispering Cairns",
        "type": "nomad_camp",
        "region": "broken_djinnhold",
        "continent": "sablewaste",
        "desc": "A moving camp of tents pitched between old ruins. The djinn-touched trade dreams for bread.",
        "specialty": "Djinn Broker — one wish per week, if you can pay its riddle.",
        "services": ["market", "notice_board"],
        "fast_travel_cost": 220,
        "market_items": ["relic_shard", "wisp_essence", "acid_flask_item", "antidote", "bandage",
                         "copper_ring", "stud_of_the_quiet", "wolf_tooth_pendant", "tattered_cape",
                         "old_boots", "worn_trousers", "earring_of_resolve", "leather_boots"],
        "trainer_ids": [],
        "vendor_recipe_ids": [],
    },
    # ==================== VERDANIA (Sylvan tree-city, undersea gate) ====================
    {
        "id": "emerald_bough",
        "name": "Emerald Bough",
        "type": "sylvan_treecity",
        "region": "deep_verdant",
        "continent": "verdania",
        "desc": "A city grown, not built — sylvan homes carved into living branches wider than roads.",
        "specialty": "Grove Circle — druidic training, living armor, and canopy-forged bows.",
        "services": ["sanctuary", "market", "trainers", "notice_board", "tavern", "alchemist"],
        "sanctuary_cost": 85,
        "fast_travel_cost": 280,
        "market_items": ["oak_log", "wild_herb", "wisp_essence", "greater_healing_potion",
                         "oak_shortbow", "ashwood_longbow", "leather_cap", "sages_hood",
                         "ring_of_grace", "tide_walker_sandals", "cloak_of_shadows", "skillbook_thornlash"],
        "trainer_ids": [],
        "vendor_recipe_ids": ["craft_greater_healing_potion"],
    },
    {
        "id": "atlantyrion_gate",
        "name": "Atlantyrion Gate",
        "type": "undersea_gateway",
        "region": "coral_gates",
        "continent": "verdania",
        "desc": "A shell-white pier where pearl divers, tidebound priests, and Hyliondrian envoys pass between worlds.",
        "specialty": "Tide Court — aquatic training, orb-shard trading, and tidebound relics.",
        "services": ["sanctuary", "market", "trainers", "notice_board", "alchemist"],
        "sanctuary_cost": 90,
        "fast_travel_cost": 280,
        "market_items": ["serpent_scale", "serpent_venom", "wisp_essence", "orb_fragment", "greater_healing_potion", "antidote",
                         "tide_walker_sandals", "leggings_of_the_tide", "serpent_fang_dagger",
                         "heartstone_amulet", "band_of_essence", "mantle_of_the_deep"],
        "trainer_ids": [],
        "vendor_recipe_ids": ["craft_antidote"],
    },
]

# ============================================================
# Canon migration — rewrite all town/region/continent references from the
# legacy codenames (Ironhold/Aetheria/etc.) to the canon (Oathspire/Valeria/etc.).
# Also swaps in canonical hometown names + descriptions where relevant.
# ============================================================
from world_data import CONTINENT_ID_MAP, TOWN_ID_MAP, HOMETOWN_BY_CONTINENT  # noqa: E402

# Canonical hometown display names + descriptions, keyed by the *new* id.
_CANONICAL_TOWN_META: dict[str, dict] = {
    "oathspire":       {"name": "Oathspire",       "type": "imperial_capital",
                        "desc": "The imperial capital of Valeria. Cathedrals ring the hour with a hundred bells and every knight has an oath to spend.",
                        "specialty": "The Grand Teleporter, the Emperor's Forge, and the Federated Bank — the heart of continental commerce."},
    "riverguard":      {"name": "Riverguard",      "type": "river_sanctuary",
                        "desc": "A quiet river town of white stone and willow trees. The priests of Riverguard heal any wound — for the right price.",
                        "specialty": "Sanctuary — priests remove status effects instantly and train healing skills."},
    "grunhold":        {"name": "Grunhold",        "type": "orc_capital",
                        "desc": "The Liberator's seat. Basalt walls streaked red with vein-forges. Warhorns sound at every hour.",
                        "specialty": "Warband Hall — recruit orc mercenaries and train fear-resist skills."},
    "warforge":        {"name": "Warforge",        "type": "war_outpost",
                        "desc": "A grim outpost carved into a basalt bluff. Ore, ash, and iron-hard drink.",
                        "specialty": "War Foreman — deeper ore veins and volcanic weapon recipes."},
    "elaris":          {"name": "Elaris",          "type": "half_elf_capital",
                        "desc": "The federation's shining capital — a city that speaks every language and taxes none too heavily.",
                        "specialty": "Grand Bazaar and Diplomatic Hall — hybrid recipes, foreign brokers, and every embassy of note."},
    "silvergate":      {"name": "Silvergate",      "type": "caravan_hub",
                        "desc": "A caravan hub where the Silverroad crosses the eastern march. Bards, brokers, and beguiling deals.",
                        "specialty": "Caravan Master — long-haul contracts and remote-shipping arrangements."},
    "jahrahold":       {"name": "Jahrahold",       "type": "dwarven_capital",
                        "desc": "The great hall of the Undermountain. Jahra veins run through the walls; every hearth sings.",
                        "specialty": "Jahra Forge — masterwork dwarven weapons and armor unlockable only here."},
    "deepstone":       {"name": "Deepstone",       "type": "frontier_watch",
                        "desc": "A palisade fort ringed by crystal caverns and wyrm-tracks. The wardens keep the pass at any cost.",
                        "specialty": "Warden Hall — pelt tanning, wyrm-hunting bounties, and cold-forged bows."},
    "solunara":        {"name": "Solunara",        "type": "sky_capital",
                        "desc": "A city of silver spires suspended between two suns. Elven choirs guide travellers home.",
                        "specialty": "Sun-Moon Sanctum — celestial magic training and star-forged trinkets."},
    "starfall_watch":  {"name": "Starfall Watch",  "type": "sky_watch",
                        "desc": "A tower-post at the storm's edge. Sky-Riders rest here between lightning-runs.",
                        "specialty": "Sky-Rider Post — mounts, wind-forged bows, and storm-charm crafting."},
    "rindivar_grove":  {"name": "Rindivar Grove",  "type": "wildblood_capital",
                        "desc": "A ring of ancient totems where the Primal Sovereignty raises the young of every Aspect. Fires burn all night.",
                        "specialty": "Totem Circle — Beast Aspect training and pack-bonding rites."},
    "beastcairn":      {"name": "Beastcairn",      "type": "nomad_camp",
                        "desc": "A moving camp of tents pitched between old totems. The djinn-touched trade dreams for bread.",
                        "specialty": "Djinn Broker — one wish per week, if you can pay its riddle."},
    "atlantyrion":     {"name": "Atlantyrion",     "type": "undersea_capital",
                        "desc": "The pearl-white capital of the Underwater Kingdom. Coral bridges span the tide and every window is a lantern of light.",
                        "specialty": "Tide Court — aquatic training, orb-shard trading, and tidebound relics."},
    "veilgrove":       {"name": "Veilgrove",       "type": "sylvan_treecity",
                        "desc": "The Mystleaf Council's seat — a city grown, not built, into living branches wider than roads.",
                        "specialty": "Grove Circle — druidic training, living armor, and canopy-forged bows."},
}


TRADE_NPCS = {
    "oathspire": {"id": "oathspire_trade", "name": "Aldric the Broker", "title": "Federated Broker", "desc": "If it can be counted, weighed, or sworn, Aldric has a rate for it.", "specialties": ["merchant", "cooking", "blacksmithing", "tailoring", "cartography"]},
    "riverguard": {"id": "sister_maren", "name": "Sister Maren", "title": "Sanctuary Herbalist", "desc": "The river teaches patience, and Sister Maren brews it into every draught.", "specialties": ["herbalism", "alchemy", "enchanting", "cooking", "tailoring"]},
    "grunhold": {"id": "gorash_bone_anvil", "name": "Gorash Bone-Anvil", "title": "Orc War-Smith", "desc": "Every hammer-strike is a war cry.", "specialties": ["blacksmithing", "armorsmithing", "mining", "leatherworking", "hunting"]},
    "warforge": {"id": "thazka_emberhand", "name": "Thazka Emberhand", "title": "Volcanic Smith", "desc": "She folds ash and ore into blades that thirst.", "specialties": ["blacksmithing", "armorsmithing", "mining", "engineering", "leatherworking"]},
    "elaris": {"id": "vex_elenor", "name": "Vex Elenor", "title": "Gem Broker", "desc": "Half-Elf coins spend twice as fast when they shine.", "specialties": ["jewelcrafting", "merchant", "enchanting", "tailoring", "blacksmithing"]},
    "silvergate": {"id": "karvo_caravan", "name": "Karvo the Caravan Master", "title": "Long-Haul Trader", "desc": "He knows every road and every road knows his price.", "specialties": ["merchant", "cartography", "leatherworking", "cooking", "engineering"]},
    "jahrahold": {"id": "brunmir_deep_finger", "name": "Brunmir Deep-Finger", "title": "Jahra Smith", "desc": "The mountain gave him hands that remember every vein.", "specialties": ["mining", "blacksmithing", "armorsmithing", "engineering", "jewelcrafting"]},
    "deepstone": {"id": "hildra_cold_forge", "name": "Hildra Cold-Forge", "title": "Frontier Smith", "desc": "Cold steel, cold eyes, warm ale.", "specialties": ["mining", "leatherworking", "bow_crafting", "engineering", "armorsmithing"]},
    "solunara": {"id": "serathiel_moonglow", "name": "Serathiel Moonglow", "title": "Celestial Enchanter", "desc": "Moonlight is merely starlight wearing a softer mask.", "specialties": ["enchanting", "herbalism", "alchemy", "bow_crafting", "tailoring"]},
    "starfall_watch": {"id": "vaelion_sky_rider", "name": "Vaelion Sky-Rider", "title": "Storm Bowyer", "desc": "Arrows that outrun the wind, or so he claims.", "specialties": ["bow_crafting", "leatherworking", "enchanting", "engineering", "cartography"]},
    "rindivar_grove": {"id": "rin_totem_speaker", "name": "Rin Totem-Speaker", "title": "Primal Crafter", "desc": "The beasts give, the beasts take, and Rin keeps the count.", "specialties": ["hunting", "leatherworking", "beast_taming", "herbalism", "cooking"]},
    "beastcairn": {"id": "mirage_djinn", "name": "Mirage the Djinn-Touched", "title": "Nomad Trader", "desc": "Dreams for bread, bread for dreams.", "specialties": ["hunting", "leatherworking", "cooking", "merchant", "excavation"]},
    "atlantyrion": {"id": "thalassa_pearlwarden", "name": "Thalassa Pearlwarden", "title": "Tide Forger", "desc": "The ocean yields ingredients; Thalassa yields wonders.", "specialties": ["fishing", "alchemy", "herbalism", "jewelcrafting", "enchanting"]},
    "veilgrove": {"id": "willowen_rootweaver", "name": "Willowen Rootweaver", "title": "Mystleaf Artisan", "desc": "Branches bend for those who know how to ask.", "specialties": ["herbalism", "alchemy", "bow_crafting", "logging", "enchanting"]},
}


# Region ids referenced by legacy QUESTS need to be rewritten too.
_REGION_ID_MAP: dict[str, str] = {
    "vale_of_elder_kings": "vale_of_oaths",
    "blackmoor_reach":     "riverguard_march",
    "emberreach":          "liberators_heart",
    "zaheer_march":        "warforge_march",
    "hollow_fen":          "elaris_reach",
    "wraith_scar":         "silvergate_pass",
    "undermountain_hall":  "jahra_holdfast",
    "stone_wardens":       "deepstone_watch",
    "haya_ascendant":      "solunara_ascendant",
    "stormpeaks":          "starfall_march",
    "mirage_dunes":        "rindivar_reach",
    "broken_djinnhold":    "beastcairn_pass",
    "deep_verdant":        "veilgrove_hollow",
    "coral_gates":         "atlantyrion_gate",
}

# Notice-board giver ids used by regional quests reference old town ids.
_GIVER_ID_MAP: dict[str, str] = {
    "ironhold_notice_board":          "oathspire_notice_board",
    "willowmere_notice_board":        "riverguard_notice_board",
    "emberhold_notice_board":         "grunhold_notice_board",
    "ashvault_notice_board":          "warforge_notice_board",
    "mourngate_notice_board":         "elaris_notice_board",
    "black_hollow_notice_board":      "silvergate_notice_board",
    "khaz_moroth_notice_board":       "jahrahold_notice_board",
    "frostwatch_notice_board":        "deepstone_notice_board",
    "sun_moon_haven_notice_board":    "solunara_notice_board",
    "windrest_notice_board":          "starfall_watch_notice_board",
    "sun_bazaar_notice_board":        "rindivar_grove_notice_board",
    "whispering_cairns_notice_board": "beastcairn_notice_board",
    "emerald_bough_notice_board":     "veilgrove_notice_board",
    "atlantyrion_gate_notice_board":  "atlantyrion_notice_board",
}


def _apply_canon_migration() -> None:
    # 1. TOWNS — rewrite id / region / continent + canonical name/desc/specialty.
    _hometown_ids = set(HOMETOWN_BY_CONTINENT.values())
    for t in TOWNS:
        new_id = TOWN_ID_MAP.get(t["id"], t["id"])
        t["id"] = new_id
        t["region"] = _REGION_ID_MAP.get(t.get("region"), t.get("region"))
        t["continent"] = CONTINENT_ID_MAP.get(t.get("continent"), t.get("continent"))
        t["hometown"] = new_id in _hometown_ids
        meta = _CANONICAL_TOWN_META.get(new_id)
        if meta:
            t["name"] = meta["name"]
            t["type"] = meta.get("type", t.get("type"))
            t["desc"] = meta["desc"]
            t["specialty"] = meta["specialty"]
            t.setdefault("trade_npc", TRADE_NPCS.get(new_id))

    # 2. Special-case: Veilgrove is now the Sylvan capital in Daw'ul Talalu, not Hylion.
    for t in TOWNS:
        if t["id"] == "veilgrove":
            t["continent"] = "daw_ul_talalu"
            t["region"] = "veilgrove_hollow"
        elif t["id"] == "atlantyrion":
            t["continent"] = "hylion"
            t["region"] = "atlantyrion_gate"

    # 3. QUESTS — rewrite region + giver references.
    for q in QUESTS:
        q["region"] = _REGION_ID_MAP.get(q.get("region"), q.get("region"))
        q["giver"] = _GIVER_ID_MAP.get(q.get("giver"), q.get("giver"))


# ============================================================
# QUESTS — Regional and Story quests (separate from daily missions)
# ============================================================
# category: regional | story | event
QUESTS: list[dict] = [
    # ---------- Regional (Aetheria) ----------
    {
        "id": "regional_wolf_menace",
        "category": "regional",
        "board": "lounge",
        "town_id": "oathspire",
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
        "board": "lounge",
        "town_id": "oathspire",
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
        "board": "notice",
        "town_id": "riverguard",
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
        "board": "notice",
        "town_id": "riverguard",
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

# ============================================================
# Auto-generated notice board quests — ~10 per town,
# biome-appropriate kill/gather/action quests. See gen_npcs.py.
# ============================================================
from gen_npcs import generate_notice_board_quests  # noqa: E402
QUESTS.extend(generate_notice_board_quests())

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


# ============================================================
# Heritage Rank Progression — costs and stat rewards
# ============================================================

# Heritage point cost to reach each rank (index 0 = Rank 2, etc.)
# No longer used — rank-up requires full resource bar + level gate

# Level gate: must be at least this level to reach each rank
HERITAGE_RANK_LEVEL_REQS = [10, 20, 30, 40]

# Permanent stat bonuses per rank-up, per race — REMOVED in favor of Heritage Surge
# Heritage Surge: powerful temporary buff, duration + cooldown scale with rank

HERITAGE_SURGE_RANK_CONFIG = [
    {"duration": 3, "cooldown_hours": 24},   # Rank 2
    {"duration": 4, "cooldown_hours": 18},   # Rank 3
    {"duration": 5, "cooldown_hours": 12},   # Rank 4
    {"duration": 5, "cooldown_hours": 8},    # Rank 5
]

HERITAGE_SURGES: dict[str, dict] = {
    "human": {
        "id": "oathbreaker_resolve",
        "name": "Oathbreaker's Resolve",
        "desc": "All actions count as critical success for the surge duration.",
        "effects": {"force_outcome": 6},
        "narrative": "You shatter every oath that ever bound you. For a heartbeat, the world bends to your will — every strike true, every word sharp, every gamble certain.",
    },
    "elf": {
        "id": "celestial_conjunction",
        "name": "Celestial Conjunction",
        "desc": "Both solar and lunar bonuses active at once: +6 strike, -30% damage taken, +10% heal.",
        "effects": {"strike_bonus": 6, "damage_taken_mult": 0.70, "heal_mult": 1.10, "dual_celestial": True},
        "narrative": "Sun and Moon collide in the sky above you. Both celestial tides flood your veins at once — starlight and sunlight, blade and grace, wrath and mercy.",
    },
    "dwarf": {
        "id": "mountain_wrath",
        "name": "Mountain's Wrath",
        "desc": "Take 50% less damage, immune to debuffs, and repair armor 10% per action.",
        "effects": {"damage_taken_mult": 0.50, "debuff_immune": True, "armor_repair_pct": 10},
        "narrative": "The mountain wakes inside your bones. Stone-hard, ancient, unbreakable — you become the wall that no army has ever crossed.",
    },
    "half_elf": {
        "id": "dual_awakening",
        "name": "Dual Awakening",
        "desc": "Both heritages fully active: full elf + full human bonuses, +2 to all racial resources.",
        "effects": {"strike_bonus": 4, "heal_mult": 1.10, "damage_taken_mult": 0.85, "resource_boost": 2},
        "narrative": "Both bloodlines roar awake at once — elf and human, moon and iron, grace and grit. You are no longer half of anything. You are whole.",
    },
    "orc": {
        "id": "unchained_fury",
        "name": "Unchained Fury",
        "desc": "+10 strike, immune to control/fear, every hit deals double damage.",
        "effects": {"strike_bonus": 10, "control_immune": True, "damage_mult": 2.0},
        "narrative": "The chains inside you snap. Not the iron ones — the deeper ones. The ones that said 'know your place.' Fury becomes geometry. Every blow lands twice.",
    },
    "wildblood": {
        "id": "primal_overdrive",
        "name": "Primal Overdrive",
        "desc": "+8 strike, +15% evasion, 25% lifesteal for the surge duration.",
        "effects": {"strike_bonus": 8, "evasion_bonus": 15, "lifesteal_pct": 25},
        "narrative": "The beast inside stops whispering and screams. Your veins run hot with primal fire — strike like a predator, dodge like a ghost, drink the life of your enemies.",
    },
    "hyliondrian": {
        "id": "tidal_cataclysm",
        "name": "Tidal Cataclysm",
        "desc": "Instantly heal 50% HP, then +10% heal per action, immune to debuffs.",
        "effects": {"instant_heal_pct": 50, "heal_per_action_pct": 10, "debuff_immune": True},
        "narrative": "The ocean answers your call — not as a wave, but as a cataclysm. Salt water floods your wounds, closes them, remakes you. Every breath heals. No poison, no curse, no rot can touch you.",
    },
    "sylvan": {
        "id": "verdant_bloom",
        "name": "Verdant Bloom",
        "desc": "+20% evasion, +30% stealth, gather yields 3x materials, immune to detection.",
        "effects": {"evasion_bonus": 20, "stealth_bonus": 30, "gather_mult": 3, "detection_immune": True},
        "narrative": "The forest blooms inside you. Leaves unfurl from your skin, roots weave through your shadow. You are the green — unseen, untouchable, abundant. The land gives triple to its child.",
    },
}

# Passive multiplier per rank (1.0 at Rank 1, 2.0 at Rank 5)
HERITAGE_RANK_MULT = [1.0, 1.25, 1.5, 1.75, 2.0]


def get_town(town_id: str) -> dict | None:
    return TOWNS_BY_ID.get(town_id)
def get_quest(quest_id: str) -> dict | None:
    return QUESTS_BY_ID.get(quest_id)
def get_active_events(weekday: int) -> list[dict]:
    """Given today's weekday (0=Mon..6=Sun), return which events are active."""
    active = []
    for e in EVENTS:
        if -1 in e["schedule_days"] or weekday in e["schedule_days"]:
            active.append(e)
    return active


def default_home_town_for_race(race_id: str) -> str:
    """Race's canonical starting town per the v2 world spec."""
    from world_data import HOMELAND_TOWN_BY_RACE
    return HOMELAND_TOWN_BY_RACE.get(race_id, "oathspire")


def default_home_continent_for_race(race_id: str) -> str:
    """Race's canonical home continent per the v2 world spec."""
    from world_data import HOMETOWN_BY_CONTINENT
    home_town = default_home_town_for_race(race_id)
    for cont, town in HOMETOWN_BY_CONTINENT.items():
        if town == home_town:
            return cont
    return "valeria"


def default_home_biome_for_race(race_id: str) -> str:
    """First biome the character sees — always the tier-1 biome of their home continent."""
    from world_data import CONTINENTS_V2
    cont_id = default_home_continent_for_race(race_id)
    for c in CONTINENTS_V2:
        if c["id"] == cont_id and c.get("biomes"):
            return c["biomes"][0]["id"]
    return "golden_plains"


# Apply migration now that TOWNS + QUESTS lists are populated.
_apply_canon_migration()
TOWNS_BY_ID = {t["id"]: t for t in TOWNS}
