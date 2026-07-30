# Paladin Mastery — 30 Skills + 10 Passives

**Role:** The Divine Tank — a holy warrior who gets **tankier** as HP drops. Armor, magic resistance, and heal amplification all scale inversely with health. The enemy's best window is at the *start* of the fight.
**Masteries per trainer:** 3 (Paladin + 2 others)
**Trainers teaching Paladin:** Oathspire, Solunara, Atlantyrion

---

## Paladin Identity

**Knight:** "The more I buff, the harder I hit."
**Paladin:** "The more you hurt me, the harder I am to kill."

**Core loop:** Absorb damage → get tankier at low HP → heal amplified by low-HP scaling → punish enemies with holy strikes

- **Inverse HP scaling** — Paladin gets stronger defensively as HP drops. Armor, essence, and heal amp all increase at lower thresholds.
- **Magical damage** — holy strikes deal `magical` damage scaling with `essence`. Paladin is the only tank mastery with meaningful magical offense.
- **Divine healing** — self-focused, reactive (low_hp triggers), amplified when wounded. Sustain, not support.
- **Bonus damage vs. undead/devils** — holy damage is inherently more effective against unholy enemies (narrative + passive).
- **Buff stacking for survival** — buffs focus on `armor_bonus`, `essence`, and `durability`, NOT `might`. Stack to survive, not to kill.

### Stat Focus

| Stat | Priority | Why |
|------|----------|-----|
| `armor_bonus` | **Primary** | Physical tanking — scales higher at low HP |
| `essence` | **Primary** | Magic resistance + healing power — scales higher at low HP |
| `durability` | **Secondary** | HP pool — bigger pool = more low-HP thresholds to work with |
| `might` | **Secondary** | Physical strikes exist but aren't the focus |
| `grace` | **Minimal** | Not a precision class |
| `insight` | **Minimal** | Magical damage scales with essence, not insight |
| `cognition` | **None** | Not a utility class |

### Low-HP Scaling Design

| HP Range | Bonus | Flavor |
|----------|-------|--------|
| 100-75% | Baseline | "The Paladin is fresh, armor holds." |
| 75-50% | +2 armor, +2 essence, +10% heal amp | "The first wounds awaken the faith." |
| 50-25% | +4 armor, +4 essence, +25% heal amp | "The Paladin is bleeding but unbroken." |
| 25-0% | +6 armor, +6 essence, +50% heal amp | "The Paladin should be dead. The faith says otherwise." |

### Status Identity

| Status | Role |
|--------|------|
| `warded` | **Signature** — applied on almost every defensive skill and buff |
| `stunned` | **Secondary** — holy impact, hammer strikes |
| `shaken` | **Secondary** — divine judgment breaks enemy morale |
| `blinded` | **Rare** — holy light against unholy |
| `bleeding` | **Rare** — physical strikes only |
| `inspired` | **None** — Paladin doesn't inspire, they *endure* |
| `evasive`/`hidden` | **None** — Paladin stands and takes it |

### Trigger Identity

| Trigger | Role |
|---------|------|
| `low_hp` | **Primary** — Paladin's signature. Most heals and strongest buffs trigger here |
| `always` | **Secondary** — standard strikes and buffs |
| `opponent_wounded` | **Secondary** — execute-style holy strikes |
| `opening_move` | **Rare** — the initial charge |
| `self_debuff` | **Rare** — cleansing |

### What the Paladin Does NOT Do

- **No multi-hit** — one heavy hit, like Knight
- **No evasion/hidden** — Paladin stands and takes it
- **No poison/burning/DoT** — that's Assassin/Alchemist
- **No stacking might** — that's Knight. Paladin stacks *survivability*
- **No burst damage** — Paladin is sustained, not bursty
- **No ally buffs** — mechanically self-targeted. The faith protects the Paladin first.

### How Paladin Differs from Knight

| Aspect | Knight | Paladin |
|--------|--------|---------|
| Power source | Self-buffs (stacking might) | Divine power (wards + heals + essence) |
| Damage type | Physical only | Physical + Magical (holy) |
| Healing | None | Yes — self-healing, amplified at low HP |
| Defense style | Stack armor buffs | Wards + healing + inverse HP scaling |
| Low-HP behavior | **Offensive** (might buffs, fury) | **Defensive** (armor, essence, heal amp) |
| Playstyle | "I'm wounded, so I'll kill you faster" | "I'm wounded, so you can't kill me at all" |
| Stat focus | Armor + Might | Armor + Essence + Durability |

---

## Passives — Auto-Learned, Unlocked Every 10 Levels

| # | Name | Level | Effect |
|---|------|-------|--------|
| 1 | Divine Shield | 10 | Start every combat with `warded` status |
| 2 | Holy Fortitude | 20 | All self-heals increased by +15% |
| 3 | Blessed Armor | 30 | +2 permanent `armor_bonus` and +2 permanent `essence` (innate, always active) |
| 4 | Faith Unbroken | 40 | When HP drops below 75%, gain +2 `armor_bonus` and +2 `essence` for 3 turns |
| 5 | Divine Retribution | 50 | Bonus damage (x1.5) against undead and devil enemies |
| 6 | Martyr's Resolve | 60 | When HP drops below 50%, gain +4 `armor_bonus`, +4 `essence`, and +25% heal amplification for 3 turns |
| 7 | Aura of Warding | 70 | When `warded`, reduce all incoming damage by an additional 10% |
| 8 | Last Light | 80 | When HP drops below 25%, gain +6 `armor_bonus`, +6 `essence`, and +50% heal amplification for 3 turns |
| 9 | Resurrection | 90 | When HP would reach 0, survive with 1 HP instead. Cannot trigger again for 1 day (real-time cooldown). |
| 10 | Avatar of Faith | 100 | All low-HP scaling bonuses are permanent (always active, regardless of HP) |

### Passive Synergy

```
Level 10:  Free opening ward → baseline protection
Level 20:  Heals are stronger → divine sustain
Level 30:  Innate armor + essence → tanky from the start
Level 40:  First threshold (75%) → faith awakens, armor/essence climb
Level 50:  Bonus vs undead/devils → thematic power
Level 60:  Second threshold (50%) → serious tank, heals amplified
Level 70:  Warded reduces damage 10% → the wall gets thicker
Level 80:  Third threshold (25%) → nearly unkillable, heals massive
Level 90:  Survive death at 1 HP, 1-day cooldown → the faith refuses death
Level 100: ALL thresholds permanent → the Paladin is always at peak faith
```

---

## Skill Structure

All skills use the new format — no `power` or `skill_capacity_cost`.

| Field | Description |
|-------|-------------|
| `power_type` | strike, defend, heal, debuff, buff |
| `damage_type` | physical, magical, true (strikes only) |
| `trigger` | always, low_hp, opponent_wounded, opponent_status, opening_move, self_debuff |
| `status_apply` | Status inflicted on enemy |
| `self_status` | Status applied to self (always `warded` for buffs/defends) |
| `stat_mod` | Temporary stat changes — `{"self": {...}, "enemy": {...}}` |
| `mod_duration` | How many turns stat_mod lasts |
| `heal_percent` | Heals X% of max HP (heal skills only) |

**Paladin rules:** No `hits` > 1. No `evasive`/`hidden`/`inspired` self_status. All buffs target self only. Buffs focus on `armor_bonus`, `essence`, `durability` — NOT `might`. Heals trigger mostly on `low_hp`. Magical strikes scale with `essence`.

---

## Tier Overview

| Tier | Level Req | Gold Cost | Learn Time | Count | Buffs | Phys Strikes | Mag Strikes | Heals | Defends | Debuffs |
|------|-----------|-----------|------------|-------|-------|-------------|-------------|-------|---------|---------|
| Basic | 1 | 50g | 5 min | 6 | 2 | 1 | 1 | 1 | 1 | 0 |
| Advanced | 3 | 150g | 30 min | 7 | 2 | 1 | 1 | 1 | 1 | 1 |
| Expert | 8 | 400g | 1 hr | 7 | 1 | 1 | 1 | 2 | 1 | 1 |
| Master | 15 | 1000g | 1 hr | 8 | 3 | 1 | 1 | 2 | 1 | 0 |
| Legendary | 20 | 2500g | 1 day | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| **Total** | | | | **30** | **8** | **4** | **4** | **6** | **4** | **2** |

*(Legendary skills are true-damage strikes, counted separately)*

---

## Basic Tier (Level 1, 50g, 5min) — 2 Buffs, 1 Phys Strike, 1 Mag Strike, 1 Heal, 1 Defend

### 1. Shield of Faith
```python
{"id": "shield_of_faith", "name": "Shield of Faith", "cooldown": 3,
 "power_type": "defend", "trigger": "always",
 "self_status": "warded",
 "stat_mod": {"self": {"armor_bonus": 3, "essence": 2}}, "mod_duration": 3}
```
**Description:** A glowing crest surrounds the Paladin, raising both physical armor and magical resistance with divine protection.
**Narrative:** The Paladin raises their shield — not steel, but faith. A sigil blazes to life before it, a crest of light that hums like a choir. The first blow breaks against it. The first spell fizzles against it. The faith doesn't discriminate.

---

### 2. Blessed Strike
```python
{"id": "blessed_strike", "name": "Blessed Strike", "cooldown": 2,
 "power_type": "strike", "damage_type": "magical", "trigger": "always",
 "status_apply": "shaken",
 "stat_mod": {"enemy": {"might": -2}}, "mod_duration": 2}
```
**Description:** Holy symbols ignite along the blade as the Paladin strikes, dealing magical damage and shaking the enemy's resolve.
**Narrative:** The Paladin's blade is old, but the symbols etched along its edge are older. They wake at the Paladin's touch — golden, humming — and when the edge bites, the enemy feels something that has nothing to do with the cut. Doubt. The sense that they are on the wrong side of something. The might drains from their arms.

---

### 3. Merciful Touch
```python
{"id": "merciful_touch", "name": "Merciful Touch", "cooldown": 4,
 "power_type": "heal", "trigger": "low_hp",
 "self_status": "warded",
 "heal_percent": 0.10,
 "stat_mod": {"self": {"essence": 2, "armor_bonus": 2}}, "mod_duration": 3}
```
**Description:** The Paladin places a hand upon their own wounds, restoring HP with divine compassion. Amplified by low-HP scaling.
**Narrative:** The Paladin kneels, gauntlets forgotten, and presses a bare palm to the wound. Warmth flows — not magic, not medicine, just the simple mercy of someone who refuses to let themself fall. The wound closes. The armor hardens. The faith says not yet.

---

### 4. Hammer of Light
```python
{"id": "hammer_of_light", "name": "Hammer of Light", "cooldown": 3,
 "power_type": "strike", "damage_type": "physical", "trigger": "always",
 "status_apply": "stunned",
 "stat_mod": {"enemy": {"armor_bonus": -2}}, "mod_duration": 2}
```
**Description:** The Paladin's hammer crashes down with divine weight, stunning the enemy and denting their armor.
**Narrative:** The hammer is steel, but it falls like judgment. The impact rings like a church bell — deep, resonant, final. The enemy's knees buckle. Their armor dents. The Paladin is already lifting the hammer again.

---

### 5. Divine Aegis
```python
{"id": "divine_aegis", "name": "Divine Aegis", "cooldown": 4,
 "power_type": "buff", "trigger": "always",
 "self_status": "warded",
 "stat_mod": {"self": {"armor_bonus": 3, "essence": 3, "durability": 2}}, "mod_duration": 3}
```
**Description:** The Paladin channels faith into a protective aura that reinforces armor, magical resistance, and vitality simultaneously.
**Narrative:** The Paladin doesn't move. Doesn't speak. Just believes. And the belief becomes real — a shimmer in the air, a weight on the shoulders that feels like safety. Armor tightens. The spirit hardens. The body endures. This is the foundation. The stack begins.

---

### 6. Lightbearer's Oath
```python
{"id": "lightbearers_oath", "name": "Lightbearer's Oath", "cooldown": 4,
 "power_type": "buff", "trigger": "opening_move",
 "self_status": "warded",
 "stat_mod": {"self": {"armor_bonus": 2, "essence": 2, "durability": 2}}, "mod_duration": 3}
```
**Description:** An oath echoes with celestial authority, strengthening the Paladin's defenses as battle begins.
**Narrative:** The Paladin speaks the Oath of the Light — the first promise, the one that started everything. The words hang in the air like a bell still ringing. The armor sets. The spirit steadies. The light remembers. Opening move only.

---

## Advanced Tier (Level 3, 150g, 30min) — 2 Buffs, 1 Phys Strike, 1 Mag Strike, 1 Heal, 1 Defend, 1 Debuff

### 7. Sacred Charge
```python
{"id": "sacred_charge", "name": "Sacred Charge", "cooldown": 3,
 "power_type": "strike", "damage_type": "physical", "trigger": "opening_move",
 "status_apply": "stunned",
 "stat_mod": {"enemy": {"armor_bonus": -3, "might": -2}}, "mod_duration": 2}
```
**Description:** The Paladin charges with divine momentum, crashing into the enemy and shattering their guard.
**Narrative:** The Paladin lowers their shield and runs — not with rage, but with purpose. For a heartbeat, light trails from their shoulders like wings that don't exist. The enemy doesn't see the Paladin. They see what's behind the Paladin. They break.

---

### 8. Judgment Hammer
```python
{"id": "judgment_hammer", "name": "Judgment Hammer", "cooldown": 4,
 "power_type": "strike", "damage_type": "magical", "trigger": "always",
 "status_apply": "shaken",
 "stat_mod": {"enemy": {"might": -3, "essence": -2}}, "mod_duration": 3}
```
**Description:** A pillar of light crashes from the heavens, hammering the enemy with divine judgment and weakening their magical resistance.
**Narrative:** The Paladin raises a fist to the sky. The sky answers. A column of radiance descends — silent, absolute, patient — and the enemy is driven to their knees beneath a verdict they didn't know was coming. The light seeps in. The resistance crumbles.

---

### 9. Holy Barrier
```python
{"id": "holy_barrier", "name": "Holy Barrier", "cooldown": 4,
 "power_type": "defend", "trigger": "always",
 "self_status": "warded",
 "stat_mod": {"self": {"armor_bonus": 4, "essence": 3}}, "mod_duration": 3}
```
**Description:** A luminous sigil expands into a radiant dome, shielding the Paladin from both physical and magical harm.
**Narrative:** The Paladin traces a circle in the air. It stays. Light blooms from the line — a dome of gold and white, humming with the patience of a god who has decided nothing gets through. Nothing does.

---

### 10. Consecrate Blade
```python
{"id": "consecrate_blade", "name": "Consecrate Blade", "cooldown": 5,
 "power_type": "buff", "trigger": "always",
 "self_status": "warded",
 "stat_mod": {"self": {"essence": 3, "might": 2}}, "mod_duration": 4}
```
**Description:** Runes crawl across the Paladin's weapon, enchanting it with holy power. Boosts essence for magical strikes and might for physical ones.
**Narrative:** The Paladin runs a finger along the blade's edge. The metal hums. Runes bloom in its wake — ancient, golden, alive. The weapon is no longer just steel. It is a verdict waiting to be delivered. The Paladin's own power surges to meet it.

---

### 11. Sunburst
```python
{"id": "sunburst", "name": "Sunburst", "cooldown": 4,
 "power_type": "debuff", "damage_type": "magical", "trigger": "always",
 "status_apply": "blinded",
 "stat_mod": {"enemy": {"grace": -3}}, "mod_duration": 2}
```
**Description:** An explosion of sunlight erupts outward from the Paladin, blinding the enemy and reducing their accuracy.
**Narrative:** The Paladin opens their palm. The light that comes out is not gentle. It is the sun at noon, the desert at midday, the moment when shadows are not allowed. The enemy screams and covers their eyes. By the time they can see again, the Paladin has already moved.

---

### 12. Divine Light
```python
{"id": "divine_light", "name": "Divine Light", "cooldown": 5,
 "power_type": "heal", "trigger": "low_hp",
 "self_status": "warded",
 "heal_percent": 0.12,
 "stat_mod": {"self": {"essence": 3, "armor_bonus": 3}}, "mod_duration": 3}
```
**Description:** Warm holy light washes over the Paladin, healing wounds and fortifying defenses. Amplified by low-HP scaling.
**Narrative:** The darkness crawls beneath the skin — blood, exhaustion, the whisper of something giving up. The Paladin presses a palm to their chest and speaks a name of light. The darkness screams as it burns away. The wounds close. The armor sets. The faith says stand.

---

### 13. Guardian's Blessing
```python
{"id": "guardians_blessing", "name": "Guardian's Blessing", "cooldown": 5,
 "power_type": "buff", "trigger": "always",
 "self_status": "warded",
 "stat_mod": {"self": {"armor_bonus": 3, "essence": 3, "durability": 2}}, "mod_duration": 4}
```
**Description:** The Paladin raises a sacred emblem as divine light spreads, reinforcing armor, magical resistance, and vitality.
**Narrative:** The emblem is old — dented, tarnished, older than the Paladin's bloodline. But when they raise it, it glows like the first dawn. Skin hardens. Bones settle. The spirit fortifies. The line holds.

---

## Expert Tier (Level 8, 400g, 1hr) — 1 Buff, 1 Phys Strike, 1 Mag Strike, 2 Heals, 1 Defend, 1 Debuff

### 14. Divine Intercession
```python
{"id": "divine_intercession", "name": "Divine Intercession", "cooldown": 5,
 "power_type": "defend", "trigger": "low_hp",
 "self_status": "warded",
 "stat_mod": {"self": {"armor_bonus": 5, "essence": 4}}, "mod_duration": 3}
```
**Description:** When the Paladin is near death, divine power surges — massively boosting armor and magical resistance. Amplified by low-HP scaling.
**Narrative:** The blow lands. The Paladin should fall. Instead, they stand. Something moves behind their eyes — not rage, not desperation, but a calm that doesn't belong to the dying. The armor hardens. The spirit flares. The faith says not yet. The Paladin is still here.

---

### 15. Lay on Hands
```python
{"id": "lay_on_hands", "name": "Lay on Hands", "cooldown": 5,
 "power_type": "heal", "trigger": "low_hp",
 "self_status": "warded",
 "heal_percent": 0.15,
 "stat_mod": {"self": {"essence": 3, "durability": 2}}, "mod_duration": 3}
```
**Description:** The Paladin channels raw divine energy through their own body, healing significantly and fortifying their spirit. Amplified by low-HP scaling.
**Narrative:** The Paladin presses both palms to their chest. The light that comes is not gentle — it is a river, a flood, a force that will not be denied. Wounds knit. Bones set. The Paladin gasps, and the breath that enters them tastes like morning. The faith says stand. The Paladin stands.

---

### 16. Exorcism
```python
{"id": "exorcism", "name": "Exorcism", "cooldown": 4,
 "power_type": "debuff", "damage_type": "magical", "trigger": "opponent_status",
 "status_apply": "shaken",
 "stat_mod": {"enemy": {"might": -4, "essence": -3}}, "mod_duration": 3}
```
**Description:** Sacred words force darkness to flee, shattering the enemy's resolve and weakening both their physical and magical power.
**Narrative:** The Paladin speaks the Rite of Banishment — not loud, not fast, but with the weight of a thousand priests who spoke it before. The enemy's shadow writhes. Something behind their eyes screams and leaves. What remains is smaller. Weaker. Afraid. The holy words strip away their strength and their magic alike.

---

### 17. Celestial Spear
```python
{"id": "celestial_spear", "name": "Celestial Spear", "cooldown": 4,
 "power_type": "strike", "damage_type": "magical", "trigger": "always",
 "status_apply": "bleeding",
 "stat_mod": {"enemy": {"armor_bonus": -3, "essence": -2}}, "mod_duration": 3}
```
**Description:** A blazing lance of light streaks through the air, piercing the enemy and leaving them wounded and vulnerable.
**Narrative:** The Paladin extends a hand. Light gathers, condenses, hardens — and then it flies. The spear is silent until it hits. The sound it makes is the sound of something holy meeting something that isn't. The enemy bleeds light. Their armor cracks. Their magic falters.

---

### 18. Divine Resolve
```python
{"id": "divine_resolve", "name": "Divine Resolve", "cooldown": 4,
 "power_type": "defend", "trigger": "self_debuff",
 "self_status": "warded",
 "stat_mod": {"self": {"durability": 3, "essence": 3, "armor_bonus": 3}}, "mod_duration": 3}
```
**Description:** The Paladin's faith overcomes despair, cleansing debuffs and fortifying their body and spirit against further harm.
**Narrative:** The fear crawls in — cold, old, patient. The Paladin closes their eyes. They remember the temple. The candles. The voice that said *fear is a test, not a verdict*. They open their eyes. The fear is gone. The armor sets. The spirit hardens. They are still here.

---

### 19. Faith's Bulwark
```python
{"id": "faiths_bulwark", "name": "Faith's Bulwark", "cooldown": 5,
 "power_type": "buff", "trigger": "always",
 "self_status": "warded",
 "stat_mod": {"self": {"armor_bonus": 4, "essence": 4, "durability": 3}}, "mod_duration": 4}
```
**Description:** The Paladin's faith crystallizes into a living fortress — boosting armor, magical resistance, and vitality in a single invocation.
**Narrative:** The Paladin doesn't speak. Doesn't move. Just believes. And the belief becomes walls — not visible, not physical, but real. Every attack that comes finds the Paladin harder to hurt. Every spell finds the Paladin harder to curse. The faith is a fortress, and the Paladin is its only door.

---

### 20. Last Stand
```python
{"id": "last_stand", "name": "Last Stand", "cooldown": 5,
 "power_type": "heal", "trigger": "low_hp",
 "self_status": "warded",
 "heal_percent": 0.20,
 "stat_mod": {"self": {"armor_bonus": 4, "essence": 4}}, "mod_duration": 3}
```
**Description:** When the Paladin is on the brink, faith erupts — healing substantially and hardening both armor and magical resistance. Amplified by low-HP scaling.
**Narrative:** The Paladin is on one knee. The enemy raises their weapon for the final blow. And then — light. Not from the sky. Not from a prayer. From the Paladin themself. The light is not gentle. It is the light of someone who has decided that today is not the day. The wounds close. The armor sets. The Paladin rises. The enemy hesitates.

---

## Master Tier (Level 15, 1000g, 1hr) — 3 Buffs, 1 Phys Strike, 1 Mag Strike, 2 Heals, 1 Defend

### 21. Holy Nova
```python
{"id": "holy_nova", "name": "Holy Nova", "cooldown": 6,
 "power_type": "heal", "trigger": "always",
 "self_status": "warded",
 "heal_percent": 0.15,
 "stat_mod": {"self": {"essence": 4, "armor_bonus": 3}}, "mod_duration": 4}
```
**Description:** Light expands in every direction from the Paladin — healing wounds and hardening defenses in a burst of divine power.
**Narrative:** The Paladin presses their palms together and speaks the final word. Light detonates. It is not gentle. It is not soft. It is the mercy of a god who has decided the fighting stops now. Wounds close. Armor sets. The Paladin stands in the center of the light, and the light says *this one is mine*.

---

### 22. Sanctuary
```python
{"id": "sanctuary", "name": "Sanctuary", "cooldown": 6,
 "power_type": "defend", "trigger": "always",
 "self_status": "warded",
 "stat_mod": {"self": {"armor_bonus": 5, "essence": 5, "durability": 3}}, "mod_duration": 4}
```
**Description:** A peaceful aura surrounds the Paladin, declaring the ground sacred. Massive boost to all three defensive stats.
**Narrative:** The Paladin kneels and presses a palm to the earth. The ground answers — light spreads outward in a slow circle, and the air inside it changes. It feels like a temple. The enemy raises their weapon and... hesitates. Something in them doesn't want to. Something in them remembers what sacred means. The Paladin doesn't hesitate.

---

### 23. Justice Descends
```python
{"id": "justice_descends", "name": "Justice Descends", "cooldown": 5,
 "power_type": "strike", "damage_type": "magical", "trigger": "opponent_wounded",
 "status_apply": "stunned",
 "stat_mod": {"enemy": {"might": -4, "armor_bonus": -4, "essence": -3}}, "mod_duration": 3}
```
**Description:** A divine verdict falls from above, punishing the wounded enemy with heavenly force. Stuns and devastates all enemy stats.
**Narrative:** The enemy is bleeding, retreating, broken. The Paladin looks up — not at the enemy, but at the sky. "It is decided." The sky agrees. What falls is not lightning. It is a verdict, and it lands like one. The enemy crumples. Their armor shatters. Their magic dies. The judgment is final.

---

### 24. Guardian's Crown
```python
{"id": "guardians_crown", "name": "Guardian's Crown", "cooldown": 6,
 "power_type": "buff", "trigger": "always",
 "self_status": "warded",
 "stat_mod": {"self": {"armor_bonus": 6, "essence": 5, "durability": 4}}, "mod_duration": 4}
```
**Description:** A glowing crown appears above the Paladin's head, boosting all defenses with divine authority. The ultimate survivability buff.
**Narrative:** The crown doesn't rest on the Paladin's head — it hovers, spinning slowly, casting light in every direction. It is not a symbol of kings. It is a symbol of guardians. The Paladin wears it because someone has to, and they volunteered. The armor hardens. The spirit flares. The body endures. Nothing gets through.

---

### 25. Resurrection Prayer
```python
{"id": "resurrection_prayer", "name": "Resurrection Prayer", "cooldown": 7,
 "power_type": "heal", "trigger": "low_hp",
 "self_status": "warded",
 "heal_percent": 0.35,
 "stat_mod": {"self": {"essence": 4, "armor_bonus": 4, "durability": 3}}, "mod_duration": 4}
```
**Description:** A heartfelt prayer rekindles fading life, restoring a massive amount of HP when the Paladin is on the brink of death. Amplified by low-HP scaling. Note: The Resurrection passive (level 90) is separate — if HP would reach 0, the Paladin survives with 1 HP instead, but this cannot trigger again for 1 real-time day.
**Narrative:** The Paladin is on the ground. The light is fading. They whisper a prayer — not for themselves, but for the ones who are counting on them to stand. Something hears. Something answers. The Paladin's eyes open. The wounds close. The armor sets. The prayer is finished. The fight is not. But if the prayer is not enough — if the blade falls anyway — the faith catches them at the last breath. One HP. One heartbeat. One more chance. The faith will not do it again today. Tomorrow, maybe. Not today.

---

### 26. Consecrated Ground
```python
{"id": "consecrated_ground", "name": "Consecrated Ground", "cooldown": 6,
 "power_type": "buff", "trigger": "always",
 "self_status": "warded",
 "heal_percent": 0.10,
 "stat_mod": {"self": {"armor_bonus": 4, "essence": 4, "durability": 3}}, "mod_duration": 4}
```
**Description:** The Paladin consecrates the battlefield, bathing it in holy light that heals and fortifies. Buff + heal in one.
**Narrative:** The Paladin's hammer strikes the ground. The crack glows. Light seeps into the earth like water into dry soil, and the battlefield changes — grass straightens, wounds close, the air tastes like morning. This ground is sacred now. The Paladin stands on it. The enemy does not belong here.

---

### 27. Divine Wrath
```python
{"id": "divine_wrath", "name": "Divine Wrath", "cooldown": 5,
 "power_type": "strike", "damage_type": "physical", "trigger": "opponent_wounded",
 "status_apply": "stunned",
 "stat_mod": {"enemy": {"armor_bonus": -5, "might": -4}}, "mod_duration": 3}
```
**Description:** The Paladin's hammer descends with the weight of divine fury, crushing the wounded enemy's armor and stunning them.
**Narrative:** The enemy is hurt. Good. The Paladin raises the hammer high — higher than any human should — and brings it down. The impact is not steel on steel. It is faith on flesh. The enemy's armor buckles. Their arms go numb. The hammer rises again. The faith is patient. The faith is relentless.

---

### 28. Guardian Angel
```python
{"id": "guardian_angel", "name": "Guardian Angel", "cooldown": 6,
 "power_type": "heal", "trigger": "low_hp",
 "self_status": "warded",
 "heal_percent": 0.25,
 "stat_mod": {"self": {"armor_bonus": 5, "essence": 5, "durability": 3}}, "mod_duration": 4}
```
**Description:** A translucent angel hovers near the Paladin, mending wounds and fortifying defenses when all seems lost. Amplified by low-HP scaling.
**Narrative:** The Paladin is failing. They know it. And then — a presence. Not a person, not a memory, but something between. Wings of light unfurl behind them, and a hand rests on their shoulder. The wounds close. The armor sets. The spirit flares. The Paladin stands. They are not fighting alone. They never were.

---

## Legendary Tier (Level 20, 2500g, 1 day — Quest-gated) — 2 True-Damage Strikes

### 29. Last Judgment
```python
{"id": "last_judgment", "name": "Last Judgment", "cooldown": 8,
 "power_type": "strike", "damage_type": "true", "trigger": "opponent_wounded",
 "status_apply": "stunned",
 "stat_mod": {"enemy": {"might": -5, "armor_bonus": -6, "essence": -5}},
 "mod_duration": 4}
```
**Description:** A heavenly sword descends from the sky, delivering a powerful execution against evil. True damage ignores all defense. Only usable against wounded enemies. Bonus damage vs undead/devils.
**Narrative:** The Paladin raises both hands to the sky. The clouds part. Something descends — not a weapon, but a decision. A blade of pure light, vast as a cathedral spire, falls with the patience of a god who has finished deliberating. The enemy looks up. There is no dodge. There is no block. There is only the verdict, and it is final. Against the undead, the light burns hotter. Against devils, the judgment cuts deeper. The faith knows its enemies.

**Quest: The Final Verdict**
- **Trainer:** Serathiel Moonglow (Solunara)
- **Min Level:** 20
- **Objectives:**
  - Kill 5 Undead in the Ashen Border
  - Gather 3 Relic Shards
  - Learn at least 5 Paladin skills from Serathiel Moonglow
- **Reward:** Unlocks Last Judgment

---

### 30. Ascension of the Light
```python
{"id": "ascension_of_the_light", "name": "Ascension of the Light", "cooldown": 10,
 "power_type": "strike", "damage_type": "true", "trigger": "low_hp",
 "status_apply": "stunned",
 "stat_mod": {"enemy": {"might": -6, "armor_bonus": -8, "essence": -6}},
 "mod_duration": 5,
 "self_status": "warded",
 "heal_percent": 0.30}
```
**Description:** The Paladin becomes an avatar of divine endurance. Radiant wings unfold as celestial power engulfs the battlefield. True damage ignores all defense. Devastates enemy stats. Heals the Paladin massively. Only usable when below 25% HP. Amplified by low-HP scaling. Bonus damage vs undead/devils.
**Narrative:** The Paladin is dying. The light is almost gone. And then — a choice. Not to fight harder, but to become something else. The Paladin lets go of everything — the armor, the doubt, the fear — and the light rushes in to fill the space. Wings unfold. Not feathered. Not solid. Just light, shaped like mercy, moving like judgment. The Paladin rises. The wounds close. The armor sets. The enemy looks up and sees not a warrior, but a verdict wearing a face. The battlefield holds its breath. And then the light descends. Against the unholy, the light is absolute. Against the damned, the mercy is final.

**Quest: Ascension of the Light**
- **Trainer:** Serathiel Moonglow (Solunara)
- **Min Level:** 20
- **Objectives:**
  - Complete "The Final Verdict" quest (learn Last Judgment first)
  - Kill 1 Heritage Boss
  - Gather 1 Jahra Ingot
  - Learn at least 15 Paladin skills total
- **Reward:** Unlocks Ascension of the Light
