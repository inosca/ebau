"""
Migrates and Service and all active Activations into an existing or a new Circulation.

This is used to move some existing services of the type "Unter-Fachstelle" into a new
parent "Fachstelle" service.

This was written for the 1. Jul 2020 migration of Fachstellen for Kanton Schwyz.
"""
from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand

from camac.core.models import (
    Activation,
    Circulation,
    CirculationState,
    InstanceResource,
)
from camac.user.models import Service


class Command(BaseCommand):
    help = "Migrate service to a new parent and ensure that all unclosed activations follow."

    def add_arguments(self, parser):
        parser.add_argument(
            "--bgz-id",
            type=int,
            dest="bgz_id",
            help="Id of the Baugesuchszentrale (BGZ), default: 7",
            default=7,  # Baugesuchszentrale
        )
        parser.add_argument(
            "--old-service-id",
            type=int,
            dest="old_id",
            help="old service ID",
            default=99,  # ANJF (Fischerei)
            # default=98,  # ANJF (Jagd)
            # default=97,  # ANJF (Natur- und Landschaftsschutz)
        )
        parser.add_argument(
            "--new-service-parent",
            type=int,
            dest="new_parent",
            help="ID of new parent Service",
            default=13,  # Amt für Umweltschutz
        )
        parser.add_argument(
            "--instance-resource-for-new-circulations",
            type=str,
            dest="instance_resource_for_new_circulations",
            default="Zirkulation BGZ",
        )

    def _get_service(self, service_id):
        return Service.objects.get(pk=service_id)

    def _update_activation(self, activation, parent):
        changed = False
        self.stdout.write(
            "Activation '%s' belongs to '%s' issued by '%s'"
            % (activation.activation_id, activation.service, activation.service_parent)
        )
        self.stdout.write(
            "Activation '%s' has circulation '%s: %s'"
            % (
                activation.activation_id,
                activation.circulation,
                activation.circulation.service,
            )
        )
        if activation.service_parent != parent:
            activation.service_parent = parent
            changed = True
        if activation.circulation.service != activation.service_parent:
            current_instance = activation.circulation.instance

            circulation = None
            circulation_is_active = False
            try:
                circulation = Circulation.objects.filter(
                    service=activation.service_parent, instance=current_instance
                ).latest("circulation_id")
                circulation_is_active = (
                    Activation.objects.filter(circulation=circulation).count() > 0
                )
            except ObjectDoesNotExist:
                pass

            if not circulation_is_active:
                circulation_name = "Zirkulation vom %s" % (
                    datetime.today().strftime("%d.%m.%Y %H:%M")
                )
                circulation = Circulation(
                    name=circulation_name,
                    instance=current_instance,
                    service=activation.service_parent,
                    instance_resource_id=self._instance_resource_id,
                )
                circulation.save()
                self.stdout.write(
                    "New circulation '%s: %s (%s)'"
                    % (
                        circulation.circulation_id,
                        circulation.service,
                        circulation.name,
                    )
                )

            self.stdout.write(
                "Using circulation '%s: %s (%s)'"
                % (circulation.circulation_id, circulation.service, circulation.name)
            )

            if activation.circulation != circulation:
                activation.circulation = circulation
                changed = True

        if changed:
            activation.save()
            self.stdout.write(
                self.style.SUCCESS(
                    "Activation '%s' moved to Service '%s' and Circulation '%s: %s' "
                    % (
                        activation,
                        activation.service_parent,
                        activation.circulation,
                        activation.circulation.service,
                    )
                )
            )

    def handle(self, *args, **options):
        self._circulation_states = CirculationState.objects.exclude(
            name__in=["OK", "DONE"]
        )
        self._instance_resource_id = InstanceResource.objects.get(
            name=options["instance_resource_for_new_circulations"]
        ).instance_resource_id
        self.stdout.write("Starting migration...")
        service = self._get_service(service_id=options["old_id"])
        parent = self._get_service(service_id=options["new_parent"])
        old_parent = service.service_parent
        if service.service_parent != parent:
            service.service_parent = parent
            service.save()
            self.stdout.write(
                self.style.SUCCESS(
                    "Sucessfully moved '%s' from '%s' to '%s'"
                    % (service, old_parent, parent)
                )
            )

        activations = Activation.objects.filter(
            service=service, circulation_state__in=self._circulation_states
        )
        self.stdout.write("Found %s activations for '%s'" % (len(activations), service))

        for activation in activations:
            self._update_activation(activation, parent)
