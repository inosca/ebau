from caluma.caluma_workflow.models import WorkItem

from camac.instance.master_data import MasterData
from camac.instance.models import Instance
from camac.permissions import models as permissions_models
from camac.permissions.events import EmptyEventHandler

from .common import (
    ApplicantsEventHandlerMixin,
    DistributionHandlerMixin,
    GeometerHandlerMixin,
    InstanceCopyHandlerMixin,
    InstanceCreationHandlerMixin,
    InstanceSubmissionHandlerMixin,
)


class PermissionEventHandlerSO(
    GeometerHandlerMixin,
    ApplicantsEventHandlerMixin,
    DistributionHandlerMixin,
    InstanceCreationHandlerMixin,
    InstanceSubmissionHandlerMixin,
    InstanceCopyHandlerMixin,
    EmptyEventHandler,
):
    def instance_submitted(self, instance: Instance):
        super().instance_submitted(instance)

        for acl in permissions_models.InstanceACL.currently_active().filter(
            instance=instance,
            access_level="municipality-before-submission",
        ):
            self.manager.revoke(acl)

    def formal_exam_completed(self, instance: Instance, work_item: WorkItem):
        master_data = MasterData.from_case_id(instance.case.pk)
        if not master_data.geometer_required:
            return

        self.grant_geometer_permission(work_item)
