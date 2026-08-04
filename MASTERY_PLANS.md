# Erchistorn — Mastery Plans

> Audit date: **Aug 4, 2026**
> Method: each mastery's design spec in [`docs/skills/`](docs/skills) compared
> against the shipped implementation in `game_data.py` (skills + passive tables)
> and `game_engine.py` (mechanics), then verified by executing the code.
>
> Companion to [ENGINE_AUDIT_AND_PLAN.md](ENGINE_AUDIT_AND_PLAN.md) (engine
> correctness) and [GAME_IMPROVEMENT_PLAN.md](GAME_IMPROVEMENT_PLAN.md) (content
> roadmap). This document is about **the 11 masteries specifically**.

---

> ## ✅ EXECUTED — Aug 4, 2026
>
> **Shipped:** all 30 Druid skills · Alchemist passive table (10) + wiring + route ·
> 7 Mage Library passives · Hunter `unbreakable_focus` (and the guidance reset it
> guards) · Rogue `con_master` + `slippery_soul` · Priest passives route · the
> aggregate passives route (was missing priest *and* alchemist).
>
> **Two further gaps found while executing, both fixed:**
> - **48 of 53 skill trainers pointed at towns that no longer exist.** The canon v2
>   rename migrated characters but never `TEACHERS`, so visiting a real town showed
>   almost no trainers — skill learning was broken for nearly every mastery.
> - **The Rogue had no trainer at all**, and 4 teachers carried `mastery_focus`
>   values from an earlier class list (`berserker`, `tank`, `ranger`, `saint`).
>
> **Audit corrections.** Three "unwired" passives below were false positives —
> `knight.second_wind` and `rogue.quick_learner` are implemented in `server.py`
> (which the first sweep didn't search), and `rogue.trap_specialist` is a bare
> `charges = 2 if level >= 70` with no name to match on. Text search cannot detect
> level-gated passives implemented as plain comparisons; those are covered by
> behavioural tests in `tests/test_mastery_passives.py` instead. Real remaining
> gaps are listed at the end.
>
> 214 tests pass. All 11 masteries crash-tested at level 1, 12 and 100.

---

## How to read this

Every mastery was checked on four axes:

| Axis | Question |
|---|---|
| **Skills** | Are the 30 spec'd skills actually in `SKILLS`? |
| **Passives** | Does the 10-level passive table exist, and is each entry wired into the engine? |
| **Mechanics** | Do the mastery's engine helpers implement its declared resource system? |
| **Surfacing** | Can the player see the system working? |

A passive counts as *wired* if the engine references it by id **or** implements it
via a level check with a matching log message. Level-gated passives are mostly
implemented as `if character["level"] >= N`, which an id-only search misses — the
first pass of this audit produced false positives for exactly that reason, and
the numbers below are from the corrected pass.

---

## Scoreboard

| Mastery | Skills | Passives | Unwired passives | Engine helpers | Verdict |
|---|:--:|:--:|:--:|:--:|---|
| **Druid** | **2 / 30** | 12 | 1 | 15 | 🔴 **Skill kit missing entirely** |
| **Mage** | 30 / 30 | 50 | **24** | 15 | 🔴 **Half the Arcane Library is inert** |
| **Alchemist** | 30 / 30 | **0** | — | 9 | 🟠 **No passive progression at all** |
| **Rogue** | 30 / 30 | 10 | **4** | 15 | 🟠 Level passives half-built |
| **Bard** | 30 / 30 | 11 | 0 | 12 | 🟡 Per-skill Crescendo/Encore flags ignored |
| **Knight** | 30 / 30 | 10 | 1 | 5 | 🟡 One passive missing |
| **Hunter** | 30 / 30 | 11 | 1 | 11 | 🟡 One passive missing |
| **Priest** | 30 / 30 | 11 | 0 | 20 | 🟢 Complete (2 crashes fixed this session) |
| **Paladin** | 30 / 30 | 10 | 0 | 6 | 🟢 Complete |
| **Lancer** | 30 / 30 | 10 | 0 | 6 | 🟢 Complete (crash fixed this session) |
| **Assassin** | 30 / 30 | 10 | 0 | 8 | 🟢 Complete |

**Total gap: 28 missing skills, 30 unwired passives, 1 missing passive table.**

Four masteries were also *crashing* in combat before this session — see
[Crashes already fixed](#crashes-already-fixed) at the end.

---

# 🔴 Priority 1 — Druid

**Identity (spec):** *"The wild answers when called."* Summon creatures, fuse with
them, inherit their riders. Pack synergy. The only mastery whose power lives in
other bodies.

### What's built — a lot

The Druid has the **most sophisticated engine work of any mastery**: 15 helpers
covering summon lifecycle, per-creature AI skill selection, pack synergy,
fusion + fusion riders, boss auras, and legendary passives. There is a whole
bestiary system (`/game/bestiary`), taming (`attempt_tame`), creature stat
scaling, and 5 dedicated API routes (`summon`, `unsummon`, `fuse`, `end_fusion`,
`summon_mode`).

### What's lacking — the entire skill kit

**The Druid has 2 skills. The spec calls for 30.**

Present: `thornlash`, `beast_call` (both untyped, the two starting skills).
Missing: all 30 spec'd ids, including every shapeshift form (`bear_form`,
`eagle_form`, `beast_form`), every heal (`healing_bloom`, `seed_of_life`,
`natures_rebirth`), every control skill (`entangling_roots`, `vine_prison`,
`natures_grasp`), and both legendaries (`heart_of_gaia`, `legend_of_nature`).

So a Druid levels to 100 with two skills and a summoning engine. It is the
least playable mastery in the game despite having the most engine support.

Also: `bonded_senses` passive has no engine implementation.

### Plan

| Step | Work | Effort |
|---|---|---|
| 1 | Author the 30 skills from [docs/skills/druid.md](docs/skills/druid.md) into `SKILLS` with `type: "druid"`. The doc already contains complete python dicts per skill — this is transcription plus `damage` values, not design. | M |
| 2 | Add `SKILL_RARITY` / `SKILL_EXEC` / `SKILL_EXTRAS` entries so they appear in trainers and the learning economy. | S |
| 3 | Wire shapeshift forms. These are new mechanically — a form is a persistent self-`stat_mod` plus a skill-set swap. Reuse the fusion plumbing (`_druid_get_fusion_riders`) rather than inventing a parallel system. | M |
| 4 | Implement `bonded_senses`. | XS |
| 5 | Golden combat test per form + a test asserting all 30 druid skills resolve. | S |

**Do step 1 first and alone.** It converts the Druid from unplayable to playable
in one pass and needs no engine changes.

---

# 🔴 Priority 2 — Mage

**Identity (spec):** *"Arcane fire, arcane truth, arcane cost."* Equip passives
from a 50-entry **Arcane Library**, research them by killing specific monsters,
build school synergies.

### What's built

All 30 skills. Arcane Focus generation, school synergy detection, research
routes, loadout save/load, echo/rewind mechanics, and 15 engine helpers. The
Library UI and `/game/mage/library/*` routes work.

### What's lacking — 24 of 50 passives do nothing

The player can research and equip these, and they have **no effect**:

**School of Spatial — all 11 are inert:**
`long_range`, `point_blank`, `expanding_radius`, `blink_step`, `portal_mastery`,
`gravity_shift`, `mirror_position`, `spatial_tear`, `far_strike`,
`portal_behind_ally`, `portal_behind_enemy`, `portal_through_wall`,
`portal_through_trap`

**School of Mental — 9 of 10 inert:**
`double_jeopardy`, `mind_fracture`, `paranoia`, `hallucination`, `mass_hysteria`,
`delirium`, `mind_control`, `illusion_mastery`

**Elements/Temporal — 3 inert:** `absolute_zero`, `wildfire`, `time_loop`

This is worse than a missing feature: the player spends research effort on a
visible, equippable upgrade that silently does nothing. A whole school being
dead also breaks the synergy system, since Spatial can never contribute.

**Root cause for Spatial specifically:** the school is built around *range and
positioning*, and combat has only a partial range model — `_get_weapon_range_for_combat`
and `_compute_range_gap` exist (Hunter uses them), but there is no positioning
system for portals, flanking, or terrain. Spatial cannot be implemented without
deciding how much positional simulation the game wants.

### Plan

| Step | Work | Effort |
|---|---|---|
| 1 | **Mental school (9 passives).** All are status/debuff manipulation, and the engine already has statuses, `_append_status_dedup`, and monster-turn skipping. Highest value per hour. | M |
| 2 | **Elements (3 passives).** `absolute_zero` and `wildfire` are conditional status upgrades on existing statuses; `time_loop` reuses the stun path. | S |
| 3 | **Spatial — decide scope first.** Either (a) implement the 4 range-based passives (`long_range`, `point_blank`, `far_strike`, `expanding_radius`) against the existing range model and cut the 7 portal/terrain ones from the Library, or (b) build a positioning system. **Recommend (a)** — cutting content that can't work beats shipping content that doesn't. | M or L |
| 4 | Add a test asserting every equippable Library passive is referenced by the engine, so this can't regress. | S |

> Until step 3 lands, consider flagging the unimplemented passives in the Library
> UI as "Planned" rather than letting players research them.

---

# 🟠 Priority 3 — Alchemist

**Identity (spec):** *"The Transmuter."* Close-range katar fighter who pre-imbues
skills onto the blade and spends **Combo Flow** on adaptive mini-rules.

### What's built

All 30 skills (typed `imbuable` / `cast` / `strike` rather than `alchemist` —
worth normalising). 9 `_alch_*` engine helpers covering imbue loading, imbue
riders, CF gain/spend, mini-rule execution, enemy stat mods, and per-turn ticks.
Two dedicated routes (`/combat/alchemist/cf`, `/pre-imbue`). The Combo Flow
system genuinely works and is one of the more interesting mechanics in the game.

### What's lacking — no passive progression

**`ALCHEMIST_PASSIVES` does not exist.** Every other mastery has a 10-entry table
granting a passive every 10 levels. The Alchemist gets **nothing** from level 10
to 100 — no `divine_shield`, no `oath_sworn`, no capstone. It is the only mastery
with a completely flat passive curve, which makes it strictly worse to level.

There is also no `docs/skills/alchemist.md` section defining what those passives
should be, so this needs design, not just transcription.

### Plan

| Step | Work | Effort |
|---|---|---|
| 1 | **Design 10 passives** on the Combo Flow / imbue axis, mirroring the shape other masteries use (early: quality-of-life; L60-70: the power engine; L100: capstone). Suggested spine: faster CF generation → extra imbue charges → imbue never expires → mini-rules trigger a tier earlier → dual imbue → all mini-rules at once. | S |
| 2 | Add `ALCHEMIST_PASSIVES` to `game_data.py` and the `/game/alchemist/passives` route (every other mastery has one). | S |
| 3 | Wire them in `_alch_*` helpers — most will be multipliers on existing CF/imbue values, so this is cheap. | M |
| 4 | Normalise skill `type` to `"alchemist"` so tooling and the audit stop needing special cases. | XS |

---

# 🟠 Priority 4 — Rogue

**Identity (spec):** *"The Adaptive Trickster."* Customises their passive kit
through **equippable innate skills** — misdirection, traps, counter-attacks.

### What's built

All 30 skills. The **innate system works well**: `ROGUE_INNATE_SKILLS`,
equip/unequip/swap routes, slot scaling by level, and 15 engine helpers
implementing dirty fighting, counter-strike, lucky dodger, opportunist, light
feet, slippery, con artist, and trap master.

### What's lacking

The Rogue has **two** passive systems and only one is finished:

- `ROGUE_INNATE_SKILLS` (equippable) — ✅ fully wired
- `ROGUE_PASSIVES` (level-gated, 10 entries) — ❌ 4 unimplemented:
  `quick_learner`, `trap_specialist`, `con_master`, `slippery_soul`

The confusing part: engine functions named `_rogue_apply_trap_master`,
`_rogue_get_con_artist_bonus` and `_rogue_slippery_tick` **do** exist — but they
implement the *innate* versions. The similarly-named level-gated passives are
separate entries that were never wired, which is exactly why they were easy to
miss.

### Plan

| Step | Work | Effort |
|---|---|---|
| 1 | Decide whether the 4 level-gated passives should be **distinct upgrades** to their innate namesakes (e.g. `trap_specialist` doubles innate trap damage) or were **duplicates** that should be replaced with new effects. Recommend the former — it makes the two systems reinforce each other. | XS |
| 2 | Implement the 4 in the existing `_rogue_*` helpers. | S |
| 3 | Rename either the innates or the level passives so the two systems are distinguishable by name. | XS |

---

# 🟡 Priority 5 — Bard

**Identity (spec):** *"The Master of Control."* Song mode rewrites ally rules;
Dance mode controls enemy behaviour. Builds **Crescendo**.

### What's built

All 30 skills, 11 passives all wired, 12 engine helpers. Song/Dance mode
switching, Crescendo ticking, performance chance scaling, encore chance, death
saves, and CC immunity all work. `/game/bard/mode-switch` exists.

### What's lacking — per-skill Crescendo/Encore opt-in is ignored

Seven skills declare `crescendo: True, encore: True`:

`song_of_heroes`, `song_of_hope`, `song_of_wisdom`, `song_of_freedom`,
`song_of_fortune`, `requiem_of_the_heavens`, `symphony_of_creation`

The engine **never reads those fields** — `_bard_get_crescendo_max` and
`_bard_get_encore_chance` derive everything from the character and passives. The
frontend *does* read them, so the UI advertises "this song builds Crescendo /
can Encore" while the engine treats all songs identically.

Either the fields are meaningful (and the engine should gate on them) or they are
decoration (and the UI should stop showing them). Right now the client and the
server disagree.

### Plan

| Step | Work | Effort |
|---|---|---|
| 1 | Decide: are Crescendo/Encore **per-skill opt-ins** or global? The presence of the flags on exactly 7 of 30 skills suggests opt-in was intended. | XS |
| 2 | If opt-in: gate `_bard_tick_crescendo` / `_bard_get_encore_chance` on `sk.get("crescendo")` / `sk.get("encore")`. | S |
| 3 | Add a test asserting no skill field is read by the frontend but ignored by the engine — this class of client/server drift is invisible otherwise. | S |

---

# 🟡 Priority 6 — Knight & Hunter (one passive each)

### Knight — `second_wind` (L90) unimplemented

*"Switching Oaths saves 3 stacks instead of resetting to 0."*

Everything else works: 5 Oaths with distinct stack triggers, milestone bonuses at
5 and 10, and the other 9 passives (all level-gated, correctly wired). The Oath
system is one of the best-realised mechanics in the game.

`eternal_oath` (L100) also promises stack-saving and *is* wired, so the L90
version is a strict subset — likely just missed.

**Plan:** find the Oath-switch path, save 3 stacks when `level >= 90`. **XS.**

Worth noting: the Knight has only **5 engine helpers**, the fewest of any
mastery, yet is feature-complete. Its passives are almost all flat stat/threshold
effects handled inline in `combat_turn`. That is *why* it needs so few helpers —
and also why extracting Knight during the `combat_turn` refactor
([Phase 3](ENGINE_AUDIT_AND_PLAN.md)) will be more work than the helper count
suggests.

### Hunter — `unbreakable_focus` (L?) unimplemented

Everything else works: Spirit Guidance stacking to 10, skill transmutation at
stack 10, the range-gap model, ambush, crit chance/damage scaling, and multi-hit
counts. Hunter is mechanically the richest ranged mastery.

**Plan:** implement the one passive. **XS.**

---

# 🟢 Complete — Priest, Paladin, Lancer, Assassin

These four are feature-complete against their specs: 30/30 skills, all passives
wired, resource systems implemented.

| Mastery | Resource | Engine helpers | Notes |
|---|---|:--:|---|
| **Priest** | Sanctity + Miracles | 20 (most of any mastery) | Shield walls, HoT, delayed heals, cleanses, holy bonuses |
| **Paladin** | Faith bar (power from low HP) | 6 | Faith tiers, resurrection, heal amp |
| **Lancer** | Elemental imbue | 6 | Per-element strike riders, overload, initiation |
| **Assassin** | Shadows 0→100 → BURST | 8 | Fear deposits, shadow reclaim, threshold bonuses |

All four had latent crashes that are now fixed (below). No further work planned.

---

## Crashes already fixed

Found by running real combats and by an undefined-name sweep. All were live
500-level failures, none were in the original engine audit:

| Mastery | Bug | Effect |
|---|---|---|
| **Mage** | `_mage_get_cooldown_modifier` called but never defined | `NameError` on **every skill cast** — unplayable |
| **Priest** | `_priest_start_of_turn` never defined (body stranded after a `return`) | `NameError` **from turn 2 of every fight**; HoT/delayed-heal/Smite never ran |
| **Priest** | `_priest_check_enemy_heal_lock` never defined (same cause) | `NameError` whenever a monster tried to heal |
| **Lancer, Priest, Mage, Alchemist** | `c_mult` lookup had no `0` key | `KeyError` whenever the monster was stunned/bound/ensnared/airborne — broke all four masteries' **signature control effects** |
| **Mage, Assassin** | `sk`-is-`None` on 5 helpers | `AttributeError` on a basic strike with an empty skill bar |

`tests/test_engine_integrity.py::test_no_calls_to_undefined_functions` now guards
this class of bug across the engine modules.

---

## Recommended order

Sequenced by player-visible value per hour of work:

1. **Druid skills** (M) — converts an unplayable mastery to playable. Pure transcription from an existing doc.
2. **Alchemist passives** (S design + M wiring) — removes the only flat level curve in the game.
3. **Mage Mental + Elements** (M) — 12 passives that currently do nothing on an equippable, researched upgrade path.
4. **Rogue's 4 level passives** (S) — half a passive table.
5. **Bard Crescendo/Encore decision** (S) — resolves a live client/server disagreement.
6. **Knight `second_wind` + Hunter `unbreakable_focus`** (XS each) — trivial, do them while in the file.
7. **Mage Spatial scope decision** (M or L) — needs a design call on positional simulation before any code.

Steps 1, 2, 4, 6 need **no engine architecture changes** and can land before the
`combat_turn` refactor. Step 3 touches the mage passive path, which is already
well-isolated. Step 7 should wait for the refactor.


---

# Post-execution status

| Mastery | Before | Now |
|---|---|---|
| Druid | 2/30 skills | **30/30**, all learnable from a trainer |
| Alchemist | no passive table | **10 passives**, wired + route |
| Mage | 24 inert Library passives | **7 wired**; 17 deferred (need multi-enemy or positioning) |
| Rogue | no trainer; 2 unwired passives | trainer wired, **30/30 learnable**, passives implemented |
| Hunter | `unbreakable_focus` a no-op | implemented, plus the reset it guards |
| Priest | no passives route | route added; also in the aggregate |
| All | 48/53 trainers unreachable | **53/53 reachable** |

## Still open

- **Mage Spatial school (13 passives)** — needs a positioning/terrain decision before any code. Portals, flanking and terrain have no representation in combat.
- **Mage `wildfire` / `hallucination` / `mass_hysteria` / `delirium` (4)** — all describe multi-enemy behaviour ("spreads to adjacent", "attacks their own ally"). Combat is strictly 1v1, so these cannot be implemented as written. Either add multi-enemy encounters or rewrite them as single-target effects.
- **Druid `bonded_senses`** — needs the summon's attack skill mirrored as a passive rider; the fusion-rider plumbing is the natural place.
- **Bard per-skill `crescendo` / `encore`** — 7 skills declare them, the frontend reads them, the engine ignores them. Needs the design call in Priority 5 above.
- **Druid shapeshift forms** — the 30 skills are in, but forms are currently plain buffs. Making them true skill-set swaps is the follow-up.
- **Alchemist skill `type`** — still `imbuable`/`cast`/`strike` rather than `alchemist`, so tooling needs a special case.


---

# Second pass — Aug 4, 2026

Everything listed under "Still open" above is now closed except one deliberate deferral.

| Item | Outcome |
|---|---|
| Mage Spatial school | **8 of 14 implemented.** The combat loop already maintained a real range model (`player_range`, `monster_range`, `range_gap`), so Long Range, Point Blank, Far Strike, Gravity Shift, Reposition, Blink Step, Mirror Position and Expanding Radius all work. |
| Mage portal/terrain passives (6) | Flagged `planned` and **blocked from being equipped** — previously a player could spend research on a permanent no-op. Spatial still has 8 equippable, enough for both synergy tiers. |
| `wildfire` / `hallucination` / `mass_hysteria` / `delirium` | Reinterpreted as single-target equivalents that keep each passive's identity: burn intensifies, decoys eat attacks while evasive, debuffs last 50% longer, addled enemies strike themselves. Descriptions rewritten so the Library no longer advertises multi-enemy behaviour. |
| `elemental_overload_mage`, `temporal_echo`, `overload_mage` | Implemented. **The Arcane Library is now 44/44 equippable passives wired**, up from 26. |
| Bard Crescendo / Encore | The 7 flagged skills turned out to be exactly the 7 performance skills, so the flags were redundant — but that exposed the real bug: **Crescendo built every turn even if the Bard never performed.** It now only builds while a performance declaring `crescendo` is active, and Encore only rolls for skills declaring `encore`. |
| Druid `bonded_senses` | Implemented — the Druid echoes its strongest summon's attack at half strength with no status rider, once per turn. |
| Druid shapeshift forms | There are 3 forms, not 8, and they already had distinct stat profiles. The real gap was **exclusivity** — nothing stopped stacking bear + eagle + beast at once. Forms are now mutually exclusive. |
| Alchemist skill `type` | **No change needed.** `mastery_req: ["alchemist"]` already identifies them; `type` carries the meaningful `imbuable` / `cast` / `strike` subtype that the combat HUD displays. My audit tooling was reading the wrong field. |

### One more bug found while doing the above

**All 19 Druid skills carrying `stat_mod: {"self": ...}` silently dropped their stat
bonuses.** Every self-stat_mod branch in `combat_turn` is gated on a specific
mastery (`_is_knight`, `_is_mage`, ...) and the Druid was never one of them — nor
were Bard or Priest. There was no generic fallback at all. Added one, plus the
start-of-turn re-application the other masteries have (buffs live in `state`
because `combat_turn` restores `character["stats"]` on exit).

### Still deferred

- **6 portal/terrain Spatial passives** — need portals, terrain or allies. Blocked from equipping rather than silently inert.
- **`combat_turn` mastery extraction** — untouched. Still the top structural priority; see [ENGINE_AUDIT_AND_PLAN.md](ENGINE_AUDIT_AND_PLAN.md) Phase 3.

241 tests pass. All 11 masteries crash-tested at level 100 with every passive active.
