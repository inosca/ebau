from django.db import models


class Attachment(models.Model):
    attachment_id = models.AutoField(
        db_column='ATTACHMENT_ID', primary_key=True)
    name = models.CharField(db_column='NAME', max_length=255)
    instance = models.ForeignKey(
        'instance.Instance', models.DO_NOTHING, db_column='INSTANCE_ID',
        related_name='attachments')
    path = models.CharField(db_column='PATH', max_length=1024)
    size = models.IntegerField(db_column='SIZE')
    date = models.DateTimeField(db_column='DATE')
    user = models.ForeignKey('user.User', models.DO_NOTHING,
                             db_column='USER_ID', related_name='attachments')
    identifier = models.CharField(db_column='IDENTIFIER', max_length=255)
    mime_type = models.CharField(db_column='MIME_TYPE', max_length=255)
    attachment_section = models.ForeignKey(
        'AttachmentSection', models.DO_NOTHING,
        db_column='ATTACHMENT_SECTION_ID', related_name='attachments')
    service = models.ForeignKey('core.Service', models.DO_NOTHING,
                                db_column='SERVICE_ID', related_name='+',
                                blank=True, null=True)
    is_parcel_picture = models.PositiveIntegerField(
        db_column='IS_PARCEL_PICTURE', default=0)
    digital_signature = models.PositiveSmallIntegerField(
        db_column='DIGITAL_SIGNATURE', default=0)
    is_confidential = models.PositiveSmallIntegerField(
        db_column='IS_CONFIDENTIAL', default=0)

    class Meta:
        managed = True
        db_table = 'ATTACHMENT'


class AttachmentExtension(models.Model):
    attachment_extension_id = models.AutoField(
        db_column='ATTACHMENT_EXTENSION_ID', primary_key=True)
    name = models.CharField(db_column='NAME', max_length=10)

    class Meta:
        managed = True
        db_table = 'ATTACHMENT_EXTENSION'


class AttachmentExtensionRole(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    attachment_extension = models.ForeignKey(
        AttachmentExtension, models.DO_NOTHING,
        db_column='ATTACHMENT_EXTENSION_ID', related_name='+')
    role = models.ForeignKey('core.Role', models.DO_NOTHING,
                             db_column='ROLE_ID', related_name='+')
    mode = models.CharField(
        db_column='MODE', max_length=10, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'ATTACHMENT_EXTENSION_ROLE'
        unique_together = (('attachment_extension', 'role'),)


class AttachmentExtensionService(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    attachment_extension = models.ForeignKey(
        AttachmentExtension, models.DO_NOTHING,
        db_column='ATTACHMENT_EXTENSION_ID', related_name='+')
    service = models.ForeignKey(
        'core.Service', models.DO_NOTHING, db_column='SERVICE_ID',
        related_name='+')
    mode = models.CharField(
        db_column='MODE', max_length=10, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'ATTACHMENT_EXTENSION_SERVICE'
        unique_together = (('attachment_extension', 'service'),)


class AttachmentSection(models.Model):
    attachment_section_id = models.AutoField(
        db_column='ATTACHMENT_SECTION_ID', primary_key=True)
    name = models.CharField(db_column='NAME', max_length=100)
    sort = models.IntegerField(db_column='SORT')

    class Meta:
        managed = True
        db_table = 'ATTACHMENT_SECTION'


class AttachmentSectionRole(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    attachment_section = models.ForeignKey(
        AttachmentSection, models.DO_NOTHING,
        db_column='ATTACHMENT_SECTION_ID', related_name='+')
    role = models.ForeignKey('core.Role', models.DO_NOTHING,
                             db_column='ROLE_ID', related_name='+')
    mode = models.CharField(
        db_column='MODE', max_length=10, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'ATTACHMENT_SECTION_ROLE'
        unique_together = (('attachment_section', 'role'),)


class AttachmentSectionService(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    attachment_section = models.ForeignKey(
        AttachmentSection, models.DO_NOTHING,
        db_column='ATTACHMENT_SECTION_ID', related_name='+')
    service = models.ForeignKey(
        'core.Service', models.DO_NOTHING, db_column='SERVICE_ID',
        related_name='+')
    mode = models.CharField(db_column='MODE', max_length=20)

    class Meta:
        managed = True
        db_table = 'ATTACHMENT_SECTION_SERVICE'
        unique_together = (('attachment_section', 'service'),)
