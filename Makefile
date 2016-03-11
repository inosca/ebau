SHELL:=/bin/bash

.PHONY: docs help up reset-db init-db watch fancy-up classloader dumper 

PHP_DEFINES=-d log_errors=1 -d display_errors=1 -d error_reporting=32767 -d display_startup_errors=1

DB_CONTAINER?=docker_camac_db_1

follow-log:
	@tail -f camac/logs/application.log

follow-syslog:
	@docker exec -it docker_camac_web_1 tail -f /var/log/apache2/error.log

fancy-up:
	tmux new-session -n 'camac runner' -d 'make up'
	tmux split-window -v 'make follow-log'
	tmux select-pane -U
	tmux select-pane -U
	tmux split-window -h 'make watch'
	tmux -2 attach-session -d

reset-db:
	@docker exec -it $(DB_CONTAINER) chmod +x /var/local/tools/database/drop_user.sh
	@docker exec -it $(DB_CONTAINER) /var/local/tools/database/drop_user.sh
	@make init-db

init-db:
	@docker exec -it $(DB_CONTAINER) chmod +x /var/local/tools/database/create_camac_user.sh
	@docker exec -it $(DB_CONTAINER) /var/local/tools/database/create_camac_user.sh
	@docker exec -it $(DB_CONTAINER) chmod +x /var/local/tools/database/insert_base_structure.sh
	@docker exec -it $(DB_CONTAINER) /var/local/tools/database/insert_base_structure.sh

classloader:
	@docker exec -it docker_camac_web_1 php -c /var/local/tools/zend/php_cli.ini /var/local/tools/zend/classmap_generator.php -w -l  /var/www/html/application/ -o /var/www/html/application/class_map.php
	@docker exec -it docker_camac_web_1 php -c /var/local/tools/zend/php_cli.ini /var/local/tools/zend/classmap_generator.php -w -l  /var/www/html/configuration/ -o /var/www/html/configuration/class_map.php
	@docker exec -it docker_camac_web_1 php -c /var/local/tools/zend/php_cli.ini /var/local/tools/zend/classmap_generator.php -w -l  /var/www/html/library/ -o /var/www/html/library/class_map.php

up:
	@chmod o+w camac/logs
	@chmod o+w camac/configuration/upload
	@docker-compose -f docker/docker-compose.yml up

init: up init-db
	@docker exec -it docker_camac_web_1 chown -R www-data /var/www/html/logs /var/www/html/cache

css:
	@cd camac/configuration/public/css/; make css

watch:
	@cd camac/configuration/public/css/; make watch

log:
	@echo "TODO"
	@exit 3 
	@tmux new-session -n camac-log -d 'tail -f camac/logs/application.log'
	@tmux split-window -v 'vagrant ssh -c "sudo tail -f /var/log/apache2/vagrant-error.log"'
	@tmux -2 attach-session -d

build: classloader
	echo "Not implemented yet"

init-live-db:
	@docker ps | grep docker_camac_live_db_1 || echo "You must run the live version of the Database"
	@docker exec -it docker_camac_live_db_1 chmod +x /var/local/tools/database/create_camac_user.sh
	@docker exec -it docker_camac_live_db_1 /var/local/tools/database/create_camac_user.sh
	@docker exec -it docker_camac_live_db_1 chmod +x /var/local/tools/database/insert_uri_dump.sh
	@docker exec -it docker_camac_live_db_1 chown -R oracle /var/local/database/
	@docker exec -it docker_camac_live_db_1 /var/local/tools/database/insert_uri_dump.sh

export-structure: 
	@docker exec -it $(DB_CONTAINER) chown -R oracle /var/local/database/
	@docker exec -it $(DB_CONTAINER) /var/local/tools/database/export_structure.sh
