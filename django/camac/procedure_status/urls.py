from rest_framework.routers import SimpleRouter

from camac.procedure_status import views

r = SimpleRouter(trailing_slash=False)

r.register(r"status-timeline", views.StatusTimelineView, "status-timeline")

urlpatterns = r.urls
