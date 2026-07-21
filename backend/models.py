"""MongoDB Pydantic models with PyObjectId + BaseDocument pattern."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Annotated, Any, Optional

from bson import ObjectId
from pydantic import BaseModel, BeforeValidator, ConfigDict, Field


def _coerce_object_id(value: Any) -> str:
    if isinstance(value, ObjectId):
        return str(value)
    if isinstance(value, str):
        return value
    raise ValueError(f"Invalid ObjectId: {value!r}")


PyObjectId = Annotated[str, BeforeValidator(_coerce_object_id)]


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class BaseDocument(BaseModel):
    """Base model — reads `_id` from Mongo and exposes it as `id`."""

    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)

    id: Optional[PyObjectId] = Field(default=None, alias="_id")

    @classmethod
    def from_mongo(cls, doc: dict | None):
        if doc is None:
            return None
        if "_id" in doc:
            doc["_id"] = str(doc["_id"])
        return cls(**doc)

    def to_mongo(self) -> dict:
        data = self.model_dump(by_alias=True, exclude_none=True)
        if "_id" in data and isinstance(data["_id"], str):
            try:
                data["_id"] = ObjectId(data["_id"])
            except Exception:
                data.pop("_id", None)
        return data


# ---------- USER ----------
class User(BaseDocument):
    email: str
    password_hash: str
    display_name: str
    role: str = "player"
    created_at: str = Field(default_factory=utc_now_iso)


class UserPublic(BaseModel):
    id: str
    email: str
    display_name: str
    role: str
    created_at: str
    has_character: bool = False


# ---------- CHARACTER ----------
class CharacterStats(BaseModel):
    vitality: int
    cognition: int
    essence: int
    drive: int
    resilience: int = 0
    grace: int = 0


class StatusEffect(BaseModel):
    id: str
    name: str
    kind: str  # "buff" | "debuff"
    duration: int  # turns/minutes
    magnitude: int = 0


class InventoryItem(BaseModel):
    item_id: str
    quantity: int = 1


class EquippedGear(BaseModel):
    weapon: Optional[str] = None
    armor: Optional[str] = None
    trinket: Optional[str] = None


class LearnedSkill(BaseModel):
    skill_id: str
    cooldown_remaining: int = 0


class Character(BaseDocument):
    user_id: str
    name: str
    race: str
    role: str
    mastery: str
    portrait_id: str
    oath: Optional[str] = None
    heritage: Optional[str] = None  # for half-elf
    level: int = 1
    xp: int = 0
    gold: int = 50
    hp: int
    max_hp: int
    stats: CharacterStats
    inventory: list[InventoryItem] = Field(default_factory=list)
    equipped: EquippedGear = Field(default_factory=EquippedGear)
    skills: list[LearnedSkill] = Field(default_factory=list)
    statuses: list[StatusEffect] = Field(default_factory=list)
    reputation: dict[str, int] = Field(default_factory=dict)
    tutorial_step: int = 0
    tutorial_complete: bool = False
    current_continent: str = "aetheria"
    current_biome: str = "grasslands"
    login_streak: int = 0
    last_login_date: Optional[str] = None
    last_daily_refresh: Optional[str] = None
    daily_missions: list[dict] = Field(default_factory=list)
    inner_blood: int = 0  # Wildblood race
    exhaust: int = 0  # Orc/Wildblood race
    zone_active: bool = False
    kills: int = 0
    crafts: int = 0
    created_at: str = Field(default_factory=utc_now_iso)


# ---------- WORLD EVENT ----------
class WorldEvent(BaseDocument):
    character_name: str
    text: str
    kind: str = "general"  # "kill" | "loot" | "craft" | "general"
    created_at: str = Field(default_factory=utc_now_iso)


# ---------- REQUEST/RESPONSE PAYLOADS ----------
class RegisterPayload(BaseModel):
    email: str
    password: str
    display_name: str


class LoginPayload(BaseModel):
    email: str
    password: str


class CreateCharacterPayload(BaseModel):
    name: str
    race: str
    role: str
    mastery: str
    portrait_id: str
    oath: Optional[str] = None
    heritage: Optional[str] = None


class ActionPayload(BaseModel):
    action_id: str  # e.g., "hunt", "gather", "explore", "fish", "loot_ruins"
    biome_id: str
    target_id: Optional[str] = None  # monster or material or ruin


class CombatStartPayload(BaseModel):
    biome_id: str
    monster_id: str


class CombatTurnPayload(BaseModel):
    combat_id: str
    manual_skill_id: Optional[str] = None
    manual_item_id: Optional[str] = None


class CraftPayload(BaseModel):
    recipe_id: str


class LearnSkillPayload(BaseModel):
    skill_id: str
    teacher_id: Optional[str] = None
    skillbook_item_id: Optional[str] = None
