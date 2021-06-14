from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer, make_column_selector
from sklearn.preprocessing import StandardScaler, OneHotEncoder

import numpy as np

class ModelPreprocesser(TransformerMixin):
    def __init__(self) -> None:
        self.pipeline = self.get_pipeline()

    def fit(self, X):
        self.pipeline.fit(X)

    def transform(self, X):
        self.pipeline.transform(X)

    def _get_pipeline():
        # Categorical attributes pipeline
        cat_pipeline = Pipeline([
            ('encoder', OneHotEncoder())
        ])

        # Numerical attributes pipeline
        num_pipeline = Pipeline([
            ('scaler', StandardScaler())
        ])

        prep_pipeline = ColumnTransformer([
            ('cat', cat_pipeline, make_column_selector(dtype_include=object)),
            ('num', num_pipeline, make_column_selector(dtype_include=np.number))
        ])

        pipeline = Pipeline([
            ('feature_selector', FeatureSelector(['season', 'team_1', 'team_2',
                                                'league_match'])),
            ('goals_difference', GoalDifference()),
            ('winratio', WinRatio()),
            ('lossratio', LossRatio()),
            ('drawratio', DrawRatio()),
            ('prep', prep_pipeline)
        ])

        return pipeline

class FeatureSelector(BaseEstimator, TransformerMixin):
    def __init__(self, features):
        self.features = features
    
    def fit(self, X):
        return self
    
    def transform(self, X, y=None):
        return X.drop(self.features, axis=1)
    
class GoalDifference(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass
    
    def fit(self, X):
        return self
    
    def transform(self, X, y=None):
        X['goals_difference_t1'] = X['goals_scored_t1'] - X['goals_conceded_t1']
        X['goals_difference_t2'] = X['goals_scored_t2'] - X['goals_conceced_t2']

        return X
    
class WinRatio(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass
    
    def fit(self, X):
        return self
    
    def transform(self, X, y=None):
        total_wins_t1 = X['home_wins_t1'] + X['away_wins_t1']
        total_wins_t2 = X['home_wins_t2'] + X['away_wins_t2']
        
        
        X['win_ratio_t1'] = total_wins_t1 / self._get_total_matches(X, 't1')
        X['win_ratio_t2'] = total_wins_t2 / self._get_total_matches(X, 't2')
        
        return X
        
    def _get_total_matches(self, X, team: str):
        return X[f'home_wins_{team}'] + X[f'away_wins_{team}'] + \
               X[f'home_losses_{team}'] + X[f'away_losses_{team}'] + \
               X[f'home_draws_{team}'] + X[f'away_draws_{team}']
    
class LossRatio(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass
    
    def fit(self, X):
        return self
    
    def transform(self, X, y=None):
        total_losses_t1 = X['home_losses_t1'] + X['away_losses_t1']
        total_losses_t2 = X['home_losses_t2'] + X['away_losses_t2']
        
        
        X['loss_ratio_t1'] = total_losses_t1 / self._get_total_matches(X, 't1')
        X['loss_ratio_t2'] = total_losses_t2 / self._get_total_matches(X, 't2')
        
        return X
        
    def _get_total_matches(self, X, team: str):
        return X[f'home_wins_{team}'] + X[f'away_wins_{team}'] + \
               X[f'home_losses_{team}'] + X[f'away_losses_{team}'] + \
               X[f'home_draws_{team}'] + X[f'away_draws_{team}']
    
class DrawRatio(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass
    
    def fit(self, X):
        return self
    
    def transform(self, X, y=None):
        total_draws_t1 = X['home_draws_t1'] + X['away_draws_t1']
        total_draws_t2 = X['home_draws_t2'] + X['away_draws_t2']
        
        
        X['draw_ratio_t1'] = total_draws_t1 / self._get_total_matches(X, 't1')
        X['draw_ratio_t2'] = total_draws_t2 / self._get_total_matches(X, 't2')
        
        return X
        
    def _get_total_matches(self, X, team: str):
        return X[f'home_wins_{team}'] + X[f'away_wins_{team}'] + \
               X[f'home_losses_{team}'] + X[f'away_losses_{team}'] + \
               X[f'home_draws_{team}'] + X[f'away_draws_{team}']