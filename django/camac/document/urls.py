from rest_framework.routers import SimpleRouter

from . import views

r = SimpleRouter(trailing_slash=False)

r.register(r'attachments', views.AttachmentView, 'attachment')
r.register(r'attachment-sections', views.AttachmentSectionView,
           'attachment-section')

urlpatterns = r.urls
