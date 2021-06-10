from pytest import fixture

import pandas as pd
import os

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

@fixture
def get_dataframes():
    matches_df = pd.read_csv(os.path.join(THIS_DIR, 'test_matches_df.csv'))
    rank_df = pd.read_csv(os.path.join(THIS_DIR, 'test_rank_df.csv'))

    return matches_df, rank_df

@fixture
def get_removed_characters_df():
    matches_df = pd.read_csv(os.path.join(THIS_DIR,
                                        'test_matches_df_no_chars.csv'))
    rank_df = pd.read_csv(os.path.join(THIS_DIR, 'test_rank_df_no_chars.csv'))

    return matches_df, rank_df

@fixture
def get_renamed_df():
    matches_df = pd.read_csv(os.path.join(THIS_DIR,
                                        'test_matches_df_rename.csv'))

    return matches_df