from rest_framework.routers import SimpleRouter

from camac.work_items import views

r = SimpleRouter(trailing_slash=False)

r.register(r"work-item-templates", views.WorkItemTemplateViewset, "work-item-template")

urlpatterns = r.urls
