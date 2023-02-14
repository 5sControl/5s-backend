#!/bin/sh

# create tables 
python manage.py makemigrations
python manage.py migrate

# fill algorithm table
python manage.py algorithm

# run server
python manage.py runserver 0.0.0.0:8000

# yes Y | python manage.py makemigrations &&
# python manage.py migrate &&

