import mimetypes
import shutil
from pathlib import Path

from caluma.caluma_user.models import BaseUser
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
from camac.user.models import Group, User

PERSON_MAPPING = {
    "last_name": "name",
    "first_name": "vorname",
    "street": "strasse",
    "zip": "plz",
    "town": "ort",
}


class KtSchwyzDossierWriter(DossierWriter):
    id: str = None
    proposal = CamacNgAnswerFieldWriter(target="bezeichnung")
    cantonal_id = None
    parcel = None
    egrid = None
    coordinates = None
    address = None
    usage = None
    type = None
    publication_date = None
    decision_date = None
    construction_start_date = None
    profile_approval_date = None
    completion_date = None
    link = None
    applicant = CamacNgListAnswerWriter(
        target="bauherrschaft", column_mapping=PERSON_MAPPING
    )
    landowner = None
    project_author = None

    def __init__(self, dossier: Dossier):
        self.Meta.dossier = dossier
        # we need access to dossier's instance and case for writing
        for field in self.Meta.dataclass.__dataclass_fields__.keys():
            prop = getattr(self, field)
            if prop:
                prop.owner = self
                prop.value = getattr(self.Meta.dossier, field)


class KtSchwyzXlsxDossierImporter(DossierImporter):
    loader_class = XlsxFileDossierLoader
    dossier_writer = KtSchwyzDossierWriter

    @transaction.atomic
    def _handle_dossier(self, dossier: Dossier):
        dossier.Meta.instance = self._create_instance(dossier)
        writer = self.dossier_writer(dossier)
        writer.write_all()
        self._handle_dossier_attachments(dossier)
        self._set_workflow_state()

    def _create_instance(self, dossier: Dossier) -> Instance:
        """Create a Camac NG Instance with a case.

        camac.instance.domain_logic.CreateInstanceLogic should be able to do the job and
        spit out a reasonably generic starting point.
        """
        camac_user = User.objects.get(username=self.settings["USER"])
        group = Group.objects.get(name=self.settings["GROUP"])
        instance_state = InstanceState.objects.get(
            pk=self.settings["INSTANCE_STATE_MAPPING"][dossier.Meta.target_state]
        )
        creation_data = dict(
            instance_state=InstanceState.objects.get(
                pk=self.settings["INSTANCE_STATE_MAPPING"][dossier.Meta.target_state]
            ),
            previous_instance_state=instance_state,
            user=camac_user,
            group=group,
            form=Form.objects.get(pk=self.settings["FORM_ID"]),
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

    def _validate_dossier_attachment(self, dossier: Dossier) -> bool:
        pass

    def _handle_dossier_attachments(self, dossier: Dossier):
        """Create attachments for dossier."""

        user = User.objects.get(username=self.settings["USER"])
        group = Group.objects.get(name=self.settings["GROUP"])

        documents_dir = Path(self.temp_dir) / str(self.import_case.id) / str(dossier.id)

        for document in documents_dir.iterdir():
            path = f"{settings.MEDIA_ROOT}/attachments/files/{dossier.Meta.instance.pk}"
            Path(path).mkdir(parents=True, exist_ok=True)
            target_file = Path(path) / document.name
            shutil.copyfile(document, str(target_file))

            mime_type, _ = mimetypes.guess_type(target_file)

            attachment = Attachment.objects.create(
                instance=dossier.Meta.instance,
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
                attachment_section_id=self.settings["ATTACHMENT_SECTION_ID"]
            )
            attachment_section.attachments.add(attachment)

    def _set_workflow_state(self):
        """Fast-Forward case to Dossier.Meta.target_state."""
        pass

    def _ensure_retrieveable(self):
        """Make imported dossier appear in results when searched for by internal id."""
        pass
