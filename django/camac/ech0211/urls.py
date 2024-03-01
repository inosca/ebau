from django.conf import settings
from django.urls import path, re_path
from django.views.generic import RedirectView
from rest_framework.routers import SimpleRouter

from camac.ech0211 import views

r = SimpleRouter(trailing_slash=False)

r.register(r"files", views.ECHFileView, "ech-file")

urlpatterns = r.urls


urlpatterns += [
    re_path(
        r"application/(?P<instance_id>\d+)/?$",
        views.ApplicationView.as_view({"get": "retrieve"}),
        name="application",
    ),
    re_path(
        r"applications",
        views.ApplicationsView.as_view({"get": "list"}),
        name="applications",
    ),
    re_path(
        r"message/$", views.MessageView.as_view({"get": "retrieve"}), name="message"
    ),
    re_path(
        r"event/(?P<instance_id>(\d+))/(?P<event_type>(\w+))/?$",
        views.EventView.as_view({"post": "create"}),
        name="event",
    ),
    re_path(r"send/$", views.SendView.as_view({"post": "create"}), name="send"),
    *[
        path(key, RedirectView.as_view(url=url))
        for key, url in settings.ECH0211.get("REDIRECTS", {}).items()
    ],
]
