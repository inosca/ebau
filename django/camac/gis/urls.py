from django.urls import re_path

from camac.gis.views import GISDataView

urlpatterns = [re_path(r"^data$", GISDataView.as_view(), name="gis-data")]