from rest_framework.routers import SimpleRouter

from .views import AccessLevelViewset, InstanceACLViewset, InstancePermissionsViewset

r = SimpleRouter(trailing_slash=False)

r.register(r"instance-acls", InstanceACLViewset, basename="instance-acls")
r.register(
    r"instance-permissions", InstancePermissionsViewset, basename="instance-permissions"
)
r.register(r"access-levels", AccessLevelViewset, basename="access-levels")


urlpatterns = r.urls
