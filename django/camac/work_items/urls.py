from rest_framework.routers import SimpleRouter

from camac.work_items import views

r = SimpleRouter(trailing_slash=False)

r.register(r"work-item-templates", views.WorkItemTemplateViewset, "work-item-template")
r.register(
    r"work-item-list-filter-presets",
    views.WorkItemListFilterPresetViewset,
    "work-item-list-filter-preset",
)

urlpatterns = r.urls
