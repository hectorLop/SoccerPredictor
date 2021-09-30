from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer, make_column_selector
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
from datetime import datetime

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
            ('cat', cat_pipeline, make_column_selector(dtype_include=object)),
            ('num', num_pipeline, make_column_selector(dtype_include=np.number))
        ])

        # Final pipeline
        pipeline = Pipeline([
            ('feature_selector', FeatureSelector(['season', 'team_1', 'team_2',
                                                'league_match'])),
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
        X = pd.DataFrame(X, columns=VARIABLES)
        # Adds an id to be used in the Feature Store
        X['results_id'] = np.arange(len(X))
        # Adds a timestamp to define the datetime where the features were created
        now = datetime.now()
        X['created_on'] = [datetime(now.year, now.month, now.day)] * len(X)
        
        return X