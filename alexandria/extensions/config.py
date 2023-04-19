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


PERMISSIONS = {
    "kt_gr": {
        "applicant": {"admin": ["beilagen-zum-gesuch"]},
        "municipality": {},
        "service": {},
        "support": {"admin": ["beilagen-zum-gesuch"]},
    }
}

PERMISSION_ORDERED = [
    ReadPermission,
    WritePermission,
    AdminInternalPermission,
    AdminServicePermission,
    AdminPermission,
]