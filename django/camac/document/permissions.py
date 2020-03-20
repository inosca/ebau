from django.conf import settings

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
        "municipality": {"admin": [1, 4, 5, 6, 7, 8, 9]},
        "Portal": {"admin": [1], "read": [5, 9, 4]},
        "Fachstelle": {"read": [1, 5, 4, 6, 9], "adminint": [2], "adminsvc": [8]},
        "Kanton": {"read": [1, 2], "admin": [8, 6, 9]},
        "Publikation": {"read": [4]},
        "Gemeinde Sachbearbeiter": {"admin": [6, 7, 1, 4, 5, 8, 9]},
        "Fachstelle Sachbearbeiter": {
            "read": [1, 4, 5, 6, 9],
            "adminint": [2],
            "adminsvc": [8],
        },
        "Lesezugriff": {"read": [1, 8, 4, 5, 6]},
    },
    "demo": {"applicant": {"admin": [250, 251]}},
}


def section_permissions_for_role(role):
    app_name = settings.APPLICATION_NAME
    role_perms = settings.APPLICATIONS[app_name].get("ROLE_PERMISSIONS", {})
    role_name_int = role_perms.get(role.name)
    return PERMISSIONS[app_name].get(role_name_int, {})
