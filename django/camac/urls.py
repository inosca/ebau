from django.conf import settings
from django.conf.urls import include, url
from ebau_gwr.linker.views import GWRLinkViewSet
from ebau_gwr.token_proxy.views import TokenProxyView
from rest_framework.routers import SimpleRouter

from camac.caluma.views import CamacAuthenticatedGraphQLView
from camac.swagger.views import SCHEMA_VIEW

# TODO: Ensure that only the necessary routes are registered dependening on
# settings.APPLICATION_NAME


class UnswaggeredGWRLinkViewSet(GWRLinkViewSet):
    swagger_schema = None


class UnswaggeredTokenProxyView(TokenProxyView):
    swagger_schema = None


r = SimpleRouter(trailing_slash=False)

r.register(
    r"^api/v1/housing-stat-token",
    UnswaggeredTokenProxyView,
    basename="housingstattoken",
)
r.register(r"^api/v1/linker/gwr-links", UnswaggeredGWRLinkViewSet)

urlpatterns = [
    url(r"^api/v1/", include("camac.applicants.urls")),
    url(r"^api/v1/", include("camac.core.urls")),
    url(r"^api/v1/", include("camac.user.urls")),
    url(r"^api/v1/", include("camac.instance.urls")),
    url(r"^api/v1/", include("camac.document.urls")),
    url(r"^api/v1/", include("camac.dossier_import.urls")),
    url(r"^api/v1/", include("camac.circulation.urls")),
    url(r"^api/v1/", include("camac.notification.urls")),
    url(r"^api/v1/", include("camac.objection.urls")),
    url(r"^ech/v1/", include("camac.echbern.urls")),
    url(r"^api/v1/", include("gisbern.urls")),
    url(r"^api/v1/", include("camac.responsible.urls")),
    url(r"^api/v1/stats/", include("camac.stats.urls")),
    url(
        r"^api/swagger(?P<format>\.json|\.yaml)$",
        SCHEMA_VIEW.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    url(
        r"^api/swagger/$",
        SCHEMA_VIEW.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    url(
        r"^api/redoc/$",
        SCHEMA_VIEW.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
    url(
        r"^graphql",
        CamacAuthenticatedGraphQLView.as_view(graphiql=settings.DEBUG),
        name="graphql",
    ),
    # url(r'^api/docs/$', schema_view),
    # url(r'^api/auth/$', include('keycloak_adapter.urls')),
] + r.urls

if settings.ENABLE_SILK:  # pragma: no cover
    urlpatterns.append(url(r"^api/silk/", include("silk.urls", namespace="silk")))
