FROM python:3.10.9-slim

WORKDIR /app

# Install pipenv
RUN pip install --upgrade pip && pip install pipenv

# Initialize pipenv and install the packages you want
# Replace 'requests pandas' with any other packages you need
RUN pipenv install requests pandas

# Install all pipenv packages globally (into the system environment)
RUN pipenv install --system --deploy

RUN apt-get update && \
    apt-get install -y openssh-server && \
    mkdir /var/run/sshd && \
    echo 'root:rootpass' | chpasswd && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

EXPOSE 22

# Copy your app files
COPY batch.py model.bin ./
CMD ["/usr/sbin/sshd", "-D"]

