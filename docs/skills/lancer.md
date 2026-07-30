# Lancer Mastery — 30 Skills + 10 Passives

**Role:** The Elemental Lance Master — a melee fighter who imbues their lance with elemental buffs, each changing what their strikes do. The more elements stacked, the more versatile and devastating the combination. Inspired by the Force Blader archetype.
**Masteries per trainer:** 3 (Lancer + 2 others)
**Trainers teaching Lancer:** Oathspire, Warforge, Jahrahold

---

## Lancer Identity

**Knight:** "The more I buff, the harder I hit."
**Paladin:** "The more you hurt me, the harder I am to kill."
**Lancer:** "The more elements I stack, the more versatile I kill."

**Core loop:** Imbue lance with element → stack multiple elements → strikes carry elemental riders → adapt to enemy weaknesses → execute

- **Elemental imbue system** — Lancer buffs themself with elemental imbues. Each element changes what strikes do: fire burns, ice slows, lightning stuns, earth shatters, wind evades, thunder shocks.
- **Stack and combine** — multiple elements can be active simultaneously. Stack Fire + Earth for burning + armor pen, or Ice + Lightning for slow + stun. The more elements, the more devastating.
- **Strikes are physical** — elements add effects ON TOP of the physical hit, not replace it. Thunder imbue adds magical damage, but the spear still pierces.
- **Combo-driven** — Lancer gets stronger as the fight goes on, building elemental stacks that increase crit chance and damage.
- **Glass cannon tendencies** — less defensive than Knight/Paladin. Some evasion from Wind imbue, but not a tank. Kill them before they kill you.

### The Elemental System

| Element | Imbue Name | Effect on Strikes | Status Applied |
|---------|-----------|-------------------|----------------|
| **Fire** | Flame Imbue | Bonus physical damage, might boost | `burning` |
| **Ice** | Frost Imbue | Slows enemy, reduces grace, armor boost | `ensnared` |
| **Lightning** | Storm Imbue | Stun chance, might + grace boost | `stunned` |
| **Earth** | Stone Imbue | Armor penetration, might + armor boost | `shaken` |
| **Wind** | Gale Imbue | Accuracy/crit boost, evasion | `evasive` (self) |
| **Thunder** | Thunder Imbue | Bonus magical damage, insight boost | `shaken` |

### Stat Focus

| Stat | Priority | Why |
|------|----------|-----|
| `grace` | **Primary** | Accuracy + crit — Lancer needs to hit to apply elemental effects |
| `might` | **Primary** | Physical strike scaling — the base damage of every hit |
| `insight` | **Secondary** | Magical damage for Thunder imbue and magical strikes |
| `armor_bonus` | **Secondary** | Light defensive capability — not a tank |
| `essence` | **Minimal** | Some magic resist for survival |
| `durability` | **Minimal** | Not a tank |
| `cognition` | **None** | Not utility-focused |

### Status Identity

| Status | Source | Role |
|--------|--------|------|
| `burning` | Fire imbue | DoT rider on strikes |
| `ensnared` | Ice imbue | Slow + freeze, reduces enemy mobility |
| `stunned` | Lightning imbue / strikes | Control |
| `shaken` | Earth/Thunder imbue | Armor/magic resist reduction |
| `evasive` | Wind imbue (self) | Accuracy/crit/evasion boost |
| `bleeding` | Physical strikes | Some strikes cause bleeding |
| `warded` | **None** | Lancer doesn't ward — that's Paladin |
| `inspired` | **None** | Lancer doesn't inspire |
| `hidden` | **None** | Lancer doesn't stealth |

### Trigger Identity

| Trigger | Role |
|---------|------|
| `always` | **Primary** — standard imbues and strikes |
| `opening_move` | **Secondary** — charge attacks, first-strike imbues |
| `opponent_wounded` | **Secondary** — execute-style elemental strikes |
| `low_hp` | **Rare** — desperate last strikes |
| `opponent_status` | **Rare** — elemental exploit strikes |

### What the Lancer Does NOT Do

- **No healing** — pure offensive, no `heal_percent`
- **No `warded`** — not a tank, that's Paladin's signature
- **No `inspired`** — not a buffer, that's Bard/Paladin
- **No heavy armor stacking** — that's Knight
- **No inverse HP scaling** — that's Paladin
- **No stealth/poison** — that's Assassin/Rogue
- **No multi-hit > 2** — one multi-hit skill (thrust + sweep combo), rest are single hit

### How Lancer Differs from the Other Melees

| Aspect | Knight | Paladin | Lancer |
|--------|--------|---------|--------|
| Buff type | Armor + Might | Armor + Essence + Durability | **Elemental imbues** |
| Buff purpose | Ramp up power | Survive longer | **Change what strikes do** |
| Damage | Physical only | Physical + Magical (holy) | Physical + **elemental riders** |
| Status | Stun, shaken | Stun, shaken, blinded | **Burning, ensnared, stunned, shaken, evasive** |
| Playstyle | Stack → smash | Get hurt → endure | **Imbue → adapt → strike** |
| Stat focus | Armor + Might | Armor + Essence | **Grace + Might + Insight** |
| Versatility | Low (one mode) | Low (one mode) | **High (6 elements, mix and match)** |

---

## Passives — Auto-Learned, Unlocked Every 10 Levels

| # | Name | Level | Effect |
|---|------|-------|--------|
| 1 | Elemental Initiation | 10 | Start every combat with one random elemental imbue active |
| 2 | Lingering Elements | 20 | Elemental buffs last +1 turn longer than listed |
| 3 | Elemental Harmony | 30 | When 2+ elements are active, strikes deal +10% bonus damage |
| 4 | Critical Imbue | 40 | While any elemental imbue is active, +10% crit chance |
| 5 | Elemental Mastery | 50 | All elemental imbue stat_mods increased by +1 |
| 6 | Elemental Cascade | 60 | When an elemental buff expires, 50% chance to auto-apply a different element |
| 7 | Storm Rider | 70 | While Lightning imbue is active, +15% damage on all strikes |
| 8 | Elemental Fusion | 80 | When 3+ elements are active, strikes deal +25% bonus damage and apply 2 statuses |
| 9 | Elemental Overload | 90 | Once per combat, can activate all 6 elements simultaneously for 2 turns |
| 10 | Avatar of Elements | 100 | All elemental imbue durations increased by +3 turns. Elemental Overload (passive 9) can be used twice per combat instead of once. When all 6 elements are active, strikes deal +10% bonus damage. |

### Passive Synergy

```
Level 10:  Free opening element → immediate imbue
Level 20:  Elements last longer → more uptime
Level 30:  2+ elements = +10% damage → reward stacking
Level 40:  Any imbue = +10% crit → Lancer hits harder
Level 50:  All imbues stronger → every element hits harder
Level 60:  Expired buffs auto-replace → seamless rotation
Level 70:  Lightning active = +15% damage → Storm Rider shines
Level 80:  3+ elements = +25% damage + 2 statuses → fusion devastation
Level 90:  All 6 elements at once for 2 turns → overload burst
Level 100: Imbues last +3 turns, Overload twice per combat, 6-element bonus → the Lancer is a walking storm
```

**The full build at level 100:**
- All imbue durations +3 turns (longer uptime, not permanent)
- Elemental Overload usable twice per combat (all 6 elements for 2 turns, twice)
- +25% damage from Elemental Fusion (3+ elements)
- +10% damage from Elemental Harmony (2+ elements)
- +10% crit from Critical Imbue
- +15% damage from Storm Rider (Lightning active)
- +10% bonus damage when all 6 elements active
- The Lancer is a one-person elemental storm

---

## Skill Structure

All skills use the new format — no `power` or `skill_capacity_cost`.

| Field | Description |
|-------|-------------|
| `power_type` | strike, defend, debuff, buff |
| `damage_type` | physical, magical, true (strikes only) |
| `trigger` | always, low_hp, opponent_wounded, opponent_status, opening_move, self_debuff |
| `status_apply` | Status inflicted on enemy |
| `self_status` | Status applied to self (Lancer uses `evasive` for wind imbues, none for others) |
| `stat_mod` | Temporary stat changes — `{"self": {...}, "enemy": {...}}` |
| `mod_duration` | How many turns stat_mod lasts |
| `hits` | Number of hits per use (default 1, max 2 for Lancer) |

**Lancer rules:** No `heal_percent`. No `warded` or `inspired` self_status. No `hits` > 2. Imbues are `buff` power_type with elemental stat_mods. Strikes are physical unless marked magical. Buffs focus on `grace`, `might`, and `insight` — NOT `armor_bonus`/`essence`/`durability` (that's Knight/Paladin).

---

## Tier Overview

| Tier | Level Req | Gold Cost | Learn Time | Count | Imbues | Strikes | Defends | Debuffs | Buffs | Legendary |
|------|-----------|-----------|------------|-------|--------|---------|---------|---------|-------|-----------|
| Basic | 1 | 50g | 5 min | 6 | 2 | 2 | 1 | 0 | 1 | 0 |
| Advanced | 3 | 150g | 30 min | 7 | 2 | 3 | 0 | 1 | 1 | 0 |
| Expert | 8 | 400g | 1 hr | 7 | 2 | 1 | 1 | 2 | 1 | 0 |
| Master | 15 | 1000g | 1 hr | 8 | 4 | 3 | 0 | 1 | 0 | 0 |
| Legendary | 20 | 2500g | 1 day | 2 | 0 | 0 | 0 | 0 | 0 | 2 |
| **Total** | | | | **30** | **10** | **9** | **2** | **4** | **3** | **2** |

---

## Basic Tier (Level 1, 50g, 5min) — 2 Imbues, 2 Strikes, 1 Defend, 1 Buff

### 1. Flame Imbue
```python
{"id": "flame_imbue", "name": "Flame Imbue", "cooldown": 3,
 "power_type": "buff", "trigger": "always",
 "stat_mod": {"self": {"might": 2}}, "mod_duration": 3}
```
**Description:** The Lancer ignites their lance with fire elemental energy. While active, strikes deal bonus physical damage and apply `burning`.
**Narrative:** The Lancer runs a hand along the spear shaft. Where the fingers pass, metal glows — cherry red, then orange, then white. The air shimmers. The spear hums with heat. The next thing it touches will remember what fire is.

---

### 2. Frost Imbue
```python
{"id": "frost_imbue", "name": "Frost Imbue", "cooldown": 3,
 "power_type": "buff", "trigger": "always",
 "stat_mod": {"self": {"might": 2, "grace": 1}, "enemy": {"grace": -2}}, "mod_duration": 3}
```
**Description:** The Lancer encases their lance in ice elemental energy. While active, strikes slow the enemy and apply `ensnared`.
**Narrative:** The Lancer breathes on the spear. The breath is cold — not winter cold, but something older. Frost crawls along the shaft, crystallizes at the tip. The air around the weapon stills. The next thing it touches will forget how to move.

---

### 3. Gale Thrust
```python
{"id": "gale_thrust", "name": "Gale Thrust", "cooldown": 1,
 "power_type": "strike", "damage_type": "physical", "trigger": "always",
 "stat_mod": {"enemy": {"grace": -1}}, "mod_duration": 2}
```
**Description:** A lightning-fast thrust where wind spirals around the spear as the Lancer darts through the enemy. Carries any active elemental effects.
**Narrative:** The spear is a blur — not because it's fast, but because the Lancer is already past. Wind trails the shaft like a ghost. The enemy feels the cut before they see the move. If the lance is imbued, they feel that too.

---

### 4. Guard Break
```python
{"id": "guard_break", "name": "Guard Break", "cooldown": 3,
 "power_type": "strike", "damage_type": "physical", "trigger": "always",
 "stat_mod": {"enemy": {"armor_bonus": -3}}, "mod_duration": 2}
```
**Description:** A precise thrust that slips through shields and shatters enemy defenses. Carries any active elemental effects.
**Narrative:** The enemy's shield is a wall. The Lancer doesn't aim at it — they aim at the gap, the weld, the inch that was never quite perfect. The spear finds it. The wall becomes a door. And through the door comes fire, or ice, or lightning — whatever the Lancer brought.

---

### 5. Cyclone Wall
```python
{"id": "cyclone_wall", "name": "Cyclone Wall", "cooldown": 3,
 "power_type": "defend", "trigger": "always",
 "self_status": "evasive",
 "stat_mod": {"self": {"grace": 2}}, "mod_duration": 2}
```
**Description:** Rapid spinning of the spear deflects projectiles and redirects arrows aside. Grants evasion.
**Narrative:** The arrows come — three, five, seven. The Lancer spins the spear like a staff, and the shaft becomes a blur. Wood and steel meet arrow and bone. Every shaft splinters. The Lancer doesn't even look up.

---

### 6. Warrior's Focus
```python
{"id": "warriors_focus", "name": "Warrior's Focus", "cooldown": 3,
 "power_type": "buff", "trigger": "always",
 "stat_mod": {"self": {"grace": 2, "might": 2}}, "mod_duration": 3}
```
**Description:** The Lancer centers themself, balancing grace and power. A foundational buff that enhances both accuracy and strike damage.
**Narrative:** The Lancer plants the spear and breathes. Not a battle cry, not a prayer — just a breath. The kind that comes before everything else. When they open their eyes, the world is slower. The spear is lighter. The enemy is closer than they want to be.

---

## Advanced Tier (Level 3, 150g, 30min) — 2 Imbues, 3 Strikes, 1 Debuff, 1 Buff

### 7. Storm Imbue
```python
{"id": "storm_imbue", "name": "Storm Imbue", "cooldown": 4,
 "power_type": "buff", "trigger": "always",
 "stat_mod": {"self": {"might": 3, "grace": 2}}, "mod_duration": 3}
```
**Description:** The Lancer calls lightning into their lance. While active, strikes have a stun chance and apply `stunned`.
**Narrative:** The Lancer raises the spear to the sky. The sky grumbles. Then it agrees. Lightning crawls down the shaft — not striking, but settling, coiling, waiting. The spear hums with it. The next thrust will carry the storm.

---

### 8. Stone Imbue
```python
{"id": "stone_imbue", "name": "Stone Imbue", "cooldown": 4,
 "power_type": "buff", "trigger": "always",
 "stat_mod": {"self": {"might": 3, "armor_bonus": 2}, "enemy": {"armor_bonus": -2}}, "mod_duration": 3}
```
**Description:** The Lancer reinforces their lance with earth elemental energy. While active, strikes penetrate armor and apply `shaken`.
**Narrative:** The Lancer drives the butt of the spear into the ground. The earth trembles — not much, just enough. When they raise it, the shaft is heavier, denser, as if the stone climbed inside. The next thing it hits won't just bleed. It will crack.

---

### 9. Sky Piercer
```python
{"id": "sky_piercer", "name": "Sky Piercer", "cooldown": 3,
 "power_type": "strike", "damage_type": "physical", "trigger": "always",
 "status_apply": "bleeding",
 "stat_mod": {"enemy": {"armor_bonus": -4}}, "mod_duration": 3}
```
**Description:** The Lancer lowers their spear before exploding forward in a blur, the tip tearing through armor like paper. Carries any active elemental effects.
**Narrative:** The Lancer folds low — knees bent, spear tucked — and then unfolds like a spring uncoiling. The spear hits armor and doesn't slow. It goes through. Through plate, through padding, through the confidence of everyone watching. And through it all, fire burns, or ice freezes, or lightning arcs — whatever the Lancer carries, the enemy receives.

---

### 10. Falcon Rush
```python
{"id": "falcon_rush", "name": "Falcon Rush", "cooldown": 3,
 "power_type": "strike", "damage_type": "physical", "trigger": "opening_move",
 "status_apply": "stunned",
 "stat_mod": {"enemy": {"grace": -2}}, "mod_duration": 2}
```
**Description:** The Lancer moves as swiftly as a hunting falcon, closing the distance and striking before the enemy can react. Opening move only. Carries any active elemental effects.
**Narrative:** The enemy blinks. The Lancer is gone. Not hidden — just fast. By the time the enemy's eyes open, the spear is already in their ribs and the Lancer is already pulling it free. Opening moves don't get a second chance. And neither does the element riding the blade.

---

### 11. Dragon Fang
```python
{"id": "dragon_fang", "name": "Dragon Fang", "cooldown": 4,
 "power_type": "strike", "damage_type": "physical", "trigger": "always",
 "status_apply": "bleeding",
 "stat_mod": {"enemy": {"armor_bonus": -3, "might": -2}}, "mod_duration": 3}
```
**Description:** A brutal armor-piercing stab that sinks the spear deep into the target, leaving them wounded and weakened. Carries any active elemental effects.
**Narrative:** The Lancer commits — full body, full weight, full reach. The spear sinks to the crossguard. The enemy's eyes go wide. When the Lancer pulls free, something comes with it — not just blood, but the enemy's certainty that they'll walk away from this. And the element that rode the blade stays behind, burning or freezing or shocking where the wound is.

---

### 12. Elemental Weakness
```python
{"id": "elemental_weakness", "name": "Elemental Weakness", "cooldown": 4,
 "power_type": "debuff", "damage_type": "magical", "trigger": "always",
 "stat_mod": {"enemy": {"might": -3, "grace": -3, "armor_bonus": -2}}, "mod_duration": 3}
```
**Description:** The Lancer exploits gaps in the enemy's defenses, exposing them to all elemental effects. Reduces might, grace, and armor simultaneously.
**Narrative:** The Lancer doesn't strike — they probe. The spear tip taps armor, tests joints, finds the gaps. Each tap leaves a mark — not a wound, but a weakness. The enemy feels heavier, slower, more vulnerable. They are. The elements are coming, and they'll find the door already open.

---

### 13. Battle Readiness
```python
{"id": "battle_readiness", "name": "Battle Readiness", "cooldown": 4,
 "power_type": "buff", "trigger": "opening_move",
 "self_status": "evasive",
 "stat_mod": {"self": {"grace": 3, "might": 2}}, "mod_duration": 3}
```
**Description:** The Lancer enters combat with heightened awareness and reflexes. Boosts accuracy and damage while granting evasion. Opening move only.
**Narrative:** The Lancer settles into the stance — feet apart, spear angled, weight centered. It's not a pose. It's a decision. The kind that says *I am ready for whatever comes next*. The enemy comes next. The Lancer is ready.

---

## Expert Tier (Level 8, 400g, 1hr) — 2 Imbues, 1 Strike, 1 Defend, 2 Debuffs, 1 Buff

### 14. Gale Imbue
```python
{"id": "gale_imbue", "name": "Gale Imbue", "cooldown": 4,
 "power_type": "buff", "trigger": "always",
 "self_status": "evasive",
 "stat_mod": {"self": {"grace": 4, "might": 2}}, "mod_duration": 3}
```
**Description:** The Lancer wraps their lance in wind elemental energy. While active, strikes gain accuracy and crit chance, and the Lancer becomes `evasive`.
**Narrative:** The Lancer swings the spear in a wide arc, and the wind doesn't resist — it follows. Air spirals around the shaft, around the arm, around the Lancer themself. They become harder to see, harder to hit, harder to predict. The next thrust won't just land — it will land exactly where it needs to.

---

### 15. Thunder Imbue
```python
{"id": "thunder_imbue", "name": "Thunder Imbue", "cooldown": 5,
 "power_type": "buff", "trigger": "always",
 "stat_mod": {"self": {"insight": 4, "might": 2}, "enemy": {"essence": -2}}, "mod_duration": 3}
```
**Description:** The Lancer channels thunder into their lance, adding magical damage to strikes. While active, strikes deal bonus magical damage and apply `shaken`.
**Narrative:** This is not lightning. Lightning is fast, bright, and done. Thunder is the voice that comes after — the sound that shakes the walls and reminds everyone who is in charge. The Lancer's spear doesn't crackle. It *hums*. Deep. Low. The kind of sound that makes armor vibrate and courage falter.

---

### 16. Dragon Dive
```python
{"id": "dragon_dive", "name": "Dragon Dive", "cooldown": 4,
 "power_type": "strike", "damage_type": "physical", "trigger": "opening_move",
 "status_apply": "stunned",
 "stat_mod": {"enemy": {"armor_bonus": -4, "might": -2}}, "mod_duration": 2}
```
**Description:** The Lancer vaults skyward before descending like a falling dragon, crashing down with devastating force. Opening move only. Carries any active elemental effects.
**Narrative:** The Lancer doesn't jump — they launch. For a moment, they're above the battlefield, silhouetted against the sky, spear pointed down. Then gravity and intent pull them back. The impact cracks the earth. The enemy doesn't stand. And every element the Lancer carried comes crashing down with them — fire, ice, lightning, all at once, all in one point.

---

### 17. Frostbite
```python
{"id": "frostbite", "name": "Frostbite", "cooldown": 4,
 "power_type": "debuff", "damage_type": "magical", "trigger": "opponent_status",
 "status_apply": "ensnared",
 "stat_mod": {"enemy": {"grace": -4, "might": -3}}, "mod_duration": 3}
```
**Description:** The Lancer exploits an already-statused enemy, driving ice energy into their wounds. Freezes them in place and devastates grace and might. Only triggers when enemy has a status effect.
**Narrative:** The enemy is already hurting — burning, bleeding, something. Good. The Lancer touches the wound with the spear tip and pushes cold through it. Not surface cold — deep cold, the kind that reaches bones and stays. The enemy seizes. Their joints lock. Their muscles forget how to fire. They are not dead. They are just not moving.

---

### 18. Shock Lock
```python
{"id": "shock_lock", "name": "Shock Lock", "cooldown": 4,
 "power_type": "debuff", "damage_type": "magical", "trigger": "opponent_status",
 "status_apply": "stunned",
 "stat_mod": {"enemy": {"might": -4, "grace": -3}}, "mod_duration": 3}
```
**Description:** The Lancer channels lightning into an already-statused enemy's wounds, locking their muscles with electrical overload. Stuns and devastates might and grace. Only triggers when enemy has a status effect.
**Narrative:** The enemy is wounded. The Lancer doesn't let wounds heal — they make them worse. The spear tip finds the existing wound and sends a jolt through it. Not enough to kill. Enough to seize. The enemy's body locks — arms rigid, legs straight, eyes wide. They are a statue that knows it's about to be broken.

---

### 19. Iron Breeze
```python
{"id": "iron_breeze", "name": "Iron Breeze", "cooldown": 4,
 "power_type": "defend", "trigger": "always",
 "self_status": "evasive",
 "stat_mod": {"self": {"grace": 3, "armor_bonus": 2}}, "mod_duration": 2}
```
**Description:** The Lancer weaves wind and steel into a defensive pattern, deflecting blows while maintaining mobility. Grants evasion and light armor.
**Narrative:** The enemy swings. The Lancer isn't there — not because they dodged, but because the wind moved them. The spear deflects, the body shifts, the feet glide. It looks like a dance. It is a dance — one where the Lancer leads and the enemy keeps stepping on their own feet.

---

### 20. Elemental Surge
```python
{"id": "elemental_surge", "name": "Elemental Surge", "cooldown": 5,
 "power_type": "buff", "trigger": "always",
 "self_status": "evasive",
 "stat_mod": {"self": {"grace": 3, "insight": 3, "might": 2}}, "mod_duration": 3}
```
**Description:** The Lancer surges all active elemental energy to maximum intensity. Boosts grace, insight, and might simultaneously while granting evasion.
**Narrative:** The Lancer closes their eyes for half a second. When they open them, every element flares — fire burns hotter, ice freezes deeper, lightning cracks louder. The spear becomes a prism, every color of destruction visible at once. The Lancer doesn't just carry the elements now. They command them.

---

## Master Tier (Level 15, 1000g, 1hr) — 4 Imbues, 3 Strikes, 1 Debuff

### 21. Inferno Imbue
```python
{"id": "inferno_imbue", "name": "Inferno Imbue", "cooldown": 5,
 "power_type": "buff", "trigger": "always",
 "stat_mod": {"self": {"might": 5, "grace": 2}, "enemy": {"armor_bonus": -3}}, "mod_duration": 4}
```
**Description:** An advanced fire imbue that engulfs the lance in roaring flames. While active, strikes deal massive bonus physical damage and apply `burning`. Reduces enemy armor.
**Narrative:** The basic flame was a candle. This is a bonfire. The Lancer doesn't run a hand along the shaft — they will the fire into being, and the spear becomes a brand. The air around it distorts. The ground beneath it chars. The enemy can feel the heat from across the battlefield. They will feel much more when it arrives.

---

### 22. Glacier Imbue
```python
{"id": "glacier_imbue", "name": "Glacier Imbue", "cooldown": 5,
 "power_type": "buff", "trigger": "always",
 "stat_mod": {"self": {"might": 4, "grace": 3}, "enemy": {"grace": -4, "might": -2}}, "mod_duration": 4}
```
**Description:** An advanced ice imbue that encases the lance in a glacier's heart. While active, strikes freeze deep and apply `ensnared`. Devastates enemy grace and might.
**Narrative:** The frost imbue was a coating. This is a glacier. The spear isn't cold — it is *cold itself*, the concept made metal. Ice crystallizes in the air around it, falls as snow, settles on the enemy's shoulders like a warning. When the spear strikes, the freeze doesn't stop at the skin. It reaches the marrow. The enemy's next breath comes out as fog, and the one after that doesn't come at all.

---

### 23. Tempest Imbue
```python
{"id": "tempest_imbue", "name": "Tempest Imbue", "cooldown": 5,
 "power_type": "buff", "trigger": "always",
 "stat_mod": {"self": {"might": 5, "grace": 3}, "enemy": {"might": -3, "grace": -3}}, "mod_duration": 4}
```
**Description:** An advanced lightning imbue that turns the lance into a storm conductor. While active, strikes carry devastating electrical force and apply `stunned`. Reduces enemy might and grace.
**Narrative:** The storm imbue was a spark. This is the whole sky. Lightning doesn't crawl down the shaft — it lives in it, coils around it, breathes through it. The spear crackles continuously, and each crack sounds like a warning the enemy should have heeded. When the thrust lands, the thunder comes first. Then the pain. Then the silence.

---

### 24. Volcano Imbue
```python
{"id": "volcano_imbue", "name": "Volcano Imbue", "cooldown": 6,
 "power_type": "buff", "trigger": "always",
 "stat_mod": {"self": {"might": 5, "armor_bonus": 3}, "enemy": {"armor_bonus": -4, "might": -3}}, "mod_duration": 4}
```
**Description:** A combo imbue fusing fire and earth. The lance becomes a volcanic force — molten core, stone shell. While active, strikes apply both `burning` and `shaken`. Massive armor penetration and might boost.
**Narrative:** The Lancer drives the spear into the earth and wills two elements at once — fire below, stone above. The shaft glows red, then hardens to black. It is magma made solid, a volcano compressed to a weapon. The enemy sees the heat shimmer and the stone weight and understands, too late, that they are about to be buried and burned at the same time.

---

### 25. Thunder Pursuit
```python
{"id": "thunder_pursuit", "name": "Thunder Pursuit", "cooldown": 4,
 "power_type": "strike", "damage_type": "magical", "trigger": "opponent_wounded",
 "status_apply": "stunned",
 "stat_mod": {"enemy": {"grace": -3, "might": -3}}, "mod_duration": 3}
```
**Description:** Lightning follows each step as the Lancer chases fleeing enemies with thunderous pursuit. Only triggers when the enemy is wounded. Carries any active elemental effects.
**Narrative:** The enemy runs. The Lancer follows — not running, but hunting. Each step cracks with thunder, each stride closes the gap. The enemy looks back and sees lightning wearing a face. They don't look back again. And every element the Lancer carries rides the bolt — fire that burns through the wound, ice that freezes the blood, stone that cracks the bone.

---

### 26. World Splitter
```python
{"id": "world_splitter", "name": "World Splitter", "cooldown": 6,
 "power_type": "strike", "damage_type": "physical", "trigger": "opponent_wounded",
 "status_apply": "stunned",
 "stat_mod": {"enemy": {"armor_bonus": -6, "might": -3}}, "mod_duration": 3}
```
**Description:** The Lancer splits the ground with one thrust. The earth cracks beneath the spear, devastating the enemy's footing and defenses. Only triggers when the enemy is wounded. Carries any active elemental effects.
**Narrative:** The Lancer drives the spear down — not at the enemy, but at the world. The ground splits. The crack runs forward, fast, hungry, and the enemy is standing on the wrong side of it. When it reaches them, the earth opens. The enemy falls. The spear is waiting at the bottom — and it brings fire, ice, lightning, everything the Lancer has loaded into it, all at once, all into the wound the earth already made.

---

### 27. Crimson Spear
```python
{"id": "crimson_spear", "name": "Crimson Spear", "cooldown": 5,
 "power_type": "strike", "damage_type": "physical", "trigger": "low_hp",
 "status_apply": "bleeding",
 "stat_mod": {"self": {"might": 5}, "enemy": {"armor_bonus": -4, "might": -3}},
 "mod_duration": 3}
```
**Description:** The spear glows blood red as the Lancer channels desperation into devastating power. Only usable when HP is low. Carries any active elemental effects.
**Narrative:** The Lancer is bleeding — their own blood, not the enemy's. They should be falling. Instead, the spear begins to glow. Red. Deep. Hungry. The Lancer grins through the pain and whispers to the weapon: "Take what you need." The spear does. The enemy pays for it. And every element riding the blade flares crimson — red fire, red ice, red lightning — as if the blood itself is fuel.

---

### 28. Elemental Collapse
```python
{"id": "elemental_collapse", "name": "Elemental Collapse", "cooldown": 6,
 "power_type": "debuff", "damage_type": "magical", "trigger": "opponent_wounded",
 "stat_mod": {"enemy": {"might": -5, "grace": -5, "armor_bonus": -4, "essence": -3}}, "mod_duration": 4}
```
**Description:** The Lancer detonates all active elemental energy inside the enemy's wounds at once, causing a catastrophic collapse of their defenses. Devastates all stats. Only triggers when the enemy is wounded.
**Narrative:** The enemy is wounded — burning, frozen, shocked, shaking. The Lancer sees all of it and makes a decision. They snap their fingers. Every element inside the enemy's wounds detonates at once — fire feeds ice, ice feeds lightning, lightning feeds stone, stone feeds fire. The chain reaction is silent. The enemy's collapse is not. They fold. They don't get back up. Not for a while.

---

## Legendary Tier (Level 20, 2500g, 1 day — Quest-gated) — 2 True-Damage Strikes

### 29. Celestial Javelin
```python
{"id": "celestial_javelin", "name": "Celestial Javelin", "cooldown": 8,
 "power_type": "strike", "damage_type": "true", "trigger": "always",
 "status_apply": "bleeding",
 "stat_mod": {"enemy": {"might": -5, "grace": -5, "armor_bonus": -6}}, "mod_duration": 4}
```
**Description:** The Lancer throws a divine spear of pure elemental light. A radiant lance descends from the heavens, piercing all defenses with true damage. Carries ALL active elemental effects simultaneously. True damage ignores all defense.
**Narrative:** The Lancer draws back — not the physical spear, but something deeper. They pull from the sky itself, from the space between stars, and what forms in their hand is not metal. It is light, condensed into a shape that remembers what a spear is. And every element the Lancer has ever known pours into it — fire and ice, lightning and stone, wind and thunder — all of them, all at once, compressed into a single throw. The air doesn't resist. The armor doesn't matter. The enemy doesn't get to matter. The javelin arrives, and it goes through everything — steel, bone, shadow, doubt — and keeps going. What remains is not a wound. It is a convergence of every way to die.

**Quest: The Spear That Pierced Heaven**
- **Trainer:** Thazka Emberhand (Warforge)
- **Min Level:** 20
- **Objectives:**
  - Kill 5 Iron Scar creatures in Mushkara
  - Gather 3 Relic Shards
  - Learn at least 5 Lancer skills from Thazka Emberhand
- **Reward:** Unlocks Celestial Javelin

---

### 30. Avatar of the Storm
```python
{"id": "avatar_of_the_storm", "name": "Avatar of the Storm", "cooldown": 10,
 "power_type": "strike", "damage_type": "true", "trigger": "low_hp",
 "status_apply": "stunned",
 "stat_mod": {"enemy": {"might": -6, "grace": -6, "armor_bonus": -8, "essence": -4}},
 "mod_duration": 5,
 "self_status": "evasive"}
```
**Description:** The Lancer becomes one with all elements simultaneously — fire, ice, lightning, stone, wind, and thunder fuse into a single impossible state. A devastating true-damage strike that applies every elemental status at once. True damage ignores all defense. Only usable when below 25% HP.
**Narrative:** The Lancer is broken — armor cracked, spear splintered, blood on the shaft. They should fall. Instead, they close their eyes. And in the darkness behind their lids, they feel them — all six elements, every imbue they've ever learned, every element they've ever carried. They don't choose one. They choose all of them. The spear reforms — not steel, not light, but something that is both and neither. Fire burns along the shaft. Ice crystallizes at the tip. Lightning coils around the blade. Stone hardens the grip. Wind spirals around the Lancer's body. Thunder hums in the air. The Lancer opens their eyes. They are not a warrior anymore. They are a storm wearing a face. The enemy sees the Lancer step forward and knows, with the certainty of a closing door, that they are about to learn what every element feels like at once.

**Quest: Avatar of the Storm**
- **Trainer:** Thazka Emberhand (Warforge)
- **Min Level:** 20
- **Objectives:**
  - Complete "The Spear That Pierced Heaven" quest (learn Celestial Javelin first)
  - Kill 1 Heritage Boss
  - Gather 1 Jahra Ingot
  - Learn at least 15 Lancer skills total
- **Reward:** Unlocks Avatar of the Storm
