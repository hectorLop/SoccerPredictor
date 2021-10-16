from pathlib import Path
from src.config.config import DATA_DIR, CODE_DIR
from src.config.logger_config import logger
from src.training.utils import load_data, train_model
from dagster import solid, pipeline, Output, OutputDefinition, execute_pipeline

import pandas as pd

@solid(
    output_defs=[
        OutputDefinition(name='X_train', is_required=True),
        OutputDefinition(name='X_test', is_required=True),
        OutputDefinition(name='y_train', is_required=True),
        OutputDefinition(name='y_test', is_required=True),
    ]
)
def get_data(context):
    logger.info('TRAINING: Loading the data...')
    X_train, X_test, y_train, y_test = load_data()

    yield Output(X_train, 'X_train')
    yield Output(X_test, 'X_test')
    yield Output(y_train, 'y_train')
    yield Output(y_test, 'y_test')

@solid
def model_training(context, X_train, X_test, y_train, y_test):
    logger.info('TRAINING: Training the model')
    config_path = Path(CODE_DIR, 'training/model_config.yaml')
    train_model(config_path, X_train, X_test, y_train, y_test)

@pipeline
def train_pipeline():
    X_train, X_test, y_train, y_test = get_data()
    model_training(X_train, X_test, y_train, y_test)

if __name__ == '__main__':
    execute_pipeline(train_pipeline)