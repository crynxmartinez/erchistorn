# Hardening Plan — Tiers 1 to 3

> **Status: Tier 1 complete, Tier 2.3 complete, Tier 2.1 in progress.**
> Results are recorded inline under each item. Five more bugs were found while
> executing this plan, four of them player-facing:
>
> | # | Bug | Found by |
> |---|---|---|
> | 1 | Creation summary under-reported Vitality (showed 4, created 6) — client never applied `role.bonus` | 1.1, running the UI |
> | 2 | Stat breakdown credited unnamed contributors; Resilience row absent entirely | 1.1 |
> | 3 | Skill library rendered a bare "PWR" label — `skill.power` is now `skill.damage` | 1.1 |
> | 4 | Victory panel reported double the rewards actually granted (+41 XP for 20) | 1.1 |
> | 5 | **Skinning was dead after every victory** — the turn handler deleted the combat doc that `/combat/skin` looks up | 1.2, endpoint matrix |
>
> Plus stale content: the landing page advertised seven continents by names that
> no longer exist, and nine strings named retired towns (Ironhold, Willowmere) or
> a retired continent (Aetheria).

Written after a full test-play pass over real HTTP and Mongo (357 tests green,
eight request-time crashes fixed, three repos pushed). Everything below comes
from something actually observed, not from a general checklist.

The organising lesson: **every bug found in that pass loaded cleanly and failed
only when a request reached it.** Imports succeeded, routes registered,
`len(app.routes)` looked right, and the endpoint 500'd or silently did nothing
the moment a player touched it. Tier 1 exists to make that class impossible to
ship again. Tier 2 removes the reasons it kept happening. Tier 3 is optional.

Second lesson, equally load-bearing: **two of those eight bugs were introduced by
my own refactor**, which had byte-identical golden logs after every single step.
The logs were honest; they just only cover paths the scenarios walk, and no
scenario ever swore the Oath of Vanguard. That is why Tier 2 leads with coverage
measurement rather than more restructuring.

---

## Tier 1 — before anyone plays

### 1.1 Run the frontend against a live backend

**Why.** 29 frontend files were changed and **not one has ever been loaded in a
browser.** They are also precisely the files that consume the API surface this
work renamed. If `main` auto-deploys, this is already live and possibly broken.

**What changed underneath them:**

| Change | What the UI must now read |
|---|---|
| `power` removed everywhere | stats (`might`/`grace`/`insight`/`resilience`); `monster_threat`, never `monster_power` |
| New `derived` block on character | `armor`, `magic_resistance`, `physical_reduction_pct`, `xp_for_next` |
| New equip slot | `hands` in `equipped` and in slot labels |
| Skill bar seeded at creation | `skill_bar` arrives populated with bare skill-id strings |
| `skill.power` renamed | `skill.damage` |
| Skill-use reporting | `skill_id` / `skill_text` on the `player_strike` **log entry**, not on `result` |

**Steps.**
1. Boot Mongo and the backend; `npm install` and `npm run dev` in `frontend/`.
2. Load the app with the browser console and network panel open. Treat **any**
   console error or non-2xx as a finding.
3. Walk the flows that touch renamed fields, in this order — each one exercises a
   different rename: create a character (skill bar populated?) → character sheet
   (`derived` armor/MR/xp_for_next rendering, not `NaN` or blank?) → biome
   explore → combat (mastery HUD, skill lines in the log, threat not power) →
   town (market, gemsmith, runesmith) → inventory (equip into `hands`, tooltips).
4. Fix on the spot, then re-walk.

**Verify.** Zero console errors and zero non-2xx across all six flows, on at
least three masteries with different resource systems (Knight/oaths,
Mage/library, Alchemist/combo-flow).

**Risk if skipped.** Total — this is the only surface a player sees, and it is
the least verified thing in the project.

**Size.** Half a day, most of it fixing rather than finding.

### RESULT — done

Created two characters end to end through the forge, fought and won, walked all
eight town tabs and five nav tabs. **Zero console errors, zero failed requests**
at the end. Four bugs fixed on the way (rows 1–4 above).

What the run confirmed was actually working: armor renders as `52 (34.3%)` rather
than 0, monsters show `THREAT 11` and never "power", the `hands` slot appears in
the equipment panel, `skill_bar` arrives populated (`Shield Bash / Iron Stance`
visible in the combat HUD), and the mastery HUD offers all five Oaths.

Two things I flagged and then disproved rather than "fixed":
- `REACT_APP_BACKEND_URL` is empty, which looks broken but is correct — the UI
  calls relative `/api` and craco's devServer proxies to port 8000.
- Gather nodes read `novice(missing)` in extracted text, but `ml-1` supplies the
  gap visually. Nothing to fix.

---

### 1.2 Promote the endpoint matrix to a committed test

**Why.** A throwaway harness found three dead routes by tracking *"never once
succeeded"* separately from *"crashed"*. That distinction is what surfaced
`GET /game/professions/mine` and the five Mage `KeyError: '_id'` routes — a route
that 4xx's on every possible input is as dead as one that throws, and only one of
those five surfaced under test because the other four failed argument validation
before reaching their bug. The signal should not live in a scratch file.

**What to build.** `tests/integration/test_endpoint_matrix.py`, behind a pytest
marker (`-m integration`) because it needs a live server and Mongo:

- Walk all 167 routes across a scenario set covering every mastery.
- **Fail** on any 5xx.
- **Fail** on any route with zero successes across the whole run.
- Print a per-route `ok / 4xx / 5xx` table plus the distinct 4xx reasons, so a
  newly-gated route is diagnosable rather than just red.

**Encode the contracts already learned** — these cost real time to discover and
must not be rediscovered:

```
combat sub-endpoints   require combat_id (Pydantic-validated, so a miss is 422)
knight oath            iron | wrath | bulwark | endurance | vanguard
bard mode-switch       song | dance
summon / fuse          require creature_id, and a *tamed* bestiary entry first
summon_mode            auto | manual        (not aggressive/defensive/balanced)
alchemist cf           action: analysis | adjustment | optimization | perfect_formula
                       perfect_formula also takes choice: delivery | conversion |
                       sequence | breakdown
alchemist pre-imbue    requires skill_id, and the skill must be imbuable
character/travel       continent          (not town_id)
teleporter/travel      continent_id       (not destination_id)
heritage milestones    continent + years
tame                   level >= 10, monster at <= 30% HP, not construct/undead
skin                   only after the monster dies (state["skinnable"])
```

**Also encode the multi-step chains**, since single calls can never reach these
handler bodies: `tame -> bestiary -> summon -> summon_mode -> fuse -> end_fusion
-> unsummon`, and `consecutive strikes -> CF accrues -> cf action`.

**Verify.** Deliberately break one route; confirm the matrix goes red. Same
sabotage discipline as the existing static checks.

**Size.** A day. Much of the logic already exists in the scratch harnesses.

---

### 1.3 Audit Mongo queries for the missing-field assumption

**Why.** The worst bug of the pass was not a typo, it was a wrong mental model:
in MongoDB `{"$lt": n}` **does not match documents where the field is absent.**
Every pre-existing character has no `schema_version`, so the migration query
matched *none of them* and the whole migration was inert for exactly the
documents it was written for. Measured: old query matched 0 of 2 seeded legacy
characters, fixed query matched both. There is no reason to believe that was the
only place holding this assumption.

**Steps.**
1. Grep every `$lt`, `$lte`, `$gt`, `$gte`, `$ne`, `$in`, `$nin` in queries
   against `characters`, `combats`, `users`.
2. For each, ask one question: *can a document predating this field exist, and
   must it match?* If yes, wrap in
   `{"$or": [{"f": {"$exists": False}}, {"f": None}, {"f": {"$lt": n}}]}`.
3. Pay particular attention to `$ne` — it *does* match missing fields, which is
   the opposite trap and equally surprising in the other direction.

**Verify.** For each query touched, seed a document without the field and assert
the query's match/no-match is what the code intends. Do this against real Mongo,
not a mock — a mock would have happily reproduced the original bug.

**Size.** Half a day.

---

## Tier 2 — before more feature work

### 2.1 Measure branch coverage of `combat_turn`, then close the gaps

**Why.** Identical golden logs after every refactor step *felt* like proof and
was not: `mastery/outgoing.py` read a bare `turn` and crashed every Knight sworn
to Vanguard, because no scenario selected that oath. Byte-identical output over
an unknown fraction of paths is a much weaker guarantee than it appears. **Get
the number.** Until then the golden suite's worth is unmeasured.

**Steps.**
1. `coverage run --branch` over the golden suite; report on `game_engine.py` and
   `backend/mastery/`.
2. List uncovered branches in `combat_turn` and the mastery modules.
3. Add golden scenarios until the mastery-state space is genuinely walked:
   - all five Knight oaths (the exact gap that shipped a crash)
   - every Druid form, and summon active vs not
   - both Bard modes, Crescendo at each threshold
   - Alchemist: each imbue element, CF at 0/5/10/15/20
   - Priest trigger states (`opponent_status`, `self_debuff`)
   - Mage schools and library loadouts
   - Rogue innate slots, Assassin stealth in and out, Lancer overload, Hunter pet
4. Adding scenarios adds new digests without altering existing ones, so this is
   safe to do incrementally.

**Verify.** Branch coverage of `combat_turn` and `mastery/` above a threshold you
commit to in CI. Then re-run the sabotage drill: break one rider per mastery and
confirm each is caught. The previous drill caught 10 of 12; the two misses are
what this item exists to fix.

**Do this before Tier 3.2.** Refactoring further without it repeats the exact
mistake that produced two of the eight bugs.

**Size.** Two days, mostly writing scenarios.

### RESULT — measured, gap closed, and the number is smaller than it felt

**The number, finally.** Branch coverage under the golden suite:

| | default `pytest` (11 representative) | full sweep, before | full sweep, after |
|---|---|---|---|
| `game_engine.py` | 34% | 39% | **41%** |
| `combat_turn` alone | 53% statements | — | — |
| `mastery/core.py` | 88% | 99% | 99% |
| `mastery/lancer.py` | 69% | 80% | 80% |
| `mastery/mitigation.py` | 60% | 68% | **71%** |
| `mastery/outgoing.py` *(where the crash was)* | 43% | 56% | **62%** |
| `mastery/skill_effects.py` | 42% | 44% | 45% |
| **TOTAL** | 37% | 42% | **44%** |

Two things worth being blunt about:

1. **The default `pytest` run executes only 11 scenarios**, not 1,584 — the full
   sweep is gated behind `GOLDEN_FULL=1`. So during the refactor, "golden logs
   identical" routinely meant *34% of `game_engine.py`*. That is a far weaker
   statement than it sounded like at the time.
2. **Tripling the scenario count bought 2 percentage points.** The resource-variant
   dimension went 1,584 -> 5,040 scenarios and moved the total 42% -> 44%. Honest
   conclusion: the remaining uncovered code is *not* gated on mastery resource
   state. It is gated on things the matrix does not vary at all — defeat paths,
   counter procs (`if random.random() < _cc`), stun handling, mage turn-stealing,
   legendary powers. Those need different levers (a monster strong enough to win,
   more seeds, status-bearing enemies), not more variants.

**What the variants did fix is the specific hole that shipped a crash**, and that
is provable rather than asserted. Perturbing the Vanguard rider in
`mastery/outgoing.py`:

```
OLD set (1,584 — Knights always swore Iron)  ->  0 scenarios moved   *** bug ships ***
NEW set (5,040 — all five oaths)             -> 40 scenarios moved   CAUGHT
```

The scenario expansion is purely additive: **0 of 1,584 pre-existing digests
changed**, 3,456 added, 0 removed. Variant 0 of each mastery deliberately keeps
the original unsuffixed key so its digest must still match byte for byte.

Sabotage drill re-run: Vanguard oath (40 moved), Vanguard stack threshold (11
moved), Alchemist Combo Flow (crash — caught). The two previous misses are now
both caught.

**Next lever for coverage** (not done): add a monster that can actually kill a
level-1 character, to reach the `state["active"] = False` defeat blocks and the
counter/death paths, which are the largest unexercised runs inside `combat_turn`.

---

### 2.2 Split the overloaded `skill["type"]` field

**Why.** `type` currently holds **two unrelated meanings**: mastery names
(`"knight"`, `"bard"`, `"druid"`) *and* mechanical kinds (`"strike"`, `"cast"`,
`"imbuable"`). The Alchemist's entire Combo Flow system gates on
`power_type == "strike" and type == "strike"`, which only **11 of 350 skills**
satisfy. One data edit tagging a skill with its mastery instead of its kind
silently disables a whole mastery mechanic — with no error anywhere. This is a
live trap, not a tidiness concern.

**Steps.**
1. Introduce `kind` (mechanical: `strike`/`cast`/`imbuable`/`buff`/`debuff`) and
   `mastery` (owner). Keep `type` populated during the transition.
2. Update every read site — `is_alch_strike` first, it is the one with a proven
   failure mode.
3. Add a test: every skill has a `kind` from a closed enum, every skill's
   `mastery` matches the mastery that grants it, and the count of skills passing
   the alchemist strike gate is greater than zero and stable.
4. Drop `type` once no reader remains.

**Verify.** Golden logs unchanged. Alchemist CF still accrues on consecutive
strikes (measured behaviour: 0 → 2 → 4 → 6, resetting on a miss).

**Risk.** Highest in this tier — touches 350 data entries and a gate with a
proven silent-failure mode. Do it after 2.1, so coverage can catch a regression.

**Size.** A day.

---

### 2.3 Structured 500 logging and a counter

**Why.** Every crash in this pass was found by reading uvicorn tracebacks by
hand. In production these are invisible: the client sees `Internal Server Error`,
nothing counts them, and nobody learns until a player complains. This converts
the whole bug class from *"someone mentions it eventually"* to *"you see it the
day it ships"* — and it is the cheapest item in the plan.

**Steps.**
1. A FastAPI exception handler logging route, method, user id, exception class
   and traceback at ERROR, with the response still a generic 500 to the client.
2. A 500 counter per route.
3. Log 4xx at INFO with the `detail`, so "this route now rejects everything"
   is visible too — that was the shape of three of the eight bugs.

**Verify.** A deliberately failing test route logs exactly once with the route
name present, and increments the counter.

**Size.** Two hours.

---

## Tier 3 — optional housekeeping

### 3.1 Split `server.py` into routers
5,900 lines, 167 routes. Real ergonomic win, zero correctness win. Do it when
touching a domain anyway, not as a project.

### 3.2 The remaining 46 `combat_turn` guards
Only two are worth it, and only because the control flow is genuinely
misleading: `_priest_process_skill` *replaces* the player-action branch rather
than adding to it, and `is_alch_strike` acts as a spine predicate. **Requires
2.1 first.** Reducing line count for its own sake is how two of the eight bugs
got in.

### 3.3 React Query adoption
Deferred from the original audit. Revisit only after 1.1, which may change what
the client actually needs.

---

## One design question — measured, not decided

`HP_PER_LEVEL = 4` is flat, so it progressively swamps stat-derived HP:

| Character | Level | Vitality | max_hp |
|---|---|---|---|
| Knight | 25 | 18 | **326** |
| Mage | 40 | 12 | **326** |

Two very different builds landing on the identical number is the symptom. At L95
the flat term contributes ~376 against ~200 from base stats, so **Vitality
investment stops mattering late.** That may be deliberate compression.

I am flagging the measurement and not changing it, because I misjudged one
balance curve earlier in this pass by extrapolating from a single data point (I
sampled the weakest tier-1 bow and concluded the damage curve was broken; with
best-in-tier weapons, turns-to-kill is flat at 0.7–1.6 from L1 to L95 and the
scaling is healthy). Curve changes should be your call, from intent.

---

## Sequencing

```
1.1 frontend ───────────────┐   highest risk, fully independent, do first
1.2 endpoint matrix ────────┤   cheapest while the contracts are fresh
1.3 mongo audit ────────────┘   independent

2.3 logging ────────────────┐   two hours, unblocks diagnosing everything after
2.1 coverage ───────────────┤   gates 2.2 and 3.2
2.2 type split ─────────────┘   needs 2.1's safety net

3.x ─────────────────────────── only when touching that area anyway
```

Rough total for Tiers 1 and 2: about a week. Tier 1 alone is roughly two days
and removes the shipping risk; **if only one item gets done, it should be 1.1**,
because it is the only unverified thing a player actually touches.
