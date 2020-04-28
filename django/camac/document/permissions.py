from django.conf import settings
from django.db.models import Q
from django.utils.translation import gettext as _
from rest_framework import exceptions

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
        "portal": {"admin": [1], "read": [5, 9, 4]},
        "fachstelle": {"read": [1, 5, 4, 6, 9], "adminint": [2], "adminsvc": [8]},
        "kanton": {"read": [1, 2], "admin": [8, 6, 9]},
        "publikation": {"read": [4]},
        "gemeinde sachbearbeiter": {"admin": [6, 7, 1, 4, 5, 8, 9]},
        "fachstelle sachbearbeiter": {
            "read": [1, 4, 5, 6, 9],
            "adminint": [2],
            "adminsvc": [8],
        },
        "lesezugriff": {"read": [1, 8, 4, 5, 6]},
    },
    "demo": {"applicant": {"admin": [250, 251]}},
}


def ensure_active_service_for_context_update(serializer, data):
    """Enforce changes to the context field only happen by active service.

    In EBAU-BE, the context contains flags whether an attachment is a decision,
    which only users of the active service (Leitbehörde) are allowed to change.
    """
    if not serializer.instance:
        return data

    user_service = serializer.context["request"].group.service
    attachment = serializer.instance
    active_service = attachment.instance.active_service()

    if not user_service or (
        active_service != user_service
        and data.get("context", attachment.context) != attachment.context
    ):
        # context changed, but we're not active service
        raise exceptions.ValidationError(_("Only active service can change context"))
    return data


# Custom attachment validators. Use this to apply any custom validation rules
VALIDATE_ATTACHMENTS = {
    "kt_bern": ensure_active_service_for_context_update,
    "demo": ensure_active_service_for_context_update,
}

# Loosen filters allow additional visibility. They are used as an "OR"
# to the other filters, and as such can be used to allow additional
# access to attachments.
# Don't set a filter for your application (and don't set it to None)
# if this feature not used!
LOOSEN_FILTERS = {
    "kt_bern": lambda request: Q(
        context__isDecision=True, instance__involved_applicants__invitee=request.user
    ),
    # in test mode, we don't want to complicate the setup, so we don't enforce
    # user to be invitee
    "demo": lambda request: Q(context__isDecision=True),
}


def section_permissions_for_role(role):
    app_name = settings.APPLICATION_NAME
    app_permissions = PERMISSIONS[app_name]
    role_perms = settings.APPLICATIONS[app_name].get("ROLE_PERMISSIONS", {})
    role_name_int = role_perms.get(role.name, role.name).lower()
    if role_name_int not in app_permissions:
        # fallback
        role_name_int = role.name.lower()
    return app_permissions.get(role_name_int, {})
