from __future__ import annotations

import typing

from django.conf import settings

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


class HasAdditionalDemand(Check):
    """Grant permissions if there is a ready fill-additional-demand work item.

    If we already have a document, we need to make sure that we only grant
    permission if it's linked to the ready fill-additional-demand work item.
    """

    def apply(
        self,
        userinfo: ACLUserInfo,
        context: AlexandriaPermissionContext,
    ) -> bool:
        from caluma.caluma_workflow.models import WorkItem

        work_items = WorkItem.objects.filter(
            task_id=settings.ADDITIONAL_DEMAND["FILL_TASK"],
            status=WorkItem.STATUS_READY,
            case__family=context.instance.case,
        )

        if context.document:
            # If we already have a document, we need to make sure the work item
            # belongs to that document.
            work_items = work_items.filter(
                document_id=context.document.metainfo.get("caluma-document-id")
            )

        return work_items.exists()
