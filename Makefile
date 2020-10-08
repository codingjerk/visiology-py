all: test lint typecheck coverage quality build

.PHONY: test lint typecheck coverage quality build deploy all

test:
	@echo [ === TEST === ]
	@python3 -m pytest --quiet

lint:
	@echo [ === LINT === ]
	@python3 -m pycodestyle . --exclude venv,tests,setup.py,build,dist,.eggs

typecheck:
	@echo [ === TYPECHECK === ]
	@python3 -m mypy --strict --pretty --allow-untyped-decorators --no-error-summary --ignore-missing-imports visiology_py i2ls tests

coverage:
	@echo [ === COVERAGE === ]
	@PYTHONPATH=. python3 -m pytest --cov=visiology_py --cov-fail-under=50 --cov-report=term-missing:skip-covered --quiet
	@PYTHONPATH=. python3 -m pytest --cov=i2ls --cov-fail-under=90 --cov-report=term-missing:skip-covered --quiet

quality:
	@echo [ === QUALITY === ]
	@radon mi visiology_py/**.py i2ls/**.py
	@radon cc visiology_py/**.py i2ls/**.py

build:
	@echo [ === BUILD === ]
	@python3 setup.py -q sdist bdist

deploy:
	@echo [ === DEPLOY === ]
	@rm -rf dist/visiology-py-*.linux-x86_64.tar.gz
	@python3 -m twine upload dist/visiology-py-*.tar.gz
