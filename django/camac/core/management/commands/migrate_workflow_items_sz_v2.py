from caluma.caluma_form import api as form_api
from caluma.caluma_form.models import Form, Question
from caluma.caluma_workflow.models import Case, Task
from django.core.management.base import BaseCommand
from django.db import transaction

from camac.core.models import WorkflowEntry

WORKFLOW_ITEM_QUESTION = {
    47: "bewilligungsverfahren-gr-sitzung-bewilligungsdatum",  # Bewilligungsdatum
    55: "baukontrolle-realisierung-baubeginn",  # Baubegin erfolgt (table)
    56: "baukontrolle-realisierung-schnurgeruestabnahme",  # Schnergerustbanahme (table)
    57: "baukontrolle-realisierung-werke",  # Meldung an Werk
    58: "baukontrolle-realisierung-rohbauabnahme",  # Rohbauabnahme (table)
    59: "baukontrolle-realisierung-schlussabnahme",  # Schlussabname (table)
    67: "baukontrolle-realisierung-bauende",  # Bauende (table)
    68: "baukontrolle-realisierung-geometer",  # Meldung an Geometer
    69: "baukontrolle-realisierung-liegenschaftsschaetzung",  # Meldung an Liegenschaftsschatzung
    82: "bewilligungsverfahren-rueckzug",  # Ruckzug
    85: "bewilligungsverfahren-datum-gesamtentscheid",  # Kant Gesamtentscheid
    86: "bewilligungsverfahren-gr-sitzung-beschwerdefrist",  # Beschwerdefrist
    88: "baukontrolle-realisierung-kanalisationsabnahme",  # Kanalisationsabnahme (table)
}


class Command(BaseCommand):
    help = """Migrate the workflow entry dates to caluma answers."""

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry",
            default=False,
            action="store_true",
            help="Don't apply changes",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        sid = transaction.savepoint()

        task = Task.objects.get(slug="building-authority")

        cases = Case.objects.filter(
            parent_work_item__isnull=True, instance__isnull=False
        ).exclude(instance__instance_state__name__in=["new", "subm"])
        for case in cases:
            building_authority_workitem = case.work_items.filter(task=task).first()
            if not building_authority_workitem:
                self.stdout.write(
                    f"No building authority work item found for case: {case}"
                )
                continue

            document = building_authority_workitem.document

            table_row_answers = []
            for workflow_item, question in WORKFLOW_ITEM_QUESTION.items():
                workflow_entry = WorkflowEntry.objects.filter(
                    workflow_item_id=workflow_item, instance=case.instance
                )
                if not workflow_entry:
                    continue

                if len(workflow_entry) > 1:
                    self.stdout.write(
                        f"There are multiple workflow entries: {workflow_entry} in instance {case.instance}"
                    )

                question = Question.objects.get(slug=question)

                # Check if question is on a table form
                if question.forms.filter(slug="realisierung-tabelle"):
                    table_row_answers.append(
                        (question, workflow_entry.first().workflow_date.date())
                    )
                else:
                    form_api.save_answer(
                        document=document,
                        question=question,
                        date=workflow_entry.first().workflow_date.date(),
                    )

            self._write_table_row(table_row_answers, document)

        if options["dry"]:
            transaction.savepoint_rollback(sid)
        else:
            transaction.savepoint_commit(sid)

    def _write_table_row(self, answers, document):
        realisierung_table_form = Form.objects.get(slug="realisierung-tabelle")
        realisierung_table_question = Question.objects.get(
            slug="baukontrolle-realisierung-table"
        )

        if document.answers.filter(
            question=realisierung_table_question, documents__isnull=False
        ).exists():
            self.stdout.write(
                f"Skip table migration for document {document} since entries exist"
            )
            return

        row_document = form_api.save_document(form=realisierung_table_form)

        for question, value in answers:
            form_api.save_answer(
                document=row_document,
                question=question,
                date=value,
            )

        form_api.save_answer(
            document=document,
            question=realisierung_table_question,
            value=[row_document.pk],
        )

        self.stdout.write(
            f"Migrated row document {row_document} for document {document}"
        )
