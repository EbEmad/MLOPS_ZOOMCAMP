FROM apache/airflow:3.0.1

COPY req.txt .
# Install required Python packages
RUN pip install --no-cache-dir -r req.txt
RUN usermod -aG docker airflow

# Copy the DAGs directory to the Airflow home directory
COPY dags/ /opt/airflow/dags/

# Copy the entrypoint script
COPY run.sh /run.sh

# Switch to the root user to change permissions
USER root
RUN chmod +x /run.sh
RUN apt-get update && apt-get install -y git iputils-ping