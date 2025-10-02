from django.contrib import admin
from django.contrib.auth.models import Group as DjangoGroup
from django_celery_beat import admin as dcb_admin
from django_q import admin as q_admin

from camac.user.admin.views import *  # noqa 401, 403

admin.site.unregister(DjangoGroup)

# django-q
admin.site.unregister(q_admin.Success)
admin.site.unregister(q_admin.Failure)
admin.site.unregister(q_admin.Schedule)
admin.site.unregister(q_admin.OrmQ)

# django-celery-beat
admin.site.unregister(dcb_admin.PeriodicTask)
admin.site.unregister(dcb_admin.ClockedSchedule)
admin.site.unregister(dcb_admin.CrontabSchedule)
admin.site.unregister(dcb_admin.SolarSchedule)
admin.site.unregister(dcb_admin.IntervalSchedule)
