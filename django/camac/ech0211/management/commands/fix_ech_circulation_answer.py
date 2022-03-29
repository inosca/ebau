from caluma.caluma_user.models import AnonymousUser
from caluma.caluma_workflow.models import WorkItem
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Count

from camac.caluma.api import CalumaApi
from camac.core.models import Activation, Circulation, CirculationAnswer
from camac.instance.models import Instance


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "-d", "--dry", action="store_true", help="Dry run only, no changes"
        )

    @transaction.atomic
    def handle(self, *args, **options):
        sid = transaction.savepoint()

        activations = Activation.objects.annotate(
            notice_count=Count("notices__pk")
        ).filter(
            circulation_state__name="DONE",
            circulation_answer__isnull=True,
            notice_count__gte=2,
        )
        activation_ids = list(activations.values_list("pk", flat=True))
        circulation_ids = list(activations.values_list("circulation__pk", flat=True))

        # update activations to have status unknown
        activations.update(
            circulation_answer=CirculationAnswer.objects.get(name="unknown")
        )

        # fix work item status
        WorkItem.objects.filter(
            **{
                "status": WorkItem.STATUS_CANCELED,
                "meta__activation-id__in": activation_ids,
            }
        ).update(status=WorkItem.STATUS_COMPLETED)
        self.stdout.write(
            f"Updated answer to unknown for {len(activation_ids)} eCH activations and fixed their work item status"
        )

        api = CalumaApi()
        user = AnonymousUser()

        # fix affected circulations
        affected_circulations = Circulation.objects.filter(pk__in=circulation_ids)
        for circulation in affected_circulations:
            api.sync_circulation(circulation, user)

        self.stdout.write("Fixed circulations for instances:")
        for instance_id in sorted(
            affected_circulations.values_list("instance", flat=True)
        ):
            instance = Instance.objects.get(pk=instance_id)
            self.stdout.write(
                f"- {instance_id}, {instance.instance_state.get_name()}, {instance.responsible_service().get_name()}"
            )

        if options["dry"]:
            transaction.savepoint_rollback(sid)
        else:
            transaction.savepoint_commit(sid)
