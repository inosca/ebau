from django.urls import re_path
from rest_framework.routers import SimpleRouter

from camac.work_items import views

r = SimpleRouter(trailing_slash=False)

r.register(r"work-item-templates", views.WorkItemTemplateViewset, "work-item-template")
r.register(
    r"work-item-list-filter-presets",
    views.WorkItemListFilterPresetViewset,
    "work-item-list-filter-preset",
)
r.register(r"work-item-list-rows", views.WorkItemListRowViewset, "work-item-list-row")

urlpatterns = [
    *r.urls,
    re_path(
        r"^work-item-list-task-options",
        views.WorkItemListTaskOptionsView.as_view(),
        name="work-item-list-task-option-list",
    ),
]
