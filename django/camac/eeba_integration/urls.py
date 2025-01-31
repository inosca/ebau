from django.urls import re_path

from camac.eeba_integration.views import EebaExportView

urlpatterns = [
    re_path(
        r"^instances/(?P<pk>\d+)/eeba_export/$",
        EebaExportView.as_view(),
        name="instance-eeba-export",
    ),
]
