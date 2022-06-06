from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import databall.db.settings as settings

url = getattr(settings, 'DATABASE_URL', 'sqlite://')
engine = create_engine(url, future=True)
Session = sessionmaker(engine, future=True)
