.PHONY: install

install:
	uv sync

create-env:
	uv venv

run-dev:
	uv run langgraph dev