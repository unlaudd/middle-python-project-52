#!/usr/bin/env bash
set -e

# Install uv package manager
curl -LsSf https://astral.sh/uv/install.sh | sh
source "$HOME/.local/bin/env"

# Install project dependencies
uv sync

# Compile translation messages
uv run python manage.py compilemessages

# Collect static files for production
uv run python manage.py collectstatic --noinput

# Apply database migrations
uv run python manage.py migrate