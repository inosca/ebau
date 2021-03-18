from collections import defaultdict
from datetime import date

from caluma.caluma_form import api as form_api
from caluma.caluma_form.models import Document, HistoricalAnswer, Question
from caluma.caluma_form.validators import CustomValidationError
from django.core.management.base import BaseCommand
from django.db import transaction

from camac.instance.models import Instance


class Command(BaseCommand):
    help = "Fixes the migration of 'Einfache Vorabklärung'"

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

    @transaction.atomic
    def handle(self, *args, **options):
        sid = transaction.savepoint()

        instance_filters = (
            {"case__meta__camac-instance-id": options["instance"]}
            if options["instance"]
            else {}
        )

        self.failures = defaultdict(list)
        self.migrated_documents = Document.objects.filter(
            form_id="vorabklaerung-einfach",
            case__isnull=False,
            created_at__date__lte=date(2021, 3, 8),
            **instance_filters,
        )

        for document in self.migrated_documents:
            self.fix_description(document)
            self.fix_names(document)
            self.fix_coordinates(document)

        self.summary()

        if options["dry"]:
            transaction.savepoint_rollback(sid)
        else:
            transaction.savepoint_commit(sid)

    def _find_historical_answer(self, document, slug):
        answer = (
            HistoricalAnswer.objects.filter(document_id=document.pk, question_id=slug)
            .order_by("-history_date")
            .first()
        )

        if not answer:
            self.failures[document.case.meta.get("camac-instance-id")].append(slug)
            return None

        return answer.value

    def _has_answer(self, document, slug):
        answer = document.answers.filter(question_id=slug).first()

        return answer.value != "" or answer.value is None if answer else False

    def fix_description(self, document):
        if not self._has_answer(document, "beschreibung-bauvorhaben"):
            value = self._find_historical_answer(document, "beschreibung-bauvorhaben")
            if value:
                form_api.save_answer(
                    document=document,
                    question=Question.objects.get(slug="beschreibung-bauvorhaben"),
                    value=value[:1000],
                )

    def fix_names(self, document):
        table = document.answers.filter(
            question_id="personalien-gesuchstellerin"
        ).first()

        if not table:
            return

        migrated_row = table.documents.order_by("-created_at").first()

        if not migrated_row:
            return

        if not self._has_answer(migrated_row, "name-gesuchstellerin"):
            last_name = self._find_historical_answer(
                document, "name-gesuchstellerin-vorabklaerung"
            )
            if last_name:
                form_api.save_answer(
                    document=migrated_row,
                    question=Question.objects.get(slug="name-gesuchstellerin"),
                    value=last_name[:30],
                )

        if not self._has_answer(migrated_row, "vorname-gesuchstellerin"):
            first_name = self._find_historical_answer(
                document, "vorname-gesuchstellerin-vorabklaerung"
            )
            if first_name:
                form_api.save_answer(
                    document=migrated_row,
                    question=Question.objects.get(slug="vorname-gesuchstellerin"),
                    value=first_name[:30],
                )

    def fix_coordinates(self, document):
        table = document.answers.filter(question_id="parzelle").first()

        if not table:
            self.stdout.write(
                self.style.WARNING(
                    f"{document.case.meta.get('camac-instance-id')}: No table for parcel found"
                )
            )
            return

        migrated_row = table.documents.order_by("-created_at").first()

        if not migrated_row:
            self.stdout.write(self.style.WARNING("No migrated row found"))
            return

        for old_slug, new_slug in [
            ("lagekoordinaten-ost-einfache-vorabklaerung", "lagekoordinaten-ost"),
            ("lagekoordinaten-nord-einfache-vorabklaerung", "lagekoordinaten-nord"),
        ]:
            if not self._has_answer(migrated_row, new_slug):
                value = self._find_historical_answer(document, old_slug)
                if value:
                    try:
                        form_api.save_answer(
                            document=migrated_row,
                            question=Question.objects.get(slug=new_slug),
                            value=value,
                        )
                    except CustomValidationError:
                        self.failures[
                            document.case.meta.get("camac-instance-id")
                        ].append(old_slug)

    def summary(self):
        instance_ids = list(
            Instance.objects.filter(
                pk__in=list(
                    self.migrated_documents.values_list(
                        "case__meta__camac-instance-id", flat=True
                    )
                )
            )
            .exclude(instance_state__name__in=["new", "archived"])
            .values_list("pk", flat=True)
        )

        success = [i for i in instance_ids if i not in self.failures]
        if success:
            self.stdout.write(
                self.style.SUCCESS(f"{len(success)} instances successfully migrated:")
            )
            self.stdout.write(self.style.SUCCESS(f" - {', '.join(map(str,success))}"))

        warning = [
            i for i in instance_ids if i in self.failures and len(self.failures[i]) < 5
        ]
        if warning:
            self.stdout.write(
                self.style.WARNING(f"{len(warning)} instances migrated with warnings:")
            )
            self.stdout.write(
                self.style.WARNING(
                    "\n".join(
                        map(
                            lambda i: f" - {i}: {', '.join(self.failures[i])}",
                            warning,
                        )
                    )
                )
            )

        fail = [
            i for i in instance_ids if i in self.failures and len(self.failures[i]) == 5
        ]
        if fail:
            self.stdout.write(
                self.style.ERROR(f"{len(fail)} instances could not be migrated:")
            )
            self.stdout.write(self.style.ERROR(f" - {', '.join(map(str,fail))}"))
