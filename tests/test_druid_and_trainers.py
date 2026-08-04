"""Druid skill kit + trainer reachability.

Two gaps, both found by comparing shipped data against the design docs:

1. The Druid had **2 of its 30 spec'd skills** implemented, while having the most
   elaborate engine support of any mastery (summons, fusion, pack synergy, 15
   helpers). It was the least playable mastery in the game.

2. The canon v2 rename remapped continent/biome/town ids and migrated every
   character record, but **`TEACHERS` was never migrated**. 48 of 53 skill
   teachers pointed at towns that no longer exist, and because
   `/game/data/teachers` filters by `town_id`, visiting a real town surfaced
   almost no trainers — skill learning was unreachable for most masteries.
"""
from __future__ import annotations

import pytest


MASTERIES_WITH_DOCS = ["knight", "paladin", "lancer", "rogue", "bard", "alchemist",
                       "mage", "priest", "druid", "assassin", "hunter"]


# ============================================================
# Druid skill kit
# ============================================================

def test_druid_has_a_full_skill_kit(gd):
    druid = [s for s in gd.SKILLS if s.get("type") == "druid"]
    assert len(druid) >= 30, f"Druid has only {len(druid)} skills (spec calls for 30)"


def test_every_mastery_has_a_comparable_skill_count(gd):
    """No mastery should be an order of magnitude behind the others."""
    from collections import Counter
    counts = Counter(s.get("type") for s in gd.SKILLS if s.get("type") in MASTERIES_WITH_DOCS)
    # alchemist skills are typed imbuable/cast/strike, so it is excluded here and
    # covered by test_alchemist_skills_exist below.
    checked = {m: counts.get(m, 0) for m in MASTERIES_WITH_DOCS if m != "alchemist"}
    thin = {m: n for m, n in checked.items() if n < 25}
    assert not thin, f"masteries with a thin skill kit: {thin}"


def test_alchemist_skills_exist(gd):
    """Alchemist skills use type imbuable/cast/strike rather than 'alchemist'."""
    alch_types = {"imbuable", "cast", "strike"}
    n = sum(1 for s in gd.SKILLS if s.get("type") in alch_types)
    assert n >= 25, f"only {n} alchemist-shaped skills found"


def test_druid_skills_are_well_formed(gd):
    druid = [s for s in gd.SKILLS if s.get("type") == "druid"]
    required = ("id", "name", "power_type", "cooldown", "rarity",
                "level_req", "cost_gold", "learn_seconds", "desc")
    for s in druid:
        for field in required:
            assert field in s, f"druid skill {s.get('id')} missing {field}"
        assert s["rarity"] in gd.RARITY_COST, f"{s['id']} has unknown rarity {s['rarity']}"


def test_druid_damage_scales_with_rarity(gd):
    """A legendary strike must hit harder than a common one."""
    strikes = [s for s in gd.SKILLS
               if s.get("type") == "druid" and s.get("power_type") == "strike"]
    by_rarity = {}
    for s in strikes:
        by_rarity.setdefault(s["rarity"], []).append(s["damage"])
    order = [r for r in ("common", "uncommon", "rare", "epic", "legendary") if r in by_rarity]
    maxima = [max(by_rarity[r]) for r in order]
    assert maxima == sorted(maxima), f"druid strike damage not ordered by rarity: {dict(zip(order, maxima))}"


def test_druid_skills_are_in_the_lookup_table(gd):
    druid = [s for s in gd.SKILLS if s.get("type") == "druid"]
    for s in druid:
        assert gd.SKILLS_BY_ID.get(s["id"]) is not None, f"{s['id']} missing from SKILLS_BY_ID"


def test_no_duplicate_skill_ids(gd):
    from collections import Counter
    dupes = [sid for sid, n in Counter(s["id"] for s in gd.SKILLS).items() if n > 1]
    assert not dupes, f"duplicate skill ids: {dupes}"


# ============================================================
# Trainer reachability
# ============================================================

def test_every_teacher_is_in_a_real_town(gd):
    import game_data_p2 as p2
    towns = {t["id"] for t in p2.TOWNS}
    orphans = [(t["id"], t["town_id"]) for t in gd.TEACHERS if t["town_id"] not in towns]
    assert not orphans, f"{len(orphans)} teachers in non-existent towns: {orphans[:8]}"


def test_every_teacher_is_on_a_real_continent(gd):
    conts = {c["id"] for c in gd.CONTINENTS}
    orphans = [(t["id"], t["continent_id"]) for t in gd.TEACHERS
               if t["continent_id"] not in conts]
    assert not orphans, f"{len(orphans)} teachers on non-existent continents: {orphans[:8]}"


def test_every_teacher_teaches_real_skills(gd):
    bad = []
    for t in gd.TEACHERS:
        for sid in (t.get("teaches") or []):
            if sid not in gd.SKILLS_BY_ID:
                bad.append((t["id"], sid))
    assert not bad, f"teachers offering unknown skills: {bad[:10]}"


def test_druid_skills_are_learnable_from_a_trainer(gd):
    """A skill nobody teaches is unreachable content."""
    druid = {s["id"] for s in gd.SKILLS if s.get("type") == "druid"}
    taught = set()
    for t in gd.TEACHERS:
        taught |= set(t.get("teaches") or [])
    unreachable = sorted(druid - taught)
    assert not unreachable, f"druid skills no trainer teaches: {unreachable}"


@pytest.mark.parametrize("mastery", ["knight", "mage", "priest", "druid",
                                     "paladin", "lancer", "assassin", "bard",
                                     "hunter", "rogue"])
def test_each_mastery_has_at_least_one_reachable_trainer(gd, mastery):
    import game_data_p2 as p2
    towns = {t["id"] for t in p2.TOWNS}
    trainers = [t for t in gd.TEACHERS
                if t.get("mastery_focus") == mastery and t["town_id"] in towns]
    assert trainers, f"{mastery} has no trainer in any real town"


def test_no_teacher_has_an_obsolete_mastery_focus(gd):
    """Four teachers carried focuses from an earlier class list (berserker, tank,
    ranger, saint) that are not masteries in the game."""
    real = {m["id"] for m in gd.MASTERIES}
    bad = [(t["id"], t.get("mastery_focus")) for t in gd.TEACHERS
           if t.get("mastery_focus") not in real]
    assert not bad, f"teachers with a non-existent mastery_focus: {bad}"


def test_every_mastery_has_a_trainer(gd):
    """The Rogue had no trainer at all — 30 skills with no way to learn them."""
    real = {m["id"] for m in gd.MASTERIES}
    focuses = {t.get("mastery_focus") for t in gd.TEACHERS}
    assert not (real - focuses), f"masteries with no trainer: {sorted(real - focuses)}"


@pytest.mark.parametrize("mastery", ["druid", "rogue", "knight", "mage", "priest"])
def test_mastery_skills_are_fully_learnable(gd, mastery):
    own = {s["id"] for s in gd.SKILLS if s.get("type") == mastery}
    if not own:
        pytest.skip(f"{mastery} skills are not typed by mastery name")
    taught = set()
    for t in gd.TEACHERS:
        taught |= set(t.get("teaches") or [])
    unreachable = sorted(own - taught)
    assert not unreachable, f"{mastery} skills no trainer teaches: {unreachable[:8]}"


# ============================================================
# Race / role / mastery reachability
# ============================================================

def test_every_advertised_race_mastery_is_reachable(gd):
    """A race listing a mastery no role it can take allows is dead content.

    Found by creating a character for every race x mastery combination over HTTP:
    dwarf+alchemist, orc+hunter and orc+alchemist were all advertised and all
    impossible, because Alchemist needs scholar/healer and Hunter needs scout while
    both races can only be fighter or guardian.
    """
    from origins import ROLE_AVAILABLE_MASTERIES
    unreachable = []
    for race in gd.RACES:
        for mastery in race.get("masteries", []):
            if not any(mastery in ROLE_AVAILABLE_MASTERIES.get(role, [])
                       for role in race.get("roles", [])):
                unreachable.append(f"{race['id']}+{mastery}")
    assert not unreachable, (
        "race/mastery combinations that can never be created: "
        f"{unreachable}. Either remove the mastery from the race, add a role to "
        "the race, or widen ROLE_AVAILABLE_MASTERIES."
    )


def test_every_race_can_reach_at_least_one_mastery(gd):
    from origins import ROLE_AVAILABLE_MASTERIES
    stranded = []
    for race in gd.RACES:
        reachable = [m for m in race.get("masteries", [])
                     if any(m in ROLE_AVAILABLE_MASTERIES.get(r, [])
                            for r in race.get("roles", []))]
        if not reachable:
            stranded.append(race["id"])
    assert not stranded, f"races with no playable mastery: {stranded}"


def test_every_mastery_is_reachable_by_some_race(gd):
    """A mastery no race can reach is unplayable content."""
    from origins import ROLE_AVAILABLE_MASTERIES
    playable = set()
    for race in gd.RACES:
        for m in race.get("masteries", []):
            if any(m in ROLE_AVAILABLE_MASTERIES.get(r, [])
                   for r in race.get("roles", [])):
                playable.add(m)
    missing = sorted({m["id"] for m in gd.MASTERIES} - playable)
    assert not missing, f"masteries no race can play: {missing}"
