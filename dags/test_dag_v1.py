from airflow.models.dag import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.dates import days_ago
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow.contrib.kubernetes.secret import Secret
from airflow.contrib.kubernetes.volume import Volume
from airflow.contrib.kubernetes.volume_mount import VolumeMount
from datetime import timedelta

aws_access_key_id = Secret('env', 'AWS_ACCESS_KEY_ID', 'airflow-aws', 'AWS_ACCESS_KEY_ID')
aws_secret_access_key = Secret('env', 'AWS_SECRET_ACCESS_KEY', 'airflow-aws', 'AWS_SECRET_ACCESS_KEY')
aws_account = Secret('env', 'AWS_ACCOUNT', 'airflow-aws', 'AWS_ACCOUNT')
spark_image = 'gcr.io/engineering-sandbox-228018/dev-airflow:1.10.12'

volume_mount = VolumeMount(
    'persist-disk',
    mount_path='/airflo',
    sub_path=None,
    read_only=True
)
volume_config = {
    'persistentVolumeClaim': {
        'claimName': 'nfs-airflow-dags'
    }
}
volume = Volume(name='persist-disk', configs=volume_config)
DAG_NAME = 'test_dag_v1'

default_args = {
    'owner': 'airflow',
    'namespace': 'airflow',
    'depends_on_past': False,
    'get_logs': True,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
    'image_pull_policy': 'Always',
    'is_delete_operator_pod': False,
    'do_xcom_push': False,
    'volumes': [volume],
    'volume_mounts': [volume_mount],
    'labels': {"project": "cthulhu"},
    'secrets': [aws_account, aws_access_key_id, aws_secret_access_key],
    'start_date': days_ago(1)
}
dag = DAG(DAG_NAME, schedule_interval='*/10 * * * *', default_args=default_args)

run_this_1 = DummyOperator(task_id='run_this_1', dag=dag)
run_this_2 = DummyOperator(task_id='run_this_2', dag=dag)
run_this_2.set_upstream(run_this_1)
run_this_3 = DummyOperator(task_id='run_this_3', dag=dag)
run_this_3.set_upstream(run_this_2)
