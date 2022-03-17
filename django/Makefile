.DEFAULT_GOAL := help

GIT_USER=$(shell git config user.email)

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort -k 1,1 | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: install
install: ## Install production environment
	@pip install --upgrade -r requirements.txt

.PHONY: install-dev
install-dev: ## Install development environment
	@pip install --upgrade -r requirements-dev.txt

.PHONY: start
start: ## Start the development server
	@docker-compose -f ../docker-compose.yml start db
	@python manage.py runserver

.PHONY: test
test: ## Test the project
	@touch .env
	@black --check .
	@flake8
	@pytest -vv --cov --no-cov-on-fail --vcr-record=none -n auto --dist loadscope

.PHONY: sqlsequencereset
sqlsequencereset:
	@python manage.py sqlsequencereset core | python manage.py dbshell

.PHONY: sequencenamespace
sequencenamespace:  ## Set the Sequence namespace for a given user
	@# please also update "SEQUENCE_NAMESPACE_APPS" in settings.py when changing apps here
	@python manage.py sequencenamespace --user $(GIT_USER) core document responsible --execute

.PHONY: import-help-text
import-help-text: ## Import help texts into form.json from csv. First argument needs to be the path to the csv file (FILE=pahtToFile)
	@python3 form_json_helper.py import $(FILE)

.PHONY: export-form
export-form: ## Export form.json to csv
	@python3 form_json_helper.py export
