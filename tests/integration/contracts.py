"""What each endpoint actually requires to succeed.

Every entry here cost real debugging time to discover. They are written down so
the next run of the matrix does not rediscover them, and — more importantly — so
a route that *only* fails on a wrong argument is not mistaken for a working one.

Three of the eight bugs in the last pass were found precisely because a route was
tracked as "never once succeeded" rather than lumped in with "returned an error":

  - GET /game/professions/mine raised ImportError on every call
  - five Mage routes raised KeyError: '_id'
  - /game/druid/passives and /game/rogue/passives did not exist

A single wrong-shaped call would have 4xx'd on all of them and looked identical
to a route that was merely gated. The distinction is the whole point.
"""
from __future__ import annotations

# ---------------------------------------------------------------------------
# Literal vocabularies. Wrong values here produce 422s that read like bugs.
# ---------------------------------------------------------------------------

KNIGHT_OATHS = ("iron", "wrath", "bulwark", "endurance", "vanguard")
BARD_MODES = ("song", "dance")
#: NOT aggressive/defensive/balanced — that guess cost a full debugging cycle.
SUMMON_MODES = ("auto", "manual")
ALCHEMIST_CF_ACTIONS = ("analysis", "adjustment", "optimization", "perfect_formula")
#: Only meaningful when action == "perfect_formula".
PERFECT_FORMULA_CHOICES = ("delivery", "conversion", "sequence", "breakdown")
INNATE_ACTIONS = ("strike", "defend", "evade", "aim", "counter", "focus")

#: Field-name traps: these two travel endpoints disagree with each other.
TRAVEL_FIELD = "continent"          # POST /game/character/travel
TELEPORT_FIELD = "continent_id"     # POST /game/teleporter/travel

# ---------------------------------------------------------------------------
# Preconditions that cannot be satisfied by argument shape alone.
# ---------------------------------------------------------------------------

#: Gates that require game state, not a different payload. Reaching the handler
#: body behind each of these needs the listed setup performed first.
STATE_GATES = {
    "tame": "level >= 10, target at <= 30% HP, and not construct/undead",
    "skin": "the monster must be dead — state['skinnable'] is set on victory",
    "summon": "a tamed bestiary entry must exist first",
    "fuse": "an active summon is required",
    "end_fusion": "fusion must be active",
    "cf_action": "Combo Flow must have accrued from consecutive strikes",
    "pre_imbue": "requires skill_id, and the skill must be flagged imbuable",
    "guild_join": "an existing guild is required",
    "heritage_boss": "heritage rank and an active continent window",
}

#: Multi-step chains. A single call can never reach the later handler bodies, so
#: these must be walked in order. Two of the eight bugs lived in bodies only
#: reachable this way.
CHAINS = {
    "druid_summon": ["tame", "bestiary", "summon", "summon_mode", "fuse",
                     "end_fusion", "unsummon"],
    "alchemist_cf": ["strike", "strike", "strike", "cf_action"],
    "quest": ["accept", "claim", "abandon"],
    "combat": ["start", "turn", "abandon"],
}


def combat_body(combat_id: str, action: str = "strike", **extra) -> dict:
    """Every combat sub-endpoint needs combat_id — it is Pydantic-validated, so
    omitting it yields a 422 that looks like a gate rather than a mistake."""
    body = {"combat_id": combat_id, "action_type": action}
    body.update(extra)
    return body
