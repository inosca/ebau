from rest_framework.routers import SimpleRouter

from camac.alert_message import views

r = SimpleRouter(trailing_slash=False)

r.register(r"alert-messages", views.AlertMessageViewSet, "alert-message")

urlpatterns = r.urls
