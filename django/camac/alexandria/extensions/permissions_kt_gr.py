from caluma.caluma_workflow.models import WorkItem
from django.conf import settings

# We need to import everything, so that we can dynamically import all permissions in permissions.py
from .permissions_base import *  # noqa F403


class AdminNewPermission(AdminStatePermission):  # noqa F405
    writable_states = ["new"]
    deletable_states = ["new"]


class InternalAdminCirculationPermission(
    InternalAdminPermission, AdminDeletableStatePermission  # noqa F405
):
    deletable_states = ["circulation"]


class AdminAdditionalDemandPermission(
    AdminStatePermission, AdminReadyWorkItemPermission  # noqa F405
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
