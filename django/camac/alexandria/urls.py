from alexandria.core import views as alexandria_views
from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import PatchedDocumentViewSet, PatchedFileViewSet

r = SimpleRouter(trailing_slash=False)

# override the default viewset with our patched versions
# this needs to be updated when new urls are added in alexandria
r.register(r"categories", alexandria_views.CategoryViewSet)
r.register(r"documents", PatchedDocumentViewSet)
r.register(r"files", PatchedFileViewSet)
r.register(r"tags", alexandria_views.TagViewSet)
r.register(r"tagsynonymgroups", alexandria_views.TagSynonymGroupViewSet)

urlpatterns = r.urls

urlpatterns.append(path("hook", alexandria_views.hook_view, name="hook"))
