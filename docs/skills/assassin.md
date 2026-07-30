# Assassin Mastery — 30 Skills + 10 Passives

**Role:** The Shadow Reaper — a burst-damage glass cannon who accumulates shadows through kills and combat, then unleashes them in a devastating burst at 100. Shadows also weaken enemies through fear, and the Assassin is strongest at night.
**Masteries per trainer:** 3 (Assassin + 2 others)
**Trainers teaching Assassin:** Deepstone, Starfall Watch, Beastcairn, Veilgrove

---

## Assassin Identity

**Knight:** "The more I buff, the harder I hit."
**Paladin:** "The more you hurt me, the harder I am to kill."
**Lancer:** "The more elements I stack, the more versatile I kill."
**Assassin:** "The more shadows I collect, the closer you are to death."

**Core loop:** Kill enemies → accumulate shadows → deposit fear on targets → reclaim shadows on kill → reach 100 → BURST → reset → repeat

- **Shadow accumulation** — Shadows are a persistent resource (0-100) visible on the Assassin's status. Kills, critical hits, and stealth breaks all generate shadows. The more shadows, the higher the damage, crit, and accuracy.
- **Shadow as fear** — When the Assassin targets an enemy, they deposit shadows as fear, reducing that enemy's stats. If the enemy dies, the Assassin reclaims all deposited shadows plus the kill bonus. Risk vs reward: deposit weakens the enemy but temporarily lowers the Assassin's own shadow count.
- **BURST at 100** — When shadows reach 100, the next skill deals 3x damage, guaranteed crit, and ignores 70% of target armor. Then shadows reset to 0. The cycle begins again.
- **Night power** — During night, the Assassin gains passive shadow generation, stronger shadow thresholds, and enhanced stealth. The night belongs to the Assassin.
- **Stealth = 100% evasion** — While `hidden`, the Assassin cannot be hit. Stealth breaks on attack, but the breaking strike is a guaranteed crit with bonus shadow gain.
- **Glass cannon** — No healing, no tanking, no buffing allies. Pure offense. Kill them before they kill you.

### The Shadow System

**Shadow Generation:**

| Source | Shadows Gained |
|--------|---------------|
| Kill an enemy | +10 base (+ reclaim all deposited fear) |
| Stealth break (attack from hidden) | +15 |
| Critical hit | +5 |
| Each turn (night only) | +3 |
| Opening from stealth | +10 |

**Shadow Thresholds:**

| Shadows | Damage Bonus | Crit Bonus | Accuracy Bonus |
|---------|-------------|------------|----------------|
| 0-24 | +5% | +5% | +0% |
| 25-49 | +10% | +10% | +5% |
| 50-74 | +20% | +15% | +10% |
| 75-99 | +30% | +20% | +15% |
| **100** | **BURST: 3x damage, guaranteed crit, ignores 70% of target armor. Resets to 0.** |

**Fear Deposit (Debuff on Enemy):**

- Each shadow deposited reduces enemy main stats (might, grace, insight) by -1 per shadow
- Fear stacks — the more you target one enemy, the more fear accumulates
- Reclaim on kill — all deposited shadows return to the Assassin + kill bonus
- At 75+ shadows (Shadow Convergence passive), fear deposits cost no shadows

**Night Bonuses:**

- Passive shadow generation: +3/turn (increases with passives)
- Shadow threshold effects doubled
- Stealth lasts longer, harder to break
- Fear deposits are stronger

### Stat Focus

| Stat | Priority | Why |
|------|----------|-----|
| `grace` | **Primary** | Crit + accuracy — shadows amplify both, grace is the base |
| `might` | **Primary** | Physical burst damage — the BURST at 100 needs raw power |
| `insight` | **Secondary** | Shadow magic — dark damage scales with insight |
| `cognition` | **Secondary** | Stealth utility, shadow manipulation |
| `armor_bonus` | **None** | Glass cannon |
| `durability` | **None** | Glass cannon |
| `essence` | **None** | No healing, no magic resist |

### Status Identity

| Status | Source | Role |
|--------|--------|------|
| `hidden` | Stealth skills | **Signature** — 100% evasion, opening from shadow |
| `shaken` | Fear deposits / shadow strikes | **Primary** — fear, the manifestation of deposited shadows |
| `bleeding` | Precision strikes | **Secondary** — vital hits, critical cuts |
| `stunned` | Shadow strikes to vitals | **Rare** — shadow paralyze |
| `evasive` | Escape skills | **Rare** — escape mechanic, not sustained |
| `poisoned` | **None** | Replaced by shadow system entirely |
| `warded` | **None** | Not a tank |
| `inspired` | **None** | Not a buffer |
| `burning` | **None** | That's Lancer/Mage |

### Trigger Identity

| Trigger | Role |
|---------|------|
| `opening_move` | **Primary** — stealth openers, first-strike from hidden |
| `opponent_wounded` | **Primary** — execute scaling, finish the wounded |
| `opponent_status` | **Secondary** — exploit feared/shaken enemies |
| `always` | **Secondary** — standard shadow strikes |
| `low_hp` | **Rare** — desperate last strikes |
| `self_debuff` | **None** — Assassin debuffs others, not self |

### What the Assassin Does NOT Do

- **No poison** — shadow replaces poison entirely
- **No healing** — no `heal_percent`, pure offense
- **No `warded`** — not a tank
- **No `inspired`** — not a buffer
- **No elemental imbues** — that's Lancer
- **No buff stacking** — that's Knight
- **No evasion counter** — that's Rogue. Assassin evades through stealth, not dodging
- **No ally anything** — solo killer

### How Assassin Differs from the Other Masteries

| Aspect | Knight | Paladin | Lancer | Assassin |
|--------|--------|---------|--------|----------|
| Stacking resource | Armor + Might buffs | Inverse HP scaling | Elemental imbues | **Shadows (0-100)** |
| Burst mechanic | Buff ramp → big hit | Low HP → survive + heal | Element stack → versatile kill | **100 shadows → BURST (3x)** |
| Signature status | `warded` | `warded` | `evasive` | `hidden` |
| Playstyle | Stack → smash | Get hurt → endure | Imbue → adapt → strike | **Kill → stack shadows → BURST → reset** |
| Night bonus | None | None | None | **Passive shadow gen + stronger thresholds** |
| Enemy interaction | Debuff armor/might | Debuff might/essence | Debuff varies by element | **Deposit fear → reclaim on kill** |
| Versatility | Low (one mode) | Low (one mode) | High (6 elements) | **Low (one mode: kill)** |

---

## Passives — Auto-Learned, Unlocked Every 10 Levels

| # | Name | Level | Effect |
|---|------|-------|--------|
| 1 | Shadow Born | 10 | Start every combat with 10 shadows. Night: start with 20. |
| 2 | Shadow Harvest | 20 | Each kill grants +5 bonus shadows (total +15 per kill). |
| 3 | Shadow Precision | 30 | Shadows now also increase accuracy: +1% accuracy per 10 shadows. |
| 4 | Shadow Crit | 40 | Shadows now also increase crit damage: +10% crit damage at 50+, +20% at 75+. |
| 5 | Fear Mastery | 50 | Fear deposits are 50% stronger — each shadow deposited reduces enemy main stats (might, grace, insight) by 1.5 instead of 1. |
| 6 | Shadow Step | 60 | After a kill, 50% chance to re-enter `hidden`. Night: 75% chance. |
| 7 | Night Child | 70 | During night, all shadow threshold effects doubled. Passive shadow gen increased to +5/turn. |
| 8 | Shadow Convergence | 80 | At 75+ shadows, all strikes apply `shaken` (fear) automatically. Fear deposits cost no shadows. |
| 9 | Eclipse Mastery | 90 | BURST at 100 shadows now deals 4x damage instead of 3x. After BURST, retain 25 shadows instead of resetting to 0. |
| 10 | Avatar of Shadow | 100 | Always at minimum 50 shadows. BURST threshold lowered to 75. Night: always at 75 shadows. Stealth always breaks on attack, but after breaking, gain 75% evasion for 1 turn (the shadow lingers). Stealth skill cooldowns reduced by 50%. |

### Passive Synergy

>```
>Level 10:  Free 10 shadows → immediate power from turn 1
>Level 20:  +5 bonus shadows per kill → snowball faster
>Level 30:  Shadows boost accuracy → never miss at high stacks
>Level 40:  Shadows boost crit damage → BURST hits even harder
>Level 50:  Fear deposits 50% stronger → enemies crumble faster
>Level 60:  Kill → re-stealth → chain kills → shadow snowball
>Level 70:  Night doubles everything → Assassin is a god at night
>Level 80:  75+ shadows = free fear → no deposit cost → pure gain
>Level 90:  BURST = 4x + retain 25 → less punishing reset
>Level 100: Always 50+ shadows, BURST at 75, lingering evasion after stealth breaks, shorter stealth cooldowns → the shadow itself
>```

**The full build at level 100 (Night):**
- Starting shadows: 75 (Avatar of Shadow + Night)
- Per turn: +5 (Night Child)
- Per kill: +15 (Shadow Harvest)
- Per crit: +5
- Per stealth break: +15
- At 75 shadows (always, at night): +60% damage, +40% crit, +30% accuracy, +20% crit damage
- Free fear on every strike (no deposit cost)
- Stealth always breaks on attack, but leaves 75% evasion for 1 turn (shadow linger)
- Stealth skill cooldowns reduced by 50%
- BURST threshold: 75 (not 100), deals 4x damage, retains 25 after
- "The night belongs to the Assassin. Everything in it is just a shadow waiting to be collected."

---

## Skill Structure

All skills use the new format — no `power` or `skill_capacity_cost`.

| Field | Description |
|-------|-------------|
| `power_type` | strike, defend, debuff, buff |
| `damage_type` | physical, magical, true (strikes only) |
| `trigger` | always, low_hp, opponent_wounded, opponent_status, opening_move, self_debuff |
| `status_apply` | Status inflicted on enemy |
| `self_status` | Status applied to self (Assassin uses `hidden` for stealth, `evasive` for escape) |
| `stat_mod` | Temporary stat changes — `{"self": {...}, "enemy": {...}}` |
| `mod_duration` | How many turns stat_mod lasts |
| `hits` | Number of hits per use (default 1, max 3 for Assassin) |

**Assassin rules:** No `heal_percent`. No `warded` or `inspired` self_status. No `poisoned` status. No `burning` status. `hidden` grants 100% evasion while active. Shadows are the core mechanic — skills should reference shadow generation, fear deposits, and BURST interactions in descriptions. Buffs focus on `grace`, `might`, and `insight` — NOT `armor_bonus`/`essence`/`durability`.

---

## Tier Overview

| Tier | Level Req | Gold Cost | Learn Time | Count | Strikes | Stealth | Debuffs | Buffs | Defends | Legendary |
|------|-----------|-----------|------------|-------|---------|---------|---------|-------|---------|-----------|
| Basic | 1 | 50g | 5 min | 6 | 3 | 1 | 1 | 1 | 0 | 0 |
| Advanced | 3 | 150g | 30 min | 7 | 3 | 1 | 1 | 1 | 1 | 0 |
| Expert | 8 | 400g | 1 hr | 7 | 3 | 1 | 1 | 1 | 1 | 0 |
| Master | 15 | 1000g | 1 hr | 8 | 4 | 1 | 1 | 1 | 1 | 0 |
| Legendary | 20 | 2500g | 1 day | 2 | 0 | 0 | 0 | 0 | 0 | 2 |
| **Total** | | | | **30** | **13** | **4** | **4** | **4** | **3** | **2** |

---

## Basic Tier (Level 1, 50g, 5min) — 3 Strikes, 1 Stealth, 1 Debuff, 1 Buff

### 1. Shadow Strike
```python
{"id": "shadow_strike", "name": "Shadow Strike", "cooldown": 2,
 "power_type": "strike", "damage_type": "physical", "trigger": "always",
 "status_apply": "bleeding",
 "stat_mod": {"enemy": {"grace": -2}}, "mod_duration": 2}
```
**Description:** A quick slash infused with shadow energy. Each hit deposits a small amount of fear into the enemy. Generates shadows on critical hits.
**Narrative:** The Assassin's blade doesn't catch the light — it eats it. The cut is shallow but cold, and something worse than blood leaks out. The enemy feels a weight settle on their chest, a whisper at the edge of hearing. That's the shadow. It's already inside.

---

### 2. Backstab
```python
{"id": "backstab", "name": "Backstab", "cooldown": 3,
 "power_type": "strike", "damage_type": "physical", "trigger": "opening_move",
 "status_apply": "bleeding",
 "stat_mod": {"enemy": {"grace": -3, "might": -2}}, "mod_duration": 2}
```
**Description:** The Assassin strikes from behind, delivering a devastating blow to an unaware target. Opening move only. Guaranteed crit if used from `hidden`. Generates +10 shadows on stealth break.
**Narrative:** Patience is the weapon. The Assassin watches, counts the enemy's breaths, learns their rhythm. When the moment comes — when the enemy's weight shifts wrong — the blade arrives. Not fast. Just precise. And the enemy never sees the hand that held it. The shadow that was hiding the Assassin transfers to the wound. It stays there.

---

### 3. Heart Piercer
```python
{"id": "heart_piercer", "name": "Heart Piercer", "cooldown": 2,
 "power_type": "strike", "damage_type": "physical", "trigger": "always",
 "stat_mod": {"enemy": {"armor_bonus": -2, "might": -1}}, "mod_duration": 2}
```
**Description:** The blade slips precisely between armor plates, aiming directly for a vital point. Each strike deposits fear, weakening the enemy's resolve.
**Narrative:** Armor has gaps. Not many — but enough. The Assassin knows them all: the armpit, the throat, the join beneath the pauldron. The blade finds the gap the way water finds a crack. The enemy feels it before they understand it. And something darker than the blade settles into the wound — a fear that doesn't bleed out.

---

### 4. Smoke Veil
```python
{"id": "smoke_veil", "name": "Smoke Veil", "cooldown": 4,
 "power_type": "buff", "trigger": "always",
 "self_status": "hidden",
 "stat_mod": {"self": {"grace": 3}}, "mod_duration": 2}
```
**Description:** The Assassin throws a smoke pellet and disappears into the cloud, becoming `hidden`. While hidden, the Assassin has 100% evasion. The next attack breaks stealth for a guaranteed crit and +15 shadows.
**Narrative:** The pellet hits the ground. Smoke blooms — not gradual, not slow, but instant. One second the Assassin is there. The next, there is only smoke and the sound of footsteps that are already somewhere else. The enemy swings at the cloud. The cloud doesn't bleed.

---

### 5. Death Mark
```python
{"id": "death_mark", "name": "Death Mark", "cooldown": 4,
 "power_type": "debuff", "damage_type": "physical", "trigger": "always",
 "status_apply": "shaken",
 "stat_mod": {"enemy": {"grace": -3, "armor_bonus": -3, "might": -2}}, "mod_duration": 3}
```
**Description:** The Assassin marks the enemy with a shadow sigil, depositing a large amount of fear. The mark weakens all defenses and marks the target for death. If the marked enemy dies, the Assassin reclaims all deposited shadows.
**Narrative:** The Assassin traces a symbol in the air — quick, precise, final. The mark appears on the enemy's chest, dark as ink, cold as a closing door. The enemy feels it before they see it: a weight, a certainty, a whisper that says *you are already chosen*. The shadow has been deposited. The Assassin will collect it when the enemy stops breathing.

---

### 6. Shadow Focus
```python
{"id": "shadow_focus", "name": "Shadow Focus", "cooldown": 3,
 "power_type": "buff", "trigger": "always",
 "stat_mod": {"self": {"grace": 3, "might": 2}}, "mod_duration": 3}
```
**Description:** The Assassin centers themself, drawing ambient shadows inward. Boosts accuracy and damage, accelerating shadow accumulation.
**Narrative:** The Assassin closes their eyes. The shadows in the room — under the table, behind the pillar, beneath the enemy's feet — shift. They move toward the Assassin like water finding a drain. When the Assassin opens their eyes, they are sharper. Faster. Hungry. The shadows are feeding them.

---

## Advanced Tier (Level 3, 150g, 30min) — 3 Strikes, 1 Stealth, 1 Debuff, 1 Buff, 1 Defend

### 7. Silent Execution
```python
{"id": "silent_execution", "name": "Silent Execution", "cooldown": 4,
 "power_type": "strike", "damage_type": "physical", "trigger": "opening_move",
 "status_apply": "bleeding",
 "stat_mod": {"enemy": {"grace": -3, "might": -2}}, "mod_duration": 3}
```
**Description:** One clean slash ends the encounter before anyone reacts. Opening move only. If used from `hidden`, breaks stealth for guaranteed crit and +15 shadows. Deposits heavy fear on the target.
**Narrative:** The enemy is talking. Planning. Breathing. The Assassin is already moving. The blade crosses the distance in silence — no footstep, no breath, no warning. The enemy's sentence stops mid-word. They look down. The cut is already there. And the shadow that rode the blade settles into the wound like it belongs there. Because it does.

---

### 8. Phantom Strike
```python
{"id": "phantom_strike", "name": "Phantom Strike", "cooldown": 4,
 "power_type": "strike", "damage_type": "physical", "trigger": "always",
 "hits": 2,
 "status_apply": "bleeding",
 "stat_mod": {"enemy": {"grace": -2}}, "mod_duration": 2}
```
**Description:** The Assassin attacks so quickly that afterimages remain. Two rapid strikes, each depositing fear. Multi-hit generates more shadows per use.
**Narrative:** The enemy sees the Assassin move. Then they see it again. Two shapes — both striking, both real, both impossible. The afterimages fade, but the cuts don't. And each cut carries a shadow that settles into the wound. The enemy counts the cuts and gives up. The Assassin counts the shadows and smiles.

---

### 9. Crimson Dash
```python
{"id": "crimson_dash", "name": "Crimson Dash", "cooldown": 3,
 "power_type": "strike", "damage_type": "physical", "trigger": "always",
 "status_apply": "bleeding",
 "stat_mod": {"enemy": {"grace": -2, "armor_bonus": -2}}, "mod_duration": 2}
```
**Description:** The Assassin dashes through the enemy in a straight line, leaving a trail of shadow and blood. Deposits fear on impact.
**Narrative:** The Assassin doesn't run — they cut. The dash is a line drawn through the enemy, and the line is red on one side and black on the other. By the time the trail fades, the Assassin is on the other side and the enemy is looking down at a wound they didn't feel arrive. The shadow came with it. It's not leaving.

---

### 10. Night Veil
```python
{"id": "night_veil", "name": "Night Veil", "cooldown": 5,
 "power_type": "buff", "trigger": "always",
 "self_status": "hidden",
 "stat_mod": {"self": {"grace": 4, "might": 2}}, "mod_duration": 3}
```
**Description:** The Assassin wraps themself in living shadow, becoming `hidden`. Stronger than Smoke Veil — lasts longer and boosts both grace and might. Night: duration extended by +1 turn. Breaking stealth grants +15 shadows and guaranteed crit.
**Narrative:** The Assassin doesn't need smoke. They need shadow. The darkness around them thickens, solidifies, wraps around them like a second skin. The enemy looks at the spot where the Assassin was and sees nothing. Not smoke, not blur — nothing. As if the Assassin was never there. As if the shadow swallowed them. It did.

---

### 11. Shadow Terror
```python
{"id": "shadow_terror", "name": "Shadow Terror", "cooldown": 5,
 "power_type": "debuff", "damage_type": "magical", "trigger": "always",
 "status_apply": "shaken",
 "stat_mod": {"enemy": {"might": -4, "grace": -3, "cognition": -2}}, "mod_duration": 3}
```
**Description:** The Assassin floods the enemy's mind with shadow, inducing terror. Devastates might, grace, and cognition. Deposits a massive amount of fear. If the enemy dies while under this effect, the Assassin reclaims all shadows + bonus.
**Narrative:** The Assassin whispers. Not words — just a sound, a frequency, a vibration that the ear doesn't catch but the mind does. The enemy's eyes go wide. They see things that aren't there — shadows moving, faces in the dark, their own death wearing their face. They swing at nothing. They miss everything. The fear is eating them. The Assassin is patient. The fear will finish the job.

---

### 12. Shadowstep
```python
{"id": "shadowstep", "name": "Shadowstep", "cooldown": 3,
 "power_type": "defend", "trigger": "always",
 "self_status": "evasive",
 "stat_mod": {"self": {"grace": 4}}, "mod_duration": 2}
```
**Description:** The Assassin melts into darkness and reappears elsewhere, gaining extreme evasion. Not stealth — a quick repositioning that makes the next attack miss.
**Narrative:** The Assassin steps left — and isn't. The shadow they stepped into swallows them whole. A heartbeat later, the shadow behind the enemy opens, and the Assassin steps out. The enemy hasn't turned around yet. They will. But the Assassin will already be somewhere else by then.

---

### 13. Dark Pursuit
```python
{"id": "dark_pursuit", "name": "Dark Pursuit", "cooldown": 3,
 "power_type": "strike", "damage_type": "physical", "trigger": "opponent_wounded",
 "status_apply": "bleeding",
 "stat_mod": {"enemy": {"grace": -3, "might": -2}}, "mod_duration": 2}
```
**Description:** The Assassin relentlessly chases fleeing prey. Only triggers when the enemy is wounded. Each strike deposits additional fear — the wounded are easier to terrify.
**Narrative:** The enemy runs. The Assassin follows — not fast, but inevitable. Every shadow the enemy passes through, the Assassin is already there. Every corner they turn, the blade is already waiting. The enemy learns what every target learns: running only changes where you die. And the shadows that follow them are not theirs. They belong to the Assassin. The Assassin is coming to collect.

---

## Expert Tier (Level 8, 400g, 1hr) — 3 Strikes, 1 Stealth, 1 Debuff, 1 Buff, 1 Defend

### 14. Vanishing Kill
```python
{"id": "vanishing_kill", "name": "Vanishing Kill", "cooldown": 5,
 "power_type": "strike", "damage_type": "physical", "trigger": "opponent_status",
 "status_apply": "bleeding",
 "self_status": "hidden",
 "stat_mod": {"enemy": {"grace": -3, "might": -2}}, "mod_duration": 2}
```
**Description:** The Assassin strikes and disappears in the same motion, re-entering `hidden`. Only triggers when the enemy has a status effect (fear, bleeding). The strike deposits heavy fear, then the Assassin vanishes to strike again.
**Narrative:** The blade enters. The blade leaves. The Assassin enters the shadow. The enemy falls. It happens in the space between heartbeats — so fast that witnesses see the victim crumble and nothing else. The Assassin is already counting the next target. The shadow they left behind in the wound is counting too.

---

### 15. Shadow Flurry
```python
{"id": "shadow_flurry", "name": "Shadow Flurry", "cooldown": 5,
 "power_type": "strike", "damage_type": "physical", "trigger": "always",
 "hits": 3,
 "status_apply": "bleeding",
 "stat_mod": {"enemy": {"grace": -3, "armor_bonus": -2}}, "mod_duration": 2}
```
**Description:** The Assassin unleashes three rapid shadow-infused strikes. Each hit deposits fear and generates shadows on crits. The Assassin's signature multi-hit — no other mastery hits this fast.
**Narrative:** The Assassin doesn't swing three times. They swing once, and the shadow swings twice more. Three cuts arrive at the same moment — the blade, the shadow of the blade, and the shadow of the shadow. The enemy counts three wounds and wonders which one is real. They all are. And each one carries a piece of the dark.

---

### 16. Soul Sever
```python
{"id": "soul_sever", "name": "Soul Sever", "cooldown": 4,
 "power_type": "strike", "damage_type": "magical", "trigger": "always",
 "status_apply": "shaken",
 "stat_mod": {"enemy": {"might": -3, "essence": -3, "grace": -2}}, "mod_duration": 3}
```
**Description:** The blade glows with ghostly shadow energy, damaging body and spirit alike. Magical damage that deposits deep fear, devastating might, essence, and grace.
**Narrative:** The Assassin's blade changes — not in shape, but in nature. Shadow crawls along the edge, and when it cuts, it doesn't just part flesh. It parts something deeper. The enemy feels the wound in a place they can't name, and the part of them that was brave goes quiet. The shadow takes it. The Assassin keeps it.

---

### 17. Shadow Clone
```python
{"id": "shadow_clone", "name": "Shadow Clone", "cooldown": 5,
 "power_type": "buff", "trigger": "always",
 "self_status": "hidden",
 "stat_mod": {"self": {"grace": 5}}, "mod_duration": 3}
```
**Description:** The Assassin splits into an illusionary duplicate, becoming `hidden` while the clone distracts. Grants extreme grace. Breaking stealth from this state generates +20 shadows instead of +15.
**Narrative:** The Assassin splits — not physically, but perceptually. Two Assassins stand where one was. Both move. Both look real. The enemy swings at one and hits nothing. The other is already behind them. Which is real? The blade will tell. And the shadow that made the clone returns to the Assassin when the deception ends — heavier, darker, hungrier.

---

### 18. Shadow Prison
```python
{"id": "shadow_prison", "name": "Shadow Prison", "cooldown": 6,
 "power_type": "debuff", "damage_type": "magical", "trigger": "always",
 "status_apply": "shaken",
 "stat_mod": {"enemy": {"grace": -4, "might": -3, "cognition": -2}}, "mod_duration": 3}
```
**Description:** Living shadows wrap around the enemy, binding them in a prison of pure darkness. Devastates grace, might, and cognition. Deposits massive fear — the imprisoned are the most terrified.
**Narrative:** The Assassin raises a hand. The shadows on the ground rise with it — not metaphorically, but actually. They reach for the enemy, wrap around ankles, wrists, throat. The enemy can't move. The shadows are patient. The Assassin is not. And every shadow that binds the enemy is a shadow the Assassin will reclaim when the binding ends — one way or another.

---

### 19. Black Feathers
```python
{"id": "black_feathers", "name": "Black Feathers", "cooldown": 6,
 "power_type": "defend", "trigger": "low_hp",
 "self_status": "hidden",
 "stat_mod": {"self": {"grace": 5}}, "mod_duration": 3}
```
**Description:** Dark feathers fill the air as the Assassin escapes in a burst of ravens, becoming `hidden`. Only usable when HP is low. The escape generates +15 shadows — desperation fuels the dark.
**Narrative:** The enemy swings. The Assassin shatters. Not into blood — into feathers. Black, iridescent, alive. The ravens scatter in every direction, and the enemy is left swinging at birds. When the feathers settle, the Assassin is gone. The enemy is alone. They won't be for long. And the Assassin is already somewhere in the dark, counting the shadows the ravens brought back.

---

### 20. Eclipse Blade
```python
{"id": "eclipse_blade", "name": "Eclipse Blade", "cooldown": 5,
 "power_type": "buff", "trigger": "always",
 "stat_mod": {"self": {"might": 4, "grace": 3, "insight": 2}}, "mod_duration": 4}
```
**Description:** The blade absorbs surrounding light, empowering the Assassin's weapon with pure darkness. Boosts might, grace, and insight. While active, all strikes generate +2 bonus shadows per hit. Night: doubles the shadow bonus.
**Narrative:** The Assassin raises the blade. The light doesn't dim — it leaves. It pours into the steel like water into a drain, and the weapon becomes a void with an edge. The air around it is cold. The enemy can see the Assassin. They just can't see the blade. That's the point. And every cut the blade makes drinks more than blood — it drinks shadow, and the shadow feeds the Assassin.

---

## Master Tier (Level 15, 1000g, 1hr) — 4 Strikes, 1 Stealth, 1 Debuff, 1 Buff, 1 Defend

### 21. Shadow Convergence
```python
{"id": "shadow_convergence", "name": "Shadow Convergence", "cooldown": 6,
 "power_type": "buff", "trigger": "always",
 "stat_mod": {"self": {"grace": 5, "might": 4, "insight": 3}}, "mod_duration": 4}
```
**Description:** The Assassin draws all nearby shadows into themself, surging their shadow count by +25 instantly. Boosts grace, might, and insight dramatically. While active, all strikes deposit fear at no shadow cost.
**Narrative:** The Assassin closes their eyes and opens their hand. Every shadow in the room — under the tables, behind the pillars, beneath the enemy's feet — moves. Not slowly. They rush toward the Assassin like rivers to the sea. The room brightens as the shadows leave. The Assassin darkens as they arrive. When they open their eyes, there is no shadow left in the room. It's all inside. And it's hungry.

---

### 22. Night Requiem
```python
{"id": "night_requiem", "name": "Night Requiem", "cooldown": 6,
 "power_type": "strike", "damage_type": "physical", "trigger": "always",
 "hits": 3,
 "status_apply": "bleeding",
 "stat_mod": {"enemy": {"grace": -3, "armor_bonus": -3, "might": -2}}, "mod_duration": 3}
```
**Description:** The Assassin dances through the enemy, three shadow-infused cuts arriving simultaneously. Each hit deposits fear and generates shadows. Night: each hit generates +3 bonus shadows.
**Narrative:** The Assassin moves — not between enemies, but through them. The blade visits each one in turn, a whisper of steel and shadow. Three cuts, three enemies, three breaths of silence. When the Assassin stops, all three begin to bleed at the same time. The requiem plays itself. And the shadows that rode each cut stay behind, nesting in the wounds, waiting for the Assassin to collect them when the singing stops.

---

### 23. Death's Whisper
```python
{"id": "deaths_whisper", "name": "Death's Whisper", "cooldown": 5,
 "power_type": "debuff", "damage_type": "magical", "trigger": "opponent_wounded",
 "status_apply": "shaken",
 "stat_mod": {"enemy": {"might": -5, "grace": -4, "cognition": -3, "essence": -2}},
 "mod_duration": 3}
```
**Description:** A chilling whisper echoes behind the enemy, devastating all their stats. Only triggers when the enemy is wounded. Deposits catastrophic fear — the wounded hear the shadow clearest.
**Narrative:** The enemy is bleeding. Tired. Starting to think about retreat. And then — a whisper. Not loud. Not even a word. Just a sound behind their ear, close enough to feel breath that isn't there. The enemy turns. Nothing. Turns back. The Assassin is in front of them now. The whisper was a distraction. The shadow was the message. And the message says: *everything you have left belongs to me now.*

---

### 24. Umbral Cloak
```python
{"id": "umbral_cloak", "name": "Umbral Cloak", "cooldown": 6,
 "power_type": "buff", "trigger": "always",
 "self_status": "hidden",
 "stat_mod": {"self": {"grace": 5, "might": 3}}, "mod_duration": 4}
```
**Description:** The Assassin wraps themself in a cloak of pure shadow, becoming `hidden` for an extended duration. The strongest stealth skill — breaks for guaranteed crit and +20 shadows. Night: stealth duration +2 turns, and breaking stealth generates +30 shadows instead of +20. Stealth always breaks on attack.
**Narrative:** The shadow doesn't just hide the Assassin — it replaces them. Where the Assassin stood, there is only a silhouette, a suggestion, a trick of the light. The enemy attacks the silhouette. Their blade passes through. The silhouette smiles. The Assassin is already behind them, blade raised, shadow coiling. When the blade falls, the shadow shatters — but the pieces don't disappear. They linger, clinging to the Assassin's skin, making the next strike harder to land. The shadow always lets go. But it does so slowly.

---

### 25. Final Contract
```python
{"id": "final_contract", "name": "Final Contract", "cooldown": 6,
 "power_type": "strike", "damage_type": "physical", "trigger": "low_hp",
 "status_apply": "bleeding",
 "stat_mod": {"self": {"might": 4, "grace": 3}, "enemy": {"armor_bonus": -5, "might": -4, "grace": -3}},
 "mod_duration": 3}
```
**Description:** The Assassin accepts any price for victory. A devastating strike that empowers the Assassin and crushes the enemy. Only usable when HP is low. Generates +20 shadows — desperation is the darkest shadow.
**Narrative:** The Assassin is dying. They know it. They accept it. The contract is signed — not on paper, but in blood and intent. The blade rises with the weight of a final promise. Whatever happens after, this strike will land. This strike will end it. The enemy sees the Assassin's eyes and understands: this is not a fight anymore. This is a delivery. And the shadow that rides the blade is the deepest one the Assassin has ever carried — the shadow of their own death, aimed at someone else.

---

### 26. King Slayer
```python
{"id": "king_slayer", "name": "King Slayer", "cooldown": 6,
 "power_type": "strike", "damage_type": "physical", "trigger": "opponent_wounded",
 "status_apply": "bleeding",
 "stat_mod": {"enemy": {"might": -5, "armor_bonus": -5, "grace": -4, "durability": -3}},
 "mod_duration": 4}
```
**Description:** A technique designed to eliminate high-value targets. Devastates all enemy stats. Only triggers when the enemy is wounded. Deposits maximum fear — even kings fear the shadow.
**Narrative:** The enemy is powerful — a boss, a king, something that doesn't bleed easily. The Assassin doesn't care. This technique wasn't designed for soldiers. It was designed for the ones who think they're untouchable. The blade finds the chink that power hides, the gap that confidence leaves open. The enemy falls. The throne is empty. And the shadow that was deposited in the king's heart returns to the Assassin, heavier than it left, carrying the weight of a crown.

---

### 27. Shadow Devour
```python
{"id": "shadow_devour", "name": "Shadow Devour", "cooldown": 6,
 "power_type": "strike", "damage_type": "magical", "trigger": "opponent_status",
 "status_apply": "stunned",
 "stat_mod": {"enemy": {"might": -5, "grace": -5, "essence": -4, "cognition": -3}},
 "mod_duration": 3}
```
**Description:** The Assassin devours all fear deposited on the enemy, converting it into a devastating magical strike. Only triggers when the enemy has a status effect. Reclaims ALL deposited shadows and converts them into damage. The more fear deposited, the harder this hits.
**Narrative:** The enemy is covered in shadow — fear, terror, the dark that the Assassin has been planting all fight. The Assassin raises a hand. The shadows on the enemy shudder. Then they tear free — all of them, every last strand — and pour into the Assassin's blade. The enemy screams. Not from pain, but from the sudden absence of something they didn't know was there. The blade glows black. The Assassin smiles. The enemy's fear is about to visit them one last time.

---

### 28. Eclipse Burst
```python
{"id": "eclipse_burst", "name": "Eclipse Burst", "cooldown": 8,
 "power_type": "strike", "damage_type": "physical", "trigger": "always",
 "status_apply": "stunned",
 "stat_mod": {"enemy": {"might": -5, "grace": -5, "armor_bonus": -5}}, "mod_duration": 3}
```
**Description:** The Assassin channels all accumulated shadows into a single devastating strike. If shadows are at 100, this skill triggers the BURST automatically — 3x damage, guaranteed crit, ignores 70% of target armor. Otherwise, deals bonus damage proportional to current shadow count. After BURST, shadows reset to 0.
**Narrative:** The Assassin stops. For the first time in the fight, they are still. The shadows inside them surge — not gently, not patiently, but like a dam breaking. The blade becomes a point of absolute darkness, a void that swallows light and hope and certainty. The Assassin steps forward. One step. One strike. The world goes dark for a heartbeat — and when the light returns, the enemy is on their knees, and the Assassin's shadows are gone. All of them. Spent. The blade is just steel again. But the enemy will never be the same.

---

## Legendary Tier (Level 20, 2500g, 1 day — Quest-gated) — 2 True-Damage Strikes

### 29. Reaper's Arrival
```python
{"id": "reapers_arrival", "name": "Reaper's Arrival", "cooldown": 8,
 "power_type": "strike", "damage_type": "true", "trigger": "always",
 "status_apply": "stunned",
 "stat_mod": {"enemy": {"might": -5, "grace": -5, "armor_bonus": -6, "cognition": -4}},
 "mod_duration": 4,
 "self_status": "hidden"}
```
**Description:** The battlefield grows unnaturally silent as the Assassin walks calmly toward the enemy. True damage ignores all defense. Devastates all enemy stats. Grants `hidden` — the Assassin becomes shadow itself. Deposits ALL remaining shadows as fear on the target. Night: automatically triggers BURST if shadows are at 75+.
**Narrative:** The noise stops. Not gradually — all at once, like the world holds its breath. The Assassin walks forward. Not fast. Not slow. With the patience of someone who has already decided the outcome. The enemy sees them coming and feels something they've never felt before: the certainty that this is not a fight. This is an arrival. Every shadow the Assassin has collected pours forward — not around them, but through them, ahead of them, into the enemy before the blade even arrives. By the time the steel touches skin, the enemy is already drowning in dark. The blade comes down. The silence breaks. The enemy doesn't.

**Quest: The Price of Shadows**
- **Trainer:** Hildra Cold-Forge (Deepstone)
- **Min Level:** 20
- **Objectives:**
  - Kill 5 Crystal Cavern creatures in Khardrum
  - Gather 3 Relic Shards
  - Learn at least 5 Assassin skills from Hildra Cold-Forge
- **Reward:** Unlocks Reaper's Arrival

---

### 30. Eclipse of Shadows
```python
{"id": "eclipse_of_shadows", "name": "Eclipse of Shadows", "cooldown": 10,
 "power_type": "strike", "damage_type": "true", "trigger": "low_hp",
 "status_apply": "stunned",
 "stat_mod": {"enemy": {"might": -6, "grace": -6, "armor_bonus": -8, "cognition": -5, "essence": -4}},
 "mod_duration": 5,
 "self_status": "hidden"}
```
**Description:** The Assassin becomes the ultimate shadow — all accumulated shadows explode in a single true-damage strike that devours everything. True damage ignores all defense. Devastates all enemy stats. Grants `hidden`. Only usable when below 25% HP. Automatically triggers BURST regardless of shadow count — the desperation itself is the shadow. After BURST, retain 25 shadows instead of resetting to 0. Night: BURST deals 5x damage instead of 4x.
**Narrative:** The Assassin is dying. The shadows gather — not around them, but *as* them. The Assassin's body stops being solid. It becomes shadow, and the shadow becomes the Assassin. There is no blade to see. No body to hit. No person to kill. Just darkness, moving with intent. Every shadow the Assassin has ever collected — every kill, every crit, every whisper in the dark — surges forward at once. The enemy doesn't see the blade. They see the eclipse. And when the shadow passes, they are on the ground, and the Assassin is standing, and the night is quiet. The shadows don't reset. They never do, not for this one. The Assassin keeps just enough to remember who they are. The rest went into the enemy. The enemy won't be needing them.

**Quest: Eclipse of Shadows**
- **Trainer:** Hildra Cold-Forge (Deepstone)
- **Min Level:** 20
- **Objectives:**
  - Complete "The Price of Shadows" quest (learn Reaper's Arrival first)
  - Kill 1 Heritage Boss
  - Gather 1 Jahra Ingot
  - Learn at least 15 Assassin skills total
- **Reward:** Unlocks Eclipse of Shadows
