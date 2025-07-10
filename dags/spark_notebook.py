from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator
from time import sleep
from pyspark.sql import SparkSession



def spark_fun():
    spark = SparkSession.builder.appName("demo").getOrCreate()
    df = spark.createDataFrame(
        [
            ("sue", 32),
            ("li", 3),
            ("bob", 75),
            ("heo", 13),
        ],
        ["first_name", "age"],
    )
    # Access the first row of the DataFrame
    first_row = df.head()  # `head()` returns the first row as a Row object

    # Extract the value of the first column (first_name) and second column (age)
    first_value = first_row['first_name']  # You can specify the column name you need
    print(first_value)

def dummpy_spark_fun():
    from pyspark.sql import SparkSession
    spark = SparkSession.builder.appName("demo").getOrCreate()
    df = spark.createDataFrame(
        [
            ("sue", 32),
            ("li", 3),
            ("bob", 75),
            ("heo", 13),
        ],
        ["first_name", "age"],
    )

defualt_args = {
    'owner':'monged',
    'retries':2,
    'retry_delay': timedelta(seconds=5)
}

def printfun():
    for number in range(10):
        print(number*'*')



def printfun2(name, salary):
    # print(f"Emploee {name} has received {salary}$ deposit as a monthly salary.")
    print_msg = 'ahmed'
    return print_msg


def full_statment(ti):
    name = ti.xcom_pull("print_Salary_task")
    print(f"my name is {name}.")

def delay ():
    sleep(2)


with DAG(
    dag_id = 'spark_dag_new_one_222',
    description = 'this is our first python dag operator',
    default_args = defualt_args,
    start_date = datetime(2025,4,5,1),
    schedule_interval = '@daily',
    catchup=False
)as dag:
    # task1 = PythonOperator(
    #     task_id = 'create_a_starts_pyramid',
    #     python_callable = printfun
    # )
    task2 = PythonOperator(
        task_id = 'print_Salary_task',
        python_callable = printfun2,
        op_args=["Ahmed", 1000]
    )

    task3 = PythonOperator(
        task_id = 'spark_task',
        python_callable = spark_fun
    )

    task4 = PythonOperator(
        task_id = 'print_using_xcom_output',
        python_callable = full_statment
    )

    task5 = PythonOperator(
        task_id = 'spark_dummy',
        python_callable = dummpy_spark_fun
    )

    task2>>task4>>task3>>task5