from logging import getLogger

from caluma.core.mutation import Mutation
from caluma.core.permissions import (
    BasePermission,
    object_permission_for,
    permission_for,
)

log = getLogger()

"""Caluma permissions for Kanton Bern"""


class CustomPermission(BasePermission):
    @object_permission_for(Mutation)
    def has_object_permission_default(self, mutation, info, instance):
        operation = mutation.__name__
        log.warning(
            f"ACL: fallback object permission: allowing "
            f"mutation '{operation}' on {instance}"
        )
        return True

    @permission_for(Mutation)
    def has_permission_default(self, mutation, info):
        operation = mutation.__name__
        log.warning(f"fallback permission: allowing mutation '{operation}'")
        return True
