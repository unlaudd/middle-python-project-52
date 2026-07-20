# Task Manager Makefile
# Usage: make <target>
# Example: make start, make test, make help

# Variables
PYTHON := uv run python
MANAGE := $(PYTHON) manage.py

# Phony targets (prevent conflicts with files of the same name)
.PHONY: help install build migrate makemigrations collectstatic compilemessages start test render-start

help: ## Show this help message
	@echo "Available commands:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install project dependencies using uv
	uv sync

build: ## Run the production build script (build.sh)
	./build.sh

migrate: ## Apply database migrations
	$(MANAGE) migrate

makemigrations: ## Create new database migrations based on model changes
	$(MANAGE) makemigrations

collectstatic: ## Collect static files for production deployment
	$(MANAGE) collectstatic --noinput

compilemessages: ## Compile translation files (.po to .mo)
	$(MANAGE) compilemessages

start: ## Run the local development server
	$(MANAGE) runserver

test: ## Run the Django test suite
	$(MANAGE) test

render-start: ## Start the application with Gunicorn (for Render/Production)
	gunicorn task_manager.wsgi:application