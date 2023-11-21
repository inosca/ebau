import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from camac.core.models import InstanceResource, IrRoleAcl
from camac.instance.models import InstanceState
from camac.user.models import Role
from camac.utils import clean_join


class Command(BaseCommand):
    help = "Assign instance resource ACLs"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.filename = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            f"acls/{settings.APPLICATION_NAME}.json",
        )

    def add_arguments(self, parser):
        parser.add_argument("-d", "--dump", dest="dump", action="store_true")

    def handle(self, *app_labels, **options):
        if options.get("dump"):
            self.dump()
        else:
            self.assign()

    def dump(self):
        data = {}

        for ir in InstanceResource.objects.all().order_by("pk"):
            acls = {}

            for role in ir.role_acls.values_list("role__name", flat=True).order_by(
                "role__name"
            ):
                acls[role] = list(
                    ir.role_acls.filter(role__name=role)
                    .order_by("instance_state__name")
                    .values_list("instance_state__name", flat=True)
                )

            resource_description = ir.resource.get_trans_attr("description")
            label = clean_join(
                clean_join(
                    ir.resource.get_name(),
                    f"({resource_description})" if resource_description else None,
                ),
                ir.get_name(),
                separator=" > ",
            )

            data[ir.pk] = {
                "label": label,
                "acls": acls,
            }

        with open(self.filename, "w") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)

    def assign(self):
        with open(self.filename, "r") as file:
            data = json.load(file)

            for ir_pk, config in data.items():
                instance_resource = InstanceResource.objects.get(pk=ir_pk)

                for role_name, instance_states in config["acls"].items():
                    role = Role.objects.get(name=role_name)

                    for instance_state_name in instance_states:
                        instance_state = InstanceState.objects.get(
                            name=instance_state_name
                        )

                        _, created = IrRoleAcl.objects.get_or_create(
                            instance_resource=instance_resource,
                            role=role,
                            instance_state=instance_state,
                        )

                        if created:
                            self.stdout.write(
                                self.style.SUCCESS(
                                    f"New ACL: {role_name}, {instance_state_name} on IR {instance_resource.get_name()}"
                                )
                            )
