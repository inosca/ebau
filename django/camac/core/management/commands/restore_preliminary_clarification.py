import collections
import json
from datetime import date

from caluma.caluma_form import api as form_api
from caluma.caluma_form.models import Document, HistoricalAnswer, Question
from caluma.caluma_form.validators import CustomValidationError
from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.serializers.json import DjangoJSONEncoder
from django.db import transaction
from django.utils.timezone import now

QUESTIONS = [
    "name-gesuchstellerin-vorabklaerung",
    "vorname-gesuchstellerin-vorabklaerung",
    "lagekoordinaten-ost-einfache-vorabklaerung",
    "lagekoordinaten-nord-einfache-vorabklaerung",
]


class Command(BaseCommand):
    help = "Restore the applicant and parcel data for preliminary clarifications"

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry",
            "-d",
            dest="dry",
            action="store_true",
            default=False,
        )
        parser.add_argument(
            "--instance",
            "-i",
            dest="instance",
            type=int,
            default=None,
        )
        parser.add_argument(
            "--export",
            "-e",
            dest="export",
            action="store_true",
            default=False,
        )

    @transaction.atomic
    def handle(self, *args, **options):
        sid = transaction.savepoint()

        instance_filters = (
            {"case__meta__camac-instance-id": options["instance"]}
            if options["instance"]
            else {}
        )

        self.documents = Document.objects.filter(
            form_id="vorabklaerung-einfach",
            case__isnull=False,
            created_at__date__lte=date(2021, 3, 8),
            **instance_filters,
        )
        self.restore_file = settings.APPLICATION_DIR("restore_applicant.json")

        if options["export"]:
            self.run_export()
        else:
            self.run_import()

        if options["dry"]:
            transaction.savepoint_rollback(sid)
        else:
            transaction.savepoint_commit(sid)

    def run_export(self):
        data = collections.defaultdict(dict)

        data["meta"]["export_date"] = now()
        data["meta"]["last_answer_date"] = (
            HistoricalAnswer.objects.order_by("-history_date").first().history_date
        )

        for document in self.documents:
            instance_id = document.case.meta["camac-instance-id"]

            for slug in QUESTIONS:
                answer = (
                    HistoricalAnswer.objects.filter(
                        question_id=slug, document_id=document.pk
                    )
                    .order_by("-history_date")
                    .first()
                )

                data[instance_id][slug] = answer.value if answer else None

        with open(self.restore_file, "w") as f:
            f.write(json.dumps(data, indent=2, cls=DjangoJSONEncoder))

    def run_import(self):
        with open(self.restore_file, "r") as f:
            all_data = json.load(f)

            for document in self.documents:
                instance_id = document.case.meta["camac-instance-id"]
                data = all_data.get(str(instance_id))

                if not data:
                    continue

                for table, old, new, validate in [
                    (
                        "personalien-gesuchstellerin",
                        "name-gesuchstellerin-vorabklaerung",
                        "name-gesuchstellerin",
                        lambda s: s[:30],
                    ),
                    (
                        "personalien-gesuchstellerin",
                        "vorname-gesuchstellerin-vorabklaerung",
                        "vorname-gesuchstellerin",
                        lambda s: s[:30],
                    ),
                    (
                        "parzelle",
                        "lagekoordinaten-ost-einfache-vorabklaerung",
                        "lagekoordinaten-ost",
                        float,
                    ),
                    (
                        "parzelle",
                        "lagekoordinaten-nord-einfache-vorabklaerung",
                        "lagekoordinaten-nord",
                        float,
                    ),
                ]:
                    value = data.get(old)
                    if value:
                        try:
                            form_api.save_answer(
                                document=self._get_first_table_row(document, table),
                                question=Question.objects.get(slug=new),
                                value=validate(value),
                            )
                        except CustomValidationError as e:
                            self.stdout.write(
                                self.style.ERROR(
                                    f"Error while migrating {new} for instance {instance_id}: {e.detail[0]}"
                                )
                            )

    def _get_first_table_row(self, document, slug):
        table = document.answers.filter(question_id=slug).first()

        return table.documents.order_by("-created_at").first() if table else None
