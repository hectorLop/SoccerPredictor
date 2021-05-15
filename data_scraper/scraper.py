import yaml
from typing import Dict, List, Tuple
from abc import ABC, abstractmethod

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Firefox

class SeleniumWebScraper():
    """
    This class models a web scraper using Selenium

    Parameters
    ----------
    config_file : str
        Configuration file path
    driver_path : str
        Selenium driver path. Default is 'geckodriver' by PATH access.

    Attributes
    ----------
    _webdriver : object
        Selenium webdriver.
    _config : dict
        Dictionary containing the scraper configuration.
    """
    def __init__(self, config_file: str, driver_path: str = 'geckodriver') -> None:
        self._webdriver = self._create_webdriver(driver_path)
        self._config = self._get_config_from_yaml(config_file)

    def _create_webdriver(self, driver_path: str = 'geckodriver') -> webdriver.Firefox:
        """
        Creates a Firefox webdriver

        Returns
        -------
        driver : webdriver.Firefox
            Object which represents the Firefox webdriver
        """
        # Add options to hide the webdriver window
        options = webdriver.FirefoxOptions()
        options.add_argument('-headless')
        driver = webdriver.Firefox(executable_path=driver_path, options=options)
        
        return driver

    def _get_config_from_yaml(self, config_file: str):
        """
        Gets the scraper configuration from the config yaml file.

        Parameters
        ----------
        config_file : str
            Configuration YAML file path
        
        Returns
        -------
        config : dict
            Dictionary containing the YAML information
        """
        with open(config_file) as file:
            config = yaml.load(file, Loader=yaml.FullLoader)

        return config
    
    def get_matches_data(self):
        """
        Gets the matches related data.

        Returns
        -------
        data : List[Tuple]
            List containing a tuple for each match
        """
        scraper = MatchesDataScraper(self._webdriver, self._config['matches_data'])
        data = scraper.get_data()
        
        return data

    def get_ranks_data(self):
        """
        Gets the ranking related data.

        Returns
        -------
        data : List[Tuple]
            List containing a tuple for each team.
        """
        scraper = RanksDataScraper(self._webdriver, self._config['ranks_data'])
        data = scraper.get_data()

        return data

class DataScraper(ABC):
    """
    Abstract class which defines the interface for a scraper 
    of the https://www.resultados-futbol.com webpage

    Parameters
    ----------
    webdriver : object
        Selenium webdriver
    data_config : dict
        Dictionary containing the information to retrieve the requested data

    Attributes
    ----------
    _webdriver : object
        Selenium webdriver
    _config : dict
        Dictionary containing the information to retrieve the requested data
    """
    def __init__(self, webdriver: Firefox, data_config: Dict) -> None:
        self._webdriver = webdriver
        self._config = data_config

    @abstractmethod
    def get_data(self):
        pass


class MatchesDataScraper(DataScraper):
    """
    Scraper to retrieve match related data.

    Parameters
    ----------
    webdriver : selenium.webdriver.Firefox
        Firefox selenium webdriver
    matches_data_config : dict
        Dictionary containing the scraper's config

    Attributes
    ----------
    _webdriver : selenium.webdriver.Firefox
        Firefox selenium webdriver
    _config : dict
        Dictionary containing the scraper's config
    """
    def __init__(self, webdriver: Firefox, matches_data_config: Dict) -> None:
        super().__init__(webdriver, matches_data_config)

    def get_data(self) -> List[Tuple[int, int, str, str, str, str]]:
        """
        Retrieves the desired data using the configuration file.

        Returns
        -------
        full_matches_data : list[tuple[int, int, str, str, str, str]]
            List of tuples. Each tuple represents a match related data.
        """
        full_matches_data = []
        
        for season in range(self._config['starter_season'], self._config['end_season'] + 1):
            for league_match in range(1, self._config['max_league_match'] + 1):
                # Creates the url to retrieve the data
                url = self._config['url'].format(season, league_match)      
                self._webdriver.get(url)
                
                partial_matches_data = self._retrieve_matches_data()        

                for match in partial_matches_data:
                    if self._is_first_round(league_match): 
                        home = 'team_1' # If it is the first round, the team_1 plays in its stadium
                        full_matches_data.append((season, league_match, home, *match))
                    else:
                        home = 'team_2' # team_2 plays in its stadium
                        outcome = self._get_second_round_outcome(match[2]) # The outcome needs to be changed in the 2nd round
                        full_matches_data.append((season, league_match, home, match[1], match[0], outcome)) 
                                                
        return full_matches_data

    def _is_first_round(self, league_match: int) -> bool:
        """
        Determines if a league match belong to the second round.
        In LaLiga the second round starts in the league match number 20.

        Parameters
        ----------
        league_match : int
            League match number

        Returns
        -------
        bool
            True if the league match belongs to the second round, False otherwise.
        """
        return league_match < 20

    def _get_second_round_outcome(self, outcome: str) -> str:
        """
        Changes the outcome when the league match belongs to the second round.

        Parameters
        ----------
        outcome : str
            Current outcome

        Returns
        -------
        str
            New outcome
        """
        new_outcomes = {
            'team_1': 'team_2',
            'team_2': 'team_1',
            'draw': 'draw'
        }

        return new_outcomes[outcome]

    def _retrieve_matches_data(self) -> List[Tuple[str, str, str]]:
        """
        Retrieves the matches related data.
        The matches related data is composed of the both teams that
        played the match and the match outcome.

        Returns
        -------
        matches : list [tuple [str, str, str]] 
            List contaning matches info. Each match is represented as a tuple.
        """
        # Gets teams and results for each match
        teams = self._webdriver.find_elements_by_xpath(self._config['teams_xpath'])
        results = self._webdriver.find_elements_by_xpath(self._config['results_xpath'])
        
        matches = []
        
        for i in range(len(results)):
            # Teams which played the match
            team_1, team_2 = teams[i].get_attribute('title').split('-')
            # Match outcome
            outcome = self._get_outcome(results[i].text)
            
            matches.append((team_1, team_2, outcome))
        
        return matches
            
    def _get_outcome(self, result: str) -> str:
        """
        Determines the outcome from a match

        Parameters
        ----------
        result : str
            Match result in digits. E.g 2-1

        Returns
        -------
        str
            Match outcome in categories. The categories are team_1 win,
            team_2 win or draw
        """
        # Get the number of goals for both teams
        home_team_goals, visitor_team_goals = [int(result) for result in result.split('-')]
        
        if home_team_goals > visitor_team_goals:
            return 'team_1'
        elif visitor_team_goals > home_team_goals:
            return 'team_2'
        else:
            return 'draw'

class RanksDataScraper(DataScraper):
    def __init__(self, webdriver: Firefox, data_config: Dict) -> None:
        super().__init__(webdriver, data_config)

    def get_data(self):
        full_ranks_data = []

        for season in range(self._config['starter_season'], self._config['end_season'] + 1):
            for league_match in range(1, self._config['max_league_match'] + 1):
                # Creates the url to retrieve the data
                url = self._config['url'].format(season, league_match)      
                self._webdriver.get(url)

                raw_teams_data = self._retrieve_raw_teams_ranking_data()
                teams_info = self._get_teams_info(raw_teams_data)

                for info in teams_info:
                    full_ranks_data.append((season, league_match, *info))

        return full_ranks_data

    def _retrieve_raw_teams_ranking_data(self):
        # HTML element containing the ranking
        ranking_element = self._webdriver.find_element_by_id('clasificacion')

        # Table containing the teams ranking data
        rank_data = ranking_element.find_element_by_id('tabla2')
        rank_body = rank_data.find_element_by_tag_name('tbody')     
        teams_data = rank_body.find_elements_by_tag_name('tr')
    
        return teams_data

    def _get_teams_info(self, teams):
        teams_info = []
        
        for team in teams:
            wins = team.find_element_by_class_name('win')
            home_wins = wins.get_attribute('data-home')
            away_wins = wins.get_attribute('data-away')

            losses = team.find_element_by_class_name('lose')
            home_losses = losses.get_attribute('data-home')
            away_losses = losses.get_attribute('data-away')

            draws = team.find_element_by_class_name('draw')
            home_draws = draws.get_attribute('data-home')
            away_draws = draws.get_attribute('data-away')

            rank = team.find_element_by_tag_name('th').text

            goals_scored = team.find_element_by_class_name('f').text
            goals_conceded = team.find_element_by_class_name('c').text
            
            team_name = team.find_element_by_class_name('equipo').text
            
            win_streak, draw_streak, loss_streak = self._get_teams_streaks(team)
            
            teams_info.append((rank, team_name, home_wins, away_wins, home_losses, away_losses, home_draws, away_draws,
                            goals_scored, goals_conceded, win_streak, draw_streak, loss_streak))
        
        return teams_info

    def _get_teams_streaks(self, team):
        icons = team.find_elements_by_class_name('tooltip.left.form-icon')
        streak = []
        
        for s in icons[::-1]:
            result = s.get_attribute('class')
            
            if result == 'tooltip left form-icon form-win':
                streak.append('W')
            elif result == 'tooltip left form-icon form-loss':
                streak.append('L')
            else:
                streak.append('D')
        
        streaks = self._compute_streak(streak)
        
        return streaks['W'], streaks['D'], streaks['L']
        
    def _compute_streak(self, streak):
        streaks = {
            'W': 0,
            'D': 0,
            'L': 0
        }
        
        streaks[streak[0]] += 1
        
        for s in streak[1:]:
            if streaks[s] > 0:
                streaks[s] += 1
            else:
                return streaks
        
        return streaks