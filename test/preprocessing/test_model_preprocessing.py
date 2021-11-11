import pytest
import pandas as pd
import numpy as np

from src.preprocessing.model_preprocessing import (
    feature_eng_pipeline,
    FeatureSelector,
    ToDataset,
    WinRatio,
    DrawRatio,
    LossRatio,
)
from src.config.config import VARIABLES

def test_model_preprocessing():
    """
    Test the model preprocessing pipeline
    """
    df = pd.read_csv('test/data/results_1999_transformed.csv')

    pipeline = feature_eng_pipeline()

    y = df['outcome'].replace({
        'team_1': 0,
        'team_2': 1,
        'draw': 2
    })
    X = df.drop('outcome', axis=1)
    X_trans = pipeline.fit_transform(X)

    expected_variables = VARIABLES[:-1] + ['created_on']
    
    assert expected_variables == list(X_trans.columns)    

def test_feature_selector():
    """
    Test the FeatureSelector preprocess
    """
    data = {
        'league_match': [10],
        'home': ['team_1'],
        'outcome': ['draw'],
        'season': [2021]
    }
    df = pd.DataFrame(data)

    selector = FeatureSelector(['home', 'season'])
    X_trans = selector.fit_transform(df)

    assert list(X_trans.columns) == ['league_match', 'outcome']

def test_to_dataset():
    """
    Test the ToDataset preprocess
    """
    data = np.zeros((4, len(VARIABLES)-1))
    
    to_dataset = ToDataset()
    X = to_dataset.fit_transform(data)

    expected_vars = [var for var in VARIABLES if var != 'outcome']

    assert list(X.columns) == (expected_vars + ['created_on'])

def test_win_ratio():
    """
    Test the WinRatio preprocess
    """
    data = {
        'league_match': [10],
        'home_wins_t1': [10],
        'home_wins_t2': [10],
        'away_wins_t1': [10],
        'away_wins_t2': [10],
    }

    df = pd.DataFrame(data)

    win_ratio = WinRatio()
    X_trans = win_ratio.fit_transform(df)

    assert X_trans['home_win_ratio_t1'].values == 1.0
    assert X_trans['home_win_ratio_t2'].values == 1.0
    assert X_trans['away_win_ratio_t1'].values == 1.0
    assert X_trans['away_win_ratio_t2'].values == 1.0

def test_draw_ratio():
    """
    Test the DrawRatio preprocess
    """
    data = {
        'league_match': [10],
        'home_draws_t1': [10],
        'home_draws_t2': [10],
        'away_draws_t1': [10],
        'away_draws_t2': [10],
    }

    df = pd.DataFrame(data)

    win_ratio = DrawRatio()
    X_trans = win_ratio.fit_transform(df)

    assert X_trans['home_draw_ratio_t1'].values == 1.0
    assert X_trans['home_draw_ratio_t2'].values == 1.0
    assert X_trans['away_draw_ratio_t1'].values == 1.0
    assert X_trans['away_draw_ratio_t2'].values == 1.0

def test_loss_ratio():
    """
    Test the LossRatio preprocess
    """
    data = {
        'league_match': [10],
        'home_losses_t1': [10],
        'home_losses_t2': [10],
        'away_losses_t1': [10],
        'away_losses_t2': [10],
    }

    df = pd.DataFrame(data)

    win_ratio = LossRatio()
    X_trans = win_ratio.fit_transform(df)

    assert X_trans['home_loss_ratio_t1'].values == 1.0
    assert X_trans['home_loss_ratio_t2'].values == 1.0
    assert X_trans['away_loss_ratio_t1'].values == 1.0
    assert X_trans['away_loss_ratio_t2'].values == 1.0