from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

default_args = {
    'owner': 'monged',
    'retries': 3,
    'retry_delay': timedelta(seconds=3)

}

with DAG(
dag_id = 'create_databse_and_add_new_row',
default_args = default_args,
start_date = datetime(2025,3,1),
schedule_interval = "@daily"
) as dag:
    task1 = SQLExecuteQueryOperator(
        task_id = "create_database_if_not_exist_and_add_row",
        conn_id="postgresql_db",
        sql = """
                CREATE TABLE IF NOT EXISTS public.airflow(
                id SERIAL PRIMARY KEY,
                name text not null)
         """
    )
    task1


    