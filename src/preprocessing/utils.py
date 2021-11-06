from sklearn.model_selection import train_test_split
from typing import List, Tuple, Type

import pandas as pd
import numpy as np

class FeaturePipeline():
    """
    Pipeline to apply sequential data preprocesses

    Arguments
    ---------
    preprocesses : List[object]
        List containing the preprocesses to be applied.
    
    Attributes
    ----------
    _preprocesses : List[object]
        List containing the preprocesses to be applied.
    """
    def __init__(self, preprocesses: List[object]) -> None:
        if not isinstance(preprocesses, list) or not preprocesses:
            raise ValueError('You must pass the preprocesses as a non-empty list')

        self._preprocesses = preprocesses

    def transform(self, dataframe : pd.DataFrame) -> pd.DataFrame:
        """
        Transform a dataset using a set of preprocesses

        Parameters
        ----------
        dataframe : pandas.DataFrame
            Data to be transformed.
        
        Returns
        -------
        dataframe : pandas.DataFrame
            Transformed data.
        """
        if not isinstance(dataframe, pd.DataFrame):
            raise TypeError('The data must be a pandas.DataFrame')
            
        for preprocess in self._preprocesses:
            dataframe = preprocess(dataframe)

        return dataframe

    def __call__(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        return self.transform(dataframe)

def get_training_test_sets(
    df : pd.DataFrame
    ) -> Tuple[pd.DataFrame, pd.DataFrame, np.ndarray, np.ndarray]:
    """
    Prepare the training and test sets from a given dataset.

    Parameters
    ----------
    df : pandas.DataFrame
        Original dataset

    Returns
    -------
    X_train
        Training set features
    X_test 
        Test set features
    y_train
        Training set targets
    y_test
        Test set targets
    """
    # Encode categorical target
    y = df['outcome'].replace({
        'team_1': 0,
        'team_2': 1,
        'draw': 2
    }).values

    X = df.drop('outcome', axis=1)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,
                                                        random_state=42,
                                                        stratify=y)

    return X_train, X_test, y_train, y_test

