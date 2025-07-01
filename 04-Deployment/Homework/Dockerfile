FROM agrigorev/zoomcamp-model:mlops-2024-3.10.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN mkdir -p /app/output

COPY starter.ipynb .
COPY model.bin .
COPY run.sh /app/
EXPOSE 8000
ENTRYPOINT ["bash", "run.sh"]