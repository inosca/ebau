from django.conf import settings
from django.conf.urls import url
from rest_framework.routers import SimpleRouter

from .views import GetNextView

urlpatterns = []
if settings.ECH_API:
    r = SimpleRouter()
    urlpatterns = [url(r"getNext", GetNextView.as_view(), name="getNext")]
    urlpatterns += r.urls
