from alexandria.core.models import Document
from caluma.caluma_workflow.models import WorkItem
from django.conf import settings

from camac.caluma.api import CalumaApi


class Permission:
    write = False
    destroy = False

    def __init__(self, request):
        self.request = request

    def can_create(self, group, instance) -> bool:
        return self.write

    def can_update(self, group, document) -> bool:
        return self.write

    def can_destroy(self, group, document) -> bool:
        return self.destroy


class ReadPermission(Permission):
    """Read permission."""

    pass


class WritePermission(Permission):
    """Read and write permission."""

    write = True


class AdminPermission(WritePermission):
    """Read, write and delete permission."""

    destroy = True


class AdminServicePermission(AdminPermission):
    """Read and write permissions for all attachments, but delete only on attachments owned by the current service."""

    def is_owned_by_service(self, group, document) -> bool:
        return not document or int(document.created_by_group) == group.service.pk

    def can_destroy(self, group, document) -> bool:
        return self.is_owned_by_service(group, document) and super().can_destroy(
            group, document
        )


class InternalReadPermission(ReadPermission):
    """Read permission on attachments owned by the current service."""

    pass


class InternalAdminPermission(AdminServicePermission):
    """Read, write and delete permission on attachments owned by the current service."""

    def can_create(self, group, instance) -> bool:
        return super().can_create(group, instance)

    def can_update(self, group, document) -> bool:
        return self.is_owned_by_service(group, document) and super().can_update(
            group, document
        )


class AdminDeletableStatePermission(AdminPermission):
    """Read and write permission, but delete only in certain states."""

    deletable_states = []

    def in_deleteable_state(self, instance) -> bool:
        return instance.instance_state.name in self.deletable_states

    def can_destroy(self, group, document) -> bool:
        return self.in_deleteable_state(
            document.instance_document.instance
        ) and super().can_destroy(
            group,
            document,
        )


class AdminStatePermission(AdminDeletableStatePermission):
    """Read, but write and delete only in certain states."""

    writable_states = []

    def in_writable_state(self, instance) -> bool:
        return instance.instance_state.name in self.writable_states

    def can_create(self, group, instance) -> bool:
        return self.in_writable_state(instance) and super().can_create(
            group,
            instance,
        )

    def can_update(self, group, document) -> bool:
        return self.in_writable_state(
            document.instance_document.instance
        ) and super().can_update(
            group,
            document,
        )


class AdminReadyWorkItemPermission(AdminPermission):
    """Read, write and delete only on work items in ready state."""

    def get_work_item(self, document_id):  # pragma: no cover
        raise NotImplementedError

    def in_ready_state(self, document=None) -> bool:
        if self.request.data["type"] == "files":
            document = Document.objects.get(pk=self.request.data["document"]["id"])

        if not document:
            document_id = self.request.data["metainfo"]["caluma-document-id"]
        else:
            document_id = document.metainfo["caluma-document-id"]

        work_item = self.get_work_item(document_id)
        return work_item and work_item.status == WorkItem.STATUS_READY

    def can_create(self, group, instance) -> bool:
        return self.in_ready_state() and super().can_create(group, instance)

    def can_update(self, group, document) -> bool:
        return self.in_ready_state(document) and super().can_update(group, document)

    def can_destroy(self, group, document) -> bool:
        return self.in_ready_state(document) and super().can_destroy(group, document)


class AdminPaperPermission(AdminPermission):
    def can_create(self, group, instance) -> bool:
        return CalumaApi().is_paper(instance) and super().can_create(group, instance)

    def can_update(self, group, document) -> bool:
        return CalumaApi().is_paper(
            document.instance_document.instance
        ) and super().can_update(group, document)

    def can_destroy(self, group, document) -> bool:
        return CalumaApi().is_paper(
            document.instance_document.instance
        ) and super().can_destroy(group, document)


class AdminNewPermission(AdminStatePermission):
    writable_states = ["new"]
    deletable_states = ["new"]


class InternalAdminCirculationPermission(
    InternalAdminPermission, AdminDeletableStatePermission
):
    deletable_states = ["circulation"]


class AdminAdditionalDemandPermission(
    AdminStatePermission, AdminReadyWorkItemPermission
):
    writable_states = ["init-distribution", "circulation"]
    deletable_states = ["init-distribution", "circulation"]

    # this is a temporary restriction
    # the end goal would be to add an event after the fill task has been completed and
    # mark those documents as not editable anymore.
    def get_work_item(self, document_id):
        return (
            WorkItem.objects.filter(
                task_id=settings.ADDITIONAL_DEMAND["ADDITIONAL_DEMAND_FILL_TASK"],
                document_id=document_id,
            )
            .order_by("-created_at")
            .first()
        )


class AdminNewPaperPermission(AdminNewPermission, AdminPaperPermission):  # noqa F405
    pass
