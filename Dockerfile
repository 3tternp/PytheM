FROM python:3.11-slim

WORKDIR /usr/src/app

COPY . .

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    tcpdump \
    libnetfilter-queue-dev \
    libffi-dev \
    libssl-dev \
  && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir .

CMD [ "pythem" ]

