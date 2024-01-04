import uuid
from importlib import import_module

from django.db import models
from django.utils.translation import gettext_lazy as _

from camac.models import dynamic_default_value


@dynamic_default_value(0)
def next_datasource_sort():
    last = GISDataSource.objects.order_by("-sort").first()
    return last.sort + 1 if last else 0


class GISDataSource(models.Model):
    CLIENT_SOGIS = "camac.gis.clients.sogis.SoGisClient"
    CLIENT_PARAM = "camac.gis.clients.param.ParamGisClient"
    CLIENT_ADMIN = "camac.gis.clients.admin.AdminGisClient"
    CLIENT_KT_GR = "camac.gis.clients.gr.GrGisClient"
    CLIENT_ECH_0206 = "camac.gis.clients.ech_0206.Ech0206"
    CLIENT_BEGIS = "camac.gis.clients.begis.BeGisClient"

    CLIENT_CHOICES = [
        (CLIENT_SOGIS, _("GIS Canton Solothurn")),
        (CLIENT_KT_GR, _("GIS Canton GR")),
        (CLIENT_BEGIS, _("GIS Canton Bern")),
        (CLIENT_PARAM, _("Parameter")),
        (CLIENT_ECH_0206, _("Ech0206")),
        (CLIENT_ADMIN, _("Federal GIS Switzerland")),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.CharField(max_length=255)
    client = models.CharField(max_length=255, choices=CLIENT_CHOICES)
    config = models.JSONField(default=dict)
    disabled = models.BooleanField(default=False)
    sort = models.IntegerField(default=next_datasource_sort)

    class Meta:
        ordering = ["sort"]

    def get_client_cls(self):
        parts = self.client.split(".")
        class_name = parts.pop()

        return getattr(import_module(".".join(parts)), class_name)

    def get_required_params(self):
        client = self.get_client_cls()
        if hasattr(client, "required_params"):
            return client.required_params
        return client.get_required_params(self)

    def get_is_queue_enabled(self):
        client = self.get_client_cls()
        if hasattr(client, "is_queue_enabled"):
            return client.is_queue_enabled
        return False
