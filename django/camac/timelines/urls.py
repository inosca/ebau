from rest_framework.routers import SimpleRouter

from . import views

urlpatterns = []

r = SimpleRouter(trailing_slash=False)
r.register(r"form-timelines", views.FormTimelineView, "form-timelines")

urlpatterns.extend(r.urls)
