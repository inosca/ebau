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
    swagger_schema = None
    permission_classes = [DefaultPermission | PublicationPermission]
    filter_backends = [
        PatchedSearch,
        OrderingFilter,
        PatchedDjangoFilterBackend,
    ]


class PatchedFileViewSet(views.FileViewSet):
    swagger_schema = None
    permission_classes = [DefaultPermission | PublicationPermission]


class PatchedTagViewSet(views.TagViewSet):
    swagger_schema = None
    filter_backends = [
        PatchedSearch,
        OrderingFilter,
        PatchedDjangoFilterBackend,
    ]


class PatchedCategoryViewSet(views.CategoryViewSet):
    swagger_schema = None


class PatchedTagSynonymGroupViewSet(views.TagSynonymGroupViewSet):
    swagger_schema = None


class PatchedMarkViewSet(views.MarkViewSet):
    swagger_schema = None
    permission_classes = [DefaultPermission | PublicationPermission]
