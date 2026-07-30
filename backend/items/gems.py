"""Gem system — 9 gems, one per main/life stat.
Gems are bought from the marketplace (not dropped by monsters).
Each gem gives a flat +1 to its stat when socketed into an item.
"""
from __future__ import annotations

# ============================================================
# Gems — one per stat (6 main + 3 life)
# ============================================================
GEMS: list[dict] = [
    # Main stats
    {"id": "gem_might",      "name": "Ruby of Might",      "stat": "might",      "value": 1,
     "desc": "A blood-red ruby that pulses with raw strength. Socketing it into a weapon or armor grants +1 Might.",
     "price": 500},
    {"id": "gem_grace",      "name": "Sapphire of Grace",   "stat": "grace",      "value": 1,
     "desc": "A deep blue sapphire that shimmers like water. Grants +1 Grace when socketed.",
     "price": 500},
    {"id": "gem_cognition",  "name": "Topaz of Cognition",  "stat": "cognition",  "value": 1,
     "desc": "A golden topaz that sharpens the mind. Grants +1 Cognition when socketed.",
     "price": 500},
    {"id": "gem_insight",    "name": "Amethyst of Insight", "stat": "insight",    "value": 1,
     "desc": "A violet amethyst that crackles with arcane potential. Grants +1 Insight when socketed.",
     "price": 500},
    {"id": "gem_essence",    "name": "Emerald of Essence",  "stat": "essence",    "value": 1,
     "desc": "A vivid emerald that hums with mana. Grants +1 Essence when socketed.",
     "price": 500},
    {"id": "gem_durability", "name": "Onyx of Durability",  "stat": "durability", "value": 1,
     "desc": "A black onyx that feels solid as stone. Grants +1 Durability when socketed.",
     "price": 500},
    # Life stats
    {"id": "gem_vitality",   "name": "Garnet of Vitality",  "stat": "vitality",   "value": 1,
     "desc": "A deep red garnet that beats like a heart. Grants +1 Vitality when socketed.",
     "price": 800},
    {"id": "gem_mp",         "name": "Opal of Mana",        "stat": "mp",         "value": 1,
     "desc": "An iridescent opal swirling with liquid mana. Grants +1 Max MP when socketed.",
     "price": 800},
    {"id": "gem_stamina",    "name": "Quartz of Stamina",   "stat": "stamina",    "value": 1,
     "desc": "A clear quartz that vibrates with energy. Grants +1 Max Stamina when socketed.",
     "price": 800},
]

GEMS_BY_ID: dict[str, dict] = {g["id"]: g for g in GEMS}
