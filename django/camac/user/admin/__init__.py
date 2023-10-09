from django.contrib import admin
from django.contrib.auth.models import Group as DjangoGroup
from django_q import admin as q_admin

from camac.user.admin.views import *  # noqa 401, 403

admin.site.unregister(DjangoGroup)
admin.site.unregister(q_admin.Success)
admin.site.unregister(q_admin.Failure)
admin.site.unregister(q_admin.Schedule)
admin.site.unregister(q_admin.OrmQ)
