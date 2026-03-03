dev:
    uv run manage.py runserver

typecheck:
    uv run pyrefly check

lint:
    uv run ruff check --fix

format:
    uv run ruff format
