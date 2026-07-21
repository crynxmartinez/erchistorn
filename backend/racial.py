"""Racial mechanics — Heritage Rank I passive bonuses + resource updates."""
from __future__ import annotations

import random
from datetime import datetime, timezone


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
def racial_combat_mods(character: dict) -> dict:
    """Returns {strike_bonus, damage_taken_mult, heal_mult, log_msgs, extra_effects}."""
    mods = {
        "strike_bonus": 0,
        "damage_taken_mult": 1.0,
        "heal_mult": 1.0,
        "log_msgs": [],
        "extra_effects": [],
    }
    race = character.get("race")
    hp_ratio = character["hp"] / max(1, character["max_hp"])

    # --- Elf: day/night bonuses ---
    if race == "elf":
        tod = current_time_of_day()
        if tod == "lunar":
            mods["strike_bonus"] += 3
            mods["damage_taken_mult"] *= 0.85
            mods["log_msgs"].append("Moonlight sharpens the elf's blade.")
        else:
            mods["heal_mult"] *= 1.05
            mods["log_msgs"].append("Sunlight steadies the elf's hand.")

    # --- Orc: Blood of the Liberated ---
    if race == "orc" and hp_ratio < 0.30:
        mods["strike_bonus"] += 3   # ~+5% dmg approximated
        mods["log_msgs"].append("Blood of the Liberated — the orc's fury rises.")

    # --- Wildblood: Beast Aspect passives ---
    if race == "wildblood":
        aspect = character.get("beast_aspect", "predator")
        if aspect == "predator":
            # +3% damage vs wounded (approx as +2 strike when enemy wounded, applied outside)
            pass
        elif aspect == "swift":
            mods["damage_taken_mult"] *= 0.97
        elif aspect == "guardian":
            mods["damage_taken_mult"] *= 0.95
        elif aspect == "keen_sense":
            mods["strike_bonus"] += 1
        elif aspect == "venomous":
            if random.random() < 0.15:
                mods["extra_effects"].append("apply_poison")

    # --- Half-Elf: chosen heritage diluted (half) ---
    if race == "half_elf":
        heritage = character.get("heritage")
        if heritage == "elf":
            tod = current_time_of_day()
            if tod == "lunar":
                mods["strike_bonus"] += 1  # half of +3
            else:
                mods["heal_mult"] *= 1.025

    # --- Sylvan: fragile penalty offset when in Normal Form (default) ---
    # Shrunken form toggle would be an active ability (Rank III) — deferred.
    # No passive combat mod here for MVP.

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
        character["inner_blood"] = min(100, character.get("inner_blood", 0) + 2)
        if outcome in (1, 2):
            character["exhaustion"] = min(100, character.get("exhaustion", 0) + 2)

    # Orc: Defiance from taking bad outcomes
    if race == "orc" and outcome in (1, 2):
        character["defiance"] = min(100, character.get("defiance", 0) + 5)
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

    # Human: Oath Progress — tricky to detect linkage to oath; use flat small gain on crit success
    if race == "human" and outcome == 6:
        character["oath_progress"] = min(100, character.get("oath_progress", 0) + 5)

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
        character["inner_blood"] = min(100, character.get("inner_blood", 0) + 5)

    return msgs


def ensure_racial_defaults(character: dict) -> None:
    """Backfill missing racial fields on old character docs."""
    defaults = {
        "exhaustion": 0, "resolve": 100, "heritage_rank": 1,
        "oath_progress": 0, "celestial_charge": 0, "stoneguard": 0,
        "harmony": 0, "defiance": 0, "inner_blood": 0, "tide": 0,
        "verdant_essence": 0, "beast_aspect": None, "marine_adaptation": None,
        "zone_active": False,
        "home_town": "ironhold", "current_town": None, "visited_towns": [],
        "guild_id": None, "guild_rank": None,
        "active_quests": [], "completed_quests": [],
    }
    for k, v in defaults.items():
        if k not in character or character.get(k) is None:
            if isinstance(v, list) and character.get(k) is None:
                character[k] = list(v)
            else:
                character.setdefault(k, v)
