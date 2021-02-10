from caluma.caluma_form.api import save_answer
from caluma.caluma_form.models import Question
from caluma.caluma_user.models import AnonymousUser
from caluma.caluma_workflow.api import (
    cancel_work_item,
    complete_work_item,
    skip_work_item,
    suspend_work_item,
)
from caluma.caluma_workflow.models import Case, Task, WorkItem
from caluma.caluma_workflow.utils import bulk_create_work_items
from django.contrib.postgres.fields.jsonb import KeyTransform
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import IntegerField
from django.db.models.functions import Cast
from django.utils.timezone import now

from camac.core.models import Publication
from camac.instance.models import Instance

MAPPING = {
    "start": "publikation-startdatum",
    "end": "publikation-ablaufdatum",
    "text": "publikation-text",
    "publication_anzeiger_1": "publikation-1-publikation-anzeiger",
    "publication_anzeiger_2": "publikation-2-publikation-anzeiger",
    "publication_amtsblatt": "publikation-amtsblatt",
    "anzeiger": "publikation-anzeiger-von",
}


class Command(BaseCommand):
    help = "Migrates the legacy publication to the new caluma publication"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.questions = list(Question.objects.filter(forms__pk="publikation"))
        self.user = AnonymousUser(username="admin")

    def _get_question(self, slug):
        return next(filter(lambda q: q.pk == slug, self.questions))

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry",
            dest="dry",
            action="store_true",
            default=False,
        )
        parser.add_argument(
            "--exclude-migrated",
            dest="exclude_migrated",
            action="store_true",
            default=False,
        )
        parser.add_argument(
            "--instance",
            dest="instance",
            type=int,
            default=None,
        )

    @transaction.atomic
    def handle(self, *args, **options):
        sid = transaction.savepoint()

        self.fill_task = Task.objects.get(pk="fill-publication")

        cases = (
            Case.objects.filter(
                workflow_id__in=[
                    "building-permit",
                    "preliminary-clarification",
                    *([] if options["exclude_migrated"] else ["migrated"]),
                ]
            )
            .annotate(
                instance_id=Cast(
                    KeyTransform("camac-instance-id", "meta"),
                    output_field=IntegerField(),
                )
            )
            .exclude(work_items__task_id="fill-publication")
            .exclude(
                instance_id__in=(
                    [options["instance"]]
                    if options["instance"]
                    else list(
                        Instance.objects.filter(
                            instance_state__name__in=["new", "subm"]
                        ).values_list("pk", flat=True)
                    )
                )
            )
            .order_by("instance_id")
        )

        total = cases.count()
        for i, case in enumerate(cases, 1):
            instance = Instance.objects.get(pk=case.meta.get("camac-instance-id"))

            percentage = round(i / total * 100)

            self.stdout.write(
                f"Migrate instance {instance.pk} ({i} of {total}) [{percentage}%]",
                ending="\r",
            )
            self.stdout.flush()

            # Set the case status to running so we can skip, complete, cancel
            # and suspend work items even if the cases are already completed.
            # Don't save it though to avoid a historical entry for this
            # manipuliation, just setting it will suffice for the validation
            # layer to work.
            previous_status = case.status
            case.status = Case.STATUS_RUNNING

            self.migrate_publication(case, instance)
            self.fix_work_item_status(case, instance)

            # reset the case status
            case.status = previous_status

        if options["dry"]:
            transaction.savepoint_rollback(sid)
        else:
            transaction.savepoint_commit(sid)

    def migrate_publication(self, case, instance):
        publication = Publication.objects.filter(instance=instance.pk).first()

        target_work_item = bulk_create_work_items(
            tasks=[self.fill_task],
            case=case,
            user=self.user,
        )[0]

        if not publication:
            return

        for attr, slug in MAPPING.items():
            value = getattr(publication, attr)

            if not value:
                continue

            save_answer(
                document=target_work_item.document,
                question=self._get_question(slug),
                value=value,
                user=self.user,
            )

        if publication.start < now().date():
            complete_work_item(target_work_item, self.user)

    def fix_work_item_status(self, case, instance):
        # refetch new work items from db but only if ready
        fill_work_item = case.work_items.filter(
            task_id="fill-publication", status=WorkItem.STATUS_READY
        ).first()
        create_work_item = case.work_items.filter(
            task_id="create-publication", status=WorkItem.STATUS_READY
        ).first()

        if instance.instance_state.name in ["rejected", "correction"]:
            if fill_work_item:
                suspend_work_item(fill_work_item, self.user)
            if create_work_item:
                suspend_work_item(create_work_item, self.user)

        if (
            instance.instance_state.name
            in [
                "sb1",
                "sb2",
                "conclusion",
            ]
            and fill_work_item
        ):
            skip_work_item(fill_work_item, self.user)

        if instance.instance_state.name in [
            "evaluated",
            "finished",
            "finished_internal",
        ]:
            if fill_work_item:
                skip_work_item(fill_work_item, self.user)

            if create_work_item:
                cancel_work_item(create_work_item, self.user)
