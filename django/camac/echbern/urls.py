from django.conf import settings
from django.conf.urls import url
from rest_framework.routers import SimpleRouter

from .views import ApplicationsView, ApplicationView, GetNextView

urlpatterns = []
if settings.ECH_API:
    r = SimpleRouter()
    urlpatterns = [
        url(r"getNext", GetNextView.as_view(), name="getNext"),
        url(
            r"application/(?P<instance_id>\d+)/?$",
            ApplicationView.as_view({"get": "retrieve"}),
            name="application",
        ),
        url(
            r"applications",
            ApplicationsView.as_view({"get": "list"}),
            name="applications",
        ),
    ]
    urlpatterns += r.urls
