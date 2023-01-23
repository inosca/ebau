from caluma.caluma_form.models import Answer, Document
from caluma.caluma_workflow.models import Case, Task, WorkItem
from django.core.management.base import BaseCommand
from django.db import connection, transaction
from django.db.models import OuterRef, Subquery
from tqdm import tqdm

from camac.core.models import InstanceService


class Command(BaseCommand):
    help = (
        """Migrate old camac module objection to new caluma module legal-submission."""
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry",
            default=False,
            action="store_true",
            help="Don't apply changes",
        )
        parser.add_argument(
            "--only-data",
            default=False,
            action="store_true",
            help="Only migrate objection data - no work item creation",
        )
        parser.add_argument(
            "--reset",
            default=False,
            action="store_true",
            help="Remove migrated data",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if options.get("reset"):
            self.reset()

        sid = transaction.savepoint()

        if not options.get("only_data"):
            self.create_work_items()

        self.migrate_data()

        if options["dry"]:
            transaction.savepoint_rollback(sid)
        else:
            transaction.savepoint_commit(sid)

    def write(self, text):
        self.stdout.write(self.style.SUCCESS(text))

    def reset(self):
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE caluma_workflow_workitem SET previous_work_item_id = NULL WHERE task_id = 'legal-submission';"
            )
            cursor.execute(
                "DELETE FROM caluma_workflow_workitem WHERE task_id = 'legal-submission';"
            )

        Document.objects.filter(form__pk__startswith="legal-submission").delete()

    def migrate_data(self):
        self.write("Fetching cases with existing objections to migrate...")

        cases_with_data = (
            Case.objects.prefetch_related(
                "instance__objections",
                "instance__objections__objection_participants",
            )
            .filter(instance__objections__isnull=False)
            .distinct()
        )

        self.write("Migrating objections to legal submissions...")

        for case in tqdm(cases_with_data):
            self.migrate_objections(
                case, case.work_items.get(task_id="legal-submission")
            )

        self.write("Objections migrated!")

    def create_work_items(self):
        self.write("Fetching cases that need a legal submission work item...")

        ebau_number_subquery = WorkItem.objects.filter(
            task_id="ebau-number",
            case_id=OuterRef("pk"),
            status__in=[WorkItem.STATUS_COMPLETED, WorkItem.STATUS_SKIPPED],
        )

        cases = (
            Case.objects.select_related("instance", "instance__instance_state")
            .annotate(
                # Previous work item
                ebau_number_work_item_id=Subquery(
                    ebau_number_subquery.values("pk")[:1]
                ),
                # Creation date of new work item
                ebau_number_work_item_closed_at=Subquery(
                    ebau_number_subquery.values("closed_at")[:1]
                ),
                # Lead authority
                addressed_group=Subquery(
                    InstanceService.objects.filter(
                        active=1,
                        service__service_group__name__in=[
                            "district",
                            "municipality",
                            "lead-service",
                        ],
                        instance_id=OuterRef("instance__pk"),
                    ).values("service_id")[:1]
                ),
            )
            .filter(ebau_number_work_item_id__isnull=False)
            .exclude(work_items__task_id="legal-submission")
            .distinct()
        )

        task = Task.objects.get(pk="legal-submission")

        documents = []
        work_items = []

        self.write("Creating legal submission work items...")

        for case in tqdm(cases):
            document = Document(form_id="legal-submission")
            work_item = WorkItem(
                name=task.name,
                task=task,
                case=case,
                document=document,
                status=self.determine_status(case),
                previous_work_item_id=case.ebau_number_work_item_id,
                created_at=case.ebau_number_work_item_closed_at,
                addressed_groups=[str(case.addressed_group)],
            )

            documents.append(document)
            work_items.append(work_item)

        Document.objects.bulk_create(documents)
        WorkItem.objects.bulk_create(work_items)

        self.write("Legal submission work items created!")

    def determine_status(self, case):
        status = case.instance.instance_state.name

        if status == "rejected":
            return WorkItem.STATUS_SUSPENDED
        elif status == "archived":
            return WorkItem.STATUS_CANCELED
        elif status in [
            "sb1",
            "sb2",
            "conclusion",
            "finished",
            "finished_internal",
            "evaluated",
        ]:
            return WorkItem.STATUS_SKIPPED

        return WorkItem.STATUS_READY

    def migrate_objections(self, case, work_item):
        objections = case.instance.objections.all()

        if not objections.exists():
            return

        row_answer = Answer.objects.create(
            question_id="legal-submission-table", document=work_item.document
        )

        for objection in objections:
            row_document = Document.objects.create(
                form_id="legal-submission-form", family=work_item.document
            )

            Answer.objects.bulk_create(
                [
                    Answer(
                        question_id="legal-submission-title",
                        document=row_document,
                        value=objection.title,
                    ),
                    Answer(
                        question_id="legal-submission-receipt-date",
                        document=row_document,
                        date=objection.creation_date,
                    ),
                    Answer(
                        question_id="legal-submission-type",
                        document=row_document,
                        value=["legal-submission-type-objection"],
                    ),
                    Answer(
                        question_id="legal-submission-status",
                        document=row_document,
                        value="legal-submission-status-open"
                        if work_item.status == WorkItem.STATUS_READY
                        else "legal-submission-status-done",
                    ),
                ]
            )

            self.migrate_participants(objection, row_document)

            row_answer.documents.add(row_document)

    def migrate_participants(self, objection, document):
        participants = objection.objection_participants.all()

        if not participants.exists():
            return

        row_answer = Answer.objects.create(
            question_id="legal-submission-legal-claimants-table-question",
            document=document,
        )

        for participant in participants:
            row_document = Document.objects.create(
                form_id="personalien-tabelle", family=document.family
            )

            Answer.objects.bulk_create(
                [
                    Answer(
                        question_id="juristische-person-gesuchstellerin",
                        document=row_document,
                        value="juristische-person-gesuchstellerin-ja"
                        if participant.company
                        else "juristische-person-gesuchstellerin-nein",
                    ),
                    Answer(
                        question_id="name-juristische-person-gesuchstellerin",
                        document=row_document,
                        value=participant.company,
                    ),
                    Answer(
                        question_id="name-gesuchstellerin",
                        document=row_document,
                        value=participant.name,
                    ),
                    Answer(
                        question_id="strasse-gesuchstellerin",
                        document=row_document,
                        value=participant.address,
                    ),
                    Answer(
                        question_id="vertreterin",
                        document=row_document,
                        value="vertreterin-ja"
                        if participant.representative
                        else "vertreterin-nein",
                    ),
                    Answer(
                        question_id="telefon-oder-mobile-gesuchstellerin",
                        document=row_document,
                        value=participant.phone,
                    ),
                    Answer(
                        question_id="e-mail-gesuchstellerin",
                        document=row_document,
                        value=participant.email,
                    ),
                    Answer(
                        question_id="ort-gesuchstellerin",
                        document=row_document,
                        value=participant.city,
                    ),
                ]
            )

            row_answer.documents.add(row_document)
