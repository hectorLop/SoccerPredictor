from typing import Dict
from dagster import pipeline, solid, execute_pipeline
from src.scripts.data_ingestion.data_ingestion import retrieve_data, ingest_data
from src.config.logger_config import logger

@solid
def extract_data(context) -> dict:
    data = retrieve_data()

    return data

@solid
def ingest_data_to_db(context, data : dict) -> None:
    ingest_data(data)
    context.log.info('Data inserted succesfully')

@pipeline
def data_ingestion_pipeline():
    ingest_data_to_db(extract_data())

if __name__ == '__main__':
    logger.info('DAGSTER: Data Ingestion Pipeline started')
    execute_pipeline(data_ingestion_pipeline)
    logger.info('DAGSTER: Data Ingestion Pipeline finished')