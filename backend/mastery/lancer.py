"""Lancer — The Elemental Lance Master.

Identity: imbues the lance with elemental buffs, each of which changes what the
Lancer's strikes do. Holding multiple elements at once compounds the riders.

First mastery extracted from `combat_turn` (7 guard calls — the smallest surface,
chosen to prove the pattern). Behaviour is a byte-for-byte move: the golden logs
must read IDENTICAL after this lands. The heavy lifting already lived in
`_lancer_*` helpers in game_engine; what moved here are the call sites and the
inline stat_mod bookkeeping that was interleaved with ten other masteries'.
"""
from __future__ import annotations

import random

from mastery_hooks import BaseHooks, TurnContext, register


@register
class LancerHooks(BaseHooks):
    mastery = "lancer"

    # ---- start of turn ------------------------------------------------
    def on_turn_start(self, ctx: TurnContext) -> None:
        import game_engine as ge

        state, character, log = ctx.state, ctx.character, ctx.log

        # Avatar of Elements (level 100): 2 overload charges
        if ctx.turn == 0 and character.get("level", 1) >= 100:
            state["lancer_overload_charges"] = 2
        if ctx.turn == 0:
            ge._lancer_check_initiation(state, character, log)
            ge._lancer_check_overload(state, character, log)

        # Re-apply active self stat_mods from skills. combat_turn restores
        # character["stats"] on the way out, so every mastery's buffs live in
        # `state` and are re-applied at the top of each turn.
        for entry in state.get("lancer_self_stat_mods", []):
            for stat, val in entry.get("mods", {}).items():
                character["stats"][stat] = character["stats"].get(stat, 0) + val

    # ---- accuracy roll -----------------------------------------------
    def on_action_selected(self, ctx: TurnContext) -> None:
        """Critical Imbue (level 40): +10% crit chance while any imbue is active.

        Runs after the accuracy roll, so it can upgrade a non-crit into a crit.
        Mutates ctx.outcome, which the spine reads back.
        """
        character, state = ctx.character, ctx.state
        if character.get("level", 1) < 40 or ctx.outcome >= 5:
            return
        if state.get("lancer_active_imbues") and random.random() < 0.10:
            ctx.outcome = 5
            ctx.note("lancer_passive",
                     "Critical Imbue — elemental focus grants a critical hit!")

    # ---- skill resolution --------------------------------------------
    def on_skill_used(self, ctx: TurnContext) -> None:
        """Imbue loading and stat_mod application for the skill just used.

        Not part of the MasteryHooks protocol — called explicitly by the spine at
        the point the original code ran, because skill-effect application sits
        between action selection and damage computation and several masteries need
        that exact slot. Kept as a named method rather than folded into
        on_action_selected so the call order stays visible at the call site.
        """
        import game_engine as ge

        state, character, log = ctx.state, ctx.character, ctx.log
        sk = ctx.skill
        if not sk:
            return

        # Apply elemental imbue when casting a buff carrying an `element`.
        if sk.get("element") and sk.get("power_type") == "buff":
            ge._lancer_apply_imbue(state, character, sk, log)

        # Self stat_mods from non-imbue buff/defend skills.
        if sk.get("stat_mod", {}).get("self") and not sk.get("element"):
            self_mods = dict(sk["stat_mod"]["self"])
            mod_dur = sk.get("mod_duration", 3)
            state.setdefault("lancer_self_stat_mods", []).append(
                {"mods": self_mods, "duration": mod_dur})
            for stat, val in self_mods.items():
                character["stats"][stat] = character["stats"].get(stat, 0) + val
            log.append({"kind": "lancer_stat_mod",
                        "text": f"Focus: {', '.join(f'{k} {v:+d}' for k, v in self_mods.items())} "
                                f"for {mod_dur} turns."})

        # Enemy stat_mods from strike/debuff skills.
        if sk.get("stat_mod", {}).get("enemy"):
            enemy_mods = sk["stat_mod"]["enemy"]
            mod_dur = sk.get("mod_duration", 3)
            state.setdefault("lancer_enemy_stat_mods", []).append(
                {"mods": enemy_mods, "duration": mod_dur})
            m_stats = state.get("monster_stats", {})
            for stat, val in enemy_mods.items():
                m_stats[stat] = m_stats.get(stat, 0) + val
            log.append({"kind": "lancer_stat_mod",
                        "text": f"Elemental: {', '.join(f'{k} {v:+d}' for k, v in enemy_mods.items())} "
                                f"to enemy for {mod_dur} turns."})

    # ---- damage -------------------------------------------------------
    def on_damage_computed(self, ctx: TurnContext) -> None:
        """Elemental strike riders — damage multiplier and status application."""
        import game_engine as ge

        if ctx.outgoing <= 0:
            return
        state, character, log = ctx.state, ctx.character, ctx.log
        riders = ge._lancer_get_strike_riders(state, character)

        if riders.get("damage_mult", 1.0) > 1.0:
            old = ctx.outgoing
            ctx.outgoing = int(ctx.outgoing * riders["damage_mult"])
            bonus = ctx.outgoing - old
            if bonus > 0:
                elem_count = ge._lancer_get_element_count(state)
                log.append({"kind": "lancer_rider",
                            "text": f"Elemental riders — +{bonus} damage "
                                    f"({elem_count} elements active)!"})

        for status in riders.get("statuses", []):
            if ctx.outcome >= 3:
                ge._append_status_dedup(state, ge.make_status(status),
                                        key="monster_statuses")
        if riders.get("statuses"):
            log.append({"kind": "lancer_rider",
                        "text": f"Elemental effects: {', '.join(riders['statuses'])}!"})

    # ---- end of turn --------------------------------------------------
    def on_turn_end(self, ctx: TurnContext) -> None:
        import game_engine as ge

        state, character, log = ctx.state, ctx.character, ctx.log
        ge._lancer_tick_end_of_turn(state, character, log)

        # Expire self stat_mods, refunding the stats they granted.
        active = []
        for entry in state.get("lancer_self_stat_mods", []):
            if entry["duration"] > 0:
                active.append(entry)
            else:
                for stat, val in entry["mods"].items():
                    character["stats"][stat] = character["stats"].get(stat, 0) - val
        state["lancer_self_stat_mods"] = active
        for entry in state["lancer_self_stat_mods"]:
            entry["duration"] -= 1

        # Expire enemy stat_mods the same way.
        active_enemy = []
        for entry in state.get("lancer_enemy_stat_mods", []):
            if entry["duration"] > 0:
                active_enemy.append(entry)
            else:
                m_stats = state.get("monster_stats", {})
                for stat, val in entry["mods"].items():
                    m_stats[stat] = m_stats.get(stat, 0) - val
        state["lancer_enemy_stat_mods"] = active_enemy
        for entry in state["lancer_enemy_stat_mods"]:
            entry["duration"] -= 1
