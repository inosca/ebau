from camac.instance.models import Instance
from camac.permissions import models as permissions_models
from camac.permissions.events import EmptyEventHandler


class PermissionEventHandlerSO(EmptyEventHandler):
    def instance_submitted(self, instance: Instance):
        if instance.instance_state.name != "subm":
            return

        for acl in permissions_models.InstanceACL.currently_active().filter(
            instance=instance,
            access_level="municipality-before-submission",
        ):
            self.manager.revoke(acl)
