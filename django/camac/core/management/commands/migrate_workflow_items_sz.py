from datetime import datetime, timedelta

from caluma.caluma_form import api as form_api
from caluma.caluma_form.models import Answer, Document, Form, Question
from caluma.caluma_user.models import BaseUser
from caluma.caluma_workflow.models import Case, Task, WorkItem
from caluma.caluma_workflow.utils import get_jexl_groups
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from camac.core.models import WorkflowEntry, WorkflowItem

WORKFLOW_ITEM_QUESTION = {
    55: "baukontrolle-realisierung-baubeginn",  # Baubegin erfolgt (table)
    56: "baukontrolle-realisierung-schnurgeruestabnahme",  # Schnergerustbanahme (table)
    57: "baukontrolle-realisierung-werke",  # Meldung an Werk
    58: "baukontrolle-realisierung-rohbauabnahme",  # Rohbauabnahme (table)
    59: "baukontrolle-realisierung-schlussabnahme",  # Schlussabname (table)
    68: "baukontrolle-realisierung-geometer",  # Meldung an Geometer
    69: "baukontrolle-realisierung-liegenschaftsschaetzung",  # Meldung an Liegenschaftsschatzung
    82: "bewilligungsverfahren-rueckzug",  # Ruckzug
    84: "beschwerdeverfahren-sistierung",  # Sistierung
    85: "bewilligungsverfahren-datum-gesamtentscheid",  # Kant Gesamtentscheid
    86: "bewilligungsverfahren-gr-sitzung-beschwerdefrist",  # Beschwerdefrist
    88: "baukontrolle-realisierung-kanalisationsabnahme",  # Kanalisationsabnahme (table)
}

WORKFLOW_ITEM_QUESTION_MAP = {
    72: "bewilligungsverfahren-gr-sitzung-versand",
    61: "baukontrolle-realisierung-bauende",  # (table)
    71: "bewilligungsverfahren-bewilligung-bis",
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
        form = Form.objects.get(slug="bauverwaltung")

        cases = (
            Case.objects.all()
            .exclude(instance__instance_state__name__in=["new", "subm"])
            .iterator()
        )
        for case in cases:

            if not case.work_items.filter(task=task).exists() and hasattr(
                case, "instance"
            ):
                document = Document.objects.create(form=form)

                for workflow_item, question in WORKFLOW_ITEM_QUESTION.items():
                    workflow_entry = WorkflowEntry.objects.filter(
                        workflow_item_id=workflow_item, instance=case.instance
                    )
                    if not workflow_entry:
                        continue

                    if len(workflow_entry) > 1:
                        self.stdout.write(
                            f"There are equal workflow entries: {workflow_entry}"
                        )

                    question = Question.objects.get(slug=question)

                    # Check if question is on a table form
                    if question.forms.filter(slug="realisierung-tabelle"):
                        row_document = form_api.save_document(
                            form=Form.objects.get(slug="realisierung-tabelle")
                        )

                        form_api.save_answer(
                            document=row_document,
                            question=question,
                            date=workflow_entry.first().workflow_date.date(),
                        )

                        form_api.save_answer(
                            document=document,
                            question=Question.objects.get(
                                slug="baukontrolle-realisierung-table"
                            ),
                            value=[row_document.pk],
                        )

                    else:
                        form_api.save_answer(
                            document=document,
                            question=question,
                            date=workflow_entry.first().workflow_date.date(),
                        )

                    workflow_item_name = WorkflowItem.objects.get(
                        workflow_item_id=workflow_entry.first().workflow_item_id
                    ).name
                    self.stdout.write(
                        f"Migrated workflow entry {workflow_entry.first().workflow_item_id} {workflow_item_name} to answer: {question} for instance {case.instance.pk}"
                    )

                WorkItem.objects.create(
                    case=case,
                    task=task,
                    meta={},
                    name=task.name,
                    status=WorkItem.STATUS_READY
                    if case.instance.instance_state.name != "arch"
                    else WorkItem.STATUS_COMPLETED,
                    deadline=(timezone.now() + timedelta(seconds=task.lead_time))
                    if task.lead_time
                    else None,
                    addressed_groups=get_jexl_groups(
                        task.address_groups, task, case, BaseUser(), None, {}
                    ),
                    controlling_groups=get_jexl_groups(
                        task.control_groups, task, case, BaseUser(), None, {}
                    ),
                    document=document,
                )

        content = open(
            "camac/core/management/commands/config/workflow_entries.txt"
        ).readlines()[2:]

        workflow_entries = [
            line.replace(" ", "").replace("\n", "").split("|") for line in content
        ]

        for workflow_entry in workflow_entries:
            case = Case.objects.get(
                **{"meta__camac-instance-id": int(workflow_entry[3])}
            )
            building_authority_workitem = case.work_items.get(task=task)

            question = Question.objects.get(
                slug=WORKFLOW_ITEM_QUESTION_MAP[int(workflow_entry[4])]
            )

            Answer.objects.create(
                document=building_authority_workitem.document,
                question=question,
                date=datetime.strptime(workflow_entry[1], "%Y-%m-%d%H:%M:%S+%f").date(),
            )
            self.stdout.write(
                f"Answer created for question {question} from workflow entry {workflow_entry[0]} for the instance {workflow_entry[3]}"
            )

        if options["dry"]:
            transaction.savepoint_rollback(sid)
        else:
            transaction.savepoint_commit(sid)
