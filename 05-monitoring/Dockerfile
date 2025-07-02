FROM python:3.11.13-slim-bullseye

# Set working directory
WORKDIR /app

# Install venv and other needed tools
RUN apt-get update && apt-get install -y python3-venv && \
    python3 -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip

# Set PATH so the virtualenv is used by default
ENV PATH="/opt/venv/bin:$PATH"

# Copy and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the rest of the app
COPY . .

# Default command (you can change it as needed)
COPY run.sh /app/
EXPOSE 8001
EXPOSE 8000
ENTRYPOINT ["bash", "run.sh"]
