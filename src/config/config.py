from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent.parent.parent.absolute()
DATA_DIR = Path(BASE_DIR, 'data')
FEATURES_DIR = Path(BASE_DIR, 'features')
STORES_DIR = Path(BASE_DIR, 'stores')
CODE_DIR = Path(BASE_DIR, 'src')

# Final Features
VARIABLES = [
    'rank_t1', 'rank_t2', 'home_win_ratio_t1',
    'home_win_ratio_t2', 'away_win_ratio_t1', 'away_win_ratio_t2',
    'home_draw_ratio_t1', 'home_draw_ratio_t2', 'away_draw_ratio_t1',
    'away_draw_ratio_t2', 'home_loss_ratio_t1', 'home_loss_ratio_t2',
    'away_loss_ratio_t1', 'away_loss_ratio_t2', 'general_goals_scored_t1',
    'general_goals_scored_t2', 'home_goals_scored_t1', 'home_goals_scored_t2',
    'away_goals_scored_t1', 'away_goals_scored_t2', 'general_goals_conceded_t1',
    'general_goals_conceded_t2', 'home_goals_conceded_t1',
    'home_goals_conceded_t2', 'away_goals_conceded_t1', 
    'away_goals_conceded_t2', 'outcome']

DVC_FILES = [
    'prep_pipeline.pkl.dvc',
    'model.pkl.dvc',
    'test_data.parquet.dvc',
    'training_data.parquet.dvc',
]

SCRAPER_CONFIG_FILE = Path(CODE_DIR, 'scraper/scraper_config.yml')