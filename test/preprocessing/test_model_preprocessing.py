import pytest
import pandas as pd

from numpy.testing import assert_almost_equal
from src.preprocessing.model_preprocessing import ModelPreprocesser

def test_model_preprocessing():
    df = pd.read_csv('test/data/results_1999_transformed.csv')

    preprocesser = ModelPreprocesser()

    y = df['outcome'].replace({
        'team_1': 0,
        'team_2': 1,
        'draw': 2
    })
    X = df.drop('outcome', axis=1)
    X_trans = preprocesser.fit_transform(X)

    expected_df = pd.read_csv('test/data/results_1999_feature_engineered.csv')

    # Exclude 'created_on' column and get the dataframe values
    X_trans_val = X_trans.iloc[:, :-1].values
    expected_df_val = expected_df.iloc[:, :-1].values

    assert_almost_equal(X_trans_val, expected_df_val, decimal=2)