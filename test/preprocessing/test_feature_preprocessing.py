from test.data.data_fixtures import get_features_df
import pytest

from src.preprocessing.features_preprocesses import (
    get_feature_pipeline,
    FeaturePipeline,
    ComputeWins
)
from pandas._testing import assert_frame_equal

from test.data.data_fixtures import get_features_df

def test_feature_pipeline(get_features_df):
    results, general, home, away, expected_results = get_features_df

    pipeline = get_feature_pipeline(general, home, away)

    results_trans = pipeline(results)

    assert_frame_equal(results_trans, expected_results)