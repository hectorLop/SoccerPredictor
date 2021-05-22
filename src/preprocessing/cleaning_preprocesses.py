from typing import Dict
import pandas as pd
import numpy as np

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
    def __init__(self, characters: str = '\n* ') -> None:
        self._characters = characters

    def __call__(self, dataframe: pd.DataFrame, column: str) -> pd.DataFrame:
        # Check if the dataframe column is of type string
        if not dataframe[column].dtype == 'O':
            raise ValueError('Dataframe column values must be strings')
        
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
    def __init__(self) -> None:
        pass

    def __call__(self, dataframe: pd.DataFrame, column: str, map_dict: Dict) -> pd.DataFrame:
        # Replace the old names by the new ones
        dataframe[column] = dataframe[column].replace(map_dict)

        return dataframe