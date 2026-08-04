# `combat_turn` — Refactor Plan

> Plan date: **Aug 4, 2026**
> Target: [`backend/game_engine.py`](backend/game_engine.py) `combat_turn`
> Companion to [ENGINE_AUDIT_AND_PLAN.md](ENGINE_AUDIT_AND_PLAN.md) (Phase 3) and
> [MASTERY_PLANS.md](MASTERY_PLANS.md).

---

## Why this function is the problem

| Measure | Value |
|---|--:|
| Lines | **2,270** |
| `_is_<mastery>(character)` guard calls inside | **140** |
| `if` / `elif` statements | **441** |
| Maximum indent depth | **8** |

Guard calls per mastery:

| Mastery | Guards | | Mastery | Guards |
|---|--:|---|---|--:|
| hunter | 21 | | paladin | 10 |
| assassin | 18 | | druid | 10 |
| bard | 17 | | alchemist | 8 |
| knight | 13 | | lancer | 7 |
| priest | 12 | | | |
| rogue | 12 | | **total** | **140** |
| mage | 12 | | | |

Eleven independent resource systems are interleaved into one control-flow spine.
Touching Hunter's range code means scrolling past Bard's Crescendo.

**This is not a style complaint — it is where the bugs came from.** Every defect
found in this codebase so far lived inside or adjacent to this function:

- `_mage_get_cooldown_modifier` — *called, never defined*. `NameError` on every Mage cast.
- `_priest_start_of_turn` / `_priest_check_enemy_heal_lock` — `def` lines lost in an
  edit, bodies stranded as unreachable code after a `return`. Priests crashed from
  turn 2 of every fight.
- `c_mult = {1:…,6:…}[c_out]` — no `0` key. `KeyError` whenever any mastery landed
  a stun. Broke Lancer, Priest, Mage and Alchemist signature mechanics at once.
- Generic self `stat_mod` — every branch gated on a specific mastery, and Druid,
  Bard and Priest were in none of them. 19 Druid skills silently dropped their
  stat bonuses.

That last one is the tell: **eight mastery-gated branches and no fallback is not a
mistake anyone makes in a 200-line function.** The size is causing the defects.

---

## The turn's actual phase structure

Mapped from the source rather than assumed. Line numbers are indicative.

| # | Phase | Lines | What happens |
|--:|---|---|---|
| 1 | **Setup** | 7303–7327 | Validate `action_type`, strip out-of-combat Paladin faith bonuses, compute racial mods |
| 2 | **Turn start** | 7329–7512 | Per-mastery start-of-turn: Knight Oath bonuses, Paladin passives, Priest passives, Lancer initiation/overload, Assassin shadow init, Hunter range init, unified range system, Rogue innates, Bard init + Crescendo tick, Druid init, Mage Arcane Focus + echo, generic stat_mod re-application, Alchemist pre-imbue |
| 3 | **Items** | 7514–7542 | Pre-combat auto-items (turn 0), manual item use |
| 4 | **Action select** | 7543–7678 | Innate action handling, transient flag clearing, skill cooldown/weapon/capacity checks, range gating |
| 5 | **Player attack** | 7679–8236 | Weapon damage, skill damage, per-mastery riders and damage modifiers |
| 6 | **Apply to monster** | 8237–8739 | Damage application, statuses, on-hit mastery effects |
| 7 | **Enemy turn** | 8740–8944 | Control checks (bound/stun/blind/ensnare, Mage turn-steal, Alchemist launch), monster skill selection, monster damage computation |
| 8 | **Apply to player** | 8945–9290 | Armor/MR, innate defenses, per-mastery dodge and mitigation (Knight, Assassin, Hunter, Rogue, …) |
| 9 | **Turn end** | 9291–9540 | Per-mastery ticks, stat_mod expiry, DoT ticks |
| 10 | **Resolve** | 9541–9562 | Victory/defeat, rewards, return payload |

---

## The hook protocol

Derived from the phases above — not invented. Each hook maps to exactly one phase
boundary where mastery logic currently lives.

```python
class MasteryHooks(Protocol):
    """One implementation per mastery. All methods optional (a base class
    provides no-ops), all receive the same mutable TurnContext."""

    def on_turn_start(self, ctx: TurnContext) -> None: ...
    def on_action_selected(self, ctx: TurnContext) -> None: ...
    def on_damage_computed(self, ctx: TurnContext) -> None: ...   # mutates ctx.outgoing
    def on_hit_landed(self, ctx: TurnContext) -> None: ...
    def on_enemy_turn_start(self, ctx: TurnContext) -> None: ...  # may set ctx.enemy_turn_consumed
    def on_incoming_damage(self, ctx: TurnContext) -> None: ...   # mutates ctx.incoming
    def on_turn_end(self, ctx: TurnContext) -> None: ...
```

`TurnContext` is a single mutable object replacing the ~40 locals currently
threaded through the function:

```python
@dataclass
class TurnContext:
    character: dict
    state: dict
    monster: dict
    log: list[dict]
    action_type: str
    turn: int
    skill: dict | None          # the resolved skill this turn, or None for innate
    outgoing: float            # damage the player is about to deal
    incoming: float            # damage the player is about to take
    outcome: int               # player's d6 result
    enemy_outcome: int         # enemy's d6 result (0 = did not act)
    enemy_turn_consumed: bool
    racial_mods: dict
```

The spine then reads:

```python
hooks = hooks_for(character)          # [KnightHooks()] etc., by masteries list
for h in hooks: h.on_turn_start(ctx)
...
for h in hooks: h.on_damage_computed(ctx)
```

**Mutating a shared context rather than returning values** is deliberate: the
current code mutates `state` and `character` freely, so a return-value protocol
would require auditing every mutation site up front. Context mutation is a
behaviour-preserving transformation; tightening it to pure functions is a later,
separate step.

---

## Safety net — built and verified first

`tests/golden.py`. This existed before a single line was moved.

- **1,584 scenarios / 19,820 turns.** 11 masteries × 4 levels (1/20/60/100) ×
  3 monsters × 6 innate actions × 2 seeds.
- Each scenario pins the **log entries** (kind, text, damage, outcome), **player
  HP**, **victory state**, and **28 tracked state keys** — every mastery's resource
  meter, so a refactor that silently stops Crescendo or Shadows building is caught
  even when the log looks fine.
- Levels 1/20/60/100 deliberately straddle the passive unlock bands, so
  level-gated behaviour is exercised.
- Fixtures store a **sha256 digest per scenario**, not full traces — full traces
  are ~21 MB and do not belong in git. `python -m tests.golden diff "<key>"`
  replays one scenario in full when a digest moves.

**Determinism was verified before building it**: same seed → byte-identical logs,
different seed → divergence. This only holds because `progression.py` removed the
`random.choice` from the level-up path.

```bash
python -m tests.golden record            # before touching anything
python -m tests.golden verify            # after every extraction — must say IDENTICAL
python -m tests.golden diff "<key>"      # replay one scenario when a digest moves
```

### The net was tested against deliberate sabotage

A safety net nobody has tried to break is an assumption, not a net. One behaviour
change was injected per mastery, in that mastery's own resource machinery, and the
harness had to catch each:

| Target | Result | Scenarios changed |
|---|---|--:|
| knight (Oath starting stacks) | CAUGHT | 108 |
| paladin (faith tier) | CAUGHT | 108 |
| lancer (element count) | CAUGHT | 6 |
| assassin (burst threshold) | CAUGHT | 144 |
| rogue (opportunist bonus) | CAUGHT | 48 |
| hunter (communion threshold) | CAUGHT | 46 |
| bard (crescendo max) | CAUGHT | 144 |
| alchemist (combo multiplier) | CAUGHT | 500 |
| priest (sanctity multiplier) | CAUGHT | 144 |
| core dice (advantage level) | CAUGHT | 1294 |
| mage (cooldown modifier) | not observable | 0 |
| druid (max summons) | not observable | 0 |

**The first run caught only 8 of 12, and fixing that mattered more than the score
suggests.** Two real problems surfaced:

1. **A genuine blind spot.** Changing the Knight's starting Oath stacks produced
   *zero* diffs, because `state["knight_oath"]` was never set in any scenario — the
   entire Oath branch was dead in the harness. Fixed by explicitly activating each
   mastery's resource (`_activate_resources`): Oath selected, Bard mode set,
   Alchemist pre-imbued, Druid summoned.
2. **Thin skill bars.** Scenarios used only the two starting skills, so cooldowns
   rarely bound and several paths never manifested. Bars are now filled with up to
   10 of the mastery's own skills, which is what made the Priest sabotage detectable.

The two remaining misses are understood, not unknown:

- **mage cooldown modifier** — the reduction fires, but with a full bar the skill
  picker finds an available skill either way, so nothing observable changes.
  Covered directly by `tests/test_combat_cooldowns.py` instead.
- **druid max summons** — the cap only binds when summoning past it, and scenarios
  summon once. Structurally unobservable here.

A probe test confirmed all three of mage/priest/druid per-turn ticks **do** execute
in 144 scenarios each, so this is about sabotage observability, not coverage.

---

## Extraction order

Ascending guard count, so the pattern is proven on the cheapest mastery first and
the riskiest is done last with the most practice.

| Order | Mastery | Guards | Notes |
|--:|---|--:|---|
| 1 | **Lancer** | 7 | Elemental imbue only. Smallest surface — proves the pattern. |
| 2 | Alchemist | 8 | Combo Flow + imbue; helpers already well-isolated (`_alch_*`). |
| 3 | Druid | 10 | Summons already live in their own helpers. |
| 4 | Paladin | 10 | Faith bar is mostly a stat recompute. |
| 5 | Mage | 12 | Library passives now fully wired, so behaviour is pinned. |
| 6 | Priest | 12 | 20 helpers already extracted; mostly call-site moves. |
| 7 | Rogue | 12 | Innates already separate; level passives interleaved. |
| 8 | Knight | 13 | **Deceptive** — only 5 helpers, because its passives are inline flat effects. Expect more work than the count suggests. |
| 9 | Bard | 17 | Song/Dance mode split touches many phases. |
| 10 | Assassin | 18 | Shadow thresholds interleave with damage computation. |
| 11 | **Hunter** | 21 | Range model + Communion transforms touch nearly every phase. |

**One mastery per session.** Each is independently shippable, and the golden logs
must read IDENTICAL before moving on. The work is interruptible by design — design
tasks can be slotted between extractions.

---

## Definition of done

- `combat_turn` under ~400 lines
- Zero `_is_<mastery>(character)` calls inside it
- Each mastery's logic in one place, readable without scrolling past another's
- All 1,584 golden scenarios IDENTICAL
- Full unit suite green (241 tests)
- All 11 masteries crash-free at levels 1/20/60/100

## Explicit non-goals

- **No behaviour changes.** Not even fixing a bug spotted mid-extraction — note it,
  finish the extraction, verify identical, then fix it as a separate change with
  its own re-recorded golden. Mixing the two makes the golden useless.
- **No pure-function conversion.** Context mutation preserves current semantics;
  tightening comes later.
- **No performance work.**

---

## Risks

| Risk | Mitigation |
|---|---|
| A mastery reads another's state mid-turn | The shared `TurnContext` keeps every hook able to see the same state, exactly as today. Cross-reads survive the move. |
| Hook ordering changes behaviour | Hooks run in a fixed order derived from the current source order, not by mastery name. |
| A scenario the golden misses | 1,584 scenarios cover every mastery × action × level band, but coverage is not proof. The 241 unit tests are the second net. |
| Interruption leaves it half-done | Each mastery is a complete unit; a partial extraction is never committed with diverged goldens. |


---

# Execution log

## Round 1 — Aug 4, 2026

| Metric | Before | After | Δ |
|---|--:|--:|--:|
| `combat_turn` lines | 2,270 | **2,021** | −249 |
| Mastery guard calls | 140 | **122** | −18 |
| `if`/`elif` branches | 441 | **392** | −49 |
| Duplicated stat_mod expiry loops | 21 | **8** | −13 |
| Control-flow depth | 8 | 8 | — |

**Golden logs read IDENTICAL after every step.** 316 unit tests pass. All 11
masteries crash-free across levels 1/20/60/100 × 6 innate actions × manual and
auto skill selection.

### What moved

1. **`tick_stat_mods()`** — the same 15-line expiry loop existed **21 times**
   across 19 state buckets, the largest single block of duplication in the
   function and a standing invitation for one copy to drift. 13 collapsed; the 8
   remaining differ materially (e.g. Paladin's enemy mods deliberately expire
   without refunding, which the shared helper would have "fixed" and broken the
   goldens).
2. **`apply_self_stat_mods()` / `apply_enemy_stat_mods()`** — 6 self-apply and
   4 enemy-bank blocks collapsed. These also fixed a latent aliasing hazard: some
   copies did `self_mods = sk["stat_mod"]["self"]` without copying, so a later
   mutation would have corrupted the shared skill definition for every character
   in the process. The helper always copies.
3. **`mastery_hooks.py`** — `TurnContext` + a 7-phase `MasteryHooks` protocol,
   with `HOOK_ORDER` mirroring the original inline execution order. Ordering is
   observable, so it is declared rather than incidental.
4. **`mastery/lancer.py`** — fully extracted (all 7 guards), the pilot that proved
   the pattern end to end.
5. **`mastery/core.py`** — turn-start and turn-end phases extracted for Knight,
   Paladin, Priest, Assassin, Hunter, Mage, Alchemist. Rogue, Bard and Druid have
   registered hook classes with no phases moved yet.

### Ratchet tests

`tests/test_mastery_hooks.py` pins the structure so the spine cannot silently
regain its old shape: guard count ≤ 122, length ≤ 2,021, expiry loops ≤ 8. These
may fall, never rise. It also pins the registry contract (every mastery
registered, every mastery in `HOOK_ORDER`, declared order respected) and the
shared helpers' semantics.

### What remains inline, and why

122 guards are still in the spine, concentrated in the damage path:

| Mastery | Guards left | Blocker |
|---|--:|---|
| hunter | 20 | Range model + Communion transforms touch nearly every phase |
| bard | 17 | Song/Dance mode split spans player and enemy phases |
| assassin | 16 | Shadow thresholds interleave with damage computation |
| rogue | 12 | Innate checks sit inside the incoming-damage chain |
| mage | 11 | Passive modifiers interleave with damage type resolution |
| knight | 11 | Oath milestones read and write mid-damage |
| druid | 10 | Summon actions interleave with the turn sequence |
| priest | 10 | Skill processing replaces the whole player-action branch |
| paladin | 8 | Faith scaling reads HP mid-turn |
| alchemist | 7 | `is_alch_strike` and the basic-attack imbue rider are embedded |

These are **not** appended to a phase — they are woven into damage computation, so
moving them requires restructuring the spine's damage flow. That is the next
round, and it needs the `on_damage_computed` / `on_incoming_damage` /
`on_hit_landed` phases carrying real state rather than the two that are wired now.

Doing it in the same pass as the clean moves would have meant a large diff with no
way to attribute a golden-log divergence to a specific change. Every step above
was verified in isolation.


---

## Round 2 — the damage path

| Metric | Original | Round 1 | **Round 2** |
|---|--:|--:|--:|
| `combat_turn` lines | 2,270 | 2,021 | **1,353** (−40%) |
| Mastery guard calls | 140 | 122 | **46** (−67%) |
| `if`/`elif` branches | 441 | 392 | **~250** |
| Duplicated expiry loops | 21 | 8 | **8** |

**Golden logs IDENTICAL after every step.** 316 tests pass. Zero crashes across
11 masteries × 4 levels × 6 innate actions × 2 monsters × manual and auto picks.

### What moved in round 2

| Module | Lines | Was |
|---|--:|---|
`mastery/mitigation.py` | 283 | 22 interleaved guards mutating `c_dmg` in one 180-line chain |
`mastery/skill_effects.py` | 395 | 45 guards / 353 lines of "what happens because this skill was used" |
`mastery/outgoing.py` | 232 | 12 guards / 192 lines of post-damage riders |
`mastery/core.py` | 226 | turn-start / turn-end for 7 masteries |
`mastery/lancer.py` | 163 | one fully-extracted mastery (the pilot) |

### Why pipelines, not per-mastery loops

The mitigation chain looked like an obvious `for h in hooks_for(character)` loop.
It is not, for two reasons that a loop would have broken silently:

1. **RNG order is observable.** Assassin, Hunter, Rogue, Bard and the `confused`
   check all call `random.random()`. Reordering them shifts every later roll in the
   turn — the goldens diverge even though each step's own logic is untouched.
2. **Two steps are universal, and sit *between* masteries** — the range-gap check
   (after Assassin) and the `confused` self-hit (after Rogue). A per-mastery loop
   has nowhere to put them.

So `INCOMING_PIPELINE` declares the sequence as data: `(required_mastery | None,
step)`. Order is explicit and reviewable rather than emergent from a registry.

### Two mistakes worth recording

**A boundary that cut through a block.** The first attempt at `skill_effects.py`
ended the region mid-way through the cooldown/capacity block, so `_cd` — a local
the spine still needed — went out of scope. `UnboundLocalError`, 21 tests red.
Reverted, moved the boundary before the cooldown block, re-extracted.

**Guessing the crossing set instead of computing it.** I checked region-assigned
locals against a *hand-written list* of names I thought the spine used. `_cd` was
not on that list. The fix was to compute it: locals assigned inside the region and
read after it before being reassigned. That found `outcome` and `skill_used_msg` for
`skill_effects`, and `total_dmg` and `outcome` for `outgoing` — and correctly
rejected `bonus` and `shadows`, which appear after the region only inside comments.

Both were caught in seconds because the harness existed first. Neither would have
been obvious from reading.

### What is left, and what it is

46 guards remain. They are no longer a wall — they are the parts genuinely
interleaved with the spine's own control flow:

- **Priest (7)** — `_priest_process_skill` *replaces* the whole player-action
  branch rather than adding to it, so the spine has to know about it.
- **Paladin (6)** — faith scaling reads HP at several points mid-turn.
- **Bard (6)** — unevadable attacks and CC immunity alter the dice roll and the
  enemy's status application, in two different phases.
- **Alchemist (6)** — `is_alch_strike` is a *predicate the spine branches on*, not
  an effect that can be appended.
- **Knight (6)**, **Hunter (4)**, **Rogue (4)**, **Druid (4)**, **Assassin (2)**,
  **Mage (1)**.

Getting these out means changing the spine's control flow, not moving blocks — for
example letting a mastery *replace* the player-action branch rather than decorate
it. That is a design change, and it should be made deliberately rather than as a
side effect of a refactor pass.

The ratchet tests hold the line at 46 guards / 1,353 lines: those numbers may fall,
never rise.
