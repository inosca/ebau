from django.conf import settings
from django.conf.urls import url
from rest_framework.routers import SimpleRouter

from .views import bern as be_views, schwyz as sz_views

r = SimpleRouter(trailing_slash=False)
urlpatterns = []

if settings.APPLICATION_NAME == "kt_schwyz":
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
            r"schwyz-form-config",
            sz_views.FormConfigDownloadView.as_view(),
            name="schwyz-form-config-download",
        )
    )

elif settings.APPLICATION_NAME == "kt_bern":
    r.register(r"instances", be_views.InstanceView, "instance")

elif settings.APPLICATION_NAME == "demo":

    r.register(r"bern-instances", be_views.InstanceView, "bern-instance")

    r.register(r"schwyz-forms", sz_views.FormView, "schwyz-form")
    r.register(r"schwyz-instances", sz_views.InstanceView, "schwyz-instance")
    r.register(r"schwyz-form-fields", sz_views.FormFieldView, "schwyz-form-field")
    r.register(
        r"schwyz-instance-states", sz_views.InstanceStateView, "schwyz-instance-state"
    )
    r.register(
        r"schwyz-instance-responsibilities",
        sz_views.InstanceResponsibilityView,
        "schwyz-instance-responsibility",
    )
    r.register(
        r"schwyz-journal-entries", sz_views.JournalEntryView, "schwyz-journal-entry"
    )
    r.register(r"schwyz-issues", sz_views.IssueView, "schwyz-issue")
    r.register(
        r"schwyz-issue-templates", sz_views.IssueTemplateView, "schwyz-issue-template"
    )
    r.register(
        r"schwyz-issue-template-sets",
        sz_views.IssueTemplateSetView,
        "schwyz-issue-template-set",
    )
    urlpatterns.append(
        url(
            r"schwyz-form-config",
            sz_views.FormConfigDownloadView.as_view(),
            name="schwyz-form-config-download",
        )
    )

urlpatterns.extend(r.urls)
