from django.urls import re_path

from camac.stats.views import (
    ActivationSummaryView,
    ClaimSummaryView,
    InstancesCycleTimesView,
    InstanceSummaryView,
)

urlpatterns = [
    re_path(
        r"instances-summary", InstanceSummaryView.as_view(), name="instances-summary"
    ),
    re_path(r"claims-summary", ClaimSummaryView.as_view(), name="claims-summary"),
    re_path(
        r"activations-summary",
        ActivationSummaryView.as_view(),
        name="activations-summary",
    ),
    re_path(
        r"instances-cycle-times",
        InstancesCycleTimesView.as_view(),
        name="instances-cycle-times",
    ),
]
