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

from test.data.data_fixtures import (
    get_dataframes,
    get_removed_characters_df,
    get_renamed_df,
    get_cleaned_df
)

def test_remove_special_characters(get_dataframes, get_removed_characters_df):
    matches_df, rank_df = get_dataframes
    expected_matches_df, expected_rank_df = get_removed_characters_df

    characters = ['\n', '*', ' ']

    remove_characters = RemoveSpecialCharacters(['team_1', 'team_2'],
                                                characters)
    matches_df_trans = remove_characters(matches_df)

    remove_characters = RemoveSpecialCharacters(['team'],
                                                characters)
    rank_df_trans = remove_characters(rank_df)

    assert_frame_equal(matches_df_trans, expected_matches_df)
    assert_frame_equal(rank_df_trans, expected_rank_df)

def test_remove_first_league_match(get_dataframes):
    # Get the test dataframe
    matches_df, _ = get_dataframes

    # Transform the data
    remove_first_league_match = RemoveFirstLeagueMatch()
    transformed_df = remove_first_league_match(matches_df)

    # Get the league match values
    league_matches = transformed_df['league_match']

    # Assert if the first league match has been removed
    assert np.unique(league_matches)[0] != 1

def test_rename_teams(get_dataframes, get_renamed_df):
    matches_df, _ = get_dataframes
    expected_matches_df = get_renamed_df

    renamer = RenameTeams(['team_1', 'team_2'],
                        {'Gimnàstic Tarragona': 'Gimnàstic'})

    matches_df_trans = renamer(matches_df)

    assert_frame_equal(expected_matches_df, matches_df_trans)

def test_cleaning_pipeline(get_dataframes, get_cleaned_df):
    matches_df, rank_df = get_dataframes
    expected_matches_df, expected_rank_df = get_cleaned_df

    characters = ['\n', '*', ' ']

    matches_pipeline = Pipeline([
        RemoveFirstLeagueMatch(),
        RemoveSpecialCharacters(['team_1', 'team_2'], characters),
        RenameTeams(['team_1', 'team_2'], {'Gimnàstic Tarragona': 'Gimnàstic'})
    ])

    rank_pipeline = Pipeline([
        RemoveSpecialCharacters(['team'], characters)
    ])

    matches_df_trans = matches_pipeline.transform(matches_df)
    rank_df_trans = rank_pipeline.transform(rank_df)

    assert_frame_equal(matches_df_trans, expected_matches_df)
    assert_frame_equal(rank_df_trans, expected_rank_df)