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

### Phase 3.3 — Weary rename + stat tooltips (2026-02, current session)
- **BUGFIX**: the "Exhausted" debuff and the numeric "Exhaust(ion)" racial meter had colliding names — the STATUS badge said EXHAUSTED while the meter read 0. Renamed the debuff to **Weary** (`id: weary`), added a one-time startup migration that rewrites legacy `exhausted` statuses on existing characters (2 records renamed on first boot).
- **BUGFIX**: statuses never decremented — added `_tick_character_statuses(character)` after every `/api/game/action` so debuffs like Weary / Bleeding / Poisoned expire naturally instead of persisting until an Inn visit.
- **ENHANCEMENT**: every stat, resource meter, and status badge on the Character Sheet + Racial Panel now surfaces a hover tooltip (Radix, `delayDuration=120`) explaining what it does. New `STAT_HINTS` / `STATUS_HINTS` maps in `CharacterSheet.jsx` and `hint` fields in `RacialPanel.jsx`. Status badges also show remaining duration inline as `Weary (3)`.
- **Tests**: verified via testing agent — 100% pass, 7/7 backend + 10/10 frontend cases. Confirmed the word "Exhausted" never appears on a status badge anymore, Weary tooltip explicitly says "NOT the same as the Exhaustion meter", and a 20-action Wildblood loop saw its Weary status expire on its own.

### Phase 3.4 — Journal (Codex) drawer (2026-02, current session)
- **NEW**: an in-world Codex accessible via a JOURNAL button in the Game HUD tab bar. Uses shadcn Sheet + Tabs + ScrollArea (right-side slide-in, ~768px wide on desktop).
- Seven tabs: **Preface**, **Stats**, **Statuses**, **Races**, **World**, **Bestiary**, **Materials**. Everything is styled like a leather-bound book — parchment header ("The Book of Erchis"), pixel headings, and body copy inline with the game aesthetic.
- **Single source of truth**: hint strings moved from CharacterSheet/RacialPanel into `/app/frontend/src/data/hints.js` (STAT_HINTS, STATUS_HINTS, EXHAUSTION_HINT, RESOLVE_HINT, RESOURCE_META, RACE_TO_RESOURCE). Both tooltips and the Codex read from the same file.
- **Content**: 8 races with lore + Heritage Rank I passive + resource meter + Beast Aspects / Marine Adaptations sub-lists; 7 continents grouped by their biomes; **54 monsters** in the Bestiary grouped by continent → biome with power/HP/drops; **97 items** in the Materials tab grouped by 6 rarity buckets with rarity colour classes.
- **Lazy-loaded + cached**: 7 parallel `/api/game/data/*` calls fire only on first open; subsequent opens re-use cached state (verified via network interceptor).
- **Tests**: 13/13 frontend acceptance criteria pass. Fixed the Radix a11y warning by wiring `SheetTitle` + `SheetDescription` into the parchment header.

### Phase A/B/C/D — Full world spec compliance (2026-02, current session)
Massive rewrite to bring the world in line with the master design spec.
- **Phase A · Canon world rename**: 7 legacy continents renamed + expanded to **8 accessible** (Valeria/Mushkara/Concordia/Khardrum/Haya/Gennel/Hylion/Daw'ul Talalu) + **3 locked** (Azurea/Vael'Turog/Orinth). All 14 hometowns and 24 biomes renamed to canon (Ironhold→Oathspire, Solunara, Jahrahold, Elaris, Grunhold, Rindivar Grove, Atlantyrion, Veilgrove, etc.). Startup migration rewrites any legacy character record IDs idempotently. Race → canonical homeland map: Sylvans really do start in Veilgrove now, Dwarves in Jahrahold, etc.
- **Phase B · Grand Teleporter / Waystones / Homeland Reputation**: `/api/game/teleporter/travel` (100g fee, 10-min cooldown, hometown-only, arrival at destination hometown). 16 Waystones with discover→activate→travel (2 per continent, per-biome). Reputation dict per character, seeded Friendly for natives + Neutral for others (7 tiers hated→exalted).
- **Phase C · Exploration Progress %**: per-biome character progress with 10/25/50/75/100 milestones. Explore actions add +20/+12/+6/+2/0/-2 per dice outcome; non-explore actions add half. Response body exposes `explore_hits`.
- **Phase D · Formal Professions**: **19 professions** across gathering/crafting/service. Up to 3 slots per character (unlock at Lv 1/10/25). Ranks Novice→Grandmaster with 200/600/1500/3500/8000 xp thresholds. Learn/abandon endpoints; 25% xp saved on abandon; **7-day relearn cooldown** enforced. Every gather/hunt/fish/loot_ruins action grants XP to the matching learned profession.
- **Frontend**: two new HUD tabs (**TRADES**, **TELEPORTER**). World map rewritten to show all 11 continents + a live Exploration Progress panel underneath. All race/continent names pretty-cased.
- **Tests**: 23/23 pytest cases + 5/5 UI acceptance areas verified by testing agent. Fixed `rank_from_xp` off-by-one, added hometown-gating flag on teleporter destinations, cleaned teleporter arrival state.

### Phase E/F/G (2026-02, current session)
Massive lore/gameplay expansion:
- **NPCs** — 8 canonical hometown NPCs (Captain Ansel/Oathspire, Warchief Thraka/Grunhold, Envoy Seraphine/Elaris, Grandmaster Thora/Jahrahold, Loremaster Sylanya/Solunara, Matriarch Zerith/Rindivar Grove, Tide-Priest Calvar/Atlantyrion, Elder Mireth/Veilgrove) with relationship tiers (Stranger→Devoted) and 3-quest arcs each (Q2 unlocks at Acquainted, Q3 at Trusted).
- **Regional Biome Bosses** — 8 bosses (one per continent's tier-4 biome) with unique rare drops (Ashen Lord's Regalia set, Demonfang, Diplomat's Signet, Deepforge Hammer, Starfall Bow, Ancient Fang, Abyssal Trident, Elderroot Bough). Dedicated `boss` action exposed per biome.
- **Cross-Continent Legendary Recipes** — 5 legendary crafts each requiring materials from ≥2 continents.
- **Phase E Racial Active Abilities** — all 8 races now have a cooldowned active ability:
  · Human — Adaptability Focus (24h, choose 1 of 5 daily focuses)
  · Dwarf — Field Repair (12h, restore armor + weapon durability)
  · Orc — Break the Chain (40 Defiance, purge control effects)
  · Elf — Celestial Shift (1 Charge, 6h; +30% HP heal + purge debuffs)
  · Half-Elf — Heritage Attunement (3 Harmony, 24h; +1 atk/eva for 5 actions + resolve)
  · Wildblood — Bloodrage (40 Inner Blood, 8h; +2 atk / -1 eva for 4 actions)
  · Hyliondrian — Tidal Grace (3 Tide, 12h; +40% HP heal + purge)
  · Sylvan — Shrunken Form (1 Verdant Essence, 10-min CD, toggle; +2 eva / -1 atk while shrunken; toggle-off is free)
- **Status modifiers now affect combat power** — `compute_player_power` sums all status `modifiers.attack_success_mod` so buffs/debuffs actually influence dice deltas.
- **Fresh characters seeded in home_town** — all 8 races now spawn inside their hometown (was previously spawning wilderness with `current_town=None`), enabling regional 0.75x price bonuses immediately.
- **Boss action bug fixed** — Phase-G boss injection now correctly runs AFTER `_apply_biome_id_migration()` so the injected `boss` action survives the dict rebuild.
- **Tests**: 80/83 pytest cases pass (3 skipped by design), covering all 8 racial abilities, all 8 boss biomes, all 8 home_town spawns, NPC quest chains, regional pricing.

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
- **Emergent launch (2026-08):** Game was pulled from GitHub (originally built for Vercel + MongoDB Atlas). Adapted to run on Emergent resources by making the MongoDB TLS connection conditional in `server.py` (TLS skipped for local `mongodb://localhost`, kept for Atlas). Verified end-to-end on the Emergent local Mongo — auth, character creation, and game actions all persist. No other code changes.
- Existing pre-Phase-3 characters were wiped (schema change to add Main Stats).
- All portraits use DiceBear pixel-art API.
- No LLM used — 100% static narrative pool.
- CORS explicitly whitelists FRONTEND_URL for cookie auth.
