# pragma: exclude file

from camac.permissions.events import EmptyEventHandler

from .common import (
    ApplicantsEventHandlerMixin,
    InstanceCreationHandlerMixin,
    InstanceSubmissionHandlerMixin,
)


class PermissionEventHandlerAG(
    ApplicantsEventHandlerMixin,
    InstanceCreationHandlerMixin,
    InstanceSubmissionHandlerMixin,
    EmptyEventHandler,
):
    pass
