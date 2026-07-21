# Auth Testing Playbook — Erchis Fantasy Dice RPG

## Overview
- Custom JWT email/password auth
- httpOnly cookies (`access_token` 24h, `refresh_token` 30d)
- Passwords hashed with bcrypt ($2b$)
- No admin seeding — users self-register

## Step 1: MongoDB
```bash
mongosh
use test_database
db.users.find().limit(3)
db.users.getIndexes()   # email is unique
```
Verify hashes start with `$2b$`.

## Step 2: API smoke test
```bash
# Register
curl -c cookies.txt -X POST http://localhost:8001/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@erchis.io","password":"password123","display_name":"TestHero"}'

# /me
curl -b cookies.txt http://localhost:8001/api/auth/me

# Create character (Human requires oath)
curl -b cookies.txt -X POST http://localhost:8001/api/game/character \
  -H "Content-Type: application/json" \
  -d '{"name":"Erethon","race":"human","role":"fighter","mastery":"knight","portrait_id":"human_aldric","oath":"I will restore the fallen kingdom."}'

# Roll a gather
curl -b cookies.txt -X POST http://localhost:8001/api/game/action \
  -H "Content-Type: application/json" \
  -d '{"action_id":"gather","biome_id":"grasslands","target_id":"wild_herb"}'

# Start combat
curl -b cookies.txt -X POST http://localhost:8001/api/game/combat/start \
  -H "Content-Type: application/json" \
  -d '{"biome_id":"grasslands","monster_id":"gray_wolf"}'
```

## Frontend flows to verify
1. Register → forward to Character Creation
2. Race selection filters roles/masteries
3. Portrait picker (5 per race)
4. Human requires Sacred Oath; Half-Elf requires Heritage
5. Character creation → game loads
6. Tutorial overlay shows on first entry (skippable)
7. Login reward modal shows on day 1
8. Biome view: hunt triggers combat, gather/explore/fish/loot_ruins triggers narrative reveal
9. Dice roll animates then reveals outcome (1-6) with color-coded label
10. Combat: manual skill/item override + AUTO
11. Inventory: rarity-coloured tiles, equip weapons/armor, study skillbooks
12. Crafting: recipes gated by materials/level/profession
13. Skills: NPC teachers charge gold, level-gated
14. Daily missions progress with actions/kills; claim button after complete
15. Leaderboard populates
16. World Events feed shows recent player deeds
