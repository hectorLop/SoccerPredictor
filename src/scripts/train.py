from src.preprocessing.model_preprocessing import ModelPreprocesser
from xgboost import XGBClassifier
from sklearn.preprocessing import LabelEncoder
from src.config.logger_config import logger

import pickle
import pandas as pd
import os
import sys

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(sys.path[0], 'src/models_pipelines/')

def transform_data(dataframe):
    y_train = dataframe['outcome']
    y_train = LabelEncoder().fit_transform(y_train)
    dataframe = dataframe.drop('outcome', axis=1)

    preprocesser = ModelPreprocesser()
    transformed_data = preprocesser.fit_transform(dataframe)
    pipeline = preprocesser.pipeline

    with open(os.path.join(THIS_DIR, DATA_DIR + 'pipeline.pkl'), 'wb') as file:
        pickle.dump(pipeline, file)

    return transformed_data, y_train

def train_model(X, y):
    xgboost = XGBClassifier(num_class=3,
                            learning_rate=0.01,
                            max_depth=5,
                            eval_metric='mlogloss',
                            use_label_encoder=False)

    xgboost.fit(X, y)

    with open(os.path.join(THIS_DIR, DATA_DIR + 'xgboost_model.pkl'), 'wb') as file:
        pickle.dump(xgboost, file)

if __name__ == '__main__':
    dataframe = pd.read_csv(os.path.join(THIS_DIR, 'soccer_dataset.csv'))
    dataframe = dataframe.rename(columns={'goals_conceced_t2': 'goals_conceded_t2'})
    logger.info('Preprocessing data')
    X, y = transform_data(dataframe)
    logger.info('Training the model')
    train_model(X, y)
    logger.info('Model training completed. Generated new model and pipeline files.')