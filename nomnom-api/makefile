dev:
	uv run uvicorn app.main:app --reload --port 8000

migrate:
	uv run alembic upgrade head

.PHONY: dev migrate