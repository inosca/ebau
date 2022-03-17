from django.urls import re_path
from rest_framework.routers import SimpleRouter

from . import views

r = SimpleRouter(trailing_slash=False)

r.register(r"locations", views.LocationView)
r.register(r"groups", views.GroupView)
r.register(r"public-groups", views.PublicGroupView, basename="publicgroup")
r.register(r"roles", views.RoleView)
r.register(r"services", views.ServiceView)
r.register(r"public-services", views.PublicServiceView, basename="publicservice")
r.register(r"users", views.UserView)
r.register(r"public-users", views.PublicUserView, basename="publicuser")

urlpatterns = [re_path(r"^me", views.MeView.as_view({"get": "retrieve"}), name="me")]

urlpatterns.extend(r.urls)
