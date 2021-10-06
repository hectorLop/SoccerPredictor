import numpy as np
import pandas as pd
import yaml
import pickle

from pathlib import Path
from src.scraper.scraper import Scraper
from src.scraper.utils import DataParser
from src.preprocessing.features_preprocesses import get_feature_pipeline
from src.preprocessing.model_preprocessing import ModelPreprocesser
from src.config.config import CODE_DIR, DATA_DIR
from src.config.logger_config import logger

def load_data():
    scraper_config = Path(CODE_DIR, 'scraper/scraper_config.yml')

    with open(scraper_config) as file:
        config = yaml.full_load(file)

    scraper = Scraper(config)

    data = scraper.scrap_data()

    parser = DataParser()

    general_ranking, results = parser.parse_general_data(data['general'])
    home_ranking = parser.parse_home_away_data(data['home'])
    away_ranking = parser.parse_home_away_data(data['away'])

    results_df, general_df, home_df, away_df = create_dataframes(results,
                                                                general_ranking,
                                                                home_ranking,
                                                                away_ranking)

    logger.info('CREATING FEATURES')
    feature_pipeline = get_feature_pipeline(general_df, home_df,
                                            away_df)
    data = feature_pipeline(results_df)

    logger.info('CREATING PREPROCESSING PIPELINE')
    with open(Path(DATA_DIR, 'prep_pipeline.pkl'), 'rb') as file:
        preprocesser_pipeline = pickle.load(file)

    data = data.drop('outcome', axis=1)
    data = preprocesser_pipeline.transform(data)

    data = data.drop(['results_id', 'created_on'], axis=1)

    return data

def generate_preds(data):
    logger.info('GENERATING PREDICTIONS')
    with open(Path(DATA_DIR, 'model.pkl'), 'rb') as file:
        model = pickle.load(file)

    preds = model.predict(data)

    return preds

def create_dataframes(results, general_ranking, home_ranking, away_ranking):
    results_cols = ['season', 'league_match', 'home', 'team_1', 'team_2',
                    'outcome']
    ranking_cols = ['season', 'league_match', 'rank_pos', 'team',
                    'matches', 'wins', 'draws', 'losses', 'goals_scored',
                    'goals_conceded', 'goals_difference']

    results_df = pd.DataFrame(results, columns=results_cols)
    #TODO: Check why the results come with the before league match number
    results_df['league_match'] = results_df['league_match'] + 1

    general_df = pd.DataFrame(general_ranking, columns=ranking_cols)

    home_df = pd.DataFrame(home_ranking, columns=ranking_cols)

    away_df = pd.DataFrame(away_ranking, columns=ranking_cols)

    return results_df, general_df, home_df, away_df

if __name__ == '__main__':
    data = load_data()
    logger.info('DATA LOADING')
    preds = generate_preds(data)

    print(preds)