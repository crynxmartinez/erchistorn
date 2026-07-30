# Alchemist Mastery — 30 Skills + Imbue System + Combo Flow

**Role:** The Transmuter — a close-range katar fighter who transmutes skills onto their blade, punching enemies with loaded effects. Every strike is an experiment. Every following strike is the improved formula.
**Masteries per trainer:** 3 (Alchemist + 2 others)
**Trainers teaching Alchemist:** Warforge, Riverguard, Rindivar Grove, Silvergate

---

## Alchemist Identity

**Core loop:** Imbue skill onto katar → strike to deliver → observe result → build Combo Flow → spend CF to adapt → re-imbue without losing momentum

- **Weapon: Katar** — punching dagger. The Alchemist fights with their fists, not vials.
- **Katar shape-shifting** — every imbue physically transforms the blade. Acid = liquid blade, Frost = ice spike, Lightning = claw, Poison = needle. Players see what's loaded at a glance.
- **Range 0 (melee)** when striking with imbue — the katar is a fist weapon. Range 1 for non-imbued cast skills.
- **Two-button combat** — Imbue (load a skill onto the katar) + Strike (punch with the loaded skill). Imbuable skills cannot be cast normally — they must be loaded.
- **Skill riding on fist** — when imbued, every strike deals punch damage + the skill's full effect (status, stat_mod) as a rider. You're not casting — you're punching someone with a skill.
- **Imbue mini-rules** — each imbue has a unique behavioral rule, not just a different status. Acid stacks armor reduction. Frost freezes on 4th hit. Lightning chains every 3rd hit. Poison scales with time. Choosing an imbue changes HOW you fight.
- **Combo Flow = scientific method** — CF is not a combo meter. It's the Alchemist continuously calculating and refining the exchange. Each strike is an experiment. Each following strike is the improved formula. CF is **spendable** — the Alchemist chooses when to cash in for adaptation, not just escalation.
- **Adaptive transmutation** — switch imbues mid-combat to adapt to enemy weaknesses. CF is preserved across swaps. Rushing Strike can re-imbue AND punch in the same action — momentum never dies.
- **Pre-action imbue** — imbuing before combat doesn't cost a turn. The Alchemist always enters combat loaded.
- **Charge-based imbues** — each imbue lasts a set number of strikes before fading. Forbidden Formula = 1 charge (nuke), Corrosive Mist = 3 charges (sustained).
- **Self-transmutation** — utility skills alter the Alchemist's own body (Iron Skin, Mutagen, Swift) or the terrain (Stone Wall, Spike Field). FMA-style: clap hands → transmute.
- **No resource bar** — the weapon IS the resource. The katar stores current imbue, charges, and cooldown. No mana, no combo meter UI. The blade tells you everything.
- **No throwing** — the Alchemist doesn't throw potions. They transmute. Clap hands → katar changes → punch.

### The Imbue System

The Alchemist's unique mechanic. Instead of casting skills one at a time with cooldowns, the Alchemist **imbues a skill onto their katar** — the skill doesn't cast, it **loads**. Every strike now deals physical punch damage + the skill's full effect as a rider.

**How it works:**
- **Imbue action** — transmute a skill onto the katar (clap hands → blade gains the skill's properties AND shape)
- **Pre-combat:** Imbue freely — no turn cost, combat hasn't started yet
- **In-combat:** Re-imbuing costs your turn — BUT Rushing Strike can re-imbue AND strike in the same action (see Strike Skills)
- **Charges** — each imbue lasts a set number of strikes. When charges run out, the imbue fades and the skill goes on cooldown.
- **Re-imbuing the same skill** refreshes charges (but still costs a turn in combat)
- **Only 1 imbue active at a time** — the katar holds one skill

**Imbue mini-rules — each imbue changes HOW you fight:**
Every imbue has a unique behavioral rule beyond just applying a different status. This means choosing an imbue is a tactical decision, not a numerical one.

| Imbue | Mini-Rule | Blade Shape |
|-------|-----------|-------------|
| Acid Bomb | Every hit reduces armor **more** — stacking -1 armor per hit on top of base -3 | Liquid blade (green, dripping, flexible — metal flows like mercury) |
| Flash Powder | Every hit reduces enemy accuracy further — -1 grace per hit on top of base -2 | Mirror edge (polished, reflective, blinding glints) |
| Frost Mixture | Every hit slows. **4th hit freezes** (enemy skips next turn) | Long ice spike (extended, crystalline, frost mist) |
| Lightning Bottle | Every **3rd hit** chains to a 2nd target | Claw (forked into 3 prongs, arcing blue-white) |
| Poison Capsule | Damage **increases** the longer combat lasts — +10% per turn elapsed | Needle (thin, hollow, drips venom — syringe-like) |
| Corrosive Mist | Feeds on existing statuses — each status on enemy = +50% armor reduction | Eroding blade (pitted, smoking, degrading and reforming) |
| Living Slime | Every hit slows more — **3rd hit immobilizes** (can't move, can still attack) | Whip (extending, retracting, translucent green strands) |
| Transmutation Touch | Every hit converts more — **2nd hit** turns armor to paper (0 armor_bonus) | Dull edge (flat grey, no reflection, reeks of ozone) |
| Explosive Chain | Every hit detonates — each strike hits **2x** | Jagged crackling blade (sparking, unstable) |
| Forbidden Formula | 1 charge. True damage. **All statuses at once.** Katar cracks after. | Shifting (flickers between all shapes — can't settle) |

**Why mini-rules matter:**
- Frost = control (slow → freeze on 4th hit) — use when enemy is fast
- Lightning = AoE pressure (chain every 3rd hit) — use vs multiple enemies
- Poison = scaling (gets stronger over time) — use in long fights
- Acid = armor shred (stacking reduction) — use vs heavy armor
- Slime = lockdown (immobilize on 3rd) — use vs mobile enemies
- Explosive = raw damage (2x hits) — use when you need burst
- The Alchemist reads the enemy, chooses the imbue that exploits the weakness, and adapts

### Combo Flow System — The Scientific Method in Combat

Every strike builds **Combo Flow (CF)**. But CF is not a combo meter — it's the Alchemist **observing, adjusting, and optimizing** the exchange between katar and enemy. Each strike is an experiment. Each following strike is the improved formula.

**How it works:**
- Each strike generates **+1 CF** (Flurry generates +3, one per hit)
- CF is **spendable** — the Alchemist chooses when to cash in, not auto-triggered
- CF **does NOT reset** when switching imbues — analysis carries across experiments
- CF **resets to 0** when:
  - The Alchemist gets `stunned` (interrupted — experiment ruined)
  - The Alchemist skips a turn (doesn't strike — data lost)
  - Combat ends

**CF Spend Options — the Alchemist adapts:**

| CF Cost | Ability | What It Represents |
|---------|---------|-------------------|
| 5 CF | **Analysis** | Reveal one enemy weakness — which imbue they're most vulnerable to. The Alchemist studies the enemy. |
| 10 CF | **Adjustment** | Enhance the current imbue's mini-rule (Frost freezes on 3rd hit instead of 4th, Lightning chains on 2nd hit, Poison gains +20% per turn, etc.). The Alchemist refines the formula. |
| 15 CF | **Optimization** | Strike cooldowns reduced by 1 for 3 turns, OR next re-imbue is a free action. The Alchemist streamlines the process. |
| 20 CF | **Perfect Formula** | Choose ONE culmination (see below). The Alchemist has mastered the exchange. |

**20 CF — Perfect Formula choices:**
- **Perfect Delivery** — Next strike: +2 hits (both carry imbue at +2 stacks)
- **Perfect Conversion** — Refresh active imbue's charges to full (no re-imbue needed)
- **Perfect Sequence** — Re-imbue AND strike in the same turn (no momentum loss)
- **Perfect Breakdown** — Next strike ignores all armor and deals true damage

**Now the player thinks:**
- "I have 18 CF. Do I spend 15 to make re-imbueing free? Or save for 20 to get Perfect Breakdown? Or spend 10 to enhance my acid so it stacks faster?"
- "Enemy is fast — I should spend 5 CF on Analysis to confirm Frost is the weakness, then switch."
- "I'm at 20 CF with 1 charge left on Poison — Perfect Conversion refreshes charges AND keeps my CF-enhanced poison scaling. That's better than Perfect Delivery."

**Example combat flow:**
```
Pre-combat: Imbue Poison Capsule (4 charges, needle blade)

Turn 1: Strike Quick Jab     → punch + poisoned + -3 might     (CF=1, 3 charges left)
Turn 2: Strike Flurry (3)    → 3 punches + 3x poisoned         (CF=4, 0 charges — fades)
Turn 3: Rushing Strike       → re-imbue Acid + gap-close + punch (CF=5, 3 charges — NO dead turn!)
Turn 4: Spend 5 CF → Analysis → reveals enemy weak to Frost     (CF=0)
Turn 5: Rushing Strike       → re-imbue Frost + punch           (CF=1, 3 charges)
Turn 6: Strike Flurry (3)    → 3 punches + 3x ensnared + 4th hit FREEZES (CF=4, 0 charges)
Turn 7: Rushing Strike       → re-imbue Lightning + punch       (CF=5, 2 charges)
Turn 8: Strike Flurry (3)    → 3 punches + 3rd hit CHAINS      (CF=8, 0 charges)
Turn 9: Spend 5 CF → Analysis → confirms Poison weakness        (CF=3)
Turn 10: Rushing Strike      → re-imbue Poison + punch          (CF=4, 4 charges)
Turn 11: Strike Flurry (3)   → 3 punches + poison scaling +30%  (CF=7)
Turn 12: Strike Quick Jab    → punch + poison scaling +40%      (CF=8, 2 charges)
Turn 13: Strike Flurry (3)   → 3 punches + poison scaling +60%  (CF=11, 0 charges)
Turn 14: Spend 10 CF → Adjustment → Poison now +30% per turn    (CF=1)
Turn 15: Rushing Strike      → re-imbue Poison + punch +90%     (CF=2, 4 charges)
```

**Why this works:**
- **Scientific method fantasy** — the Alchemist observes (Analysis), adjusts (Adjustment), optimizes (Optimization), and perfects (Perfect Formula). CF is intelligence, not just momentum.
- **Decisions, not escalation** — the player chooses when to spend CF and what to spend it on. 18 CF is a real choice.
- **Imbue swaps don't break flow** — Rushing Strike re-imbues AND punches. CF carries across swaps. The Alchemist never has a dead turn.
- **Stun = reset** — enemies have counterplay. CC the Alchemist to ruin their experiment.
- **Can't stall** — skipping a turn resets CF. The Alchemist must keep experimenting.
- **Adaptation, not just damage** — CF can reveal weaknesses, enhance imbues, reduce cooldowns, or deliver a perfect strike. The Alchemist adapts to the enemy, not just hits harder.

### Skill Types — The Three Categories

The 30 skills split into 3 types:

**Type 1: Imbuable Skills (enemy-affecting) — load onto katar**
These are skills that affect the enemy — debuffs, enemy transmutations, alchemical strikes. When imbued, their full effect (status_apply, stat_mod against enemy) rides on every punch. They **cannot be cast normally** — they must be loaded onto the katar.

**Type 2: Strike Skills (punch patterns) — the delivery**
These are HOW you punch. Different strikes = different attack patterns (heavy, flurry, rushing, etc.). The imbued skill's effect rides on top. The strike determines **how** you hit — the imbue determines **what** it does.

**Type 3: Cast Skills (self/utility) — used normally**
These affect the Alchemist or the environment — buffs, heals, defends, terrain transmutation. Cast normally with cooldowns. Cannot be imbued.

**The combo math:** 10 imbuable skills × 10 strike patterns = **100 possible attacks** from 20 skills. The Alchemist has the most combat variety from the fewest buttons.

### Stat Focus

| Stat | Priority | Why |
|------|----------|-----|
| `might` | Primary | Katar strikes scale with physical power — the punch is the base damage |
| `grace` | Primary | Melee accuracy + dodge — the Alchemist is in the enemy's face |
| `durability` | Secondary | Melee range = getting hit. Need to survive. |
| `cognition` | Secondary | Skill capacity — more imbue/strike options |
| `essence` | Minimal | Transmutation is alchemical, not magical |
| `insight` | Minimal | Not a caster — the katar does the talking |
| `armor_bonus` | Minimal | Relies on Iron Skin Transmutation for defense |

### Status Identity

| Category | Statuses | How the Alchemist Uses Them |
|----------|----------|---------------------------|
| **Signature** | `burning`, `poisoned`, `ensnared` | Acid, poison, and frost — the three core alchemical elements. Applied via imbued strikes. |
| **Secondary** | `stunned`, `blinded`, `shaken`, `bleeding` | Lightning, flash, transmutation, and stone imbues. Tactical disruption. |
| **Rare** | `warded`, `evasive`, `inspired`, `hidden` | Self-transmutation buffs. The Alchemist enhances themselves, not others. |
| **Unique** | `frozen` | Not yet — potential future imbue upgrade. |

### Trigger Identity

| Category | Triggers | How the Alchemist Uses Them |
|----------|----------|---------------------------|
| **Primary** | `always` | Most imbues and strikes have no condition — punch on demand |
| **Secondary** | `opponent_status`, `opponent_wounded` | Conditional imbues (Corrosive Mist needs existing status, Transmutation Touch needs wounded enemy) |
| **Rare** | `low_hp` | Emergency skills (Forbidden Formula, Phoenix Mixture, Philosopher's Transmutation) |

### What the Alchemist Does NOT Do

- **No ranged strikes** — imbued strikes are range 0 (melee). The katar is a fist weapon.
- **No casting imbuable skills** — if a skill is imbuable, you CAN'T cast it normally. It must be loaded onto the katar.
- **No throwing** — no potions, no vials, no bombs. The Alchemist transmutes, then punches.
- **No summoning** — no pets, no constructs, no homunculus. Terrain transmutation only.
- **No AoE** — except Spinning Strike (adjacent only). Single-target focused.
- **No healing others** — all heals are self-drinks. The Alchemist is selfish.
- **No stealth** — Smoke Transmutation grants brief `hidden`, but not a stealth playstyle.
- **No staves, no wands** — the katar is the only weapon. The Alchemist transmutes the blade, not a casting implement.

---

## Skill Structure

All skills use the new format — no `power` or `skill_capacity_cost`.

| Field | Description |
|-------|-------------|
| `type` | `imbuable`, `strike`, or `cast` — determines how the skill is used |
| `power_type` | strike, defend, heal, debuff, buff (cast skills only) |
| `damage_type` | physical, magical, true (strikes only) |
| `trigger` | always, low_hp, opponent_wounded, opponent_status, opening_move |
| `imbue_charges` | Number of strikes the imbue lasts before fading (imbuable skills only) |
| `imbue_status` | Status applied to enemy per strike while imbued (imbuable skills only) |
| `imbue_stat_mod` | Stat changes applied to enemy per strike while imbued (imbuable skills only) |
| `imbue_mod_duration` | How many turns imbue_stat_mod lasts (imbuable skills only) |
| `imbue_mini_rule` | Unique behavioral rule for the imbue (imbuable skills only) — e.g. freeze_on_4th_hit, chain_on_3rd_hit, stacking_armor_shred |
| `blade_shape` | Visual transformation of the katar when imbued (imbuable skills only) — e.g. liquid, claw, needle, ice_spike |
| `hits` | Number of hits per strike (strike skills only) |
| `cf_gain` | Combo Flow gained per use (strike skills only) |
| `strike_rule` | Unique mechanical rule for the strike (strike skills only) — e.g. never_misses, armor_break, gap_close_and_reload, interrupt, cf_consumer |
| `legendary_rule` | Unique legendary mechanic (legendary skills only) — e.g. auto_adapt_katar, infinite_charges_max_mini_rules |
| `status_apply` | Status inflicted on enemy (cast skills only) |
| `self_status` | Status applied to self (cast skills only) |
| `stat_mod` | Temporary stat changes (cast skills only) |
| `mod_duration` | How many turns stat_mod lasts |
| `heal_percent` | Heals X% of max HP (cast heal skills only) |
| `cooldown` | Cooldown after charges deplete (imbuable) or after use (cast/strike) |

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

| Tier | Level Req | Gold Cost | Learn Time | Count | Imbuable | Strikes | Cast |
|------|-----------|-----------|------------|-------|----------|---------|------|
| Basic | 1 | 50g | 5 min | 6 | 2 | 2 | 2 |
| Advanced | 3 | 150g | 30 min | 7 | 3 | 2 | 2 |
| Expert | 8 | 400g | 1 hr | 7 | 4 | 3 | 0 |
| Master | 15 | 1000g | 1 hr | 8 | 1 | 3 | 4 |
| Legendary | 20 | 2500g | 1 day | 2 | 0 | 1 | 1 |

---

## Basic Tier (Level 1, 50g, 5min) — 2 Imbuable, 2 Strike, 2 Cast

### 1. Acid Bomb
```python
{"id": "acid_bomb", "name": "Acid Bomb", "type": "imbuable", "trigger": "always",
 "imbue_charges": 3,
 "imbue_status": "burning",
 "imbue_stat_mod": {"enemy": {"armor_bonus": -3}},
 "imbue_mod_duration": 2,
 "imbue_mini_rule": "stacking_armor_shred",
 "blade_shape": "liquid",
 "cooldown": 4}
```
**Description:** The Alchemist claps their hands over the katar. The metal liquefies — green, dripping, flexible. The blade flows like mercury, eating through whatever it touches. Every punch melts armor on contact, and **each subsequent hit shreds more** — -1 additional armor per strike on top of the base -3. The acid compounds. By the third hit, the enemy might as well be naked.
**Narrative:** The Alchemist presses their palms together. The transmutation circle flashes — brief, blue, gone. The katar changes. The metal doesn't just coat — it *liquefies*. The blade hangs like mercury, dripping green, reshaping with every movement. The Alchemist doesn't throw anything. They punch. The first strike lands and the enemy's chestplate sizzles — -3 armor, gone. The second punch hits the same spot and the acid has already started — -4 more, the metal peeling. The third finds flesh — -5, and the armor is a memory. The acid doesn't just burn. It *compounds*. 3 charges. Liquid blade.

**Mini-Rule: Stacking Armor Shred** — Each hit adds -1 more `armor_bonus` reduction on top of the base -3. Hit 1: -3. Hit 2: -4. Hit 3: -5. The longer the acid works, the less armor matters.

---

### 2. Flash Powder
```python
{"id": "flash_powder_alch", "name": "Flash Powder", "type": "imbuable", "trigger": "always",
 "imbue_charges": 3,
 "imbue_status": "blinded",
 "imbue_stat_mod": {"enemy": {"grace": -2}},
 "imbue_mod_duration": 2,
 "imbue_mini_rule": "stacking_accuracy_drain",
 "blade_shape": "mirror",
 "cooldown": 4}
```
**Description:** The Alchemist transmutes the katar's edge into a mirror surface — polished, reflective, blinding. Every strike releases a flash on impact, and **each subsequent hit drains more accuracy** — -1 additional grace per strike on top of the base -2. The enemy swings at shadows. By the third hit, they're punching empty air.
**Narrative:** The Alchemist claps. The katar doesn't gleam — it *mirrors*. The blade becomes polished silver, reflecting light in every direction. The first punch lands and the flash blinds — -2 grace, the enemy sees stars. The second punch, and the stars get worse — -3, they're swinging at shapes. The third — -4, and the shapes aren't there. The enemy can't fight what they can't see, and every hit makes them blinder. 3 charges. Mirror blade.

**Mini-Rule: Stacking Accuracy Drain** — Each hit adds -1 more `grace` reduction on top of the base -2. Hit 1: -2. Hit 2: -3. Hit 3: -4. The enemy's accuracy crumbles with every flash.

---

### 3. Quick Jab
```python
{"id": "quick_jab", "name": "Quick Jab", "type": "strike",
 "damage_type": "physical", "trigger": "always",
 "hits": 1,
 "cf_gain": 1,
 "strike_rule": "never_misses",
 "cooldown": 1}
```
**Description:** A fast, direct katar punch. Low damage, but **never misses** — ignores enemy `evasive` and `hidden`. The bread-and-butter strike for building CF and applying imbue effects when the enemy tries to dodge.
**Narrative:** No windup. No flourish. The Alchemist steps in and punches — fast, clean, surgical. The katar finds the gap between armor plates and slips in. The enemy tries to dodge. The katar is already there. It's not a heavy hit. It doesn't need to be. It's the first note of a combo, and the Alchemist is just getting started. The enemy can't evade what they can't predict.

**Strike Rule: Never Misses** — Ignores `evasive` and `hidden` statuses. The Alchemist's analysis is too precise. When the enemy tries to dodge, Quick Jab finds them anyway.

---

### 4. Heavy Crush
```python
{"id": "heavy_crush", "name": "Heavy Crush", "type": "strike",
 "damage_type": "physical", "trigger": "always",
 "hits": 1,
 "cf_gain": 1,
 "strike_rule": "armor_break",
 "cooldown": 2}
```
**Description:** A devastating overhead katar slam. High damage with **permanent armor break** — -2 `armor_bonus` that doesn't recover. The big delivery for when you need one punch to count AND weaken the enemy for the rest of the fight.
**Narrative:** The Alchemist raises the katar overhead. Both hands. Full body weight behind it. The blade comes down like a guillotine — through guard, through armor, through bone. It's not fast. It's not clever. It's just heavy. And when it lands, the armor doesn't just dent — it *breaks*. The -2 armor is permanent. The enemy can't repair it. The imbue rides the impact deep — acid burns farther, poison spreads wider, lightning arcs longer. The heavy hit makes everything worse, and the armor break makes sure it stays worse.

**Strike Rule: Armor Break** — -2 `armor_bonus` permanently (not temporary like stat_mod). The damage compounds across the entire fight. Every Heavy Crush makes the enemy more vulnerable to everything that follows.

---

### 5. Healing Draught
```python
{"id": "healing_draught", "name": "Healing Draught", "type": "cast",
 "power_type": "heal", "trigger": "low_hp",
 "self_status": "warded",
 "heal_percent": 0.10,
 "stat_mod": {"self": {"essence": 1}}, "mod_duration": 2,
 "cooldown": 3}
```
**Description:** The one non-transmute skill. A quick-drink crimson potion that closes wounds and wards the body. The Alchemist's emergency button.
**Narrative:** The Alchemist doesn't pray. They drink. The vial tilts, the crimson liquid flows, and the wounds close. Not magic — chemistry. The body knows what to do; the draught just tells it to do it faster. The Alchemist wipes their mouth. The bottle is empty. The bleeding has stopped. Triggers when HP is low.

---

### 6. Iron Skin Transmutation
```python
{"id": "iron_skin_transmutation", "name": "Iron Skin Transmutation", "type": "cast",
 "power_type": "buff", "trigger": "always",
 "self_status": "warded",
 "stat_mod": {"self": {"armor_bonus": 4}}, "mod_duration": 3,
 "cooldown": 4}
```
**Description:** The Alchemist claps their hands to their own chest. Skin transmutes to steel — grey, smooth, reflective. The enemy's blade lands and skids.
**Narrative:** The Alchemist presses their palms to their own chest. The transmutation is different — not the katar, not the ground, but themselves. The skin ripples. Grey. Smooth. Cold. It doesn't feel like flesh anymore. It feels like plate. The enemy's blade lands and skids off like rain on stone. The Alchemist doesn't flinch. They're a wall now. A wall with a katar.

---

## Advanced Tier (Level 3, 150g, 30min) — 3 Imbuable, 2 Strike, 2 Cast

### 7. Frost Mixture
```python
{"id": "frost_mixture", "name": "Frost Mixture", "type": "imbuable", "trigger": "always",
 "imbue_charges": 3,
 "imbue_status": "ensnared",
 "imbue_stat_mod": {"enemy": {"grace": -2, "might": -2}},
 "imbue_mod_duration": 3,
 "imbue_mini_rule": "freeze_on_4th_hit",
 "blade_shape": "ice_spike",
 "cooldown": 4}
```
**Description:** The Alchemist transmutes the katar into a long ice spike — crystalline, extended, trailing frost mist. Every punch slows the enemy more, and the **4th hit freezes them solid** — enemy skips their next turn. The control imbue. Use against fast enemies.
**Narrative:** The Alchemist claps. The katar doesn't change color — it changes state. The metal crystallizes, extends, becomes a spike of ice longer than the original blade. Frost mist curls off it. The first punch lands and the enemy's skin frosts — they're slower. The second, and the frost reaches their joints — they're sluggish. The third, and their breath visibleizes — they're struggling. The fourth hit — they freeze. Solid. They can't move. They can't act. They stand there, encased in ice, while the Alchemist watches and plans the next experiment. 3 charges. Ice spike blade.

**Mini-Rule: Freeze on 4th Hit** — Every hit applies `ensnared` and slows. On the 4th hit total (across all strikes while this imbue is active), the enemy is **frozen** — they skip their next turn entirely. The Alchemist's control option. Use Flurry to reach the 4th hit fast.

---

### 8. Lightning Bottle
```python
{"id": "lightning_bottle", "name": "Lightning Bottle", "type": "imbuable", "trigger": "always",
 "imbue_charges": 2,
 "imbue_status": "stunned",
 "imbue_stat_mod": {"enemy": {"grace": -2, "armor_bonus": -2}},
 "imbue_mod_duration": 2,
 "imbue_mini_rule": "chain_on_3rd_hit",
 "blade_shape": "claw",
 "cooldown": 5}
```
**Description:** The Alchemist transmutes the katar into a lightning claw — forked into 3 prongs, arcing blue-white between tines. Every punch locks the enemy's muscles, and the **3rd hit chains to a 2nd target**. The AoE pressure imbue. Use against groups.
**Narrative:** The Alchemist claps. The katar doesn't just glow — it *forks*. The blade splits into three prongs, lightning arcing between them like a cage. The first punch lands and the enemy seizes — electricity through every nerve. The second, and they can't think straight. The third hit — the lightning doesn't stay in one body. It *chains*. The arc jumps from the primary target to whoever's standing too close, hitting both. The Alchemist doesn't aim the chain. The lightning finds its own path. 2 charges. Claw blade.

**Mini-Rule: Chain on 3rd Hit** — Every 3rd hit (across all strikes while this imbue is active) chains to a 2nd target, dealing 50% damage and applying the stun. Use Flurry to trigger the chain in a single turn.

---

### 9. Poison Capsule
```python
{"id": "poison_capsule", "name": "Poison Capsule", "type": "imbuable", "trigger": "always",
 "imbue_charges": 4,
 "imbue_status": "poisoned",
 "imbue_stat_mod": {"enemy": {"might": -3, "cognition": -2}},
 "imbue_mod_duration": 3,
 "imbue_mini_rule": "scaling_damage_over_time",
 "blade_shape": "needle",
 "cooldown": 4}
```
**Description:** The Alchemist transmutes the katar into a hollow needle — thin, precise, dripping venom from the tip. Every punch injects poison, and **damage increases the longer combat lasts** — +10% per turn elapsed. The scaling imbue. Use in long fights.
**Narrative:** The Alchemist claps. The katar doesn't just change — it *thins*. The blade becomes a needle, hollow, precise, with venom dripping from the tip like a syringe. The first punch is a scratch — the enemy barely notices. But the poison is patient. Turn 2: +10% damage. Turn 5: +50%. Turn 10: +100%. The longer the fight, the more the venom burns. The enemy thinks they're winning because the early hits are weak. They're wrong. The Alchemist is just letting the formula mature. 4 charges. Needle blade.

**Mini-Rule: Scaling Damage Over Time** — Poison damage increases +10% per turn elapsed in combat. Turn 1: base damage. Turn 5: +50%. Turn 10: +100%. The Alchemist's long-game imbue. Weak early, devastating late. Pair with Flurry for maximum poison application.

---

### 10. Flurry
```python
{"id": "flurry", "name": "Flurry", "type": "strike",
 "damage_type": "physical", "trigger": "always",
 "hits": 3,
 "cf_gain": 3,
 "strike_rule": "cf_builder",
 "cooldown": 3}
```
**Description:** Three rapid katar punches in succession. Each hit carries the imbue — triple status application in one turn. **The ultimate CF builder** — +3 CF per use, triple imbue mini-rule procs. Low damage, but the setup strike that makes everything else work.
**Narrative:** The Alchemist doesn't wind up. They just go — one-two-three, fast as breathing. The katar is a blur. Each punch lands in the same spot, driving the imbue deeper with every hit. Acid eats through three layers in one turn. Poison injects three doses. Frost counts as 3 hits toward the freeze. Lightning counts as 3 hits toward the chain. The enemy doesn't have time to react between hits. They barely have time to fall. And the Alchemist just gained 3 CF — closer to Analysis, closer to Adjustment, closer to the Perfect Formula.

**Strike Rule: CF Builder** — Generates +3 CF (triple normal). Also procs imbue mini-rules 3 times in one turn — Frost freeze counter +3, Lightning chain counter +3, Acid armor shred stacks 3x. The setup strike that accelerates everything.

---

### 11. Rushing Strike
```python
{"id": "rushing_strike", "name": "Rushing Strike", "type": "strike",
 "damage_type": "physical", "trigger": "always",
 "hits": 1,
 "cf_gain": 1,
 "strike_rule": "gap_close_and_reload",
 "cooldown": 2}
```
**Description:** The Alchemist closes the gap AND re-imbues the katar in the same action. **Gap-closer + reload + punch** — this is the strike that solves the momentum problem. When charges run out, Rushing Strike re-imbues and strikes simultaneously. No dead turns. No lost momentum.
**Narrative:** The enemy steps back. The Alchemist doesn't let them. One step — hands clap mid-stride, katar transmutes. Two steps — the new blade gleams. Three — the katar is in the enemy's chest. The rush isn't just a gap-closer. It's a *reload*. The Alchemist transmutes mid-motion, loading a new imbue while closing the distance, and delivers the punch all in one fluid action. The enemy thought distance was safety. The enemy thought a spent katar meant a free turn. The Alchemist disagrees on both counts.

**Strike Rule: Gap-Close + Reload** — Rushing Strike re-imbues the katar with a chosen imbue AND strikes in the same turn. This is the Alchemist's answer to the momentum problem — charges run out, but the flow never dies. The player selects which imbue to load when using Rushing Strike.

---

### 12. Swift Transmutation
```python
{"id": "swift_transmutation", "name": "Swift Transmutation", "type": "cast",
 "power_type": "buff", "trigger": "always",
 "self_status": "evasive",
 "stat_mod": {"self": {"grace": 4, "might": 1}}, "mod_duration": 3,
 "cooldown": 4}
```
**Description:** The Alchemist claps their hands to their own legs. The muscles transmute — lighter, faster, spring-loaded. The Alchemist blurs across the battlefield.
**Narrative:** The Alchemist presses their palms to their thighs. The transmutation is quick — bones hollow, muscles tighten, tendons snap taut. The world slows — not because time changed, but because the body got faster. The enemy swings. The Alchemist is already behind them. The enemy turns. The Alchemist is already punching.

---

### 13. Stone Wall
```python
{"id": "stone_wall", "name": "Stone Wall", "type": "cast",
 "power_type": "defend", "trigger": "always",
 "self_status": "warded",
 "stat_mod": {"self": {"grace": 2}}, "mod_duration": 2,
 "cooldown": 4}
```
**Description:** The Alchemist claps their hands to the ground. Stone erupts between them and the enemy — a wall of transmuted rock. The Alchemist is hidden, warded, and breathing.
**Narrative:** The Alchemist drops to one knee and slams both palms into the dirt. The ground answers. Stone surges up — not gradually, but instantly — a wall of rock between the Alchemist and the enemy. The enemy's next swing hits stone. The Alchemist is behind it, catching their breath, planning the next imbue. The wall won't last. The Alchemist doesn't need it to.

---

## Expert Tier (Level 8, 400g, 1hr) — 4 Imbuable, 3 Strike

### 14. Corrosive Mist
```python
{"id": "corrosive_mist", "name": "Corrosive Mist", "type": "imbuable", "trigger": "opponent_status",
 "imbue_charges": 3,
 "imbue_status": "burning",
 "imbue_stat_mod": {"enemy": {"armor_bonus": -4, "might": -2}},
 "imbue_mod_duration": 3,
 "imbue_mini_rule": "feeds_on_existing_statuses",
 "blade_shape": "eroding",
 "cooldown": 5}
```
**Description:** The Alchemist transmutes the katar into an eroding blade — pitted, smoking, metal visibly degrading and reforming. Every punch releases corrosive vapor, and **each status effect on the enemy adds +50% armor reduction**. The amplifier imbue. Use after applying other statuses.
**Narrative:** The enemy is already burning. Already poisoned. Already suffering. Good. The Alchemist claps, and the katar changes — the blade doesn't just coat, it *erodes*. Pits form, smoke rises, the metal degrades and reforms in real time. The first punch lands and the mist seeps into the existing burns, the existing poison, the existing pain. Two statuses on the enemy? +100% armor reduction. Three? +150%. The more the enemy suffers, the more the corrosion eats. It doesn't create new suffering — it amplifies the old. Only triggers when the enemy has a status effect. 3 charges. Eroding blade.

**Mini-Rule: Feeds on Existing Statuses** — Each status effect currently on the enemy adds +50% to the base armor reduction (-4). 1 status: -6 armor. 2 statuses: -8. 3 statuses: -10. The Alchemist's combo imbue — pair with Poison + Frost for devastating armor melt.

---

### 15. Living Slime
```python
{"id": "living_slime", "name": "Living Slime", "type": "imbuable", "trigger": "always",
 "imbue_charges": 2,
 "imbue_status": "ensnared",
 "imbue_stat_mod": {"enemy": {"grace": -3, "might": -3, "armor_bonus": -2}},
 "imbue_mod_duration": 3,
 "imbue_mini_rule": "immobilize_on_3rd_hit",
 "blade_shape": "whip",
 "cooldown": 5}
```
**Description:** The Alchemist transmutes the katar into a whip — extending, retracting, translucent green strands. Every punch leaves living slime that crawls over the enemy, and the **3rd hit immobilizes** them completely — can't move, can't reposition, can still attack. The lockdown imbue. Use against mobile enemies.
**Narrative:** The Alchemist claps. The katar doesn't gleam — it *extends*. The blade becomes a whip, translucent green strands reaching and retracting like a living thing. Because it is a living thing. The first punch lands and the slime transfers — crawling up the enemy's arm, wrapping around their joints. The second punch, and the slime reaches their legs. The third hit — the slime *locks*. The enemy can't move. They can swing, they can attack, but they can't run, can't reposition, can't escape. The Alchemist has all the time in the world now. 2 charges. Whip blade.

**Mini-Rule: Immobilize on 3rd Hit** — Every 3rd hit (across all strikes while this imbue is active) immobilizes the enemy — they can't move or reposition for 2 turns (can still attack). Different from Frost's freeze (which skips the turn entirely). Slime locks movement, not action.

---

### 16. Transmutation Touch
```python
{"id": "transmutation_touch", "name": "Transmutation Touch", "type": "imbuable", "trigger": "opponent_wounded",
 "imbue_charges": 2,
 "imbue_status": "shaken",
 "imbue_stat_mod": {"enemy": {"armor_bonus": -5, "might": -3, "essence": -2}},
 "imbue_mod_duration": 3,
 "imbue_mini_rule": "armor_to_paper_on_2nd_hit",
 "blade_shape": "dull_edge",
 "cooldown": 5}
```
**Description:** The Alchemist transmutes the katar into a dull edge — flat grey, no reflection, reeks of ozone. The blade doesn't cut anymore. It *unmakes*. Every punch transmutes the enemy's armor, and the **2nd hit turns armor to paper** — enemy `armor_bonus` drops to 0. The armor-killer imbue. Use against heavily armored enemies.
**Narrative:** The enemy is bleeding. Good. The Alchemist claps, and the katar changes — not visibly, but essentially. The blade becomes dull. Flat. Grey. It doesn't reflect light. It doesn't cut. It *unmakes*. The first punch lands on the enemy's chestplate and the iron softens — not melts, softens. Steel becomes clay. The second punch — the armor stops being armor entirely. It becomes paper. `armor_bonus` drops to 0. The enemy's protection is gone, not because it broke, but because it stopped being what it was. Only triggers when the enemy is wounded. 2 charges. Dull edge blade.

**Mini-Rule: Armor to Paper on 2nd Hit** — On the 2nd hit (across all strikes while this imbue is active), the enemy's `armor_bonus` is set to 0 for 3 turns. Not a reduction — a complete nullification. The transmutation is absolute. Pair with Flurry to trigger in one turn.

---

### 17. Explosive Chain
```python
{"id": "explosive_chain", "name": "Explosive Chain", "type": "imbuable", "trigger": "always",
 "imbue_charges": 2,
 "imbue_status": "burning",
 "imbue_stat_mod": {"enemy": {"armor_bonus": -3, "grace": -2}},
 "imbue_mod_duration": 2,
 "imbue_mini_rule": "double_hit_detonation",
 "blade_shape": "jagged",
 "cooldown": 5}
```
**Description:** The Alchemist transmutes the katar into a jagged, crackling blade — sparking, unstable, barely contained. Every punch detonates on impact — **each strike hits 2x**: once from the katar, once from the blast. The raw damage imbue. Use when you need burst.
**Narrative:** The Alchemist claps. The katar vibrates — unstable, reactive, barely contained. The blade crackles with alchemical potential, sparks flying off the jagged edge. The first punch lands and the impact triggers a detonation — the enemy takes the katar AND the blast. Two hits, one punch. The second punch is the same — blade, then boom. The enemy doesn't know which hurt more. The Alchemist doesn't care. 2 charges. Jagged blade. Every strike hits twice.

**Mini-Rule: Double Hit Detonation** — Every strike while this imbue is active hits 2x. The second hit is an explosion dealing 50% of the first hit's damage. Both hits apply the imbue's status and stat_mod. Pair with Flurry for 6 total hits in one turn.

---

### 18. Spinning Strike
```python
{"id": "spinning_strike", "name": "Spinning Strike", "type": "strike",
 "damage_type": "physical", "trigger": "always",
 "hits": 1,
 "cf_gain": 1,
 "strike_rule": "reposition",
 "cooldown": 3}
```
**Description:** The Alchemist spins with the katar extended, striking the primary target and any adjacent enemy, then **repositions to the opposite side**. The imbue spreads to all targets hit, and the Alchemist ends up behind the enemy. The repositioning strike.
**Narrative:** The Alchemist plants their foot and spins — katar out, arm straight, full rotation. The blade catches the primary enemy in the ribs, then continues through to whoever's standing too close. The imbue rides both hits — acid on two targets, poison in two bloodstreams, frost on two bodies. And when the spin ends, the Alchemist is behind the enemy. The enemy turns. The Alchemist is already punching from the new angle. The Alchemist was surrounded. They aren't anymore.

**Strike Rule: Reposition** — After hitting, the Alchemist moves to the opposite side of the primary target. This repositions for the next strike, avoids enemy front-facing abilities, and can break engagement. The tactical movement strike.

---

### 19. Piercing Strike
```python
{"id": "piercing_strike", "name": "Piercing Strike", "type": "strike",
 "damage_type": "physical", "trigger": "always",
 "hits": 1,
 "cf_gain": 1,
 "strike_rule": "ignores_50_percent_armor",
 "cooldown": 2}
```
**Description:** A focused thrust that **ignores 50% of the enemy's armor**. The katar goes deep — delivering the imbue straight to the tissue beneath the steel. The deep-delivery strike for high-armor enemies.
**Narrative:** The enemy has armor. Good armor. The Alchemist doesn't care. They shift their grip — katar forward, blade flat, point-first. The thrust is surgical. The katar finds the gap between plates and slides through, bypassing steel, bypassing leather, reaching flesh. The imbue doesn't have to fight through armor — it's already inside. Acid burns from within. Poison starts at the heart. The enemy didn't feel the entry. They feel the effect.

**Strike Rule: Ignores 50% Armor** — Bypasses 50% of the enemy's current `armor_bonus` for this strike. The imbue is delivered directly to flesh, not filtered through steel. The anti-armor strike — pair with Acid Bomb or Transmutation Touch for maximum armor destruction.

---

### 20. Counter Strike
```python
{"id": "counter_strike", "name": "Counter Strike", "type": "strike",
 "damage_type": "physical", "trigger": "always",
 "hits": 1,
 "cf_gain": 1,
 "strike_rule": "interrupt",
 "cooldown": 2}
```
**Description:** A reactive strike that **interrupts enemy casting**. If the enemy is preparing a skill, Counter Strike cancels it. The imbue lands on the counter, punishing aggression with denial.
**Narrative:** The enemy swings. The Alchemist doesn't dodge — they step *in*. The katar comes up as the enemy's blade comes down, and the punch lands before the swing finishes. But if the enemy is casting — gathering energy, preparing a skill, charging an attack — the Counter Strike does more. It *interrupts*. The enemy's preparation shatters. The skill is lost. The cooldown still ticks. The enemy wasted their turn AND took a katar to the ribs. The imbue rides the counter — acid in the wound, poison in the blood, frost in the muscle. The enemy was attacking. Now they're bleeding AND silenced.

**Strike Rule: Interrupt** — If used when the enemy is preparing/casting a skill, Counter Strike cancels the enemy's action. The enemy's skill goes on cooldown without firing. The Alchemist punishes aggression with denial — the ultimate anti-caster strike.

---

## Master Tier (Level 15, 1000g, 1hr) — 1 Imbuable, 3 Strike, 4 Cast

### 21. Forbidden Formula
```python
{"id": "forbidden_formula", "name": "Forbidden Formula", "type": "imbuable", "trigger": "low_hp",
 "imbue_charges": 1,
 "imbue_status": "burning",
 "imbue_stat_mod": {"enemy": {"armor_bonus": -5, "grace": -4, "might": -3}},
 "imbue_mod_duration": 3,
 "imbue_mini_rule": "all_statuses_true_damage",
 "blade_shape": "shifting",
 "cooldown": 6}
```
**Description:** The Alchemist transmutes the katar with a forbidden formula — banned, unstable, and devastating. The blade can't settle on a shape — it flickers between liquid, claw, needle, ice spike, all of them. One charge. One punch. **True damage. All statuses at once.** The katar cracks after the strike.
**Narrative:** The Alchemist is cornered. Bleeding. Dying. They clap — not the quick clap of routine transmutation, but the slow, deliberate press of palms that means something terrible is coming. The katar changes. Not color. Not temperature. *Nature*. The blade can't hold a form — it flickers between liquid acid, lightning claw, poison needle, ice spike, eroding metal, all of them, cycling through every transmutation the Alchemist has ever learned. One charge. One punch. The Alchemist steps in and delivers everything. The enemy takes it all — fire, acid, poison, lightning, frost, corrosion, slime, transmutation, explosion — every alchemical reaction at once, channeled through a single point of contact. True damage. No armor. No resistance. No survival. The katar cracks after the strike. The formula is too much for the blade. It was worth it. Triggers when HP is low. 1 charge. Shifting blade.

**Mini-Rule: All Statuses + True Damage** — The single hit applies ALL imbue statuses simultaneously (burning, poisoned, ensnared, stunned, blinded, shaken, bleeding) and deals true damage (ignores all armor and resistance). The katar cracks after — cannot be imbued next turn. The nuke. One shot, one kill.

---

### 22. Guard Break
```python
{"id": "guard_break", "name": "Guard Break", "type": "strike",
 "damage_type": "physical", "trigger": "always",
 "hits": 1,
 "cf_gain": 1,
 "strike_rule": "stance_break",
 "cooldown": 3}
```
**Description:** A brutal katar strike that **breaks the enemy's stance** — removes `warded` status and prevents the enemy from gaining `warded` for 2 turns. The imbue follows through the broken defense.
**Narrative:** The enemy is braced. Shield up, stance solid, chin tucked. The Alchemist doesn't aim around the guard — they aim through it. The katar comes down at the joint between shield and arm, the weak point in every stance. The impact is ugly — metal on metal, bone on bone — and the guard crumbles. The enemy's `warded` status shatters. They can't re-ward. They can't brace again. And the imbue is already in the wound, taking advantage of the opening. The enemy was defending. Now they're bleeding and exposed.

**Strike Rule: Stance Break** — Removes `warded` from the enemy and prevents them from gaining `warded` for 2 turns. The anti-defense strike — use against enemies who turtle behind shields or wards. The imbue lands through the broken guard, unimpeded.

---

### 23. Rising Strike
```python
{"id": "rising_strike", "name": "Rising Strike", "type": "strike",
 "damage_type": "physical", "trigger": "always",
 "hits": 1,
 "cf_gain": 1,
 "strike_rule": "launch",
 "cooldown": 3}
```
**Description:** An upward katar slash that **launches the enemy airborne** — they can't act next turn. The imbue is applied mid-flight — the enemy takes the element while they're helpless in the air.
**Narrative:** The Alchemist drops low — below the enemy's guard, below their sightline — and drives the katar upward. The blade catches the enemy under the ribs and lifts. Feet leave the ground. The enemy is airborne, helpless, and the imbue is already working — acid eating through their chest cavity, poison flooding their bloodstream, frost crystallizing their lungs. They hang in the air for a moment, suspended, and then they fall. They land wrong. They always land wrong. And they can't act next turn — they're too busy recovering from the launch. The Alchemist is already standing over them, loading the next imbue.

**Strike Rule: Launch** — Enemy is launched airborne and **cannot act on their next turn**. They're recovering from the launch, not frozen — just helpless. The imbue is applied mid-flight for maximum effect. The setup strike for a free turn of pressure.

---

### 24. Executioner Strike
```python
{"id": "executioner_strike", "name": "Executioner Strike", "type": "strike",
 "damage_type": "physical", "trigger": "always",
 "hits": 1,
 "cf_gain": 0,
 "strike_rule": "cf_consumer",
 "cooldown": 4}
```
**Description:** The finishing strike. **Consumes ALL current CF** — +10% damage per CF spent. Below 30% HP: +50% base damage on top. The imbue rides the execute. The perfect closer for a long combo chain — everything you've built, cashed in at once.
**Narrative:** The enemy is stumbling. Broken. Barely standing. The Alchemist sees it — the wobble in their knees, the sag in their shoulders, the way their weapon droops. The Alchemist steps in. One punch. Clean. Final. But this punch is different — every experiment, every observation, every adjustment the Alchemist has made during this fight goes into it. All the CF. All the data. The katar finds the neck, the heart, the spine — whatever ends it fastest. 10 CF? +100% damage. 20 CF? +200%. Below 30% HP? Add another +50%. The enemy drops. The combo is over. The CF is spent. The Alchemist shakes the blood off the katar and starts a new experiment.

**Strike Rule: CF Consumer** — Consumes ALL current CF for +10% damage per CF spent. CF gain = 0 (you're spending, not building). Below 30% HP: +50% base damage on top. The closer — use when you've built CF and the enemy is low. The decision strike: do you cash in now, or keep building for a bigger execute?

---

### 25. Mutagen Injection
```python
{"id": "mutagen_injection", "name": "Mutagen Injection", "type": "cast",
 "power_type": "buff", "trigger": "always",
 "self_status": "inspired",
 "stat_mod": {"self": {"might": 4, "grace": 3, "durability": 2}}, "mod_duration": 3,
 "cooldown": 5}
```
**Description:** The Alchemist transmutes their own body — bones shift, muscles swell, joints realign. Not a drink. An injection. The Alchemist becomes something more than human for three turns.
**Narrative:** The Alchemist doesn't drink. They inject — the needle goes into the neck, the plunger goes down, and the mutagen goes to work. Bones shift audibly. Muscles swell visibly. The spine extends, the jaw widens, the eyes sharpen. It's not painful — it's transformative. When it's done, the Alchemist is different: taller, denser, faster. The enemy sees the change and hesitates. The Alchemist doesn't. The mutagen lasts three turns. The mutation is worth it.

---

### 26. Phoenix Mixture
```python
{"id": "phoenix_mixture", "name": "Phoenix Mixture", "type": "cast",
 "power_type": "defend", "trigger": "low_hp",
 "self_status": "warded",
 "heal_percent": 0.15,
 "stat_mod": {"self": {"armor_bonus": 4, "essence": 3, "durability": 2}}, "mod_duration": 3,
 "cooldown": 6}
```
**Description:** The Alchemist transmutes their own blood — fire replaces plasma, warmth replaces cold. The body refuses to die. Wounds close, armor hardens, and the Alchemist rises.
**Narrative:** The Alchemist is dying. They press their palms together — not over the katar, but over their own heart. The transmutation is internal. The blood changes — not color, but temperature. It burns. Not painfully — *alive*. The fire doesn't consume; it rebuilds. The wounds close. The pain fades. The fire wraps around the body like a cocoon, and when it fades, the Alchemist is standing. The enemy thought they won. The Phoenix disagrees. Triggers when HP is low.

---

### 27. Smoke Transmutation
```python
{"id": "smoke_transmutation", "name": "Smoke Transmutation", "type": "cast",
 "power_type": "defend", "trigger": "always",
 "self_status": "hidden",
 "stat_mod": {"self": {"grace": 2}}, "mod_duration": 2,
 "cooldown": 4}
```
**Description:** The Alchemist transmutes the air around them into thick chemical smoke. They vanish — hidden, untargetable. A breather between combo chains.
**Narrative:** The Alchemist claps their hands together and pulls them apart. The air between their palms changes — not to fire, not to stone, but to smoke. Thick, gray, chemical. It billows outward and the Alchemist is gone. The enemy swings at shapes. The shapes aren't there. The Alchemist is three steps away, catching their breath, planning the next imbue. The smoke clears in two turns. The Alchemist will be ready before then.

---

### 28. Spike Field
```python
{"id": "spike_field", "name": "Spike Field", "type": "cast",
 "power_type": "debuff", "trigger": "always",
 "status_apply": "bleeding",
 "stat_mod": {"enemy": {"grace": -3, "might": -2}}, "mod_duration": 3,
 "cooldown": 5}
```
**Description:** The Alchemist claps their hands to the ground and transmutes the terrain into a field of jagged stone spikes. The enemy takes bleeding damage and loses grace — the ground itself fights for the Alchemist.
**Narrative:** The Alchemist drops to one knee and slams both palms into the earth. The transmutation is violent — the ground erupts. Stone spikes burst upward in a radius around the enemy, piercing boots, catching legs, tearing armor. The enemy can't move without impaling themselves further. Every step is a wound. Every shift is a cut. The Alchemist stands up and watches the enemy bleed on their new terrain. The battlefield isn't neutral anymore.

---

## Legendary Tier (Level 20, 2500g, 1 day — Quest-gated) — 1 Cast, 1 Strike

### 29. Philosopher's Transmutation
```python
{"id": "philosophers_transmutation", "name": "Philosopher's Transmutation", "type": "cast",
 "power_type": "heal", "trigger": "low_hp",
 "self_status": "inspired",
 "heal_percent": 0.30,
 "stat_mod": {"self": {"might": 3, "grace": 3, "essence": 3, "durability": 3, "insight": 3, "cognition": 3}}, "mod_duration": 4,
 "legendary_rule": "infinite_charges_max_mini_rules",
 "cooldown": 7}
```
**Description:** The Alchemist transmutes their own body into its perfect form — the Philosopher's ideal. Every wound closes. Every stat surges. And for 4 turns, the Alchemist **transcends alchemy itself**: every imbue has **infinite charges** (never fades), and every imbue's mini-rule triggers at **maximum effect** (Frost freezes on 1st hit, Lightning chains on every hit, Poison gains +100% per turn, Acid shreds -5 per hit, etc.). The Alchemist doesn't need to re-imbue. The katar holds everything.
**Narrative:** The Alchemist is dying. They don't reach for a vial. They reach for themselves. Both palms press against their own chest — not the quick clap of combat transmutation, but the deep, deliberate press of something final. The transmutation starts at the heart and moves outward. The blood changes — not color, but quality. It becomes richer, denser, alive in a way blood shouldn't be. The bones harden. The muscles tighten. The nerves fire faster. The wounds close — not gradually, but all at once, as if the body remembers what it was before the fight and decides to be that again. But that's not the legend. The legend is the katar. The blade starts to glow — not one color, but all of them, shifting, cycling, settling into something new: a form that doesn't need to be reloaded. The imbue doesn't fade. The charges don't deplete. The mini-rules fire at maximum. Frost freezes on the first hit. Lightning chains on every hit. Poison doubles every turn. The Alchemist has become the Philosopher's Stone — and the katar is the proof. Triggers when HP is low.

**Legendary Rule: Infinite Charges + Max Mini-Rules** — For 4 turns after casting: the active imbue never runs out of charges (no re-imbuing needed), and all mini-rules trigger at maximum effect:
- Acid: -5 armor per hit (instead of -1 stacking)
- Flash: -5 grace per hit (instead of -1 stacking)
- Frost: Freezes on 1st hit (instead of 4th)
- Lightning: Chains on every hit (instead of 3rd)
- Poison: +100% damage per turn (instead of +10%)
- Corrosive: +200% armor reduction per status (instead of +50%)
- Slime: Immobilizes on 1st hit (instead of 3rd)
- Transmutation Touch: Armor to paper on 1st hit (instead of 2nd)
- Explosive: 3x hits per strike (instead of 2x)
- The Alchemist has transcended the formula. They ARE the formula.

**Quest: The Philosopher's Stone**
- **Trainer:** Thazka Emberhand (Warforge)
- **Min Level:** 20
- **Objectives:**
  - Kill 5 Iron Scar creatures in Mushkara
  - Gather 3 Relic Shards
  - Learn at least 5 Alchemist skills from Thazka Emberhand
- **Reward:** Unlocks Philosopher's Transmutation

---

### 30. Legend of Alchemy
```python
{"id": "legend_of_alchemy", "name": "Legend of Alchemy", "type": "strike",
 "damage_type": "true", "trigger": "low_hp",
 "hits": 8,
 "cf_gain": 0,
 "self_status": "inspired",
 "heal_percent": 0.25,
 "status_apply": "stunned",
 "stat_mod": {"enemy": {"might": -6, "grace": -6, "armor_bonus": -8, "cognition": -5, "essence": -4, "insight": -4, "durability": -4}},
 "mod_duration": 5,
 "legendary_rule": "auto_adapt_katar",
 "cooldown": 10}
```
**Description:** The ultimate strike. The Alchemist doesn't choose the imbue — **the katar chooses for them**. Every punch automatically re-transmutes the blade into the element the enemy is weakest against. 8 hits, true damage, each one the **optimal response** to the enemy's current state. The Alchemist has transcended choosing. They simply understand.
**Narrative:** The Alchemist is dying. The katar is cracked. The imbues are spent. And then — they clap. Not once. Not twice. They keep clapping, but something is different. The blade doesn't settle on one form. It *adapts*. The first punch — the enemy has high armor, so the katar becomes liquid acid. The armor dissolves. The second punch — the enemy is trying to cast, so the katar becomes a lightning claw. The cast is interrupted. The third punch — the enemy is moving to escape, so the katar becomes an ice spike. They freeze. The fourth — the enemy is bleeding, so the katar becomes a dull edge. Their armor turns to paper. The fifth — the enemy is surrounded by allies, so the katar becomes a claw and chains. The sixth — the enemy is weakened, so the katar becomes a needle and the poison scales. The seventh — the enemy is stunned, so the katar becomes jagged and detonates for maximum damage. The eighth — the enemy is dying, so the katar becomes shifting, and the Forbidden Formula ends it. True damage. Every hit. The Alchemist didn't choose a single imbue. The katar read the enemy and responded. The Alchemist has transcended alchemy. They don't transmute anymore — they *understand*. And understanding is faster than choosing. The katar shatters after the last punch. The enemy is on the ground. The Alchemist is standing, healed, inspired, holding a broken blade and a legend. Triggers when HP is low.

**Legendary Rule: Auto-Adapt Katar** — Each of the 8 hits automatically selects the optimal imbue based on the enemy's current state:
- Enemy has high armor → Acid (liquid blade, armor shred)
- Enemy is casting → Lightning (claw, stun + interrupt)
- Enemy is mobile → Frost (ice spike, freeze)
- Enemy is wounded → Transmutation Touch (dull edge, armor to paper)
- Enemy has allies nearby → Lightning (claw, chain)
- Enemy is status-afflicted → Corrosive Mist (eroding, amplified)
- Enemy is low HP → Poison (needle, scaling damage) or Explosive (jagged, burst)
- Final hit → Forbidden Formula (shifting, true damage, all statuses)
- The Alchemist doesn't choose. The katar knows. 8 hits, true damage, each one the perfect response. CF gain = 0 (this IS the culmination).

**Quest: The Philosopher's Stone**
- **Trainer:** Thazka Emberhand (Warforge)
- **Min Level:** 20
- **Objectives:**
  - Complete "The Philosopher's Stone" quest (learn Philosopher's Transmutation first)
  - Kill 1 Heritage Boss
  - Gather 1 Jahra Ingot
  - Learn at least 15 Alchemist skills total
- **Reward:** Unlocks Legend of Alchemy
