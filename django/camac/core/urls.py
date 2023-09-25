from rest_framework.routers import SimpleRouter

from . import views

r = SimpleRouter(trailing_slash=False)

r.register(r"publication-entries", views.PublicationEntryView, "publication")
r.register(r"authorities", views.AuthorityView, "authority")
r.register(r"workflow-entries", views.WorkflowEntryView, "workflow-entry")
r.register(r"resources", views.ResourceView, "resource")
r.register(r"instance-resources", views.InstanceResourceView, "instance-resource")
r.register(r"static-contents", views.StaticContentView, "static-content")

urlpatterns = r.urls
