from src.db.data import Match, Rank
from src.db.manager import DBManager
import os

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

manager = DBManager(os.path.join(THIS_DIR, 'db_config.yml'))

# 4 - create movies
match = Match(1999, 1, 'Madrid', 'Barsa', 'draw')
rank = Rank(1999, 1, 'Madrid', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

manager.insert(match)
manager.insert(rank)

manager.close()