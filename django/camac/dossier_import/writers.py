import hashlib
import logging
import re
import traceback
from dataclasses import asdict, fields
from datetime import datetime
from pathlib import Path
from typing import Any, List, Optional

import magic
from caluma.caluma_form import api as form_api
from caluma.caluma_form.models import Answer, AnswerDocument, Document, Question
from caluma.caluma_user.models import BaseUser
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File
from django.db import IntegrityError
from django.utils import timezone
from django.utils.translation import gettext as _
from future.moves import itertools
from rest_framework.exceptions import ValidationError

from camac.core.models import WorkflowEntry
from camac.document.models import Attachment, AttachmentSection
from camac.dossier_import.domain_logic import get_or_create_ebau_nr
from camac.dossier_import.dossier_classes import CalumaPlotData, Dossier
from camac.dossier_import.loaders import safe_join
from camac.dossier_import.messages import Message, MessageCodes, Severity
from camac.instance.domain_logic import SUBMIT_DATE_FORMAT
from camac.instance.models import Instance
from camac.user.models import Group, User

log = logging.getLogger("dossier_import")


class FieldWriter:
    target: str
    value: Any = None
    name: Optional[str] = None
    protected: bool = False

    def __init__(
        self,
        target: str,
        value=None,
        name=None,
        owner=None,
        context=None,
        column_mapping: Optional[dict] = None,
        protected: bool = False,
    ):
        # The field writer allows for static values: set value in the field definition
        # in the writer class (e. g. for required answers)
        # The `protected` keyword protects the field to be deleted on a reimport.

        self.target = target
        self.value = value
        self.column_mapping = column_mapping
        self.owner = owner
        self.context = context
        self.name = name or target
        self.protected = protected

    def can_delete(self):  # pragma: no cover TODO: cover
        if not self.protected:
            return True
        if dossier := self.context.get("dossier"):
            dossier._meta.errors.append(
                Message(
                    level=Severity.WARNING.value,
                    code=MessageCodes.WRITING_READ_ONLY_FIELD.value,
                    detail=f"Ignoring {self.owner.delete_keyword} on field {self.target} (readonly).",
                )
            )
        return False


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
    def __init__(
        self,
        task: str = None,
        formatter: str = None,
        *args,
        **kwargs,
    ):
        self.task = task
        self.formatter = formatter
        super().__init__(*args, **kwargs)

    def write(self, instance, value):
        if not value:
            return
        if self.formatter == "to-string":
            value = str(value)
        try:
            dossier = self.context.get("dossier")
            if self.task:
                work_item = instance.case.work_items.filter(task_id=self.task).first()

                if not work_item:  # pragma: no cover
                    dossier._meta.errors.append(
                        Message(
                            level=Severity.WARNING.value,
                            code=MessageCodes.INCONSISTENT_WORKFLOW_STATE.value,
                            detail=f"Missing {self.task} work item, cannot write {self.target}",
                        )
                    )
                    return

                document = work_item.document
            else:
                document = instance.case.document
            question = Question.objects.get(slug=self.target)
            if (
                question.type == "text"
                and question.max_length
                and question.max_length < len(value)
            ):
                value = value[: question.max_length - 3] + "..."
                dossier._meta.warnings.append(
                    Message(
                        level=Severity.WARNING.value,
                        code=MessageCodes.FIELD_VALIDATION_ERROR.value,
                        detail=_(
                            'Value "%(value)s" in field %(target)s is too long (max: %(max)s)'
                        )
                        % dict(
                            value=value, target=self.target, max=question.max_length
                        ),
                    )
                )
            try:
                form_api.save_answer(
                    question=question,
                    document=document,
                    value=value,
                    user=BaseUser(
                        username=self.owner._user.username, group=self.owner._group.pk
                    ),
                )
            except ValidationError:  # pragma: no cover
                dossier._meta.errors.append(
                    Message(
                        level=Severity.WARNING.value,
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
                    level=Severity.WARNING.value,
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

        question = Question.objects.get(pk=self.target)
        try:
            form_api.save_answer(
                question=question,
                document=row_document,
                value=value,
                user=BaseUser(
                    username=self.owner._user.username, group=self.owner._group.pk
                ),
            )
        except ValidationError:  # pragma: no cover
            dossier._meta.errors.append(
                Message(
                    level=Severity.WARNING.value,
                    code=MessageCodes.FIELD_VALIDATION_ERROR.value,
                    detail=f"Failed to write {value} to {self.target} for dossier {instance}",
                )
            )
            return


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
                        question = Question.objects.get(
                            slug=self.column_mapping[field.name]
                        )

                        # Some fields are parsed as integer but are not written
                        # into an integer field in every canton
                        if question.type in [
                            Question.TYPE_TEXT,
                            Question.TYPE_TEXTAREA,
                        ]:
                            value = str(value)

                        form_api.save_answer(
                            question=question,
                            value=value,
                            document=row_document,
                            user=BaseUser(
                                username=self.owner._user.username,
                                group=self.owner._group.pk,
                            ),
                        )
                    except ValidationError:  # pragma: no cover
                        self.context.get("dossier")._meta.errors.append(
                            Message(
                                level=Severity.WARNING.value,
                                code=MessageCodes.FIELD_VALIDATION_ERROR.value,
                                detail=f"Failed to write {value} for field {field.name} to {self.target} for dossier {instance}.",
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
                    level=Severity.WARNING.value,
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
        user_id,
        group_id: int,
        *args,
        **kwargs,
    ):
        """Construct writer for importing dossier.

        In order to make a clear difference between importing data fields and functional or
        configuration properties make the latter private properties prefixed with an '_' to
        avoid collision (e.g. user is pretty likely to collide at some point)
        """
        self._user = user_id and User.objects.get(pk=user_id)
        self._group = Group.objects.get(pk=group_id)
        self._caluma_user = BaseUser(
            username=self._user.username, group=self._group.service.pk
        )
        self._caluma_user.camac_group = self._group.pk

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

    def existing_dossier(self, dossier_id):
        """Return the instance identified by dossier_id.

        Different configs use different methods to identify instances. This
        is just an abstraction that is needed for retrieving instances
        when reimporting dossiers.
        """
        raise NotImplementedError  # pragma: no cover

    def set_dossier_id(self, instance, dossier_id):
        """Make the instance retrievable by dossier_id.

        The reverse of `self.existing_dossier`
        """
        raise NotImplementedError  # pragma: no cover

    def _set_workflow_state(self, instance: Instance, target_state: str):
        """Fast-Forward case to Dossier.Meta.target_state."""
        raise NotImplementedError  # pragma: no cover

    def _create_dossier_attachments(
        self, dossier: Dossier, instance: Instance
    ) -> List[Message]:
        """Create attachments for files in dossier's attachments.

        This will get the file-name after stripping the dossier-id from the
        path.

        python-magic is used to guess the MIME type.

        If an attachment by that name already exists the contents will be
        replaced, rather than creating a new one
        """
        messages = []
        if not dossier.attachments:
            return messages

        instance_files_path = Path(
            f"{settings.MEDIA_ROOT}/attachments/files/{instance.pk}"
        )

        attachments_path = instance_files_path / str(dossier.id)

        attachments_path.mkdir(parents=True, exist_ok=True)
        for document in dossier.attachments:
            content = File(document.file_accessor)

            file_path = re.sub(
                # ensure that dossier.id is only removed at the beginning of a path
                r"^{dossier_id}/".format(dossier_id=dossier.id),
                "",
                document.name.encode("utf-8", errors="ignore").decode(
                    "utf-8", errors="ignore"
                ),
            )

            mimimi = magic.Magic(mime=True, uncompress=True)
            mime_type = mimimi.from_buffer(content.file.read())
            content.file.seek(0)

            if not mime_type:  # pragma: no cover
                messages.append(
                    Message(
                        level=Severity.WARNING.value,
                        code=MessageCodes.MIME_TYPE_UNKNOWN,
                        detail=file_path,
                    )
                )
                continue

            defaults = dict(
                user=self._user,
                instance=instance,
                service=self._group.service,
                group=self._group,
                name=file_path,
                size=content.size,
                context={},
                date=timezone.localtime(),
                mime_type=mime_type,
            )

            attachment, created = Attachment.objects.get_or_create(
                instance=instance,
                name=file_path,
                defaults=defaults,
            )

            # If an attachment by the same name exists we'll overwrite the file, unless the data is identical.
            # Django's own `FileField.path.save` method cannot be used because it would create another
            # file with a random suffix, thus cluttering the file system.
            if not created:  # pragma: no cover   TODO: cover
                if (
                    hashlib.md5(attachment.path.file.read()).digest()
                    == hashlib.md5(content.read()).digest()
                ):
                    continue
                content.seek(0)
                try:
                    with Path(attachment.path.path).open("wb") as file:
                        file.write(content.read())
                except OSError as e:  # pragma: no cover
                    tb = traceback.format_exc()
                    log.exception(tb)
                    messages.append(
                        Message(
                            level=Severity.ERROR.value,
                            code=MessageCodes.UNHANDLED_EXCEPTION,
                            detail=f"Something went wrong replacing '{file_path}' with error: {e}",
                        )
                    )
                    continue
                defaults["size"] = attachment.path.size
                Attachment.objects.filter(pk=attachment.pk).update(**defaults)
                messages.append(
                    Message(
                        level=Severity.INFO.value,
                        code=MessageCodes.ATTACHMENT_UPDATED.value,
                        detail=attachment.name,
                    )
                )
                continue
            attachment.path.save(file_path, content, save=True)
            if created:
                attachment_section = AttachmentSection.objects.get(
                    attachment_section_id=settings.DOSSIER_IMPORT[
                        "ATTACHMENT_SECTION_ID"
                    ]
                )
                attachment_section.attachments.add(attachment)
            att_sec = (
                attachment.attachment_sections.filter(
                    attachment_section_id=settings.DOSSIER_IMPORT[
                        "ATTACHMENT_SECTION_ID"
                    ]
                )
                .values("name", "attachment_section_id")
                .first()
            )
            messages.append(
                Message(
                    level=Severity.INFO.value,
                    code=MessageCodes.ATTACHMENT_CREATED.value,
                    detail=f"{attachment.name} ({attachment.mime_type}) in section {'{name} ({attachment_section_id})'.format(**att_sec)}",
                )
            )
        return messages
