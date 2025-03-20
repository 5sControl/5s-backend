#!/bin/sh
# FIXED ERROR migrations ManyToMany fields
python manage.py migrate --fake Mailer 0002_workingtimedaysofweek_alter_workingtime_days_of_week
python manage.py migrate --fake Mailer 0003_alter_workingtimedaysofweek_day_of_week_and_more

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