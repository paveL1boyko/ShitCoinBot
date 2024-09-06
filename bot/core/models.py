from datetime import datetime

from pydantic import BaseModel, Field


class UserStats(BaseModel):
    energy: int
    coins: int
    league: int
    rank: int
    minigame: bool
    energyRefilledAt: datetime


class SessionData(BaseModel):
    user_agent: str = Field(validation_alias="User-Agent")
    proxy: str | None = None
