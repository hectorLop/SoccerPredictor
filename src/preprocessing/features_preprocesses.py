import pandas as pd
import numpy as np

from abc import ABC, abstractmethod
from typing import Tuple, List


class FeaturePreprocess(ABC):
    """
    Abstract class which defines some common methods to the
    preprocesses intended to create features.
    """
    def __init__(self):
        pass

    @abstractmethod
    def __call__(self):
        pass

    def _retrieve_team_data(self, rank_df: pd.DataFrame, season: int,
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
        data = rank_df[(rank_df['season'] == season) 
                    & (rank_df['league_match'] == league_match) 
                    & (rank_df['team'] == team)].values[0]
        
        return data

    def _get_parameters_to_search_team(self, df_row: np.ndarray, team: str) -> Tuple[int, int, str]:
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

    def _get_team_data(self, df_row: np.ndarray, rank_df: pd.DataFrame, team: str) -> np.ndarray:
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
        season, league_match, team = self._compute_search_parameters(df_row, team)
        
        data = self._retrieve_team_data(rank_df, season, league_match, team)

        return data

class ComputeGoalsConceded(FeaturePreprocess):
    def __init__(self, ):
        super().__init__()

    def __call__(self, dataframe: pd.DataFrame, rank_df: pd.DataFrame,
                 columns: List[str], new_columns: List[str]) -> pd.DataFrame:
        # Zip the columns and new columns to iterate through them
        for column, new_column in zip(columns, new_columns):
            dataframe[new_column] = dataframe.apply(self._compute_goals_conceded, 
                                                    args=(rank_df, column),
                                                    axis=1)

        return dataframe

    def _compute_goals_conceded(self, df_row: np.ndarray, rank_df: pd.DataFrame, team: str) -> int:
        data = self._get_team_data(df_row, rank_df, team)
        
        return data[11]