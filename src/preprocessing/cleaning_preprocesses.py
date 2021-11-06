from typing import Dict, List
from src.preprocessing.utils import FeaturePipeline

import pandas as pd

def cleaning_pipeline():
    pipeline = FeaturePipeline([
        RemoveFirstLeagueMatch(),
        RemoveWrongOutcome()
    ])

    return pipeline

class RemoveSpecialCharacters():
    """
    Remove special characters, whitespaces and line breaks
    from a specific dataframe column.

    Parameters
    ----------
    columns : str
        Dataframe's columns to be checked.

    Attributes
    ----------
    _columns : str
        Dataframe's columns to be checked.
    """
    def __init__(self, columns: List[str]) -> None:
        self._columns = columns

    def __call__(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        for column in self._columns:
            # Check if the dataframe column is of type string
            if dataframe[column].str.match(r'\W+').sum() > 0:
                dataframe[column] = dataframe[column].str.replace(r'\W+', '')

        return dataframe

class RemoveFirstLeagueMatch():
    """
    Removes the first league match from each season due it does not have
    any related statistics
    """
    def __init__(self) -> None:
        pass

    def __call__(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        # Exclude rows where the league_match is 1
        dataframe = dataframe[~(dataframe['league_match'] == 1)]
        dataframe = dataframe.reset_index(drop=True)
        
        return dataframe

class RemoveWrongOutcome():
    """
    Removes the first league match from each season due it does not have
    any related statistics
    """
    def __init__(self) -> None:
        pass

    def __call__(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        # Exclude rows where the league_match is 1
        valid_indices = dataframe['outcome'].isin(['team_1', 'team_2', 'draw']).values
        dataframe = dataframe.loc[valid_indices, :].copy()
        
        return dataframe