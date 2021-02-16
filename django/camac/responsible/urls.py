from rest_framework.routers import SimpleRouter

from . import views

r = SimpleRouter(trailing_slash=False)

r.register(r"responsible-services", views.ResponsibleServiceView)

urlpatterns = r.urls
