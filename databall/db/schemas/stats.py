from pydantic import BaseModel, NonNegativeInt, StrictInt

from databall.db.schemas.game import GameID
from databall.db.schemas.player import PlayerID
from databall.db.schemas.team import TeamID


class StrictNonNegativeInt(NonNegativeInt):
    strict = True


class Stats(BaseModel):
    min: StrictNonNegativeInt
    fgm: StrictNonNegativeInt
    fga: StrictNonNegativeInt
    fg3m: StrictNonNegativeInt
    fg3a: StrictNonNegativeInt
    ftm: StrictNonNegativeInt
    fta: StrictNonNegativeInt
    oreb: StrictNonNegativeInt
    dreb: StrictNonNegativeInt
    reb: StrictNonNegativeInt
    ast: StrictNonNegativeInt
    stl: StrictNonNegativeInt
    blk: StrictNonNegativeInt
    tov: StrictNonNegativeInt
    pf: StrictNonNegativeInt
    pts: StrictNonNegativeInt
    plus_minus: StrictInt


class PlayerStats(PlayerID, TeamID, GameID, Stats):
    pass


class TeamStats(TeamID, GameID, Stats):
    pass
