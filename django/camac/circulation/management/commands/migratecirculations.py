from django.core.management.base import BaseCommand
from django.db import transaction

from camac.core.models import Circulation


class Command(BaseCommand):
    help = """
    Migrate "old" single circulations to new multicirculations.
    """

    @transaction.atomic
    def handle(self, *args, **options):
        circulations = Circulation.objects.filter(service=None)

        for circulation in circulations:
            created_circulations = {}
            activations = circulation.activations.all()
            for activation in activations:
                service_parent_id = activation.service_parent.pk

                if service_parent_id not in created_circulations:
                    name = "Zirkulation vom {0}".format(
                        activation.start_date.strftime("%d.%m.%Y %H:%M")
                    )
                    new_circulation = Circulation.objects.create(
                        instance_resource_id=circulation.instance_resource_id,
                        instance=circulation.instance,
                        service=activation.service_parent,
                        name=name,
                    )
                    created_circulations[service_parent_id] = new_circulation
                    print(
                        "Create new circulation {0} from old circulation {1}".format(
                            new_circulation.pk, circulation.pk
                        )
                    )

                # assign activation to new circulation
                print(
                    "Assign activation {0} to circulation {1}".format(
                        activation.pk, created_circulations[service_parent_id].pk
                    )
                )
                activation.circulation = created_circulations[service_parent_id]
                activation.save()

        print("done")
