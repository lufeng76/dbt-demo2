import datetime

from airflow import models
from airflow.kubernetes.secret import Secret
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from airflow.operators import bash_operator

import os

JOB_NAME = 'sample_dag_task_running_on_gke'
start_date = datetime.datetime(2021, 1, 31)

with models.DAG(
        dag_id='dbt_k8s_run',
        schedule_interval=None,
        start_date=start_date) as dag:
    
    bash_task = bash_operator.BashOperator(
        task_id="bash-task",
        bash_command="echo 'this is the first task'",
        dag=dag
    )

    dbt_task = KubernetesPodOperator(
        task_id="dbt-task",
        name="dbt-task",
        namespace="default",
        
        # Ensures that cache is always refreshed
        image_pull_policy='Always',
        # Artifact image of dbt repo
        image='gcr.io/lufeng-cepf/dbt-demo:ff502d9',
        cmds=["/bin/bash", "-c","/dbt/dbt_run.sh run dev jaffle_shop {} false"],
        affinity={}         
        # affinity={
        #     'nodeAffinity': {
        #         # requiredDuringSchedulingIgnoredDuringExecution means in order
        #         # for a pod to be scheduled on a node, the node must have the
        #         # specified labels. However, if labels on a node change at
        #         # runtime such that the affinity rules on a pod are no longer
        #         # met, the pod will still continue to run on the node.
        #         'requiredDuringSchedulingIgnoredDuringExecution': {
        #             'nodeSelectorTerms': [{
        #                 'matchExpressions': [{
        #                     # When nodepools are created in Google Kubernetes
        #                     # Engine, the nodes inside of that nodepool are
        #                     # automatically assigned the label
        #                     # 'cloud.google.com/gke-nodepool' with the value of
        #                     # the nodepool's name.
        #                     'key': 'cloud.google.com/gke-nodepool',
        #                     'operator': 'In',
        #                     # The label key's value that pods can be scheduled
        #                     # on.
        #                     # In this case it will execute the command on the node
        #                     # pool created by the Airflow bash operator.
        #                     'values': [
        #                         'pool-1'
        #                     ]
        #                 }]
        #             }]
        #         }
        #     }
        # } 
        )

    bash_task >> dbt_task