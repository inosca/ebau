SHELL:=/bin/bash

.PHONY: docs help up reset-db init-db watch fancy-up classloader dumper 

PHP_DEFINES=-d log_errors=1 -d display_errors=1 -d error_reporting=32767 -d display_startup_errors=1

fancy-up:
	tmux new-session -n 'camac runner' -d 'make up'
	tmux split-window -v 'make watch'
	tmux split-window -v 'tail -f camac/logs/application.log'
	tmux -2 attach-session -d

reset-db:
	docker cp docker/db docker_camac_db_1:/usr/local/src
	docker exec -it docker_camac_db_1 chmod +x /usr/local/src/db/drop_user.sh
	docker exec -it docker_camac_db_1 /usr/local/src/db/drop_user.sh
	#make init-db

init-db:
	docker cp docker/db docker_camac_db_1:/usr/local/src/
	docker exec -it docker_camac_db_1 chmod +x /usr/local/src/db/init_db.sh
	docker exec -it docker_camac_db_1 /usr/local/src/db/init_db.sh

classloader:
	docker exec -it docker_camac_web_1 php -c /usr/src/tools/zend/php_cli.ini /usr/src/tools/zend/classmap_generator.php -w -l  /var/www/html/application/ -o /var/www/html/application/class_map.php
	docker exec -it docker_camac_web_1 php -c /usr/src/tools/zend/php_cli.ini /usr/src/tools/zend/classmap_generator.php -w -l  /var/www/html/configuration/ -o /var/www/html/configuration/class_map.php
	docker exec -it docker_camac_web_1 php -c /usr/src/tools/zend/php_cli.ini /usr/src/tools/zend/classmap_generator.php -w -l  /var/www/html/library/ -o /var/www/html/library/class_map.php

up:
	chmod o+w camac/logs
	docker-compose -f docker/docker-compose.yml up

init: up init-db
	docker exec -it docker_camac_web_1 chown -R www-data /var/www/html/logs /var/www/html/cache

css:
	@cd camac/configuration/public/css/; make css

watch:
	@cd camac/configuration/public/css/; make watch

log:
	echo "TODO"
	exit 3 
	tmux new-session -n camac-log -d 'tail -f camac/logs/application.log'
	tmux split-window -v 'vagrant ssh -c "sudo tail -f /var/log/apache2/vagrant-error.log"'
	tmux -2 attach-session -d

dumper:
	@docker cp tools/camac/ docker_camac_web_1:/var/local/
	@docker exec -it docker_camac_web_1 php $(PHP_DEFINES) /var/local/camac/dumper.php

build: classloader
	echo "Not implemented yet"

init_live_db:
	@docker ps | grep docker_camac_live_db_1 || echo "You must run the live version of the Database"
	docker cp -L database/ docker_camac_live_db_1:/var/local/
	docker exec -it docker_camac_live_db_1 chmod +x /var/local/database/create_camac_user.sh
	docker exec -it docker_camac_live_db_1 /var/local/database/create_camac_user.sh
	docker exec -it docker_camac_live_db_1 chmod +x /var/local/database/uri_dumps/insert.sh
	docker exec -it docker_camac_live_db_1 chown -R oracle /var/local/database/
	docker exec -it docker_camac_live_db_1 /var/local/database/uri_dumps/insert.sh
