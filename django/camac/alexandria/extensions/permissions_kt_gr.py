from django.conf import settings
from django.db.models import Q

# We need to import everything, so that we can dynamically import all permissions in permissions.py
from .permissions_base import *  # noqa F403


class AREPermission(Permission):  # noqa F405
    @classmethod
    def is_are_service(cls, group) -> bool:
        return group.service.pk == settings.APPLICATION["ALEXANDRIA"]["ARE_SERVICE_ID"]


class AdminServiceAREPermission(AREPermission, AdminServicePermission):  # noqa F405
    """Read, write, delete only for ARE Service."""

    @classmethod
    def can_write(cls, group, document=None) -> bool:
        return cls.is_are_service(group) and super().can_write(group, document)

    @classmethod
    def can_destroy(cls, group, document) -> bool:
        return cls.is_are_service(group) and super().can_destroy(group, document)


class ARECategoryPermission(AREPermission, AdminDeletableStatePermission):  # noqa F405
    """
    Special permission for the category Stellungnahmen ans ARE.

    Service ARE: Read
    Other services: Read Internal, write, delete only in circulation
    """

    deletable_states = ["circulation"]

    @classmethod
    def can_write(cls, group, document=None) -> bool:
        return not cls.is_are_service(group) and super().can_write(group, document)

    @classmethod
    def can_destroy(cls, group, document) -> bool:
        return not cls.is_are_service(group) and super().can_destroy(group, document)


def special_visibilities(user, role, prefix):
    visibility_filter = Q()

    if role == "service":
        # ARECategory
        if user.group != settings.APPLICATION["ALEXANDRIA"]["ARE_SERVICE_ID"]:
            visibility_filter |= Q(
                **{
                    f"{prefix}category__metainfo__access__service__iexact": "ARECategory",
                    f"{prefix}created_by_group": user.group,
                }
            )
        else:
            visibility_filter |= Q(
                **{
                    f"{prefix}category__metainfo__access__service__iexact": "ARECategory",
                }
            )

    return visibility_filter
