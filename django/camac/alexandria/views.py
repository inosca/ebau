from alexandria.core import views
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import BasePermission
from rest_framework_json_api.django_filters import DjangoFilterBackend

from camac.filters import MultilingualSearchFilter
from camac.user.permissions import DefaultPermission, PublicationPermission


class AlexandriaFileDownloadPermission(BasePermission):
    """Allow anonymous download of files.

    For file downloads we use presigned URLs so anonymous users can download a
    file if they use the correct presigned URL. This permission removes the
    condition of being authenticated and will always return true for the
    download action.
    """

    def has_permission(self, request, view):
        return (
            view.__class__.__name__ == "PatchedFileViewSet"
            and getattr(view, "action", None) == "download"
        )


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
    permission_classes = [
        DefaultPermission | PublicationPermission | AlexandriaFileDownloadPermission
    ]


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
