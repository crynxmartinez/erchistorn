"""Unit tests for the Resolve system — pure function tests, no server needed.

Run: python -m pytest test_resolve.py -v
Or:  python test_resolve.py
"""
import sys
import os
from pathlib import Path
from datetime import datetime, timezone, timedelta

# Ensure backend dir is on path
sys.path.insert(0, str(Path(__file__).parent))

from game_engine import (
    _tick_resolve, _resolve_tier, _resolve_multiplier,
    _resolve_study_buff_hours, _resolve_combat_damage_mod,
    _resolve_expedition_mod, _resolve_combat_gain, _award_resolve,
    _resolve_fields,
    RESOLVE_FLOOR, RESOLVE_RESTED, RESOLVE_DEMORALIZED,
    RESOLVE_FOCUSED, RESOLVE_PEAK,
    REGEN_PER_HOUR, DECAY_PER_HOUR,
)

passed = 0
failed = 0


def check(label, condition, detail=""):
    global passed, failed
    if condition:
        print(f"  ✅ {label}")
        passed += 1
    else:
        print(f"  ❌ {label} — {detail}")
        failed += 1


def make_ch(resolve=50, last_update=None):
    ch = {"resolve": resolve}
    if last_update is not None:
        ch["last_resolve_update"] = last_update
    else:
        ch["last_resolve_update"] = datetime.now(timezone.utc).isoformat()
    return ch


# ============================================================
# 1. _tick_resolve — boundaries and time progression
# ============================================================
print("\n" + "=" * 60)
print("  _tick_resolve — boundaries & time")
print("=" * 60)

# Below floor: regenerates toward 50
ch = make_ch(resolve=10, last_update=(datetime.now(timezone.utc) - timedelta(hours=5)).isoformat())
_tick_resolve(ch)
check("Below floor regen 5h: 10 -> 20", ch["resolve"] == 20, f"got {ch['resolve']}")

# Regen caps at floor (50)
ch = make_ch(resolve=40, last_update=(datetime.now(timezone.utc) - timedelta(hours=10)).isoformat())
_tick_resolve(ch)
check("Regen caps at 50", ch["resolve"] == 50, f"got {ch['resolve']}")

# Equilibrium band 50-65: no change
ch = make_ch(resolve=55, last_update=(datetime.now(timezone.utc) - timedelta(hours=3)).isoformat())
_tick_resolve(ch)
check("Equilibrium 55 stays 55", ch["resolve"] == 55, f"got {ch['resolve']}")

ch = make_ch(resolve=50, last_update=(datetime.now(timezone.utc) - timedelta(hours=48)).isoformat())
_tick_resolve(ch)
check("Equilibrium 50 stays 50 (48h)", ch["resolve"] == 50, f"got {ch['resolve']}")

# Above rested: decays toward 65
ch = make_ch(resolve=90, last_update=(datetime.now(timezone.utc) - timedelta(hours=10)).isoformat())
_tick_resolve(ch)
check("Decay 90 -> 80 (10h)", ch["resolve"] == 80, f"got {ch['resolve']}")

# Decay floors at 65
ch = make_ch(resolve=70, last_update=(datetime.now(timezone.utc) - timedelta(hours=100)).isoformat())
_tick_resolve(ch)
check("Decay floors at 65", ch["resolve"] == 65, f"got {ch['resolve']}")

# 0 hours: no change
ch = make_ch(resolve=30, last_update=datetime.now(timezone.utc).isoformat())
_tick_resolve(ch)
check("0 hours = no change", ch["resolve"] == 30, f"got {ch['resolve']}")

# 1 hour
ch = make_ch(resolve=20, last_update=(datetime.now(timezone.utc) - timedelta(hours=1)).isoformat())
_tick_resolve(ch)
check("1 hour regen: 20 -> 22", ch["resolve"] == 22, f"got {ch['resolve']}")


# ============================================================
# 2. Remainder preservation
# ============================================================
print("\n" + "=" * 60)
print("  Remainder preservation")
print("=" * 60)

start = datetime.now(timezone.utc) - timedelta(hours=1, minutes=54)  # 1.9h
ch = make_ch(resolve=20, last_update=start.isoformat())
_tick_resolve(ch)
expected_ts = start + timedelta(hours=1)
actual_ts = datetime.fromisoformat(ch["last_resolve_update"])
if actual_ts.tzinfo is None:
    actual_ts = actual_ts.replace(tzinfo=timezone.utc)
diff = abs((actual_ts - expected_ts).total_seconds())
check("Timestamp advances by exactly 1h", diff < 1, f"diff={diff}s")
check("Resolve advanced by 1 hour only", ch["resolve"] == 22, f"got {ch['resolve']}")


# ============================================================
# 3. Idempotence — two ticks 1 second apart
# ============================================================
print("\n" + "=" * 60)
print("  Idempotence")
print("=" * 60)

ch = make_ch(resolve=30, last_update=(datetime.now(timezone.utc) - timedelta(seconds=5)).isoformat())
_tick_resolve(ch)
r1 = ch["resolve"]
_tick_resolve(ch)
check("Two ticks 5s apart = no change", ch["resolve"] == r1, f"{r1} -> {ch['resolve']}")


# ============================================================
# 4. Clamping at 0 and 100
# ============================================================
print("\n" + "=" * 60)
print("  Clamping")
print("=" * 60)

ch = make_ch(resolve=5)
_award_resolve(ch, -100, "test")
check("Clamp to 0", ch["resolve"] == 0, f"got {ch['resolve']}")

ch = make_ch(resolve=95)
_award_resolve(ch, 100, "test")
check("Clamp to 100", ch["resolve"] == 100, f"got {ch['resolve']}")

ch = make_ch(resolve=50)
_award_resolve(ch, -5, "test")
check("Award -5 from 50 = 45", ch["resolve"] == 45, f"got {ch['resolve']}")

ch = make_ch(resolve=50)
_award_resolve(ch, 10, "test")
check("Award +10 from 50 = 60", ch["resolve"] == 60, f"got {ch['resolve']}")


# ============================================================
# 5. Tier names
# ============================================================
print("\n" + "=" * 60)
print("  Tier names")
print("=" * 60)

check("Tier 0 = Demoralized", _resolve_tier(make_ch(resolve=0)) == "Demoralized")
check("Tier 24 = Demoralized", _resolve_tier(make_ch(resolve=24)) == "Demoralized")
check("Tier 25 = Stable", _resolve_tier(make_ch(resolve=25)) == "Stable")
check("Tier 50 = Stable", _resolve_tier(make_ch(resolve=50)) == "Stable")
check("Tier 64 = Stable", _resolve_tier(make_ch(resolve=64)) == "Stable")
check("Tier 65 = Focused", _resolve_tier(make_ch(resolve=65)) == "Focused")
check("Tier 84 = Focused", _resolve_tier(make_ch(resolve=84)) == "Focused")
check("Tier 85 = Peak", _resolve_tier(make_ch(resolve=85)) == "Peak")
check("Tier 100 = Peak", _resolve_tier(make_ch(resolve=100)) == "Peak")


# ============================================================
# 6. Multiplier boundaries
# ============================================================
print("\n" + "=" * 60)
print("  Multiplier boundaries")
print("=" * 60)

check("Train mult 24 = 0.75", _resolve_multiplier(make_ch(resolve=24)) == 0.75)
check("Train mult 25 = 1.0", _resolve_multiplier(make_ch(resolve=25)) == 1.0)
check("Train mult 64 = 1.0", _resolve_multiplier(make_ch(resolve=64)) == 1.0)
check("Train mult 65 = 1.10", _resolve_multiplier(make_ch(resolve=65)) == 1.10)
check("Train mult 84 = 1.10", _resolve_multiplier(make_ch(resolve=84)) == 1.10)
check("Train mult 85 = 1.25", _resolve_multiplier(make_ch(resolve=85)) == 1.25)
check("Train mult 100 = 1.25", _resolve_multiplier(make_ch(resolve=100)) == 1.25)


# ============================================================
# 7. Combat damage mod
# ============================================================
print("\n" + "=" * 60)
print("  Combat damage mod")
print("=" * 60)

check("Dmg mod 20 = 0.90", _resolve_combat_damage_mod(make_ch(resolve=20)) == 0.90)
check("Dmg mod 24 = 0.90", _resolve_combat_damage_mod(make_ch(resolve=24)) == 0.90)
check("Dmg mod 25 = 1.0", _resolve_combat_damage_mod(make_ch(resolve=25)) == 1.0)
check("Dmg mod 50 = 1.0", _resolve_combat_damage_mod(make_ch(resolve=50)) == 1.0)
check("Dmg mod 84 = 1.0", _resolve_combat_damage_mod(make_ch(resolve=84)) == 1.0)
check("Dmg mod 85 = 1.05", _resolve_combat_damage_mod(make_ch(resolve=85)) == 1.05)
check("Dmg mod 90 = 1.05", _resolve_combat_damage_mod(make_ch(resolve=90)) == 1.05)


# ============================================================
# 8. Study buff hours
# ============================================================
print("\n" + "=" * 60)
print("  Study buff hours")
print("=" * 60)

check("Study 20 = 1.5h (3*0.5)", _resolve_study_buff_hours(make_ch(resolve=20), 3.0) == 1.5)
check("Study 50 = 3.0h", _resolve_study_buff_hours(make_ch(resolve=50), 3.0) == 3.0)
check("Study 65 = 4.0h (3+1)", _resolve_study_buff_hours(make_ch(resolve=65), 3.0) == 4.0)
check("Study 85 = 5.0h (3+2)", _resolve_study_buff_hours(make_ch(resolve=85), 3.0) == 5.0)


# ============================================================
# 9. Expedition mod
# ============================================================
print("\n" + "=" * 60)
print("  Expedition mod")
print("=" * 60)

mod20 = _resolve_expedition_mod(make_ch(resolve=20))
mod50 = _resolve_expedition_mod(make_ch(resolve=50))
mod70 = _resolve_expedition_mod(make_ch(resolve=70))
mod90 = _resolve_expedition_mod(make_ch(resolve=90))

check("Exped 20 yield=0.85", mod20["yield_mult"] == 0.85)
check("Exped 20 poor=0.05", mod20["poor_chance"] == 0.05)
check("Exped 50 yield=1.0", mod50["yield_mult"] == 1.0)
check("Exped 70 yield=1.10", mod70["yield_mult"] == 1.10)
check("Exped 70 good=0.05", mod70["good_chance"] == 0.05)
check("Exped 90 yield=1.20", mod90["yield_mult"] == 1.20)
check("Exped 90 good=0.10", mod90["good_chance"] == 0.10)


# ============================================================
# 10. Combat gain — threat ratio buckets
# ============================================================
print("\n" + "=" * 60)
print("  Combat gain — threat ratio buckets")
print("=" * 60)

# Use a minimal character with known stats
# compute_action_rating uses stats — we need enough to get a rating > 0
ch_low = {"resolve": 50, "stats": {"might": 10, "grace": 10, "insight": 10, "vitality": 10, "essence": 10, "armor": 0},
          "level": 1, "equipped": {}}
ch_high = {"resolve": 50, "stats": {"might": 100, "grace": 100, "insight": 100, "vitality": 100, "essence": 100, "armor": 50},
           "level": 50, "equipped": {}}

# Low-level character vs high threat (boss) -> ratio >= 1.0 -> +3
gain_boss = _resolve_combat_gain(ch_low, 100)
check("L1 vs threat 100 -> +3", gain_boss == 3, f"got {gain_boss}")

# Low-level character vs trivial (threat 1) -> ratio < 0.10 -> +0
gain_trivial = _resolve_combat_gain(ch_low, 1)
check("L1 vs threat 1 -> +0 (trivial)", gain_trivial == 0, f"got {gain_trivial}")

# High-level character vs low threat -> ratio < 0.10 -> +0
gain_high_trivial = _resolve_combat_gain(ch_high, 5)
check("L50 vs threat 5 -> +0 (trivial)", gain_high_trivial == 0, f"got {gain_high_trivial}")


# ============================================================
# 11. _resolve_fields helper
# ============================================================
print("\n" + "=" * 60)
print("  _resolve_fields helper")
print("=" * 60)

ch = make_ch(resolve=42, last_update="2025-01-01T00:00:00+00:00")
fields = _resolve_fields(ch)
check("resolve_fields has resolve", fields["resolve"] == 42)
check("resolve_fields has last_update", fields["last_resolve_update"] == "2025-01-01T00:00:00+00:00")


# ============================================================
# 12. Resolve history
# ============================================================
print("\n" + "=" * 60)
print("  Resolve history")
print("=" * 60)

ch = make_ch(resolve=50)
_award_resolve(ch, 5, "test1")
_award_resolve(ch, 3, "test2")
_award_resolve(ch, -2, "test3")
check("History has 3 entries", len(ch["resolve_history"]) == 3)
check("Latest entry is test3", ch["resolve_history"][0]["reason"] == "test3")
check("Resolve is 56", ch["resolve"] == 56)

# History caps at 10
ch2 = make_ch(resolve=50)
for i in range(15):
    _award_resolve(ch2, 1, f"event_{i}")
check("History caps at 10", len(ch2["resolve_history"]) == 10)


# ============================================================
# 13. Acceptance: resolve 20 vs 90 produces different multipliers
# ============================================================
print("\n" + "=" * 60)
print("  ACCEPTANCE: Resolve 20 vs 90 — outcomes differ")
print("=" * 60)

ch20 = make_ch(resolve=20)
ch90 = make_ch(resolve=90)

# Training multiplier
m20 = _resolve_multiplier(ch20)
m90 = _resolve_multiplier(ch90)
check("Training: 20 < 90", m20 < m90, f"{m20} vs {m90}")

# Combat damage
d20 = _resolve_combat_damage_mod(ch20)
d90 = _resolve_combat_damage_mod(ch90)
check("Combat dmg: 20 < 90", d20 < d90, f"{d20} vs {d90}")

# Study buff
s20 = _resolve_study_buff_hours(ch20, 3.0)
s90 = _resolve_study_buff_hours(ch90, 3.0)
check("Study: 20 < 90", s20 < s90, f"{s20} vs {s90}")

# Expedition
e20 = _resolve_expedition_mod(ch20)
e90 = _resolve_expedition_mod(ch90)
check("Exped yield: 20 < 90", e20["yield_mult"] < e90["yield_mult"], f"{e20['yield_mult']} vs {e90['yield_mult']}")


# ============================================================
# Summary
# ============================================================
print("\n" + "=" * 60)
print(f"  RESULTS: {passed} passed, {failed} failed")
print("=" * 60)
if failed > 0:
    sys.exit(1)
