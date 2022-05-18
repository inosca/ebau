from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Value
from django.db.models.functions import Replace

from camac.core.models import Activation
from camac.document.models import Attachment
from camac.user.models import Group, Service, ServiceGroup, User, UserGroup


class Command(BaseCommand):
    help = "Merge the 'Gemeinderäte externe Pendenzen' and 'Gemeinderäte interne Pendenzen' together"

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry",
            dest="dry",
            action="store_true",
            default=False,
        )

    @transaction.atomic
    def handle(self, *args, **options):
        sid = transaction.savepoint()

        # Rename services "Gemeinderat externe Pendenz"
        Service.objects.filter(name__contains="externe Pendenz").update(
            name=Replace("name", Value("externe Pendenz"), Value("Pendenzen")),
            description=Replace(
                "description", Value("externe Pendenz"), Value("Pendenzen")
            ),
        )

        # Rename service group "Gemeinderat externe Pendenzen"
        ServiceGroup.objects.filter(name__contains="externe Pendenzen").update(
            name=Replace("name", Value("externe Pendenzen"), Value("Pendenzen"))
        )

        # Rename groups "Gemeinderat extern"
        Group.objects.filter(name__contains="externe Pendenz").update(
            name=Replace("name", Value("externe Pendenz"), Value("Pendenzen"))
        )

        # Assign users with group "Gemeinderat externe Pendenz" to new group
        users = User.objects.filter(groups__name__contains="interne Pendenz")

        for user in users:
            for group in user.groups.filter(name__contains="interne Pendenz"):
                new_group = Group.objects.get(
                    name__contains=f"{' '.join(group.name.split(' ', 2)[:2])} Pendenzen"
                )

                if not user.groups.filter(group_id=new_group.pk).exists():
                    user.groups.through.objects.filter(user=user, group=group).update(
                        group_id=new_group.pk
                    )

        # Assign all existing activations with service intern to new service
        services_intern = Service.objects.filter(name__contains="interne Pendenz")
        self._assign_new_service(services_intern, Activation)

        # Assign all existing attachments with service intern to new service
        self._assign_new_service(services_intern, Attachment)

        # Delete attachments with service "Gemeinderat interne Pendenz"
        Attachment.objects.filter(service__in=services_intern).delete()

        # Delete services "Gemeinderat interne Pendenz"
        services_intern.delete()

        # Delete service group "Gemeinderat interne Pendenzen"
        ServiceGroup.objects.filter(name__contains="interne Pendenzen").delete()

        # Delete groups "Gemeinderat interne Pendenz"
        Group.objects.filter(name__contains="interne Pendenz").delete()

        # Delete user group "Gemeinderat interne Pendenz"
        UserGroup.objects.filter(group__name__contains="interne Pendenz").delete()

        if options["dry"]:  # pragma: no cover
            transaction.savepoint_rollback(sid)
        else:
            transaction.savepoint_commit(sid)

    def _assign_new_service(self, services, model):
        objects_with_old_service = model.objects.filter(service__in=services)
        for obj in objects_with_old_service:
            obj.service_id = Service.objects.get(
                name__contains=f"{' '.join(obj.service.name.split(' ', 2)[:2])} Pendenzen"
            ).pk
            obj.save()
