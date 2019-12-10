from rest_framework.routers import SimpleRouter

from . import views

r = SimpleRouter(trailing_slash=False)

r.register(r"publication-entries", views.PublicationEntryView, "publication")
r.register(
    r"publication-entry-user-permissions",
    views.PublicationEntryUserPermissionView,
    "publication-permissions",
)

urlpatterns = r.urls
