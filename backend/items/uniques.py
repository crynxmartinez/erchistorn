"""Unique items — hand-designed items with fixed affixes and legendary powers.
These drop as-is (no affix rolling). Each has a specific base item it's built from.
"""
from __future__ import annotations

UNIQUE_ITEMS: list[dict] = [
    # --- Weapons ---
    {
        "id": "ashbringer", "base_id": "iron_greatsword", "name": "Ashbringer", "rarity": "unique",
        "fixed_prefixes": [{"id": "sharp", "tier": 1, "stats": {"might": 12}}],
        "fixed_suffixes": [{"id": "of_vampirism", "tier": 1, "bonus_effects": [{"type": "lifesteal", "value": 0.10}]}],
        "bonus_effects": [{"type": "extra_damage", "element": "fire", "value": 5}],
        "legendary_power": "holy_wrath",
        "req_stats": {"might": 16}, "req_level": 10,
        "desc": "A blade of light forged in the first age. It burns the unworthy and guides the just. The ash of its making still clings to the steel.",
    },
    {
        "id": "gods_bane", "base_id": "dragonbone_greatsword", "name": "God's Bane", "rarity": "unique",
        "fixed_prefixes": [{"id": "sharp", "tier": 1, "stats": {"might": 14}}],
        "fixed_suffixes": [{"id": "of_fury", "tier": 1, "bonus_effects": [{"type": "crit_damage", "value": 0.15}]}],
        "bonus_effects": [{"type": "armor_pen", "value": 0.05}],
        "legendary_power": "executioner",
        "req_stats": {"might": 22}, "req_level": 15,
        "desc": "The blade that ended the Age of Gods. It hums with the last breaths of divinity.",
    },
    {
        "id": "thunderstrike", "base_id": "war_hammer", "name": "Thunderstrike", "rarity": "unique",
        "fixed_prefixes": [{"id": "sharp", "tier": 1, "stats": {"might": 10}}],
        "fixed_suffixes": [{"id": "of_precision", "tier": 1, "bonus_effects": [{"type": "crit_chance", "value": 0.06}]}],
        "bonus_effects": [{"type": "extra_damage", "element": "lightning", "value": 4}],
        "legendary_power": "storm_call",
        "req_stats": {"might": 16}, "req_level": 10,
        "desc": "A hammer that crackles with captured storm energy. Every swing echoes with thunder.",
    },
    {
        "id": "frostfang", "base_id": "steel_dagger", "name": "Frostfang", "rarity": "unique",
        "fixed_prefixes": [{"id": "keen", "tier": 1, "stats": {"grace": 10}}],
        "fixed_suffixes": [{"id": "of_precision", "tier": 1, "bonus_effects": [{"type": "crit_chance", "value": 0.06}]}],
        "bonus_effects": [{"type": "extra_damage", "element": "ice", "value": 3}],
        "legendary_power": "frost_nova",
        "req_stats": {"grace": 16}, "req_level": 10,
        "desc": "A dagger carved from eternal ice. It never melts, and neither does the cold it leaves behind.",
    },
    {
        "id": "bloodletter", "base_id": "void_katar", "name": "Bloodletter", "rarity": "unique",
        "fixed_prefixes": [{"id": "sharp", "tier": 1, "stats": {"might": 8}}],
        "fixed_suffixes": [{"id": "of_vampirism", "tier": 1, "bonus_effects": [{"type": "lifesteal", "value": 0.08}]}],
        "bonus_effects": [{"type": "crit_chance", "value": 0.04}],
        "legendary_power": "blood_pact",
        "req_stats": {"might": 16, "grace": 14}, "req_level": 15,
        "desc": "The katar drinks deeply. Its wielder drinks deeper. The price is paid in heartbeats.",
    },
    {
        "id": "starcaller", "base_id": "cosmic_orb", "name": "Starcaller", "rarity": "unique",
        "fixed_prefixes": [{"id": "arcane", "tier": 1, "stats": {"essence": 12}}],
        "fixed_suffixes": [{"id": "of_the_owl", "tier": 1, "stats": {"insight": 10}}],
        "bonus_effects": [{"type": "magical_amp", "value": 0.05}],
        "legendary_power": "arcane_surge",
        "req_stats": {"insight": 20}, "req_level": 15,
        "desc": "An orb that contains a captured star. Its light never fades, and neither does the mage who holds it.",
    },
    {
        "id": "sky_piercer", "base_id": "dragonlance", "name": "Sky Piercer", "rarity": "unique",
        "fixed_prefixes": [{"id": "keen", "tier": 1, "stats": {"grace": 8}}],
        "fixed_suffixes": [{"id": "of_the_wolf", "tier": 1, "stats": {"might": 8}}],
        "bonus_effects": [{"type": "armor_pen", "value": 0.05}],
        "legendary_power": "gravity_well",
        "req_stats": {"might": 18, "grace": 16}, "req_level": 15,
        "desc": "A lance that defies distance itself. The enemy is never far enough.",
    },
    {
        "id": "phoenix_feather", "base_id": "archmage_tome", "name": "Phoenix Feather", "rarity": "unique",
        "fixed_prefixes": [{"id": "wise", "tier": 1, "stats": {"insight": 12}}],
        "fixed_suffixes": [{"id": "of_the_serpent", "tier": 1, "stats": {"essence": 10}}],
        "bonus_effects": [{"type": "hp_regen", "value": 2}, {"type": "mp_regen", "value": 2}],
        "legendary_power": "phoenix_rebirth",
        "req_stats": {"insight": 20}, "req_level": 15,
        "desc": "A tome bound in phoenix leather. The last page is blank — it fills with the reader's eulogy, then burns it away.",
    },
    {
        "id": "aegis_of_eternity", "base_id": "tower_shield", "name": "Aegis of Eternity", "rarity": "unique",
        "fixed_prefixes": [{"id": "heavy", "tier": 1, "stats": {"vitality": 10}}],
        "fixed_suffixes": [{"id": "of_warding", "tier": 1, "bonus_effects": [{"type": "armor_bonus", "value": 6}]}],
        "bonus_effects": [{"type": "evasion", "value": 3}],
        "legendary_power": "aegis_eternal",
        "req_stats": {"vitality": 18}, "req_level": 15,
        "desc": "A shield that has guarded heroes across three ages. When the bearer falls, the shield stands alone for one final breath.",
    },
    {
        "id": "whisper_of_shadows", "base_id": "cloak_of_shadows", "name": "Whisper of Shadows", "rarity": "unique",
        "fixed_prefixes": [{"id": "keen", "tier": 1, "stats": {"grace": 8}}],
        "fixed_suffixes": [{"id": "of_evasion", "tier": 1, "bonus_effects": [{"type": "evasion", "value": 6}]}],
        "bonus_effects": [{"type": "action_speed", "value": 0.04}],
        "legendary_power": "mirror_image",
        "req_stats": {"grace": 14}, "req_level": 10,
        "desc": "A cloak that moves on its own. Sometimes it moves when you don't. Sometimes it doesn't move when you do.",
    },

    # --- Armor ---
    {
        "id": "dragonscale_armor", "base_id": "dragonscale_tunic", "name": "Dragonscale of the Eternal", "rarity": "unique",
        "fixed_prefixes": [{"id": "heavy", "tier": 1, "stats": {"vitality": 10}}],
        "fixed_suffixes": [{"id": "of_the_turtle", "tier": 1, "stats": {"durability": 8}}],
        "bonus_effects": [{"type": "armor_bonus", "value": 5}, {"type": "status_resist", "value": 0.05}],
        "legendary_power": "berserker_rage",
        "req_stats": {"vitality": 20}, "req_level": 15,
        "desc": "The last gift of a dying dragon. It remembers fire, and fire remembers it — and they have an understanding.",
    },
    {
        "id": "archmage_regalia", "base_id": "archmage_robe", "name": "Archmage's Regalia", "rarity": "unique",
        "fixed_prefixes": [{"id": "wise", "tier": 1, "stats": {"insight": 10}}],
        "fixed_suffixes": [{"id": "of_the_serpent", "tier": 1, "stats": {"essence": 8}}],
        "bonus_effects": [{"type": "mp_regen", "value": 3}, {"type": "magical_amp", "value": 0.05}],
        "legendary_power": "arcane_surge",
        "req_stats": {"insight": 18}, "req_level": 15,
        "desc": "The robes of the last archmage. They float a half-inch above the ground, as if even the earth is unworthy of touching them.",
    },

    # --- Accessories ---
    {
        "id": "worldserpent_band", "base_id": "gold_signet", "name": "Band of the Worldserpent", "rarity": "unique",
        "fixed_prefixes": [{"id": "arcane", "tier": 1, "stats": {"essence": 8}}],
        "fixed_suffixes": [{"id": "of_the_owl", "tier": 1, "stats": {"insight": 6}}],
        "bonus_effects": [{"type": "magic_resist_pct", "value": 0.05}],
        "legendary_power": None,
        "req_stats": {"essence": 16}, "req_level": 15,
        "desc": "Scaled gold that wraps the finger twice. It is warm in winter, cool in summer, and old in every season.",
    },
    {
        "id": "first_oath_pendant", "base_id": "eye_of_the_deep", "name": "Pendant of the First Oath", "rarity": "unique",
        "fixed_prefixes": [{"id": "heavy", "tier": 1, "stats": {"vitality": 6}}],
        "fixed_suffixes": [{"id": "of_the_turtle", "tier": 1, "stats": {"durability": 6}}],
        "bonus_effects": [{"type": "heal_amp", "value": 0.05}, {"type": "status_resist", "value": 0.05}],
        "legendary_power": None,
        "req_stats": {"vitality": 14}, "req_level": 15,
        "desc": "A simple iron pendant, unmarked, unadorned. It was forged in the age of the first oath, and it remembers every promise ever kept.",
    },
]

UNIQUE_ITEMS_BY_ID: dict[str, dict] = {u["id"]: u for u in UNIQUE_ITEMS}
