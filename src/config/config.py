from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent.parent.parent.absolute()
DATA_DIR = Path(BASE_DIR, 'data')
FEATURES_DIR = Path(BASE_DIR, 'features')
STORES_DIR = Path(BASE_DIR, 'stores')

# Final Features
VARIABLES = ['team_1', 'team_2', 'rank_t1', 'rank_t2', 'general_wins_t1',
           'general_wins_t2', 'home_wins_t1', 'home_wins_t2', 'away_wins_t1',
            'away_wins_t2', 'general_draws_t1', 'general_draws_t2', 'home_draws_t1',
           'home_draws_t2', 'away_draws_t1', 'away_draws_t2', 'general_losses_t1',
           'general_losses_t2', 'home_losses_t1', 'home_losses_t2',
           'away_losses_t1', 'away_losses_t2', 'general_goals_scored_t1',
           'general_goals_scored_t2', 'home_goals_scored_t1',
           'home_goals_scored_t2', 'away_goals_scored_t1', 'away_goals_scored_t2',
           'general_goals_conceded_t1', 'general_goals_conceded_t2',
           'home_goals_conceded_t1', 'home_goals_conceded_t2',
           'away_goals_conceded_t1', 'away_goals_conceded_t2', 'outcome']