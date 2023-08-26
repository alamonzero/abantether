FROM python:3.11-slim-bullseye

RUN apt-get update && apt-get upgrade -y && apt-get install -y --no-install-recommends \
    apt-transport-https \
    gcc \
    libc-dev \
    gettext \
    libpq-dev \
    postgresql-client \
    python3-dev \
    gdal-bin \
    libgdal-dev \
    supervisor \
    procps curl \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
ADD . .

RUN RUN pip --timeout=60 install -U pip \
    && pip --timeout=60 install --no-cache-dir -r requirements.txt

EXPOSE 8000

RUN 
