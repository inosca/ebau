from django.urls import re_path

from camac.gis import views

urlpatterns = [
    re_path(
        r"^data/(?:(?P<task_id>[\w-]+)/)?$",
        views.GISDataView.as_view(),
        name="gis-data",
    ),
    re_path(
        r"^apply$",
        views.GISApplyView.as_view(),
        name="gis-apply",
    ),
]
