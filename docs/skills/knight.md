# Knight Mastery — 30 Skills + 5 Oaths + 10 Passives

**Role:** The Oathbound — a heavy armor frontline warrior who commits to a sacred Oath before battle, growing stronger each turn they hold it. The longer the Knight stays committed, the more unstoppable they become.
**Masteries per trainer:** 3 (Knight + 2 others)
**Trainers teaching Knight:** Oathspire, Grunhold, Warforge, Jahrahold

---

## Knight Identity

**Core loop:** Choose Oath → hold it → stack power → unleash heavy strikes → never switch

- **Pure physical** — no magical damage, no elemental effects. Steel on steel.
- **No healing** — Knight survives through armor and defiance, not recovery.
- **No evasion, no stealth** — Knight stands in the open and dares the enemy to hit them.
- **No multi-hit** — one heavy hit, not many small ones. `hits` is always 1.
- **Self-buff focused** — all buffs target self. The Knight is the wall, not the cheerleader.
- **Ramping power curve** — moderate early, monstrous once Oath stacks accumulate.
- **Commitment = power** — switching Oaths resets stacks to 0. The Knight doesn't adapt; they double down.

### The Oath System

The Knight has **5 Oaths** — all unlocked at level 1. Before each battle, the Knight chooses one Oath to swear. The Oath sits in a dedicated **Oath slot** below the skill bar.

**How Oaths work:**
- Each Oath gains stacks through **different combat triggers** (see table below) — choosing an Oath means choosing how you fight
- The Oath's effect multiplies by the current stack count (+1 per stack)
- At **5 stacks**, the Oath's 5-stack milestone bonus activates
- At **10 stacks**, the Oath's 10-stack milestone bonus activates
- If the Knight switches Oaths, **stacks reset to 0** (or save 3 with Second Wind / Eternal Oath)
- Oath effects are **always-on** — they don't compete with skills for turns

**Example:**
- Turn 1: Knight swears Oath of Iron. Gets hit. Stack = 1. +1 `armor_bonus`.
- Turn 3: Gets hit again, uses defend skill. Stack = 3. +3 `armor_bonus`.
- Turn 7: Still holding Iron. Stack = 7. +7 `armor_bonus`. 5-stack milestone active: immune to `shaken`.
- Turn 8: Knight switches to Oath of Wrath. Stack = 0. No bonus this turn.
- Turn 9: Knight deals damage. Oath of Wrath. Stack = 1. +1 `might`.

**Why this works:**
- **Playstyle diversity** — each Oath gains stacks differently, so choosing Iron plays completely differently than choosing Wrath
- **Commitment** — the Knight commits to a strategy and is rewarded for holding it
- **Ramping terror** — enemies must kill the Knight fast or face a monster
- **Trade-offs** — switching is always available but always punished
- **Unique identity** — no other mastery has a pre-battle commitment system

### The 5 Oaths

| # | Name | +1 per Stack | Stack Trigger | 5-Stack Bonus | 10-Stack Bonus | Theme |
|---|------|-------------|--------------|---------------|----------------|-------|
| 1 | Oath of Iron | +1 `armor_bonus` | Gain stack when **hit** or when using a **defend skill** | Immune to `shaken` — the wall doesn't crack | Reflect 10% incoming damage back to attacker — the wall hits back | Defense — become a wall |
| 2 | Oath of Wrath | +1 `might` | Gain stack when you **deal damage** (2 stacks on roll 5+) | +20% strike damage — the hammer swings harder | All strikes apply `bleeding` — the hammer draws blood | Offense — become a hammer |
| 3 | Oath of Bulwark | -1 enemy `might`, -1 enemy `grace` | Gain stack when **enemy attacks you** (hit or miss) | Enemy cannot gain buffs — crushed spirit | Enemy attacks have -20% accuracy — can barely swing | Control — crush the enemy down |
| 4 | Oath of Endurance | +1 `durability` | Gain stack at **end of every turn** (+1 extra below 50% HP) | Immune to `stunned` — nothing stops you | Additional -15% incoming damage — near invulnerable | Survivability — outlast anything |
| 5 | Oath of Vanguard | +1 all stats, -1 `armor_bonus` | Gain stack when you **strike before the enemy acts** or use `opening_move` skills | Armor penalty removed — the risk pays off | +1 all stats/stack becomes +2 all stats/stack — all-in rewarded | High risk/reward — all-in |

### Stat Focus

| Stat | Priority | Why |
|------|----------|-----|
| `armor_bonus` | **Primary** | Knight is the armor mastery — highest defense in the game |
| `might` | **Primary** | Raw physical force — heavy strikes, no finesse |
| `durability` | **Secondary** | Endurance, HP pool, staying power |
| `grace` | **Minimal** | Knights aren't graceful — they're reliable |
| `insight` | **None** | No magic, no elemental scaling |
| `essence` | **None** | No magic resistance focus — armor handles defense |
| `cognition` | **Minimal** | Not a utility class |

### Status Identity

| Status | Role |
|--------|------|
| `warded` | **Signature** — Knight's defensive buff, applied on almost every buff skill |
| `stunned` | **Signature** — Knight controls through impact, not poison or fear |
| `shaken` | **Secondary** — armor crushing breaks confidence |
| `bleeding` | **Rare** — only on heavy execution strikes |
| `inspired` | **None** — Knight doesn't inspire, they *anchor* |

### Trigger Identity

| Trigger | Role |
|---------|------|
| `always` | **Primary** — Knight is consistent, always ready |
| `low_hp` | **Secondary** — Knight's defiance shines when wounded |
| `opening_move` | **Secondary** — the charge, the first strike |
| `opponent_wounded` | **Rare** — Knight doesn't chase, they hold ground |
| `self_debuff` | **Rare** — Knight rarely gets debuffed (high armor) |

### What the Knight Does NOT Do

- **No healing** (that's Priest/Druid/Paladin)
- **No magical damage** (that's Mage/Paladin/Druid)
- **No evasion/hidden** (that's Assassin/Rogue/Hunter)
- **No multi-hit combos** (that's Assassin/Lancer)
- **No poison/burning/DoT** (that's Assassin/Alchemist/Hunter)
- **No ally buffs** (that's Bard/Paladin — Knight buffs *themselves*)
- **No mobility skills** (that's Lancer/Rogue — Knight stands and fights)

---

## Passives — Auto-Learned, Unlocked Every 10 Levels

| # | Name | Level | Effect |
|---|------|-------|--------|
| 1 | Oath Sworn | 10 | Start every combat with 2 Oath stacks instead of 0 |
| 2 | Extended Vow | 20 | Each stack-gain event gives +1 extra stack (stacks build twice as fast) |
| 3 | Battle Hardened | 30 | +10 permanent `armor_bonus` (innate, always active) |
| 4 | Adrenal Surge | 40 | When HP drops below 50%, gain `might +15` for 3 turns (once per combat) |
| 5 | Iron Will | 50 | Immune to `shaken` and `stunned` status effects — the Oath cannot be broken |
| 6 | Oath Mastery | 60 | At 5+ Oath stacks, the Oath's effect doubles |
| 7 | Fortress | 70 | At 10+ Oath stacks, all incoming damage reduced by 25% |
| 8 | Unbreakable | 80 | When below 25% HP, reduce all incoming damage by 30% |
| 9 | Second Wind | 90 | Switching Oaths saves 3 stacks instead of resetting to 0 |
| 10 | Eternal Oath | 100 | All Oath effects tripled. Switching Oaths saves 3 stacks. Oath Milestone bonuses (5-stack and 10-stack) are always active |

### Passive Synergy

```
Level 10:  Start with 2 stacks → immediate power, not a slow start
Level 20:  Stack gains doubled → reach milestones faster
Level 30:  Base armor always higher → tankier without Oath
Level 40:  Mid-fight might spike when wounded → defiance
Level 50:  Can't be controlled → the Oath cannot be broken
Level 60:  THE POWER ENGINE → 5+ stacks = doubled Oath effect
Level 70:  THE DEFENSE ENGINE → 10+ stacks = 25% damage reduction
Level 80:  Can't be bursted at low HP → ultimate tank
Level 90:  Switching saves 3 stacks → flexibility without starting over
Level 100: EVERYTHING TRIPLED, MILESTONES ACTIVE → the eternal Knight
```

**The full build at level 100:**
- Oath effects tripled (Oath of Iron = +3 armor/stack, Oath of Wrath = +3 might/stack, etc.)
- Switching Oaths saves 3 stacks — swap without starting from zero
- Start with 2 stacks, each stack-gain event gives +1 extra (Extended Vow doubles stack rate)
- At 5+ stacks, Oath effect doubles (Oath Mastery) + 5-stack milestone bonus active
- At 10+ stacks, 25% damage reduction (Fortress) + 10-stack milestone bonus active
- "The Knight doesn't swear an Oath. The Knight becomes the Oath."

---

## Skill Structure

All skills use the new format — no `power` or `skill_capacity_cost`.

| Field | Description |
|-------|-------------|
| `power_type` | strike, defend, debuff, buff |
| `damage_type` | physical, true (strikes only) |
| `trigger` | always, low_hp, opponent_wounded, opening_move, self_debuff |
| `status_apply` | Status inflicted on enemy |
| `self_status` | Status applied to self (always `warded` for buffs) |
| `stat_mod` | Temporary stat changes — `{"self": {...}, "enemy": {...}}` |
| `mod_duration` | How many turns stat_mod lasts (3-5 for buffs to enable stacking) |

**Knight rules:** No `heal_percent`. No `magical` damage. No `hits` > 1. No `evasive`/`hidden`/`inspired` self_status. All buffs target self only. Skills should reference Oath synergy, commitment, and ramping power in descriptions. Buffs focus on `armor_bonus`, `might`, and `durability` — NOT `grace`/`insight`/`essence`.

---

## Tier Overview

| Tier | Level Req | Gold Cost | Learn Time | Count | Buffs | Strikes | Defends | Debuffs |
|------|-----------|-----------|------------|-------|-------|---------|---------|---------|
| Basic | 1 | 50g | 5 min | 6 | 4 | 2 | 0 | 0 |
| Advanced | 3 | 150g | 30 min | 7 | 3 | 3 | 0 | 1 |
| Expert | 8 | 400g | 1 hr | 7 | 2 | 2 | 3 | 0 |
| Master | 15 | 1000g | 1 hr | 8 | 4 | 2 | 2 | 0 |
| Legendary | 20 | 2500g | 1 day | 2 | 0 | 2 | 0 | 0 |
| **Total** | | | | **30** | **13** | **11** | **5** | **1** |

---

## Basic Tier (Level 1, 50g, 5min) — 4 Buffs, 2 Strikes

### 1. Shield Bash
```python
{"id": "shield_bash", "name": "Shield Bash", "cooldown": 2,
 "power_type": "strike", "damage_type": "physical", "trigger": "always",
 "status_apply": "stunned",
 "stat_mod": {"enemy": {"might": -2}}, "mod_duration": 2}
```
**Description:** The Knight drives their shield directly into the opponent's chest, staggering them.
**Narrative:** The Knight plants their feet and slams the shield forward with the weight of an oath behind it. The enemy staggers, ears ringing, strength faltering. Simple. Effective. The first thing every Knight learns.

---

### 2. Iron Stance
```python
{"id": "iron_stance", "name": "Iron Stance", "cooldown": 3,
 "power_type": "buff", "trigger": "always",
 "self_status": "warded",
 "stat_mod": {"self": {"armor_bonus": 2, "might": 2}}, "mod_duration": 3}
```
**Description:** The Knight plants their feet, lowers their center of gravity, and locks into a foundational combat stance. Synergizes with any Oath — the stance holds while the Oath stacks.
**Narrative:** Nothing fancy. No flash, no roar, no light. The Knight just... stands differently. Feet wider. Knees bent. Weight settled. But the enemy's next blow lands differently too — heavier in the arm, lighter in the result. The stance holds. The Knight holds. The Oath holds. Everything holds.

---

### 3. War Cry
```python
{"id": "war_cry", "name": "War Cry", "cooldown": 4,
 "power_type": "buff", "trigger": "opening_move",
 "self_status": "warded",
 "stat_mod": {"self": {"might": 3}}, "mod_duration": 3}
```
**Description:** The Knight raises their weapon and unleashes a battle cry, hardening their resolve for the fight ahead.
**Narrative:** A roar splits the silence before the charge. The Knight's voice carries the weight of every war they've survived. The muscles tighten. The grip solidifies. The fear doesn't go away — it just becomes irrelevant. Opening move only.

---

### 4. Vanguard Step
```python
{"id": "vanguard_step", "name": "Vanguard Step", "cooldown": 3,
 "power_type": "buff", "trigger": "always",
 "self_status": "warded",
 "stat_mod": {"self": {"armor_bonus": 3}}, "mod_duration": 3}
```
**Description:** The Knight steps forward, shield raised, armor angled to catch the coming blow.
**Narrative:** The Knight steps forward first — not charging, not running, just advancing. One step. The shield angles. The plate aligns. The enemy's next strike will hit steel at the worst possible angle. The Knight knows this because the Knight designed it that way.

---

### 5. Pommel Strike
```python
{"id": "pommel_strike", "name": "Pommel Strike", "cooldown": 2,
 "power_type": "strike", "damage_type": "physical", "trigger": "always",
 "status_apply": "stunned",
 "stat_mod": {"enemy": {"might": -2, "grace": -1}}, "mod_duration": 2}
```
**Description:** The Knight reverses their grip and drives the pommel into the enemy's jaw or temple.
**Narrative:** The blade is for cutting. The pommel is for convincing. The Knight reverses the grip and drives the hard steel knob into the enemy's face. Stars burst. Knees buckle. The enemy's next swing will be slower, clumsier, and weaker. The Knight is already re-gripping.

---

### 6. Steady Grip
```python
{"id": "steady_grip", "name": "Steady Grip", "cooldown": 3,
 "power_type": "buff", "trigger": "always",
 "self_status": "warded",
 "stat_mod": {"self": {"might": 2, "armor_bonus": 2}}, "mod_duration": 3}
```
**Description:** The Knight adjusts their grip on sword and shield, locking both into optimal position. Synergizes with Oath of Wrath — might buffs compound with Oath stacks.
**Narrative:** A small adjustment — half an inch on the sword, a quarter turn on the shield. It looks like nothing. It changes everything. The blade strikes truer. The shield covers more. The Knight's hands don't shift because the Knight's hands never shift. Another layer on the Oath. The commitment deepens.

---

## Advanced Tier (Level 3, 150g, 30min) — 3 Buffs, 3 Strikes, 1 Debuff

### 7. King's Challenge
```python
{"id": "kings_challenge", "name": "King's Challenge", "cooldown": 4,
 "power_type": "debuff", "damage_type": "physical", "trigger": "always",
 "status_apply": "shaken",
 "stat_mod": {"enemy": {"might": -3}}, "mod_duration": 3}
```
**Description:** The Knight plants their sword into the ground, raises their shield high, and roars a royal challenge.
**Narrative:** The blade sinks into the earth. The shield rises. The Knight's voice rolls across the field like a war-drum, and every enemy feels their courage wither. The challenge is not a request. It's a dare. The enemy accepts. They shouldn't have.

---

### 8. Lion's Charge
```python
{"id": "lions_charge", "name": "Lion's Charge", "cooldown": 3,
 "power_type": "strike", "damage_type": "physical", "trigger": "opening_move",
 "status_apply": "stunned",
 "stat_mod": {"enemy": {"armor_bonus": -3}}, "mod_duration": 2}
```
**Description:** With explosive speed, the Knight lowers their shoulder and charges, smashing through the front line.
**Narrative:** The Knight explodes from the line — shield first, boots tearing earth. The impact crumples armor like parchment. The enemy flies backward, ears full of the Lion's roar. Opening move only. There is no second charge. There doesn't need to be.

---

### 9. Heavy Strike
```python
{"id": "heavy_strike", "name": "Heavy Strike", "cooldown": 3,
 "power_type": "strike", "damage_type": "physical", "trigger": "always",
 "status_apply": "shaken",
 "stat_mod": {"enemy": {"armor_bonus": -3}}, "mod_duration": 3}
```
**Description:** The Knight winds up and delivers a single devastating overhead blow. No finesse, no technique — just mass and steel.
**Narrative:** The Knight doesn't swing — they drop. The blade comes down with the full weight of plate, muscle, and intent. The enemy's armor doesn't block it; it witnesses it. The dent is deep. The enemy's confidence is deeper gone. This is what stacked might looks like when it hits something.

---

### 10. Bulwark
```python
{"id": "bulwark", "name": "Bulwark", "cooldown": 5,
 "power_type": "buff", "trigger": "always",
 "self_status": "warded",
 "stat_mod": {"self": {"armor_bonus": 4, "might": 3}}, "mod_duration": 4}
```
**Description:** The Knight braces shield and body into a single fortified position, reinforcing both offense and defense. Synergizes with Oath of Iron — armor buffs compound with Oath stacks.
**Narrative:** The Knight doesn't move. They become a structure. Shield locked, shoulders squared, weight distributed. The buff settles in — armor hardens, might sharpens. The Oath stacks beneath it. The enemy sees a person. The physics see a wall. Four turns of this. The Knight can wait.

---

### 11. Banner of Valor
```python
{"id": "banner_of_valor", "name": "Banner of Valor", "cooldown": 5,
 "power_type": "buff", "trigger": "always",
 "self_status": "warded",
 "stat_mod": {"self": {"might": 3, "armor_bonus": 2}}, "mod_duration": 4}
```
**Description:** The Knight plants their personal banner into the earth. The Oath it represents hardens their resolve. Synergizes with any Oath — the banner amplifies the commitment.
**Narrative:** The banner strikes the ground and the cloth catches a wind that wasn't there before. It's not magic — it's meaning. The Knight fights for something, and the something fights back through them. The might rises. The armor sets. The Oath deepens. The banner stands. The Knight stands.

---

### 12. Fortress Breaker
```python
{"id": "fortress_breaker", "name": "Fortress Breaker", "cooldown": 4,
 "power_type": "strike", "damage_type": "physical", "trigger": "always",
 "status_apply": "bleeding",
 "stat_mod": {"enemy": {"armor_bonus": -4}}, "mod_duration": 3}
```
**Description:** The Knight lifts the blade with both hands before bringing it down like a falling tower.
**Narrative:** Two hands on the grip. One breath. The blade falls — and the enemy's defense shatters beneath it like a gate that forgot how to hold. The cut goes deep. The bleeding starts. The enemy's armor was their confidence. Both are gone now.

---

### 13. Plate Armor Mastery
```python
{"id": "plate_armor_mastery", "name": "Plate Armor Mastery", "cooldown": 5,
 "power_type": "buff", "trigger": "always",
 "self_status": "warded",
 "stat_mod": {"self": {"armor_bonus": 5, "durability": 3}}, "mod_duration": 4}
```
**Description:** The Knight shifts, tightens, and aligns every strap and plate on their body, maximizing armor effectiveness.
**Narrative:** The Knight takes a breath and adjusts — a buckle here, a pauldron there, a gorget a quarter-inch higher. It takes seconds. The armor goes from "worn" to "integrated." The plates move with the body, not against it. The gaps close. The coverage maximizes. The enemy will need to find a new plan.

---

## Expert Tier (Level 8, 400g, 1hr) — 2 Buffs, 2 Strikes, 3 Defends

### 14. Shield Wall
```python
{"id": "shield_wall", "name": "Shield Wall", "cooldown": 5,
 "power_type": "defend", "trigger": "always",
 "self_status": "warded",
 "stat_mod": {"self": {"armor_bonus": 5, "durability": 2}}, "mod_duration": 4}
```
**Description:** The Knight slams their shield forward and locks into a defensive formation stance.
**Narrative:** The Knight's shield drops into position — not held, but locked. Arm, shoulder, and spine align into a single braced line. Nothing comes through. Nothing ever has. The wall doesn't need allies. The wall is the ally.

---

### 15. Guardian's Sacrifice
```python
{"id": "guardians_sacrifice", "name": "Guardian's Sacrifice", "cooldown": 5,
 "power_type": "defend", "trigger": "low_hp",
 "self_status": "warded",
 "stat_mod": {"self": {"armor_bonus": 5, "might": 3}}, "mod_duration": 3}
```
**Description:** The Knight, wounded and cornered, channels pain into defiance — armor hardens and might surges.
**Narrative:** The Knight is bleeding. The enemy grins. And then the Knight's eyes change — not desperate, not fearful, but *committed*. The pain becomes fuel. The armor feels heavier, but in the right way. The grip tightens. The Knight is wounded, yes. But the Knight is not weakened. Triggers when HP is low.

---

### 16. Commanding Presence
```python
{"id": "commanding_presence", "name": "Commanding Presence", "cooldown": 5,
 "power_type": "buff", "trigger": "always",
 "self_status": "warded",
 "stat_mod": {"self": {"might": 4, "armor_bonus": 3}}, "mod_duration": 4}
```
**Description:** The Knight straightens to full height, radiating authority that reinforces their own combat prowess.
**Narrative:** The Knight doesn't shout. They stand. Taller. Straighter. The armor catches the light differently. The enemy sees it and hesitates — not from fear, but from the recognition that this opponent is not guessing. The Knight knows exactly what they're doing. The buff settles. The might rises. The armor sets.

---

### 17. Crushing Blow
```python
{"id": "crushing_blow", "name": "Crushing Blow", "cooldown": 4,
 "power_type": "strike", "damage_type": "physical", "trigger": "opponent_wounded",
 "status_apply": "shaken",
 "stat_mod": {"enemy": {"armor_bonus": -5, "might": -3}}, "mod_duration": 3}
```
**Description:** The Knight capitalizes on a wounded enemy with a devastating blow that crumbles armor and spirit alike. The longer the Oath has been held, the harder this hits.
**Narrative:** The enemy is hurt — bleeding, staggering, open. The Knight doesn't hesitate. The blade comes down with every Oath stack behind it. The armor doesn't just dent; it cracks. The enemy's might breaks with it. This is what the commitment was for. Only triggers when the enemy is wounded.

---

### 18. Unbreakable Will
```python
{"id": "unbreakable_will", "name": "Unbreakable Will", "cooldown": 4,
 "power_type": "defend", "trigger": "self_debuff",
 "self_status": "warded",
 "stat_mod": {"self": {"durability": 3, "armor_bonus": 3}}, "mod_duration": 3}
```
**Description:** The Knight closes their eyes, remembers their oath, and burns away poison, fear, and doubt.
**Narrative:** The whispers crawl in — fear, doubt, the cold voice that says *fall*. The Knight remembers a name, an oath, a hand that once trusted them. The whispers burn. The armor hardens. The body locks. The Knight opens their eyes. The debuff is gone. The will is not. Only triggers when debuffed.

---

### 19. Titan's Strength
```python
{"id": "titans_strength", "name": "Titan's Strength", "cooldown": 5,
 "power_type": "buff", "trigger": "always",
 "self_status": "warded",
 "stat_mod": {"self": {"might": 5, "armor_bonus": 2}}, "mod_duration": 4}
```
**Description:** The Knight channels raw physical power, swelling muscle density and hardening bone.
**Narrative:** The Knight doesn't grow — they densify. The muscles compress, the bones thicken, the frame solidifies. The armor sits differently now — tighter, more integrated, like it was made for this exact moment. The might is not borrowed. It's earned. Four turns of this. The enemy will feel every one.

---

### 20. Ground Slam
```python
{"id": "ground_slam", "name": "Ground Slam", "cooldown": 4,
 "power_type": "strike", "damage_type": "physical", "trigger": "always",
 "status_apply": "stunned",
 "stat_mod": {"enemy": {"might": -3, "armor_bonus": -3}}, "mod_duration": 3}
```
**Description:** The Knight raises their weapon overhead and drives it into the earth, sending a shockwave through the ground.
**Narrative:** The Knight lifts the blade — or the shield, or the fist, it doesn't matter — and drives it down. The ground cracks. The shockwave travels. The enemy's feet leave the floor involuntarily. When they land, their stance is broken, their armor is rattled, and their might is shaking. The Knight is already standing. The ground is still trembling.

---

## Master Tier (Level 15, 1000g, 1hr) — 4 Buffs, 2 Strikes, 2 Defends

### 21. Iron Formation
```python
{"id": "iron_formation", "name": "Iron Formation", "cooldown": 6,
 "power_type": "defend", "trigger": "always",
 "self_status": "warded",
 "stat_mod": {"self": {"armor_bonus": 8, "durability": 4}}, "mod_duration": 4}
```
**Description:** The Knight lowers their stance and becomes an immovable fortress. Greatly increases personal defense.
**Narrative:** The Knight sinks into the earth like a root. Plate aligns with plate, muscle locks with bone, and the world pushes — and the world fails to move them. This is not a stance. This is a formation of one. The armor bonus is enormous. The durability is absolute. Four turns of immovable.

---

### 22. Royal Execution
```python
{"id": "royal_execution", "name": "Royal Execution", "cooldown": 5,
 "power_type": "strike", "damage_type": "physical", "trigger": "opponent_wounded",
 "status_apply": "bleeding",
 "stat_mod": {"enemy": {"might": -4, "armor_bonus": -3}}, "mod_duration": 3}
```
**Description:** The Knight calmly steps forward before delivering a single overwhelming strike worthy of an executioner.
**Narrative:** The enemy is bleeding, broken, swaying. The Knight walks forward — not fast, not slow — and raises the blade with the patience of a crown. One strike. All the stacked might behind a single edge. It is enough. Only triggers when the enemy is wounded.

---

### 23. Guardian's Oath
```python
{"id": "guardians_oath", "name": "Guardian's Oath", "cooldown": 6,
 "power_type": "buff", "trigger": "always",
 "self_status": "warded",
 "stat_mod": {"self": {"might": 4, "armor_bonus": 4, "durability": 3}}, "mod_duration": 4}
```
**Description:** The Knight speaks their Oath aloud, and the words themselves harden body, armor, and resolve. The strongest buff in the Knight's arsenal — amplifies whatever Oath is active.
**Narrative:** The Knight speaks — not a prayer, not a spell, but a promise. "While I stand, I hold." The words don't echo; they settle. Into the armor. Into the muscles. Into the bones. The Oath resonates with it. The might rises. The armor hardens. The durability deepens. Four turns. The enemy has four turns to reconsider.

---

### 24. Warlord's Fury
```python
{"id": "warlords_fury", "name": "Warlord's Fury", "cooldown": 6,
 "power_type": "buff", "trigger": "low_hp",
 "self_status": "warded",
 "stat_mod": {"self": {"might": 6, "armor_bonus": 3}}, "mod_duration": 4}
```
**Description:** Wounded and cornered, the Knight channels raw fury into a massive might surge. No healing — just rage.
**Narrative:** The Knight is bleeding. The enemy is closing in. And the Knight... smiles. Not happiness — recognition. The fury comes. Not hot, not blind, but cold and precise. The might surges — +6, the biggest single might buff in the Knight's arsenal. The armor sets. The Knight doesn't heal. The Knight doesn't need to. The enemy needs to survive the next four turns. Triggers when HP is low.

---

### 25. Crown of Iron
```python
{"id": "crown_of_iron", "name": "Crown of Iron", "cooldown": 6,
 "power_type": "buff", "trigger": "always",
 "self_status": "warded",
 "stat_mod": {"self": {"armor_bonus": 6, "might": 4, "durability": 3}}, "mod_duration": 4}
```
**Description:** The Knight assumes the stance of a ruler — armor maximized, might sharpened, endurance deepened. The capstone buff — with Oath stacks and this active, the Knight is a monument.
**Narrative:** The Knight doesn't wear a crown. They become one. The posture shifts — not aggressive, not defensive, but regal. The armor bonus is the highest in the basic rotation. The might is significant. The durability ensures they'll be here for a while. With the Oath stacking beneath this, the enemy isn't fighting a person. They're fighting a monument.

---

### 26. King's Command
```python
{"id": "kings_command", "name": "King's Command", "cooldown": 6,
 "power_type": "buff", "trigger": "always",
 "self_status": "warded",
 "stat_mod": {"self": {"might": 5, "armor_bonus": 3, "durability": 2}}, "mod_duration": 4}
```
**Description:** The Knight issues a command to themselves — a royal decree that empowers body and steel.
**Narrative:** The Knight speaks three words. Not to allies. Not to the enemy. To themselves. A decree. The body obeys — might surges, armor hardens, endurance deepens. The Knight is not asking. The Knight is not hoping. The Knight is commanding, and the Knight obeys. This is what self-reliance looks like at its peak.

---

### 27. Last Bastion
```python
{"id": "last_bastion", "name": "Last Bastion", "cooldown": 7,
 "power_type": "defend", "trigger": "low_hp",
 "self_status": "warded",
 "stat_mod": {"self": {"armor_bonus": 7, "durability": 5, "might": 3}}, "mod_duration": 4}
```
**Description:** Even while surrounded and wounded, the Knight refuses to fall. Armor, endurance, and might all surge.
**Narrative:** They're everywhere. The Knight doesn't count them anymore. Blood in their eyes, cracks in their shield, and still — still — they stand. The armor bonus is massive. The durability is enormous. The might ensures that falling isn't the only option — taking them down is. The enemy hesitates. They've seen this before. This is the one that doesn't stop. Triggers when HP is low.

---

### 28. Oath Strike
```python
{"id": "oath_strike", "name": "Oath Strike", "cooldown": 4,
 "power_type": "strike", "damage_type": "physical", "trigger": "always",
 "status_apply": "bleeding",
 "stat_mod": {"enemy": {"might": -3, "armor_bonus": -3, "grace": -2}}, "mod_duration": 3}
```
**Description:** The Knight channels every Oath stack and active buff into a single devastating blow. The longer the Oath has been held, the harder it hits.
**Narrative:** The Knight whispers the Oath as the blade descends — not for the enemy, but for the steel. The edge remembers every promise it has kept. Every Oath stack, every buff, every turn of commitment flows into this single strike. The might behind it is not just the Knight's — it's the accumulation of every stance, every command, every turn of faith. It keeps one more promise.

---

## Legendary Tier (Level 20, 2500g, 1 day — Quest-gated) — 2 Strikes

### 29. Final Duel
```python
{"id": "final_duel", "name": "Final Duel", "cooldown": 8,
 "power_type": "strike", "damage_type": "true", "trigger": "always",
 "status_apply": "bleeding",
 "stat_mod": {"enemy": {"might": -5, "grace": -5, "armor_bonus": -5}}, "mod_duration": 4}
```
**Description:** The Knight challenges one enemy to honorable single combat. True damage ignores all defense. Every Oath stack and active buff flows into this strike.
**Narrative:** The Knight lowers their blade and meets the enemy's eyes. "Just us." The world falls away — the battle, the noise, the blood. There is only the duel. The Knight advances, and every Oath stack they've accumulated — every stance, every buff, every turn of commitment — channels into the blade. The enemy knows, with the certainty of a closing door, that this is the last thing they will see. True damage. No defense. No negotiation.

**Quest: The Broken Oath**
- **Trainer:** Master Arden (Oathspire)
- **Min Level:** 20
- **Objectives:**
  - Kill 5 Ruin Ghouls in the Ashen Border
  - Gather 3 Relic Shards
  - Learn at least 5 Knight skills from Master Arden
- **Reward:** Unlocks Final Duel

---

### 30. Legend of Erchis
```python
{"id": "legend_of_erchis", "name": "Legend of Erchis", "cooldown": 10,
 "power_type": "strike", "damage_type": "true", "trigger": "low_hp",
 "status_apply": "stunned",
 "stat_mod": {"enemy": {"might": -6, "grace": -6, "armor_bonus": -8, "durability": -4}},
 "mod_duration": 5,
 "self_status": "warded"}
```
**Description:** The Knight channels every Oath ever sworn. A radiant armored spirit appears behind them as one final world-shaking strike decides the battle. Only usable when below 25% HP. True damage ignores all defense. All Oath stacks and buffs flow into this strike. Grants `warded`.
**Narrative:** The Knight is on one knee. Blood on the shield. Cracks in the plate. And then — light. Not from the sun. From the Oath itself. A figure of golden armor rises behind them, vast and silent, a ghost of every Knight who ever kept their word. The Knight rises with it. Every Oath stack they've accumulated, every buff they've cast, every turn they held the line — it all flows into the blade. The blade rises. The world holds its breath. And then the Knight strikes — true damage, absolute, final — and the world remembers why Knights exist. Triggers when HP is low.

**Quest: Legend of Erchis**
- **Trainer:** Master Arden (Oathspire)
- **Min Level:** 20
- **Objectives:**
  - Complete "The Broken Oath" quest (learn Final Duel first)
  - Kill 1 Heritage Boss
  - Gather 1 Jahra Ingot
  - Learn at least 15 Knight skills total
- **Reward:** Unlocks Legend of Erchis
