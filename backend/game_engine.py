"""Dice, action resolution, combat engine, crafting engine."""
from __future__ import annotations

import random
from datetime import datetime, timedelta, timezone
from typing import Any

from game_data import (
    BIOME_ACTIONS,
    ITEMS_BY_ID,
    RECIPES_BY_ID,
    SKILL_EXTRAS,
    SKILLS_BY_ID,
    apply_armor,
    apply_magic_resistance,
    compute_accuracy,
    compute_armor,
    compute_barrier,
    compute_evasion,
    compute_healing,
    compute_magic_resistance,
    compute_physical_damage,
    compute_magical_damage,
    compute_action_rating,
    compute_monster_threat,
    compute_skill_capacity,
    compute_status_duration_mult,
    get_monster,
)
from items import (
    compute_item_total_stats as _compute_item_total_stats,
    compute_item_bonus_effects as _compute_item_bonus_effects,
    SET_BONUSES as _SET_BONUSES,
    LEGENDARY_POWERS as _LEGENDARY_POWERS,
    generate_drop,
    generate_rune_drop,
)


def _get_equipped_item(character: dict, slot: str) -> dict | None:
    """Look up an equipped item by slot. Supports both old static item IDs
    and new procedural item instances (stored in character['item_instances'])."""
    equipped = character.get("equipped", {})
    item_ref = equipped.get(slot)
    if not item_ref:
        return None
    # Try static items first (old system)
    item = ITEMS_BY_ID.get(item_ref)
    if item and not item.get("base_id"):
        # Old-style static item — return as-is
        return item
    # Try item instances (new system)
    instances = character.get("item_instances", [])
    for inst in instances:
        if isinstance(inst, dict) and inst.get("instance_id") == item_ref:
            return inst
    # Fallback: return static item even if it has base_id (base item template)
    if item:
        return item
    return None


def _compute_weapon_damage(item: dict) -> int:
    """Compute weapon damage from an item. New items use total stats; old items use 'power'."""
    if item.get("base_id") or item.get("prefixes") or item.get("upgrades"):
        # New-style item instance — sum all total stats as weapon damage
        total_stats = _compute_item_total_stats(item)
        return sum(v for v in total_stats.values() if isinstance(v, (int, float)))
    if item.get("base_stats"):
        # New-style base item template — sum base_stats
        return sum(v for v in item["base_stats"].values() if isinstance(v, (int, float)))
    # Old-style item — use power field
    # No item in the game carries a scalar `power` any more — every item's
    # strength lives in its stats. Nothing left to fall back to.
    return 0


def _get_item_stats(item: dict) -> dict[str, int]:
    """Get total stats from an item (new or old format)."""
    if item.get("base_id") or item.get("prefixes") or item.get("upgrades"):
        return _compute_item_total_stats(item)
    # New-style base item template (has base_stats but no instance fields)
    if item.get("base_stats"):
        return dict(item["base_stats"])
    # Old-style item — use 'stats' field
    return dict(item.get("stats", {}))


def _get_item_bonus_effects(item: dict) -> list[dict]:
    """Get bonus effects from an item (new or old format)."""
    if item.get("base_id") or item.get("prefixes") or item.get("upgrades"):
        return _compute_item_bonus_effects(item)
    # Old-style items don't have bonus effects
    return []


def _apply_item_heal_amp(state: dict, heal_amount: int) -> int:
    """Apply heal_amp and skill_healing from item bonus effects to a heal amount."""
    ibe = state.get("item_bonus_effects", {})
    amp = ibe.get("heal_amp", 0)
    skill_heal = ibe.get("skill_healing", 0)
    total_amp = amp + skill_heal
    if total_amp > 0:
        return int(heal_amount * (1.0 + total_amp))
    return heal_amount


def _apply_item_magic_resist_pct(state: dict, damage: int) -> int:
    """Apply magic_resist_pct from item bonus effects to incoming magical damage."""
    pct = state.get("item_bonus_effects", {}).get("magic_resist_pct", 0)
    if pct > 0:
        return int(damage * (1.0 - pct))
    return damage


def _aggregate_item_bonus_effects(character: dict) -> dict:
    """Aggregate all bonus effects from equipped items and set bonuses into a single dict.
    Returns {effect_type: total_value} and {effect_type: [extra fields]} for complex effects."""
    from game_data import EQUIP_SLOTS
    equipped = character.get("equipped", {})
    seen_items = set()
    totals: dict[str, float] = {}
    extra_damage_list: list[dict] = []
    for slot in EQUIP_SLOTS:
        item_id = equipped.get(slot)
        if not item_id or item_id in seen_items:
            continue
        seen_items.add(item_id)
        item = _get_equipped_item(character, slot)
        if not item:
            item = ITEMS_BY_ID.get(item_id)
        if not item:
            continue
        for eff in _get_item_bonus_effects(item):
            etype = eff.get("type")
            if not etype:
                continue
            if etype == "extra_damage":
                extra_damage_list.append(eff)
            else:
                totals[etype] = totals.get(etype, 0) + eff.get("value", 0)

    # Set bonus bonus_effects
    set_bonuses = _check_set_bonuses(character)
    for set_id, count in set_bonuses.items():
        bonus = _SET_BONUSES.get(set_id, {}).get("bonuses", {}).get(count, {})
        for eff in bonus.get("bonus_effects", []):
            etype = eff.get("type")
            if not etype:
                continue
            if etype == "extra_damage":
                extra_damage_list.append(eff)
            else:
                totals[etype] = totals.get(etype, 0) + eff.get("value", 0)

    if extra_damage_list:
        totals["_extra_damage"] = extra_damage_list  # type: ignore
    return totals


def _aggregate_legendary_powers(character: dict) -> list[str]:
    """Collect all legendary power IDs from equipped items and 4-piece set bonuses."""
    from game_data import EQUIP_SLOTS
    equipped = character.get("equipped", {})
    seen_items = set()
    powers: list[str] = []
    for slot in EQUIP_SLOTS:
        item_id = equipped.get(slot)
        if not item_id or item_id in seen_items:
            continue
        seen_items.add(item_id)
        item = _get_equipped_item(character, slot)
        if not item:
            item = ITEMS_BY_ID.get(item_id)
        if not item:
            continue
        lp = item.get("legendary_power")
        if lp and lp in _LEGENDARY_POWERS:
            powers.append(lp)

    # 4-piece set bonuses can grant legendary powers
    set_bonuses = _check_set_bonuses(character)
    for set_id, count in set_bonuses.items():
        bonus = _SET_BONUSES.get(set_id, {}).get("bonuses", {}).get(count, {})
        lp = bonus.get("legendary_power")
        if lp and lp in _LEGENDARY_POWERS and lp not in powers:
            powers.append(lp)

    return powers


def _apply_item_bonus_effects_to_damage(state: dict, character: dict, log: list,
                                        total_dmg: int, outcome: int, damage_type: str) -> int:
    """Apply item bonus effects that modify player damage. Returns new total_dmg."""
    ibe = state.get("item_bonus_effects", {})
    if not ibe:
        return total_dmg

    # crit_chance: chance to upgrade outcome to crit
    crit_chance = ibe.get("crit_chance", 0)
    if crit_chance > 0 and outcome < 5 and total_dmg > 0:
        if random.random() < crit_chance:
            outcome = 5
            total_dmg = int(total_dmg * 1.6)
            log.append({"kind": "item_crit", "text": f"Item crit chance — critical hit! {total_dmg} damage!"})

    # crit_damage: bonus multiplier on crits
    crit_dmg = ibe.get("crit_damage", 0)
    if crit_dmg > 0 and outcome >= 5 and total_dmg > 0:
        bonus = int(total_dmg * crit_dmg)
        total_dmg += bonus
        if bonus > 0:
            log.append({"kind": "item_crit_dmg", "text": f"Item crit damage — +{bonus} damage!"})

    # magical_amp: boost magical/holy damage
    magic_amp = ibe.get("magical_amp", 0)
    if magic_amp > 0 and damage_type in ("magical", "holy") and total_dmg > 0:
        bonus = int(total_dmg * magic_amp)
        total_dmg += bonus
        if bonus > 0:
            log.append({"kind": "item_magic_amp", "text": f"Magical amplification — +{bonus} damage!"})

    # physical_amp: boost physical damage
    phys_amp = ibe.get("physical_amp", 0)
    if phys_amp > 0 and damage_type == "physical" and total_dmg > 0:
        bonus = int(total_dmg * phys_amp)
        total_dmg += bonus
        if bonus > 0:
            log.append({"kind": "item_phys_amp", "text": f"Physical amplification — +{bonus} damage!"})

    # magic_pen: bypass magic resistance (flat bonus to magical damage)
    magic_pen = ibe.get("magic_pen", 0)
    if magic_pen > 0 and damage_type in ("magical", "holy") and total_dmg > 0:
        bonus = int(total_dmg * magic_pen)
        total_dmg += bonus
        if bonus > 0:
            log.append({"kind": "item_magic_pen", "text": f"Magic penetration — +{bonus} damage!"})

    # armor_pen: reduce enemy armor effect (flat bonus damage)
    armor_pen = ibe.get("armor_pen", 0)
    if armor_pen > 0 and damage_type == "physical" and total_dmg > 0:
        bonus = int(total_dmg * armor_pen)
        total_dmg += bonus
        if bonus > 0:
            log.append({"kind": "item_armor_pen", "text": f"Armor penetration — +{bonus} damage!"})

    # extra_damage: add bonus elemental damage, boosted by elemental amps
    extra_dmg_list = ibe.get("_extra_damage", [])
    if isinstance(extra_dmg_list, list):
        for ed in extra_dmg_list:
            ed_val = ed.get("value", 0)
            if ed_val > 0:
                element = ed.get("element", "")
                # Elemental amps boost matching extra_damage
                elem_amp_key = f"{element}_amp" if element else None
                elem_amp = ibe.get(elem_amp_key, 0) if elem_amp_key else 0
                if elem_amp > 0:
                    ed_val = int(ed_val * (1.0 + elem_amp))
                total_dmg += ed_val
                log.append({"kind": "item_extra_damage", "text": f"+{ed_val} {element or 'bonus'} damage!"})

    # lifesteal: heal player after damage
    lifesteal = ibe.get("lifesteal", 0)
    if lifesteal > 0 and total_dmg > 0:
        heal = int(total_dmg * lifesteal)
        if heal > 0:
            character["hp"] = min(character.get("max_hp", 999), character.get("hp", 0) + heal)
            log.append({"kind": "item_lifesteal", "text": f"Lifesteal — healed {heal} HP!"})

    # action_speed: chance for bonus damage from extra action
    action_speed = ibe.get("action_speed", 0)
    if action_speed > 0 and total_dmg > 0:
        if random.random() < action_speed:
            bonus = int(total_dmg * 0.5)
            total_dmg += bonus
            if bonus > 0:
                log.append({"kind": "item_action_speed", "text": f"Action speed — extra strike for +{bonus} damage!"})

    return total_dmg


def _apply_legendary_powers_on_strike(state: dict, character: dict, log: list,
                                      total_dmg: int, outcome: int,
                                      damage_type: str = "physical") -> int:
    """Apply on_strike legendary powers. Returns new total_dmg."""
    powers = state.get("legendary_powers", [])
    if not powers:
        return total_dmg

    for lp_id in powers:
        lp = _LEGENDARY_POWERS.get(lp_id)
        if not lp:
            continue
        eff = lp.get("effect", {})
        etype = eff.get("type")

        # Passive lifesteal (Blood Pact) — fires on every strike
        if lp.get("trigger") == "passive" and etype == "lifesteal":
            if total_dmg > 0:
                heal = int(total_dmg * eff.get("value", 0.15))
                if heal > 0:
                    character["hp"] = min(character.get("max_hp", 999), character.get("hp", 0) + heal)
                    log.append({"kind": "legendary_power", "text": f"{lp['name']} — lifesteal healed {heal} HP!"})
            continue

        # Passive free_cast_above (Arcane Surge) — repurposed as magical damage bonus
        if lp.get("trigger") == "passive" and etype == "free_cast_above":
            if total_dmg > 0 and damage_type in ("magical", "holy"):
                resource = eff.get("resource", "mp")
                threshold = eff.get("threshold", 0.80)
                if resource == "mp":
                    max_mp = character.get("max_mp", 0)
                    cur_mp = character.get("mp", 0)
                    if max_mp > 0 and cur_mp / max_mp >= threshold:
                        bonus = int(total_dmg * 0.15)
                        total_dmg += bonus
                        log.append({"kind": "legendary_power", "text": f"{lp['name']} — arcane surge! +{bonus} magical damage!"})
            continue

        if lp.get("trigger") != "on_strike":
            continue

        if etype == "every_nth_strike":
            n = eff.get("n", 3)
            counter = state.setdefault("lp_strike_counter", {}).get(lp_id, 0) + 1
            state["lp_strike_counter"][lp_id] = counter
            if counter >= n:
                state["lp_strike_counter"][lp_id] = 0
                bonus = int(total_dmg * (eff.get("damage_mult", 1.5) - 1.0))
                total_dmg += bonus
                status = eff.get("status")
                if status:
                    _append_status_dedup(state, make_status(status), key="monster_statuses")
                elem = eff.get("element", "")
                log.append({"kind": "legendary_power", "text": f"{lp['name']} — every {n}rd strike! +{bonus} {elem} damage!"})

        elif etype == "chain":
            # In 1v1, chain damage is bonus damage
            bonus = int(total_dmg * eff.get("damage_mult", 0.5))
            total_dmg += bonus
            log.append({"kind": "legendary_power", "text": f"{lp['name']} — chains for +{bonus} damage!"})

        elif etype == "chance_status":
            if random.random() < eff.get("chance", 0.20):
                status = eff.get("status", "frozen")
                _append_status_dedup(state, make_status(status), key="monster_statuses")
                log.append({"kind": "legendary_power", "text": f"{lp['name']} — {status} applied!"})

        elif etype == "execute":
            monster_hp = state.get("monster_hp", 0)
            monster_max = state.get("monster_max_hp", 1)
            if monster_max > 0 and monster_hp / monster_max < eff.get("threshold", 0.20):
                total_dmg = int(total_dmg * eff.get("damage_mult", 2.0))
                log.append({"kind": "legendary_power", "text": f"{lp['name']} — EXECUTE! Double damage!"})

    return total_dmg


def _apply_legendary_powers_passive(state: dict, character: dict, log: list) -> None:
    """Apply passive legendary powers at combat start and per-turn."""
    powers = state.get("legendary_powers", [])
    if not powers:
        return

    for lp_id in powers:
        lp = _LEGENDARY_POWERS.get(lp_id)
        if not lp or lp.get("trigger") != "passive":
            continue
        eff = lp.get("effect", {})
        etype = eff.get("type")

        if etype == "scaling_stat":
            # e.g. Berserker Rage: +1 Might per 10% missing HP
            stat = eff.get("stat", "might")
            max_hp = character.get("max_hp", 1)
            cur_hp = character.get("hp", max_hp)
            missing_pct = (max_hp - cur_hp) / max_hp * 100
            per_pct = eff.get("per_missing_hp_pct", 10)
            bonus = int(missing_pct / per_pct) * eff.get("value", 1)
            # Remove previous bonus before applying new (prevents stacking)
            prev_key = f"lp_{lp_id}_{stat}_bonus"
            prev_bonus = state.get(prev_key, 0)
            if prev_bonus > 0:
                character["stats"][stat] = character["stats"].get(stat, 0) - prev_bonus
            # Apply new bonus
            if bonus > 0:
                character["stats"][stat] = character["stats"].get(stat, 0) + bonus
                log.append({"kind": "legendary_power", "text": f"{lp['name']} — +{bonus} {stat} from rage!"})
            state[prev_key] = bonus

        elif etype == "lifesteal":
            # Blood Pact: lifesteal handled in damage, but downside is per-turn self damage
            downside = eff.get("downside", {})
            if downside.get("type") == "self_damage_pct":
                dmg = int(character.get("max_hp", 1) * downside.get("value", 0.05))
                character["hp"] = max(1, character.get("hp", 0) - dmg)
                log.append({"kind": "legendary_power", "text": f"{lp['name']} — blood price: -{dmg} HP!"})

        elif etype == "free_cast_above":
            # Arcane Surge: no MP cost on skills — but player skills don't cost MP.
            # Repurposed: +15% magical damage when above MP threshold.
            # Applied in on_strike handler.
            pass

        elif etype == "range_bonus":
            # Gravity Well: applied after range init at turn 0 — skip here
            pass

        elif etype == "revive":
            # Phoenix Rebirth: handled on death
            pass


def _apply_legendary_powers_when_hit(state: dict, character: dict, log: list, damage: int) -> int:
    """Apply when_hit legendary powers. Returns damage after modifications."""
    powers = state.get("legendary_powers", [])
    if not powers:
        return damage

    for lp_id in powers:
        lp = _LEGENDARY_POWERS.get(lp_id)
        if not lp or lp.get("trigger") != "when_hit":
            continue
        eff = lp.get("effect", {})
        etype = eff.get("type")

        if etype == "full_block_below":
            hp_ratio = character.get("hp", 0) / max(1, character.get("max_hp", 1))
            if hp_ratio < eff.get("hp_threshold", 0.30):
                log.append({"kind": "legendary_power", "text": f"{lp['name']} — full block! No damage!"})
                return 0

        elif etype == "chance_decoy":
            if random.random() < eff.get("chance", 0.10):
                log.append({"kind": "legendary_power", "text": f"{lp['name']} — decoy absorbs the hit!"})
                return 0

    return damage


def _get_item_weapon_type(item: dict) -> str | None:
    """Get weapon_type from an item (new or old format)."""
    if item.get("weapon_type"):
        return item["weapon_type"]
    # Map old item IDs to weapon types
    old_id = item.get("id", "")
    _OLD_WEAPON_TYPE_MAP = {
        "iron_dagger": "dagger", "serpent_fang_dagger": "dagger",
        "iron_longsword": "sword_1h", "knights_bastard_sword": "sword_1h", "crescent_blade": "sword_1h",
        "iron_greatsword": "sword_2h",
        "wolfbone_axe": "axe_1h",
        "bronze_mace": "hammer_1h",
        "oak_shortbow": "bow", "ashwood_longbow": "bow",
        "riverstone_staff": "tome", "war_staff": "tome",
        "gloomreaper_scythe": "scythe",
        "bone_shield": "shield", "iron_kite_shield": "shield",
    }
    return _OLD_WEAPON_TYPE_MAP.get(old_id)


def _check_weapon_req(character: dict, weapon_req: str) -> bool:
    """Check if the character's equipped weapon satisfies the skill's weapon_req.
    Returns True if weapon_req is 'none' or if any equipped weapon matches."""
    if not weapon_req or weapon_req == "none":
        return True
    from game_data import WEAPON_REQ_MAP
    allowed_types = WEAPON_REQ_MAP.get(weapon_req, [])
    if not allowed_types:
        return True  # unknown weapon_req = allow
    equipped = character.get("equipped", {})
    for hand in ("left_hand", "right_hand"):
        item_ref = equipped.get(hand)
        if not item_ref:
            continue
        item = _get_equipped_item(character, hand)
        if not item:
            item = ITEMS_BY_ID.get(item_ref)
        if not item:
            continue
        wtype = _get_item_weapon_type(item)
        if wtype and wtype in allowed_types:
            return True
    return False


def _check_set_bonuses(character: dict) -> dict:
    """Check active set bonuses from equipped items.
    Returns {'set_id': count, ...} for sets with 2+ pieces equipped."""
    equipped = character.get("equipped", {})
    instances = character.get("item_instances", [])
    set_counts: dict[str, int] = {}
    seen_instances = set()
    for slot in equipped:
        ref = equipped.get(slot)
        if not ref:
            continue
        # Find the item (instance or static)
        item = None
        for inst in instances:
            if isinstance(inst, dict) and inst.get("instance_id") == ref:
                item = inst
                break
        if not item:
            item = ITEMS_BY_ID.get(ref)
        if not item:
            continue
        set_id = item.get("set_id")
        if set_id and set_id in _SET_BONUSES:
            set_counts[set_id] = set_counts.get(set_id, 0) + 1
    return {sid: c for sid, c in set_counts.items() if c >= 2}
from regional_resources import (
    CRIT_QUANTITY_BONUS,
    NODE_COOLDOWN_SECONDS,
    RANK_ORDER,
    TOOL_DURABILITY_COST,
    has_profession_for_node,
    nodes_for_biome,
    pick_resource_node,
    seconds_until_node_ready,
)
from world_data import xp_multiplier_for, continental_bonus_for
from heritage_system import is_heritage_month_for, get_heritage_bonuses
from professions import PROFESSIONS_BY_ID, gain_profession_xp, has_profession_rank
from narratives import pick_narrative
from racial import racial_combat_mods, tick_racial_on_combat_win, current_time_of_day

# Biome theme → monster category mapping for continental bonuses
_BIOME_THEME_MAP = {
    "demonfall_crater": "demon",
    "iron_scar": "demon",
    "ash_barrens": "demon",
    "ancient_den": "beast",
    "beastwood": "beast",
    "roaring_savanna": "beast",
    "bloodwind_plains": "beast",
}

def _monster_category(monster: dict) -> str | None:
    """Infer monster category from biome theme for continental bonus checks."""
    tags = monster.get("tags", [])
    if tags:
        return tags[0]
    biome = monster.get("biome", "")
    return _BIOME_THEME_MAP.get(biome)


def _continental_heal_mult(character: dict) -> float:
    """Haya healing_quality continental bonus."""
    bonus = continental_bonus_for(character.get("current_continent", ""), "healing_quality")
    if bonus:
        return float(bonus)
    return 1.0


# ============================================================
# DICE — power-delta weighted d6
# ============================================================
# Base weights by delta bucket (roll 1..6)
DELTA_WEIGHTS: list[tuple[int, list[int]]] = [
    (-15, [45, 32, 15, 5, 2, 1]),
    (-10, [32, 28, 20, 10, 6, 4]),
    (-5,  [20, 25, 25, 15, 10, 5]),
    (0,   [10, 15, 20, 25, 20, 10]),
    (5,   [5,  10, 15, 25, 25, 20]),
    (10,  [3,  7,  12, 20, 30, 28]),
    (15,  [1,  2,  5,  15, 32, 45]),
]


def _weights_for_delta(delta: int, luck_shift: int = 0) -> list[int]:
    # Clamp delta into buckets
    if delta <= -15:
        base = DELTA_WEIGHTS[0][1]
    elif delta >= 15:
        base = DELTA_WEIGHTS[-1][1]
    else:
        # find closest bucket
        idx = 3
        for i, (thr, _) in enumerate(DELTA_WEIGHTS):
            if delta <= thr:
                idx = i
                break
        base = DELTA_WEIGHTS[idx][1]
    if luck_shift <= 0:
        return list(base)
    # shift probability mass upward
    w = list(base)
    for _ in range(luck_shift):
        if w[0] > 0:
            w[0] = max(0, w[0] - 3)
            w[-1] += 3
    return w


def roll_dice(player_power: int, target_power: int, luck: int = 0) -> dict:
    delta = player_power - target_power
    luck_shift = max(0, luck // 5)
    weights = _weights_for_delta(delta, luck_shift)
    outcome = random.choices([1, 2, 3, 4, 5, 6], weights=weights, k=1)[0]
    return {"outcome": outcome, "delta": delta, "weights": weights}


# ============================================================
# GRACE-BASED ACCURACY vs EVASION DICE
# ============================================================
# Advantage levels based on (accuracy - evasion) difference:
#   diff 0-2:  Neutral
#   diff 3-5:  Accuracy Advantage I
#   diff 6-9:  Accuracy Advantage II
#   diff 10+:  Accuracy Advantage III
#   diff -3 to -5: Evasion Advantage I
#   diff -6 to -9: Evasion Advantage II
#   diff -10+:     Evasion Advantage III
ADVANTAGE_WEIGHTS: dict[str, list[int]] = {
    "neutral":          [10, 15, 20, 25, 20, 10],
    "acc_adv_1":        [6,  10, 14, 26, 24, 20],
    "acc_adv_2":        [3,  6,  10, 22, 28, 31],
    "acc_adv_3":        [1,  3,  6,  16, 34, 40],
    "evas_adv_1":       [20, 24, 26, 14, 10, 6],
    "evas_adv_2":       [31, 28, 22, 10, 6,  3],
    "evas_adv_3":       [40, 34, 16, 6,  3,  1],
}


def _advantage_level(diff: int) -> str:
    if diff >= 10:
        return "acc_adv_3"
    elif diff >= 6:
        return "acc_adv_2"
    elif diff >= 3:
        return "acc_adv_1"
    elif diff <= -10:
        return "evas_adv_3"
    elif diff <= -6:
        return "evas_adv_2"
    elif diff <= -3:
        return "evas_adv_1"
    else:
        return "neutral"


def roll_accuracy_evasion(accuracy: int, evasion: int) -> dict:
    """Roll d6 weighted by accuracy vs evasion advantage level."""
    diff = accuracy - evasion
    level = _advantage_level(diff)
    weights = ADVANTAGE_WEIGHTS[level]
    outcome = random.choices([1, 2, 3, 4, 5, 6], weights=weights, k=1)[0]
    return {"outcome": outcome, "diff": diff, "advantage": level}


# ============================================================
# ACTION RESOLUTION (non-combat: hunt/gather/explore/fish/loot_ruins)
# ============================================================
STATUS_TEMPLATES: dict[str, dict] = {
    "bleeding":  {"name": "Bleeding",  "kind": "debuff", "duration": 3, "magnitude": 2, "dot_type": "physical"},
    "poisoned":  {"name": "Poisoned",  "kind": "debuff", "duration": 4, "magnitude": 3, "dot_type": "magical"},
    "weary":     {"name": "Weary",     "kind": "debuff", "duration": 2, "magnitude": 0},
    "sick":      {"name": "Sick",      "kind": "debuff", "duration": 5, "magnitude": 1},
    "cursed":    {"name": "Cursed",    "kind": "debuff", "duration": 6, "magnitude": 2, "dot_type": "magical"},
    # Applied by high-tier monster rage skills ("Demonic Fury", "Primal Fury") when
    # they drop to low HP. It had no template, so make_status fell through to the
    # generic default and produced a *debuff* — the enrage did nothing for the
    # monster, and anything counting debuffs on the target (e.g. the Mage's
    # Delirium) treated the monster's own rage as a weakness to exploit.
    "bloodrage":  {"name": "Bloodrage",  "kind": "buff",   "duration": 3, "magnitude": 3},
    "blessed":   {"name": "Blessed",   "kind": "buff",   "duration": 4, "magnitude": 2},
    "focused":   {"name": "Focused",   "kind": "buff",   "duration": 3, "magnitude": 2},
    "burning":   {"name": "Burning",   "kind": "debuff", "duration": 3, "magnitude": 3, "dot_type": "magical"},
    "stunned":   {"name": "Stunned",   "kind": "debuff", "duration": 1, "magnitude": 0},
    "shaken":    {"name": "Shaken",    "kind": "debuff", "duration": 2, "magnitude": 1},
    "blinded":   {"name": "Blinded",   "kind": "debuff", "duration": 2, "magnitude": 1},
    "ensnared":  {"name": "Ensnared",  "kind": "debuff", "duration": 2, "magnitude": 0},
    "warded":    {"name": "Warded",    "kind": "buff",   "duration": 3, "magnitude": 2},
    "hidden":    {"name": "Hidden",    "kind": "buff",   "duration": 2, "magnitude": 0},
    "evasive":   {"name": "Evasive",   "kind": "buff",   "duration": 2, "magnitude": 2},
    "recovering": {"name": "Recovering", "kind": "debuff", "duration": 3, "magnitude": 0},
    "sanctuary_blessing": {"name": "Sanctuary Blessing", "kind": "buff", "duration": 10, "magnitude": 0},
    "inspired":  {"name": "Inspired",   "kind": "buff",   "duration": 3, "magnitude": 2},
    "mesmerized": {"name": "Mesmerized", "kind": "debuff", "duration": 2, "magnitude": 0},
    "silenced":   {"name": "Silenced",   "kind": "debuff", "duration": 2, "magnitude": 0},
    "confused":   {"name": "Confused",   "kind": "debuff", "duration": 2, "magnitude": 0},
    "blind":      {"name": "Blind",      "kind": "debuff", "duration": 2, "magnitude": 0},
    "bind":       {"name": "Bound",      "kind": "debuff", "duration": 2, "magnitude": 0},
}


def make_status(status_id: str) -> dict:
    tpl = STATUS_TEMPLATES.get(status_id, {"name": status_id.title(), "kind": "debuff", "duration": 2, "magnitude": 1})
    return {"id": status_id, **tpl}
def _has_player_status(character: dict, state: dict, status_id: str) -> bool:
    """Check if player has a status in either character statuses or state player_statuses."""
    if any(s.get("id") == status_id for s in character.get("statuses", [])):
        return True
    if any(s.get("id") == status_id for s in state.get("player_statuses", [])):
        return True
    return False


def _tick_dots(target: dict, statuses_key: str, defender: dict | None, log: list[dict], label: str, hp_key: str = "hp") -> None:
    """Process damage-over-time effects on a target. defender is the character dict for armor/MR."""
    armor = compute_armor(defender) if defender else 0
    mr = compute_magic_resistance(defender) if defender else 0
    for s in target.get(statuses_key, []):
        dot_type = s.get("dot_type")
        if dot_type and s.get("duration", 0) > 0:
            mag = s.get("magnitude", 0)
            if dot_type == "physical":
                # Bleed uses 50% of armor
                dmg = apply_armor(mag, armor // 2)
            elif dot_type == "magical":
                dmg = apply_magic_resistance(mag, mr)
            else:
                dmg = mag  # true damage DoT
            current_hp = target.get(hp_key, 0)
            target[hp_key] = max(0, current_hp - dmg)
            log.append({"kind": "dot", "text": f"{label} suffers {dmg} {dot_type} damage from {s['name']}.", "damage": dmg, "dot_type": dot_type})
        # decrement duration
        s["duration"] = max(0, int(s.get("duration", 0)) - 1)
    # remove expired
    target[statuses_key] = [s for s in target.get(statuses_key, []) if s.get("duration", 0) > 0]


def _clamp_and_sync_combat_hp(character: dict, state: dict, log: list[dict] | None = None) -> None:
    """Clamp player hp to [0, max_hp] and mirror it into combat state."""
    character["hp"] = max(0, min(character.get("max_hp", character["hp"]), character["hp"]))
    state["player_hp"] = character["hp"]
    state["player_max_hp"] = character["max_hp"]
    # Paladin: update faith scaling whenever HP changes are synced
    if _is_paladin(character):
        _paladin_update_scaling(state, character, log if log is not None else [])


def apply_self_stat_mods(state: dict, character: dict, mods: dict, duration: int,
                         key: str, log: list, log_kind: str, label: str) -> None:
    """Bank a self stat_mod bucket entry and apply it to the character now.

    Seven near-identical copies of this lived inside `combat_turn`, one per
    mastery, differing only in the state key and the log wording. Paired with
    `tick_stat_mods` for expiry.
    """
    mods = dict(mods)
    state.setdefault(key, []).append({"mods": mods, "duration": duration})
    for stat, val in mods.items():
        character["stats"][stat] = character["stats"].get(stat, 0) + val
    if log_kind:
        log.append({
            "kind": log_kind,
            "text": f"{label}{', '.join(f'{k} {v:+d}' for k, v in mods.items())} "
                    f"for {duration} turns.",
        })


def apply_enemy_stat_mods(state: dict, mods: dict, duration: int, key: str,
                          log: list | None = None, log_kind: str = "",
                          label: str = "", apply_now: bool = False) -> None:
    """Bank an enemy stat_mod bucket entry.

    `apply_now` mirrors the originals: some masteries applied the modifier to
    `monster_stats` immediately, others only banked it for the tick to handle.
    """
    mods = dict(mods)
    state.setdefault(key, []).append({"mods": mods, "duration": duration})
    if apply_now:
        m_stats = state.setdefault("monster_stats", {})
        for stat, val in mods.items():
            m_stats[stat] = m_stats.get(stat, 0) + val
    if log is not None and log_kind:
        log.append({
            "kind": log_kind,
            "text": f"{label}{', '.join(f'{k} {v:+d}' for k, v in mods.items())} "
                    f"to enemy for {duration} turns.",
        })


def tick_stat_mods(state: dict, key: str, target_stats: dict) -> None:
    """Expire one bucket of temporary stat modifiers, refunding what they granted.

    Every mastery kept its own bucket (`knight_self_stat_mods`,
    `paladin_enemy_stat_mods`, ...) and `combat_turn` carried **21 copies of this
    same loop** across 19 buckets — the single largest block of duplication in the
    function, and a standing invitation for one copy to drift from the rest.

    Semantics are preserved exactly: an entry with `duration > 0` survives this
    turn and is decremented afterwards; an entry at 0 is removed and its stats are
    subtracted. That ordering means a mod lasts one turn longer than its literal
    duration, which is what every existing copy did.
    """
    entries = state.get(key) or []
    if not entries:
        return
    surviving = []
    for entry in entries:
        if entry.get("duration", 0) > 0:
            surviving.append(entry)
        else:
            for stat, val in (entry.get("mods") or {}).items():
                target_stats[stat] = target_stats.get(stat, 0) - val
    state[key] = surviving
    for entry in surviving:
        entry["duration"] -= 1


def _append_status_dedup(char_or_state: dict, status: dict, key: str = "statuses") -> None:
    """Add or refresh a status without duplicates."""
    lst = char_or_state.setdefault(key, [])
    for s in lst:
        if s.get("id") == status.get("id"):
            s["duration"] = max(int(s.get("duration", 0)), int(status.get("duration", 0)))
            return
    lst.append(status)


def _resolve_gather_node(character: dict, action_id: str, biome_id: str, target_id: str | None) -> dict | None:
    """Pick and validate a resource node for gather/fish.
    Returns node dict on success, or a dict with 'error' key if blocked."""
    from regional_resources import (
        get_profession_tool,
        has_profession_for_node,
        node_on_cooldown,
        nodes_for_biome,
        pick_resource_node,
        seconds_until_node_ready,
    )
    from professions import PROFESSIONS_BY_ID

    node = pick_resource_node(character, biome_id, action_id, target_id)
    if not node:
        # No matching node found — determine which tool the player lacks
        if action_id == "fish":
            tool_name = PROFESSIONS_BY_ID.get("fishing", {}).get("tool", {}).get("name", "Fishing Rod")
        else:
            tool_name = "a gathering tool"
        return {"error": f"You need {tool_name} to {action_id} here."}

    # On cooldown? Still allow but with cooldown notice.
    if node_on_cooldown(character, node["id"]):
        secs = seconds_until_node_ready(character, node["id"])
        return {"id": f"scavenge_{node['item_id']}", "name": f"{node['name']} (cooldown {secs}s)",
                "item_id": node["item_id"], "profession": None, "min_rank": node["min_rank"],
                "rarity": node["rarity"], "scavenge": True, "cooldown_secs": secs}

    # Profession check — blocked without the profession
    has, reason = has_profession_for_node(character, node)
    if not has:
        return {"error": f"You need {reason} to gather from {node['name']}."}

    # Check tool exists and is not broken
    tool = get_profession_tool(character, node["profession"])
    prof_meta = PROFESSIONS_BY_ID.get(node["profession"], {})
    tool_name = prof_meta.get("tool", {}).get("name", "a tool")
    if not tool:
        return {"error": f"You need a {tool_name} to gather from {node['name']}. Buy one in town."}
    if int(tool.get("durability", 0)) <= 0:
        return {"error": f"Your {tool_name} is broken! Repair it in town to gather from {node['name']}."}
    return node


def resolve_action(character: dict, action_id: str, biome_id: str, target_id: str | None) -> dict:
    """Resolve a non-combat action node. Returns dict with outcome, narrative, rewards, hp_delta, status, node info."""
    action_meta = next((a for a in BIOME_ACTIONS.get(biome_id, []) if a["id"] == action_id), None)
    supported = {"explore", "hunt", "gather", "fish", "loot_ruins"}
    if not action_meta and action_id not in supported:
        return {"error": f"Action '{action_id}' not available in biome '{biome_id}'"}

    # Pick a target if not specified and static targets exist
    if not target_id and action_meta and action_meta.get("targets"):
        target_id = random.choice(action_meta["targets"])

    # Resource node resolution for gather/fish
    node: dict | None = None
    if action_id in ("gather", "fish"):
        node = _resolve_gather_node(character, action_id, biome_id, target_id)
        if node and "error" in node:
            return {"error": node["error"]}
        target_id = node.get("item_id") if node else target_id

    # Hunt requires a hunting tool (Hunter's Kit)
    if action_id == "hunt":
        from regional_resources import get_profession_tool
        from professions import PROFESSIONS_BY_ID
        hunt_tool = get_profession_tool(character, "hunting")
        tool_name = PROFESSIONS_BY_ID.get("hunting", {}).get("tool", {}).get("name", "Hunter's Kit")
        if not hunt_tool:
            return {"error": f"You need a {tool_name} to hunt. Buy one in town."}
        if int(hunt_tool.get("durability", 0)) <= 0:
            return {"error": f"Your {tool_name} is broken! Repair it in town to hunt."}

    player_pow = compute_action_rating(character)
    if action_id == "hunt":
        monster = get_monster(target_id) if target_id else None
        target_pow = compute_monster_threat(monster, character.get("level", 1)) if monster else 5
        target_name = monster["name"] if monster else "quarry"
    elif action_id in ("gather", "fish"):
        target_pow = 4
        target_name = node.get("name", "resource") if node else (ITEMS_BY_ID.get(target_id or "", {}).get("name") or "resource")
    elif action_id == "explore":
        target_pow = 5
        target_name = biome_id
    elif action_id == "loot_ruins":
        target_pow = 8
        target_name = "the ruins"
    else:
        target_pow = 5
        target_name = target_id or "unknown"

    dice = roll_dice(player_pow, target_pow, luck=character.get("stats", {}).get("cognition", 0))
    outcome = dice["outcome"]

    biome_name = biome_id.replace("_", " ")

    # Narrative
    key_map = {"hunt": "hunt", "gather": "gather", "explore": "explore",
               "fish": "fish", "loot_ruins": "loot_ruins"}
    narrative_key = key_map.get(action_id, "explore")

    # substitution
    subs: dict[str, str] = {
        "char": character.get("name", "the traveler"),
        "target": target_name,
        "material": target_name,
        "biome": biome_name,
    }
    narrative = pick_narrative(narrative_key, outcome, **subs)

    # Rewards
    rewards: dict[str, Any] = {"gold": 0, "xp": 0, "items": []}
    hp_delta = 0
    status_applied: str | None = None
    monster_slain = None

    if outcome == 1:  # crit fail
        hp_delta = -random.randint(8, 18)
        # Crit fail on gather/fish: extra tool damage and possible node destruction
        if action_id in ("gather", "fish") and node and not node.get("scavenge"):
            _consume_tool_and_cooldown(character, action_id, node, outcome)
    elif outcome == 2:  # fail + status
        hp_delta = -random.randint(2, 6)
        # apply a random bad status
        status_applied = random.choice(["bleeding", "poisoned", "weary", "sick"])
        if action_id in ("gather", "fish") and node and not node.get("scavenge"):
            _consume_tool_and_cooldown(character, action_id, node, outcome)
    elif outcome == 3:  # fail
        hp_delta = 0
    elif outcome == 4:  # success + bad
        hp_delta = -random.randint(1, 4)
        status_applied = random.choice(["bleeding", "weary"])
        _apply_action_rewards(action_id, target_id, rewards, tier="normal", outcome=outcome, character=character, biome_id=biome_id, node=node, monster=get_monster(target_id) if action_id == "hunt" else None)
        if action_id == "hunt":
            monster_slain = target_id
    elif outcome == 5:  # success
        _apply_action_rewards(action_id, target_id, rewards, tier="normal", outcome=outcome, character=character, biome_id=biome_id, node=node, monster=get_monster(target_id) if action_id == "hunt" else None)
        if action_id == "hunt":
            monster_slain = target_id
    elif outcome == 6:  # crit success
        _apply_action_rewards(action_id, target_id, rewards, tier="critical", outcome=outcome, character=character, biome_id=biome_id, node=node, monster=get_monster(target_id) if action_id == "hunt" else None)
        if action_id == "hunt":
            monster_slain = target_id

    result = {
        "outcome": outcome,
        "narrative": narrative,
        "rewards": rewards,
        "hp_delta": hp_delta,
        "status_applied": status_applied,
        "target_id": target_id,
        "target_name": target_name,
        "monster_slain": monster_slain,
        "dice_debug": {"player_pow": player_pow, "target_pow": target_pow, "delta": dice["delta"]},
    }
    if node:
        result["node"] = {
            "id": node.get("id"),
            "name": node.get("name"),
            "item_id": node.get("item_id"),
            "profession": node.get("profession"),
            "rarity": node.get("rarity"),
            "scavenge": node.get("scavenge", False),
            "cooldown_secs": node.get("cooldown_secs") if node.get("cooldown_secs") else NODE_COOLDOWN_SECONDS.get(node.get("rarity", "common"), 30),
        }
        if node.get("profession_missing"):
            result["node"]["profession_missing"] = node["profession_missing"]
        if node.get("no_tool"):
            result["node"]["no_tool"] = node["no_tool"]
    return result


def _consume_tool_and_cooldown(character: dict, action_id: str, node: dict, outcome: int) -> dict:
    """Consume tool durability and set node cooldown. Returns summary for the result log."""
    from regional_resources import consume_tool_durability, set_node_cooldown
    summary = {"tool_used": False, "tool_broken": False, "cooldown_set": False}
    if not node or node.get("scavenge") or not node.get("profession"):
        return summary
    rarity = node.get("rarity", "common")
    cost = TOOL_DURABILITY_COST.get(rarity, 1)
    if outcome == 1:  # crit fail doubles tool damage
        cost *= 2
    elif outcome == 5:  # success with benefit halves tool damage
        cost = max(1, cost // 2)
    remaining, broken = consume_tool_durability(character, node["profession"], cost)
    summary["tool_used"] = True
    summary["tool_remaining"] = remaining
    summary["tool_broken"] = broken
    set_node_cooldown(character, node["id"], rarity)
    summary["cooldown_set"] = True
    return summary


def _apply_action_rewards(action_id: str, target_id: str | None, rewards: dict, tier: str, monster: dict | None,
                          character: dict | None = None, biome_id: str | None = None, node: dict | None = None,
                          outcome: int = 0):
    continent_id = character.get("current_continent") if character else None
    if action_id == "hunt" and monster:
        drops, xp, gold = _roll_loot(monster, character, critical=(tier == "critical"))
        rewards["xp"] += xp
        rewards["gold"] += gold
        rewards["items"].extend(drops)
    elif action_id in ("gather", "fish"):
        scavenge = not node or node.get("scavenge", False)
        rarity = node.get("rarity", "common") if node else "common"
        material_id = node.get("item_id") if node else (target_id or "wild_herb")
        base_xp = {"common": 5, "uncommon": 7, "rare": 12, "epic": 18, "legendary": 25}.get(rarity, 5)
        base_gold = {"common": 2, "uncommon": 4, "rare": 8, "epic": 14, "legendary": 20}.get(rarity, 2)
        qty = 1
        if tier == "critical":
            qty += CRIT_QUANTITY_BONUS.get(rarity, 1)
        elif tier == "normal" and outcome == 5 and not scavenge:  # success with benefit extra
            qty += 1
        # Item bonus: gathering_yield — boost gather quantity by percentage
        _gy = _aggregate_item_bonus_effects(character).get("gathering_yield", 0) if character else 0
        if _gy > 0:
            qty = qty + int(qty * _gy)
        if scavenge:
            base_xp = max(1, base_xp // 2)
            base_gold = max(0, base_gold // 2)
            qty = max(1, qty // 2)
        # Continental XP bonus for matching profession
        if not scavenge and node and node.get("profession"):
            mult = xp_multiplier_for(continent_id, node["profession"])
            base_xp = int(base_xp * mult)
        rewards["xp"] += base_xp
        rewards["gold"] += base_gold
        rewards["items"].append((material_id, qty))
        # crit gets a bonus rare drop
        if tier == "critical" and not scavenge:
            rare_bonus = random.choice(["relic_shard", "wisp_essence", "serpent_venom"])
            rewards["items"].append((rare_bonus, 1))
        # Continental bonus: Hylion gather_success — extra chance for bonus fish
        if action_id == "fish" and continent_id:
            _gs = continental_bonus_for(continent_id, "gather_success")
            if _gs and random.random() < float(_gs):
                rewards["items"].append((material_id, 1))
        # Continental bonus: Hylion pearl_coral_chance — extra rare drop when fishing
        if action_id == "fish" and continent_id:
            _pc = continental_bonus_for(continent_id, "pearl_coral_chance")
            if _pc and random.random() < float(_pc):
                rewards["items"].append(("river_pearl", 1))
        # Continental bonus: Daw'ul Talalu magical_plant_chance — extra rare plant when gathering
        if action_id == "gather" and continent_id:
            _mp = continental_bonus_for(continent_id, "magical_plant_chance")
            if _mp and random.random() < float(_mp):
                rewards["items"].append(("moonpetal", 1))
        # Heritage month bonus: +50% gather yield on heritage continent
        if action_id in ("gather", "fish") and continent_id and is_heritage_month_for(continent_id):
            _hb = get_heritage_bonuses(continent_id)
            if _hb:
                _mult = _hb.get("gather_yield_mult", 1.0)
                # Apply bonus to the last material drop
                if rewards["items"]:
                    last = rewards["items"][-1]
                    if isinstance(last, tuple) and len(last) == 2:
                        bonus_qty = max(0, int(last[1] * (_mult - 1.0)))
                        if bonus_qty > 0:
                            rewards["items"].append((last[0], bonus_qty))
        # Apply tool durability and cooldown after successful gather
        if not scavenge and node and character:
            _consume_tool_and_cooldown(character, action_id, node, outcome)
    elif action_id == "explore":
        if tier == "critical":
            rewards["items"].append(("relic_shard", 1))
            # tiny chance for a skillbook
            if random.random() < 0.35:
                rewards["items"].append((random.choice(["skillbook_ward", "skillbook_purge"]), 1))
    elif action_id == "loot_ruins":
        rewards["xp"] += 20
        rewards["gold"] += random.randint(15, 40)
        rewards["items"].append(("relic_shard", 1))
        if tier == "critical":
            rewards["gold"] += 100
            rewards["items"].append(("skillbook_smite", 1))


# ============================================================
# COMBAT ENGINE
# ============================================================

# Innate action types (replaces old AUTO-only system)
INNATE_ACTIONS = ["strike", "defend", "evade", "aim", "counter", "focus"]

# Telegraph flavor texts by monster skill power_type
_TELEGRAPH_FLAVOR = {
    "strike": [
        "The {name} raises its weapon — a heavy strike is coming!",
        "The {name} shifts its weight, coiling for a powerful blow!",
        "The {name} locks its eyes on you, preparing to strike!",
        "The {name} bares its teeth and winds up for a devastating hit!",
    ],
    "heal": [
        "The {name} begins to glow with restorative energy — it's preparing to heal!",
        "The {name} murmurs ancient words, reaching for mending magic!",
        "The {name} coils inward, gathering life essence to mend its wounds!",
    ],
    "buff": [
        "The {name} begins chanting — a protective ward is forming!",
        "The {name} steels itself, drawing on inner power to bolster its defenses!",
        "The {name} shimmers with gathering energy — a buff is incoming!",
    ],
    "debuff": [
        "The {name} begins a sinister incantation — a debuff is coming!",
        "The {name} fixes you with a withering gaze, preparing to curse you!",
        "The {name} exhales a cloud of dark energy, aiming to weaken you!",
    ],
}

_TELEGRAPH_COLOR = {
    "strike": "destructive",
    "heal": "primary",
    "buff": "primary",
    "debuff": "amber",
}


def generate_telegraph(state: dict, character: dict) -> dict:
    """Predict the monster's next action WITHOUT executing it.
    Uses the same _pick_monster_skill logic the combat turn uses.
    Returns a telegraph dict for the frontend to display.
    """
    if not state.get("active"):
        return {"available": False}

    monster = get_monster(state["monster_id"])
    if not monster:
        return {"available": False}

    m_hp_ratio = state["monster_hp"] / max(1, state["monster_max_hp"])
    hp_ratio = character.get("hp", 1) / max(1, character.get("max_hp", 1))
    turn = state.get("turn", 0)

    m_skill = _pick_monster_skill(monster, state, m_hp_ratio, hp_ratio, turn)

    if not m_skill:
        # Basic attack — no skill
        m_stats = state.get("monster_stats", {})
        c_base = 3 + (state["monster_threat"] // 2)
        min_dmg = int(c_base * 0.4)
        max_dmg = int(c_base * 1.6)
        return {
            "available": True,
            "action_type": "strike",
            "skill_name": None,
            "damage_type": "physical",
            "estimated_damage": f"{min_dmg}-{max_dmg}",
            "warning_text": f"The {monster['name']} readies a basic attack!",
            "is_heavy": c_base >= 10,
            "color": "destructive",
        }

    ptype = m_skill.get("power_type", "strike")
    dmg_type = m_skill.get("damage_type", "physical")
    skill_name = m_skill.get("name", "Unknown")

    # Estimate damage range for strike/debuff
    est_damage = None
    is_heavy = False
    if ptype in ("strike", "debuff"):
        m_stats = state.get("monster_stats", {})
        c_base = m_skill.get("damage", 3)
        if ptype == "strike":
            if dmg_type == "physical":
                c_base = m_skill["damage"] + int(m_stats.get("might", 0) * 0.5)
            elif dmg_type == "magical":
                c_base = m_skill["damage"] + int(m_stats.get("insight", 0) * 0.5)
        min_dmg = int(c_base * 0.4)
        max_dmg = int(c_base * 1.6)
        est_damage = f"{min_dmg}-{max_dmg}"
        is_heavy = c_base >= 10

    flavor_pool = _TELEGRAPH_FLAVOR.get(ptype, _TELEGRAPH_FLAVOR["strike"])
    warning = random.choice(flavor_pool).format(name=monster["name"])

    return {
        "available": True,
        "action_type": ptype,
        "skill_name": skill_name,
        "damage_type": dmg_type,
        "estimated_damage": est_damage,
        "warning_text": warning,
        "is_heavy": is_heavy,
        "color": _TELEGRAPH_COLOR.get(ptype, "destructive"),
    }


# Combo multiplier tiers
def _combo_mult(combo: int) -> float:
    if combo >= 7:
        return 2.0
    elif combo >= 5:
        return 1.5
    elif combo >= 3:
        return 1.2
    return 1.0


# ============================================================
# ALCHEMIST COMBAT SYSTEM
# ============================================================

def _is_alchemist(character: dict) -> bool:
    return "alchemist" in (character.get("masteries") or [])


def _alch_has_passive(character: dict, passive_id: str) -> bool:
    """Is this auto-learned Alchemist passive unlocked at the character's level?

    ALCHEMIST_PASSIVES was missing entirely until now — the Alchemist was the
    only mastery that gained nothing between level 10 and 100. Passives are
    level-gated and auto-learned, so membership is purely a level check.
    """
    if not _is_alchemist(character):
        return False
    from game_data import ALCHEMIST_PASSIVES
    entry = next((p for p in ALCHEMIST_PASSIVES if p["id"] == passive_id), None)
    if not entry:
        return False
    return character.get("level", 1) >= entry.get("level", 999)


def _alch_load_imbue(state: dict, skill: dict, log: list[dict], character: dict | None = None) -> None:
    """Load an imbue skill onto the katar."""
    state["alchemist_imbue"] = skill
    charges = skill.get("imbue_charges", 3)
    # Stable Compound (L30): the coating lasts one extra hit.
    if character is not None and _alch_has_passive(character, "stable_compound"):
        charges += 1
    if state.get("alchemist_infinite_charges", 0) > 0:
        charges = 999
    state["alchemist_imbue_charges"] = charges
    state["alchemist_imbue_hits"] = 0
    state["alchemist_poison_stacks"] = 0
    blade = skill.get("blade_shape", "unknown")
    log.append({"kind": "alchemist_imbue", "text": f"The katar transmutes — blade becomes {blade}. {skill['name']} loaded ({charges} charges)."})


def _alch_apply_imbue_rider(state: dict, character: dict, monster: dict, log: list[dict], hit_count: int = 1) -> None:
    """Apply imbue effects (status + stat_mod) for each hit while imbued."""
    imbue = state.get("alchemist_imbue")
    if not imbue or state.get("alchemist_imbue_charges", 0) <= 0:
        return

    max_rules = state.get("alchemist_max_mini_rules", False)
    mini_rule = imbue.get("imbue_mini_rule", "")
    charges_left = state.get("alchemist_imbue_charges", 0)

    for _ in range(hit_count):
        if state.get("alchemist_infinite_charges", 0) <= 0:
            # Endless Reaction (L90): charges hold while Combo Flow is 10+.
            if not (_alch_has_passive(character, "endless_reaction")
                    and state.get("alchemist_cf", 0) >= 10):
                state["alchemist_imbue_charges"] = charges_left - 1
            charges_left -= 1
        if charges_left < 0 and state.get("alchemist_infinite_charges", 0) <= 0:
            break

        # Apply imbue status
        imbue_status = imbue.get("imbue_status")
        if imbue_status:
            _append_status_dedup(state, make_status(imbue_status), key="monster_statuses")

        # Apply imbue stat_mod to enemy
        imbue_stat_mod = imbue.get("imbue_stat_mod", {}).get("enemy", {})
        if imbue_stat_mod:
            dur = imbue.get("imbue_mod_duration", 2)
            _alch_apply_enemy_stat_mod(state, imbue_stat_mod, dur, mini_rule, max_rules)

        # Track hit count for mini-rules
        state["alchemist_imbue_hits"] = state.get("alchemist_imbue_hits", 0) + 1
        hits = state["alchemist_imbue_hits"]

        # Execute mini-rule
        _alch_execute_mini_rule(state, character, monster, log, mini_rule, hits, max_rules)

    # Check if imbue is depleted
    if state.get("alchemist_imbue_charges", 0) <= 0 and state.get("alchemist_infinite_charges", 0) <= 0:
        log.append({"kind": "alchemist_imbue", "text": "The katar's imbue fades — the blade returns to normal."})
        state["alchemist_imbue"] = None
        state["alchemist_imbue_hits"] = 0
        state["alchemist_poison_stacks"] = 0


def _alch_apply_enemy_stat_mod(state: dict, stat_mod: dict, duration: int, mini_rule: str, max_rules: bool) -> None:
    """Apply enemy stat modifications, enhanced by mini-rules where applicable."""
    mods = dict(stat_mod)

    # Mini-rule enhancements to stat_mod
    if mini_rule == "stacking_armor_shred":
        hits = state.get("alchemist_imbue_hits", 0)
        extra = -1 * hits if not max_rules else -5 * hits
        mods["armor_bonus"] = mods.get("armor_bonus", 0) + extra
    elif mini_rule == "stacking_accuracy_drain":
        hits = state.get("alchemist_imbue_hits", 0)
        extra = -1 * hits if not max_rules else -5 * hits
        mods["grace"] = mods.get("grace", 0) + extra
    elif mini_rule == "feeds_on_existing_statuses":
        num_statuses = len(state.get("monster_statuses", []))
        mult = 2.0 if max_rules else 1.5
        for k in mods:
            if k == "armor_bonus":
                mods[k] = int(mods[k] * (mult ** num_statuses))

    # Store as a temporary stat mod entry
    existing = state.setdefault("alchemist_enemy_stat_mods", [])
    existing.append({"mods": mods, "duration": duration})


def _alch_get_enemy_stat_mod_total(state: dict) -> dict:
    """Get aggregate enemy stat mods from active imbue."""
    mods_list = state.get("alchemist_enemy_stat_mods", [])
    total: dict[str, int] = {}
    active = []
    for entry in mods_list:
        if entry["duration"] > 0:
            for k, v in entry["mods"].items():
                total[k] = total.get(k, 0) + v
            entry["duration"] -= 1
            if entry["duration"] > 0:
                active.append(entry)
    state["alchemist_enemy_stat_mods"] = active
    return total


def _alch_execute_mini_rule(state: dict, character: dict, monster: dict, log: list[dict],
                             rule: str, hits: int, max_rules: bool) -> None:
    """Execute the unique mini-rule for the current imbue."""
    if not rule:
        return

    # Check adjustment bonus (CF spend: Adjustment) — doubles next mini-rule proc
    adjustment = state.get("alchemist_adjustment_bonus", False)

    if rule == "freeze_on_4th_hit":
        threshold = 1 if max_rules else 4
        if hits % threshold == 0:
            _append_status_dedup(state, make_status("stunned"), key="monster_statuses")
            if adjustment:
                _append_status_dedup(state, make_status("ensnared"), key="monster_statuses")
                state["alchemist_adjustment_bonus"] = False
            log.append({"kind": "alchemist_mini_rule", "text": "Frost bites deep — the enemy is frozen solid! Turn skipped."})

    elif rule == "chain_on_3rd_hit":
        threshold = 1 if max_rules else 3
        if hits % threshold == 0:
            extra_dmg = int(state.get("monster_threat", 5) * 0.3)
            if adjustment:
                extra_dmg *= 2
                state["alchemist_adjustment_bonus"] = False
            state["monster_hp"] = max(0, state["monster_hp"] - extra_dmg)
            log.append({"kind": "alchemist_mini_rule", "text": f"Lightning chains! Arcing damage hits for {extra_dmg}."})

    elif rule == "scaling_damage_over_time":
        stacks = state.get("alchemist_poison_stacks", 0) + 1
        state["alchemist_poison_stacks"] = stacks
        scale = 2.0 if max_rules else 1.1
        if adjustment:
            scale *= 1.2
            state["alchemist_adjustment_bonus"] = False
        bonus = int(3 * stacks * (scale - 1.0))
        if bonus > 0:
            state["monster_hp"] = max(0, state["monster_hp"] - bonus)
            log.append({"kind": "alchemist_mini_rule", "text": f"Poison intensifies — +{bonus} damage (stack {stacks})."})

    elif rule == "immobilize_on_3rd_hit":
        threshold = 1 if max_rules else 3
        if hits % threshold == 0:
            dur = 4 if adjustment else 2
            if adjustment:
                state["alchemist_adjustment_bonus"] = False
            state["alchemist_enemy_immobilized"] = dur
            log.append({"kind": "alchemist_mini_rule", "text": f"Living slime locks the enemy's legs — immobilized for {dur} turns!"})

    elif rule == "armor_to_paper_on_2nd_hit":
        threshold = 1 if max_rules else 2
        if hits % threshold == 0:
            dur = 5 if adjustment else 3
            if adjustment:
                state["alchemist_adjustment_bonus"] = False
            state.setdefault("alchemist_enemy_stat_mods", []).append(
                {"mods": {"armor_bonus": -999}, "duration": dur}
            )
            log.append({"kind": "alchemist_mini_rule", "text": "Transmutation complete — enemy armor is paper!"})

    elif rule == "double_hit_detonation":
        extra = int(5 * (2 if max_rules else 1))
        if adjustment:
            extra *= 2
            state["alchemist_adjustment_bonus"] = False
        state["monster_hp"] = max(0, state["monster_hp"] - extra)
        log.append({"kind": "alchemist_mini_rule", "text": f"Explosive detonation! +{extra} blast damage."})

    elif rule == "all_statuses_true_damage":
        for s in ["burning", "poisoned", "ensnared", "stunned", "blinded", "shaken", "bleeding"]:
            _append_status_dedup(state, make_status(s), key="monster_statuses")
        state["alchemist_katar_cracked"] = True
        log.append({"kind": "alchemist_mini_rule", "text": "FORBIDDEN FORMULA — all statuses applied! True damage! The katar cracks."})


def _alch_apply_strike_rule(state: dict, character: dict, monster: dict, log: list[dict],
                             skill: dict, outcome: int, total_dmg: int) -> int:
    """Apply strike rule effects. Returns modified damage."""
    rule = skill.get("strike_rule", "")
    if not rule:
        return total_dmg

    if rule == "never_misses":
        if outcome < 4:
            log.append({"kind": "alchemist_strike_rule", "text": "Quick Jab finds its mark — never misses!"})
            return max(total_dmg, int(total_dmg * 0.5))  # partial hit minimum

    elif rule == "armor_break":
        # Permanent armor reduction
        state.setdefault("alchemist_enemy_stat_mods", []).append(
            {"mods": {"armor_bonus": -2}, "duration": 999}
        )
        log.append({"kind": "alchemist_strike_rule", "text": "Heavy Crush — enemy armor permanently reduced by 2!"})

    elif rule == "cf_builder":
        # Flurry: triple CF gain already handled in CF gain logic
        log.append({"kind": "alchemist_strike_rule", "text": "Flurry — triple CF gain, triple imbue procs!"})

    elif rule == "gap_close_and_reload":
        # Re-imbue: player can load a new imbue next turn without losing action
        state["alchemist_free_reimbue"] = True
        log.append({"kind": "alchemist_strike_rule", "text": "Rushing Strike — gap closed! Free re-imbue available next turn."})

    elif rule == "reposition":
        state["alchemist_repositioned"] = True
        log.append({"kind": "alchemist_strike_rule", "text": "Spinning Strike — repositioned behind the enemy!"})

    elif rule == "ignores_50_percent_armor":
        # Damage already calculated — add back 50% of armor-reduced damage
        # Approximate: boost damage by 25% to simulate ignoring half armor
        total_dmg = int(total_dmg * 1.25)
        log.append({"kind": "alchemist_strike_rule", "text": "Piercing Strike — bypasses 50% armor!"})

    elif rule == "interrupt":
        # Cancel enemy's next skill preparation
        state["alchemist_interrupt"] = True
        log.append({"kind": "alchemist_strike_rule", "text": "Counter Strike — interrupts enemy casting!"})

    elif rule == "stance_break":
        # Remove warded from enemy, prevent re-warding
        state["monster_statuses"] = [s for s in state.get("monster_statuses", []) if s.get("id") != "warded"]
        state["alchemist_ward_block"] = 2
        log.append({"kind": "alchemist_strike_rule", "text": "Guard Break — enemy warded removed, can't re-ward for 2 turns!"})

    elif rule == "launch":
        state["alchemist_enemy_launched"] = True
        log.append({"kind": "alchemist_strike_rule", "text": "Rising Strike — enemy launched airborne! Can't act next turn."})

    elif rule == "cf_consumer":
        cf = state.get("alchemist_cf", 0)
        if cf > 0:
            bonus_mult = 1.0 + (0.10 * cf)
            total_dmg = int(total_dmg * bonus_mult)
            log.append({"kind": "alchemist_strike_rule", "text": f"Executioner Strike — consumes {cf} CF for +{cf*10}% damage!"})
            state["alchemist_cf"] = 0
        # Execute bonus: +50% below 30% HP
        if state["monster_hp"] / max(1, state["monster_max_hp"]) < 0.3:
            total_dmg = int(total_dmg * 1.5)
            log.append({"kind": "alchemist_strike_rule", "text": "EXECUTE — enemy below 30% HP! +50% damage!"})

    elif rule == "legendary_strike":
        # Auto-adapt katar: each hit chooses optimal imbue based on enemy state
        log.append({"kind": "alchemist_strike_rule", "text": "Legend of Alchemy — the katar adapts. 8 hits of true damage."})
        # Apply all stat_mods from the skill
        stat_mod = skill.get("stat_mod", {}).get("enemy", {})
        if stat_mod:
            dur = skill.get("mod_duration", 5)
            state.setdefault("alchemist_enemy_stat_mods", []).append({"mods": stat_mod, "duration": dur})

        # Auto-adapt: apply optimal imbue effect per hit based on enemy state
        m_stats = state.get("monster_stats", {})
        m_hp_ratio = state["monster_hp"] / max(1, state["monster_max_hp"])
        monster_statuses = state.get("monster_statuses", [])
        num_hits = skill.get("hits", 8)
        for h in range(num_hits):
            # Determine optimal imbue for this hit
            if h == num_hits - 1:
                # Final hit: Forbidden Formula — all statuses + true damage
                for s in ["burning", "poisoned", "ensnared", "stunned", "blinded", "shaken", "bleeding"]:
                    _append_status_dedup(state, make_status(s), key="monster_statuses")
                log.append({"kind": "alchemist_adapt", "text": f"Hit {h+1}: Shifting blade — FORBIDDEN FORMULA! All statuses!"})
            elif m_stats.get("armor_bonus", 0) > 10 and h == 0:
                # High armor → Acid (liquid blade, armor shred)
                state.setdefault("alchemist_enemy_stat_mods", []).append({"mods": {"armor_bonus": -5}, "duration": 3})
                log.append({"kind": "alchemist_adapt", "text": f"Hit {h+1}: Liquid blade — acid shreds armor!"})
            elif any(s.get("id") == "stunned" for s in monster_statuses) and h >= 3:
                # Stunned → Explosive (jagged, burst)
                extra = int(total_dmg * 0.1)
                state["monster_hp"] = max(0, state["monster_hp"] - extra)
                log.append({"kind": "alchemist_adapt", "text": f"Hit {h+1}: Jagged blade — detonation! +{extra} damage."})
            elif m_hp_ratio < 0.3:
                # Low HP → Poison (needle, scaling) or Explosive
                extra = int(total_dmg * 0.15)
                state["monster_hp"] = max(0, state["monster_hp"] - extra)
                log.append({"kind": "alchemist_adapt", "text": f"Hit {h+1}: Jagged blade — execute burst! +{extra} damage."})
            elif len(monster_statuses) >= 3:
                # Status-afflicted → Corrosive (eroding, amplified)
                state.setdefault("alchemist_enemy_stat_mods", []).append({"mods": {"armor_bonus": -3, "might": -2}, "duration": 3})
                log.append({"kind": "alchemist_adapt", "text": f"Hit {h+1}: Eroding blade — corrosion amplified!"})
            elif m_stats.get("grace", 0) > 10:
                # Mobile/high evasion → Frost (ice spike, freeze)
                _append_status_dedup(state, make_status("ensnared"), key="monster_statuses")
                log.append({"kind": "alchemist_adapt", "text": f"Hit {h+1}: Ice spike — frost freezes the enemy!"})
            else:
                # Default → Lightning (claw, chain)
                _append_status_dedup(state, make_status("stunned"), key="monster_statuses")
                log.append({"kind": "alchemist_adapt", "text": f"Hit {h+1}: Lightning claw — stun + chain!"})

    return total_dmg


def _alch_gain_cf(state: dict, skill: dict, log: list[dict], character: dict | None = None) -> None:
    """Gain Combo Flow from a strike."""
    cf_gain = skill.get("cf_gain", 1)
    if cf_gain <= 0:
        return
    # Steady Hands (L10): +1 Combo Flow per strike.
    if character is not None and _alch_has_passive(character, "steady_hands"):
        cf_gain += 1
    # Item bonus: combo_gain — boost CF gain by percentage
    _cg = state.get("item_bonus_effects", {}).get("combo_gain", 0)
    if _cg > 0:
        cf_gain = cf_gain + int(cf_gain * _cg)
    current = state.get("alchemist_cf", 0)
    cf_max = state.get("alchemist_cf_max", 20)
    # Deep Reserves (L20): raise the Combo Flow ceiling.
    if character is not None and _alch_has_passive(character, "deep_reserves"):
        cf_max = max(cf_max, 25)
    new_cf = min(cf_max, current + cf_gain)
    if new_cf > current:
        state["alchemist_cf"] = new_cf
        if new_cf >= 5 and current < 5:
            log.append({"kind": "alchemist_cf", "text": f"Combo Flow: {new_cf} — Analysis available (5 CF)."})
        elif new_cf >= 10 and current < 10:
            log.append({"kind": "alchemist_cf", "text": f"Combo Flow: {new_cf} — Adjustment available (10 CF)."})
        elif new_cf >= 15 and current < 15:
            log.append({"kind": "alchemist_cf", "text": f"Combo Flow: {new_cf} — Optimization available (15 CF)."})
        elif new_cf >= 20 and current < 20:
            log.append({"kind": "alchemist_cf", "text": f"Combo Flow: {new_cf} — Perfect Formula available (20 CF)!"})


def _alch_spend_cf(state: dict, character: dict, monster: dict, log: list[dict], action: str, choice: str = "") -> bool:
    """Spend Combo Flow on an adaptive action. Returns True if successful."""
    cf = state.get("alchemist_cf", 0)
    costs = {"analysis": 5, "adjustment": 10, "optimization": 15, "perfect_formula": 20}
    cost = costs.get(action, 0)
    # Transmuter's Insight (L50): Combo Flow actions cost 1 less.
    if _alch_has_passive(character, "transmuters_insight"):
        cost = max(1, cost - 1)
    # Perfect Transmutation (L100): Combo Flow actions are free.
    if _alch_has_passive(character, "perfect_transmutation"):
        cost = 0
    if cf < cost:
        return False

    state["alchemist_cf"] = cf - cost

    if action == "analysis":
        # Reveal enemy weakness (increase next hit damage by 20%)
        state["alchemist_analysis_bonus"] = 1.2
        log.append({"kind": "alchemist_cf_spend", "text": f"Analysis (5 CF) — enemy weakness identified! Next strike +20%."})

    elif action == "adjustment":
        # Enhance current imbue's mini-rule (next proc at double effect)
        state["alchemist_adjustment_bonus"] = True
        log.append({"kind": "alchemist_cf_spend", "text": f"Adjustment (10 CF) — imbue mini-rule enhanced! Next proc at double effect."})

    elif action == "optimization":
        # Reduce strike cooldowns by 1 OR free re-imbue
        for sid in list(state.get("skill_cooldowns", {}).keys()):
            if state["skill_cooldowns"][sid] > 0:
                state["skill_cooldowns"][sid] = max(0, state["skill_cooldowns"][sid] - 1)
        state["alchemist_free_reimbue"] = True
        log.append({"kind": "alchemist_cf_spend", "text": f"Optimization (15 CF) — strike cooldowns reduced, free re-imbue available!"})

    elif action == "perfect_formula":
        pf = choice or "delivery"
        if pf == "delivery":
            # Perfect Delivery: +2 hits on next strike (both carry imbue at +2 stacks)
            state["alchemist_perfect_delivery"] = True
            log.append({"kind": "alchemist_cf_spend", "text": "Perfect Formula: Perfect Delivery (20 CF) — next strike +2 hits with imbue!"})
        elif pf == "conversion":
            # Perfect Conversion: refresh active imbue's charges to full
            imbue = state.get("alchemist_imbue")
            if imbue:
                state["alchemist_imbue_charges"] = 999 if state.get("alchemist_infinite_charges", 0) > 0 else imbue.get("imbue_charges", 3)
                log.append({"kind": "alchemist_cf_spend", "text": f"Perfect Formula: Perfect Conversion (20 CF) — {imbue['name']} charges refreshed to full!"})
            else:
                state["alchemist_cf"] = cf  # refund
                return False
        elif pf == "sequence":
            # Perfect Sequence: re-imbue AND strike in same turn (free re-imbue + free strike)
            state["alchemist_free_reimbue"] = True
            state["alchemist_perfect_sequence"] = True
            log.append({"kind": "alchemist_cf_spend", "text": "Perfect Formula: Perfect Sequence (20 CF) — re-imbue and strike in same turn!"})
        elif pf == "breakdown":
            # Perfect Breakdown: next strike ignores all armor, deals true damage
            state["alchemist_perfect_breakdown"] = True
            log.append({"kind": "alchemist_cf_spend", "text": "Perfect Formula: Perfect Breakdown (20 CF) — next strike ignores all armor, true damage!"})

    return True


def _alch_tick_alchemist_state(state: dict, log: list[dict]) -> None:
    """Tick Alchemist state at end of turn (decrement durations, clear flags)."""
    # CF reset on stun
    player_statuses = state.get("player_statuses", [])
    if any(s.get("id") == "stunned" for s in player_statuses):
        if state.get("alchemist_cf", 0) > 0:
            state["alchemist_cf"] = 0
            log.append({"kind": "alchemist_cf_reset", "text": "Stunned — Combo Flow resets! Experiment ruined."})

    # CF reset on skip turn (no strike this turn)
    if not state.get("alchemist_struck_this_turn", False):
        if state.get("alchemist_cf", 0) > 0:
            state["alchemist_cf"] = 0
            log.append({"kind": "alchemist_cf_reset", "text": "No strike this turn — Combo Flow resets! Data lost."})
    state["alchemist_struck_this_turn"] = False

    # Clear katar cracked (lasts 1 turn)
    state["alchemist_katar_cracked"] = False

    if state.get("alchemist_infinite_charges", 0) > 0:
        state["alchemist_infinite_charges"] -= 1
        if state["alchemist_infinite_charges"] == 0:
            state["alchemist_max_mini_rules"] = False
            log.append({"kind": "alchemist_state", "text": "Philosopher's Transmutation fades — infinite charges ended."})

    if state.get("alchemist_ward_block", 0) > 0:
        state["alchemist_ward_block"] -= 1

    if state.get("alchemist_enemy_immobilized", 0) > 0:
        state["alchemist_enemy_immobilized"] -= 1

    # Clear one-turn flags
    state["alchemist_enemy_launched"] = False
    state["alchemist_repositioned"] = False
    state["alchemist_interrupt"] = False
    state["alchemist_free_reimbue"] = False
    state["alchemist_analysis_bonus"] = 1.0
    state["alchemist_adjustment_bonus"] = False
    state["alchemist_perfect_formula"] = False
    state["alchemist_perfect_delivery"] = False
    state["alchemist_perfect_sequence"] = False
    state["alchemist_perfect_breakdown"] = False

    # Tick enemy stat mods
    _alch_get_enemy_stat_mod_total(state)


# ============================================================
# PALADIN COMBAT SYSTEM
# ============================================================

def _is_paladin(character: dict) -> bool:
    return "paladin" in (character.get("masteries") or [])


# ---- Paladin Faith Bar ----
# Inherent system: scales all main stats as HP drops. No level gating.
# 6 tiers, each with increasing stat multiplier and heal amplification.
FAITH_HP_THRESHOLDS = [0.90, 0.70, 0.50, 0.25, 0.10, 0.05]  # tier 1-6
FAITH_MULTS =         [0.10,  0.15,  0.25,  0.35,  0.40,  0.50]
FAITH_HEAL_AMPS =     [1.05,  1.10,  1.20,  1.30,  1.40,  1.50]
FAITH_TIER_NAMES = [
    "Unbroken",          # tier 0: >90% HP
    "Faith Stirring",    # tier 1: ≤90%
    "Faith Rising",      # tier 2: ≤70%
    "Faith Burning",     # tier 3: ≤50%
    "Faith Blazing",     # tier 4: ≤25%
    "Faith Unleashed",   # tier 5: ≤10%
    "Faith Ascendant",   # tier 6: ≤5%
]
FAITH_MAIN_STATS = ["might", "insight", "grace", "vitality", "essence", "armor_bonus"]


def _paladin_get_faith_tier(hp_ratio: float) -> int:
    """Determine faith tier based on current HP ratio. 0 = >90%, 6 = ≤5%."""
    for i, threshold in enumerate(reversed(FAITH_HP_THRESHOLDS)):
        if hp_ratio <= threshold:
            return len(FAITH_HP_THRESHOLDS) - i
    return 0


def _paladin_compute_faith_bonuses(tier: int, base_stats: dict, char_level: int) -> dict:
    """Compute stat bonuses for a given faith tier.
    Percentage of base stats + passive flat bonuses that stack on top."""
    bonuses = {stat: 0 for stat in FAITH_MAIN_STATS}
    bonuses["heal_amp"] = 1.0

    if tier <= 0:
        return bonuses

    # Percentage-based scaling on all main stats
    mult = FAITH_MULTS[tier - 1]
    for stat in FAITH_MAIN_STATS:
        bonuses[stat] = int(base_stats.get(stat, 0) * mult)

    # Passive flat bonuses (stack on top of faith bar, not gated by tier)
    # Faith Unbroken (L40): +8 armor when any faith tier active
    if char_level >= 40 and tier >= 1:
        bonuses["armor_bonus"] += 8
    # Martyr's Resolve (L60): +15 armor, +8 essence at tier 3+
    if char_level >= 60 and tier >= 3:
        bonuses["armor_bonus"] += 15
        bonuses["essence"] += 8
    # Last Light (L80): +25 armor, +15 essence at tier 4+
    if char_level >= 80 and tier >= 4:
        bonuses["armor_bonus"] += 25
        bonuses["essence"] += 15

    bonuses["heal_amp"] = FAITH_HEAL_AMPS[tier - 1]
    return bonuses


def _paladin_update_scaling(state: dict, character: dict, log: list[dict]) -> None:
    """Recalculate Paladin faith scaling based on current HP. Called at end of turn."""
    if not _is_paladin(character):
        return

    hp_ratio = character["hp"] / max(1, character["max_hp"])

    # Avatar of Faith (level 100 passive): always at max tier
    if state.get("paladin_avatar_of_faith"):
        new_tier = 6
    else:
        new_tier = _paladin_get_faith_tier(hp_ratio)

    old_tier = state.get("paladin_hp_tier", 0)
    base_stats = character.get("base_stats", character.get("stats", {}))
    char_level = character.get("level", 1)

    # Remove old bonuses from character stats
    old_bonuses = state.get("paladin_faith_bonuses")
    if old_bonuses:
        for stat, val in old_bonuses.items():
            if stat == "heal_amp":
                continue
            if val:
                character["stats"][stat] = character["stats"].get(stat, 0) - val
    else:
        # Backwards compat: remove old-format flat bonuses
        old_flat = {0: 0, 1: 2, 2: 4, 3: 6}
        old_armor = old_flat.get(old_tier, 0)
        old_ess = old_flat.get(old_tier, 0)
        if old_armor:
            character["stats"]["armor_bonus"] = character["stats"].get("armor_bonus", 0) - old_armor
        if old_ess:
            character["stats"]["essence"] = character["stats"].get("essence", 0) - old_ess

    # Compute and apply new bonuses
    new_bonuses = _paladin_compute_faith_bonuses(new_tier, base_stats, char_level)
    for stat, val in new_bonuses.items():
        if stat == "heal_amp":
            continue
        if val:
            character["stats"][stat] = character["stats"].get(stat, 0) + val

    state["paladin_hp_tier"] = new_tier
    state["paladin_faith_bonuses"] = new_bonuses
    state["paladin_bonus_armor"] = new_bonuses.get("armor_bonus", 0)
    state["paladin_bonus_essence"] = new_bonuses.get("essence", 0)
    state["paladin_heal_amp"] = new_bonuses.get("heal_amp", 1.0)

    if new_tier != old_tier:
        if new_tier > old_tier:
            log.append({"kind": "paladin_scaling", "text": f"Faith deepens — {FAITH_TIER_NAMES[new_tier]}! Stats +{int(FAITH_MULTS[new_tier - 1] * 100)}%, heal amp {FAITH_HEAL_AMPS[new_tier - 1]:.0%}."})
        else:
            log.append({"kind": "paladin_scaling", "text": f"Faith recedes — {FAITH_TIER_NAMES[new_tier]}."})


def _paladin_apply_heal_amp(state: dict, heal_amount: int) -> int:
    """Apply Paladin heal amplification to a heal amount."""
    if not state.get("paladin_heal_amp"):
        return heal_amount
    result = int(heal_amount * state["paladin_heal_amp"])
    # Holy Fortitude (level 20): +15% heal amp
    if state.get("paladin_holy_fortitude"):
        result = int(result * 1.15)
    return result


def _paladin_apply_holy_bonus(state: dict, character: dict, monster: dict, total_dmg: int) -> int:
    """Apply +50% damage bonus vs undead/devils for holy-tagged skills."""
    monster_category = _monster_category(monster)
    monster_tags = monster.get("tags", [])
    if monster_category in ("undead", "devil") or "undead" in monster_tags or "devil" in monster_tags:
        total_dmg = int(total_dmg * 1.5)
    return total_dmg


def _paladin_check_resurrection(state: dict, character: dict, log: list[dict]) -> bool:
    """Check if Paladin Resurrection passive triggers (survive at 1 HP).
    Returns True if resurrection triggered."""
    if not _is_paladin(character):
        return False
    if state.get("paladin_resurrection_used"):
        return False
    # Check if character has the Resurrection passive (level 90+)
    if character.get("level", 1) < 90:
        return False
    if character["hp"] <= 0:
        character["hp"] = 1
        state["paladin_resurrection_used"] = True
        log.append({"kind": "paladin_resurrection", "text": "RESURRECTION — The faith refuses death! The Paladin survives at 1 HP!"})
        return True
    return False
# ============================================================
# KNIGHT COMBAT SYSTEM
# ============================================================

KNIGHT_OATHS = {
    "iron": {
        "name": "Oath of Iron",
        "per_stack": {"armor_bonus": 1},
        "stack_trigger": "hit_or_defend",
        "milestone_5": "immune_shaken",
        "milestone_10": "reflect_10pct",
    },
    "wrath": {
        "name": "Oath of Wrath",
        "per_stack": {"might": 1},
        "stack_trigger": "deal_damage",
        "milestone_5": "strike_damage_20pct",
        "milestone_10": "strikes_bleed",
    },
    "bulwark": {
        "name": "Oath of Bulwark",
        "per_stack": {"enemy_might": -1, "enemy_grace": -1},
        "stack_trigger": "enemy_attacks",
        "milestone_5": "enemy_no_buffs",
        "milestone_10": "enemy_acc_minus_20pct",
    },
    "endurance": {
        "name": "Oath of Endurance",
        "per_stack": {"durability": 1},
        "stack_trigger": "end_of_turn",
        "milestone_5": "immune_stunned",
        "milestone_10": "damage_minus_15pct",
    },
    "vanguard": {
        "name": "Oath of Vanguard",
        "per_stack": {"all_stats": 1, "armor_bonus": -1},
        "stack_trigger": "strike_first",
        "milestone_5": "armor_penalty_removed",
        "milestone_10": "all_stats_doubled",
    },
}


def _is_knight(character: dict) -> bool:
    return "knight" in (character.get("masteries") or [])


def _is_priest(character: dict) -> bool:
    return "priest" in (character.get("masteries") or [])


def _knight_get_oath_bonus(state: dict) -> dict:
    """Get current Oath stat bonuses based on stacks and passives."""
    oath_id = state.get("knight_oath")
    if not oath_id or oath_id not in KNIGHT_OATHS:
        return {}

    oath = KNIGHT_OATHS[oath_id]
    stacks = state.get("knight_oath_stacks", 0)
    if stacks <= 0:
        return {}

    per_stack = dict(oath["per_stack"])
    multiplier = 1

    # Oath Mastery (level 60): 5+ stacks doubles effect
    if state.get("knight_oath_mastery") and stacks >= 5:
        multiplier *= 2

    # Eternal Oath (level 100): all effects tripled
    if state.get("knight_eternal_oath"):
        multiplier *= 3

    # Vanguard 10-stack: all_stats per stack becomes +2
    if oath_id == "vanguard" and stacks >= 10:
        per_stack["all_stats"] = 2

    # Vanguard 5-stack: armor penalty removed (milestone)
    if oath_id == "vanguard" and stacks >= 5:
        per_stack.pop("armor_bonus", None)

    # Eternal Oath: milestones always active (even below 5/10 stacks)
    if state.get("knight_eternal_oath") and oath_id == "vanguard":
        per_stack.pop("armor_bonus", None)
        if stacks < 10:
            per_stack["all_stats"] = max(per_stack.get("all_stats", 1), 2 if stacks >= 10 else 1)

    # Apply multiplier
    result = {}
    for k, v in per_stack.items():
        result[k] = v * stacks * multiplier

    return result


def _knight_apply_oath_bonuses(state: dict, character: dict) -> None:
    """Apply Oath stat bonuses to character stats. Called at start of turn."""
    if not _is_knight(character):
        return

    # Battle Hardened (level 30): permanent +10 armor
    if character.get("level", 1) >= 30 and state.get("knight_battle_hardened", 0) == 0:
        state["knight_battle_hardened"] = 10
        character["stats"]["armor_bonus"] = character["stats"].get("armor_bonus", 0) + 10

    bonuses = _knight_get_oath_bonus(state)
    if not bonuses:
        return

    # Store current bonuses to remove next time
    old_bonuses = state.get("knight_current_oath_bonuses", {})
    for stat, val in old_bonuses.items():
        character["stats"][stat] = character["stats"].get(stat, 0) - val

    # Apply new bonuses
    new_bonuses = {}
    for k, v in bonuses.items():
        if k == "all_stats":
            for stat in ("might", "grace", "essence", "durability", "insight", "cognition"):
                character["stats"][stat] = character["stats"].get(stat, 0) + v
                new_bonuses[stat] = new_bonuses.get(stat, 0) + v
        elif k.startswith("enemy_"):
            pass  # Enemy debuffs handled in damage calc
        else:
            character["stats"][k] = character["stats"].get(k, 0) + v
            new_bonuses[k] = v

    state["knight_current_oath_bonuses"] = new_bonuses


def _knight_gain_stack(state: dict, character: dict, log: list[dict], trigger: str) -> None:
    """Try to gain an Oath stack based on the trigger type."""
    if not _is_knight(character):
        return

    oath_id = state.get("knight_oath")
    if not oath_id or oath_id not in KNIGHT_OATHS:
        return

    oath = KNIGHT_OATHS[oath_id]
    if oath["stack_trigger"] != trigger:
        return

    # Extended Vow (level 20): +1 extra stack per gain
    gain = 1
    if character.get("level", 1) >= 20:
        gain = 2

    old_stacks = state.get("knight_oath_stacks", 0)
    new_stacks = old_stacks + gain
    state["knight_oath_stacks"] = new_stacks

    # Log milestone crossings
    if old_stacks < 5 <= new_stacks:
        log.append({"kind": "knight_oath", "text": f"{oath['name']} reaches 5 stacks — milestone bonus active!"})
    if old_stacks < 10 <= new_stacks:
        log.append({"kind": "knight_oath", "text": f"{oath['name']} reaches 10 stacks — ultimate milestone active!"})

    # Recalculate bonuses immediately so HUD shows correct values
    _knight_apply_oath_bonuses(state, character)


def _knight_check_milestones(state: dict, character: dict, monster: dict, log: list[dict]) -> dict:
    """Check and apply Oath milestone effects. Returns modifiers dict."""
    if not _is_knight(character):
        return {}

    oath_id = state.get("knight_oath")
    if not oath_id or oath_id not in KNIGHT_OATHS:
        return {}

    stacks = state.get("knight_oath_stacks", 0)
    oath = KNIGHT_OATHS[oath_id]
    mods = {}

    # Eternal Oath: milestones always active
    eternal = state.get("knight_eternal_oath", False)

    if stacks >= 5 or eternal:
        ms5 = oath["milestone_5"]
        if ms5 == "immune_shaken":
            character["statuses"] = [s for s in character.get("statuses", []) if s.get("id") != "shaken"]
            mods["immune_shaken"] = True
        elif ms5 == "strike_damage_20pct":
            mods["strike_damage_mult"] = 1.2
        elif ms5 == "enemy_no_buffs":
            mods["enemy_no_buffs"] = True
        elif ms5 == "immune_stunned":
            character["statuses"] = [s for s in character.get("statuses", []) if s.get("id") != "stunned"]
            mods["immune_stunned"] = True
        elif ms5 == "armor_penalty_removed":
            # Remove Vanguard armor penalty
            mods["vanguard_armor_restored"] = True

    if stacks >= 10 or eternal:
        ms10 = oath["milestone_10"]
        if ms10 == "reflect_10pct":
            mods["reflect_10pct"] = True
        elif ms10 == "strikes_bleed":
            mods["strikes_bleed"] = True
        elif ms10 == "enemy_acc_minus_20pct":
            mods["enemy_acc_minus_20pct"] = True
        elif ms10 == "damage_minus_15pct":
            mods["incoming_damage_mult"] = 0.85
        elif ms10 == "all_stats_doubled":
            pass  # Handled in _knight_get_oath_bonus

    return mods


def _knight_tick_end_of_turn(state: dict, character: dict, log: list[dict]) -> None:
    """Knight end-of-turn processing: Oath of Endurance stacks, Adrenal Surge check."""
    if not _is_knight(character):
        return

    # Oath of Endurance: gain stack at end of turn (+1 extra below 50% HP)
    hp_ratio = character["hp"] / max(1, character["max_hp"])
    if state.get("knight_oath") == "endurance":
        gain = 1
        if hp_ratio < 0.50:
            gain = 2
        # Extended Vow
        if character.get("level", 1) >= 20:
            gain *= 2
        old = state.get("knight_oath_stacks", 0)
        new = old + gain
        state["knight_oath_stacks"] = new
        if old < 5 <= new:
            log.append({"kind": "knight_oath", "text": "Oath of Endurance reaches 5 stacks — immune to stun!"})
        if old < 10 <= new:
            log.append({"kind": "knight_oath", "text": "Oath of Endurance reaches 10 stacks — 15% damage reduction!"})

    # Adrenal Surge (level 40): when HP drops below 50%, gain +15 might for 3 turns
    if (character.get("level", 1) >= 40 and not state.get("knight_adrenal_used")
            and hp_ratio < 0.50):
        state["knight_adrenal_used"] = True
        state.setdefault("knight_self_stat_mods", []).append({"mods": {"might": 15}, "duration": 3})
        character["stats"]["might"] = character["stats"].get("might", 0) + 15
        log.append({"kind": "knight_passive", "text": "ADRENAL SURGE — +15 Might for 3 turns!"})

    # Iron Will (level 50): immune to shaken and stunned
    if character.get("level", 1) >= 50:
        character["statuses"] = [s for s in character.get("statuses", [])
                                if s.get("id") not in ("shaken", "stunned")]

    # Check passives
    if character.get("level", 1) >= 60 and not state.get("knight_oath_mastery"):
        state["knight_oath_mastery"] = True
    if character.get("level", 1) >= 100 and not state.get("knight_eternal_oath"):
        state["knight_eternal_oath"] = True

    # Tick Knight self stat_mods
    tick_stat_mods(state, "knight_self_stat_mods", character["stats"])

    # Tick Knight enemy stat_mods
    knight_enemy = state.get("knight_enemy_stat_mods", [])
    active_knight_enemy = []
    for entry in knight_enemy:
        if entry["duration"] > 0:
            active_knight_enemy.append(entry)
        else:
            for stat, val in entry["mods"].items():
                m_stats = state.get("monster_stats", {})
                m_stats[stat] = m_stats.get(stat, 0) - val
    state["knight_enemy_stat_mods"] = active_knight_enemy
    for entry in state.get("knight_enemy_stat_mods", []):
        entry["duration"] -= 1


# ============================================================
# LANCER COMBAT SYSTEM
# ============================================================

LANCER_ELEMENTS = {
    "fire": {"status": "burning", "name": "Fire"},
    "ice": {"status": "ensnared", "name": "Ice"},
    "lightning": {"status": "stunned", "name": "Lightning"},
    "earth": {"status": "shaken", "name": "Earth"},
    "wind": {"status": None, "name": "Wind"},  # wind gives evasive, no enemy status
    "thunder": {"status": "shaken", "name": "Thunder"},
    "fire_earth": {"status": "burning", "name": "Volcano"},  # applies both burning+shaken
}


def _is_lancer(character: dict) -> bool:
    return "lancer" in (character.get("masteries") or [])
def _lancer_get_element_count(state: dict) -> int:
    """Return number of active elemental imbues."""
    return len(state.get("lancer_active_imbues", {}))


def _lancer_apply_imbue(state: dict, character: dict, skill: dict, log: list[dict]) -> None:
    """Apply a Lancer elemental imbue from a buff skill."""
    if not _is_lancer(character):
        return

    element = skill.get("element")
    if not element:
        return

    # Lingering Elements (level 20): +1 turn duration
    duration = skill.get("mod_duration", 3)
    if character.get("level", 1) >= 20:
        duration += 1
    # Avatar of Elements (level 100): +3 turns
    if character.get("level", 1) >= 100:
        duration += 3

    # Elemental Mastery (level 50): all imbue stat_mods increased by +1
    self_mods = dict(skill.get("stat_mod", {}).get("self", {}))
    if character.get("level", 1) >= 50:
        for k, v in self_mods.items():
            if v > 0:
                self_mods[k] = v + 1

    # Remove old imbue of same element if active
    old = state.get("lancer_active_imbues", {}).get(element)
    if old:
        for stat, val in old.get("stat_mods", {}).items():
            character["stats"][stat] = character["stats"].get(stat, 0) - val

    # Apply new imbue
    imbue_entry = {
        "skill_id": skill["id"],
        "duration": duration,
        "stat_mods": self_mods,
    }
    state.setdefault("lancer_active_imbues", {})[element] = imbue_entry

    # Apply stat mods immediately
    for stat, val in self_mods.items():
        character["stats"][stat] = character["stats"].get(stat, 0) + val

    log.append({"kind": "lancer_imbue", "text": f"{LANCER_ELEMENTS.get(element, {}).get('name', element)} imbue active for {duration} turns!"})


def _lancer_get_strike_riders(state: dict, character: dict) -> dict:
    """Get elemental rider effects for strikes based on active imbues."""
    if not _is_lancer(character):
        return {}

    active = state.get("lancer_active_imbues", {})
    riders = {
        "statuses": [],
        "damage_mult": 1.0,
        "extra_statuses": [],
    }

    element_count = len(active)

    # Elemental Harmony (level 30): 2+ elements = +10% damage
    if element_count >= 2 and character.get("level", 1) >= 30:
        riders["damage_mult"] *= 1.10

    # Storm Rider (level 70): Lightning active = +15% damage
    if "lightning" in active and character.get("level", 1) >= 70:
        riders["damage_mult"] *= 1.15

    # Elemental Fusion (level 80): 3+ elements = +25% damage + 2 statuses
    if element_count >= 3 and character.get("level", 1) >= 80:
        riders["damage_mult"] *= 1.25

    # Avatar of Elements (level 100): all 6 elements = +10% damage
    if element_count >= 6 and character.get("level", 1) >= 100:
        riders["damage_mult"] *= 1.10

    # Collect statuses from elements
    for elem_id in active:
        elem_info = LANCER_ELEMENTS.get(elem_id, {})
        status = elem_info.get("status")
        if status and status not in riders["statuses"]:
            riders["statuses"].append(status)

    # fire_earth applies both burning and shaken
    if "fire_earth" in active:
        if "shaken" not in riders["statuses"]:
            riders["statuses"].append("shaken")

    return riders


def _lancer_tick_end_of_turn(state: dict, character: dict, log: list[dict]) -> None:
    """Lancer end-of-turn: tick imbue durations, handle Elemental Cascade, Overload."""
    if not _is_lancer(character):
        return

    active = state.get("lancer_active_imbues", {})
    expired_elements = []

    for elem_id, imbue in list(active.items()):
        imbue["duration"] -= 1
        if imbue["duration"] <= 0:
            # Remove stat mods
            for stat, val in imbue.get("stat_mods", {}).items():
                character["stats"][stat] = character["stats"].get(stat, 0) - val
            del active[elem_id]
            expired_elements.append(elem_id)
            log.append({"kind": "lancer_imbue", "text": f"{LANCER_ELEMENTS.get(elem_id, {}).get('name', elem_id)} imbue fades."})

    # Elemental Cascade (level 60): 50% chance to auto-apply a different element
    if expired_elements and character.get("level", 1) >= 60:
        import random
        if random.random() < 0.50:
            # Pick a random element not currently active
            all_elements = [e for e in LANCER_ELEMENTS if e not in active]
            if all_elements:
                new_elem = random.choice(all_elements)
                # Apply a basic version: just the element flag with 2 turn duration
                duration = 2
                if character.get("level", 1) >= 100:
                    duration += 3
                active[new_elem] = {
                    "skill_id": f"cascade_{new_elem}",
                    "duration": duration,
                    "stat_mods": {},
                }
                log.append({"kind": "lancer_cascade", "text": f"Elemental Cascade — {LANCER_ELEMENTS[new_elem]['name']} imbue auto-applied for {duration} turns!"})

    # Tick Overload
    if state.get("lancer_overload_turns", 0) > 0:
        state["lancer_overload_turns"] -= 1
        if state["lancer_overload_turns"] <= 0:
            # Remove all overload elements
            for elem_id in list(active.keys()):
                imbue = active[elem_id]
                for stat, val in imbue.get("stat_mods", {}).items():
                    character["stats"][stat] = character["stats"].get(stat, 0) - val
                del active[elem_id]
            log.append({"kind": "lancer_overload", "text": "Elemental Overload fades."})


def _lancer_check_overload(state: dict, character: dict, log: list[dict]) -> bool:
    """Check if Elemental Overload (level 90) can be activated. Activates if no imbues active and combat just started."""
    if not _is_lancer(character):
        return False
    if character.get("level", 1) < 90:
        return False
    if state.get("lancer_overload_used") and state.get("lancer_overload_charges", 0) <= 0:
        return False
    # Auto-activate on turn 0 if no imbues
    if state.get("turn", 0) == 0 and not state.get("lancer_active_imbues"):
        state["lancer_overload_used"] = True
        state["lancer_overload_charges"] = max(0, state.get("lancer_overload_charges", 1) - 1)
        state["lancer_overload_turns"] = 2
        # Apply all 6 elements
        for elem_id in ("fire", "ice", "lightning", "earth", "wind", "thunder"):
            state["lancer_active_imbues"][elem_id] = {
                "skill_id": f"overload_{elem_id}",
                "duration": 2,
                "stat_mods": {},
            }
        log.append({"kind": "lancer_overload", "text": "ELEMENTAL OVERLOAD — all 6 elements active for 2 turns!"})
        return True
    return False


def _lancer_check_initiation(state: dict, character: dict, log: list[dict]) -> None:
    """Elemental Initiation (level 10): start combat with one random elemental imbue."""
    if not _is_lancer(character):
        return
    if character.get("level", 1) < 10:
        return
    if state.get("turn", 0) != 0:
        return
    if state.get("lancer_active_imbues"):
        return

    import random
    all_elements = list(LANCER_ELEMENTS.keys())
    elem = random.choice(all_elements)
    duration = 3
    if character.get("level", 1) >= 20:
        duration += 1
    if character.get("level", 1) >= 100:
        duration += 3
    state["lancer_active_imbues"][elem] = {
        "skill_id": f"initiation_{elem}",
        "duration": duration,
        "stat_mods": {},
    }
    log.append({"kind": "lancer_initiation", "text": f"Elemental Initiation — {LANCER_ELEMENTS[elem]['name']} imbue active!"})


# ============================================================
# ASSASSIN COMBAT SYSTEM
# ============================================================

def _is_assassin(character: dict) -> bool:
    return "assassin" in (character.get("masteries") or [])


def _assassin_get_burst_threshold(character: dict) -> int:
    """Get BURST threshold — 100 normally, 75 at level 100."""
    if character.get("level", 1) >= 100:
        return 75
    return 100


def _assassin_get_shadow_threshold_bonus(state: dict, character: dict) -> dict:
    """Get damage/crit/accuracy bonuses from current shadow count."""
    shadows = state.get("assassin_shadows", 0)
    threshold = _assassin_get_burst_threshold(character)

    # Avatar of Shadow (level 100): always minimum 50 shadows
    if character.get("level", 1) >= 100 and shadows < 50:
        shadows = 50

    # Night bonuses: threshold effects doubled (Night Child, level 70)
    is_night = state.get("is_night", False)
    night_mult = 2.0 if (is_night and character.get("level", 1) >= 70) else 1.0

    if shadows >= threshold:
        return {"damage_mult": 3.0, "crit_bonus": 1.0, "accuracy_bonus": 0.15, "burst": True}
    elif shadows >= 75:
        return {"damage_mult": 1.0 + (0.30 * night_mult), "crit_bonus": 0.20 * night_mult, "accuracy_bonus": 0.15 * night_mult, "burst": False}
    elif shadows >= 50:
        return {"damage_mult": 1.0 + (0.20 * night_mult), "crit_bonus": 0.15 * night_mult, "accuracy_bonus": 0.10 * night_mult, "burst": False}
    elif shadows >= 25:
        return {"damage_mult": 1.0 + (0.10 * night_mult), "crit_bonus": 0.10 * night_mult, "accuracy_bonus": 0.05 * night_mult, "burst": False}
    else:
        return {"damage_mult": 1.0 + (0.05 * night_mult), "crit_bonus": 0.05 * night_mult, "accuracy_bonus": 0.0, "burst": False}


def _assassin_gain_shadows(state: dict, character: dict, log: list, amount: int, source: str = "") -> None:
    """Add shadows to the Assassin's count."""
    if not _is_assassin(character):
        return
    old = state.get("assassin_shadows", 0)
    threshold = _assassin_get_burst_threshold(character)
    new_val = min(threshold, old + amount)
    state["assassin_shadows"] = new_val
    if new_val >= threshold and not state.get("assassin_burst_ready"):
        state["assassin_burst_ready"] = True
        log.append({"kind": "assassin_burst_ready", "text": f"SHADOW BURST READY — {new_val} shadows accumulated!"})
    elif amount > 0 and source:
        log.append({"kind": "assassin_shadows", "text": f"+{amount} shadows ({source}) — {new_val}/{threshold}."})


def _assassin_check_burst(state: dict, character: dict, log: list) -> dict:
    """Check if BURST should trigger. Returns burst modifiers."""
    if not _is_assassin(character):
        return {}

    threshold = _assassin_get_burst_threshold(character)
    shadows = state.get("assassin_shadows", 0)

    # Avatar of Shadow (level 100): always minimum 50
    if character.get("level", 1) >= 100 and shadows < 50:
        shadows = 50

    if shadows >= threshold and not state.get("assassin_burst_used"):
        # Trigger BURST
        state["assassin_burst_used"] = True
        state["assassin_burst_ready"] = False

        # Eclipse Mastery (level 90): 4x damage instead of 3x, retain 25 shadows
        burst_mult = 4.0 if character.get("level", 1) >= 90 else 3.0
        # Night: level 100 Eclipse of Shadows = 5x
        is_night = state.get("is_night", False)
        if is_night and character.get("level", 1) >= 90:
            burst_mult = 5.0

        retain = 25 if character.get("level", 1) >= 90 else 0
        state["assassin_shadows"] = retain

        log.append({"kind": "assassin_burst", "text": f"SHADOW BURST — {burst_mult}x damage! Shadows reset to {retain}."})
        return {"burst_mult": burst_mult, "guaranteed_crit": True, "armor_ignore_pct": 0.70}

    return {}


def _assassin_deposit_fear(state: dict, character: dict, monster: dict, log: list, amount: int = 5) -> None:
    """Deposit shadows as fear on the enemy, reducing their stats."""
    if not _is_assassin(character):
        return

    # Shadow Convergence (level 80): at 75+ shadows, fear deposits cost no shadows
    shadows = state.get("assassin_shadows", 0)
    if character.get("level", 1) >= 80 and shadows >= 75:
        # Free deposit — don't reduce shadow count
        pass
    else:
        # Cost: reduce shadow count by deposit amount
        state["assassin_shadows"] = max(0, shadows - amount)

    # Fear Mastery (level 50): 1.5 per shadow instead of 1
    stat_reduction = 1.5 if character.get("level", 1) >= 50 else 1.0
    total_reduction = int(amount * stat_reduction)

    # Apply to monster stats
    m_stats = state.get("monster_stats", {})
    for stat in ("might", "grace", "insight"):
        m_stats[stat] = m_stats.get(stat, 0) - total_reduction

    state["assassin_deposited_shadows"] = state.get("assassin_deposited_shadows", 0) + amount
    log.append({"kind": "assassin_fear", "text": f"Deposited {amount} fear — enemy stats reduced by {total_reduction} each."})


def _assassin_reclaim_shadows(state: dict, character: dict, log: list) -> None:
    """Reclaim deposited shadows on kill."""
    if not _is_assassin(character):
        return

    deposited = state.get("assassin_deposited_shadows", 0)
    if deposited > 0:
        # Shadow Harvest (level 20): +5 bonus shadows per kill
        kill_bonus = 10
        if character.get("level", 1) >= 20:
            kill_bonus += 5
        total = deposited + kill_bonus
        _assassin_gain_shadows(state, character, log, total, f"kill reclaim ({deposited} fear + {kill_bonus} kill bonus)")
        state["assassin_deposited_shadows"] = 0

        # Shadow Step (level 60): 50% chance to re-enter hidden after kill
        if character.get("level", 1) >= 60:
            import random
            chance = 0.75 if state.get("is_night") else 0.50
            if random.random() < chance:
                _append_status_dedup(state, make_status("hidden"), key="player_statuses")
                log.append({"kind": "assassin_passive", "text": "SHADOW STEP — re-entered stealth after kill!"})


def _assassin_apply_threshold_bonuses(state: dict, character: dict, total_dmg: float, outcome: int) -> tuple[float, int]:
    """Apply shadow threshold damage and crit bonuses. Returns (modified_damage, modified_outcome)."""
    if not _is_assassin(character):
        return total_dmg, outcome

    bonuses = _assassin_get_shadow_threshold_bonus(state, character)
    total_dmg = int(total_dmg * bonuses["damage_mult"])

    # Shadow Precision (level 30): +1% accuracy per 10 shadows → boost outcome
    shadows = state.get("assassin_shadows", 0)
    if character.get("level", 1) >= 100 and shadows < 50:
        shadows = 50
    if character.get("level", 1) >= 30:
        acc_bonus = shadows // 10
        outcome = min(6, outcome + (acc_bonus // 5))  # +1 outcome per 50 shadows

    # Shadow Crit (level 40): +10% crit damage at 50+, +20% at 75+
    if character.get("level", 1) >= 40 and shadows >= 75:
        total_dmg = int(total_dmg * 1.20)
    elif character.get("level", 1) >= 40 and shadows >= 50:
        total_dmg = int(total_dmg * 1.10)

    return total_dmg, outcome


def _assassin_tick_end_of_turn(state: dict, character: dict, log: list) -> None:
    """Assassin end-of-turn: night shadow generation, tick buffs."""
    if not _is_assassin(character):
        return

    # Night: passive shadow generation
    is_night = state.get("is_night", False)
    if is_night:
        night_gen = 5 if character.get("level", 1) >= 70 else 3
        _assassin_gain_shadows(state, character, log, night_gen, "night passive")

    # Tick shadow linger (evasion after stealth break)
    if state.get("assassin_shadow_linger", 0) > 0:
        state["assassin_shadow_linger"] -= 1
        if state["assassin_shadow_linger"] <= 0:
            log.append({"kind": "assassin_passive", "text": "Shadow linger fades."})

    # Tick Assassin self stat_mods
    tick_stat_mods(state, "assassin_self_stat_mods", character["stats"])

    # Tick Assassin enemy stat_mods
    assassin_enemy = state.get("assassin_enemy_stat_mods", [])
    active_assassin_enemy = []
    for entry in assassin_enemy:
        if entry["duration"] > 0:
            active_assassin_enemy.append(entry)
        else:
            for stat, val in entry["mods"].items():
                m_stats = state.get("monster_stats", {})
                m_stats[stat] = m_stats.get(stat, 0) - val
    state["assassin_enemy_stat_mods"] = active_assassin_enemy
    for entry in state.get("assassin_enemy_stat_mods", []):
        entry["duration"] -= 1


# ============================================================
# HUNTER COMBAT SYSTEM
# ============================================================

def _is_hunter(character: dict) -> bool:
    return "hunter" in (character.get("masteries") or [])


def _hunter_get_communion_threshold(character: dict) -> int:
    """Spirit Communion triggers at stack 10 normally, 8 at level 70, 6 at level 100."""
    if character.get("level", 1) >= 100:
        return 6
    if character.get("level", 1) >= 70:
        return 8
    return 10


def _get_weapon_range_for_combat(character: dict) -> int:
    """Get the range value from the character's equipped weapon (new item system).
    Returns 0 for melee weapons, 1+ for ranged weapons."""
    equipped = character.get("equipped", {})
    best_range = 0
    for hand in ("left_hand", "right_hand"):
        item_ref = equipped.get(hand)
        if not item_ref:
            continue
        item = _get_equipped_item(character, hand)
        if not item:
            item = ITEMS_BY_ID.get(item_ref)
        if not item:
            continue
        # New-style item: use 'range' field
        if "range" in item:
            best_range = max(best_range, int(item["range"]))
        # Old-style item: map by ID
        elif item.get("id") in ("oak_shortbow", "ashwood_longbow"):
            best_range = max(best_range, 2)
    return best_range


def _get_monster_range(monster: dict) -> int:
    """Get the range value from a monster. Defaults to 0 (melee)."""
    return int(monster.get("range", 0))


def _compute_range_gap(character: dict, monster: dict) -> int:
    """Compute the range gap: max(0, player_range - monster_range).
    A positive gap means the player can hit but the monster can't reach yet."""
    player_range = _get_weapon_range_for_combat(character)
    monster_range = _get_monster_range(monster)
    return max(0, player_range - monster_range)


def _hunter_get_starting_range(character: dict) -> int:
    """Hunter starting Range = weapon range + passive bonuses.
    Dagger = 0 (melee), Bow = 3, etc.
    Quick Draw (level 20): +1. Legend of the Hunt (level 100): +2."""
    r = _get_weapon_range_for_combat(character)
    if character.get("level", 1) >= 20:
        r += 1  # Quick Draw
    if character.get("level", 1) >= 100:
        r += 2  # Legend of the Hunt (bow 3 + 2 = 5)
    return r


def _hunter_gain_guidance(state: dict, character: dict, log: list, amount: int = 1) -> None:
    """Add Spirit Guidance stacks on hit.
    Ancient Tracker communion: +2 per hit (replaces base +1).
    Tracking Instinct communion: +1 additional per hit on target."""
    if not _is_hunter(character):
        return

    # Ancient Tracker communion: +2 per hit instead of +1
    if state.get("hunter_ancient_tracker_active"):
        amount = max(amount, 2)

    # Tracking Instinct communion: +1 additional per hit
    if state.get("hunter_tracking_instinct_active"):
        amount += 1

    old = state.get("hunter_spirit_guidance", 0)
    new_val = old + amount

    # Legend of the Hunt (level 100): no cap
    if character.get("level", 1) < 100:
        new_val = min(99, new_val)  # cap just below communion to allow communion trigger

    state["hunter_spirit_guidance"] = new_val

    # Check communion trigger
    threshold = _hunter_get_communion_threshold(character)
    if new_val >= threshold and not state.get("hunter_spirit_communion"):
        state["hunter_spirit_communion"] = True
        # Ancestor's Voice (level 70): +2 stacks on communion trigger
        if character.get("level", 1) >= 70:
            state["hunter_spirit_guidance"] = new_val + 2
            new_val = new_val + 2
        # Spirit Touched (level 30) communion: +10 permanent cognition
        if character.get("level", 1) >= 30:
            character["stats"]["cognition"] = character["stats"].get("cognition", 0) + 10
        log.append({"kind": "hunter_communion", "text": f"SPIRIT COMMUNION — {new_val} stacks! The ancestors join the fight!"})


def _hunter_get_crit_chance(state: dict, character: dict) -> float:
    """Get current crit chance from Spirit Guidance."""
    stacks = state.get("hunter_spirit_guidance", 0)
    threshold = _hunter_get_communion_threshold(character)

    # Keen Eye (level 10): +7% per hit instead of +5%
    # At communion: +12% per hit
    if state.get("hunter_spirit_communion"):
        per_stack = 0.12 if character.get("level", 1) >= 10 else 0.05
    else:
        per_stack = 0.07 if character.get("level", 1) >= 10 else 0.05

    crit_chance = stacks * per_stack

    # At communion (stack 10+): 100% crit chance
    if stacks >= threshold:
        crit_chance = 1.0

    return min(1.0, crit_chance)


def _hunter_get_crit_damage_mult(state: dict, character: dict) -> float:
    """Get crit damage multiplier from Spirit Guidance."""
    stacks = state.get("hunter_spirit_guidance", 0)
    threshold = _hunter_get_communion_threshold(character)

    base = 1.5  # standard crit
    # Eagle Vision (level 50): +25% baseline crit damage
    if character.get("level", 1) >= 50:
        base += 0.25
    # Legend of the Hunt (level 100): +200% at communion
    if character.get("level", 1) >= 100 and state.get("hunter_spirit_communion"):
        base += 2.0
    # Eagle Vision communion: +50% baseline
    if character.get("level", 1) >= 50 and state.get("hunter_spirit_communion"):
        base += 0.25

    # Above threshold: +10% crit damage per stack above threshold
    if stacks >= threshold:
        above = stacks - threshold
        base += above * 0.10

    return base


def _hunter_get_hit_count(state: dict, character: dict, skill: dict) -> int:
    """Get number of hits for a skill, accounting for passives and communion."""
    base_hits = skill.get("hits", 1)

    # Spirit Communion upgrades
    if state.get("hunter_spirit_communion"):
        sc = skill.get("spirit_communion", "")
        if "hits: 3" in sc and base_hits == 2:
            base_hits = 3
        elif "hits: 5" in sc and base_hits < 5:
            base_hits = 5
        elif "10_hits" in sc:
            base_hits = 10

    # Master Marksman (level 90): +1 hit, +2 at communion
    if character.get("level", 1) >= 90:
        base_hits += 2 if state.get("hunter_spirit_communion") else 1

    return base_hits


def _hunter_apply_range_modifier(state: dict, character: dict, skill: dict, log: list) -> None:
    """Apply Range modifier from skill.
    Ghost Step (level 60): Spirit Walk grants +2 additional Range."""
    range_mod = skill.get("range_modifier", 0)
    if range_mod > 0:
        # Ghost Step (level 60): Spirit Walk grants +2 extra Range
        if skill.get("id") == "spirit_walk" and character.get("level", 1) >= 60:
            range_mod += 2
        # Spirit Communion: some skills get +1 or +2 range
        if state.get("hunter_spirit_communion"):
            sc = skill.get("spirit_communion", "")
            if "+2_range" in sc or "+3_range" in sc:
                range_mod += 1
        _hunter_add_range(state, range_mod, log)


def _hunter_add_range(state: dict, amount: int, log: list) -> None:
    """Add range to hunter and sync with unified range system."""
    state["hunter_range"] = state.get("hunter_range", 0) + amount
    state["player_range"] = state.get("player_range", 0) + amount
    state["range_gap"] = state["player_range"] - state.get("monster_range", 0)
    log.append({"kind": "hunter_range", "text": f"+{amount} Range — enemy must close {state['hunter_range']} more turns."})


def _hunter_check_ambush(state: dict, character: dict, log: list) -> None:
    """Check for Ambush on first attack from stealth."""
    if state.get("hunter_ambush_used"):
        return

    is_hidden = any(s.get("name") == "hidden" for s in state.get("player_statuses", []))
    if is_hidden:
        state["hunter_ambush_used"] = True
        # +1 Range from ambush
        _hunter_add_range(state, 1, log)
        # Legend of the Hunt (level 100): 2 guaranteed crits
        crits = 2 if character.get("level", 1) >= 100 else 1
        state["hunter_guaranteed_crits"] = crits
        log.append({"kind": "hunter_ambush", "text": f"AMBUSH — {crits} guaranteed critical hit(s)! +1 Range!"})


def _hunter_apply_communion_effects(state: dict, character: dict, skill: dict, log: list, total_dmg: float, outcome: int) -> tuple[float, int]:
    """Apply Spirit Communion effects on damage. Returns (modified_damage, modified_outcome).
    Each skill has a unique communion upgrade — behavioral, not just bigger numbers."""
    if not state.get("hunter_spirit_communion"):
        return total_dmg, outcome

    sc = skill.get("spirit_communion", "")
    sid = skill.get("id", "")

    # --- Rapid Shot: 3 hits, third deals magical (handled in hit count; communion adds magical bonus) ---
    if sid == "rapid_shot" and "third_hit_deals_magical" in sc:
        total_dmg = int(total_dmg * 1.2)  # third hit magical bonus
        log.append({"kind": "hunter_communion", "text": "Ancestor's arrow — magical third strike!"})

    # --- Piercing Shot: true damage, ignores all armor ---
    if "ignores_all_armor" in sc:
        total_dmg = int(total_dmg * 1.5)
        log.append({"kind": "hunter_communion", "text": "Spirit arrow phases through all defense!"})

    # --- Snare Trap: ensnared + silenced ---
    if sid == "snare_trap" and "silenced" in sc:
        _append_status_dedup(state, make_status("silenced"), key="monster_statuses")
        log.append({"kind": "hunter_communion", "text": "Ancestor's grip silences the enemy!"})

    # --- Camouflage: summons spirit copy decoy ---
    if sid == "camouflage" and "summons_spirit_copy_decoy" in sc:
        state["hunter_spirit_copy_active"] = True
        log.append({"kind": "hunter_communion", "text": "A spirit copy stands in your place!"})

    # --- Crippling Shot: spirit root, can't act, +1 range ---
    if sid == "crippling_shot" and "cant_act" in sc:
        _append_status_dedup(state, make_status("stunned"), key="monster_statuses")  # can't act = stunned
        _hunter_add_range(state, 1, log)
        log.append({"kind": "hunter_communion", "text": "Spirit root — enemy paralyzed! +1 Range!"})

    # --- Poison Arrow: uncleansable spirit venom (true DoT, can't cleanse) ---
    if sid == "poison_arrow" and "uncleansable" in sc:
        # Upgrade existing poison to uncleansable spirit venom
        for s in state.get("monster_statuses", []):
            if s.get("name") == "poisoned":
                s["uncleansable"] = True
                s["name"] = "spirit_venom"
                break
        log.append({"kind": "hunter_communion", "text": "Spirit venom — uncleansable, ignores resistance!"})

    # --- Flash Bang: stunned + blinded + confused, +1 range ---
    if sid == "flash_bang" and "blinded" in sc:
        _append_status_dedup(state, make_status("blinded"), key="monster_statuses")
        _append_status_dedup(state, make_status("confused"), key="monster_statuses")
        _hunter_add_range(state, 1, log)
        log.append({"kind": "hunter_communion", "text": "Spirit flash — blinded, confused! +1 Range!"})

    # --- Twin Shot: 3 hits, bleeding can't be stopped ---
    if sid == "twin_shot" and "bleeding_cant_be_stopped" in sc:
        for s in state.get("monster_statuses", []):
            if s.get("name") == "bleeding":
                s["uncleansable"] = True
                break
        log.append({"kind": "hunter_communion", "text": "Spirit bleeding — the wound won't close!"})

    # --- Smoke Bomb: +2 range, all allies hidden ---
    if sid == "smoke_bomb" and "all_allies_hidden" in sc:
        _hunter_add_range(state, 1, log)  # extra +1 (total +2)
        log.append({"kind": "hunter_communion", "text": "Spirit fog — all allies hidden! +2 Range!"})

    # --- Hunter's Mark: all allies gain crit against target ---
    if sid == "hunters_mark" and "all_allies_gain_crit" in sc:
        state["hunter_marked_target"] = True  # all allies get +20% crit vs this target
        log.append({"kind": "hunter_communion", "text": "Spirit mark — all allies see the target's weaknesses!"})

    # --- Falcon Strike: spirit falcon persists 2 turns ---
    if sid == "falcon_strike" and "persists_2_turns" in sc:
        state["hunter_spirit_falcon_turns"] = 2
        log.append({"kind": "hunter_communion", "text": "Spirit falcon circles — attacks for 2 turns!"})

    # --- Spirit Walk: intangible 2 turns, +3 range, heal 5% ---
    if sid == "spirit_walk" and "intangible_2_turns" in sc:
        state["hunter_intangible_turns"] = 2
        _hunter_add_range(state, 1, log)  # extra +1 (total +3)
        heal_amt = int(character.get("max_hp", 100) * 0.05)
        character["hp"] = min(character.get("max_hp", 999), character["hp"] + heal_amt)
        log.append({"kind": "hunter_communion", "text": f"Spirit world mends you — +{heal_amt} HP, intangible 2 turns, +3 Range!"})

    # --- Rain of Arrows: 5 hits, all unevadable ---
    if sid == "rain_of_arrows" and "unevadable" in sc:
        outcome = max(5, outcome)  # can't be evaded = guaranteed hit
        log.append({"kind": "hunter_communion", "text": "Ancestor-guided arrows — unevadable!"})

    # --- Wolf Companion: spirit wolf persists 3 turns ---
    if sid == "wolf_companion" and "persists_3_turns" in sc:
        state["hunter_spirit_wolf_turns"] = 3
        log.append({"kind": "hunter_communion", "text": "Spirit wolf circles — attacks for 3 turns!"})

    # --- Explosive Trap: true damage, hits all enemies ---
    if sid == "explosive_trap" and "true_damage" in sc and "hits_all_enemies" in sc:
        total_dmg = int(total_dmg * 1.5)  # true damage bonus
        log.append({"kind": "hunter_communion", "text": "Spirit explosion — true damage, hits all enemies!"})

    # --- Hawk Vision: guaranteed crits 3 turns, see through stealth ---
    if sid == "hawk_vision" and "sees_through_stealth" in sc:
        state["hunter_sees_stealth"] = 3  # 3 turns of stealth vision
        log.append({"kind": "hunter_communion", "text": "Spirit sight — sees through all stealth!"})

    # --- Backflip: +3 range, spirit copy absorbs next hit ---
    if sid == "backflip" and "leaves_spirit_copy_behind" in sc:
        _hunter_add_range(state, 1, log)  # extra +1 (total +3)
        state["hunter_spirit_copy_active"] = True
        state["hunter_spirit_copy_absorb"] = True  # copy will absorb next hit
        log.append({"kind": "hunter_communion", "text": "Spirit copy left behind — absorbs next hit! +3 Range!"})

    # --- Monster Slayer: true damage, execute threshold 20% ---
    if "execute_threshold_20_percent" in sc:
        total_dmg = int(total_dmg * 1.5)  # true damage bonus
        monster_hp = state.get("monster_hp", 0)
        monster_max = state.get("monster_max_hp", 1)
        if monster_hp > 0 and (monster_hp / monster_max) <= 0.20:
            total_dmg = monster_hp  # instant kill
            log.append({"kind": "hunter_execute", "text": "EXECUTE — the ancestors cut the thread!"})

    # --- Bear Trap: spirit jaws, +2 range ---
    if sid == "bear_trap" and "pulled_toward_hunter" in sc:
        _hunter_add_range(state, 2, log)
        log.append({"kind": "hunter_communion", "text": "Spirit jaws drag the enemy away! +2 Range!"})

    # --- Volley Master: 5 hits, each different debuff ---
    if sid == "volley_master" and "different_debuff" in sc:
        for debuff in ["bleeding", "poisoned", "ensnared", "shaken", "silenced"]:
            _append_status_dedup(state, make_status(debuff), key="monster_statuses")
        log.append({"kind": "hunter_communion", "text": "Five arrows, five curses — bleeding, poison, snare, shaken, silence!"})

    # --- Spirit Bind: spirit prison, can't act, true DoT, +2 range ---
    if sid == "spirit_bind" and "spirit_prison" in sc:
        _append_status_dedup(state, make_status("stunned"), key="monster_statuses")  # can't act
        state["hunter_spirit_prison_active"] = True  # true damage per turn
        _hunter_add_range(state, 2, log)
        log.append({"kind": "hunter_communion", "text": "Spirit prison — enemy trapped, draining! +2 Range!"})

    # --- Storm Arrow: true damage, chains to nearby enemies ---
    if "chains_to_nearby_enemies" in sc:
        total_dmg = int(total_dmg * 1.5)  # true damage + chain bonus
        log.append({"kind": "hunter_communion", "text": "Spirit lightning chains through all enemies!"})

    # --- Nature's Blessing: cleanse debuffs, heal 25%, +2 range ---
    if sid == "natures_blessing" and "cleanses_all_debuffs" in sc:
        cleansed = []
        for s in list(character.get("statuses", [])):
            if s.get("kind") == "debuff":
                cleansed.append(s.get("name", "debuff"))
                character["statuses"].remove(s)
        heal_extra = int(character.get("max_hp", 100) * 0.10)  # extra 10% (total 25%)
        character["hp"] = min(character.get("max_hp", 999), character["hp"] + heal_extra)
        _hunter_add_range(state, 2, log)
        if cleansed:
            log.append({"kind": "hunter_communion", "text": f"Spirit + forest cleanse: {', '.join(cleansed)}! +{heal_extra} HP, +2 Range!"})
        else:
            log.append({"kind": "hunter_communion", "text": f"Spirit + forest heal: +{heal_extra} HP, +2 Range!"})

    # --- Survival Instinct: immune 1 turn, +3 range, spirit copy absorbs hit ---
    if sid == "survival_instinct" and "immune_1_turn" in sc:
        state["hunter_immune_turns"] = 1  # full immunity
        _hunter_add_range(state, 3, log)
        state["hunter_spirit_copy_active"] = True
        state["hunter_spirit_copy_absorb"] = True
        log.append({"kind": "hunter_communion", "text": "Ancestors shield you — immune 1 turn, +3 Range, copy absorbs hits!"})

    # --- Alpha Command: spirit bow, 3 true damage strikes (already handled via charges) ---
    if sid == "alpha_command" and "true_damage" in sc:
        state["hunter_spirit_bow_charges"] = 3
        log.append({"kind": "hunter_communion", "text": "Spirit Bow — next 3 strikes deal true damage!"})

    # --- Ancient Tracker: +2 guidance per hit ---
    if sid == "ancient_tracker" and "gains_2_per_hit" in sc:
        state["hunter_ancient_tracker_active"] = True
        log.append({"kind": "hunter_communion", "text": "Ancestors learn twice as fast — +2 Guidance per hit!"})

    # --- Tracking Instinct: enemy can't evade, +1 guidance per hit on target ---
    if sid == "tracking_instinct" and "cant_evade" in sc:
        state["hunter_tracking_instinct_active"] = True
        log.append({"kind": "hunter_communion", "text": "Enemy can't evade — every arrow finds its mark!"})

    # --- World Hunt: infinite range, repeats every turn ---
    if "repeats_every_turn" in sc or "enemy_cant_escape" in sc:
        state["hunter_world_hunt_active"] = True
        state["hunter_infinite_range"] = True
        log.append({"kind": "hunter_communion", "text": "World Hunt — infinite range, the hunt never ends!"})

    # --- Legend of the Wild: 10 hits, party inspired, reset guidance to 20 ---
    if sid == "legend_of_the_wild" and "ancestor_army" in sc:
        _append_status_dedup(character, make_status("inspired"))
        state["hunter_spirit_guidance"] = 20
        log.append({"kind": "hunter_communion", "text": "Ancestor army — 10 true strikes! Party inspired! Guidance reset to 20!"})

    return total_dmg, outcome


def _hunter_tick_end_of_turn(state: dict, character: dict, log: list) -> None:
    """Hunter end-of-turn: World Hunt repeat, tick stat mods,
    spirit falcon/wolf attacks, spirit prison DoT, intangible/immune ticks.
    Range decrease is handled by the unified range system."""
    if not _is_hunter(character):
        return

    # Spirit Guidance breaks when the Hunter's concentration does.
    #
    # This reset was never implemented, which left Unbreakable Focus (L80) —
    # "Spirit Guidance doesn't reset when stunned" — guarding against something
    # that could not happen, so the passive was a no-op. Both halves are here now:
    # losing a hard-won stack count to a stun is a real vulnerability, and the
    # L80 passive is what removes it.
    stacks = state.get("hunter_spirit_guidance", 0)
    if stacks > 0:
        level = character.get("level", 1)
        breaking = []
        if _has_player_status(character, state, "stunned"):
            breaking.append("stunned")
        # Communion tier of the passive also covers silence.
        if _has_player_status(character, state, "silenced"):
            breaking.append("silenced")
        if breaking:
            if level >= 80:
                log.append({"kind": "hunter_passive",
                            "text": "UNBREAKABLE FOCUS — Spirit Guidance holds through "
                                    f"{breaking[0]}!"})
            else:
                state["hunter_spirit_guidance"] = 0
                log.append({"kind": "hunter_guidance_lost",
                            "text": f"Concentration broken — Spirit Guidance reset from {stacks} "
                                    f"to 0 ({breaking[0]})."})

    # World Hunt repeat (communion): auto-attack
    if state.get("hunter_world_hunt_active") and state.get("monster_hp", 0) > 0:
        repeat_dmg = int(character["stats"].get("grace", 10) * 0.5)
        state["monster_hp"] = max(0, state["monster_hp"] - repeat_dmg)
        _hunter_gain_guidance(state, character, log, 1)
        log.append({"kind": "hunter_world_hunt", "text": f"World Hunt repeats — {repeat_dmg} true damage!"})

    # Spirit Falcon (communion): attacks independently for 2 turns
    falcon_t = state.get("hunter_spirit_falcon_turns", 0)
    if falcon_t > 0 and state.get("monster_hp", 0) > 0:
        falcon_dmg = int(character["stats"].get("grace", 10) * 0.3)
        state["monster_hp"] = max(0, state["monster_hp"] - falcon_dmg)
        _hunter_gain_guidance(state, character, log, 1)
        log.append({"kind": "hunter_spirit_falcon", "text": f"Spirit falcon dives — {falcon_dmg} damage!"})
        state["hunter_spirit_falcon_turns"] = falcon_t - 1

    # Spirit Wolf (communion): attacks independently for 3 turns
    wolf_t = state.get("hunter_spirit_wolf_turns", 0)
    if wolf_t > 0 and state.get("monster_hp", 0) > 0:
        wolf_dmg = int(character["stats"].get("grace", 10) * 0.4)
        state["monster_hp"] = max(0, state["monster_hp"] - wolf_dmg)
        _hunter_gain_guidance(state, character, log, 1)
        log.append({"kind": "hunter_spirit_wolf", "text": f"Spirit wolf lunges — {wolf_dmg} damage!"})
        state["hunter_spirit_wolf_turns"] = wolf_t - 1

    # Spirit Prison (communion): true damage per turn
    if state.get("hunter_spirit_prison_active") and state.get("monster_hp", 0) > 0:
        prison_dmg = int(character["stats"].get("grace", 10) * 0.3)
        state["monster_hp"] = max(0, state["monster_hp"] - prison_dmg)
        log.append({"kind": "hunter_spirit_prison", "text": f"Spirit prison drains — {prison_dmg} true damage!"})

    # Tick intangible turns
    if state.get("hunter_intangible_turns", 0) > 0:
        state["hunter_intangible_turns"] -= 1
        if state["hunter_intangible_turns"] <= 0:
            log.append({"kind": "hunter_intangible", "text": "You phase back into the material world."})

    # Tick immune turns
    if state.get("hunter_immune_turns", 0) > 0:
        state["hunter_immune_turns"] -= 1

    # Tick sees_stealth
    if state.get("hunter_sees_stealth", 0) > 0:
        state["hunter_sees_stealth"] -= 1

    # Spirit of the Wild (legendary quest): permanent spirit copy casts Spirit Bind every 3 turns
    if state.get("hunter_spirit_copy_active") and "spirit_of_the_wild" in (character.get("quest_passives") or []):
        spirit_bind_cd = state.get("hunter_spirit_copy_bind_cd", 0)
        if spirit_bind_cd > 0:
            state["hunter_spirit_copy_bind_cd"] = spirit_bind_cd - 1
        elif state.get("monster_hp", 0) > 0:
            _append_status_dedup(state, make_status("ensnared"), key="monster_statuses")
            state["hunter_spirit_copy_bind_cd"] = 3
            log.append({"kind": "hunter_spirit_copy", "text": "Spirit Copy casts Spirit Bind — the ancestor holds the enemy!"})

    # Tick guaranteed crits
    # (these are consumed on use, not ticked)

    # Tick Hunter self stat_mods
    tick_stat_mods(state, "hunter_self_stat_mods", character["stats"])

    # Tick Hunter enemy stat_mods
    hunter_enemy = state.get("hunter_enemy_stat_mods", [])
    active_hunter_enemy = []
    for entry in hunter_enemy:
        if entry["duration"] > 0:
            active_hunter_enemy.append(entry)
        else:
            for stat, val in entry["mods"].items():
                m_stats = state.get("monster_stats", {})
                m_stats[stat] = m_stats.get(stat, 0) - val
    state["hunter_enemy_stat_mods"] = active_hunter_enemy
    for entry in state.get("hunter_enemy_stat_mods", []):
        entry["duration"] -= 1


# ============================================================
# ROGUE COMBAT SYSTEM
# ============================================================

def _is_rogue(character: dict) -> bool:
    return "rogue" in (character.get("masteries") or [])


def _rogue_get_innate_slots(character: dict) -> int:
    """Base 5 slots, +1 at level 10 (Trickster's Eye), +1 at level 100 (Master of Tricks)."""
    slots = 5
    if character.get("level", 1) >= 10:
        slots += 1
    if character.get("level", 1) >= 100:
        slots += 1
    return slots


def _rogue_get_equipped_innates(character: dict) -> list[str]:
    """Return list of equipped innate skill IDs."""
    return character.get("rogue_innate_equipped", [])


def _rogue_has_innate(character: dict, innate_id: str) -> bool:
    """Check if a specific innate skill is equipped."""
    return innate_id in _rogue_get_equipped_innates(character)


def _rogue_init_combat(state: dict, character: dict, log: list) -> None:
    """Initialize Rogue-specific combat state."""
    if not _is_rogue(character):
        return

    level = character.get("level", 1)

    # Second Story: +5 permanent grace (applied as stat mod)
    if _rogue_has_innate(character, "second_story"):
        character["stats"]["grace"] = character["stats"].get("grace", 0) + 5
        log.append({"kind": "rogue_innate", "text": "Second Story — +5 permanent Grace!"})

    # Trap Master: first strike applies ensnared
    if _rogue_has_innate(character, "trap_master"):
        charges = 2 if level >= 70 else 1
        if level >= 100:  # Master of Tricks: double charges
            charges *= 2
        state["rogue_trap_master_charges"] = charges

    # Lucky Dodger: stacking evasion
    state["rogue_lucky_dodger_stacks"] = 0

    # Quick Hands: act first
    state["rogue_quick_hands"] = _rogue_has_innate(character, "quick_hands")

    # Dirty Fighter: random debuff on strikes
    state["rogue_dirty_fighter"] = _rogue_has_innate(character, "dirty_fighter")
    df_count = 2 if level >= 40 else 1  # Dirty Mastery at 40
    if level >= 100:  # Master of Tricks: double debuff count
        df_count *= 2
    state["rogue_dirty_fighter_count"] = df_count

    # Counter Strike
    state["rogue_counter_strike"] = _rogue_has_innate(character, "counter_strike")
    state["rogue_counter_threshold"] = 4 if level >= 50 else 3  # Counter Precision at 50
    counter_mult = 0.75 if level >= 50 else 0.5
    if level >= 100:  # Master of Tricks: double counter damage
        counter_mult *= 2
    state["rogue_counter_multiplier"] = counter_mult

    # Opportunist: +30% damage vs debuffed
    state["rogue_opportunist"] = _rogue_has_innate(character, "opportunist")

    # Slippery: chance to shake debuffs
    state["rogue_slippery"] = _rogue_has_innate(character, "slippery")
    state["rogue_slippery_chance"] = 0.50 if level >= 90 else 0.25

    # Con Artist: debuffs last +1 turn (+2 at level 80)
    state["rogue_con_artist"] = _rogue_has_innate(character, "con_artist")
    state["rogue_con_artist_bonus"] = 2 if level >= 80 else 1

    # Light Feet: immune to ensnared
    state["rogue_light_feet"] = _rogue_has_innate(character, "light_feet")

    # Master of Tricks: double all innate effects at level 100
    state["rogue_master_of_tricks"] = level >= 100
    state["_rogue_level"] = level
    state["rogue_adaptive_used"] = False


def _rogue_apply_dirty_fighter(state: dict, log: list) -> None:
    """Apply random debuff(s) from Dirty Fighter innate on strike."""
    if not state.get("rogue_dirty_fighter"):
        return

    import random
    debuffs = ["shaken", "bleeding", "blinded"]
    count = state.get("rogue_dirty_fighter_count", 1)

    for _ in range(count):
        debuff = random.choice(debuffs)
        monster_statuses = state.setdefault("monster_statuses", [])
        if not any(s.get("id") == debuff for s in monster_statuses):
            st = make_status(debuff)
            if state.get("rogue_con_artist"):
                st["duration"] += _rogue_get_con_artist_bonus(state)
            _append_status_dedup(state, st, key="monster_statuses")
            log.append({"kind": "rogue_dirty_fighter", "text": f"Dirty Fighter — {debuff.title()} applied!"})


def _rogue_check_counter_strike(state: dict, character: dict, log: list, enemy_roll: int) -> None:
    """Check if Counter Strike triggers on enemy's dice roll."""
    if not state.get("rogue_counter_strike"):
        return

    threshold = state.get("rogue_counter_threshold", 3)
    if enemy_roll <= threshold:
        weapon_dmg = character["stats"].get("might", 10) * state.get("rogue_counter_multiplier", 0.5)
        counter_dmg = int(weapon_dmg)
        state["monster_hp"] = max(0, state.get("monster_hp", 0) - counter_dmg)
        log.append({"kind": "rogue_counter", "text": f"Counter Strike — enemy rolled {enemy_roll}! Free counter for {counter_dmg} damage!"})


def _rogue_check_lucky_dodger(state: dict, log: list, enemy_missed: bool) -> None:
    """Handle Lucky Dodger stacking evasion on enemy miss."""
    if state.get("rogue_lucky_dodger_stacks") is None:
        return  # innate not equipped

    level = state.get("_rogue_level", 1)
    if enemy_missed:
        bonus = 10 if state.get("rogue_master_of_tricks") else 5
        if level >= 60:  # Evasion Training passive
            bonus = 20 if state.get("rogue_master_of_tricks") else 10
        state["rogue_lucky_dodger_stacks"] = state.get("rogue_lucky_dodger_stacks", 0) + bonus
        log.append({"kind": "rogue_lucky_dodger", "text": f"Lucky Dodger — +{bonus}% evasion! Total: +{state['rogue_lucky_dodger_stacks']}%"})
    else:
        if state.get("rogue_lucky_dodger_stacks", 0) > 0:
            log.append({"kind": "rogue_lucky_dodger", "text": "Lucky Dodger stacks reset — you were hit!"})
        state["rogue_lucky_dodger_stacks"] = 0


def _rogue_get_opportunist_bonus(state: dict) -> float:
    """Return damage multiplier from Opportunist innate if enemy has status."""
    if not state.get("rogue_opportunist"):
        return 1.0
    monster_statuses = state.get("monster_statuses", [])
    if monster_statuses:
        bonus = 1.6 if state.get("rogue_master_of_tricks") else 1.3
        return bonus
    return 1.0


def _rogue_check_light_feet(state: dict, character: dict, log: list) -> bool:
    """Check if Light Feet prevents ensnared on the player. Returns True if blocked."""
    if not state.get("rogue_light_feet"):
        return False
    player_statuses = state.get("player_statuses", [])
    ensnared = [s for s in player_statuses if s.get("id") == "ensnared" or s.get("name") == "ensnared"]
    if ensnared:
        for s in ensnared:
            player_statuses.remove(s)
        log.append({"kind": "rogue_light_feet", "text": "Light Feet — immune to Ensnared! Trap broken!"})
        return True
    return False


def _rogue_slippery_tick(state: dict, log: list) -> None:
    """Slippery innate: chance to shake off a debuff each turn."""
    if not state.get("rogue_slippery"):
        return

    import random
    chance = state.get("rogue_slippery_chance", 0.25)
    # Slippery Soul (L90): the Slippery innate shakes debuffs at 50% instead of 25%.
    if state.get("_rogue_level", 1) >= 90:
        chance = max(chance, 0.50)
    if state.get("rogue_master_of_tricks"):
        chance = min(1.0, chance * 2)

    player_statuses = state.get("player_statuses", [])
    if player_statuses and random.random() < chance:
        removed = player_statuses.pop(0)
        log.append({"kind": "rogue_slippery", "text": f"Slippery — shook off {removed.get('name', 'a debuff')}!"})


def _rogue_get_con_artist_bonus(state: dict) -> int:
    """Return extra duration for debuffs applied by Rogue."""
    if not state.get("rogue_con_artist"):
        return 0
    bonus = state.get("rogue_con_artist_bonus", 1)
    # Con Master (L80): Con Artist grants +2 turns instead of +1.
    if state.get("_rogue_level", 1) >= 80:
        bonus = max(bonus, 2)
    if state.get("rogue_master_of_tricks"):
        bonus *= 2
    return bonus


def _rogue_apply_trap_master(state: dict, log: list) -> None:
    """Apply Trap Master innate on first strike(s)."""
    charges = state.get("rogue_trap_master_charges", 0)
    if charges <= 0:
        return

    monster_statuses = state.setdefault("monster_statuses", [])
    if not any(s.get("id") == "ensnared" for s in monster_statuses):
        st = make_status("ensnared")
        st["duration"] += _rogue_get_con_artist_bonus(state)
        _append_status_dedup(state, st, key="monster_statuses")
        state["rogue_trap_master_charges"] = charges - 1
        log.append({"kind": "rogue_trap_master", "text": "Trap Master — Ensnared applied on first strike!"})


def _rogue_tick_end_of_turn(state: dict, character: dict, log: list) -> None:
    """Rogue end-of-turn processing."""
    if not _is_rogue(character):
        return

    # Slippery: chance to shake debuffs
    _rogue_slippery_tick(state, log)

    # Light Feet: check and remove ensnared
    _rogue_check_light_feet(state, character, log)

    # Tick Rogue self stat_mods
    tick_stat_mods(state, "rogue_self_stat_mods", character["stats"])

    # Tick Rogue enemy stat_mods
    tick_stat_mods(state, "rogue_enemy_stat_mods", state.setdefault("monster_stats", {}))


def _rogue_on_strike(state: dict, character: dict, log: list) -> None:
    """Called when Rogue lands a strike. Applies Trap Master and Dirty Fighter."""
    if not _is_rogue(character):
        return

    # Trap Master on first strike(s)
    _rogue_apply_trap_master(state, log)

    # Dirty Fighter: random debuff
    _rogue_apply_dirty_fighter(state, log)


def _rogue_get_evasion_bonus(state: dict) -> int:
    """Get total evasion bonus from Lucky Dodger stacks."""
    return state.get("rogue_lucky_dodger_stacks", 0)


# ============================================================
# BARD COMBAT SYSTEM
# ============================================================

def _is_bard(character: dict) -> bool:
    return "bard" in (character.get("masteries") or [])


def _bard_init_combat(state: dict, character: dict, log: list):
    """Initialize Bard combat state at turn 0."""
    if not _is_bard(character):
        return
    state["bard_mode"] = "song"  # default to song mode
    state["bard_crescendo"] = 0
    state["bard_active_performances"] = []  # list of active performance skill ids
    state["bard_encore_turns"] = 0
    state["bard_encore_performance"] = None
    state["bard_death_save_used"] = False
    state["bard_death_save_active"] = False
    state["bard_cc_immune"] = False
    state["bard_unevadable"] = False
    state["bard_silenced_enemy"] = False
    state["bard_friendly_fire"] = False
    state["bard_friendly_fire_chance"] = 0.0
    state["bard_confuse"] = False
    state["bard_confuse_chance"] = 0.0
    state["bard_pull_mesmerize"] = False
    state["bard_burn_dpt"] = 0.0
    state["bard_stun_chance"] = 0.0
    state["bard_reroll"] = False
    state["bard_cooldown_reset"] = False
    state["bard_all_rules"] = False
    state["bard_total_control"] = False
    # Check for Voice of the World quest passive
    quest_passives = character.get("quest_passives", [])
    state["bard_voice_of_world"] = "voice_of_the_world" in quest_passives
    # Charismatic (level 30): +10 permanent grace
    state["bard_charismatic"] = character.get("level", 0) >= 30
    if state["bard_charismatic"]:
        character["stats"]["grace"] = character["stats"].get("grace", 0) + 10
    # Unbreakable Voice (level 80): crescendo doesn't reset when stunned
    state["bard_unbreakable_voice"] = character.get("level", 0) >= 80
    # Legend of the Stage (level 100): performances can't be silenced
    state["bard_legend_of_stage"] = character.get("level", 0) >= 100
    # Crowd Pleaser (level 70): visual-only, Crescendo at +1 stack
    state["bard_crowd_pleaser"] = character.get("level", 0) >= 70


def _bard_get_crescendo_max(character: dict) -> int:
    """Get max crescendo stacks based on passives."""
    base = 5
    # Resonant (level 50): max 7
    if character.get("level", 0) >= 50:
        base = 7
    # Legend of the Stage (level 100): max 10
    if character.get("level", 0) >= 100:
        base = 10
    return base


def _bard_get_encore_chance(character: dict) -> float:
    """Get encore chance based on passives."""
    base = 0.20
    if character.get("level", 0) >= 40:
        base += 0.15  # Harmonic
    if character.get("level", 0) >= 90:
        base += 0.30  # Masterful Encore
    return min(base, 1.0)


def _bard_get_performance_chance(character: dict, base_chance: float, crescendo: int, crescendo_scale: float) -> float:
    """Calculate performance effect chance with Crescendo and Tuned Ear passive."""
    chance = base_chance + (crescendo * crescendo_scale)
    if character.get("level", 0) >= 10:
        chance += 0.10  # Tuned Ear
    return min(chance, 1.0)


def _bard_tick_crescendo(state: dict, character: dict, log: list):
    """Process active performances at start of turn, build Crescendo, apply effects."""
    if not _is_bard(character):
        return

    # --- Reset transient performance flags before re-applying ---
    state["bard_unevadable"] = False
    state["bard_cc_immune"] = False
    state["bard_silenced_enemy"] = False
    state["bard_friendly_fire"] = False
    state["bard_friendly_fire_chance"] = 0.0
    state["bard_confuse"] = False
    state["bard_confuse_chance"] = 0.0
    state["bard_pull_mesmerize"] = False
    state["bard_burn_dpt"] = 0.0
    state["bard_stun_chance"] = 0.0
    state["bard_reroll"] = False
    state["bard_cooldown_reset"] = False
    state["bard_death_save_active"] = False

    # Tick Bard ally stat_mods
    bard_ally = state.get("bard_ally_stat_mods", [])
    active_ally = []
    for entry in bard_ally:
        if entry["duration"] > 0:
            active_ally.append(entry)
        else:
            for stat, val in entry["mods"].items():
                character["stats"][stat] = character["stats"].get(stat, 0) - val
    state["bard_ally_stat_mods"] = active_ally
    for entry in state.get("bard_ally_stat_mods", []):
        entry["duration"] -= 1

    # Tick Bard enemy stat_mods
    tick_stat_mods(state, "bard_enemy_stat_mods", state.setdefault("monster_stats", {}))

    crescendo = state.get("bard_crescendo", 0)
    crescendo_max = _bard_get_crescendo_max(character)

    # Check if player is stunned or silenced — resets crescendo
    player_statuses = state.get("player_statuses", character.get("statuses", []))
    is_stunned = any(s.get("id") == "stunned" for s in player_statuses)
    is_silenced = any(s.get("id") == "silenced" for s in player_statuses)
    # Legend of the Stage (level 100): performances can't be silenced
    if is_silenced and state.get("bard_legend_of_stage"):
        is_silenced = False
    if is_silenced:
        crescendo = 0
        log.append({"kind": "bard_crescendo_reset", "text": "Silenced — Crescendo resets!"})
    elif is_stunned and not state.get("bard_unbreakable_voice"):
        crescendo = 0
        log.append({"kind": "bard_crescendo_reset", "text": "Stunned — Crescendo resets!"})

    # Crescendo only builds while the Bard is actually performing.
    #
    # It used to build every single turn regardless, so a Bard who never played a
    # note still reached max Crescendo — which contradicts the mastery's whole
    # identity. Seven skills declare `crescendo: True` and the frontend advertises
    # it, but the engine never read the field; this is what makes it load-bearing.
    active_perfs = state.get("bard_active_performances", []) or []
    building = any(
        (SKILLS_BY_ID.get(pid) or {}).get("crescendo")
        for pid in active_perfs
    )
    if building:
        # Steady Rhythm (level 20): +2/turn instead of +1
        gain = 2 if character.get("level", 0) >= 20 else 1
        crescendo = min(crescendo + gain, crescendo_max)
        state["bard_crescendo"] = crescendo
        if crescendo > 0:
            log.append({"kind": "bard_crescendo", "text": f"Crescendo builds to {crescendo}!"})
    else:
        state["bard_crescendo"] = crescendo
        if crescendo > 0:
            log.append({"kind": "bard_crescendo",
                        "text": f"No performance active — Crescendo holds at {crescendo}."})

    # Ensure encore performance stays in active list while encore lasts
    encore_turns = state.get("bard_encore_turns", 0)
    encore_perf = state.get("bard_encore_performance")
    active_perfs = state.get("bard_active_performances", [])
    if encore_turns > 0 and encore_perf and encore_perf not in active_perfs:
        active_perfs.append(encore_perf)
        state["bard_active_performances"] = active_perfs

    if not active_perfs:
        return
    mode = state.get("bard_mode", "song")
    voice_of_world = state.get("bard_voice_of_world", False)

    for perf_id in active_perfs:
        sk = SKILLS_BY_ID.get(perf_id)
        if not sk:
            continue
        base_chance = sk.get("base_chance", 0.10)
        crescendo_scale = sk.get("crescendo_scale", 0.05)
        chance = _bard_get_performance_chance(character, base_chance, crescendo, crescendo_scale)

        # Apply effects based on mode
        modes_to_process = [mode]
        if voice_of_world:
            modes_to_process = ["song", "dance"]

        for m in modes_to_process:
            if m == "song":
                _bard_apply_song_effect(state, character, sk, chance, log)
            elif m == "dance":
                _bard_apply_dance_effect(state, character, sk, chance, log)

    # Accumulate stun_chance from active performances
    total_stun = 0.0
    for perf_id in active_perfs:
        sk = SKILLS_BY_ID.get(perf_id)
        if sk and sk.get("stun_chance"):
            total_stun += sk["stun_chance"]
    if total_stun > 0:
        state["bard_stun_chance"] = min(total_stun * (1 + crescendo * 0.1), 0.75)

    # bard_cooldown_reset flag — reset all cooldowns each turn while active
    if state.get("bard_cooldown_reset"):
        for sid in state.get("skill_cooldowns", {}):
            state["skill_cooldowns"][sid] = 0
        log.append({"kind": "bard_song", "text": "The music flows — all cooldowns reset!"})

    # Tick encore duration
    if encore_turns > 0:
        state["bard_encore_turns"] = encore_turns - 1
        if state["bard_encore_turns"] <= 0:
            state["bard_encore_performance"] = None
            log.append({"kind": "bard_encore_end", "text": "The encore fades."})

    # Heal from performances with heal_percent
    for perf_id in active_perfs:
        sk = SKILLS_BY_ID.get(perf_id)
        if sk and sk.get("heal_percent"):
            heal_amt = int(character["max_hp"] * sk["heal_percent"])
            character["hp"] = min(character["max_hp"], character["hp"] + heal_amt)
            log.append({"kind": "bard_heal", "text": f"The performance heals {heal_amt} HP!"})

    # Burn DPT from performances
    burn_dpt = state.get("bard_burn_dpt", 0.0)
    if burn_dpt > 0:
        dmg = int(state["monster_max_hp"] * burn_dpt * (1 + crescendo * 0.1))
        state["monster_hp"] = max(0, state["monster_hp"] - dmg)
        log.append({"kind": "bard_burn", "text": f"The music burns the enemy for {dmg} true damage!"})

    # Stun chance from performances
    stun_chance = state.get("bard_stun_chance", 0.0)
    if stun_chance > 0 and random.random() < stun_chance:
        _append_status_dedup(state, make_status("stunned"), key="monster_statuses")
        log.append({"kind": "bard_stun", "text": "The performance stuns the enemy!"})


def _bard_apply_song_effect(state: dict, character: dict, sk: dict, chance: float, log: list):
    """Apply a Bard song effect."""
    effect = sk.get("song_effect", "")
    if effect == "physical_attacks_unevadable":
        state["bard_unevadable"] = True
        log.append({"kind": "bard_song", "text": "Song of Heroes — ally physical attacks cannot be evaded!"})
    elif effect == "death_save":
        state["bard_death_save_used"] = False  # reset each turn (one save per turn)
        state["bard_death_save_active"] = True
        log.append({"kind": "bard_song", "text": "Song of Hope — death save active! Allies survive lethal damage."})
    elif effect == "cooldown_reset":
        if random.random() < chance:
            # Reset a random cooldown
            cds = state.get("skill_cooldowns", {})
            if cds:
                sid = random.choice(list(cds.keys()))
                state["skill_cooldowns"][sid] = 0
                log.append({"kind": "bard_song", "text": f"Song of Wisdom — {sid} cooldown reset!"})
    elif effect == "cc_immune":
        state["bard_cc_immune"] = True
        log.append({"kind": "bard_song", "text": "Song of Freedom — allies immune to crowd control!"})
    elif effect == "reroll":
        state["bard_reroll"] = True
        log.append({"kind": "bard_song", "text": "Song of Fortune — enemy's worst die will be rerolled!"})
    elif effect == "all_rules_active":
        state["bard_unevadable"] = True
        state["bard_death_save_active"] = True
        state["bard_cc_immune"] = True
        state["bard_reroll"] = True
        state["bard_cooldown_reset"] = True
        log.append({"kind": "bard_song", "text": "Requiem — all song rules active! Allies are invincible!"})
    elif effect == "rewrite_existence":
        state["bard_unevadable"] = True
        state["bard_death_save_active"] = True
        state["bard_cc_immune"] = True
        state["bard_reroll"] = True
        state["bard_cooldown_reset"] = True
        # Reset all cooldowns
        for sid in state.get("skill_cooldowns", {}):
            state["skill_cooldowns"][sid] = 0
        log.append({"kind": "bard_song", "text": "Symphony — the rules of existence are rewritten! All cooldowns reset!"})


def _bard_apply_dance_effect(state: dict, character: dict, sk: dict, chance: float, log: list):
    """Apply a Bard dance effect."""
    effect = sk.get("dance_effect", "")
    if effect == "confuse":
        state["bard_confuse"] = True
        state["bard_confuse_chance"] = max(state.get("bard_confuse_chance", 0.0), chance)
        log.append({"kind": "bard_dance", "text": "Dance — the enemy is confused!"})
    elif effect == "pull_mesmerize":
        state["bard_pull_mesmerize"] = True
        if random.random() < chance:
            _append_status_dedup(state, make_status("mesmerized"), key="monster_statuses")
            log.append({"kind": "bard_dance", "text": "Dance — the enemy is mesmerized!"})
    elif effect == "silence":
        if random.random() < chance:
            _append_status_dedup(state, make_status("silenced"), key="monster_statuses")
            state["bard_silenced_enemy"] = True
            log.append({"kind": "bard_dance", "text": "Dance — the enemy is silenced!"})
    elif effect == "friendly_fire":
        state["bard_friendly_fire"] = True
        state["bard_friendly_fire_chance"] = max(state.get("bard_friendly_fire_chance", 0.0), chance)
        log.append({"kind": "bard_dance", "text": "Dance — the enemy attacks its own allies!"})
    elif effect == "burn":
        dpt = sk.get("dpt_percent", 0.05)
        state["bard_burn_dpt"] = max(state.get("bard_burn_dpt", 0.0), dpt)
        log.append({"kind": "bard_dance", "text": f"Dance — the enemy burns for {int(dpt*100)}% true damage per turn!"})
    elif effect == "total_control":
        state["bard_confuse"] = True
        state["bard_confuse_chance"] = max(state.get("bard_confuse_chance", 0.0), chance)
        state["bard_pull_mesmerize"] = True
        state["bard_silenced_enemy"] = True
        state["bard_friendly_fire"] = True
        state["bard_friendly_fire_chance"] = max(state.get("bard_friendly_fire_chance", 0.0), chance)
        dpt = sk.get("dpt_percent", 0.08)
        state["bard_burn_dpt"] = max(state.get("bard_burn_dpt", 0.0), dpt)
        log.append({"kind": "bard_dance", "text": "Requiem Dance — total control! Confuse, silence, burn, friendly fire!"})
    elif effect == "total_domination":
        state["bard_confuse"] = True
        state["bard_confuse_chance"] = 1.0  # guaranteed at legendary
        state["bard_pull_mesmerize"] = True
        state["bard_silenced_enemy"] = True
        state["bard_friendly_fire"] = True
        state["bard_friendly_fire_chance"] = 1.0  # guaranteed at legendary
        dpt = sk.get("dpt_percent", 0.12)
        state["bard_burn_dpt"] = max(state.get("bard_burn_dpt", 0.0), dpt)
        if sk.get("status_apply") == "mesmerized":
            _append_status_dedup(state, make_status("mesmerized"), key="monster_statuses")
        log.append({"kind": "bard_dance", "text": "Symphony Dance — total domination! The enemy has no autonomy!"})


def _bard_process_performance(state: dict, character: dict, sk: dict, log: list):
    """Process a Bard performance skill when used."""
    mode = state.get("bard_mode", "song")
    voice_of_world = state.get("bard_voice_of_world", False)

    # Add to active performances
    active = state.get("bard_active_performances", [])
    if sk["id"] not in active:
        active.append(sk["id"])
    state["bard_active_performances"] = active

    # Immediate effects
    crescendo = state.get("bard_crescendo", 0)
    base_chance = sk.get("base_chance", 0.10)
    crescendo_scale = sk.get("crescendo_scale", 0.05)
    chance = _bard_get_performance_chance(character, base_chance, crescendo, crescendo_scale)

    modes_to_process = [mode]
    if voice_of_world:
        modes_to_process = ["song", "dance"]

    for m in modes_to_process:
        if m == "song":
            _bard_apply_song_effect(state, character, sk, chance, log)
        elif m == "dance":
            _bard_apply_dance_effect(state, character, sk, chance, log)

    # Encore check — only for skills that declare they can encore. The field was
    # declared on 7 skills and shown in the UI but never read by the engine, so
    # every performance could encore regardless of what the client advertised.
    encore_chance = _bard_get_encore_chance(character) if sk.get("encore") else 0.0
    if crescendo >= _bard_get_crescendo_max(character) and character.get("level", 0) >= 100:
        if sk.get("encore"):
            encore_chance = 1.0  # guaranteed at max crescendo with Legend of the Stage
    if encore_chance > 0 and random.random() < encore_chance:
        encore_duration = 2 if character.get("level", 0) >= 90 else 1
        state["bard_encore_turns"] = encore_duration
        state["bard_encore_performance"] = sk["id"]
        log.append({"kind": "bard_encore", "text": f"Encore! The performance lingers for {encore_duration} more turn(s)!"})


def _bard_apply_all_allies_stat_mod(character: dict, stat_mod: dict, log: list):
    """Apply all_allies stat_mod to the player (since we only have 1 player in MVP)."""
    allies_mod = stat_mod.get("all_allies")
    if not allies_mod:
        return
    # In MVP, the player is the only ally, so apply to self
    if "stat_mods" not in character:
        character["stat_mods"] = []
    character["stat_mods"].append({"mod": allies_mod, "turns_remaining": 3})
    log.append({"kind": "bard_buff", "text": "The performance empowers all allies!"})


def _bard_switch_mode(state: dict, character: dict, new_mode: str, log: list) -> bool:
    """Switch Bard performance mode. Returns True if successful."""
    if new_mode not in ("song", "dance"):
        return False
    old_mode = state.get("bard_mode", "song")
    if old_mode == new_mode:
        return False
    state["bard_mode"] = new_mode
    # Legend of the Stage (level 100): instant switch, no crescendo loss
    if character.get("level", 0) >= 100:
        log.append({"kind": "bard_mode_switch", "text": f"Mode switched to {new_mode.title()}! Crescendo unchanged ({state.get('bard_crescendo', 0)})."})
    # Free Reprise (level 60): keep 50% crescendo
    elif character.get("level", 0) >= 60:
        state["bard_crescendo"] = int(state.get("bard_crescendo", 0) * 0.5)
        log.append({"kind": "bard_mode_switch", "text": f"Mode switched to {new_mode.title()}! Crescendo retained at {state['bard_crescendo']}."})
    else:
        state["bard_crescendo"] = 0
        log.append({"kind": "bard_mode_switch", "text": f"Mode switched to {new_mode.title()}! Crescendo reset."})
    return True


def _bard_check_death_save(state: dict, character: dict, damage: int, log: list) -> int:
    """Check if Bard death save prevents lethal damage. Returns modified damage."""
    if not state.get("bard_death_save_active"):
        return damage
    if character["hp"] - damage <= 0 and not state.get("bard_death_save_used"):
        state["bard_death_save_used"] = True
        # Scale save threshold with Crescendo: 1 HP at 0, up to 25% max HP at max crescendo
        crescendo = state.get("bard_crescendo", 0)
        crescendo_max = _bard_get_crescendo_max(character)
        save_hp = max(1, int(character["max_hp"] * 0.25 * (crescendo / crescendo_max))) if crescendo_max > 0 else 1
        log.append({"kind": "bard_death_save", "text": f"Song of Hope — death save! Lethal damage prevented, surviving at {save_hp} HP!"})
        return max(0, character["hp"] - save_hp)
    return damage


def _bard_check_cc_immune(state: dict, status_id: str, log: list) -> bool:
    """Check if Bard CC immunity blocks a status. Returns True if blocked."""
    if not state.get("bard_cc_immune"):
        return False
    cc_statuses = {"stunned", "shaken", "ensnared", "blind", "bind", "mesmerized", "silenced", "confused"}
    if status_id in cc_statuses:
        log.append({"kind": "bard_cc_immune", "text": f"Song of Freedom — immune to {status_id}!"})
        return True
    return False


# ============================================================
# DRUID COMBAT SYSTEM
# ============================================================

def _is_druid(character: dict) -> bool:
    return "druid" in (character.get("masteries") or [])


def _druid_get_max_summons(character: dict) -> int:
    """Max active summons: 1 per 5 Druid levels.
    Pack Leader (level 20): +1 max summon above cap.
    Alpha World (level 100): cap removed (20 summons at L100)."""
    level = character.get("level", 1)
    base = level // 5
    if level >= 20:  # Pack Leader
        base += 1
    if level >= 100:  # Alpha World — no hard cap
        return base
    return min(10, base)


def _druid_init_combat(state: dict, character: dict, log: list):
    """Initialize Druid combat state at turn 0."""
    if not _is_druid(character):
        return
    state["druid_active_summons"] = []       # list of summon dicts
    state["druid_fusion_active"] = False
    state["druid_fusion_turns"] = 0
    state["druid_fusion_summon_id"] = None
    state["druid_fusion_cooldowns"] = {}     # {summon_id: turns_remaining}
    state["druid_pack_synergy"] = None       # computed each turn
    # Twin Fusion (level 60): can fuse with 2 summons simultaneously
    state["druid_multi_fusion"] = character.get("level", 0) >= 60
    # Eternal Bond (level 80): dead summons can be re-summoned same combat
    state["druid_dead_summons"] = {}         # {creature_id: turns_until_resummon}
    # Season system
    state["druid_season"] = "spring"         # default season
    state["druid_season_cooldown"] = 0       # turns until season can be switched


def _compute_creature_stat(stat_entry, level: int) -> int:
    """Compute a creature stat at a given level.
    stat_entry can be: int (legacy flat), or {"base": X, "growth": Y} dict.
    Formula: Base × (1 + Growth × (Level - 1) / 10)
    At level 1, stat = base. Growth scales linearly per 10 levels.
    """
    if isinstance(stat_entry, dict):
        base = stat_entry.get("base", 5)
        growth = stat_entry.get("growth", 1.0)
        return int(base * (1 + growth * (level - 1) / 10))
    return stat_entry  # legacy flat value


def _compute_creature_stats(creature: dict, level: int) -> dict:
    """Compute all 6 stats for a creature at the given level."""
    raw_stats = creature.get("stats", {})
    computed = {}
    for stat_name in ("might", "grace", "cognition", "insight", "essence", "durability"):
        if stat_name in raw_stats:
            computed[stat_name] = _compute_creature_stat(raw_stats[stat_name], level)
        else:
            computed[stat_name] = raw_stats.get(stat_name, 5)
    return computed


def _compute_creature_hp(creature: dict, level: int) -> int:
    """Compute creature HP at a given level.
    Uses the monster's base HP field scaled by level.
    Formula: base_hp × (1 + 0.15 × (Level - 1))
    At level 1, HP = base_hp. ~2.3x at level 10, ~8.4x at level 50.
    """
    base_hp = creature.get("hp", 20)
    return int(base_hp * (1 + 0.15 * (level - 1)))


def _normalize_passive_buff(buff) -> list:
    """Normalize passive_buff to a list of buff dicts.
    Normal creatures store a single dict; boss+ store a list."""
    if buff is None:
        return []
    if isinstance(buff, list):
        return buff
    if isinstance(buff, dict):
        result = [buff]
        # Handle secondary buff inside the dict
        secondary = buff.get("secondary")
        if secondary and isinstance(secondary, dict):
            result.append(secondary)
        return result
    return []


def _normalize_signature_fusion(sig) -> list:
    """Normalize signature_fusion to a list of sig dicts.
    Normal creatures store a single dict; boss+ store a list."""
    if sig is None:
        return []
    if isinstance(sig, list):
        return sig
    if isinstance(sig, dict):
        return [sig]
    return []


def _apply_passive_buffs_to_character(character: dict, buffs: list):
    """Apply passive buff list to character stats in-place."""
    for buff in buffs:
        btype = buff.get("type", "")
        value = buff.get("value", 0)
        if btype in ("might_bonus", "grace_bonus", "cognition_bonus", "insight_bonus",
                      "essence_bonus", "durability_bonus"):
            stat_name = btype.replace("_bonus", "")
            character["stats"][stat_name] = int(
                character["stats"].get(stat_name, 0) * (1.0 + value))
        elif btype == "armor_bonus":
            character["stats"]["armor_bonus"] = character["stats"].get("armor_bonus", 0) + int(value * 10)
        elif btype == "evasion_bonus":
            character["stats"]["grace"] = int(
                character["stats"].get("grace", 0) * (1.0 + value))
        elif btype == "crit_chance":
            character["stats"]["insight"] = int(
                character["stats"].get("insight", 0) * (1.0 + value * 0.5))
        elif btype == "magic_resist":
            character["stats"]["essence"] = int(
                character["stats"].get("essence", 0) * (1.0 + value * 0.5))
        # lifesteal, poison_chance, ensnare_chance, regen, double_attack
        # are handled as combat flags, not stat modifications


def _remove_passive_buffs_from_character(character: dict, buffs: list):
    """Reverse passive buff application (when summon dies or is unsummoned)."""
    for buff in buffs:
        btype = buff.get("type", "")
        value = buff.get("value", 0)
        if btype in ("might_bonus", "grace_bonus", "cognition_bonus", "insight_bonus",
                      "essence_bonus", "durability_bonus"):
            stat_name = btype.replace("_bonus", "")
            character["stats"][stat_name] = int(
                character["stats"].get(stat_name, 0) / (1.0 + value))
        elif btype == "armor_bonus":
            character["stats"]["armor_bonus"] = character["stats"].get("armor_bonus", 0) - int(value * 10)
        elif btype == "evasion_bonus":
            character["stats"]["grace"] = int(
                character["stats"].get("grace", 0) / (1.0 + value))
        elif btype == "crit_chance":
            character["stats"]["insight"] = int(
                character["stats"].get("insight", 0) / (1.0 + value * 0.5))
        elif btype == "magic_resist":
            character["stats"]["essence"] = int(
                character["stats"].get("essence", 0) / (1.0 + value * 0.5))


def _compute_pack_synergy(active_summons: list, character: dict | None = None) -> dict | None:
    """Compute pack synergy bonuses based on number of active summons.
    Base thresholds: 3+ = Pack Bond, 5+ = Pack Hunt, 7+ = Pack Alpha, 10 = Wild Sovereign.
    Sovereign's Will (level 70): thresholds reduced to 2/4/6/9.
    Wild Sovereign (level 90): all bonuses doubled.
    """
    count = len(active_summons)
    level = character.get("level", 1) if character else 1

    # Sovereign's Will (level 70): lower thresholds
    if level >= 70:
        t_bond, t_hunt, t_alpha, t_sovereign = 2, 4, 6, 9
    else:
        t_bond, t_hunt, t_alpha, t_sovereign = 3, 5, 7, 10

    if count < t_bond:
        return None
    synergy = {
        "name": "Pack Bond",
        "count": count,
        "summon_damage_mult": 1.0,
        "extra_hits": 0,
        "extra_action_every_other": False,
        "extra_action_every": False,
        "druid_stat_mult": 1.0,
        "share_buffs": False,
    }
    if count >= t_bond:
        synergy["name"] = "Pack Bond"
        synergy["summon_damage_mult"] = 1.20
        synergy["druid_stat_mult"] = 1.05
    if count >= t_hunt:
        synergy["name"] = "Pack Hunt"
        synergy["extra_hits"] = 1
        synergy["druid_stat_mult"] = 1.10
    if count >= t_alpha:
        synergy["name"] = "Pack Alpha"
        synergy["extra_action_every_other"] = True
        synergy["druid_stat_mult"] = 1.15
    if count >= t_sovereign:
        synergy["name"] = "The Wild Sovereign"
        synergy["share_buffs"] = True
        synergy["druid_stat_mult"] = 1.20

    # Wild Sovereign passive (level 90): double all bonuses
    if level >= 90:
        synergy["summon_damage_mult"] = 1.0 + (synergy["summon_damage_mult"] - 1.0) * 2
        synergy["extra_hits"] *= 2
        synergy["druid_stat_mult"] = 1.0 + (synergy["druid_stat_mult"] - 1.0) * 2
        if synergy["extra_action_every_other"]:
            synergy["extra_action_every_other"] = False
            synergy["extra_action_every"] = True  # upgraded to every turn
        synergy["share_buffs"] = True  # double-shared

    return synergy


def _druid_summon_creature(character: dict, state: dict, bestiary_entry: dict, log: list) -> dict:
    """Summon a tamed creature from the bestiary onto the battlefield."""
    max_summons = _druid_get_max_summons(character)
    active = state.get("druid_active_summons", [])

    if len(active) >= max_summons:
        return {"error": f"Max active summons reached ({max_summons})."}

    creature_id = bestiary_entry["id"]
    # No duplicates
    if any(s["id"] == creature_id for s in active):
        return {"error": f"{bestiary_entry['name']} is already summoned."}

    # Check fusion cooldown
    cooldowns = state.get("druid_fusion_cooldowns", {})
    if cooldowns.get(creature_id, 0) > 0:
        return {"error": f"{bestiary_entry['name']} is recovering from fusion ({cooldowns[creature_id]} turns)."}

    # Eternal Bond (level 80): dead summons can be re-summoned same combat after 1 turn cooldown
    dead_summons = state.get("druid_dead_summons", {})
    if creature_id in dead_summons:
        return {"error": f"{bestiary_entry['name']} was defeated this combat. Resummon available in {dead_summons[creature_id]} turn(s)."}

    level = character.get("level", 1)
    computed_stats = _compute_creature_stats(bestiary_entry, level)
    max_hp = _compute_creature_hp(bestiary_entry, level)

    # Normalize buffs and skills
    buffs = _normalize_passive_buff(bestiary_entry.get("passive_buff"))
    sigs = _normalize_signature_fusion(bestiary_entry.get("signature_fusion"))

    profile_skills = bestiary_entry.get("profile_skills", {})
    if not profile_skills or not any(profile_skills.values()):
        # Fallback: use flat skills list
        flat = bestiary_entry.get("skills", [])
        profile_skills = {"attack": [], "defense": [], "utility": []}
        for sk in flat:
            cat = _classify_skill(sk)
            profile_skills[cat].append(sk)

    summon = {
        "id": creature_id,
        "name": bestiary_entry["name"],
        "creature_tier": bestiary_entry.get("creature_tier", "normal"),
        "level": level,
        "hp": max_hp,
        "max_hp": max_hp,
        "stats": computed_stats,
        "profile_skills": profile_skills,
        "signature_fusion": sigs,
        "passive_buff": buffs,
        "personality": bestiary_entry.get("personality", "aggressive"),
        "mode": "auto",
        "formation": None,
        "boss_aura": bestiary_entry.get("boss_aura"),
        "legendary_passive": bestiary_entry.get("legendary_passive"),
        "skill_cooldowns": {},
        "mp": 0,
        "stamina": 100,
        "fused": False,
        "extra_action_this_turn": False,
    }

    active.append(summon)
    state["druid_active_summons"] = active

    # Apply passive buffs to character
    _apply_passive_buffs_to_character(character, buffs)

    # Recompute pack synergy
    state["druid_pack_synergy"] = _compute_pack_synergy(active, character)

    log.append({
        "kind": "druid_summon",
        "text": f"You summon {bestiary_entry['name']}! (Active: {len(active)}/{max_summons})"
    })

    synergy = state.get("druid_pack_synergy")
    if synergy:
        log.append({
            "kind": "druid_pack_synergy",
            "text": f"{synergy['name']} active — {synergy['count']} summons on the field!"
        })

    return {"success": True, "summon": summon}
def _druid_unsummon_creature(character: dict, state: dict, creature_id: str, log: list) -> dict:
    """Unsummon a creature (remove from battlefield, return to bestiary)."""
    active = state.get("druid_active_summons", [])
    summon = next((s for s in active if s["id"] == creature_id), None)
    if not summon:
        return {"error": "That creature is not currently summoned."}
    if summon.get("fused"):
        return {"error": f"{summon['name']} is fused with you — cannot unsummon."}

    # Remove passive buffs
    _remove_passive_buffs_from_character(character, summon.get("passive_buff", []))
    active = [s for s in active if s["id"] != creature_id]
    state["druid_active_summons"] = active
    state["druid_pack_synergy"] = _compute_pack_synergy(active, character)

    log.append({"kind": "druid_unsummon", "text": f"You unsummon {summon['name']}."})
    return {"success": True}


def _druid_pick_summon_skill(summon: dict, state: dict, character: dict, turn: int) -> dict | None:
    """Pick a skill for a summon based on its personality and Auto AI rules.
    Returns the skill dict or None (pass)."""
    profile = summon.get("profile_skills", {})
    if not profile or not any(profile.values()):
        return None

    personality = summon.get("personality", "aggressive")
    s_hp_ratio = summon["hp"] / max(1, summon["max_hp"])
    enemy_hp_ratio = state.get("monster_hp", 1) / max(1, state.get("monster_max_hp", 1))
    druid_hp_ratio = character.get("hp", 1) / max(1, character.get("max_hp", 1))
    cooldowns = summon.get("skill_cooldowns", {})
    mp = summon.get("mp", 0)
    stamina = summon.get("stamina", 100)

    def _usable(skills):
        result = []
        for sk in skills:
            sid = sk.get("id", "")
            if cooldowns.get(sid, 0) > 0:
                continue
            if sk.get("cost_mp", 0) > mp:
                continue
            if sk.get("cost_stamina", 0) > stamina:
                continue
            result.append(sk)
        return result

    attack = _usable(profile.get("attack", []))
    defense = _usable(profile.get("defense", []))
    utility = _usable(profile.get("utility", []))

    if not attack and not defense and not utility:
        return None

    # Standard Auto AI priority (modified by personality):
    # 1. Enemy above 30% HP → Attack
    # 2. Enemy below 30% HP → Attack (kill)
    # 3. Druid below 50% HP → Defense
    # 4. Summon below 30% HP → Utility

    def _pick_best(skills):
        if not skills:
            return None
        # Pick highest power skill
        best = None
        best_score = -1
        for sk in skills:
            ptype = sk.get("power_type", "strike")
            if ptype == "strike":
                score = sk.get("damage", 5) + sk.get("hits", 1) * 3
            elif ptype == "heal":
                score = sk.get("damage", 10) + 20
            elif ptype == "buff":
                score = 15
            elif ptype == "debuff":
                score = 10
            else:
                score = 5
            if score > best_score:
                best = sk
                best_score = score
        return best

    # Personality overrides
    if personality == "aggressive":
        # Always prefers Attack; Defense only when Druid < 30%; Utility only when summon < 15%
        if attack:
            return _pick_best(attack)
        if druid_hp_ratio < 0.30 and defense:
            return _pick_best(defense)
        if s_hp_ratio < 0.15 and utility:
            return _pick_best(utility)
        return _pick_best(defense or utility or [])

    elif personality == "protective":
        # Defense check comes FIRST — when any ally < 70% HP
        if druid_hp_ratio < 0.70 and defense:
            return _pick_best(defense)
        if attack:
            return _pick_best(attack)
        return _pick_best(utility or defense or [])

    elif personality == "opportunist":
        # Uses Utility proactively when enemy < 50%
        if enemy_hp_ratio < 0.50 and utility:
            return _pick_best(utility)
        if attack:
            return _pick_best(attack)
        if s_hp_ratio < 0.30 and utility:
            return _pick_best(utility)
        return _pick_best(defense or utility or [])

    elif personality == "guardian":
        # Turn 1: always Defense; then alternate Attack/Defense
        if turn == 0 and defense:
            return _pick_best(defense)
        if turn % 2 == 1 and defense:
            return _pick_best(defense)
        if attack:
            return _pick_best(attack)
        return _pick_best(defense or utility or [])

    elif personality == "taunting":
        # Defense when self < 60%; attacks only after defense
        if s_hp_ratio < 0.60 and defense:
            return _pick_best(defense)
        if attack:
            return _pick_best(attack)
        return _pick_best(defense or utility or [])

    # Standard AI (no personality override)
    if attack:
        return _pick_best(attack)
    if druid_hp_ratio < 0.50 and defense:
        return _pick_best(defense)
    if s_hp_ratio < 0.30 and utility:
        return _pick_best(utility)
    return _pick_best(defense or utility or [])


def _druid_execute_summon_action(summon: dict, state: dict, character: dict, log: list, synergy: dict | None) -> dict:
    """Execute a summon's action against the monster. Returns result dict."""
    sk = _druid_pick_summon_skill(summon, state, character, state.get("turn", 0))
    if not sk:
        log.append({"kind": "druid_summon_pass", "text": f"{summon['name']} holds its position."})
        return {"action": "pass"}

    # Set cooldown
    sid = sk.get("id", "")
    cd = sk.get("cooldown", 1)
    summon.setdefault("skill_cooldowns", {})[sid] = cd

    # Deduct resources
    summon["mp"] = max(0, summon.get("mp", 0) - sk.get("cost_mp", 0))
    summon["stamina"] = max(0, summon.get("stamina", 100) - sk.get("cost_stamina", 0))

    ptype = sk.get("power_type", "strike")
    s_stats = summon.get("stats", {})

    if ptype in ("strike", "debuff"):
        # Deal damage to monster
        base_power = sk.get("damage", 5)
        might = s_stats.get("might", 5)
        dmg = int(base_power + might * 0.8)

        # Pack synergy damage bonus
        if synergy:
            dmg = int(dmg * synergy.get("summon_damage_mult", 1.0))

        # Druid boss aura: magic damage boost
        magic_boost = state.get("druid_aura_magic_boost", 0)
        if magic_boost > 0 and sk.get("damage_type") == "magical":
            dmg = int(dmg * (1.0 + magic_boost))

        # Extra hits from synergy
        hits = sk.get("hits", 1)
        if synergy:
            hits += synergy.get("extra_hits", 0)

        total_dmg = 0
        for _ in range(hits):
            hit_dmg = max(1, dmg + random.randint(-2, 2))
            total_dmg += hit_dmg

        # Apply armor ignore
        if sk.get("armor_ignore"):
            pass  # true damage, no armor reduction
        else:
            m_armor = state.get("monster_stats", {}).get("armor", 0) if isinstance(state.get("monster_stats", {}).get("armor"), int) else 0
            total_dmg = max(1, total_dmg - m_armor)

        state["monster_hp"] = max(0, state["monster_hp"] - total_dmg)

        # Apply status
        status = sk.get("status_apply")
        if status:
            _append_status_dedup(state, make_status(status), key="monster_statuses")

        # Apply stat_mod to enemy
        stat_mod = sk.get("stat_mod", {})
        enemy_mods = stat_mod.get("enemy", {})
        if enemy_mods:
            mod_dur = sk.get("mod_duration", 3)
            state.setdefault("druid_summon_enemy_stat_mods", []).append(
                {"mods": enemy_mods, "duration": mod_dur})
            m_stats = state.setdefault("monster_stats", {})
            for stat, val in enemy_mods.items():
                m_stats[stat] = m_stats.get(stat, 0) + val

        # Lifesteal
        lifesteal = sk.get("lifesteal", 0)
        if lifesteal:
            heal = int(total_dmg * lifesteal)
            summon["hp"] = min(summon["max_hp"], summon["hp"] + heal)
            log.append({"kind": "druid_summon_lifesteal", "text": f"{summon['name']} heals {heal} HP from lifesteal!"})

        log.append({
            "kind": "druid_summon_attack",
            "text": f"{summon['name']} uses {sk.get('name', 'Attack')} — {total_dmg} damage!"
        })
        return {"action": "attack", "skill": sk.get("name"), "damage": total_dmg}

    elif ptype in ("buff", "defend"):
        # Apply buff to summon or druid
        self_status = sk.get("self_status")
        if self_status:
            # Apply to summon itself
            summon.setdefault("statuses", [])
            if not any(s.get("id") == self_status for s in summon.get("statuses", [])):
                summon["statuses"].append(make_status(self_status))

        stat_mod = sk.get("stat_mod", {})
        self_mods = stat_mod.get("self", {})
        if self_mods:
            for stat, val in self_mods.items():
                summon["stats"][stat] = summon["stats"].get(stat, 0) + val

        log.append({
            "kind": "druid_summon_defend",
            "text": f"{summon['name']} uses {sk.get('name', 'Defend')}!"
        })
        return {"action": "defend", "skill": sk.get("name")}

    elif ptype == "heal":
        heal_pct = sk.get("heal_percent", 0.10)
        heal_amt = int(summon["max_hp"] * heal_pct)
        summon["hp"] = min(summon["max_hp"], summon["hp"] + heal_amt)
        self_status = sk.get("self_status")
        if self_status:
            summon.setdefault("statuses", [])
            if not any(s.get("id") == self_status for s in summon.get("statuses", [])):
                summon["statuses"].append(make_status(self_status))
        log.append({
            "kind": "druid_summon_heal",
            "text": f"{summon['name']} uses {sk.get('name', 'Heal')} — restores {heal_amt} HP!"
        })
        return {"action": "heal", "skill": sk.get("name"), "heal": heal_amt}

    return {"action": "pass"}


def _druid_bonded_senses_rider(state: dict, character: dict, log: list) -> int:
    """Bonded Senses (L30): the Druid borrows its summon's attack as a passive rider.

    Spec: "While a summon is active, the Druid also gains the summon's Attack skill
    as a passive rider (weaker version — no status apply, just damage)."

    This passive had no engine implementation at all. Returns the extra damage dealt
    so callers can log or aggregate it.
    """
    if not _is_druid(character) or character.get("level", 1) < 30:
        return 0
    active = state.get("druid_active_summons", []) or []
    if not active or state.get("monster_hp", 0) <= 0:
        return 0

    # Use the strongest active summon's primary attack, at half strength and with
    # no status rider — the "weaker version" the spec calls for.
    best = 0
    source = None
    for summon in active:
        attacks = (summon.get("profile_skills") or {}).get("attack") or []
        for atk in attacks:
            dmg = int(atk.get("damage", 0))
            if dmg > best:
                best, source = dmg, (summon, atk)
    if not source or best <= 0:
        return 0

    summon, atk = source
    rider = max(1, int(best * 0.5) + int(summon.get("stats", {}).get("might", 0) * 0.15))
    state["monster_hp"] = max(0, state.get("monster_hp", 0) - rider)
    log.append({"kind": "druid_bonded_senses",
                "text": f"BONDED SENSES — you echo {summon.get('name', 'your companion')}'s "
                        f"{atk.get('name', 'attack')} for {rider} damage!"})
    return rider


def _druid_tick_summons(state: dict, character: dict, log: list):
    """Process all active summon actions at the start of the turn (after Druid acts, before enemy)."""
    if not _is_druid(character):
        return

    active = state.get("druid_active_summons", [])
    if not active:
        return

    # Bonded Senses (L30) fires once per turn while any summon is out.
    _druid_bonded_senses_rider(state, character, log)

    synergy = state.get("druid_pack_synergy")
    turn = state.get("turn", 0)

    # Wild Sovereign: share_buffs — all buffs on any summon are shared to all others
    if synergy and synergy.get("share_buffs"):
        all_statuses = {}
        for summon in active:
            if summon.get("fused"):
                continue
            for s in summon.get("statuses", []):
                if s.get("kind") == "buff" and s.get("id"):
                    all_statuses[s["id"]] = s
        for summon in active:
            if summon.get("fused"):
                continue
            existing_ids = {s.get("id") for s in summon.get("statuses", [])}
            for sid, s in all_statuses.items():
                if sid not in existing_ids:
                    summon.setdefault("statuses", []).append(dict(s))

    for summon in active:
        if summon.get("fused"):
            continue  # fused summons don't act independently

        # Tick cooldowns
        cds = summon.get("skill_cooldowns", {})
        for sid in list(cds.keys()):
            cds[sid] = max(0, cds[sid] - 1)

        # Regen some stamina
        summon["stamina"] = min(100, summon.get("stamina", 100) + 10)

        # Extra action from Pack Alpha (every other turn, or every turn with Wild Sovereign L90)
        actions = 1
        if synergy and synergy.get("extra_action_every") and turn % 2 == 1:
            actions = 2
        elif synergy and synergy.get("extra_action_every_other") and turn % 2 == 1:
            actions = 2

        # Druid boss aura: attack speed boost — chance for extra action
        attack_boost = state.get("druid_aura_attack_boost", 0)
        if attack_boost > 0 and random.random() < attack_boost:
            actions += 1

        for _ in range(actions):
            if state.get("monster_hp", 1) <= 0:
                break
            _druid_execute_summon_action(summon, state, character, log, synergy)

        # Check if summon died from any counterattack effects
        if summon["hp"] <= 0:
            log.append({"kind": "druid_summon_death", "text": f"{summon['name']} has fallen in battle! It returns to your bestiary."})
            _remove_passive_buffs_from_character(character, summon.get("passive_buff", []))
            # Eternal Bond (level 80): dead summons can be re-summoned same combat after 1 turn
            if character.get("level", 1) >= 80:
                state.setdefault("druid_dead_summons", {})[summon["id"]] = 1
                log.append({"kind": "druid_eternal_bond", "text": f"Eternal Bond — {summon['name']} can be re-summoned next turn!"})

    # Remove dead summons
    state["druid_active_summons"] = [s for s in active if s.get("hp", 0) > 0]
    state["druid_pack_synergy"] = _compute_pack_synergy(state["druid_active_summons"], character)

    # Tick fusion cooldowns
    cooldowns = state.get("druid_fusion_cooldowns", {})
    for cid in list(cooldowns.keys()):
        cooldowns[cid] = max(0, cooldowns[cid] - 1)
        if cooldowns[cid] <= 0:
            del cooldowns[cid]

    # Tick fusion signature cooldowns
    sig_cds = state.get("druid_fusion_sig_cooldowns", {})
    for sid in list(sig_cds.keys()):
        sig_cds[sid] = max(0, sig_cds[sid] - 1)
        if sig_cds[sid] <= 0:
            del sig_cds[sid]

    # Tick fusion duration
    if state.get("druid_fusion_active"):
        state["druid_fusion_turns"] = state.get("druid_fusion_turns", 0) - 1
        if state["druid_fusion_turns"] <= 0:
            _druid_end_fusion(state, character, log)

    # Tick Eternal Bond dead-summon cooldowns
    dead_summons = state.get("druid_dead_summons", {})
    for cid in list(dead_summons.keys()):
        dead_summons[cid] = max(0, dead_summons[cid] - 1)
        if dead_summons[cid] <= 0:
            del dead_summons[cid]

    # Tick season cooldown
    if state.get("druid_season_cooldown", 0) > 0:
        state["druid_season_cooldown"] -= 1


def _druid_fuse(character: dict, state: dict, creature_id: str, log: list) -> dict:
    """Fuse with an active summon."""
    active = state.get("druid_active_summons", [])
    summon = next((s for s in active if s["id"] == creature_id), None)
    if not summon:
        return {"error": "That creature is not currently summoned."}
    if summon.get("fused"):
        return {"error": f"{summon['name']} is already fused with you."}

    # Check if already fused with another (unless multi-fusion)
    if state.get("druid_fusion_active") and not state.get("druid_multi_fusion"):
        return {"error": "You are already fused. End the current fusion first."}

    # Check cooldown
    cooldowns = state.get("druid_fusion_cooldowns", {})
    if cooldowns.get(creature_id, 0) > 0:
        return {"error": f"{summon['name']} is recovering from fusion ({cooldowns[creature_id]} turns)."}

    # Apply fusion: stat stacking
    s_stats = summon.get("stats", {})
    for stat, val in s_stats.items():
        character["stats"][stat] = character["stats"].get(stat, 0) + val

    # Mark summon as fused
    summon["fused"] = True
    summon["hp"] = summon["max_hp"]  # full HP when fusion ends

    # Set fusion state
    state["druid_fusion_active"] = True
    # Fusion Adept (level 40): 4 turn duration, otherwise 3
    state["druid_fusion_turns"] = 4 if character.get("level", 1) >= 40 else 3
    state["druid_fusion_summon_id"] = creature_id

    # Recompute pack synergy (fused summon doesn't count as active on field)
    field_summons = [s for s in active if not s.get("fused")]
    state["druid_pack_synergy"] = _compute_pack_synergy(field_summons, character)

    dur = state["druid_fusion_turns"]
    log.append({
        "kind": "druid_fuse",
        "text": f"You fuse with {summon['name']}! Stats combined, abilities gained! ({dur} turns)"
    })

    return {"success": True, "summon": summon}


def _druid_end_fusion(state: dict, character: dict, log: list):
    """End fusion — unstack stats, restore summon."""
    active = state.get("druid_active_summons", [])
    fused_id = state.get("druid_fusion_summon_id")

    for summon in active:
        if summon.get("fused"):
            # Reverse stat stacking
            s_stats = summon.get("stats", {})
            for stat, val in s_stats.items():
                character["stats"][stat] = character["stats"].get(stat, 0) - val

            summon["fused"] = False
            summon["hp"] = summon["max_hp"]  # reappears at full HP

            # Set cooldown: 2 turns base, 1 with Fusion Adept (level 40), 0 with Eternal Wild (level 95)
            cooldowns = state.get("druid_fusion_cooldowns", {})
            if character.get("level", 1) >= 95:
                pass  # no cooldown with Eternal Wild
            elif character.get("level", 1) >= 40:
                cooldowns[summon["id"]] = 1  # Fusion Adept: 1 turn
            else:
                cooldowns[summon["id"]] = 2

            cd_text = "no cooldown" if character.get("level", 1) >= 95 else f"{cooldowns.get(summon['id'], 0)} turn cooldown"
            log.append({
                "kind": "druid_fusion_end",
                "text": f"Fusion with {summon['name']} ends. It reappears at full HP. ({cd_text})"
            })

    state["druid_fusion_active"] = False
    state["druid_fusion_turns"] = 0
    state["druid_fusion_summon_id"] = None
    state["druid_fusion_sig_cooldowns"] = {}
    state["druid_active_summons"] = active
    state["druid_pack_synergy"] = _compute_pack_synergy(
        [s for s in active if not s.get("fused")], character)


def _druid_get_fusion_riders(state: dict) -> dict:
    """Get attack rider and defense passive from fused summons."""
    active = state.get("druid_active_summons", [])
    riders = {"attack_skills": [], "defense_skills": [], "signature_skills": []}
    for summon in active:
        if not summon.get("fused"):
            continue
        profile = summon.get("profile_skills", {})
        if profile.get("attack"):
            riders["attack_skills"].append(profile["attack"][0])
        if profile.get("defense"):
            riders["defense_skills"].append(profile["defense"][0])
        sigs = summon.get("signature_fusion", [])
        if sigs:
            riders["signature_skills"].extend(sigs)
    return riders


def _druid_apply_fusion_attack_rider(state: dict, character: dict, log: list, total_dmg: int) -> int:
    """Apply fused summon's attack skill as a bonus rider on Druid strikes."""
    if not state.get("druid_fusion_active"):
        return total_dmg

    riders = _druid_get_fusion_riders(state)
    for atk_sk in riders["attack_skills"]:
        rider_dmg = atk_sk.get("damage", 5)
        s_stats = {}
        for summon in state.get("druid_active_summons", []):
            if summon.get("fused"):
                s_stats = summon.get("stats", {})
                break
        rider_dmg = int(rider_dmg + s_stats.get("might", 5) * 0.5)

        # Apply status from rider
        status = atk_sk.get("status_apply")
        if status:
            _append_status_dedup(state, make_status(status), key="monster_statuses")

        # Apply stat_mod from rider
        stat_mod = atk_sk.get("stat_mod", {})
        enemy_mods = stat_mod.get("enemy", {})
        if enemy_mods:
            mod_dur = atk_sk.get("mod_duration", 3)
            state.setdefault("druid_summon_enemy_stat_mods", []).append(
                {"mods": enemy_mods, "duration": mod_dur})
            m_stats = state.setdefault("monster_stats", {})
            for stat, val in enemy_mods.items():
                m_stats[stat] = m_stats.get(stat, 0) + val

        log.append({
            "kind": "druid_fusion_rider",
            "text": f"Fusion rider: {atk_sk.get('name', 'Attack')} — +{rider_dmg} damage!"
        })
        total_dmg += rider_dmg

    return total_dmg


def _druid_apply_fusion_defense(state: dict, character: dict, log: list, c_dmg: int) -> int:
    """Apply fused summon's defense skill as a passive damage reduction on incoming attacks."""
    if not state.get("druid_fusion_active"):
        return c_dmg

    riders = _druid_get_fusion_riders(state)
    for def_sk in riders["defense_skills"]:
        s_stats = {}
        for summon in state.get("druid_active_summons", []):
            if summon.get("fused"):
                s_stats = summon.get("stats", {})
                break

        # Damage reduction: based on summon's durability and skill power
        reduction = int(def_sk.get("damage", 0) + s_stats.get("durability", 5) * 0.5)
        if reduction > 0 and c_dmg > 0:
            c_dmg = max(0, c_dmg - reduction)
            log.append({
                "kind": "druid_fusion_defense",
                "text": f"Fusion defense: {def_sk.get('name', 'Defense')} — -{reduction} damage!"
            })

        # Apply self_status from defense skill (e.g., warded, evasive)
        self_status = def_sk.get("self_status")
        if self_status:
            existing = [s for s in state.get("player_statuses", []) if s.get("id") == self_status]
            if not existing and not any(s.get("id") == self_status for s in character.get("statuses", [])):
                _append_status_dedup(character, make_status(self_status), key="player_statuses")
                log.append({
                    "kind": "druid_fusion_defense",
                    "text": f"Fusion defense: {def_sk.get('name', 'Defense')} — grants {self_status.title()}!"
                })

    return c_dmg


def _druid_apply_fusion_signature(state: dict, character: dict, log: list) -> int:
    """Apply fused summon's signature ability as a bonus attack on the player's turn.
    Returns bonus damage dealt."""
    if not state.get("druid_fusion_active"):
        return 0

    riders = _druid_get_fusion_riders(state)
    if not riders["signature_skills"]:
        return 0

    # Track signature cooldowns in state
    sig_cds = state.setdefault("druid_fusion_sig_cooldowns", {})

    total_sig_dmg = 0
    for sig_sk in riders["signature_skills"]:
        sig_id = sig_sk.get("id", "")
        if sig_cds.get(sig_id, 0) > 0:
            continue  # on cooldown

        s_stats = {}
        for summon in state.get("druid_active_summons", []):
            if summon.get("fused"):
                s_stats = summon.get("stats", {})
                break

        base_power = sig_sk.get("damage", 10)
        might = s_stats.get("might", 5)
        hits = sig_sk.get("hits", 1)
        dmg_per_hit = int(base_power + might * 0.8)

        for _ in range(hits):
            hit_dmg = max(1, dmg_per_hit + random.randint(-2, 2))
            if not sig_sk.get("armor_ignore"):
                m_armor = state.get("monster_stats", {}).get("armor", 0)
                if isinstance(m_armor, int):
                    hit_dmg = max(1, hit_dmg - m_armor)
            total_sig_dmg += hit_dmg

        # Apply status from signature
        status = sig_sk.get("status_apply")
        if status:
            _append_status_dedup(state, make_status(status), key="monster_statuses")

        # Apply stat_mod to enemy
        stat_mod = sig_sk.get("stat_mod", {})
        enemy_mods = stat_mod.get("enemy", {})
        if enemy_mods:
            mod_dur = sig_sk.get("mod_duration", 3)
            state.setdefault("druid_summon_enemy_stat_mods", []).append(
                {"mods": enemy_mods, "duration": mod_dur})
            m_stats = state.setdefault("monster_stats", {})
            for stat, val in enemy_mods.items():
                m_stats[stat] = m_stats.get(stat, 0) + val

        # Set cooldown
        sig_cds[sig_id] = sig_sk.get("cooldown", 4)

        log.append({
            "kind": "druid_fusion_signature",
            "text": f"Signature: {sig_sk.get('name', 'Signature')} — {total_sig_dmg} damage!"
        })

    return total_sig_dmg


def _druid_apply_boss_aura(state: dict, character: dict, log: list):
    """Apply boss aura effects from active boss+ summons."""
    for summon in state.get("druid_active_summons", []):
        if summon.get("fused"):
            continue
        aura = summon.get("boss_aura")
        if not aura:
            continue
        effect = aura.get("effect", "")
        value = aura.get("value", 0)
        if effect == "enemy_attack_penalty":
            m_stats = state.get("monster_stats", {})
            for stat in ("might", "grace", "cognition"):
                m_stats[stat] = int(m_stats.get(stat, 5) * (1.0 - value))
        elif effect == "burning_on_hit":
            # Chance to apply burning status on monster each turn
            if random.random() < value:
                _append_status_dedup(state, make_status("burning"), key="monster_statuses")
                log.append({"kind": "druid_aura", "text": f"{summon['name']}'s aura sets the enemy ablaze!"})
        elif effect == "heal_reduction":
            state["druid_aura_heal_reduction"] = value
        elif effect == "stamina_drain":
            # Drain monster stamina each turn
            m_stam = state.get("monster_stamina", 100)
            drain = int(m_stam * value)
            state["monster_stamina"] = max(0, m_stam - drain)
            if drain > 0:
                log.append({"kind": "druid_aura", "text": f"{summon['name']}'s aura drains {drain} stamina from the enemy!"})
        elif effect == "mana_regen":
            # Restore MP to Druid and all summons each turn
            regen = int(character.get("max_mp", 0) * value) if character.get("max_mp") else 0
            if regen > 0:
                character["mp"] = min(character.get("max_mp", 0), character.get("mp", 0) + regen)
            for s in state.get("druid_active_summons", []):
                if not s.get("fused"):
                    s["mp"] = s.get("mp", 0) + int(value * 10)
        elif effect == "magic_damage_boost":
            state["druid_aura_magic_boost"] = value
        elif effect == "attack_speed_boost":
            state["druid_aura_attack_boost"] = value
        elif effect == "regen_all":
            # Heal all active summons each turn
            for s in state.get("druid_active_summons", []):
                if not s.get("fused"):
                    heal = int(s["max_hp"] * value)
                    s["hp"] = min(s["max_hp"], s["hp"] + heal)


def _druid_apply_legendary_passive(state: dict, character: dict, log: list):
    """Apply legendary passive effects from active legendary summons."""
    for summon in state.get("druid_active_summons", []):
        if summon.get("fused"):
            continue
        lp = summon.get("legendary_passive")
        if not lp:
            continue
        lp_type = lp.get("type", "")
        if lp_type == "phoenix_rebirth":
            # Mark summon as able to resurrect once
            if not summon.get("rebirth_used"):
                summon["can_rebirth"] = True
        elif lp_type == "titan_endurance":
            summon["damage_reduction"] = 0.50
        elif lp_type == "alpha_dominance":
            # When HP drops below 25%, enter unkillable state for 1 turn (once per fight)
            if not summon.get("alpha_dominance_used") and summon["hp"] < summon["max_hp"] * 0.25:
                summon["alpha_dominance_used"] = True
                summon["damage_reduction"] = 1.0  # unkillable for 1 turn
                summon["alpha_dominance_turns"] = 1
                log.append({
                    "kind": "druid_legendary_passive",
                    "text": f"{summon['name']} enters an unkillable state! Alpha Dominance activates!"
                })
            # Tick down unkillable state
            if summon.get("alpha_dominance_turns", 0) > 0:
                summon["alpha_dominance_turns"] -= 1
                if summon["alpha_dominance_turns"] <= 0:
                    summon["damage_reduction"] = 0
        elif lp_type == "leviathan_tide":
            # Every 3rd turn, tidal wave
            turn = state.get("turn", 0)
            if turn > 0 and turn % 3 == 0:
                dmg = int(summon["max_hp"] * 0.15)
                state["monster_hp"] = max(0, state["monster_hp"] - dmg)
                # Cleanse summon debuffs
                summon["statuses"] = []
                log.append({
                    "kind": "druid_legendary_passive",
                    "text": f"{summon['name']}'s tidal wave hits for {dmg} damage and cleanses itself!"
                })
        elif lp_type == "living_wood":
            # Mark as able to revive once
            if not summon.get("living_wood_revived"):
                summon["living_wood_can_revive"] = True
            # Regrow HP while above 50%
            if summon["hp"] > summon["max_hp"] * 0.50:
                heal = int(summon["max_hp"] * 0.05)
                summon["hp"] = min(summon["max_hp"], summon["hp"] + heal)
# ============================================================
# MAGE COMBAT SYSTEM
# ============================================================

def _is_mage(character: dict) -> bool:
    return "mage" in (character.get("masteries") or [])


def _mage_get_equipped_passives(character: dict) -> list[str]:
    """Get the list of equipped Arcane Library passive IDs."""
    return character.get("mage_equipped_passives", [])


def _mage_get_school_synergy(character: dict) -> dict:
    """Check for school synergy bonuses. Returns dict of school -> level (0, 3, 5)."""
    from game_data import MAGE_PASSIVES
    passive_ids = _mage_get_equipped_passives(character)
    if not passive_ids:
        return {}
    passive_map = {p["id"]: p for p in MAGE_PASSIVES}
    school_counts: dict[str, int] = {}
    for pid in passive_ids:
        p = passive_map.get(pid)
        if p:
            school = p.get("school", "")
            school_counts[school] = school_counts.get(school, 0) + 1
    synergy = {}
    for school, count in school_counts.items():
        if count >= 5:
            synergy[school] = 5
        elif count >= 3:
            synergy[school] = 3
    return synergy


def _mage_has_passive(character: dict, passive_id: str) -> bool:
    """Check if the Mage has a specific Arcane Library passive equipped."""
    return passive_id in _mage_get_equipped_passives(character)


def _mage_get_skill_tags(skill: dict | None) -> set:
    """Get the spell tags for a skill.

    `skill` is None whenever the player takes an innate action (a plain strike
    with no skill selected, which is the default for anyone who has not assigned
    skills to their skill bar yet). Every mage passive helper funnels its tag
    lookup through here, so tolerating None in one place keeps basic attacks from
    raising a 500 across all of them.
    """
    if not skill:
        return set()
    return set(skill.get("spell_tags", []))


def _mage_gain_arcane_focus(state: dict, character: dict, log: list) -> None:
    """Gain 1 Arcane Focus on odd turns (max 3). No gain if stunned/silenced."""
    if not _is_mage(character):
        return
    turn = state.get("turn", 0)
    # Only gain on odd turns (1, 3, 5, ...)
    if turn % 2 == 0:
        return
    # No focus gain if stunned or silenced
    statuses = state.get("player_statuses", [])
    for s in statuses:
        if isinstance(s, dict):
            if s.get("id") in ("stunned", "silenced"):
                return
        elif isinstance(s, str):
            if s in ("stunned", "silenced"):
                return
    current = state.get("mage_arcane_focus", 0)
    if current < 3:
        state["mage_arcane_focus"] = current + 1
        log.append({"kind": "mage_focus", "text": f"Arcane Focus: {current + 1}/3"})
    reduction = 0
    if _mage_has_passive(character, "quickened_mind"):
        reduction += 1
    synergy = _mage_get_school_synergy(character)
    if synergy.get("Temporal", 0) >= 3:
        reduction += 1
    return reduction


def _mage_apply_passive_modifiers(state: dict, character: dict, skill: dict, total_dmg: float, log: list) -> float:
    """Apply Arcane Library passive modifiers to a strike's damage. Returns modified damage."""
    tags = _mage_get_skill_tags(skill)
    is_strike = "Strike" in tags
    is_single_target = "Single-Target" in tags

    # True Strike: convert 25% to true damage (handled as damage type override, but we just boost)
    if is_strike and _mage_has_passive(character, "true_strike"):
        # 25% of damage bypasses armor — approximate as +5% total damage
        total_dmg = int(total_dmg * 1.05)
        log.append({"kind": "mage_passive", "text": "True Strike — 25% true damage!"})

    # Overchannel: +50% damage
    if is_strike and _mage_has_passive(character, "overchannel"):
        total_dmg = int(total_dmg * 1.50)
        log.append({"kind": "mage_passive", "text": "Overchannel — +50% damage!"})

    # Chain Reaction: hit 2 targets (approximate as +50% damage for single-target)
    if is_strike and is_single_target and _mage_has_passive(character, "chain_reaction"):
        total_dmg = int(total_dmg * 1.50)
        log.append({"kind": "mage_passive", "text": "Chain Reaction — spreads to 2 targets!"})

    # Echo Chamber: repeat at 50% next turn (set state flag)
    if is_strike and _mage_has_passive(character, "echo_chamber"):
        state.setdefault("mage_echo_next_turn", []).append({
            "skill_id": skill.get("id"),
            "damage": int(total_dmg * 0.50),
        })
        log.append({"kind": "mage_passive", "text": "Echo Chamber — will repeat next turn!"})

    # Implosion: AoE to adjacent (approximate as +25% damage)
    if is_strike and is_single_target and _mage_has_passive(character, "implosion"):
        total_dmg = int(total_dmg * 1.25)
        log.append({"kind": "mage_passive", "text": "Implosion — AoE splash!"})

    # Spell Penetration: ignore 50% essence (approximate as +10% damage)
    if is_strike and _mage_has_passive(character, "spell_penetration"):
        total_dmg = int(total_dmg * 1.10)
        log.append({"kind": "mage_passive", "text": "Spell Penetration — 50% essence bypassed!"})

    # Critical Theory: 20% chance to double damage
    if is_strike and _mage_has_passive(character, "critical_theory"):
        if random.random() < 0.20:
            total_dmg = int(total_dmg * 2.0)
            log.append({"kind": "mage_passive", "text": "Critical Theory — DOUBLE DAMAGE!"})

    # Glass Cannon: +100% damage
    if is_strike and _mage_has_passive(character, "glass_cannon"):
        total_dmg = int(total_dmg * 2.0)
        state["mage_glass_cannon_active"] = True
        log.append({"kind": "mage_passive", "text": "Glass Cannon — +100% damage!"})

    # Arcane Surge: every 3rd strike is true damage
    if is_strike and _mage_has_passive(character, "arcane_surge"):
        state["mage_strike_count"] = state.get("mage_strike_count", 0) + 1
        if state["mage_strike_count"] % 3 == 0:
            total_dmg = int(total_dmg * 1.20)  # true damage approximated as +20%
            log.append({"kind": "mage_passive", "text": "Arcane Surge — TRUE DAMAGE!"})

    # School Synergy: Arcane — 10% true damage at 3+, 25% true + 10% crit at 5+
    synergy = _mage_get_school_synergy(character)
    if is_strike and synergy.get("Arcane", 0) >= 3:
        total_dmg = int(total_dmg * 1.10)
        if synergy.get("Arcane", 0) >= 5:
            total_dmg = int(total_dmg * 1.25)
            if random.random() < 0.10:
                total_dmg = int(total_dmg * 2.0)
                log.append({"kind": "mage_synergy", "text": "Arcane Synergy — CRITICAL!"})

    # Storm Rider equivalent: Lightning tag + active
    # (Mage doesn't have imbues, but Lightning-tagged skills get bonus from passives)

    return total_dmg


def _mage_get_status_override(character: dict, skill: dict | None) -> str | None:
    """Check if an Arcane Library passive overrides the skill's normal status. Returns new status or None."""
    if not skill:
        return None
    tags = _mage_get_skill_tags(skill)
    original_status = skill.get("status_apply")

    # Frostfire: Fire-tagged → frostburn instead of burning
    if "Fire" in tags and _mage_has_passive(character, "frostfire"):
        return "frostburn"

    # Storm Earth: Stone-tagged → shocked instead of bleeding
    if "Stone" in tags and _mage_has_passive(character, "storm_earth"):
        return "shocked"

    # Void Lightning: Lightning-tagged → voidmarked instead of stunned
    if "Lightning" in tags and _mage_has_passive(character, "void_lightning"):
        return "voidmarked"

    # Caustic Wind: Wind-tagged → corroded instead of normal status
    if "Wind" in tags and _mage_has_passive(character, "caustic_wind"):
        return "corroded"

    # Shadow Ice: Ice-tagged → shadowfrost instead of ensnared
    if "Ice" in tags and _mage_has_passive(character, "shadow_ice"):
        return "shadowfrost"

    # Magma Skin: Stone-tagged → magma instead of bleeding
    if "Stone" in tags and _mage_has_passive(character, "magma_skin"):
        return "magma"

    return None


def _mage_get_extra_status(character: dict, skill: dict | None) -> str | None:
    """Check for passives that add an extra status. Returns additional status or None."""
    tags = _mage_get_skill_tags(skill)

    # Thunderblood: Lightning-tagged also applies bleeding
    if "Lightning" in tags and _mage_has_passive(character, "thunderblood"):
        return "bleeding"

    # Double Jeopardy (Mental): Debuff-tagged skills apply 2 statuses instead of 1.
    if "Debuff" in tags and _mage_has_passive(character, "double_jeopardy"):
        return "shaken"

    return None


def _mage_apply_arcane_library_control(state: dict, character: dict, log: list) -> None:
    """Arcane Library control passives that resolve against enemy state.

    These were declared in MAGE_PASSIVES and equippable through the Library, but
    the engine never referenced them — a player could research and slot them and
    they would do nothing at all.

    Only the passives that are meaningful in this game's 1v1 combat are handled.
    `wildfire`, `hallucination`, `mass_hysteria` and `delirium` all describe
    spreading to "adjacent enemies" or making a target "attack their own ally",
    which has no meaning without multi-enemy encounters — see MASTERY_PLANS.md.
    """
    if not _is_mage(character):
        return

    monster_statuses = state.get("monster_statuses", []) or []
    has = {s.get("id") for s in monster_statuses}

    # Absolute Zero (Elements): an already-ensnared target becomes fully frozen.
    if "ensnared" in has and _mage_has_passive(character, "absolute_zero"):
        if "stunned" not in has:
            _append_status_dedup(state, make_status("stunned"), key="monster_statuses")
            log.append({"kind": "mage_passive",
                        "text": "ABSOLUTE ZERO — the ensnared target freezes solid!"})

    # Mind Fracture (Mental): a shaken target bleeds a random stat each turn.
    if "shaken" in has and _mage_has_passive(character, "mind_fracture"):
        m_stats = state.setdefault("monster_stats", {})
        candidates = [k for k in ("might", "grace", "insight", "durability") if k in m_stats]
        if candidates:
            victim = random.choice(candidates)
            state.setdefault("mage_mind_fracture_drain", {})
            state["mage_mind_fracture_drain"][victim] = \
                state["mage_mind_fracture_drain"].get(victim, 0) + 1
            m_stats[victim] = m_stats.get(victim, 0) - 1
            log.append({"kind": "mage_passive",
                        "text": f"MIND FRACTURE — the shaken mind sheds {victim} (-1)."})

    # Paranoia (Mental): a shaken target cannot benefit from buffs.
    if "shaken" in has and _mage_has_passive(character, "paranoia"):
        if not state.get("mage_paranoia_active"):
            state["mage_paranoia_active"] = True
            log.append({"kind": "mage_passive",
                        "text": "PARANOIA — the target trusts nothing; buffs will not hold."})

    # Wildfire (Elements): an already-burning target burns twice as hard.
    #
    # Spec said the burning "spreads to all adjacent enemies", which has no meaning
    # in 1v1 combat. Reinterpreted as intensification so the passive keeps its
    # identity (fire propagates) and actually does something.
    if "burning" in has and _mage_has_passive(character, "wildfire"):
        for st in monster_statuses:
            if st.get("id") == "burning" and not st.get("_wildfire_applied"):
                st["magnitude"] = int(st.get("magnitude", 3)) * 2
                st["_wildfire_applied"] = True
                log.append({"kind": "mage_passive",
                            "text": f"WILDFIRE — the flames redouble ({st['magnitude']} per turn)!"})
                break


def _mage_get_debuff_duration_multiplier(character: dict) -> float:
    """Mass Hysteria (Mental): debuffs the Mage applies last 50% longer.

    Spec said debuffs "spread to 1 adjacent enemy at 50% duration" — meaningless
    in 1v1, so the spread becomes depth on the single target instead.
    """
    if _is_mage(character) and _mage_has_passive(character, "mass_hysteria"):
        return 1.5
    return 1.0


def _mage_check_enemy_self_attack(state: dict, character: dict, log: list) -> bool:
    """Delirium (Mental): a heavily-debuffed enemy may turn its attack on itself.

    Spec said it attacks "their own ally"; with a single opponent the equivalent
    misdirection is self-harm.
    """
    if not _is_mage(character) or not _mage_has_passive(character, "delirium"):
        return False
    debuff_count = sum(
        1 for s in (state.get("monster_statuses") or [])
        if s.get("kind") == "debuff" or s.get("id") in (
            "burning", "bleeding", "poisoned", "shaken", "stunned",
            "ensnared", "blinded", "cursed", "silenced", "confused")
    )
    if debuff_count >= 2 and random.random() < 0.25:
        log.append({"kind": "mage_passive",
                    "text": "DELIRIUM — the addled enemy turns its own attack on itself!"})
        return True
    return False


# ---- School of Spatial ----------------------------------------------------
# The Spatial school was entirely inert: 13 equippable passives, none referenced
# by the engine. On inspection the combat loop *does* maintain a real range model
# (`player_range`, `monster_range`, `range_gap`, updated every turn for the
# Hunter), so the range-based passives are implementable after all. Only the ones
# needing portals, terrain or allies are not — those are flagged `planned` in
# MAGE_PASSIVES and filtered out of the equippable Library.
def _mage_apply_spatial_range(state: dict, character: dict, log: list) -> None:
    """Long Range / Point Blank: adjust the Mage's effective range once per fight."""
    if not _is_mage(character) or state.get("mage_spatial_range_applied"):
        return
    state["mage_spatial_range_applied"] = True

    delta = 0
    if _mage_has_passive(character, "long_range"):
        delta += 1
    if _mage_has_passive(character, "point_blank"):
        delta -= 1
    if delta:
        state["player_range"] = max(0, state.get("player_range", 0) + delta)
        state["range_gap"] = state["player_range"] - state.get("monster_range", 0)
        label = "LONG RANGE" if delta > 0 else "POINT BLANK"
        log.append({"kind": "mage_passive",
                    "text": f"{label} — effective range is now {state['player_range']}."})


def _mage_get_spatial_damage_mult(state: dict, character: dict) -> float:
    """Point Blank: +30% damage while at range 0-1."""
    if not _is_mage(character) or not _mage_has_passive(character, "point_blank"):
        return 1.0
    if state.get("player_range", 0) <= 1:
        return 1.30
    return 1.0


def _mage_ignores_range_minimum(character: dict) -> bool:
    """Far Strike: strike-tagged skills can be cast at any range."""
    return _is_mage(character) and _mage_has_passive(character, "far_strike")


def _mage_apply_spatial_riders(state: dict, character: dict, skill: dict | None, log: list) -> None:
    """Gravity Shift, Reposition and Blink Step — all pure range/status effects."""
    if not _is_mage(character) or not skill:
        return
    tags = _mage_get_skill_tags(skill)
    ptype = skill.get("power_type")

    # Gravity Shift: debuffs drag the enemy a step closer.
    if (ptype == "debuff" or "Debuff" in tags) and _mage_has_passive(character, "gravity_shift"):
        state["monster_range"] = state.get("monster_range", 0) + 1
        state["range_gap"] = state.get("player_range", 0) - state["monster_range"]
        log.append({"kind": "mage_passive", "text": "GRAVITY SHIFT — the enemy is dragged a step closer!"})

    # Reposition: defend-tagged skills push the Mage a step away.
    if (ptype == "defend" or "Defend" in tags) and _mage_has_passive(character, "reposition"):
        state["player_range"] = state.get("player_range", 0) + 1
        state["range_gap"] = state["player_range"] - state.get("monster_range", 0)
        log.append({"kind": "mage_passive", "text": "REPOSITION — the Mage slides out of reach."})

    # Blink Step: teleport-tagged skills also grant `hidden`.
    if "Teleport" in tags and _mage_has_passive(character, "blink_step"):
        _append_status_dedup(state, make_status("hidden"), key="player_statuses")
        log.append({"kind": "mage_passive", "text": "BLINK STEP — the Mage blinks out of sight."})


def _mage_get_expanding_radius_bonus(character: dict) -> float:
    """Expanding Radius: spec hits 'target + 1 adjacent'. With one opponent the
    equivalent is concentrating the extra blast on the sole target."""
    if _is_mage(character) and _mage_has_passive(character, "expanding_radius"):
        return 1.20
    return 1.0


def _mage_check_mirror_position(state: dict, character: dict, log: list) -> None:
    """Mirror Position: dodging swaps the combatants' range, disrupting melee."""
    if not _is_mage(character) or not _mage_has_passive(character, "mirror_position"):
        return
    p, m = state.get("player_range", 0), state.get("monster_range", 0)
    if p != m:
        state["player_range"], state["monster_range"] = m, p
        state["range_gap"] = state["player_range"] - state["monster_range"]
        log.append({"kind": "mage_passive",
                    "text": "MIRROR POSITION — the Mage and its foe trade places!"})


def _mage_apply_status_stack_bonus(state: dict, character: dict, status_id: str, log: list) -> None:
    """Elemental Overload: elemental statuses land at +2 stacks instead of +1."""
    if not _is_mage(character) or not _mage_has_passive(character, "elemental_overload_mage"):
        return
    ELEMENTAL = {"burning", "frostburn", "shocked", "ensnared", "corroded",
                 "shadowfrost", "magma", "voidmarked"}
    if status_id not in ELEMENTAL:
        return
    for st in state.get("monster_statuses", []) or []:
        if st.get("id") == status_id:
            st["magnitude"] = int(st.get("magnitude", 1)) + 2
            st["duration"] = int(st.get("duration", 2)) + 1
            log.append({"kind": "mage_passive",
                        "text": f"ELEMENTAL OVERLOAD — {status_id} lands at full force!"})
            break


def _mage_queue_temporal_echo(state: dict, character: dict, skill: dict | None,
                              total_dmg: float, log: list) -> None:
    """Temporal Echo: Dual Cast skills echo at 25% power on the next odd turn.

    Reuses the existing `mage_echo_next_turn` queue that Echo Chamber already
    drains, so no second echo mechanism is needed.
    """
    if not _is_mage(character) or not skill:
        return
    if not _mage_has_passive(character, "temporal_echo"):
        return
    tags = _mage_get_skill_tags(skill)
    if "Dual Cast" not in tags and not skill.get("dual_cast"):
        return
    if (state.get("turn", 0) + 1) % 2 == 0:
        return  # only echoes onto odd turns
    state.setdefault("mage_echo_next_turn", []).append({
        "skill_id": skill.get("id", "spell"),
        "damage": int(total_dmg * 0.25),
    })
    log.append({"kind": "mage_passive",
                "text": "TEMPORAL ECHO — the dual cast will ring again next turn."})


def _mage_get_overload_debuff_bonus(character: dict, skill: dict | None) -> float:
    """Overload: spec turns single-target debuffs into AoE. With one opponent the
    equivalent is landing the full area effect on that target."""
    if not _is_mage(character) or not skill:
        return 1.0
    if not _mage_has_passive(character, "overload_mage"):
        return 1.0
    tags = _mage_get_skill_tags(skill)
    if skill.get("power_type") == "debuff" or "Debuff" in tags:
        return 1.25
    return 1.0


def _mage_get_decoy_miss_chance(state: dict, character: dict) -> float:
    """Hallucination (Mental): decoys absorb attacks while the Mage is evasive.

    Spec said it "creates 2 extra copies instead of 1". There is no illusion-copy
    entity in combat, so the copies are expressed as a flat chance for an incoming
    attack to hit a decoy instead.
    """
    if not _is_mage(character) or not _mage_has_passive(character, "hallucination"):
        return 0.0
    player = state.get("player_statuses", []) or []
    if any(s.get("id") == "evasive" for s in player):
        return 0.30
    return 0.0


def _mage_check_enemy_turn_skip(state: dict, character: dict, log: list) -> bool:
    """Mind Control (Mental) + Time Loop (Temporal): can the enemy act this turn?

    Returns True when the enemy's turn is consumed. Both passives were declared
    and equippable but had no engine implementation.
    """
    if not _is_mage(character):
        return False

    has = {s.get("id") for s in (state.get("monster_statuses") or [])}

    # Mind Control: shaken enemies have a 15% chance to lose their turn.
    if "shaken" in has and _mage_has_passive(character, "mind_control"):
        if random.random() < 0.15:
            log.append({"kind": "mage_passive",
                        "text": "MIND CONTROL — the enemy hesitates, its turn lost!"})
            return True

    # Time Loop: a stunned enemy repeats its last action, wasting the turn.
    if "stunned" in has and _mage_has_passive(character, "time_loop"):
        log.append({"kind": "mage_passive",
                    "text": "TIME LOOP — the enemy replays its last move and accomplishes nothing."})
        return True

    return False


def _mage_check_illusion_mastery(state: dict, character: dict, log: list) -> None:
    """Illusion Mastery (Mental): `evasive` also grants `hidden`."""
    if not _is_mage(character) or not _mage_has_passive(character, "illusion_mastery"):
        return
    player = state.get("player_statuses", []) or []
    if any(s.get("id") == "evasive" for s in player) and \
       not any(s.get("id") == "hidden" for s in player):
        _append_status_dedup(state, make_status("hidden"), key="player_statuses")
        log.append({"kind": "mage_passive",
                    "text": "ILLUSION MASTERY — the Mage vanishes mid-dodge."})


def _mage_get_cooldown_modifier(character: dict) -> int:
    """Turns to subtract from a skill's cooldown after use.

    Sources:
      - Quickened Mind (Temporal): "All cooldowns reduced by 1."
      - Temporal school synergy at 3 and at 5 equipped passives.

    This function was referenced by combat_turn but never defined, so every Mage
    who cast a skill raised NameError and got a 500 — the mastery was unplayable
    the moment a spell left the bar. Implemented to mirror
    _mage_get_debuff_duration_modifier, the sibling helper directly below.
    """
    reduction = 0
    if _mage_has_passive(character, "quickened_mind"):
        reduction += 1
    synergy = _mage_get_school_synergy(character)
    temporal = synergy.get("Temporal", 0)
    if temporal >= 3:
        reduction += 1
    if temporal >= 5:
        reduction += 1
    return reduction


def _mage_get_debuff_duration_modifier(character: dict) -> int:
    """Get extra turns for debuffs from passives. Returns integer to add to duration."""
    extra = 0
    if _mage_has_passive(character, "time_dilation"):
        extra += 1
    synergy = _mage_get_school_synergy(character)
    if synergy.get("Temporal", 0) >= 3:
        extra += 1
    if synergy.get("Mental", 0) >= 3:
        extra += 1
    return extra


def _mage_check_phobia_implant(state: dict, character: dict, skill: dict | None, log: list) -> None:
    """Phobia Implant: first debuff each combat also stuns."""
    if not _mage_has_passive(character, "phobia_implant"):
        return
    # None on innate actions — an unskilled strike is not a debuff.
    if not skill or skill.get("power_type") != "debuff":
        return
    if state.get("mage_phobia_used"):
        return
    state["mage_phobia_used"] = True
    _append_status_dedup(state, make_status("stunned"), key="monster_statuses")
    log.append({"kind": "mage_passive", "text": "Phobia Implant — the enemy is stunned by fear!"})


def _mage_process_echo(state: dict, log: list) -> int:
    """Process echo damage from Echo Chamber passive. Returns echo damage."""
    echoes = state.get("mage_echo_next_turn", [])
    if not echoes:
        return 0
    total_echo = 0
    for echo in echoes:
        total_echo += echo.get("damage", 0)
        log.append({"kind": "mage_echo", "text": f"Echo Chamber — {echo.get('skill_id', 'spell')} repeats for {echo.get('power', 0)} damage!"})
    state["mage_echo_next_turn"] = []
    return total_echo


def _mage_check_rewind(state: dict, character: dict, log: list) -> bool:
    """Check if Rewind passive can be used. Returns True if used."""
    if not _mage_has_passive(character, "rewind"):
        return False
    if state.get("mage_rewind_used"):
        return False
    # Auto-trigger when HP drops below 25%
    hp = state.get("player_hp", 0)
    max_hp = state.get("player_max_hp", 100)
    if hp > 0 and hp < max_hp * 0.25:
        state["mage_rewind_used"] = True
        prev_hp = state.get("mage_prev_hp", hp)
        state["player_hp"] = prev_hp
        log.append({"kind": "mage_passive", "text": f"Rewind — HP restored to {prev_hp}!"})
        return True
    return False


def _mage_save_rewind_state(state: dict) -> None:
    """Save current HP for Rewind passive."""
    state["mage_prev_hp"] = state.get("player_hp", 0)


def _mage_tick_end_of_turn(state: dict, character: dict, log: list) -> None:
    """Tick Mage-specific state at end of turn."""
    # Glass Cannon: take +50% damage while casting — reset flag
    state["mage_glass_cannon_active"] = False

    # Temporal Echo: if dual cast was used, set echo for next odd turn
    # (handled by echo_chamber passive already)

    # Arcane Library control passives (Absolute Zero, Mind Fracture, Paranoia)
    # and Illusion Mastery. These resolve against current enemy/player statuses,
    # so end of turn is the natural point.
    _mage_apply_arcane_library_control(state, character, log)
    _mage_check_illusion_mastery(state, character, log)
    _mage_apply_spatial_range(state, character, log)

    # Save HP for Rewind
    _mage_save_rewind_state(state)


# ============================================================
# PRIEST COMBAT SYSTEM
# ============================================================

import random as _random


def _priest_get_sanctity_mult(state: dict, character: dict) -> float:
    """Return Sanctity multiplier based on enemy HP and Priest passives.

    Base tiers: 100-75% → 1.0, 75-50% → 1.25, 50-25% → 1.50, <25% → 2.0
    Sanctified (L10): starts at 90% instead of 75%
    Deep Faith (L60): +35% / +75% / +150% → 1.35 / 1.75 / 2.50
    Avatar of Faith (L100): Sanctity doubled
    Hand of God (quest): Sanctity tripled
    Redemption (L90): at full enemy HP, +10% effect (min 1.10)
    """
    enemy_hp_ratio = state.get("monster_hp", 0) / max(1, state.get("monster_max_hp", 1))
    level = character.get("level", 1)
    quest_passives = character.get("quest_passives") or []

    # Determine thresholds
    sanctified = level >= 10
    threshold_high = 0.90 if sanctified else 0.75

    # Determine base multiplier
    if enemy_hp_ratio >= threshold_high:
        mult = 1.0
    elif enemy_hp_ratio >= 0.50:
        mult = 1.25
    elif enemy_hp_ratio >= 0.25:
        mult = 1.50
    else:
        mult = 2.0

    # Deep Faith (L60): enhanced tiers
    if level >= 60:
        if enemy_hp_ratio >= threshold_high:
            mult = 1.0  # no bonus at full HP (Redemption handles that)
        elif enemy_hp_ratio >= 0.50:
            mult = 1.35
        elif enemy_hp_ratio >= 0.25:
            mult = 1.75
        else:
            mult = 2.50

    # Avatar of Faith (L100): double sanctity
    if level >= 100:
        # Sanctity bonuses doubled means the bonus portion is doubled
        # mult = 1.0 + (mult - 1.0) * 2
        mult = 1.0 + (mult - 1.0) * 2

    # Hand of God (quest): triple sanctity
    if "hand_of_god" in quest_passives:
        mult = 1.0 + (mult - 1.0) * 3

    # Redemption (L90): at full enemy HP, +10% effect
    if level >= 90 and enemy_hp_ratio >= 0.99:
        mult = max(mult, 1.10)

    return mult


def _priest_get_miracle_chance(state: dict, character: dict, target_hp_ratio: float, is_ally: bool = False) -> float:
    """Return Miracle chance based on target's missing HP and Priest passives.

    Base: chance = 1.0 - target_hp_ratio (0% at full, 99% at 1%)
    Deep Faith (L60): +15%
    Avatar of Faith (L100): doubled when healing allies
    Hand of God (quest): guaranteed (100%) when target < 25% HP
    """
    level = character.get("level", 1)
    quest_passives = character.get("quest_passives") or []

    chance = 1.0 - target_hp_ratio

    # Deep Faith (L60): +15%
    if level >= 60:
        chance += 0.15

    # Avatar of Faith (L100): doubled when healing allies
    if level >= 100 and is_ally:
        chance *= 2.0

    # Hand of God (quest): guaranteed when target < 25% HP
    if "hand_of_god" in quest_passives and target_hp_ratio < 0.25:
        chance = 1.0

    return min(chance, 1.0)


def _priest_roll_miracle(state: dict, character: dict, target_hp_ratio: float, is_ally: bool = False) -> bool:
    """Roll for Miracle double-cast. Returns True if Miracle triggers."""
    chance = _priest_get_miracle_chance(state, character, target_hp_ratio, is_ally)
    return _random.random() < chance


def _priest_get_holy_bonus_mult(state: dict, character: dict, monster: dict) -> float:
    """Return holy damage multiplier vs undead/devils.

    Base: 1.50 (+50%)
    Holy Fire (L20): 1.75 (+75%)
    Avatar of Faith (L100): 2.00 (+100%)
    """
    level = character.get("level", 1)
    m = state.get("monster_ref", {}) or monster or {}
    monster_category = m.get("category", "")
    monster_tags = m.get("tags", [])
    is_evil = monster_category in ("undead", "devil") or "undead" in monster_tags or "devil" in monster_tags

    if not is_evil:
        return 1.0

    if level >= 100:
        return 2.0
    elif level >= 20:
        return 1.75
    else:
        return 1.50


def _priest_apply_shield_wall(state: dict, character: dict, skill: dict, log: list) -> None:
    """Apply a Shield Wall to the Priest. Replaces existing shield (breaks old one first)."""
    # Break existing shield first (triggers on-break effects like Sanctuary bind)
    if state.get("priest_shield_wall_hp", 0) > 0:
        _priest_break_shield_wall(state, character, log)

    max_hp = state.get("player_max_hp", character.get("max_hp", 1))
    base_shield = skill.get("shield_hp", 0.20)
    sanctity = _priest_get_sanctity_mult(state, character)
    level = character.get("level", 1)
    quest_passives = character.get("quest_passives") or []

    # Avatar of Faith (L100): Shield Wall Sanctity scaling doubled
    if level >= 100:
        # The sanctity bonus portion is doubled (same as skill sanctity)
        sanctity_for_shield = 1.0 + (sanctity - 1.0) * 2
    else:
        sanctity_for_shield = sanctity

    # Hand of God: sanctity tripled for shields too
    if "hand_of_god" in quest_passives:
        sanctity_for_shield = 1.0 + (sanctity - 1.0) * 3

    shield_hp = int(max_hp * base_shield * sanctity_for_shield)

    # Redemption (L90): Shield Wall gains +50% HP
    if level >= 90:
        shield_hp = int(shield_hp * 1.50)

    # Apply barrier_amp from item bonus effects
    _ibe = state.get("item_bonus_effects", {})
    _barrier_amp = _ibe.get("barrier_amp", 0)
    if _barrier_amp > 0:
        shield_hp = int(shield_hp * (1.0 + _barrier_amp))

    # Apply Essence-based barrier scaling
    shield_hp = compute_barrier(character, shield_hp)

    state["priest_shield_wall_hp"] = shield_hp
    state["priest_shield_wall_max"] = shield_hp
    state["priest_shield_wall_skill"] = skill.get("id")
    state["priest_shield_absorbed"] = 0

    log.append({"kind": "priest_shield_wall", "text": f"Shield Wall: {shield_hp} HP barrier erected."})


def _priest_break_shield_wall(state: dict, character: dict, log: list) -> None:
    """Break the current Shield Wall. Triggers on-break effects (Sanctuary bind)."""
    skill_id = state.get("priest_shield_wall_skill")
    absorbed = state.get("priest_shield_absorbed", 0)
    level = character.get("level", 1)
    quest_passives = character.get("quest_passives") or []

    # Hand of God: Shield Walls heal the Priest for 50% of damage absorbed
    if "hand_of_god" in quest_passives and absorbed > 0:
        heal_amount = int(absorbed * 0.50)
        if heal_amount > 0:
            max_hp = state.get("player_max_hp", character.get("max_hp", 1))
            old_hp = state.get("player_hp", character.get("hp", 0))
            state["player_hp"] = min(max_hp, old_hp + heal_amount)
            character["hp"] = state["player_hp"]
            log.append({"kind": "priest_shield_heal", "text": f"Hand of God — Shield Wall absorbed {absorbed} damage, healing {heal_amount} HP!"})

    # Sanctuary: when shield breaks, bind the enemy
    if skill_id == "sanctuary_priest":
        bind_status = make_status("bind")
        # Avatar of Faith: bind duration +1
        if level >= 100:
            bind_status["duration"] += 1
        _append_status_dedup(state, bind_status, key="monster_statuses")
        log.append({"kind": "priest_sanctuary_break", "text": "Sanctuary shattered! Holy chains erupt — enemy is bound!"})

    state["priest_shield_wall_hp"] = 0
    state["priest_shield_wall_max"] = 0
    state["priest_shield_wall_skill"] = None
    state["priest_shield_absorbed"] = 0


def _priest_absorb_damage(state: dict, character: dict, damage: int, log: list) -> int:
    """Absorb damage through Shield Wall first. Returns remaining damage after shield."""
    shield_hp = state.get("priest_shield_wall_hp", 0)
    if shield_hp <= 0:
        return damage

    absorbed = min(shield_hp, damage)
    state["priest_shield_wall_hp"] = shield_hp - absorbed
    state["priest_shield_absorbed"] = state.get("priest_shield_absorbed", 0) + absorbed
    remaining = damage - absorbed

    if absorbed > 0:
        log.append({"kind": "priest_shield_absorb", "text": f"Shield Wall absorbs {absorbed} damage ({state['priest_shield_wall_hp']} HP remaining)."})

    # Radiant Bulwark: when struck, blind the enemy
    if state.get("priest_shield_wall_skill") == "radiant_bulwark" and absorbed > 0:
        blind_status = make_status("blind")
        level = character.get("level", 1)
        if level >= 100:
            blind_status["duration"] += 1
        _append_status_dedup(state, blind_status, key="monster_statuses")
        log.append({"kind": "priest_radiant_bulwark", "text": "Radiant Bulwark flares — enemy is blinded!"})

    if state["priest_shield_wall_hp"] <= 0:
        _priest_break_shield_wall(state, character, log)

    return remaining


def _priest_get_cooldown_reduction(state: dict, character: dict) -> int:
    """Return extra cooldown reduction from Divine Wrath passive."""
    level = character.get("level", 1)
    enemy_hp_ratio = state.get("monster_hp", 0) / max(1, state.get("monster_max_hp", 1))
    if level >= 80 and enemy_hp_ratio <= 0.25:
        return 1
    return 0


def _priest_get_strike_damage_mult(state: dict, character: dict) -> float:
    """Return strike damage multiplier from Judgment passive."""
    level = character.get("level", 1)
    enemy_hp_ratio = state.get("monster_hp", 0) / max(1, state.get("monster_max_hp", 1))
    if level >= 70 and enemy_hp_ratio <= 0.50:
        return 1.20
    return 1.0


def _priest_start_of_turn(state: dict, character: dict, log: list) -> None:
    """Priest start-of-turn effects: HoT ticks, delayed heals, and Smite.

    This function's `def` line was lost in a past edit, leaving the body
    stranded as unreachable code after the `return` in
    _priest_get_strike_damage_mult above. combat_turn called it by name, so every
    Priest raised NameError on turn 2 of any fight — the mastery was unplayable
    past the opening turn, and none of its healing-over-time mechanics ever ran.
    """
    if not _is_priest(character):
        return

    level = character.get("level", 1)

    # Tick HoT buffs (Blessing of Renewal)
    for buff in state.get("priest_hot_buffs", []):
        if buff.get("turns_remaining", 0) > 0:
            heal_pct = buff.get("heal_percent", 0.10)
            sanctity = _priest_get_sanctity_mult(state, character)
            heal_amount = int(state.get("player_max_hp", character.get("max_hp", 1)) * heal_pct * sanctity)
            old_hp = state.get("player_hp", character.get("hp", 0))
            max_hp = state.get("player_max_hp", character.get("max_hp", 1))
            state["player_hp"] = min(max_hp, old_hp + heal_amount)
            character["hp"] = state["player_hp"]
            log.append({"kind": "priest_hot", "text": f"Blessing of Renewal ticks for {heal_amount} HP."})
            buff["turns_remaining"] -= 1

    # Remove expired HoT buffs
    state["priest_hot_buffs"] = [b for b in state.get("priest_hot_buffs", []) if b.get("turns_remaining", 0) > 0]

    # Process delayed heals (Promise of Heaven)
    for dh in state.get("priest_delayed_heals", []):
        dh["turns_remaining"] = dh.get("turns_remaining", 0) - 1
        if dh["turns_remaining"] <= 0:
            heal_pct = dh.get("heal_percent", 0.35)
            sanctity = _priest_get_sanctity_mult(state, character)
            heal_amount = int(state.get("player_max_hp", character.get("max_hp", 1)) * heal_pct * sanctity)
            old_hp = state.get("player_hp", character.get("hp", 0))
            max_hp = state.get("player_max_hp", character.get("max_hp", 1))
            state["player_hp"] = min(max_hp, old_hp + heal_amount)
            character["hp"] = state["player_hp"]
            log.append({"kind": "priest_delayed_heal", "text": f"Promise of Heaven fulfilled! Healed for {heal_amount} HP!"})

    # Remove expired delayed heals
    state["priest_delayed_heals"] = [d for d in state.get("priest_delayed_heals", []) if d.get("turns_remaining", 0) > 0]

    # Smite (L40): when enemy drops below 50% HP, gain insight +10 for 3 turns
    enemy_hp_ratio = state.get("monster_hp", 0) / max(1, state.get("monster_max_hp", 1))
    if level >= 40 and enemy_hp_ratio < 0.50 and not state.get("priest_smiting"):
        state["priest_smiting"] = True
        state["priest_smite_active"] = 3
        character["stats"]["insight"] = character["stats"].get("insight", 0) + 10
        log.append({"kind": "priest_smite", "text": "SMITE — The enemy falters! Insight +10 for 3 turns!"})


def _priest_process_skill(state: dict, character: dict, skill: dict, log: list) -> None:
    """Process a Priest skill. Applies Sanctity scaling, Miracle double-cast, and all Priest mechanics."""
    if not _is_priest(character):
        return

    level = character.get("level", 1)
    quest_passives = character.get("quest_passives") or []
    sid = skill.get("id", "")
    ptype = skill.get("power_type", "")

    # Determine target HP ratio for Miracle
    target = skill.get("target", "self")
    if target in ("ally", "all_allies"):
        # For ally-targeted skills, use player HP ratio
        target_hp_ratio = state.get("player_hp", 0) / max(1, state.get("player_max_hp", 1))
        is_ally = True
    else:
        # For self/enemy-targeted skills, use enemy HP ratio for strikes/debuffs,
        # player HP ratio for heals/buffs on self
        if ptype in ("heal", "buff", "defend", "shield_wall"):
            target_hp_ratio = state.get("player_hp", 0) / max(1, state.get("player_max_hp", 1))
        else:
            target_hp_ratio = state.get("monster_hp", 0) / max(1, state.get("monster_max_hp", 1))
        is_ally = False

    # Roll for Miracle
    miracle = _priest_roll_miracle(state, character, target_hp_ratio, is_ally)

    # Process based on power_type
    if ptype == "heal":
        _priest_process_heal(state, character, skill, log, miracle, is_ally)
    elif ptype == "strike":
        _priest_process_strike(state, character, skill, log, miracle)
    elif ptype == "shield_wall":
        _priest_process_shield_wall_skill(state, character, skill, log, miracle)
    elif ptype == "buff":
        _priest_process_buff(state, character, skill, log, miracle)
    elif ptype == "debuff":
        _priest_process_debuff(state, character, skill, log, miracle)
    elif ptype == "defend":
        _priest_process_defend(state, character, skill, log, miracle)


def _priest_process_heal(state: dict, character: dict, skill: dict, log: list, miracle: bool, is_ally: bool) -> None:
    """Process a Priest heal skill with Sanctity scaling and Miracle."""
    level = character.get("level", 1)
    quest_passives = character.get("quest_passives") or []
    heal_pct = skill.get("heal_percent", 0)
    heal_type = skill.get("heal_type", "normal")
    sanctity = _priest_get_sanctity_mult(state, character)
    max_hp = state.get("player_max_hp", character.get("max_hp", 1))

    # Hand of God: cleanse debuffs before healing
    if "hand_of_god" in quest_passives:
        _priest_cleanse_debuffs(state, character, log)

    def do_heal():
        nonlocal heal_pct
        scaled_pct = heal_pct * sanctity
        heal_amount = int(max_hp * scaled_pct)
        old_hp = state.get("player_hp", character.get("hp", 0))
        pre_hp_pct = old_hp / max(1, max_hp)
        state["player_hp"] = min(max_hp, old_hp + heal_amount)
        character["hp"] = state["player_hp"]
        post_hp_pct = state["player_hp"] / max(1, max_hp)

        # MIRACLE SAVED feedback
        if pre_hp_pct < 0.10 and post_hp_pct > 0.50:
            log.append({"kind": "priest_miracle_saved", "text": "MIRACLE SAVED — from the brink of death to safety!"})
        else:
            log.append({"kind": "priest_heal", "text": f"{skill.get('name', 'Heal')} heals {heal_amount} HP."})

        # Avatar of Faith (L100): heals on allies also apply Shield Wall (10% max HP)
        if level >= 100 and is_ally:
            sw_hp = int(max_hp * 0.10)
            # Apply a small shield wall on the target (player)
            existing = state.get("priest_shield_wall_hp", 0)
            if existing > 0:
                state["priest_shield_wall_hp"] = existing + sw_hp
                state["priest_shield_wall_max"] = max(state.get("priest_shield_wall_max", 0), state["priest_shield_wall_hp"])
            else:
                state["priest_shield_wall_hp"] = sw_hp
                state["priest_shield_wall_max"] = sw_hp
                state["priest_shield_wall_skill"] = "avatar_of_faith_shield"
            log.append({"kind": "priest_ally_shield", "text": f"Avatar of Faith — Shield Wall ({sw_hp} HP) applied to ally!"})

        # Hand of God: Miracle on heal also applies inspired
        if miracle and "hand_of_god" in quest_passives:
            inspired = make_status("inspired")
            inspired["duration"] = 3
            _append_status_dedup(state, inspired, key="player_statuses")
            log.append({"kind": "priest_miracle_inspired", "text": "Hand of God — Miracle grants inspired!"})

    # Handle heal types
    if heal_type == "hot":
        # HoT: add to priest_hot_buffs
        duration = skill.get("mod_duration", 3)
        state.setdefault("priest_hot_buffs", []).append({
            "heal_percent": heal_pct,
            "turns_remaining": duration,
            "target": skill.get("target", "ally"),
        })
        log.append({"kind": "priest_hot_applied", "text": f"{skill.get('name', 'Heal')} — HoT applied for {duration} turns."})
        if miracle:
            # Miracle: double duration
            state["priest_hot_buffs"][-1]["turns_remaining"] += duration
            log.append({"kind": "priest_miracle", "text": "MIRACLE — HoT duration doubled!"})
    elif heal_type == "delayed":
        # Delayed: add to priest_delayed_heals
        delay = skill.get("mod_duration", 2)
        state.setdefault("priest_delayed_heals", []).append({
            "heal_percent": heal_pct,
            "turns_remaining": delay,
            "target": skill.get("target", "ally"),
        })
        log.append({"kind": "priest_delayed_applied", "text": f"{skill.get('name', 'Heal')} — delayed heal set for {delay} turns."})
        if miracle:
            # Miracle: heal ticks twice (double heal_percent)
            state["priest_delayed_heals"][-1]["heal_percent"] *= 2
            log.append({"kind": "priest_miracle", "text": "MIRACLE — Delayed heal doubled!"})
    elif heal_type == "group":
        # Group heal: heal all allies (in single-player, just heal self)
        do_heal()
        if miracle:
            do_heal()
            log.append({"kind": "priest_miracle", "text": "MIRACLE — Group heal double-cast!"})
    else:
        # Fast and normal: direct heal
        do_heal()
        if miracle:
            do_heal()
            log.append({"kind": "priest_miracle", "text": "MIRACLE — Double heal!"})

    # Apply self_status from heal skills (e.g., Divine Light warded, Hymn of Salvation inspired)
    self_status = skill.get("self_status")
    if self_status:
        st = make_status(self_status)
        _append_status_dedup(state, st, key="player_statuses")

    # Apply self stat_mods from heal skills (e.g., Divine Light, Hymn of Salvation)
    stat_mod = skill.get("stat_mod", {})
    self_mods = stat_mod.get("self", {})
    if self_mods:
        duration = skill.get("mod_duration", 3)
        state.setdefault("priest_self_stat_mods", []).append({
            "mods": self_mods,
            "duration": duration,
        })
        for stat, val in self_mods.items():
            character["stats"][stat] = character["stats"].get(stat, 0) + val
        log.append({"kind": "priest_stat_mod", "text": f"{', '.join(f'{k} {v:+d}' for k,v in self_mods.items())} for {duration} turns."})

    # Miracle: double stat_mods
    if miracle and self_mods:
        state.setdefault("priest_self_stat_mods", []).append({
            "mods": self_mods,
            "duration": duration,
        })
        for stat, val in self_mods.items():
            character["stats"][stat] = character["stats"].get(stat, 0) + val


def _priest_process_strike(state: dict, character: dict, skill: dict, log: list, miracle: bool) -> None:
    """Process a Priest strike skill with Sanctity scaling, holy damage, and Miracle."""
    level = character.get("level", 1)
    quest_passives = character.get("quest_passives") or []
    sanctity = _priest_get_sanctity_mult(state, character)

    # Holy damage bonus
    holy_mult = _priest_get_holy_bonus_mult(state, character, state.get("monster_ref", {}))

    # Judgment (L70): +20% strike damage at <=50% enemy HP
    judgment_mult = _priest_get_strike_damage_mult(state, character)

    # Smite (L40): insight +10 (stat mod already applied separately)
    # This is handled via stat_mod in the skill processing, but we note it here

    # Exorcist (L50): holy strikes apply burning to undead/devils
    m = state.get("monster_ref", {}) or {}
    monster_category = m.get("category", "")
    monster_tags = m.get("tags", [])
    is_evil = monster_category in ("undead", "devil") or "undead" in monster_tags or "devil" in monster_tags

    if level >= 50 and is_evil and skill.get("damage_type") == "holy":
        _append_status_dedup(state, make_status("burning"), key="monster_statuses")
        log.append({"kind": "priest_exorcist", "text": "Exorcist — Holy fire burns the unholy!"})

    # Apply Sanctity to damage (the actual damage is computed in the main combat loop,
    # but we log the Sanctity and holy bonuses here)
    total_mult = sanctity * holy_mult * judgment_mult
    if total_mult > 1.0:
        log.append({"kind": "priest_sanctity", "text": f"Sanctity x{sanctity:.2f}, Holy x{holy_mult:.2f}, Judgment x{judgment_mult:.2f}"})

    # Hand of God: Miracle on strike also applies blind
    if miracle and "hand_of_god" in quest_passives:
        blind_status = make_status("blind")
        if level >= 100:
            blind_status["duration"] += 1
        _append_status_dedup(state, blind_status, key="monster_statuses")
        log.append({"kind": "priest_miracle_blind", "text": "Hand of God — Miracle blinds the enemy!"})

    # Apply enemy stat_mods with Sanctity scaling (e.g., Holy Water, Judgment Strike, Holy Lance)
    stat_mod = skill.get("stat_mod", {})
    enemy_mods = stat_mod.get("enemy", {})
    if enemy_mods:
        scaled_mods = {k: int(v * sanctity) for k, v in enemy_mods.items()}
        mod_dur = skill.get("mod_duration", 3)
        state.setdefault("priest_enemy_stat_mods", []).append({
            "mods": scaled_mods,
            "duration": mod_dur,
        })
        m_stats = state.get("monster_stats", {})
        for stat, val in scaled_mods.items():
            m_stats[stat] = m_stats.get(stat, 0) + val
        log.append({"kind": "priest_enemy_mod", "text": f"Enemy: {', '.join(f'{k} {v:+d}' for k,v in scaled_mods.items())} for {mod_dur} turns."})

    # Miracle: double enemy stat_mods
    if miracle and enemy_mods:
        state.setdefault("priest_enemy_stat_mods", []).append({
            "mods": scaled_mods,
            "duration": mod_dur,
        })
        m_stats = state.get("monster_stats", {})
        for stat, val in scaled_mods.items():
            m_stats[stat] = m_stats.get(stat, 0) + val

    if miracle:
        log.append({"kind": "priest_miracle", "text": "MIRACLE — Double strike!"})


def _priest_process_shield_wall_skill(state: dict, character: dict, skill: dict, log: list, miracle: bool) -> None:
    """Process a Priest Shield Wall skill."""
    _priest_apply_shield_wall(state, character, skill, log)

    # Apply any self_status from the skill (e.g., warded)
    self_status = skill.get("self_status")
    if self_status:
        level = character.get("level", 1)
        st = make_status(self_status)
        _append_status_dedup(state, st, key="player_statuses")

    # Apply any status_apply (e.g., Radiant Bulwark blinds on cast — but that's on hit, handled in absorb)
    # Apply stat_mod
    stat_mod = skill.get("stat_mod", {})
    if stat_mod.get("self"):
        self_mods = stat_mod["self"]
        mod_dur = skill.get("mod_duration", 3)
        state.setdefault("priest_self_stat_mods", []).append({
            "mods": self_mods,
            "duration": mod_dur,
        })
        for stat, val in self_mods.items():
            character["stats"][stat] = character["stats"].get(stat, 0) + val
        log.append({"kind": "priest_stat_mod", "text": f"{', '.join(f'{k} {v:+d}' for k,v in self_mods.items())} for {mod_dur} turns."})

    if miracle:
        # Miracle: recast shield at full HP (replaces)
        _priest_apply_shield_wall(state, character, skill, log)
        log.append({"kind": "priest_miracle", "text": "MIRACLE — Shield Wall recast at full HP!"})


def _priest_process_buff(state: dict, character: dict, skill: dict, log: list, miracle: bool) -> None:
    """Process a Priest buff skill with Sanctity scaling."""
    sanctity = _priest_get_sanctity_mult(state, character)
    stat_mod = skill.get("stat_mod", {})
    self_mods = stat_mod.get("self", {})

    # Sanctity amplifies buff stat mods
    scaled_mods = {}
    for k, v in self_mods.items():
        scaled_mods[k] = int(v * sanctity)

    duration = skill.get("mod_duration", 3)
    level = character.get("level", 1)

    # Apply self_status
    self_status = skill.get("self_status")
    if self_status:
        st = make_status(self_status)
        _append_status_dedup(state, st, key="player_statuses")

    # Apply stat mods
    if scaled_mods:
        state.setdefault("priest_self_stat_mods", []).append({
            "mods": scaled_mods,
            "duration": duration,
        })
        for stat, val in scaled_mods.items():
            character["stats"][stat] = character["stats"].get(stat, 0) + val
        log.append({"kind": "priest_stat_mod", "text": f"{', '.join(f'{k} {v:+d}' for k,v in scaled_mods.items())} for {duration} turns."})

    # Some buffs have heal_percent (Beacon of Faith, Prayer Circle, Divine Covenant)
    heal_pct = skill.get("heal_percent", 0)
    if heal_pct > 0:
        max_hp = state.get("player_max_hp", character.get("max_hp", 1))
        heal_amount = int(max_hp * heal_pct * sanctity)
        old_hp = state.get("player_hp", character.get("hp", 0))
        state["player_hp"] = min(max_hp, old_hp + heal_amount)
        character["hp"] = state["player_hp"]
        log.append({"kind": "priest_buff_heal", "text": f"{skill.get('name', 'Buff')} heals {heal_amount} HP."})

    if miracle:
        # Miracle: double-cast the buff (apply stat mods again)
        if scaled_mods:
            state.setdefault("priest_self_stat_mods", []).append({
                "mods": scaled_mods,
                "duration": duration,
            })
            for stat, val in scaled_mods.items():
                character["stats"][stat] = character["stats"].get(stat, 0) + val
        if heal_pct > 0:
            max_hp = state.get("player_max_hp", character.get("max_hp", 1))
            heal_amount = int(max_hp * heal_pct * sanctity)
            old_hp = state.get("player_hp", character.get("hp", 0))
            state["player_hp"] = min(max_hp, old_hp + heal_amount)
            character["hp"] = state["player_hp"]
        log.append({"kind": "priest_miracle", "text": "MIRACLE — Double buff!"})


def _priest_process_debuff(state: dict, character: dict, skill: dict, log: list, miracle: bool) -> None:
    """Process a Priest debuff skill with Sanctity scaling."""
    sanctity = _priest_get_sanctity_mult(state, character)
    level = character.get("level", 1)
    status_apply = skill.get("status_apply")

    # Apply status with Sanctity-extended duration
    if status_apply:
        statuses = status_apply if isinstance(status_apply, list) else [status_apply]
        for s in statuses:
            st = make_status(s)
            # Sanctity extends duration (round up)
            st["duration"] = max(st["duration"], int(st["duration"] * sanctity))
            # Avatar of Faith (L100): bind and blind +1 turn
            if level >= 100 and s in ("bind", "blind"):
                st["duration"] += 1
            _append_status_dedup(state, st, key="monster_statuses")

    # Apply stat_mod to enemy with Sanctity amplification
    stat_mod = skill.get("stat_mod", {})
    enemy_mods = stat_mod.get("enemy", {})
    if enemy_mods:
        scaled_mods = {}
        for k, v in enemy_mods.items():
            scaled_mods[k] = int(v * sanctity)
        state.setdefault("priest_enemy_stat_mods", []).append({
            "mods": scaled_mods,
            "duration": skill.get("mod_duration", 3),
        })
        m_stats = state.get("monster_stats", {})
        for stat, val in scaled_mods.items():
            m_stats[stat] = m_stats.get(stat, 0) + val
        log.append({"kind": "priest_enemy_mod", "text": f"Enemy: {', '.join(f'{k} {v:+d}' for k,v in scaled_mods.items())} for {skill.get('mod_duration', 3)} turns."})

    if miracle:
        # Miracle: double-cast debuff (apply status again, refresh duration)
        if status_apply:
            statuses = status_apply if isinstance(status_apply, list) else [status_apply]
            for s in statuses:
                st = make_status(s)
                if level >= 100 and s in ("bind", "blind"):
                    st["duration"] += 1
                _append_status_dedup(state, st, key="monster_statuses")
        if enemy_mods:
            miracle_mods = {k: int(v * sanctity) for k, v in enemy_mods.items()}
            state.setdefault("priest_enemy_stat_mods", []).append({
                "mods": miracle_mods,
                "duration": skill.get("mod_duration", 3),
            })
            m_stats = state.get("monster_stats", {})
            for stat, val in miracle_mods.items():
                m_stats[stat] = m_stats.get(stat, 0) + val
        log.append({"kind": "priest_miracle", "text": "MIRACLE — Double debuff!"})


def _priest_process_defend(state: dict, character: dict, skill: dict, log: list, miracle: bool) -> None:
    """Process a Priest defend skill with Sanctity scaling."""
    sanctity = _priest_get_sanctity_mult(state, character)
    stat_mod = skill.get("stat_mod", {})
    self_mods = stat_mod.get("self", {})

    # Sanctity amplifies defend stat mods
    scaled_mods = {}
    for k, v in self_mods.items():
        scaled_mods[k] = int(v * sanctity)

    duration = skill.get("mod_duration", 3)

    # Apply self_status
    self_status = skill.get("self_status")
    if self_status:
        st = make_status(self_status)
        _append_status_dedup(state, st, key="player_statuses")

    if scaled_mods:
        state.setdefault("priest_self_stat_mods", []).append({
            "mods": scaled_mods,
            "duration": duration,
        })
        for stat, val in scaled_mods.items():
            character["stats"][stat] = character["stats"].get(stat, 0) + val
        log.append({"kind": "priest_stat_mod", "text": f"{', '.join(f'{k} {v:+d}' for k,v in scaled_mods.items())} for {duration} turns."})

    # Mass Purify / Light of Hope: cleanse debuffs (self_debuff trigger)
    if skill.get("trigger") == "self_debuff":
        _priest_cleanse_debuffs(state, character, log)

    if miracle:
        if scaled_mods:
            state.setdefault("priest_self_stat_mods", []).append({
                "mods": scaled_mods,
                "duration": duration,
            })
            for stat, val in scaled_mods.items():
                character["stats"][stat] = character["stats"].get(stat, 0) + val
        log.append({"kind": "priest_miracle", "text": "MIRACLE — Double defend!"})


def _priest_cleanse_debuffs(state: dict, character: dict, log: list) -> None:
    """Remove all debuff statuses from the player."""
    debuff_ids = {"shaken", "bleeding", "burning", "poisoned", "ensnared", "stunned",
                  "blinded", "blind", "bind", "mesmerized", "silenced", "confused",
                  "weary", "sick", "cursed", "recovering"}
    removed = []
    for s in list(state.get("player_statuses", [])):
        if s.get("id") in debuff_ids:
            removed.append(s.get("id"))
            state["player_statuses"].remove(s)
    if removed:
        log.append({"kind": "priest_cleanse", "text": f"Cleansed: {', '.join(removed)}"})


def _priest_tick_end_of_turn(state: dict, character: dict, log: list) -> None:
    """Tick Priest-specific state at end of turn (stat_mods handled in main loop)."""
    if not _is_priest(character):
        return

    # Tick Smite active duration — remove insight bonus when it expires
    if state.get("priest_smite_active", 0) > 0:
        state["priest_smite_active"] -= 1
        if state["priest_smite_active"] <= 0:
            character["stats"]["insight"] = character["stats"].get("insight", 0) - 10
            log.append({"kind": "priest_smite_end", "text": "Smite fades — Insight returns to normal."})


def _priest_check_enemy_heal_lock(state: dict, character: dict) -> bool:
    """Avatar of Faith (L100): the enemy cannot heal.

    Same story as _priest_start_of_turn — the `def` line was lost, so this
    one-line body was left as a stray `return` at the tail of
    _priest_tick_end_of_turn (which is typed `-> None` and whose callers ignore
    the value). combat_turn called it by name whenever a monster tried to heal,
    raising NameError.
    """
    return character.get("level", 1) >= 100


def _classify_skill(skill: dict) -> str:
    """Classify a monster skill as 'attack', 'defense', or 'utility' based on its properties."""
    ptype = skill.get("power_type", "strike")
    trigger = skill.get("trigger", "always")
    if ptype == "strike":
        return "attack"
    if ptype == "debuff":
        # Debuffs that target enemy = attack; debuffs that buff self on low_hp = defense
        if trigger == "low_hp":
            return "defense"
        return "attack"
    if ptype == "heal":
        return "defense"
    if ptype in ("buff", "defend"):
        if trigger == "low_hp":
            return "defense"
        return "utility"
    return "utility"


# ============================================================
# TAME PROFILE CONFIG — per creature tier
# ============================================================
TIER_TAME_CONFIG: dict[str, dict] = {
    "normal":     {"tame_hp": 0.30, "tame_chance": 0.40, "failure_penalty": "enraged"},
    "mini_boss":  {"tame_hp": 0.25, "tame_chance": 0.25, "failure_penalty": "enraged"},
    "boss":       {"tame_hp": 0.15, "tame_chance": 0.15, "failure_penalty": "furious"},
    "legendary":  {"tame_hp": 0.10, "tame_chance": 0.05, "failure_penalty": "unstoppable"},
    "event_boss": {"tame_hp": 0.05, "tame_chance": 0.02, "failure_penalty": "cataclysmic"},
}


def _ensure_monster_fields(monster: dict) -> dict:
    """Fill in missing stat/skill/drop/affinity/profile fields for old monsters.
    Returns a shallow-copied dict with all fields guaranteed.

    New profile fields added:
    - passive_buff: list of buff dicts granted to Druid while summoned
    - profile_skills: dict with 'attack', 'defense', 'utility' keys (each a list of skills)
    - signature_fusion: list of signature fusion ability dicts
    - boss_aura: optional battlefield aura (boss+ only)
    - legendary_passive: optional unique passive mechanic (legendary+ only)
    - creature_tier: 'normal', 'mini_boss', 'boss', 'legendary', 'event_boss'
    """
    m = dict(monster)  # shallow copy
    if "stats" not in m:
        # Every monster in the data now ships explicit stats; this is only a
        # guard for hand-built or test monsters.
        m["stats"] = {
            "might": 5, "insight": 2, "grace": 3,
            "durability": 3, "essence": 1, "cognition": 2,
        }

    # --- Stat normalization: convert legacy stat names and flat ints to base/growth ---
    stats = m["stats"]
    # Rename vitality → durability, armor → armor_bonus
    if "vitality" in stats and "durability" not in stats:
        stats["durability"] = stats.pop("vitality")
    elif "vitality" in stats and "durability" in stats:
        stats.pop("vitality")  # durability already present, drop vitality
    if "armor" in stats:
        armor_val = stats.pop("armor")
        # Fold armor into durability (add to existing) since character system uses armor_bonus separately
        stats["durability"] = stats.get("durability", 0) + armor_val
    # Convert flat int stats to {"base": X, "growth": Y} format
    p = compute_monster_threat(m)
    default_growth = max(0.5, p * 0.08)
    for stat_name, val in list(stats.items()):
        if isinstance(val, (int, float)) and not isinstance(val, bool):
            stats[stat_name] = {"base": int(val), "growth": round(default_growth, 1)}
    if "life" not in m:
        m["life"] = {"mp": 0, "stamina": 100, "shield": 0}
    if "skills" not in m:
        m["skills"] = []
    if "affinities" not in m:
        m["affinities"] = {"weak": [], "resist": []}
    if "drops" not in m or isinstance(m["drops"], list):
        old_drops = m.get("drops", [])
        if isinstance(old_drops, list):
            # Convert old tuple format to new dict format
            common = [{"id": d[0], "chance": d[1], "qty": [1, 1]} for d in old_drops if isinstance(d, (tuple, list))]
            m["drops"] = {"common": common, "rare": [], "boss": [], "gold": [2, 8], "xp_mult": 1.0}

    # --- New profile system fields ---
    # Determine creature tier
    if "creature_tier" not in m:
        if m.get("is_event_boss"):
            m["creature_tier"] = "event_boss"
        elif m.get("is_legendary_creature"):
            m["creature_tier"] = "legendary"
        elif m.get("is_boss") or m.get("is_heritage_boss"):
            # Heritage bosses with very high power are legendary-tier
            if compute_monster_threat(m) >= 45:
                m["creature_tier"] = "legendary"
            else:
                m["creature_tier"] = "boss"
        elif m.get("rarity") == "legendary" and m.get("is_boss"):
            m["creature_tier"] = "legendary"
        elif m.get("is_mini_boss"):
            m["creature_tier"] = "mini_boss"
        else:
            m["creature_tier"] = "normal"

    # Ensure passive_buff exists (normalized to list of buff dicts)
    if "passive_buff" not in m:
        # Generate a basic passive buff based on highest stat
        p = compute_monster_threat(m)
        stats = m.get("stats", {})
        # Find highest stat
        best_stat = "might"
        best_val = 0
        for s, v in stats.items():
            sv = v.get("base", 0) if isinstance(v, dict) else v
            if sv > best_val:
                best_val = sv
                best_stat = s
        buff_type_map = {
            "might": "might_bonus", "grace": "evasion_bonus",
            "cognition": "cognition_bonus", "insight": "crit_chance",
            "essence": "magic_resist", "durability": "durability_bonus",
        }
        m["passive_buff"] = [{"type": buff_type_map.get(best_stat, "might_bonus"), "value": 0.10}]
    else:
        m["passive_buff"] = _normalize_passive_buff(m["passive_buff"])

    # Categorize existing flat skills list into profile_skills if not already done
    if "profile_skills" not in m:
        flat_skills = m.get("skills", [])
        profile = {"attack": [], "defense": [], "utility": []}
        for sk in flat_skills:
            cat = _classify_skill(sk)
            profile[cat].append(sk)
        # If no skills at all, generate basic ones from power
        if not flat_skills:
            p = compute_monster_threat(m)
            mid = m.get("id", "monster")
            profile["attack"] = [{
                "id": f"{mid}_basic_strike", "name": "Basic Strike",
                "power_type": "strike", "damage_type": "physical",
                "damage": max(3, p // 2), "cost_mp": 0, "cost_stamina": 20,
                "cooldown": 1, "trigger": "always",
            }]
            profile["defense"] = [{
                "id": f"{mid}_basic_guard", "name": "Basic Guard",
                "power_type": "buff", "cost_mp": 0, "cost_stamina": 25,
                "cooldown": 3, "trigger": "low_hp",
                "self_status": "warded", "stat_mod": {"self": {"durability": 2}},
                "mod_duration": 2,
            }]
            profile["utility"] = [{
                "id": f"{mid}_basic_rally", "name": "Rally",
                "power_type": "buff", "cost_mp": 0, "cost_stamina": 20,
                "cooldown": 3, "trigger": "always",
                "self_status": "inspired", "stat_mod": {"self": {"might": 2}},
                "mod_duration": 2,
            }]
        m["profile_skills"] = profile

    # Ensure signature_fusion exists (normalized to list)
    if "signature_fusion" not in m:
        # Generate a basic signature for legacy monsters
        p = compute_monster_threat(m)
        mid = m.get("id", "monster")
        m["signature_fusion"] = [{
            "id": f"{mid}_signature", "name": "Signature Strike",
            "power_type": "strike", "damage_type": "physical",
            "damage": max(8, p), "cost_mp": 0, "cost_stamina": 50,
            "cooldown": 4, "hits": 1, "is_signature": True,
        }]
    else:
        m["signature_fusion"] = _normalize_signature_fusion(m["signature_fusion"])

    # Boss+ fields
    if "boss_aura" not in m:
        m["boss_aura"] = None
    if "legendary_passive" not in m:
        m["legendary_passive"] = None

    # Ensure personality and archetype exist
    if "personality" not in m:
        # Derive personality from species/tags if possible
        species = m.get("species", "")
        tags = m.get("tags", [])
        if species in ("construct", "undead") or "construct" in tags:
            m["personality"] = "guardian"
        elif species in ("beast", "animal") or "beast" in tags:
            m["personality"] = "aggressive"
        elif species == "magical":
            m["personality"] = "opportunist"
        else:
            m["personality"] = "aggressive"
    if "archetype" not in m:
        # Derive archetype from stats
        stats = m.get("stats", {})
        might_val = stats.get("might", {}).get("base", 0) if isinstance(stats.get("might"), dict) else stats.get("might", 0)
        cog_val = stats.get("cognition", {}).get("base", 0) if isinstance(stats.get("cognition"), dict) else stats.get("cognition", 0)
        dur_val = stats.get("durability", {}).get("base", 0) if isinstance(stats.get("durability"), dict) else stats.get("durability", 0)
        if cog_val > might_val and cog_val > dur_val:
            m["archetype"] = "caster"
        elif dur_val > might_val:
            m["archetype"] = "tank"
        else:
            m["archetype"] = "striker"

    # --- Tame profile fields ---
    tier = m.get("creature_tier", "normal")
    tame_cfg = TIER_TAME_CONFIG.get(tier, TIER_TAME_CONFIG["normal"])
    if "tame_hp" not in m:
        m["tame_hp"] = tame_cfg["tame_hp"]
    if "tame_chance" not in m:
        m["tame_chance"] = tame_cfg["tame_chance"]
    if "tame_failure_penalty" not in m:
        m["tame_failure_penalty"] = tame_cfg["failure_penalty"]

    return m


def attempt_tame(character: dict, state: dict) -> dict:
    """Attempt to tame the current monster in combat.
    Requires monster HP below tame_hp threshold.
    On success: monster is tamed (added to bestiary).
    On failure: failure penalty applies based on creature tier.

    Passives:
    - Wild Heart (level 10): Unlocks taming, +5% chance on normal creatures
    - Apex Tamer (level 50): Unlocks mini-boss taming, +10% on all creatures
    - Mythic Tamer (level 85): Unlocks boss taming, +15% on boss+ creatures
    """
    # Wild Heart (level 10): required to tame at all
    if character.get("level", 1) < 10:
        return {"error": "You need the Wild Heart passive (level 10) to tame creatures."}

    monster = state.get("monster_ref")
    if not monster:
        return {"error": "No monster to tame."}
    if not state.get("active"):
        return {"error": "Combat is not active."}

    # One tame attempt per enemy per combat
    if state.get("tame_attempted"):
        return {"error": "You can only attempt to tame a creature once per combat."}

    # Cannot tame constructs, undead, or other players
    monster_category = _monster_category(monster)
    if monster_category in ("construct", "undead"):
        return {"error": f"Cannot tame {monster_category} creatures."}

    # Tier-based taming unlock checks
    tier = monster.get("creature_tier", "normal")
    if tier == "mini_boss" and character.get("level", 1) < 50:
        return {"error": "You need the Apex Tamer passive (level 50) to tame mini-boss creatures."}
    if tier in ("boss", "legendary", "event_boss") and character.get("level", 1) < 85:
        return {"error": "You need the Mythic Tamer passive (level 85) to tame boss creatures."}

    tame_hp_threshold = monster.get("tame_hp", 0.30)
    current_hp_ratio = state["monster_hp"] / max(1, state["monster_max_hp"])

    if current_hp_ratio > tame_hp_threshold:
        return {"error": f"The {monster['name']} is too strong to tame (must be below {int(tame_hp_threshold * 100)}% HP)."}

    # Mark attempt
    state["tame_attempted"] = True

    # Base tame chance from tier config
    tame_chance = monster.get("tame_chance", 0.40)

    # Cognition-based adjustment: +cognition_diff% per point above/below enemy resistance
    cog = character.get("stats", {}).get("cognition", 5)
    enemy_resist = monster.get("stats", {}).get("cognition", 5)
    # Handle base/growth dict stats
    if isinstance(cog, dict):
        cog = cog.get("base", 5)
    if isinstance(enemy_resist, dict):
        enemy_resist = enemy_resist.get("base", 5)
    cog_diff = cog - enemy_resist
    # Scale: +5% per point above (normal), +4% (mini-boss), +3% (boss), +2% (legendary), +1% (event boss)
    cog_scale = {"normal": 0.05, "mini_boss": 0.04, "boss": 0.03, "legendary": 0.02, "event_boss": 0.01}
    scale = cog_scale.get(tier, 0.05)
    tame_chance += cog_diff * scale

    # Wild Heart (level 10): +5% on normal creatures
    if character.get("level", 1) >= 10 and tier == "normal":
        tame_chance += 0.05

    # Apex Tamer (level 50): +10% on all creatures
    if character.get("level", 1) >= 50:
        tame_chance += 0.10

    # Mythic Tamer (level 85): +15% on boss+ creatures
    if character.get("level", 1) >= 85 and tier in ("boss", "legendary", "event_boss"):
        tame_chance += 0.15

    # Beast Taming profession rank bonus
    taming_prof = next((p for p in character.get("professions", []) if p["id"] == "beast_taming"), None)
    if taming_prof:
        rank_bonus = {"novice": 0.0, "apprentice": 0.02, "journeyman": 0.05,
                      "expert": 0.08, "master": 0.12, "grandmaster": 0.15}
        tame_chance += rank_bonus.get(taming_prof.get("rank", "novice"), 0.0)

    # Clamp chance based on tier
    chance_caps = {"normal": (0.10, 0.90), "mini_boss": (0.05, 0.60), "boss": (0.05, 0.50),
                   "legendary": (0.02, 0.25), "event_boss": (0.01, 0.10)}
    min_chance, max_chance = chance_caps.get(tier, (0.10, 0.90))
    tame_chance = max(min_chance, min(max_chance, tame_chance))

    roll = random.random()
    if roll < tame_chance:
        # Success!
        state["active"] = False
        state["tamed"] = True
        log = [{"kind": "tame_success",
                "text": f"You successfully tame the {monster['name']}! It joins your bestiary."}]
        state["log"].extend(log)
        return {"success": True, "monster": monster, "log": log}

    # Failure — apply penalty based on tier
    penalty = monster.get("tame_failure_penalty", "enraged")
    log = [{"kind": "tame_fail",
            "text": f"The {monster['name']} resists your taming attempt!"}]

    if penalty == "enraged":
        state["monster_enraged"] = True
        log.append({"kind": "tame_penalty", "text": f"The {monster['name']} enrages!"})
    elif penalty == "furious":
        state["monster_enraged"] = True
        # +1 turn enrage (already permanent in current system, but mark it)
        state["monster_furious"] = True
        log.append({"kind": "tame_penalty", "text": f"The {monster['name']} becomes FURIOUS! Enrage extended!"})
    elif penalty == "unstoppable":
        state["monster_enraged"] = True
        state["monster_furious"] = True
        # Cleanse all debuffs from monster
        state["monster_statuses"] = [s for s in state.get("monster_statuses", []) if s.get("kind") == "buff"]
        # Full heal
        state["monster_hp"] = state["monster_max_hp"]
        log.append({"kind": "tame_penalty", "text": f"The {monster['name']} becomes UNSTOPPABLE! Full heal, debuffs cleansed!"})
    elif penalty == "cataclysmic":
        state["monster_enraged"] = True
        state["monster_furious"] = True
        state["monster_statuses"] = [s for s in state.get("monster_statuses", []) if s.get("kind") == "buff"]
        state["monster_hp"] = state["monster_max_hp"]
        # Enrage allies (if multiple enemies — for now just boost monster further)
        state["monster_threat"] = int(state.get("monster_threat", 5) * 1.3)
        log.append({"kind": "tame_penalty", "text": f"The {monster['name']} triggers a CATACLYSM! Full heal, cleansed, power surge!"})

    state["log"].extend(log)
    return {"success": False, "penalty": penalty, "log": log}


def _pick_monster_skill(monster: dict, state: dict, hp_ratio: float, enemy_hp_ratio: float, turn: int) -> dict | None:
    """Pick the best available monster skill using the new profile AI logic.

    AI priority is modified by personality:
    - aggressive: Attack first; Defense only when HP < 30%; Utility only when HP < 15%
    - protective: Defense when HP < 70%; Attack otherwise
    - opportunist: Utility when enemy < 50% HP; Attack otherwise
    - guardian: Turn 1 Defense; alternate Attack/Defense
    - taunting: Defense when HP < 60%; Attack otherwise
    - Standard (no personality): HP < 30% → Utility; HP < 50% → Defense; else Attack

    Falls back to flat skills list if profile_skills not present.
    """
    mp = state.get("monster_mp", 0)
    stamina = state.get("monster_stamina", 100)
    cooldowns = state.get("monster_skill_cooldowns", {})
    enraged = state.get("monster_enraged", False)
    personality = monster.get("personality", "aggressive")

    # Use profile_skills if available, otherwise fall back to flat skills
    profile = monster.get("profile_skills")
    if profile and any(profile.values()):
        # Determine which category to pick from based on personality + AI logic
        if personality == "aggressive":
            if hp_ratio < 0.15 and profile.get("utility"):
                candidates = profile["utility"]
            elif hp_ratio < 0.30 and profile.get("defense"):
                candidates = profile["defense"]
            else:
                candidates = profile.get("attack") or profile.get("defense") or profile.get("utility") or []
        elif personality == "protective":
            if hp_ratio < 0.70 and profile.get("defense"):
                candidates = profile["defense"]
            elif profile.get("attack"):
                candidates = profile["attack"]
            else:
                candidates = profile.get("defense") or profile.get("utility") or []
        elif personality == "opportunist":
            if enemy_hp_ratio < 0.50 and profile.get("utility"):
                candidates = profile["utility"]
            elif hp_ratio < 0.30 and profile.get("utility"):
                candidates = profile["utility"]
            elif profile.get("attack"):
                candidates = profile["attack"]
            else:
                candidates = profile.get("defense") or profile.get("utility") or []
        elif personality == "guardian":
            if turn == 0 and profile.get("defense"):
                candidates = profile["defense"]
            elif turn % 2 == 1 and profile.get("defense"):
                candidates = profile["defense"]
            elif profile.get("attack"):
                candidates = profile["attack"]
            else:
                candidates = profile.get("defense") or profile.get("utility") or []
        elif personality == "taunting":
            if hp_ratio < 0.60 and profile.get("defense"):
                candidates = profile["defense"]
            elif profile.get("attack"):
                candidates = profile["attack"]
            else:
                candidates = profile.get("defense") or profile.get("utility") or []
        else:
            # Standard AI
            if hp_ratio < 0.30 and profile.get("utility"):
                candidates = profile["utility"]
            elif hp_ratio < 0.50 and profile.get("defense"):
                candidates = profile["defense"]
            else:
                candidates = profile.get("attack") or profile.get("defense") or profile.get("utility") or []

        # Filter by resources and cooldowns
        usable = []
        for sk in candidates:
            sid = sk["id"]
            if cooldowns.get(sid, 0) > 0:
                continue
            if sk.get("cost_mp", 0) > mp:
                continue
            if sk.get("cost_stamina", 0) > stamina:
                continue
            usable.append(sk)

        if not usable:
            # Fall back to any available skill from any category
            all_skills = profile.get("attack", []) + profile.get("defense", []) + profile.get("utility", [])
            usable = [sk for sk in all_skills
                      if cooldowns.get(sk["id"], 0) <= 0
                      and sk.get("cost_mp", 0) <= mp
                      and sk.get("cost_stamina", 0) <= stamina]

        if not usable:
            return None

        # Pick highest power skill from usable candidates
        # Ultimates get priority when enraged
        best = None
        best_score = -1
        for sk in usable:
            is_ult = sk.get("is_ultimate", False)
            if is_ult and not enraged:
                continue
            ptype = sk.get("power_type", "strike")
            if ptype == "strike":
                score = sk.get("damage", 5) + (50 if is_ult else 0)
            elif ptype == "heal":
                score = sk.get("damage", 10) + 20
            elif ptype == "buff":
                score = 15
            elif ptype == "debuff":
                score = 10
            else:
                score = 5
            if score > best_score:
                best = sk
                best_score = score
        return best

    # --- Legacy fallback: flat skills list ---
    skills = monster.get("skills", [])
    if not skills:
        return None

    best = None
    best_score = -1
    for sk in skills:
        sid = sk["id"]
        if cooldowns.get(sid, 0) > 0:
            continue
        if sk.get("cost_mp", 0) > mp:
            continue
        if sk.get("cost_stamina", 0) > stamina:
            continue
        trig = sk.get("trigger", "always")
        if trig == "low_hp" and hp_ratio > 0.4:
            continue
        if trig == "opponent_wounded" and enemy_hp_ratio > 0.6:
            continue
        if trig == "opening_move" and turn > 0:
            continue
        ptype = sk.get("power_type", "strike")
        is_ult = sk.get("is_ultimate", False)
        if is_ult and not enraged:
            continue
        if ptype == "strike":
            score = sk.get("damage", 5) + (50 if is_ult else 0)
        elif ptype == "heal" and hp_ratio < 0.5:
            score = sk.get("damage", 10) + 20
        elif ptype == "buff" and hp_ratio < 0.5:
            score = 15
        elif ptype == "debuff":
            score = 10
        else:
            score = 5
        if score > best_score:
            best = sk
            best_score = score
    return best
def skin_monster(character: dict, state: dict) -> dict:
    """Player-initiated skinning of a defeated monster.
    Anyone can attempt it; Hunting profession rank improves the roll.
    Returns {items, log, skinned} or {error}."""
    if not state.get("skinnable"):
        return {"error": "This creature cannot be skinned."}
    if state.get("skinned"):
        return {"error": "You have already skinned this creature."}

    monster = get_monster(state["monster_id"])
    if not monster:
        return {"error": "Unknown creature."}

    m = _ensure_monster_fields(monster)
    drops_data = m.get("drops", {})

    # Collect all possible drop item ids from the monster
    possible_items = []
    if isinstance(drops_data, dict):
        for category in ("common", "rare", "boss"):
            for drop in drops_data.get(category, []):
                possible_items.append(drop["id"])
    elif isinstance(drops_data, list):
        for drop_id, _chance in drops_data:
            possible_items.append(drop_id)

    if not possible_items:
        state["skinned"] = True
        return {"items": [], "log": f"{character['name']} finds nothing worth harvesting on the {monster['name']}.", "skinned": True}

    # Check Hunting profession
    profs = character.get("professions", []) or []
    hunt_prof = next((p for p in profs if p.get("id") == "hunting"), None)
    has_hunting = hunt_prof is not None
    rank = RANK_ORDER.get(hunt_prof.get("rank", "novice"), 0) if has_hunting else 0

    # Skin roll: d6 + rank modifier (non-hunters get -2, novice hunters get -1, grandmaster +4)
    roll = random.randint(1, 6)
    if has_hunting:
        modified_roll = max(1, min(6, roll + rank - 1))
    else:
        modified_roll = max(1, min(6, roll - 2))

    # Yield tiers
    if modified_roll <= 1:
        # Failed skin — ruined the hide
        carve = []
        msg = f"{character['name']} fumbles the skinning. The hide is ruined."
    elif modified_roll <= 2:
        # Poor: 1 common material
        carve = [(random.choice(possible_items), 1)]
        msg = f"{character['name']} salvages a scrap from the {monster['name']}."
    elif modified_roll <= 4:
        # Normal: 1-2 materials
        n = min(2, len(possible_items))
        carve = [(iid, 1) for iid in random.sample(possible_items, n)]
        msg = f"{character['name']} skins the {monster['name']} with steady hands."
    elif modified_roll == 5:
        # Good: 2-3 materials, 1-2 qty
        n = min(3, len(possible_items))
        carve = [(iid, random.randint(1, 2)) for iid in random.sample(possible_items, n)]
        msg = f"{character['name']} expertly harvests the {monster['name']}."
    else:
        # Perfect: 3-5 materials + bonus
        n = min(len(possible_items), 3 + (rank // 2))
        carve = [(iid, random.randint(1, 2)) for iid in random.sample(possible_items, min(n, len(possible_items)))]
        if rank >= 4 and possible_items:
            carve.append((random.choice(possible_items), 2))
        msg = f"{character['name']} performs a flawless harvest on the {monster['name']}!"

    # Give Hunting profession XP for skinning
    if has_hunting and carve:
        from professions import craft_points_for_roll, gain_profession_xp
        from world_data import xp_multiplier_for
        outcome_map = {1: 0, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6}
        pts = craft_points_for_roll(outcome_map.get(modified_roll, 3))
        pts = int(pts * xp_multiplier_for(character.get("current_continent"), "hunting"))
        if pts > 0:
            rank_change = gain_profession_xp(character, "hunting", pts)
        else:
            rank_change = None
    else:
        rank_change = None

    # Add items to character inventory
    for item_id, qty in carve:
        _add_item_to_inventory(character, item_id, qty)

    state["skinned"] = True
    state["skinnable"] = False

    return {
        "items": carve,
        "log": msg,
        "roll": modified_roll,
        "raw_roll": roll,
        "has_hunting": has_hunting,
        "rank_change": rank_change,
        "skinned": True,
    }


def _add_item_to_inventory(character: dict, item_id: str, qty: int):
    """Add qty of item_id to character's inventory, stacking if present."""
    inv = character.setdefault("inventory", [])
    entry = next((i for i in inv if i.get("item_id") == item_id), None)
    if entry:
        entry["quantity"] = entry.get("quantity", 0) + qty
    else:
        inv.append({"item_id": item_id, "quantity": qty})


_RARITY_GOLD_MULT = {
    "common": 1.0, "uncommon": 1.25, "rare": 1.5, "epic": 2.0, "legendary": 3.0,
}


def _sanctuary_blessing_xp_mult(character: dict) -> float:
    """Returns 1.05 if sanctuary_blessing buff is active, else 1.0."""
    if any(s.get("id") == "sanctuary_blessing" for s in character.get("statuses", [])):
        return 1.05
    return 1.0


def _roll_loot(monster: dict, character: dict | None = None, critical: bool = False) -> tuple[list, int, int]:
    """Unified loot roll for all monster drop situations.
    Uses cognition as luck modifier, hunting profession for drop bonus,
    rarity-scaled gold, and jackpot rare-drop chance.
    Returns (items, xp, gold)."""
    m = _ensure_monster_fields(monster)
    drops_data = m.get("drops", {})
    drops = []
    rarity = m.get("rarity", "common")
    # Reward scale now derives from the monster's stats rather than the retired
    # `power` scalar. Coefficients below were recalibrated against the new threat
    # distribution (old power median 32 -> new threat median 18) so gold and XP
    # keep their previous magnitudes.
    _monster_threat = compute_monster_threat(m, (character or {}).get("level", 1))

    # --- Item bonus effects (runes) ---
    _ibe = _aggregate_item_bonus_effects(character) if character else {}

    # --- Cognition luck modifier ---
    cog = 0
    if character:
        cog = character.get("stats", {}).get("cognition", 0)
    luck_mult = min(2.0, 1.0 + cog * 0.02)  # +2% per cognition point, capped at 2x

    # --- Hunting profession bonus ---
    hunt_bonus = 0.0
    if character:
        profs = character.get("professions", []) or []
        hunt_prof = next((p for p in profs if p.get("id") == "hunting"), None)
        if hunt_prof:
            rank = RANK_ORDER.get(hunt_prof.get("rank", "novice"), 0)
            hunt_bonus = rank * 0.05  # +5% per rank above novice (novice=0)

    # --- Critical bonus ---
    crit_mult = 1.5 if critical else 1.0

    # --- Roll drops ---
    if isinstance(drops_data, dict):
        # Boss pool (guaranteed-style, high chance)
        for drop in drops_data.get("boss", []):
            chance = min(0.95, drop["chance"] * crit_mult)
            if random.random() <= chance:
                qty = random.randint(drop["qty"][0], drop["qty"][1])
                drops.append((drop["id"], qty))

        # Rare pool
        for drop in drops_data.get("rare", []):
            chance = min(0.95, drop["chance"] * luck_mult * crit_mult * (1.0 + hunt_bonus + _ibe.get("rare_drop", 0)))
            if random.random() <= chance:
                qty = random.randint(drop["qty"][0], drop["qty"][1])
                drops.append((drop["id"], qty))

        # Common pool
        for drop in drops_data.get("common", []):
            chance = min(0.95, drop["chance"] * luck_mult * crit_mult * (1.0 + hunt_bonus + _ibe.get("item_drop", 0)))
            if random.random() <= chance:
                qty = random.randint(drop["qty"][0], drop["qty"][1])
                drops.append((drop["id"], qty))

        # --- Jackpot roll: extra rare drop chance ---
        is_boss = m.get("is_boss", False) or bool(drops_data.get("boss", []))
        if not is_boss and drops_data.get("rare", []):
            jackpot_chance = min(0.25, 0.03 + cog * 0.005)  # 3% base + 0.5% per cognition
            if critical:
                jackpot_chance *= 1.5
            if random.random() <= jackpot_chance:
                jackpot_drop = random.choice(drops_data["rare"])
                qty = random.randint(jackpot_drop["qty"][0], jackpot_drop["qty"][1])
                drops.append((jackpot_drop["id"], qty))

        # --- Gold with rarity scaling ---
        gold_range = drops_data.get("gold", [2, 8])
        rarity_mult = _RARITY_GOLD_MULT.get(rarity, 1.0)
        base_gold = random.randint(gold_range[0], gold_range[1])
        gold = int(base_gold * rarity_mult * crit_mult * (1.0 + _ibe.get("gold_drop", 0)))

        xp_mult = drops_data.get("xp_mult", 1.0)
    else:
        # Old list format fallback
        for drop_id, chance in drops_data:
            eff_chance = min(0.95, chance * luck_mult * crit_mult * (1.0 + hunt_bonus))
            if random.random() <= eff_chance:
                drops.append((drop_id, 1))
        base_gold = 8 + int(_monster_threat * 3.5)
        rarity_mult = _RARITY_GOLD_MULT.get(rarity, 1.0)
        gold = int(base_gold * rarity_mult * crit_mult * (1.0 + _ibe.get("gold_drop", 0)))
        xp_mult = 1.0

    xp = int((20 + _monster_threat * 7) * xp_mult * (1.0 + _ibe.get("xp_bonus", 0)))

    # --- Procedural gear drop (new item system) ---
    if character:
        _luck = min(0.20, cog * 0.005)  # luck bonus from cognition
        _gear_chance = m.get("gear_drop_chance", 0.08)
        _gear_chance = min(0.95, _gear_chance * (1.0 + _luck) * crit_mult * (1.0 + _ibe.get("item_drop", 0)))
        if random.random() <= _gear_chance:
            _gear_drop = generate_drop(m, character_luck=_luck)
            if _gear_drop:
                drops.append((_gear_drop, 1))
        # Rune drop
        _rune_chance = m.get("rune_drop_chance", 0.02)
        _rune_chance = min(0.95, _rune_chance * (1.0 + _luck) * crit_mult * (1.0 + _ibe.get("rare_drop", 0)))
        if random.random() <= _rune_chance:
            _rune_drop = generate_rune_drop(m)
            if _rune_drop:
                drops.append((_rune_drop, 1))

    # Continental bonus: Gennel beast_material_chance — extra drop from beasts
    if character and _monster_category(m) == "beast":
        _bm = continental_bonus_for(character.get("current_continent", ""), "beast_material_chance")
        if _bm and random.random() < float(_bm) and drops:
            bonus_drop = drops[0]
            drops.append((bonus_drop[0], 1))

    # Heritage month bonus: +25% combat XP on heritage continent
    if character:
        _cid = character.get("current_continent", "")
        if _cid and is_heritage_month_for(_cid):
            _hb = get_heritage_bonuses(_cid)
            if _hb:
                xp = int(xp * _hb.get("combat_xp_mult", 1.0))

    return drops, xp, gold


def start_combat(character: dict, monster_id) -> dict:
    # Heritage boss: accept a pre-built monster dict directly
    if isinstance(monster_id, dict):
        monster = monster_id
        monster_key = monster_id.get("id", "unknown")
    else:
        monster = get_monster(monster_id)
        monster_key = monster_id
    if not monster:
        return {"error": f"Unknown monster: {monster_key}"}
    m = _ensure_monster_fields(monster)
    life = m.get("life", {})

    # Compute monster stats using growth formula if stats have base/growth dicts
    char_level = character.get("level", 1)
    raw_stats = m.get("stats", {})
    computed_stats = {}
    has_growth = any(isinstance(v, dict) for v in raw_stats.values())
    if has_growth:
        for stat_name, stat_val in raw_stats.items():
            computed_stats[stat_name] = _compute_creature_stat(stat_val, char_level)
    else:
        computed_stats = raw_stats

    # Compute HP using growth formula if durability has base/growth
    dur_stat = raw_stats.get("durability")
    if isinstance(dur_stat, dict):
        computed_hp = _compute_creature_hp(m, char_level)
    else:
        computed_hp = monster["hp"]

    state = {
        "monster_id": monster_key,
        "monster_name": monster["name"],
        "monster_rarity": monster.get("rarity", "common"),
        "monster_hp": computed_hp,
        "monster_max_hp": computed_hp,
        "monster_threat": compute_monster_threat(monster, char_level),
        "monster_stats": computed_stats,
        "monster_max_mp": life.get("mp", 0),
        "monster_mp": life.get("mp", 0),
        "monster_max_stamina": life.get("stamina", 100),
        "monster_stamina": life.get("stamina", 100),
        "monster_shield": life.get("shield", 0),
        "monster_max_shield": life.get("shield", 0),
        "monster_skills": m.get("skills", []),
        "monster_skill_cooldowns": {},
        "monster_affinities": m.get("affinities", {"weak": [], "resist": []}),
        "monster_enraged": False,
        "monster_is_boss": m.get("is_boss", False),
        "monster_is_heritage_boss": m.get("is_heritage_boss", False),
        "heritage_continent": m.get("heritage_continent"),
        "heritage_token_count": m.get("heritage_token_count", 0),
        "monster_statuses": [],
        "player_statuses": list(character.get("statuses", [])),
        "player_hp": character["hp"],
        "player_max_hp": character["max_hp"],
        # Stamina meters. `player_max_stamina` was read by the stamina consumable
        # branch but never initialised anywhere — a phantom state key of exactly the
        # kind that made the Mage's cooldown passives unreachable.
        "player_stamina": 100,
        "player_max_stamina": 100,
        "turn": 0,
        "skill_cooldowns": {},
        "item_cooldowns": {},
        "skill_capacity_used": 0,
        "max_skill_capacity": compute_skill_capacity(character),
        "log": [],
        "active": True,
        # Monster profile reference (for tame, summon, etc.)
        "monster_ref": m,
        "monster_creature_tier": m.get("creature_tier", "normal"),
        "monster_personality": m.get("personality", "aggressive"),
        "monster_profile_skills": m.get("profile_skills", {}),
        "monster_passive_buff": m.get("passive_buff", []),
        "monster_signature_fusion": m.get("signature_fusion", []),
        "monster_boss_aura": m.get("boss_aura"),
        "monster_legendary_passive": m.get("legendary_passive"),
        # Day/night cycle
        "is_night": current_time_of_day() == "lunar",
        # Innate action / combo state
        "combo_count": 0,
        "combo_last_skill": None,
        "defending": False,
        "evading": False,
        "countering": False,
        "focused": False,
        # Alchemist state
        "alchemist_imbue": None,          # current imbue skill dict
        "alchemist_imbue_charges": 0,     # remaining charges
        "alchemist_imbue_hits": 0,        # hit counter for mini-rules
        "alchemist_cf": 0,                # Combo Flow points
        "alchemist_cf_max": 20,           # CF cap
        "alchemist_katar_cracked": False, # Forbidden Formula aftermath
        "alchemist_infinite_charges": 0,  # turns remaining of infinite charges (Philosopher's)
        "alchemist_max_mini_rules": False,# mini-rules at max effect (Philosopher's)
        "alchemist_ward_block": 0,        # turns enemy can't gain warded (Guard Break)
        "alchemist_enemy_launched": False,# enemy launched (Rising Strike)
        "alchemist_enemy_immobilized": 0, # turns enemy immobilized (Living Slime)
        "alchemist_poison_stacks": 0,     # poison scaling counter
        "alchemist_repositioned": False,  # behind enemy (Spinning Strike)
        "alchemist_struck_this_turn": False,  # tracks if Alchemist struck (for CF reset)
        "alchemist_pre_imbue": None,      # pre-combat imbue skill id (auto-loaded at combat start)
        # Paladin state
        "paladin_hp_tier": 0,             # current faith tier (0-6, 0=none, 6=≤5% HP)
        "paladin_faith_bonuses": None,    # dict of currently applied faith bonuses
        "paladin_bonus_armor": 0,         # bonus armor from faith scaling
        "paladin_bonus_essence": 0,       # bonus essence from faith scaling
        "paladin_heal_amp": 1.0,          # heal amplification multiplier
        "paladin_avatar_of_faith": False, # level 100 passive: all bonuses permanent
        "paladin_resurrection_used": False, # level 90 passive: survive at 1 HP
        # Knight state
        "knight_oath": None,              # current Oath: "iron", "wrath", "bulwark", "endurance", "vanguard"
        "knight_oath_stacks": 0,          # current Oath stacks
        "knight_oath_mastery": False,      # level 60 passive: 5+ stacks doubles Oath effect
        "knight_eternal_oath": False,     # level 100 passive: all Oath effects tripled
        "knight_adrenal_used": False,     # level 40 passive: once per combat might surge
        "knight_battle_hardened": 0,     # level 30 passive: permanent +10 armor
        # Lancer state
        "lancer_active_imbues": {},       # {element_id: {"skill_id": str, "duration": int, "stat_mods": dict}}
        "lancer_overload_used": False,    # level 90 passive: once per combat all 6 elements
        "lancer_overload_turns": 0,       # remaining turns of overload
        "lancer_overload_charges": 1,     # level 100: 2 charges
        "lancer_self_stat_mods": [],      # temporary self stat buffs from non-imbue skills
        "lancer_enemy_stat_mods": [],     # temporary enemy stat debuffs from strike/debuff skills
        # Mage state
        "mage_arcane_focus": 0,            # Arcane Focus for Dual Cast (0-3, gain on odd turns)
        "mage_strike_count": 0,            # for Arcane Surge passive (every 3rd strike)
        "mage_echo_next_turn": [],         # Echo Chamber: pending echo strikes for next turn
        "mage_glass_cannon_active": False,  # Glass Cannon: taking +50% damage this turn
        "mage_phobia_used": False,          # Phobia Implant: first debuff stun used
        "mage_rewind_used": False,          # Rewind: once per combat HP rewind
        "mage_prev_hp": 0,                 # Rewind: previous turn HP
        "mage_self_stat_mods": [],         # temporary self stat buffs from buff/defend skills
        "mage_enemy_stat_mods": [],        # temporary enemy stat debuffs from strike/debuff skills
        "mage_dual_cast_used": False,      # whether dual cast was used this turn
        # Assassin state
        "assassin_shadows": 0,             # current shadow count (0-100)
        "assassin_deposited_shadows": 0,   # shadows deposited as fear on current enemy
        "assassin_burst_ready": False,     # True when shadows reach threshold
        "assassin_burst_used": False,      # burst consumed this combat
        "assassin_shadow_linger": 0,      # turns of lingering evasion after stealth break
        "assassin_eclipse_blade_active": False,  # Eclipse Blade buff active
        # Hunter state
        "hunter_spirit_guidance": 0,          # current Spirit Guidance stacks (0+)
        "hunter_spirit_communion": False,     # True when stack 10 reached
        "hunter_range": 0,                    # current Range (turns before enemy closes) — hunter-specific bonuses
        "hunter_ambush_used": False,          # first attack from stealth = guaranteed crit
        "hunter_guaranteed_crits": 0,         # remaining guaranteed crit charges (Eagle Eye, Hawk Vision)
        "hunter_spirit_bow_charges": 0,       # Alpha Command: next N strikes true damage
        # Unified range system (all classes)
        "player_range": 0,                     # player's weapon range (+ hunter passives)
        "monster_range": 0,                    # monster's range value
        "range_gap": 0,                        # player_range - monster_range (positive = player advantage, negative = monster advantage)
        "hunter_world_hunt_active": False,    # World Hunt repeating every turn
        "hunter_spirit_copy_active": False,   # Spirit Copy decoy active
        "hunter_spirit_copy_absorb": False,   # Spirit Copy will absorb next hit
        "hunter_spirit_falcon_turns": 0,       # Spirit Falcon persists (communion)
        "hunter_spirit_wolf_turns": 0,         # Spirit Wolf persists (communion)
        "hunter_spirit_prison_active": False,  # Spirit Prison true DoT (communion)
        "hunter_intangible_turns": 0,         # Spirit Walk intangibility (communion)
        "hunter_immune_turns": 0,             # Survival Instinct immunity (communion)
        "hunter_sees_stealth": 0,             # Hawk Vision see-through-stealth turns
        "hunter_infinite_range": False,       # World Hunt infinite range (communion)
        "hunter_marked_target": False,        # Hunter's Mark: all allies gain crit (communion)
        "hunter_ancient_tracker_active": False,  # Ancient Tracker: +2 guidance per hit (communion)
        "hunter_tracking_instinct_active": False,  # Tracking Instinct: can't evade, +1 guidance (communion)
        "hunter_spirit_copy_bind_cd": 0,       # Spirit of the Wild: Spirit Bind cooldown
        # Druid state
        "druid_active_summons": [],           # list of active summon dicts
        "druid_fusion_active": False,         # True when fused with a summon
        "druid_fusion_turns": 0,              # remaining fusion turns
        "druid_fusion_summon_id": None,       # id of fused summon
        "druid_fusion_cooldowns": {},         # {summon_id: turns_remaining}
        "druid_fusion_sig_cooldowns": {},     # {sig_id: turns_remaining}
        "druid_pack_synergy": None,           # current pack synergy dict or None
        "druid_multi_fusion": False,          # level 90+: can fuse with multiple summons
        "druid_summon_enemy_stat_mods": [],   # enemy stat debuffs from summon skills
        "druid_aura_heal_reduction": 0,       # boss aura: heal reduction on enemy
        "druid_aura_magic_boost": 0,          # boss aura: magic damage boost
        "druid_aura_attack_boost": 0,         # boss aura: attack speed boost
        # Priest state
        "priest_shield_wall_hp": 0,           # current Shield Wall HP (0 = no shield)
        "priest_shield_wall_max": 0,          # max Shield Wall HP for reference
        "priest_shield_wall_skill": None,     # skill id that created the current shield
        "priest_hot_buffs": [],              # list of {heal_percent, turns_remaining, target}
        "priest_delayed_heals": [],          # list of {heal_percent, turns_remaining, target}
        "priest_smite_active": 0,            # turns remaining of Smite insight buff
        "priest_smiting": False,             # enemy was below 50% this combat
        "priest_shield_absorbed": 0,         # total damage absorbed by current shield (for Hand of God heal)
        "item_bonus_effects": {},             # aggregated bonus effects from equipped items
        "legendary_powers": [],               # active legendary power IDs from items + set bonuses
        "lp_strike_counter": {},              # per-power strike counter for every_nth_strike effects
        "lp_revive_used": False,              # Phoenix Rebirth once-per-combat flag
    }

    # Aggregate item bonus effects from equipped items
    state["item_bonus_effects"] = _aggregate_item_bonus_effects(character)

    # Aggregate legendary powers from equipped items and set bonuses
    state["legendary_powers"] = _aggregate_legendary_powers(character)

    # Apply flat stat bonuses from items (armor_bonus, evasion) to character stats
    _ibe = state["item_bonus_effects"]
    if _ibe.get("armor_bonus"):
        character["stats"]["armor_bonus"] = character["stats"].get("armor_bonus", 0) + int(_ibe["armor_bonus"])
    if _ibe.get("evasion"):
        character["stats"]["grace"] = character["stats"].get("grace", 0) + int(_ibe["evasion"])
    # armor_bonus_pct: percentage boost to current armor_bonus
    if _ibe.get("armor_bonus_pct", 0) > 0:
        _cur_armor = character["stats"].get("armor_bonus", 0)
        character["stats"]["armor_bonus"] = _cur_armor + int(_cur_armor * _ibe["armor_bonus_pct"])
    # max_hp_pct / max_mp_pct: increase max resources
    if _ibe.get("max_hp_pct", 0) > 0:
        _hp_bonus = int(character.get("max_hp", 100) * _ibe["max_hp_pct"])
        character["max_hp"] = character.get("max_hp", 100) + _hp_bonus
        character["hp"] = character.get("hp", 0) + _hp_bonus
    if _ibe.get("max_mp_pct", 0) > 0:
        _mp_bonus = int(character.get("max_mp", 50) * _ibe["max_mp_pct"])
        character["max_mp"] = character.get("max_mp", 50) + _mp_bonus
        character["mp"] = character.get("mp", 0) + _mp_bonus

    # Apply passive legendary powers at combat start
    _apply_legendary_powers_passive(state, character, [])

    # Paladin: initialize faith scaling immediately based on current HP
    if _is_paladin(character):
        # Avatar of Faith (level 100): all bonuses permanent
        if character.get("level", 1) >= 100:
            state["paladin_avatar_of_faith"] = True
        # Strip out-of-combat faith bonuses so combat scaling starts clean
        _ooc_bonuses = character.get("paladin_faith_bonuses")
        if _ooc_bonuses:
            for stat, val in _ooc_bonuses.items():
                if val:
                    character["stats"][stat] = character["stats"].get(stat, 0) - val
        _paladin_update_scaling(state, character, [])

    return state


def get_enchantment_bonus(character: dict, item_id: str) -> dict[str, int]:
    """Return enchantment stat bonuses for a given item from the character's inventory.

    Looks up the inventory entry for item_id and reads its 'enchantments' list.
    Returns {stat_name: total_bonus} dict.
    """
    inv = character.get("inventory", [])
    entry = next((i for i in inv if i.get("item_id") == item_id), None)
    if not entry or not entry.get("enchantments"):
        return {}
    bonuses: dict[str, int] = {}
    for ench in entry["enchantments"]:
        stat = ench.get("stat", "")
        bonus = int(ench.get("bonus", 0))
        if stat:
            bonuses[stat] = bonuses.get(stat, 0) + bonus
    return bonuses


def apply_enchantments_to_stats(character: dict) -> dict[str, int]:
    """Return effective stats = base_stats + equipped item stats + enchantment bonuses.
    Loops over all 12 equipment slots.
    Supports both old static items and new procedural item instances.
    Does not mutate the original character dict. Returns a new stats dict.
    """
    from game_data import EQUIP_SLOTS
    base_stats = dict(character.get("base_stats") or character.get("stats") or {})
    # Trained stats (from the gym/training system) are added to base
    trained = character.get("trained_stats") or {}
    for stat, val in trained.items():
        if val:
            base_stats[stat] = base_stats.get(stat, 0) + val
    equipped = character.get("equipped", {})
    seen_items = set()
    for slot in EQUIP_SLOTS:
        item_id = equipped.get(slot)
        if not item_id:
            continue
        # Don't double-count 2H weapons that occupy both hand slots
        if item_id in seen_items:
            continue
        seen_items.add(item_id)
        # Try new system first: look up via helper
        item = _get_equipped_item(character, slot)
        if not item:
            # Fallback to old lookup
            item = ITEMS_BY_ID.get(item_id)
        if not item:
            continue
        # Get stats from item (handles both old and new format)
        item_stats = _get_item_stats(item)
        for stat, val in item_stats.items():
            if val:
                base_stats[stat] = base_stats.get(stat, 0) + val
        # Keep enchantment bonuses for backward compat
        ench_bonuses = get_enchantment_bonus(character, item_id)
        for stat, bonus in ench_bonuses.items():
            base_stats[stat] = base_stats.get(stat, 0) + bonus

    # Set bonuses — applied ONCE for the whole character, after the slot loop.
    #
    # This used to live inside the loop above, which meant the bonus re-applied
    # for every equipped item, including items belonging to no set at all. Two
    # set pieces plus four unrelated items granted six times the intended stats,
    # so the optimal play was to wear the minimum set count and fill the rest
    # with junk.
    #
    # Tiers are also cumulative rather than exact-match. The old code did
    # `bonuses.get(count)`, so a set whose 3- and 4-piece tiers grant
    # bonus_effects/legendary_power instead of plain stats silently dropped the
    # 2-piece stat bonus once you equipped a third piece — wearing more of a set
    # made you strictly weaker.
    for set_id, count in _check_set_bonuses(character).items():
        tiers = _SET_BONUSES.get(set_id, {}).get("bonuses", {})
        for threshold in sorted(tiers):
            if threshold > count:
                break
            for stat, val in (tiers[threshold].get("stats") or {}).items():
                base_stats[stat] = base_stats.get(stat, 0) + val
    return base_stats


def skill_unusable_reason(skill_id: str, character: dict, state: dict,
                          hp_ratio: float, enemy_hp_ratio: float, turn: int) -> str | None:
    """Why this skill cannot be used right now, or None if it can.

    This is the single gate for skill legality. It exists because the auto-picker
    and manual selection used to disagree: `skill_id = manual_skill_id or
    _pick_next_skill(...)` meant a manually chosen skill skipped the picker
    entirely, so **skill capacity and trigger conditions were never checked for
    manual picks** — only cooldown and weapon_req were re-tested further down.

    The practical effect was that the two systems creating tactical constraint in a
    turn were advisory for anyone clicking skills, which is the normal way to play:

      - 107 of 350 skills carry a non-`always` trigger. `legend_of_erchis`
        ("only usable below 25% HP") was castable at full health; `lions_charge`
        ("opening move only. There is no second charge") was spammable.
      - Skill capacity (`2 + Cognition // 2`) was deducted but never enforced, so a
        cap-3 character could burn 6 skills and the HUD displayed "-3/3".
    """
    skill = SKILLS_BY_ID.get(skill_id)
    if not skill:
        return "unknown skill"

    if state.get("skill_cooldowns", {}).get(skill_id, 0) > 0:
        left = state["skill_cooldowns"][skill_id]
        return f"on cooldown ({left} turn(s) left)"

    weapon_req = SKILL_EXTRAS.get(skill_id, {}).get("weapon_req", "none")
    if weapon_req and weapon_req != "none" and not _check_weapon_req(character, weapon_req):
        return f"requires a {weapon_req} — none equipped"

    cap_cost = skill.get("skill_capacity_cost", 1)
    remaining = state.get("max_skill_capacity", 8) - state.get("skill_capacity_used", 0)
    if cap_cost > 0 and cap_cost > remaining:
        return f"not enough skill capacity ({cap_cost} needed, {max(0, remaining)} left)"

    trig = skill.get("trigger", "always")
    if trig == "low_hp" and hp_ratio > 0.5:
        return "only usable when wounded (below 50% HP)"
    if trig == "opponent_wounded" and enemy_hp_ratio > 0.6:
        return "only usable against a wounded enemy (below 60% HP)"
    if trig == "opening_move" and turn > 0:
        return "opening move only — the moment has passed"
    if trig == "opponent_status" and not state.get("monster_statuses"):
        return "requires the enemy to be suffering a status effect"
    if trig == "self_debuff" and not any(
        s.get("kind") == "debuff" for s in state.get("player_statuses", [])
    ):
        return "only usable while you are debuffed"
    return None


def _pick_next_skill(character: dict, state: dict, hp_ratio: float, enemy_hp_ratio: float, turn: int) -> str | None:
    """Pick the first usable skill from the character's skill bar, in slot order."""
    for ls in [s for s in character.get("skill_bar", []) if s]:
        sid = ls["skill_id"] if isinstance(ls, dict) else ls
        if skill_unusable_reason(sid, character, state, hp_ratio, enemy_hp_ratio, turn) is None:
            return sid
    return None
def _use_item(character: dict, state: dict, item_id: str, r_mods: dict, monster: dict, log: list[dict]) -> bool:
    """Use a single item, apply its effects, log it, decrement quantity. Returns True if used."""
    item = ITEMS_BY_ID.get(item_id, {})
    eff = item.get("effect", {})
    # Guard against the legacy string shape (`"effect": "heal"`). `"heal" in eff`
    # is a substring test on a string and passes, so the old code then did
    # eff["heal"] and raised TypeError — every crafted potion crashed on use.
    # Crafted consumables are normalised to the dict shape now; this keeps any
    # stragglers from taking the whole combat turn down with them.
    if not isinstance(eff, dict):
        return False
    used_msg = ""
    if "heal" in eff:
        heal = compute_healing(character, int(int(eff["heal"]) * r_mods["heal_mult"] * _continental_heal_mult(character)))
        # Blessed status: +10% healing received
        if _has_player_status(character, state, "blessed"):
            heal = int(heal * 1.10)
        # Item bonus: heal_amp
        heal = _apply_item_heal_amp(state, heal)
        character["hp"] = min(character["max_hp"], character["hp"] + heal)
        _clamp_and_sync_combat_hp(character, state, log)
        used_msg = f"{character['name']} uses {item['name']} and heals {heal} HP."
    elif "damage" in eff:
        dmg = int(eff["damage"])
        state["monster_hp"] = max(0, state["monster_hp"] - dmg)
        used_msg = f"{character['name']} hurls {item['name']} — the {monster['name']} takes {dmg} damage!"
    elif "cure" in eff:
        cured = eff["cure"]
        character["statuses"] = [s for s in character.get("statuses", []) if s.get("id") != cured]
        used_msg = f"{character['name']} uses {item['name']} and cures {cured}."
    # The effect kinds below exist on 54 crafted consumables (alchemy potions)
    # that the engine previously had no branch for at all — using one returned
    # False and silently did nothing.
    elif "restore_mp" in eff:
        amount = int(eff["restore_mp"])
        character["mp"] = min(character.get("max_mp", amount), character.get("mp", 0) + amount)
        used_msg = f"{character['name']} uses {item['name']} and restores {amount} MP."
    elif "stamina" in eff:
        amount = int(eff["stamina"])
        state["player_stamina"] = min(
            state.get("player_max_stamina", 100), state.get("player_stamina", 100) + amount
        )
        used_msg = f"{character['name']} uses {item['name']} and recovers {amount} stamina."
    elif "buff_stat" in eff:
        amount = int(eff["buff_stat"])
        stat = item.get("stat") or "might"
        status = make_status("inspired")
        status["modifiers"] = {stat: amount}
        _append_status_dedup(state, status, key="player_statuses")
        character["stats"][stat] = character["stats"].get(stat, 0) + amount
        used_msg = f"{character['name']} uses {item['name']} — {stat} +{amount}."
    elif "hp_regen" in eff:
        status = make_status("blessed")
        status["magnitude"] = int(eff["hp_regen"])
        _append_status_dedup(state, status, key="player_statuses")
        used_msg = f"{character['name']} uses {item['name']} — regenerating {eff['hp_regen']} HP per turn."
    elif "mp_regen" in eff:
        status = make_status("focused")
        status["magnitude"] = int(eff["mp_regen"])
        _append_status_dedup(state, status, key="player_statuses")
        used_msg = f"{character['name']} uses {item['name']} — regenerating {eff['mp_regen']} MP per turn."
    elif "resist" in eff:
        status = make_status("warded")
        status["magnitude"] = int(eff["resist"])
        _append_status_dedup(state, status, key="player_statuses")
        used_msg = f"{character['name']} uses {item['name']} — warded against harm."
    elif "xp_buff" in eff:
        # Out-of-combat economy buff; nothing to resolve mid-turn, but consume it
        # rather than silently rejecting the click.
        character["xp_buff_pct"] = int(eff["xp_buff"])
        used_msg = f"{character['name']} uses {item['name']} — +{eff['xp_buff']}% XP gain."
    elif "gold" in eff:
        amount = int(eff["gold"])
        character["gold"] = character.get("gold", 0) + amount
        used_msg = f"{character['name']} opens {item['name']} and finds {amount} gold."
    else:
        return False
    log.append({"kind": "item", "text": used_msg, "item_id": item_id})
    for inv in character.get("inventory", []):
        if inv.get("item_id") == item_id:
            inv["quantity"] = max(0, inv["quantity"] - 1)
            break
    character["inventory"] = [x for x in character.get("inventory", []) if x.get("quantity", 0) > 0]
    state["item_cooldowns"][item_id] = 1
    return True


def _use_pre_combat_items(character: dict, state: dict, r_mods: dict, monster: dict, log: list[dict]) -> None:
    """Use all usable items from item_bar in slot order before combat begins (turn 0 only)."""
    hp_ratio = character["hp"] / max(1, character["max_hp"])
    item_bar = [iid for iid in (character.get("item_bar") or []) if iid]
    for iid in item_bar:
        inv = next(
            (inv for inv in character.get("inventory", [])
             if (inv["item_id"] if isinstance(inv, dict) else inv[0]) == iid),
            None,
        )
        if not inv:
            continue
        qty = inv["quantity"] if isinstance(inv, dict) else inv[1]
        if qty <= 0:
            continue
        item = ITEMS_BY_ID.get(iid)
        if not item or item.get("kind") != "consumable":
            continue
        trig = item.get("trigger", "always")
        if trig == "hp_below_50" and hp_ratio > 0.5:
            continue
        if trig == "hp_below_40" and hp_ratio > 0.4:
            continue
        if trig == "status_poison" and not any(s.get("id") == "poisoned" for s in character.get("statuses", [])):
            continue
        if trig == "status_bleeding" and not any(s.get("id") == "bleeding" for s in character.get("statuses", [])):
            continue
        _use_item(character, state, iid, r_mods, monster, log)
        if state["monster_hp"] <= 0:
            return


def combat_turn(character: dict, state: dict, manual_skill_id: str | None = None, manual_item_id: str | None = None, action_type: str = "strike") -> dict:
    """Execute one round: player action, then enemy action.
    Uses new damage type system: physical (Might + Armor), magical (Insight + MR), true (ignores defenses).
    Uses Grace-based accuracy vs evasion for dice rolls.
    Tracks skill capacity per narrative (combat encounter).
    Innate actions: strike, defend, evade, aim, counter, focus.
    """
    if not state.get("active"):
        return {"error": "Combat is not active"}

    # Validate action_type
    if action_type not in INNATE_ACTIONS:
        action_type = "strike"

    _orig_stats = dict(character.get("stats", {}))
    # Strip out-of-combat Paladin faith bonuses so combat faith scaling starts clean
    if _is_paladin(character):
        _ooc_bonuses = character.get("paladin_faith_bonuses")
        if _ooc_bonuses:
            for stat, val in _ooc_bonuses.items():
                if val:
                    _orig_stats[stat] = _orig_stats.get(stat, 0) - val
            character["stats"] = dict(_orig_stats)
    monster = get_monster(state["monster_id"])
    state["monster_ref"] = monster
    turn = state["turn"]
    hp_ratio = character["hp"] / max(1, character["max_hp"])
    enemy_hp_ratio = state["monster_hp"] / max(1, state["monster_max_hp"])

    log: list[dict] = []

    # Extracted mastery hooks. Masteries still inline below are unaffected —
    # `hooks_for` only returns the ones that have been moved out, so extraction
    # proceeds one mastery at a time with the golden logs verifying each step.
    from mastery_hooks import TurnContext, hooks_for
    from mastery.mitigation import run_incoming_pipeline as _run_incoming_pipeline
    from mastery.skill_effects import apply_skill_effects as _apply_skill_effects
    from mastery.outgoing import apply_outgoing_riders as _apply_outgoing_riders
    _hooks = hooks_for(character)
    _ctx = TurnContext(
        character=character, state=state, monster=monster, log=log,
        action_type=action_type, turn=turn,
    )

    # racial combat mods for this turn
    r_mods = racial_combat_mods(character)
    for m in r_mods.get("log_msgs", []):
        log.append({"kind": "racial", "text": m})

    # Extracted masteries run through their hooks. See mastery_hooks.py.
    for _h in _hooks:
        _h.on_turn_start(_ctx)

    # Hunter: start-of-turn Range initialization + Spirit Touched
    if _is_hunter(character) and turn == 0:
        state["hunter_range"] = _hunter_get_starting_range(character)
        # Spirit Touched (level 30): +10 permanent grace
        if character.get("level", 1) >= 30:
            character["stats"]["grace"] = character["stats"].get("grace", 0) + 10
        # Spirit of the Wild (legendary quest): permanent spirit copy
        if character.get("level", 1) >= 100 and "spirit_of_the_wild" in (character.get("quest_passives") or []):
            state["hunter_spirit_copy_active"] = True

    # Unified range system: initialize for all classes at turn 0
    if turn == 0:
        if _is_hunter(character):
            state["player_range"] = state["hunter_range"]
        else:
            state["player_range"] = _get_weapon_range_for_combat(character)
        state["monster_range"] = _get_monster_range(monster)
        state["range_gap"] = state["player_range"] - state["monster_range"]

        # Gravity Well legendary power: +1 range, pin enemy at 0
        if "gravity_well" in state.get("legendary_powers", []):
            _gw = _LEGENDARY_POWERS.get("gravity_well", {})
            _gw_eff = _gw.get("effect", {})
            state["player_range"] += _gw_eff.get("value", 1)
            if _gw_eff.get("pin_enemy"):
                state["monster_range"] = 0
            state["range_gap"] = state["player_range"] - state["monster_range"]
            log.append({"kind": "legendary_power", "text": f"Gravity Well — +{_gw_eff.get('value', 1)} range, enemy pinned!"})

        if state["range_gap"] > 0:
            log.append({"kind": "range_gap", "text": f"Range advantage — {state['range_gap']} turns before enemy closes!"})
        elif state["range_gap"] < 0:
            log.append({"kind": "range_gap", "text": f"Enemy outranges you by {-state['range_gap']} — you must close the distance!"})

    # Rogue: start-of-turn innate skill initialization
    if _is_rogue(character) and turn == 0:
        _rogue_init_combat(state, character, log)
        if state.get("rogue_quick_hands"):
            log.append({"kind": "rogue_innate", "text": "Quick Hands — you act first every turn!"})

    # Bard: start-of-combat initialization
    if _is_bard(character) and turn == 0:
        _bard_init_combat(state, character, log)
        log.append({"kind": "bard_init", "text": "Bard — Song mode active. Crescendo begins!"})

    # Druid: start-of-combat initialization
    if _is_druid(character) and turn == 0:
        _druid_init_combat(state, character, log)

    # Mage: start-of-turn Arcane Focus gain (odd turns) + echo processing
    if _is_mage(character):
        # Process echo damage from Echo Chamber passive
        if turn > 0:
            echo_dmg = _mage_process_echo(state, log)
            if echo_dmg > 0:
                state["monster_hp"] = max(0, state.get("monster_hp", 0) - echo_dmg)
        # Gain Arcane Focus on odd turns
        _mage_gain_arcane_focus(state, character, log)
        # Check Rewind passive (auto-trigger below 25% HP)
        _mage_check_rewind(state, character, log)
        # Reset dual cast flag
        state["mage_dual_cast_used"] = False
        # Re-apply active self stat_mods from skills
        for entry in state.get("mage_self_stat_mods", []):
            for stat, val in entry.get("mods", {}).items():
                character["stats"][stat] = character["stats"].get(stat, 0) + val

    # Re-apply generic self stat_mods at the start of the turn.
    #
    # combat_turn resets character["stats"] to _orig_stats on the way out, so every
    # mastery's buffs live in `state` and are re-applied here each turn. The generic
    # path (Druid/Bard/Priest) needs the same treatment or its stat_mods vanish the
    # moment the turn ends.
    for entry in state.get("generic_self_stat_mods", []):
        for stat, val in entry.get("mods", {}).items():
            character["stats"][stat] = character["stats"].get(stat, 0) + val

    # Bard: performances tick at START of turn (always go first)
    if _is_bard(character) and turn > 0:
        _bard_tick_crescendo(state, character, log)

    # Alchemist: pre-combat imbue — auto-load first imbue skill from skill bar
    if _is_alchemist(character) and turn == 0 and not state.get("alchemist_imbue"):
        pre_imbue_id = state.get("alchemist_pre_imbue")
        if pre_imbue_id and pre_imbue_id in SKILLS_BY_ID:
            pre_sk = SKILLS_BY_ID[pre_imbue_id]
            if pre_sk.get("power_type") == "imbue":
                _alch_load_imbue(state, pre_sk, log, character)
        else:
            # Auto-load first imbue skill in skill bar
            for sid in (character.get("skill_bar") or []):
                if sid and sid in SKILLS_BY_ID:
                    sk_check = SKILLS_BY_ID[sid]
                    if sk_check.get("power_type") == "imbue":
                        _alch_load_imbue(state, sk_check, log, character)
                        break

    # -------- player turn --------
    skill_bar = set(s for s in (character.get("skill_bar") or []) if s)
    if manual_skill_id and manual_skill_id not in skill_bar:
        manual_skill_id = None
    item_bar = set(i for i in (character.get("item_bar") or []) if i)
    if manual_item_id and manual_item_id not in item_bar:
        manual_item_id = None

    # Pre-combat items: use all usable items in slot order on turn 0 (auto only)
    if turn == 0 and not manual_item_id:
        _use_pre_combat_items(character, state, r_mods, monster, log)
        # Check if monster died from pre-combat damage items
        if state["monster_hp"] <= 0:
            state["active"] = False
            state["skinnable"] = True
            drops, xp, gold = _roll_loot(monster, character, critical=False)
            _pcx = continental_bonus_for(character.get("current_continent", ""), "physical_combat_xp")
            if _pcx:
                xp = int(xp * float(_pcx))
            xp = int(xp * _sanctuary_blessing_xp_mult(character))
            victory_msgs = tick_racial_on_combat_win(character)
            for msg in victory_msgs:
                log.append({"kind": "racial", "text": msg})
            log.append({"kind": "victory",
                        "text": f"The {monster['name']} falls before {character['name']} can even strike!",
                        "drops": drops, "xp": xp, "gold": gold})
            _clamp_and_sync_combat_hp(character, state)
            state["turn"] = turn + 1
            state["log"].extend(log)
            character["stats"] = _orig_stats
            return {"state": state, "log": log, "victory": True, "rewards": {"xp": xp, "gold": gold, "items": drops}}

    # Manual item use on any turn
    if manual_item_id:
        _use_item(character, state, manual_item_id, r_mods, monster, log)

    # -------- innate action resolution --------
    # Non-attacking actions: defend, evade, counter, focus
    # These skip the player's attack but may apply buffs/defenses
    non_attack_actions = {"defend", "evade", "counter", "focus"}
    player_attacks = action_type not in non_attack_actions

    # Clear transient flags from previous turn (defending/evading are consumed in monster phase)
    state["defending"] = False
    state["evading"] = False

    if action_type == "defend":
        state["defending"] = True
        heal_amt = int(character["max_hp"] * 0.05)
        character["hp"] = min(character["max_hp"], character["hp"] + heal_amt)
        _clamp_and_sync_combat_hp(character, state, log)
        log.append({"kind": "innate_action", "text": f"{character['name']} braces for impact, restoring {heal_amt} HP. Incoming damage halved next turn."})
    elif action_type == "evade":
        evade_roll = random.randint(1, 6)
        if evade_roll >= 4:
            state["evading"] = True
            log.append({"kind": "innate_action", "text": f"{character['name']} reads the enemy's stance and prepares to dodge (rolled {evade_roll})."})
        else:
            log.append({"kind": "innate_action", "text": f"{character['name']} attempts to evade but stumbles (rolled {evade_roll}). No defense this turn!"})
    elif action_type == "counter":
        state["countering"] = True
        log.append({"kind": "innate_action", "text": f"{character['name']} drops into a counter stance, blade ready to punish the next attack."})
    elif action_type == "focus":
        restored = min(2, state.get("max_skill_capacity", 8) - state.get("skill_capacity_used", 0))
        state["skill_capacity_used"] = max(0, state.get("skill_capacity_used", 0) - restored)
        state["focused"] = True
        log.append({"kind": "innate_action", "text": f"{character['name']} focuses deeply, restoring {restored} skill capacity. Next skill gains +1 outcome."})

    # Skills can still be used alongside non-attack actions (heal/defend skills)
    # But strike/debuff skills are skipped if the innate action doesn't attack
    skill_id = manual_skill_id or _pick_next_skill(character, state, hp_ratio, enemy_hp_ratio, turn)

    # Manual picks go through the same gate as the auto-picker.
    #
    # Previously only cooldown and weapon_req were re-checked here, so a manually
    # selected skill bypassed **skill capacity and trigger conditions entirely**.
    # See skill_unusable_reason() for what that allowed.
    if skill_id and manual_skill_id:
        reason = skill_unusable_reason(skill_id, character, state,
                                      hp_ratio, enemy_hp_ratio, turn)
        if reason:
            name = SKILLS_BY_ID.get(skill_id, {}).get("name", skill_id)
            log.append({"kind": "skill_blocked",
                        "text": f"{name} — {reason}. Basic attack instead."})
            skill_id = None

    # If non-attacking action and auto-picked a strike skill, skip it
    if not player_attacks and skill_id and not manual_skill_id:
        sk_check = SKILLS_BY_ID.get(skill_id)
        if sk_check and sk_check.get("power_type") in ("strike", "debuff", "trap", "spirit"):
            skill_id = None

    # If non-attacking and manually picked a strike skill, still allow it (player override)
    # but the innate action's defense/buff still applies

    # Determine if this turn involves a player attack
    has_attack = player_attacks or (skill_id and SKILLS_BY_ID.get(skill_id, {}).get("power_type") in ("strike", "debuff", "trap", "spirit"))

    # Reverse range gap: monster outranges player — player can't hit yet
    player_out_of_range = has_attack and state.get("range_gap", 0) < 0

    if has_attack:
        # Determine damage type for this attack
        _sk_for_dtype = SKILLS_BY_ID.get(skill_id, {}) if skill_id else {}
        _attack_damage_type = _sk_for_dtype.get("damage_type", "physical")
        # Bard: Song of Heroes — physical attacks can't be evaded
        if _is_bard(character) and state.get("bard_unevadable") and _attack_damage_type == "physical":
            outcome = 4  # guaranteed hit
            dice = {"outcome": outcome, "advantage": "neutral"}
            log.append({"kind": "bard_unevadable", "text": "Song of Heroes — the attack cannot be evaded!"})
        else:
            # Accuracy vs Evasion dice roll (Grace-based)
            player_acc = compute_accuracy(character) + r_mods["strike_bonus"]
            # Item bonus: strike_accuracy
            _sa = state.get("item_bonus_effects", {}).get("strike_accuracy", 0)
            if _sa > 0:
                player_acc += _sa
            m_stats = state.get("monster_stats", {})
            monster_evas = m_stats.get("grace", state["monster_threat"])
            if state.get("monster_enraged"):
                monster_evas = int(monster_evas * 1.2)

            if action_type == "aim":
                # Roll 2d6, keep higher (advantage)
                dice1 = roll_accuracy_evasion(player_acc, monster_evas)
                dice2 = roll_accuracy_evasion(player_acc, monster_evas)
                dice = dice1 if dice1["outcome"] >= dice2["outcome"] else dice2
                log.append({"kind": "innate_action", "text": f"{character['name']} takes aim, rolling with advantage ({dice1['outcome']} vs {dice2['outcome']} → {dice['outcome']})."})
            else:
                dice = roll_accuracy_evasion(player_acc, monster_evas)

            outcome = dice["outcome"]

        # Item bonus: first_strike — chance to crit on first attack at turn 0
        if turn == 0 and outcome < 5:
            _fs = state.get("item_bonus_effects", {}).get("first_strike", 0)
            if _fs > 0 and random.random() < _fs:
                outcome = 5
                log.append({"kind": "item_first_strike", "text": "First Strike — opening attack is a critical hit!"})

        # Inspired buff: +1 to player's dice roll (max 6)
        if _has_player_status(character, state, "inspired"):
            outcome = min(6, outcome + 1)
            log.append({"kind": "inspired", "text": f"Inspired — outcome boosted to {outcome}!"})

        # Weary debuff: -1 to player's dice roll (min 1)
        if _has_player_status(character, state, "weary"):
            outcome = max(1, outcome - 1)
            log.append({"kind": "weary", "text": f"Weary — outcome reduced to {outcome}!"})

        # Extracted masteries may upgrade the roll (e.g. Lancer Critical Imbue).
        _ctx.outcome = outcome
        for _h in _hooks:
            _h.on_action_selected(_ctx)
        outcome = _ctx.outcome

        # Focus bonus: +1 outcome (max 6)
        if state.get("focused"):
            outcome = min(6, outcome + 1)
            state["focused"] = False
            log.append({"kind": "innate_action", "text": f"Focus pays off — outcome boosted to {outcome}!"})

        strike_narrative = pick_narrative(
            "combat_attack", outcome,
            char=character["name"], enemy=monster["name"],
        )
    else:
        outcome = 0
        dice = {"outcome": 0, "advantage": "neutral"}
        strike_narrative = ""

    # Determine weapon damage (use best weapon from either hand)
    weapon_dmg = 0
    equipped = character.get("equipped", {})
    seen_w = set()
    for hand in ("left_hand", "right_hand"):
        wid = equipped.get(hand)
        if not wid or wid in seen_w:
            continue
        seen_w.add(wid)
        w_item = _get_equipped_item(character, hand)
        if not w_item:
            w_item = ITEMS_BY_ID.get(wid)
        if w_item:
            weapon_dmg += _compute_weapon_damage(w_item)
    if weapon_dmg == 0:
        weapon_dmg = 4  # unarmed baseline

    skill_dmg = 0
    skill_status = None
    skill_used_msg = ""
    damage_type = "physical"  # default for basic attacks
    sk = None

    if skill_id and skill_id in SKILLS_BY_ID:
        sk = SKILLS_BY_ID[skill_id]
        damage_type = sk.get("damage_type", "physical")
        if sk.get("power_type") == "strike":
            skill_dmg = sk.get("damage", 0)
            skill_used_msg = f"{character['name']} unleashes {sk['name']}!"
        elif sk.get("power_type") == "heal":
            if not _is_priest(character):
                heal = compute_healing(character, int(sk.get("damage", 0) * r_mods["heal_mult"] * _continental_heal_mult(character)))
                # Blessed status: +10% healing received
                if _has_player_status(character, state, "blessed"):
                    heal = int(heal * 1.10)
                # Alchemist heal_percent bonus
                if sk.get("heal_percent"):
                    heal += int(character["max_hp"] * sk["heal_percent"])
                # Paladin heal amplification from inverse HP scaling
                if _is_paladin(character) and sk.get("inverse_hp_scaling"):
                    heal = _paladin_apply_heal_amp(state, heal)
                # Item bonus: heal_amp
                heal = _apply_item_heal_amp(state, heal)
                character["hp"] = min(character["max_hp"], character["hp"] + heal)
                _clamp_and_sync_combat_hp(character, state, log)
                skill_used_msg = f"{character['name']} casts {sk['name']} — restores {heal} HP."
        elif sk.get("power_type") == "defend":
            if not _is_priest(character):
                self_status = sk.get("self_status")
                if self_status:
                    _append_status_dedup(character, make_status(self_status))
            # Alchemist defend heal_percent
            if sk.get("heal_percent") and not _is_priest(character):
                heal = int(character["max_hp"] * sk["heal_percent"])
                # Paladin heal amp on defend skills with heal_percent
                if _is_paladin(character) and sk.get("inverse_hp_scaling"):
                    heal = _paladin_apply_heal_amp(state, heal)
                # Item bonus: heal_amp
                heal = _apply_item_heal_amp(state, heal)
                character["hp"] = min(character["max_hp"], character["hp"] + heal)
                _clamp_and_sync_combat_hp(character, state, log)
                skill_used_msg = f"{character['name']} casts {sk['name']} — restores {heal} HP and raises defense."
            else:
                skill_used_msg = f"{character['name']} raises {sk['name']}."
        elif sk.get("power_type") == "debuff":
            skill_dmg = sk.get("damage", 0)
            skill_used_msg = f"{character['name']} uses {sk['name']}."
        elif sk.get("power_type") == "trap":
            skill_dmg = sk.get("damage", 0)
            skill_used_msg = f"{character['name']} throws {sk['name']}!"
        elif sk.get("power_type") == "spirit":
            skill_dmg = sk.get("damage", 0)
            skill_used_msg = f"{character['name']} channels {sk['name']}!"
        elif sk.get("power_type") == "buff":
            if not _is_priest(character):
                self_status = sk.get("self_status")
                if self_status:
                    _append_status_dedup(character, make_status(self_status))
            skill_used_msg = f"{character['name']} casts {sk['name']}."
        elif sk.get("power_type") == "shield_wall":
            skill_used_msg = f"{character['name']} raises {sk['name']}."
        elif sk.get("power_type") == "imbue":
            # Alchemist imbue loading
            if _is_alchemist(character):
                if state.get("alchemist_katar_cracked", False):
                    log.append({"kind": "alchemist_imbue", "text": "The katar is cracked — cannot be imbued this turn!"})
                    skill_used_msg = f"The katar cracks — no imbue possible."
                else:
                    _alch_load_imbue(state, sk, log, character)
                    # Free re-imbue doesn't cost the turn
                    if state.get("alchemist_free_reimbue", False):
                        state["alchemist_free_reimbue"] = False
                        log.append({"kind": "alchemist_imbue", "text": "Free re-imbue — no turn lost!"})
                    skill_used_msg = f"{character['name']} loads {sk['name']} onto the katar."
            else:
                skill_used_msg = f"{character['name']} uses {sk['name']}."
        if sk.get("status_apply") and not (_is_priest(character) and sk.get("power_type") == "debuff"):
            skill_status = sk["status_apply"]

        # Alchemist: apply self stat_mods from cast skills
        if sk.get("stat_mod", {}).get("self") and _is_alchemist(character):
            apply_self_stat_mods(state, character, sk["stat_mod"]["self"],
                                 sk.get("mod_duration", 3), "alchemist_self_stat_mods",
                                 log, "alchemist_stat_mod", "Transmutation: ")

        # Alchemist: apply enemy stat_mods from cast skills (debuffs like Spike Field)
        if sk.get("stat_mod", {}).get("enemy") and _is_alchemist(character):
            apply_enemy_stat_mods(state, sk["stat_mod"]["enemy"],
                                  sk.get("mod_duration", 3), "alchemist_enemy_stat_mods")

        # Paladin: apply self stat_mods from buff/defend/heal skills
        if sk.get("stat_mod", {}).get("self") and _is_paladin(character):
            self_mods = dict(sk["stat_mod"]["self"])
            mod_dur = sk.get("mod_duration", 3)
            # Apply inverse HP scaling to stat_mods
            tier = state.get("paladin_hp_tier", 0)
            if tier > 0 and sk.get("inverse_hp_scaling"):
                scale = 1.0 + FAITH_MULTS[tier - 1]
                self_mods = {k: int(v * scale) if v > 0 else v for k, v in self_mods.items()}
            state.setdefault("paladin_self_stat_mods", []).append({"mods": self_mods, "duration": mod_dur})
            for stat, val in self_mods.items():
                character["stats"][stat] = character["stats"].get(stat, 0) + val
            log.append({"kind": "paladin_stat_mod", "text": f"Faith: {', '.join(f'{k} {v:+d}' for k,v in self_mods.items())} for {mod_dur} turns."})

        # Paladin: apply enemy stat_mods from strike/debuff skills
        if sk.get("stat_mod", {}).get("enemy") and _is_paladin(character):
            apply_enemy_stat_mods(state, sk["stat_mod"]["enemy"],
                                  sk.get("mod_duration", 3), "paladin_enemy_stat_mods")

        # Paladin: holy bonus on legendary strikes
        if sk.get("holy_bonus") and _is_paladin(character):
            state["paladin_holy_bonus_active"] = True

        # Knight: apply self stat_mods from buff/defend skills
        if sk.get("stat_mod", {}).get("self") and _is_knight(character):
            apply_self_stat_mods(state, character, sk["stat_mod"]["self"],
                                 sk.get("mod_duration", 3), "knight_self_stat_mods",
                                 log, "knight_stat_mod", "Oath: ")

        # Knight: apply enemy stat_mods from strike/debuff skills
        if sk.get("stat_mod", {}).get("enemy") and _is_knight(character):
            enemy_mods = sk["stat_mod"]["enemy"]
            mod_dur = sk.get("mod_duration", 3)
            state.setdefault("knight_enemy_stat_mods", []).append({"mods": enemy_mods, "duration": mod_dur})
            m_stats = state.get("monster_stats", {})
            for stat, val in enemy_mods.items():
                m_stats[stat] = m_stats.get(stat, 0) + val
            log.append({"kind": "knight_stat_mod", "text": f"Oath: {', '.join(f'{k} {v:+d}' for k,v in enemy_mods.items())} to enemy for {mod_dur} turns."})

        # Knight: Oath of Iron gains stack when using defend skill
        if sk.get("power_type") == "defend" and _is_knight(character):
            _knight_gain_stack(state, character, log, "hit_or_defend")

        # Knight: Oath of Vanguard gains stack when using opening_move skills
        if sk.get("trigger") == "opening_move" and _is_knight(character):
            _knight_gain_stack(state, character, log, "strike_first")

        # Extracted masteries apply their skill-effect riders here.
        _ctx.skill = sk
        for _h in _hooks:
            if hasattr(_h, "on_skill_used"):
                _h.on_skill_used(_ctx)

        # Assassin: apply self stat_mods from buff skills
        # Mastery skill-effect application (353 lines, 45 guards) moved verbatim to
        # mastery/skill_effects.py. Order is observable — several steps consume RNG
        # and read state an earlier step wrote — so the run was moved intact.
        _ctx.skill = sk
        _ctx.outcome = outcome
        _ctx.skill_used_msg = skill_used_msg
        _apply_skill_effects(_ctx)
        outcome = _ctx.outcome
        skill_used_msg = _ctx.skill_used_msg

        # Assassin: Avatar of Shadow (level 100) — stealth skill cooldowns reduced by 50%
        _cd = sk.get("cooldown", 2)
        if _is_assassin(character) and character.get("level", 1) >= 100 and sk.get("self_status") == "hidden":
            _cd = max(1, _cd // 2)
        # Item bonus: cooldown_reduce — reduce cooldown by percentage
        _cdr = state.get("item_bonus_effects", {}).get("cooldown_reduce", 0)
        if _cdr > 0 and _cd > 0:
            _cd = max(1, _cd - int(_cd * _cdr))
        state["skill_cooldowns"][skill_id] = _cd
        # Deduct skill capacity
        cap_cost = sk.get("skill_capacity_cost", 1)
        state["skill_capacity_used"] = state.get("skill_capacity_used", 0) + cap_cost

    # Calculate raw damage based on damage type
    if has_attack:
        if damage_type == "physical":
            raw_dmg = compute_physical_damage(character, weapon_dmg, skill_dmg)
        elif damage_type in ("magical", "holy"):
            raw_dmg = compute_magical_damage(character, weapon_dmg, skill_dmg)
        else:  # true damage
            raw_dmg = weapon_dmg + skill_dmg  # no stat scaling

        # damage multiplier based on dice outcome
        dmg_mult = {1: 0.0, 2: 0.35, 3: 0.6, 4: 0.9, 5: 1.15, 6: 1.6}[outcome]
        # Aim action: cap damage multiplier at 1.2 (no 1.6x crit)
        if action_type == "aim":
            dmg_mult = min(dmg_mult, 1.2)
        total_dmg = int(raw_dmg * dmg_mult)
        if outcome == 1:
            total_dmg = 0

        # Reverse range gap: player can't reach the monster
        if player_out_of_range and total_dmg > 0:
            total_dmg = 0
            log.append({"kind": "range_gap", "text": f"Out of range — the enemy is {-state['range_gap']} beyond your reach! Close the distance!"})

        # Combo multiplier (consecutive successful hits)
        combo = state.get("combo_count", 0)
        combo_m = _combo_mult(combo)
        if combo_m > 1.0:
            total_dmg = int(total_dmg * combo_m)

        # Update combo tracking
        if outcome >= 4:
            # Successful hit — build combo (unless same skill twice in a row)
            if skill_id and skill_id == state.get("combo_last_skill"):
                state["combo_count"] = 1  # reset for repeat skill
            else:
                state["combo_count"] = combo + 1
            state["combo_last_skill"] = skill_id
        elif outcome <= 2:
            # Miss — reset combo
            state["combo_count"] = 0
            state["combo_last_skill"] = None
        # outcome 3 = partial hit, preserves combo but doesn't build

        # Recovering debuff: -10% damage
        if any(s.get("id") == "recovering" for s in character.get("statuses", [])):
            total_dmg = int(total_dmg * 0.9)

        # Focused buff: +10% damage
        if _has_player_status(character, state, "focused"):
            total_dmg = int(total_dmg * 1.10)

        # Sick debuff: -10% damage
        if _has_player_status(character, state, "sick"):
            total_dmg = int(total_dmg * 0.9)

        # Hunter: Trap Master (level 40) — trap damage +50% (AoE bonus in 1v1)
        if _is_hunter(character) and sk and sk.get("power_type") == "trap" and character.get("level", 1) >= 40:
            total_dmg = int(total_dmg * 1.5)
            log.append({"kind": "hunter_trap_master", "text": "Trap Master — +50% trap damage (AoE)!"})

        # Critical success (outcome 6) — true damage normally can't crit
        if outcome == 6 and damage_type == "true":
            # Only crit if the skill explicitly allows it (future: skill.can_true_crit)
            total_dmg = int(raw_dmg * dmg_mult)  # no extra crit multiplier

        # Apply damage type affinity (weakness/resistance)
        affinities = state.get("monster_affinities", {})
        if damage_type in affinities.get("weak", []):
            total_dmg = int(total_dmg * 1.5)
        elif damage_type in affinities.get("resist", []):
            total_dmg = int(total_dmg * 0.5)

        # Continental bonus: Mushkara demon_damage_mult
        if _monster_category(monster) == "demon":
            demon_mult = continental_bonus_for(character.get("current_continent", ""), "demon_damage_mult")
            if demon_mult:
                total_dmg = int(total_dmg * float(demon_mult))

        # --- Alchemist strike mechanics ---
        alch_sk = SKILLS_BY_ID.get(skill_id) if skill_id else None
        is_alch_strike = (_is_alchemist(character) and alch_sk and
                          alch_sk.get("power_type") == "strike" and
                          alch_sk.get("type") == "strike")

        if is_alch_strike and outcome >= 3:
            state["alchemist_struck_this_turn"] = True
            # Apply analysis bonus (CF spend: Analysis)
            analysis_bonus = state.pop("alchemist_analysis_bonus", 1.0) if state.get("alchemist_analysis_bonus", 1.0) != 1.0 else 1.0
            if analysis_bonus != 1.0:
                total_dmg = int(total_dmg * analysis_bonus)
                log.append({"kind": "alchemist_cf_result", "text": f"Analysis pays off — +20% damage!"})

            # Apply perfect formula effects (CF spend: Perfect Formula choices)
            if state.pop("alchemist_perfect_breakdown", False):
                # Perfect Breakdown: true damage, ignore all armor
                total_dmg = int(total_dmg * 1.5)
                total_dmg = int(total_dmg * 1.5)  # bonus damage for ignoring armor
                log.append({"kind": "alchemist_cf_result", "text": "Perfect Breakdown — armor ignored, true damage!"})
            elif state.pop("alchemist_perfect_delivery", False):
                # Perfect Delivery: +2 extra hits (both carry imbue)
                extra_hits = 2
                log.append({"kind": "alchemist_cf_result", "text": f"Perfect Delivery — +{extra_hits} bonus hits!"})
                _alch_apply_imbue_rider(state, character, monster, log, hit_count=extra_hits)
                total_dmg = int(total_dmg * 1.3)  # bonus damage from extra hits

            # Apply strike rule (modifies damage, sets state flags)
            total_dmg = _alch_apply_strike_rule(state, character, monster, log, alch_sk, outcome, total_dmg)

            # Multi-hit processing (Flurry = 3 hits, Legend of Alchemy = 8 hits)
            num_hits = alch_sk.get("hits", 1)
            if num_hits > 1:
                # Recalculate: each hit deals a portion of total damage
                per_hit_dmg = max(1, total_dmg // num_hits)
                total_dmg = 0
                for h in range(num_hits):
                    hit_dmg = per_hit_dmg
                    # Small variance per hit
                    if h > 0:
                        hit_dmg = max(1, int(hit_dmg * (0.9 + random.random() * 0.2)))
                    total_dmg += hit_dmg
                    # Apply imbue rider for each hit
                    _alch_apply_imbue_rider(state, character, monster, log, hit_count=1)
                    if h < num_hits - 1:
                        log.append({"kind": "alchemist_multihit", "text": f"Hit {h+1}/{num_hits} — {hit_dmg} damage."})
                log.append({"kind": "alchemist_multihit", "text": f"Final hit {num_hits}/{num_hits} — {per_hit_dmg} damage. Total: {total_dmg}."})
            else:
                # Single hit — apply imbue rider once
                _alch_apply_imbue_rider(state, character, monster, log, hit_count=1)

            # Gain Combo Flow
            _alch_gain_cf(state, alch_sk, log, character)

            # Apply self_status and heal_percent on strike skills (e.g. Legend of Alchemy)
            if alch_sk.get("self_status"):
                _append_status_dedup(character, make_status(alch_sk["self_status"]))
                log.append({"kind": "alchemist_strike_buff", "text": f"{alch_sk['name']} grants {alch_sk['self_status']}!"})
            if alch_sk.get("heal_percent"):
                heal_amt = int(character["max_hp"] * alch_sk["heal_percent"])
                character["hp"] = min(character["max_hp"], character["hp"] + heal_amt)
                log.append({"kind": "alchemist_strike_heal", "text": f"{alch_sk['name']} heals {heal_amt} HP!"})

        elif _is_alchemist(character) and has_attack and outcome >= 3:
            # Basic attack (no skill) — still apply imbue rider if imbued
            _alch_apply_imbue_rider(state, character, monster, log, hit_count=1)

        # Paladin: holy bonus damage vs undead/devils
        if state.get("paladin_holy_bonus_active") and total_dmg > 0:
            total_dmg = _paladin_apply_holy_bonus(state, character, monster, total_dmg)
            if total_dmg > int(total_dmg / 1.5):
                log.append({"kind": "paladin_holy", "text": f"Holy power burns the unholy! +50% damage vs {monster['name']}!"})
            state["paladin_holy_bonus_active"] = False

        # Outgoing-damage riders (192 lines, 12 guards) moved verbatim to
        # mastery/outgoing.py. Order is observable, so the run was kept intact.
        _ctx.outgoing = total_dmg
        _ctx.outcome = outcome
        _ctx.skill = sk
        _apply_outgoing_riders(_ctx)
        total_dmg = _ctx.outgoing
        outcome = _ctx.outcome

        # Item bonus: skill_damage — boost damage when using a skill
        if total_dmg > 0 and sk:
            _sd = state.get("item_bonus_effects", {}).get("skill_damage", 0)
            if _sd > 0:
                bonus = int(total_dmg * _sd)
                total_dmg += bonus
                if bonus > 0:
                    log.append({"kind": "item_skill_damage", "text": f"Skill power — +{bonus} damage!"})

        # Item bonus effects — crit chance, lifesteal, extra damage, etc.
        if total_dmg > 0:
            total_dmg = _apply_item_bonus_effects_to_damage(state, character, log, total_dmg, outcome, damage_type)

        # Legendary powers — on_strike triggers (every Nth strike, chain, execute, etc.)
        if total_dmg > 0:
            total_dmg = _apply_legendary_powers_on_strike(state, character, log, total_dmg, outcome, damage_type)

        # Shield absorption — absorb damage before HP
        if state.get("monster_shield", 0) > 0:
            absorbed = min(state["monster_shield"], total_dmg)
            state["monster_shield"] -= absorbed
            total_dmg -= absorbed
            if absorbed > 0:
                log.append({"kind": "shield_absorb", "text": f"The {monster['name']}'s shield absorbs {absorbed} damage."})

        # Resolve damage modifier
        if total_dmg > 0:
            _rmod = _resolve_combat_damage_mod(character)
            if _rmod != 1.0:
                total_dmg = max(1, int(total_dmg * _rmod))

        state["monster_hp"] = max(0, state["monster_hp"] - total_dmg)

        if skill_status and outcome >= 4:
            # Apply status to monster with duration reduction based on monster "durability" (use power as proxy)
            _status = make_status(skill_status)
            # Rogue: Con Artist — extend debuff duration
            if _is_rogue(character) and _status.get("kind") == "debuff":
                bonus = _rogue_get_con_artist_bonus(state)
                if bonus > 0:
                    _status = dict(_status)
                    _status["duration"] = _status.get("duration", 2) + bonus
            # Item bonus: status_duration — extend debuff duration on enemies
            if _status.get("kind") == "debuff":
                _sdr = state.get("item_bonus_effects", {}).get("status_duration", 0)
                if _sdr > 0:
                    _status = dict(_status)
                    _extra = int(_status.get("duration", 2) * _sdr)
                    _status["duration"] = _status.get("duration", 2) + _extra
            _append_status_dedup(state, _status, key="monster_statuses")

        # Wildblood venomous aspect passive
        if "apply_poison" in r_mods.get("extra_effects", []) and outcome >= 3:
            _append_status_dedup(state, make_status("poisoned"), key="monster_statuses")

        # Item bonus: rune-based status application on hit
        if total_dmg > 0 and outcome >= 3:
            _ibe = state.get("item_bonus_effects", {})
            _rune_status_map = {
                "apply_bleed": "bleeding",
                "apply_poison": "poisoned",
                "apply_burn": "burning",
                "apply_stun": "stunned",
                "apply_chill": "chilled",
                "apply_fear": "shaken",
            }
            for _eff_key, _status_name in _rune_status_map.items():
                _chance = _ibe.get(_eff_key, 0)
                if _chance > 0 and random.random() < _chance:
                    _append_status_dedup(state, make_status(_status_name), key="monster_statuses")
                    log.append({"kind": "item_rune_status", "text": f"Rune effect — inflicted {_status_name}!"})

        log.append({
            "kind": "player_strike",
            "text": strike_narrative,
            "outcome": outcome,
            "damage": total_dmg,
            "damage_type": damage_type,
            "skill_id": skill_id,
            "skill_text": skill_used_msg,
            "advantage": dice.get("advantage", "neutral"),
        })

        # check monster death
        if state["monster_hp"] <= 0:
            state["active"] = False
            state["skinnable"] = True
            # Assassin: reclaim shadows on kill
            if _is_assassin(character):
                _assassin_reclaim_shadows(state, character, log)
            drops, xp, gold = _roll_loot(monster, character, critical=(outcome == 6))
            # Continental bonus: Mushkara physical_combat_xp
            _pcx = continental_bonus_for(character.get("current_continent", ""), "physical_combat_xp")
            if _pcx:
                xp = int(xp * float(_pcx))
            xp = int(xp * _sanctuary_blessing_xp_mult(character))
            # racial post-victory
            victory_msgs = tick_racial_on_combat_win(character)
            for msg in victory_msgs:
                log.append({"kind": "racial", "text": msg})
            log.append({"kind": "victory",
                        "text": f"The {monster['name']} falls at {character['name']}'s hand.",
                        "drops": drops, "xp": xp, "gold": gold})
            _clamp_and_sync_combat_hp(character, state)
            state["turn"] = turn + 1
            state["log"].extend(log)
            character["stats"] = _orig_stats
            return {"state": state, "log": log, "victory": True, "rewards": {"xp": xp, "gold": gold, "items": drops}}

        # -------- DoT tick on monster --------
        _tick_dots(state, "monster_statuses", None, log, f"The {monster['name']}", hp_key="monster_hp")

        # check monster death from DoT
        if state["monster_hp"] <= 0:
            state["active"] = False
            state["skinnable"] = True
            drops, xp, gold = _roll_loot(monster, character, critical=False)
            _pcx = continental_bonus_for(character.get("current_continent", ""), "physical_combat_xp")
            if _pcx:
                xp = int(xp * float(_pcx))
            xp = int(xp * _sanctuary_blessing_xp_mult(character))
            victory_msgs = tick_racial_on_combat_win(character)
            for msg in victory_msgs:
                log.append({"kind": "racial", "text": msg})
            log.append({"kind": "victory",
                        "text": f"The {monster['name']} succumbs to its wounds.",
                        "drops": drops, "xp": xp, "gold": gold})
            _clamp_and_sync_combat_hp(character, state)
            state["turn"] = turn + 1
            state["log"].extend(log)
            character["stats"] = _orig_stats
            return {"state": state, "log": log, "victory": True, "rewards": {"xp": xp, "gold": gold, "items": drops}}
    else:
        total_dmg = 0

    # -------- druid summon phase (before monster turn) --------
    if _is_druid(character) and state.get("active"):
        # Apply boss aura and legendary passive effects each turn
        _druid_apply_boss_aura(state, character, log)
        _druid_apply_legendary_passive(state, character, log)
        # Process summon actions
        _druid_tick_summons(state, character, log)
        # Check if monster died from summon attacks
        if state["monster_hp"] <= 0:
            state["active"] = False
            state["skinnable"] = True
            drops, xp, gold = _roll_loot(monster, character, critical=False)
            _pcx = continental_bonus_for(character.get("current_continent", ""), "physical_combat_xp")
            if _pcx:
                xp = int(xp * float(_pcx))
            log.append({"kind": "victory", "text": f"You are victorious! The {monster['name']} is defeated!"})
            state["turn"] = turn + 1
            state["log"].extend(log)
            return {"state": state, "log": log, "victory": True, "rewards": {"xp": xp, "gold": gold, "items": drops}}

    # -------- monster turn --------
    # Check monster statuses for bind/stun/blind/ensnared (Priest + Rogue + general)
    # Extracted masteries get a shot at the enemy's turn before it resolves —
    # control effects, turn theft. A hook may set ctx.enemy_turn_consumed.
    _ctx.enemy_turn_consumed = False
    for _h in _hooks:
        _h.on_enemy_turn_start(_ctx)

    _monster_bound = any(s.get("id") == "bind" for s in state.get("monster_statuses", []))
    _monster_stunned_status = any(s.get("id") == "stunned" for s in state.get("monster_statuses", []))
    _monster_blind = any(s.get("id") in ("blind", "blinded") for s in state.get("monster_statuses", []))
    _monster_ensnared = any(s.get("id") == "ensnared" for s in state.get("monster_statuses", []))

    # Mage: Mind Control / Time Loop can consume the enemy's turn outright.
    _mage_steals_turn = _mage_check_enemy_turn_skip(state, character, log)
    # Mage: Delirium redirects the enemy's attack onto itself.
    _mage_enemy_self_attack = _mage_check_enemy_self_attack(state, character, log)
    # Mage: Hallucination decoys can eat the incoming attack entirely.
    _mage_decoy_chance = _mage_get_decoy_miss_chance(state, character)
    if _mage_decoy_chance > 0 and random.random() < _mage_decoy_chance:
        log.append({"kind": "mage_passive",
                    "text": "HALLUCINATION — the attack tears through a decoy and finds nothing!"})
        _mage_steals_turn = True

    # Alchemist: enemy launched (Rising Strike) — skip monster turn entirely
    if state.get("alchemist_enemy_launched") or _mage_steals_turn:
        if not _mage_steals_turn:
            log.append({"kind": "alchemist_control", "text": f"The {monster['name']} is airborne — can't act this turn!"})
        c_base = 0
        c_out = 0
        m_skill = None
        skill_name = ""
        m_skill_status = None
        monster_dmg_type = "physical"
        counter_dice = {"outcome": 0, "advantage": "neutral"}
    elif _monster_bound or _monster_stunned_status or _monster_ensnared:
        # Bound, Stunned, or Ensnared: monster skips turn entirely
        if _monster_bound:
            log.append({"kind": "priest_bind", "text": f"The {monster['name']} is bound by holy chains and cannot act!"})
        elif _monster_ensnared:
            log.append({"kind": "ensnared", "text": f"The {monster['name']} is ensnared and cannot move!"})
        else:
            log.append({"kind": "stun", "text": f"The {monster['name']} is stunned and cannot act!"})
        c_base = 0
        c_out = 0
        m_skill = None
        skill_name = ""
        m_skill_status = None
        monster_dmg_type = "physical"
        counter_dice = {"outcome": 0, "advantage": "neutral"}
    else:
        # Alchemist: enemy immobilized (Living Slime) — 50% reduced damage
        _alch_immobilized = state.get("alchemist_enemy_immobilized", 0) > 0
        if _alch_immobilized:
            log.append({"kind": "alchemist_control", "text": f"The {monster['name']} is immobilized by slime — reduced action!"})
        # Boss enrage at <30% HP
        if state.get("monster_is_boss") and not state.get("monster_enraged", False):
            if state["monster_hp"] / max(1, state["monster_max_hp"]) < 0.3:
                state["monster_enraged"] = True
                log.append({"kind": "enrage", "text": f"The {monster['name']} enrages! Its eyes blaze with fury."})

        # Monster accuracy: use grace stat if available, else power
        m_stats = state.get("monster_stats", {})
        monster_acc = m_stats.get("grace", state["monster_threat"])
        if state.get("monster_enraged"):
            monster_acc = int(monster_acc * 1.3)
        player_evas = compute_evasion(character)
        # Continental bonus: Daw'ul Talalu stealth_evasion_chance
        stealth_bonus = continental_bonus_for(character.get("current_continent", ""), "stealth_evasion_chance")
        if stealth_bonus:
            player_evas = int(player_evas * (1.0 + float(stealth_bonus)))
        counter_dice = roll_accuracy_evasion(monster_acc, player_evas)
        c_out = counter_dice["outcome"]

        # Priest: blind status — monster can act but attacks miss
        if _monster_blind:
            c_out = 1
            log.append({"kind": "priest_blind", "text": f"The {monster['name']} swings blindly — the attack misses!"})

        # Knight: Bulwark 10-stack — enemy accuracy -20%
        if _is_knight(character):
            knight_ms = _knight_check_milestones(state, character, monster, log)
            if knight_ms.get("enemy_acc_minus_20pct"):
                # Reduce outcome by ~1 step (20% accuracy penalty)
                c_out = max(1, c_out - 1)
                log.append({"kind": "knight_oath", "text": "Oath of Bulwark — the enemy can barely swing!"})

        # Shaken status: -1 to monster's dice roll
        _monster_shaken = any(s.get("id") == "shaken" for s in state.get("monster_statuses", []))
        if _monster_shaken and c_out > 1:
            c_out = max(1, c_out - 1)
            log.append({"kind": "shaken", "text": f"The {monster['name']} is shaken — its attack falters!"})

        # Bard: Song of Fortune — reroll enemy's worst die
        if _is_bard(character) and state.get("bard_reroll") and c_out <= 2:
            old_out = c_out
            counter_dice = roll_accuracy_evasion(monster_acc, player_evas)
            c_out = counter_dice["outcome"]
            log.append({"kind": "bard_reroll", "text": f"Song of Fortune — enemy die rerolled from {old_out} to {c_out}!"})

        # Check monster statuses for silence/mesmerized
        _monster_silenced = any(s.get("id") == "silenced" for s in state.get("monster_statuses", []))
        _monster_mesmerized = any(s.get("id") == "mesmerized" for s in state.get("monster_statuses", []))

        # Bard: mesmerized — monster skips its turn
        if _monster_mesmerized:
            log.append({"kind": "bard_mesmerized", "text": f"The {monster['name']} is mesmerized and cannot act!"})
            m_skill = None
        elif state.get("bard_pull_mesmerize"):
            log.append({"kind": "bard_pull", "text": f"The dance pulls the {monster['name']} toward the Bard!"})
        else:
            # Pick monster skill
            m_hp_ratio = state["monster_hp"] / max(1, state["monster_max_hp"])
            m_skill = _pick_monster_skill(monster, state, m_hp_ratio, hp_ratio, turn)

        # Bard: silenced — monster can't use skills, basic attack only
        if _monster_silenced and m_skill:
            log.append({"kind": "bard_silenced", "text": f"The {monster['name']} is silenced — skill blocked!"})
            m_skill = None

        # Alchemist: interrupt (Counter Strike) — cancel monster's skill
        if state.get("alchemist_interrupt", False) and m_skill:
            log.append({"kind": "alchemist_control", "text": f"Counter Strike interrupts — the {monster['name']}'s skill is cancelled!"})
            m_skill = None

        monster_dmg_type = "physical"
        c_base = 0 if _monster_mesmerized else (3 + (state["monster_threat"] // 2))
        # Alchemist: enemy immobilized — 50% damage reduction
        if _alch_immobilized:
            c_base = c_base // 2
        skill_name = ""
        m_skill_status = None

        if m_skill:
            monster_dmg_type = m_skill.get("damage_type", "physical")
            ptype = m_skill.get("power_type", "strike")
            if ptype == "strike":
                # Scale skill power by monster stat (might for physical, insight for magical)
                if monster_dmg_type == "physical":
                    c_base = m_skill["damage"] + int(m_stats.get("might", 0) * 0.5)
                elif monster_dmg_type == "magical":
                    c_base = m_skill["damage"] + int(m_stats.get("insight", 0) * 0.5)
                else:
                    c_base = m_skill["damage"]
                skill_name = m_skill["name"]
                m_skill_status = m_skill.get("status_apply")
            elif ptype == "heal":
                heal_amt = m_skill.get("damage", 10)
                # Priest: Avatar of Faith (L100) — enemy cannot heal above current HP
                if _is_priest(character) and _priest_check_enemy_heal_lock(state, character):
                    heal_amt = 0
                    log.append({"kind": "priest_heal_lock", "text": f"Avatar of Faith — the {monster['name']}'s healing is nullified!"})
                # Druid: boss aura heal reduction
                if _is_druid(character) and state.get("druid_aura_heal_reduction", 0) > 0:
                    heal_amt = int(heal_amt * (1.0 - state["druid_aura_heal_reduction"]))
                    log.append({"kind": "druid_aura", "text": f"Aura reduces enemy healing by {int(state['druid_aura_heal_reduction'] * 100)}%!"})
                state["monster_hp"] = min(state["monster_max_hp"], state["monster_hp"] + heal_amt)
                if heal_amt > 0:
                    log.append({"kind": "enemy_skill", "text": f"The {monster['name']} uses {m_skill['name']} and heals {heal_amt} HP!"})
                # Set cooldown and consume resources
                state.setdefault("monster_skill_cooldowns", {})[m_skill["id"]] = m_skill.get("cooldown", 2)
                state["monster_mp"] = max(0, state.get("monster_mp", 0) - m_skill.get("cost_mp", 0))
                state["monster_stamina"] = max(0, state.get("monster_stamina", 100) - m_skill.get("cost_stamina", 0))
                # Skip damage phase for heal/buff skills
                c_base = 0
            elif ptype == "buff":
                buff_status = m_skill.get("status_apply", "warded")
                # Alchemist: ward_block prevents monster from gaining warded
                if buff_status == "warded" and state.get("alchemist_ward_block", 0) > 0:
                    log.append({"kind": "alchemist_control", "text": f"Guard Break — the {monster['name']} can't ward!"})
                # Mage: Paranoia (Mental) — a shaken target trusts nothing and
                # cannot benefit from buffs. Set by _mage_apply_arcane_library_control.
                elif state.get("mage_paranoia_active") and any(
                        s.get("id") == "shaken" for s in state.get("monster_statuses", [])):
                    log.append({"kind": "mage_passive",
                                "text": f"PARANOIA — the {monster['name']} refuses its own aid!"})
                # Knight: Bulwark 5-stack — enemy can't gain buffs
                elif _is_knight(character):
                    knight_ms = _knight_check_milestones(state, character, monster, log)
                    if knight_ms.get("enemy_no_buffs"):
                        log.append({"kind": "knight_oath", "text": f"Oath of Bulwark — the {monster['name']} can't buff! Crushed spirit!"})
                    else:
                        _append_status_dedup(state, make_status(buff_status), key="monster_statuses")
                        log.append({"kind": "enemy_skill", "text": f"The {monster['name']} uses {m_skill['name']}!"})
                else:
                    _append_status_dedup(state, make_status(buff_status), key="monster_statuses")
                    log.append({"kind": "enemy_skill", "text": f"The {monster['name']} uses {m_skill['name']}!"})
                state.setdefault("monster_skill_cooldowns", {})[m_skill["id"]] = m_skill.get("cooldown", 2)
                state["monster_mp"] = max(0, state.get("monster_mp", 0) - m_skill.get("cost_mp", 0))
                state["monster_stamina"] = max(0, state.get("monster_stamina", 100) - m_skill.get("cost_stamina", 0))
                c_base = 0
            elif ptype == "debuff":
                c_base = m_skill.get("damage", 3)
                skill_name = m_skill["name"]
                m_skill_status = m_skill.get("status_apply")
            # Set cooldown and consume resources for strike/debuff
            if ptype in ("strike", "debuff"):
                state.setdefault("monster_skill_cooldowns", {})[m_skill["id"]] = m_skill.get("cooldown", 2)
                state["monster_mp"] = max(0, state.get("monster_mp", 0) - m_skill.get("cost_mp", 0))
                state["monster_stamina"] = max(0, state.get("monster_stamina", 100) - m_skill.get("cost_stamina", 0))

        # Alchemist: immobilized reduces damage by half
        if _alch_immobilized:
            c_base = c_base // 2

    # c_out is 0 when the monster never acted — airborne (Alchemist Rising
    # Strike), bound (Priest), stunned, or ensnared (Lancer imbues, Mage). The
    # d6 table has no 0 key, so a bare lookup raised KeyError and crashed the
    # whole fight the moment any mastery landed its control effect. 0 damage
    # multiplier is the correct answer for "no attack happened".
    c_mult = {0: 0.0, 1: 0.0, 2: 0.4, 3: 0.7, 4: 1.0, 5: 1.2, 6: 1.6}.get(c_out, 0.0)

    # Rogue: Counter Strike innate — triggers on low enemy roll
    if _is_rogue(character) and c_out > 0:
        _rogue_check_counter_strike(state, character, log, c_out)

    # Enrage damage boost
    if state.get("monster_enraged"):
        c_mult *= 1.5

    # warded status reduces damage
    warded = _has_player_status(character, state, "warded")
    if warded:
        c_mult *= 0.5

    raw_c_dmg = int(c_base * c_mult * r_mods["damage_taken_mult"])

    # Apply defenses based on damage type
    if monster_dmg_type == "physical":
        # Monster armor stat reduces player's physical damage? No — this is monster attacking player.
        # Player's armor reduces incoming physical damage.
        c_dmg = apply_armor(raw_c_dmg, compute_armor(character))
    elif monster_dmg_type == "magical":
        c_dmg = apply_magic_resistance(raw_c_dmg, compute_magic_resistance(character))
        # Item bonus: magic_resist_pct
        c_dmg = _apply_item_magic_resist_pct(state, c_dmg)
    else:  # true damage
        c_dmg = raw_c_dmg

    # Mage: Delirium — the addled enemy lands its blow on itself instead.
    if _mage_enemy_self_attack and c_dmg > 0:
        state["monster_hp"] = max(0, state.get("monster_hp", 0) - c_dmg)
        log.append({"kind": "mage_passive",
                    "text": f"The {monster['name']} rakes itself for {c_dmg} damage!"})
        c_dmg = 0

    # -------- Innate action defenses --------
    monster_attacked = c_base > 0  # monster used a strike/debuff (not heal/buff)

    # Defending: halve incoming damage
    if state.get("defending"):
        c_dmg = int(c_dmg * 0.5)
        log.append({"kind": "innate_action", "text": f"Your defensive stance absorbs half the blow! Damage reduced to {c_dmg}."})
        state["defending"] = False

    # Evading: nullify monster's attack entirely
    if state.get("evading") and monster_attacked:
        c_dmg = 0
        log.append({"kind": "innate_action", "text": f"You sidestep the {monster['name']}'s attack — no damage!"})
        state["evading"] = False

    # Incoming-damage pipeline. This was 22 interleaved mastery guards mutating
    # c_dmg in sequence, with two universal steps (range gap, confused self-hit)
    # sitting between masteries. Order is observable — several steps consume RNG —
    # so it is declared as data in mastery/mitigation.py rather than as a loop.
    _ctx.incoming = c_dmg
    _ctx.enemy_outcome = c_out
    state["_monster_attacked"] = monster_attacked
    _run_incoming_pipeline(_ctx)
    c_dmg = int(_ctx.incoming)

    character["hp"] = max(0, character["hp"] - c_dmg)
    _clamp_and_sync_combat_hp(character, state, log)

    # Item bonus: thorns — reflect damage back to monster
    _thorns = state.get("item_bonus_effects", {}).get("thorns", 0)
    if _thorns > 0 and c_dmg > 0:
        reflect = max(1, int(c_dmg * _thorns))
        state["monster_hp"] = max(0, state["monster_hp"] - reflect)
        log.append({"kind": "item_thorns", "text": f"Thorns — reflected {reflect} damage!"})

    # Item bonus: counter_chance — chance to auto-counter when hit
    _cc = state.get("item_bonus_effects", {}).get("counter_chance", 0)
    if _cc > 0 and c_dmg > 0 and character["hp"] > 0:
        if random.random() < _cc:
            _counter_w = 0
            for hand in ("left_hand", "right_hand"):
                wid = equipped.get(hand)
                if not wid or wid in seen_w:
                    continue
                w_item = _get_equipped_item(character, hand)
                if not w_item:
                    w_item = ITEMS_BY_ID.get(wid)
                if w_item:
                    _counter_w += _compute_weapon_damage(w_item)
            if _counter_w == 0:
                _counter_w = 4
            _counter_dmg = int(compute_physical_damage(character, _counter_w, 0) * 0.7)
            if _counter_dmg > 0:
                state["monster_hp"] = max(0, state["monster_hp"] - _counter_dmg)
                log.append({"kind": "item_counter", "text": f"Counter-chance — retaliated for {_counter_dmg} damage!"})

    strike_desc = f"The {monster['name']} strikes back — {c_dmg} {monster_dmg_type} damage."
    if skill_name:
        strike_desc = f"The {monster['name']} uses {skill_name} — {c_dmg} {monster_dmg_type} damage!"
    log.append({
        "kind": "enemy_strike",
        "text": strike_desc,
        "damage": c_dmg,
        "damage_type": monster_dmg_type,
        "skill_name": skill_name,
    })

    # Counter-strike: if player was countering and monster attacked, auto counter
    if state.get("countering") and monster_attacked and character["hp"] > 0:
        state["countering"] = False
        # Auto counter-strike at outcome 4 (~0.9x damage)
        counter_weapon = 0
        for hand in ("left_hand", "right_hand"):
            wid = equipped.get(hand)
            if not wid or wid in seen_w:
                continue
            w_item = _get_equipped_item(character, hand)
            if not w_item:
                w_item = ITEMS_BY_ID.get(wid)
            if w_item:
                counter_weapon += _compute_weapon_damage(w_item)
        if counter_weapon == 0:
            counter_weapon = 4
        counter_raw = compute_physical_damage(character, counter_weapon, 0)
        counter_dmg = int(counter_raw * 0.9)
        if counter_dmg > 0:
            state["monster_hp"] = max(0, state["monster_hp"] - counter_dmg)
            log.append({"kind": "innate_action", "text": f"Counter-strike! {character['name']} retaliates for {counter_dmg} damage!"})

            # Check monster death from counter
            if state["monster_hp"] <= 0:
                state["active"] = False
                state["skinnable"] = True
                drops, xp, gold = _roll_loot(monster, character, critical=False)
                _pcx = continental_bonus_for(character.get("current_continent", ""), "physical_combat_xp")
                if _pcx:
                    xp = int(xp * float(_pcx))
                xp = int(xp * _sanctuary_blessing_xp_mult(character))
                victory_msgs = tick_racial_on_combat_win(character)
                for msg in victory_msgs:
                    log.append({"kind": "racial", "text": msg})
                log.append({"kind": "victory",
                            "text": f"The {monster['name']} falls to {character['name']}'s counter-strike!",
                            "drops": drops, "xp": xp, "gold": gold})
                _clamp_and_sync_combat_hp(character, state)
                state["turn"] = turn + 1
                state["log"].extend(log)
                character["stats"] = _orig_stats
                return {"state": state, "log": log, "victory": True, "rewards": {"xp": xp, "gold": gold, "items": drops}}
    elif state.get("countering"):
        # Counter wasted — monster didn't attack
        state["countering"] = False
        log.append({"kind": "innate_action", "text": f"Your counter stance finds no opening — the {monster['name']} didn't attack."})

    # Apply monster skill status to player
    if m_skill_status and c_out >= 3:
        # Rogue: Light Feet — immune to ensnared
        if m_skill_status == "ensnared" and state.get("rogue_light_feet"):
            log.append({"kind": "rogue_light_feet", "text": "Light Feet — immune to Ensnared!"})
        # Bard: CC immunity from Song of Freedom
        elif _is_bard(character) and _bard_check_cc_immune(state, m_skill_status, log):
            pass  # blocked by Bard CC immunity
        else:
            # Item bonus: status_resist — chance to resist any debuff
            _sr = state.get("item_bonus_effects", {}).get("status_resist", 0)
            # Item bonus: specific status resist (status_resist_stun, etc.)
            _specific_key = f"status_resist_{m_skill_status}"
            _sr_specific = state.get("item_bonus_effects", {}).get(_specific_key, 0)
            _total_sr = _sr + _sr_specific
            if _total_sr > 0 and random.random() < _total_sr:
                log.append({"kind": "item_status_resist", "text": f"Status resistance — resisted {m_skill_status}!"})
            else:
                _append_status_dedup(character, make_status(m_skill_status))

    # -------- DoT tick on player --------
    _tick_dots(character, "statuses", character, log, character["name"])

    # Tick state player_statuses (non-DoT durations)
    for s in state.get("player_statuses", []):
        s["duration"] = max(0, int(s.get("duration", 0)) - 1)
    state["player_statuses"] = [s for s in state.get("player_statuses", []) if s.get("duration", 0) > 0]

    # Extracted masteries tick their own state.
    for _h in _hooks:
        _h.on_turn_end(_ctx)

    # Tick the generic self stat_mods (masteries with no bespoke branch — Druid,
    # Bard, Priest). Mirrors the per-mastery tick blocks below.
    _generic_mods = state.get("generic_self_stat_mods", [])
    if _generic_mods:
        _still_active = []
        for entry in _generic_mods:
            if entry["duration"] > 0:
                _still_active.append(entry)
            else:
                for stat, val in entry["mods"].items():
                    character["stats"][stat] = character["stats"].get(stat, 0) - val
                if entry.get("form"):
                    state.pop("druid_active_form", None)
                    log.append({"kind": "druid_form", "text": "The borrowed shape fades."})
        state["generic_self_stat_mods"] = _still_active
        for entry in state["generic_self_stat_mods"]:
            entry["duration"] -= 1

    # Unified range system: range_gap moves toward 0 by 1 each turn
    # Positive gap: enemy closes distance. Negative gap: player closes distance.
    # Hunter infinite range (World Hunt communion) prevents gap decrease.
    # Gravity Well pin_enemy: enemy can't close distance.
    _gw_pin = "gravity_well" in state.get("legendary_powers", []) and \
              _LEGENDARY_POWERS.get("gravity_well", {}).get("effect", {}).get("pin_enemy", False)
    if state.get("range_gap", 0) > 0 and not state.get("hunter_infinite_range") and not _gw_pin:
        state["range_gap"] -= 1
        # Sync hunter_range for backward compat
        if _is_hunter(character):
            state["hunter_range"] = state["range_gap"]
        if state["range_gap"] <= 0:
            log.append({"kind": "range_gap", "text": "Range closed — enemy is in melee distance!"})
        else:
            log.append({"kind": "range_gap", "text": f"Range: {state['range_gap']} — enemy closes distance."})
    elif state.get("range_gap", 0) < 0:
        state["range_gap"] += 1
        if state["range_gap"] >= 0:
            log.append({"kind": "range_gap", "text": "Distance closed — you can reach the enemy!"})
        else:
            log.append({"kind": "range_gap", "text": f"Range: {-state['range_gap']} — you close the distance."})

    # Rogue: tick state at end of turn
    if _is_rogue(character):
        _rogue_tick_end_of_turn(state, character, log)

    # Bard: reset death save used flag for next turn (tick now runs at start of turn)
    if _is_bard(character):
        state["bard_death_save_used"] = False

    # Druid: tick enemy stat mods from summon skills
    if _is_druid(character):
        tick_stat_mods(state, "druid_summon_enemy_stat_mods", state.setdefault("monster_stats", {}))

    # Priest: tick state at end of turn
    if _is_priest(character):
        _priest_tick_end_of_turn(state, character, log)
        # Apply/remove self stat_mods that expired
        tick_stat_mods(state, "priest_self_stat_mods", character["stats"])
        # Apply/remove enemy stat_mods that expired
        tick_stat_mods(state, "priest_enemy_stat_mods", state.setdefault("monster_stats", {}))

    # tick cooldowns (player + monster)
    for sid in list(state["skill_cooldowns"].keys()):
        state["skill_cooldowns"][sid] = max(0, state["skill_cooldowns"][sid] - 1)
    for iid in list(state["item_cooldowns"].keys()):
        state["item_cooldowns"][iid] = max(0, state["item_cooldowns"][iid] - 1)
    for sid in list(state.get("monster_skill_cooldowns", {}).keys()):
        state["monster_skill_cooldowns"][sid] = max(0, state["monster_skill_cooldowns"][sid] - 1)
    # Monster regenerates stamina and a bit of MP each turn
    state["monster_stamina"] = min(state.get("monster_max_stamina", 100), state.get("monster_stamina", 100) + 15)
    state["monster_mp"] = min(state.get("monster_max_mp", 0), state.get("monster_mp", 0) + 2)

    # Item bonus effects: per-turn regen
    _ibe = state.get("item_bonus_effects", {})
    if _ibe.get("hp_regen", 0) > 0:
        heal = int(_ibe["hp_regen"])
        character["hp"] = min(character.get("max_hp", 999), character.get("hp", 0) + heal)
        log.append({"kind": "item_regen", "text": f"Regen — recovered {heal} HP!"})
    if _ibe.get("mp_regen", 0) > 0:
        mp = int(_ibe["mp_regen"])
        character["mp"] = min(character.get("max_mp", 999), character.get("mp", 0) + mp)
        log.append({"kind": "item_regen", "text": f"Regen — recovered {mp} MP!"})
    # Percentage-based regen from runes
    if _ibe.get("hp_regen_pct", 0) > 0:
        heal = int(character.get("max_hp", 100) * _ibe["hp_regen_pct"])
        if heal > 0:
            character["hp"] = min(character.get("max_hp", 999), character.get("hp", 0) + heal)
            log.append({"kind": "item_regen", "text": f"Regen — recovered {heal} HP!"})
    if _ibe.get("mp_regen_pct", 0) > 0:
        mp = int(character.get("max_mp", 50) * _ibe["mp_regen_pct"])
        if mp > 0:
            character["mp"] = min(character.get("max_mp", 999), character.get("mp", 0) + mp)
            log.append({"kind": "item_regen", "text": f"Regen — recovered {mp} MP!"})

    # Legendary powers — passive per-turn effects (Berserker Rage, Blood Pact downside)
    _apply_legendary_powers_passive(state, character, log)

    # check player death
    if character["hp"] <= 0:
        # Paladin: Resurrection passive (level 90+) — survive at 1 HP
        if _paladin_check_resurrection(state, character, log):
            _clamp_and_sync_combat_hp(character, state)
        # Legendary power: Phoenix Rebirth — revive at 50% HP once per combat
        elif not state.get("lp_revive_used") and "phoenix_rebirth" in state.get("legendary_powers", []):
            state["lp_revive_used"] = True
            revive_hp = int(character.get("max_hp", 1) * 0.50)
            character["hp"] = revive_hp
            _clamp_and_sync_combat_hp(character, state)
            log.append({"kind": "legendary_power", "text": f"PHOENIX REBIRTH — revived at {revive_hp} HP!"})
        else:
            state["active"] = False
            character["hp"] = 1  # brought to 1 (no permadeath in MVP)
            _clamp_and_sync_combat_hp(character, state)
            log.append({"kind": "defeat",
                        "text": f"{character['name']} collapses. The {monster['name']} vanishes into the shadows.",
                        "loss_gold": min(character.get("gold", 0), 20)})
            state["turn"] = turn + 1
            state["log"].extend(log)
            character["stats"] = _orig_stats
            return {"state": state, "log": log, "victory": False, "rewards": None}

    _clamp_and_sync_combat_hp(character, state)
    state["turn"] = turn + 1
    state["log"].extend(log)
    character["stats"] = _orig_stats
    return {"state": state, "log": log, "victory": None, "rewards": None}


# ============================================================
# CRAFTING
# ============================================================
CRAFT_QUEUE_SIZE = 1

# Rank-based duration modifier. Each full rank above novice trims 6% off.
RANK_SPEED_MOD = {
    "novice": 1.00,
    "apprentice": 0.94,
    "journeyman": 0.88,
    "expert": 0.82,
    "master": 0.76,
    "grandmaster": 0.70,
}


def _rank_speed_mod(character: dict, profession_id: str | None) -> float:
    if not profession_id:
        return 1.0
    prof = next((p for p in character.get("professions", []) if p["id"] == profession_id), None)
    if not prof:
        return 1.0
    return RANK_SPEED_MOD.get(prof.get("rank", "novice"), 1.0)


def _craft_duration_seconds(character: dict, recipe: dict) -> float:
    """Return modified crafting duration in seconds."""
    base = float(recipe.get("duration_seconds", 0))
    if base <= 0:
        return 0.0

    profession_id = recipe.get("profession_id")
    continent_id = character.get("current_continent")

    # Profession rank speed
    mult = _rank_speed_mod(character, profession_id)

    # Continental bonus: e.g. blacksmithing.craft_speed_mult on Khardrum
    if continent_id and profession_id:
        bonus = continental_bonus_for(continent_id, profession_id) or {}
        if isinstance(bonus, dict):
            mult *= bonus.get("craft_speed_mult", 1.0)

    # General crafting bonus (some continents may grant global craft speed)
    if continent_id:
        general = continental_bonus_for(continent_id, "crafting")
        if isinstance(general, dict):
            mult *= general.get("craft_speed_mult", 1.0)

    # Dwarf racial bonus for forge crafts
    race = character.get("race", "")
    if race == "dwarf" and profession_id in ("blacksmithing", "armorsmithing", "engineering"):
        mult *= 0.92

    return max(0.0, base * mult)


def _roll_craft(recipe: dict, character: dict) -> dict:
    """Roll the dice and determine output tier/item."""
    player_pow = 5 + character.get("stats", {}).get("cognition", 0) + character.get("level", 1) // 2
    dice = roll_dice(player_pow, 5)
    outcome = dice["outcome"]

    tier = "crude"
    if outcome == 6:
        tier = "master"
    elif outcome in (4, 5):
        tier = "fine"
    elif outcome in (2, 3):
        tier = "crude"

    # Continental bonus: Khardrum durable_equip_chance — chance to upgrade crude→fine
    continent_id = character.get("current_continent", "")
    _dec = continental_bonus_for(continent_id, "durable_equip_chance")
    if _dec and tier == "crude" and random.random() < float(_dec):
        tier = "fine"

    # Continental bonus: Haya celestial_equip_chance — chance to upgrade fine→master
    _cec = continental_bonus_for(continent_id, "celestial_equip_chance")
    if _cec and tier == "fine" and random.random() < float(_cec):
        tier = "master"

    # Heritage month bonus: +15% chance to upgrade one tier on heritage continent
    if continent_id and is_heritage_month_for(continent_id):
        _hb = get_heritage_bonuses(continent_id)
        if _hb:
            _craft_bonus = _hb.get("craft_success_bonus", 0.0)
            if _craft_bonus and tier == "crude" and random.random() < _craft_bonus:
                tier = "fine"
            elif _craft_bonus and tier == "fine" and random.random() < _craft_bonus:
                tier = "master"

    # Item bonus: crafting_quality — chance to upgrade tier by one level
    _cq = _aggregate_item_bonus_effects(character).get("crafting_quality", 0)
    if _cq > 0:
        if tier == "crude" and random.random() < _cq:
            tier = "fine"
        elif tier == "fine" and random.random() < _cq:
            tier = "master"

    lost_materials = False
    output_item = None
    if outcome == 1:
        lost_materials = True
        narrative = pick_narrative("craft", 1, char=character["name"], item=recipe["name"])
    else:
        output_item = recipe["output_by_tier"].get(tier, recipe["output_by_tier"]["crude"])
        narrative = pick_narrative("craft", outcome, char=character["name"], item=recipe["name"])

    return {
        "outcome": outcome,
        "narrative": narrative,
        "lost_materials": lost_materials,
        "output_item": output_item,
        "tier": tier,
    }


def start_craft(character: dict, recipe_id: str) -> dict:
    """Validate materials/profession, consume mats, and queue (or instantly finish) the craft."""
    recipe = RECIPES_BY_ID.get(recipe_id)
    if not recipe:
        return {"error": "Unknown recipe"}
    if character.get("level", 1) < recipe.get("min_level", 1):
        return {"error": "Level too low for this recipe"}

    profession_id = recipe.get("profession_id")
    min_rank = recipe.get("profession_min_rank")
    if profession_id and not has_profession_rank(character, profession_id, min_rank or "novice"):
        prof_name = PROFESSIONS_BY_ID.get(profession_id, {}).get("name", profession_id)
        rank_label = min_rank or "novice"
        return {"error": f"Requires {prof_name} at rank {rank_label}"}

    # Backwards compatibility with old profession_req keyed to role/mastery
    if not profession_id and recipe.get("profession_req"):
        role = character.get("role", "")
        mastery = character.get("mastery", "")
        if role not in recipe["profession_req"] and mastery not in recipe["profession_req"]:
            return {"error": f"Requires mastery: {', '.join(recipe['profession_req'])}"}

    # Queue size check
    queue = character.get("crafting_queue", [])
    if len(queue) >= CRAFT_QUEUE_SIZE:
        return {"error": "Your crafting bench is already busy"}

    # Material check
    inv = {i["item_id"] if isinstance(i, dict) else i[0]: (i["quantity"] if isinstance(i, dict) else i[1])
           for i in character.get("inventory", [])}
    for mat_id, qty in recipe["materials"]:
        if inv.get(mat_id, 0) < qty:
            return {"error": f"Missing material: {mat_id} x{qty}"}

    duration = _craft_duration_seconds(character, recipe)
    now = datetime.now(timezone.utc)
    finishes_at = now + timedelta(seconds=duration)

    entry = {
        "recipe_id": recipe_id,
        "started_at": now.isoformat(),
        "finishes_at": finishes_at.isoformat(),
        "duration_seconds": duration,
        "claimed": False,
    }

    # Instant crafts bypass the queue entirely
    if duration <= 0:
        result = _roll_craft(recipe, character)
        result["recipe_id"] = recipe_id
        result["materials_consumed"] = list(recipe["materials"])
        return result

    character["crafting_queue"] = [entry]
    return {
        "queued": True,
        "recipe_id": recipe_id,
        "recipe_name": recipe["name"],
        "finishes_at": entry["finishes_at"],
        "duration_seconds": duration,
        "materials_consumed": list(recipe["materials"]),
    }


def finish_craft(character: dict, queue_entry: dict) -> dict:
    """Resolve a queued craft: roll outcome, award profession XP, and return result."""
    recipe = RECIPES_BY_ID.get(queue_entry["recipe_id"])
    if not recipe:
        return {"error": "Unknown recipe"}

    result = _roll_craft(recipe, character)
    result["recipe_id"] = queue_entry["recipe_id"]
    result["materials_consumed"] = list(recipe["materials"])

    # Profession points on successful craft (only if not a total failure)
    profession_id = recipe.get("profession_id")
    if profession_id and result["outcome"] >= 2:
        from professions import craft_points_for_roll
        points = craft_points_for_roll(result["outcome"])
        # Apply continental multiplier to points
        continent_id = character.get("current_continent")
        points = int(round(points * xp_multiplier_for(continent_id, profession_id)))
        if points > 0:
            gain_profession_xp(character, profession_id, points)
            result["profession_points_gain"] = points

    return result


# ============================================================
# ENCHANTING — modifies an existing item in inventory
# ============================================================
def start_enchant(character: dict, recipe_id: str, target_item_id: str) -> dict:
    """Validate and execute an enchantment on a target item.

    Enchanting is instant (no queue). On roll 1, the target item may be destroyed
    based on the recipe's destroy_chance. On success, the item gains a stat bonus.
    """
    recipe = RECIPES_BY_ID.get(recipe_id)
    if not recipe:
        return {"error": "Unknown recipe"}
    if not recipe.get("is_enchantment"):
        return {"error": "Not an enchantment recipe"}

    # Check profession rank
    profession_id = recipe.get("profession_id")
    min_rank = recipe.get("profession_min_rank")
    if profession_id and not has_profession_rank(character, profession_id, min_rank or "novice"):
        prof_name = PROFESSIONS_BY_ID.get(profession_id, {}).get("name", profession_id)
        return {"error": f"Requires {prof_name} at rank {min_rank or 'novice'}"}

    # Check level
    if character.get("level", 1) < recipe.get("min_level", 1):
        return {"error": "Level too low for this enchantment"}

    # Check target item exists in inventory
    inv = character.get("inventory", [])
    target_entry = next((i for i in inv if i.get("item_id") == target_item_id), None)
    if not target_entry:
        return {"error": "Target item not in inventory"}

    # Resolve the target against procedural instances FIRST.
    #
    # Everything a player owns is an instance whose id looks like
    # "item_fc91e66e65e7"; those ids are not in ITEMS_BY_ID, which only holds the
    # legacy static catalogue. Looking the target up there alone meant this
    # returned "Unknown target item" for every item anyone could actually own —
    # measured: 0 of 6 instances on a fresh character resolved — so enchanting was
    # dead in practice and only worked for static ids the modern game never
    # creates. Same defect that made compute_armor always return 0.
    target_item = next(
        (i for i in character.get("item_instances", [])
         if i.get("instance_id") == target_item_id),
        None,
    ) or ITEMS_BY_ID.get(target_item_id)
    if not target_item:
        return {"error": "Unknown target item"}

    # Only weapons, armor, and accessories can be enchanted
    if target_item.get("kind") not in ("weapon", "armor", "accessory", "tool"):
        return {"error": "Only weapons, armor, and accessories can be enchanted"}

    # Check if item already has an enchantment (limit 1, or 2 at grandmaster)
    existing_enchants = target_entry.get("enchantments", [])
    max_enchants = 2 if has_profession_rank(character, "enchanting", "grandmaster") else 1
    if len(existing_enchants) >= max_enchants:
        return {"error": f"Item already has {len(existing_enchants)} enchantment(s). Maximum is {max_enchants}."}

    # Check materials
    inv_map = {i["item_id"] if isinstance(i, dict) else i[0]: (i["quantity"] if isinstance(i, dict) else i[1])
               for i in inv}
    for mat_id, qty in recipe["materials"]:
        if inv_map.get(mat_id, 0) < qty:
            return {"error": f"Missing material: {mat_id} x{qty}"}

    # Roll the dice
    result = _roll_craft(recipe, character)
    result["recipe_id"] = recipe_id
    result["target_item_id"] = target_item_id
    result["materials_consumed"] = list(recipe["materials"])

    enchant_stat = recipe.get("enchant_stat", "might")
    enchant_bonus = recipe.get("enchant_bonus", 1)
    destroy_chance = recipe.get("destroy_chance", 0.0)

    if result["outcome"] == 1:
        # Critical failure — check if item is destroyed
        import random as _rng
        if _rng.random() < destroy_chance:
            result["item_destroyed"] = True
            result["narrative"] = f"The enchantment backfired catastrophically! The {target_item.get('name', target_item_id)} was destroyed."
        else:
            result["item_destroyed"] = False
            result["narrative"] = f"The enchantment failed, but the {target_item.get('name', target_item_id)} survived."
    else:
        # Success — apply enchantment
        # Quality affects bonus: roll 5-6 gives +1 extra
        actual_bonus = enchant_bonus
        if result["outcome"] >= 5:
            actual_bonus += 1
            result["narrative"] = f"A surge of power! The {target_item.get('name', target_item_id)} gained +{actual_bonus} {enchant_stat}."
        else:
            result["narrative"] = f"The {target_item.get('name', target_item_id)} gained +{actual_bonus} {enchant_stat}."

        result["enchant_applied"] = True
        result["enchant_stat"] = enchant_stat
        result["enchant_bonus"] = actual_bonus

    # Award profession points
    if profession_id and result["outcome"] >= 2:
        from professions import craft_points_for_roll
        points = craft_points_for_roll(result["outcome"])
        continent_id = character.get("current_continent")
        points = int(round(points * xp_multiplier_for(continent_id, profession_id)))
        if points > 0:
            gain_profession_xp(character, profession_id, points)
            result["profession_points_gain"] = points

    return result


# ============================================================
# STAT TRAINING SYSTEM (The Gym — Torn-style real-time training)
# ============================================================

MAIN_STATS = ["might", "grace", "cognition", "insight", "essence", "durability"]
LIFE_STATS = ["vitality", "max_hp", "max_mp", "max_stamina"]

TRAINING_DAILY_BUDGET_MIN = 180  # 3 hours
TRAINING_STREAK_BONUS_MIN = 60   # +1 hour at 7-day streak
TRAINING_GOLD_PER_POINT = 500    # flat gold cost per +1
TRAINING_BASE_TIME_MIN = 30      # base time per +1
TRAINING_TIME_SCALE_MIN = 5      # extra minutes per stat point above 10
TRAINING_MAIN_CAP = 50           # max trained points per main stat
# Life stats: no cap

TRAINER_SHOP_ITEMS = [
    {
        "id": "hourglass_of_focus",
        "name": "Hourglass of Focus",
        "price": 800,
        "desc": "+1 hr training time today (one-time use).",
        "effect": "bonus_time",
        "effect_value": 60,
        "max_uses_per_day": 1,
    },
    {
        "id": "trainers_whetstone",
        "name": "Trainer's Whetstone",
        "price": 1200,
        "desc": "Halves time cost for next training session (one-time use).",
        "effect": "half_time",
        "max_uses_per_day": 1,
    },
    {
        "id": "surge_token",
        "name": "Surge Token",
        "price": 2000,
        "desc": "Instantly completes current training queue (one-time use).",
        "effect": "instant_complete",
        "max_uses_per_day": 3,
    },
    {
        "id": "mentors_blessing",
        "name": "Mentor's Blessing",
        "price": 3000,
        "desc": "+30 min training time permanently (max 3 purchases).",
        "effect": "permanent_bonus",
        "effect_value": 30,
        "max_purchases": 3,
    },
    {
        "id": "rest_day_pass",
        "name": "Rest Day Pass",
        "price": 500,
        "desc": "Carry over up to 1 hr unused training time to tomorrow (one-time use).",
        "effect": "carry_over",
        "effect_value": 60,
        "max_uses_per_day": 1,
    },
]

TRAINER_SHOP_BY_ID = {item["id"]: item for item in TRAINER_SHOP_ITEMS}


def _training_time_per_point(current_total_stat: int) -> int:
    """Time in minutes to train one +1 to a stat, given its current total value."""
    return TRAINING_BASE_TIME_MIN + max(0, current_total_stat - 10) * TRAINING_TIME_SCALE_MIN


def _training_gold_per_point() -> int:
    """Flat gold cost per +1 trained stat."""
    return TRAINING_GOLD_PER_POINT


def _training_stat_cap(stat: str) -> int | None:
    """Returns the trained-point cap for a stat, or None if uncapped."""
    if stat in MAIN_STATS:
        return TRAINING_MAIN_CAP
    return None  # life stats: no cap


def _training_trainer_type(stat: str) -> str | None:
    """Returns 'main' or 'life' for the stat, or None if not trainable."""
    if stat in MAIN_STATS:
        return "main"
    if stat in LIFE_STATS:
        return "life"
    return None


def _training_daily_budget(character: dict) -> int:
    """Compute today's training time budget in minutes for a character."""
    budget = TRAINING_DAILY_BUDGET_MIN
    # Streak bonus
    if character.get("login_streak", 0) >= 7:
        budget += TRAINING_STREAK_BONUS_MIN
    # Permanent bonus from Mentor's Blessing
    bonus_count = character.get("training_bonus_purchased", 0)
    budget += bonus_count * 30
    # Bonus time from Hourglass of Focus purchased today
    budget += character.get("training_bonus_time_today", 0)
    return budget


def _training_reset_if_needed(character: dict) -> None:
    """Reset daily training time tracking if it's a new day."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    if character.get("last_training_reset") != today:
        character["training_time_used_main"] = 0
        character["training_time_used_life"] = 0
        character["last_training_reset"] = today
        # Reset daily-use tracker for shop items
        character["training_shop_uses_today"] = {}
        # Clear bonus time from Hourglass
        character.pop("training_bonus_time_today", None)
        # Apply carry-over from Rest Day Pass
        carry_pending = character.pop("training_carry_over_pending", 0)
        if carry_pending:
            character["training_carry_over_main"] = carry_pending
            character["training_carry_over_life"] = carry_pending


def _tick_training(character: dict) -> list[dict]:
    """Check if any training queues have finished. Apply stat gains for completed ones.
    Returns list of completed training results for frontend notification."""
    completed = []
    for trainer_type in ("main", "life"):
        queue_key = f"training_queue_{trainer_type}"
        queue = character.get(queue_key)
        if not queue:
            continue
        finishes_at = queue.get("finishes_at")
        if not finishes_at:
            continue
        try:
            finish_dt = datetime.fromisoformat(finishes_at)
        except (ValueError, TypeError):
            character[queue_key] = None
            continue
        if datetime.now(timezone.utc) >= finish_dt:
            # Training complete — apply stat gains
            stat = queue["stat"]
            amount = queue["amount"]
            trained = character.setdefault("trained_stats", {})
            trained[stat] = trained.get(stat, 0) + amount
            # Recompute max_hp / max_mp / max_stamina if life stats
            if stat in LIFE_STATS:
                _recompute_life_stat(character, stat)
            completed.append({
                "trainer_type": trainer_type,
                "stat": stat,
                "amount": amount,
            })
            character[queue_key] = None
    return completed


def _recompute_life_stat(character: dict, stat: str) -> None:
    """Recompute derived HP/MP/Stamina after a life stat training completion."""
    if stat == "vitality":
        # Vitality adds to max_hp at a 10:1 ratio
        trained_vit = character.get("trained_stats", {}).get("vitality", 0)
        base_vit = character.get("base_stats", {}).get("vitality", 0)
        total_vit = base_vit + trained_vit
        # Recompute max_hp from vitality
        old_trained_vit = trained_vit - character.get("_last_vit_trained", 0)
        if old_trained_vit > 0:
            hp_add = old_trained_vit * 10
            character["max_hp"] = character.get("max_hp", 100) + hp_add
            character["hp"] = min(character.get("hp", 1) + hp_add, character["max_hp"])
    elif stat == "max_hp":
        trained_hp = character.get("trained_stats", {}).get("max_hp", 0)
        base_max = character.get("base_max_hp", 100)
        character["max_hp"] = base_max + trained_hp
        character["hp"] = min(character.get("hp", 1), character["max_hp"])
    elif stat == "max_mp":
        trained_mp = character.get("trained_stats", {}).get("max_mp", 0)
        base_max = character.get("base_max_mp", 50)
        character["max_mp"] = base_max + trained_mp
        character["mp"] = min(character.get("mp", 0), character["max_mp"])
    elif stat == "max_stamina":
        trained_stam = character.get("trained_stats", {}).get("max_stamina", 0)
        base_max = character.get("base_max_stamina", 50)
        character["max_stamina"] = base_max + trained_stam
        character["stamina"] = min(character.get("stamina", 0), character["max_stamina"])


def start_training(character: dict, trainer_type: str, stat: str, amount: int) -> dict:
    """Start a training session. Validates time budget, gold, and stat cap.
    Returns dict with success/error info and queue details."""
    if amount <= 0:
        return {"error": "Amount must be at least 1."}
    if amount > 20:
        return {"error": "Cannot train more than 20 points at once."}

    actual_trainer = _training_trainer_type(stat)
    if actual_trainer != trainer_type:
        return {"error": f"{stat} is not trained by the {trainer_type} trainer."}

    # Check if queue is already occupied
    queue_key = f"training_queue_{trainer_type}"
    if character.get(queue_key):
        return {"error": "You already have a training session in progress. Collect it first."}

    # Reset daily tracking if needed
    _training_reset_if_needed(character)

    # Check stat cap
    cap = _training_stat_cap(stat)
    trained = character.get("trained_stats", {})
    current_trained = trained.get(stat, 0)
    if cap is not None and current_trained + amount > cap:
        remaining = cap - current_trained
        if remaining <= 0:
            return {"error": f"{stat} has reached the training cap of +{cap}."}
        return {"error": f"You can only train {remaining} more {stat} (cap: +{cap})."}

    # Compute total time and gold cost
    base_stats = character.get("base_stats", {})
    current_total = base_stats.get(stat, 0) + current_trained
    total_time_min = 0
    total_gold = 0
    for i in range(amount):
        stat_at = current_total + i
        point_time = _training_time_per_point(stat_at)
        # Check for Trainer's Whetstone effect (halves time)
        if character.get("training_whetstone_active"):
            point_time = max(1, point_time // 2)
        total_time_min += point_time
        total_gold += _training_gold_per_point()

    # Clear whetstone after computing (one-time use)
    character.pop("training_whetstone_active", None)

    # Check time budget
    used_key = f"training_time_used_{trainer_type}"
    used = character.get(used_key, 0)
    budget = _training_daily_budget(character)
    # Add carry-over from Rest Day Pass
    carry_over = character.get(f"training_carry_over_{trainer_type}", 0)
    available = budget + carry_over - used
    if total_time_min > available:
        return {
            "error": f"Not enough training time. Need {total_time_min} min, have {available} min available today.",
            "time_needed": total_time_min,
            "time_available": available,
        }

    # Check gold
    if character.get("gold", 0) < total_gold:
        return {
            "error": f"Not enough gold. Need {total_gold}g, have {character.get('gold', 0)}g.",
            "gold_needed": total_gold,
            "gold_available": character.get("gold", 0),
        }

    # Deduct gold and time
    character["gold"] = character.get("gold", 0) - total_gold
    character[used_key] = used + total_time_min

    # Set up queue
    now = datetime.now(timezone.utc)
    finishes_at = now + timedelta(minutes=total_time_min)

    queue = {
        "stat": stat,
        "amount": amount,
        "started_at": now.isoformat(),
        "finishes_at": finishes_at.isoformat(),
        "duration_min": total_time_min,
        "gold_cost": total_gold,
    }
    character[queue_key] = queue

    return {
        "success": True,
        "queue": queue,
        "gold_spent": total_gold,
        "time_spent": total_time_min,
    }


def collect_training(character: dict, trainer_type: str) -> dict:
    """Collect a finished training session. Returns the stat gains or error."""
    queue_key = f"training_queue_{trainer_type}"
    queue = character.get(queue_key)
    if not queue:
        return {"error": "No training session to collect."}

    finishes_at = queue.get("finishes_at")
    if not finishes_at:
        return {"error": "Training queue is corrupted."}

    try:
        finish_dt = datetime.fromisoformat(finishes_at)
    except (ValueError, TypeError):
        character[queue_key] = None
        return {"error": "Training queue timestamp was corrupted. Queue cleared."}

    if datetime.now(timezone.utc) < finish_dt:
        remaining = (finish_dt - datetime.now(timezone.utc)).total_seconds()
        return {
            "error": "Training not yet complete.",
            "remaining_seconds": int(remaining),
            "finishes_at": finishes_at,
        }

    # Apply gains
    stat = queue["stat"]
    amount = queue["amount"]
    # Resolve multiplier — checked at collection time
    mult = _resolve_multiplier(character)
    if mult != 1.0:
        amount = max(1, int(amount * mult))
    trained = character.setdefault("trained_stats", {})
    trained[stat] = trained.get(stat, 0) + amount

    # Recompute life stats if needed
    if stat in LIFE_STATS:
        _recompute_life_stat(character, stat)

    character[queue_key] = None

    return {
        "success": True,
        "stat": stat,
        "amount": amount,
        "new_trained_total": trained[stat],
        "resolve_mult": mult,
    }


def buy_trainer_item(character: dict, item_id: str) -> dict:
    """Purchase and apply a trainer shop item."""
    item = TRAINER_SHOP_BY_ID.get(item_id)
    if not item:
        return {"error": "Unknown item."}

    # Check max purchases for permanent items
    if item.get("max_purchases"):
        purchased = character.get("training_bonus_purchased", 0)
        if purchased >= item["max_purchases"]:
            return {"error": f"You have already purchased the maximum of {item['name']}."}

    # Check daily use limits
    if item.get("max_uses_per_day"):
        uses_today = character.get("training_shop_uses_today", {}).get(item_id, 0)
        if uses_today >= item["max_uses_per_day"]:
            return {"error": f"You have used all {item['name']} for today."}

    # Check gold
    price = item["price"]
    if character.get("gold", 0) < price:
        return {"error": f"Not enough gold. Need {price}g, have {character.get('gold', 0)}g."}

    # Deduct gold
    character["gold"] = character.get("gold", 0) - price

    # Apply effect
    effect = item["effect"]
    if effect == "bonus_time":
        character["training_bonus_time_today"] = character.get("training_bonus_time_today", 0) + item["effect_value"]
    elif effect == "half_time":
        character["training_whetstone_active"] = True
    elif effect == "instant_complete":
        completed = None
        for tt in ("main", "life"):
            qk = f"training_queue_{tt}"
            if character.get(qk):
                queue = character[qk]
                stat = queue["stat"]
                amount = queue["amount"]
                trained = character.setdefault("trained_stats", {})
                trained[stat] = trained.get(stat, 0) + amount
                if stat in LIFE_STATS:
                    _recompute_life_stat(character, stat)
                character[qk] = None
                completed = {"trainer_type": tt, "stat": stat, "amount": amount}
                break
        if not completed:
            return {"error": "No active training queue to complete.", "gold_refund": price}
    elif effect == "permanent_bonus":
        character["training_bonus_purchased"] = character.get("training_bonus_purchased", 0) + 1
    elif effect == "carry_over":
        character["training_carry_over_pending"] = item["effect_value"]

    # Track daily uses
    if item.get("max_uses_per_day"):
        uses = character.setdefault("training_shop_uses_today", {})
        uses[item_id] = uses.get(item_id, 0) + 1

    return {
        "success": True,
        "item": item_id,
        "effect": effect,
        "gold_spent": price,
    }


# ============================================================
# MERCENARY EXPEDITIONS — hire a biome merc, collect loot later
# ============================================================

EXPEDITION_MIN_HOURS = 1
EXPEDITION_MAX_HOURS = 8
EXPEDITION_COOLDOWN_MIN = 30       # minutes after collect before next hire
EXPEDITION_MIN_EXPLORATION = 10    # biome exploration % required to hire

# Loyalty thresholds: hires → efficiency multiplier
LOYALTY_TIERS = [(10, 1.10), (5, 1.05)]


def _merc_loyalty_mult(character: dict, merc_id: str) -> float:
    hires = character.get("merc_loyalty", {}).get(merc_id, 0)
    for threshold, mult in LOYALTY_TIERS:
        if hires >= threshold:
            return mult
    return 1.0


def _expedition_cost(merc: dict, hours: int) -> int:
    from game_data_p2 import MERC_RANKS
    rate = MERC_RANKS[merc["rank"]]["rate"]
    cost = rate * hours
    if merc.get("quirk") == "greedy":
        cost = int(cost * 1.5)
    return cost


def _expedition_yield_points(character: dict, merc: dict, hours: int, biome_id: str) -> float:
    from game_data_p2 import MERC_RANKS
    efficiency = MERC_RANKS[merc["rank"]]["efficiency"]
    exploration = character.get("exploration_progress", {}).get(biome_id, 0)
    exploration_factor = max(0.1, exploration / 100.0)
    points = hours * efficiency * exploration_factor
    points *= _merc_loyalty_mult(character, merc["id"])
    quirk = merc.get("quirk")
    if quirk == "greedy":
        points *= 1.2
    if quirk == "night_owl" and hours >= 4:
        points *= 1.3
    return points


def _expedition_loot_pool(biome_id: str, specialty: str) -> tuple[list[str], list[str]]:
    """Returns (common_pool, rare_pool) of item_ids for a biome + specialty."""
    common_pool: list[str] = []
    rare_pool: list[str] = []
    if specialty == "hunting":
        from game_data import MONSTERS
        for m in MONSTERS:
            if m.get("biome") != biome_id:
                continue
            drops = m.get("drops", {})
            if isinstance(drops, dict):
                for d in drops.get("common", []):
                    if isinstance(d, dict) and d.get("id"):
                        common_pool.append(d["id"])
                for d in drops.get("rare", []):
                    if isinstance(d, dict) and d.get("id"):
                        rare_pool.append(d["id"])
            elif isinstance(drops, list):
                # legacy format: flat list of drop dicts or item-id strings
                for d in drops:
                    if isinstance(d, dict) and d.get("id"):
                        common_pool.append(d["id"])
                    elif isinstance(d, str):
                        common_pool.append(d)
    else:
        from regional_resources import RESOURCE_NODES
        nodes = RESOURCE_NODES.get(biome_id, [])
        if specialty == "fishing":
            wanted = [n for n in nodes if n.get("profession") == "fishing"]
            if not wanted:
                wanted = nodes  # fallback: any node in the biome
        else:  # gathering — everything except fishing
            wanted = [n for n in nodes if n.get("profession") != "fishing"]
            if not wanted:
                wanted = nodes
        for n in wanted:
            if n.get("rarity") in ("rare", "epic", "legendary"):
                rare_pool.append(n["item_id"])
            else:
                common_pool.append(n["item_id"])
        # Starter biomes may have no resource nodes at all —
        # fall back to monster drops so the merc always has something to bring back.
        if not common_pool and not rare_pool:
            return _expedition_loot_pool(biome_id, "hunting")
    return common_pool, rare_pool


def start_expedition(character: dict, biome_id: str, hours: int) -> dict:
    """Hire the biome's merc for N hours. Validates gold, exploration, cooldown."""
    from game_data_p2 import BIOME_MERCS

    if not isinstance(hours, int) or hours < EXPEDITION_MIN_HOURS or hours > EXPEDITION_MAX_HOURS:
        return {"error": f"Hours must be between {EXPEDITION_MIN_HOURS} and {EXPEDITION_MAX_HOURS}."}

    merc = BIOME_MERCS.get(biome_id)
    if not merc:
        return {"error": "No mercenary is stationed in this biome."}

    if character.get("expedition_queue"):
        return {"error": "You already have a mercenary on expedition. Collect them first."}

    # Cooldown check
    cooldown_until = character.get("expedition_cooldown_until")
    if cooldown_until:
        try:
            cd = datetime.fromisoformat(cooldown_until)
            if datetime.now(timezone.utc) < cd:
                remaining = int((cd - datetime.now(timezone.utc)).total_seconds())
                return {"error": f"Mercenaries need a break. Try again in {remaining // 60}m {remaining % 60}s.",
                        "cooldown_seconds": remaining}
        except (ValueError, TypeError):
            pass

    # Exploration requirement
    exploration = character.get("exploration_progress", {}).get(biome_id, 0)
    if exploration < EXPEDITION_MIN_EXPLORATION:
        return {"error": f"You need at least {EXPEDITION_MIN_EXPLORATION}% exploration in this biome to hire a merc (have {exploration}%)."}

    # Gold check
    cost = _expedition_cost(merc, hours)
    if character.get("gold", 0) < cost:
        return {"error": f"Not enough gold. {merc['name']} charges {cost}g for {hours}hr.",
                "gold_needed": cost}

    character["gold"] = character.get("gold", 0) - cost

    now = datetime.now(timezone.utc)
    finishes_at = now + timedelta(hours=hours)
    queue = {
        "biome_id": biome_id,
        "merc_id": merc["id"],
        "merc_name": merc["name"],
        "specialty": merc["specialty"],
        "hours": hours,
        "started_at": now.isoformat(),
        "finishes_at": finishes_at.isoformat(),
        "cost": cost,
        "resolve_at_hire": character.get("resolve", 50),
    }
    character["expedition_queue"] = queue

    return {"success": True, "queue": queue, "gold_spent": cost}


def collect_expedition(character: dict) -> dict:
    """Collect a finished expedition. Rolls loot, updates loyalty, sets cooldown."""
    queue = character.get("expedition_queue")
    if not queue:
        return {"error": "No expedition to collect."}

    try:
        finish_dt = datetime.fromisoformat(queue["finishes_at"])
    except (ValueError, TypeError, KeyError):
        character["expedition_queue"] = None
        return {"error": "Expedition record was corrupted. Cleared."}

    if datetime.now(timezone.utc) < finish_dt:
        remaining = int((finish_dt - datetime.now(timezone.utc)).total_seconds())
        return {"error": "Expedition not yet complete.", "remaining_seconds": remaining}

    from game_data_p2 import BIOME_MERCS
    biome_id = queue["biome_id"]
    hours = queue["hours"]
    merc = BIOME_MERCS.get(biome_id, {})
    merc_id = queue.get("merc_id", merc.get("id", ""))
    specialty = queue.get("specialty", merc.get("specialty", "gathering"))
    quirk = merc.get("quirk")

    # Yield
    points = _expedition_yield_points(character, merc, hours, biome_id) if merc else float(hours)
    # Resolve modifier — snapshot at hire time
    resolve_at_hire = queue.get("resolve_at_hire", 50)
    resolve_mod = _resolve_expedition_mod({"resolve": resolve_at_hire})
    points *= resolve_mod["yield_mult"]
    guaranteed = max(1, int(points))  # always at least 1 item — no failure
    extra_chance = points - int(points)
    total_items = guaranteed + (1 if random.random() < extra_chance else 0)

    common_pool, rare_pool = _expedition_loot_pool(biome_id, specialty)
    loot: dict[str, int] = {}
    if common_pool:
        for _ in range(total_items):
            item_id = random.choice(common_pool)
            loot[item_id] = loot.get(item_id, 0) + 1

    # Lucky quirk: chance at a rare item
    # Resolve good outcome: extra rare chance at Peak/Focused
    rare_found = None
    if rare_pool:
        rare_chance = 0.05 + (0.10 if quirk == "lucky" else 0.0)
        rare_chance += resolve_mod["good_chance"]
        if random.random() < rare_chance:
            rare_found = random.choice(rare_pool)
            loot[rare_found] = loot.get(rare_found, 0) + 1

    # Add loot to inventory
    inv = character.setdefault("inventory", [])
    for item_id, qty in loot.items():
        for slot in inv:
            if slot.get("item_id") == item_id:
                slot["quantity"] = slot.get("quantity", 0) + qty
                break
        else:
            inv.append({"item_id": item_id, "quantity": qty})

    # Hunting expeditions also give XP
    xp_gain = 0
    if specialty == "hunting":
        xp_gain = hours * 15
        character["xp"] = character.get("xp", 0) + xp_gain

    # Scout quirk: biome exploration
    exploration_gain = 0
    if quirk == "scout":
        ep = character.setdefault("exploration_progress", {})
        old = int(ep.get(biome_id, 0))
        exploration_gain = min(5, 100 - old)
        ep[biome_id] = old + exploration_gain

    # Loyalty
    loyalty = character.setdefault("merc_loyalty", {})
    loyalty[merc_id] = loyalty.get(merc_id, 0) + 1

    # Clear queue + set cooldown
    character["expedition_queue"] = None
    character["expedition_cooldown_until"] = (
        datetime.now(timezone.utc) + timedelta(minutes=EXPEDITION_COOLDOWN_MIN)
    ).isoformat()

    return {
        "success": True,
        "loot": [{"item_id": k, "quantity": v} for k, v in loot.items()],
        "rare_found": rare_found,
        "xp_gain": xp_gain,
        "exploration_gain": exploration_gain,
        "merc_name": queue.get("merc_name", "The merc"),
        "loyalty_hires": loyalty[merc_id],
    }


def get_expedition_merc_info(character: dict, biome_id: str) -> dict | None:
    """Full merc info for a biome including player-specific loyalty and rates."""
    from game_data_p2 import BIOME_MERCS, MERC_RANKS
    merc = BIOME_MERCS.get(biome_id)
    if not merc:
        return None
    rank_info = MERC_RANKS[merc["rank"]]
    hires = character.get("merc_loyalty", {}).get(merc["id"], 0)
    common_pool, rare_pool = _expedition_loot_pool(biome_id, merc["specialty"])
    hourly_rate = rank_info["rate"]
    if merc.get("quirk") == "greedy":
        hourly_rate = int(hourly_rate * 1.5)
    return {
        **merc,
        "biome_id": biome_id,
        "hourly_rate": hourly_rate,
        "base_rate": rank_info["rate"],
        "efficiency": rank_info["efficiency"],
        "loyalty_hires": hires,
        "loyalty_mult": _merc_loyalty_mult(character, merc["id"]),
        "loot_preview": common_pool[:8],
        "rare_preview": rare_pool[:4],
    }


# ============================================================
# STUDY PERKS SYSTEM — Atlantyrion Academy
# ============================================================

from game_data_p2 import (
    STUDY_COURSES, STUDY_TIER_COSTS, STUDY_TIER_DAYS,
    STUDY_BONUS_PER_TIER, STUDY_XP_BONUS_PCT,
    STUDY_BUFF_BASE_HOURS, STUDY_STREAK_BONUS,
)


def _today_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def _study_buff_hours(streak: int) -> int:
    """Compute buff duration in hours based on login streak."""
    hours = STUDY_BUFF_BASE_HOURS
    for threshold, bonus in sorted(STUDY_STREAK_BONUS.items()):
        if streak >= threshold:
            hours = STUDY_BUFF_BASE_HOURS + bonus
    return hours


def _study_is_exam_day(enrollment: dict) -> bool:
    """True if the next check-in will complete the current tier."""
    if not enrollment:
        return False
    tier = enrollment.get("current_tier", 1)
    required = STUDY_TIER_DAYS[tier - 1]
    completed = enrollment.get("login_days_completed", 0)
    return completed + 1 >= required


def _study_active_buff(character: dict) -> dict | None:
    """Return the active study buff dict if it hasn't expired, else None."""
    buff = character.get("study_buff")
    if not buff:
        return None
    expires_at = buff.get("expires_at")
    if expires_at and datetime.now(timezone.utc).timestamp() < datetime.fromisoformat(expires_at).timestamp():
        return buff
    return None


def _study_completed_tiers(character: dict, stat: str) -> int:
    """Return the number of completed tiers for a given stat."""
    perks = character.get("study_perks", {})
    return perks.get(stat, 0)


def _study_permanent_bonus_pct(character: dict, stat: str) -> int:
    """Return the permanent bonus percentage for a stat from completed study tiers."""
    return _study_completed_tiers(character, stat) * STUDY_BONUS_PER_TIER


def _study_buff_bonus_pct(character: dict, stat: str) -> int:
    """Return the active buff bonus percentage for a stat (0 if no active buff)."""
    buff = _study_active_buff(character)
    if buff and buff.get("stat") == stat:
        return buff.get("bonus_pct", 0)
    return 0


def _apply_study_perks_to_stats(character: dict) -> None:
    """Apply permanent study perks to character stats. Called during _recompute_stats."""
    perks = character.get("study_perks", {})
    if not perks:
        return
    base = character.get("base_stats", {})
    stats = character.get("stats", {})
    for stat, completed_tiers in perks.items():
        if completed_tiers <= 0:
            continue
        bonus_pct = completed_tiers * STUDY_BONUS_PER_TIER
        base_val = base.get(stat, 0)
        if base_val > 0:
            bonus = int(base_val * bonus_pct / 100)
            if bonus > 0:
                stats[stat] = stats.get(stat, 0) + bonus


def _apply_study_buff_to_stats(character: dict) -> None:
    """Apply active study buff to character stats. Called during _recompute_stats after perks."""
    buff = _study_active_buff(character)
    if not buff:
        return
    stat = buff.get("stat")
    bonus_pct = buff.get("bonus_pct", 0)
    if not stat or bonus_pct <= 0:
        return
    base = character.get("base_stats", {})
    base_val = base.get(stat, 0)
    if base_val > 0:
        bonus = int(base_val * bonus_pct / 100)
        if bonus > 0:
            character["stats"][stat] = character["stats"].get(stat, 0) + bonus


def _tick_study(character: dict) -> dict | None:
    """Check if study buff expired; clear it if so. Returns completion info if a tier just completed."""
    buff = character.get("study_buff")
    if buff:
        expires_at = buff.get("expires_at")
        if expires_at and datetime.now(timezone.utc).timestamp() >= datetime.fromisoformat(expires_at).timestamp():
            character["study_buff"] = None

    # Check if tier completed (login_days_completed >= required)
    enrollment = character.get("study_enrollment")
    if not enrollment:
        return None

    tier = enrollment.get("current_tier", 1)
    required = STUDY_TIER_DAYS[tier - 1]
    completed = enrollment.get("login_days_completed", 0)

    if completed >= required:
        # Tier complete!
        stat = enrollment.get("stat")
        course_id = enrollment.get("course_id")
        perks = character.setdefault("study_perks", {})
        perks[stat] = tier  # set to the completed tier level
        character["study_enrollment"] = None
        return {
            "completed": True,
            "course_id": course_id,
            "stat": stat,
            "tier": tier,
            "permanent_bonus_pct": tier * STUDY_BONUS_PER_TIER,
        }
    return None


def enroll_study(character: dict, course_id: str) -> dict:
    """Enroll in a study course tier. Validates gold, prerequisites, and existing enrollment."""
    course = STUDY_COURSES.get(course_id)
    if not course:
        return {"error": "Unknown course"}

    stat = course["stat"]
    completed_tiers = _study_completed_tiers(character, stat)

    # Determine which tier to enroll in
    next_tier = completed_tiers + 1
    if next_tier > 5:
        return {"error": "All tiers of this course are already completed"}

    # Check if already enrolled in a different course
    existing = character.get("study_enrollment")
    if existing:
        if existing.get("course_id") == course_id:
            return {"error": "Already enrolled in this course"}
        # Abandoning current course — no refund, progress lost
        character["study_enrollment"] = None
        character["study_buff"] = None

    # Check gold
    cost = STUDY_TIER_COSTS[next_tier - 1]
    if character.get("gold", 0) < cost:
        return {"error": f"Need {cost} gold to enroll in tier {next_tier}"}

    character["gold"] = character.get("gold", 0) - cost
    character["study_enrollment"] = {
        "course_id": course_id,
        "stat": stat,
        "category": course["category"],
        "current_tier": next_tier,
        "login_days_completed": 0,
        "last_checkin_date": None,
        "streak": 0,
        "enrolled_at": datetime.now(timezone.utc).isoformat(),
    }

    return {
        "success": True,
        "course_id": course_id,
        "course_name": course["name"],
        "tier": next_tier,
        "cost": cost,
        "required_days": STUDY_TIER_DAYS[next_tier - 1],
    }


def study_daily_checkin(character: dict) -> dict:
    """Daily check-in for the enrolled study course. Grants buff and increments progress."""
    enrollment = character.get("study_enrollment")
    if not enrollment:
        return {"error": "Not enrolled in any course"}

    today = _today_utc()
    if enrollment.get("last_checkin_date") == today:
        return {"error": "Already checked in today. Come back tomorrow!"}

    # Update streak
    yesterday = (datetime.now(timezone.utc) - timedelta(days=1)).strftime("%Y-%m-%d")
    last_date = enrollment.get("last_checkin_date")
    if last_date and last_date == yesterday:
        enrollment["streak"] = enrollment.get("streak", 0) + 1
    else:
        enrollment["streak"] = 1

    enrollment["last_checkin_date"] = today
    enrollment["login_days_completed"] = enrollment.get("login_days_completed", 0) + 1

    tier = enrollment.get("current_tier", 1)
    stat = enrollment.get("stat")
    category = enrollment.get("category")
    course_id = enrollment.get("course_id")
    streak = enrollment.get("streak", 1)

    # Compute buff
    is_exam_day = _study_is_exam_day(enrollment)
    bonus_pct = tier * STUDY_BONUS_PER_TIER
    if is_exam_day:
        bonus_pct *= 2  # Exam day: doubled buff

    buff_hours = _study_buff_hours(streak)
    # Resolve bonus: extends buff duration
    buff_hours = _resolve_study_buff_hours(character, buff_hours)
    expires_at = (datetime.now(timezone.utc) + timedelta(hours=buff_hours)).isoformat()

    xp_bonus_type = "hunting" if category == "main" else "gathering"

    character["study_buff"] = {
        "stat": stat,
        "bonus_pct": bonus_pct,
        "expires_at": expires_at,
        "xp_bonus_type": xp_bonus_type,
        "xp_bonus_pct": STUDY_XP_BONUS_PCT,
        "is_exam_day": is_exam_day,
    }

    # Check if tier completed
    required = STUDY_TIER_DAYS[tier - 1]
    completed = enrollment["login_days_completed"]
    tier_completed = completed >= required

    if tier_completed:
        perks = character.setdefault("study_perks", {})
        perks[stat] = tier
        character["study_enrollment"] = None

    return {
        "success": True,
        "course_id": course_id,
        "stat": stat,
        "tier": tier,
        "bonus_pct": bonus_pct,
        "buff_hours": buff_hours,
        "expires_at": expires_at,
        "xp_bonus_type": xp_bonus_type,
        "xp_bonus_pct": STUDY_XP_BONUS_PCT,
        "is_exam_day": is_exam_day,
        "streak": streak,
        "login_days_completed": completed,
        "required_days": required,
        "tier_completed": tier_completed,
        "permanent_bonus_pct": tier * STUDY_BONUS_PER_TIER if tier_completed else None,
    }


def abandon_study(character: dict) -> dict:
    """Abandon current study course. No refund, progress lost."""
    enrollment = character.get("study_enrollment")
    if not enrollment:
        return {"error": "Not enrolled in any course"}

    course_id = enrollment.get("course_id")
    character["study_enrollment"] = None
    character["study_buff"] = None

    return {"success": True, "abandoned_course": course_id}


def get_study_status(character: dict) -> dict:
    """Return full study status for the frontend."""
    enrollment = character.get("study_enrollment")
    buff = _study_active_buff(character)
    perks = character.get("study_perks", {})

    courses_info = []
    for course_id, course in STUDY_COURSES.items():
        stat = course["stat"]
        completed = perks.get(stat, 0)
        next_tier = completed + 1
        can_enroll = next_tier <= 5
        cost = STUDY_TIER_COSTS[next_tier - 1] if can_enroll else None
        required_days = STUDY_TIER_DAYS[next_tier - 1] if can_enroll else None
        is_enrolled = enrollment and enrollment.get("course_id") == course_id

        courses_info.append({
            "id": course_id,
            "name": course["name"],
            "stat": stat,
            "category": course["category"],
            "desc": course["desc"],
            "completed_tiers": completed,
            "permanent_bonus_pct": completed * STUDY_BONUS_PER_TIER,
            "next_tier": next_tier if can_enroll else None,
            "next_tier_cost": cost,
            "next_tier_days": required_days,
            "is_enrolled": bool(is_enrolled),
        })

    enrollment_info = None
    if enrollment:
        tier = enrollment.get("current_tier", 1)
        required = STUDY_TIER_DAYS[tier - 1]
        completed_days = enrollment.get("login_days_completed", 0)
        enrollment_info = {
            "course_id": enrollment.get("course_id"),
            "stat": enrollment.get("stat"),
            "category": enrollment.get("category"),
            "current_tier": tier,
            "login_days_completed": completed_days,
            "required_days": required,
            "streak": enrollment.get("streak", 0),
            "last_checkin_date": enrollment.get("last_checkin_date"),
            "is_exam_day": _study_is_exam_day(enrollment),
            "buff_hours": _study_buff_hours(enrollment.get("streak", 0)),
            "today_checked_in": enrollment.get("last_checkin_date") == _today_utc(),
        }

    buff_info = None
    if buff:
        buff_info = {
            "stat": buff.get("stat"),
            "bonus_pct": buff.get("bonus_pct"),
            "expires_at": buff.get("expires_at"),
            "xp_bonus_type": buff.get("xp_bonus_type"),
            "xp_bonus_pct": buff.get("xp_bonus_pct"),
            "is_exam_day": buff.get("is_exam_day", False),
        }

    return {
        "courses": courses_info,
        "enrollment": enrollment_info,
        "buff": buff_info,
        "perks": perks,
    }


def study_xp_bonus_for_action(character: dict, action_id: str) -> float:
    """Return XP multiplier (1.0 = no bonus) for hunting/gathering actions based on active study buff."""
    buff = _study_active_buff(character)
    if not buff:
        return 1.0

    xp_type = buff.get("xp_bonus_type")
    if xp_type == "hunting" and action_id == "hunt":
        return 1.0 + buff.get("xp_bonus_pct", 0) / 100.0
    if xp_type == "gathering" and action_id in ("gather", "fish"):
        return 1.0 + buff.get("xp_bonus_pct", 0) / 100.0

    return 1.0


# ============================================================
# RESOLVE SYSTEM — global progression multiplier
# ============================================================

RESOLVE_FLOOR   = 50   # natural regen ceiling and equilibrium
RESOLVE_RESTED  = 65   # sanctuary rest target; decay floor above this
RESOLVE_DEMORALIZED = 25  # below this = penalty tier
RESOLVE_FOCUSED = 65   # at/above this = bonus tier
RESOLVE_PEAK    = 85   # at/above this = max bonus tier
REGEN_PER_HOUR  = 2
DECAY_PER_HOUR  = 1


def _tick_resolve(ch: dict) -> None:
    """Advance Resolve toward equilibrium. Pure function of stored state.

    Charges only the whole hours it actually applies and advances the timestamp
    by exactly that much, so sub-hour remainders are preserved for the next tick.
    """
    now = datetime.now(timezone.utc)
    last_raw = ch.get("last_resolve_update")
    if last_raw is None:
        ch["last_resolve_update"] = now.isoformat()
        return

    try:
        last = datetime.fromisoformat(last_raw)
    except (ValueError, TypeError):
        ch["last_resolve_update"] = now.isoformat()
        return

    if last.tzinfo is None:
        last = last.replace(tzinfo=timezone.utc)

    hours = int((now - last).total_seconds() // 3600)
    if hours <= 0:
        return

    r = int(ch.get("resolve", RESOLVE_FLOOR))
    if r < RESOLVE_FLOOR:
        r = min(RESOLVE_FLOOR, r + hours * REGEN_PER_HOUR)
    elif r > RESOLVE_RESTED:
        r = max(RESOLVE_RESTED, r - hours * DECAY_PER_HOUR)
    # 50..65 inclusive: equilibrium, no change

    ch["resolve"] = max(0, min(100, r))
    ch["last_resolve_update"] = (last + timedelta(hours=hours)).isoformat()


def _resolve_tier(ch: dict) -> str:
    """Return the tier name for the current Resolve value."""
    r = ch.get("resolve", RESOLVE_FLOOR)
    if r < RESOLVE_DEMORALIZED:
        return "Demoralized"
    if r < RESOLVE_FOCUSED:
        return "Stable"
    if r < RESOLVE_PEAK:
        return "Focused"
    return "Peak"


def _resolve_multiplier(ch: dict) -> float:
    """Training gain multiplier based on Resolve."""
    r = ch.get("resolve", RESOLVE_FLOOR)
    if r < RESOLVE_DEMORALIZED:
        return 0.75
    if r < RESOLVE_FOCUSED:
        return 1.0
    if r < RESOLVE_PEAK:
        return 1.10
    return 1.25


def _resolve_study_buff_hours(ch: dict, base_hours: float) -> float:
    """Study buff duration with Resolve bonus."""
    r = ch.get("resolve", RESOLVE_FLOOR)
    if r < RESOLVE_DEMORALIZED:
        return base_hours * 0.5
    if r < RESOLVE_FOCUSED:
        return float(base_hours)
    if r < RESOLVE_PEAK:
        return base_hours + 1.0
    return base_hours + 2.0


def _resolve_combat_damage_mod(ch: dict) -> float:
    """Combat damage modifier based on Resolve."""
    r = ch.get("resolve", RESOLVE_FLOOR)
    if r < RESOLVE_DEMORALIZED:
        return 0.90
    if r >= RESOLVE_PEAK:
        return 1.05
    return 1.0


def _resolve_expedition_mod(ch: dict) -> dict:
    """Expedition yield + outcome modifiers based on Resolve."""
    r = ch.get("resolve", RESOLVE_FLOOR)
    if r < RESOLVE_DEMORALIZED:
        return {"yield_mult": 0.85, "good_chance": 0.0, "poor_chance": 0.05}
    if r < RESOLVE_FOCUSED:
        return {"yield_mult": 1.0, "good_chance": 0.0, "poor_chance": 0.0}
    if r < RESOLVE_PEAK:
        return {"yield_mult": 1.10, "good_chance": 0.05, "poor_chance": 0.0}
    return {"yield_mult": 1.20, "good_chance": 0.10, "poor_chance": 0.0}


def _resolve_combat_gain(ch: dict, monster_threat: int) -> int:
    """Resolve gain for winning a battle, based on threat/rating ratio."""
    from game_data import compute_action_rating
    rating = compute_action_rating(ch)
    if rating <= 0:
        return 0
    ratio = monster_threat / rating
    if ratio < 0.10:
        return 0
    if ratio < 0.50:
        return 1
    if ratio < 1.00:
        return 2
    return 3


def _award_resolve(ch: dict, delta: int, reason: str = "") -> int:
    """Apply a Resolve change, clamping to 0-100. Returns the new value."""
    r = ch.get("resolve", RESOLVE_FLOOR)
    r = max(0, min(100, r + delta))
    ch["resolve"] = r
    history = ch.setdefault("resolve_history", [])
    history.insert(0, {"delta": delta, "reason": reason, "at": datetime.now(timezone.utc).isoformat()})
    ch["resolve_history"] = history[:10]
    return r


def _resolve_fields(ch: dict) -> dict:
    """Always write resolve + last_resolve_update together."""
    return {
        "resolve": ch.get("resolve", RESOLVE_FLOOR),
        "last_resolve_update": ch.get("last_resolve_update"),
    }
