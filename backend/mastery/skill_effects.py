"""Mastery skill-effect application, extracted from `combat_turn`.

353 lines and 45 mastery guard calls: everything that happens *because a specific
skill was used*, for every mastery at once — stat_mods, imbues, shadow gains,
performance registration, per-skill-id special cases, legendary rules.

Moved verbatim as one function rather than split per mastery. Order here is
observable: several steps consume RNG and several read state an earlier step wrote,
so moving the run intact makes the extraction provably behaviour-preserving.
Splitting in the same step would have produced a large diff with no way to
attribute a golden-log divergence to a specific change. This module is where that
per-mastery split now happens, one mastery at a time.

Boundary note: the region deliberately stops before the cooldown/skill-capacity
block that follows it. A first attempt cut through that block, and `_cd` — a local
the spine still needed — went out of scope. The crossing set is computed, not
guessed: only `outcome` (the Mage's Arcane Surge and Assassin thresholds can
upgrade the roll) and `skill_used_msg` (a cracked katar rewrites the line) cross,
and both travel on the context.
"""
from __future__ import annotations

import random

from mastery_hooks import TurnContext


def apply_skill_effects(ctx: TurnContext) -> None:
    """Run every mastery's reaction to the skill used this turn, in source order."""
    import game_engine as ge
    from game_data import SKILLS_BY_ID

    state, character, log = ctx.state, ctx.character, ctx.log
    monster, sk = ctx.monster, ctx.skill
    if sk is None:
        return
    outcome = ctx.outcome
    skill_used_msg = ctx.skill_used_msg

    if sk.get("stat_mod", {}).get("self") and ge._is_assassin(character):
        ge.apply_self_stat_mods(state, character, sk["stat_mod"]["self"],
                             sk.get("mod_duration", 3), "assassin_self_stat_mods",
                             log, "assassin_stat_mod", "Shadow: ")

    # Assassin: apply enemy stat_mods from strike/debuff skills
    if sk.get("stat_mod", {}).get("enemy") and ge._is_assassin(character):
        ge.apply_enemy_stat_mods(state, sk["stat_mod"]["enemy"],
                              sk.get("mod_duration", 3), "assassin_enemy_stat_mods")

    # Mage: apply self stat_mods from buff/defend skills
    if sk.get("stat_mod", {}).get("self") and ge._is_mage(character):
        ge.apply_self_stat_mods(state, character, sk["stat_mod"]["self"],
                             sk.get("mod_duration", 3), "mage_self_stat_mods",
                             log, "mage_stat_mod", "Arcane: ")

    # Generic self stat_mods — for masteries with no bespoke branch above.
    #
    # Every self-stat_mod branch is gated on a specific mastery, and the Druid
    # was never one of them, so all 19 Druid skills carrying
    # `stat_mod: {"self": ...}` applied their status but silently dropped their
    # stat bonuses. This is the fallback so no mastery can be forgotten again.
    _BESPOKE_SELF_MOD = ("alchemist", "assassin", "hunter", "knight",
                         "lancer", "mage", "paladin", "rogue")
    if sk.get("stat_mod", {}).get("self") and not any(
            m in (character.get("masteries") or []) for m in _BESPOKE_SELF_MOD):
        self_mods = dict(sk["stat_mod"]["self"])
        mod_dur = sk.get("mod_duration", 3)

        # Shapeshift exclusivity: you are one animal at a time. Without this a
        # Druid could stack bear + eagle + beast form and keep every bonus.
        if ge._is_druid(character) and sk["id"].endswith("_form"):
            prior = state.get("druid_active_form")
            if prior and prior != sk["id"]:
                for entry in list(state.get("generic_self_stat_mods", [])):
                    if entry.get("form"):
                        for stat, val in entry["mods"].items():
                            character["stats"][stat] = character["stats"].get(stat, 0) - val
                        state["generic_self_stat_mods"].remove(entry)
                log.append({"kind": "druid_form",
                            "text": f"The {prior.replace('_', ' ')} sloughs away as a new shape takes hold."})
            state["druid_active_form"] = sk["id"]

        state.setdefault("generic_self_stat_mods", []).append({
            "mods": self_mods, "duration": mod_dur,
            "form": bool(ge._is_druid(character) and sk["id"].endswith("_form")),
        })
        for stat, val in self_mods.items():
            character["stats"][stat] = character["stats"].get(stat, 0) + val
        log.append({"kind": "self_stat_mod",
                    "text": f"{', '.join(f'{k} {v:+d}' for k, v in self_mods.items())} for {mod_dur} turns."})

    # Mage: apply enemy stat_mods from strike/debuff skills
    if sk.get("stat_mod", {}).get("enemy") and ge._is_mage(character):
        enemy_mods = sk["stat_mod"]["enemy"]
        mod_dur = sk.get("mod_duration", 3)
        # Time Dilation passive: debuffs last +1 turn
        mod_dur += ge._mage_get_debuff_duration_modifier(character)
        # Mass Hysteria (Mental): debuffs bite 50% deeper on the single target.
        mod_dur = int(mod_dur * ge._mage_get_debuff_duration_multiplier(character))
        state.setdefault("mage_enemy_stat_mods", []).append({"mods": enemy_mods, "duration": mod_dur})
        m_stats = state.get("monster_stats", {})
        for stat, val in enemy_mods.items():
            m_stats[stat] = m_stats.get(stat, 0) + val
        log.append({"kind": "mage_stat_mod", "text": f"Spell: {', '.join(f'{k} {v:+d}' for k,v in enemy_mods.items())} to enemy for {mod_dur} turns."})

    # Mage: Arcane Library passive — status override
    if ge._is_mage(character) and sk.get("status_apply"):
        override_status = ge._mage_get_status_override(character, sk)
        if override_status:
            sk["status_apply"] = override_status
            log.append({"kind": "mage_passive", "text": f"Status transformed: {override_status}!"})
        # Extra status from Thunderblood
        extra_status = ge._mage_get_extra_status(character, sk)
        if extra_status:
            ge._append_status_dedup(state, ge.make_status(extra_status), key="monster_statuses")
            log.append({"kind": "mage_passive", "text": f"Thunderblood — also applies {extra_status}!"})

    # Mage: Arcane Library passive — Phobia Implant (first debuff stuns)
    if ge._is_mage(character):
        ge._mage_check_phobia_implant(state, character, sk, log)

    # Mage: Spatial riders — Gravity Shift / Reposition / Blink Step
    if ge._is_mage(character):
        ge._mage_apply_spatial_riders(state, character, sk, log)
        # Elemental Overload: elemental statuses land at +2 stacks
        if sk and sk.get("status_apply"):
            ge._mage_apply_status_stack_bonus(state, character, sk["status_apply"], log)

    # Mage: Arcane Library passive — cooldown reduction
    #
    # Both blocks below used to read `state["cooldowns"]`, a key that nothing in
    # the engine ever writes — player skill cooldowns live in
    # `state["skill_cooldowns"]`. So Quickened Mind and Accelerated Casting
    # could never fire, no matter what the player equipped. Found by a sabotage
    # sweep against the golden harness: changing the cooldown modifier produced
    # zero behavioural diffs, which is only possible if it is unreachable.
    if ge._is_mage(character):
        cd_reduction = ge._mage_get_cooldown_modifier(character)
        if cd_reduction > 0:
            skill_id = sk.get("id", "")
            cds = state.setdefault("skill_cooldowns", {})
            current_cd = cds.get(skill_id, 0)
            if current_cd > 0:
                cds[skill_id] = max(0, current_cd - cd_reduction)
                log.append({"kind": "mage_passive",
                            "text": f"Quickened Mind — {sk.get('name', 'the spell')} "
                                    f"recharges {cd_reduction} turn(s) sooner."})

    # Mage: Accelerated Casting — cooldown 5+ becomes 4
    if ge._is_mage(character) and ge._mage_has_passive(character, "accelerated_casting"):
        skill_id = sk.get("id", "")
        if sk.get("cooldown", 0) >= 5:
            cds = state.setdefault("skill_cooldowns", {})
            if cds.get(skill_id, 0) > 4:
                cds[skill_id] = 4
                log.append({"kind": "mage_passive",
                            "text": "Accelerated Casting — the long spell comes back faster."})

    # Mage: Mana Vampire — restore MP equal to 10% of damage dealt
    if ge._is_mage(character) and ge._mage_has_passive(character, "mana_vampire") and sk.get("power_type") == "strike":
        # MP restoration handled after damage calculation in _execute_strike
        state["mage_mana_vampire_active"] = True

    # Priest: process skill (Sanctity scaling, Miracle, Shield Wall, etc.)
    if ge._is_priest(character) and sk.get("type") == "priest":
        ge._priest_process_skill(state, character, sk, log)
        # Divine Wrath (L80): cooldown reduction when enemy <= 25% HP
        priest_cd_red = ge._priest_get_cooldown_reduction(state, character)
        if priest_cd_red > 0:
            priest_sid = sk.get("id", "")
            current_cd = state.get("skill_cooldowns", {}).get(priest_sid, 0)
            if current_cd > 0:
                state["skill_cooldowns"][priest_sid] = max(0, current_cd - priest_cd_red)
                log.append({"kind": "priest_divine_wrath", "text": "Divine Wrath — cooldown reduced!"})

    # Assassin: stealth break — attacking from hidden generates shadows
    if ge._is_assassin(character) and sk.get("power_type") == "strike":
        was_hidden = any(s.get("name") == "hidden" for s in state.get("player_statuses", []))
        if was_hidden:
            # Remove hidden status
            state["player_statuses"] = [s for s in state.get("player_statuses", []) if s.get("name") != "hidden"]
            # Stealth break: +15 shadows (or +20 for Shadow Clone, +30 for Umbral Cloak at night)
            break_shadows = 15
            if sk.get("id") == "shadow_clone":
                break_shadows = 20
            if sk.get("id") == "umbral_cloak" and state.get("is_night"):
                break_shadows = 30
            ge._assassin_gain_shadows(state, character, log, break_shadows, "stealth break")
            # Guaranteed crit from stealth break
            outcome = max(5, outcome)
            log.append({"kind": "assassin_stealth_break", "text": "Stealth breaks — guaranteed critical hit!"})
            # Avatar of Shadow (level 100): 75% evasion for 1 turn after stealth break
            if character.get("level", 1) >= 100:
                state["assassin_shadow_linger"] = 1
                log.append({"kind": "assassin_passive", "text": "Shadow lingers — 75% evasion for 1 turn!"})

    # Assassin: deposit fear on strike/debuff skills
    if ge._is_assassin(character) and sk.get("power_type") in ("strike", "debuff"):
        ge._assassin_deposit_fear(state, character, monster, log, amount=5)

    # Assassin: Shadow Convergence skill surges shadows +25
    if sk.get("id") == "shadow_convergence" and ge._is_assassin(character):
        ge._assassin_gain_shadows(state, character, log, 25, "Shadow Convergence")

    # Assassin: Eclipse Blade — while active, strikes generate +2 shadows
    if sk.get("id") == "eclipse_blade" and ge._is_assassin(character):
        state["assassin_eclipse_blade_active"] = True

    # Assassin: night_veil — Night: duration extended by +1 turn
    if sk.get("id") == "night_veil" and ge._is_assassin(character) and state.get("is_night"):
        for s in state.get("player_statuses", []):
            if s.get("name") == "hidden":
                s["duration"] = s.get("duration", 2) + 1
                break
        log.append({"kind": "assassin_passive", "text": "Night Veil — night extends stealth duration by 1 turn!"})

    # Assassin: umbral_cloak — Night: stealth duration +2 turns
    if sk.get("id") == "umbral_cloak" and ge._is_assassin(character) and state.get("is_night"):
        for s in state.get("player_statuses", []):
            if s.get("name") == "hidden":
                s["duration"] = s.get("duration", 2) + 2
                break
        log.append({"kind": "assassin_passive", "text": "Umbral Cloak — night extends stealth duration by 2 turns!"})

    # Assassin: shadow_devour — reclaim ALL deposited shadows and convert to bonus damage
    if sk.get("id") == "shadow_devour" and ge._is_assassin(character):
        deposited = state.get("assassin_deposited_shadows", 0)
        if deposited > 0:
            bonus_dmg = deposited * 2  # 2 damage per deposited shadow
            state["assassin_deposited_shadows"] = 0
            ge._assassin_gain_shadows(state, character, log, deposited, "Shadow Devour reclaim")
            log.append({"kind": "assassin_devour", "text": f"Shadow Devour reclaims {deposited} fear — +{bonus_dmg} bonus damage!"})

    # Assassin: reapers_arrival — deposit ALL remaining shadows as fear; night auto-BURST at 75+
    if sk.get("id") == "reapers_arrival" and ge._is_assassin(character):
        all_shadows = state.get("assassin_shadows", 0)
        if all_shadows > 0:
            ge._assassin_deposit_fear(state, character, monster, log, amount=all_shadows)
            state["assassin_shadows"] = 0
            log.append({"kind": "assassin_devour", "text": f"Reaper's Arrival — all {all_shadows} shadows deposited as fear!"})
        # Night: auto-BURST if shadows were at 75+ (before deposit)
        if state.get("is_night") and all_shadows >= 75:
            state["assassin_shadows"] = ge._assassin_get_burst_threshold(character)
            state["assassin_burst_ready"] = True
            log.append({"kind": "assassin_passive", "text": "Reaper's Arrival — night auto-triggers BURST!"})

    # Assassin: eclipse_of_shadows — auto-BURST regardless of shadow count; retain 25 after
    if sk.get("id") == "eclipse_of_shadows" and ge._is_assassin(character):
        threshold = ge._assassin_get_burst_threshold(character)
        state["assassin_shadows"] = threshold
        state["assassin_burst_ready"] = True
        state["assassin_burst_used"] = False  # allow BURST to fire
        log.append({"kind": "assassin_passive", "text": "Eclipse of Shadows — BURST is unleashed regardless of shadow count!"})

    # Hunter: apply self stat_mods from buff skills
    if sk.get("stat_mod", {}).get("self") and ge._is_hunter(character):
        ge.apply_self_stat_mods(state, character, sk["stat_mod"]["self"],
                             sk.get("mod_duration", 3), "hunter_self_stat_mods",
                             log, "hunter_stat_mod", "Hunter: ")

    # Hunter: apply enemy stat_mods from strike/debuff/trap skills
    if sk.get("stat_mod", {}).get("enemy") and ge._is_hunter(character):
        ge.apply_enemy_stat_mods(state, sk["stat_mod"]["enemy"],
                              sk.get("mod_duration", 3), "hunter_enemy_stat_mods")

    # Rogue: apply self stat_mods from buff/defend skills
    if sk.get("stat_mod", {}).get("self") and ge._is_rogue(character):
        ge.apply_self_stat_mods(state, character, sk["stat_mod"]["self"],
                             sk.get("mod_duration", 3), "rogue_self_stat_mods",
                             log, "rogue_stat_mod", "Rogue: ")

    # Rogue: apply enemy stat_mods from strike/debuff skills
    if sk.get("stat_mod", {}).get("enemy") and ge._is_rogue(character):
        enemy_mods = sk["stat_mod"]["enemy"]
        mod_dur = sk.get("mod_duration", 3)
        # Con Artist: extend debuff stat_mod duration
        con_bonus = ge._rogue_get_con_artist_bonus(state)
        mod_dur += con_bonus
        state.setdefault("rogue_enemy_stat_mods", []).append({"mods": enemy_mods, "duration": mod_dur})
        # Apply immediately to monster stats
        m_stats = state.setdefault("monster_stats", {})
        for stat, val in enemy_mods.items():
            m_stats[stat] = m_stats.get(stat, 0) + val

    # Bard: process performance skills
    if sk.get("power_type") == "performance" and ge._is_bard(character):
        ge._bard_process_performance(state, character, sk, log)
        skill_used_msg = f"{character['name']} performs {sk['name']}!"

    # Bard: apply all_allies stat_mods from buff/defend/heal skills
    if sk.get("stat_mod", {}).get("all_allies") and ge._is_bard(character):
        ge._bard_apply_all_allies_stat_mod(character, sk["stat_mod"], log)
        allies_mods = sk["stat_mod"]["all_allies"]
        mod_dur = sk.get("mod_duration", 3)
        state.setdefault("bard_ally_stat_mods", []).append({"mods": allies_mods, "duration": mod_dur})
        for stat, val in allies_mods.items():
            character["stats"][stat] = character["stats"].get(stat, 0) + val

    # Bard: apply enemy stat_mods from strike/debuff skills
    if sk.get("stat_mod", {}).get("enemy") and ge._is_bard(character):
        enemy_mods = sk["stat_mod"]["enemy"]
        mod_dur = sk.get("mod_duration", 3)
        state.setdefault("bard_enemy_stat_mods", []).append({"mods": enemy_mods, "duration": mod_dur})
        m_stats = state.setdefault("monster_stats", {})
        for stat, val in enemy_mods.items():
            m_stats[stat] = m_stats.get(stat, 0) + val

    # Bard: heal_percent on non-performance skills (buff/defend/heal)
    if sk.get("heal_percent") and ge._is_bard(character) and sk.get("power_type") != "performance":
        heal_amt = int(character.get("max_hp", 100) * sk["heal_percent"])
        character["hp"] = min(character.get("max_hp", 999), character["hp"] + heal_amt)
        log.append({"kind": "bard_heal", "text": f"The performance heals {heal_amt} HP!"})

    # Bard: defend skills apply self_status
    if sk.get("power_type") == "defend" and ge._is_bard(character) and sk.get("self_status"):
        ge._append_status_dedup(character, ge.make_status(sk["self_status"]))

    # Bard: buff skills apply self_status
    if sk.get("power_type") == "buff" and ge._is_bard(character) and sk.get("self_status"):
        ge._append_status_dedup(character, ge.make_status(sk["self_status"]))

    # Bard: heal skills apply self_status
    if sk.get("power_type") == "heal" and ge._is_bard(character) and sk.get("self_status"):
        ge._append_status_dedup(character, ge.make_status(sk["self_status"]))

    # Bard: sunrise_chorus — cleanse debuffs on self_debuff trigger
    if sk.get("id") == "sunrise_chorus" and ge._is_bard(character):
        cleansed = []
        for s in list(character.get("statuses", [])):
            if s.get("kind") == "debuff":
                cleansed.append(s.get("name", s.get("id", "unknown")))
                character["statuses"].remove(s)
        if cleansed:
            log.append({"kind": "bard_cleanse", "text": f"Sunrise Chorus cleanses: {', '.join(cleansed)}!"})

    # Hunter: apply Range modifiers
    if ge._is_hunter(character) and sk.get("range_modifier", 0) > 0:
        ge._hunter_apply_range_modifier(state, character, sk, log)

    # Hunter: check ambush on first strike from stealth
    if ge._is_hunter(character) and sk.get("power_type") == "strike":
        ge._hunter_check_ambush(state, character, log)

    # Hunter: Trap Master (level 40) — traps affect all enemies (+50% damage in 1v1)
    if ge._is_hunter(character) and sk.get("power_type") == "trap" and character.get("level", 1) >= 40:
        # Trap Master communion: +1 Spirit Guidance per enemy hit
        if state.get("hunter_spirit_communion"):
            ge._hunter_gain_guidance(state, character, log, 1)
            log.append({"kind": "hunter_trap_master", "text": "Trap Master — +1 Spirit Guidance from trap!"})

    # Rogue: on strike — apply Trap Master and Dirty Fighter innates
    if ge._is_rogue(character) and sk.get("power_type") == "strike":
        ge._rogue_on_strike(state, character, log)

    # Hunter: Eagle Eye / Hawk Vision — set guaranteed crits
    if sk.get("id") in ("eagle_eye", "hawk_vision") and ge._is_hunter(character):
        crits = 3
        if state.get("hunter_spirit_communion"):
            crits = 3  # already 3 from communion
        state["hunter_guaranteed_crits"] = max(state.get("hunter_guaranteed_crits", 0), crits)
        log.append({"kind": "hunter_passive", "text": f"Next {crits} hits are guaranteed crits!"})

    # Hunter: Alpha Command — spirit bow charges
    if sk.get("id") == "alpha_command" and ge._is_hunter(character):
        state["hunter_spirit_bow_charges"] = 3
        log.append({"kind": "hunter_passive", "text": "Spirit Bow — next 3 strikes deal true damage!"})

    # Hunter: Ghost Step (level 60) communion — Spirit Walk grants intangible 2 turns without communion
    if sk.get("id") == "spirit_walk" and ge._is_hunter(character) and character.get("level", 1) >= 60:
        if not state.get("hunter_spirit_communion"):
            state["hunter_intangible_turns"] = max(state.get("hunter_intangible_turns", 0), 2)
            log.append({"kind": "hunter_ghost_step", "text": "Ghost Step — Spirit Walk grants intangibility for 2 turns!"})

    # Hunter: heal skills
    if sk.get("heal_percent") and ge._is_hunter(character) and sk.get("power_type") in ("heal", "defend"):
        heal_amt = int(character.get("max_hp", 100) * sk["heal_percent"])
        character["hp"] = min(character.get("max_hp", 999), character["hp"] + heal_amt)
        log.append({"kind": "hunter_heal", "text": f"Nature heals — {heal_amt} HP recovered."})

    # Alchemist: legendary rules
    if sk.get("legendary_rule") and ge._is_alchemist(character):
        lr = sk["legendary_rule"]
        if lr == "infinite_charges_max_mini_rules":
            state["alchemist_infinite_charges"] = sk.get("mod_duration", 4)
            state["alchemist_max_mini_rules"] = True
            # Re-imbue current imbue with infinite charges if one is loaded
            if state.get("alchemist_imbue"):
                state["alchemist_imbue_charges"] = 999
            log.append({"kind": "alchemist_legendary", "text": "PHILOSOPHER'S TRANSMUTATION — infinite imbue charges, all mini-rules at max effect!"})
        elif lr == "auto_adapt_katar":
            log.append({"kind": "alchemist_legendary", "text": "LEGEND OF ALCHEMY — the katar reads the enemy and adapts. 8 hits of true damage unleashed!"})

    ctx.outcome = outcome
    ctx.skill_used_msg = skill_used_msg
