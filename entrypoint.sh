#!/bin/sh

python manage.py migrate

celery -A config.celery worker -l info &
celery -A config.celery beat -l info &

python manage.py collectstatic &

python manage.py runserver 0.0.0.0:8000 &

sleep 5

python manage.py algorithm
python manage.py createadmin
#python manage.py stanowisko

while true; do
    sleep 1
done