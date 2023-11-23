.DEFAULT_GOAL := help

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort -k 1,1 | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: install-dev
install-dev: ## Install development environment
	@poetry install --all-extras

.PHONY: test
test: ## Test the extensions
	@poetry run black --check document_merge_service/extensions/
	@poetry run flake8 document_merge_service/extensions/
	@poetry run pytest -vv --cov document_merge_service/extensions --cov-report term --cov-report xml:artifacts/cobertura.xml --junitxml=artifacts/junit.xml document_merge_service/extensions/

.PHONY: format
format: ## Format the extensions
	@poetry run black document_merge_service/extensions/
	@poetry run isort document_merge_service/extensions/
