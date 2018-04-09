from django.conf.urls import url
from rest_framework.routers import SimpleRouter

from . import views

r = SimpleRouter(trailing_slash=False)

r.register(r'locations', views.LocationView)
r.register(r'roles', views.RoleView)

urlpatterns = [
    url(
        r'^me',
        views.MeView.as_view(),
        name='me'
    ),
]

urlpatterns.extend(r.urls)
