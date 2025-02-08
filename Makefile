.PHONY: lint run

lint:
	flake8 .
	isort .
	black .
	mypy .

run:
	python merkle_tree.py 
