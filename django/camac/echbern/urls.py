from django.conf import settings
from django.conf.urls import url
from django.urls import path
from django.views.generic.base import RedirectView

from .views import ApplicationsView, ApplicationView, EventView, MessageView, SendView

redirects = {
    "instance/<int:instance_id>/": "/page/index/instance-resource-id/20074/instance-id/%(instance_id)i",
    "ebau-number/<int:instance_id>/": "/taskform/taskform/index/instance-resource-id/12000002/instance-id/%(instance_id)i",
    "claim/<int:instance_id>/": "/claim/claim/index/instance-resource-id/150000/instance-id/%(instance_id)i",
    "dossier-check/<int:instance_id>/": "/page/index/instance-resource-id/150009/instance-id/%(instance_id)i",
    "revision-history/<int:instance_id>/": "/revisionhistory/revisionhistory/index/instance-resource-id/150004/instance-id/%(instance_id)i",
}

urlpatterns = []
if settings.APPLICATION.get("ECH_API"):
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
    ] + [path(key, RedirectView.as_view(url=url)) for key, url in redirects.items()]
