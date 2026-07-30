# Quest & NPC Expansion Plan

## Current State
- **16 towns** across 8 continents (2 towns each, except Aetheria which has legacy towns)
- **8 NPCs** — one flagship per hometown (oathspire, grunhold, elaris, jahrahold, solunara, rindivar_grove, atlantyrion, veilgrove)
- Each NPC has **3 quests** in a relationship-gated chain (stranger → acquainted → friend)
- **4 QUESTS** in the old QUESTS list (regional/story quests on notice boards)
- **4 EVENTS** (weekly cycle)
- Towns also have **TRADE_NPCS** (one trade-skill NPC per town, no quests)

## Goal
1. **5 NPCs per town** (80 NPCs total across 16 towns)
2. **~100 quests per town** (varied: relationship quests, story quests, daily bounties)
3. **Good loot** from NPC quests (unique items, rare materials, gold)
4. Quests reference the new starter biome monsters and items

## Architecture

### Data Structure
Each NPC follows the existing schema in `npcs.py`:
```python
{
    "id": "npc_id",
    "name": "Display Name",
    "race": "human|orc|...",
    "town": "town_id",
    "continent": "continent_id",
    "title": "Subtitle",
    "description": "Flavor paragraph",
    "personality": "One-line tone",
    "quests": [ ... ]  # 15-25 quests per NPC
}
```

### Quest Types per NPC
Each NPC will have a mix of:

1. **Chain Quests** (3-5 per NPC) — Story-driven, relationship-gated, unique item rewards
   - Tier: stranger → acquainted → friend → trusted → bonded
   - Order: 1, 2, 3, 4, 5
   - Good unique loot at the end

2. **Repeatable Bounties** (5-10 per NPC) — Kill/gather quests, repeatable
   - `repeatable: True` flag
   - Gold + XP + relationship points
   - Reference starter biome monsters/items

3. **Story Quests** (3-5 per NPC) — One-shot narrative quests
   - Unlocked by level or prior quest completion
   - Mid-tier unique/rare item rewards

### Quest Distribution per Town (100 quests)
- 5 NPCs × ~20 quests each = ~100 quests per town
- Per NPC breakdown:
  - 3-5 chain quests (relationship-gated, escalating rewards)
  - 5-8 repeatable bounties (kill X, gather Y)
  - 5-8 story/one-shot quests (level-gated)

### NPC Roles per Town (5 NPCs)
Each town gets NPCs with distinct flavors:
1. **Existing flagship NPC** (keep, expand quests)
2. **Combat Veteran** — kill bounties, hunting quests
3. **Gathering Master** — gather/fish bounties
4. **Merchant/Trader** — delivery quests, rare item rewards
5. **Mystic/Scholar** — exploration quests, lore-driven story chains

## Implementation Plan

### Phase 1: NPC Data Generation
- Create a **quest generation script** (`gen_npcs.py`) that:
  - Reads monster/item/biome data from `content_plan_data.py` and `game_data.py`
  - Generates NPC definitions with quests referencing appropriate monsters/items per continent
  - Outputs to `npcs.py` (appending to existing NPCs)
- **5 new NPCs per town** (4 new + 1 existing expanded)
- Each NPC gets 15-25 quests

### Phase 2: Quest Generation Logic
- **Bounty quests**: Auto-generated from biome monster/item lists
  - "Hunt 5 Scavenger Hounds" → kills: [("scavenger_hound", 5)]
  - "Gather 10 Scrap Bones" → gathers: [("scrap_bone", 10)]
- **Chain quests**: Hand-crafted narrative arcs per NPC type
  - Combat Veteran: escalating kill chains → unique weapon
  - Gathering Master: rare material collection → unique tool
  - Merchant: delivery/escort quests → unique accessory
  - Mystic: explore + kill quests → unique relic
- **Story quests**: Level-gated one-shots with mid-tier rewards

### Phase 3: Reward Scaling
- **Tier 1 (stranger)**: 50-150 gold, 50-100 XP, common materials
- **Tier 2 (acquainted)**: 150-400 gold, 100-250 XP, uncommon materials
- **Tier 3 (friend)**: 400-800 gold, 250-500 XP, rare materials + first unique item
- **Tier 4 (trusted)**: 800-1600 gold, 500-1000 XP, epic materials + powerful unique
- **Tier 5 (bonded)**: 1600-3000 gold, 1000-2000 XP, legendary unique item
- **Repeatable**: 50-200 gold, 30-100 XP, 10-30 relationship points

### Phase 4: Backend Changes
- Add `repeatable` field support to NPC quest system
- Modify `accept_npc_quest` to allow re-accepting repeatable quests
- Modify `complete_npc_quest` to not add repeatable quests to `completed_npc_quests`
- Add quest pool filtering by biome/continent for bounty generation

### Phase 5: Frontend Changes
- Update `NpcPanel.jsx` to handle 5 NPCs per town (scrollable list)
- Add quest type badges (chain, bounty, story, repeatable)
- Show repeatable quests with a refresh icon
- Update quest log to show more quests

### Phase 6: Old QUESTS Expansion
- Add biome-appropriate quests to the `QUESTS` list in `game_data_p2.py`
- Reference new starter biome monsters and items
- ~10 quests per town on the notice board (160 total)

## File Impact
- `backend/npcs.py` — Major expansion (8 → 80 NPCs, 24 → ~1600 quests)
- `backend/game_data_p2.py` — Add ~160 notice board quests to QUESTS
- `backend/server.py` — Add repeatable quest support
- `frontend/src/components/NpcPanel.jsx` — UI for 5 NPCs per town
- `backend/gen_npcs.py` — New generation script (optional, can hand-write)

## Scale Considerations
- 80 NPCs × 20 quests = **~1600 NPC quests**
- 16 towns × 10 quests = **~160 notice board quests**
- Total: **~1760 new quests**
- This is a LOT of data — recommend a generation script over hand-writing

## Recommended Approach
1. Write `gen_npcs.py` to auto-generate the bulk of bounty/repeatable quests
2. Hand-craft the chain/story quests for each NPC (the narrative content)
3. Run the generator to produce final `npcs.py` data
4. Test with a few towns first, then scale to all 16
