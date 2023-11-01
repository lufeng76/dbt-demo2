import datetime

from airflow import models
from airflow.kubernetes.secret import Secret
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from kubernetes.client import models as k8s_models

from airflow.operators import bash_operator
import os

JOB_NAME = 'sample_dag_task_running_on_gke'
start_date = datetime.datetime(2021, 1, 31)

with models.DAG(
        dag_id='test_k8s_run',
        schedule_interval=None,
        start_date=start_date) as dag:
    
    bash_task = bash_operator.BashOperator(
        task_id="bash-task",
        bash_command="echo 'this is the first task'",
        dag=dag
    )

    dbt_task = KubernetesPodOperator(
        task_id="k8s-task",
        name="dbt-task",
        namespace="composer-user-workloads",
        
        # Ensures that cache is always refreshed
        image_pull_policy='Always',
        # Artifact image of dbt repo
        image='gcr.io/gcp-runtimes/ubuntu_20_0_4',
        cmds=["/bin/bash", "-c","echo 'test KubernetesPodOperator'"],
        config_file="/home/airflow/composer_kube_config",
        kubernetes_conn_id="kubernetes_default",     
        )

    bash_task >> dbt_task