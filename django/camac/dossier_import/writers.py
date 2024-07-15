import hashlib
import logging
import re
import traceback
import weakref
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
from django.db import IntegrityError, transaction
from django.utils import timezone
from django.utils.translation import gettext as _
from future.moves import itertools
from rest_framework.exceptions import ValidationError

from camac.core.models import WorkflowEntry
from camac.dossier_import.domain_logic import get_or_create_ebau_nr
from camac.dossier_import.dossier_classes import CalumaPlotData, Dossier
from camac.dossier_import.loaders import safe_join
from camac.dossier_import.messages import (
    DOSSIER_IMPORT_STATUS_ERROR,
    DOSSIER_IMPORT_STATUS_SUCCESS,
    DOSSIER_IMPORT_STATUS_WARNING,
    DossierSummary,
    FieldValidationMessage,
    Message,
    MessageCodes,
    Severity,
    get_message_max_level,
)
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
        value_mapping: Optional[dict] = None,
        protected: bool = False,
    ):
        # The field writer allows for static values: set value in the field definition
        # in the writer class (e. g. for required answers)
        # The `protected` keyword protects the field to be deleted on a reimport.

        self.target = target
        self.value = value
        self.column_mapping = column_mapping
        self.value_mapping = value_mapping
        self.owner = weakref.proxy(owner) if owner else None
        self.context = context
        self.name = name or target
        self.protected = protected

    @property
    def can_delete(self):  # pragma: todo cover
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

        form_field = instance.fields.filter(name=self.target).first()
        if value == self.owner.delete_keyword:
            if self.can_delete and form_field:
                form_field.delete()
                if dossier := self.context.get("dossier"):
                    dossier._meta.warnings.append(
                        FieldValidationMessage(
                            level=Severity.INFO.value,
                            code=MessageCodes.VALUE_DELETED.value,
                            field=self.target,
                            detail="Value deleted",
                        )
                    )
            return
        form_field = form_field or instance.fields.create(name=self.target, value=value)
        if form_field.value != value:
            form_field.value = value
            form_field.save()


class CamacNgListAnswerWriter(CamacNgAnswerWriter):
    column_mapping = None

    def write(self, instance, values):
        if not values:
            return
        if values == self.owner.delete_keyword or any(
            [val == self.owner.delete_keyword for val in values]
        ):
            return super().write(instance, self.owner.delete_keyword)

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
        super().write(instance, result)


class CamacNgPersonListAnswerWriter(CamacNgListAnswerWriter):
    """Person and location objects combine address and house number in 1 line."""

    def write(self, instance, value):
        if not value:
            return
        if any([val == self.owner.delete_keyword for val in value]):
            return super().write(instance, self.owner.delete_keyword)

        for person in value:
            person.street = safe_join((person.street, person.street_number))
        super().write(instance, value)


class CamacNgStreetWriter(CamacNgAnswerWriter):
    """Combine street and street-number into one field."""

    def write(self, instance, value):
        if not value:
            return
        dossier = self.context.get("dossier")
        value = (
            value
            if value == self.owner.delete_keyword
            else safe_join((dossier.street, dossier.street_number))
        )
        super().write(instance, value)


class WorkflowEntryDateWriter(FieldWriter):
    """Write dates to workflow entries by workflow entry id.

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
        entry = WorkflowEntry.objects.filter(
            instance=instance, workflow_item_id=self.target
        ).first()
        if value == self.owner.delete_keyword:
            if not self.can_delete:  # pragma: no cover
                return
            if entry:
                entry.delete()
            return

        if not timezone.is_aware(value):
            value = timezone.make_aware(value)
        value = value.replace(hour=12)

        if not entry:
            WorkflowEntry.objects.create(
                instance=instance,
                workflow_item_id=self.target,
                workflow_date=value,
                group=instance.group_id,
            )
            return
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

                if not work_item:
                    if value == self.owner.delete_keyword:  # pragma: no cover
                        dossier._meta.warnings.append(
                            Message(
                                level=Severity.WARNING.value,
                                code=MessageCodes.DELETION_HAS_NO_EFFECT,
                                detail=_(
                                    "Deleting %(target)s has no effect because work item %(task)s does not exist. Skipping."
                                )
                                % {"target": self.target, "task": self.task},
                            )
                        )
                        return
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

            if value == self.owner.delete_keyword:
                answer = document.answers.filter(question=question).first()
                if not answer:
                    dossier._meta.warnings.append(
                        Message(
                            level=Severity.WARNING.value,
                            code=MessageCodes.DELETION_HAS_NO_EFFECT.value,
                            detail=f"Deleting {self.target} without effect",
                        )
                    )
                    return
                answer.delete()
                return

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
                        detail=f"Failed to write {value} to {self.target}",
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
                    detail=(
                        "Missing building-authority work item, cannot write ",
                        f"{self.target}. Dossier state {dossier._meta.target_state} ",
                    ),
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

        if value == self.owner.delete_keyword:
            row_document.answers.filter(question=question).delete()
            return

        try:
            form_api.save_answer(
                question=question,
                document=row_document,
                value=value,
                user=BaseUser(
                    username=self.owner._user.username, group=self.owner._group.pk
                ),
            )
        except ValidationError as e:  # pragma: no cover
            dossier._meta.errors.append(
                Message(
                    level=Severity.WARNING.value,
                    code=MessageCodes.FIELD_VALIDATION_ERROR.value,
                    detail=f"Failed to write {value} to {self.target} for dossier {instance}: {e}",
                )
            )
            return


class CalumaListAnswerWriter(FieldWriter):
    def write(self, instance, values):  # noqa: C901
        if not values:
            return

        if values == self.owner.delete_keyword or any(
            [val == self.owner.delete_keyword for val in values]
        ):
            # avoid creating entries with the e. g. <delete> value if the
            # answer does not exist
            if answer := instance.case.document.answers.filter(
                question__slug=self.target
            ).first():
                return answer.documents.all().delete()
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
                    if value is None:
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

                        if self.value_mapping and field.name in self.value_mapping:
                            value = self.value_mapping[field.name].get(value, value)

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

        if values == self.owner.delete_keyword or any(
            [val == self.owner.delete_keyword for val in values]
        ):
            return super().write(instance, self.owner.delete_keyword)
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

        if value == self.owner.delete_keyword:
            if self.can_delete and instance.case.meta.get(self.target):
                del instance.case.meta[self.target]
                instance.case.save()
            return

        formatted_value = value
        if self.formatter == "datetime-to-string":
            formatted_value = datetime.strftime(value, SUBMIT_DATE_FORMAT)
        instance.case.meta[self.target] = formatted_value
        instance.case.save()


class EbauNumberWriter(FieldWriter):
    def write(self, instance, value):  # noqa: C901
        # do not rewrite the ebau-number
        if instance.case.meta.get("ebau-number"):
            return

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
    delete_keyword = settings.DOSSIER_IMPORT["DELETE_KEYWORD"]

    class ConfigurationError(Exception):
        pass

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
        """Create the instance."""
        raise DossierWriter.ConfigurationError  # pragma: no cover

    def write_fields(self, instance: Instance, dossier: Dossier):
        for field in fields(dossier):
            writer = getattr(self, field.name, None)
            if writer:
                writer.owner = weakref.proxy(self)
                writer.context = {"dossier": dossier}
                writer.write(instance, getattr(dossier, field.name, None))

    @transaction.atomic
    def import_dossier(
        self, dossier: Dossier, import_session_id: str
    ) -> DossierSummary:
        """Handle importing of a single dossier.

        Importing a single dossier is composed of a number of steps some of which
        are mandatory, some are optional. The mandatory will rise a
        ConfigurationError exception if undefined.

        Since importing can be repeated for a single dossier we need to be able to
        identify the dataset about to be imported with an existing dossier in the
        db. To avoid code duplication the importing or re-importing procedure is
        the same for all configurations with a set of predefined methods and hooks
        that are called by the `import_dossier` method.

        # identifcation
        instance = self.existing_dossier(dossier_id)   # mandatory

        # new dossier
        instance = self.create_instance(dossier)       # mandatory
        self._post_create_instance(instance, dossier)  # optional
        self.set_dossier_id(instance, dossier_id)      # mandatory

        # all dossiers
        self.write_fields(instance, dossier)           # generic
        self._post_write_fields(instance, dossier)     # optional
        self._handle_dossier_attachments(dossier)      # mandatory
        self._set_workflow_state(instance, dossier)    # mandatory
        """

        dossier_summary = DossierSummary(
            dossier_id=dossier.id, status=DOSSIER_IMPORT_STATUS_SUCCESS, details=[]
        )
        # copy messages from loader to summary
        dossier_summary.details += dossier._meta.errors
        instance = None
        created = True
        if instance := self.existing_dossier(dossier.id):
            created = False
            instance.case.meta["updated-with-import"] = import_session_id
            instance.case.save()
            dossier_summary.instance_id = instance.pk
            dossier_summary.details.append(
                Message(
                    level=Severity.WARNING.value,
                    code=MessageCodes.UPDATE_DOSSIER.value,
                    detail="",
                )
            )
        if not instance:
            if dossier._meta.missing:
                dossier_summary.details.append(
                    Message(
                        level=Severity.ERROR.value,
                        code=MessageCodes.MISSING_REQUIRED_VALUE_ERROR.value,
                        detail=f"missing values in required fields: {dossier._meta.missing}",
                    )
                )
                dossier_summary.status = DOSSIER_IMPORT_STATUS_ERROR
                return dossier_summary
            instance = self.create_instance(dossier)
            dossier_summary.instance_id = str(instance.pk)
            self._post_create_instance(instance, dossier)
            self.set_dossier_id(instance, dossier.id)
            dossier_summary.details.append(
                Message(
                    level=Severity.DEBUG.value,
                    code=MessageCodes.INSTANCE_CREATED.value,
                    detail=f"Instance created with ID:  {instance.pk}",
                )
            )

        dossier_summary.details += self._create_dossier_attachments(dossier, instance)

        # prevent workflowstate skipping if the instance is updated
        # and also keep history
        if created:
            instance.case.meta["import-id"] = import_session_id
            instance.case.save()

            workflow_message = self._set_workflow_state(instance, dossier)
            instance.history.all().delete()
            dossier_summary.details.append(
                Message(
                    level=get_message_max_level(workflow_message),
                    code=MessageCodes.SET_WORKFLOW_STATE.value,
                    detail=workflow_message,
                )
            )

        self.write_fields(instance, dossier)

        self._post_write_fields(instance, dossier)

        # collect all messages by severity level
        dossier_summary.details += dossier._meta.warnings
        dossier_summary.details += dossier._meta.errors
        dossier_summary.details.append(
            Message(
                level=Severity.DEBUG.value,
                code=MessageCodes.FORM_DATA_WRITTEN.value,
                detail="Form data written.",
            )
        )
        # update the current dossier's status based on messages
        if (
            get_message_max_level(dossier_summary.details) == Severity.ERROR.value
        ):  # pragma: no cover
            dossier_summary.status = DOSSIER_IMPORT_STATUS_ERROR
        if get_message_max_level(dossier_summary.details) == Severity.WARNING.value:
            dossier_summary.status = DOSSIER_IMPORT_STATUS_WARNING  # pragma: no cover

        return dossier_summary

    def existing_dossier(self, dossier_id: str) -> Optional[Instance]:
        """Return the instance identified by dossier_id.

        Different configs use different methods to identify instances. This
        is just an abstraction that is needed for retrieving instances
        when reimporting dossiers.
        """
        raise DossierWriter.ConfigurationError  # pragma: no cover

    def set_dossier_id(self, instance: Instance, dossier_id: str):
        """Make the instance retrievable by dossier_id.

        The reverse of `self.existing_dossier`
        """
        raise DossierWriter.ConfigurationError  # pragma: no cover

    def _set_workflow_state(
        self, instance: Instance, dossier: Dossier
    ) -> List[Message]:
        """Fast-Forward case to Dossier.Meta.target_state."""
        raise DossierWriter.ConfigurationError  # pragma: no cover

    def _post_create_instance(
        self, instance: Instance, dossier: Dossier
    ) -> Optional[List[Message]]:
        """Do stuff in import_dossier after a new instance was created.

        Overwrite this in your config for custom behaviour.
        """
        return

    def _post_write_fields(self, instance, dossier) -> Optional[List[Message]]:
        """Do stuff after fields have been written.

        Overwrite this in your config for custom behaviour.
        """
        return

    def _handle_document(
        self, content: File, filename: str, mime_type: str, instance: Instance
    ):
        """Handle a single document when importing.

        Pick one of the provided helper methods based on the configuration or overwrite
        the whole thing.

        Defaults to _handle_legacy_document

        Other options:
         - _handle_alexandria_document
        """

        document_backends = {
            "camac-ng": self._handle_legacy_document,
            "alexandria": self._handle_alexandria_document,
        }
        try:
            return document_backends[settings.APPLICATION["DOCUMENT_BACKEND"]](
                content, filename, mime_type, instance
            )
        except KeyError:  # pragma: no cover
            raise DossierWriter.ConfigurationError(
                f"Set DOCUMENT_BACKEND APPLICATION setting to a valid document backend {document_backends.keys()}"
            )

    def _handle_alexandria_document(
        self, content: File, filename: str, mime_type: str, instance: Instance
    ) -> List[Message]:
        """Handle a single document when importing if documents are managed with Alexandria.

        Requires settings.DOSSIER_IMPORT['ALEXANDRIA_CATEGORY'] to be set.
        """
        from alexandria.core.api import create_document_file, create_file
        from alexandria.core.models import Category, Document as AlexandriaDocument

        messages = []
        category = Category.objects.get(
            pk=settings.DOSSIER_IMPORT["ALEXANDRIA_CATEGORY"]
        )
        if document := AlexandriaDocument.objects.filter(
            title=filename, **{"metainfo__camac-instance-id": str(instance.pk)}
        ).first():
            original = document.get_latest_original()
            if original.checksum == original.make_checksum(content.read()):
                return messages
            content.seek(0)
            create_file(
                document,
                user=self._user.pk,
                group=self._group.pk,
                name=filename,
                content=content,
                mime_type=mime_type,
                size=content.size,
            )

            messages.append(
                Message(
                    level=Severity.INFO.value,
                    code=MessageCodes.ATTACHMENT_UPDATED.value,
                    detail=filename,
                )
            )
            return messages
        doc, _ = create_document_file(
            user=self._user.pk,
            group=self._group.service.pk,
            category=category,
            document_title=filename,
            file_name=filename,
            file_content=content,
            mime_type=mime_type,
            file_size=content.size,
            additional_document_attributes={
                "metainfo": {"camac-instance-id": str(instance.pk)},
            },
        )

        messages.append(
            Message(
                level=Severity.INFO.value,
                code=MessageCodes.ATTACHMENT_CREATED.value,
                detail=f"{doc.title.translate()} ({doc.get_latest_original().mime_type}) in section {category.name.translate()}",
            )
        )
        return messages

    def _handle_legacy_document(
        self, content: File, filename: str, mime_type: str, instance: Instance
    ) -> List[Message]:
        """Handle importing documents in the legacy Attachment based structure.

        Requires settings.DOSSIER_IMPORT['ATTACHMENT_SECTION_ID'] to be set.
        """
        from camac.document.models import Attachment, AttachmentSection

        messages = []
        defaults = dict(
            user=self._user,
            instance=instance,
            service=self._group.service,
            group=self._group,
            name=filename,
            size=content.size,
            context={},
            date=timezone.localtime(),
            mime_type=mime_type,
        )

        attachment, created = Attachment.objects.get_or_create(
            instance=instance,
            name=filename,
            defaults=defaults,
        )

        # If an attachment by the same name exists we'll overwrite the file, unless the data is identical.
        # Django's own `FileField.path.save` method cannot be used because it would create another
        # file with a random suffix, thus cluttering the file system.
        if not created:  # pragma: todo cover
            if (
                hashlib.md5(attachment.path.file.read()).digest()
                == hashlib.md5(content.read()).digest()
            ):
                return messages
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
                        detail=f"Something went wrong replacing '{filename}' with error: {e}",
                    )
                )
                return messages
            defaults["size"] = attachment.path.size
            Attachment.objects.filter(pk=attachment.pk).update(**defaults)
            messages.append(
                Message(
                    level=Severity.WARNING.value,
                    code=MessageCodes.ATTACHMENT_UPDATED.value,
                    detail=attachment.name,
                )
            )
            return messages
        attachment.path.save(filename, content, save=True)
        if created:
            attachment_section = AttachmentSection.objects.get(
                attachment_section_id=settings.DOSSIER_IMPORT["ATTACHMENT_SECTION_ID"]
            )
            attachment_section.attachments.add(attachment)
        att_sec = (
            attachment.attachment_sections.filter(
                attachment_section_id=settings.DOSSIER_IMPORT["ATTACHMENT_SECTION_ID"]
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

    def _create_dossier_attachments(
        self, dossier: Dossier, instance: Instance
    ) -> List[Message]:
        """Create attachments for files in dossier's attachments.

        This will get the file-name after stripping the dossier-id from the
        path.

        python-magic is used to guess the MIME type.

        If an attachment by that name already exists the contents will be
        replaced, rather than creating a new one.
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

            filename = re.sub(
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
                        detail=filename,
                    )
                )
                continue

            messages += self._handle_document(content, filename, mime_type, instance)

        return messages
