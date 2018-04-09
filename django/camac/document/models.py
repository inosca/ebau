from django.db import models
from django.utils import timezone


def attachment_path_directory_path(attachment, filename):
    return 'attachments/files/{0}/{1}'.format(attachment.instance.pk, filename)


class AttachmentQuerySet(models.QuerySet):
    def filter_group(self, group):
        attachment_sections = AttachmentSection.objects.filter_group(group)
        return self.filter(attachment_section__in=attachment_sections)


class Attachment(models.Model):
    objects = AttachmentQuerySet.as_manager()

    attachment_id = models.AutoField(
        db_column='ATTACHMENT_ID', primary_key=True)
    name = models.CharField(db_column='NAME', max_length=255)
    instance = models.ForeignKey(
        'instance.Instance', models.CASCADE, db_column='INSTANCE_ID',
        related_name='attachments')
    path = models.FileField(db_column='PATH', max_length=1024,
                            upload_to=attachment_path_directory_path)
    size = models.IntegerField(db_column='SIZE')
    date = models.DateTimeField(db_column='DATE', default=timezone.now)
    user = models.ForeignKey('user.User', models.PROTECT,
                             db_column='USER_ID', related_name='attachments')
    mime_type = models.CharField(db_column='MIME_TYPE', max_length=255)
    attachment_section = models.ForeignKey(
        'AttachmentSection', models.PROTECT,
        db_column='ATTACHMENT_SECTION_ID', related_name='attachments')
    is_parcel_picture = models.PositiveIntegerField(
        db_column='IS_PARCEL_PICTURE', default=0)
    digital_signature = models.PositiveSmallIntegerField(
        db_column='DIGITAL_SIGNATURE', default=0)
    is_confidential = models.PositiveSmallIntegerField(
        db_column='IS_CONFIDENTIAL', default=0)

    identifier = models.CharField(db_column='IDENTIFIER', max_length=255,
                                  blank=True, null=True)
    """
    In old Camac Document module this identifier is used for identification
    and to build thumbnail path.
    Is only present for backwards compatability.
    """

    group = models.ForeignKey('user.Group', models.SET_NULL,
                              related_name='attachments', null=True)
    """
    Group attachment has been uploaded with. Needs to be nullable
    (but not blank!) for db backwards compatibility with old plain camac
    document module.
    """

    service = models.ForeignKey('user.Service', models.SET_NULL,
                                db_column='SERVICE_ID', related_name='+',
                                blank=True, null=True)
    """
    We use group instead of service in api - this field is only still present
    for backwards compatibility with old plain camac document module.
    """

    class Meta:
        managed = True
        db_table = 'ATTACHMENT'


class AttachmentSectionQuerySet(models.QuerySet):
    def filter_group(self, group):

        role_sections = AttachmentSectionRoleAcl.objects.filter(
            role=group.role_id
        ).values('attachment_section')

        group_sections = AttachmentSectionGroupAcl.objects.filter(
            group=group
        ).values('attachment_section')

        return self.filter(
            models.Q(pk__in=role_sections) | models.Q(pk__in=group_sections)
        )


class AttachmentSection(models.Model):
    objects = AttachmentSectionQuerySet.as_manager()
    attachment_section_id = models.AutoField(
        db_column='ATTACHMENT_SECTION_ID', primary_key=True)
    name = models.CharField(db_column='NAME', max_length=100, unique=True)
    sort = models.IntegerField(db_column='SORT', db_index=True, default=0)

    def get_mode(self, group):
        # TODO: quick implementation
        # amount of queries could be improved with subqueries and annotating
        # mode to model - not trivial though
        group_modes = AttachmentSectionGroupAcl.objects.filter(
            attachment_section=self,
            group=group
        ).values('mode')
        role_modes = AttachmentSectionRoleAcl.objects.filter(
            attachment_section=self,
            role=group.role_id
        ).values('mode')

        return group_modes.union(role_modes)[0]['mode']

    class Meta:
        managed = True
        db_table = 'ATTACHMENT_SECTION'


WRITE_PERMISSION = 'write'
READ_PERMISSION = 'read'
ADMIN_PERMISSION = 'admin'

ATTACHMENT_MODE = (
    (READ_PERMISSION, 'Read permissions'),
    (WRITE_PERMISSION, 'Read and write permissions'),
    (ADMIN_PERMISSION, 'Read, write and delete permissions')
)


class AttachmentSectionRoleAcl(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    attachment_section = models.ForeignKey(
        AttachmentSection, models.CASCADE,
        db_column='ATTACHMENT_SECTION_ID', related_name='role_acls')
    role = models.ForeignKey('user.Role', models.CASCADE,
                             db_column='ROLE_ID', related_name='+')
    mode = models.CharField(db_column='MODE', max_length=10,
                            choices=ATTACHMENT_MODE)

    class Meta:
        managed = True
        db_table = 'ATTACHMENT_SECTION_ROLE'
        unique_together = (('attachment_section', 'role'),)


class AttachmentSectionGroupAcl(models.Model):
    attachment_section = models.ForeignKey(
        AttachmentSection, models.CASCADE, related_name='group_acls')
    group = models.ForeignKey('user.Group', models.CASCADE, related_name='+')
    mode = models.CharField(max_length=10, choices=ATTACHMENT_MODE)

    class Meta:
        unique_together = (('attachment_section', 'group'),)


class AttachmentSectionServiceAcl(models.Model):
    """
    Defines what service may see what attachment section acl.

    Only here for backwards compatability as used by
    old plain Camac document module.
    AttachmentSectionGroupAcl should be used instead.
    """

    id = models.AutoField(db_column='ID', primary_key=True)
    attachment_section = models.ForeignKey(
        AttachmentSection, models.CASCADE,
        db_column='ATTACHMENT_SECTION_ID', related_name='+')
    service = models.ForeignKey(
        'user.Service', models.CASCADE, db_column='SERVICE_ID',
        related_name='+')
    mode = models.CharField(db_column='MODE', max_length=20)

    class Meta:
        managed = True
        db_table = 'ATTACHMENT_SECTION_SERVICE'
        unique_together = (('attachment_section', 'service'),)


class Template(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    name = models.CharField(max_length=255, unique=True, db_column='NAME')
    path = models.FileField(max_length=1024, upload_to='templates',
                            db_column='PATH')

    class Meta:
        db_table = 'TEMPLATE'
