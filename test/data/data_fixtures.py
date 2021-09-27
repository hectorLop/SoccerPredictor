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
        'team_1': ['barsa\n', '*madrid*', 'valencia ', 'Gimnastic*']
    }

    return pd.DataFrame(data)

@fixture
def get_features_df():
    results_dir = os.path.join(THIS_DIR, 'results_1999.csv')
    results = pd.DataFrame(results_dir)

    general_ranking_dir = os.path.join(THIS_DIR, 'general_ranking_1999.csv')
    general_ranking = pd.DataFrame(general_ranking_dir)

    home_ranking_dir = os.path.join(THIS_DIR, 'home_ranking_1999.csv')
    home_ranking = pd.DataFrame(home_ranking_dir)

    away_ranking_dir = os.path.join(THIS_DIR, 'away_ranking_1999.csv')
    away_ranking = pd.DataFrame(away_ranking_dir)

    results_trans_dir = os.path.join(THIS_DIR, 'results_1999_transformed.csv')
    results_trans = pd.DataFrame(results_trans_dir)

    return results, general_ranking, home_ranking, away_ranking, results_trans

# @fixture
# def get_features_df():
#     matches_df = pd.read_csv(os.path.join(THIS_DIR,
#                                         'test_matches_df_features_pip.csv'))

#     return matches_df

# @fixture
# def get_transformed_test_data():
#     test_data = np.load(os.path.join(THIS_DIR,
#                                         'transformed_test_data.npy'))

#     return test_data