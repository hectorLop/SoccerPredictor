from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Results(Base):
    __tablename__ = 'results'

    season = Column(Integer, primary_key=True)
    league_match = Column(Integer, primary_key=True)
    home = Column(String(50))
    team_1 = Column(String(50), primary_key=True)
    team_2 = Column(String(50), primary_key=True)
    outcome = Column(String(50))

    def __init__(self, season, league_match, home, team_1, team_2, outcome):
        self.season = season
        self.league_match = league_match
        self.home = home
        self.team_1 = team_1
        self.team_2 = team_2
        self.outcome = outcome

class GeneralRanking(Base):
    __tablename__ = 'general_ranking'

    season = Column(Integer, primary_key=True)
    league_match = Column(Integer, primary_key=True)
    rank_pos = Column(Integer)
    team = Column(String(50), primary_key=True)
    matches = Column(Integer)
    wins = Column(Integer)
    draws = Column(Integer)
    losses = Column(Integer)
    goals_scored = Column(Integer)
    goals_conceded = Column(Integer)
    goals_difference = Column(Integer)

    def __init__(self, season, league_match, rank_pos, team, matches, wins,
                draws, losses, goals_scored, goals_conceded, goals_difference):
        self.season = season
        self.league_match = league_match
        self.rank_pos = rank_pos
        self.team = team
        self.matches = matches
        self.wins = wins
        self.draws = draws
        self.losses = losses
        self.goals_scored = goals_scored
        self.goals_conceded = goals_conceded
        self.goals_difference = goals_difference

class HomeRanking(Base):
    __tablename__ = 'home_ranking'

    season = Column(Integer, primary_key=True)
    league_match = Column(Integer, primary_key=True)
    rank_pos = Column(Integer)
    team = Column(String(50), primary_key=True)
    matches = Column(Integer)
    wins = Column(Integer)
    draws = Column(Integer)
    losses = Column(Integer)
    goals_scored = Column(Integer)
    goals_conceded = Column(Integer)
    goals_difference = Column(Integer)

    def __init__(self, season, league_match, rank_pos, team, matches, wins,
                draws, losses, goals_scored, goals_conceded, goals_difference):
        self.season = season
        self.league_match = league_match
        self.rank_pos = rank_pos
        self.team = team
        self.matches = matches
        self.wins = wins
        self.draws = draws
        self.losses = losses
        self.goals_scored = goals_scored
        self.goals_conceded = goals_conceded
        self.goals_difference = goals_difference

class AwayRanking(Base):
    __tablename__ = 'away_ranking'

    season = Column(Integer, primary_key=True)
    league_match = Column(Integer, primary_key=True)
    rank_pos = Column(Integer)
    team = Column(String(50), primary_key=True)
    matches = Column(Integer)
    wins = Column(Integer)
    draws = Column(Integer)
    losses = Column(Integer)
    goals_scored = Column(Integer)
    goals_conceded = Column(Integer)
    goals_difference = Column(Integer)

    def __init__(self, season, league_match, rank_pos, team, matches, wins,
                draws, losses, goals_scored, goals_conceded, goals_difference):
        self.season = season
        self.league_match = league_match
        self.rank_pos = rank_pos
        self.team = team
        self.matches = matches
        self.wins = wins
        self.draws = draws
        self.losses = losses
        self.goals_scored = goals_scored
        self.goals_conceded = goals_conceded
        self.goals_difference = goals_difference