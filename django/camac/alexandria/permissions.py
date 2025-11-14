from __future__ import annotations

from dataclasses import dataclass, field

from alexandria.core.models import Document
from django.conf import settings

from camac.instance.models import Instance
from camac.permissions.api import PermissionManager, PermissionScope
from camac.permissions.conditions import PermissionContext


@dataclass
class AlexandriaPermissionContext(PermissionContext):
    document: Document | None
    is_new: bool = field(init=False)

    def __post_init__(self):
        self.is_new = not self.document

    def as_cache_key(self) -> str:  # pragma: no cover
        if self.document is None:
            return "new"

        return str(self.document.pk)

    @classmethod
    def from_document(cls, document: Document) -> "AlexandriaPermissionContext":
        return cls(instance=document.instance_document.instance, document=document)

    @classmethod
    def from_instance(cls, instance: Instance) -> "AlexandriaPermissionContext":
        return cls(instance=instance, document=None)


class AlexandriaPermissionManager(PermissionManager):
    def __init__(self, userinfo, permission_settings=None):
        super().__init__(
            userinfo,
            permission_settings or settings.PERMISSIONS_ALEXANDRIA,
        )

    def scoped_for(self, obj: Document | Instance) -> PermissionScope:
        """Scope manager to a given object (either a document or an instance).

        In almost every case, this should receive a document as this is the main
        object to check permissions in alexandria on. The only use-case for
        passing an instance, is if there is no document yet.
        """

        match obj:
            case Document():
                return super().scoped_for(
                    AlexandriaPermissionContext.from_document(obj)
                )
            case Instance():
                return super().scoped_for(
                    AlexandriaPermissionContext.from_instance(obj)
                )
            case _:  # pragma: no cover
                raise NotImplementedError(f"not implemented for {obj!r}")
