# pragma: exclude file

from camac.permissions.events.core import EmptyEventHandler

from .common import (
    ApplicantsEventHandlerMixin,
    DistributionHandlerMixin,
    InstanceCreationHandlerMixin,
    InstanceSubmissionHandlerMixin,
)


class PermissionEventHandlerSG(
    ApplicantsEventHandlerMixin,
    DistributionHandlerMixin,
    InstanceCreationHandlerMixin,
    InstanceSubmissionHandlerMixin,
    EmptyEventHandler,
):
    pass
