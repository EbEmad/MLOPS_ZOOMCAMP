FROM python:3.11-slim

WORKDIR /app



# Install build tools for compiling Python packages
RUN apt-get update && apt-get install -y gcc build-essential
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

RUN pip install --upgrade pip && \
    pip install mlflow[extras] psycopg2-binary boto3

COPY run.sh /app/run.sh
RUN chmod +x /app/run.sh
EXPOSE 5000
CMD [ "bash", "/app/run.sh" ]