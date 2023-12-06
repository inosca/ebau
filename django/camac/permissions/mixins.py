from typing import Optional

from .api import PermissionManager


class PermissionVisibilityMixin:
    """Mixin to filter objects according to the permission module's rules.

    The queryset is filtered to only show records where a valid ACL for the
    user exists.

    To configure the mixin, you need two things:
    1) set the `instance_prefix` attribute on your class
    2) If the Mixin is not used on a viewset, you'll need to create a
       getter @property to return the request

    The `instance_prefix` tells the mixin where the instances are in the
    DB, related to the queryset/model that is dealth with here.
    """

    instance_prefix: Optional[str] = None

    def get_queryset(self):
        qs = super().get_queryset()
        manager = PermissionManager.from_request(self.request)

        qs = manager.filter_queryset(qs, self.instance_prefix)
        # Need to be distinct() because multiple ACLs could be effective
        # for the same user/instance combo
        return qs.distinct()
