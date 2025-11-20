from caluma.caluma_form.models import Answer
from django.core.management.base import BaseCommand
from django.db import transaction


class Command(BaseCommand):
    help = """Set the correct form-type for oereb-verfahren-gemeinde forms and correct the old camac forms."""

    def add_arguments(self, parser):
        parser.add_argument(
            "--commit", dest="commit", action="store_true", default=False
        )

    @transaction.atomic
    def handle(self, *args, **options):
        sid = transaction.savepoint()

        for a in Answer.objects.filter(
            question_id="form-type",
            value="form-type-oereb",
            document__form_id="oereb-verfahren-gemeinde",
        ):
            a.value = "form-type-oereb-verfahren-gemeinde"
            a.save()

            if (
                a.document.case.instance.form_id
                != a.document.form.meta["camac-form-id"]
            ):
                a.document.case.instance.form_id = a.document.form.meta["camac-form-id"]
                a.document.case.instance.save()

                print(
                    f"For instance {a.document.case.instance.pk} the camac-form-id was wrong"
                )
            else:
                print(
                    f"Camac-form-id was right for instance {a.document.case.instance.pk}"
                )

        if options["commit"]:
            transaction.savepoint_commit(sid)
        else:
            transaction.savepoint_rollback(sid)
