# Erchis Heritage System — Implementation Plan

## Overview
Each of the 8 accessible continents gets a dedicated **Heritage Month** celebrating its culture, history, and specialties. During its month, that continent gets gameplay bonuses, an exclusive boss, daily quests, a vendor with carry-over tokens, a ladder tab, and milestone rewards. Tokens carry over year to year — no FOMO.

### Calendar
| Month | Continent | Heritage Name |
|-------|-----------|---------------|
| January | Valeria | Festival of the Oath |
| February | Mushkara | Chainbreaker's Month |
| March | Concordia | Mosaic Festival |
| April | Khardrum | Deepforge Jubilee |
| May | Haya | Celestial Accord |
| June | Gennel | Great Awakening |
| July | Hylion | Tidefall Celebration |
| August | Daw'ul Talalu | Mystleaf Revel |
| September | (Break month) | — |

---

## Phase 1: Core Data Module (`heritage_system.py`)
**Status: [x]**

Create the core data file with:
- `HERITAGE_MONTHS` — maps month number → continent, name, theme, description
- `HERITAGE_BOSSES` — 8 heritage boss definitions (upgraded variants of existing bosses)
- `HERITAGE_BONUSES` — per-continent bonus config (gathering, combat XP, crafting, market, travel)
- `HERITAGE_DAILY_QUESTS` — 3 daily quest templates per continent
- `HERITAGE_VENDORS` — vendor item catalog per continent (cosmetics, titles, buffs, pets, recipes, materials, badges)
- `HERITAGE_MILESTONES` — milestone reward definitions (1/3/5/10 year)
- Helper functions: `get_active_heritage_month()`, `get_heritage_boss()`, `get_heritage_bonuses()`, `get_heritage_daily_quests()`, `get_heritage_vendor_items()`

### Files
- `backend/heritage_system.py` (new)

---

## Phase 2: DB Collections & Token Management
**Status: [x]**

Set up MongoDB collections and token management:
- `heritage_tokens` — per-character token balances for all 8 continents
- `heritage_progress` — per-character per-continent per-year progress tracking
- `heritage_milestones` — per-character per-continent milestone tracking
- `heritage_purchases` — vendor purchase history
- Token helper functions: `get_tokens()`, `add_tokens()`, `spend_tokens()`
- Progress helper functions: `get_progress()`, `update_progress()`, `check_meta_completion()`

### Files
- `backend/heritage_system.py` (extend with DB functions)
- `backend/server.py` (add DB collection refs)

---

## Phase 3: Server Endpoints — Info & Tokens
**Status: [x]**

Add API endpoints for heritage info and token management:
- `GET /game/heritage/current` — current heritage month info + bonuses
- `GET /game/heritage/tokens` — player's token balances for all 8 continents
- `GET /game/heritage/progress` — player's meta-achievement progress for current month
- `GET /game/heritage/milestones` — player's milestone rewards across all continents

### Files
- `backend/server.py` (add endpoints)

---

## Phase 4: Heritage Bonus Hooks
**Status: [x]**

Wire heritage bonuses into existing game systems:
- **Gathering**: +50% yield when gathering on heritage continent
- **Combat XP**: +25% combat XP when fighting on heritage continent
- **Crafting**: +15% crafting success when crafting on heritage continent
- **Market**: 10% discount when buying in heritage continent towns
- **Travel**: Free waystone travel to/from heritage continent
- **Spawns**: Heritage monsters appear in heritage continent biomes

### Files
- `backend/game_engine.py` (gathering, combat XP hooks)
- `backend/server.py` (market discount, travel cost hooks)
- `backend/exploration.py` (heritage monster spawns)

---

## Phase 5: Heritage Boss System
**Status: [x]**

Add heritage boss spawning and combat:
- Heritage bosses spawn in the top-tier biome of the active heritage continent
- Bosses are upgraded variants of existing continent bosses (higher HP, power, unique drops)
- Drop heritage tokens + chance at exclusive heritage cosmetics + boss parts
- Track kill count per player for meta-achievement
- Server endpoints:
  - `GET /game/heritage/boss` — current heritage boss info + player's kill count
  - `POST /game/heritage/boss/attack` — initiate combat with heritage boss

### Files
- `backend/heritage_system.py` (boss spawn logic)
- `backend/server.py` (boss endpoints)
- `backend/game_engine.py` (combat integration if needed)

---

## Phase 6: Daily Heritage Quests
**Status: [x]**

Generate and track daily heritage quests:
- 3 quests per day themed to the heritage continent (combat, gather, craft)
- Quests reset daily (seeded by date + character ID)
- Completing all 3 = bonus tokens + meta-achievement progress
- Server endpoints:
  - `GET /game/heritage/quests/daily` — today's 3 heritage quests + completion status
  - `POST /game/heritage/quests/claim` — claim quest reward

### Files
- `backend/heritage_system.py` (quest generation)
- `backend/server.py` (quest endpoints, progress tracking hooks)

---

## Phase 7: Heritage Vendor
**Status: [x]**

Add vendor browsing and purchasing:
- Each continent has a permanent vendor (accessible year-round)
- Items cost continent-specific tokens
- Categories: cosmetics, titles, buffs, pets, recipes, materials, badges
- Previous year's items available (catch-up)
- Server endpoints:
  - `GET /game/heritage/vendor/{continent}` — browse vendor items + prices
  - `POST /game/heritage/vendor/{continent}/buy` — purchase item with tokens

### Files
- `backend/heritage_system.py` (vendor item definitions, purchase logic)
- `backend/server.py` (vendor endpoints)

---

## Phase 8: Heritage Ladder
**Status: [x]**

Add heritage ladder scoring and ranking:
- Temporary ladder tab for active heritage month
- Tracks: tokens earned, boss kills, daily quests completed, ladder score
- Top 10 at month's end get titles + bonus tokens
- Score archived in hall of fame after month ends
- Server endpoints:
  - `GET /game/heritage/ladder` — current heritage month rankings
  - `GET /game/heritage/history` — past heritage month results

### Files
- `backend/heritage_system.py` (ladder scoring)
- `backend/server.py` (ladder endpoints)

---

## Phase 9: Milestone System
**Status: [x]**

Track yearly participation and grant milestone rewards:
- Track years participated per continent per character
- Auto-grant rewards at 1/3/5/10 years
- "Erchis Heritage Master" achievement for participating in all 8 in one year
- Server endpoints:
  - `GET /game/heritage/milestones` — milestone progress + claimable rewards
  - `POST /game/heritage/milestones/claim` — claim milestone reward

### Files
- `backend/heritage_system.py` (milestone logic)
- `backend/server.py` (milestone endpoints)

---

## Phase 10: Frontend — Heritage Panel
**Status: [x]**

Create the HeritagePanel React component with tabs:
- **Tab 1: Current Heritage** — featured continent, active bonuses, daily quests, meta progress
- **Tab 2: Heritage Boss** — boss info, kill count, attack button
- **Tab 3: Vendor** — browse all 8 continent vendors, token balances, purchase
- **Tab 4: Ladder** — current heritage month rankings
- **Tab 5: Milestones** — participation history, milestone progress
- **Tab 6: Calendar** — year overview showing all 8 months

### Files
- `frontend/src/components/HeritagePanel.jsx` (new)
- `frontend/src/pages/Game.jsx` (add HeritagePanel to right slide panel)
