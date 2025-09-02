from camac.instance.models import Instance
from camac.instance.utils import get_geometer_service
from camac.permissions import api as permissions_api
from camac.permissions.events import EmptyEventHandler
from camac.user.utils import get_tax_administration


class PermissionEventHandlerSZ(
    EmptyEventHandler,
):
    def instance_completed(self, instance: Instance):
        self.manager.grant(
            instance,
            grant_type=permissions_api.GRANT_CHOICES.SERVICE.value,
            access_level="read",
            service=get_tax_administration(),
        )

    def decision_decreed(self, instance: Instance):
        if geometer_service := get_geometer_service(instance):
            self.manager.grant(
                instance,
                grant_type=permissions_api.GRANT_CHOICES.SERVICE.value,
                access_level="read",
                service=geometer_service,
            )
