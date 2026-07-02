from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Q

from camac.instance.models import Instance


class Command(BaseCommand):
    help = """Change the context key  'isDecision' to 'isDecisionOereb' for attachments of ÖREB dossiers."""

    def add_arguments(self, parser):
        parser.add_argument(
            "--commit", dest="commit", action="store_true", default=False
        )

    @transaction.atomic
    def handle(self, *args, **options):
        sid = transaction.savepoint()

        instances = Instance.objects.filter(
            Q(case__document__form_id="oereb")
            | Q(case__document__form_id="oereb-verfahren-gemeinde")
        )
        counter = 0
        for instance in instances:
            is_decision_oereb_attachments = instance.attachments.filter(
                context__isDecision=True
            )

            if is_decision_oereb_attachments:
                for attachment in is_decision_oereb_attachments:
                    attachment.context["isDecisionOereb"] = attachment.context[
                        "isDecision"
                    ]
                    del attachment.context["isDecision"]
                    attachment.save()
                    self.stdout.write(
                        f"Instance {instance.pk} attachments were migrated"
                    )
                    counter += 1
        self.stdout.write(f"{counter} instances with ÖREB attachments were migrated")

        if options["commit"]:
            transaction.savepoint_commit(sid)
        else:
            transaction.savepoint_rollback(sid)
