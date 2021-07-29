import pytest
import pandas as pd
import numpy as np
from pandas._testing import assert_frame_equal

from src.preprocessing.cleaning_preprocesses import (
    Pipeline,
    RemoveSpecialCharacters,
    RemoveFirstLeagueMatch,
    RenameTeams
)

from test.data.data_fixtures import get_df_to_clean

def test_remove_special_characters(get_df_to_clean):
    characters = ['\n', '*', ' ']

    remove_characters = RemoveSpecialCharacters(['team_1'], characters)
    clean_df = remove_characters(get_df_to_clean)

    for char in characters:
        assert char not in clean_df['team_1']

def test_remove_first_league_match(get_df_to_clean):
    remover = RemoveFirstLeagueMatch()
    cleaned_df = remover(get_df_to_clean)

    assert np.unique(cleaned_df['league_match'])[0] != 1

def test_rename_teams(get_df_to_clean):
    renamer = RenameTeams(['team_1'],
                        {'Gimnàstic Tarragona': 'Gimnàstic'})
    cleaned_df = renamer(get_df_to_clean)

    assert cleaned_df['team_1'][3] == 'Gimnàstic'

def test_cleaning_pipeline(get_df_to_clean):
    data = {
        'league_match': [2, 3, 4],
        'team_1': ['madrid', 'valencia', 'Gimnàstic']
    }
    expected_df = pd.DataFrame(data)

    matches_pipeline = Pipeline([
        RemoveFirstLeagueMatch(),
        RemoveSpecialCharacters(['team_1'], ['\n', '*', ' ']),
        RenameTeams(['team_1'], {'Gimnàstic Tarragona': 'Gimnàstic'})
    ])
    cleaned_df = matches_pipeline.transform(get_df_to_clean)

    assert_frame_equal(cleaned_df, expected_df)