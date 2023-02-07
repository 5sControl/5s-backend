FROM python:3.9

RUN apt update && apt -y install cmake gcc python3-dev musl-dev sudo

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip3 install --upgrade pip
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt

COPY . /usr/src/app/
EXPOSE 8000

RUN ["chmod", "+x", "/usr/src/app/entrypoint.sh"]

# run the command
# ENTRYPOINT ["/usr/src/app/entrypoint.sh"]

CMD ./entrypoint.sh
