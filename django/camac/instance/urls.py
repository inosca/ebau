from django.conf import settings
from django.conf.urls import url
from rest_framework.routers import SimpleRouter

from .views import bern as be_views, schwyz as sz_views

r = SimpleRouter(trailing_slash=False)
urlpatterns = []

if settings.APPLICATION_NAME == "kt_schwyz":  # pragma: no cover
    r.register(r"forms", sz_views.FormView, "form")
    r.register(r"instances", sz_views.InstanceView, "instance")
    r.register(r"form-fields", sz_views.FormFieldView, "form-field")
    r.register(r"instance-states", sz_views.InstanceStateView, "instance-state")
    r.register(
        r"instance-responsibilities",
        sz_views.InstanceResponsibilityView,
        "instance-responsibility",
    )
    r.register(r"journal-entries", sz_views.JournalEntryView, "journal-entry")
    r.register(r"issues", sz_views.IssueView)
    r.register(r"issue-templates", sz_views.IssueTemplateView, "issue-template")
    r.register(
        r"issue-template-sets", sz_views.IssueTemplateSetView, "issue-template-set"
    )
    urlpatterns.append(
        url(
            r"form-config",
            sz_views.FormConfigDownloadView.as_view(),
            name="form-config-download",
        )
    )

elif settings.APPLICATION_NAME == "kt_bern":  # pragma: no cover
    r.register(r"instances", be_views.InstanceView, "instance")

elif settings.APPLICATION_NAME == "demo":
    # Demo uses a bunch of views from SZ

    r.register(r"forms", sz_views.FormView, "form")
    r.register(r"instances", sz_views.InstanceView, "instance")
    r.register(r"form-fields", sz_views.FormFieldView, "form-field")
    r.register(r"instance-states", sz_views.InstanceStateView, "instance-state")
    r.register(
        r"instance-responsibilities",
        sz_views.InstanceResponsibilityView,
        "instance-responsibility",
    )
    r.register(r"journal-entries", sz_views.JournalEntryView, "journal-entry")
    r.register(r"issues", sz_views.IssueView, "issue")
    r.register(r"issue-templates", sz_views.IssueTemplateView, "issue-template")
    r.register(
        r"issue-template-sets", sz_views.IssueTemplateSetView, "issue-template-set"
    )
    urlpatterns.append(
        url(
            r"form-config",
            sz_views.FormConfigDownloadView.as_view(),
            name="form-config-download",
        )
    )

urlpatterns.extend(r.urls)
