import codecs
import json
from collections import Counter, defaultdict
from json import JSONDecodeError
from pathlib import Path

from caluma.caluma_form import api as form_api
from caluma.caluma_form.models import Form, Question
from caluma.caluma_form.validators import CustomValidationError
from caluma.caluma_user.models import BaseUser
from caluma.caluma_workflow import api as workflow_api
from caluma.caluma_workflow.models import Case, Workflow
from django.utils.timezone import make_aware, now

from camac.core import utils
from camac.core.models import Publication
from camac.instance.models import Instance, InstanceState, JournalEntry
from camac.user.models import Service, ServiceT, User

from .rsta_data import Beteiligter, Geschaeft


class CalumaMigrationUser(BaseUser):
    def __str__(self):
        return self.username


class Importer:
    """Load data and start imports from given filesystem path."""

    def __init__(self, path):
        self.path = path
        self.services = Counter()
        self.results = {}

    def iter(self, path: Path):
        if path.is_file():
            data = self.read_file(path)
            print(f"Loading file {path}")
            yield path.name, Geschaeft.from_dict(data)

        for _file in path.glob("**/*.json"):
            yield from self.iter(_file)

    def run(self):
        for filename, geschaeft in self.iter(self.path):
            print(f"Importing geschaeft {geschaeft.geschaefts_nr}")
            Import(self, filename, geschaeft).run()

    def find_missing_services(self):
        for filename, geschaeft in self.iter(self.path):
            Import(self, filename, geschaeft).find_missing_services()

    def read_file(self, path: Path) -> dict:
        try:
            data = json.loads(path.read_text())
        except JSONDecodeError:
            try:
                data = json.loads(codecs.open(path, "r", encoding="utf-8-sig").read())
            except JSONDecodeError:
                print(f"{path.name}: Unknown file format was passed, skipping")
                raise

        return data


workflow = Workflow.objects.get(pk="migrated")
form = Form.objects.get(pk="migriertes-dossier")
q_geschaeftstyp = Question.objects.get(pk="geschaeftstyp")
q_gemeinde = Question.objects.get(pk="gemeinde")
user = User.objects.get(username="service-account-camac-admin")
f_personalien = Form.objects.get(slug="personalien")


class Import:
    """Import a single instance from a given geschaeft."""

    def __init__(self, importer: Importer, filename: str, geschaeft: Geschaeft):
        self.importer = importer
        self.filename = filename
        self.geschaeft = geschaeft

        self.now = now()
        self.row_documents = defaultdict(list)

        self.results = {
            "filename": filename,
            "geschaeft_nr": geschaeft.geschaefts_nr,
            "geschaeft_typ": geschaeft.geschaefts_typ,
            "g_jahr": geschaeft.gJahr,
            "g_nr_extern": geschaeft.gNrExtern,
            "started": self.now,
        }
        self.error_entries = []

    def find_missing_services(self):
        try:
            ServiceT.objects.get(name=self.geschaeft.Gemeinde.service_name)
        except ServiceT.DoesNotExist:
            self.importer.services[self.geschaeft.Gemeinde.gdBez] += 1

    def run(self):
        # TODO check tags if geschaeft was imported already
        # Tag.objects.filter(
        #     service=self.service, name=self.geschaeft.geschaefts_nr
        # )

        self.municipality = ServiceT.objects.get(
            name=self.geschaeft.Gemeinde.service_name
        ).service

        self.service = Service.objects.get(pk=self.geschaeft.Mandant.service)
        self.group = self.service.groups.filter(
            role__trans__name="Leitung Leitbehörde"
        ).first()

        self.caluma_user = CalumaMigrationUser()
        self.caluma_user.username = user.username
        self.caluma_user.group = self.group.pk

        instance_state = InstanceState.objects.get(
            name=self.geschaeft.instance_state_name
        )

        # TODO: add "migrated" status so we know in case of a reimport
        self.instance = Instance.objects.create(
            creation_date=self.now,
            modification_date=self.now,
            group=self.group,
            instance_state=instance_state,
            previous_instance_state=instance_state,
            user=user,
            form_id=1,
        )

        # use gNrExtern if it's an existing ebau_nr
        if Case.objects.filter(
            **{"meta__ebau-number": self.geschaeft.gNrExtern}
        ).exists():
            ebau_nr = self.geschaeft.gNrExtern
        else:
            ebau_nr = utils.assign_ebau_nr(self.instance, self.geschaeft.gJahr)

        self.instance.instance_services.create(service=self.service, active=1)
        self.instance.tags.create(
            service=self.service, name=self.geschaeft.geschaefts_nr
        )

        self.case = workflow_api.start_case(
            workflow=workflow,
            form=form,
            user=self.caluma_user,
            meta={
                "camac-instance-id": self.instance.pk,
                "submit-date": self.geschaeft.submit_date,
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
            value=str(self.municipality.pk),
            user=self.caluma_user,
        )

        self.import_beteiligte()
        self.import_aktivitaeten()
        self.import_details()

        # TODO camac
        # * Dokumente
        # * Gebühren (evtl)

        # add errornous data
        JournalEntry.objects.create(
            instance=self.instance,
            service=self.service,
            user=user,
            text="\n---\n".join(self.error_entries),
            creation_date=self.now,
            modification_date=self.now,
        )

    def import_beteiligte(self):
        weitere_personen = set()

        for beteiligter in self.geschaeft.Beteiligte:
            if beteiligter.is_main:
                option = self.import_caluma_personalien(beteiligter)
                if option:
                    weitere_personen.add(option)
            else:
                JournalEntry.objects.create(
                    instance=self.instance,
                    service=self.service,
                    user=user,
                    text=beteiligter.journal_text,
                    creation_date=make_aware(beteiligter.bMutdat),
                    modification_date=make_aware(beteiligter.bMutdat),
                )

        form_api.save_answer(
            document=self.case.document,
            question=Question.objects.get(slug="weitere-personen"),
            value=list(weitere_personen),
            user=self.caluma_user,
        )

    def import_aktivitaeten(self):
        # import publication
        pub_akt = [akt for akt in self.geschaeft.Aktivitaeten if akt.sCodeS == 23]
        if pub_akt:
            pub_akt = pub_akt[0]

            if all([pub_akt.sDatum1, pub_akt.sDatum2]):
                Publication.objects.create(
                    instance=self.instance.pk,
                    start=pub_akt.sDatum1.date().isoformat(),
                    end=pub_akt.sDatum2.date().isoformat(),
                )
            else:
                self.error_entries.append(f"Publikation: {pub_akt.journal_text}")

        # import all other than submit date, publication
        rest = [akt for akt in self.geschaeft.Aktivitaeten if akt.sCodeS not in [1, 23]]

        for akt in rest:
            JournalEntry.objects.create(
                instance=self.instance,
                service=self.service,
                user=user,
                text=akt.journal_text,
                creation_date=make_aware(akt.sMutdat),
                modification_date=make_aware(akt.sMutdat),
            )

    def import_details(self):
        for detail in self.geschaeft.Details:
            if detail.is_main:
                form_api.save_answer(
                    document=self.case.document,
                    question=Question.objects.get(pk=detail.question_slug),
                    value=detail.dText1,
                    user=self.caluma_user,
                )
            else:
                JournalEntry.objects.create(
                    instance=self.instance,
                    service=self.service,
                    user=user,
                    text=detail.journal_text,
                    creation_date=make_aware(detail.dMutdat),
                    modification_date=make_aware(detail.dMutdat),
                )

    def import_caluma_personalien(self, beteiligter: Beteiligter):
        table_question = Question.objects.get(slug=beteiligter.tablequestion)
        row_document = form_api.save_document(form=table_question.row_form)

        self.row_documents[table_question.row_form_id].append(row_document)

        has_errors = beteiligter.Adresse.aLandCode != "CH"

        for ans in beteiligter.answer_values:
            question_slug, value, length = ans.values()

            if length and len(value) > length:
                has_errors = True
                value = value[:length]

            try:
                form_api.save_answer(
                    document=row_document,
                    question=Question.objects.get(slug=question_slug),
                    value=value,
                    user=self.caluma_user,
                )
            except CustomValidationError:
                has_errors = True
                raise

        if has_errors:
            self.error_entries.append(
                f"{beteiligter.bCodeBBezD}: {beteiligter.Adresse}"
            )

        form_api.save_answer(
            document=self.case.document,
            question=table_question,
            value=[doc.pk for doc in self.row_documents[table_question.row_form_id]],
            user=self.caluma_user,
        )

        return beteiligter.weitere_personen_option
