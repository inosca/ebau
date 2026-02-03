from rest_framework.routers import SimpleRouter

from camac.deadlines import views

r = SimpleRouter(trailing_slash=False)

r.register(r"deadline-types", views.DeadlineTypeViewSet, "deadline-types")
r.register(r"suspension-reasons", views.SuspensionReasonViewSet, "suspension-reasons")
r.register(r"suspensions", views.SuspensionViewSet, "suspensions")
r.register(
    r"instance-deadlines",
    views.InstanceDeadlineViewSet,
    "instance-deadlines",
)

urlpatterns = r.urls
