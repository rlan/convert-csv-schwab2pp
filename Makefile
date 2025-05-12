# Makefile for easy development workflows.
# See development.md for docs.
# Note GitHub Actions call uv directly, not this Makefile.

.DEFAULT_GOAL := default

.PHONY: default install lint test upgrade build clean

default: install lint test

install:
	uv sync --all-extras --group lint

lint:
	-codespell ./src
	-ruff check ./src
	-ruff format ./src

test:
	-schwab2pp example.csv test.csv
	-diff example_out.csv test.csv

upgrade:
	uv sync --upgrade --group lint

build:
	uv build

clean:
	-rm -rf dist/
	-rm -rf *.egg-info/
	-rm -rf .pytest_cache/
	-rm -rf .mypy_cache/
	-rm -rf .venv/
	-find . -type d -name "__pycache__" -exec rm -rf {} +