SHELL:=/bin/bash

.PHONY: help run run-fancy db-reset db-init css css-watch _classloader \
	init structure-export config-export config-import \
	deploy-test-server run-deploy-db run-live-db _log-follow
	ci-config-import ci-db-init

.DEFAULT_GOAL := help

DB_CONTAINER?=docker_camac_db_1

SSH_PASS=sshpass -p 'admin'


_log-follow: # Tail the log of the application
	@tail -f camac/logs/application.log


run-fancy: ## Create a tmux session that runs several useful commands at once: make up, make log-follow and make watch
	@tmux new-session -n 'camac runner' -d 'make run'
	@tmux split-window -v 'make _log-follow' # split vertically
	@tmux select-pane -U # go one pane upwards
	@tmux select-pane -U # go one pane upwards
	@tmux split-window -h 'make watch' # split horizontally on the most upper pane

	@tmux -2 attach-session -d

_init-ci: _submodule-update
	@rm -f camac/configuration
	@ln -fs ../kt_uri/configuration camac/configuration
	@rm -f camac/configuration/configs/application.ini
	@ln -s application-ci.ini camac/configuration/configs/application.ini
	for i in `ls kt_uri/library/`; do rm -f "camac/library/$$i"; done
	for i in `ls kt_uri/library/`; do ln -sf "../../kt_uri/library/$$i" "camac/library/$$i"; done
	@chmod o+w camac/logs
	@chmod o+w camac/configuration/upload

_init: _submodule-update # Initialise the code, create the necessary symlinks
	@rm -f camac/configuration
	@ln -fs ../kt_uri/configuration camac/configuration
	@rm -f camac/configuration/configs/application.ini
	@ln -s application-dev.ini camac/configuration/configs/application.ini
	for i in `ls kt_uri/library/`; do rm -f "camac/library/$$i"; done
	for i in `ls kt_uri/library/`; do ln -sf "../../kt_uri/library/$$i" "camac/library/$$i"; done
	@chmod o+w camac/logs
	@chmod o+w camac/configuration/upload


_submodule-update:
	@git submodule update --init --recursive || true


run: _init ## Runs the docker containers
	@docker-compose -f docker/docker-compose.yml up

db-reset: ## Drops the database and re-initialises it. Use the DB_CONTAINER variable to override the destination docker container
	@echo "Resetting the database"
	@docker exec -it $(DB_CONTAINER) chmod +x /var/local/tools/database/drop_user.sh
	@docker exec -it $(DB_CONTAINER) /var/local/tools/database/drop_user.sh
	@make db-init


db-init: ## Initialises the default database structure (without any data). Use the DB_CONTAINER variable to override the destination docker container
	echo "Initialise the database"
	docker exec -i $(DB_CONTAINER) chmod +x /var/local/tools/database/create_camac_user.sh
	docker exec -i $(DB_CONTAINER) bash /var/local/tools/database/create_camac_user.sh
	docker exec -i $(DB_CONTAINER) chmod +x /var/local/tools/database/insert_base_structure.sh
	docker exec -i $(DB_CONTAINER) bash /var/local/tools/database/insert_base_structure.sh


structure-export: ## Dumps the database structure. Use the DB_CONTAINER variable to override the destination docker container
	@chmod +x tools/camac/export-structure.sh
	@tools/camac/export-structure.sh $(DB_CONTAINER)


_classloader: # Build the classmaps. These are important for performance
	@docker exec -it docker_camac_web_1 bash /var/local/tools/camac/classmap_generator.sh

css: ## Create the css files from the sass files
	@cd camac/configuration/public/css/; make css


css-watch: ## Watch the sass files and create the css when they change
	@cd camac/configuration/public/css/; make watch


run-live-db: ## This is merely a command to help run another docker instance of the database (to be able to perform deplyoments)
	@docker ps | grep docker_camac_live_db_1 || echo "You must run the live version of the Database"
	@docker exec -it docker_camac_live_db_1 chmod +x /var/local/tools/database/create_camac_user.sh
	@docker exec -it docker_camac_live_db_1 /var/local/tools/database/create_camac_user.sh
	@docker exec -it docker_camac_live_db_1 chmod +x /var/local/tools/database/insert_uri_dump.sh
	@docker exec -it docker_camac_live_db_1 chown -R oracle /var/local/database/
	@docker exec -it docker_camac_live_db_1 /var/local/tools/database/insert_uri_dump.sh

_deployment_confirmation:
	@echo "Configuration will be overridden on the server"
	@echo "Press ctrl-c to abort"
	@read ohyeah

deploy-test-server: _deployment_confirmation css _classloader ## Move the code onto the test server
	@git checkout test
	@git commit --allow-empty -m "Test-Server deployment"
	@rsync -Lavz camac/* sy-jump:/mnt/sshfs/root@camac.sycloud.ch/var/www/uri/ --exclude=*.log
	@ssh sy-jump "rm /mnt/sshfs/root@camac.sycloud.ch/var/www/uri/configuration/configs/application.ini"
	@ssh sy-jump "cd /mnt/sshfs/root@camac.sycloud.ch/var/www/uri/configuration/configs/; ln -s application-testserver.ini application.ini"
	@ssh sy-jump "chown -R www-data /mnt/sshfs/root@camac.sycloud.ch/var/www/uri/logs"
	@scp tools/deploy/test-server-htaccess sy-jump:/mnt/sshfs/root@camac.sycloud.ch/var/www/uri/public/.htaccess
	@scp tools/deploy/test-server-passwd sy-jump:/mnt/sshfs/root@camac.sycloud.ch/var/www/uri/passwd
	@cd db_admin/uri_database/ && USE_DB='test_server' python manage.py importconfig

deploy-portal-test-server:
	@rsync -avz iweb_mock/* sy-jump:/mnt/sshfs/root@camac.sycloud.ch/var/www/iweb/ --exclude=node_modules/*
	# TODO: npm install, forever restart. How to call a command on the server?

run-deploy-db: ## This is merely a command to help run another docker instance for deploying
	docker-compose -f docker/docker-deploy-db.yml up


config-export: ## export the current database configuration
	@make -C db_admin/ exportconfig
	@echo "Config successfully written"


config-import: ## import the current database configuration. This will override your existing stuff!
	@make -C db_admin/ importconfig
	@echo "Config successfully imported"


ci-config-import:
	@make -C db_admin/  importconfig-ci
	@echo "config successfully imported"


ci-db-init:
	$(SSH_PASS) ssh root@localhost -p 49160 mkdir -p /var/local/database /var/local/tools
	$(SSH_PASS) scp tools/database -p 49160 root@localhost:/var/local/tools/
	$(SSH_PASS) scp database/structure_dumps -p 4916 root@localhost:/var/local/database
	$(SSH_PASS) ssh root@localhost -p 49160 bash /var/local/tools/database/insert_base_structure.sh


data-truncate: ## Truncate the data in the database
	@make -C db_admin/ truncatedata
	# @make -C db_admin/ reset_sequences # TODO
	@echo "Data sucessfully truncated"


config-shell: ## start a database shell from the configuration management application
	@cd db_admin/uri_database/ && USE_DB='docker_dev' python manage.py shell


help: ## Show the help messages
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort -k 1,1 | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


run-acceptance-tests: ## run the acceptance tests
	@make -C db_admin/ run-acceptance-tests ${ARGS}

run-acceptance-tests-fast: ## run the acceptance tests fast - meaning, don't runn quite every test
	@make -C db_admin/ run-acceptance-tests-fast ${ARGS}

ci-run-acceptance-tests: ## Run a subset of the acceptance tests
	@make -C db_admin/ run-acceptance-tests-ci

install-api-doc: ## installs the api doc generator tool
	npm i -g apidoc

generate-api-doc: ## generates documentation for the i-web portal API
	apidoc -i kt_uri/configuration/Custom/modules/portal/controllers/ -o doc/
	@echo "Documentation was saved in /doc folder."
