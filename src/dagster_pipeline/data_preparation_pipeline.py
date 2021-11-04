import pickle

from pathlib import Path

from src.config.config import CODE_DIR, DATA_DIR
from src.config.logger_config import logger
from src.preprocessing.cleaning_preprocesses import RemoveFirstLeagueMatch, RemoveWrongOutcome
from src.preprocessing.data_retriever import DataRetriever
from src.preprocessing.model_preprocessing import feature_eng_pipeline, fit_and_process_data
from src.preprocessing.utils import get_training_test_sets
from src.preprocessing.features_preprocesses import get_feature_pipeline
from dagster import solid, Output, OutputDefinition, execute_pipeline, pipeline

@solid(
    output_defs=[
        OutputDefinition(name='results', is_required=True),
        OutputDefinition(name='general', is_required=True),
        OutputDefinition(name='home', is_required=True),
        OutputDefinition(name='away', is_required=True)
    ]
)
def get_raw_data(context):
    logger.info('Data Preparation Pipeline: Getting the Raw Data')
    db_config = Path(CODE_DIR, 'db/db_config.yml')
    retriever = DataRetriever(db_config)

    results, general, home, away = retriever.get_historical_data()

    yield Output(results, 'results')
    yield Output(general, 'general')
    yield Output(home, 'home')
    yield Output(away, 'away')

@solid
def basic_preprocessing(context, results, general, home, away):
    logger.info('Data Preparation Pipeline: Basic Preprocessing')
    first_league_match_remover = RemoveFirstLeagueMatch()
    remove_wrong_outcome = RemoveWrongOutcome()

    results = first_league_match_remover(results)
    results = remove_wrong_outcome(results)

    feature_pipeline = get_feature_pipeline(general, home, away)
    data = feature_pipeline(results)

    return data

@solid(
    output_defs=[
        OutputDefinition(name='X_train', is_required=True),
        OutputDefinition(name='X_test', is_required=True),
        OutputDefinition(name='y_train', is_required=True),
        OutputDefinition(name='y_test', is_required=True),
    ]
)
def data_split(context, data):
    logger.info('Data Preparation Pipeline: Data Split')

    X_train, X_test, y_train, y_test = get_training_test_sets(data)
    
    yield Output(X_train, 'X_train')
    yield Output(X_test, 'X_test')
    yield Output(y_train, 'y_train')
    yield Output(y_test, 'y_test')
    
@solid
def model_preprocessing(context, X_train, X_test, y_train, y_test):
    logger.info('Data Preparation Pipeline: Model Preprocessing')

    prep_pipeline = feature_eng_pipeline()

    X_train, X_test, y_train, y_test = fit_and_process_data(prep_pipeline,
                                                            (X_train, y_train),
                                                            (X_test, y_test))
                                                                
    with open(Path(DATA_DIR, 'prep_pipeline.pkl'), 'wb') as outfile:
        pickle.dump(prep_pipeline, outfile)

    X_train['outcome'] = y_train
    X_test['outcome'] = y_test

    logger.info('Creating parquet files')
    X_train.to_parquet(Path(DATA_DIR, 'training_data.parquet'))
    X_test.to_parquet(Path(DATA_DIR, 'test_data.parquet'))

@pipeline
def data_preparation_pipeline():
    # Load data from the database
    results, general, home, away = get_raw_data()
    # Join the data to create an unique dataset
    data = basic_preprocessing(results, general, home, away)
    # Split the data intro training and test sets
    X_train, X_test, y_train, y_test = data_split(data)
    # Preprocess the data to be ready to train the models
    model_preprocessing(X_train, X_test, y_train, y_test)

if __name__ == '__main__':
    execute_pipeline(data_preparation_pipeline)
    logger.info('DAGSTER: Data Preparation Pipeline Finished')