SHELL:=/bin/bash

# http://clarkgrubb.com/makefile-style-guide#phony-targets

.DEFAULT_GOAL := help

.PHONY: help
help: ## Show the help messages
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort -k 1,1 | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


.PHONY: js
js:
	npm run build --prefix ./php/public


.PHONY: js-watch
js-watch:
	npm run watch --prefix ./kt_uri/configuration/public


.PHONY: css
css: ## Create the css files from the sass files
	@cd camac/configuration/public/css/; make css


.PHONY: css-watch
css-watch: ## Watch the sass files and create the css when they change
	@cd camac/configuration/public/css/; make watch


.PHONY: install-api-doc
install-api-doc: ## installs the api doc generator tool
	npm i -g apidoc


.PHONY: generate-api-doc
generate-api-doc: ## generates documentation for the i-web portal API
	apidoc -i kt_uri/configuration/Custom/modules/portal/controllers/ -o doc/
	@echo "Documentation was saved in /doc folder."


.PHONY: clear-cache ## Clear the memcache
clear-cache:
	@docker-compose exec php php -d xdebug.remote_enable=off /var/www/camac/cronjob/clear-cache.php
