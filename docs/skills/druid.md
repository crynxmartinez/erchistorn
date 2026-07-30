# Druid Mastery — 30 Skills + 12 Passives + 4 Seasons

**Role:** The Wildborn — a nature mage who tames beasts, summons them to fight alongside, and fuses with them to become something more than human. The Druid channels the Seasons to modify their skills on the fly. The Druid's power isn't just in their skills — it's in their **bestiary** and their **season**. Every creature tamed is a tool, a weapon, a companion.
**Masteries per trainer:** 3 (Druid + 2 others)
**Trainers teaching Druid:** Riverguard, Deepstone, Rindivar Grove, Veilgrove

---

## Druid Identity

**Core loop:** Choose Season → tame creatures → summon a pack → fuse with the right beast → adapt to any fight

- **Hybrid damage** — physical (shapeshifting, beast forms) and magical (nature spells, thorns, roots)
- **Best healer in the game** — multiple heal skills across all tiers, including party heals and regen
- **Summoner** — the only mastery that tames and commands creatures. The bestiary IS the power curve.
- **Shapeshifter** — transforms into beast forms (wolf, bear, eagle) for stat boosts
- **Terrain control** — roots, vines, groves, canopies reshape the battlefield
- **Pack fighter** — stronger with multiple summons active. Synergy scales exponentially.
- **Fusion** — merges with a summon to stack stats, gain skill riders, and unleash signature abilities
- **Adaptive** — the Druid's power depends on what they've tamed AND which Season they channel. Two Druids at level 50 can be wildly different based on their bestiary and season choice.
- **Seasonal** — channels Spring/Summer/Autumn/Winter to modify heal/strike/debuff/defend skills on the fly

### The Wildbond System

The Druid's unique mechanic — the thing no other mastery has — is the **Wildbond**: the ability to tame, summon, and fuse with creatures. This sits alongside skills as a core combat system, not a replacement for it.

**How the Wildbond works:**
- The Druid has three additional action buttons in combat: **Tame**, **Summon**, **Fuse**
- These are separate from the 5-skill bar — they don't compete with skills for slots
- Taming adds creatures to the **Bestiary** (cap: 50 tamed creatures)
- Summoning calls tamed creatures to fight alongside the Druid (Auto AI by default, or Manual control per-summon)
- Fusion merges a summon into the Druid, stacking stats and granting signature abilities
- The same skills a monster uses as a wild enemy are the skills it uses as a tamed summon

**Example combat flow:**
- Turn 1: Druid summons Grey Wolf (gains +15% might, +10% grace passive buff)
- Turn 2: Druid summons Cave Bear (gains +20% durability, +15% armor — now has 2 passive buffs stacking)
- Turn 3: Druid fuses with Grey Wolf (stats stack, gains bleeding attack rider, warded passive, and Predator's Fury signature ability)
- Turn 4-6: Druid is a wolf-human chimera, hitting with Druid skills + wolf attack rider + signature ability
- Turn 7: Fusion ends. Wolf reappears at full HP. Both summons continue fighting.

**Why this works:**
- **Taming as progression** — a level 30 Druid with 20 tamed creatures is dramatically stronger than one with 5. The bestiary is the power.
- **Diversity rewarded** — no duplicate summons, and pack synergy explicitly rewards having many different species
- **Adaptive fusion** — fusing with a wolf feels different from fusing with a bear. The Druid chooses the right tool for each fight.
- **Auto or Manual control** — summons default to AI (Auto), but the player can toggle any summon to Manual and pick its skill each turn. Auto for trash, Manual for bosses.

### Stat Focus

| Stat | Priority | Why |
|------|----------|-----|
| `essence` | **Primary** | Magic damage scaling + healing power + magic resistance. Druid's magical core. |
| `might` | **Primary** | Physical damage for shapeshifting and beast forms. Druid is hybrid. |
| `grace` | **Secondary** | Accuracy + evasion. Important for shapeshifted forms. |
| `durability` | **Secondary** | HP pool, staying power. Druid is not a tank but needs to survive. |
| `cognition` | **Secondary** | Skill capacity / utility. Also feeds taming success chance. |
| `insight` | **Minimal** | Some magical scaling, but less than essence. |
| `armor_bonus` | **Situational** | Gained through bark skin, stone skin, and shapeshifted forms. |

### Status Identity

| Status | Role |
|--------|------|
| `bleeding` | **Signature** — thorns, roots, and beast forms all draw blood |
| `ensnared` | **Signature** — roots and vines trap enemies. No one controls terrain like the Druid. |
| `poisoned` | **Secondary** — fungal blooms, venom-themed creatures |
| `warded` | **Secondary** — bark skin, stone skin, and defense skills |
| `inspired` | **Secondary** — nature's blessings and beast form buffs |
| `stunned` | **Rare** — earth guardian, heavy strikes. Not the Druid's main tool. |
| `evasive` | **Rare** — eagle form and wind-based skills |

### Trigger Identity

| Trigger | Role |
|---------|------|
| `always` | **Primary** — Druid is flexible, reactive, ready |
| `low_hp` | **Secondary** — healing blooms and emergency transformations |
| `opponent_status` | **Secondary** — vine prison and conditional strikes exploit already-debuffed enemies |
| `opening_move` | **Rare** — the Druid doesn't open with burst; they set up |
| `opponent_wounded` | **Rare** — the Druid doesn't chase kills; they wear down |

### What the Druid Does NOT Do

- **No stealth/hidden** (that's Rogue/Assassin/Hunter)
- **No heavy armor stacking** (that's Knight — Druid's defense is bark skin, not plate)
- **No pure burst damage** (that's Mage/Assassin — Druid is sustained, adaptive)
- **No enemy buff stealing** (that's Bard — Druid buffs themselves and their pack)
- **No constructs/undead summoning** (that's Necromancer — Druid summons living creatures only)
- **No single-target execute** (that's Assassin/Lancer — Druid wins through attrition and pack synergy)

### The Season System

The Druid's secondary mechanic — alongside the Wildbond — is the **Seasons**. The Druid channels one of four seasons at a time, which **modifies** their existing skills rather than adding new ones. This is like the Knight's Oath system: choose your season, and it changes how you fight.

**How Seasons work:**
- The Druid has **4 Seasons** — all unlocked at level 1. A Season slot sits below the skill bar.
- Only **one Season** can be active at a time. Switching is a free action (doesn't cost the turn).
- The Season **modifies** skills by power type — it doesn't replace them. A Spring Druid's Healing Bloom is still Healing Bloom, just stronger.
- Switching Seasons has a **2-turn cooldown** — you can't flip-flop every turn.
- The Season affects **Druid skills only** — summon skills are not modified.

**The 4 Seasons:**

| Season | Modifies | Effect | Playstyle |
|--------|----------|--------|-----------|
| **Spring** | Heal skills | +50% healing. Heals also grant `regen` (2 turns). Heal skills cost -1 cooldown. | Sustain — outlast anything |
| **Summer** | Strike skills | +25% damage. Strikes also apply `burning` (2 turns). Strike skills cost -1 cooldown. | Aggression — burn it down |
| **Autumn** | Debuff skills | Debuffs last +2 turns. Debuffs also drain 1 random stat from enemy to Druid. Debuff skills cost -1 cooldown. | Attrition — weaken and grow |
| **Winter** | Defend & Control skills | `ensnared`/`stunned` last +1 turn. Defense skills also grant `evasive` (1 turn). Defend skills cost -1 cooldown. | Control — lock them down |

**Example:**

```
Druid in Summer mode uses Thorn Barrage (strike, magical):
  Normal:  damage + bleeding + enemy grace -1
  Summer:  +25% damage + bleeding + burning + enemy grace -1
  (strike cooldown reduced by 1)

Druid switches to Spring. 2-turn cooldown begins.
Next turn: Druid uses Healing Bloom (heal):
  Normal:  10% heal + warded + essence +1
  Spring:  15% heal + regen (2 turns) + warded + essence +1
  (heal cooldown reduced by 1)
```

**Why this works:**
- **Adaptive** — the Druid reads the fight and picks the right Season. Boss charging a nuke? Winter to control. Party dying? Spring to heal. Need to burn? Summer.
- **No power creep** — the Season modifies *existing* skills. The Druid doesn't get new abilities, they get better use of what they have.
- **Commitment with flexibility** — 2-turn cooldown prevents flip-flopping, but switching is free, so the Druid *can* adapt mid-fight
- **Unique identity** — no other mastery modifies their own skill categories on the fly
- **Synergy with Wildbond** — Seasons affect Druid skills while the pack handles the rest. Spring Druid + wolf pack = unkillable. Summer Druid + bear fusion = devastation.

### Taming

Available only to Druids. Appears as a third action button alongside Strike and Summon.

**Taming rules:**

| Rule | Detail |
|------|--------|
| HP threshold | Enemy must be below **30% HP** (normal), **25%** (mini-boss), **15%** (boss), **10%** (legendary), **5%** (event boss) |
| One attempt | One tame attempt per enemy per combat |
| Success chance | `Druid cognition vs enemy resistance` — higher cognition = higher chance |
| Base chance (normal) | 40% at equal cognition. +5% per cognition point above enemy resistance. -5% per point below. Cap: 10%-90% |
| Base chance (mini-boss) | 25% at equal cognition. +4% per point above. -4% per point below. Cap: 5%-60% |
| Base chance (boss) | 15% at equal cognition. +3% per point above. -3% per point below. Cap: 5%-50% |
| Base chance (legendary) | 5% at equal cognition. +2% per point above. -2% per point below. Cap: 2%-25% |
| Base chance (event boss) | 2% at equal cognition. +1% per point above. -1% per point below. Cap: 1%-10% |
| Success | Monster joins bestiary permanently, removed from combat (not killed) |
| Bestiary cap | **50 tamed creatures total** — choose wisely |

**Failure penalties (scale with tier):**

| Tier | Failure Effect |
|------|---------------|
| Normal | Monster becomes **enraged** — might +3, attacks immediately |
| Mini-Boss | Monster becomes **enraged** — might +4, grace +2, attacks immediately |
| Boss | Monster becomes **furious** — might +5, grace +3, attacks immediately, gains 1 extra turn |
| Legendary | Monster becomes **unstoppable** — all stats +5, attacks immediately, gains 2 extra turns, cleanses all debuffs |
| Event Boss | Monster becomes **cataclysmic** — all stats +8, full heal, attacks immediately, gains 3 extra turns, cleanses all debuffs, enrages all allies |

**Cannot tame:**

| Category | Why |
|----------|-----|
| Constructs/Mechanical | No soul — machines can't be tamed |
| Undead | No living essence to connect with |
| Other players | Obviously |

### Summoning

Available only to Druids. Opens a dropdown of all tamed creatures. Each creature has a **personality** (Aggressive, Protective, Opportunist, Guardian, Taunting) that shapes its Auto AI behavior — see `monster-profiles.md` § 5. Personality for full details.

**Summon rules:**

| Rule | Detail |
|------|--------|
| Max active summons | **1 per 5 Druid levels** (Level 5 = 1, Level 10 = 2, ... Level 50 = 10) |
| No duplicates | Can't summon 2 of the same species |
| Action cost | Summoning costs the Druid's turn action |
| Summon HP | Equal to what the creature would have at the Druid's level |
| Summon death | If a summon dies in combat, it returns to the bestiary. Re-summonable next combat. Summons don't permanently die. |
| Buff duration | Passive buff is active while summon is on the field. If summon dies or is unsummoned, buff is lost. |
| Stat scaling | Tamed summons auto-scale to the Druid's level. A wolf tamed at level 10 fights at level 45 when the Druid is level 45. |

**Summon Command System — Auto vs Manual:**

Each summon has a **mode toggle** on the battle screen: **Auto** or **Manual**. This is per-summon — leave some on Auto while controlling others.

| Mode | How It Works |
|------|-------------|
| **Auto** | AI picks the skill based on HP thresholds (default — hands-off) |
| **Manual** | Player picks which of the summon's 3 skills to use this turn |

**Auto AI priority (default behavior):**

```
Each active summon on Auto:
  1. Enemy above 30% HP → Attack skill
  2. Enemy below 30% HP → Attack skill (going for kill)
  3. Druid below 50% HP → Defense skill (protecting the Druid)
  4. Summon below 30% HP → Utility skill (surviving)
  5. Druid fused with this summon → N/A (inside the Druid)
```

**Manual controls:**
- The summon's 3 skills appear as buttons below the summon's HP bar
- A **Pass** button is also available — the summon does nothing this turn (save stamina, avoid counterattack)
- Skills on cooldown or without enough stamina/MP are greyed out
- In Auto mode, the AI's chosen skill is **highlighted as a preview** before execution — the player can see what the AI picked and override to Manual if they disagree

**Quick commands bar** (global, affects all active summons at once):

| Button | Effect |
|--------|--------|
| **All Auto** | Set every summon to Auto mode (one click for trash fights) |
| **All Attack** | Every summon uses their Attack skill this turn (burn phase) |
| **All Defend** | Every summon uses their Defense skill this turn (survival phase) |

**Fused summons don't appear** — if a summon is fused into the Druid, it's not on the summon bar. Its skills are active as riders/passives on the Druid.

**When Manual shines:**

| Scenario | Auto Would Do | Manual Lets You Do |
|----------|--------------|-------------------|
| Boss charging AoE nuke | Wolf keeps attacking | Wolf uses Guard Howl to warded the Druid |
| Enemy at 5% HP | Bear uses Iron Hide (bear HP low) | Bear uses Crushing Slam to finish the kill |
| Druid at 80% HP, summon at 80% | Both attack | Eagle uses Scout Eye for cognition buff before Druid's big spell |
| Stamina management | AI burns stamina fast | Pass on wolf this turn to regen stamina |
| Pack coordination | Each summon acts independently | Wolf Pack Calls, bear Slams, eagle Dives — all in one turn |

**Balance:** Manual is strictly better in decision quality, but the summon's stats and skills don't change. Auto is never punished — it's the baseline. Manual is an optional skill ceiling for engaged players.

### Formation System

On top of Auto/Manual, each summon can be assigned a **Formation** — a persistent targeting directive that stays until changed. Formations work in **both** Auto and Manual mode. In Auto, the AI respects the formation when choosing targets. In Manual, the formation is a visual reminder of the summon's role.

| Formation | Behavior | Example |
|-----------|----------|---------|
| **Front** | Summon targets the enemy directly — melee pressure, draws some aggro | Wolf: always strikes the closest enemy |
| **Back** | Summon stays at range — prioritizes Utility/Defense skills, only attacks if no utility available | Eagle: scouts, buffs, and only dives when safe |
| **Protect [Ally]** | Summon prioritizes Defense skills when the target ally is below 70% HP. Otherwise attacks normally. | Bear: "Protect Druid" — tanks for the Druid |
| **Focus [Enemy]** | Summon always targets the specified enemy with Attack skills, ignoring other targets | Snake: "Focus Mage" — locks down the enemy caster |

**How Formations work:**
- Set during the Druid's turn (free action — doesn't cost the summon's action)
- Persist across turns until changed
- Each summon has one Formation slot
- In Auto mode, the AI picks the skill normally but respects the Formation's targeting rules
- In Manual mode, the player picks the skill AND the Formation guides the default target
- **Protect** overrides the AI's normal "Druid below 50% HP" threshold — it uses 70% for the *specified* ally instead
- **Focus** overrides the AI's normal target selection — the summon always hits the focused enemy

**Example: Full pack with Formations**

```
Wolf     — Front              → attacks nearest enemy every turn
Bear     — Protect Druid      → uses Defense when Druid < 70% HP, otherwise attacks
Eagle    — Back               → prioritizes Utility (Scout Eye), attacks only if no utility available
Snake    — Focus Enemy Mage   → always attacks the enemy mage with Attack skill
Treant   — Protect Priest     → uses Defense when Priest < 70% HP, otherwise attacks
```

**Why this matters:**
- **Personality without losing control** — Formations let the player shape how each summon behaves without micromanaging every turn
- **Team play** — in group content, "Protect Priest" and "Focus Mage" are critical for coordination
- **Auto mode becomes viable for bosses** — with good Formations, Auto can handle most fights. Manual is for fine-tuning.
- **Quick commands still work** — "All Attack" overrides Formations for one turn, then Formations resume

### Pack Synergy

Having multiple summons active creates **exponential synergy**:

| Active Summons | Synergy Name | Effect |
|----------------|-------------|--------|
| 1-2 | — | Normal — each acts independently |
| 3+ | **Pack Bond** | All summons +20% damage. Druid +5% all stats |
| 5+ | **Pack Hunt** | All summons +1 hit per attack. Druid +10% all stats |
| 7+ | **Pack Alpha** | Summons gain an extra action **every other turn**. Druid +15% all stats |
| 10 (max) | **The Wild Sovereign** | Every summon gains every other summon's passive buff. Druid +20% all stats. The Druid becomes a one-person army. |

**Note on Pack Alpha:** Extra action every *other* turn means on turns 1, 3, 5, etc. each summon acts once. On turns 2, 4, 6, etc. each summon acts twice. With 10 summons that's 10-20 actions per turn — already devastating. The level 90 passive (Wild Sovereign) upgrades this to *every* turn.

### Fusion

The Druid chooses **Fuse** → chooses an active summon → the summon merges into the Druid.

**Fusion effects:**

| Effect | Detail |
|--------|--------|
| Stat stacking | Druid stats = Druid stats + Summon stats (fully stacked, not averaged) |
| Passive buff | Summon's buff stays active on the Druid |
| Attack rider | Every Druid strike also triggers the summon's **Attack skill** as a bonus effect |
| Defense passive | Summon's **Defense skill** becomes a permanent passive on the Druid while fused |
| Signature ability | Druid gains access to the summon's **Signature Fusion Ability** |
| Visual | Druid's appearance changes — wolf claws, bear bulk, eagle wings, snake scales |
| Duration | **3 turns** |
| Summon state | Summon disappears (inside the Druid). Reappears at **full HP** when fusion ends. |
| Recovery | **2 turns** before that summon can fuse again (cooldown) |
| No cooldown on fusion itself | Druid can immediately fuse with a different summon |

**Fusion example — Wolf:**

```
Druid fuses with Grey Wolf (Level 45):

Stats gained:
  +15% might, +10% grace (passive buff)
  + Wolf's might, grace, durability (stat stacking)

Skill riders:
  Every Druid strike also applies: bleeding + enemy might -2 (Wolf's Attack: Savage Bite)
  Druid is permanently warded (Wolf's Defense: Guard Howl)

New ability:
  Predator's Fury — 3-hit physical, all hits bleed, 20% lifesteal (Signature Fusion)

Duration: 3 turns
After fusion: Wolf reappears at full HP, can't fuse again for 2 turns
```

**Multi-Fusion (Level 60 passive):** At high levels, the Druid can fuse with **two summons simultaneously**. This stacks both creatures' stats, both attack riders, both defense passives, and grants both signature abilities. The Druid becomes a chimera — part wolf, part eagle, part human. This is the Druid's endgame fantasy.

---

## Passives — Auto-Learned, Unlocked Every 10 Levels (Every 5 at Endgame)

These passives enhance the Wildbond system. They are auto-learned — no gold, no trainer, no choice. The Druid grows into their power naturally. Levels 85-100 unlock more frequently as the Druid approaches their full potential.

| # | Name | Level | Effect |
|---|------|-------|--------|
| 1 | Wild Heart | 10 | **Unlocks the Tame button.** +5% tame success chance on normal creatures. The Druid hears the call of the wild. |
| 2 | Pack Leader | 20 | +1 max active summon above the level-based cap. The pack grows. |
| 3 | Bonded Senses | 30 | While a summon is active, the Druid also gains the summon's Attack skill as a passive rider (weaker version — no status apply, just damage). The Druid and the pack fight as one. |
| 4 | Fusion Adept | 40 | Fusion duration extended to **4 turns**. Recovery reduced to **1 turn**. The Druid holds the fusion longer and recovers faster. |
| 5 | Apex Tamer | 50 | **Unlocks taming mini-boss creatures.** +10% tame success chance on all creatures. The Druid's reputation spreads through the wild. |
| 6 | Twin Fusion | 60 | **Can fuse with 2 summons simultaneously** (Multi-Fusion). Both creatures' stats, attack riders, defense passives, and signature abilities stack. The Druid becomes a chimera. |
| 7 | Sovereign's Will | 70 | Pack Synergy thresholds reduced: **2+** = Pack Bond, **4+** = Pack Hunt, **6+** = Pack Alpha, **9+** = The Wild Sovereign. The Druid commands the pack with less overhead. |
| 8 | Eternal Bond | 80 | Summons that die in combat can be **re-summoned same combat** (1 turn cooldown instead of next combat). The bond cannot be broken. |
| 9 | Mythic Tamer | 85 | **Unlocks taming boss creatures.** +15% tame success chance on boss+ creatures. Legendary and event bosses remain tameable at base chances. The Druid's name is spoken in fear by the wild itself. |
| 10 | Wild Sovereign | 90 | All Pack Synergy bonuses **doubled**. Pack Bond = +40% damage, +10% stats. Pack Hunt = +2 hits, +20% stats. Pack Alpha = extra action every turn (upgraded from every other). Wild Sovereign = double-shared buffs, +40% stats. |
| 11 | Eternal Wild | 95 | Fusion has **no recovery time**. The Druid can fuse, unfuse, and re-fuse freely. Multi-Fusion can be re-entered immediately after ending. |
| 12 | Alpha World | 100 | Max active summons cap **removed** (still 1 per 5 levels, but no hard cap of 10 — 20 summons at level 100). The Druid is the wild. The wild is the Druid. |

### Passive Synergy

```
Level 10:  Tame unlocked → the bestiary begins. The Druid's journey truly starts.
Level 20:  +1 summon slot → earlier pack synergy, more passive buffs stacking
Level 30:  Attack rider from summons → Druid's strikes hit harder even without fusing
Level 40:  Fusion 4 turns / 1 recovery → fusion is the default state, not a burst window
Level 50:  Mini-boss taming → access to 2-buff creatures. Power spike.
Level 60:  MULTI-FUSION → the Druid's endgame fantasy. Two creatures, two riders, two signatures.
Level 70:  Lower synergy thresholds → Pack Bond at 2 summons, Pack Hunt at 4, Pack Alpha at 6
Level 80:  Same-combat re-summon → summons are effectively immortal in combat
Level 85:  Boss taming → access to 3-buff, 5-skill, 2-signature, boss-aura creatures
Level 90:  PACK DOUBLED → all synergy bonuses doubled. The pack is an army now.
Level 95:  ETERNAL FUSION → no recovery time. Fuse freely, swap freely, stay fused.
Level 100: NO CAP → 20 summons at level 100. The Druid IS the wild.
```

**The full build at level 100:**
- Pack Synergy bonuses doubled: Pack Bond = +40% summon damage, +10% Druid stats. Pack Hunt = +2 hits, +20% stats. Pack Alpha = extra action every turn, +30% stats. Wild Sovereign = double-shared buffs, +40% stats.
- No hard cap on active summons (still 1 per 5 levels = 20 at level 100)
- Fusion has no recovery time — the Druid can fuse, unfuse, and re-fuse freely
- Multi-Fusion active — two summons fused simultaneously
- All creature tiers tameable (normal through event boss)
- "The Druid doesn't command the wild. The Druid is the wild, and the wild obeys itself."

---

## Skill Structure

All skills use the new format — no `power` or `skill_capacity_cost`.

| Field | Description |
|-------|-------------|
| `power_type` | strike, defend, heal, debuff, buff |
| `damage_type` | physical, magical, true (strikes only) |
| `trigger` | always, low_hp, opponent_wounded, opponent_status, opening_move, self_debuff |
| `status_apply` | Status inflicted on enemy |
| `self_status` | Status applied to self |
| `stat_mod` | Temporary stat changes — `{"self": {...}, "enemy": {...}}` |
| `mod_duration` | How many turns stat_mod lasts |
| `heal_percent` | Heals X% of max HP (heal skills only) |
| `hits` | Number of hits per use (default 1) |

**Available stat_mod targets:**
- `might` — physical damage scaling
- `grace` — accuracy + evasion
- `cognition` — skill capacity / utility
- `insight` — magical damage scaling
- `essence` — magic resistance + healing power
- `durability` — HP / resilience
- `armor_bonus` — physical damage reduction

---

## Tier Overview

| Tier | Level Req | Gold Cost | Learn Time | Count | Buffs | Strikes | Debuffs | Heals | Defends |
|------|-----------|-----------|------------|-------|-------|---------|---------|-------|---------|
| Basic | 1 | 50g | 5 min | 6 | 2 | 1 | 1 | 1 | 1 |
| Advanced | 3 | 150g | 30 min | 7 | 2 | 2 | 2 | 1 | 0 |
| Expert | 8 | 400g | 1 hr | 7 | 3 | 2 | 0 | 1 | 1 |
| Master | 15 | 1000g | 1 hr | 8 | 5 | 1 | 0 | 2 | 0 |
| Legendary | 20 | 2500g | 1 day | 2 | 0 | 2 | 0 | 0 | 0 |

---

## Basic Tier (Level 1, 50g, 5min) — 2 Buffs, 1 Strike, 1 Debuff, 1 Heal, 1 Defend

### 1. Entangling Roots
```python
{"id": "entangling_roots", "name": "Entangling Roots", "cooldown": 3,
 "power_type": "debuff", "damage_type": "magical", "trigger": "always",
 "status_apply": "ensnared",
 "stat_mod": {"enemy": {"grace": -2, "might": -2}}, "mod_duration": 2}
```
**Description:** The Druid presses a hand to the earth as thick roots erupt and coil around every foe.
**Narrative:** The Druid's palm touches soil. The soil answers. Roots — thick, gnarled, older than the battle — burst upward and wrap around the enemy's ankles. The enemy stumbles. The roots tighten. The earth has decided they're staying.

---

### 2. Thorn Barrage
```python
{"id": "thorn_barrage", "name": "Thorn Barrage", "cooldown": 2,
 "power_type": "strike", "damage_type": "magical", "trigger": "always",
 "status_apply": "bleeding",
 "stat_mod": {"enemy": {"grace": -1}}, "mod_duration": 2}
```
**Description:** The forest floor erupts with razor-sharp spikes as countless enchanted thorns launch at the enemy.
**Narrative:** The Druid stamps a foot. The ground between them and the enemy becomes a bed of thorns — not gradual, not growing, but instant. The spikes are thin, sharp, and hungry. The enemy's legs become a map of cuts. The blood feeds the soil. The soil asks for more.

---

### 3. Ancient Bark
```python
{"id": "ancient_bark", "name": "Ancient Bark", "cooldown": 4,
 "power_type": "defend", "trigger": "always",
 "self_status": "warded",
 "stat_mod": {"self": {"armor_bonus": 4}}, "mod_duration": 3}
```
**Description:** Tree bark spreads across the Druid's body like living armor, hardening their skin against attack.
**Narrative:** The Druid's skin darkens. Not dirt, not shadow — bark. It crawls up their arms, across their chest, over their face. It doesn't restrict movement. It reinforces it. The first blow that lands sounds like an axe hitting oak. The oak doesn't care.

---

### 4. Healing Bloom
```python
{"id": "healing_bloom", "name": "Healing Bloom", "cooldown": 4,
 "power_type": "heal", "trigger": "low_hp",
 "self_status": "warded",
 "heal_percent": 0.10,
 "stat_mod": {"self": {"essence": 1}}, "mod_duration": 2}
```
**Description:** A radiant blossom opens, releasing soothing pollen that mends wounds.
**Narrative:** The Druid cups their hands. A flower grows — not from the ground, but from their palms. It opens slowly, and the pollen that drifts out smells like rain and morning. The wounds close. The pain fades. The flower wilts, content. Triggers when HP is low.

---

### 5. Nature's Whisper
```python
{"id": "natures_whisper", "name": "Nature's Whisper", "cooldown": 4,
 "power_type": "buff", "trigger": "always",
 "self_status": "inspired",
 "stat_mod": {"self": {"cognition": 3, "grace": 2}}, "mod_duration": 3}
```
**Description:** Birds and beasts gather to share information. The Druid reads the battlefield through the eyes of the wild.
**Narrative:** The Druid tilts their head. Not listening — receiving. A sparrow lands on their shoulder. A fox pauses at the treeline. They tell the Druid what they see: the enemy's position, their fear, the gap in their guard. The Druid opens their eyes. They know everything the forest knows.

---

### 6. Stone Skin
```python
{"id": "stone_skin", "name": "Stone Skin", "cooldown": 4,
 "power_type": "buff", "trigger": "always",
 "self_status": "warded",
 "stat_mod": {"self": {"armor_bonus": 3, "durability": 2}}, "mod_duration": 3}
```
**Description:** Rock and bark reinforce the Druid's body, increasing natural resilience.
**Narrative:** The Druid's skin shifts — not fully bark, not fully stone, but something between. Grey and brown patches appear along their forearms, their shins, their neck. The enemy's blade lands and skids. The Druid doesn't flinch. They've been hit by harder things than steel.

---

## Advanced Tier (Level 3, 150g, 30min) — 2 Buffs, 2 Strikes, 2 Debuffs, 1 Heal

### 7. Spirit Wolf
```python
{"id": "spirit_wolf", "name": "Spirit Wolf", "cooldown": 4,
 "power_type": "strike", "damage_type": "magical", "trigger": "always",
 "status_apply": "bleeding",
 "stat_mod": {"enemy": {"might": -2, "grace": -2}}, "mod_duration": 2}
```
**Description:** A ghostly wolf steps from the forest mist and stands beside the Druid before lunging at the enemy.
**Narrative:** The Druid whistles — not loud, not human. The mist answers. A shape forms: silver, translucent, eyes like moonlight. The spirit wolf doesn't growl. It doesn't need to. It simply moves, and the enemy bleeds before they understand what happened. The wolf returns to the mist. It will return again.

---

### 8. Wild Growth
```python
{"id": "wild_growth", "name": "Wild Growth", "cooldown": 5,
 "power_type": "heal", "trigger": "low_hp",
 "self_status": "inspired",
 "heal_percent": 0.12,
 "stat_mod": {"self": {"essence": 2, "durability": 2}}, "mod_duration": 3}
```
**Description:** Flowers bloom instantly while vines wrap gently around the wounded, accelerating nature to heal.
**Narrative:** The Druid spreads their arms. The ground erupts — not with violence, but with life. Flowers bloom in seconds. Vines uncoil and wrap around wounds, gentle as bandages. The pain doesn't just fade; it's absorbed. The forest takes it. The forest doesn't mind. Triggers when HP is low.

---

### 9. Vine Prison
```python
{"id": "vine_prison", "name": "Vine Prison", "cooldown": 4,
 "power_type": "debuff", "damage_type": "magical", "trigger": "opponent_status",
 "status_apply": "ensnared",
 "stat_mod": {"enemy": {"grace": -3, "might": -3}}, "mod_duration": 3}
```
**Description:** Twisting vines weave into an inescapable cage around the enemy.
**Narrative:** The enemy is already hindered — bleeding, stunned, slowed. The Druid raises a hand. Vines erupt from every direction, weaving together like fingers lacing. The cage forms in a heartbeat. The enemy can see through the gaps. They can't fit through them. The Druid watches. The vines tighten. Only triggers when the enemy has a status effect.

---

### 10. Fungal Bloom
```python
{"id": "fungal_bloom", "name": "Fungal Bloom", "cooldown": 4,
 "power_type": "debuff", "damage_type": "magical", "trigger": "always",
 "status_apply": "poisoned",
 "stat_mod": {"enemy": {"might": -3, "cognition": -2}}, "mod_duration": 3}
```
**Description:** Glowing spores drift across the battlefield, poisoning enemies and clouding their minds.
**Narrative:** The Druid breathes out. The breath isn't air — it's spores. Blue, luminescent, slow. They drift like snow, and every enemy they touch begins to cough. The poison isn't fast. It's patient. It seeps into the lungs, the blood, the thoughts. The enemy's swings get weaker. Their decisions get worse. The spores keep drifting.

---

### 11. Nature's Grasp
```python
{"id": "natures_grasp", "name": "Nature's Grasp", "cooldown": 4,
 "power_type": "strike", "damage_type": "magical", "trigger": "always",
 "status_apply": "ensnared",
 "stat_mod": {"enemy": {"grace": -2, "armor_bonus": -2}}, "mod_duration": 2}
```
**Description:** The ground itself reaches for intruders, pulling enemies toward grasping roots.
**Narrative:** The enemy tries to advance. The ground disagrees. Hands — not hands, roots shaped like hands — burst from the earth and grab their ankles. The enemy is pulled off-balance, dragged forward into a space they didn't choose. The Druid is waiting. The roots are helping.

---

### 12. Beast Form
```python
{"id": "beast_form", "name": "Beast Form", "cooldown": 5,
 "power_type": "buff", "trigger": "always",
 "self_status": "inspired",
 "stat_mod": {"self": {"might": 4, "grace": 2, "durability": 2}}, "mod_duration": 3}
```
**Description:** Bones and muscles reshape into a powerful animal. The Druid transforms into a wild beast.
**Narrative:** The Druid drops to all fours. Their spine curves, their fingers curl, their jaw extends. It's not painful — it's liberating. When the transformation completes, a beast stands where the Druid was. It's faster. It's stronger. It's angrier. The enemy just lost their advantage.

---

### 13. Solar Bloom
```python
{"id": "solar_bloom", "name": "Solar Bloom", "cooldown": 5,
 "power_type": "buff", "trigger": "always",
 "self_status": "inspired",
 "stat_mod": {"self": {"might": 3, "insight": 3}}, "mod_duration": 3}
```
**Description:** Golden vines burst into radiant flowers as the Druid harnesses the warmth of the sun.
**Narrative:** The Druid raises their hands. The light that gathers isn't moonlight — it's solar. Warm, gold, alive. It sinks into the Druid's skin like warmth into cold stone. Muscles swell. Magic sharpens. The enemy sees the Druid glow and understands: the sun is on their side.

---

## Expert Tier (Level 8, 400g, 1hr) — 3 Buffs, 2 Strikes, 1 Heal, 1 Defend

### 14. Bear Form
```python
{"id": "bear_form", "name": "Bear Form", "cooldown": 5,
 "power_type": "buff", "trigger": "always",
 "self_status": "warded",
 "stat_mod": {"self": {"might": 5, "armor_bonus": 4, "durability": 3}}, "mod_duration": 3}
```
**Description:** The Druid roars as enormous claws emerge. They transform into a massive bear.
**Narrative:** The Druid doesn't just shift — they erupt. The transformation is violent, fast, and loud. Where a person stood, a bear now towers — massive, brown, furious. The ground shakes when it plants its feet. The enemy looks up. Way up. The bear shows its teeth. The enemy reconsiders.

---

### 15. Eagle Form
```python
{"id": "eagle_form", "name": "Eagle Form", "cooldown": 5,
 "power_type": "buff", "trigger": "always",
 "self_status": "evasive",
 "stat_mod": {"self": {"grace": 5, "might": 2}}, "mod_duration": 3}
```
**Description:** Feathers burst forth as wings spread wide. The Druid takes the form of a giant eagle.
**Narrative:** The Druid leaps. The leap doesn't end. Feathers replace skin, wings replace arms, and the air catches them. The giant eagle climbs, circles, and dives. The enemy swings upward and hits nothing but sky. The talons arrive from above. The beak follows.

---

### 16. Earth Guardian
```python
{"id": "earth_guardian", "name": "Earth Guardian", "cooldown": 5,
 "power_type": "strike", "damage_type": "physical", "trigger": "always",
 "status_apply": "stunned",
 "stat_mod": {"enemy": {"might": -3, "armor_bonus": -3}}, "mod_duration": 3}
```
**Description:** The ground trembles as a towering guardian of rock rises to protect the Druid and crush the enemy.
**Narrative:** The Druid stamps. The earth rises. Not a mound — a figure. A guardian of stone, ten feet tall, moss-covered, patient. It turns toward the enemy with the speed of geology. The fist comes down. The ground cracks. The enemy is in the crack.

---

### 17. Forest Wrath
```python
{"id": "forest_wrath", "name": "Forest Wrath", "cooldown": 5,
 "power_type": "strike", "damage_type": "magical", "trigger": "always",
 "status_apply": "bleeding",
 "stat_mod": {"enemy": {"might": -3, "grace": -3, "armor_bonus": -2}}, "mod_duration": 3}
```
**Description:** Branches lash out while ancient trees awaken in anger. The forest itself attacks the enemy.
**Narrative:** The Druid speaks a word in a language older than people. The forest hears. The trees — old, patient, tired of being cut — awaken. Branches whip like flails. Roots heave like fists. The enemy is in the forest now, and the forest has been waiting for someone to be angry at.

---

### 18. Moonlight Blessing
```python
{"id": "moonlight_blessing", "name": "Moonlight Blessing", "cooldown": 5,
 "power_type": "buff", "trigger": "always",
 "self_status": "inspired",
 "heal_percent": 0.08,
 "stat_mod": {"self": {"essence": 3, "grace": 2, "insight": 2}}, "mod_duration": 4}
```
**Description:** Silver light gently washes over the Druid, empowering them beneath the moon's glow.
**Narrative:** The moon isn't visible — it's day, or the canopy blocks it. But the light comes anyway. Silver, soft, patient. It settles on the Druid like dew. Wounds close. Magic sharpens. The body lightens. The moon has always favored those who speak for the wild. The Druid is its voice.

---

### 19. Seed of Life
```python
{"id": "seed_of_life", "name": "Seed of Life", "cooldown": 5,
 "power_type": "heal", "trigger": "low_hp",
 "self_status": "warded",
 "heal_percent": 0.15,
 "stat_mod": {"self": {"essence": 3, "durability": 2}}, "mod_duration": 3}
```
**Description:** A glowing seed takes root and pulses with energy, restoring life to the wounded.
**Narrative:** The Druid presses a seed into their own chest. It sinks in. For a moment, nothing. Then the glow — green, warm, spreading from the heart outward. Roots grow inward, not outward. They find the wounds, the breaks, the exhaustion. They replace it with life. The Druid rises. The seed has bloomed. Triggers when HP is low.

---

### 20. Living Canopy
```python
{"id": "living_canopy", "name": "Living Canopy", "cooldown": 5,
 "power_type": "defend", "trigger": "always",
 "self_status": "warded",
 "stat_mod": {"self": {"armor_bonus": 4, "essence": 3}}, "mod_duration": 3}
```
**Description:** Towering trees grow instantly, shielding the Druid from harm beneath a living canopy.
**Narrative:** The Druid raises both hands. The trees obey. They don't grow — they erupt. In seconds, a canopy of branches and leaves forms overhead, thick enough to block the sky. Arrows stick in the wood. Spells dissipate against the leaves. The Druid stands beneath it, safe, patient, rooted.

---

## Master Tier (Level 15, 1000g, 1hr) — 5 Buffs, 1 Strike, 2 Heals

### 21. Nature's Rebirth
```python
{"id": "natures_rebirth", "name": "Nature's Rebirth", "cooldown": 7,
 "power_type": "heal", "trigger": "low_hp",
 "self_status": "inspired",
 "heal_percent": 0.30,
 "stat_mod": {"self": {"essence": 4, "durability": 3, "grace": 2}}, "mod_duration": 4}
```
**Description:** Tiny sprouts surround the fallen as life slowly returns. The Druid revives through the power of nature.
**Narrative:** The Druid is on the ground. The blood feeds the earth. And the earth gives it back. Sprouts erupt from the soil around the Druid's body — not random, but deliberate. They weave together, form a cocoon of green, and pulse. The Druid's eyes open. The wounds are gone. The forest has decided the Druid isn't done yet. Triggers when HP is low.

---

### 22. Verdant Storm
```python
{"id": "verdant_storm", "name": "Verdant Storm", "cooldown": 6,
 "power_type": "strike", "damage_type": "magical", "trigger": "always",
 "hits": 2,
 "status_apply": "bleeding",
 "stat_mod": {"enemy": {"grace": -3, "armor_bonus": -3, "might": -2}}, "mod_duration": 3}
```
**Description:** A raging green cyclone engulfs enemies in a storm of leaves, branches, and thorns.
**Narrative:** The Druid spins. The wind follows. Leaves become blades, branches become flails, and the cyclone builds — green, roaring, alive. It sweeps across the enemy like a lawnmower made of anger. When it passes, the enemy is bleeding from a hundred cuts and the ground is covered in green. The forest is tidy like that.

---

### 23. Animal Bond
```python
{"id": "animal_bond", "name": "Animal Bond", "cooldown": 6,
 "power_type": "buff", "trigger": "always",
 "self_status": "inspired",
 "stat_mod": {"self": {"might": 4, "grace": 3, "essence": 2}}, "mod_duration": 4}
```
**Description:** Every companion responds with renewed vigor. The Druid strengthens all summoned beasts and themselves.
**Narrative:** The Druid speaks — not a word, but a feeling. Every beast on the battlefield feels it: the wolf, the eagle, the spirit, the bear. A pulse of kinship, of pack, of belonging. They straighten. They sharpen. The enemy sees the animals change and understands: they're not fighting a Druid. They're fighting a family.

---

### 24. River's Blessing
```python
{"id": "rivers_blessing", "name": "River's Blessing", "cooldown": 6,
 "power_type": "heal", "trigger": "always",
 "self_status": "warded",
 "heal_percent": 0.15,
 "stat_mod": {"self": {"essence": 3, "grace": 3, "durability": 2}}, "mod_duration": 3}
```
**Description:** Crystal-clear water flows around the Druid, restoring vitality with sacred water.
**Narrative:** The Druid cups their hands. Water appears — not from a flask, not from the sky, but from the earth itself. It's clear, cold, and alive. It flows over the Druid's hands, up their arms, across their chest. Wounds wash clean. Fatigue drains. The water sinks back into the ground, and the Druid stands refreshed, as if the battle just started.

---

### 25. Ancient Grove
```python
{"id": "ancient_grove", "name": "Ancient Grove", "cooldown": 6,
 "power_type": "buff", "trigger": "always",
 "self_status": "warded",
 "heal_percent": 0.10,
 "stat_mod": {"self": {"armor_bonus": 4, "essence": 3, "durability": 3}}, "mod_duration": 4}
```
**Description:** A tranquil grove instantly grows around the Druid, creating a sacred forest zone that heals and protects.
**Narrative:** The Druid kneels and presses both palms to the earth. The earth answers big. Trees grow — not saplings, but ancients, tall and wide, their canopies interlocking. The ground softens to moss. The air changes. This is sacred ground now. The enemy steps onto it and feels wrong. The Druid stands in the center, and the grove stands with them.

---

### 26. Verdant Ascension
```python
{"id": "verdant_ascension", "name": "Verdant Ascension", "cooldown": 6,
 "power_type": "buff", "trigger": "always",
 "self_status": "inspired",
 "stat_mod": {"self": {"might": 4, "grace": 4, "insight": 4, "essence": 3, "durability": 3}}, "mod_duration": 4}
```
**Description:** The Druid ascends into a pure nature spirit, body glowing with verdant energy. All stats surge as the wild flows through them.
**Narrative:** The Druid stops. They close their eyes. And then — they rise. Not jump, not float. Rise. Green light pours from their skin, their eyes, their mouth. The forest is inside them now, not around them. Every leaf that ever fell, every root that ever grew, every beast that ever ran — it's all there, behind their eyes. When they open them, the enemy sees not a person, but the wild itself, wearing a person's shape. And the wild is done being patient.

---

### 27. Worldroot Passage
```python
{"id": "worldroot_passage", "name": "Worldroot Passage", "cooldown": 5,
 "power_type": "buff", "trigger": "always",
 "self_status": "evasive",
 "stat_mod": {"self": {"grace": 4, "essence": 2}}, "mod_duration": 3}
```
**Description:** The Druid disappears into one tree and emerges from another, traveling through ancient roots beneath the battlefield.
**Narrative:** The Druid steps backward into a tree. Not against it — into it. The bark opens like a door. A moment later, a tree on the other side of the enemy opens the same way, and the Druid steps out. The enemy turns. The Druid is already behind them. The roots beneath the battlefield are older than the war. They don't mind giving a ride.

---

### 28. Avatar of the Forest
```python
{"id": "avatar_of_the_forest", "name": "Avatar of the Forest", "cooldown": 6,
 "power_type": "buff", "trigger": "low_hp",
 "self_status": "warded",
 "heal_percent": 0.15,
 "stat_mod": {"self": {"might": 5, "armor_bonus": 5, "essence": 4, "durability": 3}}, "mod_duration": 4}
```
**Description:** The Druid merges with a colossal forest guardian, becoming the spirit of the ancient woods.
**Narrative:** The Druid is failing. The forest disagrees. A guardian — ancient, vast, older than memory — rises from the earth behind the Druid. It doesn't fight for them. It merges with them. The Druid grows — taller, wider, bark-skinned, root-footed. Their voice becomes the forest's voice. Their fists become the forest's fists. The enemy looks up and sees the woods themselves, and the woods are angry. Triggers when HP is low.

---

## Legendary Tier (Level 20, 2500g, 1 day — Quest-gated) — 2 Strikes

### 29. Heart of Gaia
```python
{"id": "heart_of_gaia", "name": "Heart of Gaia", "cooldown": 8,
 "power_type": "strike", "damage_type": "true", "trigger": "always",
 "status_apply": "stunned",
 "stat_mod": {"enemy": {"might": -5, "grace": -5, "armor_bonus": -6, "essence": -4}},
 "mod_duration": 4,
 "self_status": "warded"}
```
**Description:** The earth itself answers the Druid's plea. True damage ignores all defense. Devastates enemy stats. Grants Warded.
**Narrative:** The Druid presses both hands into the earth — not gently, but desperately. They speak a name. Not a word. A name. The world's name. And the world hears. The ground heaves. The roots — not surface roots, but the deep ones, the ones that hold continents together — rise. The enemy is caught in something tectonic, something that was here before people and will be here after. The damage is absolute. The earth doesn't negotiate.

**Quest: The Worldroot Awakening**
- **Trainer:** Elder Lyria (Riverguard)
- **Min Level:** 20
- **Objectives:**
  - Kill 5 Ashen Border undead in Valeria
  - Gather 3 Relic Shards
  - Learn at least 5 Druid skills from Elder Lyria
- **Reward:** Unlocks Heart of Gaia

---

### 30. Legend of Nature
```python
{"id": "legend_of_nature", "name": "Legend of Nature", "cooldown": 10,
 "power_type": "strike", "damage_type": "true", "trigger": "low_hp",
 "status_apply": "stunned",
 "self_status": "inspired",
 "heal_percent": 0.20,
 "stat_mod": {"enemy": {"might": -6, "grace": -6, "armor_bonus": -8, "essence": -5, "cognition": -4, "durability": -4}},
 "mod_duration": 5}
```
**Description:** Ancient spirits gather as every plant and beast bows to the legendary protector. The Druid becomes the eternal guardian of the wild. True damage ignores all defense. Devastates all enemy stats. Heals the Druid. Grants Inspired. Only usable when below 25% HP.
**Narrative:** The Druid is on the ground. The forest is quiet. And then — not silent, but listening. Every spirit that ever walked the wood gathers. Every beast that ever lived bows its head. Every tree leans in. The Druid rises, and they are not alone. They are the forest. They are the beast. They are the root and the branch and the claw and the bloom. The enemy sees the wilderness itself stand up, and the wilderness has decided the enemy is finished. The strike that comes is not a spell. It is the world, remembering what it was before the enemy existed. Triggers when HP is low.

**Quest: The Worldroot Awakening**
- **Trainer:** Elder Lyria (Riverguard)
- **Min Level:** 20
- **Objectives:**
  - Complete "The Worldroot Awakening" quest (learn Heart of Gaia first)
  - Kill 1 Heritage Boss
  - Gather 1 Jahra Ingot
  - Learn at least 15 Druid skills total
- **Reward:** Unlocks Legend of Nature
