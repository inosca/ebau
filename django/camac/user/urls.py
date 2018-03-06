from django.conf.urls import url
from rest_framework.routers import SimpleRouter

from . import views

r = SimpleRouter(trailing_slash=False)

r.register(r'locations', views.LocationView)

urlpatterns = [
    url(
        r'me',
        views.MeView.as_view(),
        name='me'
    ),
]

urlpatterns.extend(r.urls)
