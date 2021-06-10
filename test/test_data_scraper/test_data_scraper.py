import pytest
import os
from src.data_scraper.scraper import SeleniumWebScraper

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

def test_data_scraper_get_matches_data():
    driver = os.path.join(THIS_DIR, 'geckodriver')
    scraper = SeleniumWebScraper(config_file='test/test_data_scraper/test_scraper_config.yml',
                                driver_path=driver)

    data = scraper.get_matches_data()

    assert data, 'Data retrieved is empty'
    assert len(data) == 10
    assert data[0][0] == 1999

def test_data_scraper_get_ranks_data():
    driver = os.path.join(THIS_DIR, 'geckodriver')
    scraper = SeleniumWebScraper(config_file='test/test_data_scraper/test_scraper_config.yml',
                                driver_path=driver)

    data = scraper.get_ranks_data()

    assert data, 'Data retrieved is empty'
    assert len(data) == 20
    assert data[0][0] == 1999