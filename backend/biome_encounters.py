"""Biome-specific random encounters.

Encounters trigger rarely during exploration (and occasionally on crit-success
of other actions). Each encounter offers 2-3 player choices with different
risk/reward profiles.

Trigger chances (base):
  Explore outcome 4-5:  3%
  Explore outcome 6:   10%
  Other action outcome 6: 5%
  Cognition bonus: +30% of cognition stat, capped at +15%

Per-biome cooldown: 5 actions before that biome can trigger again.
"""
from __future__ import annotations

import random
from typing import Any

# ============================================================
# ENCOUNTER TRIGGER CONFIG
# ============================================================
ENCOUNTER_BASE_CHANCE = {
    "explore_45": 0.03,
    "explore_6":  0.10,
    "other_6":    0.05,
}
COGNITION_BONUS_RATIO = 0.30
COGNITION_BONUS_CAP = 15.0
BIOME_COOLDOWN_ACTIONS = 5

# ============================================================
# ENCOUNTER DEFINITIONS
# ============================================================
# Each encounter: id, name, biome, type, weight, min_level, desc, actions[]
# Each action: id, label, effects{}, narrative
# effects keys: gold(int), items[(id,qty)], hp(int), status(str), combat(str), xp(int)

BIOME_ENCOUNTERS: dict[str, list[dict]] = {
    # ==================== VALERIA ====================
    "golden_plains": [
        {
            "id": "bandit_toll_checkpoint", "name": "Bandit Toll Checkpoint",
            "type": "combat", "weight": 20, "min_level": 1,
            "desc": "A makeshift barricade blocks the road. Two bandits lean on spears, eyeing your coin purse.",
            "actions": [
                {"id": "fight", "label": "Fight through", "effects": {"combat": "highway_bandit"},
                 "narrative": "You draw your weapon. The bandits grin — they were hoping for this."},
                {"id": "pay", "label": "Pay the toll (-15 gold)", "effects": {"gold": -15},
                 "narrative": "You toss a few coins onto their barricade and walk through. Business as usual."},
                {"id": "avoid", "label": "Take the long way around", "effects": {"hp": -5},
                 "narrative": "You backtrack through the wheat fields, losing time and energy but avoiding trouble."},
            ],
        },
        {
            "id": "lost_farmhand", "name": "Lost Farmhand",
            "type": "npc", "weight": 15, "min_level": 1,
            "desc": "A dusty farmhand waves you down from the side of the road, looking bewildered.",
            "actions": [
                {"id": "help", "label": "Give directions", "effects": {"gold": 5, "xp": 10},
                 "narrative": "You point the farmhand toward the nearest village. He presses a few coins into your hand."},
                {"id": "ignore", "label": "Walk past", "effects": {},
                 "narrative": "You nod politely and keep walking. Someone else will help him."},
            ],
        },
        {
            "id": "hidden_wheat_cache", "name": "Hidden Wheat Cache",
            "type": "resource", "weight": 15, "min_level": 1,
            "desc": "A loose tarp behind an abandoned mill reveals sacks of grain someone tried to hide.",
            "actions": [
                {"id": "take", "label": "Take what you can carry", "effects": {"items": [("wheat_sheaf", 3)], "gold": 8},
                 "narrative": "You stuff your pack with grain and find a few coins tucked in a sack."},
                {"id": "leave", "label": "Leave it — might be watched", "effects": {},
                 "narrative": "You decide against theft. The plains have eyes everywhere."},
            ],
        },
        {
            "id": "traveling_shrine_plains", "name": "Wandering Shrine",
            "type": "shrine", "weight": 10, "min_level": 1,
            "desc": "A small wayside shrine to a forgotten saint still glows faintly. Its candle has never gone out.",
            "actions": [
                {"id": "pray", "label": "Kneel and pray", "effects": {"hp": 15, "xp": 5},
                 "narrative": "Warmth flows through you. The shrine's saint remembers your visit."},
                {"id": "desecrate", "label": "Check for offerings", "effects": {"gold": 12, "hp": -8},
                 "narrative": "You pocket a few old coins from the offering box. Something stings your hand."},
            ],
        },
    ],
    "crownwood_forest": [
        {
            "id": "old_hermit_hut", "name": "The Hermit's Hut",
            "type": "npc", "weight": 15, "min_level": 1,
            "desc": "A crooked hut sits in a clearing. Smoke rises from the chimney, and an old voice hums inside.",
            "actions": [
                {"id": "visit", "label": "Knock on the door", "effects": {"items": [("wild_mushroom", 2)], "xp": 15},
                 "narrative": "The hermit welcomes you with mushroom stew and old stories. You leave wiser."},
                {"id": "steal", "label": "Sneak around back", "effects": {"items": [("oak_log", 2)], "hp": -5},
                 "narrative": "You grab a few things from the woodpile. A tripwire catches your ankle."},
            ],
        },
        {
            "id": "boar_ambush", "name": "Boar Ambush",
            "type": "combat", "weight": 20, "min_level": 1,
            "desc": "A crashing in the underbrush — a feral boar charges from the ferns, tusks gleaming!",
            "actions": [
                {"id": "fight", "label": "Stand your ground", "effects": {"combat": "boar"},
                 "narrative": "You brace for impact. The boar does not slow down."},
                {"id": "dodge", "label": "Dive aside", "effects": {"hp": -3},
                 "narrative": "You roll clear. The boar vanishes into the brush, snorting."},
            ],
        },
        {
            "id": "ancient_tree_shrine", "name": "Ancient Tree Shrine",
            "type": "shrine", "weight": 10, "min_level": 1,
            "desc": "A massive oak, split by lightning long ago, has been carved into a shrine. Moss covers the offering ledge.",
            "actions": [
                {"id": "pray", "label": "Touch the carved bark", "effects": {"hp": 20, "xp": 8},
                 "narrative": "The old oak hums beneath your palm. The forest seems to breathe around you."},
                {"id": "search", "label": "Search the roots", "effects": {"items": [("relic_shard", 1)]},
                 "narrative": "Among the roots you find a shard of something old and powerful."},
            ],
        },
        {
            "id": "mushroom_ring", "name": "Fairy Mushroom Ring",
            "type": "resource", "weight": 15, "min_level": 1,
            "desc": "A perfect ring of mushrooms sits in a sunlit glade. The air smells of honey and old magic.",
            "actions": [
                {"id": "harvest", "label": "Harvest the mushrooms", "effects": {"items": [("wild_mushroom", 4)]},
                 "narrative": "You gather the mushrooms carefully. They glow faintly in your pack."},
                {"id": "eat", "label": "Eat one on the spot", "effects": {"hp": 10, "status": "weary"},
                 "narrative": "The mushroom tastes like starlight. The world tilts for a moment, then settles."},
            ],
        },
    ],
    "imperial_riverlands": [
        {
            "id": "river_ferry_merchant", "name": "River Ferry Merchant",
            "type": "merchant", "weight": 15, "min_level": 1,
            "desc": "A flat-bottomed ferry sits at the bank. The merchant aboard waves you over, displaying wares.",
            "actions": [
                {"id": "buy", "label": "Buy supplies (-20 gold)", "effects": {"gold": -20, "items": [("minor_healing_potion", 2)]},
                 "narrative": "The merchant wraps two potions in waxed cloth and passes them across."},
                {"id": "haggle", "label": "Try to haggle", "effects": {"gold": -10, "items": [("minor_healing_potion", 1)]},
                 "narrative": "You talk the merchant down to half price for a single potion."},
                {"id": "decline", "label": "Decline and move on", "effects": {},
                 "narrative": "You wave politely and continue along the riverbank."},
            ],
        },
        {
            "id": "flash_flood", "name": "Flash Flood",
            "type": "hazard", "weight": 20, "min_level": 1,
            "desc": "The river swells without warning. Brown water crashes through the reeds toward you!",
            "actions": [
                {"id": "run", "label": "Sprint for high ground", "effects": {"hp": -5},
                 "narrative": "You throw yourself up the bank just as the water tears through. Soaked, but alive."},
                {"id": "grab", "label": "Grab what you can from the water", "effects": {"hp": -10, "gold": 25},
                 "narrative": "You wade in and snatch a floating crate. Coins spill from it — but the current bruises you."},
            ],
        },
        {
            "id": "drowned_treasure", "name": "Drowned Treasure",
            "type": "mystery", "weight": 10, "min_level": 1,
            "desc": "Something glints beneath the clear water — a sunken chest, half-buried in river silt.",
            "actions": [
                {"id": "dive", "label": "Dive for it", "effects": {"items": [("coin_purse", 2)], "gold": 30},
                 "narrative": "You haul the chest up. It cracks open — coins and purses spill out."},
                {"id": "ignore", "label": "It's too deep", "effects": {},
                 "narrative": "The water is too fast here. You mark the spot and move on."},
            ],
        },
        {
            "id": "river_spirit", "name": "River Spirit",
            "type": "npc", "weight": 10, "min_level": 1,
            "desc": "A pale figure rises from the mist above the water — translucent, ancient, watching you with silver eyes.",
            "actions": [
                {"id": "offer", "label": "Toss a coin into the river", "effects": {"gold": -5, "hp": 25, "xp": 15},
                 "narrative": "The spirit catches the coin and dissolves. You feel refreshed, as if the river blessed you."},
                {"id": "watch", "label": "Watch in silence", "effects": {"xp": 10},
                 "narrative": "The spirit regards you for a long moment, then fades. You've witnessed something rare."},
            ],
        },
    ],
    "ashen_border": [
        {
            "id": "undead_patrol", "name": "Undead Patrol",
            "type": "combat", "weight": 20, "min_level": 1,
            "desc": "Armored figures march in the fog — rusted armor, hollow faces. They haven't noticed you yet.",
            "actions": [
                {"id": "fight", "label": "Ambush them", "effects": {"combat": "ruin_ghast"},
                 "narrative": "You strike before they turn. The dead are slow to react, but they do not flee."},
                {"id": "hide", "label": "Hide in the ruins", "effects": {"hp": -3},
                 "narrative": "You press yourself into a crumbling doorway. They pass. You breathe again."},
            ],
        },
        {
            "id": "cursed_battlefield_shrine", "name": "Cursed Battlefield Shrine",
            "type": "shrine", "weight": 10, "min_level": 1,
            "desc": "A war-shrine from the old campaigns, cracked and weeping black sap. Old weapons are stacked around it.",
            "actions": [
                {"id": "pray", "label": "Kneel despite the dark", "effects": {"hp": 15, "xp": 20},
                 "narrative": "The shrine hums with old power. Something here remembers valor, not just death."},
                {"id": "loot", "label": "Take the old weapons", "effects": {"items": [("iron_ore", 3)], "gold": 15, "hp": -8},
                 "narrative": "You pry a rusted blade from the stack. Something cold brushes your skin."},
            ],
        },
        {
            "id": "scavengers_cache_ashen", "name": "Scavenger's Cache",
            "type": "resource", "weight": 15, "min_level": 1,
            "desc": "A freshly dug hole sits beneath a dead tree. Someone has been scavenging the old battlefields.",
            "actions": [
                {"id": "take", "label": "Dig it up", "effects": {"items": [("iron_ore", 3), ("coin_purse", 1)]},
                 "narrative": "You unearth a cache of scrap iron and a small coin purse."},
                {"id": "leave", "label": "Leave it", "effects": {},
                 "narrative": "Best not to cross whoever's been digging here. You move on."},
            ],
        },
        {
            "id": "ghost_soldier", "name": "Ghost Soldier",
            "type": "npc", "weight": 10, "min_level": 1,
            "desc": "A translucent soldier sits on a broken wall, staring at a rusted letter. He looks up as you approach.",
            "actions": [
                {"id": "listen", "label": "Sit and listen", "effects": {"xp": 25, "hp": 5},
                 "narrative": "The ghost tells of the last battle, the orders that never came. He fades, finally at peace."},
                {"id": "leave", "label": "Walk away quietly", "effects": {},
                 "narrative": "Some burdens are not yours to carry. You leave the soldier to his letter."},
            ],
        },
    ],
    # ==================== MUSHKARA ====================
    "bloodwind_plains": [
        {
            "id": "war_camp_recruiter", "name": "War-Camp Recruiter",
            "type": "npc", "weight": 15, "min_level": 1,
            "desc": "A scarred orc in war-gear blocks your path. 'You look like you can fight. The camp needs bodies.'",
            "actions": [
                {"id": "volunteer", "label": "Hear the offer", "effects": {"gold": 20, "xp": 15},
                 "narrative": "The recruiter tosses you coins for listening and shares intelligence about the area."},
                {"id": "decline", "label": "Not interested", "effects": {},
                 "narrative": "You shake your head. The recruiter shrugs and moves on."},
            ],
        },
        {
            "id": "scavenger_pack_ambush", "name": "Scavenger Pack",
            "type": "combat", "weight": 20, "min_level": 1,
            "desc": "A pack of lean, scarred hounds circles you — war-bred scavengers, hungry and bold.",
            "actions": [
                {"id": "fight", "label": "Fight them off", "effects": {"combat": "scavenger_hound"},
                 "narrative": "You bare your blade. The hounds spread out, surrounding you."},
                {"id": "intimidate", "label": "Stand tall and shout", "effects": {"hp": -3},
                 "narrative": "You roar and stamp. The pack hesitates, then slinks off into the grass."},
            ],
        },
        {
            "id": "weapon_cache_bloodwind", "name": "Battlefield Weapon Cache",
            "type": "resource", "weight": 15, "min_level": 1,
            "desc": "A tarp-covered mound sits between two dead trees. Rusty weapon hilts poke out from under the cloth.",
            "actions": [
                {"id": "salvage", "label": "Salvage what you can", "effects": {"items": [("iron_ore", 3), ("scrap_bone", 2)]},
                 "narrative": "Most weapons are rusted beyond use, but the metal is still worth something."},
                {"id": "leave", "label": "Leave it alone", "effects": {},
                 "narrative": "Old battlefields carry old curses. You walk away."},
            ],
        },
        {
            "id": "field_medic", "name": "Field Medic",
            "type": "shrine", "weight": 10, "min_level": 1,
            "desc": "A battered medical tent flies a faded red flag. A tired medic waves you inside.",
            "actions": [
                {"id": "treat", "label": "Get treated", "effects": {"hp": 25},
                 "narrative": "The medic patches your wounds with practiced hands. 'Try not to come back,' he says."},
                {"id": "donate", "label": "Donate supplies (-10 gold)", "effects": {"gold": -10, "xp": 15},
                 "narrative": "You leave coins for the medic's work. He nods — it means more than you know."},
            ],
        },
    ],
    "red_steppe": [
        {
            "id": "warbeast_stampede", "name": "War-Beast Stampede",
            "type": "hazard", "weight": 20, "min_level": 1,
            "desc": "The ground trembles. A herd of war-beasts thunders over the ridge, heading straight for you!",
            "actions": [
                {"id": "dodge", "label": "Dive behind a boulder", "effects": {"hp": -5},
                 "narrative": "You press against stone as the herd pounds past. Dust and thunder."},
                {"id": "outrun", "label": "Try to outrun them", "effects": {"hp": -12, "gold": 15},
                 "narrative": "You sprint alongside the stampede and grab a loose pack from a fallen rider."},
            ],
        },
        {
            "id": "orc_patrol", "name": "Orc Patrol",
            "type": "combat", "weight": 20, "min_level": 1,
            "desc": "A patrol of orc grunts spots you on the open steppe. They draw weapons and advance.",
            "actions": [
                {"id": "fight", "label": "Stand and fight", "effects": {"combat": "orc_grunt"},
                 "narrative": "You plant your feet. The orcs are not here to talk."},
                {"id": "flee", "label": "Run for the rocks", "effects": {"hp": -4},
                 "narrative": "You scramble up a rocky outcrop. The orcs lose interest after a few thrown spears."},
            ],
        },
        {
            "id": "steppe_shrine", "name": "Steppe War-Shrine",
            "type": "shrine", "weight": 10, "min_level": 1,
            "desc": "A cairn of skulls and weapons marks an old orc war-shrine. The wind moans through the bones.",
            "actions": [
                {"id": "pray", "label": "Pay respects to the fallen", "effects": {"hp": 15, "xp": 15},
                 "narrative": "You add a stone to the cairn. Something here acknowledges strength."},
                {"id": "loot", "label": "Take a weapon from the cairn", "effects": {"items": [("iron_ore", 2)], "hp": -6},
                 "narrative": "You pull a notched blade from the pile. Something cold follows you away."},
            ],
        },
        {
            "id": "wandering_hunter", "name": "Wandering Hunter",
            "type": "npc", "weight": 15, "min_level": 1,
            "desc": "A lean figure sits by a small fire, cleaning a kill. They look up without surprise.",
            "actions": [
                {"id": "share_fire", "label": "Share their fire", "effects": {"hp": 10, "xp": 15},
                 "narrative": "You sit and share stories. The hunter teaches you tracking tricks before you part."},
                {"id": "trade", "label": "Trade (-15 gold)", "effects": {"gold": -15, "items": [("minor_healing_potion", 2)]},
                 "narrative": "The hunter has potions to spare. You trade coin for supplies."},
            ],
        },
    ],
    "iron_scar": [
        {
            "id": "iron_vein_collapse", "name": "Iron-Vein Collapse",
            "type": "hazard", "weight": 20, "min_level": 1,
            "desc": "The ground beneath you cracks — an old mine shaft, giving way!",
            "actions": [
                {"id": "grab", "label": "Grab the edge", "effects": {"hp": -8},
                 "narrative": "You claw at the crumbling rock and haul yourself up. Your arms are shredded."},
                {"id": "ride", "label": "Ride the collapse down", "effects": {"hp": -15, "items": [("iron_ore", 4)]},
                 "narrative": "You fall with the rubble — and land in a rich vein of exposed ore."},
            ],
        },
        {
            "id": "battlefield_spirit", "name": "Battlefield Spirit",
            "type": "combat", "weight": 15, "min_level": 1,
            "desc": "A ghostly figure in rusted armor rises from the scarred earth, weapon raised.",
            "actions": [
                {"id": "fight", "label": "Fight the spirit", "effects": {"combat": "ruin_ghast"},
                 "narrative": "The spirit does not speak. It only swings."},
                {"id": "acknowledge", "label": "Bow your head", "effects": {"xp": 20, "hp": 5},
                 "narrative": "You lower your weapon and bow. The spirit salutes and fades."},
            ],
        },
        {
            "id": "ore_cart_merchant", "name": "Ore Cart Merchant",
            "type": "merchant", "weight": 15, "min_level": 1,
            "desc": "A cart loaded with raw ore sits at a crossroads. The driver haggles before you even speak.",
            "actions": [
                {"id": "buy", "label": "Buy ore (-15 gold)", "effects": {"gold": -15, "items": [("iron_ore", 5)]},
                 "narrative": "You load up on raw iron. The merchant counts coins and moves on."},
                {"id": "skip", "label": "Not worth it", "effects": {},
                 "narrative": "The prices are steep. You walk on."},
            ],
        },
        {
            "id": "memorial_shrine", "name": "Miner's Memorial",
            "type": "shrine", "weight": 10, "min_level": 1,
            "desc": "A rough-hewn monument lists names of miners who died when the scar collapsed.",
            "actions": [
                {"id": "pray", "label": "Pay your respects", "effects": {"hp": 15, "xp": 10},
                 "narrative": "You stand in silence. The names are many. You leave feeling grounded."},
                {"id": "search", "label": "Search around the base", "effects": {"items": [("copper_ore", 3)]},
                 "narrative": "You find loose chunks of copper ore around the memorial's foundation."},
            ],
        },
    ],
    "ash_barrens": [
        {
            "id": "volcanic_eruption", "name": "Volcanic Eruption",
            "type": "hazard", "weight": 20, "min_level": 1,
            "desc": "The ground splits open. Lava fountains into the sky, and ash rains down like black snow!",
            "actions": [
                {"id": "run", "label": "Run for cover", "effects": {"hp": -10},
                 "narrative": "You sprint through falling ash, lungs burning. You make it to a rocky overhang."},
                {"id": "harvest", "label": "Grab volcanic glass from the fissure", "effects": {"hp": -15, "items": [("volcanic_glass", 3)]},
                 "narrative": "You dart to the fissure and pry out glowing chunks of volcanic glass."},
            ],
        },
        {
            "id": "fire_elemental_ambush", "name": "Fire Elemental Ambush",
            "type": "combat", "weight": 20, "min_level": 1,
            "desc": "A column of flame rises from a crack in the basalt — and shapes itself into something with eyes.",
            "actions": [
                {"id": "fight", "label": "Fight the elemental", "effects": {"combat": "magma_slime"},
                 "narrative": "The elemental surges toward you, leaving scorched footprints on the rock."},
                {"id": "douse", "label": "Throw dirt and scatter", "effects": {"hp": -5},
                 "narrative": "You hurl a cloak of ash over the creature and scramble away while it reforms."},
            ],
        },
        {
            "id": "lava_forged_cache", "name": "Lava-Forged Cache",
            "type": "resource", "weight": 15, "min_level": 1,
            "desc": "A hollow in the basalt holds items fused by ancient heat — someone's belongings, melted together.",
            "actions": [
                {"id": "pry", "label": "Pry the cache apart", "effects": {"items": [("iron_ore", 3), ("ash_root", 2)]},
                 "narrative": "You separate metal from slag. Some of it is still usable."},
                {"id": "leave", "label": "Too hot to handle", "effects": {},
                 "narrative": "The basalt is still warm. You decide not to risk burned hands."},
            ],
        },
        {
            "id": "ember_hermit", "name": "Ember Hermit",
            "type": "npc", "weight": 10, "min_level": 1,
            "desc": "An old figure sits cross-legged on a hot stone, unaffected by the heat. 'Sit,' they say. 'The fire teaches.'",
            "actions": [
                {"id": "learn", "label": "Sit and listen", "effects": {"xp": 25, "hp": 10},
                 "narrative": "The hermit teaches you to breathe ash without choking. You leave with new knowledge."},
                {"id": "leave", "label": "Too strange", "effects": {},
                 "narrative": "You back away slowly. The hermit watches you go, expressionless."},
            ],
        },
    ],
    "demonfall_crater": [
        {
            "id": "demon_scout", "name": "Demon Scout",
            "type": "combat", "weight": 20, "min_level": 1,
            "desc": "A winged shape descends from the crater's rim — a demon scout, small but fast, and it has seen you.",
            "actions": [
                {"id": "fight", "label": "Fight the scout", "effects": {"combat": "ash_kobold"},
                 "narrative": "The scout shrieks and dives. You have seconds to react."},
                {"id": "hide", "label": "Hide in the crater's shadows", "effects": {"hp": -3},
                 "narrative": "You press into a fissure. The scout circles, then loses interest and flies on."},
            ],
        },
        {
            "id": "infernal_rift", "name": "Infernal Rift",
            "type": "hazard", "weight": 20, "min_level": 1,
            "desc": "A glowing crack opens in the crater floor. Demonic energy pulses from it, warping the air.",
            "actions": [
                {"id": "avoid", "label": "Back away carefully", "effects": {"hp": -5},
                 "narrative": "You retreat from the heat. The rift closes behind you, hissing."},
                {"id": "reach", "label": "Reach into the rift", "effects": {"hp": -15, "items": [("relic_shard", 1)]},
                 "narrative": "You thrust your hand into the light. Something presses a shard into your palm."},
            ],
        },
        {
            "id": "demonic_merchant", "name": "Demonic Merchant",
            "type": "merchant", "weight": 10, "min_level": 1,
            "desc": "A figure in fine robes sits beside a portal, displaying goods on a cloth of shadow. 'No refunds,' it smiles.",
            "actions": [
                {"id": "buy", "label": "Buy (-25 gold)", "effects": {"gold": -25, "items": [("greater_healing_potion", 2)]},
                 "narrative": "The merchant wraps the potions in silk that feels wrong. They work, though."},
                {"id": "refuse", "label": "Refuse the deal", "effects": {},
                 "narrative": "You've heard what demonic deals cost. You walk away."},
            ],
        },
        {
            "id": "cursed_shrine", "name": "Cursed Shrine",
            "type": "shrine", "weight": 10, "min_level": 1,
            "desc": "A shrine at the crater's edge, half-corrupted. Its saint's face has been scratched away, but the candle still burns.",
            "actions": [
                {"id": "pray", "label": "Pray despite the corruption", "effects": {"hp": 20, "xp": 20},
                 "narrative": "You pray through the distortion. The candle flares — and for a moment, the saint's face returns."},
                {"id": "destroy", "label": "Smash the shrine", "effects": {"hp": -10, "items": [("relic_shard", 1)]},
                 "narrative": "You shatter the corrupted altar. A shard falls — and something screams far away."},
            ],
        },
    ],
    # ==================== CONCORDIA ====================
    "trade_road_outpost": [
        {
            "id": "roadside_merchant", "name": "Roadside Merchant",
            "type": "merchant", "weight": 15, "min_level": 1,
            "desc": "A colorful cart sits at the roadside, its awning bright against the dust. 'Best prices on the trade road!'",
            "actions": [
                {"id": "buy", "label": "Browse and buy (-15 gold)", "effects": {"gold": -15, "items": [("minor_healing_potion", 2), ("bandage", 1)]},
                 "narrative": "You pick up a couple of potions and a bandage. Fair prices, honest goods."},
                {"id": "skip", "label": "Just browsing", "effects": {},
                 "narrative": "You browse but nothing catches your eye. The merchant waves you off cheerfully."},
            ],
        },
        {
            "id": "bandit_ambush_road", "name": "Bandit Ambush",
            "type": "combat", "weight": 20, "min_level": 1,
            "desc": "Two figures step out of the brush ahead, weapons drawn. 'Toll for the road,' one says.",
            "actions": [
                {"id": "fight", "label": "Fight", "effects": {"combat": "highway_bandit"},
                 "narrative": "You draw your weapon. The bandits grin at each other."},
                {"id": "pay", "label": "Pay the toll (-10 gold)", "effects": {"gold": -10},
                 "narrative": "You toss a few coins at their feet and walk through while they scramble."},
            ],
        },
        {
            "id": "lost_traveler", "name": "Lost Traveler",
            "type": "npc", "weight": 15, "min_level": 1,
            "desc": "A well-dressed traveler sits on a rock, studying an upside-down map with growing frustration.",
            "actions": [
                {"id": "help", "label": "Help with directions", "effects": {"gold": 10, "xp": 10},
                 "narrative": "You turn the map right-side up and point the way. The traveler pays you."},
                {"id": "ignore", "label": "Walk past", "effects": {},
                 "narrative": "You've got your own road to walk. You leave the traveler to their map."},
            ],
        },
        {
            "id": "wayfarers_shrine", "name": "Wayfarer's Shrine",
            "type": "shrine", "weight": 10, "min_level": 1,
            "desc": "A small stone shrine at a crossroads, worn smooth by a thousand passing hands. 'Safe travels,' reads the carving.",
            "actions": [
                {"id": "pray", "label": "Rub the stone for luck", "effects": {"hp": 10, "xp": 8},
                 "narrative": "You add your hand to the worn stone. The road ahead feels lighter."},
                {"id": "search", "label": "Check behind the shrine", "effects": {"gold": 8},
                 "narrative": "You find a few coins left as offerings. The shrine doesn't seem to mind."},
            ],
        },
    ],
    "mosaic_coast": [
        {
            "id": "smugglers_deal", "name": "Smuggler's Deal",
            "type": "merchant", "weight": 15, "min_level": 1,
            "desc": "A hooded figure waves you into an alley. 'No questions, no receipts. Interested?'",
            "actions": [
                {"id": "buy", "label": "Buy (-20 gold)", "effects": {"gold": -20, "items": [("greater_healing_potion", 1), ("coin_purse", 1)]},
                 "narrative": "You hand over gold and receive goods wrapped in oilcloth. The smuggler vanishes."},
                {"id": "refuse", "label": "Walk away", "effects": {},
                 "narrative": "You don't deal in shadows. The smuggler shrugs and melts back into the alley."},
            ],
        },
        {
            "id": "coast_guard_patrol", "name": "Coast Guard Patrol",
            "type": "combat", "weight": 20, "min_level": 1,
            "desc": "A patrol in mismatched armor spots you near the smuggling caves. 'Halt! What's your business here?'",
            "actions": [
                {"id": "fight", "label": "Fight the patrol", "effects": {"combat": "highway_bandit"},
                 "narrative": "You draw steel. The guards shout for reinforcements."},
                {"id": "bribe", "label": "Bribe them (-15 gold)", "effects": {"gold": -15},
                 "narrative": "You palm a few coins. The sergeant pockets them and looks the other way."},
            ],
        },
        {
            "id": "beached_treasure", "name": "Beached Treasure",
            "type": "mystery", "weight": 10, "min_level": 1,
            "desc": "A wrecked ship lies half-buried in the sand, its hull cracked open by the tide.",
            "actions": [
                {"id": "search", "label": "Search the wreckage", "effects": {"gold": 30, "items": [("coin_purse", 2)]},
                 "narrative": "You pick through the splintered hull and find a sealed chest — coins and purses."},
                {"id": "careful", "label": "Check for traps first", "effects": {"gold": 15, "items": [("minor_healing_potion", 1)]},
                 "narrative": "You spot a rusted tripwire and disarm it. Slimmer pickings, but safe."},
            ],
        },
        {
            "id": "sea_shrine", "name": "Tide Shrine",
            "type": "shrine", "weight": 10, "min_level": 1,
            "desc": "A shrine built into a natural arch, flooded at high tide. Salt-crusted candles still burn somehow.",
            "actions": [
                {"id": "pray", "label": "Light a candle", "effects": {"hp": 20, "xp": 10},
                 "narrative": "You light a candle and set it among the others. The sea-spray feels warm."},
                {"id": "collect", "label": "Collect salt from the shrine", "effects": {"items": [("sea_salt", 3)]},
                 "narrative": "You scrape blessed salt from the shrine's stones. It tingles in your pack."},
            ],
        },
    ],
    "amber_vineyards": [
        {
            "id": "wine_merchant", "name": "Wine Merchant",
            "type": "merchant", "weight": 15, "min_level": 1,
            "desc": "A cart loaded with casks rolls along the vineyard road. 'From last year's harvest!'",
            "actions": [
                {"id": "buy", "label": "Buy a cask (-15 gold)", "effects": {"gold": -15, "items": [("greater_healing_potion", 1), ("wild_honey", 2)]},
                 "narrative": "You buy a small cask. The merchant throws in some honey as a gift."},
                {"id": "taste", "label": "Just a taste", "effects": {"hp": 5},
                 "narrative": "You sip the wine. It's excellent. The merchant smiles and moves on."},
            ],
        },
        {
            "id": "drunken_boar_encounter", "name": "Drunken Boar",
            "type": "combat", "weight": 20, "min_level": 1,
            "desc": "A boar stumbles out of the vineyards, snout stained purple with fermented grapes. Angry and uncoordinated.",
            "actions": [
                {"id": "fight", "label": "Fight the drunk boar", "effects": {"combat": "boar"},
                 "narrative": "The boar charges — in a weaving, unpredictable line. You raise your weapon."},
                {"id": "distract", "label": "Toss it some grapes", "effects": {"items": [("grapes", 2)]},
                 "narrative": "You scatter grapes. The boar snuffles after them and forgets you entirely."},
            ],
        },
        {
            "id": "golden_insect_swarm", "name": "Golden Insect Swarm",
            "type": "resource", "weight": 15, "min_level": 1,
            "desc": "A swarm of golden insects glitters above a patch of sunlit vines. Their wings catch the light like coins.",
            "actions": [
                {"id": "catch", "label": "Try to catch some", "effects": {"items": [("golden_insect_wing", 2)]},
                 "narrative": "You net a few of the insects. Their wings are delicate and valuable."},
                {"id": "watch", "label": "Watch the swarm", "effects": {"xp": 10},
                 "narrative": "You watch the swarm dance. There's a pattern — something almost like music."},
            ],
        },
        {
            "id": "harvest_shrine", "name": "Harvest Shrine",
            "type": "shrine", "weight": 10, "min_level": 1,
            "desc": "A small shrine draped in grapevines and wheat sheaves. The harvest spirit here is old and generous.",
            "actions": [
                {"id": "pray", "label": "Give thanks for the harvest", "effects": {"hp": 20, "items": [("wild_honey", 1)]},
                 "narrative": "You kneel among the vines. The shrine breathes, and you leave with honey and health."},
                {"id": "take", "label": "Take the offerings", "effects": {"gold": 12, "hp": -5},
                 "narrative": "You pocket the offerings. The vines seem to pull away from you."},
            ],
        },
    ],
    "silverroad": [
        {
            "id": "merchant_caravan", "name": "A Merchant Caravan",
            "type": "merchant", "weight": 20, "min_level": 1,
            "desc": "A long caravan of painted wagons stretches along the Silverroad. 'Trade goods from every continent!'",
            "actions": [
                {"id": "trade", "label": "Trade (-20 gold)", "effects": {"gold": -20, "items": [("minor_healing_potion", 3), ("bandage", 2)]},
                 "narrative": "You stock up on supplies. The merchant throws in extra bandages."},
                {"id": "rob", "label": "Rob the caravan", "effects": {"combat": "highway_bandit"},
                 "narrative": "You draw your blade. The caravan guards draw theirs — faster."},
                {"id": "ignore", "label": "Walk past", "effects": {},
                 "narrative": "You nod politely and continue down the road. The caravan rolls on without you."},
            ],
        },
        {
            "id": "highway_bandits_silverroad", "name": "Highway Bandits",
            "type": "combat", "weight": 20, "min_level": 1,
            "desc": "Three bandits block the road, spears leveled. 'Everything shiny goes in the bag,' the leader growls.",
            "actions": [
                {"id": "fight", "label": "Fight all three", "effects": {"combat": "highway_bandit"},
                 "narrative": "You charge the leader. The others close in — this will be a fight."},
                {"id": "pay", "label": "Hand over your coin (-20 gold)", "effects": {"gold": -20},
                 "narrative": "You toss your purse into the dirt. The bandits scramble for it and you slip past."},
            ],
        },
        {
            "id": "broken_cart_silverroad", "name": "Broken Cart",
            "type": "resource", "weight": 15, "min_level": 1,
            "desc": "A cart sits abandoned by the roadside, one wheel shattered. Goods are scattered around it.",
            "actions": [
                {"id": "salvage", "label": "Salvage the goods", "effects": {"items": [("iron_ore", 2), ("coin_purse", 1)]},
                 "narrative": "You gather what's usable — some ore, a coin purse wedged under the seat."},
                {"id": "leave", "label": "Leave it for the owner", "effects": {},
                 "narrative": "Someone might come back for it. You walk on."},
            ],
        },
        {
            "id": "roadside_shrine_silverroad", "name": "Traveler's Shrine",
            "type": "shrine", "weight": 10, "min_level": 1,
            "desc": "A stone shrine at a crossroads, carved with names of travelers who passed this way and made it home.",
            "actions": [
                {"id": "pray", "label": "Add your name in thought", "effects": {"hp": 15, "xp": 12},
                 "narrative": "You touch the carved names and think yours. The road ahead feels safer."},
                {"id": "search", "label": "Search the base", "effects": {"gold": 10},
                 "narrative": "You find coins tucked into the shrine's cracks — offerings no one came back for."},
            ],
        },
    ],
    "diplomats_highlands": [
        {
            "id": "embassy_courier", "name": "Embassy Courier",
            "type": "npc", "weight": 15, "min_level": 1,
            "desc": "A breathless courier runs up the path, satchel bouncing. 'I've lost my escort — can you help me reach the next waystation?'",
            "actions": [
                {"id": "escort", "label": "Escort the courier", "effects": {"gold": 25, "xp": 20},
                 "narrative": "You walk the courier to safety. They press a pouch of gold into your hand."},
                {"id": "refuse", "label": "Can't stop — sorry", "effects": {},
                 "narrative": "You apologize and continue your own journey. The courier sighs and jogs on."},
            ],
        },
        {
            "id": "cliff_rockslide", "name": "Cliff Rockslide",
            "type": "hazard", "weight": 20, "min_level": 1,
            "desc": "The cliffside path crumbles underfoot! Rocks tumble into the gorge below.",
            "actions": [
                {"id": "jump", "label": "Jump to solid ground", "effects": {"hp": -8},
                 "narrative": "You leap as the path gives way. Your fingers find stone — barely."},
                {"id": "ride", "label": "Ride the slide down", "effects": {"hp": -15, "items": [("cliff_stone", 3)]},
                 "narrative": "You ride the rockslide to the gorge floor. Painful — but you land on a vein of good stone."},
            ],
        },
        {
            "id": "hidden_archive", "name": "Hidden Archive",
            "type": "mystery", "weight": 10, "min_level": 1,
            "desc": "A door in the cliffside, hidden behind overgrown ivy, stands slightly ajar. Old parchment is visible inside.",
            "actions": [
                {"id": "enter", "label": "Enter the archive", "effects": {"xp": 30, "items": [("relic_shard", 1)]},
                 "narrative": "You step inside. Shelves of old treaties line the walls. You pocket a shard and some knowledge."},
                {"id": "seal", "label": "Seal the door", "effects": {"xp": 10},
                 "narrative": "You push the door shut and pile rocks against it. Some things are better left undisturbed."},
            ],
        },
        {
            "id": "summit_shrine", "name": "Summit Shrine",
            "type": "shrine", "weight": 10, "min_level": 1,
            "desc": "At the highest point of the pass, a wind-scoured shrine looks out over the lowlands.",
            "actions": [
                {"id": "pray", "label": "Stand in the wind and pray", "effects": {"hp": 20, "xp": 15},
                 "narrative": "The wind carries something away from you — fatigue, doubt, weight. You descend feeling lighter."},
                {"id": "search", "label": "Search the shrine", "effects": {"items": [("diplomats_quill", 1)]},
                 "narrative": "You find a quill pen tucked into the shrine — fine quality, enchanted with old magic."},
            ],
        },
    ],
    # ==================== KHARDRUM ====================
    "stone_ridge": [
        {
            "id": "mining_merchant_stone", "name": "Mining Merchant",
            "type": "merchant", "weight": 15, "min_level": 1,
            "desc": "A dwarf with a cart full of picks and ore sits at the mine entrance, haggling with a customer.",
            "actions": [
                {"id": "buy", "label": "Buy supplies (-15 gold)", "effects": {"gold": -15, "items": [("copper_ore", 4), ("minor_healing_potion", 1)]},
                 "narrative": "You load up on copper and a potion. The dwarf nods approvingly."},
                {"id": "skip", "label": "Move along", "effects": {},
                 "narrative": "You've got your own supplies. The dwarf barely notices."},
            ],
        },
        {
            "id": "cave_in", "name": "Cave-In",
            "type": "hazard", "weight": 20, "min_level": 1,
            "desc": "A rumble, then dust — the mine entrance behind you collapses in a shower of stone!",
            "actions": [
                {"id": "dig", "label": "Dig your way out", "effects": {"hp": -10},
                 "narrative": "You claw through the rubble until fresh air hits your face. Your hands are raw."},
                {"id": "explore", "label": "Look for another way out", "effects": {"hp": -5, "items": [("copper_ore", 3)]},
                 "narrative": "You follow a side tunnel and find a vein of copper before emerging through a crack."},
            ],
        },
        {
            "id": "rock_creature_ambush", "name": "Rock Creature Ambush",
            "type": "combat", "weight": 20, "min_level": 1,
            "desc": "A boulder shifts — and rises on two legs. It's not a boulder at all.",
            "actions": [
                {"id": "fight", "label": "Fight the rock creature", "effects": {"combat": "boar"},
                 "narrative": "The creature swings a fist of solid stone. You dodge — barely."},
                {"id": "flee", "label": "Run for the mine entrance", "effects": {"hp": -6},
                 "narrative": "You sprint for the tunnels. The creature's footsteps shake the ground behind you."},
            ],
        },
        {
            "id": "miners_shrine", "name": "Miner's Shrine",
            "type": "shrine", "weight": 10, "min_level": 1,
            "desc": "A small shrine carved into the rock face, decorated with tiny copper offerings from generations of miners.",
            "actions": [
                {"id": "pray", "label": "Tap the shrine for luck", "effects": {"hp": 15, "xp": 10},
                 "narrative": "You tap the shrine three times, as the miners do. Something in the rock approves."},
                {"id": "take", "label": "Take the copper offerings", "effects": {"items": [("copper_ore", 3)], "hp": -5},
                 "narrative": "You pocket the tiny copper figures. The mine seems to groan around you."},
            ],
        },
    ],
    "granite_foothills": [
        {
            "id": "ore_merchant_granite", "name": "Ore Merchant",
            "type": "merchant", "weight": 15, "min_level": 1,
            "desc": "A mule-drawn cart sits at the mining camp's edge, loaded with raw ore in neat sacks.",
            "actions": [
                {"id": "buy", "label": "Buy ore (-20 gold)", "effects": {"gold": -20, "items": [("iron_ore", 5), ("copper_ore", 3)]},
                 "narrative": "You buy a mixed load. The merchant throws in extra copper for bulk."},
                {"id": "pass", "label": "Not today", "effects": {},
                 "narrative": "You wave and walk on. The merchant returns to sorting ore."},
            ],
        },
        {
            "id": "rockslide_hazard", "name": "Rockslide",
            "type": "hazard", "weight": 20, "min_level": 1,
            "desc": "Loose stone cascades down the slope above you, bouncing and cracking!",
            "actions": [
                {"id": "shelter", "label": "Shelter behind a boulder", "effects": {"hp": -5},
                 "narrative": "You press behind a granite outcrop as stones hammer the ground around you."},
                {"id": "run", "label": "Outrun it", "effects": {"hp": -12, "items": [("granite_chunk", 3)]},
                 "narrative": "You sprint alongside the slide, grabbing loose chunks of good granite as you go."},
            ],
        },
        {
            "id": "stone_beast_ambush", "name": "Stone Beast Ambush",
            "type": "combat", "weight": 20, "min_level": 1,
            "desc": "A creature of living granite rises from the scree slope, eyes glowing like furnace coals.",
            "actions": [
                {"id": "fight", "label": "Fight the stone beast", "effects": {"combat": "boar"},
                 "narrative": "The beast charges with a sound like an avalanche. You brace."},
                {"id": "avoid", "label": "Scramble up the cliff", "effects": {"hp": -4},
                 "narrative": "You climb out of reach. The beast paces below, then sinks back into the stone."},
            ],
        },
        {
            "id": "mountain_shrine", "name": "Mountain Shrine",
            "type": "shrine", "weight": 10, "min_level": 1,
            "desc": "A shrine perched on a granite shelf, wind-carved and ancient. Offerings of iron and stone in neat dwarven patterns.",
            "actions": [
                {"id": "pray", "label": "Leave an offering", "effects": {"hp": 20, "xp": 15},
                 "narrative": "You place a stone among the offerings. The mountain seems to steady beneath your feet."},
                {"id": "take", "label": "Take the iron offerings", "effects": {"items": [("iron_ore", 3)], "hp": -8},
                 "narrative": "You pocket the iron. The wind picks up — a stone falls from above, narrowly missing you."},
            ],
        },
    ],
    "ember_mines": [
        {
            "id": "mine_cart_merchant", "name": "Mine Cart Merchant",
            "type": "merchant", "weight": 15, "min_level": 1,
            "desc": "A dwarf pushes an ore cart along the tunnel, a lantern hanging from the handle. 'Supplies for the workers!'",
            "actions": [
                {"id": "buy", "label": "Buy (-20 gold)", "effects": {"gold": -20, "items": [("greater_healing_potion", 1), ("iron_ore", 3)]},
                 "narrative": "You buy a potion and some ore. The dwarf nods and pushes on into the dark."},
                {"id": "decline", "label": "Decline", "effects": {},
                 "narrative": "You step aside and let the cart pass. The dwarf's lantern fades into the tunnel."},
            ],
        },
        {
            "id": "gas_explosion", "name": "Gas Explosion",
            "type": "hazard", "weight": 20, "min_level": 1,
            "desc": "Your lantern flame gutters — then the air ignites! Invisible gas has filled the tunnel.",
            "actions": [
                {"id": "duck", "label": "Hit the ground", "effects": {"hp": -10},
                 "narrative": "You drop flat as the flame rolls over you. Singed, but alive."},
                {"id": "run", "label": "Run for the exit", "effects": {"hp": -18, "items": [("coal_chunk", 3)]},
                 "narrative": "You sprint through the fireball, grabbing loose coal. You'll feel that for days."},
            ],
        },
        {
            "id": "fire_creature_ambush", "name": "Fire Creature Ambush",
            "type": "combat", "weight": 20, "min_level": 1,
            "desc": "Something skitters across the tunnel ceiling, leaving trails of fire. It drops down in front of you.",
            "actions": [
                {"id": "fight", "label": "Fight it", "effects": {"combat": "magma_slime"},
                 "narrative": "The creature hisses and lunges. The tunnel walls glow with reflected fire."},
                {"id": "retreat", "label": "Back away slowly", "effects": {"hp": -5},
                 "narrative": "You retreat step by step. The creature watches but doesn't follow."},
            ],
        },
        {
            "id": "forge_shrine", "name": "Forge Shrine",
            "type": "shrine", "weight": 10, "min_level": 1,
            "desc": "A small anvil-shrine sits at a tunnel junction, decorated with tiny iron figurines left by miners.",
            "actions": [
                {"id": "pray", "label": "Strike the anvil", "effects": {"hp": 15, "xp": 12},
                 "narrative": "You strike the anvil three times. The ring echoes through the tunnels like a heartbeat."},
                {"id": "take", "label": "Take the figurines", "effects": {"items": [("iron_ore", 3)], "hp": -6},
                 "narrative": "You pocket the iron figurines. The tunnel seems to close in slightly."},
            ],
        },
    ],
    "crystal_caverns": [
        {
            "id": "gem_merchant", "name": "Gem Merchant",
            "type": "merchant", "weight": 15, "min_level": 1,
            "desc": "A dwarf sits behind a makeshift counter of crystal, displaying cut gems by lantern light.",
            "actions": [
                {"id": "buy", "label": "Buy gems (-25 gold)", "effects": {"gold": -25, "items": [("greater_healing_potion", 2)]},
                 "narrative": "You buy a pair of potions. The dwarf wraps them in crystal-silk."},
                {"id": "sell", "label": "Sell some ore (+15 gold)", "effects": {"gold": 15, "items": [("iron_ore", -3)]},
                 "narrative": "You trade raw ore for coin. The dwarf is always buying."},
            ],
        },
        {
            "id": "crystal_collapse", "name": "Crystal Collapse",
            "type": "hazard", "weight": 20, "min_level": 1,
            "desc": "A resonant sound — and the crystal formations around you shatter inward!",
            "actions": [
                {"id": "duck", "label": "Duck behind a pillar", "effects": {"hp": -8},
                 "narrative": "You press against a crystal column as shards rain down. You're cut but standing."},
                {"id": "grab", "label": "Grab falling crystals", "effects": {"hp": -12, "items": [("crystal_shard", 3)]},
                 "narrative": "You snatch falling crystals from the air. Your hands bleed but the gems are pristine."},
            ],
        },
        {
            "id": "crystal_monster_ambush", "name": "Crystal Monster Ambush",
            "type": "combat", "weight": 20, "min_level": 1,
            "desc": "A formation detaches from the wall — it has limbs, and they're reaching for you.",
            "actions": [
                {"id": "fight", "label": "Fight the crystal creature", "effects": {"combat": "boar"},
                 "narrative": "The creature's edges are razor-sharp. You raise your guard."},
                {"id": "flee", "label": "Run deeper into the caverns", "effects": {"hp": -5},
                 "narrative": "You sprint into a side passage. The creature doesn't follow — it returns to the wall."},
            ],
        },
        {
            "id": "crystal_shrine", "name": "Crystal Shrine",
            "type": "shrine", "weight": 10, "min_level": 1,
            "desc": "A perfect crystal formation has been shaped into a shrine. Light refracts through it in rainbow patterns.",
            "actions": [
                {"id": "pray", "label": "Step into the light", "effects": {"hp": 20, "xp": 15},
                 "narrative": "The refracted light washes over you. You feel mended, clarified."},
                {"id": "mine", "label": "Mine a piece of the shrine", "effects": {"items": [("crystal_shard", 2)], "hp": -8},
                 "narrative": "You chip off a piece. The rainbow vanishes instantly. The cavern feels colder."},
            ],
        },
    ],
    "deep_forges": [
        {
            "id": "master_smith_npc", "name": "The Master Smith",
            "type": "npc", "weight": 15, "min_level": 1,
            "desc": "An ancient dwarf works at a forge that hasn't gone cold in three hundred years. 'Watch,' he says. 'Learn.'",
            "actions": [
                {"id": "learn", "label": "Watch and learn", "effects": {"xp": 30, "items": [("iron_ore", 2)]},
                 "narrative": "You observe the master's technique. He hands you a piece of stock at the end. 'Practice.'"},
                {"id": "leave", "label": "Don't interrupt", "effects": {},
                 "narrative": "You bow respectfully and back away. The master doesn't look up."},
            ],
        },
        {
            "id": "forge_explosion", "name": "Forge Explosion",
            "type": "hazard", "weight": 20, "min_level": 1,
            "desc": "A crucible bursts, spraying molten metal across the forge hall!",
            "actions": [
                {"id": "shield", "label": "Raise your shield", "effects": {"hp": -8},
                 "narrative": "You crouch behind your shield as liquid metal sprays overhead. The shield steams."},
                {"id": "grab", "label": "Grab the spilled metal", "effects": {"hp": -15, "items": [("jahra_ingot", 1)]},
                 "narrative": "You scoop up a cooling piece of the spill. It's Jahra metal — worth the burns."},
            ],
        },
        {
            "id": "ancestor_spirit_combat", "name": "Ancestor Spirit",
            "type": "combat", "weight": 15, "min_level": 1,
            "desc": "A dwarven ghost in masterwork armor rises from the forge floor, hammer raised. 'Prove your worth.'",
            "actions": [
                {"id": "fight", "label": "Fight the ancestor", "effects": {"combat": "ruin_ghast"},
                 "narrative": "The ancestor's hammer descends. The forge flames roar in response."},
                {"id": "kneel", "label": "Kneel in respect", "effects": {"xp": 25, "hp": 10},
                 "narrative": "You kneel. The ancestor lowers the hammer, nods once, and sinks back into the stone."},
            ],
        },
        {
            "id": "deep_forge_shrine", "name": "Eternal Forge Shrine",
            "type": "shrine", "weight": 10, "min_level": 1,
            "desc": "A forge-altar at the heart of the deep halls. Its fire has burned since the founding of Khardrum.",
            "actions": [
                {"id": "pray", "label": "Feed the flame", "effects": {"hp": 25, "xp": 20},
                 "narrative": "You add a piece of coal to the eternal fire. It flares — and so does something inside you."},
                {"id": "take", "label": "Take a coal from the forge", "effects": {"items": [("forge_coal", 2)], "hp": -10},
                 "narrative": "You pocket two glowing coals. They're warm — but your hands blister badly."},
            ],
        },
    ],
    # ==================== HAYA ====================
    "verdant_edge": [
        {
            "id": "forest_spirit_npc", "name": "Forest Spirit",
            "type": "npc", "weight": 15, "min_level": 1,
            "desc": "A small glowing creature darts between the trees, leaving trails of pollen. It stops and regards you.",
            "actions": [
                {"id": "follow", "label": "Follow the spirit", "effects": {"xp": 20, "items": [("wild_herb", 3)]},
                 "narrative": "The spirit leads you to a hidden herb grove, then vanishes into the canopy."},
                {"id": "watch", "label": "Watch from a distance", "effects": {"xp": 8},
                 "narrative": "You observe the spirit's dance. There's a rhythm to it — something old and patient."},
            ],
        },
        {
            "id": "wild_beast_ambush_verdant", "name": "Wild Beast Ambush",
            "type": "combat", "weight": 20, "min_level": 1,
            "desc": "A creature bursts from the undergrowth — small, fast, and very angry.",
            "actions": [
                {"id": "fight", "label": "Fight the beast", "effects": {"combat": "boar"},
                 "narrative": "You raise your weapon as the beast leaps. No time to think."},
                {"id": "scare", "label": "Make yourself big", "effects": {"hp": -3},
                 "narrative": "You shout and wave your arms. The beast hesitates, then bolts into the brush."},
            ],
        },
        {
            "id": "hidden_herb_garden", "name": "Hidden Herb Garden",
            "type": "resource", "weight": 15, "min_level": 1,
            "desc": "A clearing full of herbs grows in impossible abundance — every species, all blooming at once.",
            "actions": [
                {"id": "harvest", "label": "Harvest the herbs", "effects": {"items": [("wild_herb", 5)]},
                 "narrative": "You gather herbs by the armful. The clearing seems to regrow as you pick."},
                {"id": "rest", "label": "Rest among the herbs", "effects": {"hp": 15},
                 "narrative": "You lie among the blooms. The scent mends something in you. You leave refreshed."},
            ],
        },
        {
            "id": "forest_shrine_verdant", "name": "Forest Shrine",
            "type": "shrine", "weight": 10, "min_level": 1,
            "desc": "A moss-covered stone shrine, so old the carving has become part of the tree growing around it.",
            "actions": [
                {"id": "pray", "label": "Touch the stone", "effects": {"hp": 15, "xp": 10},
                 "narrative": "The stone is warm. The tree above rustles though there is no wind."},
                {"id": "search", "label": "Search the roots", "effects": {"items": [("wild_herb", 2), ("relic_shard", 1)]},
                 "narrative": "You find herbs and a shard among the roots. The tree seems to permit it."},
            ],
        },
    ],
    "sunlit_canopy": [
        {
            "id": "sun_priest_npc", "name": "Sun-Priest",
            "type": "npc", "weight": 15, "min_level": 1,
            "desc": "A robed elf stands in a shaft of sunlight, eyes closed, humming a melody that makes the leaves glow.",
            "actions": [
                {"id": "listen", "label": "Listen to the hymn", "effects": {"hp": 20, "xp": 15},
                 "narrative": "The hymn washes through you like warm light. You feel strengthened."},
                {"id": "ask", "label": "Ask for a blessing", "effects": {"gold": -10, "hp": 30},
                 "narrative": "The priest touches your forehead. Light flows through you, mending deeper wounds."},
            ],
        },
        {
            "id": "light_creature_ambush", "name": "Light Creature Ambush",
            "type": "combat", "weight": 20, "min_level": 1,
            "desc": "A creature of pure light coalesces from a sunbeam, blazing and hostile.",
            "actions": [
                {"id": "fight", "label": "Fight the light creature", "effects": {"combat": "grove_wisp"},
                 "narrative": "The creature burns. You shield your eyes and raise your weapon."},
                {"id": "shadow", "label": "Step into the shade", "effects": {"hp": -3},
                 "narrative": "You duck into the shadows. The creature flickers, unable to follow, and fades."},
            ],
        },
        {
            "id": "solar_herb_cache", "name": "Solar Herb Cache",
            "type": "resource", "weight": 15, "min_level": 1,
            "desc": "A patch of golden herbs grows in a sunbeam so concentrated it burns the air around it.",
            "actions": [
                {"id": "harvest", "label": "Harvest carefully", "effects": {"items": [("sunpetal", 4)]},
                 "narrative": "You pick the glowing herbs with practiced hands. They're warm to the touch."},
                {"id": "leave", "label": "Too bright to approach", "effects": {},
                 "narrative": "The sunbeam is too intense. You shield your eyes and move on."},
            ],
        },
        {
            "id": "sun_shrine", "name": "Sun Shrine",
            "type": "shrine", "weight": 10, "min_level": 1,
            "desc": "A shrine of polished stone that catches and focuses sunlight into a single blazing point.",
            "actions": [
                {"id": "pray", "label": "Stand in the light", "effects": {"hp": 25, "xp": 15},
                 "narrative": "The focused light pierces through you — not burning, but clarifying. You feel remade."},
                {"id": "take", "label": "Pry a stone from the shrine", "effects": {"items": [("sun_stone", 1)], "hp": -8},
                 "narrative": "You pry loose a focusing stone. The light scatters. Something in the canopy goes dark."},
            ],
        },
    ],
    "moonveil_woods": [
        {
            "id": "moon_witch_npc", "name": "The Moon-Witch",
            "type": "npc", "weight": 15, "min_level": 1,
            "desc": "An elf in silver robes sits on a moonlit branch, stirring a cauldron that glows pale blue.",
            "actions": [
                {"id": "trade", "label": "Trade (-15 gold)", "effects": {"gold": -15, "items": [("greater_healing_potion", 2)]},
                 "narrative": "The witch bottles two potions and hands them down. 'Use them by moonlight,' she warns."},
                {"id": "listen", "label": "Listen to her song", "effects": {"xp": 25},
                 "narrative": "The witch sings of things hidden by daylight. You leave with knowledge you didn't expect."},
            ],
        },
        {
            "id": "illusion_trap", "name": "Illusion Trap",
            "type": "mystery", "weight": 15, "min_level": 1,
            "desc": "The path ahead shimmers and splits into three — each looking equally real. An illusion bars your way.",
            "actions": [
                {"id": "cognition", "label": "Trust your instincts", "effects": {"xp": 20, "items": [("moonveil_herb", 2)]},
                 "narrative": "You sense the right path through the shimmer. Beyond it, rare herbs grow in the moonlight."},
                {"id": "random", "label": "Pick a path at random", "effects": {"hp": -8},
                 "narrative": "You choose wrong. The illusion collapses and you fall through brush into a ravine."},
            ],
        },
        {
            "id": "lunar_herb_cache", "name": "Lunar Herb Cache",
            "type": "resource", "weight": 15, "min_level": 1,
            "desc": "Silvery herbs grow in a circle of moonlight, glowing softly in the dark woods.",
            "actions": [
                {"id": "harvest", "label": "Harvest the lunar herbs", "effects": {"items": [("moonveil_herb", 4)]},
                 "narrative": "You gather the glowing herbs. They pulse gently in your hands."},
                {"id": "leave", "label": "Leave them for the moon-witch", "effects": {},
                 "narrative": "You decide not to take from the witch's garden. Smart."},
            ],
        },
        {
            "id": "moon_shrine", "name": "Moon Shrine",
            "type": "shrine", "weight": 10, "min_level": 1,
            "desc": "A silver shrine that only reflects moonlight, invisible during the day. Its surface ripples like water.",
            "actions": [
                {"id": "pray", "label": "Touch the silver surface", "effects": {"hp": 20, "xp": 15},
                 "narrative": "Your reflection ripples and fades. You feel lighter, as if something was lifted from you."},
                {"id": "take", "label": "Scrape silver from the shrine", "effects": {"gold": 20, "hp": -10},
                 "narrative": "You pocket silver flakes. The shrine's surface goes dull. The moon seems colder."},
            ],
        },
    ],
    "celestial_lake": [
        {
            "id": "water_spirit_npc", "name": "Water Spirit",
            "type": "npc", "weight": 15, "min_level": 1,
            "desc": "A figure of living water rises from the lake's surface, singing a song that sounds like rainfall.",
            "actions": [
                {"id": "sing", "label": "Sing back", "effects": {"hp": 25, "xp": 20},
                 "narrative": "You hum a melody. The spirit harmonizes, and the lake's waters heal you."},
                {"id": "watch", "label": "Watch in silence", "effects": {"xp": 10},
                 "narrative": "The spirit sings and sinks. You've witnessed something few ever see."},
            ],
        },
        {
            "id": "lake_monster_ambush", "name": "Lake Monster Ambush",
            "type": "combat", "weight": 20, "min_level": 1,
            "desc": "The water boils — something massive surfaces right beside you, jaws wide!",
            "actions": [
                {"id": "fight", "label": "Fight the lake monster", "effects": {"combat": "river_serpent"},
                 "narrative": "You draw your weapon as the beast lunges. Water sprays everywhere."},
                {"id": "dive", "label": "Dive underwater", "effects": {"hp": -6},
                 "narrative": "You plunge beneath the surface. The monster circles, then loses interest."},
            ],
        },
        {
            "id": "sunken_treasure_lake", "name": "Sunken Treasure",
            "type": "mystery", "weight": 10, "min_level": 1,
            "desc": "The lake is perfectly clear here — and on the bottom, you can see a structure. A temple, intact.",
            "actions": [
                {"id": "dive", "label": "Dive to the temple", "effects": {"xp": 30, "items": [("relic_shard", 1)]},
                 "narrative": "You swim down and push through an intact door. Inside: a shard, still glowing."},
                {"id": "admire", "label": "Admire from the surface", "effects": {"xp": 8},
                 "narrative": "You study the temple's outline from above. Beautiful. You'll remember it."},
            ],
        },
        {
            "id": "lake_shrine", "name": "Lake Shrine",
            "type": "shrine", "weight": 10, "min_level": 1,
            "desc": "A shrine that floats on the lake's surface, supported by nothing, sinking neither nor rising.",
            "actions": [
                {"id": "pray", "label": "Step onto the shrine", "effects": {"hp": 25, "xp": 15},
                 "narrative": "The shrine holds your weight. The lake's magic flows through you."},
                {"id": "search", "label": "Search beneath the shrine", "effects": {"items": [("lake_crystal", 2)]},
                 "narrative": "You dive under the shrine and find crystals growing on its underside."},
            ],
        },
    ],
    "starfall_cliffs": [
        {
            "id": "star_gazer_npc", "name": "The Star-Gazer",
            "type": "npc", "weight": 15, "min_level": 1,
            "desc": "An elf sits at the cliff's edge, peering through a crystal lens at the sky. 'Look,' they say. 'It's falling again.'",
            "actions": [
                {"id": "look", "label": "Look through the lens", "effects": {"xp": 25, "items": [("star_fragment", 1)]},
                 "narrative": "You see a streak of light — and a fragment lands at your feet. The star-gazer smiles."},
                {"id": "leave", "label": "Too close to the edge", "effects": {},
                 "narrative": "The cliff edge makes you nervous. You back away."},
            ],
        },
        {
            "id": "meteor_strike", "name": "Meteor Strike",
            "type": "hazard", "weight": 20, "min_level": 1,
            "desc": "A blazing rock falls from the sky, crashing into the cliff just ahead of you!",
            "actions": [
                {"id": "dodge", "label": "Dive away from the impact", "effects": {"hp": -8},
                 "narrative": "You throw yourself sideways as the meteor crater opens. Rock splinters cut the air."},
                {"id": "rush", "label": "Rush to the crater", "effects": {"hp": -15, "items": [("star_fragment", 2)]},
                 "narrative": "You sprint to the smoking crater and grab glowing fragments before they cool."},
            ],
        },
        {
            "id": "sky_beast_ambush", "name": "Sky Beast Ambush",
            "type": "combat", "weight": 20, "min_level": 1,
            "desc": "A winged creature drops from the clouds, riding the updrafts — and it's diving straight at you!",
            "actions": [
                {"id": "fight", "label": "Fight the sky beast", "effects": {"combat": "grove_wisp"},
                 "narrative": "You brace as the beast's talons rake toward you. The cliff edge is no place to fight."},
                {"id": "duck", "label": "Drop flat", "effects": {"hp": -4},
                 "narrative": "You hit the ground. The beast overshoots, screeching, and climbs back into the clouds."},
            ],
        },
        {
            "id": "star_shrine", "name": "Star Shrine",
            "type": "shrine", "weight": 10, "min_level": 1,
            "desc": "A shrine built from fallen meteorites, magnetic and humming. It pulls lightly at your equipment.",
            "actions": [
                {"id": "pray", "label": "Touch the meteorite", "effects": {"hp": 20, "xp": 20},
                 "narrative": "The hum travels through your bones. Something aligns. You feel connected to the sky."},
                {"id": "take", "label": "Chip off a piece", "effects": {"items": [("star_fragment", 1)], "hp": -8},
                 "narrative": "You chip off a fragment. The hum changes pitch — and something falls from the sky in response."},
            ],
        },
    ],
    # ==================== GENNEL ====================
    "oasis_outskirts": [
        {
            "id": "oasis_merchant", "name": "Oasis Merchant",
            "type": "merchant", "weight": 15, "min_level": 1,
            "desc": "A tent beside the oasis, its awning striped in desert colors. 'Water, potions, shade — everything you need!'",
            "actions": [
                {"id": "buy", "label": "Buy supplies (-15 gold)", "effects": {"gold": -15, "items": [("minor_healing_potion", 2), ("bandage", 1)]},
                 "narrative": "You stock up. The merchant throws in a free drink of oasis water."},
                {"id": "skip", "label": "Not thirsty", "effects": {},
                 "narrative": "You wave and walk on. The merchant fans himself and waits."},
            ],
        },
        {
            "id": "sand_beast_ambush_oasis", "name": "Sand Beast Ambush",
            "type": "combat", "weight": 20, "min_level": 1,
            "desc": "The sand erupts beneath you — a burrower, drawn by your footsteps!",
            "actions": [
                {"id": "fight", "label": "Fight the burrower", "effects": {"combat": "boar"},
                 "narrative": "You leap clear as the beast surfaces. Sand sprays everywhere."},
                {"id": "run", "label": "Sprint for solid ground", "effects": {"hp": -5},
                 "narrative": "You dash for the rocks. The burrower snaps at your heels, then sinks back."},
            ],
        },
        {
            "id": "hidden_spring", "name": "Hidden Spring",
            "type": "resource", "weight": 15, "min_level": 1,
            "desc": "A crack in the rock reveals a spring of crystal-clear water, hidden from the sun.",
            "actions": [
                {"id": "drink", "label": "Drink deeply", "effects": {"hp": 20},
                 "narrative": "The water is cold and sweet. You feel restored in body and spirit."},
                {"id": "bottle", "label": "Bottle some water", "effects": {"items": [("oasis_water", 3)]},
                 "narrative": "You fill your waterskins. This water stays cool for days."},
            ],
        },
        {
            "id": "oasis_shrine", "name": "Oasis Shrine",
            "type": "shrine", "weight": 10, "min_level": 1,
            "desc": "A small shrine at the oasis's edge, decorated with desert flowers and animal bones.",
            "actions": [
                {"id": "pray", "label": "Leave a flower", "effects": {"hp": 15, "xp": 10},
                 "narrative": "You place a flower on the shrine. The oasis seems to shimmer in response."},
                {"id": "search", "label": "Search the bones", "effects": {"items": [("scrap_bone", 3), ("copper_ore", 1)]},
                 "narrative": "You pick through the offerings. Useful bones and a bit of copper."},
            ],
        },
    ],
    "blooming_desert": [
        {
            "id": "nomad_trader", "name": "Nomad Trader",
            "type": "merchant", "weight": 15, "min_level": 1,
            "desc": "A lone nomad leads a pack lizard loaded with pouches and bundles. 'Desert goods! Rare and dry!'",
            "actions": [
                {"id": "buy", "label": "Buy (-20 gold)", "effects": {"gold": -20, "items": [("greater_healing_potion", 1), ("oasis_water", 2)]},
                 "narrative": "You buy a potion and water. The nomad nods and moves on, lizard in tow."},
                {"id": "trade", "label": "Trade herbs for supplies", "effects": {"items": [("oasis_water", 3), ("wild_herb", -2)]},
                 "narrative": "You swap desert herbs for water. A fair trade in the blooming desert."},
            ],
        },
        {
            "id": "sandstorm_hazard", "name": "Sandstorm",
            "type": "hazard", "weight": 20, "min_level": 1,
            "desc": "The horizon turns brown. A wall of sand roars across the desert toward you!",
            "actions": [
                {"id": "shelter", "label": "Shelter behind a dune", "effects": {"hp": -5},
                 "narrative": "You press into the leeward side of a dune as sand screams overhead. You'll be digging grit out for days."},
                {"id": "push", "label": "Push through it", "effects": {"hp": -15, "items": [("desert_glass", 2)]},
                 "narrative": "You force your way through the storm. The sand polishes stone to glass — you pocket some."},
            ],
        },
        {
            "id": "dune_beast_ambush", "name": "Dune Beast Ambush",
            "type": "combat", "weight": 20, "min_level": 1,
            "desc": "A massive shape crests the dune above you — all teeth and scales, charging down the slope.",
            "actions": [
                {"id": "fight", "label": "Fight the dune beast", "effects": {"combat": "boar"},
                 "narrative": "You plant your feet at the dune's base. The beast thunders down at you."},
                {"id": "roll", "label": "Roll sideways", "effects": {"hp": -6},
                 "narrative": "You throw yourself sideways. The beast overshoots and vanishes over the next dune."},
            ],
        },
        {
            "id": "desert_shrine", "name": "Desert Shrine",
            "type": "shrine", "weight": 10, "min_level": 1,
            "desc": "A stone shrine half-buried in sand, its carving still sharp. Someone has been keeping it clear.",
            "actions": [
                {"id": "pray", "label": "Brush the sand away and pray", "effects": {"hp": 20, "xp": 12},
                 "narrative": "You clear the shrine and kneel. The desert wind calms. Something here endures."},
                {"id": "search", "label": "Dig beneath the shrine", "effects": {"gold": 15, "items": [("copper_ore", 2)]},
                 "narrative": "You dig and find old coins and ore. The shrine's keeper won't be pleased."},
            ],
        },
    ],
    "beastwood": [
        {
            "id": "beast_tamer_npc", "name": "The Beast Tamer",
            "type": "npc", "weight": 15, "min_level": 1,
            "desc": "A wildblood sits calmly beside a massive predator, scratching it behind the ears. 'Beautiful, isn't she?'",
            "actions": [
                {"id": "learn", "label": "Ask for tracking tips", "effects": {"xp": 25, "items": [("scrap_bone", 2)]},
                 "narrative": "The tamer teaches you predator behavior. The beast watches you the whole time."},
                {"id": "back", "label": "Back away slowly", "effects": {},
                 "narrative": "You decide not to test the beast's patience. The tamer waves goodbye."},
            ],
        },
        {
            "id": "predator_ambush_beastwood", "name": "Predator Ambush",
            "type": "combat", "weight": 20, "min_level": 1,
            "desc": "A predator drops from the canopy — silent, fast, and directly above you.",
            "actions": [
                {"id": "fight", "label": "Fight the predator", "effects": {"combat": "boar"},
                 "narrative": "You roll and draw your weapon. The predator circles, looking for an opening."},
                {"id": "freeze", "label": "Stand perfectly still", "effects": {"hp": -4},
                 "narrative": "You freeze. The predator sniffs you, loses interest, and climbs back up."},
            ],
        },
        {
            "id": "rare_herb_cache_beastwood", "name": "Rare Herb Cache",
            "type": "resource", "weight": 15, "min_level": 1,
            "desc": "In a clearing trampled by beasts, rare herbs grow in the disturbed soil — they only grow where beasts tread.",
            "actions": [
                {"id": "harvest", "label": "Harvest the rare herbs", "effects": {"items": [("beastwood_herb", 3)]},
                 "narrative": "You gather the herbs quickly. Something growls in the distance — best to move."},
                {"id": "leave", "label": "Too risky", "effects": {},
                 "narrative": "You hear predators nearby. You decide the herbs aren't worth it."},
            ],
        },
        {
            "id": "beast_shrine", "name": "Beast Shrine",
            "type": "shrine", "weight": 10, "min_level": 1,
            "desc": "A shrine of bone and wood, hung with teeth and claws — offerings from successful hunts.",
            "actions": [
                {"id": "pray", "label": "Add a token", "effects": {"hp": 15, "xp": 15},
                 "narrative": "You add a small token. The shrine's spirit acknowledges a fellow hunter."},
                {"id": "take", "label": "Take the teeth and claws", "effects": {"items": [("scrap_bone", 3), ("wolf_fang", 2)], "hp": -6},
                 "narrative": "You pocket the offerings. A low growl follows you through the wood."},
            ],
        },
    ],
    "roaring_savanna": [
        {
            "id": "herd_stampede_savanna", "name": "Herd Stampede",
            "type": "hazard", "weight": 20, "min_level": 1,
            "desc": "The ground shakes. A herd of massive beasts thunders across the savanna, straight toward you!",
            "actions": [
                {"id": "climb", "label": "Climb a tree", "effects": {"hp": -3},
                 "narrative": "You scramble up a baobab. The herd passes below, shaking the tree like an earthquake."},
                {"id": "run_along", "label": "Run with the herd", "effects": {"hp": -12, "items": [("beast_hide", 1)]},
                 "narrative": "You sprint alongside the stampede and grab a fallen beast's hide. Exhausting, but worth it."},
            ],
        },
        {
            "id": "pride_lion_ambush", "name": "Pride Lion Ambush",
            "type": "combat", "weight": 20, "min_level": 1,
            "desc": "A massive lion steps onto the path, mane bristling. Behind it, two more appear in the grass.",
            "actions": [
                {"id": "fight", "label": "Fight the pride leader", "effects": {"combat": "boar"},
                 "narrative": "You face the lion. The pride fans out behind it. This is going to be rough."},
                {"id": "back", "label": "Back away without eye contact", "effects": {"hp": -4},
                 "narrative": "You retreat slowly, never breaking eye contact. The lion holds its ground. You escape."},
            ],
        },
        {
            "id": "savanna_merchant", "name": "Savanna Trader",
            "type": "merchant", "weight": 15, "min_level": 1,
            "desc": "A wildblood trader sits under a sun shade, surrounded by bundled hides and dried meats.",
            "actions": [
                {"id": "buy", "label": "Buy (-20 gold)", "effects": {"gold": -20, "items": [("greater_healing_potion", 1), ("beast_hide", 2)]},
                 "narrative": "You buy potions and quality hides. The trader nods approvingly."},
                {"id": "skip", "label": "Move on", "effects": {},
                 "narrative": "You wave and continue across the savanna."},
            ],
        },
        {
            "id": "savanna_shrine", "name": "Savanna Shrine",
            "type": "shrine", "weight": 10, "min_level": 1,
            "desc": "A circle of standing stones on a rise, wind-polished and ancient. The grass around them grows taller.",
            "actions": [
                {"id": "pray", "label": "Stand in the circle", "effects": {"hp": 20, "xp": 15},
                 "narrative": "You step into the circle. The wind picks up, then settles. You feel the savanna's heartbeat."},
                {"id": "search", "label": "Search the stones", "effects": {"gold": 12, "items": [("copper_ore", 2)]},
                 "narrative": "You find coins and ore wedged between the stones. Old offerings, forgotten."},
            ],
        },
    ],
    "ancient_den": [
        {
            "id": "spirit_guide_npc", "name": "Spirit Guide",
            "type": "npc", "weight": 15, "min_level": 1,
            "desc": "A spectral wildblood appears at the den's entrance, translucent and ancient. 'You carry the blood. Enter.'",
            "actions": [
                {"id": "enter", "label": "Follow the guide", "effects": {"xp": 35, "items": [("relic_shard", 1)]},
                 "narrative": "The guide leads you to a hidden chamber. Ancient totems line the walls. You take a shard."},
                {"id": "refuse", "label": "Not ready", "effects": {},
                 "narrative": "You bow and step back. The guide nods — you'll return when you're ready."},
            ],
        },
        {
            "id": "alpha_beast_ambush", "name": "Alpha Beast Ambush",
            "type": "combat", "weight": 20, "min_level": 1,
            "desc": "The den's alpha blocks your path — massive, scarred, and utterly fearless.",
            "actions": [
                {"id": "fight", "label": "Challenge the alpha", "effects": {"combat": "boar"},
                 "narrative": "The alpha roars. You roar back. The den falls silent."},
                {"id": "submit", "label": "Show submission", "effects": {"hp": -5, "xp": 10},
                 "narrative": " you lower your head and bare your neck. The alpha sniffs you, accepts the gesture, and lets you pass."},
            ],
        },
        {
            "id": "ancient_cache_den", "name": "Ancient Cache",
            "type": "mystery", "weight": 10, "min_level": 1,
            "desc": "A hollow in the den wall reveals a cache wrapped in ancient leather — older than any living bloodline.",
            "actions": [
                {"id": "open", "label": "Open the cache", "effects": {"items": [("relic_shard", 1), ("wolf_fang", 3)]},
                 "narrative": "You unwrap the leather. Inside: a relic shard and ritual fangs, preserved for centuries."},
                {"id": "seal", "label": "Leave it sealed", "effects": {"xp": 15},
                 "narrative": "You respect the old ways and leave the cache. The den seems to approve."},
            ],
        },
        {
            "id": "ancestor_shrine_den", "name": "Ancestor Shrine",
            "type": "shrine", "weight": 10, "min_level": 1,
            "desc": "A totem shrine at the den's heart, carved with the faces of a hundred generations of wildbloods.",
            "actions": [
                {"id": "pray", "label": "Press your hand to the totem", "effects": {"hp": 25, "xp": 20},
                 "narrative": "The wood is warm. You feel the ancestors' presence — watchful, proud, patient."},
                {"id": "take", "label": "Carve a piece off", "effects": {"items": [("ancient_wood", 1)], "hp": -12},
                 "narrative": "You carve a piece of the totem. The den goes silent. Something follows you out."},
            ],
        },
    ],
    # ==================== HYLION ====================
    "tide_pools": [
        {
            "id": "beachcomber_merchant", "name": "Beachcomber",
            "type": "merchant", "weight": 15, "min_level": 1,
            "desc": "A hyliondrian spreads goods on a rock — shells, dried kelp, and potions in waterproof flasks.",
            "actions": [
                {"id": "buy", "label": "Buy (-15 gold)", "effects": {"gold": -15, "items": [("minor_healing_potion", 2), ("sea_salt", 1)]},
                 "narrative": "You buy potions and blessed salt. The beachcomber wraps them in kelp-paper."},
                {"id": "skip", "label": "Move on", "effects": {},
                 "narrative": "You wave and continue along the tide pools."},
            ],
        },
        {
            "id": "tide_creature_ambush", "name": "Tide Creature Ambush",
            "type": "combat", "weight": 20, "min_level": 1,
            "desc": "Something moves under the water — a many-legged shape scuttles from a tide pool!",
            "actions": [
                {"id": "fight", "label": "Fight the tide creature", "effects": {"combat": "tide_crawler"},
                 "narrative": "You draw your weapon as the creature surfaces. Salt water sprays."},
                {"id": "splash", "label": "Splash and retreat", "effects": {"hp": -3},
                 "narrative": "You kick water into its eyes and scramble back. The creature sinks into its pool."},
            ],
        },
        {
            "id": "tidal_pool_cache", "name": "Tidal Pool Cache",
            "type": "resource", "weight": 15, "min_level": 1,
            "desc": "A deep tide pool reveals glints of color — shells, pearls, and something that glows.",
            "actions": [
                {"id": "harvest", "label": "Reach in", "effects": {"items": [("sea_shell", 3), ("sea_salt", 2)]},
                 "narrative": "You gather shells and salt. The pool seems to replenish as you take."},
                {"id": "leave", "label": "Too deep to reach", "effects": {},
                 "narrative": "The pool is deeper than it looks. You decide not to risk your arm."},
            ],
        },
        {
            "id": "tide_shrine", "name": "Tide Shrine",
            "type": "shrine", "weight": 10, "min_level": 1,
            "desc": "A shrine carved into a tide-washed rock, only visible at low tide. Salt crystals line its base.",
            "actions": [
                {"id": "pray", "label": "Kneel in the shallows", "effects": {"hp": 15, "xp": 10},
                 "narrative": "You kneel in the cold water. The tide seems to pause for a moment, then resumes."},
                {"id": "collect", "label": "Collect the salt crystals", "effects": {"items": [("sea_salt", 3)]},
                 "narrative": "You scrape crystals from the shrine's base. They tingle in your pack."},
            ],
        },
    ],
    "coral_gardens": [
        {
            "id": "coral_merchant", "name": "Coral Merchant",
            "type": "merchant", "weight": 15, "min_level": 1,
            "desc": "A hyliondrian tends a shop built into living coral. 'Pearls, potions, coral tools — all grown, not mined!'",
            "actions": [
                {"id": "buy", "label": "Buy (-20 gold)", "effects": {"gold": -20, "items": [("greater_healing_potion", 1), ("sea_pearl", 1)]},
                 "narrative": "You buy a potion and a pearl. The merchant wraps them in living coral that heals around them."},
                {"id": "skip", "label": "Just looking", "effects": {},
                 "narrative": "You admire the coral shop and move on."},
            ],
        },
        {
            "id": "reef_creature_ambush", "name": "Reef Creature Ambush",
            "type": "combat", "weight": 20, "min_level": 1,
            "desc": "A section of reef detaches and swims toward you — it's not coral at all, but a creature wearing coral as armor.",
            "actions": [
                {"id": "fight", "label": "Fight the reef creature", "effects": {"combat": "tide_crawler"},
                 "narrative": "The creature's coral armor clatters as it charges. You brace in the shallows."},
                {"id": "hide", "label": "Duck into a coral tube", "effects": {"hp": -4},
                 "narrative": "You squeeze into a coral formation. The creature circles, then wanders off."},
            ],
        },
        {
            "id": "pearl_cache", "name": "Pearl Cache",
            "type": "mystery", "weight": 10, "min_level": 1,
            "desc": "A giant clam sits open in a sunlit patch of reef, its pearl visible and glowing.",
            "actions": [
                {"id": "take", "label": "Take the pearl", "effects": {"items": [("sea_pearl", 2)], "gold": 20},
                 "narrative": "You slip the pearl from the clam. It closes slowly, unbothered. A second pearl rolls free."},
                {"id": "leave", "label": "Leave it for the reef", "effects": {"xp": 10},
                 "narrative": "You decide the reef needs the pearl more than you do. The clam seems to nod."},
            ],
        },
        {
            "id": "coral_shrine", "name": "Coral Shrine",
            "type": "shrine", "weight": 10, "min_level": 1,
            "desc": "A shrine grown from living coral, shaped by generations of hyliondrians into a place of meditation.",
            "actions": [
                {"id": "pray", "label": "Meditate among the coral", "effects": {"hp": 20, "xp": 15},
                 "narrative": "You sit among the living shrine. The coral's slow heartbeat calms your own."},
                {"id": "harvest", "label": "Break off a piece of coral", "effects": {"items": [("coral_fragment", 2)], "hp": -6},
                 "narrative": "You snap off a piece. The shrine's color dims where you broke it. The reef shudders."},
            ],
        },
    ],
    "kelp_forest": [
        {
            "id": "kelp_gatherer_npc", "name": "Kelp Gatherer",
            "type": "npc", "weight": 15, "min_level": 1,
            "desc": "A hyliondrian harvests kelp with practiced strokes, cutting only the oldest fronds. 'The forest provides,' they say.",
            "actions": [
                {"id": "learn", "label": "Learn the technique", "effects": {"xp": 20, "items": [("kelp_frond", 3)]},
                 "narrative": "The gatherer teaches you which fronds to cut. You leave with kelp and knowledge."},
                {"id": "trade", "label": "Trade (-10 gold)", "effects": {"gold": -10, "items": [("kelp_frond", 4), ("sea_salt", 1)]},
                 "narrative": "You trade coin for a bundle of kelp and some salt."},
            ],
        },
        {
            "id": "kelp_predator_ambush", "name": "Forest Predator Ambush",
            "type": "combat", "weight": 20, "min_level": 1,
            "desc": "The kelp rustles — something large moves through the forest, circling you.",
            "actions": [
                {"id": "fight", "label": "Fight the predator", "effects": {"combat": "tide_crawler"},
                 "narrative": "You draw your weapon as the shape lunges from the kelp."},
                {"id": "hide", "label": "Hide in the kelp", "effects": {"hp": -3},
                 "narrative": " you press into the kelp forest. The predator circles, then moves on."},
            ],
        },
        {
            "id": "hidden_kelp_cache", "name": "Hidden Kelp Cache",
            "type": "resource", "weight": 15, "min_level": 1,
            "desc": "A hollow in the kelp forest holds a cache of rare sea herbs and dried goods.",
            "actions": [
                {"id": "take", "label": "Take the cache", "effects": {"items": [("kelp_frond", 3), ("sea_pearl", 1)]},
                 "narrative": "You gather the cache. The kelp sways as if acknowledging the exchange."},
                {"id": "leave", "label": "Leave it", "effects": {},
                 "narrative": "You decide not to take from the forest. It's not yours."},
            ],
        },
        {
            "id": "kelp_shrine", "name": "Kelp Shrine",
            "type": "shrine", "weight": 10, "min_level": 1,
            "desc": "A clearing in the kelp forest where light filters down. A stone shrine sits on the seafloor, covered in tiny shells.",
            "actions": [
                {"id": "pray", "label": "Float in the light", "effects": {"hp": 20, "xp": 12},
                 "narrative": "You float in the shaft of light. The kelp sways in rhythm. You feel held by the sea."},
                {"id": "search", "label": "Search the shells", "effects": {"items": [("sea_shell", 3), ("sea_pearl", 1)]},
                 "narrative": "You pick through the shells and find a pearl among them."},
            ],
        },
    ],
    "storm_reefs": [
        {
            "id": "shipwreck_scavenger", "name": "Shipwreck Scavenger",
            "type": "merchant", "weight": 15, "min_level": 1,
            "desc": "A hyliondrian sorts through a shipwreck, laying out salvaged goods on the reef's flat top.",
            "actions": [
                {"id": "buy", "label": "Buy salvaged goods (-20 gold)", "effects": {"gold": -20, "items": [("greater_healing_potion", 2), ("coin_purse", 1)]},
                 "narrative": "You buy potions and a recovered coin purse. The scavenger grins — good haul today."},
                {"id": "skip", "label": "Move on", "effects": {},
                 "narrative": "You wave and swim past the wreck. The scavenger returns to sorting."},
            ],
        },
        {
            "id": "lightning_strike_hazard", "name": "Lightning Strike",
            "type": "hazard", "weight": 20, "min_level": 1,
            "desc": "The storm above crackles — and a bolt of lightning strikes the water right next to you!",
            "actions": [
                {"id": "dive", "label": "Dive deep", "effects": {"hp": -8},
                 "narrative": "You plunge underwater as the bolt hits the surface. The shock tingles through you."},
                {"id": "ride", "label": "Ride the current", "effects": {"hp": -15, "items": [("storm_crystal", 2)]},
                 "narrative": "You let the charge flow through you — painful, but it crystallizes the minerals in the water."},
            ],
        },
        {
            "id": "storm_creature_ambush", "name": "Storm Creature Ambush",
            "type": "combat", "weight": 20, "min_level": 1,
            "desc": "A creature made of lightning and salt water rises from the reef, crackling with energy.",
            "actions": [
                {"id": "fight", "label": "Fight the storm creature", "effects": {"combat": "grove_wisp"},
                 "narrative": "The creature sparks and lunges. You raise your weapon against the light."},
                {"id": "ground", "label": "Press yourself to the reef", "effects": {"hp": -5},
                 "narrative": "You press flat against the reef. The creature's charge grounds harmlessly through the stone."},
            ],
        },
        {
            "id": "storm_shrine", "name": "Storm Shrine",
            "type": "shrine", "weight": 10, "min_level": 1,
            "desc": "A shrine built on the reef's highest point, where lightning strikes regularly. The stone is fused and smooth.",
            "actions": [
                {"id": "pray", "label": "Stand in the storm", "effects": {"hp": 20, "xp": 20},
                 "narrative": "You stand as lightning cracks around you. The shrine channels it — through you, not into you."},
                {"id": "take", "label": "Pry a fused stone loose", "effects": {"items": [("storm_crystal", 1)], "hp": -10},
                 "narrative": "You pry a lightning-fused stone from the shrine. The storm intensifies briefly."},
            ],
        },
    ],
    "abyssal_trench": [
        {
            "id": "deep_diver_npc", "name": "The Deep Diver",
            "type": "npc", "weight": 15, "min_level": 1,
            "desc": "A hyliondrian in a pressure-suit hangs in the dark water, examining something on the trench wall. 'Look at this,' they signal.",
            "actions": [
                {"id": "look", "label": "Swim closer", "effects": {"xp": 30, "items": [("relic_shard", 1)]},
                 "narrative": "The diver shows you ancient carvings on the trench wall. You take a rubbing — and a shard falls free."},
                {"id": "leave", "label": "Too deep", "effects": {},
                 "narrative": "The pressure is uncomfortable. You signal goodbye and ascend."},
            ],
        },
        {
            "id": "abyssal_creature_ambush", "name": "Abyssal Creature Ambush",
            "type": "combat", "weight": 20, "min_level": 1,
            "desc": "Something enormous stirs in the trench below. Two lights appear — eyes, bioluminescent and hungry.",
            "actions": [
                {"id": "fight", "label": "Fight the abyssal creature", "effects": {"combat": "ruin_ghast"},
                 "narrative": "The creature rises from the dark. You grip your weapon and pray the pressure holds."},
                {"id": "ascend", "label": "Swim for the surface", "effects": {"hp": -8},
                 "narrative": " you kick hard for the light above. The creature's eyes track you, then turn away."},
            ],
        },
        {
            "id": "trench_cache", "name": "Trench Cache",
            "type": "mystery", "weight": 10, "min_level": 1,
            "desc": "On the trench floor, a structure — not natural, not modern. Something from before the sea was here.",
            "actions": [
                {"id": "enter", "label": "Enter the structure", "effects": {"xp": 35, "items": [("relic_shard", 1), ("sea_pearl", 2)]},
                 "narrative": "You swim inside. Ancient air still fills it. You take what's offered and leave quickly."},
                {"id": "observe", "label": "Observe from outside", "effects": {"xp": 15},
                 "narrative": "You study the structure's outline. Old. Very old. You'll remember this."},
            ],
        },
        {
            "id": "abyss_shrine", "name": "Abyss Shrine",
            "type": "shrine", "weight": 10, "min_level": 1,
            "desc": "A shrine on the trench floor, lit by its own bioluminescence. The dark feels less heavy around it.",
            "actions": [
                {"id": "pray", "label": "Kneel in the dark", "effects": {"hp": 25, "xp": 20},
                 "narrative": "You kneel in the lightless deep. The shrine's glow wraps around you like a blanket."},
                {"id": "take", "label": "Take the glowing stones", "effects": {"items": [("abyss_gem", 2)], "hp": -10},
                 "narrative": "You pocket the glowing stones. The shrine goes dark. The trench feels deeper."},
            ],
        },
    ],
    # ==================== DAW'UL TALALU ====================
    "misty_thicket": [
        {
            "id": "mist_sprite_npc", "name": "Mist Sprite",
            "type": "npc", "weight": 15, "min_level": 1,
            "desc": "A small figure made of mist darts between the thorns, giggling. It pauses and tilts its head at you.",
            "actions": [
                {"id": "follow", "label": "Follow the sprite", "effects": {"xp": 20, "items": [("shadow_herb", 2)]},
                 "narrative": "The sprite leads you through the mist to a hidden clearing of shadow herbs."},
                {"id": "ignore", "label": "Ignore the giggling", "effects": {},
                 "narrative": "You push through the mist. The giggling fades behind you."},
            ],
        },
        {
            "id": "thorn_creature_ambush", "name": "Thorn Creature Ambush",
            "type": "combat", "weight": 20, "min_level": 1,
            "desc": "The thorns around you shift — they're not plants, they're limbs. A creature of briars rises around you!",
            "actions": [
                {"id": "fight", "label": "Fight the thorn creature", "effects": {"combat": "boar"},
                 "narrative": "You cut at the thorn-limbs. They regrow as fast as you sever them."},
                {"id": "burn", "label": "Use fire to scare it", "effects": {"hp": -4},
                 "narrative": "You light a torch. The thorn creature recoils from the flame and sinks back."},
            ],
        },
        {
            "id": "hidden_herb_cache_misty", "name": "Hidden Herb Cache",
            "type": "resource", "weight": 15, "min_level": 1,
            "desc": "A patch of shadow herbs grows in a mist-filled hollow, glowing faintly in the gloom.",
            "actions": [
                {"id": "harvest", "label": "Harvest the shadow herbs", "effects": {"items": [("shadow_herb", 4)]},
                 "narrative": "You gather the dark herbs. They're cool to the touch and smell of mist."},
                {"id": "leave", "label": "Leave the misty hollow", "effects": {},
                 "narrative": "The mist is too thick. You decide to come back with a light."},
            ],
        },
        {
            "id": "mist_shrine", "name": "Mist Shrine",
            "type": "shrine", "weight": 10, "min_level": 1,
            "desc": "A shrine visible only when the mist parts — which it does, briefly, as you approach.",
            "actions": [
                {"id": "pray", "label": "Step through the mist", "effects": {"hp": 15, "xp": 12},
                 "narrative": "The mist parts for you. The shrine is warm and dry. You leave before the mist closes."},
                {"id": "search", "label": "Search around the shrine", "effects": {"items": [("shadow_herb", 2), ("relic_shard", 1)]},
                 "narrative": "You find herbs and a shard in the mist. The shrine permits it — this time."},
            ],
        },
    ],
    "mistwood": [
        {
            "id": "illusionist_npc", "name": "The Illusionist",
            "type": "npc", "weight": 15, "min_level": 1,
            "desc": "A sylvan sits on a branch that may or may not exist, shuffling cards that definitely don't. 'Pick one,' they grin.",
            "actions": [
                {"id": "pick", "label": "Pick a card", "effects": {"xp": 25, "items": [("shadow_herb", 2)]},
                 "narrative": "You pick the third card. The illusionist vanishes — and herbs fall from the branch where they sat."},
                {"id": "refuse", "label": "Don't play games", "effects": {},
                 "narrative": "You walk past. The branch creaks — or does it? You don't look back."},
            ],
        },
        {
            "id": "shadow_ambush_mistwood", "name": "Shadow Ambush",
            "type": "combat", "weight": 20, "min_level": 1,
            "desc": "A shadow detaches from the mist and solidifies — humanoid, faceless, reaching.",
            "actions": [
                {"id": "fight", "label": "Fight the shadow", "effects": {"combat": "ruin_ghast"},
                 "narrative": "You strike at the shadow. Your blade passes through — then catches on something solid inside."},
                {"id": "light", "label": "Create light", "effects": {"hp": -3},
                 "narrative": "You ignite a torch. The shadow shrieks and dissolves into the mist."},
            ],
        },
        {
            "id": "hidden_path_mistwood", "name": "Hidden Path",
            "type": "mystery", "weight": 10, "min_level": 1,
            "desc": "The mist parts to reveal a path that wasn't there before. It leads deeper into the wood.",
            "actions": [
                {"id": "follow", "label": "Follow the path", "effects": {"xp": 30, "items": [("relic_shard", 1)]},
                 "narrative": "The path leads to a hidden grove. Something old waits there — and offers you a shard."},
                {"id": "ignore", "label": "Stay on the main path", "effects": {"xp": 8},
                 "narrative": "You decide not to follow paths that appear from nowhere. The mist closes behind you."},
            ],
        },
        {
            "id": "mist_shrine_mistwood", "name": "Mistwood Shrine",
            "type": "shrine", "weight": 10, "min_level": 1,
            "desc": "A shrine that exists in multiple places at once — you can see it from three angles, and it looks different from each.",
            "actions": [
                {"id": "pray", "label": "Kneel at the shrine", "effects": {"hp": 20, "xp": 15},
                 "narrative": "You kneel. The shrine settles into one form — the one that matches your need."},
                {"id": "study", "label": "Study the illusion", "effects": {"xp": 20},
                 "narrative": "You study the shifting shrine. You learn something about perception itself."},
            ],
        },
    ],
    "thorn_labyrinth": [
        {
            "id": "thorn_guide_npc", "name": "Thorn Guide",
            "type": "npc", "weight": 15, "min_level": 1,
            "desc": "A sylvan stands at a fork in the labyrinth, marking the correct path with a thorn-ribbon. 'This one,' they say.",
            "actions": [
                {"id": "follow", "label": "Follow the guide", "effects": {"xp": 20, "items": [("thorn_vine", 3)]},
                 "narrative": "The guide leads you through safely and points out useful vines along the way."},
                {"id": "tip", "label": "Tip for the guidance (-10 gold)", "effects": {"gold": -10, "items": [("thorn_vine", 4), ("shadow_herb", 1)]},
                 "narrative": "You pay for the full tour. The guide shows you a hidden herb garden too."},
            ],
        },
        {
            "id": "plant_creature_ambush", "name": "Plant Creature Ambush",
            "type": "combat", "weight": 20, "min_level": 1,
            "desc": "The labyrinth walls close in — the thorns are growing, reaching, wrapping around your legs!",
            "actions": [
                {"id": "fight", "label": "Cut your way out", "effects": {"combat": "boar"},
                 "narrative": "You hack at the living thorns. They bleed sap and squeeze tighter."},
                {"id": "freeze", "label": "Go completely still", "effects": {"hp": -4},
                 "narrative": "You stop moving. The thorns slow, confused, then retract — they only chase moving things."},
            ],
        },
        {
            "id": "bramble_cache", "name": "Bramble Cache",
            "type": "resource", "weight": 15, "min_level": 1,
            "desc": "A hollow in the labyrinth wall holds a cache of thorn materials and herbs, wrapped in living vine.",
            "actions": [
                {"id": "take", "label": "Unwrap the cache", "effects": {"items": [("thorn_vine", 3), ("shadow_herb", 2)]},
                 "narrative": "You carefully unwrap the vine. The thorns don't resist — this cache was meant to be found."},
                {"id": "leave", "label": "Leave it wrapped", "effects": {},
                 "narrative": "You decide the labyrinth's gifts come with strings attached. You move on."},
            ],
        },
        {
            "id": "thorn_shrine", "name": "Thorn Shrine",
            "type": "shrine", "weight": 10, "min_level": 1,
            "desc": "A shrine grown from the labyrinth itself — a clearing where the thorns form a perfect circle, pointing inward.",
            "actions": [
                {"id": "pray", "label": "Stand in the circle", "effects": {"hp": 20, "xp": 15},
                 "narrative": "You stand in the center. The thorns point at you — not threatening, but protective."},
                {"id": "take", "label": "Take a thorn from the circle", "effects": {"items": [("thorn_vine", 3)], "hp": -8},
                 "narrative": "You snap a thorn from the circle. The formation collapses. The labyrinth shifts."},
            ],
        },
    ],
    "lumina_grove": [
        {
            "id": "light_creature_npc", "name": "Glow Creature",
            "type": "npc", "weight": 15, "min_level": 1,
            "desc": "A creature of pure bioluminescence drifts through the grove, leaving trails of light. It pauses near you, curious.",
            "actions": [
                {"id": "interact", "label": "Reach out to it", "effects": {"hp": 20, "xp": 15},
                 "narrative": "The creature touches your hand. Light flows through you — warm, healing, ancient."},
                {"id": "watch", "label": "Watch it drift", "effects": {"xp": 10},
                 "narrative": "You watch the creature paint light through the grove. Beautiful and strange."},
            ],
        },
        {
            "id": "glow_beast_ambush", "name": "Glow Beast Ambush",
            "type": "combat", "weight": 20, "min_level": 1,
            "desc": "A beast of bioluminescent fur charges from the glowing undergrowth, blazing with light!",
            "actions": [
                {"id": "fight", "label": "Fight the glow beast", "effects": {"combat": "boar"},
                 "narrative": "The beast's light blinds you as it charges. You swing at the glow."},
                {"id": "shield", "label": "Shield your eyes", "effects": {"hp": -4},
                 "narrative": "You cover your eyes. The beast's light dims as it loses interest and lumbers off."},
            ],
        },
        {
            "id": "biolume_cache", "name": "Biolume Cache",
            "type": "resource", "weight": 15, "min_level": 1,
            "desc": "A patch of bioluminescent flora grows in concentrated abundance, lighting up the entire grove section.",
            "actions": [
                {"id": "harvest", "label": "Harvest the glowing flora", "effects": {"items": [("lumina_petal", 4)]},
                 "narrative": "You gather the glowing petals. They pulse gently in your hands, lighting your way."},
                {"id": "rest", "label": "Rest in the glow", "effects": {"hp": 15},
                 "narrative": "You lie in the bioluminescent light. It's warm, like sunlight but softer. You feel mended."},
            ],
        },
        {
            "id": "lumina_shrine", "name": "Lumina Shrine",
            "type": "shrine", "weight": 10, "min_level": 1,
            "desc": "A shrine that glows from within, its light shifting through every color of the spectrum slowly, rhythmically.",
            "actions": [
                {"id": "pray", "label": "Bathe in the light", "effects": {"hp": 25, "xp": 18},
                 "narrative": "The shrine's light washes over you in slow waves. Each color heals something different."},
                {"id": "take", "label": "Take a glowing stone", "effects": {"items": [("lumina_stone", 2)], "hp": -8},
                 "narrative": "You pocket two glowing stones. The shrine's colors slow — as if something was taken from it."},
            ],
        },
    ],
    "elderroot_hollow": [
        {
            "id": "elder_tree_spirit_npc", "name": "Elder Tree Spirit",
            "type": "npc", "weight": 15, "min_level": 1,
            "desc": "A massive face forms in the bark of the oldest tree in the hollow. Its eyes open — ancient, patient, wise.",
            "actions": [
                {"id": "speak", "label": "Speak with the spirit", "effects": {"xp": 35, "items": [("relic_shard", 1)]},
                 "narrative": "The elder tree speaks of the world before the eight peoples. It gives you a shard — a piece of that memory."},
                {"id": "bow", "label": "Bow and leave", "effects": {"xp": 15},
                 "narrative": "You bow deeply. The tree's eyes close. You've shown respect to something older than nations."},
            ],
        },
        {
            "id": "ancient_creature_ambush", "name": "Ancient Creature Ambush",
            "type": "combat", "weight": 20, "min_level": 1,
            "desc": "The roots around you shift — something has been sleeping in the hollow for centuries, and you've woken it.",
            "actions": [
                {"id": "fight", "label": "Fight the ancient creature", "effects": {"combat": "ruin_ghast"},
                 "narrative": "The creature rises from the roots — massive, slow, and very, very old. It does not appreciate being woken."},
                {"id": "retreat", "label": "Back away slowly", "effects": {"hp": -5},
                 "narrative": "You step back, step by step. The creature watches, then settles back into its roots."},
            ],
        },
        {
            "id": "root_cache", "name": "Root Cache",
            "type": "mystery", "weight": 10, "min_level": 1,
            "desc": "A hollow between the roots of the elder tree holds objects — not dropped, but placed. Offerings, or treasures?",
            "actions": [
                {"id": "take", "label": "Take the offerings", "effects": {"items": [("relic_shard", 1), ("ancient_wood", 1), ("lumina_petal", 2)]},
                 "narrative": "You take the objects. The tree doesn't react — but the hollow closes behind you as you leave."},
                {"id": "add", "label": "Add something of your own", "effects": {"gold": -10, "xp": 25, "hp": 15},
                 "narrative": "You leave a coin in the hollow. The tree's bark shifts — approval. You feel blessed."},
            ],
        },
        {
            "id": "elderroot_shrine", "name": "Elderroot Shrine",
            "type": "shrine", "weight": 10, "min_level": 1,
            "desc": "A shrine grown into the elder tree itself — its bark has formed an altar, complete with living-candle flames of pure light.",
            "actions": [
                {"id": "pray", "label": "Kneel at the living altar", "effects": {"hp": 30, "xp": 25},
                 "narrative": "You kneel at the elder tree's altar. The living candles flare. You feel the weight of centuries — and their release."},
                {"id": "take", "label": "Take a living candle", "effects": {"items": [("elderroot_candle", 1)], "hp": -12},
                 "narrative": "You pluck a living flame from the altar. It burns in your hand — not with fire, but with age. The tree weeps sap."},
            ],
        },
    ],
}


# ============================================================
# CORE LOGIC
# ============================================================

def _cognition_bonus(character: dict | None) -> float:
    """Calculate encounter chance bonus from cognition stat."""
    if not character:
        return 0.0
    cog = character.get("stats", {}).get("cognition", 0)
    return min(COGNITION_BONUS_CAP, cog * COGNITION_BONUS_RATIO)


def maybe_trigger_encounter(character: dict, biome_id: str, action_id: str, outcome: int) -> dict | None:
    """Roll for a random encounter. Returns encounter dict or None.

    Trigger rules:
    - Explore outcome 4-5: 3% base
    - Explore outcome 6: 10% base
    - Other action outcome 6: 5% base
    - Cognition adds +30% of stat value, capped at +15%
    - Per-biome cooldown: 5 actions before biome can trigger again
    """
    if outcome < 4:
        return None

    # Determine base chance
    if action_id == "explore" and outcome in (4, 5):
        base = ENCOUNTER_BASE_CHANCE["explore_45"]
    elif action_id == "explore" and outcome == 6:
        base = ENCOUNTER_BASE_CHANCE["explore_6"]
    elif action_id != "explore" and outcome == 6:
        base = ENCOUNTER_BASE_CHANCE["other_6"]
    else:
        return None

    # Cognition bonus
    bonus = _cognition_bonus(character)
    chance = base + (bonus / 100.0)  # bonus is in percentage points

    # Per-biome cooldown check
    cooldowns = character.get("encounter_cooldowns", {})
    biome_cd = cooldowns.get(biome_id, 0)
    if biome_cd > 0:
        return None

    if random.random() > chance:
        return None

    # Pick an encounter from this biome
    encounters = BIOME_ENCOUNTERS.get(biome_id, [])
    if not encounters:
        return None

    # Filter by level
    char_level = character.get("level", 1)
    valid = [e for e in encounters if char_level >= e.get("min_level", 1)]
    if not valid:
        return None

    # Weighted random selection
    weights = [e.get("weight", 10) for e in valid]
    chosen = random.choices(valid, weights=weights, k=1)[0]
    return dict(chosen)


def tick_encounter_cooldowns(character: dict, biome_id: str) -> None:
    """Decrement all encounter cooldowns by 1 and set cooldown for the given biome."""
    cooldowns = character.setdefault("encounter_cooldowns", {})
    for bid in list(cooldowns.keys()):
        cooldowns[bid] = max(0, cooldowns[bid] - 1)
        if cooldowns[bid] == 0:
            del cooldowns[bid]
    cooldowns[biome_id] = BIOME_COOLDOWN_ACTIONS


def resolve_encounter_action(encounter: dict, action_id: str) -> dict:
    """Resolve the player's chosen encounter action. Returns result dict with effects and narrative."""
    action = next((a for a in encounter.get("actions", []) if a["id"] == action_id), None)
    if not action:
        return {"error": "Invalid encounter action"}

    effects = dict(action.get("effects", {}))
    return {
        "encounter_id": encounter["id"],
        "encounter_name": encounter["name"],
        "action_id": action_id,
        "action_label": action["label"],
        "effects": effects,
        "narrative": action["narrative"],
        "combat": effects.get("combat"),
    }
