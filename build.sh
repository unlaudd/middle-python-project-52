#!/usr/bin/env bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

uv sync
uv run python manage.py collectstatic --noinput
uv run python manage.py migrate