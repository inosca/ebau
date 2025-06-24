from caluma.caluma_workflow.models import WorkItem

from camac.caluma.extensions.events.construction_monitoring import (
    is_tax_administration_involved,
)
from camac.instance.models import Instance
from camac.instance.utils import get_localized_geometer
from camac.permissions import api as permissions_api
from camac.permissions.events import EmptyEventHandler
from camac.user.utils import get_tax_administration


class PermissionEventHandlerSZ(
    EmptyEventHandler,
):
    def instance_completed(self, instance: Instance):
        work_item: WorkItem = WorkItem.objects.get(
            task_id="complete-instance", case_id=instance.case_id
        )
        if is_tax_administration_involved(work_item):
            self.manager.grant(
                instance,
                grant_type=permissions_api.GRANT_CHOICES.SERVICE.value,
                access_level="read",
                service=get_tax_administration(),
            )

    def decision_decreed(self, instance: Instance):
        if geometer_service := get_localized_geometer(instance):
            self.manager.grant(
                instance,
                grant_type=permissions_api.GRANT_CHOICES.SERVICE.value,
                access_level="read",
                service=geometer_service,
            )
