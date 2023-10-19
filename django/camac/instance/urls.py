from django.urls import re_path
from rest_framework.routers import SimpleRouter

from . import views
from .export.views import InstanceExportView
from .placeholders.views import DMSPlaceholdersDocsView


class UnswaggeredInstanceView(views.InstanceView):
    swagger_schema = None


urlpatterns = [
    re_path(
        r"instances/export$",
        InstanceExportView.as_view(),
        name="instance-export",
    ),
    re_path(
        r"dms-placeholders-docs$",
        DMSPlaceholdersDocsView.as_view(),
        name="dms-placeholders-docs",
    ),
    re_path(
        r"form-config",
        views.FormConfigDownloadView.as_view(),
        name="form-config-download",
    ),
    re_path(
        r"public-caluma-instances",
        views.PublicCalumaInstanceView.as_view(),
        name="public-caluma-instance",
    ),
]

r = SimpleRouter(trailing_slash=False)
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


urlpatterns.extend(r.urls)
