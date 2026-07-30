# Monster Profile System — Game-Wide Design

**Purpose:** Every monster and creature in the game follows a standardized profile. This system is **game-wide**, not Druid-specific. The Druid's Summon/Tame/Fusion mechanics are built on top of this system, but the profiles themselves apply to every creature in combat — wild or tamed.

---

## Profile Structure

Every monster has exactly **5 components**:

```
┌──────────────────────────────────────┐
│  MONSTER PROFILE                     │
├──────────────────────────────────────┤
│  1. Passive Buff (1)                 │
│  2. Skills (3: Attack/Defense/Utility)│
│  3. Stats (base + growth rate)       │
│  4. Signature Fusion Ability (1)     │
│  5. Personality (1)                  │
└──────────────────────────────────────┘
```

### 1. Passive Buff

A single passive buff that:
- **As a wild monster:** Always active on itself during combat
- **As a tamed summon:** Granted to the Druid while the summon is active on the battlefield
- **During Fusion:** Stays active on the Druid (the summon is inside them)

**Buff types:**

| Buff | Effect |
|------|--------|
| `might_bonus` | +X% might |
| `grace_bonus` | +X% grace |
| `cognition_bonus` | +X% cognition |
| `insight_bonus` | +X% insight |
| `essence_bonus` | +X% essence |
| `durability_bonus` | +X% durability |
| `armor_bonus` | +X armor |
| `lifesteal` | Heals X% of damage dealt |
| `poison_chance` | X% chance to poison on hit |
| `ensnare_chance` | X% chance to ensnare on hit |
| `evasion_bonus` | +X% evasion |
| `crit_chance` | +X% crit chance |
| `regen` | Heals X% max HP per turn |
| `magic_resist` | +X% magic resistance |
| `double_attack` | X% chance to attack twice |

**Rules:**
- Each monster has exactly **1 buff** — no stacking, no choosing
- Buff strength scales with the monster's tier (basic creatures give +10%, legendary give +30%)
- No two species share the same buff + skill combination — every creature feels unique

### 2. Three Skills

Each monster knows exactly **3 skills**, one from each category:

| Category | Purpose | When Wild Monster Uses It | When Tamed Summon Uses It |
|----------|---------|--------------------------|--------------------------|
| **Attack** | Deals damage to the enemy | Default action — used when aggressive | Enemy is above 30% HP, or going for kill below 30% |
| **Defense** | Protects self or ally | Used when below 50% HP | Druid is below 50% HP (protecting the Druid) |
| **Utility** | Special effect — heal, buff, CC, reposition | Used when below 30% HP (surviving) | Summon is below 30% HP, or special condition |

**Key principle:** The same skills a monster uses as a wild enemy are the skills it uses as a tamed summon. **Taming a monster means you now control the same abilities it used against you.**

**Skill format** (same as player skills):

```python
{"id": "savage_bite", "name": "Savage Bite",
 "power_type": "strike", "damage_type": "physical",
 "status_apply": "bleeding",
 "stat_mod": {"enemy": {"might": -2}}, "mod_duration": 2}
```

**Skill rules:**
- Monster skills do NOT have `spirit_communion` or any player-specific fields
- Monster skills are simpler than player skills — 1 effect per skill, no multi-hit unless the creature's identity demands it (e.g., a wolf pack alpha hits twice)
- Attack skills always deal damage + 1 status or debuff
- Defense skills always grant a buff/ward/heal to self or ally
- Utility skills always do something unique — never just damage

### 3. Stats

Every creature has **6 base stats** (same as player stats) plus a **growth rate**:

```python
{"stats": {
    "might": {"base": 12, "growth": 1.2},
    "grace": {"base": 10, "growth": 1.1},
    "cognition": {"base": 5, "growth": 0.8},
    "insight": {"base": 6, "growth": 0.9},
    "essence": {"base": 8, "growth": 1.0},
    "durability": {"base": 14, "growth": 1.3}
}}
```

**Stat formula:**
```
Stat at Level X = Base + (Base × Growth × X)
```

**As a wild monster:** Stats are fixed at the monster's encounter level.
**As a tamed summon:** Stats auto-scale to the Druid's level. A wolf tamed at level 10 fights at level 45 when the Druid is level 45.

**Stat archetypes by species:**

| Archetype | High Stats | Low Stats | Example Species |
|-----------|-----------|-----------|-----------------|
| Bruiser | Might, Durability | Grace, Cognition | Bear, Boar, Troll |
| Striker | Grace, Might | Durability, Essence | Wolf, Panther, Raptor |
| Caster | Insight, Cognition | Might, Durability | Elemental, Wisp, Faerie |
| Tank | Durability, Armor | Grace, Insight | Turtle, Crab, Golem |
| Support | Essence, Cognition | Might, Grace | Owl, Dryad, Sprite |
| Speed | Grace, Insight | Durability, Might | Eagle, Snake, Fox |

### 4. Signature Fusion Ability

A unique, powerful attack that **only exists when a Druid fuses with this creature**. This is the creature's ultimate expression — the ability it couldn't use alone but can channel through a Druid.

**Rules:**
- Every creature has exactly 1 Signature Fusion Ability
- These are stronger than normal skills — equivalent to Expert or Master tier player skills
- They define the fusion identity — fusing with a wolf feels different from fusing with a bear because of this ability
- Cannot be used outside of fusion

**Example Signature Fusion Abilities:**

| Creature | Signature Fusion | Effect |
|----------|-----------------|--------|
| Wolf | Predator's Fury | 3-hit physical attack, all hits apply bleeding, lifesteal 20% |
| Bear | Unstoppable Force | 1-hit massive physical, stun + armor ignore, knockback |
| Eagle | Sky Dive | 2-hit unevadable aerial strike, enemy grace -5 |
| Snake | Venom Cascade | 3-hit poison attack, uncleansable poison, enemy might -5 |
| Turtle | Ancient Wall | Full party warded + armor +10, taunt all enemies |
| Spider | Web Prison | Ensnare all enemies + poisoned + can't act 1 turn |

### 5. Personality

Every creature has a **personality** — a behavioral AI type that determines how it fights as a wild enemy AND how it behaves as a tamed summon on Auto mode. Personalities make each creature feel alive. Players don't just collect stats — they collect *characters*.

**Personalities:**

| Personality | Wild Behavior | Summon Auto Behavior | Example Species |
|-------------|--------------|---------------------|-----------------|
| **Aggressive** | Always attacks, even at low HP. Never uses Defense. Uses Utility only when HP < 15%. | Prioritizes Attack skill above all. Uses Defense only when Druid < 30% HP. | Wolf, Raptor, Panther |
| **Protective** | Uses Defense skill when any ally is below 70% HP. Otherwise attacks. | Uses Defense when *any* ally (not just Druid) is below 70% HP. Otherwise attacks. | Bear, Treant, Turtle |
| **Opportunist** | Targets the lowest HP enemy. Uses Utility proactively (even at high HP) to set up kills. | Targets weakest enemy. Uses Utility skill proactively when enemy is below 50% HP. | Eagle, Snake, Fox |
| **Guardian** | Uses Defense skill proactively — even at full HP. Attacks only after buffing. | Uses Defense skill on turn 1, then alternates Attack/Defense. | Crab, Golem, Boar |
| **Taunting** | Draws enemy aggro. Uses Defense to tank. Attacks when enemy is debuffed. | Draws enemy aggro. Uses Defense first, then attacks. Enemy targets this summon 50% more often. | Boar, Turtle, Troll |

**How personalities work:**
- Personality is assigned per **species** — all Grey Wolves are Aggressive, all Cave Bears are Protective
- Personality modifies the **Auto AI priority** — it doesn't change available skills, just which one the AI picks and when
- In **Manual mode**, personality is a visual label only — the player overrides it
- **Formations** can override personality — assigning "Back" to an Aggressive wolf makes it hold and use Utility instead of charging
- Personality affects **wild monster AI too** — an Aggressive wolf fights differently from a Guardian turtle even before taming

**Personality + Auto AI priority:**

```
Standard Auto AI (modified by personality):
  1. Enemy above 30% HP → Attack skill
  2. Enemy below 30% HP → Attack skill (going for kill)
  3. Druid below 50% HP → Defense skill (protecting Druid)
  4. Summon below 30% HP → Utility skill (surviving)
  5. Druid fused with this summon → N/A (inside the Druid)

Aggressive overrides:
  - Step 3: Only use Defense when Druid < 30% (not 50%)
  - Step 4: Only use Utility when summon < 15% (not 30%)
  - Always prefers Attack if available

Protective overrides:
  - Step 3: Use Defense when ANY ally < 70% HP (not just Druid at 50%)
  - Step 1-2: Still attacks, but Defense check comes FIRST

Opportunist overrides:
  - Target selection: always hits lowest HP enemy
  - Step 2: Uses Utility proactively when enemy < 50% (not just self-survival)

Guardian overrides:
  - Turn 1: Always uses Defense skill (proactive buff)
  - Then alternates: Attack → Defense → Attack → Defense

Taunting overrides:
  - Draws aggro: enemy targets this summon 50% more often
  - Step 3: Uses Defense when self < 60% HP (not just Druid at 50%)
  - Step 1-2: Attacks only after Defense is active
```

**Why this matters:**
- **Emotional attachment** — players remember their Protective bear that saved them, not just "the bear with +20% durability"
- **Strategic depth** — an Aggressive wolf and a Guardian turtle at the same power level play completely differently
- **No micromanagement needed** — personality makes Auto mode feel smart. The pack feels alive.
- **Wild enemy variety** — fighting an Aggressive wolf is different from fighting a Guardian turtle, even at the same level

---

## Monster Taming

### Tame Button

Available only to Druids. Appears as a third action button alongside Strike and Summon.

**Taming rules:**

| Rule | Detail |
|------|--------|
| HP threshold | Enemy must be below **30% HP** (normal), **15% HP** (boss), **10% HP** (legendary), **5% HP** (event boss) |
| One attempt | One tame attempt per enemy per combat |
| Success chance | `Druid cognition vs enemy resistance` — higher cognition = higher chance |
| Base chance (normal) | 40% at equal cognition. +5% per cognition point above enemy resistance. -5% per point below. Cap: 10%-90% |
| Base chance (boss) | 15% at equal cognition. +3% per cognition point above. -3% per point below. Cap: 5%-50% |
| Base chance (legendary) | 5% at equal cognition. +2% per cognition point above. -2% per point below. Cap: 2%-25% |
| Base chance (event boss) | 2% at equal cognition. +1% per cognition point above. -1% per point below. Cap: 1%-10% |
| Success | Monster joins bestiary permanently, removed from combat (not killed) |
| Failure (normal) | Monster becomes **enraged** — might +3, attacks immediately |
| Failure (boss) | Monster becomes **furious** — might +5, grace +3, attacks immediately, gains 1 extra turn |
| Failure (legendary) | Monster becomes **unstoppable** — all stats +5, attacks immediately, gains 2 extra turns, cleanses all debuffs |
| Failure (event boss) | Monster becomes **cataclysmic** — all stats +8, full heal, attacks immediately, gains 3 extra turns, cleanses all debuffs, enrages all allies |
| Bestiary cap | **50 tamed creatures total** — choose wisely |

**Cannot tame:**

| Category | Why |
|----------|-----|
| Constructs/Mechanical | No soul — machines can't be tamed |
| Undead | No living essence to connect with |
| Other players | Obviously |

**Can tame — by difficulty tier:**

| Tier | Tame Difficulty | HP Threshold | Base Chance | Examples |
|------|----------------|-------------|-------------|---------|
| Normal | Easy | 30% HP | 40% | Wolves, bears, eagles, snakes, boars |
| Mini-boss | Medium | 25% HP | 25% | Alpha wolf, giant spider queen, elder bear |
| Boss | Hard | 15% HP | 15% | Dragon whelp, troll king, hydra |
| Legendary | Hardest | 10% HP | 5% | Ancient dragon, kraken, phoenix |
| Event Boss | Haaaaarddeeeeest | 5% HP | 2% | World bosses, seasonal event bosses, raid bosses |

**Why tame a boss?** Because boss profiles are **expanded** — more passives, more skills, more power. A tamed dragon doesn't just give you one buff. It gives you five.

### Taming as Progression

The Druid's power curve isn't just leveling skills — it's **expanding the bestiary**. A level 30 Druid with 20 tamed creatures is dramatically stronger than a level 30 Druid with 5. The bestiary IS the power.

---

## Summon System

### Summon Button

Available only to Druids. Opens a dropdown of all tamed creatures.

**Summon rules:**

| Rule | Detail |
|------|--------|
| Max active summons | **1 per 5 Druid levels** (Level 5 = 1, Level 10 = 2, ... Level 50 = 10) |
| No duplicates | Can't summon 2 of the same species |
| Action cost | Summoning costs the Druid's turn action |
| Summon HP | Equal to what the creature would have at the Druid's level |
| Summon death | If a summon dies in combat, it returns to the bestiary. It can be re-summoned next combat. Summons don't permanently die |
| Buff duration | Passive buff is active while summon is on the field. If summon dies or is unsummoned, buff is lost |

### Summon Command System — Auto vs Manual

Each summon has a **mode toggle** on the battle screen: **Auto** or **Manual**. This is per-summon — the player can leave some on Auto while controlling others.

| Mode | How It Works |
|------|-------------|
| **Auto** | AI picks the skill based on HP thresholds (default — hands-off) |
| **Manual** | Player picks which of the summon's 3 skills to use this turn |

**Auto AI priority (default behavior — modified by personality):**

```
Each active summon on Auto:
  1. Enemy above 30% HP → Attack skill
  2. Enemy below 30% HP → Attack skill (going for kill)
  3. Druid below 50% HP → Defense skill (protecting Druid)
  4. Summon below 30% HP → Utility skill (surviving)
  5. Druid fused with this summon → N/A (inside the Druid)

  Note: Personality (Aggressive/Protective/Opportunist/Guardian/Taunting)
  modifies these thresholds. See Profile Structure § 5. Personality.
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

### Formation System

On top of Auto/Manual, each summon can be assigned a **Formation** — a persistent targeting directive that stays until changed. Formations work in **both** Auto and Manual mode.

| Formation | Behavior | Example |
|-----------|----------|--------|
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
- **Quick commands** (All Attack/All Defend) override Formations for one turn, then Formations resume
- **Personality** can be overridden by Formation — assigning "Back" to an Aggressive wolf makes it hold

### Turn Order

```
Druid's Turn:
  1. Druid picks their skill/action (Strike, skill, Summon, Tame, Fuse)
  2. For each active summon:
     → Auto: AI picks skill (highlighted as preview)
     → Manual: player picks skill (or Pass)
     → Fused: N/A (inside the Druid)
  3. Confirm turn
  4. Execution:
     a. Druid acts
     b. Each summon acts (in summon order)
     c. Summon buffs remain active on Druid
     d. Enemy acts
```

**The player controls the pack without micromanaging.** Auto is the baseline — Manual is an optional upgrade for players who want precision. Player decisions are:
- **Which animals to summon** (which buffs do I need?)
- **Auto or Manual?** (do I need to control this summon, or let the AI handle it?)
- **Which skill each summon uses** (when on Manual)
- **When to fuse** (which fusion ability do I need?)
- **When to tame** (is this monster worth adding?)

### When Manual Shines

| Scenario | Auto Would Do | Manual Lets You Do |
|----------|--------------|-------------------|
| Boss charging AoE nuke | Wolf keeps attacking (enemy >30%) | Wolf uses Guard Howl to warded the Druid |
| Enemy at 5% HP | Bear uses Iron Hide (bear HP low) | Bear uses Crushing Slam to finish the kill |
| Druid at 80% HP, summon at 80% | Both attack | Eagle uses Scout Eye for cognition buff before Druid's big spell |
| Stamina management | AI burns stamina fast | Pass on wolf this turn to regen stamina for next turn's Pack Call |
| Pack coordination | Each summon acts independently | Wolf Pack Calls, bear Crushing Slams, eagle Sky Dives — all in one turn |

**Balance:** Manual is strictly better in decision quality, but the summon's stats and skills don't change. Auto is never punished — it's the baseline. Manual is an optional skill ceiling for engaged players.

### Pack Synergy

Having multiple summons active creates **exponential synergy**:

| Active Summons | Synergy Name | Effect |
|----------------|-------------|--------|
| 1-2 | — | Normal — each acts independently |
| 3+ | **Pack Bond** | All summons +20% damage. Druid +5% all stats |
| 5+ | **Pack Hunt** | All summons +1 hit per attack. Druid +10% all stats |
| 7+ | **Pack Alpha** | Summons gain an extra action **every other turn**. Druid +15% all stats |
| 10 (max) | **The Wild Sovereign** | Every summon gains every other summon's passive buff. Druid +20% all stats. The Druid becomes a one-person army |

**Note on Pack Alpha:** Extra action every *other* turn means on turns 1, 3, 5, etc. each summon acts once. On turns 2, 4, 6, etc. each summon acts twice. With 10 summons that's 10-20 actions per turn — already devastating. The Druid's level 90 passive (Wild Sovereign) upgrades this to *every* turn.

This rewards **taming diversity** — 10 different species is stronger than 10 of the same type (which isn't possible anyway due to no duplicates, but the synergy makes diversity explicitly powerful).

---

## Fusion System

### How Fusion Works

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
| Summon state | Summon disappears (inside the Druid). Reappears at **full HP** when fusion ends |
| Recovery | **2 turns** before that summon can fuse again (cooldown) |
| No cooldown on fusion itself | Druid can immediately fuse with a different summon |

### Fusion Example — Wolf

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

### Multi-Fusion (Master Tier Passive)

At high levels, the Druid can fuse with **two summons simultaneously**. This stacks both creatures' stats, both attack riders, both defense passives, and grants both signature abilities. The Druid becomes a chimera — part wolf, part eagle, part human. This is the Druid's endgame fantasy.

---

## Bestiary UI — Character Screen

When playing a Druid, the character screen gains a **Bestiary tab**:

```
┌─────────────────────────────────────────────────┐
│  BESTIARY — 7 / 50 Tamed                        │
├─────────────────────────────────────────────────┤
│  ◆ Grey Wolf              Lv 45   Active        │
│    Buff: +15% Might, +10% Grace                 │
│    ATK: Savage Bite (bleeding)                  │
│    DEF: Guard Howl (warded on Druid)            │
│    UTI: Pack Call (summon attacks twice)        │
│    FUSION: Predator's Fury                      │
│                                                 │
│  ◆ Cave Bear               Lv 45   Active        │
│    Buff: +20% Durability, +15% Armor            │
│    ATK: Crushing Slam (stun)                    │
│    DEF: Iron Hide (armor +5)                    │
│    UTI: Hibernation (heal 10%)                  │
│    FUSION: Unstoppable Force                    │
│                                                 │
│  ◆ Storm Eagle             Lv 45   Inactive      │
│    Buff: +15% Grace, +10% Insight               │
│    ATK: Sky Dive (unevadable)                   │
│    DEF: Wind Shield (evasive on Druid)          │
│    UTI: Scout Eye (reveal weaknesses)           │
│    FUSION: Aerial Apex                          │
│                                                 │
│  ◆ Marsh Viper             Lv 45   Inactive      │
│    ...                                          │
│                                                 │
│  ◆ Night Owl               Lv 45   Inactive      │
│    ...                                          │
│                                                 │
│  ◆ Ancient Turtle          Lv 45   Inactive      │
│    ...                                          │
│                                                 │
│  ◆ Cave Spider             Lv 45   Inactive      │
│    ...                                          │
├─────────────────────────────────────────────────┤
│  Active: 2/9    Pack Synergy: None (need 3+)    │
│  Max Active: 9 (Level 45 ÷ 5)                   │
└─────────────────────────────────────────────────┘
```

- **Active** = currently summoned (on the battlefield)
- **Inactive** = tamed but not summoned (in reserve)
- **Level** = always matches Druid's level
- **Max Active** = Druid level ÷ 5

---

## Example Monster Profiles

### Profile: Grey Wolf

```python
{"id": "grey_wolf", "name": "Grey Wolf", "species": "beast",
 "archetype": "striker",
 "stats": {
   "might": {"base": 12, "growth": 1.2},
   "grace": {"base": 14, "growth": 1.3},
   "cognition": {"base": 6, "growth": 0.8},
   "insight": {"base": 5, "growth": 0.7},
   "essence": {"base": 7, "growth": 0.9},
   "durability": {"base": 10, "growth": 1.0}
 },
 "passive_buff": {"type": "might_bonus", "value": 0.15, "secondary": {"type": "grace_bonus", "value": 0.10}},
 "skills": {
   "attack": {"id": "savage_bite", "name": "Savage Bite",
     "power_type": "strike", "damage_type": "physical",
     "status_apply": "bleeding",
     "stat_mod": {"enemy": {"might": -2}}, "mod_duration": 2},
   "defense": {"id": "guard_howl", "name": "Guard Howl",
     "power_type": "buff",
     "self_status": "warded",
     "stat_mod": {"self": {"armor_bonus": 3}}, "mod_duration": 2},
   "utility": {"id": "pack_call", "name": "Pack Call",
     "power_type": "buff",
     "self_status": "inspired",
     "stat_mod": {"self": {"might": 3}}, "mod_duration": 2}
 },
 "signature_fusion": {"id": "predators_fury", "name": "Predator's Fury",
   "power_type": "strike", "damage_type": "physical",
   "hits": 3,
   "status_apply": "bleeding",
   "lifesteal": 0.20,
   "stat_mod": {"enemy": {"grace": -3}}, "mod_duration": 3}
}
```

### Profile: Cave Bear

```python
{"id": "cave_bear", "name": "Cave Bear", "species": "beast",
 "archetype": "bruiser",
 "stats": {
   "might": {"base": 16, "growth": 1.4},
   "grace": {"base": 6, "growth": 0.7},
   "cognition": {"base": 4, "growth": 0.5},
   "insight": {"base": 5, "growth": 0.6},
   "essence": {"base": 8, "growth": 0.8},
   "durability": {"base": 18, "growth": 1.5}
 },
 "passive_buff": {"type": "durability_bonus", "value": 0.20, "secondary": {"type": "armor_bonus", "value": 0.15}},
 "skills": {
   "attack": {"id": "crushing_slam", "name": "Crushing Slam",
     "power_type": "strike", "damage_type": "physical",
     "status_apply": "stunned",
     "stat_mod": {"enemy": {"armor_bonus": -3}}, "mod_duration": 2},
   "defense": {"id": "iron_hide", "name": "Iron Hide",
     "power_type": "buff",
     "self_status": "warded",
     "stat_mod": {"self": {"armor_bonus": 5}}, "mod_duration": 3},
   "utility": {"id": "hibernation", "name": "Hibernation",
     "power_type": "heal",
     "heal_percent": 0.10,
     "self_status": "warded",
     "stat_mod": {"self": {"durability": 3}}, "mod_duration": 2}
 },
 "signature_fusion": {"id": "unstoppable_force", "name": "Unstoppable Force",
   "power_type": "strike", "damage_type": "physical",
   "status_apply": "stunned",
   "stat_mod": {"enemy": {"armor_bonus": -5, "might": -4}}, "mod_duration": 3,
   "armor_ignore": true}
}
```

### Profile: Storm Eagle

```python
{"id": "storm_eagle", "name": "Storm Eagle", "species": "beast",
 "archetype": "speed",
 "stats": {
   "might": {"base": 8, "growth": 0.9},
   "grace": {"base": 16, "growth": 1.4},
   "cognition": {"base": 7, "growth": 0.9},
   "insight": {"base": 12, "growth": 1.2},
   "essence": {"base": 9, "growth": 1.0},
   "durability": {"base": 6, "growth": 0.6}
 },
 "passive_buff": {"type": "grace_bonus", "value": 0.15, "secondary": {"type": "insight_bonus", "value": 0.10}},
 "skills": {
   "attack": {"id": "sky_dive", "name": "Sky Dive",
     "power_type": "strike", "damage_type": "physical",
     "unevadable": true,
     "status_apply": "bleeding",
     "stat_mod": {"enemy": {"grace": -3}}, "mod_duration": 2},
   "defense": {"id": "wind_shield", "name": "Wind Shield",
     "power_type": "buff",
     "self_status": "evasive",
     "stat_mod": {"self": {"grace": 4}}, "mod_duration": 2},
   "utility": {"id": "scout_eye", "name": "Scout Eye",
     "power_type": "buff",
     "self_status": "inspired",
     "stat_mod": {"self": {"cognition": 4, "insight": 3}}, "mod_duration": 3}
 },
 "signature_fusion": {"id": "aerial_apex", "name": "Aerial Apex",
   "power_type": "strike", "damage_type": "physical",
   "hits": 2,
   "unevadable": true,
   "status_apply": "stunned",
   "stat_mod": {"enemy": {"grace": -5}}, "mod_duration": 3}
}
```

### Profile: Marsh Viper

```python
{"id": "marsh_viper", "name": "Marsh Viper", "species": "beast",
 "archetype": "striker",
 "stats": {
   "might": {"base": 8, "growth": 0.9},
   "grace": {"base": 12, "growth": 1.1},
   "cognition": {"base": 10, "growth": 1.2},
   "insight": {"base": 14, "growth": 1.3},
   "essence": {"base": 8, "growth": 0.9},
   "durability": {"base": 6, "growth": 0.6}
 },
 "passive_buff": {"type": "cognition_bonus", "value": 0.15, "secondary": {"type": "poison_chance", "value": 0.10}},
 "skills": {
   "attack": {"id": "venom_strike", "name": "Venom Strike",
     "power_type": "strike", "damage_type": "physical",
     "status_apply": "poisoned",
     "stat_mod": {"enemy": {"might": -3}}, "mod_duration": 3},
   "defense": {"id": "shed_skin", "name": "Shed Skin",
     "power_type": "heal",
     "heal_percent": 0.08,
     "cleanses": true,
     "self_status": "evasive"},
   "utility": {"id": "constrict", "name": "Constrict",
     "power_type": "debuff",
     "status_apply": "ensnared",
     "stat_mod": {"enemy": {"grace": -4, "might": -3}}, "mod_duration": 3}
 },
 "signature_fusion": {"id": "venom_cascade", "name": "Venom Cascade",
   "power_type": "strike", "damage_type": "physical",
   "hits": 3,
   "status_apply": "poisoned",
   "uncleansable": true,
   "stat_mod": {"enemy": {"might": -5}}, "mod_duration": 4}
}
```

### Profile: Ancient Turtle

```python
{"id": "ancient_turtle", "name": "Ancient Turtle", "species": "beast",
 "archetype": "tank",
 "stats": {
   "might": {"base": 10, "growth": 1.0},
   "grace": {"base": 4, "growth": 0.5},
   "cognition": {"base": 6, "growth": 0.7},
   "insight": {"base": 5, "growth": 0.6},
   "essence": {"base": 14, "growth": 1.3},
   "durability": {"base": 22, "growth": 1.8}
 },
 "passive_buff": {"type": "armor_bonus", "value": 0.25, "secondary": {"type": "essence_bonus", "value": 0.10}},
 "skills": {
   "attack": {"id": "shell_bash", "name": "Shell Bash",
     "power_type": "strike", "damage_type": "physical",
     "status_apply": "stunned",
     "stat_mod": {"enemy": {"armor_bonus": -2}}, "mod_duration": 2},
   "defense": {"id": "ancient_shell", "name": "Ancient Shell",
     "power_type": "defend",
     "self_status": "warded",
     "stat_mod": {"self": {"armor_bonus": 6, "essence": 3}}, "mod_duration": 3},
   "utility": {"id": "tidal_surge", "name": "Tidal Surge",
     "power_type": "heal",
     "heal_percent": 0.12,
     "self_status": "warded",
     "stat_mod": {"self": {"essence": 3}}, "mod_duration": 2}
 },
 "signature_fusion": {"id": "ancient_wall", "name": "Ancient Wall",
   "power_type": "defend",
   "self_status": "warded",
   "stat_mod": {"self": {"armor_bonus": 10, "essence": 5, "durability": 5}}, "mod_duration": 3,
   "taunt": true,
   "full_party": true}
}
```

### Profile: Cave Spider

```python
{"id": "cave_spider", "name": "Cave Spider", "species": "monster",
 "archetype": "caster",
 "stats": {
   "might": {"base": 6, "growth": 0.6},
   "grace": {"base": 10, "growth": 1.0},
   "cognition": {"base": 12, "growth": 1.2},
   "insight": {"base": 14, "growth": 1.3},
   "essence": {"base": 10, "growth": 1.0},
   "durability": {"base": 8, "growth": 0.8}
 },
 "passive_buff": {"type": "insight_bonus", "value": 0.15, "secondary": {"type": "ensnare_chance", "value": 0.10}},
 "skills": {
   "attack": {"id": "venom_bite", "name": "Venom Bite",
     "power_type": "strike", "damage_type": "magical",
     "status_apply": "poisoned",
     "stat_mod": {"enemy": {"grace": -2}}, "mod_duration": 3},
   "defense": {"id": "web_shield", "name": "Web Shield",
     "power_type": "defend",
     "self_status": "warded",
     "stat_mod": {"self": {"essence": 4}}, "mod_duration": 2},
   "utility": {"id": "web_trap", "name": "Web Trap",
     "power_type": "debuff",
     "status_apply": "ensnared",
     "stat_mod": {"enemy": {"grace": -4}}, "mod_duration": 3}
 },
 "signature_fusion": {"id": "web_prison", "name": "Web Prison",
   "power_type": "debuff", "damage_type": "magical",
   "status_apply": "ensnared",
   "cant_act": true,
   "status_apply_secondary": "poisoned",
   "stat_mod": {"enemy": {"grace": -5, "might": -4}}, "mod_duration": 3,
   "hits_all_enemies": true}
}
```

### Profile: Fire Elemental

```python
{"id": "fire_elemental", "name": "Fire Elemental", "species": "elemental",
 "archetype": "caster",
 "stats": {
   "might": {"base": 8, "growth": 0.8},
   "grace": {"base": 8, "growth": 0.8},
   "cognition": {"base": 14, "growth": 1.3},
   "insight": {"base": 16, "growth": 1.5},
   "essence": {"base": 12, "growth": 1.2},
   "durability": {"base": 8, "growth": 0.8}
 },
 "passive_buff": {"type": "essence_bonus", "value": 0.15, "secondary": {"type": "magic_resist", "value": 0.15}},
 "skills": {
   "attack": {"id": "fire_bolt", "name": "Fire Bolt",
     "power_type": "strike", "damage_type": "magical",
     "status_apply": "burning",
     "stat_mod": {"enemy": {"armor_bonus": -3}}, "mod_duration": 2},
   "defense": {"id": "flame_ward", "name": "Flame Ward",
     "power_type": "defend",
     "self_status": "warded",
     "stat_mod": {"self": {"essence": 4, "insight": 3}}, "mod_duration": 3},
   "utility": {"id": "ignite_ground", "name": "Ignite Ground",
     "power_type": "debuff", "damage_type": "magical",
     "status_apply": "burning",
     "stat_mod": {"enemy": {"grace": -3, "might": -2}}, "mod_duration": 3}
 },
 "signature_fusion": {"id": "inferno_burst", "name": "Inferno Burst",
   "power_type": "strike", "damage_type": "magical",
   "hits": 3,
   "status_apply": "burning",
   "stat_mod": {"enemy": {"armor_bonus": -5, "might": -4}}, "mod_duration": 4,
   "hits_all_enemies": true}
}
```

### Profile: Night Owl

```python
{"id": "night_owl", "name": "Night Owl", "species": "beast",
 "archetype": "support",
 "stats": {
   "might": {"base": 5, "growth": 0.5},
   "grace": {"base": 12, "growth": 1.1},
   "cognition": {"base": 16, "growth": 1.4},
   "insight": {"base": 14, "growth": 1.3},
   "essence": {"base": 12, "growth": 1.2},
   "durability": {"base": 7, "growth": 0.7}
 },
 "passive_buff": {"type": "cognition_bonus", "value": 0.15, "secondary": {"type": "insight_bonus", "value": 0.15}},
 "skills": {
   "attack": {"id": "talon_dive", "name": "Talon Dive",
     "power_type": "strike", "damage_type": "physical",
     "status_apply": "bleeding",
     "stat_mod": {"enemy": {"grace": -3}}, "mod_duration": 2},
   "defense": {"id": "night_veil", "name": "Night Veil",
     "power_type": "buff",
     "self_status": "evasive",
     "stat_mod": {"self": {"grace": 4, "essence": 3}}, "mod_duration": 3},
   "utility": {"id": "wisdom_gaze", "name": "Wisdom Gaze",
     "power_type": "buff",
     "self_status": "inspired",
     "stat_mod": {"self": {"cognition": 5, "insight": 4}}, "mod_duration": 3}
 },
 "signature_fusion": {"id": "midnight_revelation", "name": "Midnight Revelation",
   "power_type": "buff",
   "self_status": "inspired",
   "stat_mod": {"self": {"cognition": 8, "insight": 6, "essence": 5}}, "mod_duration": 4,
   "reveals_all_weaknesses": true,
   "guaranteed_crits": 3}
}
```

### Profile: Shadow Panther

```python
{"id": "shadow_panther", "name": "Shadow Panther", "species": "beast",
 "archetype": "striker",
 "stats": {
   "might": {"base": 14, "growth": 1.3},
   "grace": {"base": 16, "growth": 1.4},
   "cognition": {"base": 8, "growth": 0.9},
   "insight": {"base": 6, "growth": 0.7},
   "essence": {"base": 6, "growth": 0.7},
   "durability": {"base": 8, "growth": 0.8}
 },
 "passive_buff": {"type": "grace_bonus", "value": 0.20, "secondary": {"type": "evasion_bonus", "value": 0.15}},
 "skills": {
   "attack": {"id": "shadow_rip", "name": "Shadow Rip",
     "power_type": "strike", "damage_type": "physical",
     "hits": 2,
     "status_apply": "bleeding",
     "stat_mod": {"enemy": {"grace": -3}}, "mod_duration": 2},
   "defense": {"id": "shadow_step", "name": "Shadow Step",
     "power_type": "buff",
     "self_status": "evasive",
     "stat_mod": {"self": {"grace": 5}}, "mod_duration": 2},
   "utility": {"id": "prowl", "name": "Prowl",
     "power_type": "buff",
     "self_status": "hidden",
     "stat_mod": {"self": {"grace": 4, "might": 3}}, "mod_duration": 2}
 },
 "signature_fusion": {"id": "shadow_frenzy", "name": "Shadow Frenzy",
   "power_type": "strike", "damage_type": "physical",
   "hits": 4,
   "status_apply": "bleeding",
   "unevadable": true,
   "lifesteal": 0.15,
   "stat_mod": {"enemy": {"grace": -5}}, "mod_duration": 3}
}
```

### Profile: Forest Dryad

```python
{"id": "forest_dryad", "name": "Forest Dryad", "species": "magical",
 "archetype": "support",
 "stats": {
   "might": {"base": 5, "growth": 0.5},
   "grace": {"base": 8, "growth": 0.8},
   "cognition": {"base": 14, "growth": 1.3},
   "insight": {"base": 12, "growth": 1.1},
   "essence": {"base": 18, "growth": 1.6},
   "durability": {"base": 10, "growth": 1.0}
 },
 "passive_buff": {"type": "essence_bonus", "value": 0.20, "secondary": {"type": "regen", "value": 0.05}},
 "skills": {
   "attack": {"id": "thorn_whip", "name": "Thorn Whip",
     "power_type": "strike", "damage_type": "magical",
     "status_apply": "bleeding",
     "stat_mod": {"enemy": {"grace": -2}}, "mod_duration": 2},
   "defense": {"id": "bark_skin", "name": "Bark Skin",
     "power_type": "defend",
     "self_status": "warded",
     "stat_mod": {"self": {"armor_bonus": 4, "essence": 4}}, "mod_duration": 3},
   "utility": {"id": "healing_pollen", "name": "Healing Pollen",
     "power_type": "heal",
     "heal_percent": 0.12,
     "self_status": "warded",
     "stat_mod": {"self": {"essence": 3}}, "mod_duration": 2}
 },
 "signature_fusion": {"id": "gaia_embrace", "name": "Gaia's Embrace",
   "power_type": "heal",
   "heal_percent": 0.30,
   "self_status": "warded",
   "cleanses_all": true,
   "stat_mod": {"self": {"essence": 8, "durability": 5, "grace": 4}}, "mod_duration": 4,
   "full_party": true}
}
```

---

## Profile Tiers — Normal vs Boss vs Legendary vs Event

### Normal Creatures (1 Buff + 3 Skills + 1 Signature)

Standard profile. Most creatures in the game.

```
1 Passive Buff
3 Skills (Attack / Defense / Utility)
1 Signature Fusion Ability
6 Stats
```

### Mini-Boss Creatures (2 Buffs + 3 Skills + 1 Signature)

Stronger than normal. Elite versions of regular creatures.

```
2 Passive Buffs (stack on Druid while summoned)
3 Skills (Attack / Defense / Utility) — stronger variants
1 Signature Fusion Ability — enhanced
6 Stats — higher base + growth
```

### Boss Creatures (3 Buffs + 5 Skills + 2 Signatures)

Bosses have expanded profiles. This is what makes them bosses — not just bigger numbers, but **more tools**.

```
3 Passive Buffs (all stack on Druid while summoned)
5 Skills (2 Attack / 2 Defense / 1 Utility) — boss-grade power
2 Signature Fusion Abilities — the boss has TWO ultimates
6 Stats — significantly higher base + growth
Boss Aura — passive aura that affects the battlefield while summoned
```

**Boss Aura:** A passive battlefield effect that activates while the boss is summoned. This is unique to boss-tier creatures — normal creatures don't have auras.

| Boss Aura Example | Effect |
|-------------------|--------|
| Dragon's Presence | All enemies -10% to all stats while dragon is active |
| Troll King's Command | All allied summons +20% damage |
| Hydra's Terror | Enemies can't evade while hydra is active |
| Kraken's Domain | Battlefield becomes water terrain — enemies -grace, allies +essence |

### Legendary Creatures (5 Buffs + 5 Skills + 3 Signatures)

The most powerful tameable creatures. These are raid bosses, ancient dragons, world-tier threats.

```
5 Passive Buffs (all stack on Druid while summoned — this alone is game-changing)
5 Skills (2 Attack / 2 Defense / 1 Utility) — legendary-grade
3 Signature Fusion Abilities — THREE ultimates, the Druid chooses which to use each turn during fusion
6 Stats — massive base + growth
Legendary Aura — stronger version of boss aura, affects entire battlefield
Legendary Passive — a unique passive mechanic exclusive to this creature
```

**Legendary Passive:** A unique mechanic that only this creature possesses. Not a stat buff — a behavioral rule change.

| Legendary Passive Example | Effect |
|---------------------------|--------|
| Phoenix Rebirth | On death, the summon resurrects at 50% HP once per combat |
| Ancient Dragon's Wrath | Every 3rd turn, the summon breathes fire automatically (free action) |
| Kraken's Depths | Summon can't be killed while Druid is above 50% HP |
| Titan's Endurance | Summon takes 50% reduced damage from all sources |

### Event Boss Creatures (5+ Buffs + 5+ Skills + 3+ Signatures)

Seasonal, limited-time, world-event bosses. The rarest summons in the game. If you tame one of these, you have something almost no other player has.

```
5+ Passive Buffs (all stack — the Druid becomes a god while this is summoned)
5+ Skills (3 Attack / 2 Defense / 1+ Utility) — event-grade
3+ Signature Fusion Abilities — multiple ultimates
6 Stats — colossal base + growth
Event Aura — battlefield-wide effect that can't be dispelled
Event Passive — unique mechanic, stronger than legendary passive
Event Title — while summoned, the Druid gains a visible title (e.g., "Dragonlord", "Kraken Sovereign")
```

**Event Passive examples:**

| Event Passive Example | Effect |
|-----------------------|--------|
| World Dragon's Dominion | All enemies take 20% increased damage from ALL sources while dragon is active |
| Seasonal Wraith's Curse | Enemies can't heal while wraith is active |
| Raid Titan's Fortress | Full party gains immunity to one damage type (rotates each turn) |

### Why This Matters for the Druid

A Druid with 10 normal summons is strong. A Druid with 7 normal summons + 1 boss is stronger. A Druid with 5 normal + 2 bosses + 1 legendary is a raid boss themselves. A Druid with an event boss summoned is the thing other players form raids to fight.

The taming difficulty scales the reward:

| What You Tamed | What You Got |
|----------------|-------------|
| Normal creature | 1 buff, 3 skills, 1 fusion |
| Mini-boss | 2 buffs, 3 skills, 1 enhanced fusion |
| Boss | 3 buffs, 5 skills, 2 fusions, boss aura |
| Legendary | 5 buffs, 5 skills, 3 fusions, legendary aura, legendary passive |
| Event Boss | 5+ buffs, 5+ skills, 3+ fusions, event aura, event passive, visible title |

### Tier Classification Table

| Tier | Level Range | Buffs | Skills | Signatures | Aura | Tame HP | Tame Chance | Example |
|------|------------|-------|--------|------------|------|---------|-------------|---------|
| Basic | 1-10 | 1 | 3 | 1 | No | 30% HP | 40% | Grey Wolf, Marsh Viper |
| Advanced | 11-20 | 1 | 3 | 1 | No | 30% HP | 40% | Cave Bear, Storm Eagle |
| Expert | 21-30 | 1 | 3 | 1 | No | 30% HP | 40% | Shadow Panther, Cave Spider |
| Master | 31-40 | 1 | 3 | 1 | No | 30% HP | 40% | Fire Elemental, Forest Dryad |
| Mini-Boss | 15-40 | 2 | 3 | 1 | No | 25% HP | 25% | Alpha Wolf, Spider Queen |
| Boss | 20-50 | 3 | 5 | 2 | Yes | 15% HP | 15% | Dragon Whelp, Troll King |
| Legendary | 40+ | 5 | 5 | 3 | Yes+ | 10% HP | 5% | Ancient Dragon, Phoenix |
| Event Boss | 50+ | 5+ | 5+ | 3+ | Yes++ | 5% HP | 2% | World Dragon, Seasonal Wraith |

Higher tier creatures are exponentially harder to tame but provide exponentially more power. The jump from normal to boss isn't just bigger numbers — it's **more abilities, more buffs, more fusion options, and battlefield auras**.

---

## Summary

| Component | Normal | Mini-Boss | Boss | Legendary | Event Boss |
|-----------|--------|-----------|------|-----------|------------|
| Passive Buffs | 1 | 2 | 3 | 5 | 5+ |
| Skills | 3 (ATK/DEF/UTI) | 3 (enhanced) | 5 (2ATK/2DEF/1UTI) | 5 (legendary-grade) | 5+ (event-grade) |
| Signature Fusions | 1 | 1 (enhanced) | 2 | 3 | 3+ |
| Battlefield Aura | No | No | Yes | Yes (stronger) | Yes (strongest) |
| Unique Passive | No | No | No | Yes | Yes (stronger) |
| Visible Title | No | No | No | No | Yes |
| Stats | 6 | 6 (higher) | 6 (high) | 6 (massive) | 6 (colossal) |
| Tame HP Threshold | 30% | 25% | 15% | 10% | 5% |
| Tame Base Chance | 40% | 25% | 15% | 5% | 2% |
| Failure Penalty | Enraged | Enraged | Furious (+1 turn) | Unstoppable (+2 turns, cleanse) | Cataclysmic (+3 turns, full heal, cleanse, enrage allies) |

**The same skills a monster uses against you are the skills you control when you tame it. The bestiary is the Druid's power. The pack is the Druid's army. The fusion is the Druid's transformation. And if you somehow tame a dragon — you don't just have a pet. You have a war.**
