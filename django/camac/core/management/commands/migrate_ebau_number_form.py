from caluma.caluma_form.models import Answer, Document
from caluma.caluma_workflow.models import Case, WorkItem
from dateutil.parser import parse as dateutil_parse
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Exists, OuterRef
from django.utils.timezone import is_naive, make_aware
from tqdm import tqdm

from camac.core.models import Answer as CamacAnswer


class Command(BaseCommand):
    help = "Migrates the old camac form for 'eBau-Nummer vergeben' to a Caluma form"

    def add_arguments(self, parser):
        parser.add_argument("--dry", dest="dry", action="store_true", default=False)

    @transaction.atomic
    def handle(self, *args, **options):
        sid = transaction.savepoint()

        self.fix_case_meta()

        cases_without_ebau_number_document = (
            Case.objects.filter(
                workflow_id__in=[
                    "building-permit",
                    "preliminary-clarification",
                    "internal",
                    "migrated",
                ]
            )
            .exclude(instance__instance_state__name="new")
            .exclude(**{"meta__ebau-number__isnull": True})
            .exclude(
                Exists(
                    WorkItem.objects.filter(
                        case=OuterRef("pk"),
                        task_id="ebau-number",
                    )
                )
            )
        )

        work_items = []
        documents = []
        answers = []

        for case in tqdm(cases_without_ebau_number_document):
            result = self.migrate_assign_ebau_number(case)

            if result:
                work_items.append(result[0])
                documents.append(result[1])
                answers.extend(result[2])

        Document.objects.bulk_create(documents)
        Answer.objects.bulk_create(answers)
        WorkItem.objects.bulk_create(work_items)

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully created {len(documents)} documents, {len(answers)} answers and {len(work_items)} work items"
            )
        )

        if options["dry"]:
            transaction.savepoint_rollback(sid)
        else:
            transaction.savepoint_commit(sid)

    def fix_case_meta(self):
        cases = Case.objects.filter(**{"meta__ebau-number": None})
        count = cases.count()

        if not count:
            return

        # Remove meta["ebau-number"] where value is None
        for case in cases:
            del case.meta["ebau-number"]
            case.save()

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully removed empty eBau numbers on {count} cases"
            )
        )

    def get_answers(self, case):
        existing = CamacAnswer.objects.filter(
            instance=case.instance, item=1, chapter=20000, question=20035
        ).first()

        if existing and existing.answer != case.meta["ebau-number"]:
            tqdm.write(
                self.style.WARNING(
                    f"eBau number mismatch for instance {case.instance.pk}: {existing.answer} (form) != {case.meta['ebau-number']} (meta)"
                )
            )

        if not existing:
            return {"ebau-number-has-existing": "ebau-number-has-existing-no"}

        return {
            "ebau-number-has-existing": "ebau-number-has-existing-yes",
            "ebau-number-existing": case.meta["ebau-number"],
        }

    def migrate_assign_ebau_number(self, case):
        camac_answers = self.get_answers(case)

        # For simplicity, we assume that the work item was closed around the
        # submit date. However, we might not have that information if the
        # instance was migrated from old camac or RSTA - in that case we just
        # take the creation date of the case.
        if case.meta.get("submit-date"):
            submit_date = dateutil_parse(case.meta.get("submit-date"))
            closed_at = (
                make_aware(submit_date) if is_naive(submit_date) else submit_date
            )
        elif case.meta.get("migrated_from_old_camac") or case.meta.get(
            "prefecta-number"
        ):
            closed_at = case.created_at

        document = Document(form_id="ebau-number")
        work_item = WorkItem(
            task_id="ebau-number",
            status=WorkItem.STATUS_COMPLETED,
            document=document,
            case=case,
            closed_at=closed_at,
        )
        answers = []

        for question_id, value in camac_answers.items():
            answers.append(
                Answer(document=document, question_id=question_id, value=value)
            )

        return (work_item, document, answers)
