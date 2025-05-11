FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY run.sh /app/run.sh
RUN chmod +x /app/run.sh

CMD [ "bash", "/app/run.sh" ]