from airflow import DAG
from airflow.providers.http.operators.http import HttpOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta
import json


def print_users(response):
    users = json.loads(response)
    for user in users['users']:
        print(f"{user['firstName']} {user['lastName']} - {user['email']}")

defualt_args = {
    'owner':'monged',
    'retries':1,
    'retry_delay': timedelta(seconds=1)
}

with DAG(
    dag_id = 'API_data',
    schedule_interval = '@daily',
    start_date = datetime(2025,4,10),
    catchup=False,
    default_args = defualt_args
)as dag:
    
    fetch_users = HttpOperator(
        task_id='get_random_users',
        http_conn_id='API_conn',
        endpoint='?limit=5',  # gets 5 random users
        method='GET',
        response_filter=lambda response: response.text)
    
    process_users = PythonOperator(
        task_id='print_users',
        python_callable=print_users,
        op_args=["{{ ti.xcom_pull(task_ids='get_random_users') }}"],
    )

    fetch_users >> process_users