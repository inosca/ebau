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


.PHONY: _base-init
_base-init: _submodule-update
	@rm -f camac/configuration
	@ln -fs ../kt_uri/configuration camac/configuration
	ln -sf "../../kt_uri/configuration/public" "camac/public/"
	for i in `ls kt_uri/library/`; do rm -f "camac/library/$$i"; done
	for i in `ls kt_uri/library/`; do ln -sf "../../kt_uri/library/$$i" "camac/library/$$i"; done
	@mkdir -p camac/logs/mails
	@chmod -R o+w camac/logs
	@chmod o+w camac/configuration/upload
	@make _classloader

.PHONY: _submodule-update
_submodule-update:
	git submodule update --init --recursive || true
	touch camac/logs/application.log
	chmod 777 -R camac/logs || true

.PHONY: install
install: ## Install required files (jQuey, etc via NPM)
	npm install --prefix ./kt_uri/configuration/public

.PHONY: js
js:
	npm run build --prefix ./kt_uri/configuration/public

.PHONY: js-watch
js-watch:
	npm run watch --prefix ./kt_uri/configuration/public

.PHONY: run
run-ur: _base-init ## Runs the docker containers
	@docker-compose -f docker/docker-compose-ur.yml up -d

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


.PHONY: _deploy-pack
_deploy-pack: ## make a zip containing all the necessary files
	# apparently zip cannot resolve the symlinks
	# therefore we have to copy the stuff there and remove it afterwards...
	# I would use tar, but I'm pretty sure the guys at Uri can't handle tar
	@rm -r camac/configuration
	@rm -r camac/public/public
	@rm -rf camac/library/fpdf
	@rm -rf camac/library/fpdi
	@rm -rf camac/library/tbs
	@cp -r kt_uri/configuration camac/
	@cp -r kt_uri/configuration/public camac/public/public
	@cp -r kt_uri/library/fpdi camac/library/
	@cp -r kt_uri/library/fpdf camac/library/
	@cp -r kt_uri/library/tbs camac/library/
	@find camac/application | grep -Pv $(ZIP_IGNORE_PATTERN) | zip -@ camac.zip
	@find camac/configuration | grep -Pv $(ZIP_IGNORE_PATTERN) | zip -@ camac.zip
	@find camac/library | grep -Pv $(ZIP_IGNORE_PATTERN) | zip -@ camac.zip
	@find camac/public | grep -Pv $(ZIP_IGNORE_PATTERN) | zip -@ camac.zip
	@find camac/resources | grep -Pv $(ZIP_IGNORE_PATTERN) | zip -@ camac.zip
	@mkdir -p camac/cache/files
	@mkdir -p camac/cache/metadata
	@mkdir -p camac/uploads
	@mkdir -p camac/tmp
	@find camac/cache | grep -Pv $(ZIP_IGNORE_PATTERN) | zip -@ camac.zip
	@find camac/uploads | grep -Pv $(ZIP_IGNORE_PATTERN) | zip -@ camac.zip
	@zip camac.zip camac/tmp
	# truncate the log file. We wanna provide it too to avoid
	# errors, but there's no need to have the logs included
	@echo "" > camac/logs/application.log
	@rm -r camac/logs/mails/* || true
	@find camac/logs | grep -Pv $(ZIP_IGNORE_PATTERN) | zip -@ camac.zip
	@rm -r camac/cache
	@rm -r camac/uploads
	@rm -r camac/configuration
	@rm -r camac/public/public
	@rm -r camac/library/fpdi
	@rm -r camac/library/fpdf
	@rm -r camac/library/tbs
	@rmdir camac/tmp
	# revert back to normal config
	@make _init


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
	@echo "Press ENTER to continue or ctrl-c to abort"
	@read ohyeah


.PHONY: deploy-test-server
deploy-test-server: _deployment_confirmation css _classloader ## Move the code onto the test server
	@rsync -Lavz camac/ sy-jump:/mnt/ssh/root@vm-camac-webapp-stage-01.cust.adfinis-sygroup.ch/var/www/camac5.src/camac/ --exclude=*.log --exclude=db-config*.ini --exclude=node_modules/ --modify-window=1
	@ssh sy-jump "chown -R www-data /mnt/ssh/root@vm-camac-webapp-stage-01.cust.adfinis-sygroup.ch/var/www/camac5.src/camac/logs"
	@cd db_admin/uri_database/ && python manage.py importconfig --database=test_server


.PHONY: deploy-portal-test-server
deploy-portal-test-server:
	@rsync -avz iweb_mock/* sy-jump:/mnt/ssh/root@vm-camac-webapp-stage-01.cust.adfinis-sygroup.ch/var/www/camac5.src/iweb_mock/ --exclude=node_modules/
	# TODO: npm install, forever restart. How to call a command on the server?


.PHONY: run-deploy-db
run-deploy-db: ## This is merely a command to help run another docker instance for deploying
	docker-compose -f docker/docker-deploy-db.yml up

.PHONY: data-truncate
data-truncate: ## Truncate the data in the database
	@make -C db_admin/ truncatedata
	# @make -C db_admin/ reset_sequences # TODO
	@echo "Data sucessfully truncated"


.PHONY: help
help: ## Show the help messages
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort -k 1,1 | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


.PHONY: run-acceptance-tests
run-acceptance-tests: ## run the acceptance tests
	@make -C db_admin/ run-acceptance-tests ARGS="${ARGS}"


.PHONY: install-api-doc
install-api-doc: ## installs the api doc generator tool
	npm i -g apidoc


.PHONY: generate-api-doc
generate-api-doc: ## generates documentation for the i-web portal API
	apidoc -i kt_uri/configuration/Custom/modules/portal/controllers/ -o doc/
	@echo "Documentation was saved in /doc folder."


.PHONY: ci-pretend
ci-pretend:
	@source /etc/profile
	@source /opt/xvfb.sh
	@pip install -r db_admin/requirements.txt
	@source /etc/apache2/envvars
	@python .wait-for-oracle-db.py oracle-eatmydata 1521
	@ssh-keyscan -H oracle-eatmydata > ~/.ssh/known_hosts
	@make _base-init _install
	@make db-init DB_CONTAINER_HOSTNAME=oracle-eatmydata DB_CONTAINER_PORT=22
	@make ci-config-import
	@make ci-run-acceptance-tests


.PHONY: clear-cache ## Clear the memcache
clear-cache:
	bash .clear_cache.sh
