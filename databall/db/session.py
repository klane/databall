from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import databall.db.settings as settings

database = getattr(settings, 'DATABASE', ':memory:')
engine = create_engine(f'sqlite:///{database}', future=True)
Session = sessionmaker(engine, future=True)
