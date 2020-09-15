from airflow.models.dag import DAG
from datetime import datetime, timedelta
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow.contrib.kubernetes.secret import Secret

aws_access_key_id = Secret('env', 'AWS_ACCESS_KEY_ID', 'airflow-aws', 'AWS_ACCESS_KEY_ID')
aws_secret_access_key = Secret('env', 'AWS_SECRET_ACCESS_KEY', 'airflow-aws', 'AWS_SECRET_ACCESS_KEY')
aws_account = Secret('env', 'AWS_ACCOUNT', 'airflow-aws', 'AWS_ACCOUNT')
spark_image = 'gcr.io/engineering-sandbox-228018/dev-pyspark:2.4.4'


default_args = {
    'owner': 'airflow',
    'namespace': 'ns-airflow',
    'depends_on_past': False,
    'get_logs': True,
    'start_date': datetime(2020, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
    'image_pull_policy': 'Always',
    'is_delete_operator_pod': True,
    'do_xcom_push': False,
    'labels': {"project": "cthulhu"},
    'secrets': [aws_account, aws_access_key_id, aws_secret_access_key]
}

dag = DAG(
    'segmentation',
    max_active_runs=1,
    catchup=False,
    schedule_interval=timedelta(days=365),
    default_args=default_args
)

segmentation = KubernetesPodOperator(
    image=spark_image,
    image_pull_policy='Always',
    cmds=["python"],
    arguments=["/jobs/segmentation.py"],
    name="segmentation",
    task_id="segmentation_task",
    dag=dag
)
