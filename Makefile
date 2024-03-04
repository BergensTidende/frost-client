#################################################################################
# SELF DOCUMENTING HELP                                                                       #
#################################################################################

.DEFAULT_GOAL := help
.PHONY: help
help:  ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
PROJECT_NAME = frost
PYTHON_INTERPRETER = python

#################################################################################
# COMMANDS                                                                      #
#################################################################################

##@ Formatting
.PHONY: format-black
format-black: ## black (code formatter)
	@poetry run black frost

.PHONY: format-isort
format-isort: ## isort (import formatter)
	@poetry run isort frost

.PHONY: format
format: format-black format-isort ## run all formatters

##@ Linting
.PHONY: lint-black
lint-black: ## black in linting mode
	@poetry run black frost --check

.PHONY: lint-isort
lint-isort: ## isort in linting mode
	@poetry run isort frost --check

.PHONY: lint-flake8
lint-flake8: ## flake8 (linter)
	@poetry run flake8 frost

.PHONY: lint-mypy
lint-mypy: ## mypy (static-type checker)
	@poetry run mypy --python-version 3.10 --config-file pyproject.toml frost

.PHONY: lint-mypy-report
lint-mypy-report: ## run mypy & create report
	@poetry run mypy --config-file pyproject.toml frost --html-report ./mypy_html

lint: lint-black lint-isort lint-flake8 lint-mypy ## run all linters

.PHONY: test
test: ## run tests
	@poetry run pytest -v --cov=frost --cov-report=term-missing

.PHONY: convert-swagger
convert-swagger: ## convert swagger to json
	curl -X 'GET' \
  'https://converter.swagger.io/api/convert?url=https%3A%2F%2Ffrost-beta.met.no%2Fswaggerui%2Fopenapibasic.json' \
  -H 'accept: application/json' -o data/frost-openapi.json

##@ Create models
.PHONY: create-models
create-models: ## create models from frost swagger
	@poetry run datamodel-codegen --input data/frost-openapi.json --input-file-type json --output frost/api/general-models-tmp.py --output-model-type pydantic_v2.BaseModel --target-python-version 3.10 --use-double-quotes --class-name FrostAPI --snake-case-field
	@poetry run datamodel-codegen --input data/frost-reports-available.json --input-file-type json --output frost/api/reports-available-tmp.py --output-model-type pydantic_v2.BaseModel --target-python-version 3.10 --use-double-quotes --class-name ReportsAvailable --snake-case-field

##@ Releases
.PHONY: bump-patch
bump-patch: ## bump version patch
	@poetry run bump2version patch  --allow-dirty --verbose
	@poetry build
	@git add .
	@git commit -m "updating package"
	@git push --tags
	@git push

.PHONY: bump-minor
bump-minor: ## bump version minor
	@poetry run bump2version minor  --allow-dirty --verbose
	@poetry build
	@git add .
	@git commit -m "updating package"
	@git push --tags
	@git push

.PHONY: bump-major
bump-major:  ## bump version major
	@poetry run bump2version major  --allow-dirty --verbose
	@poetry build
	@git add .
	@git commit -m "updating package"
	@git push --tags
	@git push

.PHONY: release
release:  ## release package to pypi
	@poetry build & poetry publish
