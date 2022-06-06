from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import databall.db.settings as settings
from databall.db import urls

url = getattr(settings, 'DATABASE_URL', urls.sqlite_url())
engine = create_engine(url, future=True)
Session = sessionmaker(engine, future=True)

autocommit_engine = engine.execution_options(isolation_level='AUTOCOMMIT')
AutocommitSession = sessionmaker(autocommit_engine, future=True)
