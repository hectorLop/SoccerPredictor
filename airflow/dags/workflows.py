from airflow.decorators import dag
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago

import sys
#sys.path.insert(0, 'opt/airflow/dags')
sys.path.append('opt/airflow/dags')

# print(sys.path)

from src.scripts.data_ingestion.data_ingestion import retrieve_data, ingest_data
from src.config.constants import SCRAPER_CONFIG_FILE

default_args = {
    'owner': 'airflow',
}

def _extract_data(ti):
    data = retrieve_data()
    ti.xcom_push(key='data', value=data)

def _ingest_data(ti):
    data = ti.xcom_pull(key='data', task_ids=['extract_data'])[0]
    ingest_data(data)

@dag(
    dag_id='data_ingestion',
    description='Extract new matches data',
    default_args=default_args,
    start_date=days_ago(2),
    tags=['dataops']
)
def data_ingestion():
    # Tasks
    extract = PythonOperator(task_id="extract_data", python_callable=_extract_data)
    ingest = PythonOperator(task_id="ingest_data", python_callable=_ingest_data)

    extract >> ingest

data_ing = data_ingestion()