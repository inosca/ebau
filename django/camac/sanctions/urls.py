from rest_framework.routers import SimpleRouter

from camac.sanctions import views

r = SimpleRouter(trailing_slash=False)

r.register(r"sanctions", views.SanctionsViewSet, "sanction")
r.register(r"sanction-templates", views.SanctionTemplatesViewSet, "sanction-template")

urlpatterns = r.urls
