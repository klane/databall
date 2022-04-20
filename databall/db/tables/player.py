from sqlalchemy import Column, Integer, String

from databall.db.base import Base, ForeignID


class Players(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)


class PlayerID(ForeignID):
    __table__ = Players
    inherit_cache = True
