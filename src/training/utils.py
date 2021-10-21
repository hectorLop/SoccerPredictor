from pathlib import Path
import pickle
from src.config.logger_config import logger
from src.config.config import DATA_DIR
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score

import warnings
warnings.filterwarnings("ignore")

import yaml
import importlib
import mlflow
import mlflow.sklearn
import pandas as pd

def load_data():
    training_data_path = Path(DATA_DIR, 'training_data.parquet')
    test_data_path = Path(DATA_DIR, 'test_data.parquet')

    training_df = pd.read_parquet(training_data_path)
    test_df = pd.read_parquet(test_data_path)
    
    y_train = training_df['outcome'].values
    X_train = training_df.drop(['outcome', 'training_id', 'created_on'], axis=1).values

    y_test = test_df['outcome'].values
    X_test = test_df.drop(['outcome', 'test_id', 'created_on'], axis=1).values

    return X_train, X_test, y_train, y_test

def train_model(config, X_train, X_test, y_train, y_test):
    with open(config) as file:
        config = yaml.full_load(file)

    tracking_uri = 'http://ec2-34-245-186-212.eu-west-1.compute.amazonaws.com:5000'
    mlflow.set_tracking_uri(tracking_uri)

    mlflow.set_experiment('Soccer_Prediction')
    experiment = mlflow.get_experiment_by_name('Soccer_Prediction')
    experiemnt_id = experiment.experiment_id

    with mlflow.start_run(experiment_id=experiemnt_id):
        print(mlflow.get_artifact_uri())
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
        #mlflow.sklearn.log_model(model, config['name'])

    with open(Path(DATA_DIR, 'model.pkl'), 'wb') as file:
        pickle.dump(model, file)


def get_object_from_str(path):
    pm = path.rsplit(".", 1)

    if len(pm) < 2:
        raise Exception("'%s' does not exist as python class" % path)

    mod = importlib.import_module(pm[0])

    return getattr(mod, pm[1])

def eval_model(test, preds, metric_func):
    metric = metric_func(test, preds)

    return metric