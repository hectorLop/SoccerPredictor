import pytest
import pandas as pd
import numpy as np

from src.preprocessing.utils import get_training_test_sets

def test_utils():
    data = {
        'outcome': (['team_1'] * 50) + (['draw'] * 50),
        'goals': np.arange(0, 100),
        'wins': np.arange(0, 100)
    }

    df = pd.DataFrame(data)
    X_train, X_test, y_train, y_test = get_training_test_sets(df)

    assert len(y_train) == 80
    assert len(y_test) == 20