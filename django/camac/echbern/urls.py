from django.conf import settings
from django.conf.urls import url

from .views import ApplicationsView, ApplicationView, EventView, MessageView, SendView

urlpatterns = []
if settings.ECH_API:
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
        url(
            r"event/(?P<instance_id>(\d+))/(?P<event_type>(\w+))/?$",
            EventView.as_view({"post": "create"}),
            name="event",
        ),
        url(r"send/$", SendView.as_view({"post": "create"}), name="send"),
    ]
