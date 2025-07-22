from django.urls import re_path

from camac.eeba_integration.views import (
    EebaCheckIntegrationView,
    EebaExportView,
    EebaPatchIntegrationView,
)

urlpatterns = [
    re_path(
        r"^instances/(?P<pk>\d+)/eeba_export/$",
        EebaExportView.as_view(),
        name="instance-eeba-export",
    ),
    re_path(
        r"^instances/(?P<pk>\d+)/check-eeba-integration/?$",
        EebaCheckIntegrationView.as_view(),
        name="check-eeba-integration",
    ),
    re_path(
        r"^instances/(?P<pk>\d+)/patch-eeba-integration/?$",
        EebaPatchIntegrationView.as_view(),
        name="patch-eeba-integration",
    ),
]
