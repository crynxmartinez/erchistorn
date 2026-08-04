"""Golden-log harness for combat_turn.

`combat_turn` is 2,270 lines with 140 mastery guard calls and 441 branches. It
cannot be refactored safely by reading it. This harness pins its *observable
behaviour* instead: for a fixed RNG seed, a scripted fight produces an exact
sequence of log entries, HP values and state transitions. Any refactor that
changes a single one of those is caught immediately.

Determinism was verified before building this: the same seed produces byte-identical
logs across runs, and different seeds diverge. `progression.py` removed the only
`random` call on the level-up path, which is what makes seeding reliable.

Usage:
    python -m tests.golden record    # write fixtures (run BEFORE refactoring)
    python -m tests.golden verify    # compare against fixtures
"""
from __future__ import annotations

import json
import os
import random
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
if os.path.join(_ROOT, "backend") not in sys.path:
    sys.path.insert(0, os.path.join(_ROOT, "backend"))

FIXTURE_DIR = os.path.join(_HERE, "fixtures")
FIXTURE_PATH = os.path.join(FIXTURE_DIR, "combat_golden.json")

# ============================================================
# Scenario definitions
# ============================================================
MELEE_GEAR = {
    "right_hand": "iron_longsword", "left_hand": "bone_shield",
    "head": "iron_helm", "body": "iron_chainmail", "legs": "iron_greaves",
    "feet": "ironshod_boots", "hands": "iron_gauntlets", "back": "iron_mantle",
}
LIGHT_GEAR = {
    "right_hand": "iron_dagger",
    "head": "sages_hood", "body": "sages_robe", "legs": "sages_trousers",
    "feet": "sages_sandals", "hands": "sages_gloves", "back": "scholars_mantle",
}

# (mastery, role, gear, level) — levels chosen to straddle passive unlock bands.
LOADOUTS = [
    ("knight", "fighter", MELEE_GEAR), ("paladin", "fighter", MELEE_GEAR),
    ("lancer", "fighter", MELEE_GEAR), ("assassin", "fighter", LIGHT_GEAR),
    ("rogue", "scout", LIGHT_GEAR), ("hunter", "scout", LIGHT_GEAR),
    ("bard", "scholar", LIGHT_GEAR), ("alchemist", "scholar", LIGHT_GEAR),
    ("mage", "scholar", LIGHT_GEAR), ("priest", "healer", LIGHT_GEAR),
    ("druid", "healer", LIGHT_GEAR),
]
LEVELS = [1, 20, 60, 100]
ACTIONS = ["strike", "defend", "evade", "aim", "counter", "focus"]
MONSTERS = ["Highway Bandit", "Crownwood Hare", "River Otter"]
SEEDS = [7, 101]
MAX_TURNS = 14


def _build(mastery: str, role: str, gear: dict, level: int):
    """Construct a character the same way character creation does."""
    import game_data as g
    import progression as p
    from items.constants import EQUIP_SLOTS

    stats = {"vitality": 5, "cognition": 3, "essence": 3, "durability": 5,
             "might": 0, "grace": 0, "insight": 0, "resilience": 0,
             "armor_bonus": 0, "magic_resist": 0, "evasion_mod": 0,
             "attack_success_mod": 0}
    equipped = {s: None for s in EQUIP_SLOTS}
    instances, inventory = [], []
    for slot, base_id in gear.items():
        base = g.BASE_ITEMS_BY_ID.get(base_id)
        if not base:
            continue
        inst = g.build_item_instance(base, [], [], quality=0, rarity="normal")
        instances.append(inst)
        equipped[slot] = inst["instance_id"]
        inventory.append({"item_id": inst["instance_id"], "quantity": 1})

    ch = {
        "name": mastery.title(), "level": 1, "xp": 0, "gold": 100,
        "mastery": mastery, "masteries": [mastery], "role": role, "race": "human",
        "base_stats": dict(stats), "stats": dict(stats),
        "equipped": equipped, "item_instances": instances, "inventory": inventory,
        "statuses": [], "item_bar": [None] * 5,
    }
    if level > 1:
        for stat, amount in p.stat_gains_for_levels(mastery, 1, level).items():
            ch["base_stats"][stat] = ch["base_stats"].get(stat, 0) + amount
    ch["level"] = level
    ch["max_hp"] = p.max_hp_for(ch["base_stats"], level)
    ch["hp"] = ch["max_hp"]

    import game_engine as ge
    ch["stats"] = ge.apply_enchantments_to_stats(ch)

    # Fill the skill bar beyond the two starting skills.
    #
    # With only two skills, cooldowns rarely bind and several mastery code paths
    # never manifest — a sabotage sweep showed changes to the Mage's cooldown
    # modifier, the Priest's sanctity multiplier and the Druid's summon cap
    # producing zero golden diffs. A fuller bar exercises cooldowns, skill
    # capacity, and every power_type the mastery owns.
    mastery_def = g.get_mastery(mastery) or {}
    starting = list(mastery_def.get("starting_skills", []))
    own = [s["id"] for s in g.SKILLS
           if mastery in (s.get("mastery_req") or [])
           or s.get("type") == mastery]
    bar = list(dict.fromkeys(starting + sorted(own)))[:10]
    ch["skills"] = [{"skill_id": s, "cooldown_remaining": 0} for s in bar]
    ch["skill_bar"] = bar + [None] * (10 - len(bar))
    if mastery == "rogue":
        ch["rogue_innate_equipped"] = [s["id"] for s in g.ROGUE_INNATE_SKILLS[:5]]
    if mastery == "mage":
        # One passive per school rather than the first five in data order, which
        # were all Elements and left Temporal/Spatial/Mental paths unexercised.
        by_school = {}
        for p2 in g.MAGE_PASSIVES:
            if p2.get("planned"):
                continue
            by_school.setdefault(p2["school"], p2["id"])
        preferred = ["quickened_mind", "mind_control", "long_range",
                     "true_strike", "frostfire"]
        chosen = [pid for pid in preferred
                  if any(p2["id"] == pid and not p2.get("planned") for p2 in g.MAGE_PASSIVES)]
        for pid in by_school.values():
            if pid not in chosen and len(chosen) < 5:
                chosen.append(pid)
        ch["mage_equipped_passives"] = chosen[:5]
    return ch


def _canonical(obj):
    """Normalise a value so comparison is stable across runs."""
    if isinstance(obj, dict):
        return {k: _canonical(v) for k, v in sorted(obj.items())}
    if isinstance(obj, (list, tuple)):
        return [_canonical(v) for v in obj]
    if isinstance(obj, float):
        return round(obj, 6)
    if isinstance(obj, (str, int, bool)) or obj is None:
        return obj
    return str(obj)


# State keys worth pinning: the mastery resource meters. If a refactor drops one,
# the mastery silently stops working, and the log alone might not show it.
TRACKED_STATE = [
    "turn", "monster_hp", "combo_count", "skill_capacity_used",
    "knight_oath_stacks", "knight_oath",
    "paladin_faith_tier", "paladin_bonus_armor",
    "lancer_imbues", "assassin_shadows", "assassin_fear_deposited",
    "hunter_spirit_guidance", "hunter_range", "player_range", "monster_range",
    "bard_crescendo", "bard_mode", "bard_active_performances",
    "alchemist_cf", "alchemist_imbue_charges",
    "mage_arcane_focus", "mage_echo_next_turn",
    "priest_hot_buffs", "priest_smite_active",
    "druid_active_summons", "druid_active_form",
    "generic_self_stat_mods", "player_statuses", "monster_statuses",
]


def _activate_resources(mastery: str, ch: dict, state: dict) -> None:
    """Engage each mastery's resource system so its code paths actually run.

    Without this the harness has a real blind spot. Verified by sabotage: changing
    the Knight's starting Oath stacks from 2 to 3 produced ZERO golden diffs,
    because `state["knight_oath"]` was never set and the whole Oath branch was
    dead in every scenario. A safety net that cannot fail is worthless, so each
    mastery is now switched on explicitly.
    """
    import game_data as g
    import game_engine as ge

    if mastery == "knight":
        state["knight_oath"] = "iron"          # any Oath engages the stack machinery
    elif mastery == "bard":
        state["bard_mode"] = "song"
    elif mastery == "alchemist":
        imbue = next((s for s in g.SKILLS
                      if s.get("power_type") == "imbue"
                      and "alchemist" in (s.get("mastery_req") or [])), None)
        if imbue:
            state["alchemist_pre_imbue"] = imbue["id"]
    elif mastery == "druid":
        # Summon the first bestiary-shaped creature so summon/pack/fusion paths run.
        entry = next((m for m in g.MONSTERS
                      if m.get("profile_skills") and m.get("rarity") == "common"), None)
        if entry:
            try:
                ge._druid_summon_creature(ch, state, entry, [])
            except Exception:
                pass  # summon preconditions vary by level; not worth failing the scenario


def run_scenario(mastery, role, gear, level, monster_name, action, seed):
    """Execute one scripted fight and return a canonical trace."""
    import game_data as g
    import game_engine as ge

    monster = next((m for m in g.MONSTERS if m["name"] == monster_name), None)
    if monster is None:
        return None

    random.seed(seed)
    ch = _build(mastery, role, gear, level)
    state = ge.start_combat(ch, monster["id"])
    if "error" in state:
        return None
    _activate_resources(mastery, ch, state)

    trace = []
    for _ in range(MAX_TURNS):
        result = ge.combat_turn(ch, state, action_type=action)
        if "error" in result:
            trace.append({"error": result["error"]})
            break
        snapshot = {
            "log": [
                {"kind": e.get("kind"), "text": e.get("text"),
                 "damage": e.get("damage"), "outcome": e.get("outcome")}
                for e in result.get("log", [])
            ],
            "hp": ch.get("hp"),
            "victory": result.get("victory"),
            "state": {k: state.get(k) for k in TRACKED_STATE if k in state},
        }
        trace.append(_canonical(snapshot))
        if result.get("victory") is not None or not state.get("active"):
            break
    return trace


def build_all():
    """Every scenario, keyed by a stable id."""
    out = {}
    for mastery, role, gear in LOADOUTS:
        for level in LEVELS:
            for monster in MONSTERS:
                for action in ACTIONS:
                    for seed in SEEDS:
                        key = f"{mastery}|L{level}|{monster}|{action}|s{seed}"
                        trace = run_scenario(mastery, role, gear, level,
                                             monster, action, seed)
                        if trace is not None:
                            out[key] = trace
    return out


def _digest(trace) -> str:
    import hashlib
    blob = json.dumps(trace, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()[:32]


def build_hashes():
    """Scenario id -> (turn_count, digest). Committed instead of full traces: the
    full traces are ~21 MB, which does not belong in git. A digest still catches
    any behavioural change; `diff <scenario>` replays one scenario in full when
    something breaks."""
    return {k: [len(v), _digest(v)] for k, v in build_all().items()}


def record():
    os.makedirs(FIXTURE_DIR, exist_ok=True)
    data = build_hashes()
    with open(FIXTURE_PATH, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=0, sort_keys=True)
    size = os.path.getsize(FIXTURE_PATH) / 1024
    print(f"recorded {len(data)} scenario digests -> {FIXTURE_PATH} ({size:.0f} KB)")
    return 0


def verify(verbose=True):
    if not os.path.exists(FIXTURE_PATH):
        print("no fixtures — run `python -m tests.golden record` first")
        return 1
    with open(FIXTURE_PATH, encoding="utf-8") as fh:
        expected = json.load(fh)
    actual = build_hashes()

    missing = sorted(set(expected) - set(actual))
    added = sorted(set(actual) - set(expected))
    changed = [k for k in sorted(set(expected) & set(actual))
               if expected[k] != actual[k]]

    if verbose:
        print(f"scenarios: {len(expected)} expected / {len(actual)} actual")
        print(f"  missing: {len(missing)}  added: {len(added)}  changed: {len(changed)}")
        for k in changed[:10]:
            exp_turns, _ = expected[k]
            act_turns, _ = actual[k]
            note = "" if exp_turns == act_turns else f" (turns {exp_turns} -> {act_turns})"
            print(f"    CHANGED {k}{note}")
        if changed:
            print(f"\n  replay one in full with:  python -m tests.golden diff \"{changed[0]}\"")
    ok = not (missing or added or changed)
    if verbose:
        print("\nGOLDEN LOGS IDENTICAL" if ok else "\nGOLDEN LOGS DIVERGED")
    return 0 if ok else 1


def diff(key: str):
    """Replay a single scenario and dump its trace, for diagnosing a divergence."""
    parts = key.split("|")
    if len(parts) != 5:
        print("key must look like: knight|L20|Highway Bandit|strike|s7")
        return 1
    mastery, level_s, monster, action, seed_s = parts
    loadout = next((l for l in LOADOUTS if l[0] == mastery), None)
    if not loadout:
        print(f"unknown mastery {mastery}")
        return 1
    trace = run_scenario(loadout[0], loadout[1], loadout[2],
                         int(level_s.lstrip("L")), monster, action,
                         int(seed_s.lstrip("s")))
    print(json.dumps(trace, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "verify"
    if cmd == "record":
        sys.exit(record())
    if cmd == "diff":
        sys.exit(diff(sys.argv[2] if len(sys.argv) > 2 else ""))
    sys.exit(verify())
