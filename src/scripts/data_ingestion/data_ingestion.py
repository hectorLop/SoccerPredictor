import os
from typing import Dict, List, Optional
import yaml
import argparse

from src.config.logger_config import logger
from src.db.data import Results, GeneralRanking, HomeRanking, AwayRanking
from src.db.manager import DBManager
from src.scraper.scraper import Scraper
from src.scraper.utils import DataParser
from src.config.config import SCRAPER_CONFIG_FILE, CODE_DIR

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

def retrieve_data(config: Optional[Dict] = None):
    if not config:
        with open(SCRAPER_CONFIG_FILE) as file:
            config = yaml.full_load(file)

    scraper = Scraper(config)

    logger.info('Scraping data')
    data = scraper.scrap_data()

    parser = DataParser()

    logger.info('Parsing data')
    general_ranking, results = parser.parse_general_data(data['general'])
    home_ranking = parser.parse_home_away_data(data['home'])
    away_ranking = parser.parse_home_away_data(data['away'])

    data = {
        'general_ranking': general_ranking,
        'results': results,
        'home_ranking': home_ranking,
        'away_ranking': away_ranking
    }

    return data

def ingest_data(data: Dict):
    logger.info('Inserting results')
    insert_data(data['results'], Results)
    logger.info('Inserting general ranking')
    insert_data(data['general_ranking'], GeneralRanking)
    logger.info('Inserting home ranking')
    insert_data(data['home_ranking'], HomeRanking)
    logger.info('Inserting away ranking')
    insert_data(data['away_ranking'], AwayRanking)

def insert_data(data: List, table):
    manager = DBManager(os.path.join(CODE_DIR, 'db/db_config.yml'))

    manager.insert(data, table)
    manager.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-s', '--config_file',
                    type=str,
                    default='actual', required=True,
                    help='Scraper config file')
    args = parser.parse_args()

    with open(args.config_file) as file:
        config = yaml.full_load(file)

    data = retrieve_data(config)
    ingest_data(data)