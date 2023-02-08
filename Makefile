migrate:
	python manage.py makemigrations
	python manage.py migrate
run:
	python manage.py runserver
user:
	python manage.py createsuperuser
all:
	python manage.py makemigrations
	python manage.py migrate
	python manage.py runserver