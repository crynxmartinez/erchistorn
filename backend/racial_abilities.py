"""Phase E — Racial daily/cooldown active abilities.

Shipping the three highest-impact racial cooldowns from the master spec:
  · Human — Adaptability Focus (24h daily choose-your-focus)
  · Dwarf — Field Repair (12h cooldown; restore armor + weapon durability)
  · Orc   — Break the Chain (40 Defiance; removes control effect)

Other racial abilities (Elf Celestial Shift, Sylvan Shrink, Hyliondrian Drying,
Wildblood Pack Bond, Half-Elf Group Harmony) are on the backlog.
"""
from __future__ import annotations
from datetime import datetime, timezone, timedelta


# ============================================================
# HUMAN — Adaptability Focus
# ============================================================
HUMAN_FOCUSES: dict[str, dict] = {
    "combat": {
        "name": "Combat Focus",
        "desc": "+3% physical damage, +5% combat experience.",
        "modifiers": {"attack_success_mod": 1},
    },
    "adventure": {
        "name": "Adventure Focus",
        "desc": "+3% adventure success chance, +5% adventure experience.",
        "modifiers": {"evasion_mod": 1},
    },
    "crafting": {
        "name": "Crafting Focus",
        "desc": "+5% crafting experience, -5% exhaustion when crafting.",
        "modifiers": {},
    },
    "merchant": {
        "name": "Merchant Focus",
        "desc": "-3% marketplace listing fee, +3% NPC selling value.",
        "modifiers": {},
    },
    "scholar": {
        "name": "Scholar Focus",
        "desc": "+3% investigation success, +5% research experience.",
        "modifiers": {},
    },
}
HUMAN_FOCUS_COOLDOWN_HOURS = 24


def can_use_human_focus(character: dict) -> tuple[bool, str, int]:
    """Return (allowed, reason, seconds_remaining_if_blocked)."""
    if character.get("race") != "human":
        return False, "Only Humans may focus.", 0
    last = character.get("human_focus_last_used")
    if last:
        try:
            since = datetime.fromisoformat(last)
        except ValueError:
            since = None
        if since:
            elapsed = (datetime.now(timezone.utc) - since).total_seconds()
            cd = HUMAN_FOCUS_COOLDOWN_HOURS * 3600
            if elapsed < cd:
                return False, "Your last focus is still resonant.", int(cd - elapsed)
    return True, "", 0


def apply_human_focus(character: dict, focus_id: str) -> tuple[bool, str]:
    if focus_id not in HUMAN_FOCUSES:
        return False, "Unknown focus."
    allowed, reason, _ = can_use_human_focus(character)
    if not allowed:
        return False, reason
    character["human_focus"] = focus_id
    character["human_focus_last_used"] = datetime.now(timezone.utc).isoformat()
    character["human_focus_expires"] = (datetime.now(timezone.utc) + timedelta(hours=HUMAN_FOCUS_COOLDOWN_HOURS)).isoformat()
    return True, f"You commit to a {HUMAN_FOCUSES[focus_id]['name']}."


# ============================================================
# DWARF — Field Repair
# ============================================================
DWARF_FIELD_REPAIR_COOLDOWN_HOURS = 12


def can_use_dwarf_field_repair(character: dict) -> tuple[bool, str, int]:
    if character.get("race") != "dwarf":
        return False, "Only Dwarves may Field Repair.", 0
    last = character.get("dwarf_field_repair_last_used")
    if last:
        try:
            since = datetime.fromisoformat(last)
        except ValueError:
            since = None
        if since:
            elapsed = (datetime.now(timezone.utc) - since).total_seconds()
            cd = DWARF_FIELD_REPAIR_COOLDOWN_HOURS * 3600
            if elapsed < cd:
                return False, "Your hands are still tired from the last repair.", int(cd - elapsed)
    return True, "", 0


def apply_dwarf_field_repair(character: dict) -> tuple[bool, str]:
    allowed, reason, _ = can_use_dwarf_field_repair(character)
    if not allowed:
        return False, reason
    # Restores HP (armor equivalent for the current sim), removes any bleeding.
    heal = min(int(character.get("max_hp", 50) * 0.15), character.get("max_hp", 50) - character.get("hp", 0))
    character["hp"] = int(character.get("hp", 0)) + heal
    # Strip Bleeding status if present
    character["statuses"] = [s for s in character.get("statuses", []) if s.get("id") != "bleeding"]
    character["dwarf_field_repair_last_used"] = datetime.now(timezone.utc).isoformat()
    return True, f"You strip the field-plating, hammer the joints, and repair the wear. (+{heal} HP, Bleeding cleared.)"


# ============================================================
# ORC — Break the Chain
# ============================================================
ORC_BREAK_CHAIN_COST = 40
ORC_BREAK_CHAIN_COOLDOWN_HOURS = 12
ORC_CONTROL_STATUSES = ["stunned", "ensnared", "blinded", "shaken", "cursed"]


def can_use_orc_break_chain(character: dict) -> tuple[bool, str, int]:
    if character.get("race") != "orc":
        return False, "Only Orcs may break the chain.", 0
    if int(character.get("defiance", 0)) < ORC_BREAK_CHAIN_COST:
        return False, f"You need {ORC_BREAK_CHAIN_COST} Defiance. You have {character.get('defiance', 0)}.", 0
    last = character.get("orc_break_chain_last_used")
    if last:
        try:
            since = datetime.fromisoformat(last)
        except ValueError:
            since = None
        if since:
            elapsed = (datetime.now(timezone.utc) - since).total_seconds()
            cd = ORC_BREAK_CHAIN_COOLDOWN_HOURS * 3600
            if elapsed < cd:
                return False, "Your chains are still hot from the last break.", int(cd - elapsed)
    return True, "", 0


def apply_orc_break_chain(character: dict) -> tuple[bool, str]:
    allowed, reason, _ = can_use_orc_break_chain(character)
    if not allowed:
        return False, reason
    before = list(character.get("statuses", []))
    removed = [s for s in before if s.get("id") in ORC_CONTROL_STATUSES]
    character["statuses"] = [s for s in before if s.get("id") not in ORC_CONTROL_STATUSES]
    character["defiance"] = int(character.get("defiance", 0)) - ORC_BREAK_CHAIN_COST
    character["orc_break_chain_last_used"] = datetime.now(timezone.utc).isoformat()
    names = ", ".join(s.get("name", s.get("id", "?")) for s in removed) or "none"
    return True, f"You break the chain. Removed: {names}. (-{ORC_BREAK_CHAIN_COST} Defiance.)"
