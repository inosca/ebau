SHELL:=/bin/sh

include .env

# http://clarkgrubb.com/makefile-style-guide#phony-targets

.DEFAULT_GOAL := help

GIT_USER=$(shell git config user.email)
DB_CONTAINER=$(shell docker compose ps -q db)
APPLICATION_ENV=$(shell docker compose exec django bash -c 'echo $$APPLICATION_ENV')
APPLICATION_NAME=$(shell docker compose exec django bash -c 'echo $$APPLICATION')

define set_app
	sed 's/^\(APPLICATION=\).*$//\1$(1)/' -i .env django/.env
	sed 's/^\(COMPOSE_FILE=\).*$//\1compose\/$(1).yml:compose\/$(1)-dev.yml/' -i .env django/.env
endef

define set_profile
	sed 's/^\(COMPOSE_PROFILES=\).*$//\1$(1)/' -i .env django/.env
	sed 's/^\(DJANGO_CLAMD_ENABLED=\).*$//\1$(2)/' -i .env django/.env
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

.PHONY: clear-cache
clear-cache: ## Clear memcache
	docker compose exec cache sh -c "echo flush_all | nc localhost 11211"

.PHONY: dumpconfig
dumpconfig: ## Dump the current camac and caluma configuration
	docker compose exec django python manage.py camac_dump_config
	@npx --yes prettier@3.0.3 --log-level silent --write "django/${APPLICATION}/config/*.json"

.PHONY: dumpdata
dumpdata: ## Dump the current camac and caluma data
	docker compose exec django /app/manage.py camac_dump_data
	@npx --yes prettier@3.0.3 --log-level silent --write "django/${APPLICATION}/data/*.json"

.PHONY: loadconfig-camac
loadconfig-camac: ## Load the camac configuration
	@echo "\e[31m⚠️  Loading CAMAC config. This can take a moment, especially if migrations are running.\e[0m"
	@echo "\e[31m   While this is in progress, do not use the web-interface yet!\e[0m"
	@docker compose exec django ./wait-for-it.sh -t 300 127.0.0.1:80 -- python manage.py camac_load --user $(GIT_USER)

.PHONY: loadconfig-dms
loadconfig-dms: ## Load the DMS configuration
	@if docker compose config|grep -q document-merge-service; then \
		docker compose exec document-merge-service poetry run python manage.py loaddata /tmp/document-merge-service/dump.json; \
	fi

.PHONY: dumpconfig-dms
dumpconfig-dms: ## Dump the DMS configuration
	@if docker compose config|grep -q document-merge-service; then \
		docker compose exec -u root document-merge-service bash -c "poetry run python manage.py dumpdata api.Template > /tmp/document-merge-service/dump.json" ; \
		npx --yes prettier@3.0.3 --log-level silent --write "document-merge-service/${APPLICATION}/dump.json"; \
	fi


.PHONY: loadconfig-keycloak
loadconfig-keycloak: ## Load the keycloak configuration
	@if [ ${APPLICATION_ENV} = "development" ]; then \
		echo -n "loading keycloak config... "; \
		docker compose exec keycloak /opt/keycloak/bin/kc.sh import --override true --file /opt/keycloak/data/import/test-config.json >/dev/null 2>&1 || true; \
		echo "done."; \
	fi

.PHONY: dumpconfig-keycloak
dumpconfig-keycloak: ## Dump the keycloak configuration
	docker compose exec keycloak /opt/keycloak/bin/kc.sh export --file /opt/keycloak/data/import/test-config.json
	@npx --yes prettier@3.0.3 --log-level silent --write "keycloak/config/${APPLICATION}-test-config.json"

.PHONY: loadconfig
loadconfig: loadconfig-camac loadconfig-dms loadconfig-keycloak ## Load all configuration
	@echo "\e[32mConfiguration has been loaded successfully. Go ahead and login.🚀\e[0m"

.PHONY: dbshell
dbshell: ## Start a psql shell
	@docker compose exec db psql -Ucamac ${APPLICATION}

.PHONY: ember-dev
ember-dev: ## Set up .env and application.ini for local ember development
	@if docker compose config|grep -q php; then \
		sed -re 's/ember\.development.*/ember\.development = true/' -i php/${APPLICATION}/configs/application.ini; \
		sed -re 's/portal\.uri.*/portal\.uri = http:\/\/localhost:4200/' -i php/${APPLICATION}/configs/application.ini; \
		sed -re 's/baseURLPortal.*/baseURLPortal = http:\/\/localhost:4200/' -i php/${APPLICATION}/configs/application.ini; \
		echo "Set ember.development = true in application.ini"; \
	else \
		@grep -q INTERNAL_URL .env || echo INTERNAL_URL=http://localhost:4400 >> .env; \
		@echo "Added local INTERNAL_URL to .env."; \
	fi
	@grep -q PORTAL_URL .env || echo PORTAL_URL=http://localhost:4200 >> .env
	@echo "Added local PORTAL_URL to .env."

.PHONY: ember-dev-reset
ember-dev-reset: ## Set up .env and application.ini for non-local runtime (docker)
	@if docker compose config|grep -q php; then \
		sed -re 's/ember\.development.*/ember.development = false/' -i php/${APPLICATION}/configs/application.ini; \
		sed -re 's/portal\.uri.*/portal.uri = http:\/\/ebau-portal.local/' -i php/${APPLICATION}/configs/application.ini; \
		sed -re 's/baseURLPortal.*/baseURLPortal = http:\/\/ebau-portal.local/' -i php/${APPLICATION}/configs/application.ini; \
		echo "Set ember.development = false in application.ini"; \
	fi
	@sed -i '/PORTAL_URL/d' .env
	@sed -i '/INTERNAL_URL/d' .env
	@echo "Removed PORTAL_URL and INTERNAL_URL from .env."

######### Changes from eBau Bern #########

.PHONY: mergeconfig
mergeconfig: ## Merge config.json
	git mergetool --tool=jsondiff

.PHONY: migrate
migrate:  ## Migrate schema
	docker compose exec django /app/manage.py migrate
	make sequencenamespace


.PHONY: format
format:
	@yarn --cwd=ember-camac-ng install
	@yarn --cwd=ember-camac-ng lint:js --fix
	@yarn --cwd=ember-caluma-portal install
	@yarn --cwd=ember-caluma-portal lint:js --fix
	@yarn --cwd=ember install
	@yarn --cwd=ember lint:js --fix
	@(cd django && ruff format)
	@npx --yes prettier@3.0.3 --write *.yml
	@npx --yes prettier@3.0.3 --write compose/*.yml

.PHONY: makemigrations
makemigrations: ## Create schema migrations
	docker compose exec django /app/manage.py makemigrations

.PHONY: flush
flush:
	@docker compose exec django /app/manage.py flush --no-input


.PHONY: db_dump
db_dump: ## Dump the databse into an SQL dump file. Needs SNAPSHOT=xyz parameter
	@[ -z "$(SNAPSHOT)" ] && echo "Need SNAPSHOT=... make parameter to dump the DB" || true
	@[ -n "$(SNAPSHOT)" ] && docker compose exec db pg_dump $(APPLICATION_NAME) -Ucamac -c > $(SNAPSHOT)

.PHONY: db_load
db_load: ## Load an SQL dump file into the DB. Needs SNAPSHOT=xyz parameter
	@[ ! -f "$(SNAPSHOT)" ] && echo "No snapshot given, Need SNAPSHOT=... make parameter to load" || true
	@[   -f "$(SNAPSHOT)" ] && echo "restoring from $(SNAPSHOT)" || true
	@[   -f "$(SNAPSHOT)" ] && docker compose exec -T db psql -Ucamac  $(APPLICATION_NAME) < "$(SNAPSHOT)" > /dev/null ||  true

.PHONY: sequencenamespace
sequencenamespace:  ## Set the Sequence namespace for a given user. GIT_USER is detected from your git repository.
	@docker compose exec django make sequencenamespace GIT_USER=$(GIT_USER)

.PHONY: db_snapshot
db_snapshot: ## Snapshot the current database (DB-internal snapshot)
	@docker-compose exec django ./manage.py snapdb --create
.PHONY: db_restore
db_restore: ## Restore the current database from latest DB-internal snapshot
	@docker-compose exec django ./manage.py snapdb --restore --latest


.PHONY: test
test: ## Run backend tests
	@docker compose exec django make test

.PHONY: integration-tests
integration-tests: ## Run BDD integration tests
	@docker-compose run --rm bdd poetry run behave

.PHONY: kt_uri
kt_uri: ## Set APPLICATION to kt_uri
	$(call set_app,kt_uri)

.PHONY: kt_schwyz
kt_schwyz: ## Set APPLICATION to kt_schwyz
	$(call set_app,kt_schwyz)

.PHONY: kt_so
kt_so: ## Set APPLICATION to kt_so
	$(call set_app,kt_so)

.PHONY: kt_bern
kt_bern: ## Set APPLICATION to kt_bern
	$(call set_app,kt_bern)

.PHONY: kt_gr
kt_gr: ## Set APPLICATION to kt_gr
	$(call set_app,kt_gr)

.PHONY: demo
demo: ## Set APPLICATION to demo
	$(call set_app,demo)

.PHONY: profile-full
profile-full: ## Set docker compose profile to "full"
	$(call set_profile,full,true)

.PHONY: profile-slim
profile-slim: ## Unset docker compose profile
	$(call set_profile,"",false)

.PHONY: build-keycloak-themes
build-keycloak-themes: ## Build the .jar file for the keycloak themes
	@cd keycloak/themes/; ./mvnw install

.PHONY: clean
clean: ## Remove temporary files / build artefacts etc
	@find . -name node_modules -type d | xargs rm -rf
	@find . -name .pytest_cache -type d | xargs rm -rf
	@find . -name __pycache__ -type d | xargs rm -rf
	@rm -rf ./django/staticfiles ./django/coverage
	@rm -rf ./ember/tmp ./ember-caluma-portal/tmp ./ember-camac-ng/tmp
	@rm -rf ./ember/build ./ember-caluma-portal/build ./ember-camac-ng/build

.PHONY: next-version
next-version: ## Determine next version number
	@node tools/bin/next-version.js

.PHONY: release
release: ## Draft a new release
	@tools/bump-version.sh $(version)

.PHONY: release-folder
release-folder: ## Add a template for a release folder
	@if [ -z $(version) ]; then echo "Please pass a version: make release-folder version=x.x.x"; exit 1; fi
	@mkdir -p "releases/$(version)"
	@echo "# Neu\n-\n# Korrekturen\n-" >> "releases/$(version)/CHANGELOG.md"
	@echo "# Änderungen\n## Ansible (Rolle / Variablen)\n-\n## DB\n-\n## Apache\n-" >> "releases/$(version)/MANUAL.md"

.PHONY: django-shell
django-shell:
	@docker compose exec django python manage.py shell

.PHONY: user-admin
user-admin: ## Add most recent user to admin group
	@docker compose exec db psql -Ucamac ${APPLICATION} -c 'insert into "USER_GROUP" ("DEFAULT_GROUP", "GROUP_ID", "USER_ID") values (1, 1, (select "USER_ID" from "USER" order by "USER_ID" desc limit 1));'

.PHONY: debug-django
debug-django: ## start a api container with service ports for debugging
	@docker compose stop django
	@echo "Run './manage.py runserver 0:80' to start the debugging server"
	@docker compose run --user root --use-aliases --service-ports django bash

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
	@docker compose restart db > /dev/null 2>&1
	@docker compose exec db dropdb -U camac ${APPLICATION}
	@docker compose exec db createdb -U camac ${APPLICATION}
	@docker compose exec db pg_restore -d ${APPLICATION} -U camac -c --no-privileges --no-owner --if-exists /tmp/latest.dmp
	@echo "Running migrations and loading new config..."
	@docker compose stop keycloak
	@docker compose rm -f keycloak
	@docker compose restart > /dev/null 2>&1
	@make loadconfig > /dev/null 2>&1
	@rm latest.dmp


create-be-dump:
	@docker cp db/clean-dump.sql $(DB_CONTAINER):/tmp/clean-dump.sql
	@docker compose exec db psql -U camac ${APPLICATION} -f /tmp/clean-dump.sql
	@docker compose exec db pg_dump -U camac -d ${APPLICATION} -Fc -f /tmp/latest.dmp
	@docker cp $(DB_CONTAINER):/tmp/latest.dmp .
	@docker compose exec db rm /tmp/latest.dmp
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

.PHONY: watch-templatefiles
watch-templatefiles: # Upload DMS templates to minio on change
	@if command -v inotifywait >/dev/null; then \
		while inotifywait -e close_write document-merge-service/${APPLICATION}/templatefiles; do make update-templatefiles; done; \
	else \
		echo "Please install inotify-tools to use this target"; \
		exit 1; \
	fi

.PHONY: update-templatefiles
update-templatefiles: # Upload DMS templates to minio
	@docker compose run --rm --no-deps mc -u

.PHONY: prettier-check
prettier-check: # Check formatting of yml and config files with prettier
	@npx --yes prettier@3.0.3 -c **/*.yml "django/**/*.json"

.PHONY: prettier-fix
prettier-fix: # Fix formatting of yml and config files with prettier
	@npx --yes prettier@3.0.3 --write **/*.yml "django/**/*.json"

.PHONY: compare-dump
compare-dump: # Compares two given .json dump files
	@node tools/bin/compare-dumps.js $(PWD)/$(word 1,$^) $(PWD)/$(word 2,$^)