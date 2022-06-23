from caluma.caluma_form.models import Answer, Document, Question
from caluma.caluma_workflow.models import Task, WorkItem
from django.core.management.base import BaseCommand
from django.db import transaction

from camac.core.models import DocxDecision

DECISION_ANSWER_MAPPING = {
    "positive": "decision-decision-assessment-positive",
    "negative": "decision-decision-assessment-negative",
    "conditionallyPositive": "decision-decision-assessment-positive-with-reservation",
    "retreat": "decision-decision-assessment-retreat",
    "accepted": "decision-decision-assessment-accepted",
    "denied": "decision-decision-assessment-denied",
    "writtenOff": "decision-decision-assessment-depreciated",
    "obligated": "decision-decision-assessment-obligated",
    "notObligated": "decision-decision-assessment-not-obligated",
    "other": "decision-decision-assessment-other",
}

DECISION_TYPE_ANSWER_MAPPING = {
    "BAUBEWILLIGUNG": "decision-approval-type-building-permit",
    "GESAMT": "decision-approval-type-overall-building-permit",
    "KLEIN": "decision-approval-type-small-building-permit",
    "GENERELL": "decision-approval-type-general-building-permit",
    "TEILBAUBEWILLIGUNG": "decision-approval-type-partial-building-permit",
    "PROJEKTAENDERUNG": "decision-approval-type-project-modification",
    "BAUABSCHLAG_OHNE_WHST": "decision-approval-type-construction-tee-without-restoration",
    "BAUABSCHLAG_MIT_WHST": "decision-approval-type-construction-tee-with-restoration",
    "ABSCHREIBUNGSVERFUEGUNG": "decision-approval-type-deprecation-order-retreat",
    "BAUBEWILLIGUNGSFREI": "decision-approval-type-building-permit-free",
    "TEILWEISE_BAUBEWILLIGUNG_MIT_TEILWEISEM_BAUABSCHLAG_UND_TEILWEISER_WIEDERHERSTELLUNG": "decision-approval-type-partial-building-permit-partial-construction-tee-partial-restoration",
    "UNKNOWN_ECH": "decision-approval-type-unknown",
}


class Command(BaseCommand):
    help = "Migrates the old docx decision module to the new caluma form"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.task = Task.objects.get(pk="decision")
        self.workflow_question = Question.objects.get(pk="decision-workflow")
        self.decision_assessment_question = Question.objects.get(
            pk="decision-decision-assessment"
        )
        self.approval_type_question = Question.objects.get(pk="decision-approval-type")
        self.date_question = Question.objects.get(pk="decision-date")

    def add_arguments(self, parser):
        parser.add_argument("--dry", dest="dry", action="store_true", default=False)

    @transaction.atomic
    def handle(self, *args, **options):
        sid = transaction.savepoint()

        self._remove_rejected_decisions()
        self._migrate_decisions()
        self._add_missing_documents()

        if options["dry"]:
            transaction.savepoint_rollback(sid)
        else:
            transaction.savepoint_commit(sid)

    def _remove_rejected_decisions(self):
        decisions = DocxDecision.objects.filter(
            instance__instance_state__name="rejected"
        )

        self.stdout.write(
            self.style.WARNING(
                f"Deleted {decisions.count()} decisions of rejected instances"
            )
        )

        decisions.delete()

    def _migrate_decisions(self):
        decisions = DocxDecision.objects.all()
        count = decisions.count()

        answers = []
        documents = []
        work_items = []

        for i, decision in enumerate(decisions, start=1):
            # Create new decision document
            document = Document(form_id="decision")
            documents.append(document)

            # Add answers for new document
            answers.append(
                Answer(
                    document=document,
                    question=self.workflow_question,
                    value=decision.instance.case.workflow_id,
                )
            )
            answers.append(
                Answer(
                    document=document,
                    question=self.decision_assessment_question,
                    value=DECISION_ANSWER_MAPPING[decision.decision],
                )
            )
            answers.append(
                Answer(
                    document=document,
                    question=self.date_question,
                    date=decision.decision_date,
                )
            )

            if decision.instance.case.workflow_id == "building-permit":
                answers.append(
                    Answer(
                        document=document,
                        question=self.approval_type_question,
                        value=DECISION_TYPE_ANSWER_MAPPING[decision.decision_type],
                    )
                )

            # Check if there's a decision work item
            work_item = (
                decision.instance.case.work_items.filter(task=self.task)
                .order_by("-created_at")
                .last()
            )

            if not work_item:
                service = decision.instance.responsible_service(
                    filter_type="municipality"
                )
                # If not, create a new one with the previously created document
                work_items.append(
                    WorkItem(
                        task=self.task,
                        name=self.task.name,
                        addressed_groups=[str(service.pk)],
                        controlling_groups=[str(service.pk)],
                        case=decision.instance.case,
                        status=WorkItem.STATUS_SKIPPED,
                        document=document,
                    )
                )
            else:
                # If yes, assign the previously created document to that work item
                work_item.document = document
                work_item.save()

            if i % 100 == 0 or i == count:
                self.stdout.write(
                    self.style.SUCCESS(f"Migrated decision {i} of {count}")
                )

        Answer.objects.bulk_create(answers)
        Document.objects.bulk_create(documents)
        WorkItem.objects.bulk_create(work_items)

        self.stdout.write(
            self.style.WARNING(f"Created {len(work_items)} missing decision work items")
        )

    def _add_missing_documents(self):
        answers = []
        documents = []

        for work_item in WorkItem.objects.filter(
            task=self.task,
            document__isnull=True,
            status__in=[WorkItem.STATUS_READY, WorkItem.STATUS_SUSPENDED],
        ):
            # Create new decision document
            document = Document(form_id="decision")
            documents.append(document)

            # Add normally automatically created answer for workflow
            answers.append(
                Answer(
                    document=document,
                    question=self.workflow_question,
                    value=work_item.case.workflow_id,
                )
            )

            work_item.document = document
            work_item.save()

        self.stdout.write(
            self.style.WARNING(f"Created {len(documents)} missing decision documents")
        )

        Answer.objects.bulk_create(answers)
        Document.objects.bulk_create(documents)
