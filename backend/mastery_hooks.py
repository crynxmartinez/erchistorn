"""Per-mastery combat logic, extracted from `combat_turn`.

Why this module exists
----------------------
`combat_turn` grew to 2,270 lines with 140 `_is_<mastery>(character)` guard calls
and 441 branches at up to 8 levels of indentation. Eleven independent resource
systems were interleaved into one control-flow spine, so touching the Hunter's
range code meant scrolling past the Bard's Crescendo.

That size was not a style problem — it was producing defects. Every bug found in
this engine lived in or beside that function: a Mage helper that was called but
never defined; two Priest functions whose `def` lines were lost in an edit,
leaving their bodies stranded after a `return`; a `c_mult` lookup with no `0` key
that crashed the moment any mastery landed a stun; and a self-`stat_mod` path
gated on eight masteries with no fallback, so 19 Druid skills silently dropped
their bonuses. Eight mastery-gated branches and no fallback is not a mistake
anyone makes in a 200-line function.

The contract
------------
Each mastery implements `MasteryHooks`. The spine calls each hook in turn:

    for h in hooks_for(character):
        h.on_turn_start(ctx)

Hooks receive a single mutable `TurnContext` and mutate it, `ctx.state` or
`ctx.character` directly. That mirrors what the original code did — it mutated
`state` and `character` freely — so moving logic here is behaviour-preserving.
Tightening the boundary to pure functions is a separate, later step; doing both at
once would make the golden logs useless as a safety net.

Safety
------
Every extraction is verified against `tests/golden.py`: 1,584 scenarios / ~19,800
turns pinning log entries, HP, victory state and 28 mastery resource meters. The
harness was itself validated by sabotage — one deliberate behaviour change per
mastery, each of which it had to catch. Golden logs must read IDENTICAL after each
extraction; anything else means the move changed behaviour.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol, runtime_checkable


@dataclass
class TurnContext:
    """Everything a mastery hook needs for one combat turn.

    Replaces the ~40 locals that were threaded through `combat_turn`. Fields are
    mutable and hooks are expected to mutate them — see the module docstring.
    """

    character: dict
    state: dict
    monster: dict
    log: list
    action_type: str = "strike"
    turn: int = 0

    # The skill resolved for this turn, or None for a pure innate action.
    skill: dict | None = None

    # The player-facing "you used X" line. Several skill-effect steps rewrite it
    # (a cracked katar, a loaded imbue, a performance), so it travels on the
    # context rather than as a spine local.
    skill_used_msg: str = ""

    # Damage in flight. `outgoing` is what the player is about to deal;
    # `incoming` is what the player is about to take.
    outgoing: float = 0.0
    incoming: float = 0.0

    # d6 results. `enemy_outcome` is 0 when the enemy did not act at all
    # (stunned / bound / ensnared / airborne).
    outcome: int = 0
    enemy_outcome: int = 0

    # Set by a hook that consumes the enemy's turn (Mage Mind Control / Time Loop,
    # Alchemist Rising Strike).
    enemy_turn_consumed: bool = False

    racial_mods: dict = field(default_factory=dict)

    # ---- convenience -------------------------------------------------
    @property
    def hp_ratio(self) -> float:
        return self.character.get("hp", 0) / max(1, self.character.get("max_hp", 1))

    @property
    def enemy_hp_ratio(self) -> float:
        return self.state.get("monster_hp", 0) / max(1, self.state.get("monster_max_hp", 1))

    def note(self, kind: str, text: str) -> None:
        """Append a log entry. Kept as a method so hooks never build dicts by hand."""
        self.log.append({"kind": kind, "text": text})


@runtime_checkable
class MasteryHooks(Protocol):
    """One implementation per mastery. Every method is optional — `BaseHooks`
    supplies no-ops, so a mastery only overrides the phases it participates in.

    Phase order matches the turn's actual structure:

        on_turn_start        start-of-turn resources, initialisation, meters
        on_action_selected   after the skill/innate action for this turn is known
        on_damage_computed   modify ctx.outgoing before it lands
        on_hit_landed        react to damage having landed on the monster
        on_enemy_turn_start  control effects; may set ctx.enemy_turn_consumed
        on_incoming_damage   modify ctx.incoming before it lands on the player
        on_turn_end          ticks, expiry, cleanup
    """

    def on_turn_start(self, ctx: TurnContext) -> None: ...
    def on_action_selected(self, ctx: TurnContext) -> None: ...
    def on_damage_computed(self, ctx: TurnContext) -> None: ...
    def on_hit_landed(self, ctx: TurnContext) -> None: ...
    def on_enemy_turn_start(self, ctx: TurnContext) -> None: ...
    def on_incoming_damage(self, ctx: TurnContext) -> None: ...
    def on_turn_end(self, ctx: TurnContext) -> None: ...


class BaseHooks:
    """No-op implementation. Subclass and override only what applies."""

    mastery: str = ""

    def on_turn_start(self, ctx: TurnContext) -> None:
        pass

    def on_action_selected(self, ctx: TurnContext) -> None:
        pass

    def on_damage_computed(self, ctx: TurnContext) -> None:
        pass

    def on_hit_landed(self, ctx: TurnContext) -> None:
        pass

    def on_enemy_turn_start(self, ctx: TurnContext) -> None:
        pass

    def on_incoming_damage(self, ctx: TurnContext) -> None:
        pass

    def on_turn_end(self, ctx: TurnContext) -> None:
        pass


# ============================================================
# Registry
# ============================================================
# Populated by register(); `hooks_for` returns instances in a FIXED order derived
# from the original source order inside combat_turn, not alphabetically. Hook
# ordering is observable — two masteries can both modify ctx.outgoing — so the
# order is part of the contract.
_REGISTRY: dict[str, type[BaseHooks]] = {}

# Mirrors the original inline execution order inside combat_turn. Ordering is
# observable — two masteries can both modify ctx.outgoing, and turn-start blocks
# that grant permanent stats must run in the same sequence they always did — so
# this list is part of the contract, not an alphabetical convenience.
HOOK_ORDER = [
    "knight", "paladin", "priest", "lancer", "assassin", "hunter",
    "alchemist", "mage", "rogue", "bard", "druid",
]


def register(cls: type[BaseHooks]) -> type[BaseHooks]:
    """Class decorator: register a mastery's hooks."""
    if not cls.mastery:
        raise ValueError(f"{cls.__name__} must set `mastery`")
    _REGISTRY[cls.mastery] = cls
    return cls


def hooks_for(character: dict) -> list[BaseHooks]:
    """Hook instances for the character's masteries, in HOOK_ORDER."""
    owned = set(character.get("masteries") or [])
    if not owned:
        return []
    out: list[BaseHooks] = []
    for name in HOOK_ORDER:
        if name in owned and name in _REGISTRY:
            out.append(_REGISTRY[name]())
    # Any registered mastery not listed in HOOK_ORDER still runs, after the known
    # ones, so adding a mastery cannot silently disable it.
    for name in sorted(owned - set(HOOK_ORDER)):
        if name in _REGISTRY:
            out.append(_REGISTRY[name]())
    return out


def registered() -> list[str]:
    """Which masteries have been extracted so far."""
    return sorted(_REGISTRY)


# ============================================================
# Extracted masteries
# ============================================================
# Imported at the bottom so the decorators run on module import. Each import is a
# completed extraction, verified against the golden logs.
from mastery import lancer as _lancer  # noqa: E402,F401
from mastery import core as _core  # noqa: E402,F401
