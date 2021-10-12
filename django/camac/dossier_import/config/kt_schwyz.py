import mimetypes
import shutil
import zipfile
from pathlib import Path
from typing import List

from caluma.caluma_user.models import BaseUser
from caluma.caluma_workflow.api import skip_work_item
from django.conf import settings
from django.db import transaction
from django.utils.timezone import now

from camac.document.models import Attachment, AttachmentSection
from camac.dossier_import.dossier_classes import Dossier
from camac.dossier_import.importers import DossierImporter
from camac.dossier_import.loaders import XlsxFileDossierLoader
from camac.dossier_import.writers import (
    CamacNgAnswerFieldWriter,
    CamacNgListAnswerWriter,
    DossierWriter,
)
from camac.instance.domain_logic import CreateInstanceLogic
from camac.instance.models import Form, Instance, InstanceState
from camac.user.models import Group, Service, User

PERSON_MAPPING = {
    "last_name": "name",
    "first_name": "vorname",
    "street": "strasse",
    "zip": "plz",
    "town": "ort",
}


class KtSchwyzDossierWriter(DossierWriter):
    id: str = CamacNgAnswerFieldWriter(target="kommunale-gesuchsnummer")
    proposal = CamacNgAnswerFieldWriter(target="bezeichnung")
    cantonal_id = CamacNgAnswerFieldWriter(target="kantonale-gesuchsnummer")
    parcel = CamacNgAnswerFieldWriter(target="parzellen")
    egrid = None
    coordinates = CamacNgAnswerFieldWriter(target="punkte", renderer="coordinates")
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
        camac_user = User.objects.get(username=self.importer.settings["USER"])
        group = Group.objects.get(
            service_id=self.importer.import_case.service.pk,
            role_id=self.importer.settings["ROLE_ID_GROUP"],
        )
        instance_state = InstanceState.objects.get(
            pk=self.importer.settings["INSTANCE_STATE_MAPPING"][
                dossier.Meta.target_state
            ]
        )
        creation_data = dict(
            instance_state=InstanceState.objects.get(
                pk=self.importer.settings["INSTANCE_STATE_MAPPING"][
                    dossier.Meta.target_state
                ]
            ),
            previous_instance_state=instance_state,
            user=camac_user,
            group=group,
            form=Form.objects.get(pk=self.importer.settings["FORM_ID"]),
            # ebau number (??) mitgeben, präfix für import (default: jahreszal und nummer, e. g. `AV`-
        )
        instance = (
            CreateInstanceLogic.create(  # TODO: check if this instance is any good
                creation_data,
                caluma_user=BaseUser(),
                camac_user=camac_user,
                group=group,
            )
        )
        return instance

    def import_dossier(self, dossier: Dossier):
        message = {"dossier": dossier.id}
        instance = self.create_instance(dossier)
        message["instance_id"] = instance.pk
        self.write_fields(instance, dossier)
        message["import"] = "success"
        self.importer.import_case.messages.append(message)
        self.importer.import_case.save()
        # TODO: implement setting on workflow state on import
        self._set_workflow_state(instance, dossier.Meta.target_state)

    def _handle_dossier_attachments(self, dossier: Dossier, instance: Instance):
        """Create attachments for dossier."""

        user = User.objects.get(username=self.importer.settings["USER"])
        group = Group.objects.get(
            service_id=self.importer.import_case.service.pk,
            role_id=self.importer.settings["ROLE_ID_GROUP"],
        )

        documents_dir = Path(self.importer.additional_data_source) / str(dossier.id)

        for document in documents_dir.iterdir():
            path = f"{settings.MEDIA_ROOT}/attachments/files/{instance.pk}"
            Path(path).mkdir(parents=True, exist_ok=True)
            target_file = Path(path) / document.name
            shutil.copyfile(document, str(target_file))

            mime_type, _ = mimetypes.guess_type(target_file)

            attachment = Attachment.objects.create(
                instance=instance,
                user=user,
                service=group.service,
                group=group,
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

    def _set_workflow_state(self, instance: Instance, target_state) -> List[dict]:
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
        messages = []

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

        caluma_user = BaseUser(
            username=self.importer.settings["USER"],
            group=self.importer.import_case.service.pk,
        )
        caluma_user.camac_group = Group.objects.get(
            service_id=self.importer.import_case.service.pk,
            role_id=self.importer.settings["ROLE_ID_GROUP"],
        ).pk

        # In order for a work item to be completed no sibling work items can be
        # in state ready. They have to be dealt with in advance.
        for task_id in path_to_state[target_state]:
            work_item = instance.case.work_items.get(task_id=task_id)
            if work_item.status in [
                work_item.STATUS_COMPLETED,
                work_item.STATUS_SKIPPED,
            ]:
                continue
            try:
                skip_work_item(work_item, user=caluma_user, context=default_context)
            except Exception as e:
                messages.append(
                    {
                        "set_workflow_state": f"Skip work item with task_id {task_id} failed with {e}."
                    }
                )
        messages.append(
            {
                "set_workflow_state": f"Advance workflow state to {target_state} successful."
            }
        )
        return messages


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

    def initialize(self, service_id: int, path_to_archive: str, *args, **kwargs):
        """Initialize the import of a ZIP-Archive of dossiers.

        For Camac Dossier import kt_schwyz we require to identify the location/communality the
        imported dossiers belong to. This is done via `service_id`. It will be later used to
        set the correct group on the `Instance` created for all dossiers.
        """
        super().initialize()
        path = Path(self.temp_dir) / str(self.import_case.id)
        Path(path).mkdir(parents=True, exist_ok=True)
        try:
            with zipfile.ZipFile(path_to_archive, "r") as archive:
                path = Path(self.temp_dir) / str(self.import_case.id)
                archive.extractall(path=path)
                dossiers_filepath = str(path / "dossiers.xlsx")
        except FileNotFoundError:
            raise
        loader = self.get_loader()
        self.loader = loader(dossiers_filepath)
        self.import_case.service = Service.objects.get(pk=service_id)
        self.import_case.save()

        # The additional data source point to the directory where the documents have been
        # extracted to because they potentially are to big in size for handling them in memory.
        self.additional_data_source = str(
            Path(self.temp_dir) / str(self.import_case.id)
        )

    @transaction.atomic
    def import_dossiers(self):
        writer = KtSchwyzDossierWriter(importer=self)
        writer.import_from_loader(self.loader)
