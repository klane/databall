from pydantic import confloat

from databall.db.schemas.game import GameID
from databall.types import OverUnderResult, SpreadResult


class Covers(GameID):
    home_spread: confloat(ge=-30, le=30, multiple_of=0.5, strict=True)
    home_spread_result: SpreadResult
    over_under: confloat(ge=150, le=300, multiple_of=0.5, strict=True)
    over_under_result: OverUnderResult

    class Config:
        orm_mode = True
