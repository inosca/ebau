from django.db import models
from django.utils.translation import gettext_lazy as _


class GISConfig(models.Model):
    CLIENT_SOGIS = "camac.gis.clients.sogis.SoGisClient"
    CLIENT_PARAM = "camac.gis.clients.param.ParamClient"

    CLIENT_CHOICES = [
        (CLIENT_SOGIS, _("GIS Canton Solothurn")),
        (CLIENT_PARAM, _("Parameter")),
    ]

    slug = models.SlugField(primary_key=True)
    client = models.CharField(max_length=255, choices=CLIENT_CHOICES)
    config = models.JSONField(default=dict)
    disabled = models.BooleanField(default=False)
