from typing import Any

from fastapi import Query
from pydantic import BaseModel


class Item(BaseModel):
    season: int
    league_match: int
    home: str
    team_1: str
    team_2: str
    goals_conceded_t1: int
    goals_conceded_t2: int
    goals_scored_t1: int
    goals_scored_t2: int
    home_wins_t1: int
    home_wins_t2: int
    away_wins_t1: int
    away_wins_t2: int
    home_losses_t1: int
    home_losses_t2: int
    away_losses_t1: int
    away_losses_t2: int
    home_draws_t1: int
    home_draws_t2: int
    away_draws_t1: int
    away_draws_t2: int
    rank_position_t1: int
    rank_position_t2: int
    wins_streak_t1: int
    wins_streak_t2: int
    draws_streak_t1: int
    draws_streak_t2: int
    losses_streak_t1: int
    losses_streak_t2: int