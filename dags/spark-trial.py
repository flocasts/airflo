from airflow import DAG
from datetime import datetime, timedelta
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow.contrib.kubernetes.secret import Secret
from airflow.contrib.kubernetes.volume import Volume
from airflow.contrib.kubernetes.volume_mount import VolumeMount

aws_access_key_id = Secret('env', 'AWS_ACCESS_KEY_ID', 'airflow-aws', 'AWS_ACCESS_KEY_ID')
aws_secret_access_key = Secret('env', 'AWS_SECRET_ACCESS_KEY', 'airflow-aws', 'AWS_SECRET_ACCESS_KEY')
aws_account = Secret('env', 'AWS_ACCOUNT', 'airflow-aws', 'AWS_ACCOUNT')

volume_mount = VolumeMount(
    'persist-disk',
    mount_path='/airflo',
    sub_path=None,
    read_only=True
)
volume_config = {
    'persistentVolumeClaim': {
        'claimName': 'airflow-dags'
    }
}
volume = Volume(name='persist-disk', configs=volume_config)
dag = DAG(
    'spark-trial',
    max_active_runs=1,
    catchup=False,
    schedule_interval=timedelta(days=365)
)
default_args = {
    'owner': 'airflow',
    'namespace': 'airflow',
    'depends_on_past': False,
    'get_logs': True,
    'start_date': datetime(2020, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
    'image_pull_policy': 'Always',
    # import pdb; pdb.set_trace()
    'is_delete_operator_pod': False,
    'do_xcom_push': False,
    'volumes': [volume],
    'volume_mounts': [volume_mount],
    'labels': {"project": "cthulhu"},
    'secrets': [aws_account, aws_access_key_id, aws_secret_access_key],
}
dag.default_args = default_args

# BUG: Appears to be a limitation on number of arguments
bash_baseline = KubernetesPodOperator(
    image="atherin/pyspark:2.4.4",
    cmds=["/bin/bash", "-c"],
    arguments=["pwd; ls /;"],
    name="bash_baseline",
    task_id="bash-baseline-task",
    dag=dag
)

bash_baseline1 = KubernetesPodOperator(
    image="atherin/pyspark:2.4.4",
    cmds=["/bin/bash", "-c"],
    arguments=["pwd; ls /opt/;"],
    name="bash_baseline1",
    task_id="bash-baseline1-task",
    dag=dag
)

pyspark_segmentation = KubernetesPodOperator(
    image="atherin/pyspark:2.4.4",
    cmds=["python"],
    arguments=["/airflo/jobs/segmentation.py"],
    name="pyspark-segmentation",
    task_id="pyspark-segmentation-task",
    dag=dag
)

pyspark_segmentation.set_upstream(bash_baseline)
