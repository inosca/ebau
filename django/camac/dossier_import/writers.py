import hashlib
import logging
import re
import traceback
import weakref
from abc import ABC, abstractmethod
from collections.abc import Callable, Mapping
from dataclasses import asdict, fields
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import magic
from alexandria.core.tasks import make_checksum
from caluma.caluma_form import api as form_api
from caluma.caluma_form.models import (
    Answer,
    AnswerDocument,
    Document,
    Form as CalumaForm,
    Question,
)
from caluma.caluma_user.models import BaseUser
from caluma.caluma_workflow import api as workflow_api
from caluma.caluma_workflow.models import Case, WorkItem
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File
from django.db import transaction
from django.utils import timezone
from django.utils.translation import gettext as _
from future.moves import itertools
from graphql import GraphQLError
from rest_framework.exceptions import ValidationError

from camac.core.models import InstanceService, WorkflowEntry
from camac.core.utils import generate_sort_key
from camac.dossier_import.dossier_classes import (
    CalumaPlotData,
    Dossier,
    Person,
    PlotData,
)
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
from camac.dossier_import.utils import get_or_create_ebau_nr
from camac.dossier_import.validation import TargetStatus
from camac.instance.domain_logic import SUBMIT_DATE_FORMAT, CreateInstanceLogic
from camac.instance.models import Form, Instance, InstanceState
from camac.permissions.events import core as permissions_events
from camac.tags.models import Keyword
from camac.user.models import Group, User

log = logging.getLogger("dossier_import")


class FieldWriter(ABC):
    target: str
    value: Any = None
    name: str | None = None
    protected: bool = False

    def __init__(
        self,
        target: str,
        value=None,
        name=None,
        owner=None,
        context=None,
        column_mapping: dict | None = None,
        value_mapping: dict | None = None,
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

        self._question_cache = {}

    @property
    def can_delete(self):  # pragma: todo cover
        if not self.protected:
            return True
        if dossier := self.context.get("dossier"):
            dossier._meta.errors.append(
                Message(
                    level=Severity.WARNING.value,
                    code=MessageCodes.WRITING_READ_ONLY_FIELD.value,
                    detail=_("Ignoring %(keyword)s on field %(target)s (readonly).")
                    % {
                        "keyword": self.owner.delete_keyword,
                        "target": self.target,
                    },
                )
            )
        return False

    @abstractmethod
    def write(self, instance, values):  # pragma: no cover
        ...

    def get_question(self, slug: str) -> Question:
        if slug not in self._question_cache:
            self._question_cache[slug] = Question.objects.get(pk=slug)

        return self._question_cache[slug]


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
                            detail=_("Value deleted"),
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
            val == self.owner.delete_keyword for val in values
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
        if any(val == self.owner.delete_keyword for val in value):
            return super().write(instance, self.owner.delete_keyword)

        for person in value:
            person.street = safe_join((person.street, person.street_number))
        super().write(instance, value)


class CamacNgPointsWriter(CamacNgAnswerWriter):
    """Wrap coordinates list in a list.

    Coordinate tuples are treated as separate points. I. e. the import
    does not allow importing of geometries consisting of multiple points.
    """

    def write(self, instance, values):
        if not values:
            return
        if values == self.owner.delete_keyword or any(
            val == self.owner.delete_keyword for val in values
        ):
            return super().write(instance, self.owner.delete_keyword)

        result = []
        for obj in values:
            # Ignore if a dataclass without any meaningful data makes it this far
            if not any(asdict(obj).values()):  # pragma: no cover
                continue
            result.append(
                [
                    {
                        column_name: getattr(obj, key, None)
                        for key, column_name in self.column_mapping.items()
                    }
                ]
            )
        super().write(instance, result)


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
        formatter: str | Callable | None = None,
        *args,
        **kwargs,
    ):
        self.task = task
        self.formatter = formatter
        super().__init__(*args, **kwargs)

    def _apply_value_format(self, value):
        if self.formatter == "to-string":
            return str(value)
        if callable(self.formatter):  # pragma: no cover
            return self.formatter(value)
        return value

    def write(self, instance, value):
        # allow False values for boolean answer mappings, but no other empty value
        if not value and value is not False:
            return

        old_value = value
        value = self._apply_value_format(old_value)

        dossier = self.context.get("dossier")

        if not value:  # pragma: no cover
            log.warning(f"'{self.target}': '{old_value}' could not be formatted.")
            return

        try:
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
                            detail=_(
                                "Missing %(task)s work item, cannot write %(target)s"
                            )
                            % {"task": self.task, "target": self.target},
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
                            detail=_("Deleting %(target)s without effect")
                            % {"target": self.target},
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
                        % {
                            "value": value,
                            "target": self.target,
                            "max": question.max_length,
                        },
                    )
                )
            try:
                form_api.save_answer(
                    question=question,
                    document=document,
                    value=value,
                    user=self.owner._caluma_user,
                )
            except ValidationError as v:  # pragma: no cover
                dossier._meta.errors.append(
                    Message(
                        level=Severity.WARNING.value,
                        code=MessageCodes.FIELD_VALIDATION_ERROR.value,
                        detail=_("Failed to write %(value)s to %(target)s: %(error)s")
                        % {"value": value, "target": self.target, "error": v},
                    )
                )
                return

        except ObjectDoesNotExist as e:  # pragma: no cover
            raise RuntimeError(
                f"Failed to write {value} to field {self.target} on {instance} because of : {e}"
            ) from e


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
                    detail=_(
                        "Missing %(task)s work item, cannot write %(target)s. Dossier state %(state)s."
                    )
                    % {
                        "task": "building-authority",
                        "target": self.target,
                        "state": dossier._meta.target_state,
                    },
                )
            )
            return
        table_answer, _created = Answer.objects.update_or_create(
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
                user=self.owner._caluma_user,
            )
        except ValidationError as e:  # pragma: no cover
            dossier._meta.errors.append(
                Message(
                    level=Severity.WARNING.value,
                    code=MessageCodes.FIELD_VALIDATION_ERROR.value,
                    detail=_(
                        "Failed to write %(value)s to %(target)s for dossier %(dossier)s: %(error)s"
                    )
                    % {
                        "value": value,
                        "target": self.target,
                        "dossier": instance,
                        "error": e,
                    },
                )
            )
            return


class CalumaTableAnswerWriter(FieldWriter):
    """Write a list of dataclass items into a Caluma table question.

    Each item in the list becomes one row document of the table question
    referenced by `self.target`. The dataclass fields are mapped to column
    questions via `self.column_mapping` (falling back to the field name) and
    their values may be remapped via `self.value_mapping`.
    """

    def write(self, instance: Instance, values: list[PlotData] | list[Person]):
        """Write the given list items as rows of the target table question."""
        if not values:
            # If we don't have any values, return
            return

        if self.owner.delete_keyword in values:
            # If the field is marked to be deleted, we delete all existing row
            # documents and return
            answer = instance.case.document.answers.filter(
                question__slug=self.target
            ).first()

            if answer:
                answer.documents.all().delete()

            return

        row_documents = [self.write_row(instance, obj) for obj in values]

        form_api.save_answer(
            document=instance.case.document,
            question=self.get_question(self.target),
            value=[doc.pk for doc in row_documents if doc],
            user=self.owner._caluma_user,
        )

    def write_row(self, instance: Instance, obj: Person | PlotData) -> Document | None:
        """Create and populate a single row document for one list item."""
        data = asdict(obj)

        if not any(data.values()):  # pragma: no cover
            # If all properties of this list item are empty, we don't write
            # anything for this row
            return None

        table_question = self.get_question(self.target)
        row_document = form_api.save_document(form=table_question.row_form)

        for field_name, value in data.items():
            if value is None:
                continue
            try:
                slug = (
                    self.column_mapping[field_name]
                    if self.column_mapping
                    else field_name
                )
                question = self.get_question(slug)

                if question.type in [Question.TYPE_TEXT, Question.TYPE_TEXTAREA]:
                    # Some fields are parsed as integer but are not written into
                    # an integer field in every canton, cast them to strings
                    value = str(value)

                if self.value_mapping and field_name in self.value_mapping:
                    value = self.value_mapping[field_name].get(value, value)

                form_api.save_answer(
                    question=question,
                    value=value,
                    document=row_document,
                    user=self.owner._caluma_user,
                )
            except (ValidationError, GraphQLError):  # pragma: no cover
                self.context.get("dossier")._meta.errors.append(
                    Message(
                        level=Severity.WARNING.value,
                        code=MessageCodes.FIELD_VALIDATION_ERROR.value,
                        detail=_(
                            "Failed to write %(value)s for field %(field)s to %(target)s for dossier %(dossier)s."
                        )
                        % {
                            "value": value,
                            "field": field_name,
                            "target": self.target,
                            "dossier": instance,
                        },
                    )
                )
                continue
            except Exception:  # pragma: no cover
                self.context.get("dossier")._meta.errors.append(
                    Message(
                        level=Severity.WARNING.value,
                        code=MessageCodes.UNHANDLED_EXCEPTION.value,
                        detail=_(
                            "Failed to write %(value)s for field %(field)s to %(target)s for dossier %(dossier)s."
                        )
                        % {
                            "value": value,
                            "field": field_name,
                            "target": self.target,
                            "dossier": instance,
                        },
                    )
                )
                continue

        return row_document


class CalumaPlotDataWriter(CalumaTableAnswerWriter):
    def write(self, instance, values):
        if not values:
            return

        compiled = []
        dossier = self.context.get("dossier")
        coordinates = dossier.coordinates if dossier else []

        if values == self.owner.delete_keyword or any(
            val == self.owner.delete_keyword for val in values
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


class SubmitDateWriter(FieldWriter):
    """Write the submit date into the case's meta field.

    The value is stored under the `submit-date` key of `case.meta` as a string
    formatted with `SUBMIT_DATE_FORMAT`. Naive datetimes are assumed to be in
    UTC and made timezone-aware before formatting.

    The field is always protected and can't be cleared on a reimport.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, target="submit-date", protected=True)

    def write(self, instance: Instance, value: datetime | str | None):
        if not value:
            return

        if value == self.owner.delete_keyword:
            # The error message for the user is generated as a side-effect of
            # the property `can_delete`. Since we need the error message, even
            # though we know that deleting is not allowed, we trigger it here.
            _ = self.can_delete
            return

        if not timezone.is_aware(value):
            value = timezone.make_aware(value, UTC)

        instance.case.meta[self.target] = datetime.strftime(value, SUBMIT_DATE_FORMAT)
        instance.case.save(update_fields=["meta"])


class EbauNumberWriter(FieldWriter):
    def write(self, instance, value):
        # do not rewrite the ebau-number
        if instance.case.meta.get("ebau-number"):
            return

        dossier = self.context.get("dossier")
        if not dossier.submit_date:
            dossier._meta.errors.append(
                Message(
                    level=Severity.WARNING.value,
                    code=MessageCodes.FIELD_VALIDATION_ERROR.value,
                    detail=_(
                        "Failed to write %(value)s to %(target)s for dossier %(dossier)s"
                    )
                    % {"value": value, "target": self.target, "dossier": instance},
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


class ResponsibleUserWriter(FieldWriter):
    def write(self, instance: Instance, value):
        dossier = self.context.get("dossier")

        existing_responsible_users = instance.responsible_services.filter(
            responsible_user__isnull=False
        )

        if str(value).upper() == settings.DOSSIER_IMPORT["DELETE_KEYWORD"]:
            # TODO: really only the ones that point to users?
            existing_responsible_users.delete()
        elif value:
            # No further validation - User must exist, otherwise
            # we can't write the responsible user
            users = User.objects.filter(email=value)
            responsible_service = instance.responsible_service()

            users_count = users.count()
            if not responsible_service:
                detail = _("No responsible service, cannot set responsible user")

            elif users_count == 1:
                # One user found, expected case, simply assign and be happy
                # Delete any old ones, so this becomes the new properly-set value
                existing_responsible_users.delete()
                instance.responsible_services.create(
                    responsible_user=users.get(),
                    service=responsible_service,
                )
                return

            elif users_count > 1:
                detail = _("Multiple users in database with email {value}").format(
                    value=value
                )
            elif users_count == 0:
                detail = _("No user found in database with email {value}").format(
                    value=value
                )

            dossier._meta.errors.append(
                Message(
                    level=Severity.WARNING.value,
                    code=MessageCodes.FIELD_VALIDATION_ERROR.value,
                    detail=_("Could not assign/update responsible: {detail}").format(
                        detail=detail
                    ),
                )
            )
        elif not value:
            # No change: If anything's there,
            pass


class CalumaCombinedStreetAndNumberWriter(CalumaAnswerWriter):
    """Combine street and street number into one field."""

    def __init__(
        self,
        fields: list[str] = None,
        *args,
        **kwargs,
    ):
        fields = fields or []
        self.fields = fields
        super().__init__(*args, **kwargs)

    def write(self, instance, values):
        dossier = self.context.get("dossier")
        if dossier.street == settings.DOSSIER_IMPORT["DELETE_KEYWORD"]:
            combined_value = dossier.street
        else:
            combined_value = safe_join(
                (
                    getattr(dossier, field, "")
                    for field in self.fields
                    if getattr(dossier, field, None)
                ),
                separator=" ",
            )

        super().write(instance, combined_value)


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
            username=self._user.username,
            group=self._group.service.pk if self._group.service else None,
        )
        self._caluma_user.camac_group = self._group.pk

    def get_instance_state(self, dossier: Dossier) -> InstanceState:
        """Get the instance state for a dossier."""

        return InstanceState.objects.get(
            name=settings.DOSSIER_IMPORT["INSTANCE_STATE_MAPPING"].get(
                dossier._meta.target_state
            )
        )

    def create_instance(self, dossier: Dossier) -> Instance:
        """Create the instance."""

        instance_state = self.get_instance_state(dossier)

        creation_data = {
            "instance_state": instance_state,
            "previous_instance_state": instance_state,
            "user": self._user,
            "group": self._group,
            "form": Form.objects.get(pk=settings.DOSSIER_IMPORT["FORM_ID"]),
        }

        instance = CreateInstanceLogic.create(
            creation_data,
            caluma_user=self._caluma_user,
            camac_user=self._user,
            group=self._group,
            caluma_form=CalumaForm.objects.get(
                pk=settings.DOSSIER_IMPORT["CALUMA_FORM"]
            ),
            start_caluma=True,
        )

        InstanceService.objects.create(
            instance=instance,
            service_id=self._group.service_id,
            active=1,
            activation_date=None,
        )

        dossier_number = CreateInstanceLogic.generate_identifier(
            instance, dossier.submit_date.year
        )

        instance.case.meta.update(
            {
                "dossier-number": dossier_number,
                "dossier-number-sort": generate_sort_key(dossier_number),
            }
        )
        instance.case.save()
        permissions_events.Trigger.instance_submitted(None, instance)
        form_api.save_answer(
            document=instance.case.document,
            question=Question.objects.get(slug="gemeinde"),
            value=str(self._group.service_id),
            user=self._caluma_user,
        )

        return instance

    def write_fields(self, instance: Instance, dossier: Dossier):
        for field in fields(dossier):
            writer = getattr(self, field.name, None)
            if writer:
                self.add_context(writer, dossier).write(
                    instance, getattr(dossier, field.name, None)
                )

    def add_context(self, writer: FieldWriter, dossier: Dossier):
        writer.owner = weakref.proxy(self)
        writer.context = {"dossier": dossier, "caluma_user": self._caluma_user}
        return writer

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
        self.set_workflow_state(instance, dossier)     # mandatory
        """

        dossier_summary = DossierSummary(
            dossier_id=dossier.id, status=DOSSIER_IMPORT_STATUS_SUCCESS, details=[]
        )
        # copy messages from loader to summary
        dossier_summary.details += dossier._meta.errors
        instance = None
        created = True
        if instance := self.find_existing_instance(dossier, self._caluma_user):
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
                        detail=_("missing values in required fields: %(fields)s")
                        % {"fields": dossier._meta.missing},
                    )
                )
                dossier_summary.status = DOSSIER_IMPORT_STATUS_ERROR
                return dossier_summary
            instance = self.create_instance(dossier)
            dossier_summary.instance_id = str(instance.pk)
            self._post_create_instance(instance, dossier)
            self.link_instance_and_dossier(instance, dossier, self._caluma_user)
            dossier_summary.details.append(
                Message(
                    level=Severity.DEBUG.value,
                    code=MessageCodes.INSTANCE_CREATED.value,
                    detail=_("Instance created with ID:  %(id)s") % {"id": instance.pk},
                )
            )

        dossier_summary.details += self._create_dossier_attachments(dossier, instance)

        # prevent workflowstate skipping if the instance is updated
        # and also keep history
        if created:
            instance.case.meta["import-id"] = import_session_id
            instance.case.save()

            workflow_messages = self.set_workflow_state(instance, dossier)
            instance.history.all().delete()
            dossier_summary.details.extend(workflow_messages)

        self.write_fields(instance, dossier)

        self._post_write_fields(instance, dossier)

        # collect all messages by severity level
        dossier_summary.details += dossier._meta.warnings
        dossier_summary.details += dossier._meta.errors
        dossier_summary.details.append(
            Message(
                level=Severity.DEBUG.value,
                code=MessageCodes.FORM_DATA_WRITTEN.value,
                detail=_("Form data written."),
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

    def get_existing_dossier_ids(self, dossier_ids: list[str]) -> list[str]:
        """Return all dossier IDs that already exist.

        Looks for existing keyword records for all the dossier IDs passed in the
        XLSX file.
        """
        return list(
            Keyword.objects.filter(
                name__in=dossier_ids,
                service=self._group.service,
                instances__isnull=False,
            ).values_list("name", flat=True)
        )

    def get_existing_and_new_dossier_ids(
        self, dossier_and_cantonal_ids: list[tuple[str, str]]
    ) -> tuple[set[str], set[str], Mapping[str, str]]:
        # Each dossier ID may be discarded for various reasons and based on
        # different criteria depending on the import status as a new or reimported
        # dossier.
        dossier_ids = [
            dossier_id for dossier_id, _ in dossier_and_cantonal_ids if dossier_id
        ]
        existing_dossier_ids = set(self.get_existing_dossier_ids(dossier_ids))
        new_dossier_ids = set(dossier_ids) - existing_dossier_ids
        return existing_dossier_ids, new_dossier_ids, {}

    def find_existing_instance(
        self, dossier: Dossier, user: BaseUser
    ) -> Instance | None:
        """Return the instance identified linked by the dossier.

        Looks for a keyword record with the dossier's ID as name and returns the
        instance of that keyword if found.
        """
        keyword = Keyword.objects.filter(
            name=dossier.id, service=self._group.service
        ).first()

        return keyword.instances.first() if keyword else None

    def link_instance_and_dossier(
        self, instance: Instance, dossier: Dossier, user: BaseUser
    ):
        """Make the instance retrievable by the dossier.

        The reverse of `self.find_existing_instance`
        :param instance:
        :param dossier:
        :param user:
        """
        keyword = Keyword.objects.filter(
            name=dossier.id, service=self._group.service
        ).first()

        if keyword:  # pragma: no cover
            # This only happens after an import was undone
            keyword.instances.add(instance)
        else:
            instance.keywords.create(name=dossier.id, service=self._group.service)

    def get_workflow_skip_path(self, instance: Instance, dossier: Dossier) -> list[str]:
        """Return the ordered task_ids to skip to reach the target state.

        The tasks are skipped in the returned order to walk the case from its
        current state to the dossier's target state. Overwrite this in your
        config to define the path for each supported target state.

        Args:
            instance: The instance whose case is being advanced.
            dossier: The dossier being imported.

        Returns:
            The task_ids to skip, in the order they should be skipped.

        Raises:
            ConfigurationError: If the config does not implement this method.
        """
        raise DossierWriter.ConfigurationError  # pragma: no cover

    def get_decision_answer_value(self, dossier: Dossier) -> str:
        """Map the dossier's target state to the decision form's answer value.

        Overwrite this in your config if the canton's decision answers differ
        from the default (e.g. Kt. BE uses a workflow-dependent mapping).

        Args:
            dossier: The dossier being imported.

        Returns:
            The answer value to write for the decision question.
        """
        decision = settings.DECISION["ANSWERS"]["DECISION"]

        return {
            TargetStatus.APPROVED.value: decision["APPROVED"],
            TargetStatus.REJECTED.value: decision["REJECTED"],
            TargetStatus.WRITTEN_OFF.value: decision["WITHDRAWAL"],
            TargetStatus.DONE.value: decision["APPROVED"],
        }[dossier._meta.target_state]

    def write_decision_form(self, decision_work_item: WorkItem, dossier: Dossier):
        """Write the decision answer onto the decision work item's document.

        Called from `before_skip_work_item` when the decision work item is
        skipped. Overwrite this in your config (calling `super`) to write
        additional canton-specific decision answers.

        Args:
            decision_work_item: The decision work item being skipped.
            dossier: The dossier being imported.
        """
        form_api.save_answer(
            document=decision_work_item.document,
            question=Question.objects.get(
                slug=settings.DECISION["QUESTIONS"]["DECISION"]
            ),
            value=self.get_decision_answer_value(dossier),
            user=self._caluma_user,
        )

    def get_pre_complete_config(self, dossier: Dossier) -> dict:
        """Return the `PRE_COMPLETE` config that drives `run_pre_complete`.

        Overwrite this in your config to adjust the sibling-handling side
        effects for the import (e.g. Kt. SZ tweaks them before skipping).

        Returns:
            The mapping of task_id to the actions (skip, cancel, ...) and the
            sibling tasks to run them on before that task is completed.
        """
        return settings.APPLICATION["CALUMA"]["PRE_COMPLETE"]

    def run_pre_complete(
        self, work_item: WorkItem, instance: Instance, dossier: Dossier
    ):
        """Resolve blocking sibling work items before skipping a work item.

        A work item can only be completed or skipped once none of its siblings
        are still in the `ready` state. The `PRE_COMPLETE` config (see
        `get_pre_complete_config`) defines, per task, which sibling tasks to
        deal with and how (e.g. skip or cancel) before that task is handled.
        """
        config = self.get_pre_complete_config(dossier)
        task_config = config.get(work_item.task_id) if config else None

        if not task_config:
            return

        for action_name, tasks in task_config.items():
            action = getattr(workflow_api, f"{action_name}_work_item")
            for item in work_item.case.work_items.filter(
                task_id__in=tasks, status=WorkItem.STATUS_READY
            ):
                action(item, self._caluma_user)

    def before_skip_work_item(
        self, work_item: WorkItem, instance: Instance, dossier: Dossier
    ):
        """Run side effects before a work item is skipped.

        By default this writes the decision form when the decision work item is
        being skipped, and always resolves blocking sibling work items via
        `run_pre_complete`. Overwrite this in your config (calling `super`) for
        custom per-canton behaviour.

        Args:
            work_item: The work item that is about to be skipped.
            instance: The instance whose case is being advanced.
            dossier: The dossier being imported.
        """
        if work_item.task_id == "decision":
            self.write_decision_form(work_item, dossier)

        self.run_pre_complete(work_item, instance, dossier)

    def get_skip_context(self, work_item: WorkItem) -> dict:
        """Return the context passed to `skip_work_item` for a work item.

        By default no notifications or history entries are created. For the
        `init-construction-monitoring` work item we additionally pass `skip` so
        the construction monitoring process is marked as skipped instead of
        completed.

        Args:
            work_item: The work item that is about to be skipped.

        Returns:
            The context forwarded to the caluma `skip_work_item` API.
        """
        context = {"no-notification": True, "no-history": True}

        if work_item.task_id == "init-construction-monitoring":
            context["skip"] = True

        return context

    def after_skip_work_item(
        self, work_item: WorkItem, instance: Instance, dossier: Dossier
    ):
        """Run side effects after a work item is skipped.

        By default this triggers the `decision_decreed` permission event once
        the decision work item has been skipped. Overwrite this in your config
        (calling `super`) for custom per-canton behaviour.

        Args:
            work_item: The work item that was just skipped.
            instance: The instance whose case is being advanced.
            dossier: The dossier being imported.
        """
        if work_item.task_id == "decision":
            permissions_events.Trigger.decision_decreed(None, instance)

    def set_workflow_state(self, instance: Instance, dossier: Dossier) -> list[Message]:
        """Fast-forward the instance's case to the dossier's target state.

        A caluma workflow can only advance by completing work items, so to reach
        the target state we walk the ordered tasks from `get_workflow_skip_path`
        and, for each one, resolve the blocking siblings and run any decision
        handling (`before_skip_work_item`), skip the work item, then run the
        follow-up side effects (`after_skip_work_item`).

        Args:
            instance: The instance whose case should be advanced.
            dossier: The dossier being imported; its target state defines how
                far the case is advanced.

        Returns:
            The messages collected while advancing the workflow, for the import
            summary.
        """
        messages = []
        target_state = dossier._meta.target_state

        for task_id in self.get_workflow_skip_path(instance, dossier):
            try:
                work_item = instance.case.work_items.get(task_id=task_id)
            except WorkItem.DoesNotExist as e:  # pragma: no cover
                messages.append(
                    Message(
                        level=Severity.ERROR.value,
                        code=MessageCodes.WORKFLOW_SKIP_ITEM_FAILED.value,
                        detail=_(
                            "Skip work item with task_id %(task_id)s failed with %(error)s."
                        )
                        % {
                            "task_id": task_id,
                            "error": DossierWriter.ConfigurationError(e),
                        },
                    )
                )
                continue

            if work_item.case.status != Case.STATUS_RUNNING:  # pragma: no cover
                # TODO: This was copied from the original implementation in AG &
                # GR. Check if this is really necessary. How could we even get
                # into such a state realistically?
                continue

            self.before_skip_work_item(work_item, instance, dossier)
            workflow_api.skip_work_item(
                work_item,
                user=self._caluma_user,
                context=self.get_skip_context(work_item),
            )
            self.after_skip_work_item(work_item, instance, dossier)

        messages.append(
            Message(
                level=Severity.DEBUG.value,
                code=MessageCodes.SET_WORKFLOW_STATE.value,
                detail=_("Workflow state set to %(state)s.") % {"state": target_state},
            )
        )

        return messages

    def _post_create_instance(
        self, instance: Instance, dossier: Dossier
    ) -> list[Message] | None:
        """Do stuff in import_dossier after a new instance was created.

        Overwrite this in your config for custom behaviour.
        """
        return

    def _post_write_fields(self, instance, dossier) -> list[Message] | None:
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
            impl = document_backends[settings.APPLICATION["DOCUMENT_BACKEND"]]
        except KeyError as e:  # pragma: no cover
            raise DossierWriter.ConfigurationError(
                "Set DOCUMENT_BACKEND APPLICATION setting to a valid document "
                f"backend: {list(document_backends)}"
            ) from e
        return impl(content, filename, mime_type, instance)

    def _handle_alexandria_document(
        self, content: File, filename: str, mime_type: str, instance: Instance
    ) -> list[Message]:
        """Handle a single document when importing if documents are managed with Alexandria.

        Requires settings.DOSSIER_IMPORT['ALEXANDRIA_CATEGORY'] to be set.
        """
        from alexandria.core.api import create_document_file, create_file
        from alexandria.core.models import Category, Document as AlexandriaDocument

        messages = []
        category = Category.objects.get(
            pk=settings.DOSSIER_IMPORT["ALEXANDRIA_CATEGORY"]
        )

        if (
            category.allowed_mime_types is not None
            and len(category.allowed_mime_types)
            and mime_type not in category.allowed_mime_types
        ):
            messages.append(
                Message(
                    level=Severity.WARNING.value,
                    code=MessageCodes.MIME_TYPE_INVALID.value,
                    detail=_(
                        'Unallowed mime type for file "%(filename)s" (%(mime_type)s) - the file was not imported'
                    )
                    % {"filename": filename, "mime_type": mime_type},
                )
            )

            return messages

        if settings.DOSSIER_IMPORT.get("ALEXANDRIA_UPDATE_EXISTING_DOCUMENTS") and (
            document := AlexandriaDocument.objects.filter(
                title=filename, **{"metainfo__camac-instance-id": str(instance.pk)}
            ).first()
        ):
            original = document.get_latest_original()
            if original.checksum == make_checksum(content.read()):
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

        doc, _file = create_document_file(
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
                detail=_("%(filename)s (%(mime_type)s) in section %(section)s")
                % {
                    "filename": doc.title,
                    "mime_type": doc.get_latest_original().mime_type,
                    "section": category.name.translate(),
                },
            )
        )
        return messages

    def _handle_legacy_document(
        self, content: File, filename: str, mime_type: str, instance: Instance
    ) -> list[Message]:
        """Handle importing documents in the legacy Attachment based structure.

        Requires settings.DOSSIER_IMPORT['ATTACHMENT_SECTION_ID'] to be set.
        """
        from camac.document.models import Attachment, AttachmentSection

        messages = []
        defaults = {
            "user": self._user,
            "instance": instance,
            "service": self._group.service,
            "group": self._group,
            "name": filename,
            "size": content.size,
            "context": {},
            "date": timezone.localtime(),
            "mime_type": mime_type,
        }

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
                        detail=_(
                            "Something went wrong replacing '%(filename)s' with error: %(error)s"
                        )
                        % {"filename": filename, "error": e},
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
                detail=_("%(filename)s (%(mime_type)s) in section %(section)s")
                % {
                    "filename": attachment.name,
                    "mime_type": attachment.mime_type,
                    "section": "{name} ({attachment_section_id})".format(**att_sec),
                },
            )
        )
        return messages

    def _create_dossier_attachments(
        self, dossier: Dossier, instance: Instance
    ) -> list[Message]:
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

        if settings.APPLICATION["DOCUMENT_BACKEND"] == "camac-ng":
            instance_files_path = Path(
                f"{settings.MEDIA_ROOT}/attachments/files/{instance.pk}"
            )
            attachments_path = instance_files_path / str(dossier.id)
            attachments_path.mkdir(parents=True, exist_ok=True)

        for document in dossier.attachments:
            content = File(document.file_accessor)

            filename = re.sub(
                # ensure that dossier.id is only removed at the beginning of a path
                rf"^{dossier.id}/",
                "",
                document.name.encode("utf-8", errors="ignore").decode(
                    "utf-8", errors="ignore"
                ),
            )

            mimimi = magic.Magic(mime=True)
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
