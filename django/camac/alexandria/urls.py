from alexandria.core import views as alexandria_views
from django.urls import path
from rest_framework.routers import SimpleRouter

from camac.alexandria import views

r = SimpleRouter(trailing_slash=False)

# override the default viewset with our patched versions
# this needs to be updated when new urls are added in alexandria
r.register(r"categories", views.PatchedCategoryViewSet)
r.register(r"documents", views.PatchedDocumentViewSet)
r.register(r"files", views.PatchedFileViewSet)
r.register(r"tags", views.PatchedTagViewSet)
r.register(r"tagsynonymgroups", views.PatchedTagSynonymGroupViewSet)
r.register(r"marks", views.PatchedMarkViewSet)

urlpatterns = r.urls

urlpatterns.append(path("hook", alexandria_views.hook_view, name="hook"))
