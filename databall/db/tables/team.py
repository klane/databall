from sqlalchemy import Column, Integer, String

from databall.db.base import Base, ForeignID


class Teams(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    abbreviation = Column(String(3), nullable=False, unique=True)


class TeamID(ForeignID):
    __table__ = Teams
    inherit_cache = True
