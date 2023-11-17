from alexandria.core import views
from rest_framework.filters import OrderingFilter
from rest_framework_json_api.django_filters import DjangoFilterBackend

from camac.filters import MultilingualSearchFilter
from camac.user.permissions import DefaultPermission, PublicationPermission


class PatchedDjangoFilterBackend(DjangoFilterBackend):
    search_param = "filter[search]"


class PatchedSearch(MultilingualSearchFilter):
    search_param = "filter[search]"


class PatchedDocumentViewSet(views.DocumentViewSet):
    permission_classes = [DefaultPermission | PublicationPermission]
    filter_backends = [
        PatchedSearch,
        OrderingFilter,
        PatchedDjangoFilterBackend,
    ]


class PatchedFileViewSet(views.FileViewSet):
    permission_classes = [DefaultPermission | PublicationPermission]


class PatchedTagViewSet(views.TagViewSet):
    filter_backends = [
        PatchedSearch,
        OrderingFilter,
        PatchedDjangoFilterBackend,
    ]
