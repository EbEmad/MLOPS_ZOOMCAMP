from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    'owner': 'ebemadv2',
    'start_date': datetime(2025, 6, 14),
}

with DAG(
    dag_id='dag_ml_pipeline_bash_docker_run',
    default_args=default_args,
    description='Run ML pipeline with BashOperator and docker run',
    schedule=None,
    catchup=False,
) as dag:

    dataset_creation_task = BashOperator(
        task_id="faked_dataset_creation_task",
        bash_command='echo "Hey the dataset is ready, let\'s trigger the training process"',
    )

    model_train_and_publish_task = BashOperator(
        task_id='docker_model_train_and_publish_task',
        bash_command="""
docker run --rm \
    -e MINIO_ENDPOINT=minio:9000 \
    -e MINIO_ACCESS_KEY_ID=nb8NqRD9hhz55kXOWLHh \
    -e MINIO_SECRET_ACCESS_KEY=SqpQK9QAy9noVjlCdxrrrEqx0JTaxDckXMBdeQae \
    -e MINIO_BUCKET_NAME=mlflow \
    test:v1 python model_tuning.py
""",
    )

    dataset_creation_task >> model_train_and_publish_task