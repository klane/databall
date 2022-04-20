from functools import partial

from sqlalchemy import Column, Integer, String

from databall.db import columns
from databall.db.base import Base


class Players(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)


PlayerID = partial(columns.foreign_key, Players.id)
