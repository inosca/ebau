from django.conf.urls import url
from rest_framework.routers import SimpleRouter

from .views import gis_data_view, save_gis_data_view

r = SimpleRouter()

urlpatterns = [
    url(
        r'^egrid/(?P<egrid>.+)$',
        gis_data_view,
        name="egrid"
    ),
    url(
        r'^saveGisData$',
        save_gis_data_view,
        name="save"
    )
]

urlpatterns += r.urls
