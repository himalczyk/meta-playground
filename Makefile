.PHONY: lint run test test-cov test-watch

lint:
	flake8 .
	isort .
	black .
	mypy .

run:
	python merkle_tree.py

test:  # Run tests
	pytest -v

coverage:  # Run tests with coverage report
	pytest -v --cov=blockchain --cov-report=term-missing

test-watch:  # Run tests in watch mode (requires pytest-watch)
	ptw -- -v
