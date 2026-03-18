# pragma: exclude file

from camac.permissions.events.core import EmptyEventHandler

from .common import (
    ApplicantsEventHandlerMixin,
    InstanceCreationHandlerMixin,
    InstanceSubmissionHandlerMixin,
)


class PermissionEventHandlerSG(
    ApplicantsEventHandlerMixin,
    InstanceCreationHandlerMixin,
    InstanceSubmissionHandlerMixin,
    EmptyEventHandler,
):
    pass
