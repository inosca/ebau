from rest_framework.routers import SimpleRouter

from . import views

r = SimpleRouter(trailing_slash=False)

r.register(r"dossier-imports", views.DossierImportView, "dossier-import")

urlpatterns = r.urls
