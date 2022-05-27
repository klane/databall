from pydantic import BaseModel, conint, constr


class Teams(BaseModel):
    id: conint(ge=1610612737, le=1610612766, strict=True)
    name: constr(regex=r'^[A-Z][a-z]+( ([A-Z]|\d{2})[a-z]+)+$', strict=True)
    abbreviation: constr(regex=r'^[A-Z]{3}$', strict=True)


class TeamID(BaseModel):
    team_id: Teams.__annotations__['id']
