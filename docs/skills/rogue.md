# Rogue Mastery — 30 Skills + 10 Innate Skills + 10 Passives

**Role:** The Adaptive Trickster — a cunning combatant who customizes their own passive kit through innate skills, fighting dirty with misdirection, traps, and counter-attacks. No two Rogues fight the same way.
**Masteries per trainer:** 3 (Rogue + 2 others)
**Trainers teaching Rogue:** Grunhold, Elaris, Silvergate

---

## Rogue Identity

**Knight:** "The more I buff, the harder I hit."
**Paladin:** "The more you hurt me, the harder I am to kill."
**Lancer:** "The more elements I stack, the more versatile I kill."
**Assassin:** "The more shadows I collect, the closer you are to death."
**Rogue:** "Every Rogue fights differently. Because every Rogue carries a different bag of tricks."

**Core loop:** Pick 5 innate skills → adapt loadout to enemy → fight dirty with tricks and debuffs → counter enemy mistakes → swap loadout for next fight

- **Innate skill system** — The Rogue has 10 innate skills learned immediately (no trainer, no gold). Only 5 can be equipped at once. These are passive/reaction abilities — always active while equipped. Swap outside of combat.
- **Dirty fighting** — The Rogue fights without honor: blinding, tripping, stealing, feigning. Every skill is a trick, every strike is unfair.
- **Counter-attacker** — The Rogue punishes enemy mistakes. When enemies miss or are debuffed, the Rogue exploits the opening.
- **Adaptability** — The Rogue's strength comes from choosing the right tools for the right fight. Face a tank? Equip armor-piercing tricks. Face a caster? Equip anti-magic tricks.
- **Evasion over armor** — The Rogue dodges, doesn't tank. High `grace`, stacking evasion, and `evasive` status keep them alive.
- **Glass cannon** — No healing, no tanking, no buffing allies. Pure trickery and damage. Kill them before they figure out your strategy.

### The Innate Skill System

The Rogue's unique mechanic — a **loadout system** no other mastery has.

- **10 innate skills** learned immediately when you become a Rogue
- **5 slots** — pick which 5 to equip (swap outside of combat)
- These are **passive/reaction abilities** — always active while equipped, no cooldown
- They define the Rogue's playstyle and tactical approach
- The Rogue **still has 30 trainable skills** from trainers, same as other masteries
- Innate skills do NOT compete with active skills for turns — they're always-on bonuses

**Why this works:**
- **Adaptability** — Swap loadout between fights for tactical advantage
- **Trade-offs** — Only 5 slots from 10 options — choosing is the strategy
- **Unique identity** — No other mastery customizes their passive kit
- **Always-on advantage** — Passive bonuses on top of normal skill usage

### The 10 Innate Skills

| # | Name | Type | Effect |
|---|------|------|--------|
| 1 | Quick Hands | Action | The Rogue acts first every turn — the player phase happens before the enemy phase. Always. |
| 2 | Counter Strike | Reaction | When the enemy's dice roll is 3 or less (miss/glancing/partial), the Rogue automatically counter-attacks for free damage (0.5x weapon damage). |
| 3 | Dirty Fighter | Passive | All strikes apply a random debuff (`shaken`, `bleeding`, or `blinded`). |
| 4 | Light Feet | Passive | Immune to `ensnared`. The Rogue cannot be trapped or immobilized. |
| 5 | Opportunist | Passive | +30% damage against enemies with any status effect. |
| 6 | Slippery | Reaction | 25% chance to shake off any debuff each turn. |
| 7 | Trap Master | Passive | The first strike each combat applies `ensnared`. |
| 8 | Second Story | Passive | +5 permanent `grace`. The Rogue is naturally agile. |
| 9 | Con Artist | Passive | All debuffs applied by the Rogue last +1 turn longer. |
| 10 | Lucky Dodger | Passive | Each time the enemy misses, gain +5% evasion (stacking, resets when hit). |

### Sample Loadouts

**Aggressive Counter-Rogue:**
- Quick Hands (act first) + Counter Strike (free counter on enemy roll ≤3) + Opportunist (+30% vs debuffed) + Dirty Fighter (random debuff) + Lucky Dodger (stacking evasion)
- Strike first, debuff them, then when they swing and roll poorly, auto-counter for free. Every bad enemy roll = free damage.

**Control/Trickster Rogue:**
- Trap Master (ensnare first hit) + Con Artist (debuffs last longer) + Dirty Fighter (random debuffs) + Slippery (shake off debuffs) + Light Feet (immune to ensnared)
- Lock the enemy down with debuffs, outlast them, never get locked down yourself.

**Evasion Tank Rogue:**
- Lucky Dodger (stacking evasion) + Counter Strike (free counter on enemy roll ≤3) + Second Story (+5 grace) + Light Feet (immune to ensnared) + Slippery (shake off debuffs)
- Become progressively harder to hit. Every bad enemy roll = free damage. Every miss = more evasion.

### Stat Focus

| Stat | Priority | Why |
|------|----------|-----|
| `grace` | **Primary** | Evasion + accuracy — the core of dodging and counter-attacking |
| `might` | **Primary** | Strike and counter-attack damage scaling |
| `cognition` | **Secondary** | Trickery, trap effectiveness, innate skill efficiency |
| `insight` | **Secondary** | Some magical debuffs and trickery |
| `armor_bonus` | **None** | Rogue dodges, doesn't tank |
| `durability` | **None** | Glass cannon — survives by not getting hit |
| `essence` | **None** | No healing, no magic resist |

### Status Identity

| Status | Role |
|--------|------|
| `evasive` | **Signature** — evasion buff, sustainable, stacking |
| `blinded` | **Primary** — reduces enemy accuracy = more misses = more counters |
| `shaken` | **Primary** — reduces enemy stats, dirty fighting staple |
| `bleeding` | **Secondary** — counter-attack and strike wounds |
| `ensnared` | **Secondary** — traps, immobilizes for free hits |
| `stunned` | **Rare** — perfect counter or feint |
| `hidden` | **Rare** — escape/reposition tool, not sustained like Assassin |
| `poisoned` | **None** — removed entirely |
| `warded` | **None** — not a tank |
| `inspired` | **None** — not a buffer |
| `burning` | **None** — not elemental |

### Trigger Identity

| Trigger | Usage |
|---------|-------|
| `opponent_status` | **Primary** — exploits debuffed enemies |
| `opponent_wounded` | **Primary** — kicks them while they're down |
| `opening_move` | **Secondary** — ambushes, first-strike traps |
| `low_hp` | **Secondary** — desperate tricks, escapes |
| `self_debuff` | **Rare** — escape artist reactions |
| `always` | **Common** — reliable tricks and debuffs |

### What the Rogue Does NOT Do

- **No poison** — removed entirely, dirty fighting replaces it
- **No healing** — no `heal_percent`, survives by evasion
- **No `warded`** — not a tank
- **No `inspired`** — not a buffer
- **No shadow system** — that's Assassin
- **No buff stacking** — that's Knight
- **No elemental imbues** — that's Lancer
- **No inverse HP scaling** — that's Paladin
- **No stealth-focused play** — `hidden` is an escape tool, not a core mechanic (that's Assassin)
- **No permanent anything** — adaptability means swapping, not locking in

### How Rogue Compares to Other Masteries

| Aspect | Assassin | Rogue |
|--------|----------|-------|
| Unique mechanic | Shadow system (0-100) → BURST | Innate skill loadout (pick 5 from 10) |
| Evasion type | `hidden` = 100% evasion, breaks on attack | `evasive` = % evasion, sustainable, stacking |
| Playstyle | Aggressive burst, kill → stack → BURST | Adaptive counter, trick → debuff → exploit |
| Stealth | Core mechanic | Escape tool only |
| Debuffs | Fear (shaken) — shadow deposit | Dirty fighting (blinded, shaken, ensnared) |
| Customization | None — fixed playstyle | High — swap innate loadout between fights |
| Initiation | Yes — opening moves, stealth strikes | Both — can ambush or wait for counters |

---

## Passives — Auto-Learned, Unlocked Every 10 Levels

| # | Name | Level | Effect |
|---|------|-------|--------|
| 1 | Trickster's Eye | 10 | +1 innate skill slot (6 total instead of 5). |
| 2 | Quick Learner | 20 | Learn skills 25% faster from trainers. |
| 3 | Adaptive | 30 | Swap innate skills during combat (once per fight). |
| 4 | Dirty Mastery | 40 | Dirty Fighter innate now applies 2 debuffs instead of 1. |
| 5 | Counter Precision | 50 | Counter Strike innate now triggers on enemy roll ≤4 (instead of ≤3) and deals 0.75x weapon damage instead of 0.5x. |
| 6 | Evasion Training | 60 | Lucky Dodger innate stacks to +10% per miss instead of +5%. |
| 7 | Trap Specialist | 70 | Trap Master innate applies `ensnared` on first 2 strikes each combat. |
| 8 | Con Master | 80 | Con Artist innate now makes debuffs last +2 turns instead of +1. |
| 9 | Slippery Soul | 90 | Slippery innate now has 50% chance to shake debuffs each turn. |
| 10 | Master of Tricks | 100 | +1 innate skill slot (7 total). All innate effects doubled. |

### Passive Synergy

```
Level 10:  6 innate slots → more tricks in the bag
Level 20:  Faster skill learning → Rogue progresses faster
Level 30:  Swap innates mid-combat → adapt to the fight
Level 40:  Dirty Fighter hits with 2 debuffs → enemies crumble
Level 50:  Counter triggers on roll ≤4, hits harder → bad enemy rolls punish hard
Level 60:  Lucky Dodger stacks faster → become untouchable
Level 70:  2 traps per combat → more control
Level 80:  Debuffs last +2 turns → enemies stay weakened
Level 90:  50% debuff shake → nearly immune to debuffs
Level 100: 7 innate slots, all doubled → the ultimate trickster
```

**The full build at level 100:**
- 7 innate skill slots (pick 7 from 10)
- All innate effects doubled (Counter Strike = 100% weapon damage on enemy roll ≤3, Lucky Dodger = +20%/miss, etc.)
- Swap innates mid-combat (once per fight)
- Debuffs last +2 turns, 50% chance to shake debuffs each turn
- "Every Rogue fights differently. At level 100, the Rogue fights like seven Rogues at once."

---

## Skill Structure

All skills use the new format — no `power` or `skill_capacity_cost`.

| Field | Description |
|-------|-------------|
| `power_type` | strike, defend, debuff, buff |
| `damage_type` | physical, magical, true (strikes only) |
| `trigger` | always, low_hp, opponent_wounded, opponent_status, opening_move, self_debuff |
| `status_apply` | Status inflicted on enemy |
| `self_status` | Status applied to self |
| `stat_mod` | Temporary stat changes — `{"self": {...}, "enemy": {...}}` |
| `mod_duration` | How many turns stat_mod lasts |
| `hits` | Number of hits per use (default 1, max 3 for Rogue) |

**Available stat_mod targets:**
- `might` — physical damage scaling
- `grace` — accuracy + evasion
- `cognition` — skill capacity / utility
- `insight` — magical damage scaling
- `essence` — magic resistance + healing power
- `durability` — HP / resilience
- `armor_bonus` — physical damage reduction

**Rogue rules:** No `heal_percent`. No `warded` or `inspired` self_status. No `poisoned` status. No `burning` status. `evasive` is the signature status — stacking evasion is the Rogue's defense. Skills should reference dirty fighting, tricks, traps, counter-attacks, and innate skill synergies in descriptions. Buffs focus on `grace`, `might`, and `cognition` — NOT `armor_bonus`/`essence`/`durability`.

---

## Tier Overview

| Tier | Level Req | Gold Cost | Learn Time | Count | Type Breakdown |
|------|-----------|-----------|------------|-------|----------------|
| Basic | 1 | 50g | 5 min | 6 | 3 Strikes, 1 Debuff, 1 Defend, 1 Buff |
| Advanced | 3 | 150g | 30 min | 7 | 3 Strikes, 2 Debuffs, 1 Buff, 1 Defend |
| Expert | 8 | 400g | 1 hr | 7 | 3 Strikes, 1 Debuff, 1 Buff, 2 Defends |
| Master | 15 | 1000g | 1 hr | 8 | 4 Strikes, 1 Debuff, 1 Buff, 2 Defends |
| Legendary | 20 | 2500g | 1 day | 2 | 2 True-Damage Strikes |
| **Total** | | | | **30** | **15 Strikes, 5 Debuffs, 4 Buffs, 6 Defends** |

---

## Basic Tier (Level 1, 50g, 5min) — 3 Strikes, 1 Debuff, 1 Defend, 1 Buff

### 1. Dirty Trick
```python
{"id": "dirty_trick", "name": "Dirty Trick", "cooldown": 2,
 "power_type": "debuff", "damage_type": "physical", "trigger": "always",
 "status_apply": "shaken",
 "stat_mod": {"enemy": {"grace": -2, "might": -1}}, "mod_duration": 2}
```
**Description:** The Rogue flicks dirt, a coin, or debris into the opponent's face. Reduces enemy grace and might — the opening move of every dirty fighter. Synergizes with Opportunist innate (+30% damage against debuffed enemies).
**Narrative:** There's no honor in it. The Rogue doesn't care. The dirt hits the eyes, the coin clips the temple, and by the time the enemy stops blinking, the Rogue is already somewhere else. The enemy swings at the wrong shadow. The Rogue grins. This is the first trick every Rogue learns, and the last one the enemy expects.

---

### 2. Hidden Blade
```python
{"id": "hidden_blade", "name": "Hidden Blade", "cooldown": 3,
 "power_type": "strike", "damage_type": "physical", "trigger": "opening_move",
 "status_apply": "bleeding",
 "stat_mod": {"enemy": {"grace": -2}}, "mod_duration": 2}
```
**Description:** A blade appears from an unsuspected place. The Rogue reveals a concealed weapon at the perfect moment. Opening move only — sets up the fight with an early wound. Synergizes with Trap Master innate (first strike applies `ensnared`).
**Narrative:** The enemy searches the Rogue for weapons. They find the obvious ones — the belt knife, the boot dagger. They miss the one that matters. The Rogue smiles, and the blade slides from the bracer like a whispered secret. The enemy learns the secret the hard way. And if the Rogue packed Trap Master, the blade carries a wire that wraps around the enemy's ankle on the way out. Now they're bleeding AND tied down.

---

### 3. Opportunist Strike
```python
{"id": "opportunist_strike", "name": "Opportunist Strike", "cooldown": 2,
 "power_type": "strike", "damage_type": "physical", "trigger": "opponent_status",
 "status_apply": "bleeding",
 "stat_mod": {"enemy": {"might": -2}}, "mod_duration": 2}
```
**Description:** The Rogue strikes distracted enemies at their weakest. Only triggers when the enemy has a status effect. The bread-and-butter of the dirty fighter — kick them while they're down.
**Narrative:** The enemy is rubbing their eyes, pulling at a tripwire, choking on smoke. The Rogue watches. Waits. Counts the heartbeat where the enemy's guard drops lowest. Then the knife arrives — polite, precise, and completely unfair. The Rogue doesn't feel bad about it. The enemy should have fought cleaner.

---

### 4. Acrobatic Roll
```python
{"id": "acrobatic_roll", "name": "Acrobatic Roll", "cooldown": 3,
 "power_type": "defend", "trigger": "always",
 "self_status": "evasive",
 "stat_mod": {"self": {"grace": 3}}, "mod_duration": 2}
```
**Description:** The Rogue tumbles effortlessly beneath danger, rolling through incoming attacks. Grants `evasive` and boosts grace — the core defense of the Rogue. Synergizes with Lucky Dodger innate (stacking evasion on each enemy miss).
**Narrative:** The blade comes down. The Rogue isn't there — they're below it, rolling through the gap between the swing and the ground. They come up on the other side, already balanced, already moving. The enemy's sword is still falling. The Rogue is already gone. And if the Rogue packed Lucky Dodger, the next swing will miss by even more. And the one after that. And the one after that.

---

### 5. Quick Step
```python
{"id": "quick_step", "name": "Quick Step", "cooldown": 3,
 "power_type": "buff", "trigger": "always",
 "self_status": "evasive",
 "stat_mod": {"self": {"grace": 3, "might": 2}}, "mod_duration": 3}
```
**Description:** The Rogue shifts their stance, boosting grace and might while becoming `evasive`. A versatile buff that enhances both offense and defense — the Rogue is always ready to move.
**Narrative:** The Rogue bounces on their toes. Left foot forward, weight centered, blade low. It looks casual — like a dancer waiting for music. It's not casual. Every muscle is coiled. Every angle is calculated. When the enemy swings, the Rogue will already be somewhere else, and the knife will already be moving. The stance is the trick. The trick is that there's no trick — just speed.

---

### 6. Pocket Sand
```python
{"id": "pocket_sand", "name": "Pocket Sand", "cooldown": 3,
 "power_type": "debuff", "damage_type": "physical", "trigger": "always",
 "status_apply": "blinded",
 "stat_mod": {"enemy": {"grace": -3}}, "mod_duration": 2}
```
**Description:** The Rogue throws sand directly into the enemy's eyes. `blinded` reduces enemy accuracy — more bad rolls = more counter-attack opportunities. The signature dirty trick. Synergizes with Counter Strike innate (free counter on enemy roll ≤3) and Lucky Dodger (evasion stacks on miss).
**Narrative:** The hand moves — fast, casual, like brushing dust off a sleeve. The sand follows. Coarse, gritty, aimed. The enemy's eyes flood with tears and the world goes white. The Rogue is already moving. The enemy is still rubbing. And every time they swing blind, the Rogue gets faster, harder to hit, more confident. The sand wasn't the trick. The sand was the setup.

---

## Advanced Tier (Level 3, 150g, 30min) — 3 Strikes, 2 Debuffs, 1 Buff, 1 Defend

### 7. Flash Powder
```python
{"id": "flash_powder", "name": "Flash Powder", "cooldown": 4,
 "power_type": "debuff", "damage_type": "magical", "trigger": "always",
 "status_apply": "blinded",
 "stat_mod": {"enemy": {"grace": -3, "might": -2}}, "mod_duration": 3}
```
**Description:** A pouch bursts into a brilliant cloud of powder, blinding and disorienting enemies. Stronger than Pocket Sand — longer duration, hits both grace and might. Synergizes with Counter Strike innate (blinded enemies roll poorly = free counters).
**Narrative:** The Rogue tosses the pouch — underhand, lazy, like feeding a dog. It bursts. Not smoke. Light. White, searing, absolute. The enemy's world becomes a sun with no edges. They swing blind. They miss. And every miss is a knife in the ribs from a direction they can't see. The Rogue doesn't need them to see. The Rogue just needs them to swing.

---

### 8. Tripwire
```python
{"id": "tripwire", "name": "Tripwire", "cooldown": 4,
 "power_type": "debuff", "damage_type": "physical", "trigger": "always",
 "status_apply": "ensnared",
 "stat_mod": {"enemy": {"grace": -3, "might": -2}}, "mod_duration": 3}
```
**Description:** The Rogue lays a hidden snare. The first careless step sends the victim crashing down. `ensnared` immobilizes — free hits for the Rogue. Synergizes with Opportunist innate (ensnared = status effect = +30% damage).
**Narrative:** The wire is thin — gut string, nearly invisible, stretched between two anchor points the enemy will never see. The enemy steps forward. The wire catches. The ground arrives. The enemy looks up from the dirt and sees the Rogue already above them, knife descending. The trap wasn't the wire. The trap was making the enemy think the ground was safe.

---

### 9. Knife Fan
```python
{"id": "knife_fan", "name": "Knife Fan", "cooldown": 4,
 "power_type": "strike", "damage_type": "physical", "trigger": "always",
 "hits": 2,
 "status_apply": "bleeding",
 "stat_mod": {"enemy": {"grace": -2}}, "mod_duration": 2}
```
**Description:** The Rogue throws multiple daggers in a wide arc. Two hits, both bleeding. Synergizes with Dirty Fighter innate (each hit applies a random debuff on top of bleeding) and Quick Hands innate (act first = throw before enemy can react).
**Narrative:** The Rogue's hands move — left, right, left — and three daggers leave the fingers in a spread that covers every angle the enemy could dodge toward. Two find their mark. The third was a distraction. The enemy learns this when they dodge into the second knife instead of away from it. And if the Rogue packed Dirty Fighter, each knife carries a little something extra — dust, oil, a wire. The bleeding is just the beginning.

---

### 10. Hook Chain
```python
{"id": "hook_chain", "name": "Hook Chain", "cooldown": 4,
 "power_type": "strike", "damage_type": "physical", "trigger": "always",
 "status_apply": "ensnared",
 "stat_mod": {"enemy": {"grace": -2, "armor_bonus": -2}}, "mod_duration": 2}
```
**Description:** A hooked chain whistles through the air, pulling the enemy off balance. Reduces armor — the Rogue doesn't just hurt you, they strip your protection. Synergizes with Opportunist innate (ensnared = +30% damage on next hit).
**Narrative:** The chain uncoils from the Rogue's wrist — fast, singing, aimed. The hook catches the enemy's belt, their shield strap, their confidence. The Rogue pulls. The enemy stumbles forward into a space they didn't choose, and the Rogue is already waiting in it. The armor gap that the chain exposed? The knife found it. Of course it did.

---

### 11. Feign Death
```python
{"id": "feign_death", "name": "Feign Death", "cooldown": 5,
 "power_type": "defend", "trigger": "low_hp",
 "self_status": "hidden",
 "stat_mod": {"self": {"grace": 3}}, "mod_duration": 3}
```
**Description:** The Rogue lies motionless, pretending to be defeated. When the enemy turns away, they spring back into action. Grants `hidden` to escape and reposition. Triggers when HP is low — the ultimate dirty trick.
**Narrative:** The blow lands — or seems to. The Rogue crumples. Goes still. Eyes open, blank, empty. The enemy grunts, turns to the next threat. And behind them, the corpse sits up, wipes the fake blood off its chin, and smiles. The enemy will never live this down. Literally — because the knife is already in their back.

---

### 12. Wall Run
```python
{"id": "wall_run", "name": "Wall Run", "cooldown": 4,
 "power_type": "buff", "trigger": "always",
 "self_status": "evasive",
 "stat_mod": {"self": {"grace": 4, "might": 2}}, "mod_duration": 3}
```
**Description:** The Rogue sprints across walls, turning impossible movement into reality. Grants `evasive` and boosts both grace and might — the Rogue fights from angles the enemy can't predict. Synergizes with Lucky Dodger innate (evasion stacks while evasive).
**Narrative:** The enemy swings low. The Rogue doesn't dodge — they run. Up the wall, across it, boots finding stone like it's flat ground. The enemy looks up, mouth open, and the Rogue drops from above with a knife in each hand and gravity on their side. The wall wasn't an obstacle. The wall was a platform. The enemy was just standing in the landing zone.

---

### 13. Sleight of Hand
```python
{"id": "sleight_of_hand", "name": "Sleight of Hand", "cooldown": 4,
 "power_type": "strike", "damage_type": "physical", "trigger": "opponent_status",
 "status_apply": "shaken",
 "stat_mod": {"self": {"might": 2}, "enemy": {"might": -3, "grace": -2}}, "mod_duration": 3}
```
**Description:** The Rogue's hands move faster than the eye can follow. They steal a small item — and the enemy's effectiveness drops. Only triggers when the enemy has a status effect. The enemy loses might and grace while the Rogue gains might. Synergizes with Con Artist innate (debuffs last +1 turn).
**Narrative:** The enemy is distracted — bleeding, blinded, choking. The Rogue brushes past them, casual as a pickpocket in a crowd. When they're done, the enemy's weapon feels lighter. Their grip feels weaker. Their pouch feels empty. The Rogue is already counting the coins. And if the Rogue packed Con Artist, the enemy won't figure out what's missing for two extra turns. By then, the Rogue will be three streets away.

---

## Expert Tier (Level 8, 400g, 1hr) — 3 Strikes, 1 Debuff, 1 Buff, 2 Defends

### 14. Mirror Image
```python
{"id": "mirror_image", "name": "Mirror Image", "cooldown": 5,
 "power_type": "buff", "trigger": "always",
 "self_status": "evasive",
 "stat_mod": {"self": {"grace": 5}}, "mod_duration": 3}
```
**Description:** Several identical Rogues scatter in different directions. The enemy can't tell which is real. Strongest evasion buff — +5 grace and `evasive`. Synergizes with Lucky Dodger innate (stacking evasion on each miss) and Counter Strike (every bad enemy roll = free counter damage).
**Narrative:** The Rogue splits. Not physically — perceptually. Three Rogues, four, each one running a different direction, each one looking back over its shoulder with the same grin. The enemy chases one. It vanishes. The real one is already behind them, and the knife is already moving. And every time the enemy swings at a fake, the real Rogue gets harder to hit. The copies aren't the trick. The copies are the distraction. The evasion is the trick.

---

### 15. Smoke Bomb
```python
{"id": "smoke_bomb", "name": "Smoke Bomb", "cooldown": 5,
 "power_type": "defend", "trigger": "always",
 "self_status": "hidden",
 "stat_mod": {"self": {"grace": 3, "cognition": 2}}, "mod_duration": 3}
```
**Description:** Dark smoke fills the battlefield instantly. The Rogue disappears behind thick cover. Grants `hidden` to reposition — the escape tool of choice. Synergizes with Quick Hands innate (act first = reposition before enemy can act).
**Narrative:** The pellet hits the ground and the world goes dark. Not a cloud — a wall. The enemy can't see their own hands. The Rogue can. They move through the smoke like it's home, and when the cloud clears, the enemy is alone, bleeding, and confused about which direction is safe. The smoke wasn't cover. The smoke was a stage. And the Rogue just left it.

---

### 16. False Surrender
```python
{"id": "false_surrender", "name": "False Surrender", "cooldown": 5,
 "power_type": "strike", "damage_type": "physical", "trigger": "low_hp",
 "status_apply": "stunned",
 "stat_mod": {"enemy": {"grace": -3, "might": -3}}, "mod_duration": 3}
```
**Description:** The Rogue kneels in apparent defeat, luring the enemy into overconfidence before striking unexpectedly. Applies `stunned` — the enemy is caught completely off guard. Triggers when HP is low. The dirtiest trick in the book.
**Narrative:** The Rogue drops to one knee. Hands up. Blade lowered. The enemy grins — victory, easy, done. They step forward to gloat. The Rogue's knife enters from below, from the angle that kneeling created, from the vulnerability that surrender performed. The enemy's grin doesn't have time to fade. It just stops. The Rogue stands up, dusts off their knees, and picks up the enemy's coin purse on the way out.

---

### 17. Misdirection
```python
{"id": "misdirection", "name": "Misdirection", "cooldown": 5,
 "power_type": "debuff", "damage_type": "magical", "trigger": "always",
 "status_apply": "shaken",
 "stat_mod": {"enemy": {"cognition": -4, "grace": -3, "might": -2}}, "mod_duration": 3}
```
**Description:** Everyone looks the wrong way. The Rogue redirects enemy attention with masterful misdirection. Devastates cognition, grace, and might — the enemy doesn't know what's real. Synergizes with Con Artist innate (debuffs last +1 turn) and Opportunist (+30% damage against debuffed).
**Narrative:** The Rogue points. The enemy looks. There's nothing there — but the enemy's body committed before their brain caught up. By the time they turn back, the Rogue has moved, the knife has moved, and the enemy's certainty about what's real has taken a permanent vacation. The Rogue didn't lie. The Rogue just let the enemy lie to themselves. That's worse.

---

### 18. Counter Stab
```python
{"id": "counter_stab", "name": "Counter Stab", "cooldown": 5,
 "power_type": "strike", "damage_type": "physical", "trigger": "opponent_status",
 "hits": 2,
 "status_apply": "bleeding",
 "stat_mod": {"self": {"might": 3, "grace": 2}, "enemy": {"might": -3, "grace": -2}},
 "mod_duration": 3}
```
**Description:** The Rogue exploits a debuffed enemy with a devastating two-hit counter. Only triggers when the enemy has a status effect. Empowers the Rogue while crushing the enemy — the ultimate follow-up to any dirty trick. Synergizes with Dirty Fighter innate (each hit adds a random debuff).
**Narrative:** The enemy is reeling — blinded, tripped, shaken. The Rogue doesn't wait for them to recover. Two stabs, fast, precise, from two different angles. The first opens a wound. The second opens a question: *how much worse can this get?* The answer is: worse. The Rogue is already setting up the next trick while the blood is still falling.

---

### 19. Escape Artist
```python
{"id": "escape_artist", "name": "Escape Artist", "cooldown": 4,
 "power_type": "defend", "trigger": "self_debuff",
 "self_status": "evasive",
 "stat_mod": {"self": {"grace": 4, "cognition": 2}}, "mod_duration": 3}
```
**Description:** Locks, ropes, and chains seem meaningless. The Rogue breaks free from any restraint. Only triggers when the Rogue is debuffed. Grants `evasive` — the Rogue slips free and becomes harder to hit. Synergizes with Slippery innate (25% chance to shake debuffs each turn).
**Narrative:** The chains tighten. The shadow clings. The enemy grins. The Rogue doesn't — they work. Fingers find the weak link, the bent pin, the gap in the mechanism. Three seconds. The chains fall. The Rogue stretches, rolls their neck, and looks at the enemy with the expression of someone who was never actually trapped. The enemy thought they had the Rogue. The enemy was wrong. The enemy is usually wrong.

---

### 20. Trickster's Flurry
```python
{"id": "tricksters_flurry", "name": "Trickster's Flurry", "cooldown": 5,
 "power_type": "strike", "damage_type": "physical", "trigger": "always",
 "hits": 3,
 "status_apply": "bleeding",
 "stat_mod": {"self": {"might": 3, "grace": 2}, "enemy": {"grace": -3, "might": -2}},
 "mod_duration": 3}
```
**Description:** The Rogue unleashes a flurry of three strikes, each one a different dirty trick. Empowers the Rogue while devastating the enemy. Max hits for the Rogue — three strikes, three wounds, three reasons to reconsider fighting a Rogue. Synergizes with Dirty Fighter innate (each hit adds a random debuff) and Quick Hands (act first = flurry before enemy can respond).
**Narrative:** The Rogue moves — not fast, but *busy*. Left hand flicks sand. Right hand slides a blade across the ribs. Left hand again, a tripwire that wasn't there a second ago. Three hits, three tricks, three wounds. The enemy doesn't know which one to block because they all look like the opening of a different attack. They're all the same attack. The Rogue just doesn't fight fair. Fair is for people who can't think of anything better.

---

## Master Tier (Level 15, 1000g, 1hr) — 4 Strikes, 1 Debuff, 1 Buff, 2 Defends

### 21. Lucky Escape
```python
{"id": "lucky_escape", "name": "Lucky Escape", "cooldown": 6,
 "power_type": "defend", "trigger": "low_hp",
 "self_status": "evasive",
 "stat_mod": {"self": {"grace": 5, "cognition": 3}}, "mod_duration": 3}
```
**Description:** With uncanny luck, every deadly attack narrowly misses the Rogue. They slip away from certain death. Grants `evasive` and massive grace — the ultimate survival tool. Triggers when HP is low. Synergizes with Lucky Dodger innate (evasion stacks) and Counter Strike (every bad enemy roll = free counter damage).
**Narrative:** The blade is at their throat. The arrow is in the air. The fire is closing in. And the Rogue... ducks. Not deliberately — instinctively, luckily, impossibly. Everything misses by an inch. The Rogue laughs, because what else can you do when death forgets your address? And every miss makes the next miss more likely. The Rogue isn't lucky. The Rogue just makes their own luck, and their own luck is very, very good at not being there.

---

### 22. Ambush Master
```python
{"id": "ambush_master", "name": "Ambush Master", "cooldown": 6,
 "power_type": "buff", "trigger": "opening_move",
 "self_status": "hidden",
 "stat_mod": {"self": {"might": 4, "grace": 4, "cognition": 2}}, "mod_duration": 4}
```
**Description:** The perfect hiding place becomes a deadly trap. The Rogue begins combat with every advantage. Opening move only — grants `hidden` and boosts might, grace, and cognition. Synergizes with Trap Master innate (first strike applies `ensnared`) and Opportunist (+30% damage against debuffed).
**Narrative:** The enemy walks through the clearing. Confident. Alert. Ready. They check the bushes, the trees, the shadows. The Rogue is above them — not in a tree, but on the branch they forgot to check. The drop is silent. The knife is certain. The enemy never finishes their patrol. And if the Rogue packed Trap Master, the landing comes with a wire that wraps around the enemy's ankles before they can scream. The ambush wasn't the drop. The ambush was everything after.

---

### 23. Grand Heist
```python
{"id": "grand_heist", "name": "Grand Heist", "cooldown": 6,
 "power_type": "strike", "damage_type": "physical", "trigger": "opponent_wounded",
 "status_apply": "shaken",
 "stat_mod": {"self": {"might": 3, "grace": 3}, "enemy": {"armor_bonus": -5, "might": -3}},
 "mod_duration": 4}
```
**Description:** The target realizes too late that something is missing. The Rogue steals the enemy's armor protection mid-fight. Only triggers when the enemy is wounded. The Rogue doesn't just hurt you — they rob you. Synergizes with Opportunist innate (shaken = +30% damage) and Con Artist (debuffs last longer).
**Narrative:** The enemy is wounded, distracted, trying to survive. The Rogue slides in — not to kill, but to take. Fingers find straps, buckles, the pin that holds the pauldron. When the Rogue steps back, the enemy's chest plate is gone. The enemy looks down. The Rogue looks up. Neither says a word. The enemy's armor is on the ground. The Rogue's knife is in the gap where it used to be. The heist wasn't the theft. The heist was making the enemy think the armor mattered.

---

### 24. Coin Toss
```python
{"id": "coin_toss", "name": "Coin Toss", "cooldown": 5,
 "power_type": "debuff", "damage_type": "magical", "trigger": "always",
 "status_apply": "shaken",
 "stat_mod": {"enemy": {"cognition": -4, "grace": -3, "might": -3, "insight": -2}}, "mod_duration": 3}
```
**Description:** A spinning coin catches the target's eyes just long enough for an opening. The enemy's mind goes blank with confusion. Devastates four enemy stats — the ultimate misdirection. Synergizes with Con Artist innate (debuffs last +1 turn) and Opportunist (+30% damage against debuffed).
**Narrative:** The Rogue flips a coin — gold, spinning, catching the light. The enemy's eyes follow it. Up. Down. Around. And while they're watching the money, the Rogue takes everything else: their focus, their balance, their certainty about which hand the knife is in. The coin lands. The enemy doesn't. And if the Rogue packed Con Artist, the enemy won't remember which way is up for two extra turns. The coin wasn't the trick. The coin was the distraction. The trick was everything that happened while they were watching.

---

### 25. Shadow Step
```python
{"id": "shadow_step", "name": "Shadow Step", "cooldown": 6,
 "power_type": "defend", "trigger": "always",
 "self_status": "hidden",
 "stat_mod": {"self": {"grace": 4, "cognition": 3}}, "mod_duration": 3}
```
**Description:** The Rogue vanishes from one position and appears in another, instantly. Grants `hidden` — the repositioning tool for advanced Rogues. Synergizes with Quick Hands innate (act first = vanish before enemy can act) and Counter Strike (hidden = enemy rolls poorly = free counter).
**Narrative:** The enemy blinks. The Rogue is gone. Not behind the pillar, not behind the wall — just gone. Then the knife arrives from a direction that doesn't make sense. The enemy turns toward it. The Rogue is already somewhere else. The shadow wasn't hiding. The shadow was moving. And the Rogue was inside it, riding it to the next angle, the next opening, the next impossible strike.

---

### 26. Master Picklock
```python
{"id": "master_picklock", "name": "Master Picklock", "cooldown": 6,
 "power_type": "strike", "damage_type": "physical", "trigger": "opponent_wounded",
 "status_apply": "ensnared",
 "stat_mod": {"enemy": {"armor_bonus": -6, "grace": -3, "cognition": -2}}, "mod_duration": 3}
```
**Description:** Complex mechanisms click open effortlessly. The Rogue "unlocks" the enemy's defenses, dismantling their protection. Only triggers when the enemy is wounded. Applies `ensnared` — the enemy is locked in place while their armor falls apart. Synergizes with Opportunist innate (+30% damage against debuffed).
**Narrative:** The enemy's guard is a lock. The Rogue is a key. They don't force it — they read it, feel it, find the tumblers. One twist, two, three. The enemy's defense opens like a door that forgot it was supposed to stay shut. The Rogue steps through. The enemy wonders how they got in. And now they can't move, can't run, can't adjust. The lock wasn't the enemy's guard. The lock was the enemy's certainty. The Rogue just picked it.

---

### 27. King of Thieves
```python
{"id": "king_of_thieves", "name": "King of Thieves", "cooldown": 6,
 "power_type": "strike", "damage_type": "physical", "trigger": "opponent_status",
 "status_apply": "shaken",
 "stat_mod": {"self": {"might": 4, "grace": 3, "cognition": 2}, "enemy": {"might": -4, "grace": -3, "cognition": -3}},
 "mod_duration": 4}
```
**Description:** No treasure is truly safe. The Rogue steals the enemy's power and claims it for themselves. Only triggers when the enemy has a status effect. The Rogue gains might, grace, and cognition while the enemy loses all three — the ultimate exploitation. Synergizes with Dirty Fighter innate (random debuff on hit) and Con Artist (debuffs last longer).
**Narrative:** The enemy has power — strength, speed, wit. The Rogue doesn't need any of it. They need a moment, and the enemy is kind enough to provide one. When it's done, the enemy is slower, weaker, dimmer. The Rogue is faster, sharper, meaner. The enemy looks at their hands and doesn't recognize them. The Rogue looks at their own hands and likes what they see. The theft wasn't the stats. The theft was the confidence. And the enemy just ran out.

---

### 28. Trickster's Gambit
```python
{"id": "tricksters_gambit", "name": "Trickster's Gambit", "cooldown": 6,
 "power_type": "strike", "damage_type": "physical", "trigger": "always",
 "hits": 3,
 "status_apply": "bleeding",
 "stat_mod": {"self": {"might": 4, "grace": 3}, "enemy": {"might": -3, "grace": -3, "armor_bonus": -3}},
 "mod_duration": 4}
```
**Description:** The Rogue bets everything on one impossible sequence — three strikes, each one a different trick, each one stealing something from the enemy. Empowers the Rogue while devastating enemy stats and armor. The master-level flurry. Synergizes with Dirty Fighter innate (each hit adds a random debuff) and Quick Hands (act first = flurry before enemy can respond).
**Narrative:** The Rogue looks at the odds — three enemies, one knife, no escape. They should run. They don't. They grin, crack their neck, and throw themselves into the middle of it. Three strikes, three angles, three tricks. The first takes blood. The second takes balance. The third takes armor. The gamble is insane. The Rogue is insane. That's why it works. And if the Rogue packed Quick Hands, there's a fourth strike that takes something else — dignity, maybe. Or coins.

---

## Legendary Tier (Level 20, 2500g, 1 day — Quest-gated) — 2 True-Damage Strikes

### 29. Perfect Crime
```python
{"id": "perfect_crime", "name": "Perfect Crime", "cooldown": 8,
 "power_type": "strike", "damage_type": "true", "trigger": "opponent_wounded",
 "status_apply": "bleeding",
 "self_status": "hidden",
 "stat_mod": {"enemy": {"might": -5, "grace": -5, "armor_bonus": -6, "cognition": -4}},
 "mod_duration": 4}
```
**Description:** Nothing suggests the Rogue was ever there. True damage ignores all defense. The enemy doesn't understand what happened. Grants `hidden` — the Rogue vanishes after the strike. Only triggers when the enemy is wounded. The ultimate expression of dirty fighting: strike, rob, disappear. Synergizes with all innate skills — the perfect capstone for any loadout.
**Narrative:** The enemy is standing. Then they're not. There's no sound, no flash, no warning. Just a cut that appears on their throat like it was always there. They look around for the attacker. There's no one. They look down at the blood. There's no weapon. They look at their stats — diminished, drained, dismantled. The Rogue was here. The Rogue is gone. There is no evidence. There never is. And every innate skill the Rogue packed — Dirty Fighter, Con Artist, Trap Master — they all fired at once. The enemy didn't lose to a trick. They lost to all the tricks, simultaneously, and they'll never know which one was the one that killed them.

**Quest: The Untraceable Hand**
- **Trainer:** Vex Elenor (Elaris)
- **Min Level:** 20
- **Objectives:**
  - Kill 5 Silverroad bandits in Concordia
  - Gather 3 Relic Shards
  - Learn at least 5 Rogue skills from Vex Elenor
- **Reward:** Unlocks Perfect Crime

---

### 30. Legend of Trickery
```python
{"id": "legend_of_trickery", "name": "Legend of Trickery", "cooldown": 10,
 "power_type": "strike", "damage_type": "true", "trigger": "low_hp",
 "status_apply": "stunned",
 "self_status": "hidden",
 "stat_mod": {"enemy": {"might": -6, "grace": -6, "armor_bonus": -8, "cognition": -5, "insight": -4},
 "mod_duration": 5}
```
**Description:** Reality itself seems to bend around every deception. The Rogue becomes the greatest trickster alive. True damage ignores all defense. Devastates every enemy stat. Grants `hidden`. Only usable when HP is low — the last trick, the biggest trick, the trick that ends the fight. Synergizes with all innate skills at once — the ultimate expression of the Adaptive Trickster.
**Narrative:** The Rogue is cornered. Wounded. Out of tricks. And then — they smile. Not a grin. Not a bluff. A real smile, the kind that says *you think you've won*. The shadows bend. The light lies. The enemy sees three Rogues, then none, then six. Their sword hits nothing. Their shield blocks nothing. Their certainty becomes the biggest lie on the battlefield. And when the Rogue finally strikes — from where? from nowhere? from everywhere? — the enemy falls without understanding what happened. Because there was nothing to understand. There was only the trick, and they were the mark. And every innate skill the Rogue ever packed — Quick Hands, Counter Strike, Dirty Fighter, Lucky Dodger, all of them — they all fire at once. The Rogue doesn't fight like one Rogue. The Rogue fights like all of them. Every trick, every angle, every dirty trick that ever worked — all at once, all at the same time, all aimed at the same enemy who thought they had the Rogue cornered. They didn't. They never did. They never will.

**Quest: The Untraceable Hand**
- **Trainer:** Vex Elenor (Elaris)
- **Min Level:** 20
- **Objectives:**
  - Complete "The Untraceable Hand" quest (learn Perfect Crime first)
  - Kill 1 Heritage Boss
  - Gather 1 Jahra Ingot
  - Learn at least 15 Rogue skills total
- **Reward:** Unlocks Legend of Trickery
