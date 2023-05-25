from caluma.caluma_form.models import Document, Form
from django.core.management.base import BaseCommand
from django.db import transaction


class Command(BaseCommand):
    help = """Migrat the form of the old oereb form"""

    def add_arguments(self, parser):
        parser.add_argument("--dry", dest="dry", action="store_true", default=False)

    @transaction.atomic
    def handle(self, *args, **options):
        sid = transaction.savepoint()

        canton_oereb_documents = Document.objects.filter(form_id="oereb")

        for document in canton_oereb_documents:
            if document.answers.filter(
                value__in=[
                    "oereb-thema-gpz",
                    "oereb-thema-gnp",
                    "oereb-thema-snp-qgp-qp",
                    "oereb-thema-snp-bl-gemeinde",
                ]
            ):
                document.form = Form.objects.get(slug="oereb-verfahren-gemeinde")
                document.save()
                answer = document.answers.filter(question_id="oereb-thema")
                splitted_answer = answer.first().value.split("thema-")
                answer.update(
                    question_id="oereb-thema-gemeinde",
                    value=f"{splitted_answer[0]}thema-gemeinde-{splitted_answer[1]}",
                )

        if options["dry"]:
            transaction.savepoint_rollback(sid)
        else:
            transaction.savepoint_commit(sid)
