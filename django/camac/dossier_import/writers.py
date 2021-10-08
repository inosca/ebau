from dataclasses import fields
from typing import Optional

from camac.dossier_import.dossier_classes import Dossier
from camac.dossier_import.importers import DossierImporter
from camac.dossier_import.loaders import DossierLoader
from camac.instance.models import Instance


class FieldWriter:
    target: str
    value = None

    def __init__(self, target: str, owner=None, column_mapping: Optional[dict] = None):
        self.target = target
        self.column_mapping = column_mapping
        self.owner = owner

    def write(self, instance: Instance, value):
        raise NotImplementedError


class CamacNgAnswerFieldWriter(FieldWriter):
    def write(self, instance, value):
        (
            form_field,
            created,
        ) = instance.fields.get_or_create(name=self.target, defaults=dict(value=value))
        if not created:
            form_field.value = value
            form_field.save()


class CamacNgListAnswerWriter(FieldWriter):
    column_mapping = None

    def write(self, instance, value):
        mapped_values = [
            {
                column_name: getattr(row, key, None)
                for key, column_name in self.column_mapping.items()
            }
            for row in value
        ]
        field, created = instance.fields.get_or_create(
            name=self.target, defaults=dict(value=mapped_values)
        )
        if not created:
            field.value = mapped_values
            field.save()


class DossierWriter:
    def __init__(self, importer: DossierImporter):
        self.importer = importer

    def import_from_loader(self, loader: DossierLoader):
        for dossier in loader.load():
            self.import_dossier(dossier)

    def create_instance(self, dossier: Dossier):
        """Instance etc erstellen."""
        raise NotImplementedError

    def write_fields(self, instance: Instance, dossier: Dossier):
        for field in fields(dossier):
            writer = getattr(self, field.name, None)
            if writer:
                writer.write(instance, getattr(dossier, field.name))

    def import_dossier(self, dossier: Dossier):
        instance = self.create_instance(dossier)
        self.write_fields(instance, dossier)
        self._handle_dossier_attachments(dossier)
        self._set_workflow_state()

    def _set_workflow_state(self):
        """Fast-Forward case to Dossier.Meta.target_state."""
        raise NotImplementedError

    def _handle_dossier_attachments(self, dossier: Dossier, instance: Instance):
        """Add attachment per dossier to the correct attachemnt section."""
        raise NotImplementedError

    def _ensure_retrieveable(self):
        """Make imported dossiers identifiable.

        E. g. client deployment specific location for storing `internal id`
        """
        raise NotImplementedError  # pragma: no cover
