from django.conf import settings
from django.conf.urls import url
from rest_framework.routers import SimpleRouter

from . import views

r = SimpleRouter(trailing_slash=False)
urlpatterns = []

r.register(r"instance-states", views.InstanceStateView, "instance-state")
r.register(r"forms", views.FormView, "form")
r.register(r"instances", views.InstanceView, "instance")
r.register(r"form-fields", views.FormFieldView, "form-field")
r.register(
    r"instance-responsibilities",
    views.InstanceResponsibilityView,
    "instance-responsibility",
)
r.register(r"journal-entries", views.JournalEntryView, "journal-entry")
r.register(r"history-entries", views.HistoryEntryView, "history-entry")
r.register(r"issues", views.IssueView)
r.register(r"issue-templates", views.IssueTemplateView, "issue-template")
r.register(r"issue-template-sets", views.IssueTemplateSetView, "issue-template-set")

urlpatterns.append(
    url(
        r"form-config",
        views.FormConfigDownloadView.as_view(),
        name="form-config-download",
    )
)


def enable_public_caluma_instances():
    urlpatterns.append(
        url(
            r"public-caluma-instances",
            views.PublicCalumaInstanceView.as_view(),
            name="public-caluma-instance",
        )
    )


if settings.APPLICATION.get("ENABLE_PUBLIC_ENDPOINTS"):  # pragma: no cover
    enable_public_caluma_instances()

urlpatterns.extend(r.urls)
