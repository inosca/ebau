from django.urls import re_path
from rest_framework.routers import SimpleRouter

from .views import gis_data_view

r = SimpleRouter()

urlpatterns = [re_path(r"^egrid/(?P<egrid>.+)$", gis_data_view, name="egrid")]

urlpatterns += r.urls
