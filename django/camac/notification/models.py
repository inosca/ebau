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
