all: test lint typecheck

test:
	@echo [ === TEST === ]
	@python3 -m pytest --quiet

lint:
	@echo [ === LINT === ]
	@python3 -m pycodestyle . --exclude venv,tests,setup.py

typecheck:
	@echo [ === TYPECHECK === ]
	@python3 -m mypy --strict --pretty --no-error-summary --ignore-missing-imports visiology_py tests
