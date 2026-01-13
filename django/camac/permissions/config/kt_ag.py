# pragma: exclude file

from camac.permissions.events import EmptyEventHandler
from camac.user.models import Service, ServiceGroup

from .common import (
    ApplicantsEventHandlerMixin,
    DistributionHandlerMixin,
    InstanceCreationHandlerMixin,
    InstanceSubmissionHandlerMixin,
)


class PermissionEventHandlerAG(
    ApplicantsEventHandlerMixin,
    DistributionHandlerMixin,
    InstanceCreationHandlerMixin,
    InstanceSubmissionHandlerMixin,
    EmptyEventHandler,
):
    def inquiry_sent(self, instance, work_item):
        super().inquiry_sent(instance, work_item)
        if str(Service.objects.get(slug="afb").pk) in work_item.addressed_groups:
            self.manager.grant(
                instance,
                grant_type="SERVICE_GROUP",
                access_level="read",
                service_group=ServiceGroup.objects.get(slug="service-cantonal"),
                event_name="inquiry-sent",
            )
