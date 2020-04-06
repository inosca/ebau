from rest_framework.routers import SimpleRouter

from . import views

r = SimpleRouter(trailing_slash=False)

r.register(r"objection-timeframes", views.ObjectionTimeframeView)
r.register(r"objections", views.ObjectionView)
r.register(r"objection-participants", views.ObjectionParticipantView)

urlpatterns = r.urls
