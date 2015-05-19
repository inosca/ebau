SHELL:=/bin/bash

.PHONY: docs cleanup help up

up:
	@echo "( The vagrant box needs vagrant 1.2.3 or later please download from )"
	@echo "( http://downloads.vagrantup.com                                    )"
	tools/vagrant/get_software
	vagrant up --provision

halt:
	vagrant halt

bye:
	vagrant suspend

destroy:
	vagrant destroy -f

dup: destroy up

hup: halt up

css:
	@cd camac/configuration/public/css/; make css

watch:
	@cd camac/configuration/public/css/; make watch

log:
	tmux new-session -n camac-log -d 'tail -f camac/logs/application.log'
	tmux split-window -v 'vagrant ssh -c "sudo tail -f /var/log/apache2/vagrant-error.log"'
	tmux -2 attach-session -d
