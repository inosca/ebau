from __future__ import annotations

import typing

from camac.permissions.conditions import Check

if typing.TYPE_CHECKING:  # pragma: no cover
    from camac.alexandria.permissions import AlexandriaPermissionContext
    from camac.permissions.api import ACLUserInfo


class OwnDocument(Check):
    """Grant permission if we deal with an own (via service) document."""

    def apply(
        self,
        userinfo: ACLUserInfo,
        context: AlexandriaPermissionContext,
    ) -> bool:
        if not context.document:
            return False

        return userinfo.service.pk == context.document.created_by_group
