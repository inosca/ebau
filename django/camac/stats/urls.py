from django.conf.urls import url

from camac.stats.views import (
    ActivationSummaryView,
    ClaimSummaryView,
    InstanceSummaryView,
)

urlpatterns = [
    url(r"instances-summary", InstanceSummaryView.as_view(), name="instances-summary"),
    url(r"claims-summary", ClaimSummaryView.as_view(), name="claims-summary"),
    url(
        r"activations-summary",
        ActivationSummaryView.as_view(),
        name="activations-summary",
    ),
]
