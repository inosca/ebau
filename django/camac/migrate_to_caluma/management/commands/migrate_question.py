from logging import getLogger

from caluma.caluma_form import models as form_models
from caluma.caluma_workflow import models as workflow_models
from django.core.management.base import BaseCommand
from django.db import transaction

from camac.core.models import Answer
from camac.instance.models import Instance

log = getLogger(__name__)


class DryRun(BaseException):
    """Used to jump out of atomic block to implement dryrun."""

    pass


class Command(BaseCommand):
    """Migrate single question from old Camac to Caluma/Camac-NG."""

    help = "Migrate single question from old Camac to Caluma/Camac-NG."

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._dry_run = False

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry", help="Dry-run migration (don't commit DB)", action="store_true"
        )

    def handle(self, *args, **options):
        for instance in Instance.objects.all():
            try:
                self.migrate_instance(instance)
            except DryRun:
                log.info("Dry run: rolling back migration")
            except KeyboardInterrupt:
                log.fatal("User-requested stop. Current instance will not be saved")
                return
            except RuntimeError as exc:
                log.error(str(exc))
                # TODO: abort instance or whole migration?
                break

    @transaction.atomic
    def migrate_instance(self, instance):
        camac_answer = Answer.objects.filter(question_id=98, instance=instance).first()
        if not camac_answer:
            return
        caluma_case = workflow_models.Case.objects.filter(
            **{"meta__camac-instance-id": instance.instance_id}
        ).first()
        caluma_question = caluma_case.document.form.questions.filter(
            slug="oereb-verfahren"
        )
        if not caluma_question.exists():
            return
        caluma_answer = caluma_case.document.answers.filter(
            question_id="bezeichnung"
        ).first()
        if caluma_answer:
            return

        form_models.Answer.objects.create(
            document=caluma_case.document,
            value=camac_answer.answer,
            question_id="bezeichnung",
        )

        if self._dry_run:
            raise DryRun()
