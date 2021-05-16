import pytest

from src.data_scraper.scraper import SeleniumWebScraper

def test_data_scraper_get_matches_data():
    scraper = SeleniumWebScraper(config_file='test/test_data_scraper/test_scraper_config.yml')

    data = scraper.get_matches_data()

    assert len(data) != 0, 'Data retrieved is empty'
    assert data[0][0] == 1999

def test_data_scraper_get_ranks_data():
    scraper = SeleniumWebScraper(config_file='test/test_data_scraper/test_scraper_config.yml')

    data = scraper.get_ranks_data()

    assert len(data) != 0, 'Data retrieved is empty'
    assert data[0][0] == 1999