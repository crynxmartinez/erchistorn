# Erchistorn — Game Improvement Plan

> Generated from a full game audit on Jul 26, 2026.
> The game has massive content (1,577 items, 236 monsters, 39 biomes, 19 professions)
> but lacks **depth of decision-making**. These improvements address the boredom timeline.

---

## Boredom Timeline (Current State)

| Player Type | Time to Boredom | Primary Reason |
|---|---|---|
| Casual | 3-5 days | Core loop is fun but combat gets repetitive |
| Regular | 1-2 weeks | Runs out of new skills, quests feel samey |
| Hardcore | 2-3 weeks | Only heritage bosses left, no endgame grind |
| Completionist | 3-4 weeks | All professions maxed, all biomes explored, nothing new |

---

## Priority 1: Combat Overhaul

**Problem:** Combat is fully automated — player clicks "Roll" and watches. No real decisions mid-fight. After 20-30 fights, players spam through without reading.

**Goal:** Make every combat turn a meaningful decision.

### 1A. Innate Actions System (Replaces AUTO Button)

**Concept:** The current AUTO button is replaced with a **dropdown of innate actions** — always-available combat stances that cost no cooldowns or resources. Skills become optional overrides on top of the chosen stance.

**The 6 Innate Actions:**

| Action | Effect | Risk | Best Use |
|---|---|---|---|
| **Strike** | Basic attack. Full d6 roll (1-6). Normal damage multiplier. | None — safe default | When you're winning, no threat |
| **Defend** | No attack. -50% incoming damage next monster turn. Self-heal 5% max HP. | Give up your turn's damage | Telegraph shows heavy hit coming |
| **Evade** | No attack. Roll d6 for dodge: **4+ = nullify** monster's next attack. **1-3 = take FULL damage** (no defense). | High risk — fail = full damage | Telegraph shows devastating hit, low HP, defend not enough |
| **Aim** | Attack with **advantage** (roll 2d6, keep higher). Damage multiplier capped at 1.2x (no 1.6x crit). | Lower damage ceiling | Fighting high-evasion enemies, keep missing |
| **Counter** | Defensive stance. If monster **attacks** next turn and you survive → **free counter-strike** (auto outcome 4, ~0.9x damage). If monster uses heal/buff/debuff → counter wasted. | Wasted if monster doesn't strike | Expect a basic attack, want to punish |
| **Focus** | No attack. Restore **+2 skill capacity**. Next skill used gets **+1 dice outcome** (max 6). | Skip a turn of damage | Need to set up a big skill burst next turn |

**How Innate Actions interact with Skills and Items:**
- **Innate Action** = base stance for the turn (chosen from dropdown, replaces AUTO)
- **Skill** = optional override — if you pick a skill, it replaces your innate action's *attack portion*
  - Strike skill + Defend stance = you defend but also strike with the skill
  - Heal skill + Focus stance = you heal AND get the focus bonus next turn
  - Strike skill + Aim stance = skill damage rolled with advantage but capped
- **Item** = always usable alongside any stance (doesn't replace the stance)
- **Flee** = separate button, not part of the innate dropdown (always visible in corner)

**UI Layout:**
```
┌─────────────────────────────────────────────────┐
│  Monster telegraph (when available)             │
│  ⚠ "The Orc Brute raises its weapon —          │
│     a heavy strike is coming!"                  │
│  [Heavy Strike] [Physical] ~8-15 dmg            │
├─────────────────────────────────────────────────┤
│  Innate Action: [ Strike ▼ ]                    │
│    ├── Strike                                   │
│    ├── Defend                                   │
│    ├── Evade                                    │
│    ├── Aim                                      │
│    ├── Counter                                  │
│    └── Focus                                    │
├─────────────────────────────────────────────────┤
│  [ SKILL ]  [ ITEM ]          Combo: ×3 🔥      │
├─────────────────────────────────────────────────┤
│  (Skill sub-panel opens when SKILL clicked)     │
│  [ Shield Bash (CD:2) ] [ Sworn Strike (CD:3) ] │
│  [ Cancel ]                                     │
├─────────────────────────────────────────────────┤
│              [ ACT / STRIKE ]                   │
└─────────────────────────────────────────────────┘
```

### 1B. Enemy Telegraphing
- At the start of each enemy turn, show a **telegraph** of what the monster is about to do:
  - "The Orc Grunt raises its weapon — heavy strike incoming!"
  - "The Bog Hag begins chanting — debuff incoming!"
  - "The Crystal Lurker coils — it's preparing to heal!"
- Player can then choose to Defend, use a skill, or take the hit
- Telegraphs are based on the monster's AI logic (already exists in `_pick_monster_skill`)

### 1C. Combo System
- Consecutive successful hits build a **combo counter** (1x, 1.2x, 1.5x, 2x damage)
- Using the same skill twice in a row resets combo
- Missing an attack resets combo
- Defending preserves combo but doesn't build it
- Adds a risk/reward layer — do you keep attacking or play safe?

### 1D. Status Effect Visibility
- Show active status effects on both player and monster as icons with turn counters
- Hovering shows effect description
- Color-coded: green (buff), red (debuff), yellow (neutral)

### Files to Modify
- `backend/game_engine.py` — split combat_turn into player_act/monster_act, innate action resolution, combo tracking, telegraph generation, counter-strike logic, evade dice logic, focus/skill capacity restoration
- `backend/server.py` — new `/game/combat/act` + `/game/combat/resolve` endpoints, new action payload model with `action_type` field
- `frontend/src/components/CombatScreen.jsx` — innate action dropdown, telegraph banner, combo meter, skill/item sub-panels, monster status pills, two-phase turn flow (act → resolve)

### Estimated Effort: 4-5 sessions

---

## Priority 2: Skill Expansion + Talent Trees

**Problem:** Only 23 skills total (~2 per mastery). Players see everything within hours. No unlock progression, no build diversity.

**Goal:** Give players meaningful choices about how to build their character.

### 2A. Expand Skill Pool (Target: 55+ skills)
- Add 3-5 skills per mastery (currently 11 masteries):
  - **Knight:** Shield Bash, Sworn Strike, Shield Wall, Taunt, Last Stand
  - **Paladin:** Smite, Lay on Hands, Divine Shield, Judgement, Holy Aura
  - **Lancer:** Thrust, Impale, Spear Sweep, Pin, Phalanx
  - **Rogue:** Backstab, Vanish, Shadow Strike, Poison Coating, Sleight
  - **Bard:** Mocking Verse, Rally, Dissonance, Lullaby, Encore
  - **Alchemist:** Mix Potion, Acid Flask, Smoke Bomb, Transmute, Catalyst
  - **Mage:** Arcane Bolt, Ward, Fireball, Ice Lance, Mana Surge
  - **Priest:** Divine Light, Purge, Bless, Sanctuary, Resurrect
  - **Druid:** Thornlash, Beast Call, Regrowth, Entangle, Primal Form
  - **Assassin:** Shadow Step, Poison Blade, Execute, Mark of Death, Blur
  - **Hunter:** Aimed Shot, Trap, Volley, Tracking, Beast Bond

### 2B. Skill Book Drop System
- Skill books drop from:
  - Bosses (guaranteed 1 per kill)
  - Rare monsters (5% chance)
  - Event rewards
  - Heritage vendor (token cost)
  - Quest rewards
- Using a skill book teaches the skill instantly (no training time)
- Duplicate skill books can be combined to **upgrade** the skill (+1 power per tier, max +5)

### 2C. Talent Point System
- Players earn 1 talent point per level starting at level 5
- Each mastery has a mini talent tree (5 nodes):
  - Node 1: +5% damage with mastery skills
  - Node 2: -1 cooldown on mastery skills
  - Node 3: Unlock ultimate skill (requires mastery rank 3)
  - Node 4: +10% effect potency (healing, debuff duration, etc.)
  - Node 5: Passive bonus (e.g., Knight: "20% chance to block when defending")
- Points are allocated via UI, can be reset for gold cost

### Files to Modify
- `backend/game_data.py` or new `backend/game_data_skills.py` — expanded skill definitions
- `backend/server.py` — talent point endpoints, skill book use/upgrade endpoints
- `backend/game_engine.py` — talent modifiers in combat calculations
- `frontend/src/components/SkillsPanel.jsx` — talent tree UI, skill book use UI

### Estimated Effort: 4-5 sessions

---

## Priority 3: Endgame Dungeon

**Problem:** No endgame content past level ~30. Heritage bosses are once per month. Hardcore players have nothing to grind.

**Goal:** Provide an infinite, replayable challenge with escalating rewards.

### 3A. The Abyssal Rift
- Accessible from any hometown via a "Rift Gate" NPC
- Procedurally generated floors — each floor has:
  - 1-3 combat encounters (random monsters scaled to floor depth)
  - Chance of a treasure room (chests with loot)
  - Chance of an event room (shrine, merchant, mystery)
  - Boss every 5 floors (scaled heritage boss variant)
- Player chooses to **descend deeper** or **extract with loot** after each floor
- If player dies in the rift, they lose all rift loot but keep XP earned
- No cooldown — can re-enter anytime, but each run starts from floor 1

### 3B. Floor Modifiers
- Every 5 floors, a random modifier is applied:
  - "Glass Cannon" — all damage doubled (both sides)
  - "Healing Decay" — healing effectiveness reduced 20% per floor
  - "Monster Surge" — +1 monster per encounter
  - "Time Pressure" — 30 second timer per combat turn
  - "No Items" — consumables disabled
  - "Skill Lock" — random skill disabled each floor
- Modifiers stack as you descend deeper

### 3C. Rift Rewards
- **Rift Shards** — currency earned from clearing floors, spent at a rift vendor for:
  - Exclusive cosmetic titles ("Riftwalker", "Abyssal Descender")
  - Unique equipment not craftable or droppable elsewhere
  - Rift-themed pets and cosmetics
- **Rift Leaderboard** — deepest floor reached, fastest clear, most shards earned
- **Weekly Rift Challenge** — a seeded rift with fixed modifiers, same for all players, leaderboard ranked

### 3D. Rift Progression
- Track per-character:
  - Deepest floor reached
  - Total rift runs
  - Total rift shards earned
  - Boss kills in rift
- Milestone rewards at floor 10, 25, 50, 100

### Files to Create/Modify
- `backend/rift_system.py` (new) — floor generation, modifiers, reward logic
- `backend/server.py` — rift endpoints (enter, action, extract, leaderboard)
- `backend/game_engine.py` — rift combat scaling
- `frontend/src/components/RiftPanel.jsx` (new) — rift UI
- `frontend/src/pages/Game.jsx` — add rift access

### Estimated Effort: 5-6 sessions

---

## Priority 4: Quest Variety + Achievements

**Problem:** Every quest is "kill X" or "gather Y". No puzzles, no choices, no exploration challenges. No achievement system means no long-term goals.

**Goal:** Diversify quest types and give players meta-goals to chase.

### 4A. New Quest Types

**Puzzle Quests:**
- Riddle quests — NPC gives a riddle, player must find the answer item/location
- Item combination quests — "Bring me a Wild Herb and a Serpent Venom to brew a cure"
- Cipher quests — decode a message using hints from NPC dialogue
- Maze quests — navigate to a specific biome location within a time limit

**Escort Quests:**
- NPC travels with player through a biome
- Must protect NPC from encounters (NPC has HP, can be healed)
- If NPC survives → bonus reward; if NPC dies → partial reward only
- NPC provides dialogue/story during the escort

**Timed Challenges:**
- "Defeat 5 monsters in Golden Plains within 10 minutes"
- "Gather 20 resources before the node depletes"
- "Craft 5 items in one session"
- Timer displayed prominently in UI

**Multi-Stage Quests:**
- Stage 1: Gather materials → Stage 2: Craft a key item → Stage 3: Use item at a location → Stage 4: Fight a boss
- Each stage unlocks the next
- Failure at any stage resets to the beginning (or checkpoint)

**Choice Quests:**
- NPC presents a moral dilemma
- Player chooses between 2-3 options
- Each choice leads to different rewards and different follow-up quests
- Choices affect NPC relationship and available quests later

### 4B. Achievement System (100+ achievements)

**Categories:**
- **Combat:** First kill, 100 kills, 1000 kills, kill one of each rarity, boss slayer
- **Gathering:** First gather, 500 gathers, gather from every biome, rare node harvester
- **Crafting:** First craft, 100 crafts, masterwork crafter, craft one of each kind
- **Exploration:** Discover all biomes, visit all towns, activate all waystones, reach all continents
- **Heritage:** Participate in all 8 heritage months, kill all 8 heritage bosses, earn 1000 total tokens
- **Skills:** Learn 10 skills, learn all skills for a mastery, upgrade a skill to +5
- **Social:** Claim 100 daily missions, complete 50 quests, max NPC relationship with 5 NPCs
- **Special:** First death, survive with 1 HP, kill a monster 20 levels higher, craft with all 6 outcomes
- **Rift:** Reach floor 10/25/50/100, kill 10 rift bosses, earn 1000 rift shards

**Rewards:**
- Titles (displayed next to character name)
- Cosmetic badges on profile
- Small permanent bonuses (e.g., +1% XP, +5 max HP)
- Exclusive items for milestone achievements

### 4C. Title System
- Earned through achievements, quest completions, heritage milestones
- Displayed next to character name in UI and leaderboard
- Examples: "Slayer of the Oathbreaker", "Master Forger", "Riftwalker", "Heritage Champion"
- Player can equip one title at a time

### 4D. Profile Page
- View character stats, achievements, titles, play time
- Show key milestones (first boss kill, deepest rift floor, heritage participation)
- Compare with leaderboard
- Shareable profile link

### Files to Create/Modify
- `backend/achievements.py` (new) — achievement definitions, check logic, reward grants
- `backend/server.py` — achievement endpoints, new quest type handlers
- `backend/game_data_p2.py` — new quest type definitions
- `backend/npcs.py` — escort NPC logic, choice quest dialogue
- `frontend/src/components/AchievementPanel.jsx` (new) — achievement UI
- `frontend/src/components/QuestModal.jsx` — support new quest types
- `frontend/src/components/CharacterSheet.jsx` — title display, profile page

### Estimated Effort: 5-6 sessions

---

## Priority 5: Social Features (Future)

**Problem:** No guilds, no trading, no chat, no co-op. Single-player only.

### 5A. Player-to-Player Trading
- Direct item/gold trade between online players
- Trade window with confirm/cancel on both sides
- Trade history log

### 5B. Guild System
- Create/join guilds (max 50 members)
- Guild storage (shared inventory)
- Guild quests — contribute to guild goals for rewards
- Guild leaderboard
- Guild hall (cosmetic customization)

### 5C. Async PvP — Arena of Champions

**Concept:** Players build a **PvP Defense Loadout** — a set of 10 skill slots and an innate action strategy that their character uses to auto-defend when challenged by another player. This works **even while offline**. The attacker plays actively (using the new combat action menu); the defender is AI-controlled based on their loadout.

**Core Principle:** Your character is always "live" in the arena. Other players can challenge your ghost at any time. You don't need to be online to defend — but your defense is only as good as the loadout you set up.

---

#### 5C-1. PvP Defense Loadout (10 Skill Slots)

**Separate from the PvE skill bar:**
- PvE skill bar stays as-is (existing `skill_bar` field, used for monster combat)
- New `pvp_defense_bar` field — 10 slots for skills the character will use when defending in PvP
- Players assign skills from their learned skills into these 10 slots
- Skill cooldowns still apply — the AI will respect cooldowns during defense
- Skill capacity still applies — the AI won't use more skills than capacity allows per encounter

**Defense Strategy Settings:**
Along with the 10 skill slots, the player configures a **defense strategy** that controls how the AI behaves:

| Strategy | Behavior |
|---|---|
| **Aggressive** | AI prefers strike skills, uses Defend rarely, prioritizes high-damage combos |
| **Balanced** | AI mixes attack and defend based on HP ratio, uses heal skills at 50% HP |
| **Defensive** | AI leads with buffs/defends, uses heal skills at 70% HP, counters more |
| **Counter** | AI uses Counter innate action frequently, punishes attacker aggression |
| **Evade** | AI uses Evade frequently, tries to dodge heavy telegraphed hits |

**Innate Action Priority:**
Player also sets a priority order for innate actions when defending:
- Example: `[Evade, Counter, Defend, Strike, Aim, Focus]`
- AI uses this priority when deciding which innate action to take each turn, modified by the telegraph and current HP

**PvP Defense Item Bar:**
- Separate 5-slot item bar for PvP defense (`pvp_item_bar`)
- AI auto-uses items based on triggers (same trigger system as PvE pre-combat items)
- Example: Healing Potion with `hp_below_50` trigger → AI uses it when HP drops below 50%

---

#### 5C-2. The Attacker's Experience

**Challenging another player:**
- Browse the **Arena leaderboard** or search by player name
- See the defender's: character name, level, race, mastery, title, win/loss record, rank tier
- **Cannot see** the defender's: defense loadout, skill bar, item bar, or strategy (surprise element)
- Click **Challenge** → enter combat using the new two-phase combat system
- The attacker plays actively — picking innate actions, skills, items, reacting to telegraphs
- The defender is AI-controlled based on their loadout + strategy

**Combat rules:**
- Both players use their real stats, equipment, and level
- No consumables lost in PvP (items used in PvP don't deplete inventory)
- No XP loss, no gold loss, no item loss
- Best-of-5 rounds — first to 3 round wins takes the match
- Each round: both start at full HP, fight until one drops to 0
- 30-second turn timer for the attacker (if timer expires, auto-Strike)

**After the match:**
- Attacker sees: full replay log, defender's loadout revealed, rating change
- Defender (when they log in): sees a **PvP Defense Report** notification — who attacked, win/loss, replay, rating change

---

#### 5C-3. Arena Ranking System

**Rating Tiers:**
| Tier | Rating Range | Reward |
|---|---|---|
| Bronze | 0-999 | Basic arena tokens |
| Silver | 1000-1499 | +10% arena tokens |
| Gold | 1500-1999 | +25% arena tokens, exclusive cosmetic |
| Platinum | 2000-2499 | +50% arena tokens, title "Arena Challenger" |
| Diamond | 2500-2999 | +75% arena tokens, title "Arena Veteran", exclusive equipment |
| Champion | 3000+ | +100% arena tokens, title "Arena Champion", legendary cosmetic |

**Rating calculation:**
- Win vs higher-rated opponent → +25-35 rating
- Win vs lower-rated opponent → +10-20 rating
- Loss vs higher-rated opponent → -5-10 rating
- Loss vs lower-rated opponent → -15-25 rating
- Rating updates after each match for both attacker and defender
- Seasonal reset every 3 months (rating soft-resets to 1000, keep tier rewards)

**Leaderboards:**
- Global top 100
- Per-tier leaderboards
- Weekly leaderboard (most matches won this week)
- "Most successful defender" leaderboard (highest defense win rate, min 10 defenses)

---

#### 5C-4. Arena Rewards

**Arena Tokens** (earned from both attacking and defending):
- Win as attacker: 10-30 tokens (scaled by opponent rating)
- Win as defender: 15-40 tokens (bonus for successful defense)
- Lose as attacker: 3 tokens (participation)
- Lose as defender: 5 tokens (consolation)
- Daily bonus: first 3 matches each day give 2x tokens

**Arena Vendor:**
- Exclusive PvP-themed equipment (stat-stick gear with PvP-specific bonuses)
- PvP cosmetics (arena outfits, weapon skins, victory poses)
- PvP titles
- **PvP-only consumables** (one-time use per match, don't deplete):
  - Arena Potion — heal 30% max HP (1 per match)
  - Arena Bomb — 15 true damage (1 per match)
  - Arena Shield — absorb 20 damage (1 per match)

**Seasonal Rewards:**
- End of each 3-month season: tier-based rewards mailed to player
- Top 10 players get exclusive seasonal title + legendary cosmetic
- Participation reward for playing at least 10 matches per season

---

#### 5C-5. PvP Defense Report

**When the defender logs in after being attacked:**
- Modal popup: "You were challenged by [Player Name] while away!"
- Shows: match result (won/lost), rounds won/lost, rating change, replay log
- Player can watch the full replay turn-by-turn
- Multiple attacks show as a list — player can review each one
- "Defense Stats" panel: total defenses, win rate, most common attacker strategies

**Defense notifications:**
- In-game notification badge on the Arena panel
- Optional: push notification (if enabled) — "Your character was challenged in the Arena!"

---

#### 5C-6. Matchmaking & Attack Limits

**Matchmaking:**
- Attacker can challenge anyone within ±500 rating of their own rating
- Attacker can challenge anyone outside that range but with reduced rewards
- Cannot challenge the same player more than 3 times per day
- Cannot challenge players on your friends list (friendly matches separate)

**Attack limits:**
- Max 10 attacks per day (attacker side)
- No limit on how many times you can be attacked (defender side)
- Cooldown: 5 minutes between attacks
- First match of the day: bonus tokens

**Offline defense:**
- Character auto-defends using `pvp_defense_bar` + strategy settings
- If player has no PvP defense loadout set → character uses basic Strike only (easy win for attacker)
- Encourages players to set up their defense loadout early

---

#### 5C-7. Guild Wars (Future Extension)

- Guild vs guild async battles
- Each guild member's defense loadout contributes to guild defense
- Attacking guild picks which defender to challenge
- Guild war score based on total wins
- Seasonal guild war rewards

### Files to Create/Modify
- `backend/pvp_system.py` (new) — arena matchmaking, defense AI, rating calculation, replay storage
- `backend/server.py` — PvP endpoints (challenge, defend, leaderboard, defense loadout setup, replay retrieval)
- `backend/game_engine.py` — PvP combat variant (attacker active + defender AI, best-of-5 rounds, no loot loss)
- `frontend/src/components/ArenaPanel.jsx` (new) — leaderboard browse, challenge, defense loadout setup, strategy config
- `frontend/src/components/CombatScreen.jsx` — PvP combat mode (attacker side, 30s timer, round counter)
- `frontend/src/components/PvPReportModal.jsx` (new) — defense report modal, replay viewer
- `frontend/src/components/SkillsPanel.jsx` — add PvP defense bar tab (10 slots, separate from PvE skill bar)

### 5D. World Chat
- Global chat channel
- Trade channel (for market listings)
- Guild chat
- Profanity filter + moderation

### Estimated Effort: 10-12 sessions (PvP alone is 6-7)

---

## Priority 6: Crafting Depth (Future)

### 6A. Material Substitution
- Using higher-tier materials improves craft odds or output quality
- Optional material slots — add gems/essences for bonus effects

### 6B. Craft Minigame
- Timing bar or sequence matching for quality bonus
- Perfect timing = guaranteed masterwork

### 6C. Discovery System
- Combine unknown materials to discover new recipes
- Recipe journal tracks discovered vs undiscovered

### 6D. Equipment Set Bonuses
- Collect 3/5/7 pieces of a themed set for bonus effects
- Set pieces drop from specific bosses or regions

### Estimated Effort: 4-5 sessions

---

## Priority 7: Sanctuary System (Death & Recovery)

**Problem:** When HP hits 0, the player just drops to 1 HP and the combat ends. No real death penalty, no respawn location, no recovery mechanic. The old "Inn" was just a rest button with no narrative weight.

**Goal:** Replace the Inn with a **Sanctuary** — one per continent, located in the first town (hometown). Serves as the player's respawn point on death, a safe zone from PvP, a place to rest and receive blessings, and a social hub showing who else is recovering.

### 7A. Inn → Sanctuary Rename
- **Only hometowns (first towns) have Sanctuary** — all other towns lose the inn/sanctuary service entirely
- 8 sanctuaries total, one per continent:
  - Oathspire (Valeria), Grunhold (Mushkara), Elaris (Concordia), Jahrahold (Khardrum), Solunara (Haya), Rindivar Grove (Gennel), Atlantyrion (Hylion), Veilgrove (Daw'ul Talalu)
- Non-hometown towns (Riverguard, Warforge, Silvergate, Deepstone, Starfall Watch, Beastcairn) keep Market/Trainers/etc but **no Sanctuary**
- Endpoint: `/game/town/inn` → `/game/town/sanctuary`
- Frontend: tab label, button text, descriptions all updated
- Sanctuary description: "A sanctified hall where the wounded are mended and the fallen are restored. Rest here to heal, or wake here after defeat."

### 7B. Death → Sanctuary Teleport (PvE)
- When player HP reaches 0 in combat:
  - Combat ends (existing behavior)
  - Player is **teleported** to their `last_sanctuary_town` (the hometown of their current continent)
  - HP restored to 50% (not full — death has a cost)
  - Gold loss: existing 20g penalty retained
  - **"Recovering" debuff applied**: -10% damage for 3 actions
  - `current_biome` set to None (you're in town now)
  - `current_town` set to sanctuary town
  - Death count incremented: `deaths += 1`
  - Last death info recorded: `last_death = {"cause": monster_name, "location": biome_id, "timestamp": now}`
- If player has no `last_sanctuary_town` set → default to their home town

### 7C. Death → Sanctuary Teleport (PvP, Future)
- When player is attacked offline and defeated in PvP:
  - Character respawns at `last_sanctuary_town`
  - "Recovering" debuff applied
  - On next login: **Sanctuary Recovery screen** shows first
    - "You were defeated by [Player Name] in the Arena. You wake in the Sanctuary at [Town Name]."
    - Shows match replay link
    - Option to pay for Sanctuary Cleansing (remove debuff) or proceed with debuff
- Sanctuary town = **PvP safe zone** — cannot be challenged while in a Sanctuary town

### 7D. Sanctuary Services

| Service | Cost | Effect |
|---|---|---|
| **Rest** (voluntary) | `sanctuary_cost` gold | Full HP restore, clear debuffs, clear exhaustion |
| **Sanctuary Cleansing** | `sanctuary_cost × 2` gold | Remove "Recovering" death debuff immediately |
| **Sanctuary Blessing** | `sanctuary_cost × 3` gold | +5% XP gain for 10 actions (buff, not debuff removal) |

### 7E. Sanctuary Roster (Social Feature)
- **Like Torn's hospital** — when you visit a Sanctuary, you see a roster of all players who are currently:
  - In any sanctuary town (resting/recovering)
  - Carrying the "Recovering" debuff (recently died, still weak)
- Roster shows: name, level, race, which sanctuary they're in, cause of death, HP/max_hp, recovering status
- Sorted: recovering players first, then by level descending
- Endpoint: `GET /game/town/sanctuary/roster`
- Frontend: displayed below the service buttons in the Sanctuary tab

### 7F. Logout Screen Tracking (PvP Safety)
- New character field: `last_screen` (string) — tracks what screen the player was on when they logged out
- Updated via `POST /game/character/logout-screen` on `beforeunload` event
- Screen values: `"biome"`, `"town"`, `"combat"`, `"character"`, etc.
- **PvP safety rule (future)**:
  - If `last_screen` is `"town"` AND `current_town` is a sanctuary town → **cannot be attacked in PvP** (safe in sanctuary)
  - If `last_screen` is anything else → **can be attacked/mugged** in PvP
  - This means: logging out inside a Sanctuary = safe. Logging out anywhere else = vulnerable.
- This creates strategic depth: do you rush to the Sanctuary before logging out, or risk being attacked?

### 7G. Last Sanctuary Town Tracking
- New character field: `last_sanctuary_town` (string, town ID)
- Updated whenever player enters a hometown (sanctuary town) or uses the teleporter
- On death: respawn at `last_sanctuary_town`
- On login after offline PvP death: respawn at `last_sanctuary_town`

### 7H. Death Log
- Character fields:
  - `deaths`: total death count (integer)
  - `last_death`: `{cause, location, timestamp}` — most recent death info
- Used for future achievements:
  - "First Death" — die for the first time
  - "Ironborn" — reach level 20 without dying
  - "Undying" — 100 combat victories without a single death
  - "Frequent Flyer" — die 50 times (humor achievement)

### Files Modified (Implemented)
- `backend/game_data_p2.py` — sanctuary service only on 8 hometowns, removed from 6 non-hometown towns
- `backend/server.py` — sanctuary endpoint (rest/cleanse/blessing), death→teleport logic, sanctuary roster endpoint, logout-screen tracking endpoint, `last_sanctuary_town` tracking on visit/teleporter
- `backend/game_engine.py` — "Recovering" debuff (-10% dmg, 3 actions), "Sanctuary Blessing" buff (+5% XP, 10 actions)
- `backend/models.py` — `last_sanctuary_town`, `deaths`, `last_death`, `last_screen` fields
- `backend/racial.py` — backfill new fields for existing characters
- `frontend/src/components/TownView.jsx` — Sanctuary tab with 3 services + roster display
- `frontend/src/components/CombatScreen.jsx` — death/teleport narrative on defeat
- `frontend/src/components/JournalDrawer.jsx` — flavor text updated
- `frontend/src/pages/Game.jsx` — `beforeunload` handler for logout screen tracking

### Estimated Effort: 1-2 sessions ✅ Implemented

---

## Implementation Order (Recommended)

1. **Combat Overhaul** (Priority 1) — Biggest impact, makes the core loop fun
2. **Sanctuary System** (Priority 7) — Quick win, improves death mechanic and replaces Inn
3. **Skill Expansion** (Priority 2) — Pairs naturally with combat changes
4. **Quest Variety + Achievements** (Priority 4) — Independent, can be done in parallel
5. **Endgame Dungeon** (Priority 3) — Builds on improved combat
6. **Social Features** (Priority 5) — Long-term, needs player base (PvP uses Sanctuary for respawn)
7. **Crafting Depth** (Priority 6) — Polish layer

---

## Current Content Snapshot

| Category | Count |
|---|---|
| Continents | 11 |
| Biomes | 39 |
| Towns | 14 |
| Monsters | 236 |
| Items | 1,577 |
| Recipes | 1,113 |
| Skills | 23 |
| Races | 8 |
| Masteries | 11 |
| Professions | 19 |
| Resource Nodes | 438 |
| NPCs | 77 |
| NPC Quests | 1,491 |
| Heritage Bosses | 8 |
| API Endpoints | 118 |
| Frontend Components | 28 |
