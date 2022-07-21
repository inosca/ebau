import mimetypes
import re
import shutil
from dataclasses import asdict, fields
from datetime import datetime
from pathlib import Path
from typing import Any, List, Optional

from caluma.caluma_form import api as form_api
from caluma.caluma_form.models import Answer, AnswerDocument, Document, Question
from caluma.caluma_form.validators import CustomValidationError
from caluma.caluma_user.models import BaseUser
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.utils import timezone
from future.moves import itertools

from camac.core.models import WorkflowEntry
from camac.document.models import Attachment, AttachmentSection
from camac.dossier_import.domain_logic import get_or_create_ebau_nr
from camac.dossier_import.dossier_classes import CalumaPlotData, Dossier
from camac.dossier_import.loaders import safe_join
from camac.dossier_import.messages import LOG_LEVEL_WARNING, Message, MessageCodes
from camac.instance.domain_logic import SUBMIT_DATE_FORMAT
from camac.instance.models import Instance


class FieldWriter:
    target: str
    value: Any = None
    name: Optional[str] = None

    def __init__(
        self,
        target: str,
        value=None,
        name=None,
        owner=None,
        context=None,
        column_mapping: Optional[dict] = None,
    ):
        # The field writer allows for static values: set value in the field definition
        # in the writer class (e. g. for required answers)
        self.target = target
        self.value = value
        self.column_mapping = column_mapping
        self.owner = owner
        self.context = context
        self.name = name or target


class CamacNgAnswerWriter(FieldWriter):
    def write(self, instance, value):
        if not value:
            return
        (
            form_field,
            created,
        ) = instance.fields.get_or_create(name=self.target, defaults=dict(value=value))
        if not created:  # pragma: no cover
            form_field.value = value
            form_field.save()


class CamacNgListAnswerWriter(FieldWriter):
    column_mapping = None

    def write(self, instance, values):
        if not values:
            return
        if not any(any(asdict(obj).values()) for obj in values):  # pragma: no cover
            return
        result = []
        for obj in values:
            # Ignore if a dataclass without any meaningful data makes it this far
            if not any(asdict(obj).values()):  # pragma: no cover
                continue
            result.append(
                {
                    column_name: getattr(obj, key, None)
                    for key, column_name in self.column_mapping.items()
                }
            )

        field, created = instance.fields.get_or_create(
            name=self.target, defaults=dict(value=result)
        )
        if not created:  # pragma: no cover
            field.value = result
            field.save()


class CamacNgPersonListAnswerWriter(CamacNgListAnswerWriter):
    """Person and location objects combine address and house number in 1 line."""

    def write(self, instance, value):
        if not value:
            return
        for person in value:
            person.street = safe_join((person.street, person.street_number))
        super().write(instance, value)


class CamacNgStreetWriter(CamacNgAnswerWriter):
    """Combing street and street-number into one field."""

    def write(self, instance, value):
        if not value:
            return
        dossier = self.context.get("dossier")
        super().write(instance, safe_join((dossier.street, dossier.street_number)))


class WorkflowEntryDateWriter(FieldWriter):
    """Writes dates to workflow entries by workflow entry id.

    Make sure to set up application with workflow_items from
    `core.workflowitem` preferably dumped to application's
    `core.json` file.

    NOTE: not all parts of camac-ng frontend treat dates the same way which
    can lead to different dates displayed for the same value when the
    hours of the datetime object are within 2 hours of midnight.
    (Europe/Zurich to UTC offset in winter is -2 hours). Therefore
    The hours are therefore set to noon.
    """

    target: int

    def write(self, instance, value):
        if not value:  # pragma: no cov
            return
        if not timezone.is_aware(value):
            value = timezone.make_aware(value)
        value = value.replace(hour=12)
        entry, created = WorkflowEntry.objects.get_or_create(
            instance=instance,
            workflow_item_id=self.target,
            defaults={"workflow_date": value, "group": instance.group_id},
        )
        if not created:  # pragma: no cover
            entry.workflow_date = value
            entry.save()


class CalumaAnswerWriter(FieldWriter):
    def __init__(self, value_key: str = "value", task: str = None, *args, **kwargs):
        self.value_key = value_key
        self.task = task
        super().__init__(*args, **kwargs)

    def write(self, instance, value):
        if not value:
            return
        try:
            dossier = self.context.get("dossier")
            if self.task:
                work_item = instance.case.work_items.filter(task_id=self.task).first()

                if not work_item:  # pragma: no cover
                    dossier._meta.errors.append(
                        Message(
                            level=LOG_LEVEL_WARNING,
                            code=MessageCodes.INCONSISTENT_WORKFLOW_STATE.value,
                            detail=f"Missing {self.task} work item, cannot write {self.target}",
                        )
                    )
                    return

                document = work_item.document
            else:
                document = instance.case.document
            question = Question.objects.get(slug=self.target)
            try:
                form_api.save_answer(
                    question=question,
                    document=document,
                    value=value,
                    user=BaseUser(
                        username=self.owner._user.username, group=self.owner._group.pk
                    ),
                )
            except CustomValidationError:  # pragma: no cover
                dossier._meta.errors.append(
                    Message(
                        level=LOG_LEVEL_WARNING,
                        code=MessageCodes.FIELD_VALIDATION_ERROR.value,
                        detail=f"Failed to write {value} to {self.target} for dossier {instance}",
                    )
                )
                return

        except ObjectDoesNotExist as e:  # pragma: no cover
            raise RuntimeError(
                f"Failed to write {value} to field {self.target} on {instance} because of : {e}"
            )


class BuildingAuthorityRowWriter(CalumaAnswerWriter):
    # TODO: rewrite this to make due use of `caluma_form.api`
    def write(self, instance, value):
        if not value:
            return
        work_item = instance.case.work_items.filter(
            task_id="building-authority"
        ).first()
        if not work_item:  # pragma: no cover
            dossier = self.context.get("dossier")
            dossier._meta.errors.append(
                Message(
                    level=LOG_LEVEL_WARNING,
                    code=MessageCodes.INCONSISTENT_WORKFLOW_STATE.value,
                    detail=f"Missing building-authority work item, cannot write {self.target}",
                )
            )
            return
        table_answer, _ = Answer.objects.update_or_create(
            question_id="baukontrolle-realisierung-table",
            document=work_item.document,
        )

        if table_answer.documents.count():
            row_document = table_answer.documents.first()
        else:
            row_document = Document.objects.create(
                form=table_answer.question.row_form, family=work_item.document
            )
            AnswerDocument.objects.create(answer=table_answer, document=row_document)

        Answer.objects.create(
            question_id=self.target,
            document=row_document,
            **{self.value_key: value},
        )


class CalumaListAnswerWriter(FieldWriter):
    def write(self, instance, values):  # noqa: C901
        if not values:
            return
        if not any(any(asdict(obj).values()) for obj in values):  # pragma: no cover
            return
        table_question = Question.objects.get(slug=self.target)
        row_documents = []
        for obj in values:
            if not any(asdict(obj).values()):  # pragma: no cover
                continue
            try:
                row_document = form_api.save_document(form=table_question.row_form)
                row_documents.append(row_document)
                for field in fields(obj):
                    value = getattr(obj, field.name)
                    if not value:
                        continue
                    try:
                        form_api.save_answer(
                            question=Question.objects.get(
                                slug=self.column_mapping[field.name]
                            ),
                            value=value,
                            document=row_document,
                            user=BaseUser(
                                username=self.owner._user.username,
                                group=self.owner._group.pk,
                            ),
                        )
                    except CustomValidationError as e:  # pragma: no cover
                        self.context.get("dossier")._meta.errors.append(
                            Message(
                                level=LOG_LEVEL_WARNING,
                                code=MessageCodes.FIELD_VALIDATION_ERROR.value,
                                detail=f"Failed to write {value} for field {field.name} to {self.target} for dossier {instance}: {e}",
                            )
                        )
                        continue

            except (ObjectDoesNotExist, IntegrityError):  # pragma: no cover
                raise RuntimeError(
                    f"Failed to create row_document for table answer {self.target} on {instance}"
                )
        form_api.save_answer(
            document=instance.case.document,
            question=table_question,
            value=[doc.pk for doc in row_documents],
            user=BaseUser(
                username=self.owner._user.username, group=self.owner._group.pk
            ),
        )


class CalumaPlotDataWriter(CalumaListAnswerWriter):
    def write(self, instance, values):
        if not values:
            return
        compiled = []
        dossier = self.context.get("dossier")
        coordinates = dossier.coordinates if dossier else []
        for plot_data, coordinate in itertools.zip_longest(values, coordinates or []):
            compiled.append(
                CalumaPlotData(
                    coord_east=coordinate and float(coordinate.e),
                    coord_north=coordinate and float(coordinate.n),
                    egrid_number=plot_data and str(plot_data.egrid),
                    plot_number=plot_data and str(plot_data.number),
                )
            )
        super().write(instance, compiled)


class CaseMetaWriter(FieldWriter):
    def __init__(self, formatter: str = None, *args, **kwargs):
        self.formatter = formatter
        super().__init__(*args, **kwargs)

    def write(self, instance, value):
        if not value:
            return
        formatted_value = value
        if self.formatter == "datetime-to-string":
            formatted_value = datetime.strftime(value, SUBMIT_DATE_FORMAT)
        instance.case.meta[self.target] = formatted_value
        instance.case.save()


class EbauNumberWriter(CalumaAnswerWriter):
    def write(self, instance, value):  # noqa: C901
        dossier = self.context.get("dossier")
        if not dossier.submit_date:
            detail = (
                f"Failed to write {value} to {self.target} for dossier {instance}",
            )
            dossier._meta.errors.append(
                Message(
                    level=LOG_LEVEL_WARNING,
                    code=MessageCodes.FIELD_VALIDATION_ERROR.value,
                    detail=detail,
                )
            )
            return
        if not value and dossier._meta.target_state == "SUBMITTED":
            # Do not write/create an ebau-number
            return
        value = get_or_create_ebau_nr(
            value, self.owner._group.service, dossier.submit_date
        )
        instance.case.meta["ebau-number"] = value
        instance.case.save()


class DossierWriter:
    def __init__(
        self,
        import_settings: dict = settings.APPLICATION["DOSSIER_IMPORT"],
        *args,
        **kwargs,
    ):
        """Construct writer for importing dossier.

        In order to make a clear difference between importing data fields and functional or
        configuration properties make the latter private properties prefixed with an '_' to
        avoid collision (e.g. user is pretty likely to collide at some point)

        E. g. "_import_settings
        """
        self._import_settings = import_settings

    def create_instance(self, dossier: Dossier) -> Instance:
        """Instance etc erstellen."""
        raise NotImplementedError  # pragma: no cover

    def write_fields(self, instance: Instance, dossier: Dossier):
        for field in fields(dossier):
            writer = getattr(self, field.name, None)
            if writer:
                writer.owner = self
                writer.context = {"dossier": dossier}
                writer.write(instance, getattr(dossier, field.name, None))

    def import_dossier(self, dossier: Dossier) -> Message:
        # instance = self.create_instance(dossier)
        # self.write_fields(instance, dossier)
        # self._handle_dossier_attachments(dossier)
        # self._set_workflow_state(instance, dossier.Meta.target_state)
        raise NotImplementedError  # pragma: no cover

    def _set_workflow_state(self, instance: Instance, target_state: str):
        """Fast-Forward case to Dossier.Meta.target_state."""
        raise NotImplementedError  # pragma: no cover

    def _create_dossier_attachments(
        self, dossier: Dossier, instance: Instance
    ) -> List[Message]:
        """Create attachments for file pointers in dossier's attachments."""
        messages = []
        if not dossier.attachments:
            return messages

        instance_files_path = Path(
            f"{settings.MEDIA_ROOT}/attachments/files/{instance.pk}"
        )

        attachments_path = instance_files_path / str(dossier.id)

        attachments_path.mkdir(parents=True, exist_ok=True)

        for attachment in dossier.attachments:
            target_base_path = f"{settings.MEDIA_ROOT}/attachments/files/{instance.pk}"

            file_path = re.sub(
                # ensure that dossier.id is only removed at the beginning of a path
                r"^{dossier_id}/".format(dossier_id=dossier.id),
                "",
                attachment.name.encode("utf-8", errors="ignore").decode(
                    "utf-8", errors="ignore"
                ),
            )

            # make sub_dirs
            # ensure path exists if directory is not handled individually
            (Path(target_base_path) / "/".join(file_path.split("/")[:-1])).mkdir(
                parents=True, exist_ok=True
            )

            mimetypes.add_type("application/vnd.ms-outlook", ".msg")
            mime_type, _ = mimetypes.guess_type(str(Path(target_base_path) / file_path))

            if not mime_type:
                messages.append(
                    Message(
                        level=LOG_LEVEL_WARNING,
                        code=MessageCodes.MIME_TYPE_UNKNOWN,
                        detail=file_path,
                    )
                )
                continue

            with open(str(Path(target_base_path) / file_path), "wb") as target_file:
                shutil.copyfileobj(attachment.file_accessor, target_file)

                attachment = Attachment.objects.create(
                    instance=instance,
                    user=self._user,
                    service=self._group.service,
                    group=self._group,
                    name=file_path,
                    context={},
                    path=f"attachments/files/{instance.pk}/{file_path}",
                    size=target_file.tell(),
                    date=timezone.localtime(),
                    mime_type=mime_type,
                )
                attachment_section = AttachmentSection.objects.get(
                    attachment_section_id=self._import_settings["ATTACHMENT_SECTION_ID"]
                )
                attachment_section.attachments.add(attachment)

        return messages

    def _ensure_retrieveable(self):
        """Make imported dossiers identifiable.

        E. g. client deployment specific location for storing `internal id`
        """
        raise NotImplementedError  # pragma: no cover
