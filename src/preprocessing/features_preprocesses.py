import pandas as pd
import numpy as np

from abc import ABC, abstractmethod
from typing import Tuple, List
from src.config.logger_config import logger
from src.preprocessing.utils import FeaturePipeline

class FeaturePreprocess(ABC):
    """
    Abstract class which defines some common methods to the
    preprocesses intended to create features.
    """
    def __init__(self, ranking_df: pd.DataFrame,
                columns: List[str], new_columns: List[str]):
        self.ranking_df = ranking_df
        self.columns = columns
        self.new_columns = new_columns

    def _retrieve_team_data(self, season: int,
                            league_match: int, team: str) -> np.ndarray:
        """
        Retrieve a team's statistics

        Parameters
        ----------
        rank_df : pd.DataFrame
            DataFrame containing the whole teams statistics
        season : int
            Season number
        league_match : int
            League match number
        team : str
            Team's name

        Returns
        -------
        array like of shape (, columns)
            Array containing a specific team statistics
        """
        # Subtracts 1 to the league match because we want to retrieve
        # the statistics the teams have before playing a certain match
        league_match -= 1
        # Retrieves the data from the dataframe
        try:
            data = self.ranking_df[(self.ranking_df['season'] == season) 
                        & (self.ranking_df['league_match'] == league_match) 
                        & (self.ranking_df['team'] == team)].values[0]
        except Exception as ex:
            logger.info(f'Preprocess: Error on {season} - {league_match}, {team}')
            raise ex
        
        return data

    def _get_parameters_to_search_team(self, df_row: np.ndarray, team: str
                                        ) -> Tuple[int, int, str]:
        """
        Gets from a certain dataframe row the parameters needed to 
        search a specific team information

        Parameters
        ----------
        df_row : array like of shape (, columns)
            Array containing the data from a dataframe row
        team : str
            Team's name

        Returns
        -------
        Tuple[int, int, str]
            Tuple containing the parameters needed to obtain a team's statistics
        """
        season, league_match = df_row[0], df_row[1]
        
        if team == 'team_1':
            team = df_row[3]
        else:
            team = df_row[4]
            
        return season, league_match, team

    def _get_team_data(self, df_row: np.ndarray, rank_df: pd.DataFrame,
                        team: str) -> np.ndarray:
        """
        Get the statistics related from a certain team

        Parameters
        ----------
        df_row : array like of shape (, columns)
            Array containing the data from a dataframe row
        rank_df : pd.DataFrame
            Dataframe containing team statistics
        team : str
            Team's name

        Returns
        -------
        array like of shape (, columns)
            Array containing a team statistics
        """
        season, league_match, team = self._get_parameters_to_search_team(df_row,
                                                                        team)
        
        data = self._retrieve_team_data(season, league_match, team)

        return data

    def __call__(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        # Zip the columns and new columns to iterate through them
        for column, new_column in zip(self.columns, self.new_columns):
            dataframe[new_column] = dataframe.apply(self._compute_feature, 
                                                    args=(column,), axis=1)

        return dataframe

    @abstractmethod
    def _compute_feature(self, df_row: np.ndarray, team: str) -> int:
        pass

class ComputeLeagueRankPosition(FeaturePreprocess):
    def __init__(self, *args):
        super().__init__(*args)

    def _compute_feature(self, df_row: np.ndarray, team: str) -> int:
        data = self._get_team_data(df_row, self.ranking_df, team)
        
        return data[2]

class ComputeWins(FeaturePreprocess):
    def __init__(self, *args):
        super().__init__(*args)

    def _compute_feature(self, df_row: np.ndarray, team: str) -> int:
        data = self._get_team_data(df_row, self.ranking_df, team)
        
        return int(data[5])

class ComputeDraws(FeaturePreprocess):
    def __init__(self, *args):
        super().__init__(*args)

    def _compute_feature(self, df_row: np.ndarray, team: str) -> int:
        data = self._get_team_data(df_row, self.ranking_df, team)
        
        return int(data[6])

class ComputeLosses(FeaturePreprocess):
    def __init__(self, *args):
        super().__init__(*args)

    def _compute_feature(self, df_row: np.ndarray, team: str) -> int:
        data = self._get_team_data(df_row, self.ranking_df, team)
        
        return int(data[7])

class ComputeGoalsScored(FeaturePreprocess):
    def __init__(self, *args):
        super().__init__(*args)

    def _compute_feature(self, df_row: np.ndarray, team: str) -> int:
        data = self._get_team_data(df_row, self.ranking_df, team)
        
        return int(data[8])

class ComputeGoalsConceded(FeaturePreprocess):
    def __init__(self, *args):
        super().__init__(*args)

    def _compute_feature(self, df_row: np.ndarray, team: str) -> int:
        data = self._get_team_data(df_row, self.ranking_df, team)
        
        return int(data[9])

def get_feature_pipeline(general, home, away):
    # Compute general, home and away wins
    wins_pipeline = FeaturePipeline([
        ComputeWins(general,
                    ['team_1', 'team_2'],
                    ['general_wins_t1', 'general_wins_t2']),
        ComputeWins(home,
                    ['team_1', 'team_2'],
                    ['home_wins_t1', 'home_wins_t2']),
        ComputeWins(away,
                    ['team_1', 'team_2'],
                    ['away_wins_t1', 'away_wins_t2']),
    ])
    # General, home and away draws
    draws_pipeline = FeaturePipeline([
        ComputeDraws(general,
                    ['team_1', 'team_2'],
                    ['general_draws_t1', 'general_draws_t2']),
        ComputeDraws(home,
                    ['team_1', 'team_2'],
                        ['home_draws_t1', 'home_draws_t2']),
        ComputeDraws(away,
                    ['team_1', 'team_2'],
                    ['away_draws_t1', 'away_draws_t2']),
    ])
    # General, home and away losses
    loss_pipeline = FeaturePipeline([
        ComputeLosses(general,
                    ['team_1', 'team_2'],
                    ['general_losses_t1', 'general_losses_t2']),
        ComputeLosses(home,
                    ['team_1', 'team_2'],
                    ['home_losses_t1', 'home_losses_t2']),
        ComputeLosses(away,
                    ['team_1', 'team_2'],
                    ['away_losses_t1', 'away_losses_t2']),      
    ])
    # General, home and away goals scored
    goals_scored_pipeline = FeaturePipeline([
        ComputeGoalsScored(
                general,
                ['team_1', 'team_2'],
                ['general_goals_scored_t1', 'general_goals_scored_t2']),
        ComputeGoalsScored(
                home,
                ['team_1', 'team_2'],
                ['home_goals_scored_t1', 'home_goals_scored_t2']),
        ComputeGoalsScored(
                away,
                ['team_1', 'team_2'],
                ['away_goals_scored_t1', 'away_goals_scored_t2'])
    ])
    # General, home and away goals conceded
    goals_conceded_pipeline = FeaturePipeline([
        ComputeGoalsConceded(
                general,
                ['team_1', 'team_2'],
                ['general_goals_conceded_t1', 'general_goals_conceded_t2']),
        ComputeGoalsConceded(
                home,
                ['team_1', 'team_2'],
                ['home_goals_conceded_t1', 'home_goals_conceded_t2']),
        ComputeGoalsConceded(
                away,
                ['team_1', 'team_2'],
                ['away_goals_conceded_t1', 'away_goals_conceded_t2'])
    ])

    # Feature preprocessing pipeline
    pipeline = FeaturePipeline([
        ComputeLeagueRankPosition(general, ['team_1', 'team_2'],
                                ['rank_t1', 'rank_t2']),
        wins_pipeline,
        draws_pipeline,
        loss_pipeline,
        goals_scored_pipeline,
        goals_conceded_pipeline
    ])

    return pipeline