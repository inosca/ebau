from __future__ import annotations

from dataclasses import dataclass, field
from logging import getLogger
from typing import Literal

from alexandria.core.models import Document
from django.conf import settings

from camac.instance.models import Instance
from camac.permissions.api import P, PermissionManager, PermissionScope
from camac.permissions.conditions import PermissionContext
from camac.permissions.switcher import permission_switching_method

log = getLogger(__name__)


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

    @permission_switching_method
    def has_permission(self, *args) -> bool:
        return super().has_permission(*args)

    @has_permission.register_old
    def _has_permission_rbac(
        self,
        context: AlexandriaPermissionContext,
        require_expr: P,
    ) -> Literal[True]:
        """Temporary overwrite of `has_permission` to allow all alexandria actions.

        TODO: Remove this as soon as the permission module is fully integrated
        and the permissions for alexandria are configured.
        """

        instance_id = context.instance.pk
        document_uuid = context.document.pk if context.document else None

        log.info(
            f"Requesting alexandria permissions:\n"
            f"\tExpression: {require_expr}\n"
            f"\tInstance ID: {instance_id}\n"
            f"\tDocument UUID: {document_uuid}"
        )

        return True
