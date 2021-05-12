from logging import getLogger

from caluma.caluma_form import models as form_models
from caluma.caluma_workflow import models as workflow_models
from django.core.management.base import BaseCommand
from django.db import transaction

from camac.core.models import Answer
from camac.instance.models import Instance

log = getLogger(__name__)


class Command(BaseCommand):
    """Migrate single question from old Camac to Caluma/Camac-NG."""

    help = "Migrate single question from old Camac to Caluma/Camac-NG."

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._dry_run = False

    def handle(self, *args, **options):
        for instance in Instance.objects.all():
            try:
                self.migrate_instance(instance)
            except KeyboardInterrupt:
                log.fatal("User-requested stop. Current instance will not be saved")
                return
            except RuntimeError as exc:
                log.error(str(exc))
                break

    @transaction.atomic
    def migrate_instance(self, instance):
        camac_answer = Answer.objects.filter(question_id=98, instance=instance).first()
        if not camac_answer:
            return
        caluma_case = workflow_models.Case.objects.filter(
            **{"meta__camac-instance-id": instance.instance_id}
        ).first()

        if not caluma_case:
            return

        caluma_question = caluma_case.document.form.questions.filter(
            slug__in=[
                "oereb-verfahren",
                "mitberichtsverfahren-koor-bg",
                "mitberichtsverfahren-bund",
            ]
        )

        if not caluma_question.exists():
            return

        if caluma_case.document.form.slug == "oereb":
            self._create_answer(instance, caluma_case, camac_answer, "bezeichnung")

        if caluma_case.document.form.slug in ["mitbericht-kanton", "mitbericht-bund"]:
            self._create_answer(
                instance, caluma_case, camac_answer, "beschreibung-zu-mbv"
            )

    def _create_answer(self, instance, caluma_case, camac_answer, slug):
        caluma_answer = caluma_case.document.answers.filter(question_id=slug).first()
        if caluma_answer:
            return
        form_models.Answer.objects.create(
            document=caluma_case.document,
            value=camac_answer.answer,
            question_id=slug,
        )
        print(
            f"Answer created: {instance.pk}, {caluma_case.meta['dossier-number']}, {instance.group.name}, {slug}, {camac_answer.answer}"
        )
