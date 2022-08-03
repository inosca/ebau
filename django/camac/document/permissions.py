from caluma.caluma_workflow.models import Case
from django.conf import settings
from django.db.models import Q

from camac.constants import kt_uri as uri_constants
from camac.core.models import Activation
from camac.instance.models import Instance


class Permission:
    write = False
    destroy = False

    @classmethod
    def can_write(cls, attachment, group, instance=None) -> bool:
        return cls.write

    @classmethod
    def can_destroy(cls, attachment, group) -> bool:
        return cls.destroy


class ReadPermission(Permission):
    """Read permission."""

    pass


class ReadInternalPermission(Permission):
    """Read permission on attachments owned by the current service."""

    pass


class WritePermission(ReadPermission):
    """Read and write permission."""

    write = True


class AdminPermission(WritePermission):
    """Read, write and delete permission."""

    destroy = True


class AdminServicePermission(AdminPermission):
    """Read and write permissions for all attachments but delete only on attachments owned by the current service."""

    @classmethod
    def is_owned_by_service(cls, attachment, group) -> bool:
        return not attachment or attachment.service == group.service

    @classmethod
    def can_destroy(cls, attachment, group) -> bool:
        return cls.is_owned_by_service(attachment, group) and super().can_destroy(
            attachment,
            group,
        )


class AdminInternalPermission(AdminServicePermission):
    """Read, write and delete permission on attachments owned by the current service."""

    @classmethod
    def can_write(cls, attachment, group, instance=None) -> bool:
        return cls.is_owned_by_service(attachment, group) and super().can_write(
            attachment,
            group,
            instance,
        )


class AdminBeforeDecisionPermission(AdminPermission):
    """Read and write permission, but delete only before the decision."""

    @classmethod
    def is_before_decision(cls, attachment, group) -> bool:
        return not attachment or (
            attachment.instance.instance_state.name
            not in settings.APPLICATION.get("ATTACHMENT_AFTER_DECISION_STATES", [])
        )

    @classmethod
    def can_destroy(cls, attachment, group) -> bool:
        return cls.is_before_decision(attachment, group) and super().can_destroy(
            attachment,
            group,
        )


class AdminDeleteableStatePermission(AdminPermission):
    """Read and write permission, but delete only in certain states."""

    @classmethod
    def in_deleteable_state(cls, attachment, group) -> bool:
        return not attachment or (
            attachment.instance.instance_state.name
            in settings.APPLICATION.get("ATTACHMENT_DELETEABLE_STATES", [])
        )

    @classmethod
    def can_destroy(cls, attachment, group) -> bool:
        return cls.in_deleteable_state(attachment, group) and super().can_destroy(
            attachment,
            group,
        )


class AdminServiceBeforeDecisionPermission(
    AdminBeforeDecisionPermission, AdminServicePermission
):
    """Read and write permission, but delete only conditionally.

    Deleting is allowed when all of the following conditions are true:

    - Attachment is owned by the current service
    - Instance state is before the decision
    """

    pass


class AdminServiceRunningActivationPermission(AdminServicePermission):
    """Read and write permission, but delete only conditionally.

    Deleting is allowed when all of the following conditions are true:

    - Attachment is owned by the current service
    - Service has a running activation
    """

    @classmethod
    def has_running_activation(cls, instance, group) -> bool:
        return Activation.objects.filter(
            service=group.service,
            circulation__instance=instance,
            circulation_state__name__in=settings.APPLICATION.get(
                "ATTACHMENT_RUNNING_ACTIVATION_STATES", []
            ),
        ).exists()

    @classmethod
    def can_destroy(cls, attachment, group) -> bool:
        return cls.has_running_activation(
            attachment.instance, group
        ) and super().can_destroy(attachment, group)

    @classmethod
    def can_write(cls, attachment, group, instance=None) -> bool:
        # During creation, the attachment doesn't exist yet
        instance = attachment.instance if attachment else instance
        return cls.has_running_activation(instance, group) and super().can_write(
            attachment, group, instance
        )


class AdminInternalBusinessControlPermission(AdminInternalPermission):
    """Read, write and delete permission on attachments owned by the current service for internal instances."""

    @classmethod
    def is_internal_instance(cls, instance) -> bool:
        return instance.instance_state.name in settings.APPLICATION.get(
            "ATTACHMENT_INTERNAL_STATES", []
        )

    @classmethod
    def is_case_running(cls, instance) -> bool:
        return instance.case.status == Case.STATUS_RUNNING

    @classmethod
    def can_write(cls, attachment, group, instance=None) -> bool:
        # During creation, the attachment doesn't exist yet
        instance = attachment.instance if attachment else instance
        return (
            cls.is_internal_instance(instance)
            and cls.is_case_running(instance)
            and super().can_write(attachment, group, instance)
        )

    @classmethod
    def can_destroy(cls, attachment, group) -> bool:
        instance = attachment.instance
        return (
            cls.is_internal_instance(instance)
            and cls.is_case_running(instance)
            and super().can_destroy(attachment, group)
        )


def _is_internal_instance(group, instance):
    return (
        instance.instance_state.name
        in settings.APPLICATION.get("ATTACHMENT_INTERNAL_STATES", [])
    ) and (instance.group.service == group.service)


def _is_general_instance(group, instance):
    return not _is_internal_instance(group, instance)


# Permissions configuration:
# Top-Level keys are the internal role names. The second-level keys are
# the permissions, followed by a list of sections where the permission applies.
# If not mentioned, no permission is granted.
PERMISSIONS = {
    "kt_bern": {
        "applicant": {
            AdminPermission: [1, 5, 6, 7],
            ReadPermission: [3],
        },
        # municipality
        "municipality-lead": {
            AdminBeforeDecisionPermission: [3, 12, 13],
            AdminServiceBeforeDecisionPermission: [2],
            AdminInternalPermission: [4],
            ReadPermission: [1, 7, 8],
        },
        "municipality-clerk": {
            AdminBeforeDecisionPermission: [3, 12, 13],
            AdminServiceBeforeDecisionPermission: [2],
            AdminInternalPermission: [4],
            ReadPermission: [1, 7, 8],
        },
        "municipality-readonly": {
            ReadPermission: [1, 2, 3, 7, 8, 12, 13],
            ReadInternalPermission: [4],
        },
        # service
        "service-lead": {
            AdminServiceRunningActivationPermission: [2],
            AdminInternalPermission: [4],
            ReadPermission: [1, 3, 7, 8, 13, 12],
        },
        "service-clerk": {
            AdminServiceRunningActivationPermission: [2],
            AdminInternalPermission: [4],
            ReadPermission: [1, 3, 7, 8, 13, 12],
        },
        "service-readonly": {
            ReadPermission: [1, 2, 3, 7, 8, 13, 12],
            ReadInternalPermission: [4],
        },
        "subservice": {
            AdminServiceRunningActivationPermission: [2],
            AdminInternalPermission: [4],
            ReadPermission: [1, 3, 7, 8, 13, 12],
        },
        # construction control
        "construction-control-lead": {
            AdminServicePermission: [2, 3],
            AdminPermission: [10, 11],
            AdminInternalPermission: [4],
            ReadPermission: [1, 5, 6, 7, 8, 13, 12],
        },
        "construction-control-clerk": {
            AdminServicePermission: [2, 3],
            AdminPermission: [10, 11],
            AdminInternalPermission: [4],
            ReadPermission: [1, 5, 6, 7, 8, 12, 13],
        },
        "construction-control-readonly": {
            ReadPermission: [1, 2, 3, 5, 6, 7, 8, 10, 11, 12, 13],
            ReadInternalPermission: [4],
        },
        "support": {
            AdminPermission: [1, 2, 3, 4, 5, 6, 7, 10, 11, 12, 13],
            ReadPermission: [8],
        },
    },
    "kt_schwyz": {
        "municipality": {
            AdminPermission: (
                _is_general_instance,
                [1, 4, 5, 6, 7, 8, 9, 10, 11],
            ),
            AdminInternalBusinessControlPermission: (_is_internal_instance, [12]),
        },
        "portal": {AdminDeleteableStatePermission: [1], ReadPermission: [5, 9, 4]},
        "fachstelle": {
            ReadPermission: (_is_general_instance, [1, 5, 4, 6, 9, 10, 11]),
            AdminInternalPermission: (_is_general_instance, [2]),
            AdminServicePermission: (_is_general_instance, [8]),
            AdminInternalBusinessControlPermission: (_is_internal_instance, [12]),
        },
        "kanton": {ReadPermission: [1, 2, 11], AdminPermission: [8, 6, 9, 10]},
        "publikation": {ReadPermission: [4]},
        "gemeinde sachbearbeiter": {
            AdminPermission: (_is_general_instance, [6, 7, 1, 4, 5, 8, 9, 10, 11]),
            AdminInternalBusinessControlPermission: (_is_internal_instance, [12]),
        },
        "fachstelle sachbearbeiter": {
            ReadPermission: (_is_general_instance, [1, 4, 5, 6, 9, 10, 11]),
            AdminInternalPermission: (_is_general_instance, [2]),
            AdminServicePermission: (_is_general_instance, [8]),
            AdminInternalBusinessControlPermission: (_is_internal_instance, [12]),
        },
        "fachstelle leitbehörde": {
            AdminPermission: (_is_general_instance, [1, 4, 5, 6, 7, 8, 9, 10, 11]),
            AdminInternalBusinessControlPermission: (_is_internal_instance, [12]),
        },
        "lesezugriff": {ReadPermission: [1, 8, 4, 5, 6, 10, 11]},
        "support": {AdminPermission: [1, 4, 5, 6, 7, 8, 9, 10, 11]},
    },
    "kt_uri": {
        "municipality": {
            ReadPermission: [12000002, 12000003, 12000006],
            WritePermission: [12000005, 12000003],
            AdminInternalPermission: [12000001],
            AdminServicePermission: [12000000, 12000004, 12000007],
        },
        "service": {
            ReadPermission: [12000004],
            AdminInternalPermission: [12000001],
            AdminServicePermission: [12000000, 12000002, 12000003],
        },
        "trusted_service": {
            ReadPermission: [12000004],
            AdminInternalPermission: [12000001],
            AdminServicePermission: [12000000, 12000002, 12000003],
        },
        "coordination": {
            AdminInternalPermission: [12000001],
            AdminServicePermission: [12000000, 12000002, 12000004, 12000005, 12000006],
        },
        "support": {
            AdminPermission: [
                12000000,
                12000001,
                12000002,
                12000003,
                12000004,
                12000005,
                12000006,
                12000007,
                12000008,
            ],
        },
        "organization_readonly": {ReadPermission: [12000000]},
        "commission": {ReadPermission: [12000004, 12000000, 12000002, 12000003]},
        "portal user": {AdminServicePermission: [12000000], ReadPermission: [12000001]},
        "oereb_api": {
            ReadPermission: [
                12000000,
                12000001,
                12000002,
                12000003,
                12000004,
                12000005,
                12000006,
                12000007,
                12000008,
            ],
        },
    },
    "demo": {"applicant": {AdminPermission: [250, 251]}},
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
    "kt_uri": lambda request: (
        Q(context__isDecision=True, instance__involved_applicants__invitee=request.user)
    ),
    # in test mode, we don't want to complicate the setup, so we don't enforce
    # user to be invitee
    "demo": lambda request: Q(context__isDecision=True),
}


def special_permissions_uri(group):
    if group.group_id in [uri_constants.LISAG_GROUP_ID, uri_constants.KOOR_NP_GROUP_ID]:
        return {uri_constants.LISAG_ATTACHMENT_SECTION_ID: AdminServicePermission}
    elif group.group_id in [
        uri_constants.KOOR_AFJ_GROUP_ID,
        uri_constants.SACHBEARBEITUNG_AFJ_GROUP_ID,
        uri_constants.SACHBEARBEITUNG_UND_KOORDINATION_AFJ_GROUP_ID,
    ]:
        return {uri_constants.KOOR_AFJ_ATTACHMENT_SECTION_ID: AdminServicePermission}
    elif group.group_id in [uri_constants.KOOR_BG_GROUP_ID]:
        return {
            uri_constants.MUNICIPALITY_SERVICE_ATTACHMENT_SECTION_ID: AdminServicePermission
        }
    return {}


SPECIAL_PERMISSIONS = {"kt_uri": special_permissions_uri}

PERMISSION_ORDERED = [
    ReadPermission,
    WritePermission,
    AdminInternalPermission,
    AdminInternalBusinessControlPermission,
    AdminServiceRunningActivationPermission,
    AdminServiceBeforeDecisionPermission,
    AdminServicePermission,
    AdminBeforeDecisionPermission,
    AdminPermission,
]


def rebuild_app_permissions(permissions, group, instance):
    result = {}
    for role, value in permissions.items():
        result[role] = {}
        for permission, sections in value.items():
            if type(sections) is tuple:
                is_visible, sections = sections
                if instance and not is_visible(group, instance):
                    continue

            for section in sections:
                result[role][section] = permission
    return result


def section_permissions(group, instance=None):
    role = group.role.name
    app_name = settings.APPLICATION_NAME

    if instance:
        instance = (
            instance
            if isinstance(instance, Instance)
            else Instance.objects.get(pk=instance)
        )

    # use service permissions for municipalities that are involved via
    # activation and not via instance service
    if (
        settings.APPLICATION.get("USE_INSTANCE_SERVICE")
        and instance
        and role.startswith("municipality-")
    ):
        if not instance.instance_services.filter(service=group.service).exists():
            role = role.replace("municipality-", "service-")

    all_app_permissions = rebuild_app_permissions(
        PERMISSIONS[app_name], group, instance
    )
    role_perms = settings.APPLICATIONS[app_name].get("ROLE_PERMISSIONS", {})
    role_name_int = role_perms.get(role, role).lower()
    if role_name_int not in all_app_permissions:
        # fallback
        role_name_int = role.lower()

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
