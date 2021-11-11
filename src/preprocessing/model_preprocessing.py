from __future__ import annotations
from typing import List, Optional, Tuple
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer, make_column_selector
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from datetime import datetime
from src.config.logger_config import logger
from src.preprocessing.config import FEATURES_TO_DROP

import numpy as np
import pandas as pd

from src.config.config import VARIABLES

def feature_eng_pipeline() -> Pipeline:
    """
    Creates the pipeline to transform the data

    Returns
    -------
    pipeline : Pipeline
        Feature engineering pipeline.
    """
    # Categorical attributes pipeline
    cat_pipeline = Pipeline([
        ('encoder', OneHotEncoder())
    ])

    # Numerical attributes pipeline
    num_pipeline = Pipeline([
        ('scaler', StandardScaler())
    ])

    # Pipeline to transform columns
    prep_pipeline = ColumnTransformer([
        ('cat', 'passthrough', make_column_selector(dtype_include=object)),
        ('num', num_pipeline, make_column_selector(dtype_include=np.number))
    ])

    feature_pipeline = Pipeline([
        ('win_ratio', WinRatio()),
        ('draw_ratio', DrawRatio()),
        ('loss_ratio', LossRatio()),
    ])

    # Final pipeline
    pipeline = Pipeline([
        ('feature_pipeline', feature_pipeline),
        ('feature_selector', FeatureSelector(FEATURES_TO_DROP)),
        ('prep', prep_pipeline),
        ('feature_store', ToDataset())
    ])

    return pipeline

def fit_and_process_data(
    pipeline : Pipeline,
    train : Tuple[pd.DataFrame, np.ndarray],
    test : Tuple[pd.DataFrame, np.ndarray]
    ) -> Tuple[pd.DataFrame, pd.DataFrame, np.ndarray, np.ndarray]:
    """
    Fit the pipeline with the training data and uses the obtained insights
    to transform both the training and test data.

    Parameters
    ----------
    pipeline : Pipeline
        Preprocessing pipeline
    train : Tuple[pd.DataFrame, np.ndarray]
        Tuple containing the training data
    test : Tuple[pd.DataFrame, np.ndarray]
        Tuple containing the test data

    Returns
    -------
    Tuple[pd.DataFrame, pd.DataFrame, np.ndarray, np.ndarray]
        Tuple containing the transformed training and test data
    """
    # Unpack the training and test data
    X_train, y_train = train
    X_test, y_test = test

    # Fit the pipeline and transform the training data
    logger.info('Preprocessing training data')
    X_train = pipeline.fit_transform(X_train)
    # Transform the test data
    logger.info('Preprocessing test data')
    X_test = pipeline.transform(X_test)

    return X_train, X_test, y_train, y_test

class FeatureSelector(BaseEstimator, TransformerMixin):
    """
    Remove a list of features from the data

    Arguments
    ---------
    features : list of str
        Features' names
    
    Attributes
    ----------
    features : list of str
        Features' names
    """
    def __init__(self, features : List[str]):
        self.features = features
    
    def fit(self, X : pd.DataFrame, y : Optional[np.ndarray] = None) -> object:
        return self
    
    def transform(
        self,
        X : pd.DataFrame,
        y : Optional[np.ndarray] = None
        ) -> pd.DataFrame:
        return X.drop(self.features, axis=1)

class ToDataset(BaseEstimator, TransformerMixin):
    """
    Transform a matrix of values into a dataset.

    Arguments
    ---------
    columns : List of str
        List containing the desired dataset columns.

    Attributes
    ---------
    variables : List of str
        List containing the desired dataset columns.
    """
    def __init__(self, columns : List[str] = VARIABLES):
        self.variables = columns

    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        # Convert to a dataframe
        variables = [var for var in VARIABLES if var != 'outcome']

        X = pd.DataFrame(X, columns=variables)
        # Adds a timestamp to define the datetime where the features were created
        now = datetime.now()
        X['created_on'] = [datetime(now.year, now.month, now.day)] * len(X)
        
        return X

class WinRatio(BaseEstimator, TransformerMixin):
    def __init__(self) -> None:
        pass

    def fit(self, X : pd.DataFrame, y : Optional[np.ndarray] = None) -> WinRatio:
        return self

    def transform(self, X : pd.DataFrame, y : Optional[np.ndarray] = None):
        X['home_win_ratio_t1'] = X['home_wins_t1'] / X['league_match']
        X['home_win_ratio_t2'] = X['home_wins_t2'] / X['league_match']

        X['away_win_ratio_t1'] = X['away_wins_t1'] / X['league_match']
        X['away_win_ratio_t2'] = X['away_wins_t2'] / X['league_match']

        return X

class DrawRatio(BaseEstimator, TransformerMixin):
    def __init__(self) -> None:
        pass

    def fit(self, X : pd.DataFrame, y : Optional[np.ndarray] = None) -> DrawRatio:
        return self

    def transform(self, X : pd.DataFrame, y : Optional[np.ndarray] = None):
        X['home_draw_ratio_t1'] = X['home_draws_t1'] / X['league_match']
        X['home_draw_ratio_t2'] = X['home_draws_t2'] / X['league_match']

        X['away_draw_ratio_t1'] = X['away_draws_t1'] / X['league_match']
        X['away_draw_ratio_t2'] = X['away_draws_t2'] / X['league_match']

        return X

class LossRatio(BaseEstimator, TransformerMixin):
    def __init__(self) -> None:
        pass

    def fit(self, X : pd.DataFrame, y : Optional[np.ndarray] = None):
        return self

    def transform(self, X : pd.DataFrame, y : Optional[np.ndarray] = None):
        X['home_loss_ratio_t1'] = X['home_losses_t1'] / X['league_match']
        X['home_loss_ratio_t2'] = X['home_losses_t2'] / X['league_match']

        X['away_loss_ratio_t1'] = X['away_losses_t1'] / X['league_match']
        X['away_loss_ratio_t2'] = X['away_losses_t2'] / X['league_match']

        return X