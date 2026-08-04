"""Outgoing-damage riders, extracted from `combat_turn`.

192 lines of per-mastery damage riders: the run of
`if _is_<mastery>(character) and total_dmg > 0:` blocks that fire after the
player's damage is computed but before it lands — Paladin holy bonus, Priest
sanctity, Knight oath scaling, Mage passives, Assassin thresholds, Hunter
communion, Rogue opportunist, Druid fusion.

Same reasoning as mastery/mitigation.py: order is observable (several steps
consume RNG, several read state an earlier step wrote), so the run is moved
intact rather than reordered into a per-mastery loop.

Crossing locals were computed rather than guessed — `total_dmg` and `outcome` are
the only two, and both travel on the context. (`bonus` and `shadows` look like
they cross but appear only inside comments after the region.)
"""
from __future__ import annotations

import random

from mastery_hooks import TurnContext


def apply_outgoing_riders(ctx: TurnContext) -> None:
    """Apply every mastery's outgoing-damage rider, in source order."""
    import game_engine as ge
    from game_data import SKILLS_BY_ID

    state, character, log = ctx.state, ctx.character, ctx.log
    monster, sk = ctx.monster, ctx.skill
    total_dmg = ctx.outgoing
    outcome = ctx.outcome
    # The Oath of Vanguard rider below reads `turn`, but this unpack originally
    # omitted it, so `POST /game/combat/turn` raised NameError for any Knight who
    # had sworn Vanguard. It survived every earlier check because nothing
    # selected that oath: no golden scenario picked it and no playthrough set it.
    # `combat_turn` assigns `turn` exactly once, so ctx.turn never diverges.
    turn = ctx.turn

    # Paladin: Divine Retribution (level 50) — x1.5 on ALL strikes vs undead/devils
    if ge._is_paladin(character) and character.get("level", 1) >= 50 and total_dmg > 0:
        monster_category = ge._monster_category(monster)
        monster_tags = monster.get("tags", [])
        if monster_category in ("undead", "devil") or "undead" in monster_tags or "devil" in monster_tags:
            if not state.get("paladin_holy_bonus_active"):
                total_dmg = int(total_dmg * 1.5)
                log.append({"kind": "paladin_holy", "text": f"DIVINE RETRIBUTION — +50% damage vs {monster['name']}!"})

    # Priest: Sanctity scaling + holy damage bonus on strikes
    if ge._is_priest(character) and total_dmg > 0 and sk and sk.get("power_type") == "strike":
        sanctity = ge._priest_get_sanctity_mult(state, character)
        holy_mult = ge._priest_get_holy_bonus_mult(state, character, monster)
        judgment_mult = ge._priest_get_strike_damage_mult(state, character)
        total_mult = sanctity * holy_mult * judgment_mult
        if total_mult > 1.0:
            old_dmg = total_dmg
            total_dmg = int(total_dmg * total_mult)
            bonus = total_dmg - old_dmg
            if bonus > 0:
                parts = []
                if sanctity > 1.0:
                    parts.append(f"Sanctity x{sanctity:.2f}")
                if holy_mult > 1.0:
                    parts.append(f"Holy x{holy_mult:.2f}")
                if judgment_mult > 1.0:
                    parts.append(f"Judgment x{judgment_mult:.2f}")
                log.append({"kind": "priest_strike_bonus", "text": f"{' + '.join(parts)} — +{bonus} damage!"})

    # Knight: Oath milestone strike damage bonus (Oath of Wrath 5-stack: +20%)
    if ge._is_knight(character) and total_dmg > 0:
        knight_mods = ge._knight_check_milestones(state, character, monster, log)
        if knight_mods.get("strike_damage_mult"):
            total_dmg = int(total_dmg * knight_mods["strike_damage_mult"])
            log.append({"kind": "knight_oath", "text": f"Oath of Wrath empowers the strike — +{int((knight_mods['strike_damage_mult']-1)*100)}% damage!"})
        # Oath of Wrath: gain stack when dealing damage (2 stacks on roll 5+)
        if state.get("knight_oath") == "wrath" and total_dmg > 0:
            ge._knight_gain_stack(state, character, log, "deal_damage")
            if outcome >= 5:
                ge._knight_gain_stack(state, character, log, "deal_damage")
        # Oath of Vanguard: gain stack when striking before enemy acts
        if state.get("knight_oath") == "vanguard" and turn == 0:
            ge._knight_gain_stack(state, character, log, "strike_first")
        # Oath of Wrath 10-stack: all strikes apply bleeding
        if knight_mods.get("strikes_bleed") and outcome >= 3:
            ge._append_status_dedup(state, ge.make_status("bleeding"), key="monster_statuses")
            log.append({"kind": "knight_oath", "text": "Oath of Wrath — the hammer draws blood!"})

    # Extracted masteries modify outgoing damage here.
    # Fully-extracted masteries (Lancer) apply their riders through the hook
    # protocol. This dispatch was inside the moved region, so it now runs on the
    # context we were handed rather than on a spine local.
    from mastery_hooks import hooks_for
    ctx.outgoing = total_dmg
    ctx.outcome = outcome
    ctx.skill = sk
    for _h in hooks_for(character):
        _h.on_damage_computed(ctx)
    total_dmg = ctx.outgoing

    # Mage: Arcane Library passive damage modifiers
    if ge._is_mage(character) and total_dmg > 0:
        total_dmg = ge._mage_apply_passive_modifiers(state, character, sk, total_dmg, log)
        # Spatial: Point Blank close-range bonus + Expanding Radius concentration
        total_dmg = int(total_dmg * ge._mage_get_spatial_damage_mult(state, character))
        total_dmg = int(total_dmg * ge._mage_get_expanding_radius_bonus(character))
        total_dmg = int(total_dmg * ge._mage_get_overload_debuff_bonus(character, sk))
        ge._mage_queue_temporal_echo(state, character, sk, total_dmg, log)
        # Mana Vampire: restore MP equal to 10% of damage dealt
        if state.get("mage_mana_vampire_active"):
            mp_restore = int(total_dmg * 0.10)
            if mp_restore > 0:
                character["mp"] = min(character.get("max_mp", 0), character.get("mp", 0) + mp_restore)
                log.append({"kind": "mage_passive", "text": f"Mana Vampire — restored {mp_restore} MP!"})
            state["mage_mana_vampire_active"] = False

    # Assassin: shadow threshold damage bonuses and BURST
    if ge._is_assassin(character) and total_dmg > 0:
        # eclipse_burst: force BURST if at threshold, otherwise bonus damage proportional to shadows
        # `sk` is None on innate actions (a plain strike with no skill selected).
        if sk and sk.get("id") == "eclipse_burst":
            burst_mods = ge._assassin_check_burst(state, character, log)
            if burst_mods.get("burst_mult"):
                total_dmg = int(total_dmg * burst_mods["burst_mult"])
                if burst_mods.get("guaranteed_crit"):
                    outcome = max(5, outcome)
                log.append({"kind": "assassin_burst", "text": f"ECLIPSE BURST — {burst_mods['burst_mult']}x damage! Shadows consumed!"})
            else:
                # Bonus damage proportional to current shadow count
                shadows = state.get("assassin_shadows", 0)
                if character.get("level", 1) >= 100 and shadows < 50:
                    shadows = 50
                shadow_bonus = int(total_dmg * (shadows / 100.0))
                total_dmg += shadow_bonus
                total_dmg, outcome = ge._assassin_apply_threshold_bonuses(state, character, total_dmg, outcome)
                log.append({"kind": "assassin_burst", "text": f"Eclipse Burst — +{shadow_bonus} shadow damage ({shadows} shadows)!"})
        else:
            # Check for BURST
            burst_mods = ge._assassin_check_burst(state, character, log)
            if burst_mods.get("burst_mult"):
                total_dmg = int(total_dmg * burst_mods["burst_mult"])
                if burst_mods.get("guaranteed_crit"):
                    outcome = max(5, outcome)
                log.append({"kind": "assassin_burst", "text": f"BURST strikes — {burst_mods['burst_mult']}x damage!"})
            else:
                # Apply shadow threshold bonuses
                total_dmg, outcome = ge._assassin_apply_threshold_bonuses(state, character, total_dmg, outcome)

        # Shadow Convergence (level 80): 75+ shadows = all strikes apply shaken
        shadows = state.get("assassin_shadows", 0)
        if character.get("level", 1) >= 100 and shadows < 50:
            shadows = 50
        if character.get("level", 1) >= 80 and shadows >= 75 and outcome >= 3:
            ge._append_status_dedup(state, ge.make_status("shaken"), key="monster_statuses")

        # Generate shadows on critical hit
        if outcome >= 5:
            ge._assassin_gain_shadows(state, character, log, 5, "critical hit")

        # Eclipse Blade active: +2 shadows per hit
        if state.get("assassin_eclipse_blade_active"):
            blade_bonus = 4 if state.get("is_night") else 2
            ge._assassin_gain_shadows(state, character, log, blade_bonus, "Eclipse Blade")

    # Hunter: Spirit Guidance crit, communion effects, multi-hit
    if ge._is_hunter(character) and total_dmg > 0 and sk and sk.get("power_type") in ("strike", "trap", "spirit"):
        # Tracking Instinct communion: enemy can't evade
        if state.get("hunter_tracking_instinct_active"):
            outcome = max(4, outcome)  # can't be evaded = guaranteed hit
        # Hunter's Mark communion: all allies gain crit vs target
        if state.get("hunter_marked_target"):
            outcome = max(5, outcome)  # guaranteed crit vs marked target
            crit_mult = ge._hunter_get_crit_damage_mult(state, character)
            total_dmg = int(total_dmg * crit_mult)
            log.append({"kind": "hunter_mark_crit", "text": f"Spirit Mark crit — {total_dmg} damage!"})
        # Apply Spirit Bow (Alpha Command): true damage
        if state.get("hunter_spirit_bow_charges", 0) > 0:
            total_dmg = int(total_dmg * 1.5)  # true damage bonus
            state["hunter_spirit_bow_charges"] -= 1
            log.append({"kind": "hunter_spirit_bow", "text": "Spirit Bow — true damage!"})

        # Apply guaranteed crits (Eagle Eye, Hawk Vision, Ambush)
        if state.get("hunter_guaranteed_crits", 0) > 0:
            outcome = max(5, outcome)
            crit_mult = ge._hunter_get_crit_damage_mult(state, character)
            total_dmg = int(total_dmg * crit_mult)
            state["hunter_guaranteed_crits"] -= 1
            log.append({"kind": "hunter_guaranteed_crit", "text": f"Guaranteed crit — {total_dmg} damage! (x{crit_mult:.1f})"})
        else:
            # Spirit Guidance crit chance
            crit_chance = ge._hunter_get_crit_chance(state, character)
            import random as _rng
            if _rng.random() < crit_chance:
                outcome = max(5, outcome)
                crit_mult = ge._hunter_get_crit_damage_mult(state, character)
                total_dmg = int(total_dmg * crit_mult)
                log.append({"kind": "hunter_crit", "text": f"Spirit Guidance crit — {total_dmg} damage! (x{crit_mult:.1f})"})

        # Apply communion effects
        total_dmg, outcome = ge._hunter_apply_communion_effects(state, character, sk, log, total_dmg, outcome)

    # Hunter: Gain Spirit Guidance per hit (basic attacks and skills)
    if ge._is_hunter(character) and total_dmg > 0:
        if sk and sk.get("power_type") in ("strike", "trap", "spirit"):
            hits = ge._hunter_get_hit_count(state, character, sk)
            guidance_per_hit = 2 if (state.get("hunter_spirit_communion") and "spirit_guidance_gains_2_per_hit" in sk.get("spirit_communion", "")) else 1
        else:
            # Basic attack — 1 hit, 1 guidance
            hits = 1
            guidance_per_hit = 1
        for _h in range(hits):
            ge._hunter_gain_guidance(state, character, log, guidance_per_hit)

    # Rogue: Opportunist — bonus damage vs debuffed enemies
    if ge._is_rogue(character) and total_dmg > 0:
        opp_mult = ge._rogue_get_opportunist_bonus(state)
        if opp_mult > 1.0:
            total_dmg = int(total_dmg * opp_mult)
            log.append({"kind": "rogue_opportunist", "text": f"Opportunist — +{int((opp_mult - 1) * 100)}% damage vs debuffed enemy!"})

    # Druid: Pack Synergy — druid_stat_mult boosts player damage
    if ge._is_druid(character) and total_dmg > 0:
        synergy = state.get("druid_pack_synergy")
        if synergy and synergy.get("druid_stat_mult", 1.0) > 1.0:
            total_dmg = int(total_dmg * synergy["druid_stat_mult"])

    # Druid: Fusion attack rider — fused summon's attack skill adds bonus damage
    if ge._is_druid(character) and total_dmg > 0 and state.get("druid_fusion_active"):
        total_dmg = ge._druid_apply_fusion_attack_rider(state, character, log, total_dmg)

    # Druid: Fusion signature — fused summon's signature ability fires on cooldown
    if ge._is_druid(character) and state.get("druid_fusion_active"):
        sig_dmg = ge._druid_apply_fusion_signature(state, character, log)
        if sig_dmg > 0:
            total_dmg += sig_dmg

    ctx.outgoing = total_dmg
    ctx.outcome = outcome
