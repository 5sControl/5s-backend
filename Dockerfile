FROM python:3.9-slim AS builder

RUN apt-get update && apt-get install -y \
    cmake \
    gcc \
    python3-dev \
    musl-dev \
    sudo \
    unixodbc-dev \
    curl \
    gnupg

RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list

RUN apt-get update && ACCEPT_EULA=Y apt-get install -y \
    msodbcsql17 \
    freetds-dev \
    freetds-bin

RUN apt-get install -y iputils-ping

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt .
RUN pip3 install --upgrade pip && \
    pip3 install -r requirements.txt

COPY . .

EXPOSE 80

RUN chmod +x /usr/src/app/entrypoint.sh

CMD ./entrypoint.sh