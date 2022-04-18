from sqlalchemy import Column, Integer, String

from databall.db.base import Base

PLAYER_ID = Integer


class Players(Base):
    id = Column(PLAYER_ID, primary_key=True)
    name = Column(String(100), nullable=False)
