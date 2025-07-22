from django.urls import re_path

from .views import GeverSyncView

urlpatterns = [
    re_path(
        r"instances/(?P<instance_id>(\d+))/sync-gever/?$",
        GeverSyncView.as_view(),
        name="gever-sync",
    ),
]
