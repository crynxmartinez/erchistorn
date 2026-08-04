"""Base items — handcrafted weapon, armor, and accessory definitions.
These are the templates that the drop generator uses to create item instances.
No 'power' field — items give stats that feed directly into combat formulas.
"""
from __future__ import annotations

# ============================================================
# Base Items
# ============================================================
# Each base item defines:
#   id, name, kind (weapon|armor|accessory), slot, base_stats, req_stats, req_level, tier (1-3)
#   Weapons: weapon_type, range (derived from weapon_type), two_handed (derived)
#   Armors: armor_type
#   desc: flavor text
#
# The generator adds prefixes, suffixes, quality, upgrades, and instance_id.

BASE_ITEMS: list[dict] = [

    # ============================================================
    # WEAPONS — Daggers (T1-T3)
    # ============================================================
    {"id": "iron_dagger", "name": "Iron Dagger", "kind": "weapon", "slot": "right_hand",
     "weapon_type": "dagger", "base_stats": {"might": 1, "grace": 1}, "req_stats": {}, "req_level": 1, "tier": 1,
     "desc": "A simple blade forged in any back-alley smithy. Its weight says more about its maker than its edge."},
    {"id": "steel_dagger", "name": "Steel Dagger", "kind": "weapon", "slot": "right_hand",
     "weapon_type": "dagger", "base_stats": {"might": 2, "grace": 2}, "req_stats": {"might": 10}, "req_level": 6, "tier": 2,
     "desc": "A refined blade with a needle point. The steel holds an edge through a dozen duels."},
    {"id": "shadow_dagger", "name": "Shadow Dagger", "kind": "weapon", "slot": "right_hand",
     "weapon_type": "dagger", "base_stats": {"might": 4, "grace": 3}, "req_stats": {"might": 18}, "req_level": 15, "tier": 3,
     "desc": "Forged in twilight, quenched in shadow. It disappears in low light — and so do its victims."},

    # ============================================================
    # WEAPONS — Swords 1H (T1-T3)
    # ============================================================
    {"id": "iron_longsword", "name": "Iron Longsword", "kind": "weapon", "slot": "right_hand",
     "weapon_type": "sword_1h", "base_stats": {"might": 2, "vitality": 1}, "req_stats": {"might": 8}, "req_level": 1, "tier": 1,
     "desc": "A soldier's blade, plain and reliable. The edge holds through a skirmish and the crossguard turns a blow."},
    {"id": "steel_longsword", "name": "Steel Longsword", "kind": "weapon", "slot": "right_hand",
     "weapon_type": "sword_1h", "base_stats": {"might": 4, "vitality": 2}, "req_stats": {"might": 14}, "req_level": 6, "tier": 2,
     "desc": "A well-balanced blade of folded steel. It sings when it cuts air and thuds when it cuts armor."},
    {"id": "crystal_longsword", "name": "Crystal Longsword", "kind": "weapon", "slot": "right_hand",
     "weapon_type": "sword_1h", "base_stats": {"might": 7, "vitality": 3}, "req_stats": {"might": 22}, "req_level": 15, "tier": 3,
     "desc": "A blade of crystallized essence. It hums in the hand and cuts through plate like mist through a lantern."},

    # ============================================================
    # WEAPONS — Swords 2H (T1-T3)
    # ============================================================
    {"id": "iron_greatsword", "name": "Iron Greatsword", "kind": "weapon", "slot": "right_hand",
     "weapon_type": "sword_2h", "base_stats": {"might": 5, "vitality": 2}, "req_stats": {"might": 12}, "req_level": 1, "tier": 1,
     "desc": "A blade that demands two hands and gives no quarter. The smith who forged it died of exhaustion — the sword did not."},
    {"id": "steel_greatsword", "name": "Steel Greatsword", "kind": "weapon", "slot": "right_hand",
     "weapon_type": "sword_2h", "base_stats": {"might": 8, "vitality": 3}, "req_stats": {"might": 18}, "req_level": 6, "tier": 2,
     "desc": "A towering blade of layered steel. It cleaves through shield, mail, and the confidence of anyone facing it."},
    {"id": "dragonbone_greatsword", "name": "Dragonbone Greatsword", "kind": "weapon", "slot": "right_hand",
     "weapon_type": "sword_2h", "base_stats": {"might": 12, "vitality": 5}, "req_stats": {"might": 25}, "req_level": 15, "tier": 3,
     "desc": "Carved from the femur of an ancient dragon. It is warm to the touch and remembers fire."},

    # ============================================================
    # WEAPONS — Axes 1H (T1-T3)
    # ============================================================
    {"id": "wolves_fang_axe", "name": "Wolf's Fang Axe", "kind": "weapon", "slot": "right_hand",
     "weapon_type": "axe_1h", "base_stats": {"might": 3, "vitality": 1}, "req_stats": {"might": 8}, "req_level": 1, "tier": 1,
     "desc": "Bone-hafted and wolf-fanged. Plains hunters say a piece of the beast's spirit still clings to it."},
    {"id": "iron_war_axe", "name": "Iron War Axe", "kind": "weapon", "slot": "right_hand",
     "weapon_type": "axe_1h", "base_stats": {"might": 5, "durability": 1}, "req_stats": {"might": 12}, "req_level": 6, "tier": 2,
     "desc": "A brutal chopping blade on a reinforced haft. It doesn't cut — it dismantles."},
    {"id": "beastcleaver", "name": "Beastcleaver", "kind": "weapon", "slot": "right_hand",
     "weapon_type": "axe_1h", "base_stats": {"might": 8, "durability": 2}, "req_stats": {"might": 20}, "req_level": 15, "tier": 3,
     "desc": "Named for what it does. The edge is chipped from use and still sharp enough to split a skull."},

    # ============================================================
    # WEAPONS — Great Axes 2H (T1-T3)
    # ============================================================
    {"id": "iron_great_axe", "name": "Iron Great Axe", "kind": "weapon", "slot": "right_hand",
     "weapon_type": "great_axe", "base_stats": {"might": 6, "vitality": 2}, "req_stats": {"might": 14}, "req_level": 1, "tier": 1,
     "desc": "A lumbering blade on a long haft. It swings slow and lands like a landslide."},
    {"id": "steel_great_axe", "name": "Steel Great Axe", "kind": "weapon", "slot": "right_hand",
     "weapon_type": "great_axe", "base_stats": {"might": 9, "vitality": 3}, "req_stats": {"might": 20}, "req_level": 6, "tier": 2,
     "desc": "A battlefield axe meant for cleaving through ranks. The haft is wrapped in leather and old prayers."},
    {"id": "godcleaver", "name": "Godcleaver", "kind": "weapon", "slot": "right_hand",
     "weapon_type": "great_axe", "base_stats": {"might": 14, "vitality": 5}, "req_stats": {"might": 28}, "req_level": 15, "tier": 3,
     "desc": "A legend says it cleaved a god's shield in two. The god is gone. The axe remains."},

    # ============================================================
    # WEAPONS — Hammers 1H (T1-T3)
    # ============================================================
    {"id": "bronze_mace", "name": "Bronze Mace", "kind": "weapon", "slot": "right_hand",
     "weapon_type": "hammer_1h", "base_stats": {"might": 3, "vitality": 2}, "req_stats": {"might": 8}, "req_level": 1, "tier": 1,
     "desc": "A weighted club of bronze and oak. It doesn't cut — it convinces. Arguments end quickly when it speaks."},
    {"id": "war_hammer", "name": "War Hammer", "kind": "weapon", "slot": "right_hand",
     "weapon_type": "hammer_1h", "base_stats": {"might": 5, "durability": 2}, "req_stats": {"might": 12}, "req_level": 6, "tier": 2,
     "desc": "A hammer built for cracking plate. The head is hexagonal and the pein could punch through a door."},
    {"id": "doom_hammer", "name": "Doom Hammer", "kind": "weapon", "slot": "right_hand",
     "weapon_type": "hammer_1h", "base_stats": {"might": 8, "durability": 3}, "req_stats": {"might": 20}, "req_level": 15, "tier": 3,
     "desc": "The head is inscribed with runes that translate roughly to 'stop.' Most things do."},

    # ============================================================
    # WEAPONS — Great Hammers 2H (T1-T3)
    # ============================================================
    {"id": "iron_great_hammer", "name": "Iron Great Hammer", "kind": "weapon", "slot": "right_hand",
     "weapon_type": "great_hammer", "base_stats": {"might": 7, "vitality": 3, "durability": 2}, "req_stats": {"might": 14}, "req_level": 1, "tier": 1,
     "desc": "A sledgehammer given a handle and a purpose. It crushes what it cannot cut, which is everything."},
    {"id": "steel_great_hammer", "name": "Steel Great Hammer", "kind": "weapon", "slot": "right_hand",
     "weapon_type": "great_hammer", "base_stats": {"might": 10, "vitality": 4, "durability": 3}, "req_stats": {"might": 20}, "req_level": 6, "tier": 2,
     "desc": "A two-handed hammer that turns armor into scrap metal. The ground shakes when it lands."},
    {"id": "worldbreaker", "name": "Worldbreaker", "kind": "weapon", "slot": "right_hand",
     "weapon_type": "great_hammer", "base_stats": {"might": 15, "vitality": 6, "durability": 4}, "req_stats": {"might": 28}, "req_level": 15, "tier": 3,
     "desc": "They say it cracked the foundation of a fortress. The fortress disagrees, but it is no longer standing."},

    # ============================================================
    # WEAPONS — Spears 2H (T1-T3)
    # ============================================================
    {"id": "iron_spear", "name": "Iron Spear", "kind": "weapon", "slot": "right_hand",
     "weapon_type": "spear", "base_stats": {"might": 3, "grace": 2}, "req_stats": {"might": 8, "grace": 6}, "req_level": 1, "tier": 1,
     "desc": "A simple thrusting spear. Reach is its virtue — the enemy dies before they can return the favor."},
    {"id": "steel_spear", "name": "Steel Spear", "kind": "weapon", "slot": "right_hand",
     "weapon_type": "spear", "base_stats": {"might": 5, "grace": 3}, "req_stats": {"might": 14, "grace": 10}, "req_level": 6, "tier": 2,
     "desc": "A steel-tipped spear with a leaf blade. It punches through mail and keeps going."},
    {"id": "dragonlance", "name": "Dragonlance", "kind": "weapon", "slot": "right_hand",
     "weapon_type": "spear", "base_stats": {"might": 8, "grace": 5}, "req_stats": {"might": 22, "grace": 16}, "req_level": 15, "tier": 3,
     "desc": "A lance forged to pierce dragon scale. It has done so exactly once, and the story is carved on the blade."},

    # ============================================================
    # WEAPONS — Scythes 2H (T1-T3)
    # ============================================================
    {"id": "gloomreaper_scythe", "name": "Gloomreaper Scythe", "kind": "weapon", "slot": "right_hand",
     "weapon_type": "scythe", "base_stats": {"might": 5, "insight": 3}, "req_stats": {"might": 10, "insight": 8}, "req_level": 1, "tier": 1,
     "desc": "Not meant for the living. The blade was quenched in shadow, and the haft remembers hands that are no longer attached to anything."},
    {"id": "soulreaper_scythe", "name": "Soulreaper Scythe", "kind": "weapon", "slot": "right_hand",
     "weapon_type": "scythe", "base_stats": {"might": 8, "insight": 5}, "req_stats": {"might": 18, "insight": 14}, "req_level": 6, "tier": 2,
     "desc": "The blade harvests more than grain. Souls cling to it like burrs to a cloak."},
    {"id": "eternal_reaper", "name": "Eternal Reaper", "kind": "weapon", "slot": "right_hand",
     "weapon_type": "scythe", "base_stats": {"might": 12, "insight": 8}, "req_stats": {"might": 26, "insight": 20}, "req_level": 15, "tier": 3,
     "desc": "The scythe that ends all things. It does not rust. It does not dull. It waits."},

    # ============================================================
    # WEAPONS — Katars 2H (T1-T3)
    # ============================================================
    {"id": "iron_katar", "name": "Iron Katar", "kind": "weapon", "slot": "right_hand",
     "weapon_type": "katar", "base_stats": {"might": 2, "grace": 2}, "req_stats": {"might": 6, "grace": 6}, "req_level": 1, "tier": 1,
     "desc": "A punching dagger gripped in the fist. Fast, close, and personal — the way alchemists like it."},
    {"id": "steel_katar", "name": "Steel Katar", "kind": "weapon", "slot": "right_hand",
     "weapon_type": "katar", "base_stats": {"might": 4, "grace": 3}, "req_stats": {"might": 12, "grace": 10}, "req_level": 6, "tier": 2,
     "desc": "Tri-bladed katar with a reinforced grip. Each blade is a different length — the middle one is the surprise."},
    {"id": "void_katar", "name": "Void Katar", "kind": "weapon", "slot": "right_hand",
     "weapon_type": "katar", "base_stats": {"might": 7, "grace": 5}, "req_stats": {"might": 20, "grace": 16}, "req_level": 15, "tier": 3,
     "desc": "The blades are black holes in the shape of edges. Light bends around them. So do opponents."},

    # ============================================================
    # WEAPONS — Orbs 1H (T1-T3)
    # ============================================================
    {"id": "moonstone_orb", "name": "Moonstone Orb", "kind": "weapon", "slot": "right_hand",
     "weapon_type": "orb", "base_stats": {"essence": 3, "insight": 2}, "req_stats": {"insight": 8}, "req_level": 1, "tier": 1,
     "desc": "A sphere of polished moonstone that glows in the dark. It channels essence like a lens focuses light."},
    {"id": "astral_orb", "name": "Astral Orb", "kind": "weapon", "slot": "right_hand",
     "weapon_type": "orb", "base_stats": {"essence": 6, "insight": 4}, "req_stats": {"insight": 16}, "req_level": 6, "tier": 2,
     "desc": "A swirling orb that contains a captured fragment of the night sky. It hums with cosmic resonance."},
    {"id": "cosmic_orb", "name": "Cosmic Orb", "kind": "weapon", "slot": "right_hand",
     "weapon_type": "orb", "base_stats": {"essence": 10, "insight": 7}, "req_stats": {"insight": 24}, "req_level": 15, "tier": 3,
     "desc": "The orb contains a galaxy. Looking into it too long makes you forget which side of the glass you're on."},

    # ============================================================
    # WEAPONS — Tomes 1H (T1-T3)
    # ============================================================
    {"id": "apprentice_tome", "name": "Apprentice Tome", "kind": "weapon", "slot": "right_hand",
     "weapon_type": "tome", "base_stats": {"insight": 3, "essence": 2}, "req_stats": {"insight": 6}, "req_level": 1, "tier": 1,
     "desc": "A worn spellbook with dog-eared pages. The ink smudges when you sweat, which is often."},
    {"id": "scholar_tome", "name": "Scholar Tome", "kind": "weapon", "slot": "right_hand",
     "weapon_type": "tome", "base_stats": {"insight": 6, "essence": 4}, "req_stats": {"insight": 14}, "req_level": 6, "tier": 2,
     "desc": "A leather-bound grimoire with gilded page edges. The spells inside are organized by lethality."},
    {"id": "archmage_tome", "name": "Archmage Tome", "kind": "weapon", "slot": "right_hand",
     "weapon_type": "tome", "base_stats": {"insight": 10, "essence": 7}, "req_stats": {"insight": 22}, "req_level": 15, "tier": 3,
     "desc": "The pages turn themselves. The spells inside are written in a language that predates the reader by millennia."},

    # ============================================================
    # WEAPONS — Bows 2H (T1-T3)
    # ============================================================
    {"id": "oak_shortbow", "name": "Oak Shortbow", "kind": "weapon", "slot": "right_hand",
     "weapon_type": "bow", "base_stats": {"grace": 2, "might": 1}, "req_stats": {"grace": 8}, "req_level": 1, "tier": 1,
     "desc": "Carved from a single piece of Crownwood oak. Pulls smooth, looses clean, and never complains."},
    {"id": "ashwood_longbow", "name": "Ashwood Longbow", "kind": "weapon", "slot": "right_hand",
     "weapon_type": "bow", "base_stats": {"grace": 4, "vitality": 1}, "req_stats": {"grace": 12}, "req_level": 6, "tier": 2,
     "desc": "Taller than most men, drawn to the cheek and loosed with a sound like tearing silk. Range is its argument, gravity its only judge."},
    {"id": "dragonhorn_bow", "name": "Dragonhorn Bow", "kind": "weapon", "slot": "right_hand",
     "weapon_type": "bow", "base_stats": {"grace": 8, "vitality": 3}, "req_stats": {"grace": 20}, "req_level": 15, "tier": 3,
     "desc": "Carved from a dragon's horn. It flexes like living bone and looses arrows that arrive before the string stops vibrating."},

    # ============================================================
    # WEAPONS — Crossbows 2H (T1-T3)
    # ============================================================
    {"id": "light_crossbow", "name": "Light Crossbow", "kind": "weapon", "slot": "right_hand",
     "weapon_type": "crossbow", "base_stats": {"grace": 3, "might": 2}, "req_stats": {"grace": 8}, "req_level": 1, "tier": 1,
     "desc": "A compact crossbow with a goat's-foot lever. It loads fast and hits harder than it looks."},
    {"id": "heavy_crossbow", "name": "Heavy Crossbow", "kind": "weapon", "slot": "right_hand",
     "weapon_type": "crossbow", "base_stats": {"grace": 5, "might": 3}, "req_stats": {"grace": 14}, "req_level": 6, "tier": 2,
     "desc": "A military crossbow with a windlass. It takes time to load, but the bolt punches through plate like paper."},
    {"id": "hand_cannon", "name": "Hand Cannon", "kind": "weapon", "slot": "right_hand",
     "weapon_type": "crossbow", "base_stats": {"grace": 8, "might": 5}, "req_stats": {"grace": 22}, "req_level": 15, "tier": 3,
     "desc": "Not a crossbow at all, but a iron tube that spits fire and lead. The noise alone wins half the fight."},

    # ============================================================
    # WEAPONS — Instruments 2H (T1-T3)
    # ============================================================
    {"id": "travelers_lute", "name": "Traveler's Lute", "kind": "weapon", "slot": "right_hand",
     "weapon_type": "instrument", "base_stats": {"grace": 2, "cognition": 2}, "req_stats": {"grace": 6}, "req_level": 1, "tier": 1,
     "desc": "A road-worn lute with a cracked soundboard. It still plays true, and that's all a bard needs."},
    {"id": "bardic_harp", "name": "Bardic Harp", "kind": "weapon", "slot": "right_hand",
     "weapon_type": "instrument", "base_stats": {"grace": 4, "cognition": 3}, "req_stats": {"grace": 12}, "req_level": 6, "tier": 2,
     "desc": "A golden harp strung with silver threads. Its notes linger in the air like incense."},
    {"id": "eternal_chorus", "name": "Eternal Chorus", "kind": "weapon", "slot": "right_hand",
     "weapon_type": "instrument", "base_stats": {"grace": 7, "cognition": 5}, "req_stats": {"grace": 20}, "req_level": 15, "tier": 3,
     "desc": "An instrument that plays itself when no one is watching. The melody is always different, and always perfect."},

    # ============================================================
    # WEAPONS — Shields 1H (T1-T3)
    # ============================================================
    {"id": "bone_shield", "name": "Bone Shield", "kind": "weapon", "slot": "left_hand",
     "weapon_type": "shield", "base_stats": {"vitality": 2, "durability": 2}, "req_stats": {"vitality": 6}, "req_level": 1, "tier": 1,
     "desc": "A shield of boiled bone and rawhide. It absorbs blows with a dull, satisfied thud."},
    {"id": "iron_kite_shield", "name": "Iron Kite Shield", "kind": "weapon", "slot": "left_hand",
     "weapon_type": "shield", "base_stats": {"vitality": 3, "durability": 3}, "req_stats": {"vitality": 10}, "req_level": 6, "tier": 2,
     "desc": "A tall shield that covers from chin to knee. Soldiers call it 'the wall you wear.'"},
    {"id": "tower_shield", "name": "Tower Shield", "kind": "weapon", "slot": "left_hand",
     "weapon_type": "shield", "base_stats": {"vitality": 5, "durability": 5}, "req_stats": {"vitality": 16}, "req_level": 15, "tier": 3,
     "desc": "A shield taller than a man. Behind it, you are a wall. In front of it, the enemy is a problem."},

    # ============================================================
    # ARMORS — Light (cloth/robe) — Head, Body, Legs, Feet, Hands, Back
    # ============================================================
    {"id": "sages_hood", "name": "Sage's Hood", "kind": "armor", "slot": "head", "armor_type": "light",
     "base_stats": {"insight": 2, "essence": 2}, "req_stats": {}, "req_level": 1, "tier": 1,
     "desc": "A deep hood of grey wool. It shadows the eyes and sharpens the mind — or so the sages say."},
    {"id": "sages_robe", "name": "Sage's Robe", "kind": "armor", "slot": "body", "armor_type": "light",
     "base_stats": {"insight": 3, "essence": 2}, "req_stats": {"insight": 6}, "req_level": 1, "tier": 1,
     "desc": "Deep blue wool, hemmed with silver thread. Pockets within pockets hold herbs, ink, and secrets."},
    {"id": "sages_trousers", "name": "Sage's Trousers", "kind": "armor", "slot": "legs", "armor_type": "light",
     "base_stats": {"insight": 2, "essence": 1, "grace": 1}, "req_stats": {}, "req_level": 1, "tier": 1,
     "desc": "Loose-cut linen dyed the color of old ink. Comfortable on the road, comfortable in the study."},
    {"id": "sages_sandals", "name": "Sage's Sandals", "kind": "armor", "slot": "feet", "armor_type": "light",
     "base_stats": {"grace": 1, "essence": 1}, "req_stats": {}, "req_level": 1, "tier": 1,
     "desc": "Simple leather sandals. They make no sound on stone, which suits a scholar's pace."},
    {"id": "sages_gloves", "name": "Sage's Gloves", "kind": "armor", "slot": "hands", "armor_type": "light",
     "base_stats": {"insight": 1, "essence": 1, "cognition": 1}, "req_stats": {}, "req_level": 1, "tier": 1,
     "desc": "Thin cotton gloves ink-stained at the fingertips. They keep the chill off and the quill steady."},
    {"id": "scholars_mantle", "name": "Scholar's Mantle", "kind": "armor", "slot": "back", "armor_type": "light",
     "base_stats": {"insight": 2, "essence": 2, "cognition": 1}, "req_stats": {}, "req_level": 1, "tier": 1,
     "desc": "A heavy wool mantle with ink-stained cuffs. It smells of libraries and ambition."},

    # Light T3
    {"id": "archmage_hood", "name": "Archmage Hood", "kind": "armor", "slot": "head", "armor_type": "light",
     "base_stats": {"insight": 5, "essence": 4, "cognition": 2}, "req_stats": {"insight": 18}, "req_level": 15, "tier": 3,
     "desc": "A hood woven from essence-thread. It muffles outside noise and amplifies thought."},
    {"id": "archmage_robe", "name": "Archmage Robe", "kind": "armor", "slot": "body", "armor_type": "light",
     "base_stats": {"insight": 8, "essence": 5}, "req_stats": {"insight": 18}, "req_level": 15, "tier": 3,
     "desc": "Robes that float a half-inch above the floor. The fabric is woven from solidified mana."},
    {"id": "archmage_leggings", "name": "Archmage Leggings", "kind": "armor", "slot": "legs", "armor_type": "light",
     "base_stats": {"insight": 5, "essence": 3, "grace": 2}, "req_stats": {"insight": 14}, "req_level": 15, "tier": 3,
     "desc": "Silken leggings that shimmer with protective wards. Light as air, strong as will."},

    # ============================================================
    # ARMORS — Leather (hide/scale) — Head, Body, Legs, Feet, Hands, Back
    # ============================================================
    {"id": "leather_cap", "name": "Leather Cap", "kind": "armor", "slot": "head", "armor_type": "leather",
     "base_stats": {"grace": 1, "durability": 1}, "req_stats": {}, "req_level": 1, "tier": 1,
     "desc": "A softened leather skullcap. It won't stop an axe, but it'll keep the rain and small birds out of your hair."},
    {"id": "leather_vest", "name": "Leather Vest", "kind": "armor", "slot": "body", "armor_type": "leather",
     "base_stats": {"vitality": 2, "might": 1}, "req_stats": {"vitality": 6}, "req_level": 1, "tier": 1,
     "desc": "Thick hide boiled and shaped to fit a chest. Smells faintly of the forest, even after tanning."},
    {"id": "leather_leggings", "name": "Leather Leggings", "kind": "armor", "slot": "legs", "armor_type": "leather",
     "base_stats": {"vitality": 2, "grace": 1}, "req_stats": {}, "req_level": 1, "tier": 1,
     "desc": "Stiff at first, soft by the third day. They creak when you crouch and whisper when you run."},
    {"id": "leather_boots", "name": "Leather Boots", "kind": "armor", "slot": "feet", "armor_type": "leather",
     "base_stats": {"grace": 2, "vitality": 1}, "req_stats": {}, "req_level": 1, "tier": 1,
     "desc": "Soft-soled and quiet. Scouts say you can hear a rabbit blink when wearing them."},
    {"id": "leather_gloves", "name": "Leather Gloves", "kind": "armor", "slot": "hands", "armor_type": "leather",
     "base_stats": {"might": 1, "grace": 1}, "req_stats": {}, "req_level": 1, "tier": 1,
     "desc": "Workman's gloves, scarred and supple. They grip anything and fear nothing."},
    {"id": "wolfpelt_cloak", "name": "Wolfpelt Cloak", "kind": "armor", "slot": "back", "armor_type": "leather",
     "base_stats": {"grace": 2, "vitality": 1}, "req_stats": {}, "req_level": 1, "tier": 1,
     "desc": "A grey cloak that moves like smoke. Scouts say it turns the wind and quiets the footfall."},

    # Leather T2
    {"id": "boarhide_vest", "name": "Boarhide Vest", "kind": "armor", "slot": "body", "armor_type": "leather",
     "base_stats": {"vitality": 3, "might": 2}, "req_stats": {"vitality": 8}, "req_level": 6, "tier": 2,
     "desc": "Thick hide boiled and shaped to fit a chest. Smells faintly of the forest, even after tanning."},
    {"id": "scaled_hauberk", "name": "Scaled Hauberk", "kind": "armor", "slot": "body", "armor_type": "leather",
     "base_stats": {"vitality": 5, "grace": 2}, "req_stats": {"vitality": 12}, "req_level": 6, "tier": 2,
     "desc": "Serpent scales laced over leather like roof tiles. Flexible where it needs to be, rigid where it matters."},
    {"id": "wolf_skull_helm", "name": "Wolf Skull Helm", "kind": "armor", "slot": "head", "armor_type": "leather",
     "base_stats": {"might": 2, "vitality": 2, "durability": 1}, "req_stats": {"vitality": 8}, "req_level": 6, "tier": 2,
     "desc": "The skull of a dire wolf, hollowed and fitted with leather straps. Wear it and the pack remembers you."},

    # ============================================================
    # ARMORS — Heavy (plate/iron) — Head, Body, Legs, Feet, Hands, Back
    # ============================================================
    {"id": "iron_helm", "name": "Iron Helm", "kind": "armor", "slot": "head", "armor_type": "heavy",
     "base_stats": {"vitality": 2, "durability": 2}, "req_stats": {"vitality": 8}, "req_level": 1, "tier": 1,
     "desc": "A standard-issue helm, dented and re-hammered more times than anyone can count. Each dent is a story that ended well."},
    {"id": "iron_chainmail", "name": "Iron Chainmail", "kind": "armor", "slot": "body", "armor_type": "heavy",
     "base_stats": {"vitality": 4, "durability": 2}, "req_stats": {"vitality": 10}, "req_level": 1, "tier": 1,
     "desc": "Riveted mail that drapes like a metal blanket. Heavy, loud, and the reason its wearer is still alive."},
    {"id": "iron_greaves", "name": "Iron Greaves", "kind": "armor", "slot": "legs", "armor_type": "heavy",
     "base_stats": {"vitality": 3, "durability": 2}, "req_stats": {"vitality": 8}, "req_level": 1, "tier": 1,
     "desc": "Steel shin-plates strapped over leather. They turn a blade, stop a snake, and add a satisfying weight to every step."},
    {"id": "ironshod_boots", "name": "Ironshod Boots", "kind": "armor", "slot": "feet", "armor_type": "heavy",
     "base_stats": {"vitality": 2, "durability": 3, "might": 1}, "req_stats": {"vitality": 8}, "req_level": 1, "tier": 1,
     "desc": "Steel-capped and heavy. They kick doors and shins with equal authority. Running is a suggestion they politely ignore."},
    {"id": "iron_gauntlets", "name": "Iron Gauntlets", "kind": "armor", "slot": "hands", "armor_type": "heavy",
     "base_stats": {"might": 2, "durability": 2}, "req_stats": {"vitality": 8}, "req_level": 1, "tier": 1,
     "desc": "Articulated plate gloves. The grip is iron, the punch is iron, the opinion is iron."},
    {"id": "iron_mantle", "name": "Iron Mantle", "kind": "armor", "slot": "back", "armor_type": "heavy",
     "base_stats": {"vitality": 2, "durability": 2, "might": 1}, "req_stats": {"vitality": 8}, "req_level": 1, "tier": 1,
     "desc": "A heavy iron shoulder mantle. It turns blades and weather alike."},

    # Heavy T2
    {"id": "knights_plate", "name": "Knight's Plate", "kind": "armor", "slot": "body", "armor_type": "heavy",
     "base_stats": {"vitality": 6, "might": 3, "durability": 2}, "req_stats": {"vitality": 14}, "req_level": 6, "tier": 2,
     "desc": "Full plate, mirror-bright and jointed like a living thing. The knight who wore it first called it 'the second skin.'"},
    {"id": "plate_legguards", "name": "Plate Legguards", "kind": "armor", "slot": "legs", "armor_type": "heavy",
     "base_stats": {"vitality": 4, "might": 2, "durability": 2}, "req_stats": {"vitality": 12}, "req_level": 6, "tier": 2,
     "desc": "Articulated plate from hip to ankle. A blacksmith's love letter to the concept of 'not dying.'"},

    # Heavy T3
    {"id": "dragonscale_tunic", "name": "Dragonscale Tunic", "kind": "armor", "slot": "body", "armor_type": "heavy",
     "base_stats": {"vitality": 10, "might": 5, "durability": 4}, "req_stats": {"vitality": 22}, "req_level": 15, "tier": 3,
     "desc": "Each scale is a finger-width thick, warm to the touch, and harder than the pride of the dragon it was taken from."},

    # ============================================================
    # ARMORS — Generic starter
    # ============================================================
    {"id": "traveler_garb", "name": "Traveler's Garb", "kind": "armor", "slot": "body", "armor_type": "light",
     "base_stats": {"vitality": 1, "durability": 1}, "req_stats": {}, "req_level": 1, "tier": 1,
     "desc": "Worn cloth and patched leather. It has seen more roads than most boots and shrugs off rain like an old friend."},
    {"id": "worn_trousers", "name": "Worn Trousers", "kind": "armor", "slot": "legs", "armor_type": "light",
     "base_stats": {"vitality": 1}, "req_stats": {}, "req_level": 1, "tier": 1,
     "desc": "Patch-stitched breeches that have trudged through mud, rain, and three counties of argument."},
    {"id": "old_boots", "name": "Old Boots", "kind": "armor", "slot": "feet", "armor_type": "leather",
     "base_stats": {"durability": 1, "grace": 1}, "req_stats": {}, "req_level": 1, "tier": 1,
     "desc": "They've lost their sole but kept their spirit. Each step tells a story the cobbler never intended."},
    {"id": "tattered_cape", "name": "Tattered Cape", "kind": "armor", "slot": "back", "armor_type": "light",
     "base_stats": {"grace": 1, "durability": 1}, "req_stats": {}, "req_level": 1, "tier": 1,
     "desc": "More holes than cloth, but it keeps the sun off and the rain mostly out. A traveler's flag, flown at half-mast."},
    {"id": "cloak_of_shadows", "name": "Cloak of Shadows", "kind": "armor", "slot": "back", "armor_type": "light",
     "base_stats": {"grace": 3, "insight": 2}, "req_stats": {"grace": 10}, "req_level": 6, "tier": 2,
     "desc": "Woven at dusk from thread that catches no light. In darkness, the wearer becomes a rumor — seen, then doubted, then forgotten."},
    {"id": "wings_of_the_exile", "name": "Wings of the Exile", "kind": "armor", "slot": "back", "armor_type": "light",
     "base_stats": {"grace": 5, "insight": 3, "essence": 3}, "req_stats": {"grace": 18}, "req_level": 15, "tier": 3,
     "desc": "Cloak-feathers of a fallen sky knight, still warm, still reaching upward. They do not grant flight — they grant the memory of it."},

    # ============================================================
    # ACCESSORIES — Rings
    # ============================================================
    {"id": "copper_ring", "name": "Copper Ring", "kind": "accessory", "slot": "ring_l",
     "base_stats": {"might": 1}, "req_stats": {}, "req_level": 1, "tier": 1,
     "desc": "A plain band of copper, green at the edges. It was someone's once. Now it's yours."},
    {"id": "silver_band", "name": "Silver Band", "kind": "accessory", "slot": "ring_l",
     "base_stats": {"grace": 2}, "req_stats": {}, "req_level": 6, "tier": 2,
     "desc": "Silver, thin as a whisper. It makes the fingers lighter and the footwork surer."},
    {"id": "gold_signet", "name": "Gold Signet", "kind": "accessory", "slot": "ring_l",
     "base_stats": {"might": 3, "vitality": 2}, "req_stats": {"might": 16}, "req_level": 15, "tier": 3,
     "desc": "A heavy gold ring bearing the seal of a house that no longer exists. The seal still opens doors."},

    # ============================================================
    # ACCESSORIES — Necklaces
    # ============================================================
    {"id": "wolf_tooth_pendant", "name": "Wolf Tooth Pendant", "kind": "accessory", "slot": "neck",
     "base_stats": {"might": 1, "vitality": 1}, "req_stats": {}, "req_level": 1, "tier": 1,
     "desc": "A fang on a leather cord. Plains children are given one at birth — a promise that the world can be bitten."},
    {"id": "heartstone_amulet", "name": "Heartstone Amulet", "kind": "accessory", "slot": "neck",
     "base_stats": {"vitality": 3, "essence": 2, "durability": 2}, "req_stats": {"vitality": 10}, "req_level": 6, "tier": 2,
     "desc": "A polished red stone that beats once per minute, in sync with the wearer's heart. If the heart stops, the stone keeps beating."},
    {"id": "eye_of_the_deep", "name": "Eye of the Deep", "kind": "accessory", "slot": "neck",
     "base_stats": {"essence": 5, "insight": 3, "cognition": 2}, "req_stats": {"essence": 16}, "req_level": 15, "tier": 3,
     "desc": "A pearl from the deepest trench, set in coral-silver. It sees what others miss: lies, traps, and the quiet sadness in a merchant's smile."},

    # ============================================================
    # ACCESSORIES — Earrings
    # ============================================================
    {"id": "stud_of_the_quiet", "name": "Stud of the Quiet", "kind": "accessory", "slot": "earring_l",
     "base_stats": {"grace": 1}, "req_stats": {}, "req_level": 1, "tier": 1,
     "desc": "A small silver stud. It does nothing — except make the wearer slightly harder to notice, which is something."},
    {"id": "essence_stud", "name": "Essence Stud", "kind": "accessory", "slot": "earring_l",
     "base_stats": {"essence": 2, "insight": 1}, "req_stats": {}, "req_level": 6, "tier": 2,
     "desc": "A tiny crystal stud that pulses with mana. Mages wear them the way soldiers wear armor — habitually, and with quiet relief."},
    {"id": "tear_of_the_moon", "name": "Tear of the Moon", "kind": "accessory", "slot": "earring_l",
     "base_stats": {"essence": 4, "insight": 3, "grace": 2}, "req_stats": {"essence": 14}, "req_level": 15, "tier": 3,
     "desc": "A teardrop moonstone that catches light that isn't there. It was given, the story goes, by the moon herself to a mortal who made her laugh."},
]

# ============================================================
# Derived defensive stats
# ============================================================
def _apply_derived_defenses(items: list[dict]) -> None:
    """Inject `armor_bonus` and `magic_resist` into armor and shield base_stats.

    Derived from (armor_type, tier) and the slot's share, rather than written out
    by hand on 30+ entries, so the defensive curve stays consistent and is tuned
    in exactly one place (items/constants.py).

    Feeding these through `base_stats` is deliberate: `compute_item_total_stats`
    already aggregates base_stats + affixes + gems, and
    `apply_enchantments_to_stats` already resolves procedural instances
    correctly. Routing defense through that one path means armor cannot silently
    stop working for instance-based gear the way it did before — there is no
    second lookup to fall out of sync.

    Explicit values already present on an item are respected and never
    overwritten, so a hand-tuned exception stays hand-tuned.
    """
    from .constants import (
        ARMOR_BONUS_BY_TYPE_TIER,
        ARMOR_SLOT_MULT,
        MAGIC_RESIST_BY_TYPE_TIER,
        SHIELD_ARMOR_BY_TIER,
    )

    for item in items:
        stats = item.setdefault("base_stats", {})
        tier = int(item.get("tier", 1) or 1)

        # Shields — armor by tier, regardless of armor_type.
        if item.get("weapon_type") == "shield":
            stats.setdefault("armor_bonus", SHIELD_ARMOR_BY_TIER.get(tier, 10))
            continue

        if item.get("kind") != "armor":
            continue

        armor_type = item.get("armor_type")
        slot_mult = ARMOR_SLOT_MULT.get(item.get("slot", ""), 0.5)

        base_armor = ARMOR_BONUS_BY_TYPE_TIER.get((armor_type, tier))
        if base_armor is not None:
            stats.setdefault("armor_bonus", max(1, round(base_armor * slot_mult)))

        base_mr = MAGIC_RESIST_BY_TYPE_TIER.get((armor_type, tier))
        if base_mr is not None:
            stats.setdefault("magic_resist", max(1, round(base_mr * slot_mult)))


_apply_derived_defenses(BASE_ITEMS)

# Build lookup dict
BASE_ITEMS_BY_ID: dict[str, dict] = {item["id"]: item for item in BASE_ITEMS}

# ============================================================
# Helper: get range from weapon_type
# ============================================================
def get_weapon_range(weapon_type: str) -> int:
    from .constants import WEAPON_TYPES
    wt = WEAPON_TYPES.get(weapon_type)
    return wt["range"] if wt else 0

# ============================================================
# Helper: is weapon two-handed?
# ============================================================
def is_two_handed(weapon_type: str) -> bool:
    from .constants import WEAPON_TYPES
    wt = WEAPON_TYPES.get(weapon_type)
    return wt["two_handed"] if wt else False
