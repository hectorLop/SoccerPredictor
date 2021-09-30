from src.config.config import FEATURES_DIR, DATA_DIR
from src.config.logger_config import logger
from src.preprocessing.model_preprocessing import ModelPreprocesser
from sklearn.model_selection import train_test_split

from pathlib import Path

import pandas as pd

def preprocess_data():
    df = pd.read_csv(Path(DATA_DIR, 'results_data.csv'))

    preprocesser = ModelPreprocesser()

    y = df['outcome'].replace({
        'team_1': 0,
        'team_2': 1,
        'draw': 2
    })

    X = df.drop('outcome', axis=1)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,
                                                        random_state=42,
                                                        stratify=y)

    logger.info('Preprocessing training data')
    X_train = preprocesser.fit_transform(X_train)
    logger.info('Preprocessing test data')
    X_test = preprocesser.transform(X_test)

    X_train = X_train.rename(columns={'results_id': 'training_id'})
    X_test = X_test.rename(columns={'results_id': 'test_id'})

    X_train['outcome'] = y_train.values
    X_test['outcome'] = y_test.values

    logger.info('Creating parquet files')
    X_train.to_parquet(Path(DATA_DIR, 'training_data.parquet'))
    X_test.to_parquet(Path(DATA_DIR, 'test_data.parquet'))

if __name__ == '__main__':
    preprocess_data()