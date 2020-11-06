import codecs
import json
from collections import defaultdict
from json import JSONDecodeError
from pathlib import Path

from caluma.caluma_form import api as form_api
from caluma.caluma_form.models import Form, Question
from caluma.caluma_user.models import BaseUser
from caluma.caluma_workflow import api as workflow_api
from caluma.caluma_workflow.models import Workflow
from django.utils import timezone

from camac.core import utils
from camac.instance.models import Instance, InstanceState
from camac.user.models import ServiceT, User

from .rsta_data import Beteiligter, Geschaeft


class Importer:
    """Load data and start imports from given filesystem path."""

    def __init__(self, path):
        self.path = path

    def run(self, path: Path = None):
        if path is None:
            path = self.path

        if path.is_file():
            data = self.read_file(path)
            geschaeft = Geschaeft.from_dict(data)

            print(f"Importing {path}")
            Import(geschaeft).run()

        for _file in path.glob("**/*.json"):
            self.run(_file)

    def read_file(self, path: Path) -> dict:
        try:
            data = json.loads(path.read_text())
        except JSONDecodeError:
            print("Non utf-8 file was provided for input, trying utf-8 with BOM.")
            try:
                data = json.loads(codecs.open(path, "r", encoding="utf-8-sig").read())
            except JSONDecodeError as ex:
                print("Unknown character encoding was passed, skipping", ex)
                data = None

        return data


workflow = Workflow.objects.get(pk="migrated")
form = Form.objects.get(pk="migriertes-dossier")
q_geschaeftstyp = Question.objects.get(pk="geschaeftstyp")
q_gemeinde = Question.objects.get(pk="gemeinde")
user = User.objects.get(username="service-account-camac-admin")
f_personalien = Form.objects.get(slug="personalien")


class Import:
    """Import a single instance from a given geschaeft."""

    def __init__(self, geschaeft):
        self.geschaeft = geschaeft
        self.row_documents = defaultdict(list)

    def run(self):
        instance_state = self.get_instance_state()
        service = ServiceT.objects.get(
            name=f"Leitbehörde {self.geschaeft.Gemeinde.gdBez}"
        ).service
        group = service.groups.filter(role__trans__name="Leitung Leitbehörde").first()

        self.caluma_user = BaseUser()
        self.caluma_user.username = user.username
        self.caluma_user.group = group.pk

        now = timezone.now()

        # TODO: add "migrated" status so we know in case of a reimport
        self.instance = Instance.objects.create(
            creation_date=now,
            modification_date=now,
            group=group,
            instance_state=instance_state,
            previous_instance_state=instance_state,
            user=user,
            form_id=1,
        )

        # TODO: try to use geschaeft.gNrExtern
        ebau_nr = utils.assign_ebau_nr(self.instance, self.geschaeft.gJahr)

        self.instance.instance_services.create(service=service, active=1)
        self.instance.tags.create(service=service, name=self.geschaeft.geschaefts_nr)

        self.case = workflow_api.start_case(
            workflow=workflow,
            form=form,
            user=self.caluma_user,
            meta={
                "camac-instance-id": self.instance.pk,
                "submit-date": now.isoformat(),
                "ebau-number": ebau_nr,
                "prefecta-number": self.geschaeft.geschaefts_nr,
            },
        )

        # Caluma base questions
        form_api.save_answer(
            document=self.case.document,
            question=q_geschaeftstyp,
            value=self.geschaeft.geschaefts_typ,
            user=self.caluma_user,
        )

        form_api.save_answer(
            document=self.case.document,
            question=q_gemeinde,
            value=str(service.pk),
            user=self.caluma_user,
        )

        self.import_personalien()

        # TODO camac
        # * Journal
        # * Publikation
        # * Dokumente
        # * Gebühren (evtl)

    def import_personalien(self):
        # Beteiligte -> Caluma personalien

        weitere_personen = set()
        for beteiligter in self.geschaeft.Beteiligte:
            if beteiligter.is_main:
                option = self.import_beteiligter_table(beteiligter)
                if option:
                    weitere_personen.add(option)
            else:
                # TODO: import misc Beteiligter into journal
                pass

        form_api.save_answer(
            document=self.case.document,
            question=Question.objects.get(slug="weitere-personen"),
            value=list(weitere_personen),
            user=self.caluma_user,
        )

    def import_beteiligter_table(self, beteiligter: Beteiligter):
        table_question = Question.objects.get(slug=beteiligter.tablequestion)
        row_document = form_api.save_document(form=table_question.row_form)

        self.row_documents[table_question.row_form_id].append(row_document)

        for ans in beteiligter.answer_values:
            question_slug, value = ans.values()
            form_api.save_answer(
                document=row_document,
                question=Question.objects.get(slug=question_slug),
                value=value,
                user=self.caluma_user,
            )

        form_api.save_answer(
            document=self.case.document,
            question=table_question,
            value=[doc.pk for doc in self.row_documents[table_question.row_form_id]],
            user=self.caluma_user,
        )

        return beteiligter.weitere_personen_option

    def get_instance_state(self):
        # TODO "hängig"
        MAP = {"eröffnet": "in_progress", "abgeschlossen": "finished"}

        return InstanceState.objects.get(
            name=MAP.get(self.geschaeft.gStatusBezD, "in_progress")
        )
