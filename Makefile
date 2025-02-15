.PHONY: install install-dev lint types test cov serve clean

isort = isort gistapi tests
black = black gistapi tests
mypy = mypy --install-types --non-interactive gistapi

install:
	@echo "Install editable package"
	pip install -e .

install-dev:
	@echo "Install dev tools"
	pip install -e .[lint,test]

lint:
	@echo "Run linters & formatters"
	$(isort)
	$(black)

types:
	@echo "Check type hints"
	$(mypy)

test:
	@echo "Run tests with coverage"
	pytest -vvs --cov=gistapi tests

cov: test
	@echo "Build coverage html"
	coverage html

serve:
	@echo "Run Flask App Server"
	python gistapi/app.py

clean:
	@echo "Clean up files"
	rm -rf `find . -name __pycache__`
	rm -f `find . -type f -name '*.py[co]' `
	rm -f `find . -type f -name '*~' `
	rm -f `find . -type f -name '.*~' `
	rm -rf .cache
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf htmlcov
	rm -rf *.egg-info
	rm -f .coverage
	rm -f .coverage.*
	rm -rf build
	rm -rf dist
