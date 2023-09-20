from rest_framework.routers import SimpleRouter

from . import views

r = SimpleRouter(trailing_slash=False)

r.register(r"communications-topics", views.TopicView, "communications-topic")
r.register(r"communications-messages", views.MessageView, "communications-message")
r.register(
    r"communications-attachments", views.AttachmentView, "communications-attachment"
)

urlpatterns = r.urls
