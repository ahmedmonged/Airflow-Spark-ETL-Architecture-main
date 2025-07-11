from airflow import DAG
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.operators.python import PythonOperator
from datetime import datetime
from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator
from time import sleep
from pyspark.sql import SparkSession
from airflow.providers.postgres.hooks.postgres import PostgresHook
from io import StringIO
import csv

def read_csv_from_s3_with_s3hook_and_pyspark(**kwargs):
    bucket = 'source-data-crs'
    key = 'source1/Aemf1.csv'
    s3_path = f"s3a://{bucket}/{key}"

    # Get credentials from Airflow connection
    s3_hook = S3Hook(aws_conn_id='aws_s3')
    credentials = s3_hook.get_credentials()

    # Start Spark session
    spark = SparkSession.builder \
        .appName("ReadCSVFromS3") \
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:3.3.4,com.amazonaws:aws-java-sdk-bundle:1.12.262") \
        .getOrCreate()

    # Configure S3 access in Spark
    hadoop_conf = spark._jsc.hadoopConfiguration()
    hadoop_conf.set("fs.s3a.access.key", credentials.access_key)
    hadoop_conf.set("fs.s3a.secret.key", credentials.secret_key)
    if credentials.token:
        hadoop_conf.set("fs.s3a.session.token", credentials.token)
    hadoop_conf.set("fs.s3a.endpoint", "s3.amazonaws.com")
    hadoop_conf.set("fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
    hadoop_conf.set("com.amazonaws.services.s3.enableV4", "true")

    # Read the CSV with PySpark
    df = spark.read.csv(s3_path, header=True, inferSchema=True)
    print('test output')
    df.show(5)  # Just print first 5 rows

# 3. Insert into PostgreSQL
    pg_hook = PostgresHook(postgres_conn_id='AWS_PostgreSQL')
    conn = pg_hook.get_conn()
    cursor = conn.cursor()

    for row in df.collect():
        cursor.execute("""
            INSERT INTO customer (full_name, email, phone_number, source)
            VALUES (%s, %s, %s, %s)
        """, (row['full_name'], row['email'], row['phone_number'], 'ec2'))

    conn.commit()
    cursor.close()
    conn.close()


# def sparksession():
#     from pyspark.sql import SparkSession
#     spark = SparkSession.builder.appName("demo").getOrCreate()
    
# def read_csv():
#     s3_path = "s3a://source-data-crs/source1/Aemf1.csv"
#     df = spark.read.csv(s3_path, header=True, inferSchema=True)

# def list_files_in_s3(**kwargs):
#     bucket_name = 'source-data-crs'
#     prefix = 'source1/'  # optional: '' to list all files at root level

#     s3_hook = S3Hook(aws_conn_id='aws_s3')
    
#     # List all keys (file names) under the specified prefix
#     keys = s3_hook.list_keys(bucket_name=bucket_name, prefix=prefix)

#     if keys:
#         print("Files found in bucket:")
#         for key in keys:
#             print(key)
#     else:
#         print(f"No files found in bucket '{bucket_name}'.")

default_args = {
    'start_date': datetime(2025, 4, 7),
}

with DAG(
    dag_id='list_s3_files',
    default_args=default_args,
    schedule_interval="*/15 * * * *",
    catchup=False,
    tags=['s3', 'list', 'aws']
) as dag:

    list_files_task = PythonOperator(
        task_id='list_files_in_s3_bucket',
        python_callable=read_csv_from_s3_with_s3hook_and_pyspark,
        provide_context=True
    )

    list_files_task
#     # Replace with your S3 URI
#    s3_path = "s3a://source-data-crs/source1/Aemf1.csv"