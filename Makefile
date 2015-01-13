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
