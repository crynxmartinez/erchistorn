# Priest Mastery — 30 Skills + 11 Passives

**Role:** The Holy Judge — a divine specialist who blinds, binds, and burns the wicked. The weaker the enemy becomes, the stronger the Priest grows. Against undead and devils, the Priest is the worst nightmare in the game.
**Masteries per trainer:** 3 (Priest + 2 others)
**Trainers teaching Priest:** Solunara, Elaris, Starfall Watch

---

## Priest Identity

**Priest Battle Flow:**

> Protect → Stabilize → Endure → Sanctity Awakens → Judgment → Victory

Damage isn't mentioned. Because damage isn't the Priest's objective. **Keeping everyone alive is.**

- **Holy specialist** — deals +50% damage to undead and devils with holy strikes
- **Sanctity scaling** — all skills grow stronger as enemy HP drops
- **Miracle system** — chance to double-cast any skill, scaling with the **target's** missing HP. At 1% target HP, ~99% chance to Miracle. Works on enemies, allies, and self
- **Shield Wall** — holy barriers with their own HP pool that absorb damage before it reaches the Priest
- **Crowd control king** — blinds and binds enemies, locking them down
- **No physical damage** — all strikes are holy/magical, no steel
- **Self-buff focused** — all stat buffs target self, boosting `essence`, `insight`, `grace`, and `durability` only. The Priest keeps the target alive, not makes them more powerful
- **5 diverse heals** — fast heal, HoT buff, normal heal, delayed heal, and group heal — each with a unique mechanic. Heals can target allies, stat buffs cannot
- **Inevitable** — weak at full enemy HP, inevitable as the enemy crumbles. The Priest isn't raging. The Priest simply knows the enemy's defeat is now unavoidable

### Golden Rule of the Priest

> A Priest should never ask: "How do I deal more damage?"
>
> A Priest should ask: "Who dies if I make the wrong choice?"

### The Priest's Slogan

> *The Priest does not command miracles. The Priest is simply there when they happen.*

### The Sanctity System

Every Priest skill has a **Sanctity bonus** — the effect scales based on the **enemy's current HP**:

| Enemy HP | Sanctity Bonus |
|-----------|---------------|
| 100–75% | Normal effect |
| 75–50% | +25% effect |
| 50–25% | +50% effect |
| Below 25% | +100% (doubled) |

**How Sanctity applies:**
- **Heals** — enemy dying? Your heals are stronger. The divine rewards the faithful who are winning
- **Strikes** — execution mechanic. The weaker the enemy, the harder holy power hits
- **Buffs** — as the enemy crumbles, the Priest's faith surges
- **Debuffs** — the broken enemy is easier to break further

**Example:**
- Enemy at 100% HP: Divine Light heals 20%. Normal.
- Enemy at 50% HP: Divine Light heals 25%. Sanctity +25%.
- Enemy at 25% HP: Divine Light heals 30%. Sanctity +50%.
- Enemy at 10% HP: Divine Light heals 40%. Sanctity +100%.
- If Miracle triggers (ally at 10% HP, ~90% chance): Divine Light heals 40% twice = 80% total.

### Miracle System

Miracles never happen when everything is safe. The closer someone is to death, the more likely the heavens intervene. **The divine answers desperation, not comfort.**

Every Priest skill has a **Miracle chance** — the skill **activates twice** (double cast) when Miracle triggers. The chance is **equal to the target's missing HP percentage**. The "target" is whoever the skill is being used on — enemy, ally, or self:

| Target HP | Miracle Chance |
|-----------|----------------|
| 100% HP | 0% chance |
| 75% HP | 25% chance |
| 50% HP | 50% chance |
| 25% HP | 75% chance |
| 10% HP | 90% chance |
| 1% HP | 99% chance |

**How it works:**
- Miracle chance = (100% - target current HP%)
- Striking an enemy at 30% HP → 70% Miracle chance
- Healing an ally at 30% HP → 70% Miracle chance
- Buffing self at 50% HP → 50% Miracle chance
- At full target HP: 0% chance — no miracles when nobody needs one
- At 1% target HP: 99% chance — the divine answers the desperate
- Both casts benefit from Sanctity scaling
- Works on all skill types — double heal, double strike, double buff, double debuff, double shield wall
- Passives boost the Miracle chance further (Deep Faith: +15%, Avatar of Faith: +30% on allies, Hand of God: guaranteed below 25%)

**MIRACLE SAVED:** When a Priest heals someone from below 10% HP to above 50% HP in a single cast, the game displays **"MIRACLE SAVED"** instead of "Critical Heal." Not a mechanic — pure feedback. Players will remember it forever.

### Shield Wall

A Shield Wall is not a heal. Healing repairs damage already taken. Shield Walls **prevent damage from ever happening.** A skilled Priest knows when to heal, and when to ensure the wound never exists.

Shield Wall skills create a **temporary HP bar** on top of the Priest's normal HP. All incoming damage hits the Shield Wall first. When Shield Wall HP reaches 0, it breaks and excess damage carries through to the Priest's HP.

**Shield Walls do NOT stack.** If a new Shield Wall is cast while one is already active, the old shield **breaks immediately and is replaced** by the new one. Only one Shield Wall can be active at a time.

**Shield Wall HP scales with Sanctity** — the lower the enemy's HP, the stronger the shield:

| Enemy HP | Shield Wall HP Bonus |
|-----------|---------------------|
| 100–75% | Base shield |
| 75–50% | +25% shield HP |
| 50–25% | +50% shield HP |
| Below 25% | +100% shield HP (doubled) |

**Example:**
- Priest at full enemy HP: Light Barrier = 20% max HP absorb
- Enemy at 20% HP: Light Barrier = 40% max HP absorb — nearly impossible to break through

### Holy Damage

Priest strikes use `damage_type: "holy"` — a damage subtype that functions as magical damage against normal enemies but deals **+50% damage to undead and devils**.

### New Status Effects

| Status | Effect | Theme |
|--------|--------|-------|
| `blind` | Enemy attacks **miss** for the duration. Enemy can still act but cannot hit. | Holy light sears the eyes of the wicked |
| `bind` | Enemy **cannot act** — no attacks, no skills. Enemy **evasion reduced to 0** (chained, can't dodge). | Holy chains restrain the unholy |

**How they differ from existing statuses:**
- `stunned` — can't act (impact-based, physical)
- `bind` — can't act + can't dodge (holy chains, more powerful than stun but rarer)
- `blind` — can act but can't hit (control without full lockdown, more common)

### Stat Focus

| Stat | Priority | Why |
|------|----------|-----|
| `essence` | **Primary** | Magic resistance + healing power — the Priest's core stat |
| `insight` | **Primary** | Magical damage scaling — holy strikes scale with insight |
| `cognition` | **Secondary** | Utility, skill diversity |
| `grace` | **Secondary** | Accuracy — holy strikes need to land |
| `durability` | **Secondary** | HP/resilience — the Priest must survive to reach Sanctity ramp |
| `might` | **None** | No physical damage |
| `armor_bonus` | **Minimal** | Divine protection, not steel |

### Status Identity

| Status | Role |
|--------|------|
| `blind` | **Signature** — holy light blinds the wicked, unique to Priest |
| `bind` | **Signature** — holy chains restrain, unique to Priest, stronger than stun |
| `warded` | **Primary** — divine protection on buffs/defends |
| `inspired` | **Primary** — divine favor on buffs |
| `burning` | **Secondary** — holy fire on undead/devils |
| `shaken` | **Secondary** — divine judgment breaks confidence |
| `stunned` | **Rare** — only on legendary skills |

### Trigger Identity

| Trigger | Role |
|---------|------|
| `always` | **Primary** — the Priest is always ready to judge |
| `low_hp` | **Secondary** — desperate prayers for self-preservation |
| `opponent_wounded` | **Secondary** — Sanctity rewards wounded enemies |
| `self_debuff` | **Secondary** — cleansing is a core Priest response |
| `opponent_status` | **Rare** — exploiting an already-afflicted enemy |

### What the Priest Does NOT Do

- **No physical damage** (that's Knight/Lancer/Rogue)
- **No multi-hit** (that's Assassin/Lancer)
- **No evasion/stealth** (that's Assassin/Rogue/Hunter)
- **No poison/DoT** (that's Assassin/Alchemist/Hunter)
- **No ally stat buffs** (that's Bard/Paladin — Priest buffs *themselves*. Heals can target allies, stat buffs cannot)
- **No mobility** (that's Lancer/Rogue)

---

## Passives — 10 Auto-Learned + 1 Legendary Quest Passive

| # | Name | Level | Effect |
|---|------|-------|--------|
| 1 | Sanctified | 10 | Sanctity bonus starts at 90% enemy HP instead of 75% |
| 2 | Holy Fire | 20 | Holy strikes deal +75% to undead/devils (was +50%) |
| 3 | Divine Fortitude | 30 | +10 permanent `essence` (innate, always active) |
| 4 | Smite | 40 | When enemy drops below 50% HP, gain `insight +10` for 3 turns |
| 5 | Exorcist | 50 | Holy strikes apply `burning` to undead/devils |
| 6 | Deep Faith | 60 | Sanctity bonuses increased: +35% / +75% / +150%. **Miracle chance +15%** |
| 7 | Judgment | 70 | At 50% enemy HP or lower, all strikes deal +20% damage |
| 8 | Divine Wrath | 80 | At 25% enemy HP or lower, all cooldowns reduced by 1 turn |
| 9 | Redemption | 90 | At full enemy HP, skills still get +10% effect (no weak start). **Shield Wall gains +50% HP** |
| 10 | Avatar of Faith | 100 | Sanctity bonuses doubled. Holy damage doubled (+100% to undead/devils). **When healing allies, Miracle chance is doubled. Heals on allies also apply a Shield Wall (10% max HP) on the target.** `bind` and `blind` durations +1 turn. Shield Wall Sanctity scaling doubled. Enemy cannot heal below current HP |
| 11 | Hand of God | 100 (Quest) | **Legendary passive.** Miracle is **guaranteed (100%)** when target is below 25% HP. All heals **cleanse debuffs** on the target before healing. Shield Walls **heal the Priest for 50% of damage absorbed**. When Miracle triggers on a **strike**, also applies `blind`. When Miracle triggers on a **heal**, also applies `inspired` (+grace for 3 turns). Sanctity bonuses **tripled** |

### Passive Synergy

```
Level 10:  Sanctity kicks in earlier → less time at weak baseline
Level 20:  Holy fire burns evil harder → specialist identity
Level 30:  Permanent essence boost → stronger heals and magic
Level 40:  Enemy at 50% → insight surge, the smiting begins
Level 50:  Holy strikes burn the unholy → anti-evil niche locked
Level 60:  Sanctity amplified + Miracle chance +15% → double casts more often
Level 70:  Enemy at 50% → strikes hit +20% harder → execution mode
Level 80:  Enemy at 25% → cooldowns shrink → the verdict accelerates
Level 90:  No weak full-HP phase + Shield Wall +50% HP → always relevant, always protected
Level 100: SANCTITY DOUBLED, ALLY MIRACLE DOUBLED + SHIELD ON HEAL, SHIELD DOUBLED, HOLY DOUBLED → avatar of the divine
Level 100+ (Quest): HAND OF GOD — MIRACLE GUARANTEED BELOW 25%, CLEANSE ON HEAL, SHIELD ABSORBS → HEAL, SANCTITY TRIPLED → the divine itself
```

**The full build at level 100 (Avatar of Faith):**
- Sanctity: +50% / +100% / +200% based on enemy HP
- Miracle chance: up to 99% on any target, **doubled when healing allies** (ally at 50% HP → 100% Miracle)
- Healing allies applies a 10% max HP Shield Wall on them
- Holy damage: +100% to undead/devils
- Shield Wall: up to 120% max HP absorb at low enemy HP (base 50% × Sanctity 200% × Redemption +50%)
- `blind` and `bind` last +1 turn longer
- Enemy below 50%: +20% strike damage, insight +10
- Enemy below 25%: cooldowns -1, skills doubled
- Enemy cannot heal — the verdict cannot be escaped

**With Hand of God (Legendary Passive):**
- Sanctity **tripled**: +75% / +150% / +300% based on enemy HP
- Miracle **guaranteed** when target below 25% HP — no RNG, the divine answers
- All heals cleanse debuffs before healing
- Shield Walls heal the Priest for 50% of damage absorbed — pain becomes life
- Miracle on strikes also applies `blind` — the light blazes twice
- Miracle on heals also applies `inspired` — the target gains grace for 3 turns
- "The Priest does not command miracles. The Priest is simply there when they happen."

---

## Skill Structure

All skills use the new format — no `power` or `skill_capacity_cost`.

| Field | Description |
|-------|-------------|
| `power_type` | strike, defend, heal, debuff, buff, shield_wall |
| `damage_type` | holy, magical, true (strikes only) — holy deals +50% to undead/devils |
| `trigger` | always, low_hp, opponent_wounded, opponent_status, opening_move, self_debuff |
| `status_apply` | Status inflicted on enemy |
| `self_status` | Status applied to self |
| `stat_mod` | Temporary stat changes — `{"self": {...}, "enemy": {...}}` |
| `mod_duration` | How many turns stat_mod lasts |
| `heal_percent` | Heals X% of max HP (heal skills only) |
| `shield_hp` | Shield Wall HP as % of max HP (shield_wall skills only) |
| `heal_type` | Heal mechanic: `fast` (always first), `hot` (per-turn buff), `normal`, `delayed` (ticks after N turns), `group` (all party members) |
| `target` | `self` (default), `ally` (heals can target allies), `all_allies` (group heal) |
| `hits` | Number of hits per use (default 1) |

**Priest rules:** No `damage_type: "physical"`. No `hits` > 1. No `evasive`/`hidden` self_status. All **stat buffs** target self only — heals can target allies. **Buffs only target `essence`, `insight`, `grace`, and `durability`** — never `might` or `armor_bonus`. The Priest keeps the target alive, not makes them more powerful. Skills should reference Sanctity, holy power, judgment, Miracle, and the enemy's crumbling resolve in descriptions. Shield Wall skills use `shield_hp` instead of `heal_percent`.

---

## Tier Overview

| Tier | Level Req | Gold Cost | Learn Time | Count | Heals | Strikes | Buffs | Debuffs | Defends | Shield Walls |
|------|-----------|-----------|------------|-------|-------|---------|-------|---------|---------|--------------|
| Basic | 1 | 50g | 5 min | 6 | 1 | 1 | 1 | 1 | 1 | 1 |
| Advanced | 3 | 150g | 30 min | 7 | 1 | 1 | 1 | 3 | 1 | 0 |
| Expert | 8 | 400g | 1 hr | 7 | 1 | 1 | 1 | 2 | 1 | 1 |
| Master | 15 | 1000g | 1 hr | 8 | 2 | 1 | 3 | 1 | 0 | 1 |
| Legendary | 20 | 2500g | 1 day | 2 | 0 | 2 | 0 | 0 | 0 | 0 |

---

## Basic Tier (Level 1, 50g, 5min) — 1 Heal, 1 Strike, 1 Buff, 1 Debuff, 1 Shield Wall, 1 Defend

### 1. Swift Prayer
```python
{"id": "swift_prayer", "name": "Swift Prayer", "cooldown": 0,
 "power_type": "heal", "heal_type": "fast", "trigger": "always",
 "target": "ally",
 "heal_percent": 0.02}
```
**Description:** A flash of divine light — small but instant. Heals 2% of target's max HP. **Always acts first**, ignoring turn order. **No cooldown.** The emergency button. Sanctity boosts the heal as the enemy's HP drops. If Miracle triggers, heals twice.
**Narrative:** The Priest doesn't have time to kneel. Doesn't have time to chant. They just reach — one hand, one thought, one word. The light is small, barely a spark. But it's first. It's always first. Before the enemy's blade falls, before the arrow finds its mark, before the wound opens — the spark is there. Small. Fast. Enough. The enemy blinks. The ally breathes. The Priest is already moving to the next prayer.

---

### 2. Light Barrier
```python
{"id": "light_barrier", "name": "Light Barrier", "cooldown": 3,
 "power_type": "shield_wall", "trigger": "always",
 "shield_hp": 0.20}
```
**Description:** A wall of holy light surrounds the Priest with a temporary HP bar that absorbs damage before it reaches the Priest. Shield Wall HP = 20% of max HP, scaled by Sanctity. At low enemy HP, the shield doubles. Shield Walls do not stack — casting a new one replaces the old. If Miracle triggers, the shield is recast at full HP (replaces the old shield).
**Narrative:** The Priest traces a circle in the air. It stays — golden, humming, patient. But this isn't a ward. It's a wall. It has weight. It has substance. The enemy's blade meets it and the wall holds — not deflecting, but absorbing. Each blow chips away at the light. The wall shrinks. But the enemy is getting weaker too, and as they weaken, the wall thickens. The Priest stands behind it, calm, unhurried. The wall is patient. The Priest is patient. The enemy is not.

---

### 3. Bless
```python
{"id": "bless", "name": "Bless", "cooldown": 4,
 "power_type": "buff", "trigger": "always",
 "self_status": "inspired",
 "stat_mod": {"self": {"insight": 2, "grace": 2}}, "mod_duration": 3}
```
**Description:** The Priest blesses themselves with divine favor. Sanctity amplifies the blessing as the enemy crumbles.
**Narrative:** The Priest speaks the old words — not loud, not commanding, but inviting. The light that answers is gentle. It settles on the shoulders like a mantle. The body straightens. The blade steadies. The fear quiets. The blessing doesn't make you stronger. It reminds you that you already are. And the enemy is getting weaker.

---

### 4. Holy Water
```python
{"id": "holy_water", "name": "Holy Water", "cooldown": 3,
 "power_type": "strike", "damage_type": "holy", "trigger": "always",
 "status_apply": "burning",
 "stat_mod": {"enemy": {"might": -2}}, "mod_duration": 2}
```
**Description:** The Priest consecrates water into a sacred weapon. Holy damage burns undead and devils with +50% force. Sanctity amplifies the strike as the enemy's HP drops.
**Narrative:** The Priest pulls a vial — clear water, blessed this morning, still humming with prayer. They throw it. The water doesn't splash; it sears. Where it touches the enemy, the skin smokes and the darkness recoils. Against the undead, it's not just burning — it's unmaking. Holy water doesn't negotiate with evil. It just burns. And the weaker the evil gets, the hotter it burns.

---

### 5. Blinding Light
```python
{"id": "blinding_light", "name": "Blinding Light", "cooldown": 4,
 "power_type": "debuff", "damage_type": "holy", "trigger": "always",
 "status_apply": "blind",
 "stat_mod": {"enemy": {"grace": -2}}, "mod_duration": 2}
```
**Description:** The Priest summons a flash of holy radiance that sears the enemy's vision. The enemy can still act but their attacks miss. Sanctity extends the blindness as the enemy weakens.
**Narrative:** The Priest opens their palm. The light is not gentle. It is not warm. It is the light of judgment — white, absolute, and furious. The enemy's vision whites out. They swing, but they swing at nothing. They shout, but they shout at the light. The Priest watches the blind thing rage and misses every blow. "The wicked cannot see what they fight."

---

### 6. Soul Ward
```python
{"id": "soul_ward", "name": "Soul Ward", "cooldown": 4,
 "power_type": "defend", "trigger": "always",
 "self_status": "warded",
 "stat_mod": {"self": {"essence": 3, "armor_bonus": 2}}, "mod_duration": 3}
```
**Description:** A shimmering seal forms around the Priest, protecting against spiritual attacks. Sanctity deepens the ward as the enemy falters.
**Narrative:** The Priest draws a sigil in the air — complex, precise, ancient. It solidifies into a seal that orbits them slowly. It doesn't stop blades. It stops the things blades can't — curses, hexes, the whispers that crawl in through the soul. The enemy's magic hits the seal and shatters. The Priest doesn't blink. The enemy is running out of weapons. The Priest is not.

---

## Advanced Tier (Level 3, 150g, 30min) — 1 Heal, 1 Strike, 1 Buff, 3 Debuffs, 1 Defend

### 7. Blessing of Renewal
```python
{"id": "blessing_of_renewal", "name": "Blessing of Renewal", "cooldown": 5,
 "power_type": "heal", "heal_type": "hot", "trigger": "always",
 "target": "ally",
 "self_status": "inspired",
 "heal_percent": 0.10,
 "mod_duration": 3}
```
**Description:** A holy buff applied to the target that heals 10% of the **owner's** max HP at the start of each of the owner's turns for 3 turns. The "owner" is whoever the buff is applied to — if cast on an ally, that ally heals each turn. Sanctity boosts each tick as the enemy's HP drops. If Miracle triggers, the buff is applied twice (double duration).
**Narrative:** The Priest doesn't heal the wound. They bless the body. The light settles into the target's skin — not a flash, but a glow. Slow. Steady. Persistent. Each morning the owner wakes, the wound is smaller. Each turn the owner takes, the light pulses and the flesh knits. The Priest moves on. The blessing stays. The owner heals. The enemy bleeds. The renewal doesn't stop until the prayer is finished — and the prayer lasts.

---

### 8. Chain of Light
```python
{"id": "chain_of_light", "name": "Chain of Light", "cooldown": 5,
 "power_type": "debuff", "damage_type": "holy", "trigger": "always",
 "status_apply": "bind",
 "stat_mod": {"enemy": {"might": -3, "grace": -2}}, "mod_duration": 1}
```
**Description:** Chains of pure holy light descend from above, binding the enemy completely. The enemy cannot act or dodge. Sanctity extends the binding as the enemy weakens.
**Narrative:** The Priest looks up. The sky looks back. Chains — not iron, but light, forged in something older than fire — descend. They wrap around the enemy with the patience of a verdict. The enemy cannot move. Cannot attack. Cannot dodge. The chains don't care about struggling. They were made for things that shouldn't be free. The Priest watches the chained thing and begins the next prayer.

---

### 9. Cleansing Flame
```python
{"id": "cleansing_flame", "name": "Cleansing Flame", "cooldown": 4,
 "power_type": "debuff", "damage_type": "holy", "trigger": "opponent_status",
 "status_apply": "burning",
 "stat_mod": {"enemy": {"might": -3, "essence": -2}}, "mod_duration": 3}
```
**Description:** White holy fire purifies the corrupted. The flame burns away corruption from the enemy. Sanctity intensifies the burn as the enemy's HP drops. Only triggers when the enemy has a status effect.
**Narrative:** The Priest opens their palm. The fire is white — not hot, not red, but clean. It wraps around the enemy and finds the corruption, the poison, the dark thing hiding beneath the skin. It burns that and nothing else. Against the undead, the fire doesn't just cleanse — it unmakes. The enemy screams. The Priest watches. The flame does its work. Only triggers when the enemy has a status effect.

---

### 10. Angel's Grace
```python
{"id": "angels_grace", "name": "Angel's Grace", "cooldown": 5,
 "power_type": "buff", "trigger": "always",
 "self_status": "inspired",
 "stat_mod": {"self": {"grace": 3, "essence": 2, "durability": 2}}, "mod_duration": 3}
```
**Description:** Soft feathers of light drift around the Priest as divine favor blesses them. Sanctity amplifies the grace as the enemy crumbles.
**Narrative:** The Priest doesn't summon the feathers. They just arrive — white, soft, impossible, drifting like snow. They settle on the Priest's shoulders, their arms, their brow. Each one is a whisper of approval from something vast and kind. The Priest moves with new purpose. The feathers follow. The enemy falters. The feathers don't.

---

### 11. Judgment Strike
```python
{"id": "judgment_strike", "name": "Judgment Strike", "cooldown": 4,
 "power_type": "strike", "damage_type": "holy", "trigger": "always",
 "status_apply": "shaken",
 "stat_mod": {"enemy": {"grace": -3, "might": -2}}, "mod_duration": 3}
```
**Description:** The Priest channels holy power into a single divine strike. Holy damage scales with Sanctity — the weaker the enemy, the harder the judgment falls.
**Narrative:** The Priest doesn't swing a weapon. They extend a hand. The holy power that erupts is not a spell — it's a verdict. It hits the enemy like a gavel, and the enemy's confidence shatters with it. Their grace breaks. Their might falters. The Priest's arm doesn't waver. The enemy has been judged. The sentence is ongoing.

---

### 12. Divine Rebuke
```python
{"id": "divine_rebuke", "name": "Divine Rebuke", "cooldown": 4,
 "power_type": "debuff", "damage_type": "holy", "trigger": "always",
 "status_apply": "shaken",
 "stat_mod": {"enemy": {"might": -3, "grace": -3, "cognition": -2}}, "mod_duration": 3}
```
**Description:** The Priest points forward as holy power erupts, driving back darkness. Sanctity deepens the rebuke as the enemy's HP drops.
**Narrative:** The Priest doesn't shout. They point. One finger, one direction, one judgment. The holy power that erupts is not a request. It's a boundary. The enemy crosses it and the world pushes back — hard. The darkness recoils. The enemy staggers. The Priest's arm doesn't waver. The enemy is learning what holy means.

---

### 13. Light of Hope
```python
{"id": "light_of_hope", "name": "Light of Hope", "cooldown": 4,
 "power_type": "defend", "trigger": "self_debuff",
 "self_status": "warded",
 "stat_mod": {"self": {"essence": 2, "grace": 2}}, "mod_duration": 3}
```
**Description:** A calming light restores determination, dispelling fear and despair from the Priest. Sanctity strengthens the restoration as the enemy weakens. Only triggers when debuffed.
**Narrative:** The fear is a weight — cold, old, pressing. The Priest closes their eyes and remembers why they kneel. Not for power. Not for glory. For hope. The light comes from within, soft and steady. The fear lifts. The Priest opens their eyes. The enemy is bleeding. The Priest is still here. The Priest will be here tomorrow. Only triggers when debuffed.

---

## Expert Tier (Level 8, 400g, 1hr) — 1 Heal, 1 Strike, 1 Buff, 2 Debuffs, 1 Shield Wall, 1 Defend

### 14. Divine Light
```python
{"id": "divine_light", "name": "Divine Light", "cooldown": 0,
 "power_type": "heal", "heal_type": "normal", "trigger": "always",
 "target": "ally",
 "self_status": "warded",
 "heal_percent": 0.20,
 "stat_mod": {"self": {"essence": 3, "durability": 2}}, "mod_duration": 3}
```
**Description:** A pillar of holy light descends on the target, healing 20% of their max HP. Normal turn order — can go first or second. **No cooldown.** The bread-and-butter heal. Sanctity amplifies the heal as the enemy's HP drops — at low enemy HP, this heal can reach 40%. If Miracle triggers, heals twice.
**Narrative:** The Priest raises both hands. The light doesn't gather — it arrives. A pillar, golden, solid, patient. It falls on the wounded and the wounds close. Not slowly. Not gently. Completely. The enemy watches the light fall and knows: that light is not for them. The light is for the faithful. The enemy is not faithful. The enemy is bleeding. The Priest's ally is not.

---

### 15. Mass Purify
```python
{"id": "mass_purify", "name": "Mass Purify", "cooldown": 5,
 "power_type": "defend", "trigger": "self_debuff",
 "self_status": "warded",
 "stat_mod": {"self": {"essence": 3, "durability": 2}}, "mod_duration": 3}
```
**Description:** The Priest raises a sacred relic as cleansing light spreads outward, removing curses and poison. Sanctity deepens the purification as the enemy weakens. Only triggers when debuffed.
**Narrative:** The relic is old — a shard of something holy, carried for generations. When the Priest raises it, the light doesn't just glow. It cleanses. Poison evaporates. Curses unravel. The dark things clinging to the Priest's skin scream and let go. The light fades. The Priest is clean. The darkness is gone. The enemy is next. Only triggers when debuffed.

---

### 16. Heaven's Judgment
```python
{"id": "heavens_judgment", "name": "Heaven's Judgment", "cooldown": 5,
 "power_type": "strike", "damage_type": "holy", "trigger": "always",
 "status_apply": "shaken",
 "stat_mod": {"enemy": {"might": -3, "grace": -3, "armor_bonus": -2}}, "mod_duration": 3}
```
**Description:** A beam of radiant judgment descends from the sky, calling divine wrath upon evil. Holy damage scales with Sanctity — the weaker the enemy, the heavier the verdict. Deals +50% to undead and devils.
**Narrative:** The Priest raises both hands. The sky opens — not with clouds, but with purpose. A beam of holy light descends, silent, absolute, patient. It finds the enemy. It doesn't negotiate. The enemy is driven to their knees under a weight that isn't physical. Against the undead, the beam doesn't just judge — it annihilates. The judgment is not about pain. It's about truth. The truth is heavy. And it's getting heavier.

---

### 17. Radiant Prison
```python
{"id": "radiant_prison", "name": "Radiant Prison", "cooldown": 6,
 "power_type": "debuff", "damage_type": "holy", "trigger": "always",
 "status_apply": "bind",
 "stat_mod": {"enemy": {"grace": -3, "might": -2}}, "mod_duration": 2}
```
**Description:** A cage of pure holy light forms around the enemy, binding them completely for 2 turns. The enemy cannot act or dodge. Sanctity extends the imprisonment as the enemy weakens. Upgraded Chain of Light.
**Narrative:** The Priest draws a square in the air. The light doesn't descend this time — it grows. Bars of radiance rise from the ground, locking into place around the enemy. A cage. Not of iron — of judgment. The enemy throws themselves against the bars and the bars sing, holy and unmoved. The Priest watches the caged thing and prepares the next prayer. The prison is patient. The Priest is patient. The enemy is running out of time.

---

### 18. Beacon of Faith
```python
{"id": "beacon_of_faith", "name": "Beacon of Faith", "cooldown": 5,
 "power_type": "buff", "trigger": "always",
 "self_status": "inspired",
 "heal_percent": 0.08,
 "stat_mod": {"self": {"essence": 4, "cognition": 2}}, "mod_duration": 4}
```
**Description:** A brilliant beacon shines into the heavens, strengthening the faithful and mending wounds. Sanctity amplifies both the buff and the heal as the enemy crumbles.
**Narrative:** The Priest raises a hand. Light erupts — not outward, but upward. A pillar of radiance punches into the sky. Everyone on the battlefield sees it. The faithful feel it: a warmth, a steadiness, a reminder. The Priest stands at the base of the pillar, and the pillar stands with them. The enemy looks up. The enemy should not have looked up.

---

### 19. Sunflare
```python
{"id": "sunflare", "name": "Sunflare", "cooldown": 6,
 "power_type": "debuff", "damage_type": "holy", "trigger": "always",
 "status_apply": "blind",
 "stat_mod": {"enemy": {"might": -3, "grace": -3}}, "mod_duration": 3}
```
**Description:** The Priest summons a miniature sun that detonates with holy radiance, blinding the enemy for 3 turns and crushing their might. Sanctity extends the blindness as the enemy weakens. Upgraded Blinding Light.
**Narrative:** The Priest holds both palms upward. The light gathers — not a flash this time, but a star. Small, white, burning, impossible. It rises. It detonates. The battlefield whites out. When vision returns, the enemy is blinking, weeping, swinging at shadows. Their might is gone — not taken, but forgotten. The Priest stands in the afterglow, eyes open, unbothered. The sun is holy. The sun is patient. The enemy cannot see.

---

### 20. Radiant Bulwark
```python
{"id": "radiant_bulwark", "name": "Radiant Bulwark", "cooldown": 6,
 "power_type": "shield_wall", "trigger": "always",
 "shield_hp": 0.35,
 "status_apply": "blind",
 "self_status": "warded"}
```
**Description:** A towering wall of holy light surrounds the Priest with a temporary HP bar that absorbs 35% of max HP (Sanctity-scaled). When the shield is struck, the holy light flares and applies `blind` to the enemy — the wall fights back. At low enemy HP, the shield can reach 70% absorb. Shield Walls do not stack — casting a new one replaces the old. If Miracle triggers, the shield is recast at full HP (replaces the old shield).
**Narrative:** The Priest raises both hands. Light doesn't just glow — it towers. A wall of radiance rises from the ground, solid, humming, alive. The enemy swings. The wall holds. And then — the wall flares. The light blazes outward from the impact point, searing the enemy's eyes. They stumble back, blind, swinging at nothing. The wall stands. The Priest stands behind it. The enemy cannot see. The enemy cannot break through. The wall is fighting back.

---

## Master Tier (Level 15, 1000g, 1hr) — 1 Shield Wall, 1 Strike, 2 Heals, 1 Debuff, 3 Buffs

### 21. Sanctuary
```python
{"id": "sanctuary_priest", "name": "Sanctuary", "cooldown": 6,
 "power_type": "shield_wall", "trigger": "always",
 "shield_hp": 0.50,
 "self_status": "warded",
 "stat_mod": {"self": {"essence": 4, "durability": 3}}, "mod_duration": 4}
```
**Description:** Sacred symbols bloom across the ground, creating a holy zone of safety. Shield Wall HP = 50% of max HP (Sanctity-scaled). When the shield breaks, holy chains erupt from the shards and apply `bind` to the enemy — the sanctuary fights back even in death. At low enemy HP, the shield can reach 100% absorb. Shield Walls do not stack — casting a new one replaces the old (breaking the old shield triggers its `bind` effect). If Miracle triggers, the shield is recast at full HP (replaces the old shield).
**Narrative:** The Priest speaks the word. The ground answers. Symbols — ancient, golden, burning — bloom across the earth in a circle around the Priest. But this isn't just a ward. It's a fortress. The wall has weight. The wall has HP. The enemy throws everything at it and the wall holds — 50% of the Priest's max HP, thickened by Sanctity. And when it finally breaks? The shards don't scatter. They become chains. Holy chains erupt from the fragments and bind the enemy where they stand. The sanctuary doesn't just protect. It punishes those who break it.

---

### 22. Holy Lance
```python
{"id": "holy_lance", "name": "Holy Lance", "cooldown": 6,
 "power_type": "strike", "damage_type": "holy", "trigger": "always",
 "status_apply": "bleeding",
 "stat_mod": {"enemy": {"might": -4, "armor_bonus": -3}}, "mod_duration": 3}
```
**Description:** The Priest summons a lance of pure holy light and hurls it at the enemy. Holy damage pierces defenses and causes bleeding on undead and devils. Sanctity amplifies the strike as the enemy's HP drops.
**Narrative:** The Priest doesn't throw a weapon. They throw a verdict. The lance forms in their hand — not forged, but manifested, pure holy light compressed into a spear. It flies. It doesn't miss. It pierces the enemy and the light detonates inside, burning from within. Against the undead, the wound doesn't just bleed — it unravels. The enemy staggers. The lance is gone. The light stays. The enemy is coming apart.

---

### 23. Promise of Heaven
```python
{"id": "promise_of_heaven", "name": "Promise of Heaven", "cooldown": 7,
 "power_type": "heal", "heal_type": "delayed", "trigger": "always",
 "target": "ally",
 "self_status": "inspired",
 "heal_percent": 0.35,
 "mod_duration": 2}
```
**Description:** A holy buff applied to the target. After **2 turns**, the target is healed for 35% of their max HP in a single tick. High risk/reward — the target must survive 2 turns before the heal triggers. Sanctity amplifies the payoff — at low enemy HP, this can heal 70%. If Miracle triggers, the heal ticks twice (70% base, up to 140% with Sanctity).
**Narrative:** The Priest doesn't heal the wound. They make a promise. The light settles into the target — not as a glow, but as a countdown. Two turns. The target feels it: a warmth building, building, not yet released. The enemy sees it and panics — they have two turns to kill the target before the promise breaks. Two turns to finish what they started. But the enemy is weakening. The promise is growing. And when the second turn ends, the heavens open. The light arrives. 35% — no, more. The enemy is at 20% HP. Sanctity doubles it. The promise is fulfilled. The target stands. The enemy does not.

---

### 24. Hymn of Salvation
```python
{"id": "hymn_of_salvation", "name": "Hymn of Salvation", "cooldown": 7,
 "power_type": "heal", "heal_type": "group", "trigger": "always",
 "target": "all_allies",
 "self_status": "inspired",
 "heal_percent": 0.15,
 "stat_mod": {"self": {"essence": 4, "durability": 3}}, "mod_duration": 3}
```
**Description:** The Priest's voice echoes with celestial harmony, healing **all party members** for 15% of their max HP. The Priest's only group skill. Sanctity boosts all targets — at low enemy HP, this becomes a 30% group heal. If Miracle triggers, all allies are healed twice.
**Narrative:** The Priest sings. Not a battle cry — a hymn. Old, simple, the kind sung in temples at dawn. The notes don't just sound; they heal. Every ally on the battlefield feels it — a warmth, a steadiness, a closing of wounds. The enemy hears it too, and the hymn is not for them. The hymn is for the faithful. The enemy is not faithful. The enemy is bleeding. The allies are not. The Priest doesn't stop singing until everyone who can hear is whole.

---

### 25. Final Judgment
```python
{"id": "final_judgment", "name": "Final Judgment", "cooldown": 8,
 "power_type": "debuff", "damage_type": "holy", "trigger": "opponent_wounded",
 "status_apply": ["bind", "blind"],
 "stat_mod": {"enemy": {"might": -5, "grace": -5, "essence": -3}}, "mod_duration": 3}
```
**Description:** The Priest pronounces the final verdict — holy chains bind the enemy completely while holy light blinds them. Applies both `bind` and `blind` for 3 turns. The enemy cannot act, cannot dodge, cannot see. Sanctity extends the judgment as the enemy's HP drops. Only triggers when the enemy is wounded.
**Narrative:** The Priest speaks the words. Not a prayer — a sentence. The words are old, final, and carry the weight of something that cannot be appealed. Chains of light descend. Light blazes. The enemy is bound and blind at the same time — chained, seared, locked in holy judgment. They cannot move. They cannot see. They cannot fight. The Priest watches the condemned thing and begins the last prayer. The verdict is delivered. The execution is next. Only triggers when the enemy is wounded.

---

### 26. Holy Revelation
```python
{"id": "holy_revelation", "name": "Holy Revelation", "cooldown": 6,
 "power_type": "buff", "trigger": "always",
 "self_status": "inspired",
 "stat_mod": {"self": {"cognition": 4, "insight": 3, "essence": 2}}, "mod_duration": 4}
```
**Description:** Mystic visions unfold before the faithful. The Priest sees the enemy's weaknesses with divine clarity. Sanctity amplifies the revelation as the enemy crumbles.
**Narrative:** The Priest closes their eyes. The visions come — not asked for, but given. They see the enemy's past, their fears, the crack in their armor that no one else can see. They see the battle before it happens. The Priest opens their eyes. They know exactly where to strike, where to heal, where to stand. The enemy feels exposed. They should. The Priest can see everything they're afraid of.

---

### 27. Prayer Circle
```python
{"id": "prayer_circle", "name": "Prayer Circle", "cooldown": 6,
 "power_type": "buff", "trigger": "always",
 "self_status": "inspired",
 "heal_percent": 0.10,
 "stat_mod": {"self": {"insight": 3, "grace": 3, "essence": 3, "cognition": 2}}, "mod_duration": 4}
```
**Description:** The Priest combines prayers into overwhelming divine power, empowering all stats and healing. Sanctity amplifies both the buff and the heal as the enemy weakens.
**Narrative:** The Priest begins to pray — not one prayer, but all of them. Every prayer they know, spoken simultaneously, woven together like threads in a tapestry. The words overlap, harmonize, build. The light that comes is not a single beam. It's a cathedral of radiance. The Priest stands in the center, and everything about them sharpens. The enemy is crumbling. The Priest is ascending.

---

### 28. Divine Covenant
```python
{"id": "divine_covenant", "name": "Divine Covenant", "cooldown": 6,
 "power_type": "buff", "trigger": "always",
 "self_status": "inspired",
 "heal_percent": 0.12,
 "stat_mod": {"self": {"insight": 4, "essence": 4, "grace": 3, "durability": 2}}, "mod_duration": 4}
```
**Description:** Golden threads of light connect the Priest to the divine, forging a sacred bond that empowers and heals. Sanctity amplifies the covenant as the enemy crumbles. The strongest Priest buff.
**Narrative:** The Priest speaks the covenant — not a prayer, but a contract. Golden threads appear, connecting the Priest to the sky, to the earth, to something beyond. The threads pulse with power. The Priest's body heals. Their faith hardens. The enemy sees the threads and understands: this isn't a person anymore. This is a representative. And the representative is winning.

---

## Legendary Tier (Level 20, 2500g, 1 day — Quest-gated) — 2 Holy True-Damage Strikes

### 29. Choir of Heaven
```python
{"id": "choir_of_heaven", "name": "Choir of Heaven", "cooldown": 8,
 "power_type": "strike", "damage_type": "true", "trigger": "always",
 "status_apply": "stunned",
 "self_status": "inspired",
 "heal_percent": 0.15,
 "stat_mod": {"enemy": {"might": -5, "grace": -5, "armor_bonus": -6, "essence": -4, "cognition": -3}},
 "mod_duration": 4}
```
**Description:** Angelic hymns fill the battlefield as celestial voices descend. True damage ignores all defense. Holy power devastates enemy stats. Heals the Priest. Grants `inspired`. Sanctity doubles the true damage at low enemy HP. Deals +50% to undead and devils.
**Narrative:** The Priest opens their mouth. What comes out is not one voice. It's a choir — vast, harmonious, impossible. The sound fills the battlefield, and it's not just sound. It's judgment. It's mercy. It's the weight of every prayer ever spoken, arriving at once. The enemy hears it and buckles. Their strength drains. Their defenses crumble. Their certainty shatters. Against the undead, the choir doesn't just sing — it unmade. The Priest stands at the center of the chorus, and the chorus is not impressed. The enemy is dying. The choir is just getting started.

**Quest: The Celestial Choir**
- **Trainer:** Serathiel Moonglow (Solunara)
- **Min Level:** 20
- **Objectives:**
  - Kill 5 Undead in the Ashen Border
  - Gather 3 Relic Shards
  - Learn at least 5 Priest skills from Serathiel Moonglow
- **Reward:** Unlocks Choir of Heaven

---

### 30. Legend of the Faithful
```python
{"id": "legend_of_the_faithful", "name": "Legend of the Faithful", "cooldown": 10,
 "power_type": "strike", "damage_type": "true", "trigger": "low_hp",
 "status_apply": ["stunned", "blind"],
 "self_status": "inspired",
 "heal_percent": 0.25,
 "stat_mod": {"enemy": {"might": -6, "grace": -6, "armor_bonus": -8, "essence": -5, "cognition": -4, "durability": -4}},
 "mod_duration": 5}
```
**Description:** Countless wings of light unfold behind the Priest as divine radiance transforms the battlefield. The Priest becomes the chosen vessel of the heavens. True damage ignores all defense. Applies `stunned` and `blind`. Devastates all enemy stats. Heals the Priest massively. Grants `inspired`. Sanctity doubles the true damage at low enemy HP. Deals +50% to undead and devils. Only usable when below 25% HP.
**Narrative:** The Priest is dying. The faith is not. They kneel, and the heavens descend — not gently, but completely. Wings unfold behind the Priest: not two, not four, but countless — vast, radiant, filling the sky. The Priest rises, and they are not a person anymore. They are a vessel. The divine pours through them, and what pours out is not a spell. It is a verdict. The enemy is stunned. The enemy is blind. The enemy feels every prayer the Priest has ever spoken, arriving at once. The battlefield becomes a cathedral. The enemy becomes a sinner. The Priest becomes the legend. Triggers when HP is low.

**Quest: The Celestial Choir**
- **Trainer:** Serathiel Moonglow (Solunara)
- **Min Level:** 20
- **Objectives:**
  - Complete "The Celestial Choir" quest (learn Choir of Heaven first)
  - Kill 1 Heritage Boss
  - Gather 1 Jahra Ingot
  - Learn at least 15 Priest skills total
- **Reward:** Unlocks Legend of the Faithful

---

## Legendary Passive Quest — Hand of God

**Quest: The Hand of God**
- **Trainer:** Serathiel Moonglow (Solunara)
- **Min Level:** 20
- **Objectives:**
  - Complete "The Celestial Choir" quest (learn Legend of the Faithful first)
  - Kill 3 Heritage Bosses
  - Gather 3 Jahra Ingots
  - Learn at least 20 Priest skills total
  - Reach level 100
- **Reward:** Unlocks Hand of God passive — the Priest becomes the divine itself
