from django.conf.urls import include, url
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from camac.user.permissions import ViewPermissions

# TODO: Ensure that only the necessary routes are registered dependening on
# settings.APPLICATION_NAME


SWAGGER_DESCRIPTION = """\
# Gemeindeschnittstelle eBau

## Authentifizierung

Zur Authentifizierung wird der Standard [OpenID Connect](https://openid.net/connect/) genutzt. Pro Gemeindesoftware wird eine `client-id` und ein `client-secret` vergeben, mit welchen Tokens bezogen werden können:

```bash
curl --request POST \
--url 'https://ebau-test.sycloud.ch/auth/realms/camac/protocol/openid-connect/token' \
--header 'content-type: application/x-www-form-urlencoded' \
--data grant_type=client_credentials \
--data client_id='${client-id}' \
--data client_secret=${client-secret}
```

Mit einem gültigen Token können API-Abfragen gemacht werden. Nachfolgend ein paar Beispiele:

**Sichtbare Gesuche auflisten:**

```bash
curl -X GET "https://ebau-test.sycloud.ch/ech/v1/applications?group=123" -H "Authorization: Bearer ${TOKEN}"
```

**Gesuch-Details abfragen (BaseDelivery):**

```bash
curl -X GET "https://ebau-test.sycloud.ch/ech/v1/application/XYZ?group=123" -H "Authorization: Bearer ${TOKEN}"
```

Die verfügbaren Gruppen sind unter dem Endpoint `/api/v1/me` verfügbar:

```bash
curl -X GET "https://ebau-test.sycloud.ch/api/v1/me" -H "Authorization: Bearer ${TOKEN}"
```
"""

schema_view = get_schema_view(
    openapi.Info(
        title="Camac API", default_version="v1", description=SWAGGER_DESCRIPTION
    ),
    public=True,
    permission_classes=(ViewPermissions,),
)

urlpatterns = [
    url(r"^api/v1/", include("camac.applicants.urls")),
    url(r"^api/v1/", include("camac.user.urls")),
    url(r"^api/v1/", include("camac.instance.urls")),
    url(r"^api/v1/", include("camac.document.urls")),
    url(r"^api/v1/", include("camac.circulation.urls")),
    url(r"^api/v1/", include("camac.notification.urls")),
    url(r"^ech/v1/", include("camac.echbern.urls")),
    url(r"^api/v1/", include("gisbern.urls")),
    url(
        r"^api/swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    url(
        r"^api/swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    url(
        r"^api/redoc/$",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
    # url(r'^api/docs/$', schema_view),
    # url(r'^api/auth/$', include('keycloak_adapter.urls')),
]
