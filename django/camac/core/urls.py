from rest_framework.routers import SimpleRouter

from . import views

r = SimpleRouter(trailing_slash=False)

r.register(r"publication-entries", views.PublicationEntryView, "publication")
r.register(r"authorities", views.AuthorityView, "authority")

"""
This endpoint is disabled because the legality of it is not clear
revert !2353 to remove
r.register(
    r"publication-entry-user-permissions",
    views.PublicationEntryUserPermissionView,
    "publication-permissions",
)
"""

urlpatterns = r.urls
