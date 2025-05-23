FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


RUN pip install --upgrade pip && \
    pip install mlflow[extras] psycopg2-binary boto3

COPY run.sh /app/run.sh
RUN chmod +x /app/run.sh
EXPOSE 5000
CMD [ "bash", "/app/run.sh" ]