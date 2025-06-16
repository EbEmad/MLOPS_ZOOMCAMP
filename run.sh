#!/bin/bash

echo "Starting MLflow server..."
mlflow server \
  --backend-store-uri postgresql://mlflow:mlflow@db:5432/mlflow \
  --default-artifact-root s3://mlflow/ \
  --host 0.0.0.0 \
  --port 5000 &   # run in background (&)

echo "Starting Jupyter Notebook..."
jupyter notebook \
  --ip=0.0.0.0 \
  --port=8000 \
  --allow-root \
  --no-browser \
  --NotebookApp.token='' \
  --NotebookApp.password=''