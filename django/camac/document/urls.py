from django.conf import settings
from django.urls import re_path
from rest_framework.routers import SimpleRouter

from . import views


class UnswaggeredAttachmentView(views.AttachmentView):
    swagger_schema = None


class UnswaggeredAttachmentSectionView(views.AttachmentSectionView):
    swagger_schema = None


class UnswaggeredAttachmentDownloadView(views.AttachmentDownloadView):
    swagger_schema = None


r = SimpleRouter(trailing_slash=False)

r.register(
    r"attachments",
    UnswaggeredAttachmentView
    if "document" in settings.APPLICATION.get("EXCLUDE_DOCS", [])
    else views.AttachmentView,
)
r.register(
    r"attachment-sections",
    UnswaggeredAttachmentSectionView
    if "document" in settings.APPLICATION.get("EXCLUDE_DOCS", [])
    else views.AttachmentSectionView,
)
r.register(r"templates", views.TemplateView)
r.register(r"attachment-download-history", views.AttachmentDownloadHistoryView)

urlpatterns = [
    re_path(
        r"^(?P<path>attachments/files/.+\..+)$",
        UnswaggeredAttachmentDownloadView.as_view({"get": "retrieve"})
        if "document" in settings.APPLICATION.get("EXCLUDE_DOCS", [])
        else views.AttachmentDownloadView.as_view({"get": "retrieve"}),
        name="attachment-download",
    ),
    re_path(
        r"^attachments/files/",
        UnswaggeredAttachmentDownloadView.as_view({"get": "list"})
        if "document" in settings.APPLICATION.get("EXCLUDE_DOCS", [])
        else views.AttachmentDownloadView.as_view({"get": "list"}),
        name="multi-attachment-download",
    ),
]

urlpatterns.extend(r.urls)
