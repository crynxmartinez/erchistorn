"""Phase G — Biome Bosses, Cross-Continent Recipes, and Regional Prices.

Bosses:
 - One flagship boss per accessible continent (8 total) — spawned into the top-tier biome.
 - Bosses are regular MONSTERS with an `is_boss: True` flag, higher power/hp, and
   a rare-part drop that feeds cross-continent legendary recipes.

Cross-continent recipes:
 - Six legendary recipes that require materials from ≥3 continents. They gate
   the best-in-slot equipment behind cross-continent travel.

Regional prices:
 - Continental market items are cheaper if native to that continent, more
   expensive if foreign. Multipliers applied on the /market/buy path.
"""
from __future__ import annotations


# ============================================================
# BOSSES — 1 per accessible continent, dropped into the top-tier biome.
# Each drops a unique "boss part" used in cross-continent recipes.
# ============================================================
BOSSES: list[dict] = [
    {"id": "boss_ashen_lord",       "name": "The Ashen Lord",           "biome": "ashen_border",     "continent": "valeria",
     "power": 30,  "hp": 400,  "is_boss": True,  "creature_tier": "boss",
     "species": "undead", "archetype": "caster", "personality": "opportunist",
     "stats": {"might": {"base": 20, "growth": 1.5}, "grace": {"base": 18, "growth": 1.4}, "cognition": {"base": 35, "growth": 2.5},
               "insight": {"base": 30, "growth": 2.2}, "essence": {"base": 32, "growth": 2.3}, "durability": {"base": 25, "growth": 1.8}},
     "passive_buff": [
         {"type": "cognition_bonus", "value": 0.20},
         {"type": "lifesteal", "value": 0.10},
         {"type": "magic_resist", "value": 0.15},
     ],
     "profile_skills": {
         "attack": [
             {"id": "boss_ashen_lord_drain", "name": "Life Drain", "power_type": "strike", "damage_type": "magical", "power": 18, "cost_mp": 3, "cost_stamina": 0, "cooldown": 1, "trigger": "always"},
             {"id": "boss_ashen_lord_death_coil", "name": "Death Coil", "power_type": "strike", "damage_type": "magical", "power": 28, "cost_mp": 8, "cost_stamina": 0, "cooldown": 3, "trigger": "opponent_wounded", "is_ultimate": True, "status_apply": "poisoned"},
         ],
         "defense": [
             {"id": "boss_ashen_lord_bone_armor", "name": "Bone Armor", "power_type": "buff", "damage_type": "physical", "power": 0, "cost_mp": 0, "cost_stamina": 30, "cooldown": 3, "trigger": "low_hp", "status_apply": "warded"},
             {"id": "boss_ashen_lord_curse", "name": "Hexing Curse", "power_type": "debuff", "damage_type": "magical", "power": 10, "cost_mp": 4, "cost_stamina": 0, "cooldown": 2, "trigger": "opening_move", "status_apply": "poisoned"},
         ],
         "utility": [
             {"id": "boss_ashen_lord_fear_aura", "name": "Fear Aura", "power_type": "debuff", "damage_type": "magical", "power": 8, "cost_mp": 3, "cost_stamina": 0, "cooldown": 2, "trigger": "opening_move", "status_apply": "weary"},
         ],
     },
     "signature_fusion": [
         {"id": "boss_ashen_lord_death_fusion", "name": "Death Coil Fusion", "power_type": "strike", "damage_type": "magical", "power": 35, "cost_mp": 8, "cost_stamina": 0, "cooldown": 4, "hits": 1, "is_signature": True, "status_apply": "poisoned", "lifesteal": 0.20},
         {"id": "boss_ashen_lord_bone_fusion", "name": "Bone Storm Fusion", "power_type": "strike", "damage_type": "physical", "power": 30, "cost_mp": 0, "cost_stamina": 50, "cooldown": 5, "hits": 3, "is_signature": True, "status_apply": "bleeding", "armor_ignore": True},
     ],
     "boss_aura": {"type": "fear_aura", "radius": "battlefield", "effect": "enemy_attack_penalty", "value": 0.15},
     "drops": [("oath_seal_part",           0.40), ("greater_healing_potion", 0.8), ("relic_shard", 0.7)]},
    {"id": "boss_demon_warleader",  "name": "The Demon-Warleader",      "biome": "demonfall_crater", "continent": "mushkara",
     "power": 42,  "hp": 620,  "is_boss": True,  "creature_tier": "boss",
     "species": "demon", "archetype": "bruiser", "personality": "aggressive",
     "stats": {"might": {"base": 40, "growth": 2.8}, "grace": {"base": 20, "growth": 1.5}, "cognition": {"base": 18, "growth": 1.3},
               "insight": {"base": 16, "growth": 1.2}, "essence": {"base": 28, "growth": 2.0}, "durability": {"base": 35, "growth": 2.5}},
     "passive_buff": [
         {"type": "might_bonus", "value": 0.25},
         {"type": "lifesteal", "value": 0.12},
         {"type": "crit_chance", "value": 0.15},
     ],
     "profile_skills": {
         "attack": [
             {"id": "boss_demon_warleader_hellfire", "name": "Hellfire", "power_type": "strike", "damage_type": "magical", "power": 22, "cost_mp": 5, "cost_stamina": 0, "cooldown": 1, "trigger": "always", "status_apply": "burning"},
             {"id": "boss_demon_warleader_apocalypse", "name": "Apocalypse", "power_type": "strike", "damage_type": "magical", "power": 35, "cost_mp": 12, "cost_stamina": 0, "cooldown": 3, "trigger": "opponent_wounded", "is_ultimate": True, "status_apply": "burning"},
         ],
         "defense": [
             {"id": "boss_demon_warleader_demon_fury", "name": "Demonic Fury", "power_type": "buff", "damage_type": "physical", "power": 0, "cost_mp": 0, "cost_stamina": 40, "cooldown": 3, "trigger": "low_hp", "status_apply": "bloodrage"},
             {"id": "boss_demon_warleader_soul_rip", "name": "Soul Rip", "power_type": "debuff", "damage_type": "magical", "power": 15, "cost_mp": 7, "cost_stamina": 0, "cooldown": 2, "trigger": "opponent_wounded", "status_apply": "poisoned"},
         ],
         "utility": [
             {"id": "boss_demon_warleader_soul_fear", "name": "Soul Fear", "power_type": "debuff", "damage_type": "magical", "power": 10, "cost_mp": 5, "cost_stamina": 0, "cooldown": 2, "trigger": "opening_move", "status_apply": "weary"},
         ],
     },
     "signature_fusion": [
         {"id": "boss_demon_warleader_apocalypse_fusion", "name": "Apocalypse Fusion", "power_type": "strike", "damage_type": "magical", "power": 42, "cost_mp": 12, "cost_stamina": 0, "cooldown": 4, "hits": 2, "is_signature": True, "status_apply": "burning", "lifesteal": 0.20},
         {"id": "boss_demon_warleader_hellfire_fusion", "name": "Hellfire Nova Fusion", "power_type": "strike", "damage_type": "magical", "power": 38, "cost_mp": 10, "cost_stamina": 0, "cooldown": 5, "hits": 3, "is_signature": True, "status_apply": "burning", "hits_all_enemies": True},
     ],
     "boss_aura": {"type": "infernal_aura", "radius": "battlefield", "effect": "burning_on_hit", "value": 0.20},
     "drops": [("chainbreaker_fragment_part", 0.40), ("demonbone_part", 0.7), ("jahra_ingot", 0.5)]},
    {"id": "boss_amber_diplomat",   "name": "The Amber Diplomat (Fallen)","biome": "diplomats_highlands","continent": "concordia",
     "power": 50,  "hp": 780,  "is_boss": True,  "creature_tier": "boss",
     "species": "humanoid", "archetype": "caster", "personality": "opportunist",
     "stats": {"might": {"base": 18, "growth": 1.3}, "grace": {"base": 25, "growth": 1.8}, "cognition": {"base": 45, "growth": 3.2},
               "insight": {"base": 40, "growth": 2.8}, "essence": {"base": 42, "growth": 3.0}, "durability": {"base": 28, "growth": 2.0}},
     "passive_buff": [
         {"type": "cognition_bonus", "value": 0.25},
         {"type": "insight_bonus", "value": 0.20},
         {"type": "magic_resist", "value": 0.20},
     ],
     "profile_skills": {
         "attack": [
             {"id": "boss_amber_diplomat_arcane_bolt", "name": "Arcane Bolt", "power_type": "strike", "damage_type": "magical", "power": 25, "cost_mp": 3, "cost_stamina": 0, "cooldown": 1, "trigger": "always"},
             {"id": "boss_amber_diplomat_arcane_nova", "name": "Arcane Nova", "power_type": "strike", "damage_type": "magical", "power": 38, "cost_mp": 10, "cost_stamina": 0, "cooldown": 3, "trigger": "opponent_wounded", "is_ultimate": True, "status_apply": "stunned"},
         ],
         "defense": [
             {"id": "boss_amber_diplomat_reflection", "name": "Arcane Reflection", "power_type": "buff", "damage_type": "magical", "power": 0, "cost_mp": 6, "cost_stamina": 0, "cooldown": 3, "trigger": "low_hp", "status_apply": "warded"},
             {"id": "boss_amber_diplomat_mana_burn", "name": "Mana Burn", "power_type": "debuff", "damage_type": "magical", "power": 15, "cost_mp": 5, "cost_stamina": 0, "cooldown": 2, "trigger": "opening_move", "status_apply": "weary"},
         ],
         "utility": [
             {"id": "boss_amber_diplomat_mana_shield", "name": "Mana Shield", "power_type": "buff", "damage_type": "magical", "power": 0, "cost_mp": 5, "cost_stamina": 0, "cooldown": 3, "trigger": "low_hp", "status_apply": "warded"},
         ],
     },
     "signature_fusion": [
         {"id": "boss_amber_diplomat_arcane_fusion", "name": "Arcane Nova Fusion", "power_type": "strike", "damage_type": "magical", "power": 45, "cost_mp": 10, "cost_stamina": 0, "cooldown": 4, "hits": 1, "is_signature": True, "status_apply": "stunned", "hits_all_enemies": True},
         {"id": "boss_amber_diplomat_prism_fusion", "name": "Prism Beam Fusion", "power_type": "strike", "damage_type": "magical", "power": 42, "cost_mp": 12, "cost_stamina": 0, "cooldown": 5, "hits": 2, "is_signature": True, "unevadable": True},
     ],
     "boss_aura": {"type": "arcane_aura", "radius": "battlefield", "effect": "mana_regen", "value": 0.10},
     "drops": [("federation_seal_part",     0.40), ("prism_gem_part", 0.7), ("orb_fragment", 0.5)]},
    {"id": "boss_forge_golem",      "name": "The Forge Golem of Deepvein","biome": "deep_forges",     "continent": "khardrum",
     "power": 60,  "hp": 950,  "is_boss": True,  "creature_tier": "boss",
     "species": "construct", "archetype": "tank", "personality": "guardian",
     "stats": {"might": {"base": 45, "growth": 3.0}, "grace": {"base": 12, "growth": 0.9}, "cognition": {"base": 15, "growth": 1.1},
               "insight": {"base": 14, "growth": 1.0}, "essence": {"base": 30, "growth": 2.0}, "durability": {"base": 55, "growth": 3.8}},
     "passive_buff": [
         {"type": "armor_bonus", "value": 0.30},
         {"type": "durability_bonus", "value": 0.20},
         {"type": "might_bonus", "value": 0.20},
     ],
     "profile_skills": {
         "attack": [
             {"id": "boss_forge_golem_ember_spit", "name": "Ember Spit", "power_type": "strike", "damage_type": "magical", "power": 28, "cost_mp": 3, "cost_stamina": 0, "cooldown": 1, "trigger": "always", "status_apply": "burning"},
             {"id": "boss_forge_golem_inferno", "name": "Inferno", "power_type": "strike", "damage_type": "magical", "power": 42, "cost_mp": 10, "cost_stamina": 0, "cooldown": 3, "trigger": "opponent_wounded", "is_ultimate": True, "status_apply": "burning"},
         ],
         "defense": [
             {"id": "boss_forge_golem_fire_shield", "name": "Flame Shield", "power_type": "buff", "damage_type": "magical", "power": 0, "cost_mp": 4, "cost_stamina": 0, "cooldown": 3, "trigger": "low_hp", "status_apply": "warded"},
             {"id": "boss_forge_golem_ironhide", "name": "Ironhide", "power_type": "buff", "damage_type": "physical", "power": 0, "cost_mp": 0, "cost_stamina": 35, "cooldown": 3, "trigger": "low_hp", "status_apply": "warded"},
         ],
         "utility": [
             {"id": "boss_forge_golem_ignite_ground", "name": "Ignite Ground", "power_type": "debuff", "damage_type": "magical", "power": 10, "cost_mp": 4, "cost_stamina": 0, "cooldown": 3, "trigger": "always", "status_apply": "burning"},
         ],
     },
     "signature_fusion": [
         {"id": "boss_forge_golem_inferno_fusion", "name": "Inferno Fusion", "power_type": "strike", "damage_type": "magical", "power": 50, "cost_mp": 10, "cost_stamina": 0, "cooldown": 4, "hits": 3, "is_signature": True, "status_apply": "burning", "hits_all_enemies": True},
         {"id": "boss_forge_golem_iron_fusion", "name": "Iron Storm Fusion", "power_type": "strike", "damage_type": "physical", "power": 48, "cost_mp": 0, "cost_stamina": 50, "cooldown": 5, "hits": 3, "is_signature": True, "status_apply": "bleeding", "armor_ignore": True},
     ],
     "boss_aura": {"type": "heat_aura", "radius": "battlefield", "effect": "stamina_drain", "value": 0.15},
     "drops": [("living_stone_heart_part",  0.40), ("jahra_fragment_part", 0.7), ("jahra_ingot", 0.6)]},
    {"id": "boss_starfall_avatar",  "name": "The Starfall Avatar",      "biome": "starfall_cliffs",  "continent": "haya",
     "power": 70,  "hp": 1200, "is_boss": True,  "creature_tier": "boss",
     "species": "magical", "archetype": "caster", "personality": "opportunist",
     "stats": {"might": {"base": 20, "growth": 1.4}, "grace": {"base": 35, "growth": 2.4}, "cognition": {"base": 55, "growth": 3.8},
               "insight": {"base": 50, "growth": 3.5}, "essence": {"base": 52, "growth": 3.6}, "durability": {"base": 35, "growth": 2.4}},
     "passive_buff": [
         {"type": "cognition_bonus", "value": 0.30},
         {"type": "essence_bonus", "value": 0.25},
         {"type": "evasion_bonus", "value": 0.20},
     ],
     "profile_skills": {
         "attack": [
             {"id": "boss_starfall_avatar_arcane_bolt", "name": "Arcane Bolt", "power_type": "strike", "damage_type": "magical", "power": 32, "cost_mp": 3, "cost_stamina": 0, "cooldown": 1, "trigger": "always"},
             {"id": "boss_starfall_avatar_arcane_nova", "name": "Arcane Nova", "power_type": "strike", "damage_type": "magical", "power": 48, "cost_mp": 10, "cost_stamina": 0, "cooldown": 3, "trigger": "opponent_wounded", "is_ultimate": True, "status_apply": "stunned"},
         ],
         "defense": [
             {"id": "boss_starfall_avatar_reflection", "name": "Arcane Reflection", "power_type": "buff", "damage_type": "magical", "power": 0, "cost_mp": 6, "cost_stamina": 0, "cooldown": 3, "trigger": "low_hp", "status_apply": "warded"},
             {"id": "boss_starfall_avatar_mana_burn", "name": "Mana Burn", "power_type": "debuff", "damage_type": "magical", "power": 18, "cost_mp": 5, "cost_stamina": 0, "cooldown": 2, "trigger": "opening_move", "status_apply": "weary"},
         ],
         "utility": [
             {"id": "boss_starfall_avatar_mana_shield", "name": "Mana Shield", "power_type": "buff", "damage_type": "magical", "power": 0, "cost_mp": 5, "cost_stamina": 0, "cooldown": 3, "trigger": "low_hp", "status_apply": "warded"},
         ],
     },
     "signature_fusion": [
         {"id": "boss_starfall_avatar_arcane_fusion", "name": "Arcane Nova Fusion", "power_type": "strike", "damage_type": "magical", "power": 55, "cost_mp": 10, "cost_stamina": 0, "cooldown": 4, "hits": 1, "is_signature": True, "status_apply": "stunned", "hits_all_enemies": True},
         {"id": "boss_starfall_avatar_starfall_fusion", "name": "Starfall Fusion", "power_type": "strike", "damage_type": "magical", "power": 52, "cost_mp": 12, "cost_stamina": 0, "cooldown": 5, "hits": 3, "is_signature": True, "status_apply": "stunned", "unevadable": True},
     ],
     "boss_aura": {"type": "celestial_aura", "radius": "battlefield", "effect": "magic_damage_boost", "value": 0.20},
     "drops": [("star_shard_part",          0.40), ("celestial_thread_part", 0.7), ("skillbook_wind_step", 0.15)]},
    {"id": "boss_alpha_king",       "name": "The Alpha King of Ancient Den","biome": "ancient_den",  "continent": "gennel",
     "power": 80,  "hp": 1400, "is_boss": True,  "creature_tier": "legendary",
     "species": "beast", "archetype": "bruiser", "personality": "aggressive",
     "stats": {"might": {"base": 60, "growth": 4.0}, "grace": {"base": 35, "growth": 2.4}, "cognition": {"base": 25, "growth": 1.8},
               "insight": {"base": 22, "growth": 1.6}, "essence": {"base": 30, "growth": 2.0}, "durability": {"base": 50, "growth": 3.5}},
     "passive_buff": [
         {"type": "might_bonus", "value": 0.35},
         {"type": "crit_chance", "value": 0.25},
         {"type": "lifesteal", "value": 0.15},
         {"type": "grace_bonus", "value": 0.20},
         {"type": "durability_bonus", "value": 0.20},
     ],
     "profile_skills": {
         "attack": [
             {"id": "boss_alpha_king_maul", "name": "Savage Maul", "power_type": "strike", "damage_type": "physical", "power": 38, "cost_mp": 0, "cost_stamina": 25, "cooldown": 1, "trigger": "always", "status_apply": "bleeding"},
             {"id": "boss_alpha_king_primal_devastation", "name": "Primal Devastation", "power_type": "strike", "damage_type": "physical", "power": 55, "cost_mp": 0, "cost_stamina": 60, "cooldown": 3, "trigger": "opponent_wounded", "is_ultimate": True, "status_apply": "bleeding"},
         ],
         "defense": [
             {"id": "boss_alpha_king_primal_fury", "name": "Primal Fury", "power_type": "buff", "damage_type": "physical", "power": 0, "cost_mp": 0, "cost_stamina": 40, "cooldown": 3, "trigger": "low_hp", "status_apply": "bloodrage"},
             {"id": "boss_alpha_king_roar", "name": "Terrifying Roar", "power_type": "debuff", "damage_type": "physical", "power": 20, "cost_mp": 0, "cost_stamina": 30, "cooldown": 2, "trigger": "opening_move", "status_apply": "weary"},
         ],
         "utility": [
             {"id": "boss_alpha_king_primal_roar", "name": "Primal Roar", "power_type": "debuff", "damage_type": "physical", "power": 15, "cost_mp": 0, "cost_stamina": 30, "cooldown": 2, "trigger": "opening_move", "status_apply": "weary"},
         ],
     },
     "signature_fusion": [
         {"id": "boss_alpha_king_primal_fusion", "name": "Primal Devastation Fusion", "power_type": "strike", "damage_type": "physical", "power": 65, "cost_mp": 0, "cost_stamina": 60, "cooldown": 4, "hits": 3, "is_signature": True, "status_apply": "bleeding", "lifesteal": 0.15},
         {"id": "boss_alpha_king_alpha_fusion", "name": "Alpha's Wrath Fusion", "power_type": "strike", "damage_type": "physical", "power": 60, "cost_mp": 0, "cost_stamina": 50, "cooldown": 5, "hits": 2, "is_signature": True, "status_apply": "stunned", "armor_ignore": True},
         {"id": "boss_alpha_king_pack_fusion", "name": "Pack Lord's Fusion", "power_type": "buff", "damage_type": "physical", "power": 0, "cost_mp": 0, "cost_stamina": 40, "cooldown": 4, "hits": 0, "is_signature": True, "status_apply": "bloodrage", "lifesteal": 0.20},
     ],
     "boss_aura": {"type": "primal_aura", "radius": "battlefield", "effect": "attack_speed_boost", "value": 0.25},
     "legendary_passive": {"type": "alpha_dominance", "desc": "When HP drops below 25%, summons 2 pack minions and enters unkillable state for 1 turn."},
     "drops": [("primal_blood_crystal_part",0.40), ("alpha_fang_part", 0.7), ("skillbook_thornlash", 0.15)]},
    {"id": "boss_leviathan",        "name": "The Leviathan of the Trench","biome": "abyssal_trench", "continent": "hylion",
     "power": 90,  "hp": 1600, "is_boss": True,  "creature_tier": "legendary",
     "species": "beast", "archetype": "caster", "personality": "opportunist",
     "stats": {"might": {"base": 25, "growth": 1.6}, "grace": {"base": 40, "growth": 2.6}, "cognition": {"base": 60, "growth": 4.2},
               "insight": {"base": 55, "growth": 3.8}, "essence": {"base": 58, "growth": 4.0}, "durability": {"base": 45, "growth": 3.0}},
     "passive_buff": [
         {"type": "essence_bonus", "value": 0.35},
         {"type": "magic_resist", "value": 0.30},
         {"type": "insight_bonus", "value": 0.25},
         {"type": "regen", "value": 0.10},
         {"type": "evasion_bonus", "value": 0.20},
     ],
     "profile_skills": {
         "attack": [
             {"id": "boss_leviathan_void_touch", "name": "Void Touch", "power_type": "strike", "damage_type": "magical", "power": 42, "cost_mp": 4, "cost_stamina": 0, "cooldown": 1, "trigger": "always", "status_apply": "poisoned"},
             {"id": "boss_leviathan_void_collapse", "name": "Void Collapse", "power_type": "strike", "damage_type": "magical", "power": 60, "cost_mp": 12, "cost_stamina": 0, "cooldown": 3, "trigger": "opponent_wounded", "is_ultimate": True, "status_apply": "poisoned"},
         ],
         "defense": [
             {"id": "boss_leviathan_shadow_mend", "name": "Shadow Mend", "power_type": "heal", "damage_type": "magical", "power": 50, "cost_mp": 6, "cost_stamina": 0, "cooldown": 3, "trigger": "low_hp"},
             {"id": "boss_leviathan_abyssal_drain", "name": "Abyssal Drain", "power_type": "debuff", "damage_type": "magical", "power": 25, "cost_mp": 7, "cost_stamina": 0, "cooldown": 2, "trigger": "opponent_wounded", "status_apply": "weary"},
         ],
         "utility": [
             {"id": "boss_leviathan_mist_veil", "name": "Abyssal Veil", "power_type": "buff", "damage_type": "magical", "power": 0, "cost_mp": 5, "cost_stamina": 0, "cooldown": 3, "trigger": "always", "status_apply": "evasive"},
         ],
     },
     "signature_fusion": [
         {"id": "boss_leviathan_void_fusion", "name": "Void Collapse Fusion", "power_type": "strike", "damage_type": "magical", "power": 70, "cost_mp": 12, "cost_stamina": 0, "cooldown": 4, "hits": 2, "is_signature": True, "status_apply": "poisoned", "uncleansable": True},
         {"id": "boss_leviathan_tidal_fusion", "name": "Tidal Devastation Fusion", "power_type": "strike", "damage_type": "magical", "power": 65, "cost_mp": 8, "cost_stamina": 0, "cooldown": 5, "hits": 3, "is_signature": True, "status_apply": "weary", "unevadable": True},
         {"id": "boss_leviathan_abyss_fusion", "name": "Abyssal Drain Fusion", "power_type": "strike", "damage_type": "magical", "power": 58, "cost_mp": 10, "cost_stamina": 0, "cooldown": 4, "hits": 1, "is_signature": True, "status_apply": "weary", "lifesteal": 0.25},
     ],
     "boss_aura": {"type": "abyssal_aura", "radius": "battlefield", "effect": "heal_reduction", "value": 0.30},
     "legendary_passive": {"type": "leviathan_tide", "desc": "Every 3rd turn, unleashes a tidal wave that hits all enemies and cleanses own debuffs."},
     "drops": [("leviathan_scale_part",     0.40), ("divine_water_part", 0.7), ("skillbook_tidefury", 0.15)]},
    {"id": "boss_thorn_guardian",   "name": "The Thorn Guardian Awakened","biome": "elderroot_hollow","continent": "daw_ul_talalu",
     "power": 100, "hp": 1900, "is_boss": True,  "creature_tier": "legendary",
     "species": "plant", "archetype": "tank", "personality": "guardian",
     "stats": {"might": {"base": 55, "growth": 3.5}, "grace": {"base": 30, "growth": 2.0}, "cognition": {"base": 50, "growth": 3.4},
               "insight": {"base": 45, "growth": 3.0}, "essence": {"base": 55, "growth": 3.6}, "durability": {"base": 70, "growth": 4.8}},
     "passive_buff": [
         {"type": "durability_bonus", "value": 0.40},
         {"type": "armor_bonus", "value": 0.35},
         {"type": "regen", "value": 0.15},
         {"type": "might_bonus", "value": 0.25},
         {"type": "essence_bonus", "value": 0.20},
     ],
     "profile_skills": {
         "attack": [
             {"id": "boss_thorn_guardian_arcane_bolt", "name": "Arcane Bolt", "power_type": "strike", "damage_type": "magical", "power": 45, "cost_mp": 3, "cost_stamina": 0, "cooldown": 1, "trigger": "always"},
             {"id": "boss_thorn_guardian_arcane_nova", "name": "Arcane Nova", "power_type": "strike", "damage_type": "magical", "power": 65, "cost_mp": 10, "cost_stamina": 0, "cooldown": 3, "trigger": "opponent_wounded", "is_ultimate": True, "status_apply": "stunned"},
         ],
         "defense": [
             {"id": "boss_thorn_guardian_reflection", "name": "Arcane Reflection", "power_type": "buff", "damage_type": "magical", "power": 0, "cost_mp": 6, "cost_stamina": 0, "cooldown": 3, "trigger": "low_hp", "status_apply": "warded"},
             {"id": "boss_thorn_guardian_mana_burn", "name": "Mana Burn", "power_type": "debuff", "damage_type": "magical", "power": 25, "cost_mp": 5, "cost_stamina": 0, "cooldown": 2, "trigger": "opening_move", "status_apply": "weary"},
         ],
         "utility": [
             {"id": "boss_thorn_guardian_mana_shield", "name": "Mana Shield", "power_type": "buff", "damage_type": "magical", "power": 0, "cost_mp": 5, "cost_stamina": 0, "cooldown": 3, "trigger": "low_hp", "status_apply": "warded"},
         ],
     },
     "signature_fusion": [
         {"id": "boss_thorn_guardian_arcane_fusion", "name": "Arcane Nova Fusion", "power_type": "strike", "damage_type": "magical", "power": 75, "cost_mp": 10, "cost_stamina": 0, "cooldown": 4, "hits": 1, "is_signature": True, "status_apply": "stunned", "hits_all_enemies": True},
         {"id": "boss_thorn_guardian_thorn_fusion", "name": "Thorn Storm Fusion", "power_type": "strike", "damage_type": "physical", "power": 70, "cost_mp": 0, "cost_stamina": 60, "cooldown": 5, "hits": 3, "is_signature": True, "status_apply": "bleeding", "armor_ignore": True},
         {"id": "boss_thorn_guardian_overgrowth_fusion", "name": "Living Overgrowth Fusion", "power_type": "buff", "damage_type": "physical", "power": 0, "cost_mp": 0, "cost_stamina": 50, "cooldown": 4, "hits": 0, "is_signature": True, "status_apply": "warded", "lifesteal": 0.20},
     ],
     "boss_aura": {"type": "elderroot_aura", "radius": "battlefield", "effect": "regen_all", "value": 0.15},
     "legendary_passive": {"type": "living_wood", "desc": "On death, revives at 30% HP once. Regrows 5% HP per turn while above 50%."},
     "drops": [("thorn_guardian_core_part", 0.40), ("living_wood_part", 0.7), ("skillbook_sunlance", 0.15)]},
]


# ============================================================
# BOSS-PART ITEMS — the rare crafting materials bosses drop.
# ============================================================
BOSS_PARTS: list[dict] = [
    {"id": "oath_seal_part",              "name": "Oath Seal Fragment",           "rarity": "epic",      "kind": "boss_part", "desc": "A fragment of a broken oath-seal from the Vale of Oaths. It still whispers promises that were never kept."},
    {"id": "chainbreaker_fragment_part",  "name": "Chainbreaker Fragment",        "rarity": "epic",      "kind": "boss_part", "desc": "A shard of the great chain that once bound the Orcs. It is warm to the touch, as if remembering the fire of liberation."},
    {"id": "demonbone_part",              "name": "Demonbone Sliver",             "rarity": "epic",      "kind": "boss_part", "desc": "A sliver of bone from a vanquished demon. Black as ash, and it screams faintly when placed near open flame."},
    {"id": "federation_seal_part",        "name": "Federation Seal Half",         "rarity": "epic",      "kind": "boss_part", "desc": "Half of a federation seal from Concordia. The other half is held by someone you will probably have to fight."},
    {"id": "prism_gem_part",              "name": "Prism Gem Core",               "rarity": "epic",      "kind": "boss_part", "desc": "The core of a prism gem, refracting light into colors that do not exist. Scholars argue about what that means."},
    {"id": "living_stone_heart_part",     "name": "Living Stone Heart",           "rarity": "epic",      "kind": "boss_part", "desc": "A stone heart that still beats, slowly, from the deep halls of Khardrum. Dwarves say it is the mountain remembering a friend."},
    {"id": "jahra_fragment_part",         "name": "Deep Jahra Fragment",          "rarity": "epic",      "kind": "boss_part", "desc": "A raw fragment of Jahra ore, unworked. It is lighter than it should be and harder than anything you own."},
    {"id": "star_shard_part",             "name": "Starfall Shard",               "rarity": "epic",      "kind": "boss_part", "desc": "A shard of fallen sky-stone from the Starfall Cliffs. It glows at night and hums during storms."},
    {"id": "celestial_thread_part",       "name": "Celestial Thread",             "rarity": "epic",      "kind": "boss_part", "desc": "A thread of celestial silk from Haya. It floats if you let go of it, and it never tangles."},
    {"id": "primal_blood_crystal_part",   "name": "Primal Blood Crystal",         "rarity": "epic",      "kind": "boss_part", "desc": "A crystal of solidified primal blood from Gennel. It pulses in rhythm with the bearer's heartbeat."},
    {"id": "alpha_fang_part",             "name": "Alpha Fang",                   "rarity": "epic",      "kind": "boss_part", "desc": "The fang of an alpha beast, larger than a human hand. Wildblood hunters say the spirit of the pack still lives inside it."},
    {"id": "leviathan_scale_part",        "name": "Leviathan Scale",              "rarity": "legendary", "kind": "boss_part", "desc": "A scale from a deep-sea leviathan, blue-black and the size of a shield. It has never dried out."},
    {"id": "divine_water_part",           "name": "Divine Water Fragment",        "rarity": "legendary", "kind": "boss_part", "desc": "A vial of water from the sacred depths of Hylion. It glows faintly and heals what it touches."},
    {"id": "thorn_guardian_core_part",    "name": "Thorn Guardian Core",          "rarity": "legendary", "kind": "boss_part", "desc": "The heartwood core of a thorn guardian from Daw'ul Talalu. It still grows, slowly, even after being cut."},
    {"id": "living_wood_part",            "name": "Living Wood Core",             "rarity": "legendary", "kind": "boss_part", "desc": "A core of living wood from the Mystleaf forests. It puts out tiny leaves if you water it."},
]


# ============================================================
# CROSS-CONTINENT LEGENDARY RECIPES — each requires materials
# from ≥3 continents to force travel/trade.
# ============================================================
CROSS_CONTINENT_RECIPES: list[dict] = [
    {"id": "craft_moonfang_spear", "name": "Moonfang Spear", "kind": "weapon",
     "requires": {"jahra_fragment_part": 1, "alpha_fang_part": 1, "star_shard_part": 1, "living_wood": 2},
     "produces": {"id": "moonfang_spear", "name": "Moonfang Spear", "rarity": "legendary",
                  "kind": "weapon", "power": 40, "slot": "right_hand", "two_handed": True, "price": 1200, "desc": "Forged from Jahra, starlight, and the fang of an alpha beast. It is said to howl when drawn under a full moon."},
     "profession": "blacksmithing", "profession_min_rank": "expert",
     "recipe_source": "Cross-continent (Khardrum · Gennel · Haya · Daw'ul Talalu)"},
    {"id": "craft_tidebound_amulet", "name": "Tidebound Amulet", "kind": "relic",
     "requires": {"leviathan_scale_part": 1, "prism_gem_part": 1, "oath_seal_part": 1, "abyss_coral": 3},
     "produces": {"id": "tidebound_amulet", "name": "Tidebound Amulet", "rarity": "legendary",
                  "kind": "relic", "power": 0, "price": 1000, "desc": "An amulet that hums with the rhythm of the deep sea. Wearers say they can hear the Tide Mothers singing in their dreams."},
     "profession": "jewelcrafting", "profession_min_rank": "expert",
     "recipe_source": "Cross-continent (Hylion · Concordia · Valeria)"},
    {"id": "craft_ashenlord_greatsword", "name": "Ashen Lord's Greatsword", "kind": "weapon",
     "requires": {"oath_seal_part": 1, "chainbreaker_fragment_part": 1, "demonbone_part": 1, "jahra_ingot": 3},
     "produces": {"id": "ashenlord_greatsword", "name": "Ashen Lord's Greatsword", "rarity": "legendary",
                  "kind": "weapon", "power": 45, "slot": "right_hand", "two_handed": True, "price": 1500, "desc": "A greatsword forged in the fires of Demonfall, quenched in the blood of chains. Its edge has never dulled and never will."},
     "profession": "blacksmithing", "profession_min_rank": "master",
     "recipe_source": "Cross-continent (Valeria · Mushkara · Khardrum)"},
    {"id": "craft_celestial_robes", "name": "Celestial Robes of the Choir", "kind": "armor",
     "requires": {"celestial_thread_part": 1, "star_shard_part": 1, "silverleaf": 5, "moonleaf": 4},
     "produces": {"id": "celestial_robes", "name": "Celestial Robes of the Choir", "rarity": "legendary",
                  "kind": "armor", "power": 30, "slot": "body", "price": 1100, "desc": "Robes woven from celestial thread and star-shard light. They weigh nothing and turn aside blows that should be fatal."},
     "profession": "tailoring", "profession_min_rank": "expert",
     "recipe_source": "Cross-continent (Haya · Daw'ul Talalu)"},
    {"id": "craft_thorn_bow", "name": "Thornwood Longbow", "kind": "weapon",
     "requires": {"thorn_guardian_core_part": 1, "living_wood_part": 1, "silverleaf": 3, "alpha_fang_part": 1},
     "produces": {"id": "thorn_longbow", "name": "Thornwood Longbow", "rarity": "legendary",
                  "kind": "weapon", "power": 38, "slot": "right_hand", "two_handed": True, "price": 1100, "desc": "A living bow grown from thorn guardian heartwood. It still grows, still remembers the forest, and never misses what it can see."},
     "profession": "bow_crafting", "profession_min_rank": "expert",
     "recipe_source": "Cross-continent (Daw'ul Talalu · Haya · Gennel)"},
    {"id": "craft_forgeheart_platemail", "name": "Forgeheart Platemail", "kind": "armor",
     "requires": {"living_stone_heart_part": 1, "jahra_fragment_part": 2, "chainbreaker_fragment_part": 1, "iron_ore": 8},
     "produces": {"id": "forgeheart_platemail", "name": "Forgeheart Platemail", "rarity": "legendary",
                  "kind": "armor", "power": 42, "slot": "body", "price": 1400, "desc": "Plate armor forged around a living stone heart. It is said the mountain itself guards the one who wears it."},
     "profession": "armorsmithing", "profession_min_rank": "master",
     "recipe_source": "Cross-continent (Khardrum · Mushkara)"},
]


# ============================================================
# REGIONAL PRICE MULTIPLIERS
# ============================================================
# For any item that has a `home_continent` set, prices are:
#   - 0.75x when bought on the home continent
#   - 1.4x when bought on a foreign continent
# Items without a home_continent use 1.0x baseline everywhere.
ITEM_HOME_CONTINENT: dict[str, str] = {
    # Valeria — no unique materials yet in the ITEMS list; use bandit-adjacent goods
    "oak_log":            "valeria",
    "iron_ore":           "mushkara",   # bloodiron feel
    "copper_ore":         "khardrum",
    "wild_herb":          "haya",
    "wisp_essence":       "haya",
    "wolf_pelt":          "gennel",
    "boar_hide":          "gennel",
    "serpent_scale":      "hylion",
    "serpent_venom":      "hylion",
    "orb_fragment":       "hylion",
    "jahra_ingot":        "khardrum",
    "relic_shard":        "concordia",
    "ghast_dust":         "valeria",
    "river_stone":        "valeria",
}


def regional_price_multiplier(item_id: str, continent_id: str | None) -> float:
    home = ITEM_HOME_CONTINENT.get(item_id)
    if not home or not continent_id:
        return 1.0
    return 0.75 if continent_id == home else 1.4
