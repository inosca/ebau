from django.conf.urls import url
from rest_framework.routers import SimpleRouter

from . import views

r = SimpleRouter(trailing_slash=False)

r.register(r'attachments', views.AttachmentView, 'attachment')
r.register(r'attachment-sections', views.AttachmentSectionView,
           'attachment-section')


urlpatterns = [
    url(
        r'^(?P<path>attachments/files/.+\..+)$',
        views.AttachmentPathView.as_view(),
        name='attachment-download'
    ),
]

urlpatterns.extend(r.urls)
