from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator
from time import sleep

defualt_args = {
    'owner':'monged',
    'retries':5,
    'retry_delay': timedelta(seconds=10)
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
    dag_id = 'dag_with_py_operatorv01',
    description = 'this is our first python dag operator',
    default_args = defualt_args,
    start_date = datetime(2025,3,1,1),
    schedule_interval = '@daily'
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
    # task3 = PythonOperator(
    #     task_id = 'wait_task',
    #     python_callable = delay
    # )

    task4 = PythonOperator(
        task_id = 'print_using_xcom_output',
        python_callable = full_statment
    )

    task2>>task4