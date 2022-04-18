from sqlalchemy import Column, Integer, String

from databall.db.base import Base

TEAM_ID = Integer


class Teams(Base):
    id = Column(TEAM_ID, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    abbreviation = Column(String(3), nullable=False, unique=True)
