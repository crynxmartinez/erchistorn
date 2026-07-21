"""Dice, action resolution, combat engine, crafting engine."""
from __future__ import annotations

import random
from typing import Any

from game_data import (
    BIOME_ACTIONS,
    ITEMS_BY_ID,
    MONSTERS,
    RECIPES_BY_ID,
    SKILLS_BY_ID,
    compute_player_power,
    get_monster,
    get_race,
)
from narratives import pick_narrative
from racial import racial_combat_mods, tick_racial_on_combat_win


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
# ACTION RESOLUTION (non-combat: hunt/gather/explore/fish/loot_ruins)
# ============================================================
STATUS_TEMPLATES: dict[str, dict] = {
    "bleeding":  {"name": "Bleeding",  "kind": "debuff", "duration": 3, "magnitude": 2},
    "poisoned":  {"name": "Poisoned",  "kind": "debuff", "duration": 4, "magnitude": 3},
    "exhausted": {"name": "Exhausted", "kind": "debuff", "duration": 2, "magnitude": 0},
    "sick":      {"name": "Sick",      "kind": "debuff", "duration": 5, "magnitude": 1},
    "cursed":    {"name": "Cursed",    "kind": "debuff", "duration": 6, "magnitude": 0},
    "blessed":   {"name": "Blessed",   "kind": "buff",   "duration": 4, "magnitude": 2},
    "focused":   {"name": "Focused",   "kind": "buff",   "duration": 3, "magnitude": 2},
    "burning":   {"name": "Burning",   "kind": "debuff", "duration": 3, "magnitude": 3},
    "stunned":   {"name": "Stunned",   "kind": "debuff", "duration": 1, "magnitude": 0},
    "shaken":    {"name": "Shaken",    "kind": "debuff", "duration": 2, "magnitude": 1},
    "blinded":   {"name": "Blinded",   "kind": "debuff", "duration": 2, "magnitude": 1},
    "ensnared":  {"name": "Ensnared",  "kind": "debuff", "duration": 2, "magnitude": 0},
    "warded":    {"name": "Warded",    "kind": "buff",   "duration": 3, "magnitude": 2},
    "hidden":    {"name": "Hidden",    "kind": "buff",   "duration": 2, "magnitude": 0},
    "evasive":   {"name": "Evasive",   "kind": "buff",   "duration": 2, "magnitude": 2},
}


def make_status(status_id: str) -> dict:
    tpl = STATUS_TEMPLATES.get(status_id, {"name": status_id.title(), "kind": "debuff", "duration": 2, "magnitude": 1})
    return {"id": status_id, **tpl}


def _append_status_dedup(char_or_state: dict, status: dict, key: str = "statuses") -> None:
    """Add or refresh a status without duplicates."""
    lst = char_or_state.setdefault(key, [])
    for s in lst:
        if s.get("id") == status.get("id"):
            s["duration"] = max(int(s.get("duration", 0)), int(status.get("duration", 0)))
            return
    lst.append(status)


def resolve_action(character: dict, action_id: str, biome_id: str, target_id: str | None) -> dict:
    """Resolve a non-combat action node. Returns dict with outcome, narrative, rewards, hp_delta, status."""
    action_meta = None
    for a in BIOME_ACTIONS.get(biome_id, []):
        if a["id"] == action_id:
            action_meta = a
            break
    if not action_meta:
        return {"error": f"Action '{action_id}' not available in biome '{biome_id}'"}

    # Pick a target if not specified
    if not target_id and action_meta.get("targets"):
        target_id = random.choice(action_meta["targets"])

    player_pow = compute_player_power(character)
    if action_id == "hunt":
        monster = get_monster(target_id) if target_id else None
        target_pow = monster["power"] if monster else 5
        target_name = monster["name"] if monster else "quarry"
    elif action_id in ("gather", "fish"):
        target_pow = 4
        target_name = (ITEMS_BY_ID.get(target_id or "", {}).get("name")) if target_id else "resource"
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
    elif outcome == 2:  # fail + status
        hp_delta = -random.randint(2, 6)
        # apply a random bad status
        status_applied = random.choice(["bleeding", "poisoned", "exhausted", "sick"])
    elif outcome == 3:  # fail
        hp_delta = 0
    elif outcome == 4:  # success + bad
        hp_delta = -random.randint(1, 4)
        status_applied = random.choice(["bleeding", "exhausted"])
        _apply_action_rewards(action_id, target_id, rewards, tier="normal", monster=get_monster(target_id) if action_id == "hunt" else None)
        if action_id == "hunt":
            monster_slain = target_id
    elif outcome == 5:  # success
        _apply_action_rewards(action_id, target_id, rewards, tier="normal", monster=get_monster(target_id) if action_id == "hunt" else None)
        if action_id == "hunt":
            monster_slain = target_id
    elif outcome == 6:  # crit success
        _apply_action_rewards(action_id, target_id, rewards, tier="critical", monster=get_monster(target_id) if action_id == "hunt" else None)
        if action_id == "hunt":
            monster_slain = target_id

    return {
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


def _apply_action_rewards(action_id: str, target_id: str | None, rewards: dict, tier: str, monster: dict | None):
    if action_id == "hunt" and monster:
        rewards["xp"] += 15 + monster["power"] * 3
        rewards["gold"] += 5 + monster["power"]
        for drop_id, chance in monster.get("drops", []):
            roll = random.random()
            if tier == "critical":
                roll *= 0.5  # double chance
            if roll <= chance:
                rewards["items"].append((drop_id, 1))
    elif action_id in ("gather", "fish"):
        rewards["xp"] += 5
        rewards["gold"] += 2
        material_id = target_id or "wild_herb"
        qty = 2 if tier == "critical" else 1
        rewards["items"].append((material_id, qty))
        # crit gets a bonus rare drop
        if tier == "critical":
            rare_bonus = random.choice(["relic_shard", "wisp_essence", "serpent_venom"])
            rewards["items"].append((rare_bonus, 1))
    elif action_id == "explore":
        rewards["xp"] += 10
        rewards["gold"] += 5
        if tier == "critical":
            rewards["gold"] += 40
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
def start_combat(character: dict, monster_id: str) -> dict:
    monster = get_monster(monster_id)
    if not monster:
        return {"error": f"Unknown monster: {monster_id}"}
    return {
        "monster_id": monster_id,
        "monster_name": monster["name"],
        "monster_hp": monster["hp"],
        "monster_max_hp": monster["hp"],
        "monster_power": monster["power"],
        "monster_statuses": [],
        "player_statuses": list(character.get("statuses", [])),
        "turn": 0,
        "skill_cooldowns": {},
        "item_cooldowns": {},
        "log": [],
        "active": True,
    }


def _pick_best_skill(character: dict, state: dict, hp_ratio: float, enemy_hp_ratio: float, turn: int) -> str | None:
    """Pick the best skill from the character's learned skills that is not on cooldown and matches trigger."""
    learned = character.get("skills", [])
    best = None
    best_score = -1
    for ls in learned:
        sid = ls["skill_id"] if isinstance(ls, dict) else ls
        cd = state["skill_cooldowns"].get(sid, 0)
        if cd > 0:
            continue
        skill = SKILLS_BY_ID.get(sid)
        if not skill:
            continue
        trig = skill.get("trigger", "always")
        if trig == "low_hp" and hp_ratio > 0.5:
            continue
        if trig == "opponent_wounded" and enemy_hp_ratio > 0.6:
            continue
        if trig == "opening_move" and turn > 0:
            continue
        if trig == "opponent_status" and not state.get("monster_statuses"):
            continue
        if trig == "self_debuff" and not any(
            s.get("kind") == "debuff" for s in state.get("player_statuses", [])
        ):
            continue
        # score
        score = skill.get("power", 0)
        if skill.get("power_type") == "heal" and hp_ratio < 0.4:
            score += 10  # prioritize heal when hurt
        if skill.get("power_type") == "defend" and hp_ratio < 0.35:
            score += 6
        if score > best_score:
            best_score = score
            best = sid
    return best


def _pick_best_item(character: dict, state: dict, hp_ratio: float) -> str | None:
    for inv in character.get("inventory", []):
        iid = inv["item_id"] if isinstance(inv, dict) else inv[0]
        qty = inv["quantity"] if isinstance(inv, dict) else inv[1]
        if qty <= 0:
            continue
        cd = state["item_cooldowns"].get(iid, 0)
        if cd > 0:
            continue
        item = ITEMS_BY_ID.get(iid)
        if not item or item.get("kind") != "consumable":
            continue
        trig = item.get("trigger", "always")
        if trig == "hp_below_50" and hp_ratio > 0.5:
            continue
        if trig == "hp_below_40" and hp_ratio > 0.4:
            continue
        if trig == "status_poison" and not any(s.get("id") == "poisoned" for s in state.get("player_statuses", [])):
            continue
        if trig == "status_bleeding" and not any(s.get("id") == "bleeding" for s in state.get("player_statuses", [])):
            continue
        return iid
    return None


def combat_turn(character: dict, state: dict, manual_skill_id: str | None = None, manual_item_id: str | None = None) -> dict:
    """Execute one round: player action, then enemy action."""
    if not state.get("active"):
        return {"error": "Combat is not active"}

    monster = get_monster(state["monster_id"])
    turn = state["turn"]
    hp_ratio = character["hp"] / max(1, character["max_hp"])
    enemy_hp_ratio = state["monster_hp"] / max(1, state["monster_max_hp"])

    log: list[dict] = []

    # racial combat mods for this turn
    r_mods = racial_combat_mods(character)
    for m in r_mods.get("log_msgs", []):
        log.append({"kind": "racial", "text": m})

    # -------- player turn --------
    skill_id = manual_skill_id or _pick_best_skill(character, state, hp_ratio, enemy_hp_ratio, turn)
    item_id = manual_item_id or _pick_best_item(character, state, hp_ratio)

    # Item first (usually healing before strike)
    if item_id:
        item = ITEMS_BY_ID.get(item_id, {})
        eff = item.get("effect", {})
        used_msg = ""
        if "heal" in eff:
            heal = int(int(eff["heal"]) * r_mods["heal_mult"])
            character["hp"] = min(character["max_hp"], character["hp"] + heal)
            used_msg = f"{character['name']} uses {item['name']} and heals {heal} HP."
        elif "damage" in eff:
            dmg = int(eff["damage"])
            state["monster_hp"] = max(0, state["monster_hp"] - dmg)
            used_msg = f"{character['name']} hurls {item['name']} — the {monster['name']} takes {dmg} damage!"
        elif "cure" in eff:
            cured = eff["cure"]
            character["statuses"] = [s for s in character.get("statuses", []) if s.get("id") != cured]
            used_msg = f"{character['name']} uses {item['name']} and cures {cured}."
        log.append({"kind": "item", "text": used_msg, "item_id": item_id})
        # decrement quantity
        for inv in character.get("inventory", []):
            if inv.get("item_id") == item_id:
                inv["quantity"] = max(0, inv["quantity"] - 1)
                break
        state["item_cooldowns"][item_id] = 1

    # Skill / basic strike
    player_pow = compute_player_power(character) + r_mods["strike_bonus"]
    dice = roll_dice(player_pow, state["monster_power"],
                     luck=character.get("stats", {}).get("cognition", 0))
    outcome = dice["outcome"]
    strike_narrative = pick_narrative(
        "combat_attack", outcome,
        char=character["name"], enemy=monster["name"],
    )
    base_dmg = 4 + (player_pow // 3)
    skill_dmg = 0
    skill_status = None
    skill_used_msg = ""
    if skill_id and skill_id in SKILLS_BY_ID:
        sk = SKILLS_BY_ID[skill_id]
        if sk.get("power_type") == "strike":
            skill_dmg = sk.get("power", 0)
            skill_used_msg = f"{character['name']} unleashes {sk['name']}!"
        elif sk.get("power_type") == "heal":
            heal = int(sk.get("power", 0) * r_mods["heal_mult"])
            character["hp"] = min(character["max_hp"], character["hp"] + heal)
            skill_used_msg = f"{character['name']} casts {sk['name']} — restores {heal} HP."
        elif sk.get("power_type") == "defend":
            self_status = sk.get("self_status")
            if self_status:
                _append_status_dedup(character, make_status(self_status))
            skill_used_msg = f"{character['name']} raises {sk['name']}."
        elif sk.get("power_type") == "debuff":
            skill_dmg = sk.get("power", 0)
            skill_used_msg = f"{character['name']} uses {sk['name']}."
        if sk.get("status_apply"):
            skill_status = sk["status_apply"]
        state["skill_cooldowns"][skill_id] = sk.get("cooldown", 2)

    # damage math based on dice outcome
    dmg_mult = {1: 0.0, 2: 0.35, 3: 0.6, 4: 0.9, 5: 1.15, 6: 1.6}[outcome]
    total_dmg = int((base_dmg + skill_dmg) * dmg_mult)
    if outcome == 1:
        total_dmg = 0
    state["monster_hp"] = max(0, state["monster_hp"] - total_dmg)

    if skill_status and outcome >= 4:
        _append_status_dedup(state, make_status(skill_status), key="monster_statuses")

    # Wildblood venomous aspect passive
    if "apply_poison" in r_mods.get("extra_effects", []) and outcome >= 3:
        _append_status_dedup(state, make_status("poisoned"), key="monster_statuses")

    log.append({
        "kind": "player_strike",
        "text": strike_narrative,
        "outcome": outcome,
        "damage": total_dmg,
        "skill_id": skill_id,
        "skill_text": skill_used_msg,
    })

    # check monster death
    if state["monster_hp"] <= 0:
        state["active"] = False
        drops = []
        for drop_id, chance in monster.get("drops", []):
            if random.random() <= chance:
                drops.append((drop_id, 1))
        xp = 20 + monster["power"] * 4
        gold = 8 + monster["power"] * 2
        # racial post-victory
        victory_msgs = tick_racial_on_combat_win(character)
        for msg in victory_msgs:
            log.append({"kind": "racial", "text": msg})
        log.append({"kind": "victory",
                    "text": f"The {monster['name']} falls at {character['name']}'s hand.",
                    "drops": drops, "xp": xp, "gold": gold})
        state["turn"] = turn + 1
        state["log"].extend(log)
        return {"state": state, "log": log, "victory": True, "rewards": {"xp": xp, "gold": gold, "items": drops}}

    # -------- monster turn --------
    counter_pow = state["monster_power"]
    counter_dice = roll_dice(counter_pow, player_pow)
    c_out = counter_dice["outcome"]
    c_base = 3 + (counter_pow // 2)
    c_mult = {1: 0.0, 2: 0.4, 3: 0.7, 4: 1.0, 5: 1.2, 6: 1.6}[c_out]
    # warded status reduces damage
    warded = any(s.get("id") == "warded" for s in character.get("statuses", []))
    if warded:
        c_mult *= 0.5
    c_dmg = int(c_base * c_mult * r_mods["damage_taken_mult"])
    character["hp"] = max(0, character["hp"] - c_dmg)
    log.append({
        "kind": "enemy_strike",
        "text": f"The {monster['name']} strikes back — {c_dmg} damage.",
        "damage": c_dmg,
    })

    # tick cooldowns
    for sid in list(state["skill_cooldowns"].keys()):
        state["skill_cooldowns"][sid] = max(0, state["skill_cooldowns"][sid] - 1)
    for iid in list(state["item_cooldowns"].keys()):
        state["item_cooldowns"][iid] = max(0, state["item_cooldowns"][iid] - 1)

    # check player death
    if character["hp"] <= 0:
        state["active"] = False
        character["hp"] = 1  # brought to 1 (no permadeath in MVP)
        log.append({"kind": "defeat",
                    "text": f"{character['name']} collapses. The {monster['name']} vanishes into the shadows.",
                    "loss_gold": min(character.get("gold", 0), 20)})
        state["turn"] = turn + 1
        state["log"].extend(log)
        return {"state": state, "log": log, "victory": False, "rewards": None}

    state["turn"] = turn + 1
    state["log"].extend(log)
    return {"state": state, "log": log, "victory": None, "rewards": None}


# ============================================================
# CRAFTING
# ============================================================
def resolve_craft(character: dict, recipe_id: str) -> dict:
    recipe = RECIPES_BY_ID.get(recipe_id)
    if not recipe:
        return {"error": "Unknown recipe"}
    if character.get("level", 1) < recipe.get("min_level", 1):
        return {"error": "Level too low for this recipe"}
    if recipe.get("profession_req"):
        role = character.get("role", "")
        mastery = character.get("mastery", "")
        if role not in recipe["profession_req"] and mastery not in recipe["profession_req"]:
            return {"error": f"Requires mastery: {', '.join(recipe['profession_req'])}"}

    # check materials
    inv = {i["item_id"] if isinstance(i, dict) else i[0]: (i["quantity"] if isinstance(i, dict) else i[1])
           for i in character.get("inventory", [])}
    for mat_id, qty in recipe["materials"]:
        if inv.get(mat_id, 0) < qty:
            return {"error": f"Missing material: {mat_id} x{qty}"}

    # roll craft dice — cognition + level modifiers
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
    # outcome 1 = total failure
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
        "materials_consumed": recipe["materials"],
        "lost_materials": lost_materials,
        "output_item": output_item,
        "tier": tier,
    }
