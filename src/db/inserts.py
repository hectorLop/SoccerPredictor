from src.db.data import Match, Rank
from src.db.db import Session, engine, Base
import pandas as pd

# 2 - generate database schema
Base.metadata.create_all(engine)

# 3 - create a new session
session = Session()

# 4 - create movies
match = Match(1999, 1, 'Madrid', 'Barsa', 'draw')
rank = Rank(1999, 1, 'Madrid', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

session.add(match)
session.add(rank)

# 10 - commit and close session
session.commit()
session.close()