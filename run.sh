#!/bin/bash

# Set default artifact root if not provided
export MLFLOW_ARTIFACT_ROOT=${MLFLOW_ARTIFACT_ROOT:-/app/02-experiment-tracking/mlflow_artifacts}
# Wait for PostgreSQL
echo "Waiting for PostgreSQL..."
until pg_isready -h postgres -p 5432 -U mlflow; do
  sleep 1
done
echo "PostgreSQL ready!"
# Start services
echo "Starting MLflow server..."
mlflow server \
  --backend-store-uri postgresql://mlflow:mlflow@postgres:5432/mlflow \
  --default-artifact-root file://${MLFLOW_ARTIFACT_ROOT} \
  --host 0.0.0.0 \
  --port 5000 &

echo "Starting Jupyter Notebook..."
jupyter notebook \
  --ip=0.0.0.0 \
  --port=8000 \
  --no-browser \
  --NotebookApp.token='' \
  --NotebookApp.password=''

# Keep container running if Jupyter crashes
wait