from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Match(Base):
    __tablename__ = 'matches'

    match_id = Column(Integer, primary_key=True)
    season = Column(Integer)
    league_match = Column(Integer)
    team_1 = Column(String(50))
    team_2 = Column(String(50))
    outcome = Column(String(50))

    def __init__(self, season, league_match, team_1, team_2, outcome):
        self.season = season
        self.league_match = league_match
        self.team_1 = team_1
        self.team_2 = team_2
        self.outcome = outcome

class Rank(Base):
    __tablename__ = 'ranking'

    rank_id = Column(Integer, primary_key=True)
    season = Column(Integer)
    league_match = Column(Integer)
    team = Column(String(50))
    home_wins = Column(Integer)
    away_wins = Column(Integer)
    home_losses = Column(Integer)
    away_losses = Column(Integer)
    home_draws = Column(Integer)
    away_draws = Column(Integer)
    goals_scored = Column(Integer)
    goals_conceded = Column(Integer)
    win_streak = Column(Integer)
    draw_streak = Column(Integer)
    loss_streak = Column(Integer)

    def __init__(self, season, league_match, team, home_wins, away_wins,
                home_losses, away_losses, home_draws, away_draws, goals_scored,
                goals_conceded, win_streak, draw_streak, loss_streak):
        self.season = season
        self.league_match = league_match
        self.team = team
        self.home_wins = home_wins
        self.away_wins = away_wins
        self.home_losses = home_losses
        self.away_losses = away_losses
        self.home_draws = home_draws
        self.away_draws = away_draws
        self.goals_scored = goals_scored
        self.goals_conceded = goals_conceded
        self.win_streak = win_streak
        self.draw_streak = draw_streak
        self.loss_streak = loss_streak