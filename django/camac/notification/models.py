from django.db import models


class NotificationTemplate(models.Model):
    purpose  = models.CharField(db_column='PURPOSE', max_length=100)
    subject  = models.TextField(db_column='SUBJECT')
    body     = models.TextField(db_column='BODY')

    class Meta:
        managed  = True
        db_table = 'NOTIFICATION_TEMPLATE'


class NotificationTemplateT(models.Model):
    template = models.ForeignKey(NotificationTemplate, models.DO_NOTHING,
                                 db_column='TEMPLATE_ID', related_name='+')
    language = models.CharField(db_column='LANGUAGE', max_length=2)
    purpose  = models.CharField(db_column='PURPOSE', max_length=100)
    subject  = models.TextField(db_column='SUBJECT')
    body     = models.TextField(db_column='BODY')

    class Meta:
        managed = True
        db_table = 'NOTIFICATION_TEMPLATE_T'


class ANotification(models.Model):
    action = models.OneToOneField('core.Action', models.DO_NOTHING,
                                  db_column='ACTION_ID', primary_key=True,
                                  related_name='+')
    template = models.ForeignKey(NotificationTemplate, models.DO_NOTHING,
                                 db_column='TEMPLATE_ID', related_name='+')
    recipient_type = models.CharField(
        db_column='RECIPIENT_TYPE', max_length=160
    )
    processor = models.CharField(db_column='PROCESSOR', max_length=160)

    class Meta:
        managed  = True
        db_table = 'ACTION_NOTIFICATION'
