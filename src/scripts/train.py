from pathlib import Path
import pickle
from src.config.logger_config import logger
from src.config.config import FEATURES_DIR, VARIABLES, DATA_DIR
from feast import FeatureStore
from datetime import datetime
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score

import warnings
warnings.filterwarnings("ignore")

import yaml
import argparse
import importlib
import numpy as np
import mlflow
import mlflow.sklearn
import pandas as pd

def load_data():
    store = FeatureStore(repo_path=FEATURES_DIR)
    training_variables = ['training_data:' + variable for variable in VARIABLES]
    test_variables = ['test_data:' + variable for variable in VARIABLES]

    training_data_ids = np.arange(6542)
    test_data_ids = np.arange(1636)

    now = datetime.now()
    training_timestamps = [datetime(now.year, now.month, now.day)] * len(training_data_ids)
    test_timestamps = [datetime(now.year, now.month, now.day)] * len(test_data_ids)

    training_entity_df = pd.DataFrame({
        'training_id': training_data_ids,
        "event_timestamp": training_timestamps
        })
    testing_entity_df = pd.DataFrame({
        'test_id': test_data_ids,
        "event_timestamp": test_timestamps
        })

    training_df = store.get_historical_features(
        entity_df=training_entity_df,
        features=training_variables
    ).to_df()

    test_df = store.get_historical_features(
        entity_df=testing_entity_df,
        features=test_variables
    ).to_df()

    y_train = training_df['outcome'].values
    X_train = training_df.drop(['outcome', 'training_id', 'event_timestamp'],
                                axis=1).values

    y_test = test_df['outcome'].values
    X_test = test_df.drop(['outcome', 'test_id', 'event_timestamp'],
                            axis=1).values

    return X_train, X_test, y_train, y_test

def get_object_from_str(path):
    pm = path.rsplit(".", 1)

    if len(pm) < 2:
        raise Exception("'%s' does not exist as python class" % path)

    mod = importlib.import_module(pm[0])

    return getattr(mod, pm[1])

def eval_model(test, preds):
    acc = accuracy_score(test, preds)

    return acc

def train_model(config):
    logger.info('Loading the data')
    X_train, X_test, y_train, y_test = load_data()

    tracking_uri = 'http://ec2-54-154-10-25.eu-west-1.compute.amazonaws.com:5000'
    mlflow.set_tracking_uri(tracking_uri)

    with mlflow.start_run():
        logger.info('Creating the model')
        params = config['params']
        model = get_object_from_str(config['model'])(**params)

        logger.info('Training the model')
        model.fit(X_train, y_train)
        train_preds = model.predict(X_train)
        train_acc = accuracy_score(y_train, train_preds)

        logger.info('Cross validating the model')
        scores = cross_val_score(model, X_train, y_train, cv=5)
        val_acc = scores.mean()

        logger.info('Testing the model')
        test_preds = model.predict(X_test)
        test_acc = accuracy_score(y_test, test_preds)

        for param, value in params.items():
            mlflow.log_param(param, value)

        mlflow.log_metric('train_acc', train_acc)
        mlflow.log_metric('val_acc', val_acc)
        mlflow.log_metric('test_acc', test_acc)

        logger.info('Logging the model')
        mlflow.sklearn.log_model(model, config['name'])

    with open(Path(DATA_DIR, 'model.pkl'), 'wb') as file:
        pickle.dump(model, file)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-m', '--model',
                    type=str,
                    required=True,
                    help='Model config file')
    args = parser.parse_args()

    with open(args.model) as file:
        config = yaml.full_load(file)

    train_model(config)