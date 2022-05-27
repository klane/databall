from pydantic import BaseModel, conint, constr


class Players(BaseModel):
    id: conint(gt=0, lt=1.7e6, strict=True)
    name: constr(regex=r'^[A-Z][A-Za-z,\'\-\.]+( [A-Za-z,\'\-\.]+)*$', strict=True)


class PlayerID(BaseModel):
    player_id: Players.__annotations__['id']
