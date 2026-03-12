from caluma.caluma_workflow.models import Case
from django.conf import settings
from django.db.models import Q

from camac.caluma.models import Inquiry
from camac.constants import kt_uri as uri_constants
from camac.instance.models import Instance

# Note: The permissions declared here must also be replicated (functionally and
# by name) in the corresponding Vue app, here:
#    --> (camac-ng)/php/public/public-shared/js/src/apidocuments-permissions.js
# And don't forget to register it at the bottom of the file (dasherized class
# name here must be mapped to JS permission class)


class SameServiceQSMixin:
    """Mixin to provide filter API for same-service-only document visibility.

    Implement the `build_q()` method such that only attachments are visible
    that belong to the same service as the current user.

    This is generally also referred to as the "Internal" mode
    """

    @classmethod
    def build_q(cls, group, attachment_prefix):
        # Internal - user's service must match
        return Q(**{f"{attachment_prefix}service": group.service})


class Permission:
    write = False
    destroy = False

    @classmethod
    def can_write(cls, attachment, group, instance=None) -> bool:
        return cls.write

    @classmethod
    def can_destroy(cls, attachment, group) -> bool:
        return cls.destroy

    @classmethod
    def build_q(cls, group, attachment_prefix):
        return Q()


class ReadPermission(Permission):
    """Read permission."""

    pass


class ReadInternalPermission(SameServiceQSMixin, Permission):
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


class AdminInternalPermission(SameServiceQSMixin, AdminServicePermission):
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
    def _get_states(cls):
        return settings.APPLICATION.get("ATTACHMENT_AFTER_DECISION_STATES", [])

    @classmethod
    def is_before_decision(cls, attachment, group) -> bool:
        return not attachment or (
            attachment.instance.instance_state.name not in cls._get_states()
        )

    @classmethod
    def can_destroy(cls, attachment, group) -> bool:
        return cls.is_before_decision(attachment, group) and super().can_destroy(
            attachment,
            group,
        )


class ReadWriteDuringSB1(AdminServicePermission):
    """Read and write permission, but only after the decision."""

    @classmethod
    def is_in_sb1(cls, instance, group) -> bool:
        instance_state = instance.instance_state.name
        return instance_state == "sb1"

    @classmethod
    def can_destroy(cls, attachment, group) -> bool:
        return (
            attachment
            and cls.is_in_sb1(attachment.instance, group)
            and super().can_destroy(
                attachment,
                group,
            )
        )

    @classmethod
    def can_write(cls, attachment, group, instance=None) -> bool:
        return cls.is_in_sb1(instance, group) and super().can_write(
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


class AdminServiceRunningInquiryPermission(AdminServicePermission):
    """Read and write permission, but delete only conditionally.

    Deleting is allowed when all of the following conditions are true:

    - Attachment is owned by the current service
    - Service has a running inquiry
    """

    @classmethod
    def has_running_inquiry(cls, instance, group) -> bool:
        return (
            Inquiry.objects.for_instance(instance)
            .addressed_to(group.service_id)
            .only_pending()
            .exists()
        )

    @classmethod
    def can_destroy(cls, attachment, group) -> bool:
        return cls.has_running_inquiry(
            attachment.instance, group
        ) and super().can_destroy(attachment, group)

    @classmethod
    def can_write(cls, attachment, group, instance=None) -> bool:
        # During creation, the attachment doesn't exist yet
        instance = attachment.instance if attachment else instance
        return cls.has_running_inquiry(instance, group) and super().can_write(
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
            ReadPermission: [3, 14],
        },
        # municipality
        "municipality-lead": {
            AdminBeforeDecisionPermission: [3, 12, 13, 14],
            AdminServiceBeforeDecisionPermission: [2],
            AdminInternalPermission: [4],
            ReadPermission: [1, 5, 6, 7, 8, 10, 11],
        },
        "municipality-clerk": {
            AdminBeforeDecisionPermission: [3, 12, 13, 14],
            AdminServiceBeforeDecisionPermission: [2],
            AdminInternalPermission: [4],
            ReadPermission: [1, 5, 6, 7, 8, 10, 11],
        },
        "municipality-readonly": {
            ReadPermission: [1, 2, 3, 5, 6, 7, 8, 10, 11, 12, 13, 14],
            ReadInternalPermission: [4],
        },
        # service
        "service-lead": {
            AdminServiceRunningInquiryPermission: [2],
            AdminInternalPermission: [4],
            ReadPermission: [1, 3, 5, 6, 7, 8, 10, 11, 13, 12, 14],
        },
        "service-clerk": {
            AdminServiceRunningInquiryPermission: [2],
            AdminInternalPermission: [4],
            ReadPermission: [1, 3, 5, 6, 7, 8, 10, 11, 13, 12, 14],
        },
        "service-readonly": {
            ReadPermission: [1, 2, 3, 5, 6, 7, 8, 10, 11, 13, 12, 14],
            ReadInternalPermission: [4],
        },
        "subservice": {
            AdminServiceRunningInquiryPermission: [2],
            AdminInternalPermission: [4],
            ReadPermission: [1, 3, 5, 6, 7, 8, 10, 11, 13, 12, 14],
        },
        # construction control
        "construction-control-lead": {
            AdminServicePermission: [2, 3],
            AdminPermission: [10, 11],
            AdminInternalPermission: [4],
            ReadPermission: [1, 5, 6, 7, 8, 13, 12, 14],
        },
        "construction-control-clerk": {
            AdminServicePermission: [2, 3],
            AdminPermission: [10, 11],
            AdminInternalPermission: [4],
            ReadPermission: [1, 5, 6, 7, 8, 12, 13, 14],
        },
        "construction-control-readonly": {
            ReadPermission: [1, 2, 3, 5, 6, 7, 8, 10, 11, 12, 13, 14],
            ReadInternalPermission: [4],
        },
        "support": {
            AdminPermission: [1, 2, 3, 4, 5, 6, 7, 10, 11, 12, 13, 14],
            ReadPermission: [8],
        },
        "geometer-lead": {
            # Geometer has access to all sections, but the documents
            # are explicitly marked for them
            ReadPermission: [1, 2, 3, 5, 6, 7, 11, 12, 13, 14],
            AdminInternalPermission: [4],
            # Write only on "Beilagen SB1 (Papier und Nachrichten)".  This is
            # like AdminServicePermission, but limits it to after decision.
            ReadWriteDuringSB1: [10],
        },
        "geometer-clerk": {
            # Geometer has access to all sections, but the documents
            # are explicitly marked for them
            ReadPermission: [1, 2, 3, 5, 6, 7, 11, 12, 13, 14],
            AdminInternalPermission: [4],
            # Write only on "Beilagen SB1 (Papier und Nachrichten)".  This is
            # like AdminServicePermission, but limits it to after decision.
            ReadWriteDuringSB1: [10],
        },
        "geometer-readonly": {
            # Geometer has access to all sections, but the documents
            # are explicitly marked for them
            ReadPermission: [1, 2, 3, 5, 6, 7, 10, 11, 12, 13, 14],
            ReadInternalPermission: [4],
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
                12000009,
                12000010,
                12000011,
            ],
        },
        "organization_readonly": {ReadPermission: [12000000]},
        "commission": {ReadPermission: [12000004, 12000000, 12000002, 12000003]},
        "portal user": {
            AdminServicePermission: [12000000, 12000009],
            ReadPermission: [12000001],
        },
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
        "building_commission": {
            ReadPermission: [12000000, 12000002, 12000003, 12000004]
        },
    },
    "test": {"applicant": {AdminPermission: [250, 251]}},
}


def _allow_always(*_):
    return True


def _has_documents_write_permission(level_slug, manager, instance):
    if not instance:
        return False

    return manager.has_all(instance, "documents-write")


PERMISSIONS_BY_ACCESSLEVEL = {
    "kt_bern": {
        "read": {
            ReadPermission: (_allow_always, [1, 2, 3, 5, 6, 7, 8, 10, 11, 12, 13, 14]),
            ReadInternalPermission: (_allow_always, [4]),
        },
        "geometer": {
            ReadPermission: (_allow_always, [1, 2, 3, 5, 6, 7, 8, 10, 11, 12, 13, 14]),
            ReadInternalPermission: (_allow_always, [4]),
            AdminInternalPermission: (_has_documents_write_permission, [4]),
            ReadWriteDuringSB1: (_has_documents_write_permission, [10]),
        },
        "legal-authority": {
            ReadPermission: (_allow_always, [1, 2, 3, 5, 6, 7, 8, 10, 11, 12, 13, 14]),
            ReadInternalPermission: (_allow_always, [4]),
            AdminInternalPermission: (_has_documents_write_permission, [4]),
        },
        "applicant": {
            # TODO: In theory, certain attachment sections should only be
            # editable at a certain time (e.g. Nachforderungen only if additional-demands
            # are writeable)
            AdminPermission: (_has_documents_write_permission, [1, 5, 6, 7]),
            ReadPermission: (_allow_always, [3, 14]),
        },
    },
    "kt_schwyz": {
        "read": {
            # TODO proper definition of permissions
            # All sections excluding internal sections (2, 7) and
            # section for applicant (9)
            ReadPermission: (_allow_always, [1, 4, 5, 6, 8, 10, 11]),
        },
    },
    "kt_uri": {
        "read": {
            # TODO proper definition of permissions
            # Same sections included as for service excluding
            # internal section
            ReadPermission: (
                _allow_always,
                [
                    12000000,
                    12000002,
                    12000003,
                    12000004,
                    12000005,
                ],
            ),
        }
    },
}


def get_accesslevel_permissions(
    level_slug, manager, instance=None
) -> dict[type[Permission], list[int]]:
    """Return a dict that maps permission types to a list of applicable sections.

    If no config is defined for the given access level, an empty dict is returned.
    A callback condition needs to be configured for every permission config, which
    determines whether the permission currently applies for the defined sections.
    """
    app_name = settings.APPLICATION_NAME

    canton_config = PERMISSIONS_BY_ACCESSLEVEL.get(app_name, {})
    level_config = canton_config.get(level_slug, {})

    filtered_level_config = {
        perm: section_ids
        for perm, (callback, section_ids) in level_config.items()
        if callback(level_slug, manager, instance)
    }

    return filtered_level_config


# Loosen filters allow additional visibility. They are used as an "OR"
# to the other filters, and as such can be used to allow additional
# access to attachments.
# Don't set a filter for your application (and don't set it to None)
# if this feature not used!
LOOSEN_FILTERS = {
    "kt_bern": lambda request: Q(
        context__isDecision=True, instance__involved_applicants__invitee=request.user
    ),
    "kt_uri": lambda request: Q(
        context__isDecision=True, instance__involved_applicants__invitee=request.user
    ),
    # in test mode, we don't want to complicate the setup, so we don't enforce
    # user to be invitee
    "test": lambda request: Q(context__isDecision=True),
}


def special_permissions_uri(group):
    if group.group_id == uri_constants.LISAG_GROUP_ID:
        return {uri_constants.LISAG_ATTACHMENT_SECTION_ID: AdminServicePermission}
    elif group.service and (
        group.service.slug == "rechtsvertretung-altdorf"
        or group.name == "Baukommission Altdorf"
    ):
        return {uri_constants.APPEAL_DOCUMENTS_SECTION_ID: ReadPermission}
    elif group.group_id == uri_constants.KOOR_AFJ_GROUP_ID:
        return {
            uri_constants.KOOR_AFJ_ATTACHMENT_SECTION_ID: AdminServicePermission,
            uri_constants.LISAG_ATTACHMENT_SECTION_ID: AdminServicePermission,
        }
    elif group.group_id in [
        uri_constants.KOOR_AFJ_GROUP_ID,
        uri_constants.SACHBEARBEITUNG_AFJ_GROUP_ID,
        uri_constants.SACHBEARBEITUNG_UND_KOORDINATION_AFJ_GROUP_ID,
    ]:
        return {uri_constants.KOOR_AFJ_ATTACHMENT_SECTION_ID: AdminServicePermission}
    elif group.group_id == uri_constants.KOOR_BG_GROUP_ID:
        return {
            uri_constants.MUNICIPALITY_SERVICE_ATTACHMENT_SECTION_ID: AdminServicePermission
        }
    elif group.group_id == uri_constants.KOOR_NP_GROUP_ID:
        return {
            uri_constants.MUNICIPALITY_SERVICE_ATTACHMENT_SECTION_ID: AdminServicePermission,
            uri_constants.LISAG_ATTACHMENT_SECTION_ID: AdminServicePermission,
            uri_constants.ARE_ATTACHMENT_SECTION_ID: AdminServicePermission,
        }
    elif group.group_id == uri_constants.KOOR_BD_GROUP_ID:
        return {uri_constants.LISAG_ATTACHMENT_SECTION_ID: AdminServicePermission}
    elif group.group_id == uri_constants.KOOR_AFU_GROUP_ID:
        return {uri_constants.LISAG_ATTACHMENT_SECTION_ID: AdminServicePermission}
    elif group.group_id in uri_constants.DOCUMENTS_ARE_GROUPS:
        return {uri_constants.ARE_ATTACHMENT_SECTION_ID: AdminServicePermission}
    elif group.group_id in uri_constants.DOCUMENTS_AFU_GROUPS:
        return {uri_constants.AFU_ATTACHMENT_SECTION_ID: AdminServicePermission}
    return {}


SPECIAL_PERMISSIONS = {"kt_uri": special_permissions_uri}

PERMISSION_ORDERED = [
    ReadPermission,
    WritePermission,
    AdminInternalPermission,
    AdminInternalBusinessControlPermission,
    AdminServiceRunningInquiryPermission,
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
    # activation and not via instance service. Involved instance services
    # (not active) should be treated as services involved via activation.
    if (
        settings.APPLICATION.get("USE_INSTANCE_SERVICE")
        and instance
        and role.startswith("municipality-")
    ):
        if not instance.instance_services.filter(
            service=group.service, active=1
        ).exists():
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


class SectionPermissions:
    def __init__(self, manager):
        self.manager = manager

    def get_permissions(self, section, group, instance=None) -> list[type[Permission]]:
        """Return a list of permission classes relevant for the given section.

        If we are in single-instance mode (instance parameter is given) AND
        the user has access levels on the instance, the traditional role-based
        permissions are ignored and only accesslevel-based permissions are used.
        """
        access_levels = self.manager.current_access_levels(instance) if instance else []

        if not access_levels:
            section_perm = section_permissions(group, instance).get(section.pk)
            return [section_perm] if section_perm else []

        # Else: Enforce access-level permissions, ignore role-based permissions
        perms = [
            get_accesslevel_permissions(level, self.manager, instance)
            for level in access_levels
        ]
        # perms: list of permisssion => list-of-section-ids

        relevant_permissions = []
        for perm_config in perms:
            for perm, section_ids in perm_config.items():
                if section.pk in section_ids:
                    relevant_permissions.append(perm)

        return relevant_permissions

    def can_destroy(self, section, attachment, group):
        permission_classes = self.get_permissions(section, group, attachment.instance)
        return any(
            permission_class.can_destroy(attachment, group)
            for permission_class in permission_classes
            if permission_class
        )

    def can_write(self, section, attachment, group, instance=None):
        permission_classes = self.get_permissions(section, group, instance)
        return any(
            permission_class.can_write(attachment, group, instance)
            for permission_class in permission_classes
            if permission_class
        )
