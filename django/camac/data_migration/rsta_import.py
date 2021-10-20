import codecs
import json
import mimetypes
import pickle
import re
import sys
import traceback
from collections import Counter, defaultdict
from json import JSONDecodeError
from pathlib import Path
from typing import Optional

from caluma.caluma_form import api as form_api
from caluma.caluma_form.models import Form, Question
from caluma.caluma_form.validators import CustomValidationError
from caluma.caluma_user.models import BaseUser
from caluma.caluma_workflow import api as workflow_api
from caluma.caluma_workflow.models import Case, Workflow
from django.core.files import File
from django.db import transaction
from django.utils.timezone import make_aware, now

from camac.core import utils
from camac.core.models import Publication
from camac.document.models import Attachment, AttachmentSection
from camac.instance.models import Instance, InstanceState, JournalEntry
from camac.tags.models import Tags
from camac.user.models import Service, ServiceT, User

from .rsta_data import Beteiligter, Geschaeft

workflow = Workflow.objects.get(pk="migrated")
form = Form.objects.get(pk="migriertes-dossier")
q_geschaeftstyp = Question.objects.get(pk="geschaeftstyp")
q_gemeinde = Question.objects.get(pk="gemeinde")
user, _ = User.objects.get_or_create(
    username="prefecta-migration", defaults={"name": "Prefecta", "surname": "Migration"}
)
f_personalien = Form.objects.get(slug="personalien")
attachment_section = AttachmentSection.objects.get(trans__name="Intern")


def read_file(path: Path) -> dict:
    try:
        data = json.loads(path.read_text())
    except JSONDecodeError:
        try:
            data = json.loads(codecs.open(path, "r", encoding="utf-8-sig").read())
        except JSONDecodeError:
            print(f'Unknown file format was passed, skipping: "{path.name}"')
            raise

    return data


class CalumaMigrationUser(BaseUser):
    def __str__(self):
        return self.username


class Importer:
    """Load data and start imports from given filesystem path."""

    def __init__(
        self,
        path,
        state_file: Optional[Path] = None,
        document_path: Optional[Path] = None,
        reimport: bool = True,
        debug: bool = False,
    ):
        self.path = path
        self.services = Counter()
        self.state_file = state_file or Path.cwd() / "migrate_rsta_state.pickle"
        self.reimport = reimport
        self.debug = debug

        self.document_path = document_path or self.path
        if self.document_path.is_file():
            self.document_path = self.document_path.parent

        try:
            self.results = pickle.load(self.state_file.open("rb"))
            assert isinstance(self.results, dict)
        except (FileNotFoundError, AssertionError):
            self.results = {}

    @property
    def all_files(self) -> list:
        return self.results.keys()

    @property
    def completed_files(self) -> list:
        return [
            filename
            for filename, result in self.results.items()
            if result["status"] == "completed"
        ]

    def write_result(self, filename, result):
        self.results[filename] = result
        pickle.dump(self.results, self.state_file.open("wb"))

    def iter(self, path: Path):
        if path.is_file():
            data = read_file(path)
            yield path.name, Geschaeft.from_dict(data)

        for _file in path.glob("*.json"):
            if _file.name in self.completed_files:
                continue

            yield from self.iter(_file)

    def run(self, reimport: bool = True, debug: bool = False):
        self._exec_method("run", reimport, debug)

    def set_zustaendig(self, reimport: bool = True, debug: bool = False):
        self._exec_method("set_zustaendig", reimport, debug)

    def reimport_documents(self, reimport: bool = True, debug: bool = False):
        self._exec_method("reimport_documents", reimport, debug)

    def _exec_method(self, method, reimport: bool = True, debug: bool = False):
        start = now()

        for filename, geschaeft in self.iter(self.path):
            print(f"Importing geschaeft {geschaeft.geschaefts_nr} from file {filename}")
            _import = Import(self, filename, geschaeft)
            result = getattr(_import, method)(reimport, debug)
            self.write_result(filename, result)

        duration = (now() - start).total_seconds()

        total = len(self.results)
        completed = len(
            [
                result
                for result in self.results.values()
                if result["status"] == "completed"
            ]
        )
        failed = len(
            [result for result in self.results.values() if result["status"] == "failed"]
        )

        hours, minutes, seconds = duration // 3600, duration // 60 % 60, duration % 60

        print(
            "\n"
            "Migration Summary\n"
            "-----------------\n"
            f"Total: {total}, Completed: {completed}, Failed: {failed}\n"
            f"Duration: {hours} h, {minutes} min, {seconds} s"
        )

    def find_missing_services(self):
        for _, geschaeft in self.iter(self.path):
            try:
                ServiceT.objects.get(
                    name=geschaeft.Gemeinde.service_name, language="de"
                )
            except (ServiceT.DoesNotExist, ServiceT.MultipleObjectsReturned):
                self.services[geschaeft.Gemeinde.gdBez] += 1


class Import:
    """Import a single instance from a given geschaeft."""

    def __init__(self, importer: Importer, filename: str, geschaeft: Geschaeft):
        self.importer = importer
        self.filename = filename
        self.geschaeft = geschaeft
        self.instance = None

        self.now = now()
        self.row_documents = defaultdict(list)

        self.results = {
            "filename": filename,
            "geschaeft_nr": geschaeft.geschaefts_nr,
            "geschaeft_typ": geschaeft.geschaefts_typ,
            "g_jahr": geschaeft.gJahr,
            "g_nr_extern": geschaeft.gNrExtern,
            "started": self.now,
            "status": "running",
            "errors": [],
        }

    def log_error(self, error):
        self.results["errors"].append(error)

    def run(self, reimport: bool = True, debug: bool = False) -> bool:
        return self._exec_method("_run", reimport, debug)

    def set_zustaendig(self, reimport: bool = True, debug: bool = False) -> bool:
        return self._exec_method("_set_zustaendig", reimport, debug)

    def reimport_documents(self, reimport: bool = True, debug: bool = False) -> bool:
        return self._exec_method("_reimport_documents", reimport, debug)

    def _exec_method(self, method, reimport: bool = True, debug: bool = False) -> bool:
        try:
            self._init()
            getattr(self, method)(reimport)
            self.results["status"] = "completed"
        except Exception:  # noqa: B901
            self.results["status"] = "failed"

            print(f'## Error: file "{self.filename}" failed!')

            if not debug:
                traceback.print_exc(file=sys.stdout)
            else:
                raise

        return self.results

    def _init(self):
        self.municipality = self.get_municipality(self.geschaeft.Gemeinde.service_name)
        self.service = Service.objects.get(pk=self.geschaeft.Mandant.service)
        self.group = self.service.groups.filter(
            trans__name__startswith="Leitung Regierungsstatthalteramt"
        ).first()

        self.caluma_user = CalumaMigrationUser()
        self.caluma_user.username = user.username
        self.caluma_user.group = self.group.service_id

    @transaction.atomic
    def _run(self, reimport):
        instance_state = InstanceState.objects.get(
            name=self.geschaeft.instance_state_name
        )

        # see if tag already exists -> geschaeft was imported already
        tag = Tags.objects.filter(
            name=self.geschaeft.geschaefts_nr, service=self.service
        ).first()
        if tag:
            if reimport:
                # clean up all camac fields trough cascade, caluma is upsert anyways
                tag.instance.delete()
                tag.delete()

            else:
                # don't touch existing instance
                return

        self.instance = Instance.objects.create(
            creation_date=self.now,
            modification_date=self.now,
            group=self.group,
            instance_state=instance_state,
            previous_instance_state=instance_state,
            user=user,
            form_id=1,
        )

        ebau_nr = self.get_or_create_ebau_nr()

        self.instance.instance_services.create(service=self.service, active=1)
        self.instance.tags.create(
            service=self.service, name=self.geschaeft.geschaefts_nr
        )

        self._set_zustaendig()

        self.case = Case.objects.filter(
            **{
                "meta__prefecta-number": self.geschaeft.geschaefts_nr,
                "meta__prefecta-mandant": self.geschaeft.gMandant,
            }
        ).first()

        if self.case and reimport:
            self.case.delete()
            self.case = None

        if not self.case:
            self.case = workflow_api.start_case(
                workflow=workflow,
                form=form,
                user=self.caluma_user,
                meta={
                    "camac-instance-id": self.instance.pk,
                    "submit-date": self.geschaeft.submit_date,
                    "ebau-number": ebau_nr,
                    "prefecta-number": self.geschaeft.geschaefts_nr,
                    "prefecta-mandant": self.geschaeft.gMandant,
                },
            )

        if instance_state.name == "finished":
            decision = self.case.work_items.filter(task__slug="decision").get()
            decision.status = decision.STATUS_SKIPPED
            decision.save()
            self.case.status = self.case.STATUS_COMPLETED
            self.case.save()

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
        self.import_documents()

        # TODO camac
        # * Gebühren (evtl)

        # add errornous data
        if self.results["errors"]:
            JournalEntry.objects.create(
                instance=self.instance,
                service=self.service,
                user=user,
                text="\n---\n".join(self.results["errors"]),
                creation_date=self.now,
                modification_date=self.now,
            )

    def _reimport_documents(self, reimport: bool = True, debug: bool = False):
        # see if tag already exists -> geschaeft was imported already
        tag = Tags.objects.filter(
            name=self.geschaeft.geschaefts_nr, service=self.service
        ).first()

        if not tag:
            return

        self.instance = tag.instance

        self.case = Case.objects.filter(
            **{
                "meta__prefecta-number": self.geschaeft.geschaefts_nr,
                "meta__prefecta-mandant": self.geschaeft.gMandant,
            }
        ).first()

        case_inst_id = self.case.meta.get("camac-instance-id")

        if self.case.meta.get("camac-instance-id") != self.instance.pk:
            print(
                f"Tag {self.instance.pk} and Case {case_inst_id} do not match for {self.geschaeft.geschaefts_nr}, {self.geschaeft.gMandant}"
            )
            return

        self.import_documents()

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
                self.log_error(f"Publikation: {pub_akt.journal_text}")

        for akt in self.geschaeft.Aktivitaeten:
            JournalEntry.objects.create(
                instance=self.instance,
                service=self.service,
                user=user,
                text=akt.journal_text,
                creation_date=make_aware(akt.journal_date),
                modification_date=make_aware(akt.journal_date),
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
            self.log_error(f"{beteiligter.bCodeBBezD}: {beteiligter.Adresse}")

        form_api.save_answer(
            document=self.case.document,
            question=table_question,
            value=[doc.pk for doc in self.row_documents[table_question.row_form_id]],
            user=self.caluma_user,
        )

        return beteiligter.weitere_personen_option

    def import_documents(self):
        for doc in self.geschaeft.Dokumente:
            path = self.importer.document_path / doc.file_path
            path_latin1 = self.importer.document_path / doc.file_path_latin1

            attachment = self.instance.attachments.filter(name=path.name).first()

            # skip existing attachments
            if attachment and attachment.size > 0:
                continue

            file = None
            size = 0

            for p in [path, path_latin1]:
                try:
                    file = File(p.open("rb"), name=p.name)
                    size = file.size
                    break
                except FileNotFoundError:
                    continue

            if file is None:
                self.log_error(
                    f"Dokument nicht gefunden | Fichier introuvable: {path.name}"
                )

            if attachment:
                attachment.path = file
                attachment.size = size
                attachment.mime_type = (
                    mimetypes.guess_type(str(path))[0] or "application/octet-stream"
                )
                attachment.save()
                continue

            attachment = Attachment.objects.create(
                instance=self.instance,
                user=user,
                service=self.service,
                group=self.group,
                name=path.name,
                context={"displayName": doc.docName},
                path=file,
                size=size,
                date=make_aware(doc.docCreatedat) if doc.docCreatedat else self.now,
                mime_type=mimetypes.guess_type(str(path))[0]
                or "application/octet-stream",
            )
            attachment_section.attachments.add(attachment)

    def get_municipality(self, name):
        try:
            return ServiceT.objects.get(name=name, language="de").service
        except ServiceT.MultipleObjectsReturned:
            return ServiceT.objects.get(
                name=name, language="de", service__disabled=0
            ).service

    def _set_zustaendig(self, reimport: bool = True):
        zustaendig = self.geschaeft.gZustaendig

        if not zustaendig:
            return

        instance = self.instance

        if instance is None:
            tag = Tags.objects.filter(
                name=self.geschaeft.geschaefts_nr, service=self.service
            ).first()

            if tag is None:
                return

            instance = tag.instance

        Tags.objects.get_or_create(
            instance=instance, service=self.service, name=f"zuständig: {zustaendig}"
        )

    def get_or_create_ebau_nr(self):
        # use gNrExtern if it's an existing ebau_nr
        pattern = re.compile("([0-9]{4}-[1-9][0-9]*)")
        result = pattern.search(str(self.geschaeft.gNrExtern))

        if result:
            try:
                match = result.groups()[0]
                case = Case.objects.filter(**{"meta__ebau-number": match}).first()
                instance_id = case.meta.get("camac-instance-id")
                instance = Instance.objects.get(pk=instance_id)

                if instance.services.filter(service_id=self.service.pk).exists():
                    return match
            except Instance.DoesNotExist:
                pass

        return utils.assign_ebau_nr(self.instance, self.geschaeft.gJahr)
