
from airflow import DAG
from airflow.providers.microsoft.mssql.hooks.mssql import MsSqlHook
from airflow.operators.python import PythonOperator
from datetime import datetime

def test_sql_connection():
    hook = MsSqlHook(mssql_conn_id='sql_server_conn')
    result = hook.get_pandas_df("SELECT TOP 5 * FROM [ContosoRetailDW].[dbo].[DimChannel]")
    print(result)

with DAG(
    dag_id='test_local_sql_server',
    start_date=datetime(2025, 4, 8),
    schedule_interval=None,
    catchup=False,
) as dag:

    test_conn = PythonOperator(
        task_id='test_mssql_read',
        python_callable=test_sql_connection
    )
