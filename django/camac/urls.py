from django.conf import settings
from django.conf.urls import include
from django.contrib import admin
from django.urls import re_path

from camac.caluma.views import CamacAuthenticatedGraphQLView
from camac.swagger.views import get_swagger_view

# TODO: Ensure that only the necessary routes are registered dependening on
# settings.APPLICATION_NAME


schema_view = get_swagger_view()

urlpatterns = [
    re_path(r"^api/v1/", include("camac.applicants.urls")),
    re_path(r"^api/v1/", include("camac.core.urls")),
    re_path(r"^api/v1/", include("camac.user.urls")),
    re_path(r"^api/v1/", include("camac.instance.urls")),
    re_path(r"^api/v1/", include("camac.document.urls")),
    re_path(r"^api/v1/", include("camac.dossier_import.urls")),
    re_path(r"^api/v1/", include("camac.circulation.urls")),
    re_path(r"^api/v1/", include("camac.notification.urls")),
    re_path(r"^api/v1/", include("camac.objection.urls")),
    re_path(r"^api/v1/", include("camac.gisbern.urls")),
    re_path(r"^api/v1/", include("camac.responsible.urls")),
    re_path(r"^api/v1/", include("camac.communications.urls")),
    re_path(r"^api/v1/", include("camac.tags.urls")),
    re_path(r"^api/v1/", include("camac.billing.urls")),
    re_path(r"^api/v1/", include("camac.permissions.urls")),
    re_path(r"^api/v1/stats/", include("camac.stats.urls")),
    re_path(r"^api/v1/gis/", include("camac.gis.urls")),
    re_path(r"^api/v1/linker/", include("ebau_gwr.linker.urls")),
    re_path(r"^api/v1/", include("ebau_gwr.token_proxy.urls")),
    re_path(
        r"^graphql",
        CamacAuthenticatedGraphQLView.as_view(graphiql=settings.DEBUG),
        name="graphql",
    ),
    re_path(r"^alexandria/api/v1/", include("camac.alexandria.urls")),
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
    # Admin
    re_path(r"^django/admin/", admin.site.urls),
    re_path(r"^django/i18n/", include("django.conf.urls.i18n")),
    re_path(r"^django/oidc/", include("mozilla_django_oidc.urls")),
]

if settings.ECH0211:  # pragma: no cover
    urlpatterns += [re_path(r"^ech/v1/", include("camac.ech0211.urls"))]

if settings.ENABLE_SILK:  # pragma: no cover
    urlpatterns.append(re_path(r"^api/silk/", include("silk.urls", namespace="silk")))
