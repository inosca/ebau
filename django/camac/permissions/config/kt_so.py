from camac.instance.models import Instance
from camac.permissions import models as permissions_models
from camac.permissions.events import EmptyEventHandler

from .common import (
    ApplicantsEventHandlerMixin,
    DistributionHandlerMixin,
    GrantSupportOnCreationHandlerMixin,
    InstanceSubmissionHandlerMixin,
)


class PermissionEventHandlerSO(
    ApplicantsEventHandlerMixin,
    DistributionHandlerMixin,
    GrantSupportOnCreationHandlerMixin,
    InstanceSubmissionHandlerMixin,
    EmptyEventHandler,
):
    def instance_submitted(self, instance: Instance):
        super().instance_submitted(instance)

        for acl in permissions_models.InstanceACL.currently_active().filter(
            instance=instance,
            access_level="municipality-before-submission",
        ):
            self.manager.revoke(acl)
