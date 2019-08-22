from django.conf.urls import url
from rest_framework.routers import SimpleRouter

from .views import GetNextView

r = SimpleRouter()

urlpatterns = [url(r"getNext", GetNextView.as_view(), name="getNext")]

urlpatterns += r.urls
