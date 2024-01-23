# Работа через Docker

build:
	docker compose build

run:
	docker compose up -d

stop:
	docker compose down -v

lint:
	docker compose run --rm py-linters flake8 /app/

makemigrations:
	docker compose run --rm app ./manage.py makemigrations

migrate:
	docker compose run --rm app ./manage.py migrate

first_start:
	make build migrate
	docker compose run --rm app ./manage.py createsuperuser
