from django.urls import re_path

from camac.ech0211.views.kt_schwyz import ApplicationsView, ApplicationView

urlpatterns = [
    re_path(
        r"application/(?P<instance_id>\d+)/?$",
        ApplicationView.as_view({"get": "retrieve"}),
        name="application",
    ),
    re_path(
        r"applications",
        ApplicationsView.as_view({"get": "list"}),
        name="applications",
    ),
]
