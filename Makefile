APP_DIR = app

.PHONY: lint flake8 isort black mypy run test coverage test-watch

flake:  # Run flake8 linting
	flake8 .

isort:  # Run isort to sort imports
	isort .

black:  # Run black formatter
	black .

mypy:  # Run mypy type checking
	mypy .

lint: flake isort black mypy  # Run all linting tools

run:
	python $(APP_DIR)/main.py

test:  # Run tests
	pytest -v

coverage:  # Run tests with coverage report
	pytest -v --cov=$(APP_DIR)/blockchain --cov-report=term-missing

test-watch:  # Run tests in watch mode (requires pytest-watch)
	ptw -- -v
