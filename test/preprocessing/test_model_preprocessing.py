import pytest
from numpy.testing import assert_array_equal

from src.preprocessing.model_preprocessing import ModelPreprocesser
from test.data.data_fixtures import get_transformed_test_data, get_features_df

def test_model_preprocessing(get_transformed_test_data, get_features_df):
    expected_test_data = get_transformed_test_data
    test_data = get_features_df

    preprocesser = ModelPreprocesser()

    y = test_data['outcome'].to_numpy()
    X = test_data.drop('outcome', axis=1)

    X_trans = preprocesser.fit_transform(X)

    assert_array_equal(X_trans, expected_test_data)