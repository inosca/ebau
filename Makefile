SHELL:=/bin/sh

# http://clarkgrubb.com/makefile-style-guide#phony-targets

.DEFAULT_GOAL := help

GIT_USER=$(shell git config user.email)

define set_env
	sed 's/^\(APPLICATION=\).*$//\1$(1)/' -i .env django/.env
endef

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

.PHONY: clear-cache
clear-cache: ## Clear the memcache
	@docker-compose exec php php -d xdebug.remote_enable=off /var/www/camac/cronjob/clear-cache.php

.PHONY: dumpconfig-camac
dumpconfig-camac:
	docker-compose exec django python manage.py dumpconfig

.PHONY: dumpconfig-caluma
dumpconfig-caluma:
	docker-compose exec caluma python manage.py dumpdata \
		workflow.workflow \
		workflow.task \
		workflow.taskflow \
		workflow.flow \
		form.form \
		form.formquestion \
		form.question \
		form.questionoption \
		form.option \
		> caluma/fixtures/config.json && prettier --write caluma/fixtures/config.json

.PHONY: dumpconfig
dumpconfig: dumpconfig-caluma dumpconfig-camac

.PHONY: dumpdata-camac
dumpdata-camac: ## Dump the data tables
	docker-compose exec django /app/manage.py dumpcamacdata

.PHONY: dumpdata-caluma
dumpdata-caluma:
	docker-compose exec caluma python manage.py dumpdata \
		workflow.case \
		workflow.workitem \
		form.document \
		form.answer \
		form.answerdocument \
		> caluma/fixtures/data.json && prettier --write caluma/fixtures/data.json


.PHONY: dumpdata
dumpdata: dumpdata-caluma dumpdata-camac

.PHONY: loadconfig-camac
loadconfig-camac:
	@docker-compose exec django python manage.py loadconfig --user $(GIT_USER)

.PHONY: loadconfig-caluma
loadconfig-caluma:
	@docker-compose exec caluma python manage.py loaddata caluma/fixtures/config.json

.PHONY: loaddata-caluma
loaddata-caluma:
	@docker-compose exec caluma python manage.py loaddata caluma/fixtures/data.json

.PHONY: loadconfig
loadconfig: loadconfig-caluma loadconfig-camac

.PHONY: dbshell
dbshell: ## Start a psql shell
	@docker-compose exec db psql -Ucamac


######### Changes from eBau Bern #########

.PHONY: mergeconfig
mergeconfig: ## Merge config.json
	git mergetool --tool=jsondiff

.PHONY: migrate
migrate:  ## Migrate schema
	docker-compose exec django /app/manage.py migrate
	make sequencenamespace

.PHONY: grunt-build-be
grunt-build-be: ## Grunt build
	docker-compose exec php sh -c "cd ../camac/public && npm run build-be"

.PHONY: grunt-watch-be
grunt-watch-be: ## Grunt watch
	docker-compose exec php sh -c "cd ../camac/public && npm run build-be && npm run watch-be"

.PHONY: grunt-build-sz
grunt-build-sz: ## Grunt build
	docker-compose exec php sh -c "cd ../camac/public && npm run build-sz"

.PHONY: grunt-watch-sz
grunt-watch-sz: ## Grunt watch
	docker-compose exec php sh -c "cd ../camac/public && npm run build-sz && npm run watch-sz"

.PHONY: prettier-format
prettier-format:
	docker-compose exec php sh -c "cd ../camac/public && npm run prettier-format"

.PHONY: makemigrations
makemigrations: ## Create schema migrations
	docker-compose exec django /app/manage.py makemigrations

.PHONY: flush-camac
flush-camac:
	@docker-compose exec django /app/manage.py flush --no-input

.PHONY: flush-caluma
flush-caluma:
	@docker-compose exec caluma python manage.py flush --no-input

.PHONY: flush
flush: flush-caluma flush-camac

# Directory for DB snapshots
.PHONY: _db_snapshots_dir
_db_snapshots_dir:
	@mkdir -p db_snapshots

.PHONY: db_snapshot
db_snapshot: _db_snapshots_dir  ## Make a snapshot of the current state of the database
	@docker-compose exec db  pg_dump -Ucamac -c > db_snapshots/$(shell date -Iseconds).sql

.PHONY: db_restore
db_restore:  ## Restore latest DB snapshot created with `make db_snapshot`
	@mkdir -p db_snapshots
	@echo "restoring from $(SNAPSHOT)"
	@docker-compose exec -T db psql -Ucamac < $(SNAPSHOT) > /dev/null

.PHONY: sequencenamespace
sequencenamespace:  ## Set the Sequence namespace for a given user. GIT_USER is detected from your git repository.
	@docker-compose exec django make sequencenamespace GIT_USER=$(GIT_USER)

.PHONY: log
log: ## Show logs of web container
	@docker-compose logs --follow php

.PHONY: test
test: ## Run backend tests
	@docker-compose exec django make test

.PHONY: kt_uri
kt_uri: ## Set APPLICATION to kt_uri
	$(call set_env,kt_uri)

.PHONY: kt_schwyz
kt_schwyz: ## Set APPLICATION to kt_uri
	$(call set_env,kt_schwyz)

.PHONY: kt_bern
kt_bern: ## Set APPLICATION to kt_uri
	$(call set_env,kt_bern)

.PHONY: demo
demo: ## Set APPLICATION to kt_uri
	$(call set_env,demo)
