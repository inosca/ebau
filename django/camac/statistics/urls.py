from django.urls import re_path

from camac.statistics.views import (
    DossierStatisticsExportView,
    RPG2StatisticsExportView,
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
    re_path(
        r"rpg2$",
        RPG2StatisticsExportView.as_view(),
        name="statistics-rpg2",
    ),
]
