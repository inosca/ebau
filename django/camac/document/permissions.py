from django.conf import settings
from django.db.models import Q

from camac.constants import kt_uri as uri_constants

# Permissions configuration:
# Top-Level keys are the internal role names. The second-level keys are
# the permissions, followed by a list of sections where the permission applies.
# If not mentioned, no permission is granted.
#
# Permission types:
#   * "read"
#   * "write" (read+write, NO DELETE)
#   * "admin" (read+write+delete)
#   * "adminsvc" (admin, but only delete documents where service=self.group.service)
#   * "adminint" (admin, but can only see documents created within own service)
PERMISSIONS = {
    "kt_bern": {
        "municipality-lead": {
            "read": [1, 7, 8],
            "adminsvc": [2, 3],
            "adminint": [4],
            "admin": [13, 12],
        },
        "applicant": {"admin": [1, 5, 6, 7, 13, 10, 11, 12], "read": [3]},
        "service-lead": {
            "adminsvc": [2],
            "read": [3, 1, 7, 8, 13, 12],
            "adminint": [4],
        },
        "service-clerk": {
            "adminint": [4],
            "read": [1, 3, 7, 8, 13, 12],
            "adminsvc": [2],
        },
        "construction-control-lead": {
            "adminsvc": [2, 3],
            "read": [1, 5, 6, 7, 8, 13, 12],
            "adminint": [4],
            "admin": [10, 11],
        },
        "support": {"admin": [1, 2, 3, 4, 5, 6, 7, 13, 10, 11, 12], "read": [8]},
        "service-readonly": {"read": [1, 2, 3, 4, 7, 8, 13, 12]},
        "municipality-readonly": {"read": [1, 2, 3, 4, 7, 8, 13, 12]},
        "construction-control-readonly": {
            "read": [1, 2, 3, 4, 5, 6, 7, 8, 13, 10, 11, 12]
        },
        "subservice": {"adminsvc": [2], "read": [1, 3, 7, 8, 13, 12], "adminint": [4]},
        "municipality-clerk": {
            "adminint": [4],
            "read": [1, 7, 8],
            "adminsvc": [2, 3],
            "admin": [13, 12],
        },
        "construction-control-clerk": {
            "adminint": [4],
            "read": [1, 5, 6, 7, 8, 13, 12],
            "adminsvc": [2, 3],
            "admin": [10, 11],
        },
    },
    "kt_schwyz": {
        "municipality": {"admin": [1, 4, 5, 6, 7, 8, 9, 10, 11]},
        "portal": {"admin": [1], "read": [5, 9, 4]},
        "fachstelle": {
            "read": [1, 5, 4, 6, 9, 10, 11],
            "adminint": [2],
            "adminsvc": [8],
        },
        "kanton": {"read": [1, 2, 11], "admin": [8, 6, 9, 10]},
        "publikation": {"read": [4]},
        "gemeinde sachbearbeiter": {"admin": [6, 7, 1, 4, 5, 8, 9, 10, 11]},
        "fachstelle sachbearbeiter": {
            "read": [1, 4, 5, 6, 9, 10, 11],
            "adminint": [2],
            "adminsvc": [8],
        },
        "fachstelle leitbehörde": {"admin": [1, 4, 5, 6, 7, 8, 9, 10, 11]},
        "lesezugriff": {"read": [1, 8, 4, 5, 6, 10, 11]},
    },
    "kt_uri": {
        "municipality": {
            "read": [
                12000002,
                12000003,
                12000006,
            ],
            "write": [
                12000005,
            ],
            "adminint": [12000001],
            "adminsvc": [
                12000000,
                12000004,
                12000007,
            ],
        },
        "service": {
            "read": [
                12000004,
            ],
            "adminint": [12000001],
            "adminsvc": [
                12000000,
                12000002,
                12000003,
            ],
        },
        "trusted_service": {
            "read": [
                12000004,
            ],
            "adminint": [12000001],
            "adminsvc": [
                12000000,
                12000002,
                12000003,
            ],
        },
        "coordination": {
            "adminint": [12000001],
            "adminsvc": [
                12000000,
                12000002,
                12000004,
                12000005,
                12000006,
            ],
        },
        "support": {
            "admin": [
                12000000,
                12000001,
                12000002,
                12000003,
                12000004,
                12000005,
                12000006,
                12000007,
            ],
        },
        "organization_readonly": {"read": [12000000]},
        "commission": {
            "read": [
                12000004,
                12000000,
                12000002,
                12000003,
            ]
        },
        "portal user": {"adminsvc": [12000000]},
    },
    "demo": {"applicant": {"admin": [250, 251]}},
}

# Custom attachment validators. Use this to apply any custom validation rules
VALIDATE_ATTACHMENTS = {}

# Loosen filters allow additional visibility. They are used as an "OR"
# to the other filters, and as such can be used to allow additional
# access to attachments.
# Don't set a filter for your application (and don't set it to None)
# if this feature not used!
LOOSEN_FILTERS = {
    "kt_bern": lambda request: Q(
        context__isDecision=True, instance__involved_applicants__invitee=request.user
    ),
    "kt_uri": lambda request: (
        Q(context__isPublished=True)
        | Q(
            context__isDecision=True,
            instance__involved_applicants__invitee=request.user,
        )
    ),
    # in test mode, we don't want to complicate the setup, so we don't enforce
    # user to be invitee
    "demo": lambda request: Q(context__isDecision=True),
}


def special_permissions_uri(group):
    if group.group_id in [uri_constants.LISAG_GROUP_ID, uri_constants.KOOR_NP_GROUP_ID]:
        return {uri_constants.LISAG_ATTACHMENT_SECTION_ID: "adminsvc"}
    return {}


SPECIAL_PERMISSIONS = {"kt_uri": special_permissions_uri}

PERMISSION_ORDERED = ["read", "write", "adminint", "adminsvc", "admin"]


def rebuild_app_permissions(permissions):
    result = {}
    for role, value in permissions.items():
        result[role] = {}
        for permission, sections in value.items():
            for section in sections:
                result[role][section] = permission
    return result


def section_permissions(group):
    role = group.role
    app_name = settings.APPLICATION_NAME
    all_app_permissions = rebuild_app_permissions(PERMISSIONS[app_name])
    role_perms = settings.APPLICATIONS[app_name].get("ROLE_PERMISSIONS", {})
    role_name_int = role_perms.get(role.name, role.name).lower()

    if role_name_int not in all_app_permissions:
        # fallback
        role_name_int = role.name.lower()

    app_permissions = all_app_permissions.get(role_name_int, {})
    special_permissions = SPECIAL_PERMISSIONS.get(app_name, lambda _: None)(group)

    if not special_permissions:
        return app_permissions

    for section, special_permission in special_permissions.items():
        regular_permission = all_app_permissions[role_name_int].get(section)
        if not regular_permission or PERMISSION_ORDERED.index(
            special_permission
        ) > PERMISSION_ORDERED.index(regular_permission):
            app_permissions[section] = special_permission

    return app_permissions
