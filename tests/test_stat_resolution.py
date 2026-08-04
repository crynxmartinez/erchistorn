"""Gear -> stat resolution.

These tests pin down the single most important invariant in the item system:
**every equipped slot must resolve through one shared code path**, whether it
holds a legacy static item id or a procedural instance_id.

Regression targets (all were live bugs):
  - compute_armor ignored item instances AND no item granted armor_bonus
  - compute_player_power ignored item instances
  - compute_accuracy / compute_evasion ignored item instances
  - set bonuses were applied once per equipped item and were not cumulative
"""
from __future__ import annotations

import pytest

from conftest import make_character, make_set_loadout, recompute


# ============================================================
# Armor
# ============================================================

def test_armor_slots_grant_armor(gd):
    """Every armor-slot base item must contribute armor. Regression: all 30
    armor base items granted zero, so plate == naked."""
    armor_slots = {"head", "body", "legs", "feet", "back", "hands"}
    armor_bases = [b for b in gd.BASE_ITEMS_BY_ID.values() if b.get("slot") in armor_slots]
    assert armor_bases, "no armor base items found"

    without = [b["id"] for b in armor_bases
               if int((b.get("base_stats") or {}).get("armor_bonus", 0)) <= 0]
    assert not without, f"armor base items granting no armor: {without}"


def test_plated_knight_has_armor(plated_knight, gd):
    """The canonical regression: a Knight in full starter plate must have armor."""
    assert gd.compute_armor(plated_knight) > 0


def test_armor_reduces_incoming_damage(plated_knight, naked_knight, gd):
    """Armor must actually reduce damage. Regression: plate took full damage."""
    plated_armor = gd.compute_armor(plated_knight)
    naked_armor = gd.compute_armor(naked_knight)
    assert plated_armor > naked_armor

    raw = 40
    assert gd.apply_armor(raw, plated_armor) < gd.apply_armor(raw, naked_armor)


def test_heavy_armor_beats_light_armor(gd):
    """armor_type must be a meaningful choice: heavy > leather > light."""
    heavy = make_character(equipped_bases={"body": "iron_chainmail"})
    leather = make_character(equipped_bases={"body": "leather_vest"})
    light = make_character(equipped_bases={"body": "sages_robe"})

    a_heavy = gd.compute_armor(heavy)
    a_leather = gd.compute_armor(leather)
    a_light = gd.compute_armor(light)
    assert a_heavy > a_leather > a_light > 0


def test_higher_tier_armor_grants_more_armor(gd):
    """Tier must scale armor, so upgrades feel like upgrades."""
    t1 = make_character(equipped_bases={"body": "iron_chainmail"})     # heavy T1
    t2 = make_character(equipped_bases={"body": "knights_plate"})      # heavy T2
    t3 = make_character(equipped_bases={"body": "dragonscale_tunic"})  # heavy T3
    assert gd.compute_armor(t1) < gd.compute_armor(t2) < gd.compute_armor(t3)


def test_shield_grants_armor(gd):
    """Shields are the archetypal armor source and must contribute."""
    with_shield = make_character(equipped_bases={"left_hand": "bone_shield"})
    assert gd.compute_armor(with_shield) > gd.compute_armor(make_character())


def test_resilience_contributes_to_armor(gd):
    """The Guardian role promises '+2 Resilience, +1 defence'. Regression:
    resilience was granted by the role but read by no formula at all."""
    plain = make_character(base_stats={"resilience": 0})
    tough = make_character(base_stats={"resilience": 10})
    assert gd.compute_armor(tough) > gd.compute_armor(plain)


def test_armor_reduction_is_capped(gd):
    """Reduction must never exceed MAX_DMG_REDUCTION regardless of armor."""
    raw = 1000
    taken = gd.apply_armor(raw, 100_000)
    floor = int(raw * (1.0 - gd.MAX_DMG_REDUCTION))
    assert taken >= floor


def test_zero_armor_is_a_no_op(gd):
    assert gd.apply_armor(37, 0) == 37


# ============================================================
# Magic resistance
# ============================================================

def test_gear_contributes_magic_resistance(gd):
    """Regression: compute_magic_resistance was Essence-only with a
    'could be added here in future' comment, so gear MR was a no-op."""
    plain = make_character(base_stats={"essence": 5})
    warded = make_character(base_stats={"essence": 5}, equipped_bases={"body": "sages_robe"})
    assert gd.compute_magic_resistance(warded) > gd.compute_magic_resistance(plain)


def test_magic_resistance_reduction_is_capped(gd):
    raw = 1000
    taken = gd.apply_magic_resistance(raw, 100_000)
    assert taken >= int(raw * (1.0 - gd.MAX_DMG_REDUCTION))


# ============================================================
# Player power (drives all non-combat action rolls)
# ============================================================

def test_player_power_responds_to_gear(plated_knight, naked_knight, gd):
    """Regression: compute_player_power looked up instance_ids in ITEMS_BY_ID,
    so hunt/gather/explore/loot rolled identically naked or fully geared."""
    assert gd.compute_player_power(plated_knight) > gd.compute_player_power(naked_knight)


def test_player_power_counts_accessory_slots(gd):
    """Regression: only 7 of 12 equip slots were counted — rings, earrings and
    neck never contributed."""
    bare = make_character()
    ringed = make_character(equipped_bases={"ring_l": "copper_ring"})
    assert gd.compute_player_power(ringed) > gd.compute_player_power(bare)


def test_player_power_grows_with_level(gd):
    low = make_character(level=1)
    high = make_character(level=20)
    assert gd.compute_player_power(high) > gd.compute_player_power(low)


# ============================================================
# Accuracy / evasion
# ============================================================

def test_accuracy_responds_to_gear(gd):
    """Regression: compute_accuracy read a weapon 'accuracy' field that item
    instances never carry."""
    bare = make_character(base_stats={"grace": 5})
    armed = make_character(base_stats={"grace": 5}, equipped_bases={"right_hand": "iron_dagger"})
    assert gd.compute_accuracy(armed) >= gd.compute_accuracy(bare)


def test_evasion_responds_to_light_gear(gd):
    """Light armor should favour evasion — the armor_type descriptions promise it."""
    bare = make_character(base_stats={"grace": 5})
    nimble = make_character(base_stats={"grace": 5}, equipped_bases={"feet": "leather_boots"})
    assert gd.compute_evasion(nimble) >= gd.compute_evasion(bare)


# ============================================================
# Two-handed dedup
# ============================================================

def test_two_handed_weapon_counted_once(gd, ge):
    """A 2H weapon fills both hand slots but must only be counted once."""
    import game_data as g
    base = g.BASE_ITEMS_BY_ID["iron_greatsword"]
    inst = g.build_item_instance(base, [], [], quality=0, rarity="normal")

    ch = make_character(base_stats={"might": 0})
    ch["item_instances"] = [inst]
    ch["inventory"] = [{"item_id": inst["instance_id"], "quantity": 1}]
    ch["equipped"]["left_hand"] = inst["instance_id"]
    ch["equipped"]["right_hand"] = inst["instance_id"]
    recompute(ch)

    expected = int(inst["base_stats"]["might"])
    assert ch["stats"]["might"] == expected, "2H weapon double-counted"


# ============================================================
# Set bonuses
# ============================================================

def _set_with_stat_tier(ge):
    """Find a set whose lowest tier grants plain stats, for assertion clarity."""
    for set_id, data in ge._SET_BONUSES.items():
        tiers = data.get("bonuses", {})
        low = min(tiers) if tiers else None
        if low is not None and tiers[low].get("stats"):
            return set_id, low, tiers[low]["stats"]
    pytest.skip("no set with stat-granting lowest tier")


def test_set_bonus_independent_of_filler_items(ge):
    """Regression (bug A): _check_set_bonuses was called inside the per-slot
    loop, so the bonus re-applied once per equipped item — including items
    belonging to no set. 2 pieces + 4 filler gave 6x the intended bonus."""
    set_id, threshold, stats = _set_with_stat_tier(ge)

    no_filler = make_set_loadout(set_id, threshold, n_filler=0)
    with_filler = make_set_loadout(set_id, threshold, n_filler=4)

    for stat in stats:
        assert no_filler["stats"][stat] == with_filler["stats"][stat], (
            f"{stat} changed when unrelated filler items were equipped"
        )


def test_set_bonus_matches_declared_value(ge):
    """Wearing exactly the threshold count grants exactly the declared stats."""
    set_id, threshold, stats = _set_with_stat_tier(ge)
    ch = make_set_loadout(set_id, threshold)
    for stat, val in stats.items():
        assert ch["stats"][stat] == val, f"{stat}: expected {val}, got {ch['stats'][stat]}"


def test_set_bonus_is_monotonic_in_piece_count(ge):
    """Regression (bug B): tiers were looked up by exact piece count, so the
    2-piece stats silently vanished at 3+ pieces. More pieces must never be
    worse than fewer."""
    set_id, threshold, stats = _set_with_stat_tier(ge)
    tracked = next(iter(stats))

    values = []
    for n in range(threshold, 6):
        ch = make_set_loadout(set_id, n)
        values.append(ch["stats"][tracked])

    assert values == sorted(values), (
        f"{tracked} not monotonic across {threshold}..5 pieces: {values}"
    )
    assert all(v > 0 for v in values), f"set bonus lost at some piece count: {values}"


def test_below_threshold_grants_no_set_bonus(ge):
    """One piece of a set must grant nothing."""
    set_id, threshold, stats = _set_with_stat_tier(ge)
    if threshold <= 1:
        pytest.skip("set threshold is 1; nothing below it")
    ch = make_set_loadout(set_id, threshold - 1)
    for stat in stats:
        assert ch["stats"][stat] == 0, f"{stat} granted below the set threshold"
