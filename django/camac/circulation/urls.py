from rest_framework.routers import SimpleRouter

from . import views

r = SimpleRouter(trailing_slash=False)

r.register(r"circulations", views.CirculationView)
r.register(r"activations", views.ActivationView)

urlpatterns = r.urls
