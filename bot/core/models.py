from datetime import datetime

from pydantic import BaseModel, Field


class UserStats(BaseModel):
    energy: int
    coins: int
    league: int
    rank: int
    minigame: bool
    energyRefilledAt: datetime


class UserData(BaseModel):
    db_id: int = Field(..., alias="dbId")
    username: str
    bonus_coin_count: int = Field(..., alias="bonusCoinCount")
    coin_count: int = Field(..., alias="coinCount")
    energy_regen_rate: int = Field(..., alias="energyRegenRate")
    energy_remain: int = Field(..., alias="energyRemain")
    energy_max: int = Field(..., alias="energyMax")
    invite_code: str = Field(..., alias="inviteCode")
    ref_counter: int = Field(..., alias="refCounter")
    league: int
    rank: int
    shit_usd_rate: float = Field(..., alias="shitUsdRate")
    season: int
    minigame: bool
    energy_refilled_at: datetime = Field(..., alias="energyRefilledAt")


class SessionData(BaseModel):
    user_agent: str = Field(validation_alias="User-Agent")
    proxy: str | None = None
