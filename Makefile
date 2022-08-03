deps:
	pip3 install --upgrade pip poetry
	poetry install

dev: deps

format:
	poetry run isort src tests
	poetry run black src tests

lint: format
	poetry run flake8 src/* tests/*
	poetry run mypy src/*.py tests/*.py

update-requirements:
	poetry export --format=requirements.txt > src/requirements.txt

security-baseline:
	poetry run bandit -r src

complexity-baseline:
	$(info Maintainability index)
	poetry run radon mi src
	$(info Cyclomatic complexity index)
	poetry run xenon --max-absolute C --max-modules A --max-average A src

pr: lint security-baseline complexity-baseline

clean:
	poetry env remove python3
