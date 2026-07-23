import datetime

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
from caluma.caluma_workflow.utils import create_work_items
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import IntegerField
from django.db.models.fields.json import KeyTransform
from django.db.models.functions import Cast
from django.utils.timezone import now

from camac.core.models import PublicationEntry
from camac.instance.models import Instance

ANSWER_MAPPING = {
    "publication_date": "publikation-publikationsbeginn",
    "publication_end_date": "publikation-publikationsende",
    "text": "publikation-mailvorschau",
    "note": "publikation-bemerkungen",
}

NOTE_ANSWER_MAPPING = {
    "1.0": "publikation-bemerkungen-profilierung-auf-verlangen",
    "2.0": "publikation-bemerkungen-profiliert",
    "3.0": "publikation-bemerkungen-verpflockt",
    "4.0": "publikation-bemerkungen-keine-profilierung",
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
            "--commit",
            dest="commit",
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

        if options["instance"]:
            case = Instance.objects.get(pk=options["instance"]).case

            case.meta["migrated-publication"] = True

            self.migrate_publication(case)

            if options["commit"]:
                transaction.savepoint_commit(sid)
            else:
                transaction.savepoint_rollback(sid)

        else:
            cases = (
                Case.objects.all()
                .annotate(
                    instance_id=Cast(
                        KeyTransform("camac-instance-id", "meta"),
                        output_field=IntegerField(),
                    )
                )
                .exclude(
                    work_items__task_id__in=["fill-publication", "create-publication"]
                )
                .exclude(
                    instance_id__in=(
                        list(
                            Instance.objects.filter(
                                instance_state__name__in=[
                                    "new",
                                    "subm",
                                    "arch",
                                    "old",
                                    "rejected",
                                ]
                            ).values_list("pk", flat=True)
                        )
                    )
                )
                .order_by("instance_id")
            )

            total = cases.count()

            for i, case in enumerate(cases, 1):
                try:
                    instance = case.instance
                except Case.instance.RelatedObjectDoesNotExist:
                    self.stdout.write(f"For the case {case.pk} no instance exists!")
                    continue

                case.meta["migrated-publication"] = True

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

                self.migrate_publication(case)
                self.fix_work_item_status(case, instance)

                # reset the case status
                case.status = previous_status

            if options["commit"]:
                transaction.savepoint_commit(sid)
            else:
                transaction.savepoint_rollback(sid)

    def migrate_publication(self, case):
        publication = PublicationEntry.objects.filter(instance=case.instance.pk).first()

        target_work_item = create_work_items(
            tasks=[self.fill_task],
            case=case,
            user=self.user,
        )[0]

        if not publication:
            return

        for attr, slug in ANSWER_MAPPING.items():
            value = getattr(publication, attr)

            if not value:
                continue

            if attr == "note":
                value = NOTE_ANSWER_MAPPING[str(value)]

            save_answer(
                document=target_work_item.document,
                question=self._get_question(slug),
                user=self.user,
                **(
                    {"date": value}
                    if isinstance(value, datetime.datetime)
                    else {"value": value}
                ),
            )

        if publication.publication_date.date() < now().date():
            complete_work_item(target_work_item, self.user)

    def fix_work_item_status(self, case, instance):
        if instance.instance_state.name == "rejected":
            self.process_work_item(case, "fill-publication", suspend_work_item)
            self.process_work_item(case, "create-publication", suspend_work_item)

        elif instance.instance_state.name in [
            "old",
            "arch",
            "del",
        ]:
            self.process_work_item(case, "fill-publication", skip_work_item)
            self.process_work_item(case, "create-publication", cancel_work_item)

    def process_work_item(self, case, task_id, fn):
        work_item = case.work_items.filter(
            task_id=task_id, status=WorkItem.STATUS_READY
        ).first()

        if work_item:
            fn(work_item, self.user)
