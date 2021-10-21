import mimetypes
import shutil
import zipfile
from dataclasses import dataclass
from pathlib import Path

from caluma.caluma_core.events import on
from caluma.caluma_user.models import BaseUser
from caluma.caluma_workflow import api as workflow_api
from caluma.caluma_workflow.api import skip_work_item
from caluma.caluma_workflow.events import pre_skip_work_item
from caluma.caluma_workflow.models import WorkItem
from dataclasses_json import dataclass_json
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.utils.timezone import now

from camac.caluma.extensions.events.general import get_caluma_setting
from camac.document.models import Attachment, AttachmentSection
from camac.dossier_import.dossier_classes import Dossier
from camac.dossier_import.importers import DossierImporter
from camac.dossier_import.loaders import InvalidImportDataError, XlsxFileDossierLoader
from camac.dossier_import.writers import (
    CamacNgAnswerFieldWriter,
    CamacNgListAnswerWriter,
    DossierWriter,
)
from camac.instance.domain_logic import CreateInstanceLogic
from camac.instance.models import Form, Instance, InstanceState
from camac.user.models import Group, Location


@on(pre_skip_work_item, raise_exception=True)
@transaction.atomic
def handle_pre_skip_work_item_in_import(sender, work_item, user, **kwargs):
    config = get_caluma_setting("PRE_COMPLETE")
    config.pop("depreciate-case", None)
    config = config.get(work_item.task_id)
    # skip side effects in task `make-decision`
    if config:
        for action_name, tasks in config.items():
            action = getattr(workflow_api, f"{action_name}_work_item")

            for item in work_item.case.work_items.filter(
                task_id__in=tasks, status=WorkItem.STATUS_READY
            ):
                action(item, user)


PERSON_MAPPING = {
    "company": "firma",
    "last_name": "name",
    "first_name": "vorname",
    "street": "strasse",
    "zip": "plz",
    "town": "ort",
    "phone": "tel",
    "email": "email",
}

PARCEL_MAPPING = {"egrid": "egrid", "number": "number", "municipality": "municipality"}

COORDINATES_MAPPING = {"e": "lat", "n": "lng"}

LOG_LEVEL_DEBUG = 0
LOG_LEVEL_INFO = 1
LOG_LEVEL_WARNING = 2
LOG_LEVEL_ERROR = 3


@dataclass_json
@dataclass
class Message:
    level: int
    message: dict


class ConfigurationError(Exception):
    pass


class KtSchwyzDossierWriter(DossierWriter):
    id: str = CamacNgAnswerFieldWriter(target="kommunale-gesuchsnummer")
    proposal = CamacNgAnswerFieldWriter(target="bezeichnung")
    cantonal_id = CamacNgAnswerFieldWriter(target="kantonale-gesuchsnummer")
    parcel = CamacNgListAnswerWriter(target="parzellen", column_mapping=PARCEL_MAPPING)
    coordinates = CamacNgListAnswerWriter(
        target="punkte", column_mapping=COORDINATES_MAPPING
    )
    address = None
    usage = CamacNgAnswerFieldWriter(target="betroffene-nutzungszonen")
    type = CamacNgAnswerFieldWriter(target="verfahrensart-migriertes-dossier")
    publication_date = CamacNgAnswerFieldWriter(
        target="publikationsdatum", renderer="datetime"
    )
    construction_start_date = CamacNgAnswerFieldWriter(
        target="datum-baubeginn", renderer="datetime"
    )
    profile_approval_date = CamacNgAnswerFieldWriter(
        target="datum-schnurgeruestabnahme", renderer="datetime"
    )
    decision_date = CamacNgAnswerFieldWriter(target="tb-datum", renderer="datetime")
    final_approval_date = CamacNgAnswerFieldWriter(
        target="datum-schlussabnahme", renderer="datetime"
    )
    completion_date = CamacNgAnswerFieldWriter(
        target="datum-bauende", renderer="datetime"
    )
    link = CamacNgAnswerFieldWriter(target="link")
    custom_1 = CamacNgAnswerFieldWriter(target="freies-textfeld-1")
    custom_2 = CamacNgAnswerFieldWriter(target="freies-textfeld-2")
    applicant = CamacNgListAnswerWriter(
        target="bauherrschaft", column_mapping=PERSON_MAPPING
    )
    landowner = CamacNgListAnswerWriter(
        target="grundeigentumerschaft", column_mapping=PERSON_MAPPING
    )
    project_author = CamacNgListAnswerWriter(
        target="projektverfasser-planer", column_mapping=PERSON_MAPPING
    )

    def create_instance(self, dossier: Dossier) -> Instance:
        """Create a Camac NG Instance with a case.

        camac.instance.domain_logic.CreateInstanceLogic should be able to do the job and
        spit out a reasonably generic starting point.
        """
        instance_state_id = self.importer.settings["INSTANCE_STATE_MAPPING"].get(
            dossier._meta.target_state
        )
        instance_state = instance_state_id and InstanceState.objects.get(
            pk=instance_state_id
        )
        creation_data = dict(
            instance_state=InstanceState.objects.get(
                pk=self.importer.settings["INSTANCE_STATE_MAPPING"][
                    dossier._meta.target_state
                ]
            ),
            previous_instance_state=instance_state,
            user=self.importer.user,
            group=self.importer.group,
            form=Form.objects.get(pk=self.importer.settings["FORM_ID"]),
        )
        instance = (
            CreateInstanceLogic.create(  # TODO: check if this instance is any good
                creation_data,
                caluma_user=BaseUser(),
                camac_user=self.importer.user,
                group=self.importer.group,
            )
        )
        ebau_number_prefix = f"IM-{self.importer.group.pk}-{dossier.submit_date.year}"
        last_seq = (
            Instance.objects.filter(identifier__startswith=ebau_number_prefix)
            .order_by("-identifier")
            .values_list("identifier", flat=True)
        )
        next_seq = int(last_seq[0].split("-")[-1]) + 1 if last_seq else 1
        ebau_number = f"{ebau_number_prefix}-{next_seq:04}"
        instance.identifier = ebau_number
        instance.save()
        return instance

    def import_dossier(self, dossier: Dossier):
        message = Message(level=LOG_LEVEL_INFO, message={"dossier": dossier.id})

        if dossier._meta.missing:
            message.level = LOG_LEVEL_WARNING
            message.message["action"] = "dossier skipped"
            message.message[
                "reason"
            ] = f"missing values in required fields: {dossier._meta.missing}"
            self.importer.import_case.messages.append(message.to_dict())
            self.importer.import_case.save()
            return
        if Instance.objects.filter(
            fields__name="kommunale-gesuchsnummer",
            fields__value=dossier.id,
            group_id=self.importer.group.pk,
        ).first():
            message.level = LOG_LEVEL_WARNING
            message.message["action"] = "dossier skipped"
            message.message[
                "reason"
            ] = f"Dossier with `kantonale gesuchsnummer` {dossier.cantonal_id} already exists."
            self.importer.import_case.messages.append(message.to_dict())
            self.importer.import_case.save()
            return
        instance = self.create_instance(dossier)
        instance.location = self.importer.location
        instance.save()
        instance.case.meta["import-id"] = str(self.importer.import_case.pk)
        instance.case.save()
        message.message["instance_id"] = instance.pk
        self.write_fields(instance, dossier)
        message.message["import"] = "success"
        self.importer.import_case.save()
        self._create_dossier_attachments(dossier, instance)
        workflow_message = self._set_workflow_state(
            instance, dossier._meta.target_state
        )
        message.level = workflow_message.level
        message.message["set_workflow_state"] = workflow_message

    def _create_dossier_attachments(self, dossier: Dossier, instance: Instance):
        """Create attachments for dossier.

        Ignore if archive holds no documents directory
        """

        documents_dir = Path(self.importer.additional_data_source) / str(dossier.id)
        if not documents_dir.exists():
            return

        for document in documents_dir.iterdir():
            path = f"{settings.MEDIA_ROOT}/attachments/files/{instance.pk}"
            Path(path).mkdir(parents=True, exist_ok=True)
            target_file = Path(path) / document.name
            shutil.copyfile(document, str(target_file))

            mime_type, _ = mimetypes.guess_type(target_file)

            attachment = Attachment.objects.create(
                instance=instance,
                user=self.importer.user,
                service=self.importer.group.service,
                group=self.importer.group,
                name=document.name,
                context={},
                path=str(target_file),
                size=target_file.stat().st_size,
                date=now(),
                mime_type=mime_type,
            )
            attachment_section = AttachmentSection.objects.get(
                attachment_section_id=self.importer.settings["ATTACHMENT_SECTION_ID"]
            )
            attachment_section.attachments.add(attachment)

    def _set_workflow_state(self, instance: Instance, target_state) -> Message:
        """Advance instance's case through defined workflow sequence to target state.

        In order to advance to a specified worklow state after every flow all tasks need to be
        in a status other than ready so that the relevant work_item can be completed.

        Therefore every target_state needs to be informed on the sibling work-items and how to handle
        them before completion and progression to the next task in line.

        This is configured in the following:

        <TARGETSTATE> = [
            (<task_to_complete>: [<task_to_sikp>, ... ]),
            ...
        ]

        If required this could be extended with the option to handle sibling tasks differently on each stage, such
         as cancelling them instead of skipping.
        """
        message = Message(level=LOG_LEVEL_INFO, message="")

        # configure workflow state advance path and strategies
        SUBMITTED = ["submit"]
        APPROVED = SUBMITTED + [
            "complete-check",
            "skip-circulation",
            "make-decision",
        ]
        DONE = APPROVED + ["archive-instance"]

        path_to_state = {"SUBMITTED": SUBMITTED, "APPROVED": APPROVED, "DONE": DONE}

        default_context = {"no-notification": True}

        camac_user = self.importer.user

        caluma_user = BaseUser(username=camac_user.name, group=self.importer.group.pk)
        caluma_user.camac_group = self.importer.group.pk

        # In order for a work item to be completed no sibling work items can be
        # in state ready. They have to be dealt with in advance.
        for task_id in path_to_state[target_state]:
            try:
                work_item = instance.case.work_items.get(task_id=task_id)
            except ObjectDoesNotExist as e:
                message.level = LOG_LEVEL_WARNING
                message.message = f"Skip work item with task_id {task_id} failed with {ConfigurationError(e)}."
                continue
            # overwrite side effects for import
            config = get_caluma_setting("PRE_COMPLETE")
            # skip side effects in task `make-decision`
            config and config.pop("depreciate-case", None)
            config = config and config.get(work_item.task_id)
            if config:
                for action_name, tasks in config.items():
                    action = getattr(workflow_api, f"{action_name}_work_item")

                    for item in work_item.case.work_items.filter(
                        task_id__in=tasks, status=WorkItem.STATUS_READY
                    ):
                        action(item, caluma_user)
            skip_work_item(work_item, user=caluma_user, context=default_context)
        return message


class KtSchwyzXlsxDossierImporter(DossierImporter):
    """
    Dossier Importer for Kt Schwyz for importing ZIP archives of dossiers with attachments.

    The importer expects an archive that holds metadata on dossiers and attachments in directories
    per dossier.
    It will extract from dossier_import.zip to the temporary import dir e.g.
     /tmp/dossier-import/<import_case_id>/
        - file: `dossiers.xlsx`
        - dir: attachments/
    Then create an instance with a case, fill in form data and other properties from metadata,  handle attachments
     and "work" through workitems to suit the target state after import.
    """

    loader_class = XlsxFileDossierLoader

    def initialize(
        self, group_id: int, location_id: int, path_to_archive: str, *args, **kwargs
    ):
        """Initialize the import of a ZIP-Archive of dossiers.

        For Camac Dossier import kt_schwyz we require to identify the location/communality the
        imported dossiers belong to. This is done via `group_id` that relates to service.
        user_id selects the user doing the import.
        """
        super().initialize()
        path = Path(self.temp_dir.name) / str(self.import_case.id)
        Path(path).mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(path_to_archive, "r") as archive:
            path = Path(self.temp_dir.name) / str(self.import_case.id)
            for fileinfo in archive.infolist():
                filename = fileinfo.filename
                if filename.endswith("/"):
                    attachment_dir = path / filename
                    attachment_dir.mkdir(parents=True, exist_ok=True)
                    continue
                with open(f"{str(path)}/{filename}", "wb") as f:
                    shutil.copyfileobj(archive.open(fileinfo.filename), f)
            dossiers_filepath = str(path / "dossiers.xlsx")
        loader = self.get_loader()
        self.loader = loader(dossiers_filepath)
        self.group = Group.objects.get(pk=group_id)
        self.location = Location.objects.get(pk=location_id)
        self.import_case.service = self.group.service
        self.import_case.save()

        # The additional data source point to the directory where the documents have been
        # extracted to because they potentially are to big in size for handling them in memory.
        self.additional_data_source = str(
            Path(self.temp_dir.name) / str(self.import_case.id)
        )

    @transaction.atomic
    def import_dossiers(self):
        writer = KtSchwyzDossierWriter(importer=self)
        try:
            for dossier in self.loader.load():
                writer.import_dossier(dossier)
        except InvalidImportDataError as e:
            message = Message(
                level=LOG_LEVEL_ERROR,
                message=f"Import failed because of bad import data: {e}",
            ).to_dict()
            self.import_case.messages.append(message)
            self.import_case.save()
            raise
