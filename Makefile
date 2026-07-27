.PHONY: install test lint format quality dashboard docker-build

install:
	python -m pip install --upgrade pip
	pip install -r requirements-dev.txt

lint:
	ruff check src tests dashboard scripts

format:
	ruff format src tests dashboard scripts
	ruff check --fix src tests dashboard scripts

test:
	pytest

quality: lint test

dashboard:
	streamlit run dashboard/app.py

docker-build:
	docker build -t ethiopia-fi-forecast:week12 .
