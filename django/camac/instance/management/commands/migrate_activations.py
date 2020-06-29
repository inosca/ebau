"""
Migrates and Service and all active Activations into an existing or a new Circulation.

This is used to move some existing services of the type "Unter-Fachstelle" into a new
parent "Fachstelle" service.

This was written for the 1. Jul 2020 migration of Fachstellen for Kanton Schwyz.
"""
from datetime import datetime, timedelta

from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from django.utils import timezone

from camac.core.models import Activation, Circulation, CirculationState
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
            type=int,
            dest="instance_resource_for_new_circulations",
            default=39,
        )
        parser.add_argument(
            "--instance-resource-for-new-circulations-bgz",
            type=int,
            dest="instance_resource_for_new_circulations_bgz",
            default=18,
        )

    def _get_service(self, service_id):
        if service_id == 0:
            return None

        return Service.objects.get(pk=service_id)

    def _is_circulation_active(self, circulation):
        return (
            Activation.objects.filter(
                circulation=circulation,
                circulation_state__in=self._active_circulation_states,
            ).count()
            > 0
        )

    def _create_new_circulation(self, instance, service, instance_resource_id):
        circulation_name = "Zirkulation vom %s" % (
            datetime.today().strftime("%d.%m.%Y %H:%M")
        )
        circulation = Circulation(
            name=circulation_name,
            instance=instance,
            service=service,
            instance_resource_id=instance_resource_id,
        )
        circulation.save()
        self.stdout.write(
            "New circulation '%s: %s (%s)'"
            % (circulation.circulation_id, circulation.service, circulation.name)
        )

        return circulation

    def _update_activation(self, activation, parent):  # noqa: C901
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

        current_instance = activation.circulation.instance

        # Get current circulation for sanity check
        current_circulation = Circulation.objects.filter(
            service=activation.service_parent, instance=current_instance
        ).latest("circulation_id")
        if activation.circulation != current_circulation:
            self.stdout.write("Old activation %s, skip!" % activation.activation_id)
            return

        if activation.service_parent != parent:
            if parent is None:
                activation.service_parent = self._bgz_service
            else:
                activation.service_parent = parent
            changed = True
        if activation.circulation.service != activation.service_parent:
            circulation = None
            circulation_is_active = False
            try:
                circulation = Circulation.objects.filter(
                    service=activation.service_parent, instance=current_instance
                ).latest("circulation_id")

                circulation_is_active = self._is_circulation_active(circulation)
            except ObjectDoesNotExist:
                pass

            if not circulation_is_active:
                circulation = self._create_new_circulation(
                    current_instance,
                    activation.service_parent,
                    self._instance_resource_id,
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

        if parent is not None:
            self._create_bgz_circulation(current_instance, parent)

    def _create_bgz_circulation(self, current_instance, target_service):
        self.stdout.write("Checking for BGZ Ciculation")
        bgz_circulation = None
        bgz_circulation_is_active = False
        try:
            bgz_circulation = Circulation.objects.filter(
                service=self._bgz_service, instance=current_instance
            ).latest("circulation_id")
            bgz_circulation_is_active = self._is_circulation_active(bgz_circulation)
        except ObjectDoesNotExist:
            pass

        if not bgz_circulation_is_active:
            bgz_circulation = self._create_new_circulation(
                current_instance, self._bgz_service, self._bgz_instance_resource_id
            )

        bgz_activation = None
        try:
            bgz_activation = Activation.objects.get(
                service_parent=self._bgz_service,
                service=target_service,
                circulation=bgz_circulation,
            )
        except ObjectDoesNotExist:
            pass

        if bgz_activation is None:
            bgz_activation = Activation(
                circulation=bgz_circulation,
                service=target_service,
                service_parent=self._bgz_service,
                circulation_state=CirculationState.objects.get(circulation_state_id=1),
                start_date=timezone.now().replace(microsecond=0),
                deadline_date=timezone.now().replace(microsecond=0)
                + timedelta(days=28),
                version=1,
            )
            bgz_activation.save()
            self.stdout.write(
                "Created BGZ Activation '%s' for Circulation '%s: %s (%s)'"
                % (
                    bgz_activation,
                    bgz_circulation.circulation_id,
                    bgz_circulation.service,
                    bgz_circulation.name,
                )
            )

    def handle(self, *args, **options):
        self._active_circulation_states = CirculationState.objects.exclude(
            name__in=["OK", "DONE"]
        )
        self._instance_resource_id = options["instance_resource_for_new_circulations"]
        self._bgz_instance_resource_id = options[
            "instance_resource_for_new_circulations_bgz"
        ]
        self.stdout.write("Starting migration...")
        self._bgz_service = self._get_service(service_id=options["bgz_id"])
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
            service=service, circulation_state__in=self._active_circulation_states
        )
        self.stdout.write("Found %s activations for '%s'" % (len(activations), service))

        for activation in activations:
            self._update_activation(activation, parent)
