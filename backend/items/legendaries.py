"""Legendary powers — game-changing effects on unique/legendary/mythic items.
Each power has a trigger that determines when it fires in combat.
"""
from __future__ import annotations

LEGENDARY_POWERS: dict[str, dict] = {
    "holy_wrath": {
        "id": "holy_wrath", "name": "Holy Wrath",
        "desc": "Every 3rd strike deals +50% damage as fire and applies Burning.",
        "trigger": "on_strike",
        "effect": {"type": "every_nth_strike", "n": 3, "damage_mult": 1.5, "element": "fire", "status": "burning"},
    },
    "storm_call": {
        "id": "storm_call", "name": "Storm Call",
        "desc": "Strikes chain to adjacent enemy for 50% damage.",
        "trigger": "on_strike",
        "effect": {"type": "chain", "damage_mult": 0.5},
    },
    "blood_pact": {
        "id": "blood_pact", "name": "Blood Pact",
        "desc": "15% Lifesteal, but take 5% max HP per turn.",
        "trigger": "passive",
        "effect": {"type": "lifesteal", "value": 0.15, "downside": {"type": "self_damage_pct", "value": 0.05}},
    },
    "frost_nova": {
        "id": "frost_nova", "name": "Frost Nova",
        "desc": "20% chance to freeze enemy on hit.",
        "trigger": "on_strike",
        "effect": {"type": "chance_status", "chance": 0.20, "status": "frozen"},
    },
    "berserker_rage": {
        "id": "berserker_rage", "name": "Berserker Rage",
        "desc": "+1 Might per 10% missing HP.",
        "trigger": "passive",
        "effect": {"type": "scaling_stat", "stat": "might", "per_missing_hp_pct": 10, "value": 1},
    },
    "arcane_surge": {
        "id": "arcane_surge", "name": "Arcane Surge",
        "desc": "+15% magical damage when above 80% MP.",
        "trigger": "passive",
        "effect": {"type": "free_cast_above", "resource": "mp", "threshold": 0.80},
    },
    "phoenix_rebirth": {
        "id": "phoenix_rebirth", "name": "Phoenix Rebirth",
        "desc": "On death, revive at 50% HP (once per combat).",
        "trigger": "passive",
        "effect": {"type": "revive", "hp_pct": 0.50, "once_per_combat": True},
    },
    "gravity_well": {
        "id": "gravity_well", "name": "Gravity Well",
        "desc": "+1 Range. Enemy can't close distance.",
        "trigger": "passive",
        "effect": {"type": "range_bonus", "value": 1, "pin_enemy": True},
    },
    "executioner": {
        "id": "executioner", "name": "Executioner",
        "desc": "+100% damage to enemies below 20% HP.",
        "trigger": "on_strike",
        "effect": {"type": "execute", "threshold": 0.20, "damage_mult": 2.0},
    },
    "aegis_eternal": {
        "id": "aegis_eternal", "name": "Aegis Eternal",
        "desc": "Shield blocks reduce 100% damage when HP below 30%.",
        "trigger": "when_hit",
        "effect": {"type": "full_block_below", "hp_threshold": 0.30},
    },
    "wrath_of_steel": {
        "id": "wrath_of_steel", "name": "Wrath of Steel",
        "desc": "Every 3rd strike deals +50% damage and applies Bleeding.",
        "trigger": "on_strike",
        "effect": {"type": "every_nth_strike", "n": 3, "damage_mult": 1.5, "status": "bleeding"},
    },
    "mirror_image": {
        "id": "mirror_image", "name": "Mirror Image",
        "desc": "When hit, 10% chance to create decoy (absorbs next hit).",
        "trigger": "when_hit",
        "effect": {"type": "chance_decoy", "chance": 0.10},
    },
}
