from django.conf.urls import url
from rest_framework.routers import SimpleRouter

from . import views

r = SimpleRouter(trailing_slash=False)

r.register(r"attachments", views.AttachmentView)
r.register(r"attachment-sections", views.AttachmentSectionView)
r.register(r"templates", views.TemplateView)
r.register(r"attachment-download-history", views.AttachmentDownloadHistoryView)


urlpatterns = [
    url(
        r"^(?P<path>attachments/files/.+\..+)$",
        views.AttachmentDownloadView.as_view({"get": "retrieve"}),
        name="attachment-download",
    ),
    url(
        r"^attachments/files/",
        views.AttachmentDownloadView.as_view({"get": "list"}),
        name="multi-attachment-download",
    ),
]

urlpatterns.extend(r.urls)
