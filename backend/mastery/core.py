"""Turn-start and turn-end hooks for the masteries still partly inline.

Each class here owns the phases that moved cleanly out of `combat_turn`:
start-of-turn resource setup and end-of-turn ticking. The damage-path logic for
these masteries is still inline in the spine — it is interleaved with damage
computation rather than appended to a phase, so moving it needs the spine
restructured, which is a separate step under the same golden-log discipline.

Grouped in one module rather than one file per mastery because each is currently
20 lines or fewer. They split out as they grow — `lancer.py` is already separate
because it is fully extracted.

HOOK_ORDER in mastery_hooks.py preserves the original inline execution order.
Ordering is observable (two masteries can both touch ctx.outgoing), so it is part
of the contract, not an implementation detail.
"""
from __future__ import annotations

from mastery_hooks import BaseHooks, TurnContext, register


@register
class KnightHooks(BaseHooks):
    """The Oathbound — commits to an Oath and grows stronger holding it."""

    mastery = "knight"

    def on_turn_start(self, ctx: TurnContext) -> None:
        import game_engine as ge

        state, character, log = ctx.state, ctx.character, ctx.log
        # Oath Sworn (level 10): start combat with 2 stacks
        if (ctx.turn == 0 and character.get("level", 1) >= 10
                and state.get("knight_oath") and state.get("knight_oath_stacks", 0) == 0):
            state["knight_oath_stacks"] = 2
            log.append({"kind": "knight_passive",
                        "text": "OATH SWORN — starting with 2 Oath stacks!"})
        ge._knight_apply_oath_bonuses(state, character)
        # Re-apply active self stat_mods (Iron Stance, Adrenal Surge, ...). Buffs
        # live in `state` because combat_turn restores character["stats"] on exit.
        for entry in state.get("knight_self_stat_mods", []):
            for stat, val in entry.get("mods", {}).items():
                character["stats"][stat] = character["stats"].get(stat, 0) + val

    def on_turn_end(self, ctx: TurnContext) -> None:
        import game_engine as ge

        ge._knight_tick_end_of_turn(ctx.state, ctx.character, ctx.log)


@register
class PaladinHooks(BaseHooks):
    """Holy warrior whose power rises as HP falls — the Faith bar."""

    mastery = "paladin"

    def on_turn_start(self, ctx: TurnContext) -> None:
        import game_engine as ge

        state, character, log = ctx.state, ctx.character, ctx.log
        level = character.get("level", 1)

        if ctx.turn == 0 and level >= 10:
            ge._append_status_dedup(state, ge.make_status("warded"), key="player_statuses")
            log.append({"kind": "paladin_passive",
                        "text": "DIVINE SHIELD — Warded at combat start!"})
        if ctx.turn == 0 and level >= 20:
            state["paladin_holy_fortitude"] = True
        if ctx.turn == 0 and level >= 30 and not state.get("paladin_blessed_armor_applied"):
            character["stats"]["armor_bonus"] = character["stats"].get("armor_bonus", 0) + 2
            character["stats"]["essence"] = character["stats"].get("essence", 0) + 2
            state["paladin_blessed_armor_applied"] = True
            log.append({"kind": "paladin_passive",
                        "text": "BLESSED ARMOR — +2 Armor, +2 Essence (permanent)!"})
        if ctx.turn == 0 and level >= 100:
            state["paladin_avatar_of_faith"] = True
            log.append({"kind": "paladin_passive",
                        "text": "AVATAR OF FAITH — Faith bar permanently at maximum "
                                "(Faith Ascendant)!"})
        if ctx.turn == 0:
            ge._paladin_update_scaling(state, character, log)

        for entry in state.get("paladin_self_stat_mods", []):
            for stat, val in entry.get("mods", {}).items():
                character["stats"][stat] = character["stats"].get(stat, 0) + val

    def on_turn_end(self, ctx: TurnContext) -> None:
        import game_engine as ge

        state, character = ctx.state, ctx.character
        ge.tick_stat_mods(state, "paladin_self_stat_mods", character["stats"])
        # Paladin enemy mods expire without refunding — the originals never
        # subtracted them, and preserving that is what keeps the goldens identical.
        surviving = [e for e in state.get("paladin_enemy_stat_mods", [])
                     if e.get("duration", 0) > 0]
        state["paladin_enemy_stat_mods"] = surviving
        for entry in surviving:
            entry["duration"] -= 1
        # Faith scaling updates live via _clamp_and_sync_combat_hp.
        if character.get("level", 1) >= 100 and not state.get("paladin_avatar_of_faith"):
            state["paladin_avatar_of_faith"] = True


@register
class PriestHooks(BaseHooks):
    """Voice of the gods — Sanctity scales with how wounded the enemy is."""

    mastery = "priest"

    def on_turn_start(self, ctx: TurnContext) -> None:
        import game_engine as ge

        character, log = ctx.character, ctx.log
        level = character.get("level", 1)

        if ctx.turn == 0:
            if level >= 30:
                character["stats"]["essence"] = character["stats"].get("essence", 0) + 10
                log.append({"kind": "priest_passive",
                            "text": "DIVINE FORTITUDE — +10 Essence (permanent)!"})
            if level >= 10:
                log.append({"kind": "priest_passive",
                            "text": "SANCTIFIED — Sanctity activates at 90% enemy HP!"})
            if level >= 100:
                log.append({"kind": "priest_passive",
                            "text": "AVATAR OF FAITH — Sanctity doubled, heals shield "
                                    "allies, enemy heal locked!"})
        # Start-of-turn HoT / delayed heals / Smite live in the engine helper.
        if ctx.turn > 0:
            ge._priest_start_of_turn(ctx.state, character, log)

    def on_turn_end(self, ctx: TurnContext) -> None:
        import game_engine as ge

        ge._priest_tick_end_of_turn(ctx.state, ctx.character, ctx.log)


@register
class AssassinHooks(BaseHooks):
    """The Shadow Reaper — banks Shadows to 100, then BURSTs."""

    mastery = "assassin"

    def on_turn_start(self, ctx: TurnContext) -> None:
        import game_engine as ge

        if ctx.turn != 0:
            return
        state, character, log = ctx.state, ctx.character, ctx.log
        level = character.get("level", 1)
        if level >= 10:
            start_shadows = 20 if state.get("is_night") else 10
            ge._assassin_gain_shadows(state, character, log, start_shadows, "Shadow Born")
        if level >= 100 and state.get("is_night"):
            state["assassin_shadows"] = 75
            log.append({"kind": "assassin_passive",
                        "text": "AVATAR OF SHADOW — 75 shadows at night!"})

    def on_turn_end(self, ctx: TurnContext) -> None:
        import game_engine as ge

        ge._assassin_tick_end_of_turn(ctx.state, ctx.character, ctx.log)


@register
class HunterHooks(BaseHooks):
    """Master of Precision — Spirit Guidance stacks, and range gap matters."""

    mastery = "hunter"

    def on_turn_end(self, ctx: TurnContext) -> None:
        import game_engine as ge

        ge._hunter_tick_end_of_turn(ctx.state, ctx.character, ctx.log)


@register
class MageHooks(BaseHooks):
    """Arcane Library — equipped passives reshape what spells do."""

    mastery = "mage"

    def on_turn_end(self, ctx: TurnContext) -> None:
        import game_engine as ge

        state, character = ctx.state, ctx.character
        ge._mage_tick_end_of_turn(state, character, ctx.log)
        ge.tick_stat_mods(state, "mage_self_stat_mods", character["stats"])
        ge.tick_stat_mods(state, "mage_enemy_stat_mods",
                          state.setdefault("monster_stats", {}))


@register
class AlchemistHooks(BaseHooks):
    """The Transmuter — pre-imbues the katar and spends Combo Flow."""

    mastery = "alchemist"

    def on_turn_end(self, ctx: TurnContext) -> None:
        import game_engine as ge

        state, character = ctx.state, ctx.character
        ge._alch_tick_alchemist_state(state, ctx.log)
        ge.tick_stat_mods(state, "alchemist_self_stat_mods", character["stats"])


@register
class RogueHooks(BaseHooks):
    """The Adaptive Trickster — builds a passive kit from innate slots."""

    mastery = "rogue"


@register
class BardHooks(BaseHooks):
    """Master of Control — Song rewrites ally rules, Dance controls the enemy."""

    mastery = "bard"


@register
class DruidHooks(BaseHooks):
    """The wild answers when called — summons, fusion, pack synergy."""

    mastery = "druid"
