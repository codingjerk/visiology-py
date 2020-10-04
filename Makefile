all: test lint typecheck build

.PHONY: test lint typecheck build deploy all

test:
	@echo [ === TEST === ]
	@python3 -m pytest --quiet

lint:
	@echo [ === LINT === ]
	@python3 -m pycodestyle . --exclude venv,tests,setup.py,build,dist,.eggs

typecheck:
	@echo [ === TYPECHECK === ]
	@python3 -m mypy --strict --pretty --no-error-summary --ignore-missing-imports visiology_py tests

build:
	@echo [ === BUILD === ]
	@python3 setup.py -q sdist bdist

deploy:
	@echo [ === DEPLOY === ]
	@rm -rf dist/visiology-py-*.linux-x86_64.tar.gz
	@python3 -m twine upload dist/visiology-py-*.tar.gz
