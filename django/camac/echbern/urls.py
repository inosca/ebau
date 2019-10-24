from django.conf import settings
from django.conf.urls import url
from rest_framework.routers import SimpleRouter

from .views import ApplicationsView, ApplicationView, MessageView

urlpatterns = []
if settings.ECH_API:
    r = SimpleRouter()
    urlpatterns = [
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
        url(r"message/$", MessageView.as_view({"get": "retrieve"}), name="message"),
    ]
    urlpatterns += r.urls
