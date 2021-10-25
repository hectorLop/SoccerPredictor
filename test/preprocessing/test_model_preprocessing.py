import pytest
import pandas as pd

from numpy.testing import assert_almost_equal
from src.preprocessing.model_preprocessing import ModelPreprocesser
from src.config.config import VARIABLES

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

    expected_variables = VARIABLES[:-1] + ['results_id', 'created_on']
    
    assert expected_variables == list(X_trans.columns)