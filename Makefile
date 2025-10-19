.PHONY: install

install:
	uv sync

create-env:
	uv venv