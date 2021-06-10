from typing import Dict, List
import pandas as pd
import numpy as np

class Pipeline():
    def __init__(self, preprocesses: List) -> None:
        self.preprocesses = preprocesses

    def transformm(self, dataframe):
        for preprocess in self.preprocesses:
            dataframe = preprocess(dataframe)

        return dataframe

class RemoveSpecialCharacters():
    """
    Remove special characters, whitespaces and line breaks
    from a specific dataframe column.

    Parameters
    ----------
    _characters : str
        String containing the special characters to be removed.
        Default are line breaks and whitespaces.

    Attributes
    ----------
    _characters : str
        String containing the special characters to be removed
    """
    def __init__(self, columns: List[str], characters: List[str]) -> None:
        self._characters = ''.join(characters)
        self._columns = columns

    def __call__(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        for column in self._columns:
            # Check if the dataframe column is of type string
            if not dataframe[column].dtype == 'O':
                raise ValueError(f'{column} column must be of type string')
            
            # Remove the special characters
            dataframe[column] = dataframe[column].apply(
                                                self._remove_special_characters)

        return dataframe

    def _remove_special_characters(self, word: str) -> str:
        """
        Remove a certain set of characters from a word.

        Parameters
        ----------
        word : str
            Word to be cleaned

        Returns
        -------
        str
            Cleaned word
        """
        return word.strip(self._characters)

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

        return dataframe

class RenameTeams():
    """
    Rename a certain set of teams
    """
    def __init__(self, columns: List[str], map_dict: Dict) -> None:
        self._columns = columns
        self._map_dict = map_dict

    def __call__(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        for column in self._columns:
            # Replace the old names by the new ones
            dataframe[column] = dataframe[column].replace(self._map_dict)

        return dataframe