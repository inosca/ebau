from django.urls import re_path

from camac.eeba_integration.views import EebaExportView, EebaIntegrationView

urlpatterns = [
    re_path(
        r"^instances/(?P<pk>\d+)/eeba_export/$",
        EebaExportView.as_view(),
        name="instance-eeba-export",
    ),
    re_path(
        r"^instances/(?P<pk>\d+)/eeba-integration/?$",
        EebaIntegrationView.as_view(),
        name="eeba-integration-create",
    ),
    re_path(
        r"^instances/(?P<pk>\d+)/eeba-integration/(?P<integration_id>[\w-]+)/?$",
        EebaIntegrationView.as_view(),
        name="eeba-integration-detail",
    ),
    re_path(
        r"^instances/(?P<pk>\d+)/eeba-integration/(?P<integration_id>[\w-]+)/(?P<retry_action>retry|rerun)/?$",
        EebaIntegrationView.as_view(),
        name="eeba-integration-retry",
    ),
]
