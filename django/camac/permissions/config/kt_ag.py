# pragma: exclude file

from camac.permissions.events import EmptyEventHandler

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
    pass
