import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class GISDataSource(models.Model):
    CLIENT_SOGIS = "camac.gis.clients.sogis.SoGisClient"
    CLIENT_PARAM = "camac.gis.clients.param.ParamGisClient"
    CLIENT_ADMIN = "camac.gis.clients.admin.AdminGisClient"
    CLIENT_KT_GR = "camac.gis.clients.gr.GrGisClient"

    CLIENT_CHOICES = [
        (CLIENT_SOGIS, _("GIS Canton Solothurn")),
        (CLIENT_KT_GR, _("GIS Canton GR")),
        (CLIENT_PARAM, _("Parameter")),
        (CLIENT_ADMIN, _("Federal GIS Switzerland")),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.CharField(max_length=255)
    client = models.CharField(max_length=255, choices=CLIENT_CHOICES)
    config = models.JSONField(default=dict)
    disabled = models.BooleanField(default=False)
