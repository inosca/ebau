# We need to import everything, so that we can dynamically import all permissions in permissions.py
from .permissions_base import *  # noqa F403


class AdminNewPermission(AdminStatePermission):  # noqa F405
    writable_states = ["new"]
    deletable_states = ["new"]


class InternalAdminCirculationPermission(
    InternalAdminPermission, AdminDeletableStatePermission  # noqa F405
):
    deletable_states = ["circulation"]
