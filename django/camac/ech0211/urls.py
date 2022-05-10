from django.urls import path, re_path
from django.views.generic import RedirectView

from camac.ech0211.views.kt_bern import (
    ApplicationsView as BEApplicationsView,
    ApplicationView as BEApplicationView,
    EventView as BEEventView,
    MessageView as BEMessageView,
    SendView as BESendView,
)
from camac.ech0211.views.kt_schwyz import (
    ApplicationsView as SZApplicationsView,
    ApplicationView as SZApplicationView,
)
from camac.swagger.views.kt_bern import SCHEMA_VIEW as BE_SCHEMA_VIEW
from camac.swagger.views.kt_schwyz import SCHEMA_VIEW as SZ_SCHEMA_VIEW


class SZUrlsConf:
    schema_view = SZ_SCHEMA_VIEW

    swagger_urlpatterns = [
        re_path(
            r"^api/swagger(?P<format>\.json|\.yaml)$",
            schema_view.without_ui(cache_timeout=0),
            name="schema-json",
        ),
        re_path(
            r"^api/swagger/$",
            schema_view.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        ),
        re_path(
            r"^api/redoc/$",
            schema_view.with_ui("redoc", cache_timeout=0),
            name="schema-redoc",
        ),
    ]

    urlpatterns = [
        re_path(
            r"application/(?P<instance_id>\d+)/?$",
            SZApplicationView.as_view({"get": "retrieve"}),
            name="application",
        ),
        re_path(
            r"applications",
            SZApplicationsView.as_view({"get": "list"}),
            name="applications",
        ),
    ] + swagger_urlpatterns


class BEUrlsConf:
    redirects = {
        "instance/<int:instance_id>/": "/page/index/instance-resource-id/20074/instance-id/%(instance_id)i",
        "ebau-number/<int:instance_id>/": "/taskform/taskform/index/instance-resource-id/12000002/instance-id/%(instance_id)i",
        "claim/<int:instance_id>/": "/claim/claim/index/instance-resource-id/150000/instance-id/%(instance_id)i",
        "dossier-check/<int:instance_id>/": "/page/index/instance-resource-id/150009/instance-id/%(instance_id)i",
        "revision-history/<int:instance_id>/": "/revisionhistory/revisionhistory/index/instance-resource-id/150004/instance-id/%(instance_id)i",
    }

    schema_view = BE_SCHEMA_VIEW

    swagger_urlpatterns = [
        re_path(
            r"^api/swagger(?P<format>\.json|\.yaml)$",
            schema_view.without_ui(cache_timeout=0),
            name="schema-json",
        ),
        re_path(
            r"^api/swagger/$",
            schema_view.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        ),
        re_path(
            r"^api/redoc/$",
            schema_view.with_ui("redoc", cache_timeout=0),
            name="schema-redoc",
        ),
    ]

    urlpatterns = (
        [
            re_path(
                r"application/(?P<instance_id>\d+)/?$",
                BEApplicationView.as_view({"get": "retrieve"}),
                name="application",
            ),
            re_path(
                r"applications",
                BEApplicationsView.as_view({"get": "list"}),
                name="applications",
            ),
            re_path(
                r"message/$", BEMessageView.as_view({"get": "retrieve"}), name="message"
            ),
            re_path(
                r"event/(?P<instance_id>(\d+))/(?P<event_type>(\w+))/?$",
                BEEventView.as_view({"post": "create"}),
                name="event",
            ),
            re_path(r"send/$", BESendView.as_view({"post": "create"}), name="send"),
        ]
        + [path(key, RedirectView.as_view(url=url)) for key, url in redirects.items()]
        + swagger_urlpatterns
    )
