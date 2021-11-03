from typing import Optional
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer, make_column_selector
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from datetime import datetime
from src.config.logger_config import logger
from src.preprocessing.config import FEATURES_TO_DROP
from src.preprocessing.utils import FeaturePipeline

import numpy as np
import pickle
import pandas as pd

from src.config.config import VARIABLES

class ModelPreprocesser(BaseEstimator, TransformerMixin):
    def __init__(self, trained_pipeline : str = '') -> None:
        if trained_pipeline:
            self.pipeline = self._get_trained_pipeline(trained_pipeline)
        else:
            self.pipeline = self._get_pipeline()

    def fit(self, X, y=None):
        self.pipeline.fit(X)

        return self

    def transform(self, X, y=None):
        X_trans = self.pipeline.transform(X)

        return X_trans

    def fit_and_process_data(self, X_train, X_test, y_train, y_test):
        logger.info('Preprocessing training data')
        X_train = self.pipeline.fit_transform(X_train)
        logger.info('Preprocessing test data')
        X_test = self.pipeline.transform(X_test)

        X_train = X_train.rename(columns={'results_id': 'training_id'})
        X_test = X_test.rename(columns={'results_id': 'test_id'})

        return X_train, X_test, y_train, y_test

    def process_data(self, data):
        data = self.pipeline.transform(data)

        return data

    def _get_trained_pipeline(self, trained_pipeline : str):
        with open(trained_pipeline, 'rb') as file:
            pipeline = pickle.load(file)

        return pipeline

    def _get_pipeline(self):
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
            ('feature_store', ToFeatureStore())
        ])

        return pipeline

class FeatureSelector(BaseEstimator, TransformerMixin):
    def __init__(self, features):
        self.features = features
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        return X.drop(self.features, axis=1)

class ToFeatureStore(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        # Convert to a dataframe
        X = pd.DataFrame(X, columns=VARIABLES[:-1])
        # Adds an id to be used in the Feature Store
        X['results_id'] = np.arange(len(X))
        # Adds a timestamp to define the datetime where the features were created
        now = datetime.now()
        X['created_on'] = [datetime(now.year, now.month, now.day)] * len(X)
        
        return X

class WinRatio(BaseEstimator, TransformerMixin):
    def __init__(self) -> None:
        pass

    def fit(self, X : pd.DataFrame, y : Optional[np.ndarray] = None):
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

    def fit(self, X : pd.DataFrame, y : Optional[np.ndarray] = None):
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