FROM python:3.9-slim AS builder

RUN apt update && apt -y install cmake gcc python3-dev musl-dev sudo unixodbc-dev curl \
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list && apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17 \
    apt -y install freetds-dev freetds-bin \
    apt-get update && apt-get install -y iputils-ping

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt .
RUN pip3 install --upgrade pip \
    pip3 install -r requirements.txt

COPY . /usr/src/app/
EXPOSE 80

RUN ["chmod", "+x", "/usr/src/app/entrypoint.sh"]

CMD ./entrypoint.sh
