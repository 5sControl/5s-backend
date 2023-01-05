#!/bin/bash
sudo chown $(whoami):$(whoami) /usr/src/app/database &&
yes Y | python manage.py makemigrations &&
python manage.py migrate &&
python manage.py runserver
