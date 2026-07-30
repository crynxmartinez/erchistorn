# Mage Mastery — 30 Skills + 50 Arcane Library Passives + Spell Weaving

**Role:** The Architect — a mid-range arcane scholar who transforms their own skills through the Arcane Library and weaves two spells together on even turns. The Mage's power isn't in their spells — it's in *how they change them*.
**Masteries per trainer:** 3 (Mage + 2 others)
**Trainers teaching Mage:** Elaris, Starfall Watch, Atlantyrion

---

## Mage Identity

**Core loop:** Build Arcane Library loadout → setup on odd turns → weave 2 spells on even turns → adapt loadout between fights

- **Mid-range (Range 2)** — not melee (0), not sniper (3). The Mage is close enough to matter, far enough to cast. Enemies can close the gap in 2 turns — positioning matters.
- **Pure magical damage** — no physical strikes (except Stone Spear), no weapons. The Mage fights with the elements, the mind, and reality itself.
- **Build-crafting mastery** — the Mage's passives aren't auto-learned. They choose 5 from 50, and each one *transforms* how skills work — not just bigger numbers, but different effects entirely.
- **Spell Weaving** — every even turn (2, 4, 6, 8...) the Mage casts 2 skills simultaneously. Odd turns are setup. Even turns are explosion.
- **Elemental diversity** — fire, ice, lightning, stone, wind, void, time, space, mind. The Mage has more damage types than any mastery.
- **Illusion and control** — telekinesis, portals, time manipulation, hallucinations. The Mage doesn't just damage — they reshape the battlefield.
- **Squishy** — low HP, low armor. The Mage survives through wards, evasion, and positioning — not durability.
- **Combo master** — two spells at once means the whole is greater than the parts. Debuff + Strike, Defend + Buff, two Strikes — the Mage chooses how to weave.
- **No two Mages are the same** — the Arcane Library means every Mage has a different build. Two level 50 Mages can play completely differently based on which 5 passives they chose.

### The Arcane Library

The Mage's unique mechanic — the thing no other mastery has — is the **Arcane Library**: a collection of 50 **transformation passives** organized into 5 Schools. The Mage chooses **5** to equip, and each one changes how their skills *work* — not just how much they hit for.

**How it works:**
- **5 passive slots**, unlocking every 10 levels (10, 20, 30, 40, 50)
- In the character menu, below the skill collapsible is the **Passive collapsible** — 5 slots for Arcane Library passives
- **50 passives** across 5 Schools (Elements: 10, Arcane: 10, Spatial: 14, Temporal: 6, Mental: 10) — see tables below
- Each passive is a **modifier** — it changes how skills behave, not just stats
- A skill can be modified by **multiple passives simultaneously** — this is where the chaos lives
- **Swap freely out of combat** — the Mage prepares their loadout like a scholar packing books
- **School Synergy**: equipping 3+ passives from the same School unlocks a bonus (see below)

**Research — Passives are Earned, Not Given:**
- Passives are **not** unlocked automatically at level milestones. The slot unlocks, but it's empty.
- To fill it, the Mage must **Research** passives by defeating specific creatures or completing specific challenges.
- Each passive has a **Research requirement** — a creature to kill, a biome to clear, a boss to defeat.
- Examples:
  - Kill a **Fire Dragon** → Research **Wildfire** (fire spreads to adjacent enemies)
  - Kill a **Frost Giant** → Research **Absolute Zero** (ensnared becomes frozen)
  - Kill a **Thunder Titan** → Research **Void Lightning** (stunned becomes voidmarked)
  - Clear the **Void Rift** event → Research **Rewind** (once per combat, rewind HP/position)
  - Defeat **3 Bosses** → Research **Glass Cannon** (+100% damage, +50% taken)
- Research is **permanent** — once unlocked, the passive is available forever.
- The Mage can Research passives in any order — they don't need to follow the School structure.
- This means a level 10 Mage with 1 slot could have **any** passive from the 50, as long as they completed the Research.

**Spell Tags — How Passives Know What to Affect:**
- Every skill has **Spell Tags** — descriptors that define what the skill *is*.
- Passives affect **tags**, not hardcoded skill names. This makes future skills automatic.
- Example tags: `Fire`, `Ice`, `Lightning`, `Stone`, `Wind`, `Projectile`, `Explosion`, `Strike`, `Debuff`, `Buff`, `Defend`, `Single-Target`, `AoE`, `Teleport`, `Illusion`
- Example: **Frostfire** affects all skills with the `Fire` tag — not just "Fireball." If a future expansion adds `Magma Rain` (tags: `Fire`, `Stone`, `AoE`), Frostfire automatically transforms it.
- Example: **Chain Reaction** affects all skills with `Single-Target` + `Strike` tags — any future single-target strike automatically chains.
- Tags are listed in each skill's JSON definition (see Skill Structure below).

**Loadout Saves — Favorites:**
- The Mage can save up to **5 Loadouts** — named preset builds.
- Example: "Boss Build" (3 Arcane + 2 Elements for burst), "PvP Build" (3 Mental + 2 Spatial for control), "Farming Build" (3 Spatial + 2 Arcane for speed).
- Switching Loadouts is **one click** — but only **out of combat**.
- This lets the Mage adapt to any situation without rebuilding from scratch every time.

**Why this works:**
- **Build-crafting** — the Mage's power comes from *choice*, not auto-learning. No other mastery has this.
- **Transformation, not enhancement** — passives don't say "+15% damage." They say "burning becomes frostburn." The skill *is* different.
- **Chaos engine** — with 5 passives active, every skill is modified by up to 5 passives simultaneously. A single Fireball can become an AoE frostburn that chains and echoes.
- **The catch** — not every passive affects every skill. Frostfire only affects `Fire`-tagged skills. Overload only affects `Single-Target` + `Debuff`-tagged skills. The Mage must build *synergies* — choosing passives that transform the skills they actually use.
- **5 slots, not 10** — 5 passives × 2 Dual Cast spells = 10 passive interactions per even turn. Still chaotic, but **balanceable**. 10 slots would be 20 interactions — insane.

#### School of Elements — Transmute What Skills Apply

| # | Passive | Effect |
|---|---------|--------|
| 1 | Frostfire | `Fire`-tagged skills apply `frostburn` instead of `burning` — frostburn deals damage AND slows (acts as `ensnared` for 1 turn) |
| 2 | Storm Earth | `Stone`-tagged skills apply `shocked` instead of `bleeding` — shocked targets take +25% damage from all sources |
| 3 | Void Lightning | `Lightning`-tagged skills apply `voidmarked` instead of `stunned` — voidmarked targets take true damage from the next hit |
| 4 | Caustic Wind | `Wind`-tagged skills apply `corroded` instead of their normal status — corroded reduces `armor_bonus` by 3 per turn (stacks) |
| 5 | Shadow Ice | `Ice`-tagged skills apply `shadowfrost` instead of `ensnared` — shadowfrost = ensnared + the target cannot be healed |
| 6 | Magma Skin | `Stone`-tagged skills apply `magma` instead of `bleeding` — magma deals burning damage over 3 turns AND spreads to adjacent enemies |
| 7 | Thunderblood | `Lightning`-tagged skills also apply `bleeding` in addition to their normal status |
| 8 | Absolute Zero | `Ice`-tagged skills: if the target is already `ensnared`, they become `frozen` (can't act at all) for 1 turn |
| 9 | Wildfire | `Fire`-tagged skills: if the target is already `burning`, the burning spreads to all adjacent enemies |
| 10 | Elemental Overload | All elemental skills apply their status at +2 stacks instead of +1 |

#### School of Arcane — Transmute How Skills Deal Damage

| # | Passive | Effect |
|---|---------|--------|
| 11 | True Strike | `Strike`-tagged skills convert 25% of damage to true damage |
| 12 | Overchannel | `Strike`-tagged skills deal +50% damage but cost +50% MP |
| 13 | Chain Reaction | `Single-Target` + `Strike`-tagged skills hit 2 targets (spreads to nearest enemy at 50% power) |
| 14 | Echo Chamber | `Strike`-tagged skills repeat at 50% power on the following turn (free, no action cost) |
| 15 | Implosion | `Single-Target` + `Strike`-tagged skills deal AoE damage to adjacent enemies |
| 16 | Spell Penetration | `Strike`-tagged skills ignore 50% of target's `essence` (magic resistance) |
| 17 | Critical Theory | `Strike`-tagged skills have 20% chance to deal double damage (crit) |
| 18 | Mana Vampire | `Strike`-tagged skills restore MP equal to 10% of damage dealt |
| 19 | Glass Cannon | `Strike`-tagged skills deal +100% damage but you take +50% damage while casting |
| 20 | Arcane Surge | Every 3rd `Strike`-tagged skill in combat deals true damage automatically |

#### School of Spatial — Transmute Range, Targeting, Positioning

| # | Passive | Effect |
|---|---------|--------|
| 21 | Long Range | +1 Range to all skills (range 2 → 3) |
| 22 | Point Blank | -1 Range but +30% damage at range 0-1 |
| 23 | Expanding Radius | Single-target skills hit target + 1 adjacent enemy |
| 24 | Blink Step | `Teleport`-tagged skills also grant `hidden` for 1 turn |
| 25 | Portal Mastery | Portals last 2 turns (enemy can be lured into them) |
| 26 | Reposition | `Defend`-tagged skills also move you +1 range away from the enemy |
| 27 | Gravity Shift | `Debuff`-tagged skills also pull the enemy 1 range closer |
| 28 | Mirror Position | When you dodge, you swap positions with the enemy (confuses melee) |
| 29 | Spatial Tear | `Buff`-tagged skills create a 1-turn portal behind the enemy for flanking |
| 30 | Far Strike | `Strike`-tagged skills can be cast at any range (no minimum) |
| 31 | Portal Behind Ally | `Teleport`-tagged skills can place the exit portal behind an ally for flanking support |
| 32 | Portal Behind Enemy | `Teleport`-tagged skills can place the exit portal behind the enemy — melee allies get backstab bonus |
| 33 | Portal Through Wall | `Teleport`-tagged skills ignore terrain — portals can pass through walls, doors, and obstacles |
| 34 | Portal Through Trap | `Teleport`-tagged skills can redirect a portal exit onto a trap — the enemy walks through and triggers it |

#### School of Temporal — Transmute Timing, Cooldowns, Turn Order

*The smallest school — time already breaks games. 6 passives, not 10.*

| # | Passive | Effect |
|---|---------|--------|
| 35 | Quickened Mind | All cooldowns reduced by 1 |
| 36 | Time Dilation | `Debuff`-tagged skills last +1 turn |
| 37 | Rewind | Once per combat, rewind to your previous turn's HP and position |
| 38 | Temporal Echo | Dual Cast skills echo at 25% power on the next odd turn |
| 39 | Time Loop | Enemies with `stunned` repeat their last action next turn (wastes their turn) |
| 40 | Accelerated Casting | Spells with cooldown 5+ have cooldown reduced to 4 |

#### School of Mental — Transmute Debuffs, Illusions, Mind Effects

| # | Passive | Effect |
|---|---------|--------|
| 41 | Overload | `Single-Target` + `Debuff`-tagged skills become AoE (hit all enemies) |
| 42 | Double Jeopardy | `Debuff`-tagged skills apply 2 different statuses instead of 1 |
| 43 | Mind Fracture | `shaken` targets also lose 1 random stat per turn |
| 44 | Paranoia | `shaken` targets cannot receive buffs (they don't trust allies) |
| 45 | Hallucination | `Illusion`-tagged skills create 2 extra copies instead of 1 |
| 46 | Mass Hysteria | `Debuff`-tagged skills spread to 1 adjacent enemy at 50% duration |
| 47 | Delirium | Enemies with 2+ debuffs have 25% chance to attack their own ally |
| 48 | Phobia Implant | The first `Debuff`-tagged skill each combat also applies `stunned` for 1 turn |
| 49 | Mind Control | `shaken` enemies have 15% chance to skip their turn |
| 50 | Illusion Mastery | `evasive` also grants `hidden` — the Mage vanishes on dodge |

#### School Synergy Bonuses

Equipping 3+ passives from the same School unlocks a synergy bonus. With only 5 slots, committing 3+ to one school is a **major investment** — over half your loadout.

| School | 3+ Synergy | 5+ Synergy (all-in) |
|--------|-----------|-------------------|
| Elements | All element skills apply +1 stack of their status | All element skills also apply a 2nd random element's status |
| Arcane | All strikes have 10% true damage | All strikes have 25% true damage + 10% crit |
| Spatial | +1 Range to all skills | `Teleport`-tagged skills don't cost an action |
| Temporal | All cooldowns -1 | Dual Cast also works on turn 10+ of combat |
| Mental | All debuffs last +1 turn | All debuffs spread to adjacent enemies |

#### The Chaos Engine — How Transformations Stack

Passives **stack**. With 5 slots, a single Fireball (tags: `Fire`, `Strike`, `Single-Target`, `Projectile`, `Explosion`) could be modified by:

- **Frostfire** → burning becomes frostburn (damage + slow)
- **Chain Reaction** → hits 2 targets
- **Echo Chamber** → repeats at 50% next turn
- **Implosion** → each hit also damages adjacent enemies
- **Critical Theory** → 20% chance to deal double damage

Result: Fireball hits **2 targets** with **frostburn**, **spreads to adjacent enemies**, **20% crit chance**, then **repeats at 50% power next turn**. That's one skill with 5 passive interactions — balanceable, but still chaotic.

**The catch:** not every passive affects every skill. Frostfire only affects `Fire`-tagged skills. Overload only affects `Single-Target` + `Debuff`-tagged skills. The Mage has to **build synergies** — choosing passives that transform the skills they actually use.

### Spell Weaving (Dual Cast)

The Mage's second unique mechanic. **Every even turn** (2, 4, 6, 8...) the Mage selects **2 different skills from their skill bar** and both cast simultaneously.

**Arcane Focus — The Resource That Powers Dual Cast:**
- Dual Cast is **not guaranteed** — it costs **Arcane Focus**.
- **Odd turns:** Gain 1 Arcane Focus (max 3). The Mage builds power during setup.
- **Even turns:** Spend 1 Arcane Focus to Dual Cast. If Focus = 0, the Mage casts 1 skill (normal turn).
- **Stunned/silenced:** No Focus gained that turn. The enemy has **counterplay** — stun the Mage on odd turns to deny Focus, preventing the even-turn explosion.
- This means the Mage must **protect their setup turns** — if they get CC'd on turn 1, they can't Dual Cast on turn 2.

**How it works:**
- **Odd turns:** 1 skill (normal cast — setup, reposition, defend) + gain 1 Arcane Focus
- **Even turns:** Spend 1 Focus → cast 2 skills simultaneously (both resolve at the same time — not sequentially)
- **No duplicate spells** — the Mage cannot cast the same skill twice in one Dual Cast (no Fireball + Fireball). The two skills must be **different**.
- Both skills' effects combine — debuffs land *before* strikes resolve, buffs apply *before* the paired skill's effect
- **MP cost:** both skills cost their normal MP — no discount, no penalty
- **Cooldowns:** both skills go on cooldown normally

**Combo examples (with transformation passives):**

| Turn | Skill 1 | Skill 2 | Result |
|------|---------|---------|--------|
| 2 | Frost Prison (Overload → AoE) | Meteor Storm (Frostfire → frostburn) | All enemies ensnared, then all take frostburn + AoE |
| 4 | Gravity Well (Gravity Shift → pulls closer) | Chain Lightning (Chain Reaction → 2 targets) | Enemy pulled in, then lightning chains between 2 clustered targets |
| 6 | Time Slow (Time Dilation → +1 turn) | Telekinetic Crush (Echo Chamber → repeats) | Enemy slowed for 4 turns, crushed now AND next turn for free |

**Why this creates a rhythm:**
- **Odd turns** = the Mage is vulnerable. One action, building Focus. The enemy knows this.
- **Even turns** = the Mage is terrifying. Two actions. The enemy dreads this.
- **Counterplay** — stun the Mage on odd turns to deny Focus. Silence them to prevent Dual Cast. The enemy has tools.
- Smart enemies will **save their CC for odd turns** to break the Mage's rhythm
- The Mage must **plan ahead** — protect setup turns, save defensive skills for when Focus is low
- Some Temporal passives can **break the rhythm** — "Dual Cast also works on turn 10+" extends the power window

### Stat Focus

| Stat | Priority | Why |
|------|----------|-----|
| `insight` | Primary | Magical damage scaling — the Mage's strikes hit harder with more insight |
| `essence` | Primary | Magic resistance + healing power — the Mage is squishy and needs every bit of defense |
| `cognition` | Secondary | Skill capacity / utility — more skills means more combo options for Spell Weaving |
| `grace` | Secondary | Accuracy + evasion — the Mage dodges, not tanks |
| `durability` | Minimal | HP / resilience — the Mage's lowest priority. They don't build for health. |
| `might` | Minimal | Physical damage — nearly useless for the Mage (only Stone Spear scales with it) |
| `armor_bonus` | Minimal | Physical damage reduction — the Mage relies on wards, not armor |

### Status Identity

| Category | Statuses | How the Mage Uses Them |
|----------|----------|----------------------|
| **Signature** | `burning`, `ensnared`, `stunned` | Fire, ice, and lightning — the three core elements. Applied constantly across all tiers. |
| **Secondary** | `shaken`, `evasive`, `warded`, `hidden` | Illusions, wards, and mobility. The Mage controls the mind and the battlefield. |
| **Rare** | `bleeding`, `inspired` | Only from Stone Spear and legendary skills. Not a core part of the Mage's identity. |
| **Transformed** | `frostburn`, `shocked`, `voidmarked`, `corroded`, `shadowfrost`, `magma`, `frozen` | Only available through Arcane Library transformation passives. These are the Mage's *built* statuses — they don't exist without the right passives. |

### Trigger Identity

| Category | Triggers | How the Mage Uses Them |
|----------|----------|----------------------|
| **Primary** | `always` | The Mage casts on their terms — most skills have no condition |
| **Secondary** | `opponent_status`, `opponent_wounded` | Combo setup — debuff first, then the conditional skill hits harder |
| **Rare** | `low_hp`, `opening_move` | Emergency skills (Mana Explosion, Time Stop) and first-turn plays |

### What the Mage Does NOT Do

- **No melee** — range 0 is not an option. The Mage fights at range 2 and repositions when enemies close in.
- **No heavy armor** — the Mage wears robes. `armor_bonus` is their lowest stat priority.
- **No healing** — the Mage has zero heal skills. They survive through avoidance, not recovery.
- **No taunting** — the Mage never wants to be hit. No aggro management.
- **No summoning** — the Mage fights alone. No pets, no companions, no constructs.
- **No physical multi-hit** — `hits` > 1 only appears on magical strikes (Chain Lightning, Meteor Storm, Elemental Convergence). No physical weapon combos.
- **No auto-learned passives** — unlike every other mastery, the Mage's passives are *chosen*, not given. This is the core of the Arcane Library.

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
| `spell_tags` | List of tags describing the skill — passives affect tags, not skill names. Examples: `["Fire", "Strike", "Single-Target", "Projectile", "Explosion"]` |

**Available spell tags:**
- **Element:** `Fire`, `Ice`, `Lightning`, `Stone`, `Wind`, `Void`
- **Type:** `Strike`, `Debuff`, `Buff`, `Defend`, `Heal`
- **Targeting:** `Single-Target`, `AoE`, `Projectile`, `Explosion`
- **Mechanic:** `Teleport`, `Illusion`, `Portal`

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

| Tier | Level Req | Gold Cost | Learn Time | Count | Strikes | Debuffs | Defends | Buffs |
|------|-----------|-----------|------------|-------|---------|---------|---------|-------|
| Basic | 1 | 50g | 5 min | 6 | 4 | 0 | 1 | 1 |
| Advanced | 3 | 150g | 30 min | 7 | 2 | 3 | 1 | 1 |
| Expert | 8 | 400g | 1 hr | 7 | 1 | 3 | 1 | 2 |
| Master | 15 | 1000g | 1 hr | 8 | 4 | 3 | 0 | 1 |
| Legendary | 20 | 2500g | 1 day | 2 | 2 | 0 | 0 | 0 |

---

## Basic Tier (Level 1, 50g, 5min) — 4 Strikes, 1 Defend, 1 Buff

### 1. Arcane Burst
```python
{"id": "arcane_burst", "name": "Arcane Burst", "cooldown": 2,
 "power_type": "strike", "damage_type": "magical", "trigger": "always",
 "stat_mod": {"enemy": {"grace": -1}}, "mod_duration": 2}
```
**Description:** The Mage gathers shimmering energy between both hands, compresses it into a bright sphere, and hurls it forward. The orb bursts on impact with a sharp wave of arcane light.
**Narrative:** The Mage's palms come together. Light gathers — not from the sun, not from a flame, but from the space between thoughts. It compresses, densifies, becomes a sphere the size of a fist. The Mage opens their hands. The sphere leaves. The impact is not loud. It is final.

---

### 2. Wind Blade
```python
{"id": "wind_blade", "name": "Wind Blade", "cooldown": 2,
 "power_type": "strike", "damage_type": "magical", "trigger": "always",
 "status_apply": "bleeding",
 "stat_mod": {"enemy": {"grace": -2}}, "mod_duration": 2}
```
**Description:** With a sweeping gesture, the Mage cuts through the air. An almost invisible blade of compressed wind races forward and slices through its path.
**Narrative:** The Mage doesn't chant. They gesture — a casual sweep of the hand, like brushing hair from their face. The air disagrees. A crescent of compressed wind leaves the gesture and crosses the battlefield in silence. The enemy feels the cut before they hear it. They don't hear it.

---

### 3. Stone Spear
```python
{"id": "stone_spear", "name": "Stone Spear", "cooldown": 3,
 "power_type": "strike", "damage_type": "physical", "trigger": "always",
 "status_apply": "bleeding",
 "stat_mod": {"enemy": {"armor_bonus": -2}}, "mod_duration": 2}
```
**Description:** The Mage stomps the ground and pulls upward with one hand. Stone tears free, forms into a jagged spear, and shoots toward the enemy.
**Narrative:** The Mage stomps. The ground obeys. Stone tears free — not gradually, but violently — and shapes itself into a spear mid-flight. It's not elegant. It's geology with intent. The enemy's armor meets stone, and the stone doesn't care about the armor.

---

### 4. Arcane Ward
```python
{"id": "arcane_ward", "name": "Arcane Ward", "cooldown": 4,
 "power_type": "defend", "trigger": "always",
 "self_status": "warded",
 "stat_mod": {"self": {"essence": 3}}, "mod_duration": 3}
```
**Description:** The Mage draws interlocking runes in front of themselves. The symbols connect and harden into a translucent wall of blue energy.
**Narrative:** The Mage's finger moves — quick, precise, practiced. Lines appear in the air, connect, interlock. The runes glow blue, then solidify. The wall doesn't block attacks. It unmakes them. The enemy's blade hits the ward and the force just... disperses. The Mage is already drawing the next one.

---

### 5. Blink
```python
{"id": "blink", "name": "Blink", "cooldown": 3,
 "power_type": "buff", "trigger": "always",
 "self_status": "evasive",
 "stat_mod": {"self": {"grace": 4}}, "mod_duration": 2}
```
**Description:** The Mage's outline flickers and collapses into sparks. A heartbeat later, those sparks gather again at a nearby location.
**Narrative:** The enemy swings. The Mage isn't there. Not dodged — gone. Sparks hang in the air where they stood, and a heartbeat later, the sparks gather three meters to the left. The Mage reforms, already casting. The enemy's sword is still falling. The Mage is already finished.

---

### 6. Water Lash
```python
{"id": "water_lash", "name": "Water Lash", "cooldown": 3,
 "power_type": "strike", "damage_type": "magical", "trigger": "always",
 "status_apply": "stunned",
 "stat_mod": {"enemy": {"grace": -2}}, "mod_duration": 2}
```
**Description:** The Mage draws moisture from the air and snaps their arm forward. Water twists into a powerful lash that crashes against the target.
**Narrative:** The Mage's hand opens. The air gets drier. The moisture gathers — from breath, from sweat, from the morning dew — and coils around the Mage's arm like a serpent. They snap it forward. The lash hits the enemy's face with the force of a wave and the precision of a whip. The enemy staggers, wet, stunned.

---

## Advanced Tier (Level 3, 150g, 30min) — 2 Strikes, 3 Debuffs, 1 Defend, 1 Buff

### 7. Fireball
```python
{"id": "fireball", "name": "Fireball", "cooldown": 3,
 "power_type": "strike", "damage_type": "magical", "trigger": "always",
 "status_apply": "burning",
 "stat_mod": {"enemy": {"armor_bonus": -3}}, "mod_duration": 3}
```
**Description:** The Mage traces a burning circle in the air. Fire gathers within it before surging toward the target and erupting into a roaring explosion.
**Narrative:** The Mage's finger traces a circle. The circle catches fire — not gradually, but instantly, as if the air inside it was always meant to burn. The fireball forms, condenses, and launches. The impact is not subtle. The enemy's armor blackens. Their skin blisters. The Mage is already tracing the next circle.

---

### 8. Frost Prison
```python
{"id": "frost_prison", "name": "Frost Prison", "cooldown": 4,
 "power_type": "debuff", "damage_type": "magical", "trigger": "always",
 "status_apply": "ensnared",
 "stat_mod": {"enemy": {"grace": -3, "might": -2}}, "mod_duration": 3}
```
**Description:** Cold mist curls around the Mage's fingers. Ice races across the ground, climbs the enemy's body, and seals them inside a frozen cage.
**Narrative:** The Mage exhales. The breath is cold — not winter cold, but absolute cold, the cold of empty space. Ice forms on the ground, crawls toward the enemy, and climbs. It seals their feet, their legs, their torso. The enemy is locked in ice. The Mage watches. The ice watches too.

---

### 9. Chain Lightning
```python
{"id": "chain_lightning", "name": "Chain Lightning", "cooldown": 4,
 "power_type": "strike", "damage_type": "magical", "trigger": "always",
 "hits": 2,
 "status_apply": "stunned",
 "stat_mod": {"enemy": {"grace": -2}}, "mod_duration": 2}
```
**Description:** The Mage raises one hand toward the sky. A bolt crashes into the first target, then leaps from foe to foe in branching flashes.
**Narrative:** The Mage raises a hand. The sky doesn't darken — it sharpens. The bolt descends, hits the first enemy, and doesn't stop. It leaps — from enemy to enemy, from body to body — in a chain of white-blue flashes. Two enemies seize simultaneously. The Mage lowers their hand. The thunder arrives late.

---

### 10. Mana Shield
```python
{"id": "mana_shield", "name": "Mana Shield", "cooldown": 4,
 "power_type": "defend", "trigger": "always",
 "self_status": "warded",
 "stat_mod": {"self": {"essence": 4, "armor_bonus": 2}}, "mod_duration": 3}
```
**Description:** A layer of glowing mana spreads across the Mage's body, bending and dispersing attacks before they reach flesh.
**Narrative:** The Mage doesn't raise a shield. They become one. Mana spreads across their skin like a second layer, glowing, humming, alive. The enemy's blade hits it and bends — not the blade, but the force behind it. The mana absorbs, disperses, redirects. The Mage stands inside their own magic, untouched.

---

### 11. Spell Seal
```python
{"id": "spell_seal", "name": "Spell Seal", "cooldown": 4,
 "power_type": "debuff", "damage_type": "magical", "trigger": "always",
 "status_apply": "shaken",
 "stat_mod": {"enemy": {"insight": -4, "cognition": -3, "might": -2}}, "mod_duration": 3}
```
**Description:** The Mage sketches a lock-shaped sigil in the air. Glowing chains of script wrap around the target's hands and voice, preventing magical casting.
**Narrative:** The Mage draws a lock. The lock becomes real. Chains of glowing script wrap around the enemy's wrists, their throat, their magic. The enemy tries to cast. The chains tighten. The spell dies in their throat. The enemy tries again. The chains tighten more. The Mage watches, patient, while the enemy learns what silence feels like.

---

### 12. Arcane Chains
```python
{"id": "arcane_chains", "name": "Arcane Chains", "cooldown": 4,
 "power_type": "debuff", "damage_type": "magical", "trigger": "opponent_status",
 "status_apply": "ensnared",
 "stat_mod": {"enemy": {"grace": -3, "might": -3}}, "mod_duration": 3}
```
**Description:** Circular runes appear beneath the enemy. Chains of blue-white energy rise from them and tighten around the target.
**Narrative:** The enemy is already suffering — burning, bleeding, frozen. The Mage adds to it. Runes appear beneath the enemy's feet, and chains rise from them like serpents from water. They wrap, tighten, and hold. The enemy can't move. The Mage can. That's the arrangement. Only triggers when the enemy has a status effect.

---

### 13. Illusory Double
```python
{"id": "illusory_double", "name": "Illusory Double", "cooldown": 5,
 "power_type": "buff", "trigger": "always",
 "self_status": "evasive",
 "stat_mod": {"self": {"grace": 5}}, "mod_duration": 3}
```
**Description:** The Mage splits into several identical figures. Each copy mirrors the same gestures, making the real caster difficult to identify.
**Narrative:** The Mage doesn't move. They multiply. Three Mages stand where one was. Four. Five. All identical, all casting, all real — or none of them are. The enemy swings at one. It dissipates. They swing at another. Also false. The real Mage is already behind them, and the fireball is already in the air.

---

## Expert Tier (Level 8, 400g, 1hr) — 1 Strike, 3 Debuffs, 1 Defend, 2 Buffs

### 14. Gravity Well
```python
{"id": "gravity_well", "name": "Gravity Well", "cooldown": 5,
 "power_type": "debuff", "damage_type": "magical", "trigger": "always",
 "status_apply": "ensnared",
 "stat_mod": {"enemy": {"grace": -4, "might": -3, "cognition": -2}}, "mod_duration": 3}
```
**Description:** The Mage closes their fist and the air bends inward. Dust, weapons, and enemies slide helplessly toward a dark sphere of crushing force.
**Narrative:** The Mage closes their fist. The world leans. Not metaphorically — physically. A dark sphere appears in the air, and everything starts falling toward it: dust, arrows, the enemy's footing. The enemy slides, stumbles, is pulled inward. The Mage watches. The sphere doesn't let go. It just pulls.

---

### 15. Telekinetic Crush
```python
{"id": "telekinetic_crush", "name": "Telekinetic Crush", "cooldown": 5,
 "power_type": "strike", "damage_type": "magical", "trigger": "opponent_wounded",
 "status_apply": "stunned",
 "stat_mod": {"enemy": {"might": -4, "armor_bonus": -3}}, "mod_duration": 3}
```
**Description:** The Mage raises a hand and the target is dragged into the air. Unseen pressure closes around the victim, lifting and squeezing.
**Narrative:** The enemy is already wounded. The Mage raises a hand. The enemy rises — not jumping, not flying, but lifted. Invisible force wraps around them and tightens. Armor dents. Bones creak. The enemy's eyes go wide. The Mage's hand closes. The enemy drops. The Mage opens their hand. Only triggers when the enemy is wounded.

---

### 16. Mirror Spell
```python
{"id": "mirror_spell", "name": "Mirror Spell", "cooldown": 5,
 "power_type": "defend", "trigger": "always",
 "self_status": "warded",
 "stat_mod": {"self": {"essence": 4, "grace": 2}}, "mod_duration": 3}
```
**Description:** A glass-like rune appears before the Mage. The incoming spell sinks into it, reverses direction, and erupts back toward its source.
**Narrative:** The enemy casts. The spell flies. The Mage doesn't dodge — they reflect. A rune appears, glassy, shimmering. The spell hits it, sinks in, and for a moment, disappears. Then it comes back — reversed, redirected, angry. The enemy takes their own magic to the face. The Mage adjusts the rune. Next.

---

### 17. Mind Maze
```python
{"id": "mind_maze", "name": "Mind Maze", "cooldown": 5,
 "power_type": "debuff", "damage_type": "magical", "trigger": "opponent_status",
 "status_apply": "shaken",
 "stat_mod": {"enemy": {"cognition": -5, "grace": -3, "might": -2}}, "mod_duration": 3}
```
**Description:** The Mage meets the target's gaze and whispers a single phrase. The enemy's surroundings twist into an endless labyrinth.
**Narrative:** The Mage speaks — not a spell, but a word. One word, in a language the enemy doesn't know but somehow understands. And then the world changes. The battlefield becomes a maze — walls where there were none, paths that loop back, exits that lead deeper. The enemy stumbles through their own mind. The Mage watches from outside. Only triggers when the enemy has a status effect.

---

### 18. Void Portal
```python
{"id": "void_portal", "name": "Void Portal", "cooldown": 5,
 "power_type": "buff", "trigger": "always",
 "self_status": "evasive",
 "stat_mod": {"self": {"grace": 4, "essence": 2}}, "mod_duration": 3}
```
**Description:** The Mage tears open a dark oval in space, then opens another farther away. The two portals ripple as though connected by an unseen tunnel.
**Narrative:** The Mage reaches into the air and pulls. Space tears — not violently, but like fabric parting. A dark oval appears. Another opens across the battlefield. The Mage steps into one and emerges from the other. The enemy charges the first portal. It closes. The Mage is already behind them.

---

### 19. Phantom Terrain
```python
{"id": "phantom_terrain", "name": "Phantom Terrain", "cooldown": 5,
 "power_type": "debuff", "damage_type": "magical", "trigger": "always",
 "status_apply": "shaken",
 "stat_mod": {"enemy": {"grace": -3, "cognition": -3, "might": -2}}, "mod_duration": 3}
```
**Description:** The Mage waves a hand and the surroundings distort. Safe roads appear as cliffs, open ground looks blocked, and false dangers emerge.
**Narrative:** The Mage waves a hand. The battlefield lies. The ground that was flat now looks like a chasm. The wall that was solid now looks like a door. The enemy charges the door and hits the wall. They avoid the chasm and step onto nothing. The Mage watches the enemy fight a battlefield that doesn't exist.

---

### 20. Dream Step
```python
{"id": "dream_step", "name": "Dream Step", "cooldown": 5,
 "power_type": "buff", "trigger": "always",
 "self_status": "hidden",
 "stat_mod": {"self": {"grace": 4, "cognition": 2}}, "mod_duration": 2}
```
**Description:** The Mage fades into pale mist and briefly travels through visions only the target can perceive.
**Narrative:** The Mage doesn't teleport. They dream. Their body becomes mist — pale, drifting, intangible. They pass through the enemy's mind, through memories and fears, and emerge on the other side. The enemy sees things that aren't there. The Mage is already casting. The dream is already over.

---

## Master Tier (Level 15, 1000g, 1hr) — 4 Strikes, 3 Debuffs, 1 Buff

### 21. Meteor Storm
```python
{"id": "meteor_storm", "name": "Meteor Storm", "cooldown": 6,
 "power_type": "strike", "damage_type": "magical", "trigger": "always",
 "hits": 3,
 "status_apply": "burning",
 "stat_mod": {"enemy": {"armor_bonus": -4, "grace": -3}}, "mod_duration": 3}
```
**Description:** The Mage lifts both arms as the sky darkens. Red cracks appear overhead before blazing stones rain across the battlefield.
**Narrative:** The Mage raises both arms. The sky answers — not with clouds, but with fire. Red cracks appear overhead, and through them, stones fall. Not rocks — meteors. Burning, screaming, patient. Three impacts. Three craters. The enemy is in one of them. The Mage lowers their arms. The sky closes.

---

### 22. Blizzard
```python
{"id": "blizzard", "name": "Blizzard", "cooldown": 6,
 "power_type": "debuff", "damage_type": "magical", "trigger": "always",
 "status_apply": "ensnared",
 "stat_mod": {"enemy": {"grace": -4, "might": -3, "cognition": -2}}, "mod_duration": 3}
```
**Description:** The Mage spins their staff and cold clouds gather instantly. Snow and ice roar outward in a blinding storm.
**Narrative:** The Mage spins their staff. The air freezes. Not gradually — absolutely. Snow erupts from nowhere, wind screams from nothing, and the battlefield becomes a white wall. The enemy can't see. Can't move. Can't feel their fingers. The Mage stands in the eye of the storm, calm, dry, watching.

---

### 23. Thunderfield
```python
{"id": "thunderfield", "name": "Thunderfield", "cooldown": 6,
 "power_type": "strike", "damage_type": "magical", "trigger": "always",
 "status_apply": "stunned",
 "stat_mod": {"enemy": {"grace": -3, "armor_bonus": -3, "might": -2}}, "mod_duration": 3}
```
**Description:** The Mage marks the ground with a crackling rune. Dark clouds form above it and lightning begins hammering the marked zone.
**Narrative:** The Mage kneels and draws a rune on the ground. The rune crackles. Above it, clouds form — dark, low, angry. Lightning descends. Not once — repeatedly. The zone becomes a prison of thunder. The enemy inside it doesn't just take damage. They take electricity. The Mage watches from outside the zone. The zone does the work.

---

### 24. Time Slow
```python
{"id": "time_slow", "name": "Time Slow", "cooldown": 6,
 "power_type": "debuff", "damage_type": "magical", "trigger": "always",
 "status_apply": "shaken",
 "stat_mod": {"enemy": {"grace": -5, "might": -4, "cognition": -3}}, "mod_duration": 3}
```
**Description:** The Mage turns an invisible wheel with both hands. Enemy movements become heavy and delayed while falling debris drifts through the air.
**Narrative:** The Mage's hands move — not casting, but turning. An invisible wheel. And the world slows. The enemy's sword is still falling, but it falls like it's underwater. Their dodge starts but finishes late. Their thoughts form but arrive slow. The Mage walks between them, normal speed, untouched by the drag. Time is not a wall. It's a medium. The Mage changes the viscosity.

---

### 25. Elemental Convergence
```python
{"id": "elemental_convergence", "name": "Elemental Convergence", "cooldown": 6,
 "power_type": "strike", "damage_type": "magical", "trigger": "always",
 "hits": 2,
 "status_apply": "burning",
 "stat_mod": {"enemy": {"armor_bonus": -4, "grace": -3, "might": -2}}, "mod_duration": 3}
```
**Description:** Fire, ice, lightning, stone, and wind circle the Mage. The elements compress together before surging outward in a violent multicolored blast.
**Narrative:** The Mage stands still. The elements come. Fire circles left. Ice circles right. Lightning spirals up. Stone orbits below. Wind wraps around all of it. They shouldn't coexist. They don't care. The Mage compresses them — all five, into one point — and releases. The blast is every color and none of them. The enemy doesn't have a favorite element anymore. They have all of them.

---

### 26. Mana Explosion
```python
{"id": "mana_explosion", "name": "Mana Explosion", "cooldown": 6,
 "power_type": "strike", "damage_type": "magical", "trigger": "low_hp",
 "status_apply": "stunned",
 "stat_mod": {"self": {"might": 3}, "enemy": {"armor_bonus": -5, "grace": -4, "might": -3}},
 "mod_duration": 3}
```
**Description:** The Mage draws power inward until their body glows. They release it all at once in a circular wave of pure force.
**Narrative:** The Mage is cornered. Wounded. Out of options. So they choose the last one. They pull mana inward — not from the surroundings, but from their own reserves, their own life force. Their body glows. Their skin cracks with light. And then they release. The explosion is not fire, not ice, not lightning. It's force. Pure, absolute, indiscriminate. The enemy flies. The Mage stands. Triggers when HP is low.

---

### 27. Reality Fracture
```python
{"id": "reality_fracture", "name": "Reality Fracture", "cooldown": 6,
 "power_type": "debuff", "damage_type": "magical", "trigger": "opponent_wounded",
 "status_apply": "stunned",
 "stat_mod": {"enemy": {"might": -5, "grace": -5, "armor_bonus": -4, "cognition": -3}}, "mod_duration": 4}
```
**Description:** The Mage draws a line through empty space. The world cracks along it, causing gravity, distance, or direction to behave unnaturally.
**Narrative:** The Mage draws a line. Not on the ground — in reality. The world cracks along it. Gravity tilts. Distance stretches. Up becomes sideways. The enemy tries to run and moves backward. They try to dodge and fall upward. The rules are broken. The Mage wrote new ones. The enemy is living in them. Only triggers when the enemy is wounded.

---

### 28. Time Stop
```python
{"id": "time_stop", "name": "Time Stop", "cooldown": 7,
 "power_type": "buff", "trigger": "low_hp",
 "self_status": "warded",
 "heal_percent": 0.10,
 "stat_mod": {"self": {"grace": 5, "essence": 3, "cognition": 2}}, "mod_duration": 3}
```
**Description:** The Mage snaps their fingers and sound disappears. Creatures, weapons, and spells remain suspended until time suddenly resumes.
**Narrative:** The Mage snaps their fingers. The world stops. Not slows — stops. The enemy's sword hangs in the air. The arrow is frozen mid-flight. The fireball is a still photograph. The Mage walks through the stillness, adjusts position, casts a spell, and returns. They snap again. Time resumes. The enemy takes the spell from a direction they didn't see. The Mage is already gone. Triggers when HP is low.

---

## Legendary Tier (Level 20, 2500g, 1 day — Quest-gated) — 2 True-Damage Strikes

### 29. Cosmic Convergence
```python
{"id": "cosmic_convergence", "name": "Cosmic Convergence", "cooldown": 8,
 "power_type": "strike", "damage_type": "true", "trigger": "always",
 "status_apply": "stunned",
 "self_status": "inspired",
 "stat_mod": {"enemy": {"might": -5, "grace": -5, "armor_bonus": -6, "essence": -4, "cognition": -3}},
 "mod_duration": 4}
```
**Description:** The Mage aligns glowing symbols like stars across the sky. Their light gathers into one point before descending as a colossal beam. True damage ignores all defense. Devastates enemy stats. Grants Inspired.
**Narrative:** The Mage looks up. The sky isn't the sky anymore — it's a canvas. Symbols appear, arranged like constellations, each one a word in a language older than the world. They align. They gather. The light condenses into a single point, blinding, absolute. And then it descends — a beam of celestial force that doesn't just pierce armor. It pierces reality. The enemy is in the beam. The enemy is the beam. When the light fades, the enemy is less than they were. Much less.

**Quest: The Arcane Ascension**
- **Trainer:** Vex Elenor (Elaris)
- **Min Level:** 20
- **Objectives:**
  - Kill 5 Silverroad elementals in Concordia
  - Gather 3 Relic Shards
  - Learn at least 5 Mage skills from Vex Elenor
- **Reward:** Unlocks Cosmic Convergence

---

### 30. Legend of the Arcane
```python
{"id": "legend_of_the_arcane", "name": "Legend of the Arcane", "cooldown": 10,
 "power_type": "strike", "damage_type": "true", "trigger": "low_hp",
 "hits": 8,
 "status_apply": "stunned",
 "self_status": "inspired",
 "heal_percent": 0.15,
 "stat_mod": {"enemy": {"might": -6, "grace": -6, "armor_bonus": -8, "essence": -5, "cognition": -4, "insight": -4, "durability": -4}},
 "mod_duration": 5,
 "spell_tags": ["Fire", "Ice", "Lightning", "Stone", "Wind", "Void", "Time", "Space"]}
```
**Description:** The Mage doesn't cast one spell. They cast **every element in sequence** — fire, ice, lightning, stone, wind, void, time, space — each appearing one after another in a single devastating chain. 8 hits, each a different element, each true damage. The enemy burns, freezes, shatters, is crushed, is cut, is unmade, is slowed, is displaced — all in one turn. Heals the Mage 15%. Grants Inspired. Only usable when below 25% HP.
**Narrative:** The Mage is dying. The magic is not. It doesn't gather — it *erupts*. Fire first. The enemy screams. Then ice. The scream shatters. Then lightning — through the cracks in the ice. Then stone — through the burns. Then wind — through the wounds. Then void — through the gaps in reality the other five tore open. Then time — the enemy's body ages a decade in a second. Then space — the enemy exists in three places at once and none of them are safe. Eight elements. Eight impacts. One turn. The Mage isn't casting anymore. They *are* the elements. When it ends, the enemy is on the ground. The Mage is standing. The elements are gone. The legend is not. Triggers when HP is low.

**Quest: The Arcane Ascension**
- **Trainer:** Vex Elenor (Elaris)
- **Min Level:** 20
- **Objectives:**
  - Complete "The Arcane Ascension" quest (learn Cosmic Convergence first)
  - Kill 1 Heritage Boss
  - Gather 1 Jahra Ingot
  - Learn at least 15 Mage skills total
- **Reward:** Unlocks Legend of the Arcane
