"""Incoming-damage pipeline, extracted from `combat_turn`.

This was one contiguous 180-line chain of 22 mastery guards, every one doing the
same thing to the same variable: adjusting `c_dmg` before it reached the player's
HP. Eight masteries interleaved as a run of
`if _is_<mastery>(character) and monster_attacked and c_dmg > 0:` blocks.

Why a pipeline rather than the generic hook loop
------------------------------------------------
Order is **observable**, in two ways that a `for h in hooks_for(...)` loop would
silently break:

1. Several steps call `random.random()`. Reordering them shifts every subsequent
   roll in the turn, so the golden logs would diverge even though each step's own
   logic was untouched.
2. Two steps are **universal**, not mastery-gated — the range-gap check and the
   `confused` self-hit — and they sit *between* masteries (after Assassin, and
   after Rogue). A per-mastery loop has nowhere to put them.

So the sequence is declared explicitly as data. Each step names the mastery it
requires (or None for universal), and `run_incoming_pipeline` walks them in order.
The order below is the original source order, unchanged.
"""
from __future__ import annotations

import random

from mastery_hooks import TurnContext


def _attacked(ctx: TurnContext) -> bool:
    """Did the enemy actually swing? Heals and buffs do not count."""
    return bool(ctx.state.get("_monster_attacked"))


def _player_has(ctx: TurnContext, *names: str) -> bool:
    """Match on `id` or `name`.

    The originals were inconsistent about which they checked — Assassin and Hunter
    matched `name` only, Rogue matched both. That inconsistency is load-bearing for
    the goldens, so it is preserved per-step rather than unified here.
    """
    for s in ctx.state.get("player_statuses", []) or []:
        if s.get("name") in names or s.get("id") in names:
            return True
    return False


def _player_has_name(ctx: TurnContext, name: str) -> bool:
    return any(s.get("name") == name for s in ctx.state.get("player_statuses", []) or [])


# ============================================================
# Steps, in exact original order
# ============================================================

def _knight_milestones(ctx: TurnContext) -> None:
    import game_engine as ge

    if not _attacked(ctx) or ctx.incoming <= 0:
        return
    state, character, log = ctx.state, ctx.character, ctx.log
    level = character.get("level", 1)
    mods = ge._knight_check_milestones(state, character, ctx.monster, log)
    if mods.get("incoming_damage_mult"):
        ctx.incoming = int(ctx.incoming * mods["incoming_damage_mult"])
    if level >= 70 and state.get("knight_oath_stacks", 0) >= 10:
        ctx.incoming = int(ctx.incoming * 0.75)
    if level >= 80 and (character["hp"] / max(1, character["max_hp"])) < 0.25:
        ctx.incoming = int(ctx.incoming * 0.70)
        log.append({"kind": "knight_passive", "text": "UNBREAKABLE — damage reduced by 30%!"})


def _knight_stack_on_hit(ctx: TurnContext) -> None:
    import game_engine as ge

    if _attacked(ctx) and ctx.incoming > 0:
        ge._knight_gain_stack(ctx.state, ctx.character, ctx.log, "hit_or_defend")


def _knight_stack_on_swing(ctx: TurnContext) -> None:
    import game_engine as ge

    if _attacked(ctx):
        ge._knight_gain_stack(ctx.state, ctx.character, ctx.log, "enemy_attacks")


def _knight_reflect(ctx: TurnContext) -> None:
    import game_engine as ge

    if not _attacked(ctx) or ctx.incoming <= 0:
        return
    mods = ge._knight_check_milestones(ctx.state, ctx.character, ctx.monster, ctx.log)
    if mods.get("reflect_10pct"):
        reflect = max(1, int(ctx.incoming * 0.10))
        ctx.state["monster_hp"] = max(0, ctx.state["monster_hp"] - reflect)
        ctx.note("knight_oath", f"Oath of Iron reflects {reflect} damage back!")


def _assassin_shadow_linger(ctx: TurnContext) -> None:
    if not _attacked(ctx) or ctx.state.get("assassin_shadow_linger", 0) <= 0:
        return
    if random.random() < 0.75:
        ctx.incoming = 0
        ctx.note("assassin_passive", "Shadow linger — the attack passes through shadow!")


def _assassin_hidden(ctx: TurnContext) -> None:
    if _attacked(ctx) and _player_has_name(ctx, "hidden"):
        ctx.incoming = 0
        ctx.note("assassin_hidden", "The Assassin is hidden — the attack hits nothing!")


def _range_gap(ctx: TurnContext) -> None:
    """Universal: a positive range gap means the enemy cannot reach at all."""
    if _attacked(ctx) and ctx.state.get("range_gap", 0) > 0:
        ctx.incoming = 0
        ctx.note("range_gap",
                 f"Range {ctx.state['range_gap']} — the enemy can't close the distance!")


def _hunter_defences(ctx: TurnContext) -> None:
    state = ctx.state
    if not _attacked(ctx):
        return
    if (ctx.incoming > 0 and state.get("range_gap", 0) <= 0
            and state.get("player_range", 0) <= 0):
        ctx.incoming = int(ctx.incoming * 1.25)
        ctx.note("hunter_range", "Range 0 — melee vulnerability! +25% damage taken!")
    if ctx.incoming > 0 and state.get("hunter_intangible_turns", 0) > 0:
        ctx.incoming = 0
        ctx.note("hunter_intangible",
                 "You phase through the spirit world — the attack hits nothing!")
    if ctx.incoming > 0 and state.get("hunter_immune_turns", 0) > 0:
        ctx.incoming = 0
        ctx.note("hunter_immune", "Ancestor spirits shield you — the attack is absorbed!")
    if ctx.incoming > 0 and state.get("hunter_spirit_copy_absorb"):
        ctx.incoming = 0
        state["hunter_spirit_copy_absorb"] = False
        ctx.note("hunter_spirit_copy", "The spirit copy absorbs the blow and dissolves!")
    if ctx.incoming > 0 and _player_has_name(ctx, "evasive"):
        if random.random() < 0.75:
            ctx.incoming = 0
            ctx.note("hunter_evasive", "The Hunter dodges — the attack misses!")


def _rogue_defences(ctx: TurnContext) -> None:
    import game_engine as ge

    state, log = ctx.state, ctx.log
    if not _attacked(ctx):
        return
    if ctx.incoming > 0 and _player_has(ctx, "evasive"):
        dodge = 0.75 if state.get("rogue_master_of_tricks") else 0.50
        if random.random() < dodge:
            ctx.incoming = 0
            log.append({"kind": "rogue_evasive",
                        "text": "The Rogue dodges — the attack misses!"})
    if ctx.incoming > 0:
        bonus = ge._rogue_get_evasion_bonus(state)
        if bonus > 0 and random.random() < (bonus / 100.0):
            ctx.incoming = 0
            log.append({"kind": "rogue_lucky_dodger",
                        "text": f"Lucky Dodger — {bonus}% evasion kicks in! Attack misses!"})
    if _player_has_name(ctx, "hidden"):
        ctx.incoming = 0
        log.append({"kind": "rogue_hidden",
                    "text": "The Rogue is hidden — the attack hits nothing!"})
    # Reads whether the attack ended up missing, so it runs after the dodges.
    ge._rogue_check_lucky_dodger(state, log, enemy_missed=(ctx.incoming == 0))


def _confused_self_hit(ctx: TurnContext) -> None:
    """Universal: a confused enemy may hit itself instead."""
    if not _attacked(ctx) or ctx.incoming <= 0:
        return
    if not any(s.get("id") == "confused" for s in ctx.state.get("monster_statuses", [])):
        return
    if random.random() < 0.50:
        dmg = int(ctx.incoming)
        ctx.state["monster_hp"] = max(0, ctx.state["monster_hp"] - dmg)
        ctx.note("confused",
                 f"The {ctx.monster['name']} is confused — it strikes itself for {dmg} damage!")
        ctx.incoming = 0


def _bard_redirects(ctx: TurnContext) -> None:
    state = ctx.state
    name = ctx.monster.get("name", "the enemy")
    if _attacked(ctx) and ctx.incoming > 0 and state.get("bard_friendly_fire"):
        if random.random() < state.get("bard_friendly_fire_chance", 0.10):
            dmg = int(ctx.incoming)
            state["monster_hp"] = max(0, state["monster_hp"] - dmg)
            ctx.note("bard_friendly_fire",
                     f"Dance of Freedom — the {name} attacks itself for {dmg} damage!")
            ctx.incoming = 0
    if _attacked(ctx) and ctx.incoming > 0 and state.get("bard_confuse"):
        if random.random() < state.get("bard_confuse_chance", 0.10):
            dmg = int(ctx.incoming)
            state["monster_hp"] = max(0, state["monster_hp"] - dmg)
            ctx.note("bard_confuse",
                     f"Dance of Confusion — the {name} strikes itself for {dmg} damage!")
            ctx.incoming = 0


def _bard_death_save(ctx: TurnContext) -> None:
    import game_engine as ge

    if ctx.incoming > 0:
        ctx.incoming = ge._bard_check_death_save(
            ctx.state, ctx.character, int(ctx.incoming), ctx.log)


def _mage_glass_cannon(ctx: TurnContext) -> None:
    if ctx.state.get("mage_glass_cannon_active") and ctx.incoming > 0:
        ctx.incoming = int(ctx.incoming * 1.50)
        ctx.note("mage_passive", "Glass Cannon — +50% damage taken!")


def _druid_fusion_defence(ctx: TurnContext) -> None:
    import game_engine as ge

    if ctx.incoming > 0 and ctx.state.get("druid_fusion_active"):
        ctx.incoming = ge._druid_apply_fusion_defense(
            ctx.state, ctx.character, ctx.log, int(ctx.incoming))


def _paladin_aura_of_warding(ctx: TurnContext) -> None:
    import game_engine as ge

    if ctx.character.get("level", 1) >= 70 and ctx.incoming > 0:
        if ge._has_player_status(ctx.character, ctx.state, "warded"):
            ctx.incoming = int(ctx.incoming * 0.90)
            ctx.note("paladin_passive",
                     "AURA OF WARDING — -10% damage taken while Warded!")


def _priest_shield_wall(ctx: TurnContext) -> None:
    import game_engine as ge

    if ctx.incoming > 0 and ctx.state.get("priest_shield_wall_hp", 0) > 0:
        ctx.incoming = ge._priest_absorb_damage(
            ctx.state, ctx.character, int(ctx.incoming), ctx.log)


def _legendary_when_hit(ctx: TurnContext) -> None:
    """Universal: legendary item powers with a when-hit trigger."""
    import game_engine as ge

    if ctx.incoming > 0:
        ctx.incoming = ge._apply_legendary_powers_when_hit(
            ctx.state, ctx.character, ctx.log, int(ctx.incoming))


# (required_mastery | None, step) — exact original source order.
INCOMING_PIPELINE = [
    ("knight",   _knight_milestones),
    ("knight",   _knight_stack_on_hit),
    ("knight",   _knight_stack_on_swing),
    ("knight",   _knight_reflect),
    ("assassin", _assassin_shadow_linger),
    ("assassin", _assassin_hidden),
    (None,       _range_gap),
    ("hunter",   _hunter_defences),
    ("rogue",    _rogue_defences),
    (None,       _confused_self_hit),
    ("bard",     _bard_redirects),
    ("bard",     _bard_death_save),
    ("mage",     _mage_glass_cannon),
    ("druid",    _druid_fusion_defence),
    ("paladin",  _paladin_aura_of_warding),
    ("priest",   _priest_shield_wall),
    (None,       _legendary_when_hit),
]


def run_incoming_pipeline(ctx: TurnContext) -> None:
    """Apply every mitigation step in order, skipping masteries not owned."""
    owned = set(ctx.character.get("masteries") or [])
    for required, step in INCOMING_PIPELINE:
        if required is None or required in owned:
            step(ctx)
