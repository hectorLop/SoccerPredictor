import scrapy
import logging
import re

from src.scraper.spiders import GeneralDataSpider, AwayDataSpider, HomeDataSpider
from scrapy.crawler import CrawlerProcess
from typing import Dict, Tuple, List
from itertools import product
from src.config.logger_config import logger

logging.getLogger('scrapy').propagate = False

class Scraper():
    """
    Scrapy Scraper class

    Parameters
    ----------
    config : dict
        Dictionary containing the scraper configuration

    Attributes
    ----------
    _process : CrawlerProcess
        Scrapy CrawlerProcess object
    _config: dict
        Dictionary containing the scraper configuration
    """

    def __init__(self, config: Dict):
        self._process = CrawlerProcess()
        self._config = config

    def _generate_urls(self) -> Tuple[List, List, List]:
        """
        Generates the urls to be scrapped

        Returns
        -------
        tuple: 
            A tuple containing:
                - general_urls (list): List containing the urls to retrieve the 
                        general statistics
                - home_urls (list): List containing the urls to retrieve the 
                        in home statistics
                - away_urls (list): List containing the urls to retrieve the 
                        outside home statistics
        """
        general_urls, home_urls, away_urls = [], [], []
        
        # Iterator ranges
        season_range = range(
            self._config['start_season'],
            self._config['end_season'] + 1
            )
        # There are 38 league matches per season
        league_match_range = range(self._config['start_league_match'], 39)
        
        for season, league_match in product(season_range, league_match_range):
            # Stopping criteria
            if (season, league_match) == (self._config['end_season'], self._config['end_league_match']):
                logger.info(f"""Scraping stopping criteria reached in
                            Season{season} - League Match {league_match}""")
                break
            # The URL from 2016/2017 season is slightly different
            elif season == 2016:
                general_url = self._config['general_url_2016']
                home_url = self._config['home_url_2016']
                away_url = self._config['away_url_2016']
            # Normal case
            else:
                general_url = self._config['general_url']
                home_url = self._config['home_url']
                away_url = self._config['away_url']
            
            general_urls.append(general_url.format(season=season,
                                                  season_end=season+1,
                                                  league_match=league_match))
            home_urls.append(home_url.format(season=season,
                                             season_end=season+1,
                                             league_match=league_match))
            away_urls.append(away_url.format(season=season,
                                             season_end=season+1,
                                             league_match=league_match))
                
        return general_urls, home_urls, away_urls

    def scrap_data(self):
        soccer_urls, home_urls, away_urls = self._generate_urls()

        info = {
            'general': [],
            'home': [],
            'away': [],
        }

        self._process.crawl(GeneralDataSpider,
                            outputResponse=info,
                            start_urls=soccer_urls)
        self._process.crawl(HomeDataSpider,
                            outputResponse=info,
                            start_urls=home_urls)
        self._process.crawl(AwayDataSpider,
                            outputResponse=info,
                            start_urls=away_urls)
        self._process.start()

        return info