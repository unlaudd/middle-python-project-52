install:
	uv sync

build:
	./build.sh

collectstatic:
	uv run python manage.py collectstatic --noinput

migrate:
	uv run python manage.py migrate

render-start:
	gunicorn task_manager.wsgi

start:
	uv run python manage.py runserver