from dataclasses import fields
from typing import Any, Optional

from django.conf import settings
from django.utils import timezone

from camac.core.models import WorkflowEntry
from camac.dossier_import.dossier_classes import Dossier
from camac.dossier_import.loaders import safe_join
from camac.dossier_import.messages import Message
from camac.instance.models import Instance


class RenderError:
    pass


class FieldWriter:
    target: str
    value: Any = None
    name: Optional[str] = None

    def __init__(
        self,
        target: str,
        name=None,
        owner=None,
        column_mapping: Optional[dict] = None,
        renderer: Optional[str] = None,
    ):
        self.target = target
        self.column_mapping = column_mapping
        self.renderer = renderer
        self.owner = owner
        self.name = name or target

    def write(self, instance: Instance, value):
        raise NotImplementedError  # pragma: no cover

    def render(self, value):
        raise NotImplementedError  # pragma: no cover


class CamacNgAnswerFieldWriter(FieldWriter):
    def write(self, instance, value):
        (
            form_field,
            created,
        ) = instance.fields.get_or_create(name=self.target, defaults=dict(value=value))
        if not created:  # pragma: no cover
            form_field.value = value
            form_field.save()


class CamacNgListAnswerWriter(FieldWriter):
    column_mapping = None

    def write(self, instance, value):
        rows = []
        for obj in value:
            if any(getattr(obj, field.name, None) for field in fields(obj)):
                rows.append(obj)
        if not rows:
            return

        mapped_values = [
            {
                column_name: getattr(row, key, None)
                for key, column_name in self.column_mapping.items()
            }
            for row in rows
        ]
        field, created = instance.fields.get_or_create(
            name=self.target, defaults=dict(value=mapped_values)
        )
        if not created:  # pragma: no cover
            field.value = mapped_values
            field.save()


class CamacNgPersonListAnswerWriter(CamacNgListAnswerWriter):
    """Person and location objects combine address and house number in 1 line."""

    def write(self, instance, value):
        for person in value:
            person.street = safe_join((person.street, person.street_number))
        super().write(instance, value)


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


class DossierWriter:
    def __init__(
        self,
        import_settings: dict = settings.APPLICATION["DOSSIER_IMPORT"],
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
            value = getattr(dossier, field.name, None)
            if not value:  # pragma: no cover
                continue
            writer = getattr(self, field.name, None)
            if writer:
                writer.write(instance, getattr(dossier, field.name))

    def import_dossier(self, dossier: Dossier) -> Message:
        # instance = self.create_instance(dossier)
        # self.write_fields(instance, dossier)
        # self._handle_dossier_attachments(dossier)
        # self._set_workflow_state(instance, dossier.Meta.target_state)
        raise NotImplementedError  # pragma: no cover

    def _set_workflow_state(self, instance: Instance, target_state: str):
        """Fast-Forward case to Dossier.Meta.target_state."""
        raise NotImplementedError  # pragma: no cover

    def _create_dossier_attachments(self, dossier: Dossier, instance: Instance):
        """Add attachment per dossier to the correct attachemnt section."""
        raise NotImplementedError  # pragma: no cover

    def _ensure_retrieveable(self):
        """Make imported dossiers identifiable.

        E. g. client deployment specific location for storing `internal id`
        """
        raise NotImplementedError  # pragma: no cover
