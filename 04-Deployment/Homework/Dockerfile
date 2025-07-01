FROM agrigorev/zoomcamp-model:mlops-2024-3.10.13-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY starter.ipynb .
COPY model.bin .
RUN mkdir -p /app/output
COPY run.sh /app/
EXPOSE 8000
ENTRYPOINT ["bash", "run.sh"]