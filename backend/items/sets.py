"""Set items — 6 sets × 4 pieces each. Set bonuses scale with pieces equipped.
Set items have fixed stats (like uniques) but belong to a named set.
"""
from __future__ import annotations

# ============================================================
# Set Definitions
# ============================================================
SET_BONUSES: dict[str, dict] = {
    "iron_champion": {
        "name": "Iron Champion",
        "desc": "The regalia of a knight who held a bridge alone for three days.",
        "pieces": ["iron_champion_blade", "iron_champion_helm", "iron_champion_plate", "iron_champion_greaves"],
        "bonuses": {
            2: {"stats": {"might": 3, "vitality": 3}, "desc": "+3 Might, +3 Vitality"},
            3: {"bonus_effects": [{"type": "armor_bonus", "value": 5}], "desc": "+5 Armor"},
            4: {"legendary_power": "wrath_of_steel", "desc": "Grants Wrath of Steel: every 3rd strike +50% dmg + Bleeding"},
        },
    },
    "sage_wisdom": {
        "name": "Sage's Wisdom",
        "desc": "The garments of a sage who learned to read the threads of fate.",
        "pieces": ["sage_hood", "sage_robe", "sage_trousers", "sage_mantle"],
        "bonuses": {
            2: {"stats": {"insight": 4, "essence": 4}, "desc": "+4 Insight, +4 Essence"},
            3: {"bonus_effects": [{"type": "mp_regen", "value": 3}], "desc": "+3 MP regen/turn"},
            4: {"legendary_power": "arcane_surge", "desc": "Grants Arcane Surge: +15% magical damage when above 80% MP"},
        },
    },
    "wolf_pack": {
        "name": "Wolf Pack",
        "desc": "The hunting gear of a plains pack-leader. The wolves still answer to it.",
        "pieces": ["wolf_pack_axe", "wolf_pack_helm", "wolf_pack_cloak", "wolf_pack_pendant"],
        "bonuses": {
            2: {"stats": {"might": 4, "grace": 2}, "desc": "+4 Might, +2 Grace"},
            3: {"bonus_effects": [{"type": "crit_chance", "value": 0.04}], "desc": "+4% Crit chance"},
            4: {"legendary_power": "berserker_rage", "desc": "+1 Might per 10% missing HP"},
        },
    },
    "shadow_step": {
        "name": "Shadow Step",
        "desc": "The tools of an assassin who became a shadow, and then became many.",
        "pieces": ["shadow_dagger", "shadow_cloak", "shadow_earring", "shadow_ring"],
        "bonuses": {
            2: {"stats": {"grace": 4, "might": 2}, "desc": "+4 Grace, +2 Might"},
            3: {"bonus_effects": [{"type": "evasion", "value": 5}], "desc": "+5 Evasion"},
            4: {"legendary_power": "mirror_image", "desc": "When hit, 10% chance to create decoy"},
        },
    },
    "tide_master": {
        "name": "Tide Master",
        "desc": "The regalia of a Hyliondrian tide-caller who commanded the ocean's breath.",
        "pieces": ["tide_orb", "tide_mantle", "tide_sandals", "tide_amulet"],
        "bonuses": {
            2: {"stats": {"essence": 4, "grace": 3}, "desc": "+4 Essence, +3 Grace"},
            3: {"bonus_effects": [{"type": "magical_amp", "value": 0.05}], "desc": "+5% Magical damage"},
            4: {"legendary_power": "frost_nova", "desc": "20% chance to freeze enemy on hit"},
        },
    },
    "hunt_prowess": {
        "name": "Hunt Prowess",
        "desc": "The gear of a legendary hunter who never missed, and never needed a second arrow.",
        "pieces": ["hunt_bow", "hunt_cloak", "hunt_earring", "hunt_boots"],
        "bonuses": {
            2: {"stats": {"grace": 4, "vitality": 2}, "desc": "+4 Grace, +2 Vitality"},
            3: {"bonus_effects": [{"type": "crit_damage", "value": 0.10}], "desc": "+10% Crit damage"},
            4: {"legendary_power": "executioner", "desc": "+100% damage to enemies below 20% HP"},
        },
    },
}

# ============================================================
# Set Item Definitions (fixed stats, like uniques)
# ============================================================
SET_ITEMS: list[dict] = [
    # --- Iron Champion (Might/Vitality tank set) ---
    {
        "id": "iron_champion_blade", "base_id": "steel_greatsword", "name": "Champion's Greatsword", "rarity": "set",
        "set_id": "iron_champion", "slot": "right_hand", "kind": "weapon", "weapon_type": "sword_2h",
        "base_stats": {"might": 6, "vitality": 3}, "fixed_prefixes": [{"id": "sharp", "tier": 2, "stats": {"might": 6}}],
        "fixed_suffixes": [{"id": "of_the_bear", "tier": 2, "stats": {"vitality": 4}}],
        "bonus_effects": [], "req_stats": {"might": 14}, "req_level": 6, "tier": 2,
        "desc": "The blade of the Iron Champion. It has been sharpened so many times it is thinner than it was forged — and sharper for it.",
    },
    {
        "id": "iron_champion_helm", "base_id": "iron_helm", "name": "Champion's Helm", "rarity": "set",
        "set_id": "iron_champion", "slot": "head", "kind": "armor", "armor_type": "heavy",
        "base_stats": {"vitality": 3, "durability": 3}, "fixed_prefixes": [{"id": "heavy", "tier": 2, "stats": {"vitality": 4}}],
        "fixed_suffixes": [{"id": "of_the_turtle", "tier": 2, "stats": {"durability": 4}}],
        "bonus_effects": [], "req_stats": {"vitality": 10}, "req_level": 6, "tier": 2,
        "desc": "The helm of the Iron Champion. The visor is dented inward — from a blow that should have killed, and didn't.",
    },
    {
        "id": "iron_champion_plate", "base_id": "knights_plate", "name": "Champion's Plate", "rarity": "set",
        "set_id": "iron_champion", "slot": "body", "kind": "armor", "armor_type": "heavy",
        "base_stats": {"vitality": 5, "might": 3, "durability": 2}, "fixed_prefixes": [{"id": "heavy", "tier": 2, "stats": {"vitality": 5}}],
        "fixed_suffixes": [{"id": "of_warding", "tier": 2, "bonus_effects": [{"type": "armor_bonus", "value": 4}]}],
        "bonus_effects": [], "req_stats": {"vitality": 12}, "req_level": 6, "tier": 2,
        "desc": "The plate of the Iron Champion. It has been repaired so many times that no original piece remains — and yet it is the same armor.",
    },
    {
        "id": "iron_champion_greaves", "base_id": "iron_greaves", "name": "Champion's Greaves", "rarity": "set",
        "set_id": "iron_champion", "slot": "legs", "kind": "armor", "armor_type": "heavy",
        "base_stats": {"vitality": 3, "durability": 2}, "fixed_prefixes": [{"id": "sturdy", "tier": 2, "stats": {"durability": 4}}],
        "fixed_suffixes": [{"id": "of_the_bear", "tier": 2, "stats": {"vitality": 4}}],
        "bonus_effects": [], "req_stats": {"vitality": 10}, "req_level": 6, "tier": 2,
        "desc": "The greaves of the Iron Champion. They have stood on every battlefield and never knelt.",
    },

    # --- Wolf Pack (Physical DPS set) ---
    {
        "id": "wolf_pack_axe", "base_id": "iron_war_axe", "name": "Pack Leader's Axe", "rarity": "set",
        "set_id": "wolf_pack", "slot": "right_hand", "kind": "weapon", "weapon_type": "axe_1h",
        "base_stats": {"might": 4, "durability": 1}, "fixed_prefixes": [{"id": "sharp", "tier": 2, "stats": {"might": 5}}],
        "fixed_suffixes": [{"id": "of_the_wolf", "tier": 2, "stats": {"might": 4}}],
        "bonus_effects": [{"type": "crit_chance", "value": 0.02}], "req_stats": {"might": 12}, "req_level": 6, "tier": 2,
        "desc": "The axe of the pack leader. The wolves carved their teeth into the haft — each notch is a kill.",
    },
    {
        "id": "wolf_pack_helm", "base_id": "wolf_skull_helm", "name": "Pack Leader's Helm", "rarity": "set",
        "set_id": "wolf_pack", "slot": "head", "kind": "armor", "armor_type": "leather",
        "base_stats": {"might": 2, "vitality": 2, "durability": 1}, "fixed_prefixes": [{"id": "sharp", "tier": 2, "stats": {"might": 4}}],
        "fixed_suffixes": [{"id": "of_the_wolf", "tier": 2, "stats": {"might": 4}}],
        "bonus_effects": [], "req_stats": {"vitality": 8}, "req_level": 6, "tier": 2,
        "desc": "The skull of the alpha that taught the pack to hunt. It still leads.",
    },
    {
        "id": "wolf_pack_cloak", "base_id": "wolfpelt_cloak", "name": "Pack Leader's Cloak", "rarity": "set",
        "set_id": "wolf_pack", "slot": "back", "kind": "armor", "armor_type": "leather",
        "base_stats": {"grace": 2, "vitality": 1}, "fixed_prefixes": [{"id": "keen", "tier": 2, "stats": {"grace": 4}}],
        "fixed_suffixes": [{"id": "of_the_fox", "tier": 2, "stats": {"grace": 4}}],
        "bonus_effects": [], "req_stats": {}, "req_level": 6, "tier": 2,
        "desc": "A cloak of grey wolf pelts. The pack sees it and remembers obedience.",
    },
    {
        "id": "wolf_pack_pendant", "base_id": "wolf_tooth_pendant", "name": "Pack Leader's Pendant", "rarity": "set",
        "set_id": "wolf_pack", "slot": "neck", "kind": "accessory",
        "base_stats": {"might": 1, "vitality": 1}, "fixed_prefixes": [{"id": "sharp", "tier": 2, "stats": {"might": 3}}],
        "fixed_suffixes": [{"id": "of_the_bear", "tier": 2, "stats": {"vitality": 3}}],
        "bonus_effects": [], "req_stats": {}, "req_level": 6, "tier": 2,
        "desc": "A fang from the first wolf the pack leader ever killed. It hangs heavier than it should.",
    },

    # --- Shadow Step (Assassin set) ---
    {
        "id": "shadow_dagger", "base_id": "steel_dagger", "name": "Shadow Step Dagger", "rarity": "set",
        "set_id": "shadow_step", "slot": "right_hand", "kind": "weapon", "weapon_type": "dagger",
        "base_stats": {"might": 2, "grace": 2}, "fixed_prefixes": [{"id": "keen", "tier": 2, "stats": {"grace": 5}}],
        "fixed_suffixes": [{"id": "of_precision", "tier": 2, "bonus_effects": [{"type": "crit_chance", "value": 0.04}]}],
        "bonus_effects": [], "req_stats": {"grace": 10}, "req_level": 6, "tier": 2,
        "desc": "A dagger that exists in two places at once. The shadow knows where it lands before the hand does.",
    },
    {
        "id": "shadow_cloak", "base_id": "cloak_of_shadows", "name": "Shadow Step Cloak", "rarity": "set",
        "set_id": "shadow_step", "slot": "back", "kind": "armor", "armor_type": "light",
        "base_stats": {"grace": 3, "insight": 2}, "fixed_prefixes": [{"id": "keen", "tier": 2, "stats": {"grace": 4}}],
        "fixed_suffixes": [{"id": "of_evasion", "tier": 2, "bonus_effects": [{"type": "evasion", "value": 4}]}],
        "bonus_effects": [], "req_stats": {"grace": 10}, "req_level": 6, "tier": 2,
        "desc": "A cloak that drinks light. In shadow, the wearer is the shadow.",
    },
    {
        "id": "shadow_earring", "base_id": "stud_of_the_quiet", "name": "Shadow Step Stud", "rarity": "set",
        "set_id": "shadow_step", "slot": "earring_l", "kind": "accessory",
        "base_stats": {"grace": 1}, "fixed_prefixes": [{"id": "keen", "tier": 2, "stats": {"grace": 3}}],
        "fixed_suffixes": [{"id": "of_the_fox", "tier": 2, "stats": {"grace": 3}}],
        "bonus_effects": [], "req_stats": {}, "req_level": 6, "tier": 2,
        "desc": "A stud that muffles footfalls. The quiet it gives is not silence — it is absence.",
    },
    {
        "id": "shadow_ring", "base_id": "copper_ring", "name": "Shadow Step Ring", "rarity": "set",
        "set_id": "shadow_step", "slot": "ring_l", "kind": "accessory",
        "base_stats": {"might": 1}, "fixed_prefixes": [{"id": "sharp", "tier": 2, "stats": {"might": 3}}],
        "fixed_suffixes": [{"id": "of_precision", "tier": 2, "bonus_effects": [{"type": "crit_chance", "value": 0.04}]}],
        "bonus_effects": [], "req_stats": {}, "req_level": 6, "tier": 2,
        "desc": "A ring that tightens when the wearer is seen. It prefers the dark.",
    },

    # --- Tide Master (Water caster set) ---
    {
        "id": "tide_orb", "base_id": "astral_orb", "name": "Tide Master's Orb", "rarity": "set",
        "set_id": "tide_master", "slot": "right_hand", "kind": "weapon", "weapon_type": "orb",
        "base_stats": {"essence": 6, "insight": 4}, "fixed_prefixes": [{"id": "arcane", "tier": 2, "stats": {"essence": 5}}],
        "fixed_suffixes": [{"id": "of_the_serpent", "tier": 2, "stats": {"essence": 4}}],
        "bonus_effects": [], "req_stats": {"insight": 14}, "req_level": 6, "tier": 2,
        "desc": "An orb filled with ocean water from the deepest trench. It pulses with the tide.",
    },
    {
        "id": "tide_mantle", "base_id": "scholars_mantle", "name": "Tide Master's Mantle", "rarity": "set",
        "set_id": "tide_master", "slot": "back", "kind": "armor", "armor_type": "light",
        "base_stats": {"insight": 2, "essence": 2, "cognition": 1}, "fixed_prefixes": [{"id": "arcane", "tier": 2, "stats": {"essence": 4}}],
        "fixed_suffixes": [{"id": "of_the_owl", "tier": 2, "stats": {"insight": 4}}],
        "bonus_effects": [], "req_stats": {}, "req_level": 6, "tier": 2,
        "desc": "A mantle woven from kelp-silk. It breathes underwater and hums in currents.",
    },
    {
        "id": "tide_sandals", "base_id": "leather_boots", "name": "Tide Master's Sandals", "rarity": "set",
        "set_id": "tide_master", "slot": "feet", "kind": "armor", "armor_type": "leather",
        "base_stats": {"grace": 2, "vitality": 1}, "fixed_prefixes": [{"id": "keen", "tier": 2, "stats": {"grace": 3}}],
        "fixed_suffixes": [{"id": "of_the_fox", "tier": 2, "stats": {"grace": 3}}],
        "bonus_effects": [], "req_stats": {}, "req_level": 6, "tier": 2,
        "desc": "Sandals that grip wet stone like a gecko. The ocean doesn't notice you're walking on it.",
    },
    {
        "id": "tide_amulet", "base_id": "heartstone_amulet", "name": "Tide Master's Amulet", "rarity": "set",
        "set_id": "tide_master", "slot": "neck", "kind": "accessory",
        "base_stats": {"vitality": 3, "essence": 2, "durability": 2}, "fixed_prefixes": [{"id": "arcane", "tier": 2, "stats": {"essence": 4}}],
        "fixed_suffixes": [{"id": "of_the_owl", "tier": 2, "stats": {"insight": 3}}],
        "bonus_effects": [], "req_stats": {"vitality": 10}, "req_level": 6, "tier": 2,
        "desc": "An amulet containing a pearl that pulses with the rhythm of the deep tide.",
    },

    # --- Hunt Prowess (Ranger set) ---
    {
        "id": "hunt_bow", "base_id": "ashwood_longbow", "name": "Hunt Prowess Bow", "rarity": "set",
        "set_id": "hunt_prowess", "slot": "right_hand", "kind": "weapon", "weapon_type": "bow",
        "base_stats": {"grace": 4, "vitality": 1}, "fixed_prefixes": [{"id": "keen", "tier": 2, "stats": {"grace": 5}}],
        "fixed_suffixes": [{"id": "of_precision", "tier": 2, "bonus_effects": [{"type": "crit_chance", "value": 0.04}]}],
        "bonus_effects": [], "req_stats": {"grace": 12}, "req_level": 6, "tier": 2,
        "desc": "A bow that has drawn blood on every continent. The string hums with anticipation.",
    },
    {
        "id": "hunt_cloak", "base_id": "wolfpelt_cloak", "name": "Hunt Prowess Cloak", "rarity": "set",
        "set_id": "hunt_prowess", "slot": "back", "kind": "armor", "armor_type": "leather",
        "base_stats": {"grace": 2, "vitality": 1}, "fixed_prefixes": [{"id": "keen", "tier": 2, "stats": {"grace": 4}}],
        "fixed_suffixes": [{"id": "of_the_fox", "tier": 2, "stats": {"grace": 4}}],
        "bonus_effects": [], "req_stats": {}, "req_level": 6, "tier": 2,
        "desc": "A cloak that masks scent and sound. The prey never knows it is being hunted.",
    },
    {
        "id": "hunt_earring", "base_id": "stud_of_the_quiet", "name": "Hunt Prowess Earring", "rarity": "set",
        "set_id": "hunt_prowess", "slot": "earring_l", "kind": "accessory",
        "base_stats": {"grace": 1}, "fixed_prefixes": [{"id": "keen", "tier": 2, "stats": {"grace": 3}}],
        "fixed_suffixes": [{"id": "of_precision", "tier": 2, "bonus_effects": [{"type": "crit_chance", "value": 0.04}]}],
        "bonus_effects": [], "req_stats": {}, "req_level": 6, "tier": 2,
        "desc": "An earring that sharpens hearing. The hunter hears the prey's heartbeat from a hundred paces.",
    },
    {
        "id": "hunt_boots", "base_id": "leather_boots", "name": "Hunt Prowess Boots", "rarity": "set",
        "set_id": "hunt_prowess", "slot": "feet", "kind": "armor", "armor_type": "leather",
        "base_stats": {"grace": 2, "vitality": 1}, "fixed_prefixes": [{"id": "keen", "tier": 2, "stats": {"grace": 3}}],
        "fixed_suffixes": [{"id": "of_haste", "tier": 2, "bonus_effects": [{"type": "action_speed", "value": 0.04}]}],
        "bonus_effects": [], "req_stats": {}, "req_level": 6, "tier": 2,
        "desc": "Boots that leave no track. The hunter walks on wind.",
    },
]

SET_ITEMS_BY_ID: dict[str, dict] = {s["id"]: s for s in SET_ITEMS}
