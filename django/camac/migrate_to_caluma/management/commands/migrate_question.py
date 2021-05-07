import codecs
import inspect
import itertools
import json
import re
from collections import defaultdict
from datetime import datetime
from logging import getLogger
from pprint import pprint

from caluma.caluma_form import models as form_models
from caluma.caluma_workflow import models as workflow_models
from caluma.caluma_workflow.jexl import GroupJexl
from django.core.management.base import BaseCommand
from django.core.validators import EMPTY_VALUES
from django.db import transaction
from django.db.models import F, Value
from django.db.models.expressions import CombinedExpression, Func
from django.utils.timezone import now

from camac.constants import kt_uri as uri_constants
from camac.core.models import Answer, ChapterPage
from camac.instance.models import Instance, JournalEntry
from camac.instance.serializers import generate_identifier
from camac.migrate_to_caluma import question_map
from camac.user.models import Location, User

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
        )
        caluma_question = caluma_case.document.form.questions.filter(slug="bezeichnung")
        if not caluma_question.exists():
            return
        caluma_answer = caluma_case.document.answers.filter(slug="bezeichnung").first()
        if caluma_answer:
            return

        import pdb

        pdb.set_trace()

        if self._dry_run:
            raise DryRun()
