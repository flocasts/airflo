from airflow import DAG
from datetime import datetime, timedelta
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow import configuration as conf
import logging

logging.info(conf)
logging.info('moose')
namespace = conf.get('kubernetes', 'NAMESPACE')

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2020, 1, 1),
    'email': ['andrew.therin@flosports.tv'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'k8_example_v1',
    max_active_runs=1,
    catchup=False,
    default_args=default_args,
    schedule_interval=timedelta(days=365)
)


start = DummyOperator(task_id='run_this_first', dag=dag)

passing = KubernetesPodOperator(
    namespace='ns-andrew-tan',
    image="python:3.6-stretch",
    cmds=["python", "-c"],
    arguments=["print('hello world')"],
    labels={"env": "dev"},
    name="passing-test",
    task_id="passing-task",
    get_logs=True,
    do_xcom_push=False,
    dag=dag
)

failing = KubernetesPodOperator(
    namespace='ns-andrew-tan',
    image="ubuntu:16.04",
    cmds=["python", "-c"],
    arguments=["print('hello world')"],
    labels={"env": "dev"},
    name="fail",
    task_id="failing-task",
    get_logs=True,
    do_xcom_push=False,
    dag=dag
)

passing.set_upstream(start)
failing.set_upstream(start)
