"""Racial mechanics — Heritage Rank passives, resource updates, and rank progression."""
from __future__ import annotations

import random
from datetime import datetime, timezone

from game_data_p2 import (
    HERITAGE_RANK_1, HERITAGE_SURGES, HERITAGE_SURGE_RANK_CONFIG,
    HERITAGE_RANK_LEVEL_REQS, HERITAGE_RANK_MULT,
)

# Build race → resource_key map from HERITAGE_RANK_1
_RACE_TO_RESOURCE = {race: meta["resource"] for race, meta in HERITAGE_RANK_1.items()}


# =====================================================
# Time of day (server UTC)
# =====================================================
def current_time_of_day() -> str:
    """Solar = 06:00-17:59 UTC. Lunar = 18:00-05:59 UTC."""
    h = datetime.now(timezone.utc).hour
    return "solar" if 6 <= h < 18 else "lunar"


# =====================================================
# Racial passive bonuses (Rank I)
# Applied by combat_turn and resolve_action
# =====================================================
def _rank_mult(character: dict) -> float:
    """Passive scaling multiplier based on heritage_rank (1..5)."""
    rank = max(1, min(5, character.get("heritage_rank", 1)))
    return HERITAGE_RANK_MULT[rank - 1]


def racial_combat_mods(character: dict) -> dict:
    """Returns {strike_bonus, damage_taken_mult, heal_mult, log_msgs, extra_effects, surge_effects}."""
    mods = {
        "strike_bonus": 0,
        "damage_taken_mult": 1.0,
        "heal_mult": 1.0,
        "log_msgs": [],
        "extra_effects": [],
        "surge_effects": None,
    }
    race = character.get("race")
    hp_ratio = character["hp"] / max(1, character["max_hp"])
    mult = _rank_mult(character)

    # --- Heritage Surge active? ---
    surge_remaining = character.get("heritage_surge_active", 0)
    if surge_remaining > 0:
        surge = HERITAGE_SURGES.get(race, {})
        fx = surge.get("effects", {})
        mods["surge_effects"] = fx
        mods["strike_bonus"] += fx.get("strike_bonus", 0)
        if "damage_taken_mult" in fx:
            mods["damage_taken_mult"] *= fx["damage_taken_mult"]
        if "heal_mult" in fx:
            mods["heal_mult"] *= fx["heal_mult"]
        if fx.get("damage_mult"):
            mods["extra_effects"].append("surge_double_damage")
        if fx.get("debuff_immune"):
            mods["extra_effects"].append("surge_debuff_immune")
        if fx.get("control_immune"):
            mods["extra_effects"].append("surge_control_immune")
        if fx.get("lifesteal_pct"):
            mods["extra_effects"].append(f"surge_lifesteal:{fx['lifesteal_pct']}")
        if fx.get("evasion_bonus"):
            mods["extra_effects"].append(f"surge_evasion:{fx['evasion_bonus']}")
        if fx.get("dual_celestial"):
            # Both solar + lunar at once — apply lunar bonuses on top
            mods["strike_bonus"] += 3
            mods["damage_taken_mult"] *= 0.85
            mods["heal_mult"] *= 1.05
        mods["log_msgs"].append(f"{surge.get('name', 'Heritage Surge')} is active! ({surge_remaining} actions left)")

    # --- Elf: day/night bonuses ---
    if race == "elf":
        tod = current_time_of_day()
        if tod == "lunar":
            mods["strike_bonus"] += round(3 * mult)
            mods["damage_taken_mult"] *= 1.0 - (0.15 * mult)
            mods["log_msgs"].append("Moonlight sharpens the elf's blade.")
        else:
            mods["heal_mult"] *= 1.0 + (0.05 * mult)
            mods["log_msgs"].append("Sunlight steadies the elf's hand.")

    # --- Orc: Blood of the Liberated ---
    if race == "orc" and hp_ratio < 0.30:
        mods["strike_bonus"] += round(3 * mult)
        mods["log_msgs"].append("Blood of the Liberated — the orc's fury rises.")

    # --- Wildblood: Beast Aspect passives ---
    if race == "wildblood":
        aspect = character.get("beast_aspect", "predator")
        if aspect == "predator":
            pass
        elif aspect == "swift":
            mods["damage_taken_mult"] *= 1.0 - (0.03 * mult)
        elif aspect == "guardian":
            mods["damage_taken_mult"] *= 1.0 - (0.05 * mult)
        elif aspect == "keen_sense":
            mods["strike_bonus"] += round(1 * mult)
        elif aspect == "venomous":
            if random.random() < 0.15 * mult:
                mods["extra_effects"].append("apply_poison")

    # --- Half-Elf: chosen heritage diluted (half) ---
    if race == "half_elf":
        heritage = character.get("heritage")
        if heritage == "elf":
            tod = current_time_of_day()
            if tod == "lunar":
                mods["strike_bonus"] += round(1 * mult)
            else:
                mods["heal_mult"] *= 1.0 + (0.025 * mult)

    # --- Sylvan: fragile penalty offset when in Normal Form (default) ---
    # --- Dwarf: passive is out-of-combat (armor, mining) — no direct combat mod ---
    # --- Hyliondrian: passive is water-region — no direct land-combat mod ---

    return mods


# =====================================================
# Racial resource accumulation (per action / per combat turn)
# =====================================================
def tick_racial_resources_on_action(character: dict, outcome: int, action_id: str) -> list[str]:
    """Called after any /game/action call. Returns log messages for UI."""
    msgs = []
    race = character.get("race")

    # Wildblood: Inner Blood from actions/damage
    if race == "wildblood":
        character["inner_blood"] = min(100, character.get("inner_blood", 0) + 5)
        if outcome in (1, 2):
            character["exhaustion"] = min(100, character.get("exhaustion", 0) + 2)

    # Orc: Defiance from taking bad outcomes
    if race == "orc" and outcome in (1, 2):
        character["defiance"] = min(100, character.get("defiance", 0) + 10)
        character["exhaustion"] = min(100, character.get("exhaustion", 0) + 1)

    # Elf: Celestial Charge on successful actions during matching celestial period
    if race == "elf" and outcome >= 4:
        # Simplified: 1 in 5 chance per successful action, cap 2/day (approximated via cap 5 total)
        if random.random() < 0.20 and character.get("celestial_charge", 0) < 5:
            character["celestial_charge"] = character.get("celestial_charge", 0) + 1
            msgs.append("A Celestial Charge awakens within you.")

    # Dwarf: Stoneguard from crafting/mining actions
    if race == "dwarf" and action_id in ("gather",) and outcome >= 4:
        if random.random() < 0.25 and character.get("stoneguard", 0) < 5:
            character["stoneguard"] = character.get("stoneguard", 0) + 1

    # Hyliondrian: Tide from fishing
    if race == "hyliondrian" and action_id == "fish" and outcome >= 3:
        if character.get("tide", 0) < 5:
            character["tide"] = character.get("tide", 0) + 1

    # Sylvan: Verdant Essence from gather (herbs)
    if race == "sylvan" and action_id == "gather" and outcome >= 4:
        if random.random() < 0.30 and character.get("verdant_essence", 0) < 5:
            character["verdant_essence"] = character.get("verdant_essence", 0) + 1

    # Half-Elf: Harmony from any success
    if race == "half_elf" and outcome >= 4:
        if random.random() < 0.20 and character.get("harmony", 0) < 5:
            character["harmony"] = character.get("harmony", 0) + 1

    # Human: Oath Progress — gain on crit success and regular success
    if race == "human" and outcome >= 5:
        character["oath_progress"] = min(100, character.get("oath_progress", 0) + 10)

    # Universal: recover a bit of resolve on successful actions
    if outcome >= 5:
        character["resolve"] = min(100, character.get("resolve", 0) + 2)
    elif outcome == 1:
        character["resolve"] = max(0, character.get("resolve", 0) - 3)

    return msgs


def tick_racial_on_combat_win(character: dict) -> list[str]:
    """Called on combat victory."""
    msgs = []
    race = character.get("race")
    hp_ratio = character["hp"] / max(1, character["max_hp"])

    # Orc Battle Recovery (Rank II preview — kept simple)
    if race == "orc" and hp_ratio < 0.5:
        recovered = 3
        character["hp"] = min(character["max_hp"], character["hp"] + recovered)
        character["exhaustion"] = max(0, character.get("exhaustion", 0) - 2)
        msgs.append(f"Battle Recovery — the Orc regains {recovered} HP.")

    # Wildblood: Inner Blood on kill
    if race == "wildblood":
        character["inner_blood"] = min(100, character.get("inner_blood", 0) + 10)

    return msgs


def ensure_racial_defaults(character: dict) -> None:
    """Backfill missing racial fields on old character docs."""
    defaults = {
        "exhaustion": 0, "resolve": 100, "heritage_rank": 1,
        "heritage_surge_active": 0, "heritage_surge_last_used": None,
        "oath_progress": 0, "celestial_charge": 0, "stoneguard": 0,
        "harmony": 0, "defiance": 0, "inner_blood": 0, "tide": 0,
        "verdant_essence": 0, "beast_aspect": None, "marine_adaptation": None,
        "zone_active": False,
        "home_town": "ironhold", "current_town": None, "visited_towns": [],
        "guild_id": None, "guild_rank": None,
        "active_quests": [], "completed_quests": [],
        "deaths": 0, "last_death": None, "last_sanctuary_town": None,
        "last_screen": None,
    }
    for k, v in defaults.items():
        if k not in character or character.get(k) is None:
            if isinstance(v, list) and character.get(k) is None:
                character[k] = list(v)
            else:
                character.setdefault(k, v)


# =====================================================
# Heritage Rank-Up
# =====================================================
def can_rank_up(character: dict) -> tuple[bool, str, dict]:
    """Check if the player can rank up. Requires full resource bar + level gate."""
    rank = character.get("heritage_rank", 1)
    if rank >= 5:
        return False, "Already at maximum heritage rank.", {}
    idx = rank - 1  # 0-based index into LEVEL_REQS
    level_req = HERITAGE_RANK_LEVEL_REQS[idx]
    level = character.get("level", 1)

    if level < level_req:
        return False, f"Requires character level {level_req} (you are {level}).", {}

    # Check resource bar is full
    race = character.get("race")
    resource_key = _RACE_TO_RESOURCE.get(race)
    if not resource_key:
        return False, "No racial resource for this race.", {}
    meta = HERITAGE_RANK_1.get(race, {})
    max_val = meta.get("resource_max", 1)
    current = character.get(resource_key, 0)
    if current < max_val:
        return False, f"Resource not full ({current}/{max_val}).", {}

    surge = HERITAGE_SURGES.get(race, {})
    return True, "", {"level_req": level_req, "surge": surge, "resource_key": resource_key}


def apply_rank_up(character: dict) -> tuple[bool, str]:
    """Reset resource bar to 0, increment heritage_rank. Surge unlocks at rank 2+."""
    ok, reason, info = can_rank_up(character)
    if not ok:
        return False, reason

    # Reset the racial resource bar
    resource_key = info["resource_key"]
    character[resource_key] = 0

    character["heritage_rank"] = character.get("heritage_rank", 1) + 1

    surge = info.get("surge", {})
    surge_name = surge.get("name", "Heritage Surge")
    return True, f"Heritage Rank increased to {character['heritage_rank']}! Surge unlocked: {surge_name}."


# =====================================================
# Heritage Surge
# =====================================================
def can_activate_surge(character: dict) -> tuple[bool, str, int]:
    """Check if the player can activate their Heritage Surge.
    Returns (ok, reason, seconds_remaining)."""
    rank = character.get("heritage_rank", 1)
    if rank < 2:
        return False, "Heritage Surge unlocks at Rank 2.", 0

    if character.get("heritage_surge_active", 0) > 0:
        return False, "Heritage Surge is already active.", 0

    # Require full resource bar
    race = character.get("race")
    resource_key = _RACE_TO_RESOURCE.get(race)
    if not resource_key:
        return False, "No racial resource for this race.", 0
    meta = HERITAGE_RANK_1.get(race, {})
    max_val = meta.get("resource_max", 1)
    current = character.get(resource_key, 0)
    if current < max_val:
        return False, f"You need full {meta.get('resource_label', resource_key)} ({current}/{max_val}).", 0

    # Check cooldown
    last_used = character.get("heritage_surge_last_used")
    if last_used:
        last_dt = datetime.fromisoformat(last_used)
        now = datetime.now(timezone.utc)
        elapsed = (now - last_dt).total_seconds()
        idx = min(rank - 2, len(HERITAGE_SURGE_RANK_CONFIG) - 1)
        cooldown_seconds = HERITAGE_SURGE_RANK_CONFIG[idx]["cooldown_hours"] * 3600
        if elapsed < cooldown_seconds:
            return False, "Heritage Surge is on cooldown.", int(cooldown_seconds - elapsed)

    return True, "", 0


def apply_surge(character: dict) -> tuple[bool, str]:
    """Activate Heritage Surge. Consumes full resource bar, sets duration, records timestamp."""
    ok, reason, _ = can_activate_surge(character)
    if not ok:
        return False, reason

    rank = character.get("heritage_rank", 1)
    idx = min(rank - 2, len(HERITAGE_SURGE_RANK_CONFIG) - 1)
    config = HERITAGE_SURGE_RANK_CONFIG[idx]
    duration = config["duration"]

    # Consume the full resource bar
    race = character.get("race")
    resource_key = _RACE_TO_RESOURCE.get(race)
    if resource_key:
        character[resource_key] = 0

    character["heritage_surge_active"] = duration
    character["heritage_surge_last_used"] = datetime.now(timezone.utc).isoformat()

    # Apply instant effects
    surge = HERITAGE_SURGES.get(race, {})
    fx = surge.get("effects", {})
    if fx.get("instant_heal_pct"):
        heal_amt = int(character["max_hp"] * fx["instant_heal_pct"] / 100)
        character["hp"] = min(character["max_hp"], character["hp"] + heal_amt)

    # Purge debuffs if debuff_immune
    if fx.get("debuff_immune"):
        character["statuses"] = [s for s in character.get("statuses", []) if s.get("kind") != "debuff"]

    # Resource boost (for half-elf dual awakening — boosts AFTER consuming, so they get +2)
    if fx.get("resource_boost") and resource_key:
        meta = HERITAGE_RANK_1.get(race, {})
        max_val = meta.get("resource_max", 1)
        character[resource_key] = min(max_val, character.get(resource_key, 0) + fx["resource_boost"])

    return True, f"{surge.get('name', 'Heritage Surge')} activated! Lasts {duration} actions.", surge.get("narrative", "")


def tick_surge_on_action(character: dict) -> list[str]:
    """Decrement surge counter after each action. Returns log messages."""
    msgs = []
    remaining = character.get("heritage_surge_active", 0)
    if remaining > 0:
        # Apply per-action surge effects
        race = character.get("race")
        surge = HERITAGE_SURGES.get(race, {})
        fx = surge.get("effects", {})

        if fx.get("heal_per_action_pct"):
            heal_amt = int(character["max_hp"] * fx["heal_per_action_pct"] / 100)
            character["hp"] = min(character["max_hp"], character["hp"] + heal_amt)
            msgs.append(f"Surge heals {heal_amt} HP.")

        if fx.get("armor_repair_pct"):
            msgs.append(f"Surge repairs armor by {fx['armor_repair_pct']}%.")

        character["heritage_surge_active"] = remaining - 1
        if character["heritage_surge_active"] <= 0:
            character["heritage_surge_active"] = 0
            msgs.append(f"{surge.get('name', 'Heritage Surge')} has faded.")

    return msgs


def get_active_surge_info(character: dict) -> dict | None:
    """Return info about currently active surge, or None."""
    remaining = character.get("heritage_surge_active", 0)
    if remaining <= 0:
        return None
    race = character.get("race")
    surge = HERITAGE_SURGES.get(race, {})
    return {
        "name": surge.get("name", "Heritage Surge"),
        "desc": surge.get("desc", ""),
        "effects": surge.get("effects", {}),
        "actions_remaining": remaining,
    }
