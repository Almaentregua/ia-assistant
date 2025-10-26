.PHONY: install

install:
	uv sync

create-env:
	uv venv

#https://pydevtools.com/handbook/explanation/what-is-an-editable-install/
editable-install:
	uv pip install -e .

run-dev:
	uv run langgraph dev

