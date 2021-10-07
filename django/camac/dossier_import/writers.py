from typing import Optional

from camac.dossier_import.dossier_classes import Dossier


class FieldWriter:
    target: str
    value = None

    def __init__(self, target: str, owner=None, column_mapping: Optional[dict] = None):
        self.target = target
        self.column_mapping = column_mapping
        self.owner = owner

    def write(self, value):
        raise NotImplementedError


class CamacNgAnswerFieldWriter(FieldWriter):
    def write(self):
        (
            form_field,
            created,
        ) = self.owner.Meta.dossier.Meta.instance.fields.get_or_create(
            name=self.target, defaults=dict(value=self.value)
        )
        if not created:
            form_field.value = self.value
            form_field.save()


class CamacNgListAnswerWriter(FieldWriter):
    column_mapping = None

    def write(self):
        mapped_values = [
            {
                column_name: getattr(row, key, None)
                for key, column_name in self.column_mapping.items()
            }
            for row in self.value
        ]
        field, created = self.owner.Meta.dossier.Meta.instance.fields.get_or_create(
            name=self.target, defaults=dict(value=mapped_values)
        )
        if not created:
            field.value = mapped_values
            field.save()


class DossierWriter:
    class Meta:
        dossier = None
        dataclass = Dossier

    def write_all(self):
        for field_name in self.Meta.dataclass.__dataclass_fields__.keys():
            field = getattr(self, field_name)
            if field:
                field.write()
