"""Phase E — Racial daily/cooldown active abilities.

Shipping all 8 racial cooldowns from the master spec:
  · Human       — Adaptability Focus (24h daily choose-your-focus)
  · Dwarf       — Field Repair (12h; restore armor + weapon durability)
  · Orc         — Break the Chain (40 Defiance; removes control effect)
  · Elf         — Celestial Shift (1 Charge, 6h; starlight cleanse + heal)
  · Half-Elf    — Heritage Attunement (3 Harmony, 24h; blended-bloodline buff)
  · Wildblood   — Bloodrage (40 Inner Blood, 8h; berserk buff for 4 actions)
  · Hyliondrian — Tidal Grace (3 Tide, 12h; heal + purify)
  · Sylvan      — Shrunken Form (1 Verdant Essence, 10-min CD; toggle stealth mode)
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


# ============================================================
# Shared cooldown helper
# ============================================================
def _cooldown_remaining(character: dict, key: str, cooldown_hours: float) -> int:
    """Return seconds remaining on the given last-used timestamp field."""
    last = character.get(key)
    if not last:
        return 0
    try:
        since = datetime.fromisoformat(last)
    except ValueError:
        return 0
    elapsed = (datetime.now(timezone.utc) - since).total_seconds()
    cd = cooldown_hours * 3600
    return int(max(0, cd - elapsed))


# ============================================================
# ELF — Celestial Shift
# Spend 1 Celestial Charge to invoke starlight: heals 30% max HP,
# purges all debuffs. 6h cooldown.
# ============================================================
ELF_CELESTIAL_SHIFT_COST = 1
ELF_CELESTIAL_SHIFT_COOLDOWN_HOURS = 6


def can_use_elf_celestial_shift(character: dict) -> tuple[bool, str, int]:
    if character.get("race") != "elf":
        return False, "Only Elves may call the starlight.", 0
    if int(character.get("celestial_charge", 0)) < ELF_CELESTIAL_SHIFT_COST:
        return False, f"You need {ELF_CELESTIAL_SHIFT_COST} Celestial Charge. You have {character.get('celestial_charge', 0)}.", 0
    rem = _cooldown_remaining(character, "elf_celestial_shift_last_used", ELF_CELESTIAL_SHIFT_COOLDOWN_HOURS)
    if rem > 0:
        return False, "The stars have not yet returned to alignment.", rem
    return True, "", 0


def apply_elf_celestial_shift(character: dict) -> tuple[bool, str]:
    allowed, reason, _ = can_use_elf_celestial_shift(character)
    if not allowed:
        return False, reason
    heal = min(int(character.get("max_hp", 50) * 0.30), character.get("max_hp", 50) - character.get("hp", 0))
    character["hp"] = int(character.get("hp", 0)) + heal
    # Purge every debuff (leaves buffs untouched — buffs are marked with is_buff=True)
    before = character.get("statuses", []) or []
    character["statuses"] = [s for s in before if s.get("is_buff")]
    purged = len(before) - len(character["statuses"])
    character["celestial_charge"] = int(character.get("celestial_charge", 0)) - ELF_CELESTIAL_SHIFT_COST
    character["elf_celestial_shift_last_used"] = datetime.now(timezone.utc).isoformat()
    return True, f"Starlight floods your veins. (+{heal} HP, {purged} debuff{'s' if purged != 1 else ''} purged.)"


# ============================================================
# HALF-ELF — Heritage Attunement
# Spend 3 Harmony to blend both bloodlines: +1 attack, +1 evasion,
# +5 resolve for 5 actions. 24h cooldown.
# ============================================================
HALFELF_ATTUNEMENT_COST = 3
HALFELF_ATTUNEMENT_COOLDOWN_HOURS = 24
HALFELF_ATTUNEMENT_DURATION = 5   # actions


def can_use_halfelf_attunement(character: dict) -> tuple[bool, str, int]:
    if character.get("race") != "half_elf":
        return False, "Only Half-Elves may attune both heritages.", 0
    if int(character.get("harmony", 0)) < HALFELF_ATTUNEMENT_COST:
        return False, f"You need {HALFELF_ATTUNEMENT_COST} Harmony. You have {character.get('harmony', 0)}.", 0
    rem = _cooldown_remaining(character, "halfelf_attunement_last_used", HALFELF_ATTUNEMENT_COOLDOWN_HOURS)
    if rem > 0:
        return False, "Your bloodlines are still humming from the last attunement.", rem
    return True, "", 0


def apply_halfelf_attunement(character: dict) -> tuple[bool, str]:
    allowed, reason, _ = can_use_halfelf_attunement(character)
    if not allowed:
        return False, reason
    # Apply Heritage Attunement buff — 5 actions of +1 attack / +1 evasion
    statuses = character.setdefault("statuses", [])
    statuses = [s for s in statuses if s.get("id") != "heritage_attunement"]
    statuses.append({
        "id": "heritage_attunement",
        "name": "Heritage Attunement",
        "duration": HALFELF_ATTUNEMENT_DURATION,
        "is_buff": True,
        "modifiers": {"attack_success_mod": 1, "evasion_mod": 1},
    })
    character["statuses"] = statuses
    character["resolve"] = min(100, int(character.get("resolve", 0)) + 5)
    character["harmony"] = int(character.get("harmony", 0)) - HALFELF_ATTUNEMENT_COST
    character["halfelf_attunement_last_used"] = datetime.now(timezone.utc).isoformat()
    return True, f"Both bloodlines resonate. Heritage Attunement active for {HALFELF_ATTUNEMENT_DURATION} actions."


# ============================================================
# WILDBLOOD — Bloodrage
# Spend 40 Inner Blood to enter a berserk state: +2 attack, -1 evasion
# for 4 actions. 8h cooldown. Adds Weary status when it ends (via duration expiry logic in server).
# ============================================================
WILDBLOOD_BLOODRAGE_COST = 40
WILDBLOOD_BLOODRAGE_COOLDOWN_HOURS = 8
WILDBLOOD_BLOODRAGE_DURATION = 4  # actions


def can_use_wildblood_bloodrage(character: dict) -> tuple[bool, str, int]:
    if character.get("race") != "wildblood":
        return False, "Only Wildbloods can call the bloodrage.", 0
    if int(character.get("inner_blood", 0)) < WILDBLOOD_BLOODRAGE_COST:
        return False, f"You need {WILDBLOOD_BLOODRAGE_COST} Inner Blood. You have {character.get('inner_blood', 0)}.", 0
    rem = _cooldown_remaining(character, "wildblood_bloodrage_last_used", WILDBLOOD_BLOODRAGE_COOLDOWN_HOURS)
    if rem > 0:
        return False, "Your beast still slumbers from the last rage.", rem
    return True, "", 0


def apply_wildblood_bloodrage(character: dict) -> tuple[bool, str]:
    allowed, reason, _ = can_use_wildblood_bloodrage(character)
    if not allowed:
        return False, reason
    statuses = character.setdefault("statuses", [])
    statuses = [s for s in statuses if s.get("id") != "bloodrage"]
    statuses.append({
        "id": "bloodrage",
        "name": "Bloodrage",
        "duration": WILDBLOOD_BLOODRAGE_DURATION,
        "is_buff": True,
        "modifiers": {"attack_success_mod": 2, "evasion_mod": -1},
    })
    character["statuses"] = statuses
    character["inner_blood"] = int(character.get("inner_blood", 0)) - WILDBLOOD_BLOODRAGE_COST
    character["wildblood_bloodrage_last_used"] = datetime.now(timezone.utc).isoformat()
    return True, f"The beast rises. Bloodrage burns for {WILDBLOOD_BLOODRAGE_DURATION} actions."


# ============================================================
# HYLIONDRIAN — Tidal Grace
# Spend 3 Tide to summon the ocean's mercy: heal 40% max HP + purge every debuff.
# 12h cooldown.
# ============================================================
HYLIONDRIAN_TIDAL_GRACE_COST = 3
HYLIONDRIAN_TIDAL_GRACE_COOLDOWN_HOURS = 12


def can_use_hyliondrian_tidal_grace(character: dict) -> tuple[bool, str, int]:
    if character.get("race") != "hyliondrian":
        return False, "Only Hyliondrians can call the tides.", 0
    if int(character.get("tide", 0)) < HYLIONDRIAN_TIDAL_GRACE_COST:
        return False, f"You need {HYLIONDRIAN_TIDAL_GRACE_COST} Tide. You have {character.get('tide', 0)}.", 0
    rem = _cooldown_remaining(character, "hyliondrian_tidal_grace_last_used", HYLIONDRIAN_TIDAL_GRACE_COOLDOWN_HOURS)
    if rem > 0:
        return False, "The tide has ebbed. Wait for it to return.", rem
    return True, "", 0


def apply_hyliondrian_tidal_grace(character: dict) -> tuple[bool, str]:
    allowed, reason, _ = can_use_hyliondrian_tidal_grace(character)
    if not allowed:
        return False, reason
    heal = min(int(character.get("max_hp", 50) * 0.40), character.get("max_hp", 50) - character.get("hp", 0))
    character["hp"] = int(character.get("hp", 0)) + heal
    before = character.get("statuses", []) or []
    character["statuses"] = [s for s in before if s.get("is_buff")]
    purged = len(before) - len(character["statuses"])
    character["tide"] = int(character.get("tide", 0)) - HYLIONDRIAN_TIDAL_GRACE_COST
    character["hyliondrian_tidal_grace_last_used"] = datetime.now(timezone.utc).isoformat()
    return True, f"The ocean answers. (+{heal} HP, {purged} debuff{'s' if purged != 1 else ''} washed away.)"


# ============================================================
# SYLVAN — Shrunken Form (toggle)
# 1 Verdant Essence to activate. 10-minute cooldown from last state change.
# While shrunken: +2 evasion_mod, -1 attack_success_mod (stealthy but weaker).
# Toggling off is free and also triggers the same 10-min cooldown.
# ============================================================
SYLVAN_SHRINK_COST = 1
SYLVAN_SHRINK_COOLDOWN_MINUTES = 10


def _sylvan_is_shrunken(character: dict) -> bool:
    return any(s.get("id") == "shrunken" for s in character.get("statuses", []) or [])


def can_use_sylvan_shrink(character: dict) -> tuple[bool, str, int]:
    if character.get("race") != "sylvan":
        return False, "Only Sylvans can slip between the leaves.", 0
    rem = _cooldown_remaining(character, "sylvan_shrink_last_used", SYLVAN_SHRINK_COOLDOWN_MINUTES / 60)
    if rem > 0:
        return False, "You are still gathering the essence to shift form.", rem
    # If not currently shrunken, need essence to activate. Toggle-off is always free.
    if not _sylvan_is_shrunken(character):
        if int(character.get("verdant_essence", 0)) < SYLVAN_SHRINK_COST:
            return False, f"You need {SYLVAN_SHRINK_COST} Verdant Essence. You have {character.get('verdant_essence', 0)}.", 0
    return True, "", 0


def apply_sylvan_shrink(character: dict) -> tuple[bool, str]:
    allowed, reason, _ = can_use_sylvan_shrink(character)
    if not allowed:
        return False, reason
    statuses = character.setdefault("statuses", [])
    if _sylvan_is_shrunken(character):
        # Toggle OFF — remove the status, no essence cost
        character["statuses"] = [s for s in statuses if s.get("id") != "shrunken"]
        character["sylvan_shrink_last_used"] = datetime.now(timezone.utc).isoformat()
        return True, "You return to your true stature."
    # Toggle ON — apply status, spend essence
    statuses.append({
        "id": "shrunken",
        "name": "Shrunken Form",
        "duration": 999,  # persists until manually toggled off
        "is_buff": True,
        "modifiers": {"evasion_mod": 2, "attack_success_mod": -1},
    })
    character["statuses"] = statuses
    character["verdant_essence"] = int(character.get("verdant_essence", 0)) - SYLVAN_SHRINK_COST
    character["sylvan_shrink_last_used"] = datetime.now(timezone.utc).isoformat()
    return True, "You slip between the leaves. Shrunken Form active."
