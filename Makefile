SHELL:=/bin/bash

.PHONY: docs help up reset-db init-db watch fancy-up classloader dumper init export-structure

.DEFAULT_GOAL := help

PHP_DEFINES=-d log_errors=1 -d display_errors=1 -d error_reporting=32767 -d display_startup_errors=1

DB_CONTAINER?=docker_camac_db_1


follow-log: ## Tail the log of the application
	@tail -f camac/logs/application.log


fancy-up: ## Create a tmux session that runs several useful commands at once: make up, make follow-log and make watch
	@tmux new-session -n 'camac runner' -d 'make up'
	@tmux split-window -v 'make follow-log' # split vertically
	@tmux select-pane -U # go one pane upwards
	@tmux select-pane -U # go one pane upwards
	@tmux split-window -h 'make watch' # split horizontally on the most upper pane

	@tmux -2 attach-session -d

init: ## Initialise the code, create the necessary symlinks
	@rm camac/configuration/configs/application.ini
	@ln -rs camac/configuration/configs/application-dev.ini \
		camac/configuration/configs/application.ini
	@rm -f camac/configuration
	@ln -rfs kt_uri/configuration camac/configuration
	@for i in `ls kt_uri/library/`; do rm -f "camac/library/$$i"; done
	@for i in `ls kt_uri/library/`; do ln -rsf "kt_uri/library/$$i" "camac/library/$$i"; done
	@chmod o+w camac/logs
	@chmod o+w camac/configuration/upload


up: init classloader ## Runs the docker containers
	@docker-compose -f docker/docker-compose.yml up


reset-db: ## Drops the database and re-initialises it. Use the DB_CONTAINER variable to override the destination docker container
	@docker exec -it $(DB_CONTAINER) chmod +x /var/local/tools/database/drop_user.sh
	@docker exec -it $(DB_CONTAINER) /var/local/tools/database/drop_user.sh
	@make init-db


init-db: ## Initialises the default database structure (without any data). Use the DB_CONTAINER variable to override the destination docker container
	@docker exec -it $(DB_CONTAINER) chmod +x /var/local/tools/database/create_camac_user.sh
	@docker exec -it $(DB_CONTAINER) /var/local/tools/database/create_camac_user.sh
	@docker exec -it $(DB_CONTAINER) chmod +x /var/local/tools/database/insert_base_structure.sh
	@docker exec -it $(DB_CONTAINER) /var/local/tools/database/insert_base_structure.sh


export-structure: ## Dumps the database structure. Use the DB_CONTAINER variable to override the destination docker container
	@chmod +x tools/camac/export-structure.sh 
	@tools/camac/export-structure.sh $(DB_CONTAINER)


classloader: ## Build the classmaps. These are important for performance
	@# for some reason, i have to append || true here. The command returns non zero
	@docker exec -it docker_camac_web_1 php -c /var/local/tools/zend/php_cli.ini /var/local/tools/zend/classmap_generator.php -w -l  /var/www/html/application/ -o /var/www/html/application/class_map.php || true
	@docker exec -it docker_camac_web_1 php -c /var/local/tools/zend/php_cli.ini /var/local/tools/zend/classmap_generator.php -w -l  /var/www/html/configuration/ -o /var/www/html/configuration/class_map.php || true
	@docker exec -it docker_camac_web_1 php -c /var/local/tools/zend/php_cli.ini /var/local/tools/zend/classmap_generator.php -w -l  /var/www/html/library/ -o /var/www/html/library/class_map.php || true


css: ## Create the css files from the sass files
	@cd camac/configuration/public/css/; make css


watch: ## Watch the sass files and create the css when they change
	@cd camac/configuration/public/css/; make watch


init-live-db: ## This is merely a command to help run another docker instance of the database (to be able to perform deplyoments)
	@docker ps | grep docker_camac_live_db_1 || echo "You must run the live version of the Database"
	@docker exec -it docker_camac_live_db_1 chmod +x /var/local/tools/database/create_camac_user.sh
	@docker exec -it docker_camac_live_db_1 /var/local/tools/database/create_camac_user.sh
	@docker exec -it docker_camac_live_db_1 chmod +x /var/local/tools/database/insert_uri_dump.sh
	@docker exec -it docker_camac_live_db_1 chown -R oracle /var/local/database/
	@docker exec -it docker_camac_live_db_1 /var/local/tools/database/insert_uri_dump.sh


deploy-test-server: css classloader ## Move the code onto the test server
	@rsync -Lavz camac/* sy-jump:/mnt/sshfs/root@camac.sycloud.ch/var/www/uri/ --exclude=*.log
	@ssh sy-jump "rm /mnt/sshfs/root@camac.sycloud.ch/var/www/uri/configuration/configs/application.ini"
	@ssh sy-jump "cd /mnt/sshfs/root@camac.sycloud.ch/var/www/uri/configuration/configs/; ln -s application-testserver.ini application.ini"
	@ssh sy-jump "chown -R www-data /mnt/sshfs/root@camac.sycloud.ch/var/www/uri/logs"
	@scp tools/deploy/test-server-htaccess sy-jump:/mnt/sshfs/root@camac.sycloud.ch/var/www/uri/public/.htaccess
	@scp tools/deploy/test-server-passwd sy-jump:/mnt/sshfs/root@camac.sycloud.ch/var/www/uri/passwd


start-deploy-db: ## This is merely a command to help run another docker instance for deploying
	docker-compose -f docker/docker-deploy-db.yml up


help: ## Show the help messages
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
