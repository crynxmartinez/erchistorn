# Bard Mastery — 30 Skills + 11 Passives

**Role:** The Master of Control — a performer who commands the battlefield through Song and Dance. In Song mode, the Bard changes the rules for allies — death saves, CC immunity, cooldown resets, rerolls. In Dance mode, the Bard controls enemy behavior — confusion, silence, friendly fire, pull. The Bard doesn't buff stats. The Bard changes what's possible.
**Masteries per trainer:** 3 (Bard + 2 others)
**Trainers teaching Bard:** Silvergate, Elaris, Riverguard

---

## Bard Identity

**Bard Battle Flow:**

> Choose Mode → Perform (goes first) → Crescendo Builds → Ticks Each Turn → Switch When Needed → Encore Lingers → The Music Fades, The Victory Remains

The Bard doesn't strike. The Bard **Performs**. In the battle UI, the Bard's action button says **"Perform"** instead of "Strike."

- **Song mode** — the Bard plays music that changes the rules for allies. Not stat buffs — behavioral shifts. Death saves, CC immunity, cooldown resets, rerolls. Affects the Bard + all party members
- **Dance mode** — the Bard performs a dance that controls enemy behavior. Not just damage — confusion, silence, friendly fire, pull. Affects enemies only
- **Performances always go first** — the music plays before anyone else acts, every turn
- **Crescendo** — each turn a Performance stays active, the behavioral effect grows stronger (max 5 stacks). Switching modes resets Crescendo to 0
- **Encore** — when a Performance expires, there's a chance it lingers for 1 more turn. The music fades, but it doesn't stop
- **No targeting** — the Bard just performs. The aura does the rest. No clicking allies, no selecting enemies
- **Rule changer** — the only mastery that changes **how the game works**, not just numbers. The Bard doesn't buff stats — the Bard changes what's possible
- **Master of control** — controlling allies or controlling enemies. The Bard doesn't fight — the Bard conducts

### Song & Dance Mode

A toggle at the bottom of the skill bar. Switching is **free** (once per turn, at the start). Each skill has **two effects** — one active in Song mode, one in Dance mode. The description changes based on which mode is active.

| | Song Mode | Dance Mode |
|---|-----------|------------|
| **Affected** | Bard + all party members | Enemies only |
| **Effect** | Rule changes — death saves, CC immunity, cooldown resets, rerolls | Behavior control — confusion, silence, friendly fire, pull, burn |
| **Targeting** | No target — aura covers the party | No target — aura hits enemies |
| **Priority** | Always goes first | Always goes first |
| **Fantasy** | The Bard changes what's possible for the party | The Bard changes what the enemy is willing to do |

### Performance as a Status

Every Performance creates a **visible status on the status bar** — both for the Bard and affected targets. Players can track:

- **Current Performance** (e.g., "🎵 Song of Heroes — Crescendo 3/5")
- **Encore** (e.g., "🎵♪ Encore: Song of Heroes — 1 turn remaining")
- **Active rule change** from the performance

No guessing. The music is visible.

### Crescendo

Each turn a Performance stays active in the **same mode**, Crescendo builds. Crescendo doesn't increase stats — it **enhances the behavioral effect**:

| Stacks | How the Effect Grows |
|--------|---------------------|
| 0 | Base effect |
| 1 | Effect strengthens |
| 2 | Effect strengthens |
| 3 | Effect strengthens |
| 4 | Effect strengthens |
| 5 (max) | Effect at full power |

**Examples:**
- Song of Hope at 0 stacks: survive at 1 HP. At 5 stacks: survive at 25% HP
- Dance of Mirrors at 0 stacks: 10% confusion. At 5 stacks: 50% confusion
- Dance of Madness at 0 stacks: 10% friendly fire. At 5 stacks: 50% friendly fire

**Switching modes resets Crescendo to 0.** This creates the core tension:
- *Stay in Song and let the rule change grow stronger?*
- *Switch to Dance to control the enemy's behavior?*
- *Lose my Crescendo or keep building?*

Crescendo is tracked on the Bard's status bar. If the Bard is stunned, Crescendo resets (unless modified by passives). If silenced, the Performance stops entirely.

### Encore

When a Performance expires, there's a **base 20% chance** it gets an Encore — the effect repeats for 1 more turn. The music lingers.

- Encore is tracked on the status bar with a distinct visual
- Active performance: **🎵 Song of Heroes**
- Encore (lingering): **🎵♪ Encore: Song of Heroes — 1 turn**
- Passives increase Encore chance (Harmonic: +15%, Masterful Encore: +30%)
- At max Crescendo with Legend of the Stage passive, Encore is guaranteed

### Audience

Purely visual. Zero mechanics. Maximum atmosphere.

As the Bard performs and Crescendo builds, the world gathers to listen:

| Crescendo | Who Shows Up |
|-----------|-------------|
| 0 | Just the Bard |
| 1 | Wisps of light drift in |
| 2 | Small birds land nearby |
| 3 | Faint spirits appear |
| 4 | Animals gather, ghostly musicians join |
| 5 (max) | Full audience — villagers, light, spirits, a crowd |
| Encore | The audience cheers. The music continues. |

The longer you perform, the more the world responds. Crescendo made visible through **life**, not numbers. When Encore triggers, the audience cheers — and the music plays on.

### Dance = Behavior Control

Dance performances don't just deal damage — they **control what the enemy does**. Each dance changes enemy behavior:

- **Dance of Mirrors** — enemy may attack a random target (including allies)
- **Dance of Chains** — enemy is pulled toward the Bard and `mesmerized`
- **Dance of Embers** — enemy takes burn damage per turn (the one DPT dance)
- **Dance of Silence** — enemy cannot use skills (basic attacks only)
- **Dance of Madness** — enemy may attack their own ally

The Bard doesn't damage the enemy's HP. The Bard damages the enemy's **autonomy**. Crescendo makes the behavior control more reliable — not bigger numbers, but higher chances.

One dance (Dance of Embers) does deal DPT — because fire is fire. But the rest? They control. That's the point.

### No Duplicate Effects

Every Performance changes a **unique rule**. No two songs change the same behavior. No two dances control the same action. Each skill is distinct:

- Song of Heroes → physical attacks can't be evaded
- Song of Hope → fatal blows leave 1 HP
- Song of Freedom → ignore one CC per turn
- Dance of Mirrors → confusion (attack random target)
- Dance of Silence → enemy can't use skills
- Dance of Madness → friendly fire chance

If you want "can't be evaded" AND "death save," you need two different songs. You can't stack the same rule from two sources.

### New Status: `mesmerized`

Dance-mode exclusive. The enemy **cannot act** and is **drawn toward the Bard** each turn. The dance controls their body — a combination of stunned + pulled, but uniquely musical.

### Turn Structure

```
Start of Turn:
  1. Performance ticks (always first — rule change for allies or behavior control for enemies)
  2. Crescendo +1 stack
  3. Bard acts (use a skill, switch modes, or maintain)
  4. Encore check (if performance ended — chance to linger 1 more turn)
```

### Golden Rule of the Bard

> A Bard should never ask: "How do I win this fight?"
>
> A Bard should ask: "Who am I conducting — my allies, or the enemy?"

### The Bard's Slogan

> *The Bard doesn't write the story. The Bard makes sure the story has heroes.*

### Stat Focus

| Stat | Priority | Why |
|------|----------|-----|
| `grace` | **Primary** | Performance quality, accuracy, evasion — the Bard's core stat |
| `cognition` | **Primary** | Song complexity, skill capacity — smarter Bard = better songs |
| `essence` | **Secondary** | Survival — the Bard must stay alive to keep performing |
| `durability` | **Secondary** | Staying power — a dead Bard stops the music |

### What the Bard Does NOT Do

- **No physical damage** (that's Knight/Lancer/Rogue)
- **No multi-hit strikes** (that's Assassin/Lancer)
- **No stealth** (that's Assassin/Rogue)
- **No self-buffing** (that's Priest — Bard buffs the **party**)
- **No healing specialty** (that's Priest — Bard has minor regen through Song, not burst heals)
- **No execution mechanic** (that's Priest/Assassin)
- **No heavy armor** (that's Knight/Paladin)
- **No burst damage** (that's Assassin/Rogue — Bard is control, not burst)

---

## Skill Structure

All skills use the new format — no `power` or `skill_capacity_cost`.

| Field | Description |
|-------|-------------|
| `power_type` | performance, strike, buff, debuff, heal, defend |
| `damage_type` | magical, true (strikes/legendary only) |
| `mode` | song, dance, both (performances only) |
| `song_effect` | Behavioral rule change in Song mode (performances only) |
| `dance_effect` | Behavioral control effect in Dance mode (performances only) |
| `base_chance` | Base % chance for probabilistic effects (performances) |
| `crescendo_scale` | How Crescendo enhances the effect per stack |
| `trigger` | always, low_hp, opponent_wounded, opponent_status, opening_move, self_debuff |
| `status_apply` | Status inflicted on enemy (one-shot skills) |
| `self_status` | Status applied to self/allies (one-shot skills) |
| `stat_mod` | Stat changes (one-shot skills only — performances use behavioral effects) |
| `mod_duration` | How many turns stat_mod lasts |
| `heal_percent` | Heals X% of max HP |
| `dpt_percent` | Damage per turn as % of enemy max HP (Dance of Embers + legendary only) |
| `crescendo` | Whether this skill builds Crescendo (performances only) |
| `encore` | Whether this skill can trigger Encore (performances only) |
| `hits` | Number of hits per use (default 1) |

**Bard rules:** No `damage_type: "physical"`. No `hits` > 1. No `evasive`/`hidden` self_status. Performances change **rules**, not stats — no `stat_mod` on performances. One-shot skills may use `stat_mod` — performances use `song_effect`/`dance_effect` instead. All one-shot **stat buffs** target `all_allies` — the Bard never self-buffs alone. No duplicate behavioral effects across performances. Skills are named like **song titles**. The action button says **"Perform"** not "Strike."

---

## Tier Overview

| Tier | Level Req | Gold Cost | Learn Time | Count | Performances | Buffs | Debuffs | Strikes | Heals | Defends |
|------|-----------|-----------|------------|-------|--------------|-------|---------|---------|-------|---------|
| Basic | 1 | 50g | 5 min | 6 | 2 | 0 | 1 | 1 | 0 | 2 |
| Advanced | 3 | 150g | 30 min | 7 | 1 | 1 | 3 | 1 | 1 | 0 |
| Expert | 8 | 400g | 1 hr | 7 | 1 | 5 | 1 | 0 | 0 | 0 |
| Master | 15 | 1000g | 1 hr | 8 | 1 | 4 | 2 | 0 | 0 | 1 |
| Legendary | 20 | 2500g | 1 day | 2 | 2 | 0 | 0 | 0 | 0 | 0 |

---

## Basic Tier (Level 1, 50g, 5min) — 2 Performances, 1 Debuff, 1 Strike, 2 Defends

### 1. Song of Heroes
```python
{"id": "song_of_heroes", "name": "Song of Heroes", "cooldown": 0,
 "power_type": "performance", "mode": "both", "trigger": "always",
 "crescendo": true, "encore": true,
 "song_effect": "physical_attacks_unevadable",
 "dance_effect": "confuse",
 "base_chance": 0.10, "crescendo_scale": 0.08}
```
**Song:** Physical allies' attacks **can't be evaded**. The song makes them undeniable — every strike lands. Crescendo: at 3+ stacks, magical allies' attacks also can't be evaded. At 5 stacks, all allies' attacks are unavoidable.
**Dance:** Enemy has a **10% chance to attack a random target** (including their own allies) each turn. Crescendo: +8% per stack (max 50% at 5 stacks). The enemy swings at shadows, at friends, at nothing.
**Narrative:** The Bard plays a war song — not loud, not aggressive, but certain. In Song, the allies feel their blades become truth. No dodge, no parry, no evasion answers them. The song says: you will hit. In Dance, the same certainty becomes the enemy's enemy — their eyes blur, their targets shift, they swing at allies they meant to protect. The Bard plays. The battlefield rewrites itself.

---

### 2. Song of Hope
```python
{"id": "song_of_hope", "name": "Song of Hope", "cooldown": 0,
 "power_type": "performance", "mode": "both", "trigger": "always",
 "crescendo": true, "encore": true,
 "song_effect": "death_save",
 "dance_effect": "pull_mesmerize",
 "base_chance": 0.15, "crescendo_scale": 0.05}
```
**Song:** **Fatal blows leave allies at 1 HP** (once per ally per performance). The song refuses to let them fall. Crescendo: survival threshold rises — 1 HP → 5% → 10% → 15% → 20% → 25% HP. At max Crescendo, allies survive at a quarter health.
**Dance:** Enemy is **pulled toward the Bard** each turn and has a **15% chance to be `mesmerized`** (cannot act). Crescendo: +5% mesmerize chance per stack (max 40%). The dance drags them closer and holds them still.
**Narrative:** The Bard plays a melody that refuses death. In Song, the allies feel it — the blade that should have killed them stops at 1 HP. The song says: not yet. Not today. In Dance, the same refusal becomes a pull — the enemy's feet move without permission, dragging them toward the Bard, and when the `mesmerized` takes hold, they stop entirely. The dance says: come here. Stay. The Bard plays. Death waits.

---

### 3. Mocking Verse
```python
{"id": "mocking_verse", "name": "Mocking Verse", "cooldown": 3,
 "power_type": "debuff", "damage_type": "magical", "trigger": "always",
 "status_apply": "shaken",
 "stat_mod": {"enemy": {"might": -2, "grace": -1}}, "mod_duration": 2}
```
**Description:** Every clever lyric lands harder than a blade. The Bard's insults weaken an enemy's confidence. A one-shot debuff — not a performance.
**Narrative:** The Bard doesn't draw a weapon. They draw a breath. The verse is sharp, personal, and unfortunately accurate. The enemy's face goes red. Their grip falters. They swing harder — too hard, too angry, too sloppy. The Bard grins. The insult was the weapon. The enemy is using it on themselves.

---

### 4. Resonant Strike
```python
{"id": "resonant_strike", "name": "Resonant Strike", "cooldown": 3,
 "power_type": "strike", "damage_type": "magical", "trigger": "always",
 "stat_mod": {"enemy": {"grace": -1}}, "mod_duration": 2}
```
**Description:** One powerful chord ripples through the air. A musical note becomes a shockwave. A one-shot strike — not a performance.
**Narrative:** The Bard hits the strings — not gently, not musically, but violently. The chord is wrong, dissonant, and it doesn't care. The sound becomes force. The shockwave crosses the battlefield and hits the enemy like an invisible hand. Their ears ring. Their stance breaks. The Bard is already tuning for the next one.

---

### 5. Harmony Shield
```python
{"id": "harmony_shield", "name": "Harmony Shield", "cooldown": 4,
 "power_type": "defend", "trigger": "always",
 "self_status": "warded",
 "stat_mod": {"all_allies": {"armor_bonus": 2, "essence": 1}}, "mod_duration": 3}
```
**Description:** Golden notes circle the party before hardening into light, forming a protective barrier of music. A one-shot defend — not a performance.
**Narrative:** The Bard plays a chord — not heard, but felt. The notes don't fade; they orbit. Golden, shimmering, they circle the party and harden into something between music and glass. The enemy's blade hits a note. The note rings. The blade stops. The Bard keeps playing.

---

### 6. Sunrise Chorus
```python
{"id": "sunrise_chorus", "name": "Sunrise Chorus", "cooldown": 4,
 "power_type": "defend", "trigger": "self_debuff",
 "self_status": "warded",
 "stat_mod": {"all_allies": {"essence": 2, "grace": 1}}, "mod_duration": 3}
```
**Description:** Bright harmonies rise with the dawn, removing fear and despair from the party. A one-shot defend — not a performance. Only triggers when debuffed.
**Narrative:** The fear is a weight. The despair is a fog. The Bard plays through it — not fighting the darkness, but playing past it. The melody rises like morning light, and the shadows don't stand a chance. The fear lifts. The fog clears. The Bard opens their eyes. The sun is up. Only triggers when debuffed.

---

## Advanced Tier (Level 3, 150g, 30min) — 1 Performance, 1 Buff, 3 Debuffs, 1 Strike, 1 Heal

### 7. Song of Wisdom
```python
{"id": "song_of_wisdom", "name": "Song of Wisdom", "cooldown": 0,
 "power_type": "performance", "mode": "both", "trigger": "always",
 "crescendo": true, "encore": true,
 "song_effect": "cooldown_reset",
 "dance_effect": "silence",
 "base_chance": 0.20, "crescendo_scale": 0.08}
```
**Song:** One magical ally's **next skill has no cooldown**. The song clears their mind and opens their arsenal. Crescendo: affects more allies per turn — 1 → 2 → 3 → 4 → 5 → all magical allies.
**Dance:** Enemy has a **20% chance to be silenced** each turn (basic attacks only — no skills). Crescendo: +8% per stack (max 60%). The dance steals their words, their magic, their options.
**Narrative:** The Bard plays a melody that opens minds. In Song, the magical allies feel their thoughts clear — every spell they know is available, every cooldown forgotten, every option open. The song says: you know more than you think. In Dance, the same clarity becomes the enemy's prison — their magic goes quiet, their skills slip away, they're left with nothing but their fists and their fear. The Bard plays. The wise grow wiser. The foolish grow silent.

---

### 8. Festival Rhythm
```python
{"id": "festival_rhythm", "name": "Festival Rhythm", "cooldown": 4,
 "power_type": "buff", "trigger": "always",
 "self_status": "inspired",
 "stat_mod": {"all_allies": {"grace": 2, "might": 1, "cognition": 1}}, "mod_duration": 3}
```
**Description:** Feet naturally move in time with the lively beat. The Bard raises the speed and energy of all allies. A one-shot buff — not a performance.
**Narrative:** The Bard plays fast — not frantic, but festive. The kind of tune that makes feet tap, that makes hands clap, that makes the whole body want to move. The allies feel it. Their steps quicken. Their blades flow. The battlefield becomes a dance floor, and the enemy is the only one who didn't get an invitation.

---

### 9. Discord
```python
{"id": "discord", "name": "Discord", "cooldown": 4,
 "power_type": "debuff", "damage_type": "magical", "trigger": "always",
 "status_apply": "shaken",
 "stat_mod": {"enemy": {"cognition": -3, "grace": -2, "might": -2}}, "mod_duration": 3}
```
**Description:** Harsh, clashing notes shatter the enemy's concentration and throw them into confusion. A one-shot debuff — not a performance.
**Narrative:** The Bard plays wrong. Not mistakes — intentional dissonance. The notes clash, grind, scrape against each other. The sound is physical: it gets inside the enemy's skull and rattles. Their thoughts scatter. Their timing breaks. They swing at the wrong moment, dodge in the wrong direction. The Bard keeps playing wrong. It's working.

---

### 10. Dance of Blades
```python
{"id": "dance_of_blades", "name": "Dance of Blades", "cooldown": 4,
 "power_type": "strike", "damage_type": "magical", "trigger": "always",
 "status_apply": "bleeding",
 "stat_mod": {"enemy": {"grace": -2}}, "mod_duration": 2}
```
**Description:** Each elegant step sends shimmering notes that cut like steel. The Bard turns graceful movement into a single devastating strike. A one-shot strike — not a performance.
**Narrative:** The Bard moves — not fighting, but performing. Each step sends a note into the air, and the note doesn't just sound. It cuts. Shimmering, razor-sharp, the music becomes a blade. The enemy bleeds from music. The Bard bows. The applause is blood.

---

### 11. Siren's Call
```python
{"id": "sirens_call", "name": "Siren's Call", "cooldown": 4,
 "power_type": "debuff", "damage_type": "magical", "trigger": "always",
 "status_apply": "ensnared",
 "stat_mod": {"enemy": {"grace": -3, "cognition": -2}}, "mod_duration": 2}
```
**Description:** An enchanting melody draws listeners closer, compelling enemies to approach the Bard. A one-shot debuff — not a performance.
**Narrative:** The Bard plays a melody — not loud, not aggressive, but magnetic. It pulls. The enemy doesn't want to approach. Their feet disagree. One step, then another, then they're walking toward the Bard without deciding to. The Bard smiles. The enemy arrives. The trap closes.

---

### 12. Ballad of Hope
```python
{"id": "ballad_of_hope", "name": "Ballad of Hope", "cooldown": 5,
 "power_type": "heal", "trigger": "low_hp",
 "self_status": "inspired",
 "heal_percent": 0.10,
 "stat_mod": {"all_allies": {"essence": 1, "grace": 1}}, "mod_duration": 3}
```
**Description:** Gentle harmonies wash over wounded companions like warm sunlight, gradually healing allies. A one-shot heal — not a performance. Triggers when HP is low.
**Narrative:** The Bard plays soft — not a war song, not a battle cry, but a ballad. Old, gentle, the kind sung to children and the wounded. The melody doesn't just sound; it heals. Wounds close in time with the rhythm. Pain fades with the harmony. The allies breathe easier. The Bard keeps playing. The hope keeps spreading. Triggers when HP is low.

---

### 13. Lullaby of Fallen Kings
```python
{"id": "lullaby_of_fallen_kings", "name": "Lullaby of Fallen Kings", "cooldown": 5,
 "power_type": "debuff", "damage_type": "magical", "trigger": "always",
 "status_apply": "stunned",
 "stat_mod": {"enemy": {"grace": -3, "might": -2, "cognition": -1}}, "mod_duration": 2}
```
**Description:** A soft tune drifts across the battlefield — the same melody played at the coronation of kings who are now dust. The enemy's eyelids get heavy. A one-shot debuff — not a performance.
**Narrative:** The Bard plays softly — not a battle hymn, not a war cry, but a lullaby. But not for children. For kings. For the ones who ruled and fell and were forgotten. The melody carries the weight of every crown that ever hit the floor. The enemy's eyelids get heavy. Their sword arm slows. Their thoughts get warm and thick and far away. They sway. They stumble. They're not asleep — they're just not awake anymore. The kings are waiting.

---

## Expert Tier (Level 8, 400g, 1hr) — 1 Performance, 5 Buffs, 1 Debuff

### 14. Song of Freedom
```python
{"id": "song_of_freedom", "name": "Song of Freedom", "cooldown": 0,
 "power_type": "performance", "mode": "both", "trigger": "always",
 "crescendo": true, "encore": true,
 "song_effect": "cc_immune",
 "dance_effect": "friendly_fire",
 "base_chance": 0.10, "crescendo_scale": 0.08}
```
**Song:** Allies **ignore one active CC** each turn (auto-cleanse). The song breaks chains, silences, stuns — whatever holds them. Crescendo: cleanses more CCs per turn — 1 → 2 → 3 → 4 → 5 → all active CCs.
**Dance:** Enemy has a **10% chance to attack their own ally** instead of the party each turn. Crescendo: +8% per stack (max 50%). The dance turns their loyalty into a weapon against themselves.
**Narrative:** The Bard plays a song about freedom — not as an idea, but as a force. In Song, the allies feel their chains break, their silences lift, their stuns shatter. Whatever was holding them lets go. The song says: you are free. In Dance, the same freedom becomes the enemy's betrayal — they look at their ally and see a target, they look at the Bard and see a friend. The dance says: who are you really fighting for? The enemy doesn't know anymore. The Bard plays. The chains break. The loyalty breaks. Only the music holds.

---

### 15. Moon Serenade
```python
{"id": "moon_serenade", "name": "Moon Serenade", "cooldown": 5,
 "power_type": "buff", "trigger": "always",
 "self_status": "warded",
 "heal_percent": 0.08,
 "stat_mod": {"all_allies": {"essence": 2, "grace": 1, "insight": 1}}, "mod_duration": 4}
```
**Description:** Silver notes drift like moonlight, strengthening and healing allies beneath the night sky. A one-shot buff — not a performance.
**Narrative:** The Bard plays a serenade — slow, silver, patient. The notes don't just sound; they glow. They drift like moonlight, settling on the party's skin. Wounds close. Magic sharpens. The body lightens. The moon has always had a soft spot for music. The Bard plays, and the moon listens.

---

### 16. Inspiring Solo
```python
{"id": "inspiring_solo", "name": "Inspiring Solo", "cooldown": 5,
 "power_type": "buff", "trigger": "always",
 "self_status": "inspired",
 "stat_mod": {"all_allies": {"might": 3, "grace": 2}}, "mod_duration": 3}
```
**Description:** The Bard performs directly for the party, helping them reach their full potential. A one-shot buff — not a performance.
**Narrative:** The Bard doesn't play for everyone. They play for each. The solo is personal, intimate, aimed. Every note says: *you*. Every chord says: *now*. The allies feel it — a surge, a focus, a sudden certainty that they are exactly where they need to be. The enemy sees the party change. The Bard sees the enemy worry.

---

### 17. Echo Verse
```python
{"id": "echo_verse", "name": "Echo Verse", "cooldown": 5,
 "power_type": "buff", "trigger": "opponent_status",
 "self_status": "inspired",
 "stat_mod": {"all_allies": {"might": 2, "grace": 2, "essence": 1}}, "mod_duration": 3}
```
**Description:** The Bard sings the final line again and its magic resonates once more, repeating the last supportive effect. A one-shot buff — not a performance. Only triggers when the enemy has a status effect.
**Narrative:** The Bard's last song ended. The magic faded. The Bard disagrees. They sing the final line again — same words, same notes, same intent — and the magic remembers. It comes back, echoes, doubles. The allies feel the buff return. The enemy feels the echo deepen. The Bard smiles. The best lines deserve an encore. Only triggers when the enemy has a status effect.

---

### 18. Epic Tale
```python
{"id": "epic_tale", "name": "Epic Tale", "cooldown": 5,
 "power_type": "buff", "trigger": "always",
 "self_status": "inspired",
 "heal_percent": 0.08,
 "stat_mod": {"all_allies": {"might": 2, "grace": 2, "durability": 2, "essence": 1}}, "mod_duration": 4}
```
**Description:** A story of impossible heroes inspires greatness. The Bard temporarily increases everyone's determination and heals the party. A one-shot buff — not a performance.
**Narrative:** The Bard doesn't play. They speak. A tale — old, grand, the kind told around fires for generations. Heroes who faced impossible odds. Warriors who didn't fall. The allies listen, and something stirs. Not magic — memory. The memory of what they're capable of. The Bard finishes the tale. The allies stand taller. The enemy feels the shift.

---

### 19. Muse's Blessing
```python
{"id": "muses_blessing", "name": "Muse's Blessing", "cooldown": 5,
 "power_type": "buff", "trigger": "always",
 "self_status": "inspired",
 "stat_mod": {"all_allies": {"insight": 3, "cognition": 2, "essence": 1}}, "mod_duration": 4}
```
**Description:** A divine muse whispers through the performance, improving creative and magical abilities of all allies. A one-shot buff — not a performance.
**Narrative:** The Bard plays, and something answers. Not a god — a muse. A whisper in the ear, a breath on the neck, a thought that isn't the Bard's but fits perfectly. The music deepens. The magic sharpens. The Bard's eyes glow with borrowed inspiration. The enemy sees the change and doesn't understand it. The muse does.

---

### 20. Curtain Call
```python
{"id": "curtain_call", "name": "Curtain Call", "cooldown": 5,
 "power_type": "debuff", "damage_type": "magical", "trigger": "opponent_status",
 "status_apply": "shaken",
 "stat_mod": {"enemy": {"might": -4, "grace": -3, "cognition": -3, "insight": -2}}, "mod_duration": 3}
```
**Description:** The Bard closes the piece with a decisive flourish, shattering enemy concentration and devastating their stats. A one-shot debuff — not a performance. Only triggers when the enemy has a status effect.
**Narrative:** The Bard plays the final chord — not soft, not gentle, but absolute. The flourish is a period at the end of a sentence. Every ongoing effect, every enchantment, every buff the enemy was riding — it stops. The silence that follows is not empty. It's heavy. The enemy feels their power drain, their focus shatter, their confidence fold. The show is over. The Bard takes a bow. Only triggers when the enemy has a status effect.

---

## Master Tier (Level 15, 1000g, 1hr) — 1 Performance, 4 Buffs, 2 Debuffs, 1 Defend

### 21. Song of Fortune
```python
{"id": "song_of_fortune", "name": "Song of Fortune", "cooldown": 0,
 "power_type": "performance", "mode": "both", "trigger": "always",
 "crescendo": true, "encore": true,
 "song_effect": "reroll",
 "dance_effect": "burn",
 "dpt_percent": 0.05, "crescendo_scale": 0.02}
```
**Song:** **Reroll the worst die** for one ally per turn. The song whispers to fate and fate listens. Crescendo: more rerolls per turn — 1 → 2 → 3 → 4 → 5 → all allies. At max Crescendo, the Bard rewrites everyone's luck.
**Dance:** Enemy takes **5% max HP as burn damage** per turn. The one DPT dance — fire, not music. Crescendo: +2% per stack (max 15% at 5 stacks). The dance burns because some things only understand fire.
**Narrative:** The Bard plays a melody that whispers to fate. In Song, the allies feel their luck shift — the bad roll becomes a good one, the miss becomes a hit, the worst moment becomes the best. The song says: try again. In Dance, the same whisper becomes fire — the enemy's skin blisters, their armor chars, their HP burns away note by note. The dance says: some things can't be rerolled. The Bard plays. Luck changes. Fire doesn't.

---

### 22. Hero's Anthem
```python
{"id": "heros_anthem", "name": "Hero's Anthem", "cooldown": 6,
 "power_type": "buff", "trigger": "opening_move",
 "self_status": "inspired",
 "stat_mod": {"all_allies": {"might": 3, "grace": 2, "armor_bonus": 2}}, "mod_duration": 4}
```
**Description:** A legendary ballad reminds everyone of ancient victories, greatly boosting morale and power. A one-shot buff — not a performance. Opening move only.
**Narrative:** The Bard plays the old anthem — the one written for heroes who are gone, the one that still makes the living stand taller. The melody is ancient, but the feeling is now. Every ally who hears it remembers what they're fighting for. Every enemy who hears it remembers what they're fighting against. The Bard plays. The battlefield remembers. Opening move only.

---

### 23. World Orchestra
```python
{"id": "world_orchestra", "name": "World Orchestra", "cooldown": 6,
 "power_type": "buff", "trigger": "always",
 "self_status": "inspired",
 "heal_percent": 0.10,
 "stat_mod": {"all_allies": {"might": 2, "grace": 2, "insight": 2, "essence": 1}}, "mod_duration": 4}
```
**Description:** Invisible instruments answer the Bard, filling the world with music and conducting the battlefield itself. A one-shot buff — not a performance.
**Narrative:** The Bard plays one note. The world plays it back. Invisible instruments join — violins from the air, drums from the ground, voices from the sky. The orchestra builds, and the Bard conducts. The music doesn't just sound; it empowers. Every ally feels it. Every stat sharpens. The battlefield is a symphony, and the Bard is the conductor.

---

### 24. Grand Performance
```python
{"id": "grand_performance", "name": "Grand Performance", "cooldown": 6,
 "power_type": "debuff", "damage_type": "magical", "trigger": "always",
 "status_apply": "stunned",
 "stat_mod": {"enemy": {"might": -4, "grace": -4, "cognition": -3, "insight": -2}}, "mod_duration": 3}
```
**Description:** Every eye turns toward the stage of battle. The Bard captivates everyone nearby. A one-shot debuff — not a performance.
**Narrative:** The Bard doesn't fight. They perform. And the performance is so compelling, so magnetic, so impossibly good that everyone stops to watch. The enemy can't look away. Their swords lower. Their guard drops. They're not fighting anymore — they're audience. The Bard plays. The enemy watches. The allies strike. The performance is a trap, and the enemy walked right in.

---

### 25. Memory Song
```python
{"id": "memory_song", "name": "Memory Song", "cooldown": 5,
 "power_type": "buff", "trigger": "always",
 "self_status": "inspired",
 "stat_mod": {"all_allies": {"cognition": 3, "insight": 2, "grace": 1}}, "mod_duration": 4}
```
**Description:** Ancient lyrics awaken buried memories. The Bard recalls forgotten knowledge, sharpening the party's mind and senses. A one-shot buff — not a performance.
**Narrative:** The Bard sings old words — not their own, but borrowed from ancestors, from teachers, from the first singers. The lyrics awaken something: memory, knowledge, the accumulated wisdom of everyone who ever played this tune. The allies' eyes sharpen. They see patterns the enemy didn't know they had. They predict moves before they're made. The song is a library, and the Bard just read every book.

---

### 26. Legend Keeper
```python
{"id": "legend_keeper", "name": "Legend Keeper", "cooldown": 6,
 "power_type": "buff", "trigger": "always",
 "self_status": "warded",
 "heal_percent": 0.10,
 "stat_mod": {"all_allies": {"might": 2, "grace": 2, "essence": 2, "durability": 1, "cognition": 1}}, "mod_duration": 4}
```
**Description:** The Bard records great deeds in song, preserving heroic memories and empowering all stats. A one-shot buff — not a performance.
**Narrative:** The Bard plays and speaks simultaneously — a song that is also a record, a melody that is also a history. Every great deed, every heroic moment, every impossible victory — the Bard weaves them into the music. The allies feel their ancestors in the notes. The Bard feels everything. All stats rise. The legend is kept. The legend is lived.

---

### 27. Whispered Melody
```python
{"id": "whispered_melody", "name": "Whispered Melody", "cooldown": 5,
 "power_type": "debuff", "damage_type": "magical", "trigger": "always",
 "status_apply": "shaken",
 "stat_mod": {"enemy": {"cognition": -4, "grace": -3, "might": -2, "insight": -2}}, "mod_duration": 3}
```
**Description:** Only the intended listener understands the tune. The Bard sends a secret message that destabilizes the enemy's mind. A one-shot debuff — not a performance.
**Narrative:** The Bard plays softly — so softly that only the enemy hears it. The melody is not music. It's a message. A whisper, a secret, a truth the enemy didn't want to know. It gets inside their head and stays. Their thoughts fracture. Their confidence crumbles. They don't know what the melody said, but it said something true, and true things are the hardest to forget.

---

### 28. Traveler's Tune
```python
{"id": "travelers_tune", "name": "Traveler's Tune", "cooldown": 6,
 "power_type": "defend", "trigger": "always",
 "self_status": "warded",
 "heal_percent": 0.08,
 "stat_mod": {"all_allies": {"grace": 2, "durability": 2, "essence": 1}}, "mod_duration": 4}
```
**Description:** The melody keeps exhaustion away during long journeys. The Bard restores stamina and grants protection to all allies. A one-shot defend — not a performance.
**Narrative:** The Bard plays a walking song — the kind sung on long roads, the kind that makes the miles shorter. The allies feel their fatigue lift. Their steps lighten. Their breathing steadies. It's not energy — it's endurance. The kind that says: *we can keep going*. The enemy is already tired. The Bard is just getting started.

---

## Legendary Tier (Level 20, 2500g, 1 day — Quest-gated)

### 29. Requiem of the Heavens
```python
{"id": "requiem_of_the_heavens", "name": "Requiem of the Heavens", "cooldown": 0,
 "power_type": "performance", "mode": "both", "trigger": "always",
 "crescendo": true, "encore": true,
 "song_effect": "all_rules_active",
 "dance_effect": "total_control",
 "heal_percent": 0.10,
 "damage_type": "true",
 "dpt_percent": 0.08, "stun_chance": 0.15,
 "base_chance": 0.25, "crescendo_scale": 0.05}
```
**Song:** **All five Song rules active simultaneously** — unevadable attacks, death save, CC immunity, cooldown reset, reroll. The heavens sing every song at once. Allies heal 10% max HP per turn. Crescendo: each rule strengthens independently as Crescendo builds.
**Dance:** **All five Dance effects active simultaneously** — confusion, pull+mesmerize, burn (8% true DPT), silence, friendly fire. The heavens perform every dance at once. 15% stun chance per turn. Crescendo: each effect's chance scales independently.
**Narrative:** The Bard plays a chord. The heavens answer. Voices — not one, not two, but a choir — descend from above, spectral, luminous, vast. In Song, every rule the Bard has ever learned activates at once — blades can't miss, death is refused, chains break, minds open, luck shifts. The party becomes invincible. In Dance, every dance the Bard has ever learned erupts simultaneously — the enemy is confused, pulled, burning, silenced, and attacking their own allies all at once. The enemy's body, mind, and loyalty all break together. The Bard stands at the center, and for one moment, the battlefield is a cathedral. The audience isn't just spirits anymore. The audience is the heavens.

**Quest: The Song of Creation**
- **Trainer:** Mira Songweaver (Silvergate)
- **Min Level:** 20
- **Objectives:**
  - Kill 5 Concordia elite guards
  - Gather 3 Relic Shards
  - Learn at least 5 Bard skills from Mira Songweaver
- **Reward:** Unlocks Requiem of the Heavens

---

### 30. Symphony of Creation
```python
{"id": "symphony_of_creation", "name": "Symphony of Creation", "cooldown": 0,
 "power_type": "performance", "mode": "both", "trigger": "low_hp",
 "crescendo": true, "encore": true,
 "song_effect": "rewrite_existence",
 "dance_effect": "total_domination",
 "heal_percent": 0.15,
 "damage_type": "true",
 "dpt_percent": 0.12, "stun_chance": 0.25,
 "base_chance": 0.40, "crescendo_scale": 0.08,
 "status_apply": "mesmerized"}
```
**Song:** **All rules at maximum power + allies heal 15% max HP per turn + all cooldowns reset every turn.** The Bard rewrites the rules of existence. The party doesn't just win — they become the story itself. Crescendo: all effects at maximum from the start, Crescendo extends duration.
**Dance:** **All dance effects at maximum power + 12% true DPT + 25% stun + `mesmerized` guaranteed.** The enemy loses all autonomy — confused, silenced, burning, attacking allies, pulled toward the Bard, and unable to act. The symphony doesn't control the enemy's behavior. The symphony replaces it. Crescendo: all effects at maximum from the start, Crescendo extends duration.
**Narrative:** The Bard is dying. The instrument is broken. And then — they sing. Not play. Sing. The first note is quiet. The second is not. The third fills the battlefield. And then the world joins — the wind hums, the earth beats, the hearts of every living thing sync with the melody. In Song, the allies become more than heroes — they become the story itself. Every rule activates. Every wound closes. Every cooldown resets. In Dance, the same symphony becomes the enemy's replacement — they are confused, silenced, burning, attacking their allies, walking toward the Bard, and unable to stop. The `mesmerized` status isn't a chance anymore. It's a certainty. The Bard isn't performing anymore. They are the performance. The enemy is the instrument. The audience is the world. Triggers when HP is low.

**Quest: The Song of Creation**
- **Trainer:** Mira Songweaver (Silvergate)
- **Min Level:** 20
- **Objectives:**
  - Complete "The Song of Creation" quest (learn Requiem of the Heavens first)
  - Kill 1 Heritage Boss
  - Gather 1 Jahra Ingot
  - Learn at least 15 Bard skills total
- **Reward:** Unlocks Symphony of Creation

---

## Passives — 10 Auto-Learned + 1 Legendary Quest Passive

| # | Name | Level | Effect |
|---|------|-------|--------|
| 1 | Tuned Ear | 10 | Performance effect chance +10% |
| 2 | Steady Rhythm | 20 | Crescendo builds +1 extra per turn (2 stacks/turn) |
| 3 | Charismatic | 30 | +10 permanent `grace` (innate, always active) |
| 4 | Harmonic | 40 | Encore chance +15% (base 20% → 35%) |
| 5 | Resonant | 50 | Crescendo max increased to 7 |
| 6 | Free Reprise | 60 | Switching modes keeps 50% of Crescendo instead of resetting to 0 |
| 7 | Crowd Pleaser | 70 | Audience appears faster — visual Crescendo at +1 stack |
| 8 | Unbreakable Voice | 80 | Crescendo no longer resets when stunned (only when silenced) |
| 9 | Masterful Encore | 90 | Encore chance +30% (total 65%). Encore lasts 2 turns instead of 1 |
| 10 | Legend of the Stage | 100 | Crescendo max 10. Encore guaranteed at max Crescendo. Mode switch is instant and unlimited. Performances cannot be silenced |
| 11 | Voice of the World | 100 (Quest) | **Legendary passive.** Song + Dance active simultaneously. Nothing else. That's already the strongest passive in the game. |

### Passive Synergy

```
Level 10:  Performance effect chance +10% → behaviors trigger more reliably
Level 20:  Crescendo builds 2/turn → peaks in 3 turns instead of 5
Level 30:  +10 permanent grace → the Bard's core stat, always active
Level 40:  Encore 35% → songs linger more often
Level 50:  Crescendo max 7 → effects at near-full power
Level 60:  Mode switch keeps 50% Crescendo → flexibility without total loss
Level 70:  Audience appears faster → the world gathers sooner (visual only)
Level 80:  Stun no longer resets Crescendo → only silence stops the music
Level 90:  Encore 65%, lasts 2 turns → the music almost never ends
Level 100: CRESCENDO MAX 10, ENCORE GUARANTEED AT PEAK, INSTANT MODE SWITCH, UNSILENCEABLE → the ultimate performer
Level 100+ (Quest): VOICE OF THE WORLD — BOTH MODES AT ONCE → the Bard becomes the music itself
```

**The full build at level 100 (Legend of the Stage):**
- Performance effect chance: +10% (Tuned Ear)
- Crescendo: 2 stacks/turn, max 10 = full power at peak (Steady Rhythm + Resonant + Legend)
- Encore: 65% base, **guaranteed** at max Crescendo, lasts 2 turns (Harmonic + Masterful + Legend)
- Mode switch: instant, unlimited, keeps 50% Crescendo (Free Reprise + Legend)
- Audience: appears faster, full crowd at Crescendo 4 instead of 5 (Crowd Pleaser)
- Stun doesn't reset Crescendo, only silence — but performances can't be silenced (Unbreakable + Legend)
- +10 permanent grace (Charismatic)
- The music never stops. The rules never lift. The enemy never recovers.

**With Voice of the World (Legendary Passive):**
- **Song + Dance active simultaneously** — the Bard's performance changes rules for allies AND controls enemy behavior at the same time
- That's it. That's the passive. Both modes at once.
- The Bard is simultaneously saving allies from death, making attacks unevadable, breaking CC, resetting cooldowns, rerolling fate — AND confusing enemies, silencing them, making them attack their allies, pulling them in, and burning them.
- "The Bard doesn't write the story. The Bard makes sure the story has heroes."

---

## Legendary Passive Quest — Voice of the World

**Quest: The Voice of the World**
- **Trainer:** Mira Songweaver (Silvergate)
- **Min Level:** 20
- **Objectives:**
  - Complete "The Song of Creation" quest (learn Symphony of Creation first)
  - Kill 3 Heritage Bosses
  - Gather 3 Jahra Ingots
  - Learn at least 20 Bard skills total
  - Reach level 100
- **Reward:** Unlocks Voice of the World passive — Song + Dance active simultaneously. The Bard becomes the music itself.
