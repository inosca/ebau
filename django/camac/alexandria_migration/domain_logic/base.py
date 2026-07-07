from abc import ABC, abstractmethod
from contextlib import contextmanager
from dataclasses import dataclass, field

import django.db.models.fields
from django.db.models import Model

from camac.alexandria_migration.models import MigrationLog, MigrationRun


@contextmanager
def disable_auto_now(*models: list[Model]):
    """
    Disable the auto_now, auto_now_add functionality in Django.

    Use this context manager for updating models where you may need to
    back-date some fields like `created_at` or similar, where Django would
    otherwise overrule the value.

    Example:
    >>> with disable_auto_now(Document, File):
    ...     Document.objects.create(created_at='sometime-in-the-past')
    """
    original = {}

    for model in models:
        for field_descriptor in model._meta.fields:
            if isinstance(field_descriptor, django.db.models.fields.DateField):
                # also matches DateTimeField
                original[field_descriptor] = {
                    "auto_now": field_descriptor.auto_now,
                    "auto_now_add": field_descriptor.auto_now_add,
                }
                field_descriptor.auto_now = False
                field_descriptor.auto_now_add = False

    try:
        yield

    finally:
        for field_descriptor, properties in original.items():
            for k, v in properties.items():
                setattr(field_descriptor, k, v)


@dataclass
class BaseMigrator(ABC):
    instance_ids: list[int]
    run: MigrationRun
    logs: list[MigrationLog] = field(default_factory=list)

    @abstractmethod
    def process(self): ...
