from pytest import fixture

import pandas as pd
import numpy as np
import os

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

@fixture
def get_cleaned_df():
    matches_df = pd.read_csv(os.path.join(THIS_DIR,
                                        'test_matches_df_pipeline.csv'))
    rank_df = pd.read_csv(os.path.join(THIS_DIR, 'test_rank_df_pipeline.csv'))

    return matches_df, rank_df

@fixture
def get_df_to_clean():
    data = {
        'league_match': [1, 2, 3, 4],
        'team_1': ['barsa\n', '*madrid*', 'valencia ', 'Gimnàstic Tarragona']
    }

    return pd.DataFrame(data)

@fixture
def get_features_df():
    matches_df = pd.read_csv(os.path.join(THIS_DIR,
                                        'test_matches_df_features_pip.csv'))

    return matches_df

@fixture
def get_transformed_test_data():
    test_data = np.load(os.path.join(THIS_DIR,
                                        'transformed_test_data.npy'))

    return test_data