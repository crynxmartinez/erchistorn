# Erchis — Fantasy Dice RPG · Product Requirements

## Original Problem Statement
Build a fantasy Torn-like game. Every action is a 6-sided dice roll with outcomes:
- 1 = critical fail
- 2 = fail with bad effect (status applied)
- 3 = fail
- 4 = success with bad effect
- 5 = success
- 6 = critical success

Each outcome has 20 different narratives. Bad-effect outcomes apply status effects (character can have statuses). 7 continents, each with biomes, monsters, gathered materials. Crafting system. Players choose professions (Torn-style).

## User Choices (locked)
- **Narratives:** static pre-written pool (no AI)
- **Multiplayer:** shared world (Phase 1: leaderboard + world event feed; Phase 2: trading/PvP/guilds/chat)
- **Energy:** none — unlimited actions
- **Combat:** turn-based dice narrative with auto skill/item selection + manual override
- **Visual:** dark fantasy pixel art (parchment + amber + hard borders, no rounded corners)
- **Auth:** JWT email/password custom
- **Difficulty:** balanced
- **Races (Erchis lore):** 8 races — Human, Elf, Dwarf, Half-Elf, Orc, Wildblood, Hyliondrian, Sylvan (with unique starting stats + racial perks)
- **Additional Phase 1:** tutorials, daily missions, daily login rewards, character portrait picker, NPC skill teachers, skillbook drops, item rarity tiers

## Architecture
- **Backend:** FastAPI · MongoDB (motor) · JWT (PyJWT) · bcrypt
- **Frontend:** React 19 · react-router-dom · Tailwind · shadcn/ui components · sonner toasts · lucide-react icons
- **Design system:** VT323 pixel display font, JetBrains Mono body, Crimson Text narrative; dark parchment palette; hard-edge no-radius; 6-tier rarity colors
- **API prefix:** `/api`
- **Cookies:** httpOnly, SameSite=None, Secure (cross-domain safe)

## Core Systems
1. **Dice Engine** (`game_engine.py`) — power-delta weighted d6. Player Power vs Target Power shifts probability across 7 tiers.
2. **Combat Engine** — turn-based. Player auto-picks best available skill (respects triggers + cooldowns) and auto-uses items (respects trigger conditions + quantity). Manual override supported. Dice outcome multiplies damage.
3. **Action System** — hunt/gather/explore/fish/loot_ruins. Each rolls dice → picks narrative from pool.
4. **Crafting** — recipes with material + profession + level requirements. Dice roll determines Crude/Fine/Master quality tier.
5. **Skills** — starter skills from Role + Mastery. Additional learned from NPC teachers (gold + level) or skillbook drops.
6. **Character progression** — XP → auto-levelup, random stat gain, +HP.
7. **Daily / login rewards** — 3 dailies refresh at midnight; 7-day login streak with escalating rewards.
8. **Tutorial** — 6-step overlay on first entry.

## What's Been Implemented (Phase 1 complete — 2026-07-21)
### Backend
- All auth routes (register, login, logout, me)
- All game routes (character, action, combat start/turn, craft, skill learn, equip, daily claim, travel, tutorial, leaderboard, events)
- Full seed data: 8 races (Erchis lore), 5 roles, 11 masteries, 40 portraits, 7 continents (Aetheria fully populated with 4 biomes), 6 monsters, 30+ items with 6 rarity tiers, 23 skills, 11 recipes, 3 NPC teachers
- 7 narrative pools × 6 outcome tiers × 10 variants each = ~420 pre-written narrative lines (with placeholder substitution)
- Dice engine with power-delta weighting + luck shift
- Combat engine with auto skill/item selection

### Frontend
- Landing page (dark parchment + pixel VT323 + amber)
- Auth (login/register combined page)
- Character creation (5-step wizard: race → role → mastery → portrait → name/oath/heritage)
- Main Game HUD (3-column: character sheet · main viewport · dailies + world feed)
- Tabs: Biome / World Map / Inventory / Forge / Skills
- Dice roll animation (shake + step-cycle → reveal)
- Narrative reveal modal with typewriter + rewards breakdown
- Combat screen with manual skill/item override + AUTO
- Inventory with rarity-color borders
- Crafting panel with dice-tiered quality
- Skills panel + NPC teacher dialogs
- Daily missions panel + login streak
- Login reward modal (7-day streak)
- Tutorial overlay (skippable, 6 steps)
- Leaderboard page
- World events feed (live-refreshed every 20s)

## Prioritized Backlog

### P1 — content depth (recommended next)
- Content: fill Continents 2-7 with biomes, monsters, materials, teachers
- Content: expand narrative pool from 10 to 20 variants per outcome
- Content: more recipes, especially cross-continent crafts
- Content: rarer skillbook drops, unique per continent

### P2 — multiplayer & polish
- Trading market (list items for gold, browse listings)
- PvP arena (challenge other players — dice combat)
- Guilds
- Global chat / DMs
- Sprite upload panel (object storage integration for you to upload real pixel art)
- Prestige subclasses at Lv 25
- Advanced racial mechanics (Elf day/night states, Wildblood Zone, Orc Blood of Liberated tracker)

### P3 — quality of life
- Character portrait upload
- Sound effects / music toggle
- Achievement system
- Bestiary + Item Codex (fills as discovered)

## User Personas
- **Casual explorer:** loves world-building, wants story every session, no time pressure. Erchis matches with dense narrative pool, no energy caps.
- **Tactical optimizer:** min-max stats + gear + dice odds. Manual combat overrides + power-delta transparency satisfy this.
- **Social/completionist:** wants leaderboards + world events. Phase 1 covers; Phase 2 will add guilds/trading/PvP.

## Notes
- Frontend uses `withCredentials: true` for all API calls
- Backend CORS explicitly whitelists `FRONTEND_URL` (from env)
- No LLM used — 100% static narrative pool as user requested
- All portraits use DiceBear pixel-art API (no upload required in Phase 1)
