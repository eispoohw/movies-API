PROJECT="MoviesAPI"

init:
	pip install -r requirements.txt

save_req:
	pip freeze > requirements.txt

start:
	python movies/manage.py runserver

migrate:
	python movies/manage.py makemigrations
	python movies/manage.py migrate

superuser:
	python movies/manage.py createsuperuser

cc:
	black movies
	isort movies

.PHONY: init migrate start
.DEFALT_GOAL: init