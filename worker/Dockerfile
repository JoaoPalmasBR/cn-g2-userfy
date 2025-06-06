FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./
RUN apt-get update && apt-get install -y curl
RUN apt-get update && apt-get install -y curl netcat-openbsd

RUN pip install --no-cache-dir -r requirements.txt

COPY config.py .
COPY processor.py .
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh", "python", "processor.py"]

