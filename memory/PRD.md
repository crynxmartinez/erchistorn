# Erchis — Fantasy Dice RPG · Product Requirements

## Original Problem Statement
Build a fantasy Torn-like game with a d6 dice engine (6 outcomes × ~20 narratives each, statuses on bad rolls), 7 continents with biomes/monsters/materials, crafting, Torn-style professions. User Choices: static narratives, shared-world multiplayer, no energy, turn-based dice combat with auto skill/item + manual override, pixel-art visual, JWT auth, balanced difficulty. Additional lore-driven features requested: 8 playable Erchis races with unique perks; tutorials; daily missions + login rewards; NPC skill teachers; skillbook drops; 6-tier item rarity.

**Phase 2 additions (this iteration):** Regions/Towns inside continents (Inn, Marketplace, Notice Board, Trainers), Guild House (create/join guilds, quest board, bulletin, events-as-quests), fast travel between towns, weekly event cycle (Mon boss / Wed tournament / weekend festival), advanced racial mechanics (Heritage Rank I + racial resource meters for all 8 races), Beast Aspect / Marine Adaptation sub-choices.

**Phase 3 additions (this iteration):** Full 7-step character creation with **Origin** system — 33 Origins (3 per Mastery) providing final bonus stats + drawback. Layered stat calculation (Race → Role → Mastery → Origin). New Main Stats (Might, Grace, Insight) alongside Life Stats (Vitality, Cognition, Essence, Drive). Derived stats (Armor bonus, Evasion mod, Attack Success mod). Minimum-1 stat rule applied. Character creation summary shows exact stat breakdown per layer.

## Architecture
- **Backend:** FastAPI · MongoDB (motor) · JWT (PyJWT) · bcrypt
- **Frontend:** React 19 · react-router-dom · Tailwind · shadcn/ui · sonner · lucide-react
- **Design:** Dark parchment · VT323 pixel display · JetBrains Mono body · Crimson Text narrative · amber accents · hard borders · 6-tier rarity colours
- **API prefix:** `/api`. Cookies: httpOnly, SameSite=None, Secure.

## Core Systems
1. **Dice Engine** — power-delta weighted d6 (game_engine.py)
2. **Combat Engine** — turn-based dice; auto skill/item selection + manual override; racial combat mods
3. **Action System** — hunt/gather/explore/fish/loot_ruins → static narrative pool
4. **Crafting** — dice-tiered quality (Crude/Fine/Master)
5. **Skills** — starter (Role + Mastery), NPC teachers, skillbook drops
6. **XP/Level** — auto-level with random stat gain and +HP
7. **Racial** — Heritage Rank I passives + racial resource meters + Beast Aspect + Marine Adaptation
8. **Towns** — Inn (rest+heal), Marketplace (buy/sell), Notice Board (regional quests), Trainers, fast travel (gold cost)
9. **Guild House** — create (5,000g)/join guilds, treasury donations, member roster; quest board (regional + story + event); bulletin board; events-as-quests
10. **Events** — weekly cycle: Monday world boss, Wednesday tournament, Sat-Sun festival + standing bounties
11. **Character Creation** — 7-step wizard: Race → Role → Mastery → Origin → Portrait → Name/Oath → Summary; layered stat computation with per-layer breakdown displayed

## What's Been Implemented

### Phase 1 (2026-07-21)
Auth, character creation (5-step), Aetheria continent, dice/combat/craft engines, narrative pool (7 actions × 6 outcomes × 10 variants), inventory with rarity colors, skills + NPC teachers, daily missions, login rewards, tutorial, leaderboard, world events feed.

### Phase 2 (2026-07-21)
Regions + 2 towns (Ironhold Forge Town + Willowmere Sanctuary), Inn/Marketplace/Notice Board/Trainers services, fast travel with gold cost, Guild House page (Quest Board / Guilds / Events / Bulletin), guild CRUD (create/join/leave/donate), quest system (regional/story/event with accept/abandon/claim), weekly event cycle (world boss / tournament / festival / bounty), racial resource meters for all 8 races, Heritage Rank I passives, Beast Aspect + Marine Adaptation on creation, Exhaustion + Resolve resources, time-of-day (server UTC) driving Elf bonuses.

### Phase 3 (2026-07-21)
**Character Creation redesign**: 7-step wizard adds Origin step (33 Origins, 3 per Mastery) and Summary step with layered stat breakdown. Backend now layers Race → Role → Mastery → Origin stats and stores Might/Grace/Insight/Armor_bonus/Evasion_mod separately. Role→Mastery availability matches user's spec exactly. Minimum-1 stat rule enforced.

### Phase 3.1 — World + Wizard polish (2026-02, current session)
- **Beast Aspect UI** (Wildblood) and **Marine Adaptation UI** (Hyliondrian) surfaced in the wizard as an extra step between Origin and Portrait. 5 Beast Aspects, 6 Marine Adaptations. Server enforces race-only validation (Human sending a beast_aspect is now rejected).
- **World Expansion**: 12 new towns populated (2 per continent) across Vulkaros, Nyxmoor, Frosthelm, Zephyria, Sablewaste, Verdania — total 14 towns. Each continent now defines 4 biomes (previously non-Aetheria had 0).
- **Town Visit gating**: `/api/game/town/visit` now blocks travel to towns whose continent is below the character's current level or not the current continent (with friendly error text).
- **HUD Town Discovery**: Unvisited towns in the current continent render as dashed-border `discover-town-<id>` buttons in the Game HUD so players see where they can wander next.

### Phase 3.2 — Biome content for the higher continents (2026-02, current session)
- **48 new monsters** across the 24 biomes of the 6 new continents (2 per biome). Power/HP scales from Vulkaros (Lv 8, power ~11–15) up to Verdania (Lv 45, power ~50–58).
- **~50 new items**: continent-specific gather materials (ash_grass, basalt_shard, hex_moss, cold_iron, silverleaf, storm_glass, djinn_glass, abyss_coral, kraken_ink, etc.), monster loot drops, six late-game weapon/armor drops (basalt_axe → sylvan_glaive; ashplate → coral_platemail), and six skillbook drops (ember_lash, wraith_ward, frost_edge, wind_step, sunlance, tidefury).
- **Biome actions** (hunt / gather / explore / loot_ruins / fish) wired for all 24 new biomes.
- **Structure**: implemented as a merge module (`/app/backend/game_data_p3.py` → `extend_world_data`) so the base `game_data.py` stays readable.
- **Tests**: 15/15 new pytest cases (`tests/test_phase3_biome_content.py`) pass — verifies monster count grew, items expanded, every new biome has a monster + hunt action, and monster power scales with continent level_req.

## Backlog

### P1 — Advanced Racial Ranks (deferred)
Heritage Ranks II–V per user's detailed spec (utility abilities, cooldowned active abilities, awakenings). Each race has its own progression tree.

### P2 — Multiplayer depth
- Guild wars & territory claims
- Trading market (player-to-player)
- PvP arena (dice combat vs other players)
- Global/guild chat
- Pack Bonds (Wildblood)
- Human daily specialization system (5 focuses)
- Marine adaptation Rank II abilities

### P3 — Content expansion
- Populate Continents 2-7 with biomes + towns + monsters + gather materials (**COMPLETE, Feb 2026**)
- Expand narrative pool from 10 → 20 variants per outcome
- More recipes requiring cross-continent materials
- Racial quests (unlock Heritage Ranks)
- Guild hall upgrades (buffs)
- Craft recipes for new-continent materials (basalt_axe, cold_iron_spear, storm_bow, djinn_scimitar, sylvan_glaive) — items exist as drops but currently have no craft path.

### P4 — Quality of life
- Sprite upload for real pixel art (object storage integration)
- Bestiary + Item Codex
- Sound / music toggle
- Achievement system
- Character reset system (rare + expensive)

## Notes
- Existing pre-Phase-3 characters were wiped (schema change to add Main Stats).
- All portraits use DiceBear pixel-art API.
- No LLM used — 100% static narrative pool.
- CORS explicitly whitelists FRONTEND_URL for cookie auth.
