#!/bin/sh

# create tables 
python manage.py makemigrations
python manage.py migrate

# fill algorithm table
python manage.py algorithm
python manage.py createadmin

# setup config
python manage.py startprocess

# run server
python manage.py runserver 0.0.0.0:80


