SHELL:=/bin/bash

DB_SCRIPT=docker/db/init_db.sh

.PHONY: docs cleanup help up

reset-db:
	echo "TODO"
	exit 2

init-db:
	docker cp docker/db/ docker_db_1:/usr/local/src/
	docker exec -it docker_db_1 chmod +x /usr/local/src/${DB_SCRIPT}
	docker exec -it docker_db_1 /usr/local/src/${DB_SCRIPT}

up:
	docker-compose -f docker/docker-compose.yml up

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
