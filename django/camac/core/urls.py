from rest_framework.routers import SimpleRouter

from . import views

r = SimpleRouter(trailing_slash=False)

r.register(r"publication-entries", views.PublicationEntryView, "publication")
r.register(r"authorities", views.AuthorityView, "authority")
r.register(r"workflow-entries", views.WorkflowEntryView, "workflow-entry")

urlpatterns = r.urls
