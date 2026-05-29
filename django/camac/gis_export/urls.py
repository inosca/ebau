from django.urls import re_path

from camac.gis_export import views

urlpatterns = [
    re_path(r"gis-export/so/?$", views.ExportSOGISView.as_view(), name="so-gis-export"),
]
