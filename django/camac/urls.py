from django.conf.urls import include, url

# TODO: Ensure that only the necessary routes are registered dependening on
# settings.APPLICATION_NAME

urlpatterns = [
    url(r"^api/v1/", include("camac.user.urls")),
    url(r"^api/v1/", include("camac.instance.urls")),
    url(r"^api/v1/", include("camac.document.urls")),
    url(r"^api/v1/", include("camac.circulation.urls")),
    url(r"^api/v1/", include("camac.notification.urls")),
    url(r"^api/v1/", include("gisbern.urls")),
]
