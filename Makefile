.PHONY: install test serve clean

install:
	@echo "Install editable package"
	pip install -e .

test:
	@echo "Run tests with coverage"
	pytest -vvs --cov=gistapi tests

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
