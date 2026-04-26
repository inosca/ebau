from django.urls import re_path

from camac.statistics.views import (
    DossierStatisticsExportView,
    WorkItemStatisticsExportView,
)

urlpatterns = [
    re_path(
        r"dossiers$",
        DossierStatisticsExportView.as_view(),
        name="statistics-dossiers",
    ),
    re_path(
        r"work-items$",
        WorkItemStatisticsExportView.as_view(),
        name="statistics-work-items",
    ),
]
