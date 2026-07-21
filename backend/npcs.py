"""NPC + Story Quest System.

Each of the 8 canonical hometowns has one flagship NPC who tells a personal
story across three relationship-gated quests. Completing quests raises the
character's relationship with that NPC, which unlocks new dialogue, unique
rewards, and the next quest in the chain.

Data schema:
NPC:
  id: str                — machine id
  name: str              — display name
  race: str
  town: str              — home town id
  continent: str
  title: str             — subtitle shown under the name
  description: str       — flavour paragraph
  personality: str       — one-line tone
  quests: list[dict]     — see Quest

Quest:
  id: str
  npc_id: str
  tier: str              — required relationship tier to accept (stranger/acquainted/friend)
  order: int             — quest chain order (1, 2, 3)
  name: str
  brief: str             — narrator setup (before accepting)
  narrative: dict        — {accept, complete} — story beats
  requirements: dict     — {kills?, gathers?, character_level?}
  rewards: dict          — {gold, xp, relationship, items?, unique_item?}
"""
from __future__ import annotations


# ============================================================
# RELATIONSHIP TIERS
# ============================================================
RELATIONSHIP_TIERS: list[str] = ["stranger", "acquainted", "friend", "trusted", "bonded"]
RELATIONSHIP_THRESHOLDS: dict[str, int] = {
    "stranger":    0,
    "acquainted":  200,
    "friend":      600,
    "trusted":     1200,
    "bonded":      2000,
}


def relationship_tier_from_points(points: int) -> str:
    lvl = "stranger"
    for name in RELATIONSHIP_TIERS:
        if points >= RELATIONSHIP_THRESHOLDS[name]:
            lvl = name
    return lvl


def tier_meets(current: str, required: str) -> bool:
    return RELATIONSHIP_TIERS.index(current) >= RELATIONSHIP_TIERS.index(required)


# ============================================================
# NPCs — one flagship per hometown, three quests each
# ============================================================
NPCS: list[dict] = [
    # ---------------- VALERIA / OATHSPIRE ----------------
    {
        "id": "captain_ansel",
        "name": "Captain Ansel of the Iron Gate",
        "race": "human", "town": "oathspire", "continent": "valeria",
        "title": "Weary Commander of the Imperial Watch",
        "description": ("Once a border-knight who lost his squire on the Ashen frontier, "
                        "Ansel now trains new recruits and keeps a quieter oath than the Empire's."),
        "personality": "Blunt. Fair. Watches your hands, never your face.",
        "quests": [
            {"id": "q_ansel_1", "npc_id": "captain_ansel", "tier": "stranger", "order": 1,
             "name": "The Missing Patrol",
             "brief": "Three of my watchmen never came back from Crownwood. Find any trace.",
             "narrative": {
                "accept": ("Ansel unfolds a stained map. 'Third squad, went east three days ago. Just a scout run. "
                           "Bring me their patrol tokens. Bring back the men if you can.'"),
                "complete": ("You lay three tokens on the table. Ansel closes his eyes. 'Not what I hoped. "
                             "But I know now. That's worth something.' He slides a purse across the wood.")
             },
             "requirements": {"kills": [("highway_bandit", 3)]},
             "rewards": {"gold": 120, "xp": 80, "relationship": 220}},
            {"id": "q_ansel_2", "npc_id": "captain_ansel", "tier": "acquainted", "order": 2,
             "name": "The Shepherd's Daughter",
             "brief": "A shepherd's girl was taken near Ashen Border. The Empire won't ride out. I will.",
             "narrative": {
                "accept": ("'Not my patrol. Not my orders. Not my problem. Except it is.' Ansel hands you his second sword. "
                           "'Bring her home. Kill anything that isn't her.'"),
                "complete": ("The girl clings to Ansel's coat and won't let go. He kneels in the mud and looks up at you. "
                             "'You have my sword. And a name. Use them both wisely.'")
             },
             "requirements": {"kills": [("gray_wolf", 4), ("ruin_ghast", 2)]},
             "rewards": {"gold": 350, "xp": 200, "relationship": 400,
                         "items": [("greater_healing_potion", 3)]}},
            {"id": "q_ansel_3", "npc_id": "captain_ansel", "tier": "friend", "order": 3,
             "name": "The Iron Oath",
             "brief": "There's a blade my squire carried the day he fell. I want it back. And I want it in your hand.",
             "narrative": {
                "accept": ("Ansel does not look at you as he speaks. 'His name was Thom. Fifteen years old. "
                           "Ashen Border, near the crooked oak. The blade is called Vigilkeeper. I made it. He kept it.'"),
                "complete": ("Ansel takes the blade, kisses the pommel, and offers it back to you hilt-first. "
                             "'Vigilkeeper doesn't rest, and neither should the one who carries it. Yours now.'")
             },
             "requirements": {"kills": [("ruin_ghast", 6)], "character_level": 5},
             "rewards": {"gold": 800, "xp": 500, "relationship": 700,
                         "unique_item": {"id": "vigilkeeper", "name": "Vigilkeeper (Ansel's Blade)",
                                         "rarity": "epic", "kind": "weapon", "power": 18, "slot": "weapon"}}},
        ],
    },
    # ---------------- MUSHKARA / GRUNHOLD ----------------
    {
        "id": "warchief_thraka",
        "name": "War-Chief Thraka Ironjaw",
        "race": "orc", "town": "grunhold", "continent": "mushkara",
        "title": "Third of the Liberator's Blood",
        "description": ("Grand-daughter of Zaheer himself, Thraka refuses her seat on the Dominion council "
                        "and prefers the forge to the parliament. Rumours say she has broken more chains than the Liberator."),
        "personality": "Loud. Direct. Laughs like an anvil dropped from a rooftop.",
        "quests": [
            {"id": "q_thraka_1", "npc_id": "warchief_thraka", "tier": "stranger", "order": 1,
             "name": "Iron From the Scar",
             "brief": "The forges are hungry. Bring me raw bloodiron from the Iron Scar. And prove you can carry it.",
             "narrative": {
                "accept": "Thraka jerks a thumb at the eastern smoke. 'Iron Scar. Warhounds. Bring me eight raw ore.'",
                "complete": "'Not bad, softwalker. Not bad at all.' She weighs the ore. 'Come back when you want harder work.'",
             },
             "requirements": {"gathers": [("iron_ore", 8)]},
             "rewards": {"gold": 200, "xp": 140, "relationship": 240}},
            {"id": "q_thraka_2", "npc_id": "warchief_thraka", "tier": "acquainted", "order": 2,
             "name": "The Broken Chain",
             "brief": "A slaver's cell was reported in the Ash Barrens. Break every chain. Leave one for me.",
             "narrative": {
                "accept": ("'Slavers. In OUR ash.' Thraka spits. 'Every chain broken. Every chain — you hear me. "
                           "Leave one whole. I want to break it myself.'"),
                "complete": ("She takes the single unbroken chain from your hand, tests it, and snaps it in half with one pull. "
                             "The pieces fall to the floor. 'Now,' she says, 'now it is a good day.'"),
             },
             "requirements": {"kills": [("orc_grunt", 4), ("orc_warhound", 3)]},
             "rewards": {"gold": 500, "xp": 320, "relationship": 450,
                         "items": [("iron_ore", 5)]}},
            {"id": "q_thraka_3", "npc_id": "warchief_thraka", "tier": "friend", "order": 3,
             "name": "The Liberator's Anvil",
             "brief": "There is one anvil in Demonfall that survived the burning. Bring me the story of who guards it now.",
             "narrative": {
                "accept": ("Thraka is quiet for the first time. 'Zaheer's anvil. Deep in the crater. Something guards it now. "
                           "I need to know what. If it can be broken, I will break it. If it cannot — I will still try.'"),
                "complete": ("She listens. Then, slowly, she smiles. 'Thank you. You have earned this.' "
                             "She hands you a hammer whose head is the exact shape of a broken shackle."),
             },
             "requirements": {"kills": [("obsidian_wraith", 4)], "character_level": 10},
             "rewards": {"gold": 1200, "xp": 800, "relationship": 750,
                         "unique_item": {"id": "chainbreaker_hammer", "name": "Chainbreaker (Thraka's Hammer)",
                                         "rarity": "epic", "kind": "weapon", "power": 22, "slot": "weapon"}}},
        ],
    },
    # ---------------- CONCORDIA / ELARIS ----------------
    {
        "id": "envoy_seraphine",
        "name": "Envoy Seraphine Twinleaf",
        "race": "half_elf", "town": "elaris", "continent": "concordia",
        "title": "Federation Broker of Quiet Contracts",
        "description": ("Seraphine handles the deals no ambassador wants their name on. A trade in three tongues, "
                        "she keeps a rose-quill on her ear and a hidden dagger in her belt."),
        "personality": "Silky. Patient. Answers every question with a smile and half an answer.",
        "quests": [
            {"id": "q_sera_1", "npc_id": "envoy_seraphine", "tier": "stranger", "order": 1,
             "name": "The Amber Sample",
             "brief": "A vintner's boy stole a jar of prototype amber wine. I need it back, unopened.",
             "narrative": {
                "accept": ("Seraphine smiles behind her fan. 'A misunderstanding. Between friends. The boy went east along Silverroad. "
                           "Bring me the jar. Do not, please, taste it.'"),
                "complete": ("She takes the jar, sets it in a small silver crate, seals it with wax, and turns back to you. "
                             "'A pleasure. As agreed.' She slides a Federation credit-note across the desk."),
             },
             "requirements": {"kills": [("highway_bandit", 2)]},
             "rewards": {"gold": 250, "xp": 130, "relationship": 230}},
            {"id": "q_sera_2", "npc_id": "envoy_seraphine", "tier": "acquainted", "order": 2,
             "name": "The Silvergate Delegation",
             "brief": "A minor lord's delegation must arrive in Silvergate alive. Nothing more, nothing less.",
             "narrative": {
                "accept": ("'Six carriages. No livery. Slow pace. You will not be seen; if you are, you will not be recognised. "
                           "If they arrive, we all win. If they do not, no one in this room ever spoke.'"),
                "complete": ("The delegation arrives, dusty but whole. Seraphine hands you a slim envelope. "
                             "'A gift. Read it in private. Do not thank me publicly.'"),
             },
             "requirements": {"kills": [("bog_hag", 2), ("cursed_knight", 2)]},
             "rewards": {"gold": 620, "xp": 380, "relationship": 460,
                         "items": [("wisp_essence", 3)]}},
            {"id": "q_sera_3", "npc_id": "envoy_seraphine", "tier": "friend", "order": 3,
             "name": "The Broken Treaty",
             "brief": "The Federation's founding treaty was hidden in fragments. I have located two. Recover the third.",
             "narrative": {
                "accept": ("Seraphine sets her fan down, and for the first time you see her eyes without it. "
                           "'The Diplomat's Highlands. The old meeting hall. If a wraith holds the fragment — I will not ask you to spare it.'"),
                "complete": ("The three fragments align on her desk into a single sheet of pale silver. "
                             "Seraphine breathes out slowly. 'You have given me the shape of my life. Take this.' "
                             "The ring she offers is set with a bloom of Federation amber."),
             },
             "requirements": {"kills": [("specter_rider", 3), ("chain_wraith", 3)], "character_level": 14},
             "rewards": {"gold": 1600, "xp": 950, "relationship": 800,
                         "unique_item": {"id": "amber_diplomacy_ring", "name": "Amber Ring of the Federation",
                                         "rarity": "epic", "kind": "relic", "power": 0}}},
        ],
    },
    # ---------------- KHARDRUM / JAHRAHOLD ----------------
    {
        "id": "grandmaster_thora",
        "name": "Grandmaster Thora Deepvein",
        "race": "dwarf", "town": "jahrahold", "continent": "khardrum",
        "title": "Keeper of the Deep Forges",
        "description": ("Fifth-generation Deepvein, and the only one who ever refused a seat on the High Council. "
                        "Her forge burns Jahra hotter than any other in the Undermountain."),
        "personality": "Terse. Precise. Trusts hands more than words.",
        "quests": [
            {"id": "q_thora_1", "npc_id": "grandmaster_thora", "tier": "stranger", "order": 1,
             "name": "Vein Test",
             "brief": "Bring me twelve of clean Jahra ore. No slag, no crumbles. I test everyone who wants my time.",
             "narrative": {
                "accept": "Thora nods once. 'Ember Mines. Fresh vein. Nothing chipped from the walls. Twelve.'",
                "complete": "She weighs each ore in her palm before speaking. 'Good hands. Good eye. Come back.'",
             },
             "requirements": {"gathers": [("iron_ore", 12)]},
             "rewards": {"gold": 300, "xp": 200, "relationship": 250}},
            {"id": "q_thora_2", "npc_id": "grandmaster_thora", "tier": "acquainted", "order": 2,
             "name": "The Crystal Grief",
             "brief": "A troll-warband keeps breaking my Crystal Caverns dig. Clear them. All of them.",
             "narrative": {
                "accept": "'Three teams lost this month. Six good miners. I forge no new hammers until the caverns are clean.'",
                "complete": "She examines your gear, grunts, and hands you a whetstone as long as your forearm.",
             },
             "requirements": {"kills": [("cavern_troll", 3), ("crystal_lurker", 2)]},
             "rewards": {"gold": 700, "xp": 480, "relationship": 480,
                         "items": [("jahra_ingot", 2)]}},
            {"id": "q_thora_3", "npc_id": "grandmaster_thora", "tier": "friend", "order": 3,
             "name": "The Anvil-Song",
             "brief": "In the Deep Forges lies my mother's anvil. I would forge you a blade upon it.",
             "narrative": {
                "accept": ("Thora presses her palm to the wall, and it is warm. 'She was Grandmaster before me. "
                           "The anvil sings only for its own blood. Bring me the last frost-wyrm scale for the temper.'"),
                "complete": ("She works through the night. At dawn she offers you a spear so cold it steams. "
                             "'This is Marrowsong. Your blade now. Its story is my mother's. Carry it well.'"),
             },
             "requirements": {"kills": [("frost_wyrm_kin", 2)], "character_level": 22},
             "rewards": {"gold": 2000, "xp": 1200, "relationship": 850,
                         "unique_item": {"id": "marrowsong_spear", "name": "Marrowsong (Thora's Spear)",
                                         "rarity": "epic", "kind": "weapon", "power": 26, "slot": "weapon"}}},
        ],
    },
    # ---------------- HAYA / SOLUNARA ----------------
    {
        "id": "loremaster_sylanya",
        "name": "Loremaster Sylanya of the Sun-Moon Choir",
        "race": "elf", "town": "solunara", "continent": "haya",
        "title": "Warden of the Celestial Archive",
        "description": ("Older than most kingdoms, Sylanya keeps a library that indexes every dream the Higher Enclave "
                        "has recorded since the fall of the Great Tree. She sleeps four hours a decade."),
        "personality": "Kind. Patient. Answers your question with three of her own.",
        "quests": [
            {"id": "q_syl_1", "npc_id": "loremaster_sylanya", "tier": "stranger", "order": 1,
             "name": "Silverleaf Notes",
             "brief": "The choir needs new songbook parchment. Bring me eight silverleaf from Sunlit Canopy.",
             "narrative": {
                "accept": "'Softly, please. The leaves resent haste.'",
                "complete": "'You listened. That is rarer than the leaves themselves.'",
             },
             "requirements": {"gathers": [("wild_herb", 8)]},
             "rewards": {"gold": 380, "xp": 260, "relationship": 240}},
            {"id": "q_syl_2", "npc_id": "loremaster_sylanya", "tier": "acquainted", "order": 2,
             "name": "The Missing Cantor",
             "brief": "One of my cantors has not returned from Moonveil. She sang a dream I need her to explain.",
             "narrative": {
                "accept": "'Illusion creatures respect only the true and the terrified. Be either. Bring her home.'",
                "complete": "The cantor bows to you before she bows to Sylanya. Sylanya notices, and smiles.",
             },
             "requirements": {"kills": [("silverleaf_dryad", 2), ("griffon", 1)]},
             "rewards": {"gold": 820, "xp": 560, "relationship": 500,
                         "items": [("wisp_essence", 4)]}},
            {"id": "q_syl_3", "npc_id": "loremaster_sylanya", "tier": "friend", "order": 3,
             "name": "The First Verse",
             "brief": "There is a stanza we lost when the Tree fell. I have found where it drifted. Bring it home.",
             "narrative": {
                "accept": "'Celestial Ruins. A star-wraith carries the verse in the shape of a scar upon its throat. "
                          "It will not give the scar up gently.'",
                "complete": "Sylanya sings it once — one line — and every leaf in the courtyard turns to face her. "
                            "'Take this. I owe you a stanza; the world owes you the courtyard.'",
             },
             "requirements": {"kills": [("star_wraith", 2)], "character_level": 30},
             "rewards": {"gold": 2400, "xp": 1500, "relationship": 900,
                         "unique_item": {"id": "sun_moon_lute", "name": "The Sun-Moon Lute",
                                         "rarity": "epic", "kind": "relic", "power": 0}}},
        ],
    },
    # ---------------- GENNEL / RINDIVAR GROVE ----------------
    {
        "id": "matriarch_zerith",
        "name": "Matriarch Zerith of the Wandering Pack",
        "race": "wildblood", "town": "rindivar_grove", "continent": "gennel",
        "title": "Alpha of the Second Ring",
        "description": ("Zerith took over the Wandering Pack after her mate died fighting a demon-scarred lion. "
                        "She still wears his claw-necklace and speaks his name when she prays."),
        "personality": "Quiet. Watches everything. Sharp when she does speak.",
        "quests": [
            {"id": "q_zer_1", "npc_id": "matriarch_zerith", "tier": "stranger", "order": 1,
             "name": "Blood-Kin Trial",
             "brief": "Any traveller who walks with our pack must kill their first Beastwood predator. Alone.",
             "narrative": {
                "accept": "'One creature. Not a cub. Not a pup. Something that will fight. Return with the tooth.'",
                "complete": "'The tooth. Yes.' She strings it on rawhide and hands it back. 'Now you are marked.'",
             },
             "requirements": {"kills": [("black_wolf", 3)]},
             "rewards": {"gold": 400, "xp": 300, "relationship": 260}},
            {"id": "q_zer_2", "npc_id": "matriarch_zerith", "tier": "acquainted", "order": 2,
             "name": "The Poacher's Grove",
             "brief": "Someone is hunting our cubs for a market abroad. Find them. Return with proof.",
             "narrative": {
                "accept": "Zerith's voice is very quiet. 'Do not confuse mercy with weakness. Bring me their sigil.'",
                "complete": "You lay the sigil on her palm. She stares at it. 'A Federation broker.' Her jaw tightens. 'Thank you.'",
             },
             "requirements": {"kills": [("highway_bandit", 4), ("orc_grunt", 2)]},
             "rewards": {"gold": 900, "xp": 620, "relationship": 520,
                         "items": [("wolf_pelt", 4)]}},
            {"id": "q_zer_3", "npc_id": "matriarch_zerith", "tier": "friend", "order": 3,
             "name": "The Alpha's Claw",
             "brief": "There is an ancient alpha in the Ancient Den. It killed my mate. I have waited three years.",
             "narrative": {
                "accept": ("Zerith closes her eyes. 'I cannot go. My pack still needs me. But you — you can. "
                           "Bring me its heart. Or bring me back, if that is what it takes.'"),
                "complete": ("She holds the heart to her chest. She does not speak for a long time. "
                             "When she does, she says only, 'His name was Ryke.' She takes off her necklace and gives it to you."),
             },
             "requirements": {"kills": [("sylvan_druid_lost", 1)], "character_level": 38},
             "rewards": {"gold": 2600, "xp": 1700, "relationship": 950,
                         "unique_item": {"id": "ryke_claw_necklace", "name": "Ryke's Claw (Zerith's Necklace)",
                                         "rarity": "epic", "kind": "relic", "power": 0}}},
        ],
    },
    # ---------------- HYLION / ATLANTYRION ----------------
    {
        "id": "tide_priest_calvar",
        "name": "Tide-Priest Calvar of the Deep Choir",
        "race": "hyliondrian", "town": "atlantyrion", "continent": "hylion",
        "title": "Voice Beneath the Reef",
        "description": ("Calvar swims where the current is coldest, and speaks to the trench-things that no one else survives. "
                        "He speaks softly on land, as if his voice weighs less in air."),
        "personality": "Serene. Slow. Every sentence sounds like it took him a moment to remember land words.",
        "quests": [
            {"id": "q_cal_1", "npc_id": "tide_priest_calvar", "tier": "stranger", "order": 1,
             "name": "Kelp for the Choir",
             "brief": "The choir requires kelp gathered when the tide is falling. Six bundles, please. Softly, softly.",
             "narrative": {
                "accept": "'Do not startle the crabs. Do not sing to the fish. Do not touch coral you do not know.'",
                "complete": "'Thank you. The choir tastes the ocean in these threads.'",
             },
             "requirements": {"gathers": [("serpent_scale", 6)]},
             "rewards": {"gold": 460, "xp": 340, "relationship": 270}},
            {"id": "q_cal_2", "npc_id": "tide_priest_calvar", "tier": "acquainted", "order": 2,
             "name": "The Reef-Killer",
             "brief": "Something is killing the reef. Faster than it grows. Find it. Silence it.",
             "narrative": {
                "accept": "'Reef Sharks are not the killers. They warn. Follow their circling. Trust the tide.'",
                "complete": "'You listened to the tide. The reef breathes again. Come closer, traveller.'",
             },
             "requirements": {"kills": [("reef_shark", 3), ("coral_construct", 2)]},
             "rewards": {"gold": 1000, "xp": 700, "relationship": 540,
                         "items": [("orb_fragment", 1)]}},
            {"id": "q_cal_3", "npc_id": "tide_priest_calvar", "tier": "friend", "order": 3,
             "name": "The Trench-Prayer",
             "brief": "In the Abyssal Trench lies a stanza we cannot sing on land. I would like it back.",
             "narrative": {
                "accept": ("Calvar rests a hand on your shoulder. 'You will need dry lungs and a wet heart. "
                           "A Kraken Spawn carries the stanza. Ask it politely first. Then swim.'"),
                "complete": ("Calvar sings the stanza once, quietly, to the water in his bowl. The bowl glows. "
                             "He takes off his tidebound ring and slides it onto your finger. 'You gave the choir its ocean.'"),
             },
             "requirements": {"kills": [("kraken_spawn", 1)], "character_level": 45},
             "rewards": {"gold": 3000, "xp": 2200, "relationship": 1000,
                         "unique_item": {"id": "calvar_tide_ring", "name": "Calvar's Tidebound Ring",
                                         "rarity": "epic", "kind": "relic", "power": 0}}},
        ],
    },
    # ---------------- DAW'UL TALALU / VEILGROVE ----------------
    {
        "id": "elder_mireth",
        "name": "Elder Mireth of the Mystleaf Council",
        "race": "sylvan", "town": "veilgrove", "continent": "daw_ul_talalu",
        "title": "Keeper of the Elderroot Wards",
        "description": ("Mireth has served the Council since the second War of Thorns. She stands smaller than a child "
                        "but her voice fills the grove."),
        "personality": "Curious. Sharp. Ends every conversation with a question you cannot answer.",
        "quests": [
            {"id": "q_mir_1", "npc_id": "elder_mireth", "tier": "stranger", "order": 1,
             "name": "Whispers in the Mist",
             "brief": "Something whispers in the Mistwood that should not. Silence it.",
             "narrative": {
                "accept": "'A jungle stalker with a voice it should not have. Do not listen to what it says.'",
                "complete": "'You did not listen. Good. Some travellers do. Come, tell me nothing about it.'",
             },
             "requirements": {"kills": [("jungle_stalker", 3)]},
             "rewards": {"gold": 520, "xp": 400, "relationship": 280}},
            {"id": "q_mir_2", "npc_id": "elder_mireth", "tier": "acquainted", "order": 2,
             "name": "The Root-Rot",
             "brief": "The Thorn Labyrinth carries a rot that is spreading. Cut it out at its heart.",
             "narrative": {
                "accept": "'Do not follow the thorns. They will lead you where the rot wants you. Trust the roots that lean toward the sun.'",
                "complete": "'Ah. You did not follow the thorns. The Council notices such things.'",
             },
             "requirements": {"kills": [("canopy_wyrm", 1), ("vine_serpent", 2)]},
             "rewards": {"gold": 1100, "xp": 800, "relationship": 560,
                         "items": [("wisp_essence", 5)]}},
            {"id": "q_mir_3", "npc_id": "elder_mireth", "tier": "friend", "order": 3,
             "name": "Seed of Elderroot",
             "brief": "One seed of the Elderroot fell last century. I know where. I would like it back.",
             "narrative": {
                "accept": ("Mireth touches the small silver locket at her throat. 'Sylvan Druid, lost to the Hollow. "
                           "He carried the seed. He is not himself. He will not be gentle. But please, be gentle in return.'"),
                "complete": ("The Elder cradles the seed and hums to it — a note so low the leaves around you tremble. "
                             "'You have done the impossible with such grace. Take this. It has waited for a hand like yours.'"),
             },
             "requirements": {"kills": [("sylvan_druid_lost", 1)], "character_level": 48},
             "rewards": {"gold": 3400, "xp": 2600, "relationship": 1050,
                         "unique_item": {"id": "elderroot_seed_relic", "name": "Elderroot Seed (Mireth's Gift)",
                                         "rarity": "legendary", "kind": "relic", "power": 0}}},
        ],
    },
]

NPCS_BY_ID: dict[str, dict] = {n["id"]: n for n in NPCS}
NPCS_BY_TOWN: dict[str, list[dict]] = {}
for n in NPCS:
    NPCS_BY_TOWN.setdefault(n["town"], []).append(n)

# Flatten all quests for lookup by quest id.
NPC_QUESTS_BY_ID: dict[str, dict] = {}
for n in NPCS:
    for q in n["quests"]:
        NPC_QUESTS_BY_ID[q["id"]] = q


def initial_npc_relationships() -> dict:
    """New characters start as strangers to every flagship NPC."""
    return {n["id"]: {"points": 0, "level": "stranger"} for n in NPCS}


def add_npc_relationship(character: dict, npc_id: str, delta: int) -> tuple[str, str] | None:
    rels = character.setdefault("npc_relationships", {})
    entry = rels.setdefault(npc_id, {"points": 0, "level": "stranger"})
    old = entry["level"]
    entry["points"] = int(entry.get("points", 0)) + int(delta)
    entry["level"] = relationship_tier_from_points(entry["points"])
    if entry["level"] != old:
        return entry["level"], old
    return None
