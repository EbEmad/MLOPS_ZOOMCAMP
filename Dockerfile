# Use official Python 3.9 slim image
FROM python:3.9-slim

# Set work directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Upgrade pip and install build dependencies for packages like numpy, xgboost, etc.
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        gcc \
        gfortran \
        libblas-dev \
        liblapack-dev \
        libffi-dev \
        libssl-dev \
        python3-dev \
        libxml2-dev \
        libxslt-dev \
    && pip install --upgrade pip setuptools wheel \
    && pip install -r requirements.txt \
    && apt-get purge -y --auto-remove build-essential gcc gfortran python3-dev \
    && rm -rf /var/lib/apt/lists/*
RUN pip install protobuf==3.20.3
RUN pip install protobuf==3.20.3 "SQLAlchemy<1.4.41"
# Copy your project files (optional)
COPY . .

# Default command to keep the container running (optional)
CMD ["bash"]
