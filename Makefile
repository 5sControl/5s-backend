migrate:
	python manage.py makemigrations
	python manage.py migrate
run:
	python manage.py runserver
fill:
	python manage.py algorithm
	python manage.py createadmin
startprocess:
	python manage.py startprocess
mssql-get:
	python manage.py inspectdb --database=mssql Skany > src/Order/models.py
all:
	make migrate
	make fill
	make startprocess
	mssql-get
	make run