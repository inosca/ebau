SHELL:=/bin/bash

# http://clarkgrubb.com/makefile-style-guide#phony-targets

.DEFAULT_GOAL := help

DB_CONTAINER?=docker_camac_db_1
DB_CONTAINER_HOSTNAME?=localhost
DB_CONTAINER_PORT?=49160

ZIP_IGNORE_PATTERN="\.(gitignore|empty)"


.PHONY: _log-follow
_log-follow: # Tail the log of the application
	@tail -f camac/logs/application.log


.PHONY: run-fancy
run-fancy: ## Create a tmux session that runs several useful commands at once: make up, make log-follow and make watch
	@tmux new-session -n 'camac runner' -d 'make run'
	@tmux split-window -v 'make _log-follow' # split vertically
	@tmux select-pane -U # go one pane upwards
	@tmux select-pane -U # go one pane upwards
	@tmux split-window -h 'make watch' # split horizontally on the most upper pane

	@tmux -2 attach-session -d

.PHONY: _base-init
_base-init: _submodule-update
	@rm -f camac/configuration
	@ln -fs ../kt_uri/configuration camac/configuration
	ln -sf "../../kt_uri/configuration/public" "camac/public/"
	for i in `ls kt_uri/library/`; do rm -f "camac/library/$$i"; done
	for i in `ls kt_uri/library/`; do ln -sf "../../kt_uri/library/$$i" "camac/library/$$i"; done
	@mkdir -p camac/logs/mails
	@chmod o+w camac/logs
	@chmod o+w camac/configuration/upload
	@make _classloader

.PHONY: _ci-init
_ci-init: _base-init
	@ENV='ci' make -C resources/configuration-templates/
	@ENV='ci' make htaccess

.PHONY: _init
_init: _base-init# Initialise the code, create the necessary symlinks
	@ENV='dev' make -C resources/configuration-templates/
	@ENV='dev' make htaccess

.PHONY: _submodule-update
_submodule-update:
	git submodule update --init --recursive || true
	touch camac/logs/application.log
	chmod 777 -R camac/logs || true


.PHONY: run
run: _init ## Runs the docker containers
	@docker-compose -f docker/docker-compose.yml up

.PHONY: db-create-user
db-create-user: _sync_db_tools ## Create the user camac in the database
	echo "Create the camac user"
	@bash ./.chmod_and_call_in_docker.sh $(DB_CONTAINER_HOSTNAME) $(DB_CONTAINER_PORT) /var/local/tools/database/create_camac_user.sh


.PHONY: db-drop
db-drop: _sync_db_tools ## Drops the whole database
	@echo "Resetting the database"
	@bash ./.chmod_and_call_in_docker.sh $(DB_CONTAINER_HOSTNAME) $(DB_CONTAINER_PORT) /var/local/tools/database/drop_user.sh


.PHONY: db-reset
db-reset: _sync_db_tools db-drop ## Drops the database and re-initialises it. Use the DB_CONTAINER variable to override the destination docker container
	@make db-init


.PHONY: _sync_db_tools
_sync_db_tools:
	echo "Syncing tools to docker container"
	sshpass -p "admin" scp -o StrictHostKeyChecking=no -r -P $(DB_CONTAINER_PORT) tools root@$(DB_CONTAINER_HOSTNAME):/var/local/
	sshpass -p "admin" scp -o StrictHostKeyChecking=no -r -P $(DB_CONTAINER_PORT) database root@$(DB_CONTAINER_HOSTNAME):/var/local/


.PHONY: db-init
db-init: _sync_db_tools ## Initialises the default database structure (without any data). Use the DB_CONTAINER variable to override the destination docker container
	echo "Initialise the database"
	@make db-create-user
	echo "Insert the base structure"
	bash ./.chmod_and_call_in_docker.sh $(DB_CONTAINER_HOSTNAME) $(DB_CONTAINER_PORT) /var/local/tools/database/insert_base_structure.sh


.PHONY: deploy-load-uri-dump
deploy-load-uri-dump: _sync_db_tools db-drop ## Installs a full dump from the uri folder into the database for deployment purposes
	echo "Insert Uri Dump into the database"
	@make db-create-user
	bash ./.chmod_and_call_in_docker.sh $(DB_CONTAINER_HOSTNAME) $(DB_CONTAINER_PORT) /var/local/tools/database/insert_deploy_dump.sh


.PHONY: deploy-import
deploy-import: ## import the config for deployment
	@make -C db_admin/ importconfig-deployment
	@echo "Config successfully imported"


.PHONY: deploy-configure
deploy-configure: _classloader ## Generate the htacces for the stage server
	ENV='stage' make -C resources/configuration-templates/
	ENV='stage' make htaccess


.PHONY: deploy-pack
deploy-pack: deploy-configure ## make a zip containing all the necessary files
	find camac/application | grep -Pv $(ZIP_IGNORE_PATTERN) | zip -@ camac.zip
	find camac/configuration | grep -Pv $(ZIP_IGNORE_PATTERN) | zip -@ camac.zip
	find camac/library | grep -Pv $(ZIP_IGNORE_PATTERN) | zip -@ camac.zip
	find camac/public | grep -Pv $(ZIP_IGNORE_PATTERN) | zip -@ camac.zip
	find camac/resources | grep -Pv $(ZIP_IGNORE_PATTERN) | zip -@ camac.zip
	mkdir -p camac/cache/files
	mkdir -p camac/cache/metadata
	mkdir -p camac/uploads
	find camac/cache | grep -Pv $(ZIP_IGNORE_PATTERN) | zip -@ camac.zip
	find camac/uploads | grep -Pv $(ZIP_IGNORE_PATTERN) | zip -@ camac.zip
	# truncate the log file. We wanna provide it too to avoid
	# errors, but there's no need to have the logs included
	echo "" > camac/logs/application.log
	rm -r camac/logs/mails/* || true
	find camac/logs | grep -Pv $(ZIP_IGNORE_PATTERN) | zip -@ camac.zip
	rm -r camac/cache
	rm -r camac/uploads
	# revert back to normal config
	make _init


.PHONY: deploy-dump
deploy-dump: _sync_db_tools ## Make full dump of the database
	echo "Dumping the full database"
	bash ./.chmod_and_call_in_docker.sh $(DB_CONTAINER_HOSTNAME) $(DB_CONTAINER_PORT) /var/local/tools/database/export_deploy_dump.sh


.PHONY: structure-export
structure-export: ## Dumps the database structure. Use the DB_CONTAINER variable to override the destination docker container
	@chmod +x tools/camac/export-structure.sh
	@tools/camac/export-structure.sh $(DB_CONTAINER)


.PHONY: _classloader
_classloader: # Build the classmaps. These are important for performance
	@bash tools/camac/classmap_generator.sh


.PHONY: css
css: ## Create the css files from the sass files
	@cd camac/configuration/public/css/; make css


.PHONY: css-watch
css-watch: ## Watch the sass files and create the css when they change
	@cd camac/configuration/public/css/; make watch


.PHONY: run-live-db
run-live-db: ## This is merely a command to help run another docker instance of the database (to be able to perform deplyoments)
	@docker ps | grep docker_camac_live_db_1 || echo "You must run the live version of the Database"
	@docker exec -it docker_camac_live_db_1 chmod +x /var/local/tools/database/create_camac_user.sh
	@docker exec -it docker_camac_live_db_1 /var/local/tools/database/create_camac_user.sh
	@docker exec -it docker_camac_live_db_1 chmod +x /var/local/tools/database/insert_uri_dump.sh
	@docker exec -it docker_camac_live_db_1 chown -R oracle /var/local/database/
	@docker exec -it docker_camac_live_db_1 /var/local/tools/database/insert_uri_dump.sh


.PHONY: _deployment_confirmation
_deployment_confirmation:
	@echo "Configuration will be overridden on the server"
	@echo "Press ctrl-c to abort"
	@read ohyeah


.PHONY: deploy-test-server
deploy-test-server: _deployment_confirmation css _classloader ## Move the code onto the test server
	@git checkout test
	@git commit --allow-empty -m "Test-Server deployment"
	@ENV='test' make -C resources/configuration-templates/
	@ENV='test' make htaccess
	@rsync -Lavz camac/* sy-jump:/mnt/sshfs/root@camac.sycloud.ch/var/www/uri/ --exclude=*.log --exclude=db-config*.ini
	@ssh sy-jump "chown -R www-data /mnt/sshfs/root@camac.sycloud.ch/var/www/uri/logs"
	@scp tools/deploy/test-server-passwd sy-jump:/mnt/sshfs/root@camac.sycloud.ch/var/www/uri/passwd
	@cd db_admin/uri_database/ && USE_DB='test_server' python manage.py importconfig
	@ENV='dev' make -C resources/configuration-templates/


.PHONY: deploy-portal-test-server
deploy-portal-test-server:
	@rsync -avz iweb_mock/* sy-jump:/mnt/sshfs/root@camac.sycloud.ch/var/www/iweb/ --exclude=node_modules/*
	# TODO: npm install, forever restart. How to call a command on the server?


.PHONY: run-deploy-db
run-deploy-db: ## This is merely a command to help run another docker instance for deploying
	docker-compose -f docker/docker-deploy-db.yml up


.PHONY: config-export
config-export: ## export the current database configuration
	@make -C db_admin/ exportconfig
	@echo "Config successfully written"


.PHONY: config-import
config-import: ## import the current database configuration. This will override your existing stuff!
	@make -C db_admin/ importconfig
	@echo "Config successfully imported"
	@make clear-cache
	@echo "Cache cleared"


.PHONY: data-truncate
data-truncate: ## Truncate the data in the database
	@make -C db_admin/ truncatedata
	# @make -C db_admin/ reset_sequences # TODO
	@echo "Data sucessfully truncated"


.PHONY: config-shell
config-shell: ## start a database shell from the configuration management application
	@cd db_admin/uri_database/ && USE_DB='docker_dev' python manage.py shell


.PHONY: help
help: ## Show the help messages
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort -k 1,1 | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


.PHONY: run-acceptance-tests
run-acceptance-tests: ## run the acceptance tests
	@make -C db_admin/ run-acceptance-tests ${ARGS}


.PHONY: run-acceptance-tests-fast
run-acceptance-tests-fast: ## run the acceptance tests fast - meaning, don't runn quite every test
	@make -C db_admin/ run-acceptance-tests-fast ${ARGS}


.PHONY: ci-run-acceptance-tests
ci-run-acceptance-tests: ## Run a subset of the acceptance tests
	@mkdir -p camac/logs/mails
	@make -C db_admin/ run-acceptance-tests-ci


.PHONY: install-api-doc
install-api-doc: ## installs the api doc generator tool
	npm i -g apidoc


.PHONY: generate-api-doc
generate-api-doc: ## generates documentation for the i-web portal API
	apidoc -i kt_uri/configuration/Custom/modules/portal/controllers/ -o doc/
	@echo "Documentation was saved in /doc folder."


.PHONY: ci-config-import
ci-config-import:
	@make -C db_admin/  importconfig-ci
	@echo "config successfully imported"


.PHONY: ci-pretend
ci-pretend:
	@source /etc/profile
	@source /opt/xvfb.sh
	@pip install -r db_admin/requirements.txt
	@source /etc/apache2/envvars
	@python .wait-for-oracle-db.py oracle-eatmydata 1521
	@ssh-keyscan -H oracle-eatmydata > ~/.ssh/known_hosts
	@make _ci-init
	@make db-init DB_CONTAINER_HOSTNAME=oracle-eatmydata DB_CONTAINER_PORT=22
	@make ci-config-import
	@make ci-run-acceptance-tests


.PHONY: htaccess
htaccess:
	python resources/htaccess/make_htaccess.py ${ENV}


.PHONY: clear-cache ## Clear the memcache
clear-cache:
	bash .clear_cache.sh
