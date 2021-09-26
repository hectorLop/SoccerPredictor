from itertools import product
from typing import Dict, List, Tuple
from src.config.logger_config import logger

import re

class DataParser():
    def __init__(self) -> None:
        pass

    def parse_home_away_data(self, data: List):
        cleaned_data = []
        ranking_parser = RankingDataParser()
        
        for element in data:
            try:
                season, league_match = self._parse_season_and_league_match(element[0])
                parsed_data = ranking_parser.parse_ranking(element[1], season, league_match)
                
                cleaned_data += parsed_data
            except:
                logger.error('Failed to parse ')
                pass
            
        return cleaned_data

    def parse_general_data(self, data: List):
        cleaned_ranking, cleaned_results = [], []
        results_parser = ResultsDataParser()
        ranking_parser = RankingDataParser()
        
        for element in data:
            try:
                season, league_match = self._parse_season_and_league_match(element[0])
                results, ranking = self._get_results_and_ranking(element[1])
            
                parsed_ranking = ranking_parser.parse_ranking(ranking, season, league_match)
                parsed_results = results_parser.parse_results(results, season, league_match)

                cleaned_ranking += parsed_ranking
                cleaned_results += parsed_results
            except:
                logger.error('Failed to parse ')
                pass
                        
        return cleaned_ranking, cleaned_results

    def _get_results_and_ranking(self, data):
        for idx, element in enumerate(data):
            if element == '#':
                results = data[:idx]
                ranking = data[idx:]
                
                return results, ranking
            
        return None, None

    def _parse_season_and_league_match(self, data):
        data = data.split('»')
        season_data = data[0].split(' ')[2]
        season = season_data.split('/')[0]
        
        league_match = data[1].split('.')[0]
        
        return season, league_match

class RankingDataParser():
    def __init__(self) -> None:
        pass

    def parse_ranking(self, ranking_data, season, league_match):
        # Remove useless data
        ranking_data = ranking_data[9:-1]

        parsed_data = []
        
        for i in range(0, len(ranking_data)):
            if re.match('[A-Z]+\s?[A-Z]*[a-z]+', normalize_unicode(ranking_data[i])):
                data = ranking_data[i:i + 8]
                data[0] = normalize_unicode(data[0])

                # Get the for and against goals (eg. 6:1)
                for_goals, against_goals = data[5].split(':')
                data = data[:5] + [for_goals, against_goals] + data[6:]

                rank_position = len(parsed_data) + 1

                parsed_data.append((season, league_match, rank_position, *data))

        return parsed_data

class ResultsDataParser():
    def __init__(self) -> None:
        pass

    def parse_results(self, data, season, league_match):
        parsed_results = []

        for i in range(0, len(data)):
            if data[i] == '-':
                home_team = normalize_unicode(data[i - 1])
                away_team = normalize_unicode(data[i + 1])
                result = data[i + 2]

                try:
                    outcome = self.parse_outcome(result, league_match)
                    if self.is_second_round(league_match):
                        home = 'team_2'
                    else:
                        home = 'team_1'

                    parsed_results.append((season, league_match, home, home_team, away_team, outcome))
                except ValueError:
                    pass
                
        return parsed_results

    def parse_outcome(self, result, league_match):
        result = result.split(' ')[0]
        home_goals, visitor_goals = result.split(':')
        
        outcome = self.get_outcome(home_goals, visitor_goals)
        
        if self.is_second_round(league_match): # Is first round
            if outcome == 'team_1':
                return 'team_2'
            elif outcome == 'team_2':
                return 'team_1'
        
        return outcome
    
    def get_outcome(self, home_goals, visitor_goals):
        if home_goals > visitor_goals:
            return 'team_1'
        elif home_goals < visitor_goals:
            return 'team_2'
        else:
            return 'draw'    
        
    def is_second_round(self, league_match):
        return int(league_match) >= 20

def normalize_unicode(word):
    normalMap = {'À': 'A', 'Á': 'A', 'Â': 'A', 'Ã': 'A', 'Ä': 'A',
             'à': 'a', 'á': 'a', 'â': 'a', 'ã': 'a', 'ä': 'a', 'ª': 'A',
             'È': 'E', 'É': 'E', 'Ê': 'E', 'Ë': 'E',
             'è': 'e', 'é': 'e', 'ê': 'e', 'ë': 'e',
             'Í': 'I', 'Ì': 'I', 'Î': 'I', 'Ï': 'I',
             'í': 'i', 'ì': 'i', 'î': 'i', 'ï': 'i',
             'Ò': 'O', 'Ó': 'O', 'Ô': 'O', 'Õ': 'O', 'Ö': 'O',
             'ò': 'o', 'ó': 'o', 'ô': 'o', 'õ': 'o', 'ö': 'o', 'º': 'O',
             'Ù': 'U', 'Ú': 'U', 'Û': 'U', 'Ü': 'U',
             'ù': 'u', 'ú': 'u', 'û': 'u', 'ü': 'u',
             'Ñ': 'N', 'ñ': 'n',
             'Ç': 'C', 'ç': 'c',
             '§': 'S',  '³': '3', '²': '2', '¹': '1'}
    normalize = str.maketrans(normalMap)

    return word.translate(normalize)