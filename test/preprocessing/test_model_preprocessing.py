import pytest
import pandas as pd

from pandas._testing import assert_frame_equal
from src.preprocessing.model_preprocessing import ModelPreprocesser
#from test.data.data_fixtures import get_transformed_test_data, get_features_df

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
    expected_df['created_on'] = expected_df['created_on'].apply(pd.to_datetime)

    assert_frame_equal(X_trans, expected_df)