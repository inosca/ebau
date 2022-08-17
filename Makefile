SHELL:=/bin/sh

include .env

# http://clarkgrubb.com/makefile-style-guide#phony-targets

.DEFAULT_GOAL := help

GIT_USER=$(shell git config user.email)
DB_CONTAINER=$(shell docker-compose ps -q db)

define set_env
	sed 's/^\(APPLICATION=\).*$//\1$(1)/' -i .env django/.env
	sed 's/^\(COMPOSE_FILE=\).*$//\1compose\/$(1).yml:compose\/$(1)-dev.yml/' -i .env django/.env
endef

.PHONY: help
help: ## Show the help messages
	@grep -h -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort -k 1,1 | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: start-dev-env
start-dev-env:  ## Interactive initial setup of dev-environment
	./tools/start-dev-env

.env:
	touch .env

.PHONY: js-watch
js-watch:
	npm run watch --prefix ./kt_uri/configuration/public


.PHONY: css
css: ## Create the css files from the sass files
	@cd camac/configuration/public/css/; make css


.PHONY: css-watch
css-watch: ## Watch the sass files and create the css when they change
	@cd camac/configuration/public/css/; make watch

.PHONY: dumpconfig
dumpconfig: ## Dump the current camac and caluma configuration
	docker-compose exec django python manage.py camac_dump_config
	@yarn prettier --loglevel silent --write "django/${APPLICATION}/config/*.json"

.PHONY: dumpdata
dumpdata: ## Dump the current camac and caluma data
	docker-compose exec django /app/manage.py camac_dump_data
	@yarn prettier --loglevel silent --write "django/${APPLICATION}/data/*.json"

.PHONY: loadconfig-camac
loadconfig-camac: ## Load the camac configuration
	@docker-compose exec django ./wait-for-it.sh -t 300 127.0.0.1:80 -- python manage.py camac_load --user $(GIT_USER)

.PHONY: loadconfig-dms
loadconfig-dms: ## Load the DMS configuration
	@if docker-compose config|grep -q document-merge-service; then \
		docker-compose exec document-merge-service poetry run python manage.py loaddata /tmp/document-merge-service/dump.json; \
	fi

.PHONY: loadconfig
loadconfig: loadconfig-camac loadconfig-dms ## Load the DMS and camac configuration

.PHONY: dbshell
dbshell: ## Start a psql shell
	@docker-compose exec db psql -Ucamac ${APPLICATION}

.PHONY: ember-dev
ember-dev: ## Set ember.development to true in application.ini
	@sed -re 's/ember\.development.*/ember.development = true/' -i php/${APPLICATION}/configs/application.ini


######### Changes from eBau Bern #########

.PHONY: mergeconfig
mergeconfig: ## Merge config.json
	git mergetool --tool=jsondiff

.PHONY: migrate
migrate:  ## Migrate schema
	docker-compose exec django /app/manage.py migrate
	make sequencenamespace

.PHONY: format
format:
	@yarn --cwd=ember-camac-ng install
	@yarn --cwd=ember-camac-ng lint:js --fix
	@yarn --cwd=ember-caluma-portal install
	@yarn --cwd=ember-caluma-portal lint:js --fix
	@yarn --cwd=ember install
	@yarn --cwd=ember lint:js --fix
	@black django
	@yarn prettier --write *.yml

.PHONY: makemigrations
makemigrations: ## Create schema migrations
	docker-compose exec django /app/manage.py makemigrations

.PHONY: flush
flush:
	@docker-compose exec django /app/manage.py flush --no-input

# Directory for DB snapshots
.PHONY: _db_snapshots_dir
_db_snapshots_dir:
	@mkdir -p db_snapshots

.PHONY: db_snapshot
db_snapshot: _db_snapshots_dir  ## Make a snapshot of the current state of the database
	@docker-compose exec db  pg_dump -Ucamac -c > db_snapshots/$(shell date -Iseconds).sql

.PHONY: db_restore
db_restore:  _db_snapshots_dir ## Restore latest DB snapshot created with `make db_snapshot`
	@echo "restoring from $(SNAPSHOT)"
	@docker-compose exec -T db psql -Ucamac < $(SNAPSHOT) > /dev/null

.PHONY: sequencenamespace
sequencenamespace:  ## Set the Sequence namespace for a given user. GIT_USER is detected from your git repository.
	@docker-compose exec django make sequencenamespace GIT_USER=$(GIT_USER)

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

.PHONY: clean
clean: ## Remove temporary files / build artefacts etc
	@find . -name node_modules -type d | xargs rm -rf
	@find . -name .pytest_cache -type d | xargs rm -rf
	@find . -name __pycache__ -type d | xargs rm -rf
	@rm -rf ./django/staticfiles ./django/coverage
	@rm -rf ./ember/tmp ./ember-caluma-portal/tmp ./ember-camac-ng/tmp
	@rm -rf ./ember/build ./ember-caluma-portal/build ./ember-camac-ng/build

.PHONY: release
release: ## Draft a new release
	@if [ -z $(version) ]; then echo "Please pass a version: make release version=x.x.x"; exit 1; fi
	@echo $(version) > VERSION.txt
	@sed -i -e 's/"version": ".*",/"version": "$(version)",/g' ember-camac-ng/package.json
	@sed -i -e 's/"version": ".*",/"version": "$(version)",/g' ember-caluma-portal/package.json
	@sed -i -e 's/__version__ = ".*"/__version__ = "$(version)"/g' django/camac/camac_metadata.py

.PHONY: release-folder
release-folder: ## Add a template for a release folder
	@if [ -z $(version) ]; then echo "Please pass a version: make release-folder version=x.x.x"; exit 1; fi
	@mkdir -p "releases/$(version)"
	@echo "# Neu\n-\n# Korrekturen\n-" >> "releases/$(version)/CHANGELOG.md"
	@echo "# Änderungen\n## Ansible (Rolle / Variablen)\n-\n## DB\n-\n## Apache\n-" >> "releases/$(version)/MANUAL.md"

.PHONY: django-shell
django-shell:
	@docker-compose exec django python manage.py shell

.PHONY: user-admin
user-admin: ## Add most recent user to admin group
	@docker-compose exec db psql -Ucamac ${APPLICATION} -c 'insert into "USER_GROUP" ("DEFAULT_GROUP", "GROUP_ID", "USER_ID") values (1, 1, (select "USER_ID" from "USER" order by "USER_ID" desc limit 1));'

.PHONY: debug-django
debug-django: ## start a api container with service ports for debugging
	@docker-compose stop django
	@echo "run ./manage.py runserver 0:80 to start debug server"
	@docker-compose run --user root --use-alias --service-ports django bash

.PHONY: load-be-dump
load-be-dump: SHELL:=/bin/bash
load-be-dump:
	@if [ ! -f latest.dmp ]; then \
		echo "Enter credentials for https://cloud.adfinis.com:"; \
		read -p "Username: " user; \
		read -p "Password: " -s pass; \
		echo "\n"; \
		curl -s -u $$user:$$pass --output latest.dmp https://cloud.adfinis.com/remote.php/webdav/partner/KantonBE/db_dumps/ebau.apps.be.ch/latest.dmp > /dev/null; \
	fi
	@docker cp latest.dmp $(DB_CONTAINER):/tmp
	@echo "Importing dump into DB..."
	@docker-compose restart db > /dev/null 2>&1
	@docker-compose exec db dropdb -U camac ${APPLICATION}
	@docker-compose exec db createdb -U camac ${APPLICATION}
	@docker-compose exec db pg_restore -d ${APPLICATION} -U camac -c --no-privileges --no-owner --if-exists /tmp/latest.dmp
	@echo "Running migrations and loading new config..."
	@docker-compose stop keycloak
	@docker-compose rm -f keycloak
	@docker-compose restart > /dev/null 2>&1
	@make loadconfig > /dev/null 2>&1
	@rm latest.dmp


create-be-dump:
	@docker cp db/clean-dump.sql $(DB_CONTAINER):/tmp/clean-dump.sql
	@docker-compose exec db psql -U camac ${APPLICATION} -f /tmp/clean-dump.sql
	@docker-compose exec db pg_dump -U camac -d ${APPLICATION} -Fc -f /tmp/latest.dmp
	@docker cp $(DB_CONTAINER):/tmp/latest.dmp .
	@docker-compose exec db rm /tmp/latest.dmp
	@echo "Please upload latest.dmp here: https://cloud.adfinis.com/apps/files/?dir=/partner/KantonBE/db_dumps/ebau.apps.be.ch"

update-lockfile:
	@yarn upgrade && rm -rf node_modules ember-*/node-modules && yarn

link-ember-caluma:
	@yarn link \
	@projectcaluma/ember-core \
	@projectcaluma/ember-form \
	@projectcaluma/ember-form-builder \
	@projectcaluma/ember-workflow \
	@projectcaluma/ember-distribution

unlink-ember-caluma:
	@yarn unlink \
	@projectcaluma/ember-core \
	@projectcaluma/ember-form \
	@projectcaluma/ember-form-builder \
	@projectcaluma/ember-workflow \
	@projectcaluma/ember-distribution
	@yarn --force
