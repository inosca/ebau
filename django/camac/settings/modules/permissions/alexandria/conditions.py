from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from django.conf import settings

from camac.permissions.conditions import Check

if TYPE_CHECKING:
    from camac.alexandria.permissions import AlexandriaPermissionContext
    from camac.permissions.api import ACLUserInfo


@dataclass
class OwnDocument(Check):
    """Grant permission if we deal with an own (via service) document."""

    include_subservice: bool = False
    """Whether to include subservices (bidirectional) in the check.

    If `True`, the permission will be granted if the document is created by:
    - the current service
    - any of the current service's subservices
    - the current service's parent service

    If `False`, the permission will only be granted if the document is created
    by the current service."""

    def apply(
        self,
        userinfo: ACLUserInfo,
        context: AlexandriaPermissionContext,
    ) -> bool:
        if not context.document:
            return False

        document_created_by_id = str(context.document.created_by_group)
        user_service_id = str(userinfo.service.pk)

        if user_service_id == document_created_by_id:
            return True

        if self.include_subservice:
            from camac.alexandria.extensions.common import (
                get_service_parent_and_children,
            )

            return document_created_by_id in get_service_parent_and_children(
                user_service_id
            )

        return False

    def __eq__(self, other):  # pragma: no cover
        return (
            isinstance(other, OwnDocument)
            and self.include_subservice == other.include_subservice
        )

    def __repr__(self):
        return f"OwnDocument({'IncludeSubservice' if self.include_subservice else 'ExcludeSubservice'})"


@dataclass
class ApplicantFile(Check):
    """Grant permission if we deal with an applicant file."""

    def apply(
        self,
        userinfo: ACLUserInfo,
        context: AlexandriaPermissionContext,
    ) -> bool:
        if not context.document:
            return False

        return context.document.created_by_group is None

    def __eq__(self, other):  # pragma: no cover
        return isinstance(other, ApplicantFile)


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

    def __eq__(self, other):  # pragma: no cover
        return isinstance(other, HasAdditionalDemand)


class IsNewDocument(Check):
    """Check if a document is new or not.

    Can be used to to combine e.g. in the create permission check
    to allow creating new files, but not moving files in.
    """

    def apply(
        self,
        userinfo: ACLUserInfo,
        context: AlexandriaPermissionContext,
    ) -> bool:
        return context.is_new

    def __eq__(self, other):  # pragma: no cover
        return isinstance(other, IsNewDocument)
