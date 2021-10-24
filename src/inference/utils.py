from pathlib import Path
from src.config.config import CODE_DIR, DATA_DIR
from src.config.logger_config import logger
from src.scraper.scraper import Scraper
from src.scraper.utils import DataParser
from src.preprocessing.config import RANKING_COLS, RESULTS_COLS
from src.preprocessing.features_preprocesses import get_feature_pipeline
from dotenv import load_dotenv
load_dotenv()

import yaml
import pandas as pd
import pickle
import os
import boto3
import json

def get_last_data():
    scraper_config = Path(CODE_DIR, 'inference/scraper_inference_config.yaml')

    with open(scraper_config) as file:
        config = yaml.full_load(file)

    # Set the scraper config
    scraper = Scraper(config)

    # Get the data
    data = scraper.scrap_data()

    # Parse the data
    parser = DataParser()
    general_ranking, results = parser.parse_general_data(data['general'])
    home_ranking = parser.parse_home_away_data(data['home'])
    away_ranking = parser.parse_home_away_data(data['away'])

    # Parse the data to dataframes
    results_df, general_df, home_df, away_df = create_dataframes(results,
                                                                general_ranking,
                                                                home_ranking,
                                                                away_ranking)

    return results_df, general_df, home_df, away_df

def create_dataframes(results, general_ranking, home_ranking, away_ranking):
    results_df = pd.DataFrame(results, columns=RESULTS_COLS)
    results_df['league_match'] = results_df['league_match']

    general_df = pd.DataFrame(general_ranking, columns=RANKING_COLS)
    general_df['league_match'] = general_df['league_match'] - 1

    home_df = pd.DataFrame(home_ranking, columns=RANKING_COLS)
    home_df['league_match'] = home_df['league_match'] - 1

    away_df = pd.DataFrame(away_ranking, columns=RANKING_COLS)
    away_df['league_match'] = away_df['league_match'] - 1

    return results_df, general_df, home_df, away_df

def preprocess_for_inference(results_df, general_df, home_df, away_df):
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

    teams = (results_df['team_1'].values, results_df['team_2'].values)

    return data, teams, results_df['league_match'][0]

def generate_preds(data):
    logger.info('GENERATING PREDICTIONS')
    with open(Path(DATA_DIR, 'model.pkl'), 'rb') as file:
        model = pickle.load(file)

    preds = model.predict(data)

    return preds

def parse_preds(preds, teams, league_match):
    data = {
        'league_match': int(league_match)
    }

    for i in range(len(preds)):
        if preds[i] == 2:
            outcome = 'draw'
        else:
            outcome = teams[preds[i]][i]

        data[f'match_{i}'] = {
            'team_1': teams[0][i],
            'team_2': teams[1][i],
            'outcome': outcome
        }
    print(data)
    # s3_data = json.dumps(data)
    # bucket = os.getenv('AWS_BUCKET')
    # s3_client = boto3.client('s3')
    # s3_client.put_object(Body=s3_data,
    #                     Bucket=bucket,
    #                     Key='predictions/predictions.json')