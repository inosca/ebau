SHELL:=/bin/bash

.PHONY: docs cleanup help up

up:
	@echo "( The vagrant box needs vagrant 1.2.3 or later please download from )"
	@echo "( http://downloads.vagrantup.com                                    )"
	tools/vagrant/if_get_box
	vagrant up --provision

halt:
	vagrant halt

bye:
	vagrant suspend

destroy:
	vagrant destroy -f

dup: destroy up

hup: halt up
