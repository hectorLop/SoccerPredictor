import pytest
import os
import yaml

from src.scraper.scraper import Scraper
from src.scraper.utils import DataParser

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
SCRAPER_CONFIG = os.path.join(THIS_DIR, 'test_scraper_config.yml')

def test_parse_data():
    # Get the scraper config
    with open(SCRAPER_CONFIG) as file:
        config = yaml.full_load(file)

    # Create the scraper
    scraper = Scraper(config)

    # Get the data
    data = scraper.scrap_data()

    parser = DataParser()

    general_ranking, results = parser.parse_general_data(data['general'])
    home_ranking = parser.parse_home_away_data(data['home'])
    away_ranking = parser.parse_home_away_data(data['away'])

    assert general_ranking[0][:4] == ('1999', ' 1', 1, 'Deportivo')
    assert home_ranking[0][:4] == ('1999', ' 1', 1, 'Deportivo')
    assert away_ranking[0][:4] == ('1999', ' 1', 1, 'Rayo')
    assert results[0][:3] == ('1999', ' 1', 'team_1')