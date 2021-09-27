from typing import Dict, List
import pandas as pd
import numpy as np

class Pipeline():
    def __init__(self, preprocesses: List) -> None:
        self.preprocesses = preprocesses

    def transform(self, dataframe: pd.DataFrame):
        for preprocess in self.preprocesses:
            dataframe = preprocess(dataframe)

        return dataframe

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

# class RenameTeams():
#     """
#     Rename a certain set of teams
#     """
#     def __init__(self, columns: List[str], map_dict: Dict) -> None:
#         self._columns = columns
#         self._map_dict = map_dict

#     def __call__(self, dataframe: pd.DataFrame) -> pd.DataFrame:
#         for column in self._columns:
#             # Replace the old names by the new ones
#             dataframe[column] = dataframe[column].replace(self._map_dict)

#         return dataframe