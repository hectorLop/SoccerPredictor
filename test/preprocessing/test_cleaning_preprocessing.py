import pytest
import pandas as pd
import numpy as np
from pandas._testing import assert_frame_equal

from src.preprocessing.cleaning_preprocesses import (
    Pipeline,
    RemoveSpecialCharacters,
    RemoveFirstLeagueMatch,
)
from src.config.logger_config import logger
from test.data.data_fixtures import get_df_to_clean

def test_remove_special_characters(get_df_to_clean):
    """
    Test the RemoveSpecialCharacters preprocess
    """
    logger.info('Testing the RemoveSpecialCharacters preprocess...')

    # Remove special characters from 'team_1'
    remove_characters = RemoveSpecialCharacters(['team_1'])
    clean_df = remove_characters(get_df_to_clean)

    # Assert that there are not special characters
    assert clean_df['team_1'].str.match(r'\W+').sum() == 0

def test_remove_first_league_match(get_df_to_clean):
    """
    Test the RemoveFirstLeagueMatch preprocess
    """
    logger.info('Testing the RemoveFirstLeagueMatch preprocess...')

    # Remove the records from the first league match
    remover = RemoveFirstLeagueMatch()
    cleaned_df = remover(get_df_to_clean)

    assert cleaned_df['league_match'].min() != 1

def test_cleaning_pipeline(get_df_to_clean):
    """
    Tests the full cleaning pipeline
    """
    logger.info('Testing the full cleaning pipeline...')
    
    # Expected data
    data = {
        'league_match': [2, 3, 4],
        'team_1': ['madrid', 'valencia', 'Gimnastic']
    }
    expected_df = pd.DataFrame(data)

    # Cleaning pipeline
    cleaning_pipeline = Pipeline([
        RemoveFirstLeagueMatch(),
        RemoveSpecialCharacters(['team_1']),
    ])
    cleaned_df = cleaning_pipeline.transform(get_df_to_clean)

    assert_frame_equal(cleaned_df, expected_df)